#!/usr/bin/env python3
"""Offline simulation of a Docs batchUpdate over a read_doc body (single tab), to check index math.
Model: one cell per UTF-16 unit; paragraph style stored on the paragraph's newline."""
import json, sys, copy

def load(path):
    d = json.load(open(path))
    if "content" in d and "tabs" not in d:
        d = d["content"]
        if isinstance(d, str): d = json.loads(d)
    return d

def cells_from(doc):
    body = doc["tabs"][0]["documentTab"]["body"]["content"]
    cells = [None]  # index 0 = section break placeholder
    for c in body:
        if "paragraph" not in c: continue
        ps = c["paragraph"]["paragraphStyle"].get("namedStyleType")
        for el in c["paragraph"]["elements"]:
            if "textRun" in el:
                s = el["textRun"]["content"]
                ts = el["textRun"].get("textStyle", {})
                units = []
                for ch in s:
                    units.append(ch)
                    if ord(ch) > 0xFFFF: units.append("")
                for ch in units:
                    cells.append({"ch": ch, "ts": dict(ts), "ps": ps if ch == "\n" else None})
            else:
                kind = [k for k in el if k not in ("startIndex", "endIndex")][0]
                cells.append({"ch": "￼", "ts": {}, "ps": None, "obj": kind})
        assert len(cells) == c["endIndex"], (len(cells), c["endIndex"])
    return cells

def para_of(cells, i):
    j = i
    while cells[j]["ch"] != "\n": j += 1
    return j  # index of the paragraph's newline

def apply(cells, req):
    (k, v), = req.items()
    if k == "deleteContentRange":
        a, b = v["range"]["startIndex"], v["range"]["endIndex"]
        assert b < len(cells), "cannot delete final newline"
        del cells[a:b]
    elif k == "insertText":
        i = v["location"]["index"]; t = v["text"]
        nl = para_of(cells, i)
        para_start = i == 1 or cells[i - 1]["ch"] == "\n"
        src = cells[i] if para_start else cells[i - 1]
        new = []
        for ch in t:
            new.append({"ch": ch, "ts": dict(src["ts"]), "ps": cells[nl]["ps"] if ch == "\n" else None})
        cells[i:i] = new
    elif k == "updateParagraphStyle":
        a, b = v["range"]["startIndex"], v["range"]["endIndex"]
        assert b <= len(cells)
        i = a
        while i < b:
            nl = para_of(cells, i)
            cells[nl]["ps"] = v["paragraphStyle"]["namedStyleType"]
            i = nl + 1
    elif k == "updateTextStyle":
        a, b = v["range"]["startIndex"], v["range"]["endIndex"]
        assert b <= len(cells)
        for c in cells[a:b]:
            for f in v["fields"].split(","):
                if f in v["textStyle"]: c["ts"][f] = v["textStyle"][f]
                else: c["ts"].pop(f, None)
    elif k == "replaceAllText":
        find = v["containsText"]["text"]; rep = v["replaceText"]
        s = "".join(c["ch"] for c in cells[1:])
        n = s.count(find); assert n == 1, n
        p = s.index(find) + 1
        ts = cells[p]["ts"]
        cells[p:p + len(find)] = [{"ch": ch, "ts": dict(ts), "ps": None} for ch in rep]
        print("replaceAllText occurrences:", n, file=sys.stderr)
    else:
        raise SystemExit("unhandled " + k)

def paragraphs(cells):
    out, start = [], 1
    for i in range(1, len(cells)):
        if cells[i]["ch"] == "\n":
            seg = cells[start:i + 1]
            runs = []
            for c in seg:
                if runs and runs[-1][1] == c["ts"]: runs[-1][0] += c["ch"]
                else: runs.append([c["ch"], c["ts"]])
            out.append((start, i + 1, cells[i]["ps"], [(t, s) for t, s in runs]))
            start = i + 1
    return out

if __name__ == "__main__":
    doc = load(sys.argv[1]); batch = json.load(open(sys.argv[2]))
    cells = cells_from(doc)
    for r in batch["requests"]: apply(cells, r)
    objs = [c for c in cells[1:] if c.get("obj")]
    print("non-text objects left:", [c["obj"] for c in objs])
    for s, e, ps, runs in paragraphs(cells):
        print(f"{s}-{e} {ps}: " + " | ".join(f"{t[:40]!r}{json.dumps(st, sort_keys=True)}" for t, st in runs))
