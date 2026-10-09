#!/usr/bin/env python3
"""verify_doc.py must pass Jeremiah's real Caulen Oct Wk2 doc (Drive markdown, with a "# Tab 1" or "# Content" tab
title) and a doc built by new_doc_batch.py, in the read_doc and the minimal form; it must fail a doc whose bold sits
in the Heading 2 style (the HTML-import bug), a read without the H1/H2 named styles, and the batch's subset form."""
import json, os, shutil, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import simulate_docs_batch as sim
V = os.path.join(here, "..", "scripts", "verify_doc.py")
d = tempfile.mkdtemp()
tmp = lambda name: os.path.join(d, name)
bad = []


def run(args):
    p = subprocess.run([sys.executable, "-I", V] + args, capture_output=True, text=True)
    return p.returncode, p.stdout


def expect(what, cond):
    if not cond:
        bad.append(what)


clines = open(os.path.join(here, "caulen_oct_wk2_expected.txt"), encoding="utf-8").read().splitlines()
json.dump(clines, open(tmp("c.json"), "w"))
real = open(os.path.join(here, "caulen_oct_wk2_real.md"), encoding="utf-8").read()
for name, md in (("tab1", real), ("content", real.replace("# Tab 1", "# Content")),   # Josh C Oct Wk2's tab title
                 ("no tab title", real.replace("# Tab 1", ""))):
    open(tmp(name + ".md"), "w", encoding="utf-8").write(md)
    expect("--md " + name, run(["--md", tmp(name + ".md"), tmp("c.json"), "--header", "Caulen F. - Week 2 - Oct"])[0] == 0)
open(tmp("unbold.md"), "w", encoding="utf-8").write(real.replace("# **Caulen F. - Week 2 - Oct**", "# Caulen F. - Week 2 - Oct"))
expect("--md unbolded header fails", run(["--md", tmp("unbold.md"), tmp("c.json")])[0] == 1)

# a doc built from an empty doc, turned back into read_doc form
mlines = open(os.path.join(here, "mason_oct_wk2_expected.txt"), encoding="utf-8").read().splitlines()
json.dump(mlines, open(tmp("m.json"), "w"))
batch = json.loads(subprocess.run([sys.executable, "-I", os.path.join(here, "..", "scripts", "new_doc_batch.py"),
                                   os.path.join(here, "blank_doc_read.json"), "Mason L. - Week 2 - Oct", tmp("m.json")],
                                  capture_output=True, text=True, check=True).stdout)
cells = sim.cells_from(sim.load(os.path.join(here, "blank_doc_read.json")))
for r in batch["requests"]:
    sim.apply(cells, r)
STYLES = {"HEADING_1": {"fontSize": {"magnitude": 20, "unit": "PT"}},
          "HEADING_2": {"bold": False, "fontSize": {"magnitude": 16, "unit": "PT"}},
          "NORMAL_TEXT": {"bold": False, "fontSize": {"magnitude": 11, "unit": "PT"},
                          "weightedFontFamily": {"fontFamily": "Arial", "weight": 400}}}


def as_read(styles):
    content = [{"endIndex": 1, "sectionBreak": {}}]
    for s, e, ps, runs in sim.paragraphs(cells):
        els, i = [], s
        for t, st in runs:
            els.append({"startIndex": i, "endIndex": i + len(t), "textRun": {"content": t, "textStyle": st}}); i += len(t)
        content.append({"startIndex": s, "endIndex": e, "paragraph": {"elements": els, "paragraphStyle": {"namedStyleType": ps}}})
    return {"documentId": "D", "revisionId": "R", "tabs": [{"tabProperties": {"tabId": "t.0"}, "documentTab": {
        "body": {"content": content}, "documentStyle": {"documentFormat": {"documentMode": "PAGELESS"}},
        "namedStyles": {"styles": [{"namedStyleType": k, "textStyle": v} for k, v in styles.items()]}}}]}


def as_minimal(read):
    """The minimal form, written exactly as verify_doc.py's docstring tells an agent to."""
    tab = read["tabs"][0]["documentTab"]
    paras = [{"namedStyleType": c["paragraph"]["paragraphStyle"]["namedStyleType"],
              "elements": [{"textRun": {"content": e["textRun"]["content"],
                                        "textStyle": {k: v for k, v in e["textRun"]["textStyle"].items() if k in ("bold", "link")}}}
                           for e in c["paragraph"]["elements"]]}
             for c in tab["body"]["content"] if "paragraph" in c]
    return {"minimal": True, "tabs": len(read["tabs"]), "documentMode": tab["documentStyle"]["documentFormat"]["documentMode"],
            "namedStyles": {s["namedStyleType"]: s["textStyle"] for s in tab["namedStyles"]["styles"]}, "paragraphs": paras}


h2_bold = dict(STYLES, HEADING_2={"bold": True, "fontSize": {"magnitude": 16, "unit": "PT"}})
no_styles = {"NORMAL_TEXT": STYLES["NORMAL_TEXT"]}
big_h1 = dict(STYLES, HEADING_1={"fontSize": {"magnitude": 24, "unit": "PT"}})
for name, doc in (("good", as_read(STYLES)), ("h2bold", as_read(h2_bold)), ("nostyles", as_read(no_styles)),
                  ("bigh1", as_read(big_h1)), ("min_good", as_minimal(as_read(STYLES))),
                  ("min_h2bold", as_minimal(as_read(h2_bold)))):
    json.dump(doc, open(tmp(name + ".json"), "w"))
expect("read form PASS", run([tmp("good.json"), tmp("m.json"), "--header", "Mason L. - Week 2 - Oct"])[0] == 0)
expect("bold baked into Heading 2 FAILs", run([tmp("h2bold.json"), tmp("m.json")])[0] == 1)
code, out = run([tmp("nostyles.json"), tmp("m.json")])
expect("missing H1/H2 named styles FAIL", code == 1 and "HEADING_2 missing" in out and "HEADING_1 missing" in out)
code, out = run([tmp("bigh1.json"), tmp("m.json")])
expect("Heading 1 24pt: WARN, still PASS", code == 0 and "WARN" in out and "Heading 1 24pt" in out)
expect("minimal form PASS", run([tmp("min_good.json"), tmp("m.json"), "--header", "Mason L. - Week 2 - Oct"])[0] == 0)
expect("minimal form, bold in Heading 2 FAILs", run([tmp("min_h2bold.json"), tmp("m.json")])[0] == 1)
json.dump(dict(as_minimal(as_read(STYLES)), namedStyles=dict(STYLES, HEADING_1=None)), open(tmp("min_null.json"), "w"))
code, out = run([tmp("min_null.json"), tmp("m.json")])
expect("minimal form, null Heading 1 style FAILs", code == 1 and "HEADING_1 missing" in out)
code, out = run([os.path.join(here, "copied_doc_subset.json"), tmp("m.json")])
expect("batch subset lacks the style fields: FAIL naming them", code == 1 and "lacks tabs, documentMode, namedStyles" in out)

shutil.rmtree(d)
for b in bad:
    print("   failed:", b)
print("ok     verify_doc" if not bad else "FAIL   verify_doc")
sys.exit(1 if bad else 0)
