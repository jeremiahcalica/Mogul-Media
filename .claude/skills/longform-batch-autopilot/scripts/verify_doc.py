#!/usr/bin/env python3
"""Check a finished longform doc against its lines (SKILL.md Step 5.5, longform-doc.md step 6).

Usage:
  verify_doc.py READ.json LINES.json [--header "Mason L. - Week 2 - Oct"]
      READ.json: read_doc of the doc after the edit (raw, or the saved {"content": ...} form).
  verify_doc.py --md TEXT.md LINES.json [--header ...]
      TEXT.md: Drive read_file_content of the doc (short, so easy to save when read_doc came back inline).
      Checks the text and headings only; the style checks need the read_doc form.
Prints one line per check, then PASS or FAIL; exits 1 on any failure.
"""
import json, re, sys


def load(path):
    d = json.load(open(path))
    if isinstance(d, dict) and "content" in d and "tabs" not in d and "body" not in d:
        d = d["content"]
        if isinstance(d, str):
            d = json.loads(d)
    return d


def ptext(p):
    return "".join(e.get("textRun", {}).get("content", "") for e in p["paragraph"]["elements"])


def check_read(doc, lines, header):
    res = []
    tabs = doc.get("tabs") or []
    res.append(("one tab", len(tabs) == 1, "%d tabs" % len(tabs)))
    tab = tabs[0]["documentTab"] if tabs else doc
    body = [c for c in tab["body"]["content"] if "paragraph" in c]
    styles = {s["namedStyleType"]: s for s in tab.get("namedStyles", {}).get("styles", [])}
    mode = tab.get("documentStyle", {}).get("documentFormat", {}).get("documentMode")
    res.append(("pageless", mode == "PAGELESS", str(mode)))
    h2 = styles.get("HEADING_2", {}).get("textStyle", {})
    res.append(("Heading 2 style not bold (Clear formatting works)", not h2.get("bold"), json.dumps(h2)))
    h1 = styles.get("HEADING_1", {}).get("textStyle", {})
    res.append(("Heading 1 style not bold", not h1.get("bold"), json.dumps(h1)))
    objs = [e for p in body for e in p["paragraph"]["elements"] if "inlineObjectElement" in e]
    res.append(("no images left", not objs, "%d inline objects" % len(objs)))
    if len(body) < 3:
        res.append(("header block", False, "fewer than 3 paragraphs"))
        return res
    hd, mf, lf = body[0], body[1], body[2]
    ok = hd["paragraph"]["paragraphStyle"].get("namedStyleType") == "HEADING_1"
    if header:
        ok = ok and ptext(hd).rstrip("\n") == header
    res.append(("header", ok, repr(ptext(hd))))
    mf_ok = (ptext(mf) == "Media Folder: \n" and all("textRun" in e for e in mf["paragraph"]["elements"])
             and not any(e["textRun"].get("textStyle", {}).get("link") for e in mf["paragraph"]["elements"]))
    res.append(("Media Folder emptied (label + one space, no chip or link)", mf_ok, repr(ptext(mf))))
    res.append(("LONGFORMS", ptext(lf) == "LONGFORMS\n", repr(ptext(lf))))
    rest = body[3:]
    want = []
    for l in lines:
        want += [("HEADING_2", l + "\n"), ("NORMAL_TEXT", "\n")]
    got = [(p["paragraph"]["paragraphStyle"].get("namedStyleType"), ptext(p)) for p in rest]
    res.append(("lines match, each Heading 2 + one empty paragraph", got == want,
                "" if got == want else "first difference: %r vs %r" % next(
                    ((g, w) for g, w in zip(got + [None] * len(want), want + [None] * len(got)) if g != w), ("", ""))))
    bad = [ptext(p)[:40] for p in rest if p["paragraph"]["paragraphStyle"].get("namedStyleType") == "HEADING_2"
           and not all(e.get("textRun", {}).get("textStyle", {}).get("bold") for e in p["paragraph"]["elements"])]
    res.append(("bold on the text of every line", not bad, "not bold: %s" % bad if bad else ""))
    return res


def check_md(md, lines, header):
    rows = [r.strip() for r in md.splitlines() if r.strip() and r.strip() != "# Tab 1"]
    res = []
    unb = lambda r, lvl: re.fullmatch(r"#{%d}\s+\*\*(.*)\*\*\s*(.*)" % lvl, r)
    h = unb(rows[0], 1) if rows else None
    res.append(("header", bool(h) and (not header or h.group(1) == header), rows[0] if rows else ""))
    m = unb(rows[1], 1) if len(rows) > 1 else None
    res.append(("Media Folder emptied", bool(m) and m.group(1) == "Media Folder:" and not m.group(2),
                rows[1] if len(rows) > 1 else ""))
    res.append(("LONGFORMS", len(rows) > 2 and rows[2] == "# **LONGFORMS**", rows[2] if len(rows) > 2 else ""))
    got = []
    for r in rows[3:]:
        x = unb(r, 2)
        got.append(x.group(1) if x and not x.group(2) else "NOT A BOLD HEADING 2: " + r)
    res.append(("lines match, each a bold Heading 2", got == lines,
                "" if got == lines else "got %d lines, first difference: %r" % (len(got), next(
                    ((g, w) for g, w in zip(got + [None] * len(lines), lines + [None] * len(got)) if g != w), None))))
    return res


def main():
    a = sys.argv[1:]
    header = None
    if "--header" in a:
        i = a.index("--header"); header = a[i + 1]; del a[i:i + 2]
    md = "--md" in a
    if md:
        a.remove("--md")
    src, lines_path = a
    lines = json.load(open(lines_path))
    res = check_md(open(src).read(), lines, header) if md else check_read(load(src), lines, header)
    for name, ok, detail in res:
        print("%s  %s%s" % ("ok  " if ok else "FAIL", name, ("  (" + detail + ")") if detail and not ok else ""))
    fail = [r for r in res if not r[1]]
    print("PASS" if not fail else "FAIL")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
