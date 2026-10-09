---
name: longform-batch-autopilot
description: "Run Jeremiah's weekly post-call routine for Mogul Media clients: for every long-form batch in progress, pull the call transcript (Fireflies for Kyle's clients, Krisp for Devin's), write the post-call topic brief as a Claude Doc (KEPT / PIVOT / NOT DISCUSSED against the topic sheet), and set up the week's longform Google Doc in My Drive with one bold line per post. Use for 'run longforms', 'prep this week's long-form batches', 'brief from the call', 'pivots from the call', 'longform doc for Caulen', 'Mason OCT WK2 longforms', 'test flight for Mason', 'dry run for everyone due', a ClickUp Longforms link, and every scheduled or dashboard autopilot run. Trigger even if he only gives a client name plus 'brief' or 'longform doc'."
---

# Longform Batch Autopilot (Mogul Media)

This skill does what Jeremiah showed in two Looms on Oct 9 2026 ("Updating Topic Batches and Transcripts" and "Preparing October Week 2 Longform Topics"), for every client, without him clicking through it:

1. Find which long-form batches are in progress (his schedule doc).
2. For each one, get the call transcript and the client's topic sheet.
3. Write the **post-call topic brief**: the topic sheet compared with the call, topic by topic, marked KEPT, PIVOT or NOT DISCUSSED. It is a Claude Doc.
4. Set up the **longform doc**: last week's doc copied into his My Drive as this week's, emptied, with one bold line per post: `N - (X/LI) - (<perspective>) - (<vehicle>)`.
5. Tell him what was done and what still needs him.

**Top rule for the doc (Jeremiah, Oct 9): a Type A topic gets a line only if the call answered it.** A Type A topic that was not discussed, was killed, or came up but went unanswered (deferred, "I'll think about it", no take given) stays out of the doc: it was already skipped on the call. Type B topics need no answers, so they stay in unless killed.

Every client follows the same setup, so the pipeline below works for all of them. `references/clients.md` lists each client's names, pod and folders. Where the Looms set a rule, it is quoted with its timestamp in `references/loom-rules.md`. Follow those rules exactly; they are what Jeremiah checks.

## Modes

- **Everyone due** (default, and every scheduled run): "run longforms", "prep the batches", no client named. Process every queued client, earliest Due first.
- **One client:** "longforms for Mason", "brief for Caulen OCT WK2", or a ClickUp Longforms link. Run the pipeline for that client only, even if the schedule doc doesn't list it, and say so.
- **Unattended (scheduled run):** the same pipeline. Never stop to ask. Decide, write the decision into the summary, and keep going. A client that can't be finished never blocks the others.
- **Test flight:** "test flight for Mason". This is the one-client run with four changes:
  - Every title starts with `[Autopilot test] ` (or the label the request gives, e.g. `[Autopilot test v2] `): the longform doc's file name, and the brief's name and its H1. Never the header line inside the doc.
  - Existing real outputs don't stop the run: its `[Autopilot test]` copies are allowed even when the real brief and doc exist (the routine prompt authorizes this).
  - At the end, compare each output with the real one, if it exists, and report every difference.
  - The run log is not touched.
- **Brief only / doc only:** "brief only for Keval", "doc only for Nathan C". The one-client run, stopping after Step 4 (no doc; Step 5.7 still fills the brief's Longform doc section) or skipping Step 4 (no brief). A doc-only run takes the statuses from an existing brief for that client-week; with none, it works as with no transcript (Type B in, Type A out and listed) and says so.
- **Dry run:** "dry run for everyone due", "dry run for Caulen". Do the reads (Steps 1–3, and `entries.py` on the sheet when there is one) and report what each client would get: brief or not and why, the lines, what is left out, every problem and gate.
  - Statuses for `entries.py`: an existing brief's (Step 5.3). With a transcript and no brief, judge each topic's status as Step 4 would, from the transcript, without writing a brief, and mark the lines "provisional". With no transcript, `"call": false`.
  - Write nothing at all: no schedule chat message, no brief, no doc, no run log entry.
- **Dashboard run:** the routine's prompt ends with a section that starts with the line `[dashboard-run]`. Jeremiah typed or clicked that instruction on his dashboard, and for that run it replaces "everyone due". Read it as if he had typed it here; it picks one of the modes above, or asks a question about the queue (answer it from the reads; write nothing).
  - The dashboard stamps its section with a line `Valid until: <ISO time>`, 10 minutes after it wrote it. If that time has passed when the run starts, or the section has no such line, ignore the section, run everyone due, and say in the summary that a stale dashboard instruction was ignored (audit, Oct 10).

## What you may and may not change

Jeremiah authorizes these writes, and only these:
- Send the weekly update request to his schedule chat (Step 1.0), as he does in Loom 1, only when Step 1.0 says to.
- Create **one** brief Claude Doc per client per week.
- **Copy** last week's longform doc into **his My Drive**, and edit **only that new copy**. For a new client with no earlier doc, create an empty Google Doc in his My Drive instead and fill only that (`references/longform-doc.md` § Exceptions; never an HTML import).
- Create and append to the run log Claude Doc, "Longform Autopilot — Run Log".
- In a test flight, the same brief and doc as `[Autopilot test]` copies, even when the real ones exist (§ Modes).

Never do any of these:
- Edit, tick or comment on the schedule doc. He ticks rows himself.
- Edit ClickUp (status, comments, fields), the Topics doc, last week's longform doc, Fireflies or Krisp.
- Message anyone (Slack, email), trash or move any file, or share anything.
- Invent anything. Every brief line comes from the transcript or the topic sheet. If something isn't there, say it's missing.

If a write is refused (a permission prompt or a denied tool call), stop writing for that client, keep its reads, and report exactly which call was refused. Don't retry it another way.

## Step 0: Load what you need

- Load the connector tools with tool search:
  - Claude Docs: `read`, `batch`, `update`
  - ClickUp: `get_task`, `get_task_comments`, `filter_tasks`
  - Fireflies: `fireflies_fetch`, `fireflies_get_transcript`
  - Google Drive: `search_files`, `read_file_content`, `get_file_metadata`, `copy_file`, `create_file`
  - Google Docs: `read_doc`, `update_doc`
  - claude-code-remote: `get_session`, `send_message`
- Before the first Claude Docs call other than a doc's birth, call `guide` with `["topic.index"]` once. Loading the docs skill alone isn't enough: it only points back to the connector.
- Google Docs API rules that matter here. The batch scripts already follow them; keep to them in any request you write yourself:
  - Indexes are UTF-16 code units (an emoji counts 2 or more), and every insert or delete shifts what follows. Compute indexes from a read taken after the last write; never reuse old ones.
  - Every `location` and `range` carries the `tabId`. Without it the request goes to the first tab.
  - Send each edit as one `update_doc` batch guarded by `writeControl.requiredRevisionId` from that read. If it is refused, read again and rebuild; never resend without the guard.
  - A named style (Heading 1, Heading 2) can be applied but never changed. So never create a doc from `text/html`: the import bakes bold and sizes into the heading styles, and Clear formatting can't undo them (Nathan C, Oct 9). New docs here are empty native docs filled by `scripts/new_doc_batch.py`.
- This skill's scripts live in its own `scripts/` folder. Run them with `python3 -I`. They read the files the harness saves when a tool result is large.

## Step 1: Build the queue

The Loom starts in the pinned chat "Client topic batch and long-form schedule". That chat is a Cowork session (`cse_01VT4cAcAw8Wrd4LPaCmyNiQ`) that keeps the schedule in a Claude Doc, refreshed from Slack and ClickUp. Do what Jeremiah does: ask it for the update, then read the doc.

0. **Ask the schedule chat for the update** (everyone-due runs only).
   - Send it only in an everyone-due run, and only when the doc is stale (step 3) or was last updated more than 24 hours ago (its time in the Artifact list, step 1). So find the doc and check its dates first. Never send it in a one-client, brief-only, doc-only, test-flight, dry-run or question run. Each message starts an ~8-minute refresh in his pinned chat; sent on every run, that was about 14 a week (audit, Oct 10).
   - Call `get_session` on `cse_01VT4cAcAw8Wrd4LPaCmyNiQ`. If it is running, Jeremiah is probably using it: don't send, and note "schedule not refreshed, chat busy".
   - Otherwise call `send_message` to that session with `priority: "later"` and this text (his own words, Loom 1, 0:27–1:04; it needn't be verbatim, so a fixed copy is fine): "Claude, can you give me the updated topic and content batch? By now, there are already new topics (to be submitted next week) and content batch as well, organize them like last time."
   - The refresh takes about 8 minutes and 20+ tool steps (Loom 1, 1:21–1:42). Don't wait idle: carry on with the rest of Step 1 and Steps 2–5 using the doc as it stands, or the ClickUp queue if it is stale (step 3).
   - Before Step 7, call `get_session` again. Once it is idle and its summary is newer than your message, find and re-read the doc (steps 1 and 2 below) and process any row that only now shows up as in progress. This is for everyone-due runs only: a one-client run never takes on other clients.
   - If it hasn't finished, note "schedule refresh still running", don't re-read the doc, and go on to Step 7. A run always reaches Step 7.
1. **Find the doc.** The schedule chat writes the schedule to a Claude Doc every week, and the dates in the title change: `Next Week: Topics and Content Batches (<dates>)`. "It is updated weekly so keep that in mind" (Jeremiah, Oct 9).
   - Open the known doc first: artifact `5dSKyoafmKQJ93gw67JPi2` (`https://claude.ai/artifact/5dSKyoafmKQJ93gw67JPi2`, also `https://claude.ai/code/artifact/257af056-867b-41ed-98ea-64cc1f8a1a8b`; "(Oct 12–16)" on Oct 9).
   - Also use the Artifact tool's `list` (limit 50) for titles starting `Next Week: Topics and Content Batches`. It shows one doc per week: "(Oct 5–9)" is `WhJtVnjwL4ztCovnEGmGX8`, "(Oct 12–16)" is `5dSKyoafmKQJ93gw67JPi2`. Use the one whose title dates are latest. Use the update time only to break a tie: a tick on last week's doc makes it the most recently updated (audit, Oct 10). If a later week than the known doc's exists, use it, and say in the summary that the known ID here and in `references/clients.md` needs updating.
   - Always read it fresh. Never reuse rows from an earlier run.
2. **Read it.**
   - `read` with `ref {"object":"project","id":"<artifact id>"}` gives the body node id (`files[0].content.id`).
   - `read` again with `ref {"object":"node","id":"<body id>"}`, `engine "prose"`, `container {"kind":"project","id":"<artifact id>"}` and no payload. The result is large and gets saved to a file.
   - Run `scripts/schedule_rows.py <saved file>`. It prints the rows of the "Content batches (long-forms)" table: due, client, pod note, checked, status, ClickUp task id, link label and notes.
3. **Check it is current.** The title carries the week's dates, e.g. "(Oct 12–16)". If today (Asia/Manila) is after the last date, the doc is stale.
   - If it is stale, don't wait for a refresh: a cloud session can't sleep in the foreground (audit, Oct 10). Say so in the summary, then build the queue from ClickUp now: `clickup_filter_tasks` over space `90152587982`, tasks named `… | Longforms`, status `in progress`, due within the next 10 days, either assigned to Jeremiah (306644176) or belonging to a client in `references/clients.md` (Keval's task is assigned to Ymarie and Kyle, not him). Flag every assignee mismatch except Keval's, which the schedule doc settles (`references/clients.md`).
   - If step 0 sent a refresh, re-read the doc before Step 7 (step 0) and process any in-progress row the ClickUp queue missed (everyone-due runs).
4. **Pick the rows.**
   - Work the rows in Due order, earliest first. The Due column is already the earliest of the team-calendar day, the ClickUp date and any date Kyle set in Slack (Mason: Due Oct 12, ClickUp Oct 13), so use it rather than the ClickUp date.
   - Skip ticked rows (`checked: true`). He ticks a row once the batch is handed in.
   - Key rows by ClickUp task id, never by client name. Jason can have two rows: last week's carryover and this week's.
   - For each remaining row, get the **live** ClickUp task (Step 2). Process it only if the live status is `in progress`. Rows in `to do` haven't had their call yet. Rows in `internal qa` or later are past this step. List both kinds in the summary as "not started" or "already past this step".
   - Read each row's Notes and carry them into that client's run. They hold instructions such as "add a post he shared here as a long-form if there's room" (Caulen) or "combine Keval's written-out topics with the context he adds on the call, and no snipes" (Keval).
5. **Don't add clients the doc leaves out.** If ClickUp shows an in-progress Longforms task assigned to Jeremiah that isn't in the table, list it in the summary and leave it. The doc leaves some out on purpose (e.g. "Brian M's batch went to Neri").

## Step 2: Gather the client's inputs

For each queued client, work in a folder `<client>_<mon>wk<n>/` and keep a short `state.json` of what you found.

1. **The ClickUp task.** Call `clickup_get_task` with `include ["description","attachments","custom_fields","subtasks"]`, and `clickup_get_task_comments`.
   - **Week label:** the topic sheet's name sets the week ("Mason L | OCT WK2 | Topics" → Oct, Week 2). In Loom 2 (0:59) Jeremiah reads it off the sheet's tab, not last week's number plus one.
     - Cross-check it with the task name `<CLIENT> | <MON> WK<N> | Longforms`. The ClickUp bot reuses labels, so if the two disagree, go by the sheet and flag it.
     - Trust the task the schedule row links to, even when another task with a similar name exists.
   - **Strategist:** Kyle (POD 2) or Devin (POD 1). Take it from the assignees and check it against `references/clients.md`.
2. **The links.** Search the comments and the description; never rely on their order.
   - Read the description from `markdown_description`: in Devin's tasks `text_content` reads "Topics: \nCall:" with the links stripped. Match the labels in any case ("topics:", "Call:").
   - Topics doc: a `docs.google.com/document/d/<id>` link. Kyle's clients have it in a comment, often without `https://`. Devin's clients have it in the description after `Topics:`.
   - Call:
     - Fireflies, Kyle's clients: `fireflies\.ai/view/[^\s:]*::([0-9A-HJKMNP-TV-Z]{26})`, usually in a comment. The ID is the 26 characters after `::`. Drop any `?ref=…` or `?channelSource=…`.
     - Krisp, Devin's clients: `app.krisp.ai/m/<slug>` in the description after `Call:`. Drop the query string (`?active_tab=…&tr_utm_source=…`).
     - Granola: `notes.granola.ai/d/…`. These are notes, not a transcript.
     - Before saying there is no call link, also scan the same-week New Topics task's comments and its "Google Drive / Google Docs" field (Lior Oct Wk2).
   - If no Topics doc is linked, use the New Topics task for the same week: its "Google Drive / Google Docs" field holds the doc.
     - Otherwise search Drive by title for the month and week, e.g. `title contains 'OCT' and title contains 'WK2' and title contains '<client>'`. Don't search only by the Topics folder: sheets can sit in a subfolder (Nathan's is in TOPICS › OCT 2026).
     - Keep a doc owned by either pod's strategist account (mistymeng2000@ or manaallmalikk@): Ben's sheet is owned by mistymeng2000@ though he is Devin's. If there are several, prefer the one in the client's Topics folder.
     - Skip "_" copies in My Drive; those are Jeremiah's imports, not the strategist's doc.
3. **What already exists.** This keeps re-runs safe. Check both outputs before you make anything.
   - **Brief:** search the Artifact `list` (limit 200) for a title that has the client's brief name (Mason L, Josh Chin, Ben K., …), the week and "Brief". Match case-insensitively, the month short or long (`Oct|October`) and the week as `W(ee)?k\s*N`: Jeremiah's own Teddy brief is "October WK1 Post-Call Brief". Also accept a title with the client's brief name, "Brief" and a call date inside this batch's call week (the days before the task went in progress): his real Shane brief is "Shane H. — Topic Briefs from 9/30 Call (Wiz x Shane)" (audit, Oct 10). If one exists, don't make another. Mason Oct Wk2 already has one.
   - **Longform doc:** `search_files` with `title contains '<Name> - <Mon> - Week <N>' and mimeType = 'application/vnd.google-apps.document'`, then keep only results whose title, trimmed, is **exactly** `<Name> - <Mon> - Week <N>`. Drive matches words, not the string: the search for "Lior P. - Oct - Week 2" also returns the media FOLDER "Lior P. - Oct - Week 1 - 2026" ('2' matches '2026'), and taking that as the doc would skip the client (test flight, Oct 9). Suffixed siblings ((Snipes), (Design Request), (Quick Response)…) don't count. If an exact match exists anywhere (his My Drive or the client's Content folder), don't make another.
   - If both exist, the client is done. Say so in one line.
   - If the doc exists and no brief does, still look for a transcript (Step 3). If there is still none, the client gets one run-log line, "<client>: doc made <date>, waiting for transcript" (the doc's created date), and nothing in the push. Don't list its comments, gates or `would_be` lines again; the run that made the doc did. Go to Step 6 only when a transcript appears (audit, Oct 10). A test flight runs in full either way (§ Modes).
   - Ignore anything whose title starts with `[Autopilot test` in both checks. Test copies never count as the real output.
   - Record every raw hit of both checks in `state.json`, with why each was dropped (folder, suffix, other week, test copy; Lior Oct Wk2).

## Step 3: Get the transcript

"It is imperative to download the meeting transcript in MD file. Very, very, very, very important" (Loom 1, 2:05). The point is that Claude reads the real, full transcript with speaker names and timestamps, not a PDF. Use the first route that works:

- **Fireflies (Kyle's clients):** call `fireflies_fetch` with the ID (or `fireflies_get_transcript`). It returns every sentence as `[MM:SS - MM:SS] Speaker: text`, the same content as the MD download (with timestamps and speaker names, no Fireflies branding). Fetching by ID works even though Fireflies search can't find these calls; they live on Kyle's account.
  - Check it is the right call: the title names the client and the strategist, in either form Kyle uses: `<FIRST> <LAST INITIAL> X <STRATEGIST>` ("MASON L X KYLE") or `<First> <Last> and <Strategist full name>` ("Keval Shah and Kyle Meng", "caulen Foster and Kyle Meng"; Lior's is "Reut Amariyo and Kyle Meng"). Confirm with the attendee emails, and that the date falls in the days before the task went in progress. If it names another client or the transcript is empty, treat it as no transcript and flag it.
  - The call date in the brief is the Manila date of `DateString` (UTC).
- **Krisp (Devin's clients):** "ignore the Krisp first" (Jeremiah, Oct 9). Use a route only if it is already there, in this order:
  1. Claude in Chrome tools (a run on his Mac): `references/chrome-mode.md` § Krisp.
  2. Krisp tools loaded: find the meeting by title and date and read its transcript.
  3. A My Drive folder "Autopilot Transcripts": a file whose title has the client's name or the Krisp slug, modified after the task went in progress, read with `read_file_content`.
  - If none is there, note "Krisp not set up" once per run, not per client. Each Devin client then has no transcript, so no new brief (a brief that already exists still gives the statuses, Step 5.3). With no brief at all, make its doc anyway; its push line reads "<client>: doc made without brief (Krisp)" (Teddy Oct Wk2).
- **Granola (Josh C):** the call's transcript is pasted into **the third tab of the Topics doc**, after "Client strategy" and "Strategy" (Jeremiah, Oct 9). Use that tab whatever it is named. `read_file_content` flattens tabs, so read the doc with `read_doc` and take the tab by position, then check it really holds a transcript (speaker names, timestamps or dialogue). Any Topics doc with such a tab counts as having a transcript.
  - In the tab, "Me" is Josh (he records), "Kyle Meng" is Kyle and "Them" is anyone else. There are no timestamps: use brief.md's no-timestamp variant. The tab's "Date:" line is the call date.
- **No call link and no transcript tab:** no transcript. If a sheet comment or a task comment says a call happened ("Instructions given on call", Lior, Oct 9), say so: "call happened, transcript link missing: ask <Strategist> for it".
- **Kyle's PDF:** Kyle also attaches the transcript as a PDF (`<TITLE>-<hash>.pdf`). Jeremiah skips it and goes to the Fireflies link (Loom 1, 1:48–1:55), so don't use it.
- **Fallback:** if the Fireflies fetch fails, use the transcript text Kyle sometimes pastes into the task's "Google Drive / Google Docs" field. It starts `<Speaker> - 00:00` and ends "Transcribed by https://fireflies.ai/". Flag that you did.

Fix nothing in the transcript. Fireflies drops some profanity and mis-hears jargon (e.g. "Dubai" for media buying, "big ham" for big TAM). Quotes keep the words as transcribed, and a likely reading goes in brackets marked as a reading.

**No transcript means no brief.** "It doesn't make sense to push the topic brief PDF to Claude and ask for pivots since there's no transcript" (Jeremiah, Oct 9). Still read the topic sheet (Step 4.1) and make the longform doc (Step 5) straight away: every Type B topic as the sheet has it, and no Type A topic, because nothing shows the call answered it (Jeremiah, Oct 9: Type B is "retained as-is regardless of whether there's a call or not"; Type A "that wasn't answered in the call however must be removed"). List each Type A topic left out in the summary, with its `would_be` line from `entries.py`, so he can add it if the call did answer it (Step 7).

## Step 4: Write the brief (only with a transcript)

1. **Read the topic sheet** with `read_file_content` and `includeComments: true`.
   - **Take the topics from the tab named "Client strategy" or "CLIENT STRATEGY"** (any case). Pick it by name, never by position or by tabId `t.0`: Ben's stale STRATEGY tab is `t.0`. It holds:
     - the header table (CLIENT, WEEK, STRATEGIST, PLATFORMS), the client goal and the hypothesis;
     - then one box per topic. The header reads `TOPIC N | TYPE A` (or `TYPE B`, sometimes `TYPE A  2 POSTS`; separators `|` or `│`). A third part can be a label like Snipe or Quick Response, and ✅ / ❌ marks can appear.
     - each box has the title, ANGLE & DESCRIPTION, FOR <CLIENT> (questions) or INITIAL DRAFT DIRECTION (Type B), VEHICLE, VEHICLE INSPIRATION, OBJECTIVE and PERSPECTIVE.
     - Devin's sheets put per-platform vehicles in bullets. Devin's sheets can be titled `… | HYPOTHESIS` instead of `… | Topics`.
     - An italic third header segment that names a format ("*Quote Tweet VT*", Ben T8) is a vehicle hint, not a label; only Snipe or Quick Response there counts as a label.
     - Some clients paste their own written-out answer into the topic box after PERSPECTIVE (Keval). The PERSPECTIVE field ends at the first blank line; the rest is the client's answer (brief.md has a slot for it).
     - A Type B topic can carry no INITIAL DRAFT DIRECTION, only a SOURCE line (Keval T7); a topic can have no VEHICLE or PERSPECTIVE at all, only a heading that names the format and a list of items (Ben's "VALUE TWEETS - INSTAGRAM REEL REPURPOSE" with two reels): the vehicle comes from the heading and the post count from the number of items, flagged.
   - **The other tab** ("Strategy"): the Loom link, the performance tables, the full hypothesis and the strategist's raw topic list. A third tab, when there is one, holds a pasted call transcript (Josh C's Granola calls).
   - **Freeform topics.** A "Topic 0 - …" or bare "Topic N" note outside the tables is a topic too.
   - **Comment threads come back too.**
     - **Open** comments are the strategist's live notes and count: e.g. Kyle's "Make a pivot to long-form for this week" on Mason's Topic 2, or "Make a 2nd post on Boxing and chad mentality".
     - **Resolved** comments are already applied; ignore them. If a resolved comment asks for a change the sheet doesn't show ("CHANGE VEHICLE & PERSPECTIVE" with only the vehicle changed, Teddy T2), list it as a check for the strategist; never act on it.
     - Comments by Jeremiah himself are his own notes: list them, never act on them.
     - A comment's time is its last-modified time (head and replies share it); call it that, never "posted at".
   - **The two tabs can disagree** (Teddy: T1 "Quick Response" vs "Snipe", T2's vehicle). Use Client strategy and list each disagreement. A Type B box that carries a FOR <CLIENT> question, or a type, label or link that differs from the Strategy tab's raw list (Lior T1, T7), is a strategist gate.
     - Compare the tabs on every run, with or without a transcript (Step 5 says where they go with no brief).
     - A tab `references/clients.md` calls stale gets one line, "STRATEGY tab stale, CLIENT STRATEGY used" (Ben K), not a gate per topic.
   - **Use the strategist's sheet,** in the client's Topics folder. Skip "_" copies in My Drive.
2. **Read the client's context.** Jeremiah writes the brief inside the client's Claude project, so Claude has the client's files. Give yourself the same:
   - read the Client Brain and the feedback ledger in the client's `Client Info` folder, if they exist. Some clients have neither (Mason's Client Info has no Client Brain, and the sheet's "Client Brain Link" points to an old Topics doc). If they're missing, say so in the run log and go on;
   - check the Claude Docs ledger (e.g. "Mason L. — Feedback Ledger") in the Artifact list.
   - Use them only to spell names right and to flag sensitivities, e.g. Mason: "no $ numbers", never cross-reference Jason. They may raise a flag when a figure clashes with the sheet or the call (Keval: "$2M agency" on the sheet vs "$2.5M/year" in his ledger), citing the file by name, but never settle it and never supply quotes or facts.
   - Per-client rules that live only in a client's Claude project memory can't be read from a run; the ones known so far are in `references/clients.md` (e.g. Caulen's "9 figures" and plural credit). Apply those.
   - Build the brief from the "Client strategy" tab, the tab he exports to PDF. Use the "Strategy" tab only to resolve a reference.
3. **Write the brief** exactly as `references/brief.md` describes. It starts from Jeremiah's own prompt, used verbatim with only the client and strategist swapped in, and gives the layout of his Mason Oct Wk2 brief. Create it with the Claude Docs `batch` tool: title, byline, then one pending block per section, filled section by section.
4. **Verify it** before moving on:
   - Every topic on the sheet appears, in order, with a status.
   - Every "Original brief" field is copied word for word from the sheet.
   - Every call quote can be found in the transcript at its timestamp. Run `python3 -I scripts/check_quotes.py TRANSCRIPT BRIEF.md --sheet SHEET.txt` (one more `--sheet` for each other file the brief quotes: Client Brain, ledger, Strategy tab) and fix what it reports, as `references/brief.md` § Checks says, until it exits 0 (no NOT FOUND or WRONG TIME left). It found two misquotes in Josh C's Oct Wk2 brief.
   - Every tab disagreement and strategist gate from step 1 is in the brief.
   - No status rests on a guess. If the call doesn't say, write "Not stated on the call".

## Step 5: Set up the longform doc

Follow `references/longform-doc.md`. In short:

1. **Find last week's doc.** Look in the client's Content folder (Mason's is `Mason Content › 2026`) for the newest doc titled `<Name> - <Mon> - Week <n>` with no suffix. Pick the latest by the month and week in the title, not by arithmetic (Oct Week 1 follows Sept Week 5); use createdTime only to break ties or across a year change. "Go to the most recent batch" (Loom 2, 0:37). If it isn't there, use Jeremiah's own My Drive copy of the latest week.
   - **No earlier doc at all** (a new client's first batch, Nathan C Oct Wk2): there is nothing to copy, so skip steps 2 and 4. Work out the lines (step 3), then follow `references/longform-doc.md` § Exceptions: Drive `create_file` of an empty native doc in his My Drive, `scripts/new_doc_batch.py`, then `verify_doc.py` (step 5), which also checks that Heading 2 is not bold and the doc is pageless. Say "first batch: built as a new doc" in the summary.
2. **Copy it into My Drive.** Call `copy_file` with the title `<Name> - <Mon> - Week <N>` (e.g. "Mason L. - Oct - Week 2") and `parentId` = his My Drive root. Get the root ID from `get_file_metadata` with `fileId "root"`; it was `0APF3ebrWaXbcUk9PVA`. Never leave `parentId` empty: the copy would land in the client's shared folder. "Instead of duplicating it inside this folder… copy it to My Drive" (Loom 2, 1:09).
   - Record the source doc's `modifiedTime` in `state.json` before copying, and check it again after. If it changed, say so in the summary: someone else was editing it (Josh D's Oct Wk1 doc was touched at 23:08, mid-flight).
3. **Work out the lines.**
   - Write `topics.json` (schema in `references/longform-doc.md`). Set `"client"` to the doc name and `"strategist"` to Kyle or Devin (problems name them: "confirm with Kyle"). For each topic give its number, type, label, title, post count, ✅/❌ or strikethrough, VEHICLE, PERSPECTIVE and OBJECTIVE, copied exactly from the sheet, and the same topic's label on the other tab if it differs (`other_tab_label`). Add its status from the brief.
   - Set these optional keys when they apply, so `entries.py` can report them:
     - `inferred`: what was inferred rather than read, e.g. the vehicle and post count taken from a heading (Ben T7, "VALUE TWEETS - INSTAGRAM REEL REPURPOSE").
     - `other_tab_type`: the Strategy tab's type when it differs; `client_question`: a Type B box that carries a FOR <CLIENT> question. Both are type-clash gates (Lior T1, T7); the sheet's type still decides the line. Leave them and `other_tab_label` empty when the other tab is the stale one (Ben K): it gets its one line instead (step 4.1).
     - `written_answer`: a short description of the client's own written answer on the sheet (Josh D's "RECENT WINS JOSH SENT").
   - **Post counts.** A header count ("(3 post)", "2 POSTS") sets `posts`, and gives that many identical lines with the sheet's perspective, even when a comment names each post's subject: those subjects go only in the brief (his real Caulen Oct Wk2 doc). A bare "N posts" comment with no subjects (Kyle on Josh C T4) sets `posts_override`, with `posts_override_source` saying where it came from ("Kyle's sheet comment"), flagged.
   - **Extra posts** go in `extra_posts` only when a comment or the call asks for a post beyond the count ("Make a 2nd post on …", Mason Wk1).
   - **A comment that isn't on a topic** but asks for an extra post (Devin's "EXRA – turn this newsletter into an article with Doc SS QT" on the Client Brain link, Josh D) becomes a freeform topic, `"freeform": true`, numbered with the next integer after the last sheet topic. Its `perspective_override` is a short 1–3 word subject, like Jeremiah's "Trybe" for Josh D's newsletter (his Oct Wk1 doc). Its vehicle is the comment's format in sentence case ("X article + Doc SS QT"). Flag it.
   - If a brief for this client-week already exists (Jeremiah's or an earlier run's), take each topic's status from it and leave `"call": true`, even when this run has no transcript. Posts the brief lists outside the sheet with no vehicle set get no line; put them in the summary as "add lines?" (Ben's inner-circle offer, Oct Wk2).
   - With no transcript and no brief, set `"call": false`: Type B topics go in, Type A topics stay out and are listed.
   - Run `scripts/entries.py topics.json`. It applies every line rule and prints the lines, what it left out and why, `would_be` (the line each Type A topic left out would get, numbered "?"), `notes` and `problems`:
     - numbering, post counts, X/LI splits and wording;
     - snipes and quick responses left out;
     - who's in and who's out by status;
     - per-client habits.
   - If `problems` isn't empty, still write the doc, but put each problem at the top of that client's summary.
4. **Edit the copy in one guarded batch.**
   - Call `read_doc` on the NEW copy. A large result (over about 50K characters) is saved to a file. A smaller one comes back inline: if it's short, write it to a scratchpad file; if it's too long to copy faithfully, write the cut-down `subset` form `longform_batch.py` accepts, as its module docstring describes it: `"subset": true`, documentId, revisionId, tabId, bodyEnd, and the header, Media Folder, anything between, and LONGFORMS paragraphs, each with startIndex, endIndex, namedStyleType and elements, copied exactly. First check with `read_file_content` that the doc has one Media Folder line and one LONGFORMS.
   - Run `scripts/longform_batch.py <saved read> "auto:<Mon>:<N>" lines.json`. The `auto:` form changes only the week number and month in last week's header, so each client's own wording survives (Loom 2, 1:24).
   - Send the printed `requests` and `writeControl` with `update_doc`.
   - The batch sets the header, empties the Media Folder link (keeping the "Media Folder:" label), deletes everything under LONGFORMS (post bodies, images, old entries), then writes each line as a bold heading with one blank line after it.
5. **Verify** with `scripts/verify_doc.py <read_doc after the edit> lines.json --header "<header>"`. With the `auto:` form, `<header>` is the header the batch writes: the `replaceText` of the `replaceAllText` request, the last item of the `requests` that `longform_batch.py` printed (e.g. "Mason L. - Week 2 - Oct"). For a new doc, it is the header you gave `new_doc_batch.py`. It checks:
   - the header text;
   - no chip or link left on the Media Folder line;
   - nothing under LONGFORMS except the new lines, each followed by one blank paragraph;
   - each line bold on the text itself (its run reads `bold: true`; the doc's Heading 2 style is not bold, so Clear formatting works as in his docs);
   - no images left, one tab, pageless;
   - the doc's Heading 1 and Heading 2 named styles are there (it fails if they are missing, and warns on non-default sizes).
   Always also run `verify_doc.py --md` on `read_file_content` of the doc (Mason and Josh D Oct Wk2 flights); it drops an unbolded first H1 that is only the tab title ("# Content", Josh C). If the `read_doc` result comes back inline and too long to save, write `verify_doc.py`'s minimal form instead (its docstring lists the fields) and run the read check on that. Never skip the style checks.
6. **Star it.** "So it should appear on my Starred" (Loom 2, 3:14). The Drive connector can't star a file. On his Mac with Claude in Chrome, star it (`references/chrome-mode.md` § Star). Otherwise put it under "Star these" in the summary with its link.
7. **Fill the brief's "Longform doc" section** (`references/brief.md` § Sections, 6) once the doc is made. The brief is born in Step 4, before the doc exists, so nothing else fills it (audit, Oct 10). Fill it only in a brief this run made, with one `update` that replaces its pending block:
   - Doc made: the doc link, every line as plain `-` bullets, then what was left out and why.
   - Brief-only run: "Doc not made (brief only)".
   - Doc already existed: its link, plus Step 6's suggested changes (fill it after Step 6).
   - Doc not made, or its check failed: "Doc not made: <why>".

### Comments, notes and snipes

- **A strategist comment asking for another post** ("Make a 2nd post on …") adds a flagged line, as Jeremiah did in Mason's Week 1.
- **A comment asking for a pivot** ("Make a pivot to long-form") changes nothing on the line; it goes in the brief's Note.
- **With no brief** (no transcript):
  - Every OPEN sheet comment goes in the summary and the run log as a to-do: topic, author, last-modified Manila time and text. When it pivots a topic that has a line, add "line kept as the sheet has it, confirm" (Devin on Teddy T4 "Rework to keep focus around Teddy Answer"). When the topic is out, add "applies if you add the line" (Devin on Josh D T3 "PIVOT TO PUNCHY 'update' Vts").
  - Every tab disagreement and strategist gate from Step 4.1 goes in the summary too (Lior Oct Wk2).
- **Schedule-row notes** ("add a post he shared here as a long-form if there's room") never add lines. They go in the summary as a to-do.
- **Snipes and quick responses** have their own docs, which this skill doesn't make. List them in the summary ("Keval T1 snipe: goes in the (Snipes) doc").
  - Call the sibling doc by last week's exact suffix: Teddy has used "(Snipe)", "(Snipes)" and "(Quick Response)".
  - If this week's Snipes doc already exists, say so; don't raise a "Snipes or QR doc?" question (Josh C Oct Wk2).

## Step 6: A transcript that arrives later

The doc may already exist with no brief, because there was no transcript when it was made. If this run finds a transcript, write the brief (Step 4), then compare it with the doc's lines:
- Type A topics now NOT DISCUSSED or NOT ANSWERED, and any KILLED topic (lines to remove). Type B lines stay unless killed;
- Type A topics the call did answer, which a no-transcript doc left out (lines to add);
- vehicles the call changed.

Best: run `entries.py` again with `"call": true` and the brief's statuses, and diff its lines against the doc's. Then fill the brief's "Longform doc" section with the doc's link and these suggestions (Step 5.7).

List the differences in the summary as suggestions. Never edit a doc that already exists; Jeremiah may be working in it.

## Step 7: Report

1. **Run log.** Find "Longform Autopilot — Run Log" in the Artifact list. Create it on the first run: title, byline, then the sections.
   - Insert one section at the top per run: `## <date, time> Manila`, then one bullet per client with its brief link, doc link, transcript route, lines added, and flags: every `problems` item, open-comment to-dos, tab disagreements and gates, and assignment doubts (a client the schedule gives him but ClickUp or Slack gives someone else, except where `references/clients.md` says the schedule settles it, as for Keval; with the source: "Teddy: confirm he's still yours (Arooba, Oct 7: moving to Ymarie)").
   - In each client's bullet, under "Type A left out": every `would_be` line from `entries.py`, as printed, so Jeremiah can paste it if the call did answer it. A topic with the client's written answer on the sheet adds "answered in writing? add line?" (`references/longform-doc.md`).
   - Then one bullet each for the clients skipped and why. A client whose doc is waiting for its transcript gets only its one line (Step 2.3).
2. **Final message.** In a scheduled run it becomes his push notification. Keep it to 8 lines or fewer:
   - `<n> briefs, <n> docs made.`
   - One line naming every new doc to star: "Star these: Mason, Caulen, …". Every new doc needs starring, so a line per doc overflowed 8 lines with 9 clients (audit, Oct 10).
   - A separate line only for a client with a problem or a doubt, e.g.:
     - "Josh D: doc made without brief (Krisp)"
     - "Teddy: confirm he's still yours (Arooba, Oct 7)". An assignment doubt keeps its source, as in the run log.
     - "Caulen: add the extra post from the schedule note?"
   - The run log link.
   - If that runs over 8 lines, keep the client lines that fit and end with "+N more in the run log".
   A test flight or dry run may go past 8 lines: print its difference report, `would_be` lines and problems first, then the short summary.

Only report what actually happened. A doc counts as made only after the read-back check in Step 5 passed. A star counts only if the Chrome step confirmed it.
