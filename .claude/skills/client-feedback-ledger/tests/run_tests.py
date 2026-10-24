"""Tests for scripts/ledger.py. Run: python3 -I tests/run_tests.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import ledger  # noqa: E402

failures = []


def check(name, got, want):
    if got != want:
        failures.append(f"{name}: got {got!r}, want {want!r}")


# Ledger IDs are stable, distinct, and shaped L-XXXXXXXXXX.
a = ledger.ledger_id("comment", "1z3RlbG215DNib9DvwTmpzngPUSfWdH_KiwQyIVzCkjc", "AAACHzB3oHc")
check("id stable", a, ledger.ledger_id("comment", "1z3RlbG215DNib9DvwTmpzngPUSfWdH_KiwQyIVzCkjc", "AAACHzB3oHc"))
check("id shape", bool(ledger.ID_RE.fullmatch(a)), True)
check("id differs by kind", a == ledger.ledger_id("reply", "1z3RlbG215DNib9DvwTmpzngPUSfWdH_KiwQyIVzCkjc", "AAACHzB3oHc"), False)
check("id ignores outer spaces", a, ledger.ledger_id("comment", " 1z3RlbG215DNib9DvwTmpzngPUSfWdH_KiwQyIVzCkjc ", "AAACHzB3oHc "))
try:
    ledger.ledger_id("vibes", "x", "y")
    failures.append("unknown kind should raise")
except ValueError:
    pass

page = f"| Oct 1 | Don't post this. | Mason | {a} |\nrandom L-abc text\n"
check("existing ids", ledger.existing_ids(page), {a})

# Word diff matches the ledger's markup, taken from real Mason entries.
check("diff replace",
      ledger.word_diff("What I'd tell an 18-year-old in 2026:", "What I'd tell the 18-year-old me in 2026:"),
      "What I'd tell [-an-]{+the+} 18-year-old{+ me+} in 2026:")
check("diff no change", ledger.word_diff("same text", "same text"), "same text")
for old, new in [
    ("I spend $5 to $7M/month on Meta ads profitably", "I spend $7M+/mo on Meta ads profitably"),
    ("- Sleep maxing → I go to bed on time now", "1) Sleep maxxing → I go to bed on time now, sometimes"),
    ("Don't post this.", "Dont post this."),
    ("line one\n\nline two", "line one\nline two added"),
]:
    m = ledger.word_diff(old, new)
    check(f"roundtrip old {old[:20]!r}", ledger.apply_markup(m, "old"), old)
    check(f"roundtrip new {new[:20]!r}", ledger.apply_markup(m, "new"), new)

# Batch labels in every format in use.
check("ledger label", ledger.parse_batch("## Sept Wk 5"), (9, 5))
check("clickup label", ledger.parse_batch("MASON | OCT WK3 | Longforms"), (10, 3))
check("doc title", ledger.parse_batch("Mason L. - Sept - Week 5"), (9, 5))
check("doc title oct", ledger.parse_batch("Marco B. - Oct - Week 3 (Snipes)"), (10, 3))
check("sep short", ledger.parse_batch("BRIAN M | SEP WK3 | Longforms"), (9, 3))
check("no batch", ledger.parse_batch("Client Feedback Log"), None)
check("next mid", ledger.next_batch(9, 3), (9, 4))
check("next roll", ledger.next_batch(9, 5), (10, 1))
check("next year", ledger.next_batch(12, 5), (1, 1))
check("label ledger", ledger.batch_label(10, 1), "Oct Wk 1")
check("label clickup", ledger.batch_label(9, 4, "clickup"), "SEP WK4")

mason_page = """## Named comments from Mason
| Sept Wk 5 | 1.2 (LI) | Oct 1, 6:13 AM | Don't post this. |
## Aug Wk 1
### LF 1
## Sept Wk 4
## Sept Wk 5
### LF 2
"""
check("last logged (headings only)", ledger.last_logged_batch(mason_page), (9, 5))
check("last logged none", ledger.last_logged_batch("**Date:**\n* Source"), None)
check("last logged agent format",
      ledger.last_logged_batch(mason_page + "## MASON | OCT WK1 — main doc\n"), (10, 1))

if failures:
    print("FAILED")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("all ledger tests passed")
