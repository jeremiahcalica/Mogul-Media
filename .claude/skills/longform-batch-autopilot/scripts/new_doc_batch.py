#!/usr/bin/env python3
"""Fill an EMPTY native Google Doc with a new client's first longform doc, formatted like the copied docs.

Usage: new_doc_batch.py BLANK_READ.json "<Name> - Week <N> - <Mon>" LINES.json

Why not HTML: a doc imported from HTML gets the import's named styles (Heading 1 bold 24pt, Heading 2
bold 18pt) and no formatting on the text itself, so Clear formatting does nothing in it (Nathan C.,
Oct 9). The Docs API can apply a named style but never change one. An empty doc made with Drive
`create_file` (contentMimeType application/vnd.google-apps.document, no content) has Google's
default named styles, the same as every copied client doc (Heading 1 20pt, Heading 2 16pt, neither
bold; Normal text Arial 11). This batch then puts the bold on the text, exactly as in Mason's doc:
  header line (incl. its newline) bold, Heading 1
  "Media Folder:" bold, then " " not bold, Heading 1
  "LONGFORMS" (incl. its newline) bold, Heading 1
  each entry line (incl. its newline) bold, Heading 2, followed by one empty Normal text paragraph.

BLANK_READ.json: read_doc of the new empty doc (raw, or {"content": {...}} / {"content": "<json>"}).
Prints {"documentId", "requests", "writeControl"} for one guarded update_doc call.
"""
import json, sys

TEXT_FIELDS = ("bold,italic,underline,strikethrough,smallCaps,backgroundColor,"
               "foregroundColor,fontSize,weightedFontFamily,baselineOffset,link")
LABEL = "Media Folder:"


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def load(path):
    d = json.load(open(path))
    if isinstance(d, dict) and "content" in d and "tabs" not in d and "body" not in d:
        d = d["content"]
        if isinstance(d, str):
            d = json.loads(d)
    return d


def main():
    doc_path, header, lines_path = sys.argv[1:4]
    doc = load(doc_path)
    lines = json.load(open(lines_path))
    if not lines:
        sys.exit("no entry lines")
    tabs = doc.get("tabs")
    if tabs and len(tabs) != 1:
        sys.exit("expected exactly one tab, found %d" % len(tabs))
    tab_id = tabs[0]["tabProperties"]["tabId"] if tabs else None
    body = (tabs[0]["documentTab"]["body"] if tabs else doc["body"])["content"]
    paras = [c for c in body if "paragraph" in c]
    text_now = "".join(e.get("textRun", {}).get("content", "")
                       for p in paras for e in p["paragraph"]["elements"])
    if len(paras) != 1 or text_now != "\n" or any("textRun" not in e for e in paras[0]["paragraph"]["elements"]):
        sys.exit("this is not an empty doc (found %d paragraphs, %r): never overwrite content" % (len(paras), text_now[:80]))
    start = paras[0]["startIndex"]                       # 1 in a new doc

    def rng(a, b):
        r = {"startIndex": a, "endIndex": b}
        if tab_id:
            r["tabId"] = tab_id
        return r

    head = [header, LABEL + " ", "LONGFORMS"]
    text = "".join(h + "\n" for h in head) + "".join(l + "\n\n" for l in lines)[:-1]
    # the doc's own final newline stays after the text, as the empty paragraph after the last line
    end = start + u16(text)
    loc = {"index": start}
    if tab_id:
        loc["tabId"] = tab_id
    reqs = [{"insertText": {"location": loc, "text": text}}]
    # start clean: everything Normal text, no text formatting (incl. the final empty paragraph)
    reqs.append({"updateParagraphStyle": {"range": rng(start, end + 1),
                 "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"}, "fields": "namedStyleType"}})
    reqs.append({"updateTextStyle": {"range": rng(start, end + 1), "textStyle": {}, "fields": TEXT_FIELDS}})
    # header block: three Heading 1 paragraphs
    pos = start
    spans = []
    for h in head:
        spans.append((pos, pos + u16(h) + 1))
        pos += u16(h) + 1
    reqs.append({"updateParagraphStyle": {"range": rng(spans[0][0], spans[2][1]),
                 "paragraphStyle": {"namedStyleType": "HEADING_1"}, "fields": "namedStyleType"}})
    bold = {"textStyle": {"bold": True}, "fields": "bold"}
    reqs.append({"updateTextStyle": dict(range=rng(*spans[0]), **bold)})                       # header + newline
    reqs.append({"updateTextStyle": dict(range=rng(spans[1][0], spans[1][0] + u16(LABEL)), **bold)})  # label only
    reqs.append({"updateTextStyle": dict(range=rng(*spans[2]), **bold)})                       # LONGFORMS + newline
    # entry lines: Heading 2 + bold, newline included; the empty paragraph after each stays Normal text
    for l in lines:
        n = u16(l) + 1
        reqs.append({"updateParagraphStyle": {"range": rng(pos, pos + n),
                     "paragraphStyle": {"namedStyleType": "HEADING_2"}, "fields": "namedStyleType"}})
        reqs.append({"updateTextStyle": dict(range=rng(pos, pos + n), **bold)})
        pos += n + 1
    print(json.dumps({"documentId": doc["documentId"], "requests": reqs,
                      "writeControl": {"requiredRevisionId": doc["revisionId"]}}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
