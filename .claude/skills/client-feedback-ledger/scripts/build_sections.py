"""Turn verified entries into Client Feedback Log sections, in Jeremiah's format.

  python3 -I build_sections.py build <input.json> <page.txt> <out.md> <dropped.json>
  python3 -I build_sections.py check <out.md> <page_after.txt>

input.json: {"client_label": "MASON", "run_date": "2026-10-24", "pass": "connectors",
             "batches": [{"batch": "OCT WK2", "docs": [{kind,title,doc_id,url,owner}]}],
             "entries": [<verified entries>]}
page.txt:   the log page's current text (to skip anything already logged)

build writes nothing if every entry is already on the page.
check exits 1 unless every line of out.md is on the page, in order, at the end.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ledger  # noqa: E402

KIND_ORDER = ["main doc", "Snipes", "Quick response posts"]
PASS_LINES = {
    "connectors": ("Pass: connectors, {date} (comments, replies, Slack text). Browser pass pending: "
                   "version-history edits, suggestions, killed posts, net change, Slack images, Loom, "
                   "call transcripts."),
    "browser": "Pass: browser, {date}. All sources.",
    # Slack text added to a batch whose doc feedback (version history, comments)
    # is already in the log. Not marked pending, so it doesn't send the browser
    # pass back to this batch.
    "slack-addendum": "Pass: connectors, {date} (Slack text only). This batch's doc feedback is already logged above.",
}
MIN_TEXT_MATCH = 25  # shorter text ("ok", "approved") is too common to match safely


def clean(text):
    """Undo transport artifacts only: HTML entities the Docs API returns (&#39; -> ')
    and Google's soft line break (vertical tab), which is a line break in the doc."""
    return html.unescape(text).replace("\x0b", "\n")


def cell(text):
    text = clean(text)
    return text.replace("\r\n", "\n").replace("|", "\\|").replace("\n", "↵").replace("\t", "⇥")


def entry_id(e):
    return ledger.ledger_id(e["type"], e["source_id"], e["native_id"])


def already_logged(e, page, ids):
    if entry_id(e) in ids:
        return "Ledger ID already on page"
    v = e["verbatim"].strip()
    if len(v) >= MIN_TEXT_MATCH:
        for probe in (v, cell(v), v.replace("\n", " ")):
            if probe[:80] in page:
                return "same text already on page (manual entry)"
    return None


def batch_key(label):
    b = ledger.parse_batch(label)
    return (b[0], b[1]) if b else (99, 9)


def build(inp, page):
    ids = ledger.existing_ids(page)
    keep, dropped = [], []
    for e in inp["entries"]:
        why = already_logged(e, page, ids)
        (dropped if why else keep).append({**e, "_why": why} if why else e)
    if not keep:
        return "", dropped

    docs_by = {}
    for b in inp["batches"]:
        for d in b["docs"]:
            docs_by.setdefault((b["batch"], d["kind"]), []).append(d)

    sections = {}
    for e in keep:
        kind = "main doc" if e["doc_kind"] == "Slack only" else e["doc_kind"]
        sections.setdefault((e["batch"], kind), []).append(e)

    out = []
    for (batch, kind) in sorted(sections, key=lambda k: (batch_key(k[0]), KIND_ORDER.index(k[1]) if k[1] in KIND_ORDER else 9)):
        es = sections[(batch, kind)]
        docs = docs_by.get((batch, kind), [])
        links = " · ".join(f"[{d['title'].strip()}]({d['url']}) ({d['owner'].split('@')[0]})" for d in docs) or "no doc"
        slack = sorted({e["source_url"] for e in es if e["type"] == "slack"})
        src = f"Source: {links}" + (f" · Slack thread: {', '.join(slack)}" if slack else "")
        out += ["", f"## {inp['client_label']} | {batch} — {kind}", src,
                PASS_LINES[inp["pass"]].format(date=inp["run_date"])]

        posts = []
        for e in es:
            p = e["post"].strip() or "Batch-level"
            if p not in posts:
                posts.append(p)
        posts.sort(key=lambda p: p == "Batch-level")  # Batch-level last, else first-seen order
        for p in posts:
            pe = [e for e in es if (e["post"].strip() or "Batch-level") == p]
            out += ["", f"### {p}"]
            com = [e for e in pe if e["type"] in ("comment", "reply")]
            sl = [e for e in pe if e["type"] == "slack"]
            if com:
                out += ["", "**Comments** (including resolved and deleted)",
                        "| Date | Anchored on (exact) | Client (verbatim) | ID |", "| --- | --- | --- | --- |"]
                for e in com:
                    cut = "anchor cut off by Google Docs at ~1,000 characters" if (
                        len(e["anchored_on"]) > 900 and e["anchored_on"].rstrip().endswith("…")) else ""
                    who = " · ".join(x for x in [e["date_pht"], e["by"], "reply" if e["type"] == "reply" else "", e["tag"], cut] if x)
                    out.append(f"| {cell(who)} | {cell(e['anchored_on'])} | {cell(e['verbatim'])} | {entry_id(e)} |")
            if sl:
                out += ["", "**Outside the doc**",
                        "| Date | Source (Slack forwarded / relayed / image · Loom mm:ss · transcript) | Client (verbatim) | ID |",
                        "| --- | --- | --- | --- |"]
                for e in sl:
                    srcc = " ".join(x for x in ["Slack", e["tag"], f"[message]({e['source_url']})"] if x)
                    out.append(f"| {cell(e['date_pht'] + ' · ' + e['by'])} | {cell(srcc)} | {cell(e['verbatim'])} | {entry_id(e)} |")
    return "\n".join(out) + "\n", dropped


def _norm(s):
    """Same normalization for both sides: ClickUp rewrites links, bold, escapes
    and table separators when it saves, so compare the text underneath."""
    s = re.sub(r"\[([^\]]*)\]\(([^)]*)\)", r"\1", s)
    s = s.replace("**", "").replace("\\", "")
    s = re.sub(r"\|\s*-{3,}\s*", "|", s)
    return re.sub(r"\s+", " ", s).strip()


def check(md, page_after):
    """Every non-blank line of md appears in page_after, in order. Returns missing lines."""
    norm = _norm
    page_n = norm(page_after)
    missing, pos = [], 0
    for line in md.splitlines():
        if not line.strip():
            continue
        ln = norm(line)
        # tables and links render differently on read-back; compare the verbatim-bearing core
        if ln.startswith("|") and ln.count(" | ") >= 3:
            cells = ln.strip("| ").split(" | ")
            core = " | ".join(cells[2:4])  # verbatim + Ledger ID must both survive
        else:
            core = ln
        core = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", core)
        core = core.replace("**", "").lstrip("#").strip()
        if not core or set(core) <= set("-| "):
            continue
        i = page_n.find(core[:120], pos)
        if i < 0:
            missing.append(line)
        else:
            pos = i
    return missing


def main(argv):
    if argv[1] == "build":
        inp = json.load(open(argv[2]))
        page = open(argv[3]).read()
        md, dropped = build(inp, page)
        open(argv[4], "w").write(md)
        json.dump(dropped, open(argv[5], "w"), indent=1, ensure_ascii=False)
        print(f"sections_chars={len(md)} kept={len(inp['entries']) - len(dropped)} dropped={len(dropped)}")
        return 0
    if argv[1] == "check":
        missing = check(open(argv[2]).read(), open(argv[3]).read())
        if missing:
            print("MISSING:")
            for m in missing:
                print(" ", m[:160])
            return 1
        print("all lines present")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
