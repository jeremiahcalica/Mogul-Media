#!/usr/bin/env python3
"""Pull the rows of one table out of the "Next Week: Topics and Content Batches" Claude Doc.

Usage: python3 -I schedule_rows.py SAVED_READ [--table "Content batches (long-forms)"]

SAVED_READ is the saved result of a full Claude Docs read of the doc's body (mcp__Claude_Docs__read with
ref {"object":"node","id":<body id>}, engine "prose", no payload). The harness saves it as plain JSON
{"verdict","rev","data":{"xml",...}}, as a JSON array [{"type":"text","text":"<that JSON>"}], or the
file may already be the bare XML; all three are handled.

Prints JSON: {"rev": N, "title": "...", "table": "...", "rows": [
  {"due": "2026-10-12", "client": "Mason", "pod_note": "", "checked": false, "status": "In progress",
   "clickup_date": "Oct 13", "task_id": "12439gnqare", "task_label": "OCT WK2 Longforms", "notes": "..."}]}
Columns are matched by header text, never by position (the order changes between weeks).
"""
import json, re, sys
import xml.etree.ElementTree as ET


def load_xml(path):
    s = open(path, encoding="utf-8").read().strip()
    if s.startswith("<"):
        return s
    d = json.loads(s)
    if isinstance(d, list):
        d = json.loads("".join(p.get("text", "") for p in d if isinstance(p, dict)))
    if isinstance(d, dict) and "data" in d:
        d = d["data"]
    return d["xml"] if isinstance(d, dict) else d


def text_of(el):
    """Visible text of an element, with date chips as their ISO value."""
    out = []
    for node in el.iter():
        if node.tag == "date":
            out.append(node.get("value", ""))
        elif node.tag == "mention":
            out.append("@" + node.get("name", ""))
        elif node.text and node.tag not in ("date", "mention"):
            out.append(node.text)
        if node is not el and node.tail:
            out.append(node.tail)
    return re.sub(r"\s+", " ", "".join(out)).strip()


def cell_text(cell):
    return re.sub(r"\s+", " ", "".join(
        (n.get("value", "") if n.tag == "date" else (n.text or "")) + (n.tail or "")
        for n in cell.iter() if n is not cell)).strip()


def main():
    args = sys.argv[1:]
    want = "Content batches (long-forms)"
    if "--table" in args:
        i = args.index("--table"); want = args[i + 1]; del args[i:i + 2]
    root = ET.fromstring(load_xml(args[0]))
    title = ""
    heading, rows_out, found = None, [], False
    for el in root:
        if el.tag == "paragraph" and el.get("heading") == "1" and not title:
            title = text_of(el)
        if el.tag == "paragraph" and el.get("heading"):
            heading = text_of(el)
            continue
        if el.tag == "table" and heading and heading.strip().lower() == want.lower() and not found:
            found = True
            rows = list(el)
            hdr = [cell_text(c).lower() for c in rows[0]]

            def col(*names):
                for n in names:
                    for i, h in enumerate(hdr):
                        if h.startswith(n):
                            return i
                return None
            c_due, c_client, c_status = col("due"), col("client"), col("status")
            c_cu_date, c_task, c_notes = col("clickup date"), col("clickup task"), col("notes")
            for r in rows[1:]:
                cells = list(r)
                get = lambda i: cells[i] if i is not None and i < len(cells) else None
                cl = get(c_client)
                li = cl.find(".//listItem") if cl is not None else None
                client_full = cell_text(cl) if cl is not None else ""
                m = re.match(r"(.*?)\s*\((.*)\)\s*$", client_full)
                link = get(c_task).find(".//link") if get(c_task) is not None else None
                href = link.get("href", "") if link is not None else ""
                tid = re.search(r"/t/([A-Za-z0-9]+)", href)
                rows_out.append({
                    "due": cell_text(get(c_due)) if get(c_due) is not None else "",
                    "client": (m.group(1) if m else client_full).strip(),
                    "pod_note": (m.group(2) if m else "").strip(),
                    "checked": bool(li is not None and li.get("checked") == "true"),
                    "status": cell_text(get(c_status)) if get(c_status) is not None else "",
                    "clickup_date": cell_text(get(c_cu_date)) if get(c_cu_date) is not None else "",
                    "task_id": tid.group(1) if tid else "",
                    "task_label": cell_text(get(c_task)) if get(c_task) is not None else "",
                    "notes": cell_text(get(c_notes)) if get(c_notes) is not None else "",
                })
    if not found:
        sys.exit("table under heading %r not found" % want)
    print(json.dumps({"rev": root.get("rev"), "title": title, "table": want, "rows": rows_out},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
