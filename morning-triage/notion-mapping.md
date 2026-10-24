# Notion mapping — how a triage task is written

Decided 2026-10-24. Jeremiah: "i think we go with the current setup i have in
Notion instead of putting more properties in it".

So: **no new properties are ever created.** Everything Step 6 needs is carried by
the properties that already exist plus the page body.

Target: "Tasks [Backend]", data source
`collection://1b6750f5-7626-8016-83d0-000b253b1852`. The "All Tasks" view
(`v=d6082178608a4ce89fd610490519f87c`) is a filtered view of it, not a separate
database.

## Field mapping

| Step 6 field | Where it goes | Note |
| --- | --- | --- |
| Title | `Task` (title) | Grammar below |
| Client | Inside `Task`, before the first pipe | Full name: "Josh C", never bare "Josh" |
| Priority | `Task Priority` | P0 -> High, P1 -> Medium, P2 -> Low |
| Due | `Due Date` | Manila time, only if a deadline was actually stated |
| Status | `Task Status` | "Not started" (the database default) |
| Role | Page body, `Role:` line | WRITER or SA |
| Source | Page body, `Source:` line | The permalink or ClickUp URL |
| Evidence | Page body, quote block | Verbatim trigger + author + time |

The page body is the home for Role, Source and Evidence because the database has
no properties for them and we are not adding any. The hard rule still holds:
every task carries a real link and a verbatim quote. They live one click in,
in the page, instead of in a column.

## Title grammar

Match the convention already in the database, which is
`Client | MONTH WKn | Deliverable` ("Brian M | JULY WK3 | Long-forms",
"Richard P | MAY WK3 & WK4 | Topics"), with short sub-item titles ("Snipe",
"Outline", "Design Request").

Triage tasks are smaller than a week's batch, so they use the two-part form:

    Client | verb + deliverable

Examples:

    Caulen F | Fix hook on item 3
    Josh C | Answer Kyle's question on the topic sheet
    Mason L | Write quick response for the Thursday post

Rules:
- Plain text only. Several existing rows contain raw `<b>` and `<p>` tags from an
  earlier automation; do not copy that.
- Full client name always. A bare first name matching two clients is NEEDS
  REVIEW and never reaches Notion at all.
- Do not invent a `MONTH WKn` segment. It only appears if the trigger itself
  names the batch week.

## Page body template

    Role: WRITER
    Source: <permalink>

    > <verbatim trigger, under 40 words>
    > -- <author>, <timestamp, Manila>

    Why this rank: <cites the trigger>   (P0 and P1 only)

## Priority mapping

`Task Priority` has exactly three options, so the mapping is 1:1 and
unambiguous:

| Triage rank | Task Priority |
| --- | --- |
| P0 (do first) | High |
| P1 (today) | Medium |
| P2 (this week) | Low |

P3 is FYI only. It never becomes a row, so it never needs an option.

## Needs review

`Task Status` has no "Needs review" option and we are not adding one. Per the
spec's own fallback, NEEDS REVIEW items stay in the morning summary and the run
log only. They are never written to Notion.

## Deduplication

Two cheap checks, no full-database scan:

1. **Same client and same deliverable** — SQL on the `Task` title against open
   rows (`Task Status` != "Done").
2. **Same permalink** — the permalink lives in the page body, which SQL cannot
   read. So this check is scoped to open rows created on or after the previous
   run (`createdTime` is queryable), which is the only set a repeat could be
   in. Those bodies get fetched and compared.

As of 2026-10-24 the database holds 292 rows, 25 of them open (1 In progress,
19 Not started, 5 On Hold), so check 2 starts from a near-empty set.

A duplicate means no new row; it is noted in the run log instead.

## The database is dormant, and that is accepted

No row has been created since 2026-07-16, three months before this was set up.
The "All Tasks" view reads empty because it filters to open tasks with a due
date in the surrounding week.

Live work moved to ClickUp: that space holds OCT WK3 and WK4 tasks updated this
week, while Notion stops in July.

Jeremiah decided to use Notion anyway, 2026-10-24: "we can still use Notion imo,
i'll experiment with it anyway, see if i like it". So triage rows will be the
only recent rows in the database. Treated as a trial, not a settled format —
expect to be told to change it.
