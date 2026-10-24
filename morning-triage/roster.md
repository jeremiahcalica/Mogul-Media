# Roster — the ONLY source of truth for task ownership

Filled from Jeremiah's own lists, 2026-10-24. Ownership is never inferred from
Slack channels, mentions, who posted, or past runs. If a client is not in this
table, items for them are NEEDS REVIEW — never MINE.

## This table changes, and that is the point

Jeremiah, 2026-10-24, on both lists: "can go down, can go up, depending if Mogul
onboards a new client and tells me to write for it or a client leaves, there are
some clients that'll leave too, important nuance here".

So:
- A new client produces no tasks until his role for them is added here.
- A client who leaves gets `Status` changed to `ending YYYY-MM-DD` or
  `handed off to <name>`. Do not delete the row — the history is what lets a
  run tell "left" apart from "never listed".
- No WRITER tasks for a client after their handoff date. Same for SA-TOPICS.
- A role can change without the client leaving (see Brian M. below).

## Roles

| Client | My role (WRITER / SA-TOPICS / BOTH / NONE) | Strategist | Slack channels | ClickUp list | Status |
| --- | --- | --- | --- | --- | --- |
| Abdul F. | BOTH | Kyle † | _TO FILL_ | ABDUL \| INTERNAL › CONTENT WRITING † | active |
| Ben K. | WRITER | Devin † | _TO FILL_ | BEN K \| INTERNAL › CONTENT WRITING † | active |
| Brian M. | SA-TOPICS | _TO FILL_ | _TO FILL_ | _TO FILL_ | active |
| Caulen F. | BOTH | Kyle † | _TO FILL_ | CAULEN \| INTERNAL › CONTENT WRITING † | active |
| Jason G. | BOTH | Kyle † | _TO FILL_ | JASON \| INTERNAL › CONTENT WRITING † | active |
| Joshua C. | BOTH | Kyle † | _TO FILL_ | JOSH \| INTERNAL › CONTENT WRITING † | active |
| Keval S. | BOTH | Kyle † | _TO FILL_ | KEVAL \| INTERNAL › CONTENT WRITING † | active |
| Laura P. | SA-TOPICS | _TO FILL_ | _TO FILL_ | _TO FILL_ | active |
| Lior P. | BOTH | Kyle † | _TO FILL_ | LIOR P \| INTERNAL › CONTENT WRITING † | active |
| Marco B. | WRITER | Devin † | _TO FILL_ | MARCO \| INTERNAL › CONTENT WRITING † | active |
| Mason L. | BOTH | Kyle † | _TO FILL_ | MASON \| INTERNAL › CONTENT WRITING † | active |
| Matt O. | SA-TOPICS | _TO FILL_ | _TO FILL_ | _TO FILL_ | active |
| Michael K. | BOTH | Kyle † | _TO FILL_ | MICHAEL K \| INTERNAL › CONTENT WRITING † | active |
| Nathan C. | WRITER | Devin † | _TO FILL_ | NATHAN C \| INTERNAL › CONTENT WRITING † | active |
| Phil R. | SA-TOPICS | _TO FILL_ | _TO FILL_ | _TO FILL_ | active |
| Shane H. | BOTH | Kyle † | _TO FILL_ | SHANE \| INTERNAL › CONTENT WRITING † | active |
| Teddy T. | WRITER | Devin † | _TO FILL_ | TEDDY \| INTERNAL › CONTENT WRITING † | active |

† = not from Jeremiah. Derived from
`.claude/skills/longform-batch-autopilot/references/clients.md` (pod table, IDs
checked Oct 9 2026) and its documented ClickUp pattern: "Each client has a folder
`<PREFIX> | INTERNAL` with a list `CONTENT WRITING`". Confirm before the first
real run. Anything marked _TO FILL_ is unknown and must not be guessed.

Counts: 17 clients — 9 BOTH, 4 WRITER, 4 SA-TOPICS.

## What the shape of this table means

- Every BOTH client is in **Kyle's** pod. Every WRITER-only client is in
  **Devin's** pod. So on Devin's clients, a topic-sheet or topic-question ask is
  NOT MINE; on Kyle's, it is.
- The four SA-TOPICS-only clients (Brian M., Laura P., Matt O., Phil R.) do not
  appear in clients.md at all, because that file is the *longform* registry and
  Jeremiah does no writing for them. A writing ask on any of these four is NOT
  MINE.
- **Brian M.** is SA-TOPICS only today, but the Notion tasks database still holds
  his old longform rows ("Brian M | JULY WK3 | Long-forms"). Past rows are not
  evidence of current ownership. A writing ask for Brian M. is NOT MINE.

## Clients deliberately absent

These are real Mogul clients that are NOT on either of Jeremiah's lists, so he
holds no role for them and they can never produce a MINE task:

- **Zarak A.** — listed in clients.md as a Kyle-pod longform client, and has rows
  in the Notion database. Not on his 2026-10-24 lists.
- **Josh D.** — listed in clients.md as a Devin-pod longform client. Not on his
  2026-10-24 lists.

clients.md has drifted from his current lists; it is the longform autopilot's
registry, not this routine's. roster.md wins here. Flagged to Jeremiah
2026-10-24 because it may also affect the longform autopilot.

## The "Josh" rule

Two Mogul clients are named Josh: **Joshua C.** (Kyle's pod, Jeremiah is BOTH)
and **Josh D.** (Devin's pod, no role). A bare "Josh" with no C or D is always
NEEDS REVIEW, never resolved to Joshua C. by probability.

## Naming

Use these exact names in the summary and the run log. In Notion titles drop the
trailing period, to match the rows already in that database ("Brian M | JULY WK3
| Long-forms", not "Brian M."): so `Joshua C | Fix hook on item 3`.
