"""Helpers for the Client Feedback Ledger.

Run as a script:
  python3 -I ledger.py id <kind> <source_id> <native_id>
  python3 -I ledger.py diff <old_file> <new_file>
  python3 -I ledger.py ids <page_file>
  python3 -I ledger.py batch "<label>"
  python3 -I ledger.py next "<label>"
"""
import base64
import difflib
import hashlib
import re
import sys

KINDS = {"edit", "net", "comment", "reply", "suggestion", "slack", "loom", "transcript", "killed"}

ID_RE = re.compile(r"\bL-[A-Z2-7]{10}\b")


def ledger_id(kind, source_id, native_id):
    """Stable ID for one entry: same source + same native ID -> same ID, every run.

    kind       one of KINDS
    source_id  the doc ID, Slack channel ID, Loom ID or transcript ID
    native_id  what identifies the item inside the source: a comment ID, a Slack
               message ts, a Loom mm:ss + line, or for a version-history edit
               "<version timestamp>|<post heading>|<change markup>"
    """
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}; use one of {sorted(KINDS)}")
    key = f"{kind}|{source_id.strip()}|{native_id.strip()}".encode("utf-8")
    digest = hashlib.sha256(key).digest()
    return "L-" + base64.b32encode(digest).decode("ascii")[:10]


def existing_ids(page_text):
    """Every Ledger ID already written in a Client Feedback Log page."""
    return set(ID_RE.findall(page_text))


_TOKEN_RE = re.compile(r"\s+|[^\s]+")


def _tokens(text):
    return _TOKEN_RE.findall(text)


def word_diff(old, new):
    """Word-level diff in the ledger's markup: [-removed-]{+added+}.

    Whitespace is kept exactly, so the result reads back to `old` if you drop the
    {+...+} parts and unwrap the [-...-] parts, and to `new` the other way round.
    """
    a, b = _tokens(old), _tokens(new)
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal":
            out.append("".join(a[i1:i2]))
            continue
        if op in ("delete", "replace"):
            out.append("[-" + "".join(a[i1:i2]) + "-]")
        if op in ("insert", "replace"):
            out.append("{+" + "".join(b[j1:j2]) + "+}")
    return "".join(out)


def apply_markup(markup, side):
    """Rebuild one side of a word_diff: side='old' or 'new'."""
    if side == "old":
        text = re.sub(r"\{\+.*?\+\}", "", markup, flags=re.S)
        return re.sub(r"\[-(.*?)-\]", r"\1", text, flags=re.S)
    if side == "new":
        text = re.sub(r"\[-.*?-\]", "", markup, flags=re.S)
        return re.sub(r"\{\+(.*?)\+\}", r"\1", text, flags=re.S)
    raise ValueError("side must be 'old' or 'new'")


MONTHS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
}
_MONTH_NAMES = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
_BATCH_RE = re.compile(
    r"\b(?P<mon>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?"
    r"|sept(?:ember)?|sep|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
    r"\s*(?:-\s*)?(?:wk|week)\s*(?P<wk>[1-5])\b",
    re.I,
)


def parse_batch(label):
    """(month, week) from any of the formats in use, or None.

    'Sept Wk 5' (ledger), 'SEP WK5' / 'OCT WK3' (ClickUp, Slack bot),
    'Mason L. - Sept - Week 5' (doc title), 'Oct - Week 2'.
    """
    m = _BATCH_RE.search(label)
    if not m:
        return None
    return MONTHS[m.group("mon").lower()], int(m.group("wk"))


def next_batch(month, week):
    """The batch after (month, week). Weeks run 1-5; Week 5 rolls to next month's Week 1."""
    if week < 5:
        return month, week + 1
    return (month % 12) + 1, 1


def batch_label(month, week, style="ledger"):
    if style == "ledger":
        return f"{_MONTH_NAMES[month]} Wk {week}"
    if style == "clickup":
        return f"{_MONTH_NAMES[month][:3].upper()} WK{week}"
    raise ValueError("style must be 'ledger' or 'clickup'")


def last_logged_batch(page_text):
    """The latest batch named in a heading of an existing log page, or None.

    Reads headings only ("## Sept Wk 5", "## MASON | OCT WK1 — main doc"), so table
    rows that mention a batch do not count.
    """
    best = None
    for line in page_text.splitlines():
        if not line.lstrip().startswith("#"):
            continue
        b = parse_batch(line)
        if b and (best is None or _order(b) > _order(best)):
            best = b
    return best


def _order(b):
    # Feedback logs span Jun 2025 -> 2026; treat Jun-Dec as the earlier half of a
    # season only when compared within the same run. Month then week is enough
    # because a run never spans more than ~3 months back.
    return (b[0], b[1])


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "id":
        print(ledger_id(argv[2], argv[3], argv[4]))
    elif cmd == "diff":
        print(word_diff(open(argv[2]).read(), open(argv[3]).read()))
    elif cmd == "ids":
        for i in sorted(existing_ids(open(argv[2]).read())):
            print(i)
    elif cmd == "batch":
        print(parse_batch(argv[2]))
    elif cmd == "next":
        b = parse_batch(argv[2])
        print(batch_label(*next_batch(*b)) if b else None)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
