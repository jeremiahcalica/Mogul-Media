# Rules from the Looms, with evidence

Jeremiah recorded two Looms on Fri Oct 9 2026, using Mason L. Oct Week 2 as the example:
- **Loom 1** "Updating Topic Batches and Transcripts" (3:48).
- **Loom 2** "Preparing October Week 2 Longform Topics" (3:28).

Every rule below was checked frame by frame against both Looms and three transcripts (Loom's SRT and two Whisper runs).
- Times are video times. The narration runs a few seconds behind his clicks, so each rule goes by what is on screen.
- He addresses Claude directly ("Okay, Claude, what we're going to do here is you're going to…", 0:00), so every "you're going to" is a step for the autopilot.
- "Skill" says where the skill does it. A cloud run has no browser, so the click-by-click route is replaced by a connector call that gives the same result. `references/chrome-mode.md` keeps the click routes for a run on his Mac.

## Loom 1: the schedule

| # | Rule | Evidence | Skill |
|---|---|---|---|
| 1.1 | Start in the existing schedule chat, "Client topic batch and long-form schedule". Don't open a new chat or a new schedule doc; the same Claude Doc is updated in place. | 0:00–0:22 "you're going to go into this conversation"; he types in its Reply box and never clicks New. 1:21 "Using Claude Docs: Update" on the same artifact. | Step 1.0 sends to session `cse_01VT4cAcAw8Wrd4LPaCmyNiQ`. |
| 1.2 | Rename it once, not every run. It used to be "Client topic batch schedule". | 0:09–0:18 ⋮ › Rename, types " and long-form", Save. | Never renamed. |
| 1.3 | The request needn't be verbatim: "you don't have to take this by verbatim… write something like this". Its three parts: the updated topic batches (new topics *to be submitted next week*), the content batches, organized like last time. | Typed 0:27–1:04, said 1:04–1:19. He corrected the wording three times ("for next" → "(to be submitted next week)", "long-form" → "content batch"). | Step 1.0 sends his exact text. |
| 1.4 | "Content batch" means the long-form batch: the doc's "Content batches (long-forms)" table and ClickUp's "… \| Longforms" tasks. | 0:51–0:56 he types "long-form", deletes it, types "content batch". | Step 1.2 reads that table. |
| 1.5 | Leave the model as it is (Opus 5.5). He opens the picker, checks it, closes it. | 1:17–1:19. | Not applicable; the routine sets the model. |
| 1.6 | Wait for the refresh to finish before using the table. It took over 8 minutes and 25 tool steps; he paused the recording ("let us assume that this is already done loading"). | Clock 15:16 → 15:24 between 1:20 and 1:21; "Used ClickUp, used Slack, and 23 more steps 8m 39s" at 1:42. | Step 1.0: carry on with the doc as it stands, re-check the chat before Step 7, and pick up rows that only appear after the refresh. |
| 1.7 | Never edit the schedule doc by hand; he only selects text to point at it. | 1:28–1:34. | Read-only. |
| 1.8 | A client is ready when its row's Status is "In progress": "let's take Mason for an example. He is in progress." To do rows wait; Internal QA rows are past this step. | 1:28–1:34. | Step 1.4, using the live ClickUp status. |
| 1.9 | The deadline is the Due column, the earliest of the team-calendar day, the ClickUp date and a date Kyle set in Slack. Mason: Due Oct 12, ClickUp Oct 13. | Doc intro and Mason's row note, 1:22–1:36. | Step 1.4 works rows in Due order. |
| 1.10 | Open the task from the row's ClickUp link, and check the task name is the right week (Keval's row links "OCT WK3 Longforms"). | 1:38–1:44. | Step 1.4 keys rows by task id; Step 2.1 cross-checks the week. |
| 1.11 | Kyle's rows have no pod tag; rows tagged "(Devin's pod)" are Devin's. | Table at 1:27. | `references/clients.md`. |

## Loom 1: the ClickUp task and the call

| # | Rule | Evidence | Skill |
|---|---|---|---|
| 2.1 | For Kyle's clients the inputs are his three Activity comments, posted together: the Topics doc chip, a transcript PDF, the Fireflies link. The description and fields are empty. | 1:44–1:48, all three "Oct 7 at 6:48 am". | Step 2.2 searches comments and description by pattern. |
| 2.2 | Open them in order: topic sheet, then the call. | 1:49 topic sheet tab, 1:55–1:59 Fireflies tab. | Step 2 then Step 3. |
| 2.3 | Never use Kyle's PDF transcript. | 1:48–1:55 he skips it; 2:05 "It is imperative to download the meeting transcript in MD file. Very, very, very, very important." | Step 3. |
| 2.4 | Fireflies: "…" beside the title › Download › Transcript tab › MD; keep Include timestamp and Show speaker name, tick Remove Fireflies Branding; keep the default file name. | 2:03–2:20; file "MASON-L-X-KYLE-88cf75cc-9bb4.md", 20.3 KB, 60 lines. | Step 3 (`fireflies_fetch` gives the same text); `chrome-mode.md` § Fireflies. |
| 2.5 | The meeting is titled `<FIRST> <LAST INITIAL> X <STRATEGIST>` ("MASON L X KYLE") and was recorded days before the batch. | 1:59, Oct 07 2026, 30:47. | Step 3 checks title and date. |
| 2.6 | Topic sheet: `<Client> \| <MON> WK<N> \| Topics`, header table CLIENT / WEEK / STRATEGIST / PLATFORMS. Use the tab the link opens, "Client strategy"; its badge "1" is Kyle's open comment. | 1:49–1:53, URL `?tab=t.mcidewmh8er7`. | Step 4.1 reads the Client strategy tab and its open comments. |
| 2.7 | Read the sheet, the task and the call only. No edits anywhere. | 1:50–2:43. | "What you may and may not change". |

## Loom 1: the brief

| # | Rule | Evidence | Skill |
|---|---|---|---|
| 3.1 | Make the brief in a new chat inside the client's project ("Mason L."), from the project page's composer, not claude.ai/new. | 2:19–2:34 "open another Claude tab… go to Mason L." | The cloud run writes the brief as a Claude Doc with the same content; `routines/per-project-brief.md` and `chrome-mode.md` put it in the project. |
| 3.2 | Attach two files to the message itself, never to project knowledge: the transcript MD first, then the topic sheet as PDF (File › Download › PDF, Tab "Current Tab"). | 2:33–2:45; last week's chat shows the same pair, MD then PDF. | Step 4 reads both through the connectors. |
| 3.3 | Copy the prompt from last week's chat "<Client> brief from <Strategist> meeting" (the latest one), the final message ending "In a claude doc pls", and paste it verbatim: "Please, in verbatim, please prompt it like this." | 2:45–3:00. The first try without that line ended "Claude's response was interrupted." | `references/brief.md` holds the exact text, curly quotes included. |
| 3.4 | The output must be a Claude Doc. | 2:47 and 3:02. | Step 4.3. |
| 3.5 | Send only once both attachments have finished processing; leave Opus 5.5 / High / Auto. | 2:45–2:59. | `chrome-mode.md`. |
| 3.6 | Wait until Claude has finished the doc; its summary changed while he watched ("four were kept" → "three were kept"). | Paused 3:01–3:02 for 1m47s; still editing at 3:27. | Step 4.4 verifies the finished doc. |
| 3.7 | The brief has a `# \| Topic \| Vehicle \| Status` table with KEPT / PIVOT (…) / NOT DISCUSSED, and per topic the Original brief, From the call and a Note. | 3:02–3:27. | `references/brief.md`. |
| 3.8 | KEPT and PIVOT topics go in the batch. | 3:14–3:21. | `entries.py` `included()`. |
| 3.9 | A NOT DISCUSSED topic goes in only if it is Type B: "topic six is type A, which means we are not going to include this… Type B. No answer needed, which is included." | 3:35–3:46. | `entries.py` `included()`. |
| 3.10 | Check the type on the sheet's `TOPIC N \| TYPE x` header; never guess it. He guessed 6 and 7 were both Type B, then checked: 6 was Type A. | 3:21–3:39. | `topics.json` takes `type` from the header. |
| 3.11 | "2 POSTS" in the header means two entries. | 3:29 `TOPIC 2 \| TYPE A  2 POSTS`; the final doc has entries 2 and 3. | `entries.py` post counts. |
| 3.12 | Type B drafts carry writer placeholders like `[Time] later` and `[2 photos: ecom brand era + now]`. Keep them; don't fill them. | 3:44–3:46. | `references/brief.md`. |

## Loom 2: the copy

| # | Rule | Evidence | Skill |
|---|---|---|---|
| 4.1 | Start once the pivots and topics are known: "after you check out the pivots and what the topics are". | Opening line. | Step 5 runs after Step 4, or straight away when there's no transcript (his instruction of Oct 9). |
| 4.2 | Go to Drive › Shared with me › MASTER FILE › the pod folder ("POD 2 (Kyle M Team)"), find the client's folder ("Mason Littlejohn", he searches the page for "mason"), then "Mason Content" › "2026". | 0:00–0:35 "click on Master File, click on Kyle M, and then search for Mason Littlejohn… go into Mason Content 2026". | `references/clients.md` holds each client's Content folder id. |
| 4.2b | Open the most recent batch by its month and week: "go to the most recent batch, I think it is October Week 1". It is the shared copy owned by writing@. Siblings like "(Snipes)" and "GDS - June - Week 4 - 2026" aren't batches. | 0:38–0:50; he selects "Mason L. - Oct - Week 1" (owner writing, 92 KB) over "Sept - Week 5". | Step 5.1 and `references/longform-doc.md` step 1. |
| 4.3 | Never edit last week's doc; make a copy: "Make a copy. Very important." | 0:51–0:57. | Step 5.2. |
| 4.4 | Name the copy `<Name> - <Mon> - Week <N>`: delete "Copy of ", change only the number. No year, no "Longforms". | 0:52–1:06. | Step 5.2. |
| 4.5 | The week comes from the topic sheet's name, not last week plus one: "This is October Week 2 Topics. This is going to be October Week 2 Long Form batch." | 0:59–1:04, hovering the sheet's tab. | Step 2.1. |
| 4.6 | Save it to the root of My Drive: "instead of duplicating it inside this folder… copy it to My Drive". | 1:07–1:17; `copyDestination=0APF3ebrWaXbcUk9PVA`. | Step 5.2 sets `parentId` to the root. |
| 4.7 | Leave the dialog's three boxes off: no sharing, no comments, no resolved comments. | 0:52 and 1:18, never clicked. | `copy_file` carries none of them. |
| 4.8 | Don't rename the file again afterwards; "rename this" means the header inside the doc. | 1:24–1:26. | — |

## Loom 2: the edit

| # | Rule | Evidence | Skill |
|---|---|---|---|
| 5.1 | Header: change only the week number, keeping that doc's own order (`Mason L. - Week 2 - Oct`, week before month, unlike the file name). Heading 1, bold, Arial 20. | 1:24–1:26. | `longform_batch.py` `auto:<Mon>:<N>`. |
| 5.2 | Delete last week's Media Folder chip and leave the label empty: "keep it empty for now. Keep it empty." | 1:27–1:37. | `longform_batch.py` removes the chip and keeps "Media Folder: ". |
| 5.3 | Keep "LONGFORMS" as it is. | 1:39. | — |
| 5.4 | Delete everything under LONGFORMS to the end: every old entry, post body, image, highlighted note and the SCHEDULE COMMENT block. "Delete all of this." | 1:35–1:39; the page count drops from 4 to 1. | `longform_batch.py`. |
| 5.5 | He keeps entry 1's heading as a template and clears its formatting (Heading 2 stays, bold goes). The end state is what counts: Heading 2 + bold lines. | 1:40–1:43 "Clear formatting." | `longform_batch.py` writes fresh Heading 2 + bold lines; the Mason test flight matched his finished doc to the index. |
| 5.6 | One line per topic, in sheet order, starting at 1 each week: "do the same for every topic". | 2:41–2:48. | `entries.py`. |
| 5.7 | Line shape: `N - (<platform>) - (<perspective>) - (<vehicle>)`. Bare number, space-hyphen-space, each slot in round brackets, nothing after the last bracket. | 2:31–2:41. | `entries.py`. |
| 5.8 | Perspective: the sheet's PERSPECTIVE word for word, every sentence, minus the final period. Not from the narration (he said "60s and 70s" but typed the sheet's "60s"). | 1:58–2:32. | `entries.py` `perspective_text()`. |
| 5.9 | Platform: the tag in the sheet's VEHICLE ("Longform (X/LI)" → `(X/LI)`), not repeated in the vehicle slot. | 2:04–2:35. | `entries.py` tag handling. |
| 5.10 | Vehicle: the vehicle type, "Longform" → `Long-form`. | 2:33–2:41 "the long-form vehicle. Long-form." | `entries.py` `norm_vehicle()`. |
| 5.11 | Each topic's own fields only. He had started line 1 with Topic 2's values and corrected them. | 2:44–2:48. | `entries.py` works topic by topic. |
| 5.12 | Bold all the lines together once they're written, then space them out: "bold it. Bold. Then space it out." Only the lines; the header block is already bold. | 2:47–3:09. | `longform_batch.py` bolds the lines, one blank line after each. |
| 5.13 | No placeholder or duplicate lines in the end. His five copies of line 1 were a demo, deleted at 3:23. | 2:51–3:24. | Lines come only from `entries.py`. |
| 5.14 | Never edit the topic sheet or resolve its comments. | 1:45–3:27. | Read-only. |
| 5.15 | Star the doc last, once it's right: "So it should appear on my starred." Star once and leave it on. | 3:10–3:22. | Step 5.6. The connectors can't star; in Chrome mode it does, otherwise it's listed under "Star these". |

## Later instructions that override the Looms

From Jeremiah, Oct 9 2026:
- Kyle's clients' calls are on Fireflies; Devin's are on Krisp, exported with "Export as transcript".
- With no transcript, don't make a brief: "it doesn't make sense to push the topic brief PDF to Claude and ask for pivots since there's no transcript". Make the longform doc straight away ("don't wait for the transcript, go straight to making the doc") with every Type B topic; Type A topics stay out, since nothing shows the call answered them ("type B topics don't need answer from the client's side so they're retained as-is regardless of whether there's a call or not, type A topics that wasn't answered in the call however must be removed").
- Each week's brief is a new chat, with last week's prompt copied verbatim along with the new transcript.
- **A Type A topic gets a line only if the call answered it:** "if something is not discussed in the call (type A topic), or a type A topic was killed/wasn't answered, it shouldn't be in the document, since it's already skipped in the call itself". Status NOT ANSWERED covers a Type A topic that came up but got no answer (deferred, no take given), even when something else is pending too.
- A new client (Nathan C.) has no earlier doc to copy, so the doc is built from scratch (`references/longform-doc.md` § Exceptions).
