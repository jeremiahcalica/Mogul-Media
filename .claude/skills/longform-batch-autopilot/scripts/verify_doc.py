#!/usr/bin/env python3
"""Check a finished longform doc against its lines (SKILL.md Step 5.5, longform-doc.md step 6).

Usage:
  verify_doc.py READ.json LINES.json [--header "Mason L. - Week 2 - Oct"]
      READ.json: read_doc of the doc after the edit: raw, the saved {"content": ...} form, or the
      minimal form below.
  verify_doc.py --md TEXT.md LINES.json [--header ...]
      TEXT.md: Drive read_file_content of the doc (short, so easy to save when read_doc came back inline).
      Checks the text and headings only; the style checks need a read_doc form.
Prints one line per check (ok / FAIL, or WARN for a difference that doesn't fail), then PASS or FAIL;
exits 1 on any failure.

Minimal form: for a read_doc result that came back inline and is too long to copy out whole. Write
a JSON file with exactly these keys, each copied from the read (all keys required):
  {"minimal": true,
   "tabs": 1,                    the number of entries in the read's "tabs" list
   "documentMode": "PAGELESS",   tabs[0].documentTab.documentStyle.documentFormat.documentMode,
                                 or null if the read has none
   "namedStyles": {              from tabs[0].documentTab.namedStyles.styles: for each style whose
                                 namedStyleType is HEADING_1, HEADING_2 (and NORMAL_TEXT if you can),
                                 that style's whole "textStyle" object, as read
     "HEADING_1": {"fontSize": {"magnitude": 20, "unit": "PT"}},
     "HEADING_2": {"bold": false, "fontSize": {"magnitude": 16, "unit": "PT"}}},
   "paragraphs": [               every item of tabs[0].documentTab.body.content after the sectionBreak,
                                 in order, from the header to the end of the body
     {"namedStyleType": "HEADING_1",          its paragraph.paragraphStyle.namedStyleType
      "elements": [{"textRun": {"content": "Mason L. - Week 2 - Oct\\n", "textStyle": {"bold": true}}}]},
     ...]}
  - A textRun keeps its "content" exactly as read (with its final "\\n") and, from its textStyle, only
    "bold" and "link" where the read has them ({} when it has neither).
  - Any other element is written as its kind with an empty object: {"inlineObjectElement": {}},
    {"richLink": {}}, {"person": {}}.
  - A table in the body is written in its place as {"table": {}}.
  - Copy every paragraph, the empty ones too ({"namedStyleType": "NORMAL_TEXT", "elements":
    [{"textRun": {"content": "\\n", "textStyle": {}}}]}).
longform_batch.py's {"subset": true, ...} form is accepted when it also carries "tabs",
"documentMode" and "namedStyles" and its paragraphs run to bodyEnd; otherwise this says what is missing.
"""
import json, re, sys

# Google's defaults, the house style of every client doc surveyed Oct 9 (longform-doc.md § Exceptions)
HOUSE = {"HEADING_1": (20, None), "HEADING_2": (16, None), "NORMAL_TEXT": (11, "Arial")}
NAMES = {"HEADING_1": "Heading 1", "HEADING_2": "Heading 2", "NORMAL_TEXT": "Normal text"}


def load(path):
    d = json.load(open(path))
    if isinstance(d, dict) and "content" in d and "tabs" not in d and "body" not in d:
        d = d["content"]
        if isinstance(d, str):
            d = json.loads(d)
    return d


def from_short(d):
    """The minimal or subset form as a read_doc dict, or a string naming what is missing."""
    kind = "minimal" if d.get("minimal") else "subset"
    if isinstance(d.get("paragraphs"), list):
        d = dict(d, paragraphs=[p for p in d["paragraphs"] if "sectionBreak" not in p])
    miss = [k for k in ("tabs", "documentMode", "namedStyles", "paragraphs") if k not in d]
    if not miss:
        ns = d["namedStyles"]
        if not isinstance(ns, dict):
            miss.append("namedStyles as {\"HEADING_1\": {textStyle}, ...}")
        for i, p in enumerate(d["paragraphs"]):
            if "table" in p:
                continue
            if "namedStyleType" not in p or not isinstance(p.get("elements"), list):
                miss.append("paragraphs[%d] namedStyleType and elements" % i)
            elif any("textRun" in e and "content" not in e["textRun"] for e in p["elements"]):
                miss.append("paragraphs[%d] textRun content" % i)
    if not miss and kind == "subset" and "bodyEnd" in d and d["paragraphs"]:
        last = d["paragraphs"][-1].get("endIndex")
        if last is not None and last != d["bodyEnd"]:
            miss.append("paragraphs to the end (they stop at %s, bodyEnd is %s: the batch's subset holds only"
                        " the paragraphs above the lines)" % (last, d["bodyEnd"]))
    if miss:
        return "the %s form lacks %s; write the minimal form in verify_doc.py's docstring" % (kind, ", ".join(miss))
    content = [{"sectionBreak": {}}]
    for p in d["paragraphs"]:
        if "table" in p:
            content.append({"table": p["table"]})
            continue
        els = [e if "textRun" not in e else {"textRun": {"content": e["textRun"]["content"],
                                                          "textStyle": e["textRun"].get("textStyle") or {}}}
               for e in p["elements"]]
        content.append({"paragraph": {"elements": els, "paragraphStyle": {"namedStyleType": p["namedStyleType"]}}})
    n = d["tabs"] if isinstance(d["tabs"], int) else len(d["tabs"])
    tab = {"body": {"content": content}, "documentStyle": {"documentFormat": {"documentMode": d["documentMode"]}},
           "namedStyles": {"styles": [{"namedStyleType": k, "textStyle": v} for k, v in d["namedStyles"].items()]}}
    return {"tabs": [{"documentTab": tab}] + [{}] * (n - 1)}


def ptext(p):
    return "".join(e.get("textRun", {}).get("content", "") for e in p["paragraph"]["elements"])


def size_warn(styles):
    diffs = []
    for k, (pt, font) in HOUSE.items():
        if k not in styles:
            continue
        ts = styles[k].get("textStyle") or {}
        got = ts.get("fontSize", {}).get("magnitude")
        if got != pt:
            size = "has no size in the read" if got is None else ("%g" % got) + "pt"
            diffs.append("%s %s, house %dpt" % (NAMES[k], size, pt))
        fam = ts.get("weightedFontFamily", {}).get("fontFamily")
        if font and fam and fam != font:
            diffs.append("%s font %s, house %s" % (NAMES[k], fam, font))
    return diffs


def check_read(doc, lines, header):
    res = []
    tabs = doc.get("tabs") or []
    res.append(("one tab", len(tabs) == 1, "%d tabs" % len(tabs)))
    tab = tabs[0]["documentTab"] if tabs else doc
    content = tab["body"]["content"]
    body = [c for c in content if "paragraph" in c]
    styles = {s["namedStyleType"]: s for s in tab.get("namedStyles", {}).get("styles", [])}
    mode = tab.get("documentStyle", {}).get("documentFormat", {}).get("documentMode")
    res.append(("pageless", mode == "PAGELESS", str(mode)))
    # a read without the named styles used to pass "not bold" silently (Nathan C Oct Wk2 test flight)
    for k, why in (("HEADING_2", " (Clear formatting works)"), ("HEADING_1", "")):
        ts = styles.get(k, {}).get("textStyle")
        res.append(("%s style in the read and not bold%s" % (NAMES[k], why), ts is not None and not ts.get("bold"),
                    "%s missing from the read's namedStyles" % k if ts is None else json.dumps(ts)))
    diffs = size_warn(styles)
    res.append(("style sizes match the house style (Heading 1 20pt, Heading 2 16pt, Normal text Arial 11)",
                True if not diffs else None, "; ".join(diffs) + " (a client can have custom styles)" if diffs else ""))
    objs = [e for p in body for e in p["paragraph"]["elements"] if "inlineObjectElement" in e]
    res.append(("no images left", not objs, "%d inline objects" % len(objs)))
    tables = [c for c in content if "table" in c]
    res.append(("no tables left", not tables, "%d tables" % len(tables)))
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
    rows = [r.strip() for r in md.splitlines() if r.strip()]
    unb = lambda r, lvl: re.fullmatch(r"#{%d}\s+\*\*(.*)\*\*\s*(.*)" % lvl, r)
    # read_file_content opens with the tab's title as an unbolded H1 ("# Tab 1", "# Content", Josh C Oct Wk2);
    # a bold first H1 is the doc's own header and stays
    if rows and re.match(r"#\s", rows[0]) and not unb(rows[0], 1):
        rows = rows[1:]
    res = []
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
    if md:
        res = check_md(open(src).read(), lines, header)
    else:
        doc = load(src)
        if isinstance(doc, dict) and (doc.get("minimal") or doc.get("subset")):
            doc = from_short(doc)
        res = [("read form", False, doc)] if isinstance(doc, str) else check_read(doc, lines, header)
    for name, ok, detail in res:
        tag = "WARN" if ok is None else "ok  " if ok else "FAIL"
        print("%s  %s%s" % (tag, name, ("  (" + detail + ")") if detail and not ok else ""))
    fail = [r for r in res if r[1] is False]
    print("PASS" if not fail else "FAIL")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
