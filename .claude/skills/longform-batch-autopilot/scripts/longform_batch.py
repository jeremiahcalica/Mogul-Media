#!/usr/bin/env python3
"""Build the update_doc arguments that turn a copied longform doc into next week's shell.

Usage: longform_batch.py COPY_READ.json NEW_HEADER LINES.json [--entry-style HEADING_2|NORMAL_TEXT]

COPY_READ.json: read_doc result of the NEW COPY (raw doc JSON or {"content": {...}} / {"content": "<json>"}).
NEW_HEADER: "auto:<Mon>:<N>" (e.g. "auto:Oct:2") changes only the week number and month in last week's header,
            the way Jeremiah does it; or the full header text, e.g. "Mason L. - Week 2 - Oct".
LINES.json: JSON list of entry lines, e.g. "1 - (X/LI) - (...) - (Long-form)".
Prints {"documentId", "requests", "writeControl"} as JSON.
"""
import json, re, sys

TEXT_FIELDS = ("bold,italic,underline,strikethrough,smallCaps,backgroundColor,"
               "foregroundColor,fontSize,weightedFontFamily,baselineOffset,link")


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def load(path):
    d = json.load(open(path))
    if isinstance(d, dict) and "content" in d and "tabs" not in d and "body" not in d:
        d = d["content"]
        if isinstance(d, str):
            d = json.loads(d)
    return d


def para_text(p):
    return "".join(e.get("textRun", {}).get("content", "") for e in p["paragraph"]["elements"])


def main():
    args = sys.argv[1:]
    style = "HEADING_2"
    if "--entry-style" in args:
        i = args.index("--entry-style"); style = args[i + 1]; del args[i:i + 2]
    explicit_fonts = "--explicit-fonts" in args     # blank-skeleton docs: match the house Arial 20 / 16
    if explicit_fonts:
        args.remove("--explicit-fonts")
    doc_path, new_header, entries_path = args
    doc = load(doc_path)
    auto = re.fullmatch(r"auto:([A-Za-z]+):(\d+)", new_header)
    entries = json.load(open(entries_path))
    tabs = doc.get("tabs")
    if tabs and len(tabs) != 1:
        sys.exit("expected exactly one tab, found %d" % len(tabs))
    tab_id = tabs[0]["tabProperties"]["tabId"] if tabs else None
    body = (tabs[0]["documentTab"]["body"] if tabs else doc["body"])["content"]
    paras = [c for c in body if "paragraph" in c]

    header = paras[0]
    old_header = para_text(header).rstrip("\n")
    if header["paragraph"]["paragraphStyle"].get("namedStyleType") != "HEADING_1":
        sys.exit("first paragraph is not HEADING_1: %r" % old_header)
    if auto:
        # Loom 2: change only the week number (and the month, at a month change) in last week's own header
        mon, week = auto.group(1), auto.group(2)
        h = re.sub(r"\bWeek\s*\d+(?:\s*/\s*\d+)?", "Week " + week, old_header, count=1)
        h = re.sub(r"\b(Jan|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\b",
                   mon, h, count=1)
        if h == old_header and not re.search(r"\bWeek\s*%s\b" % week, old_header):
            sys.exit("could not find 'Week N' in the old header %r; pass the new header explicitly" % old_header)
        new_header = h

    media = [p for p in paras if para_text(p).strip().lower().startswith("media folder")]
    if len(media) != 1:
        sys.exit("expected one 'Media Folder' paragraph, found %d" % len(media))
    longforms = [p for p in paras if para_text(p).strip().upper() == "LONGFORMS"]
    if len(longforms) != 1:
        sys.exit("expected one 'LONGFORMS' paragraph, found %d" % len(longforms))
    lf = longforms[0]
    if media[0]["startIndex"] > lf["startIndex"]:
        sys.exit("'Media Folder' paragraph is after LONGFORMS; recipe assumes it is above")

    body_end = body[-1]["endIndex"]
    ins = lf["endIndex"]                      # start of first paragraph after LONGFORMS

    def rng(a, b):
        r = {"startIndex": a, "endIndex": b}
        if tab_id:
            r["tabId"] = tab_id
        return r

    reqs = []
    if explicit_fonts:
        # 0. the header block (header, Media Folder, LONGFORMS) in Arial 20; no length change, so it goes first
        reqs.append({"updateTextStyle": {"range": rng(1, lf["endIndex"]),
                     "textStyle": {"fontSize": {"magnitude": 20, "unit": "PT"},
                                   "weightedFontFamily": {"fontFamily": "Arial"}},
                     "fields": "fontSize,weightedFontFamily"}})
    # 1. delete everything after LONGFORMS (text, images, tables); the body's final newline stays
    if body_end - 1 > ins:
        reqs.append({"deleteContentRange": {"range": rng(ins, body_end - 1)}})
    # 2. insert the entries before the surviving final newline: "E1\n\nE2\n\n...En\n" + kept "\n"
    text = "".join(e + "\n\n" for e in entries)[:-1]
    if ins >= body_end:
        # LONGFORMS is the last paragraph (a blank skeleton): Google refuses an insert at the body end,
        # so insert "\n" + text just before LONGFORMS's own newline. Line 1 still starts at `ins`.
        loc = {"index": ins - 1}
        payload = "\n" + text
    else:
        loc = {"index": ins}
        payload = text
    if tab_id:
        loc["tabId"] = tab_id
    reqs.append({"insertText": {"location": loc, "text": payload}})
    end_ins = ins + u16(text)                 # index of the kept final newline (blank last paragraph)
    # 3. reset paragraph + text style over all new paragraphs incl. the final blank one
    reqs.append({"updateParagraphStyle": {"range": rng(ins, end_ins + 1),
                 "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"}, "fields": "namedStyleType"}})
    reqs.append({"updateTextStyle": {"range": rng(ins, end_ins + 1), "textStyle": {},
                 "fields": TEXT_FIELDS}})
    # 4. each entry line: entry style + bold (range includes its newline, as in the final Wk2 doc)
    pos = ins
    for e in entries:
        n = u16(e) + 1
        if style != "NORMAL_TEXT":
            reqs.append({"updateParagraphStyle": {"range": rng(pos, pos + n),
                         "paragraphStyle": {"namedStyleType": style}, "fields": "namedStyleType"}})
        ts, fields = {"bold": True}, "bold"
        if explicit_fonts:
            ts.update({"fontSize": {"magnitude": 16, "unit": "PT"}, "weightedFontFamily": {"fontFamily": "Arial"}})
            fields = "bold,fontSize,weightedFontFamily"
        reqs.append({"updateTextStyle": {"range": rng(pos, pos + n), "textStyle": ts, "fields": fields}})
        pos += n + 1                          # skip the blank paragraph
    # 5. optional: normalise LONGFORMS paragraph mark to bold only (Wk1 had red bg + strike on it)
    reqs.append({"updateTextStyle": {"range": rng(lf["endIndex"] - 1, lf["endIndex"]),
                 "textStyle": {"bold": True}, "fields": "bold,strikethrough,backgroundColor"}})
    # 5b. anything between the Media Folder line and LONGFORMS is last week's leftovers (Ben K's
    #     "Quick Response Post" block); the skeleton has nothing there, so remove it
    m_end, lf_start = media[0]["endIndex"], lf["startIndex"]
    if lf_start > m_end:
        reqs.append({"deleteContentRange": {"range": rng(m_end, lf_start)}})
    # 6. remove non-text elements (rich link / chip / image) from the Media Folder paragraph,
    #    keeping the label and its trailing space; done after all edits below it, highest first
    for el in sorted(media[0]["paragraph"]["elements"], key=lambda x: -x["startIndex"]):
        if "textRun" not in el:
            reqs.append({"deleteContentRange": {"range": rng(el["startIndex"], el["endIndex"])}})
        elif el["textRun"].get("textStyle", {}).get("link"):
            # plain hyperlinked text (no chip): delete the linked text itself
            reqs.append({"deleteContentRange": {"range": rng(el["startIndex"], el["endIndex"]
                         - (1 if el["textRun"]["content"].endswith("\n") else 0))}})
    # 6b. the label keeps one trailing space ("Media Folder: "), as in the real docs; a blank
    #     skeleton made from HTML loses it
    m_text = para_text(media[0])
    has_obj = any("textRun" not in el for el in media[0]["paragraph"]["elements"])
    if not has_obj and m_text.endswith(":\n"):
        mloc = {"index": media[0]["endIndex"] - 1}
        if tab_id:
            mloc["tabId"] = tab_id
        reqs.append({"insertText": {"location": mloc, "text": " "}})
        reqs.append({"updateTextStyle": {"range": rng(media[0]["endIndex"] - 1, media[0]["endIndex"]),
                     "textStyle": {}, "fields": "bold"}})     # the space isn't bold in the real docs
    # 7. header, index-free, last so a length change cannot shift the ranged requests above
    rat = {"replaceAllText": {"containsText": {"text": old_header, "matchCase": True},
                              "replaceText": new_header}}
    if tab_id:
        rat["replaceAllText"]["tabsCriteria"] = {"tabIds": [tab_id]}
    reqs.append(rat)

    print(json.dumps({"documentId": doc["documentId"], "requests": reqs,
                      "writeControl": {"requiredRevisionId": doc["revisionId"]}},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
