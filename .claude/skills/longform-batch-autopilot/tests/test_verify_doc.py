#!/usr/bin/env python3
"""verify_doc.py must pass Jeremiah's real Caulen Oct Wk2 doc (Drive markdown) and a doc built by
new_doc_batch.py, and must fail a doc whose bold sits in the Heading 2 style (the HTML-import bug)."""
import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import simulate_docs_batch as sim
V = os.path.join(here, "..", "scripts", "verify_doc.py")
tmp = lambda name: os.path.join(here, "_" + name)
fails = 0

def run(args):
    return subprocess.run([sys.executable, "-I", V] + args, capture_output=True, text=True).returncode

clines = open(os.path.join(here, "caulen_oct_wk2_expected.txt"), encoding="utf-8").read().splitlines()
json.dump(clines, open(tmp("c.json"), "w"))
fails += run(["--md", os.path.join(here, "caulen_oct_wk2_real.md"), tmp("c.json"), "--header", "Caulen F. - Week 2 - Oct"]) != 0

# a doc built from an empty doc, turned back into read_doc form
mlines = open(os.path.join(here, "mason_oct_wk2_expected.txt"), encoding="utf-8").read().splitlines()
json.dump(mlines, open(tmp("m.json"), "w"))
batch = json.loads(subprocess.run([sys.executable, "-I", os.path.join(here, "..", "scripts", "new_doc_batch.py"),
                                   os.path.join(here, "blank_doc_read.json"), "Mason L. - Week 2 - Oct", tmp("m.json")],
                                  capture_output=True, text=True, check=True).stdout)
cells = sim.cells_from(sim.load(os.path.join(here, "blank_doc_read.json")))
for r in batch["requests"]:
    sim.apply(cells, r)
def as_read(h2_bold):
    content = [{"endIndex": 1, "sectionBreak": {}}]
    for s, e, ps, runs in sim.paragraphs(cells):
        els, i = [], s
        for t, st in runs:
            els.append({"startIndex": i, "endIndex": i + len(t), "textRun": {"content": t, "textStyle": st}}); i += len(t)
        content.append({"startIndex": s, "endIndex": e, "paragraph": {"elements": els, "paragraphStyle": {"namedStyleType": ps}}})
    return {"documentId": "D", "revisionId": "R", "tabs": [{"tabProperties": {"tabId": "t.0"}, "documentTab": {
        "body": {"content": content}, "documentStyle": {"documentFormat": {"documentMode": "PAGELESS"}},
        "namedStyles": {"styles": [{"namedStyleType": "HEADING_1", "textStyle": {"fontSize": {"magnitude": 20}}},
                                   {"namedStyleType": "HEADING_2", "textStyle": {"bold": h2_bold, "fontSize": {"magnitude": 16}}}]}}}]}
json.dump(as_read(False), open(tmp("good.json"), "w"))
json.dump(as_read(True), open(tmp("bad.json"), "w"))
fails += run([tmp("good.json"), tmp("m.json"), "--header", "Mason L. - Week 2 - Oct"]) != 0
fails += run([tmp("bad.json"), tmp("m.json")]) == 0          # must FAIL: bold baked into Heading 2
for n in ("c.json", "m.json", "good.json", "bad.json"):
    os.remove(tmp(n))
print("ok     verify_doc" if not fails else "FAIL   verify_doc")
sys.exit(1 if fails else 0)
