#!/usr/bin/env python3
"""longform_batch.py on a copied doc (header, Media Folder chip, LONGFORMS, last week's posts) must give
the structure of Jeremiah's real Mason Oct Wk2 doc: new header, "Media Folder:" bold + " \\n" not bold,
no chip, LONGFORMS, each line Heading 2 bold + one empty Normal paragraph. The cut-down ("subset") form
of the same read must give the identical batch. Run: python3 -I tests/test_copy_batch.py"""
import json, os, shutil, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import simulate_docs_batch as sim
script = os.path.join(here, "..", "scripts", "longform_batch.py")
lines = ["1 - (X/LI) - (P) - (Long-form)", "2 - (X/LI) - (Q) - (Thread)"]
tmp = tempfile.mkdtemp()
lp = os.path.join(tmp, "lines.json"); json.dump(lines, open(lp, "w"))
run = lambda read: json.loads(subprocess.run([sys.executable, "-I", script, os.path.join(here, read), "auto:Oct:2", lp],
                                             capture_output=True, text=True, check=True).stdout)
full, subset = run("copied_doc_read.json"), run("copied_doc_subset.json")
shutil.rmtree(tmp)
cells = sim.cells_from(sim.load(os.path.join(here, "copied_doc_read.json")))
for r in full["requests"]:
    sim.apply(cells, r)
got = [(s, e, ps, [(t, st) for t, st in runs]) for s, e, ps, runs in sim.paragraphs(cells)]
B = {"bold": True}
want = [(1, 25, "HEADING_1", [("Mason L. - Week 2 - Oct\n", B)]),
        (25, 40, "HEADING_1", [("Media Folder:", B), (" \n", {})]),
        (40, 50, "HEADING_1", [("LONGFORMS\n", B)]),
        (50, 81, "HEADING_2", [(lines[0] + "\n", B)]), (81, 82, "NORMAL_TEXT", [("\n", {})]),
        (82, 110, "HEADING_2", [(lines[1] + "\n", B)]), (110, 111, "NORMAL_TEXT", [("\n", {})])]
ok = got == want and full["requests"] == subset["requests"] and not [c for c in cells[1:] if c.get("obj")]
if not ok:
    print("got :", got); print("want:", want); print("subset same:", full["requests"] == subset["requests"])
print("ok     copy_batch_structure" if ok else "FAIL   copy_batch_structure")
sys.exit(0 if ok else 1)
