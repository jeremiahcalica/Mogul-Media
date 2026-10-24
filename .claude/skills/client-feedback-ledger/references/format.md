# Output format

Append to the client's Client Feedback Log, one block per batch doc. This is
Jeremiah's format, word for word:

```
## <CLIENT> | <MON WK#> — <main doc / Snipes / Quick response posts>
Source: <doc link(s)> · Slack thread: <permalink, if any>

### <Post heading, e.g. LF2 — first line of the post>

**Edits (version history)**
| Date | Change ([-removed-]{+added+}) | By | ID |

**Comments** (including resolved and deleted)
| Date | Anchored on (exact) | Client (verbatim) | ID |

**Suggestions**
| Date | Original (exact) | Suggested (exact) | Outcome: open / accepted / rejected | ID |

**Outside the doc**
| Date | Source (Slack forwarded / relayed / image · Loom mm:ss · transcript) | Client (verbatim) | ID |

**Net change (sent to client → now)**
<post text in [-removed-]{+added+} markup>
```

- Leave out any empty table.
- Feedback not tied to a post goes under "### Batch-level".
- A post the client killed gets a line under its heading: "Killed: <heading>",
  with date and attribution.
- `<MON WK#>` uses the ClickUp style: `OCT WK1`, `SEP WK4`. Use
  `scripts/ledger.py` → `batch_label(month, week, "clickup")`.
- Dates are Manila time (PHT), which is what the existing logs use. Example:
  "Oct 1, 6:13 AM".

## Verbatim inside a Markdown table

The text stays exact. Only these characters get escaped, and only so the table
renders:
- `|` → `\|`
- a line break inside a cell → `↵`, the symbol the existing Mason log uses
- a tab → `⇥`

Nothing else changes. Keep typos, casing, emoji, curly quotes and spacing.

## Ledger IDs

Every entry's ID column holds a Ledger ID from `scripts/ledger.py`:

```
python3 -I scripts/ledger.py id <kind> <source_id> <native_id>
```

| kind | source_id | native_id |
|---|---|---|
| comment | doc ID | comment ID |
| reply | doc ID | reply ID |
| suggestion | doc ID | suggestion ID, or for one found in history: `<version time>\|<post>\|<markup>` |
| edit | doc ID | `<version time>\|<post heading>\|<change markup>` |
| killed | doc ID | `<post heading>` |
| net | doc ID | `<post heading>\|<markup>` |
| slack | channel ID | message ts |
| loom | Loom video ID | `<mm:ss>\|<line>` |
| transcript | transcript ID | `<timestamp>\|<speaker>` |

**Before writing anything:** run `ids` on the page's current text and drop every
entry whose ID is already there. A run with nothing new writes nothing.

The net change for a post is recomputed every run. It gets a new ID whenever
the text has moved on, so a post that keeps changing shows each new net change
once, and an unchanged post is never repeated.

## Run summary

Shown at the end of the run. **Never posted to ClickUp.**
- clients processed, and the starting batch for each
- new entries per batch
- verification counts (checked, matched, corrected, unverified)
- destination rule used per client
- Needs Jeremiah
