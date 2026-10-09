# Longform Autopilot: decisions and how to change it

Start here before changing anything. This file holds every rule Jeremiah set, the design choices behind the automation, what is still open, and the steps for shipping a change. When something new is decided, add it here in the same commit as the change.

## Where everything lives

| What | Where |
|---|---|
| The process (source of truth) | `.claude/skills/longform-batch-autopilot/` in this repo: `SKILL.md` is the pipeline; `references/` holds the brief format, the doc rules, the client registry and the Loom rules; `scripts/` holds the line and doc scripts; `tests/` holds the golden cases |
| What actually runs | The skill installed on Jeremiah's claude.ai account, from `dist/longform-batch-autopilot.skill`. A change in the repo does nothing until it is repackaged and reinstalled |
| The schedule | Routine "Longform Batch Autopilot" (`trig_01KHnmqSHRLJhaURiFFbgoyG`), 9:52 AM and 9:52 PM Manila, paused until Jeremiah turns it on. Its prompt is in `routines/longform-batch-autopilot.md` |
| The dashboard | `dashboard/longform-autopilot.html`, published as the "Longform Autopilot Console" artifact. It runs the routine by hand and shows the run's output |
| The queue | The Claude Doc "Next Week: Topics and Content Batches (…)", kept by the pinned chat "Client topic batch and long-form schedule" (Cowork session `cse_01VT4cAcAw8Wrd4LPaCmyNiQ`). The chat updates the same doc every week; its dates change. Known doc: https://claude.ai/code/artifact/257af056-867b-41ed-98ea-64cc1f8a1a8b (also https://claude.ai/artifact/5dSKyoafmKQJ93gw67JPi2) |
| What each run did | The Claude Doc "Longform Autopilot — Run Log", made on the first real run, plus the push notification |
| Where the rules came from | `sops/loom-nuances.md` (every nuance in the two Looms, with evidence), `sops/loom-timelines.md`, `sops/source/` (his mini-SOPs and the Loom transcripts) |

## How to change it

1. **Say what changed.** In this repo (any Claude Code session here reads `CLAUDE.md`, which points to this file), describe the new rule and the real case it comes from: client, week, what you expected and what the run did.
2. **Change the rule where it lives:**

   | Kind of change | File |
   |---|---|
   | Which batches run, where inputs come from, what a run may write, the run log or summary | `SKILL.md` |
   | The brief's prompt, layout, statuses, flags | `references/brief.md` |
   | Which topics get a line, line wording, the doc edits | `references/longform-doc.md` and `scripts/entries.py` (line rules) or `scripts/longform_batch.py` / `scripts/new_doc_batch.py` (doc edits) |
   | A client's names, folders, pod, habits | `references/clients.md`, plus `CLIENTS` in `scripts/entries.py` for line habits |
   | Something Jeremiah said that overrides the Looms | `references/loom-rules.md` § Later instructions, and the rule log below |

3. **Test it.** A line rule gets a golden case (`tests/<client>_<mon>_wk<n>_topics.json` + `_expected.txt`, taken from his real doc when one exists). Run `python3 -I .claude/skills/longform-batch-autopilot/tests/run_tests.py`; every case must pass.
4. **Try it on one client.** From the dashboard, run a test flight for a client the change affects ("test flight for Mason"). Its titles start with `[Autopilot test]`, so nothing real is touched. Check the brief and the doc, then trash the test files.
5. **Ship it.** Repackage the skill, commit and push, then install the new `.skill` file (Save skill on the file, or claude.ai › Customize › Skills); it replaces the old one:
   ```
   cd /mnt/skills/examples/skill-creator && python3 -m scripts.package_skill /home/user/Mogul-Media/.claude/skills/longform-batch-autopilot /home/user/Mogul-Media/dist
   ```
6. **Log it.** Add a row to the rule log below.

The routine's prompt rarely needs to change: it loads the skill and lists what a run may write. If it does change, update it with `update_trigger` on `trig_01KHnmqSHRLJhaURiFFbgoyG`. Never delete and recreate it from Claude Code: a routine made there gets no connectors (tried Oct 9).

## Rule log: what Jeremiah decided

All on Oct 9 2026, Manila time, unless the row says otherwise. His words are verbatim. The full mining of the conversation (both URL forms of every link, UTC times, and three mid-turn messages) was done on Oct 10; anything not here is in the session transcript.

| When | His words | What it decided | Lives in |
|---|---|---|---|
| 16:08 | "I want you to help me systemize this process to run on autopilot on my Claude account… it is not just Mason but also other client accounts that'll appear." | The weekly routine from his two Looms and mini-SOPs runs on autopilot, for every client. | Whole skill; `references/clients.md` (15 clients) |
| 16:24 | "the existing brief is copy and pasted into a new Claude conversation along with the transcript of the meeting to ask for the pivots" | Check for an existing brief before making one. Each week's brief is made fresh, from his prompt word for word. | `SKILL.md` Step 2.3; `brief.md` § The prompt |
| 16:35 | "if Kyle is the strategist the transcript is going to be Fireflies, if it's Devin, the transcript is going to be 'Krisp,'… if there's none, it doesn't make sense to push the topic brief PDF to Claude and ask for pivots since there's no transcript" | Transcript source follows the strategist. No transcript, no brief. | `SKILL.md` Step 3; `clients.md` § Shared locations; `loom-rules.md` § Later instructions |
| 16:37 | "same for krisp, it can be 'exported as transcript,'" | Krisp is handled like the Fireflies MD download. | `SKILL.md` Step 3; `chrome-mode.md` § Krisp |
| 16:38 | "don't wait for the transcript- go straight to making the doc" | With no transcript, make the longform doc straight away (narrowed at 22:51–22:52 to Type B only). | `SKILL.md` Step 3 |
| 16:39 | "yes - this works" | Support all three Krisp routes (his Chrome, a drop folder, the connector), whichever is there. | `SKILL.md` Step 3 (lowered at 22:49) |
| 16:40 | "i need you to capture all the nuances in my loom, every single thing" | Every Loom nuance is recorded, frame by frame, and the skill follows them. | `references/loom-rules.md`; `sops/loom-nuances.md` (151); `sops/loom-timelines.md` |
| 16:56 | "try it too for Nathan (Nathan is a new client so there's no folder for him to duplicate the document from so you're going to have to do it manually)" | Test flights for Mason and Nathan C. A new client's first doc is built from scratch. | `SKILL.md` § Modes; `longform-doc.md` § Exceptions |
| 22:02 | "I can't 'clear formatting' for Nathan, but for Mason it's all good in the hood" | A new client's doc must behave exactly like a copied doc: never an HTML import; an empty native doc, pageless, bold on the text. | `SKILL.md` Step 0 and § What you may change; `scripts/new_doc_batch.py`; `scripts/verify_doc.py` |
| 22:14 | "The Mason L. document tells me that everything works as intended, can we do a test flight where you create all the documents for the clients that went in progress this week that are due next week" | Mason's doc is right. Test-fly every client due next week before standardizing. | Test flights below |
| 22:20 | "Nathan's doc looks good… for Joshua C the transcript of the meeting is in the third tab of the topic sheet" | The rebuilt Nathan doc is right. Josh C's transcript is the topic sheet's third tab (Granola). | `SKILL.md` Step 3 § Granola; `clients.md` › Josh C |
| 22:25 | "The easier the setup, the better, and all the nuances in this conversation should be carried forward, one change in process, i'll have to reset it up on all projects" | No per-project setup: one skill and one routine for all clients; client context read centrally. | Design 1–3 below |
| 22:27 | "Run all test flight first then let's decide what to do, i'll check every single output first" | Nothing is finalized until he has checked every output. | Process |
| 22:49 | "Ok, ignore the Krisp first" | Krisp is put off. A run uses a Krisp route only if one already exists, and says "Krisp not set up" once. | `SKILL.md` Step 3; `loom-rules.md` |
| 22:51 | "if something is not discussed in the call (type A topic), or a type A topic was killed/wasn't answered, it shouldn't be in the document, since it's already skipped in the call itself" | **Top rule:** a Type A topic gets a line only if the call answered it. New status NOT ANSWERED. | `SKILL.md` top rule; `longform-doc.md` inclusion table; `brief.md` statuses; `entries.py` `included()`; `tests/type_a_rule_*` |
| 22:52 | "type B topics don't need answer from the client's side so they're retained as-is regardless of whether there's a call or not, type A topics that wasn't answered in the call however must be removed" | Type B stays unless killed, call or no call. With no transcript and no brief: Type B in, Type A out and listed with its would-be line. | `SKILL.md` Step 3 and 5.3; `entries.py` (`call: false`); `tests/type_a_no_transcript_*` |
| 22:53 | "Let's do one last re-run before deciding where this skill / routine lives" | The v2 re-run of all 9 clients. | Test flights below |
| 23:46 | "remember that there may come a time where we'll need to iterate on this, so this conversation is important for us" | What this conversation established must survive later changes: this file and `CLAUDE.md`. | This file |
| 23:49 | "Do you think building a dashboard where I can just click somewhere to run it (like a mini terminal) works too?" | A click-to-run dashboard with a typed-instruction box. | `dashboard/longform-autopilot.html`; `routines/longform-batch-autopilot.md` § Dashboard runs |
| 23:56 | "the Claude Doc that I was pointing at earlier (where the content batches are due) is there right? this?" | Confirmed: the schedule chat's "Next Week: Topics and Content Batches" doc is the queue. | `SKILL.md` Step 1 |
| Oct 10, 00:04 | "it is updated weekly so keep that in mind… Apply the queued fixes, and write the decision log… Point the existing routine at the skill and keep it paused. Build the dashboard. Send you the updated skill file to save." | The schedule doc is the same doc updated every week (dates in its title change): read it fresh every run. Skill + the existing routine (paused) + dashboard, in that order. | `SKILL.md` Step 1.1; `clients.md`; `loom-rules.md`; routine; dashboard |

## Design decisions and why

1. **One skill on his account plus one cloud routine, no per-project setup.** A process change is one edit to the skill, not a redo in every project; the routine runs in the cloud, so his laptop can be off. Accepted with his Oct 10 order.
2. **Client context is read centrally,** from each client's Drive Client Info (Client Brain, feedback ledger) and the Claude Docs ledgers, only for names and sensitivities. His prompt says "Do not invent anything", so every brief line comes from the transcript and the sheet. Limit: rules that live only in a Claude project's memory are invisible to a run; the known ones are copied into `clients.md` (Caulen).
3. **Briefs are Claude Docs on his account, not chats in each client's project.** No tool can list or open his projects from the cloud. The content is the same as his Loom prompt produces. The optional per-project task was withdrawn (22:26) and its file removed.
4. **His prompt is used verbatim** with only the client and strategist swapped in, instead of copying last week's chat (`brief.md`).
5. **Fireflies is read through the connector by meeting ID:** same speakers and timestamps as the MD download. Fireflies search can't find Kyle's calls; fetch by ID works.
6. **A transcript that arrives later** gets its brief plus suggested line changes; a doc that already exists is never edited (`SKILL.md` Step 6).
7. **New-client docs start empty and native, never from HTML.** An HTML import bakes bold and sizes into Heading 1/2, and the Docs API can't change named styles. A survey of 8 clients' docs showed default styles, inline bold, pageless.
8. **Copy into the My Drive root with an explicit `parentId`;** pick last week's doc by the month and week in its title, as in Loom 2.
9. **Test flights prefix every title with `[Autopilot test]`,** so they never collide with real docs, and runs ignore them.
10. **Every write a run may make is listed** in the skill and the routine prompt. On Oct 9 the auto-mode check refused an unlisted Drive copy.
11. **The schedule chat is asked for the update first** (as in Loom 1), then the doc is read. The run never edits or ticks it.
12. **The existing "Longform prep autopilot" routine is repointed, not replaced.** It is the only routine with his connectors; a routine made from Claude Code gets none. Its old prompt called a skill that was never saved, and parked Krisp clients on a waiting list, which his "don't wait" rule forbids.
13. **The routine stays paused** until he has checked a run.
14. **The repo is the memory,** not the chat: chats get summarized and cloud workspaces cleared.
15. **The dashboard starts cloud runs; it doesn't run the job.** A run takes 10–30 minutes per client. Text sent with a manual fire reaches a run only after its first turn (tested Oct 10, 00:11), so the dashboard writes the instruction into the routine's prompt under `[dashboard-run]`, fires, and restores the prompt.
16. **The Type A rule's mechanics:** status NOT ANSWERED (Type A out, Type B in); BLOCKED means only "answered, waiting on an asset or sign-off"; an existing brief's statuses decide even without a transcript.
17. **Line wording follows his real docs,** each flagged "confirm": a header count gives identical lines; "Short-form listicle"; descriptive brackets dropped; LF/MF expanded; a leading "A " dropped; "plus" becomes "+". The v2 Caulen doc matched his real doc line for line.
18. **PIVOT vs KEPT follows his real briefs:** a client who answers a different question and has it accepted is PIVOT (angle) (Josh C T1, T2, T4; Caulen T2); a strategist who only rewords the question is KEPT (gaps flagged) (Caulen T5).
19. **Mason's Oct Wk2 brief layout is the default for every client** until he picks one (open question 1).
20. **Ben's value tweets stay one X/LI line** unless a FOR LINKEDIN note gives a LinkedIn format (his Oct Wk1 doc).
21. **Starring can't be automated in the cloud:** each run lists the docs under "Star these".
22. **No third full re-run after v2;** the remaining fixes were wording polish, applied and tested directly (Oct 10).
23. **Unattended runs never stop to ask:** decide, write it in the summary, keep going; one stuck client never blocks the others.
24. **Mason's "No $ numbers" rule is one summary line** until he says what it covers.

## Open questions for Jeremiah

Until he answers, each is handled as described and flagged in the run summary.

| # | Question | Raised by | Until then |
|---|---|---|---|
| 1 | One brief layout for every client (Mason's?), or keep each client's own (Ben's "Batch-wide direction" + Writer notes, Josh's "Batch status at a glance", Caulen's)? | Ben K, Josh C, Caulen | Mason's layout for everyone |
| 2 | Mason's "No $ numbers": all copy, or only revenue figures? His Wk2 brief flagged none. | Mason | One summary line per run |
| 3 | Josh D T5 is labelled QUOTE TWEET but its objective says "This is the broad TOF snipe": Snipes doc or LONGFORMS? | Josh D | Kept in LONGFORMS, flagged "may be a snipe" |
| 4 | Where do Lior's call links get posted? Oct Wk2 had none, though Kyle wrote "Instructions given on call". | Lior | "call happened, transcript link missing: ask Kyle" |
| 5 | Krisp: finish the connector (claude.ai › Customize › Connectors › Krisp), or create a My Drive "Autopilot Transcripts" drop folder? | Devin's clients | Put off ("ignore the Krisp first"); docs made without a brief |
| 6 | Kyle's bare "2 posts" comment (Josh C T4): two identical lines, or 4A + 4B with the second left out until its vehicle is set? | Josh C | Two identical lines, flagged |
| 7 | Vehicle wording: expand "LF" to "Long-form" (Teddy)? Drop a leading "A " (Josh D)? Is a quote tweet of the batch's own article an "Article wrapper" line (Lior T3, Nathan T1)? | Teddy, Josh D, Lior, Nathan | All done, each flagged "confirm" |
| 8 | Copy each client's Claude-project memory rules (Caulen's "9 figures", plural credit, Brello not the agency, not the DR copywriter) into a Drive file in their Client Info folder that every run reads? | Caulen | Hard-coded in `clients.md` |
| 9 | Is Teddy still his? Arooba wrote on Oct 7 he's moving to Ymarie; the schedule doc still gives him to Jeremiah. | Teddy | Processed, with "confirm he's still yours" |
| 10 | His Josh brief quotes each inspo post's hook from the sheet's screenshots. Should the autopilot read them too? | Josh C | "inspo screenshot not read" |
| 11 | Confirm: with no transcript, Type A topics stay out (listed with their would-be line) rather than in with a "check" flag. His 22:52 message reached the chat seven seconds before that exact question was asked. | All no-transcript clients | Out and listed |
| 12 | Confirm the schedule: 9:52 AM and 9:52 PM Manila, every day. | Routine | That schedule, paused |
| 13 | Ben's long X vehicles ("Thread with headline image", "Quote tweet with 2 doc-screenshot images") vs his shorter "Thread", "GDS/quote tweet of article"; Lior's bracket qualifier next to "+ asset" (T4, T7). | Ben K, Lior | Sheet wording, flagged |

Settled without him, from his own real outputs (say if any is wrong): an off-angle answer that is accepted is PIVOT (angle); waiting on someone else's assets is NOT ANSWERED, so no line (his "On hold"); an answer the client wrote on the sheet after the call doesn't add a line (it is listed); Ben's value tweets stay one X/LI line.

## Test flights

Every flight titled its outputs `[Autopilot test]` or `[Autopilot test v2]`. Each lists his real output where one existed.

**First flight (Oct 9, 17:40–18:00):**
- **Mason:** doc identical to his real Oct Wk2 doc at every index. Brief statuses agreed on 5 of 7; T1/T3 were "KEPT (gaps flagged)" where he wrote KEPT, so that label was narrowed. He accepted it at 22:14.
- **Nathan C:** no call yet, so no brief. The first doc was an HTML import and Clear formatting failed (22:02). It was rebuilt from an empty native doc at 22:16 (10 lines), and he accepted it at 22:20.

**v1, the 7 other clients due Oct 12–16 (22:16–22:47):**

| Client | Result | Main fix |
|---|---|---|
| Lior | 7 lines, no brief (no call link) | The existence check matched the media folder "Lior P. - Oct - Week 1 - 2026" as the doc: exact-title filter |
| Teddy | 6 lines, no brief (Krisp) | Same folder bug; open pivot comments listed as to-dos |
| Josh D | 8 lines, no brief (Krisp) | T5 is really a snipe (open question 3); unanchored EXTRA comment rule |
| Ben K | 14 lines; same as his brief's statuses give | Heading-derived vehicle (T7); existing brief's statuses used; tabs picked by name |
| Josh C | Brief from the third-tab transcript; 5 lines | T6 got a line his brief leaves out: led to his Type A rule |
| Caulen | 7 lines, 2 matched his real doc | Header count means identical lines; bracket wording |
| Keval (Wk3) | 8 lines | PERSPECTIVE ran into his pasted post: cut at the blank line |

**v2, all 9 clients, after the v1 fixes and the Type A rule (23:00–23:33):** Teddy 4/4, Lior 4/4, Nathan 3/3, Josh D 4/5 (EXTRA label too long), Ben K 5/5, Josh C 4/5 (missed details: the 5:15 AM call, "60+ accounts", a hedge written as certain), **Caulen 5/5 with a doc byte-identical to his real doc on a blind run**, Mason 4/4 (identical doc; not blind, since `brief.md`'s examples come from his Mason brief), Keval 5/5. The v2 findings are the fixes applied on Oct 10.

Links to every test doc and brief are in the session transcript; the docs are listed under Cleanup.

## Known limits

- **Starring:** the cloud connectors can't star a file. Runs list new docs under "Star these" (Chrome mode on his Mac can star).
- **Krisp:** no working route yet (open question 5). Devin's clients get docs without briefs unless a brief already exists.
- **Claude-project memory:** invisible to a run (open question 8).
- **Inspo screenshots:** not read (open question 10).
- **Deleting:** the connectors can't trash files; test outputs must be removed by hand.
- **Dashboard:** works only inside claude.ai, for the routine's owner; the first click asks once to allow Claude Code Remote for the page.

## Cleanup Jeremiah still has to do

1. **Trash the test docs in My Drive:** every doc whose title starts with `[Autopilot test]` (10, including "[Autopilot test] Nathan C. - Oct - Week 2 (OLD, HTML import, delete)") or `[Autopilot test v2]` (9). Optionally delete the 8 test brief Claude Docs; runs ignore them either way.
2. **Morning brief routine** (`trig_013pxL6NEyBfyVNCmLttb4pt`): its Oct 8 run has been stuck since 22:09 UTC on a permission prompt for ClickUp `clickup_resolve_assignees`. Answer it, or set that tool to "Always allow".
3. **Install the new skill file** (Save skill). The file sent on Oct 9 at 18:25 is stale.
4. **Before turning the schedule on:** run one test flight or dry run from the dashboard and check it.

## IDs

- Routine `trig_01KHnmqSHRLJhaURiFFbgoyG`; schedule chat `cse_01VT4cAcAw8Wrd4LPaCmyNiQ` (claude.ai/chat/f6da90a8-f5ac-80f7-905d-050254f551d3); schedule doc `5dSKyoafmKQJ93gw67JPi2` = `257af056-867b-41ed-98ea-64cc1f8a1a8b` (the Oct 5–9 week's was `WhJtVnjwL4ztCovnEGmGX8`).
- My Drive root `0APF3ebrWaXbcUk9PVA`; ClickUp workspace `9015589795`, space `90152587982`; Jeremiah 306644176, Kyle 120211600, Devin 88679247. Every client's folders: `references/clients.md`.
- His real outputs used as references: Mason brief `6WmBeLB5ZDBBsAHFG1QENx`, Mason Wk2 doc `167ngEIEU_hgNP-ML1vPBL_NslV7YtK5InF9wQ4s3jOc`, Josh Chin brief `21DpTAV3tTyyz33eKihwL7`, Ben K brief `HSaC73NTFvCt2iT9AMZ1tR`, Caulen Wk2 doc `1b1KiVovf-lHQOztKJMdZ6uv6sXIoid56Df0_7YPTMNg`, Teddy Oct Wk1 brief `Q97rUVTeXVtur3t96zH7wy`.
- Branch `claude/quirky-gates-shi8bl` of `jeremiahcalica/Mogul-Media`.
