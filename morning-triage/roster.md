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

| Client | My role (WRITER / SA-TOPICS / BOTH / NONE) | Strategist | Slack channels | ClickUp folder › list | Status |
| --- | --- | --- | --- | --- | --- |
| Abdul F. | BOTH | Kyle † | #internal-abdul ‡ | ABDUL \| INTERNAL › CONTENT WRITING (`901525097685`) ✓ | active |
| Ben K. | WRITER | Devin † | #internal-ben-k ‡ | BEN K \| INTERNAL › CONTENT WRITING (`901525335531`) ✓ | active |
| Brian M. | SA-TOPICS | _TO FILL_ | #internal-brian-m ‡ | BRIAN M \| INTERNAL › CONTENT WRITING (`901509779186`) ✓ | active |
| Caulen F. | BOTH | Kyle † | #internal-caulen ‡ | CAULEN \| INTERNAL › CONTENT WRITING (`901525335499`) ✓ | active |
| Jason G. | BOTH | Kyle † | #internal-jason ‡ | JASON \| INTERNAL › CONTENT WRITING (`901523997807`) ✓ | active |
| Joshua C. | BOTH | Kyle † | #internal-josh ✓ | JOSH \| INTERNAL › CONTENT WRITING (`901514959348`) ✓ | active |
| Keval S. | BOTH | Kyle † | #internal-keval ‡ | KEVAL \| INTERNAL › CONTENT WRITING (`1200780000001967`) ✓ | active |
| Laura P. | SA-TOPICS | Kyle ✓ | #internal-laura ‡ | LAURA \| INTERNAL › CONTENT WRITING (`1200780000001080`) ✓ | active |
| Lior P. | BOTH | Kyle † | #internal-lior-p ‡ | LIOR P \| INTERNAL › CONTENT WRITING (`901523580791`) ✓ | active |
| Marco B. | WRITER | Devin † | #internal-marco ‡ | MARCO \| INTERNAL › CONTENT WRITING (`901524688017`) ✓ | active |
| Mason L. | BOTH | Kyle † | #internal-mason ‡ | MASON \| INTERNAL › CONTENT WRITING (`901507747284`) ✓ | active |
| Matt O. | SA-TOPICS | _TO FILL_ | #internal-matt ‡ | MATT O\| INTERNAL › CONTENT WRITING (`901513869537`) ✓ | active |
| Michael K. | BOTH | Kyle † | #internal-michael-k ‡ | MICHAEL K \| INTERNAL › CONTENT WRITING (`901524922267`) ✓ | active |
| Nathan C. | WRITER | Devin † | #internal-nathan-c ‡ | NATHAN C \| INTERNAL › CONTENT WRITING (`1200780000003023`) ✓ | active |
| Phil R. | SA-TOPICS | _TO FILL_ | #internal-phil ‡ | PHIL \| INTERNAL › CONTENT WRITING (`1200780000001073`) ✓ | active |
| Shane H. | BOTH | Kyle † | #internal-shane-hummus ‡ | SHANE \| INTERNAL › CONTENT WRITING (`901507172439`) ✓ | active |
| Teddy T. | WRITER | Devin † | #internal-teddy ‡ | TEDDY \| INTERNAL › CONTENT WRITING (`901524097226`) ✓ | active |

✓ = verified live in ClickUp on 2026-10-24 by task search. Folder and list IDs
are real, not derived. Every client's list is named `CONTENT WRITING`; only the
parent folder differs. Space `90152587982` ("Shared with me").

‡ = found in Slack on 2026-10-24 by channel search, not stated by Jeremiah.
All 23 `#internal-*` channels are private; every one matching a roster client is
listed above. Confirm before the first real run.

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
- **Brian M.** is SA-TOPICS only today, confirmed by Jeremiah 2026-10-24:
  "true, Brian M is now SA topics only". ClickUp shows the switch cleanly — his
  last `Longforms` task is SEP WK3, and his current OCT WK4 task is
  `New Topics`. The Notion database still holds his old longform rows
  ("Brian M | JULY WK3 | Long-forms"). Past rows are not evidence of current
  ownership. A writing ask for Brian M. is NOT MINE.

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

## #internal-josh is Joshua C. — resolved

Jeremiah, 2026-10-24: "Joshua C. - i left Josh D.'s internal channel before".

So **#internal-josh (`C09DD4N69EJ`) is Joshua C.'s channel** and Agent B scans
it, even though Devin Downs created it. Josh D.'s channel still exists; Jeremiah
is simply no longer in it, which is why a Slack search run as him returns only
one Josh channel.

**The rule that follows:** a channel's absence from a Slack search is not
evidence the channel does not exist. It can mean Jeremiah left it — which is
itself a signal he holds no role there. Never conclude "no channel" from a
search; conclude "no channel he is in".

Laura P.'s strategist is **Kyle**, confirmed by Jeremiah the same day
("Confirm - it's Kyle").

## Channels that exist but are NOT scanned

These `#internal-*` channels have no roster client, so Agent B never reads them:
#internal-zarak-sarah, #internal-toby, #internal-brian-c, #internal-apptics,
#internal-dana, #internal-davie.

Jeremiah, 2026-10-24, on the names not on his lists: "the ones that aren't on
the list may be clients that have already left". "May be" is not confirmation,
so nothing here is treated as a departure — they are simply clients he holds no
role for, which produces the same result: never MINE.

## The "Brian" rule

Two Mogul clients are named Brian: **Brian M.** (SA-TOPICS, #internal-brian-m)
and **Brian C.** (no role, #internal-brian-c, ClickUp folder
`BRIAN C | INTERNAL`). Both have channels, both have ClickUp folders, and both
have rows in the Notion database. A bare "Brian" with no M or C is NEEDS REVIEW,
exactly like a bare "Josh".

## The "Josh" rule

Two Mogul clients are named Josh: **Joshua C.** (Kyle's pod, Jeremiah is BOTH)
and **Josh D.** (Devin's pod, no role). A bare "Josh" with no C or D is always
NEEDS REVIEW, never resolved to Joshua C. by probability.

## Naming

Use these exact names in the summary and the run log. In Notion titles drop the
trailing period, to match the rows already in that database ("Brian M | JULY WK3
| Long-forms", not "Brian M."): so `Joshua C | Fix hook on item 3`.
