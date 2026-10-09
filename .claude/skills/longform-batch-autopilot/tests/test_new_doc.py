#!/usr/bin/env python3
"""new_doc_batch.py on an empty doc must give the exact structure of Jeremiah's real Mason Oct Wk2 doc:
same paragraph boundaries, paragraph styles and text formatting (bold on the text, not in the styles),
so Clear formatting behaves the same as in his copied docs. Run: python3 -I tests/test_new_doc.py"""
import json, os, shutil, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import simulate_docs_batch as sim

lines = open(os.path.join(here, "mason_oct_wk2_expected.txt"), encoding="utf-8").read().splitlines()
tmp = tempfile.mkdtemp()
lp = os.path.join(tmp, "lines.json")
json.dump(lines, open(lp, "w"))
out = subprocess.run([sys.executable, "-I", os.path.join(here, "..", "scripts", "new_doc_batch.py"),
                      os.path.join(here, "blank_doc_read.json"), "Mason L. - Week 2 - Oct", lp],
                     capture_output=True, text=True, check=True).stdout
shutil.rmtree(tmp)
batch = json.loads(out)
cells = sim.cells_from(sim.load(os.path.join(here, "blank_doc_read.json")))
for r in batch["requests"]:
    sim.apply(cells, r)
got = sim.paragraphs(cells)

B = {"bold": True}
want = [(1, 25, "HEADING_1", [("Mason L. - Week 2 - Oct\n", B)]),
        (25, 40, "HEADING_1", [("Media Folder:", B), (" \n", {})]),
        (40, 50, "HEADING_1", [("LONGFORMS\n", B)])]
# paragraph ends of the real doc 167ngEIEU_hgNP-ML1vPBL_NslV7YtK5InF9wQ4s3jOc (read Oct 9)
real_ends = [215, 216, 287, 288, 359, 360, 486, 487, 597, 598, 773, 774, 936, 937, 1103, 1104]
pos = 50
for i, l in enumerate(lines):
    want.append((pos, real_ends[2 * i], "HEADING_2", [(l + "\n", B)]))
    want.append((real_ends[2 * i], real_ends[2 * i + 1], "NORMAL_TEXT", [("\n", {})]))
    pos = real_ends[2 * i + 1]
bad = 0
for g, w in zip(got, want):
    g = (g[0], g[1], g[2], [(t, s) for t, s in g[3]])
    if g != w:
        bad += 1
        print("got :", g); print("want:", w)
if len(got) != len(want):
    bad += 1; print("paragraph count", len(got), "want", len(want))
print("ok     new_doc_mason_structure" if not bad else "FAIL   new_doc_mason_structure")
sys.exit(1 if bad else 0)
