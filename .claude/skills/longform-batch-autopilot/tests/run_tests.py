#!/usr/bin/env python3
"""Golden tests for entries.py: each <case>_topics.json must give exactly <case>_expected.txt.
The expected lines are the real LONGFORMS lines Jeremiah wrote for that week. Shared-copy split
fixes are applied; hand edits that no rule can predict are excluded. Exceptions: nathan_oct_wk2 and
ben_k_oct_wk2 are provisional snapshots of the script's own output, since neither week had a real doc
when they were made (Nathan's first batch; Ben's statuses come from Jeremiah's real Oct 8 brief, and
the value tweet rule from his real Oct Wk1 doc, where 'Value tweet ">" Listicle' stayed one X/LI line).
Replace each with his real lines once he writes that week. type_a_rule and type_a_no_transcript are
synthetic cases for Jeremiah's Oct 9 rule: a Type A topic gets a line only if the call answered it (not
discussed, killed or unanswered = no line; no transcript = Type B only).
Then every tests/test_*.py runs: the doc batches, the read-back and quote checks, and
test_entries_notes.py (the notes, problems and would-be lines entries.py prints beside the lines).
Run: python3 -I tests/run_tests.py"""
import glob, json, os, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
script = os.path.join(here, "..", "scripts", "entries.py")
failed = 0
for topics in sorted(glob.glob(os.path.join(here, "*_topics.json"))):
    case = os.path.basename(topics)[:-len("_topics.json")]
    expected = os.path.join(here, case + "_expected.txt")
    if not os.path.exists(expected):
        continue
    out = json.loads(subprocess.run([sys.executable, "-I", script, topics], capture_output=True, text=True, check=True).stdout)
    got = [e["line"] for e in out["entries"]]
    want = open(expected, encoding="utf-8").read().splitlines()
    if got == want:
        print("ok    ", case)
    else:
        failed += 1
        print("FAIL  ", case)
        for i in range(max(len(got), len(want))):
            g = got[i] if i < len(got) else "<none>"
            w = want[i] if i < len(want) else "<none>"
            if g != w:
                print("   got :", g)
                print("   want:", w)
# every other check (doc batches, read-back check, quote check) is a tests/test_*.py script
for t in sorted(glob.glob(os.path.join(here, "test_*.py"))):
    if subprocess.run([sys.executable, "-I", t]).returncode:
        failed += 1
sys.exit(1 if failed else 0)
