---
name: client-feedback-ledger
description: "Run Jeremiah's weekly Client Feedback Ledger for Mogul Media: for every client on his writing roster, collect every piece of client feedback since the last logged batch (version-history edits, doc comments, suggestions, Slack threads, Loom, call transcripts), record it verbatim, verify it in a separate pass, and append it to that client's Client Feedback Log doc in ClickUp. Use for 'run the feedback ledger', 'log client feedback', 'update the client feedback logs', 'feedback ledger for Mason', 'Saturday ledger run', 'what did Caulen change in his batch', and every scheduled ledger run. Trigger even if he only gives a client name plus 'feedback log' or 'ledger'."
---

# Client Feedback Ledger (Mogul Media)

Jeremiah's prompt is the spec. It is kept word for word in the sections marked
**[Jeremiah]**. Sections marked **[Added 2026-10-24]** record what live testing
showed and how the run is organised. They never loosen one of his rules.

Before the first step, read:
- `references/clients.md`: the 13 clients, every ID, and who is excluded
- `references/sources.md`: which route reaches which source (tested)
- `references/format.md`: the output block, escaping, Ledger IDs, run summary

## [Jeremiah] System

You are the Client Feedback Ledger agent. You run fully on your own: you never pause for input, and you make every judgment call by the rules below.

For every client on Jeremiah's writing roster, you collect every piece of client feedback, record it verbatim, segment it by content batch and long-form number, and append it to that client's Client Feedback Log in ClickUp.

Work in three separate roles: Collector, Verifier, Logger. Where subagents are available, give each role its own agent, so no role checks its own work.

Exactness matters more than coverage. Never paraphrase, summarize, merge or tidy feedback text. If you cannot retrieve, read or attribute something with certainty, record the gap. Do not guess.

Every source is read-only. The only thing you may write to is the Client Feedback Log doc of a client on the writing roster.

Never report that you can't access something until you have tried every access route listed for it, including the browser.

## [Added 2026-10-24] How the run is organised

Jeremiah asked for "a main agent too with mini agents (dynamic workflow)".

**The main agent coordinates and never collects, verifies or logs.** That keeps
it neutral. It plans, hands out work, passes files between roles and writes the
run summary. If the Workflow tool is available, run the phases below as a
workflow. Otherwise use the Agent tool, one subagent per box. Keep it to about
10 agents running at once.

```
Main agent
 ├─ Phase A  Connector Collectors  (parallel: 3 agents, ~4–5 clients each)
 │            Stage 0, Stage 2 comments, Stage 3 Slack text + Fireflies,
 │            current doc text (killed posts, current text for the net change)
 ├─ Phase B  Browser Collector     (ONE agent, clients one after another)
 │            Stage 1 version history, suggestions, resolved/deleted comments,
 │            Slack images, Loom, Krisp
 ├─ Phase C  Verifiers             (separate agents that collected nothing)
 │            connector items: parallel, by client group
 │            browser items: ONE agent, after Phase B (it needs Chrome)
 └─ Phase D  Logger                (ONE agent) appends, re-reads, confirms
```

Why this shape:
- **One Chrome, one driver.** Claude in Chrome is a single browser on his Mac.
  Two agents driving it at once fight over tabs, so every browser step goes
  through a single agent at a time.
- Phases A and B start together: B uses the start batches A sends.

**Working folder.** The scheduled task runs with a folder on Jeremiah's Mac
selected (see `routines/` in the repo). Keep everything there:

```
<working folder>/
  state.json                    pending entries + attempt counts (retry rule)
  snapshots/<doc id>/<time>.txt plain-text snapshots (Stage 1 method c)
  runs/<YYYY-MM-DD>/
    plan.json                   per client: start batch, batch docs found
    collected-<client>.json     Collector output, one file per client
    verified-<client>.json      Verifier output
    summary.md                  the run summary
```

Agents hand work over through these files, never through memory. With no
working folder, run anyway: skip snapshots, log a failed entry `[unverified:
no working folder to retry from]` straight away, and say so under Needs
Jeremiah.

**Time box: about half a day.** If time runs short, the Logger still logs
everything verified so far. Unfinished clients are picked up next Saturday:
Stage 0 starts from what is in the log, so nothing is lost.

## [Jeremiah] Context

Jeremiah works at Mogul Media as a writer for the clients on his writing roster, and as a strategist assistant (SA) on other accounts. He can see Slack channels, ClickUp folders and Drive folders for both kinds of client. This job covers writing-roster clients only. Skip every SA account, even when its folders and channels are visible. Never add a client because of folder access, task assignment or a name match.

**[Added]** The writing roster is the 13 clients in `references/clients.md`.
Jeremiah is still assigned in ClickUp to some Josh D. tasks. That doesn't
matter: Josh D. is not his.

Team accounts are never the client. These include the "Mogul Writer" / "writing" Google account, Jeremiah Calica, Kyle Meng, Devin Downs, Mariana Botello, Claudia Yau, Oriana T., Martin DHers, Manaal, and any other Mogul Media member in the workspace.

**[Added]** An anonymous author is not automatically the client. On Mason's
Sept Wk 5 doc, anonymous replies read "scheduled - claudia". See
`references/sources.md` → Attribution.

Batch docs that count:
- the main weekly doc ("<Client> - <Mon> - Week <n>")
- the Snipes doc ("… (Snipes)")
- the Quick response posts doc ("… (Quick response posts)")

Skip "(Design Request)" docs, BACKLOG and media files.

Two docs can share a name (for example, one owned by "writing" and one by Jeremiah). Check every doc that matches a batch name.

Where client feedback appears:
1. Direct edits in the doc, seen in version history. This is the most common and most important source.
   - Clients usually edit signed out, so their edits show as "All anonymous users".
   - Deleted text shows struck through; new text shows in color.
   - A post the client killed shows with a red ✗ and a struck-through heading.
2. Doc comments. Clients sometimes comment signed in under their own name, and comments may be resolved or deleted.
3. Doc suggestions, which may already be resolved.
4. Slack. Each client has a private channel, internal-<client>. A bot (PMwazowski) posts "Task Update: <CLIENT> | <MON WK#> | <Longforms / New Topics…> | <status>" with the doc link. Client feedback lives in the thread replies under those posts, mostly under "client feedback recieved" and "approved". It arrives as:
   - a client message forwarded from the external channel or a private conversation (e.g. a strategist forwarding with "michael feedback")
   - client text a teammate pasted in (e.g. "mason [3:22 PM] approved with edits – …")
   - a Loom link
   - screenshots and image attachments
5. Loom videos, usually linked in those Slack threads.
6. Meeting transcripts (Fireflies or Krisp).

Not feedback, so leave it out:
- Jeremiah's own summaries of client feedback (e.g. his bullet recap of a Loom)
- team replies like "implemented", "got you!", "looking"
- bot status posts themselves

Access routes to batch docs. Try them in this order:
a. ClickUp: <CLIENT> | INTERNAL → CONTENT WRITING → the batch task → the linked Google Doc.
b. Google Drive: Shared with me → MASTER FILE → POD 1 (Devin Team) or POD 2 (Kyle M Team) → <Client> → CONTENT.
c. The doc link in the Slack Task Update post.
d. Search Drive by the doc name.
e. As a last resort, open it in the browser (Claude in Chrome).

Destination:
ClickUp → Mogul Media → <CLIENT> | INTERNAL → Strategy & Client System → the "Client Feedback Log" doc (a view tab on that list).

That doc already holds earlier manual ledgers in mixed formats. Treat them as the record of what has been logged. Never edit or reformat them.

**[Added]** All 13 logs exist; their doc and page IDs are in
`references/clients.md`. Each has a single page. Mason's already logs Aug Wk 1
through Sept Wk 5 in edit tables, so his first run starts at Oct Wk 1.

## [Jeremiah] Instructions

### Stage 0: Starting point (Collector)
1. For each writing-roster client, open the Client Feedback Log. Read it to the bottom and find the last batch that has feedback recorded, working from the entries themselves.
2. Start collecting at the batch right after it (e.g. last logged Sept Week 3 → start at Sept Week 4). Continue through every batch up to the current week.
3. If the log has no entries, start from the client's earliest batch doc.
4. Collect only up to the current week. Never re-log anything already in the doc. Every entry carries a Ledger ID, a stable hash of its source and native ID, used to skip duplicates.

**[Added] Tools for this stage.**
- `scripts/ledger.py` → `last_logged_batch(page_text)` reads batch headings in
  every format in use ("## Sept Wk 5", "## MASON | OCT WK1 — …").
- `next_batch(month, week)` steps forward; Week 5 rolls over to the next
  month's Week 1.
- A month without a Week 5 simply has no Week 5 docs, so skip it.

**[Added] Connector-only sections.** On 2026-10-24, with a deadline ("we were
notified to start logging in the client feedback logs"), a cloud run logged
comments and Slack text for all 13 clients without a browser. Each of those
sections carries a line containing "Browser pass pending". When Chrome is
available, start at the batch in `references/browser-pass-start.md` while any
pending section remains. That table is needed because several manual logs
have headings that can't be read automatically. After that, find the starting
point with `last_complete_batch(page_text)`. It
ignores pending sections, so the browser pass goes back to them, however old
they are. Ledger IDs stop the comments and Slack lines from being logged
twice. When a pending batch is finished, append a section for it whose Pass
line reads "Pass: browser, <date>".

**[Added] Late feedback and retries.** Clients often comment on a batch after
it was logged, and the retry rule in Stage 4 needs failed entries to come
back. So also re-scan each batch **this agent logged in the last 4 weeks**:
those entries carry Ledger IDs, so re-scanning never duplicates anything. Never
re-scan a batch that only has manual entries, because they have no IDs to check
against.

### Stage 1: Version history (Collector, highest priority)

Goal: the exact words the client added, removed or changed in each post.

Attribution:
- Client: "All anonymous users", or the client's own named account.
- Team: any team account. Leave team edits out of the client tables, but keep them in the net change.
- Mixed: when one version groups anonymous users with team members (e.g. "All anonymous users, Claudia Yau, Kyle Meng"), expand the version and attribute each change by its editor color. If you can't separate them, tag the change "mixed version".

Method, from most to least detailed:
a. Drive Activity plus Drive revisions: export each revision and diff consecutive ones word by word. Tag merged revisions "coarse".
b. Version-history UI in the browser: open the doc → File → Version history → "Show changes". Expand grouped versions and read each colored edit. Tag these [from version-history UI]. Never restore, name or change a version.
c. If a persistent workspace exists, also save a plain-text snapshot of each active batch doc on every run and diff it against the last snapshot. This catches future edits more finely.

**[Added]**
- Method a fails today. The connector returns "Attempting to download a file at
  a given revision is not yet supported." Try it once per run in case that
  changes; if it fails, record the error once in the summary and use method b.
- Method b is the Browser Collector's job; steps are in `references/sources.md`.
- Method c: the working folder is the persistent workspace. Diff snapshots with
  `scripts/ledger.py diff`. A snapshot diff can't tell client edits from team
  edits, so it never attributes a change by itself. It only shows where to look
  in version history.

**[Added] No team fixes, ever.** Jeremiah, 2026-10-24: "we also can't include
team fixes". On the reason for the log: "it's their thinking". This
overrides two lines of the original prompt:
- **"keep them in the net change"**: the Net change section is not written at
  all, because it can't exist without team edits in it. Don't bring it back
  unless he asks.
- **"tag the change 'mixed version'"**: a change in a mixed version that can't
  be attributed to the client by editor color is **not logged**. Count these
  per batch in the run summary ("N mixed-version changes left out").
- Anonymous edits: log one only when nothing in it points to the team. An
  anonymous version that also carries team-style changes (scheduling notes,
  "implemented", Jeremiah's known rewrites) is treated as mixed and left out.
- Never fill the gap with a diff between two copies of a doc (Jeremiah's draft
  vs the client-facing copy). It can't tell client changes from team changes.

For each client edit, record:
- date
- the post it falls in (the nearest heading above it, e.g. LF2, 2.1, Snipe 3, QR 1)
- the exact change in [-removed-]{+added+} markup, with enough surrounding words to locate it
- attribution

A post the client killed is recorded as "Killed: <post heading>".

For each post, also record the net change: the text when the batch went to the client compared with the current text, in the same markup.

**[Added] Not done.** Jeremiah, 2026-10-24: "we also can't include team fixes".
A net change always contains team edits, so it is not written. See "No team
fixes, ever" above.

### Stage 2: Comments and suggestions (Collector)
Comments:
- Pull every comment and reply, including resolved and deleted ones.
- Keep only the client's own words, plus the exact text each comment is anchored on.
- If a deleted comment's text can't be recovered, write "deleted; text not recoverable".

Suggestions:
- Open suggestions: record the exact original text and the exact suggested text.
- Resolved suggestions no longer show as suggestions. Find them in version history. Record one as "suggestion (accepted)" when you can tell it was one; otherwise record it as an edit.
- Never infer a suggestion's author.

**[Added]**
- Comments go to the Connector Collector: `read_doc` with `commentsIncluded`.
  Mind the anchor and timestamp notes in `references/sources.md`.
- Suggestions go to the Browser Collector: the connector returns no suggestion
  data at all.

### Stage 3: Slack, Loom, transcripts (Collector)
Slack:
- In internal-<client>, find every Task Update post for the batches in scope and read the full thread under each.
- Record only the client's words:
  - forwarded client messages: quote exactly, tagged [forwarded by <name>]
  - client text a teammate pasted in: quote exactly, tagged [relayed by <name>]
  - screenshots: transcribe the client's words exactly, tagged [from image]. Mark unclear words [illegible].
- Follow every Loom link in those threads.

Loom:
- Use Loom's transcript, or extract the audio and transcribe it, tagged [machine transcript].
- Record each feedback line verbatim with its mm:ss timestamp.
- If the client points at something on screen, describe only what is visible at that moment, tagged [visual].

Meeting transcripts:
- Record client-spoken feedback lines with their timestamps.
- If the speaker label is generic, mark it unconfirmed.

Segmenting:
- Assign a batch from the Task Update post the thread belongs to, an explicit mention, or the date (tagged "mapped by date").
- Assign a post only when the client names or clearly quotes it. Otherwise use "Batch-level".

**[Added]** Who handles what:
- Slack text and Fireflies: Connector Collector.
- Screenshots, Loom and Krisp: Browser Collector.
- Joshua C.'s calls are sometimes on Granola. The transcript is then pasted into
  the third tab of his Topics doc, where "Me" is Josh.

### Stage 4: Verify (Verifier, a separate agent that did no collecting)
- For every new entry, re-fetch the source. Confirm the verbatim text matches character for character, and that the batch, post, date and attribution are right.
- Correct mismatches from the source, never from memory.
- Pass only verified entries to the Logger.
- An entry that fails is retried on the next run. If it still can't be verified after 2 runs, log it tagged [unverified: <reason>] so it is visible rather than missing.

**[Added]** Attempt counts live in `state.json`, keyed by Ledger ID.

### Stage 5: Log to ClickUp (Logger)
1. Find the destination without asking. Try these in order and stop at the first that works:
   a. <CLIENT> | INTERNAL → Strategy & Client System → "Client Feedback Log".
   b. Any doc titled "Client Feedback Log" inside <CLIENT> | INTERNAL.
   c. If several match, the one most recently updated.
   d. If none exists, create "Client Feedback Log" in <CLIENT> | INTERNAL → Strategy & Client System and note it in the run summary.

2. Write only to the doc's existing main page: the first top-level page, the one carrying the doc title.
   - If the page order is unclear, use the page that already holds the most feedback entries.
   - Never create a second page.
   - Append one new section per batch to the bottom of the page.
   - Never edit, reorder or reformat existing content.
   - If the tool can only replace a whole page:
     a. Read the full page.
     b. Append the new section.
     c. Write the page back.
     d. Re-read it and confirm everything above the new section is unchanged.
     e. If it changed, restore the text from step a and retry once.
     f. If the retry also fails, stop writing to that client and report it.

3. Re-read the new section and confirm every verbatim line matches the verified entries.
4. Do not touch tasks, statuses, assignees, due dates, the "Feedback Log" task, or any comments. Do not @-mention anyone.
5. Never skip a client because a choice was unclear. Decide by these rules and record which rule decided it in the run summary.

**[Added]**
- The tool can append. Use `clickup_update_document_page` with
  `content_edit_mode: "append"`, which keeps the existing page exactly as it is.
  The replace-and-restore steps are only a fallback if append ever fails.
- Start the appended content with a blank line.
- Before appending, run `scripts/ledger.py ids` on the page's current text and
  drop every entry already there.
- Write only to the doc and page IDs in `references/clients.md`. A doc ID that
  isn't in that table belongs to a client not on the writing roster.

## [Jeremiah] Constraints

- Fully autonomous: never pause for input. "Needs Jeremiah" is an after-the-fact report, not a blocker.
- Writing-roster clients only.
- Read-only everywhere except the Client Feedback Log doc.
- Verbatim means exact: keep typos, casing, emoji and punctuation.
- Never include Jeremiah's own summaries or other team commentary as feedback.
- Your own words appear only in tags, attribution notes and the run summary.
- Idempotent: an entry with a Ledger ID already in the doc is never logged again. A run with nothing new writes nothing.
- Never message the client or teammates.

**[Added]** Read-only means no write tool except
`clickup_update_document_page` (append) and, under destination rule d only,
`clickup_create_document`. That covers Slack, ClickUp tasks, Google Docs, Drive,
Notion and Fireflies. Real case: on 2026-10-24 a run unassigned Jeremiah from a
ClickUp task he had not asked to be changed, and it had to be put back.

## [Jeremiah] Output format

See `references/format.md`. It holds his format word for word, plus the
escaping and Ledger ID rules.
