#!/usr/bin/env python3
"""Golden tests for entries.py: each <case>_topics.json must give exactly <case>_expected.txt.
The expected lines are the real LONGFORMS lines Jeremiah wrote for that week. Shared-copy split
fixes are applied; hand edits that no rule can predict are excluded.
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
sys.exit(1 if failed else 0)
