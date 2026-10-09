---
name: longform-batch-autopilot
description: "Run Jeremiah's weekly post-call routine for Mogul Media clients: for every long-form batch in progress, pull the call transcript (Fireflies for Kyle's clients, Krisp for Devin's), write the post-call topic brief as a Claude Doc (KEPT / PIVOT / NOT DISCUSSED against the topic sheet), and set up the week's longform Google Doc in My Drive with one bold line per post. Use for 'run longforms', 'prep this week's long-form batches', 'brief from the call', 'pivots from the call', 'longform doc for <client>', 'Mason OCT WK2 longforms', a ClickUp Longforms link, and every scheduled autopilot run. Trigger even if he only gives a client name plus 'brief' or 'longform doc'."
---

# Longform Batch Autopilot (Mogul Media)

This skill does what Jeremiah showed in two Looms on Oct 9 2026 ("Updating Topic Batches and Transcripts" and "Preparing October Week 2 Longform Topics"), for every client, without him clicking through it:

1. Find which long-form batches are in progress (his schedule doc).
2. For each one, get the call transcript and the client's topic sheet.
3. Write the **post-call topic brief**: the topic sheet compared with the call, topic by topic, marked KEPT, PIVOT or NOT DISCUSSED. It is a Claude Doc.
4. Set up the **longform doc**: last week's doc copied into his My Drive as this week's, emptied, with one bold line per post: `N - (X/LI) - (<perspective>) - (<vehicle>)`.
5. Tell him what was done and what still needs him.

Every client follows the same setup, so the pipeline below works for all of them. `references/clients.md` lists each client's names, pod and folders. Where the Looms set a rule, it is quoted with its timestamp in `references/loom-rules.md`. Follow those rules exactly; they are what Jeremiah checks.

## Modes

- **Everyone due** (default, and every scheduled run): "run longforms", "prep the batches", no client named. Process every queued client, earliest Due first.
- **One client:** "longforms for Mason", "brief for Caulen OCT WK2", or a ClickUp Longforms link. Run the pipeline for that client only, even if the schedule doc doesn't list it, and say so.
- **Unattended (scheduled run):** the same pipeline. Never stop to ask. Decide, write the decision into the summary, and keep going. A client that can't be finished never blocks the others.
- **Test flight:** "test flight for Mason". This is the one-client run with three changes:
  - Every title starts with `[Autopilot test] `.
  - Existing real outputs don't stop the run.
  - At the end, compare each output with the real one, if it exists, and report every difference.
  - The run log is not touched.

## What you may and may not change

Jeremiah authorizes these writes, and only these:
- Send the weekly update request to his schedule chat (Step 1.0), as he does in Loom 1.
- Create **one** brief Claude Doc per client per week.
- **Copy** last week's longform doc into **his My Drive**, and edit **only that new copy**.
- Create and append to the run log Claude Doc, "Longform Autopilot — Run Log".

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
- If the Claude Docs connector gives no instructions, call its `guide` with `["topic.index"]` once.
- Read the `google-workspace` skill's `references/docs.md` before the first Google Docs edit.
- This skill's scripts live in its own `scripts/` folder. Run them with `python3 -I`. They read the files the harness saves when a tool result is large.

## Step 1: Build the queue

The Loom starts in the pinned chat "Client topic batch and long-form schedule". That chat is a Cowork session (`cse_01VT4cAcAw8Wrd4LPaCmyNiQ`) that keeps the schedule in a Claude Doc, refreshed from Slack and ClickUp. Do what Jeremiah does: ask it for the update, then read the doc.

0. **Ask the schedule chat for the update** (skip in a test flight).
   - Call `get_session` on `cse_01VT4cAcAw8Wrd4LPaCmyNiQ`. If it is running, Jeremiah is probably using it: don't send, and note "schedule not refreshed, chat busy".
   - Otherwise call `send_message` to that session with `priority: "later"` and this text (his own words, Loom 1, 0:27–1:04; it needn't be verbatim, so a fixed copy is fine): "Claude, can you give me the updated topic and content batch? By now, there are already new topics (to be submitted next week) and content batch as well, organize them like last time."
   - The refresh takes about 8 minutes and 20+ tool steps (Loom 1, 1:21–1:42). Don't wait idle: carry on with Steps 1–5 using the doc as it stands.
   - Before Step 7, call `get_session` again. Once it is idle and its summary is newer than your message, re-read the doc (step 2 below) and process any row that only now shows up as in progress.
   - If it hasn't finished, note "schedule refresh still running" and stop there.
1. **Find the doc.** Use the Artifact tool's `list` (limit 50) and take the most recently updated artifact whose title starts with `Next Week: Topics and Content Batches`. Last known: `https://claude.ai/artifact/5dSKyoafmKQJ93gw67JPi2` ("(Oct 12–16)").
2. **Read it.**
   - `read` with `ref {"object":"project","id":"<artifact id>"}` gives the body node id (`files[0].content.id`).
   - `read` again with `ref {"object":"node","id":"<body id>"}`, `engine "prose"`, `container {"kind":"project","id":"<artifact id>"}` and no payload. The result is large and gets saved to a file.
   - Run `scripts/schedule_rows.py <saved file>`. It prints the rows of the "Content batches (long-forms)" table: due, client, pod note, checked, status, ClickUp task id, link label and notes.
3. **Check it is current.** The title carries the week's dates, e.g. "(Oct 12–16)". If today (Asia/Manila) is after the last date, the doc is stale. Say so in the summary, then build the queue from ClickUp instead: `clickup_filter_tasks` over space `90152587982`, tasks named `… | Longforms`, status `in progress`, assigned to Jeremiah (306644176), due within the next 10 days.
4. **Pick the rows.**
   - Skip ticked rows (`checked: true`). He ticks a row once the batch is handed in.
   - Key rows by ClickUp task id, never by client name. Jason can have two rows: last week's carryover and this week's.
   - For each remaining row, get the **live** ClickUp task (Step 2). Process it only if the live status is `in progress`. Rows in `to do` haven't had their call yet. Rows in `internal qa` or later are past this step. List both kinds in the summary as "not started" or "already past this step".
   - Read each row's Notes and carry them into that client's run. They hold instructions such as "add a post he shared here as a long-form if there's room" (Caulen) or "combine Keval's written-out topics with the context he adds on the call, and no snipes" (Keval).
5. **Don't add clients the doc leaves out.** If ClickUp shows an in-progress Longforms task assigned to Jeremiah that isn't in the table, list it in the summary and leave it. The doc leaves some out on purpose (e.g. "Brian M's batch went to Neri").

## Step 2: Gather the client's inputs

For each queued client, work in a folder `<client>_<mon>wk<n>/` and keep a short `state.json` of what you found.

1. **The ClickUp task.** Call `clickup_get_task` with `include ["description","attachments","custom_fields","subtasks"]`, and `clickup_get_task_comments`.
   - **Week label:** take it from the task name `<CLIENT> | <MON> WK<N> | Longforms`, e.g. OCT WK2 → month "Oct", week 2. Trust the task the schedule row links to, even when another task with a similar name exists (the ClickUp bot reuses labels).
   - **Strategist:** Kyle (POD 2) or Devin (POD 1). Take it from the assignees and check it against `references/clients.md`.
2. **The links.** Search the comments and the description; never rely on their order.
   - Topics doc: a `docs.google.com/document/d/<id>` link. Kyle's clients have it in a comment, often without `https://`. Devin's clients have it in the description after `Topics:`.
   - Call:
     - Fireflies, Kyle's clients: `fireflies\.ai/view/[^\s:]*::([0-9A-HJKMNP-TV-Z]{26})`, usually in a comment. The ID is the 26 characters after `::`. Drop any `?ref=…` or `?channelSource=…`.
     - Krisp, Devin's clients: `app.krisp.ai/m/<slug>` in the description after `Call:`.
     - Granola: `notes.granola.ai/d/…`. These are notes, not a transcript.
   - If no Topics doc is linked, use the New Topics task for the same week: its "Google Drive / Google Docs" field holds the doc. Otherwise search the client's Topics folder (`references/clients.md`) for the month and week, e.g. `title contains 'OCT' and title contains 'WK2'`. Skip "_" copies in My Drive; those are Jeremiah's imports, not the strategist's doc.
3. **What already exists.** This keeps re-runs safe. Check both outputs before you make anything.
   - **Brief:** search the Artifact `list` for a title that has the client's brief name (Mason L, Josh Chin, Ben K., …), the week ("Oct Wk2", "October Week 2") and "Brief". If one exists, don't make another. Mason Oct Wk2 already has one.
   - **Longform doc:** `search_files` with `title contains '<Name> - <Mon> - Week <N>'`. Exclude titles with suffixes like (Snipes), (Design Request) and (Quick Response), and allow a trailing space. If one exists anywhere (his My Drive or the client's Content folder), don't make another.
   - If both exist, the client is done. Say so in one line.
   - Ignore anything titled `[Autopilot test] …` in both checks. Test copies never count as the real output.

## Step 3: Get the transcript

"It is imperative to download the meeting transcript in MD file. Very, very, very, very important" (Loom 1, 2:05). The point is that Claude reads the real, full transcript with speaker names and timestamps, not a PDF. Use the first route that works:

- **Fireflies (Kyle's clients):** call `fireflies_fetch` with the ID (or `fireflies_get_transcript`). It returns every sentence as `[MM:SS - MM:SS] Speaker: text`, the same content as the MD download. Fetching by ID works even though Fireflies search can't find these calls; they live on Kyle's account.
- **Krisp (Devin's clients):** Jeremiah exports these as a transcript ("Export as transcript"), the same way he downloads the Fireflies MD. Try in this order:
  1. **His browser.** If Claude in Chrome tools are available (a run on his Mac), follow `references/chrome-mode.md` § Krisp: open the link and export the transcript.
  2. **Krisp connector.** If Krisp tools are loaded, find the meeting by title and date and read its transcript.
  3. **Drop folder.** He may have dropped the exported file into the My Drive folder "Autopilot Transcripts". Look for a file whose title has the client's name or the Krisp slug and that was modified after the task went in progress. Read it with `read_file_content`.
  4. If none of these works, the client has no transcript this run (flag "Krisp transcript not available").
- **Granola, or no call link:** no transcript.
- **Kyle's PDF:** Kyle also attaches the transcript as a PDF (`<TITLE>-<hash>.pdf`). Jeremiah skips it and goes to the Fireflies link (Loom 1, 1:48–1:55), so don't use it.
- **Fallback:** if the Fireflies fetch fails, use the transcript text Kyle sometimes pastes into the task's "Google Drive / Google Docs" field. It starts `<Speaker> - 00:00` and ends "Transcribed by https://fireflies.ai/". Flag that you did.

Fix nothing in the transcript. Fireflies drops some profanity and mis-hears jargon (e.g. "Dubai" for media buying, "big ham" for big TAM). Quotes keep the words as transcribed, and a likely reading goes in brackets marked as a reading.

**No transcript means no brief.** "It doesn't make sense to push the topic brief to Claude and ask for pivots since there's no transcript" (Jeremiah, Oct 9). Still make the longform doc (Step 5) with every topic from the sheet as written.

## Step 4: Write the brief (only with a transcript)

1. **Read the topic sheet** with `read_file_content` and `includeComments: true`. It has two tabs:
   - "Client strategy": the header table (CLIENT, WEEK, STRATEGIST, PLATFORMS), the client goal, the hypothesis, then one box per topic: `TOPIC N | TYPE A` (or `TYPE B`, sometimes `TYPE A  2 POSTS`), the title, then ANGLE & DESCRIPTION, FOR <CLIENT> (questions) or INITIAL DRAFT DIRECTION (Type B), VEHICLE, VEHICLE INSPIRATION, OBJECTIVE, PERSPECTIVE.
   - "Strategy": the Loom link, the performance tables, the full hypothesis, and the strategist's raw topic list.
   - The comment threads come back too. Keep them: e.g. Kyle's "Make a pivot to long-form for this week" on Mason's Topic 2.
2. **Write the brief** exactly as `references/brief.md` describes. It starts from Jeremiah's own prompt, used verbatim with only the client and strategist swapped in, and gives the layout of his Mason Oct Wk2 brief. Create it with the Claude Docs `batch` tool: title, byline, then one pending block per section, filled section by section.
3. **Verify it** before moving on:
   - Every topic on the sheet appears, in order, with a status.
   - Every "Original brief" field is copied word for word from the sheet.
   - Every call quote can be found in the transcript at its timestamp.
   - No status rests on a guess. If the call doesn't say, write "Not stated on the call".

## Step 5: Set up the longform doc

Follow `references/longform-doc.md`. In short:

1. **Find last week's doc.** Look in the client's Content folder (Mason's is `Mason Content › 2026`) for the newest doc titled `<Name> - <Mon> - Week <n>` with no suffix. Pick by createdTime, not by arithmetic: Oct Week 1 follows Sept Week 5. "Go to the most recent batch" (Loom 2, 0:37). If it isn't there, use Jeremiah's own My Drive copy of the latest week.
2. **Copy it into My Drive.** Call `copy_file` with the title `<Name> - <Mon> - Week <N>` (e.g. "Mason L. - Oct - Week 2") and `parentId` = his My Drive root. Get the root ID from `get_file_metadata` with `fileId "root"`; it was `0APF3ebrWaXbcUk9PVA`. Never leave `parentId` empty: the copy would land in the client's shared folder. "Instead of duplicating it inside this folder… copy it to My Drive" (Loom 2, 1:09).
3. **Work out the lines.** Write `topics.json` with each topic's number, type, post count, VEHICLE and PERSPECTIVE (copied verbatim from the sheet), and its status from the brief. With no transcript, set `"call": false`. Run `scripts/entries.py topics.json`. It applies every line rule (numbering, 2 POSTS, X/LI splits, wording, who's in and who's out) and prints the lines plus what it left out and why.
4. **Edit the copy in one guarded batch.**
   - Call `read_doc` on the NEW copy; the result is saved to a file.
   - Run `scripts/longform_batch.py <saved read> "<Name> - Week <N> - <Mon>" lines.json`.
   - Send the printed `requests` and `writeControl` with `update_doc`.
   - The batch sets the header, empties the Media Folder link (keeping the "Media Folder:" label), deletes everything under LONGFORMS (post bodies, images, old entries), then writes each line as a bold heading with one blank line after it.
5. **Verify.** Call `read_doc` again and check four things:
   - the header text;
   - no chip or link left on the Media Folder line;
   - nothing under LONGFORMS except the new lines;
   - each line bold, with a blank paragraph after it.
6. **Star it.** "So it should appear on my Starred" (Loom 2, 3:14). The Drive connector can't star a file. On his Mac with Claude in Chrome, star it (`references/chrome-mode.md` § Star). Otherwise put it under "Star these" in the summary with its link.

**Notes from the schedule row and strategist comments** never change the lines automatically. If one asks for something extra ("add a post he shared as a long-form if there's room", "make a pivot to long-form"), add it to the summary as a to-do for Jeremiah.

## Step 6: A transcript that arrives later

The doc may already exist with no brief, because there was no transcript when it was made. If this run finds a transcript, write the brief (Step 4), then compare it with the doc's lines:
- topics that are now NOT DISCUSSED Type A or KILLED;
- vehicles the call changed.

List the differences in the summary as suggestions. Never edit a doc that already exists; Jeremiah may be working in it.

## Step 7: Report

1. **Run log.** Find "Longform Autopilot — Run Log" in the Artifact list. Create it on the first run: title, byline, then the sections.
   - Insert one section at the top per run: `## <date, time> Manila`, then one bullet per client with its brief link, doc link, transcript route, lines added, and flags.
   - Then one bullet each for the clients skipped and why.
2. **Final message.** In a scheduled run it becomes his push notification. Keep it to 8 lines or fewer:
   - `<n> briefs, <n> docs made.`
   - One line per client that needs him, e.g.:
     - "Mason: star doc"
     - "Teddy: Krisp transcript needed"
     - "Caulen: add the extra post from the schedule note?"
   - The run log link.

Only report what actually happened. A doc counts as made only after the read-back check in Step 5 passed. A star counts only if the Chrome step confirmed it.
