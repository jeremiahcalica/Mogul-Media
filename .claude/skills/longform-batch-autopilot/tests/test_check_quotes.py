#!/usr/bin/env python3
"""check_quotes.py on small synthetic calls (quotes_*.txt) and briefs (quotes_brief*.md): each quote kind must get
its status (ok, WRONG TIME, SHEET, NOT FOUND), the warnings and the unfinished-sentence list, in all three
transcript forms (Fireflies lines, Kyle's paste, untimed Granola). Run: python3 -I tests/test_check_quotes.py"""
import json, os, shutil, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
script = os.path.join(here, "..", "scripts", "check_quotes.py")
f = lambda name: os.path.join(here, name)
tmp = tempfile.mkdtemp()
bad = []


def run(*args):
    p = subprocess.run([sys.executable, "-I", script] + list(args) + ["--json"], capture_output=True, text=True)
    return p.returncode, json.loads(p.stdout)


def expect(what, cond):
    if not cond:
        bad.append(what)


def by_line(out):
    return {q["line"]: q for q in out["quotes"]}


# Fireflies lines, with the sheet
code, out = run(f("quotes_fireflies.txt"), f("quotes_brief.md"), "--sheet", f("quotes_sheet.txt"))
q = by_line(out)
expect("fireflies format", out["transcript"]["format"] == "Fireflies" and out["transcript"]["timed"])
expect("exit 1 on NOT FOUND / WRONG TIME", code == 1 and out["pass"] is False)
expect("good quote under a label's range", q[12]["status"] == "ok" and q[12]["window"] == "[00:04–00:18]")
expect("ellipsis quote with a reading inside", q[13]["status"] == "ok")
expect("tagged single time", q[7]["status"] == "ok")
expect("wrong time, says where", q[14]["status"] == "WRONG TIME" and "01:35 Sam Test" in q[14]["found_at"])
expect("unfinished quote itself ok", q[15]["status"] == "ok")
expect("unfinished sentence listed", [u["sentence"] for u in out["unfinished"]] == ["I was going to tell you about the."])
expect("starts mid-sentence warning", any("starts mid-sentence" in w for w in q[16]["warnings"]))
expect("full sentence: no warning", not q[12]["warnings"])
expect("stutter dropped is NOT FOUND, with the hint", q[17]["status"] == "NOT FOUND" and "collapsed" in q[17]["detail"])
expect("H:MM:SS", q[18]["status"] == "ok")
expect("invented quote", q[20]["status"] == "NOT FOUND")
expect("sheet quote in Flags", q[21]["status"] == "SHEET")
expect("Original brief quote", q[9]["status"] == "SHEET")
expect("reading and cited file skipped", [x["quote"] for x in out["quotes"] if x["line"] == 22] == ["payroll"])
expect("headings, table, Longform doc skipped", not {1, 2, 4, 5, 6, 8, 11, 19, 23, 24} & set(q))

# no sheet: Original brief skipped, the Flags sheet quote is NOT FOUND
code, out = run(f("quotes_fireflies.txt"), f("quotes_brief.md"))
expect("no --sheet: Original brief skipped", out["skipped"] == 1 and 9 not in by_line(out))
expect("no --sheet: sheet quote NOT FOUND", by_line(out)[21]["status"] == "NOT FOUND")

# Kyle's paste, then the same paste with its line breaks lost
flat = os.path.join(tmp, "flat.txt")
open(flat, "w").write(" ".join(l.strip() for l in open(f("quotes_pasted.txt"))))
for src in (f("quotes_pasted.txt"), flat):
    code, out = run(src, f("quotes_brief.md"))
    q = by_line(out)
    name = os.path.basename(src)
    expect(name + " format", out["transcript"]["format"] == "Fireflies (pasted)" and out["transcript"]["segments"] == 6)
    expect(name + " good + ellipsis", q[12]["status"] == "ok" and q[13]["status"] == "ok")
    expect(name + " wrong time", q[14]["status"] == "WRONG TIME")
    expect(name + " page header dropped", q[16]["status"] == "ok")

# untimed Granola: times in the brief can't be checked, quotes can
code, out = run(f("quotes_granola.txt"), f("quotes_brief_granola.md"))
q = by_line(out)
expect("granola untimed", out["transcript"]["format"] == "untimed" and not out["transcript"]["timed"])
expect("granola: a time in the brief is ignored", q[5]["status"] == "ok")
expect("granola: ellipsis across turns", q[6]["status"] == "ok")
expect("granola: unfinished turn", q[7]["status"] == "ok" and [u["sentence"] for u in out["unfinished"]] == ["I, I"])
expect("granola: invented", q[8]["status"] == "NOT FOUND" and code == 1)

# a flag's quote in its bold label is checked against its time, a time right before a short quote times it,
# and a quote made only of short fragments is still checked
flags = os.path.join(tmp, "flags.md")
open(flags, "w").write("## Topic 1 — Long-form: X\n### Flags\n"
                       "- **\"We scaled to 9 figures\" [01:35–01:40].** A number to confirm.\n"
                       "- **\"We tripled in a weekend\" [01:35–01:40].** Invented.\n"
                       "- **The \"hiring trap\" title.** A label's untimed quote is its title.\n"
                       "### From the call\n- Kyle [00:19]: \"That's perfect.\"\n- Kyle [05:19]: \"That's perfect.\"\n"
                       "- \"ten people … Honestly\" [00:04–00:14]\n")
code, out = run(f("quotes_fireflies.txt"), flags)
q = by_line(out)
expect("flag quote in a bold label", q[3]["status"] == "ok" and q[3]["window"] == "[01:35–01:40]")
expect("invented flag quote", q[4]["status"] == "NOT FOUND" and 5 not in q)
expect("time right before a short quote", q[7]["status"] == "ok" and not q[7]["warnings"] and q[8]["status"] == "WRONG TIME")
expect("short fragments only", q[9]["status"] == "NOT FOUND")

# a clean brief passes
clean = os.path.join(tmp, "clean.md")
open(clean, "w").write("## Topic 1 — Long-form: X\n### From the call\n**The mistake [00:04–00:18]:**\n"
                       "- \"Honestly, the biggest mistake I see founders make is hiring too fast.\"\n")
p = subprocess.run([sys.executable, "-I", script, f("quotes_fireflies.txt"), clean], capture_output=True, text=True)
expect("clean brief: PASS, exit 0", p.returncode == 0 and p.stdout.strip().endswith("PASS"))

shutil.rmtree(tmp)
for b in bad:
    print("   failed:", b)
print("ok     check_quotes" if not bad else "FAIL   check_quotes")
sys.exit(1 if bad else 0)
