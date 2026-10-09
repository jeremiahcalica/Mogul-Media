# Mogul Media automations

## Longform Batch Autopilot

This automates the weekly post-call routine shown in two Looms on Oct 9 2026, for every client. **Before changing anything, read `DECISIONS.md`:** every rule Jeremiah set, the open questions, and how to ship a change.

| Loom step (done by hand) | Autopilot |
|---|---|
| Ask the "Client topic batch and long-form schedule" chat for the updated table | Reads that chat's Claude Doc, "Next Week: Topics and Content Batches (…)", and checks each row's live ClickUp status |
| Open the client's ClickUp Longforms task, open the Fireflies link, download the transcript as MD | Takes the Fireflies (Kyle) or Krisp (Devin) link from the task and reads the full transcript through the connector |
| Download the topic sheet as PDF | Reads the topic sheet, including Kyle's comments, through the Drive connector |
| In the client's Claude project, start a new chat, attach both, paste last week's brief prompt verbatim | Writes the same brief from the same prompt as a Claude Doc: KEPT / PIVOT / NOT DISCUSSED, the original brief, quotes from the call, flags |
| Drive › MASTER FILE › pod › client › Content › last week's doc › Make a copy into My Drive | Copies last week's doc into My Drive as this week's |
| Rename the header, empty Media Folder, delete everything under LONGFORMS, clear formatting | Same edits, in one guarded Google Docs batch |
| Type one line per topic: `N - (X/LI) - (perspective) - (vehicle)`, bold, spaced | Builds the lines from the sheet + brief with the exact rules of the real docs, then bolds and spaces them |
| Star the doc | Stars it on your Mac (Claude in Chrome); otherwise lists it under "Star these" |

Rules that come from your messages rather than the Looms:
- **Top rule:** a Type A topic gets a line only if the call answered it. Type B topics stay unless killed.
- **No transcript:** no brief, but the longform doc is made straight away with every Type B topic. Each Type A topic is left out and listed with the line it would get.
- **Krisp, Devin's clients:** put off for now ("ignore the Krisp first"). A run uses a Krisp route only if one is set up.
- **The schedule doc** is updated every week; each run reads it fresh.
- **New client:** with no earlier doc (Nathan C), the doc is built from an empty Google Doc with the same styles as the copied docs (never an HTML import, which breaks Clear formatting).

### Files

| Path | What |
|---|---|
| `.claude/skills/longform-batch-autopilot/SKILL.md` | The pipeline the routine follows |
| `.claude/skills/longform-batch-autopilot/references/` | Brief format and prompt, longform doc rules, client registry, Loom rules, Chrome steps |
| `.claude/skills/longform-batch-autopilot/scripts/` | `schedule_rows.py` (schedule doc table), `entries.py` (LONGFORMS lines), `longform_batch.py` (the edit batch for a copied doc), `new_doc_batch.py` (a new client's first doc), `verify_doc.py` (the read-back check), `check_quotes.py` (the brief's quotes against the transcript) |
| `.claude/skills/longform-batch-autopilot/tests/` | Golden cases from his real docs (Mason, Caulen, Keval, Teddy, Ben K, Nathan) and the Type A rule; doc-batch and check tests |
| `routines/longform-batch-autopilot.md` | The scheduled routine's prompt and settings, and how dashboard runs work |
| `dashboard/longform-autopilot.html` | The dashboard: run everyone, one client, a test flight or a dry run, type any instruction, watch the run, pause the schedule |
| `DECISIONS.md` | Every decision and why, open questions, test-flight results, how to change it |
| `sops/loom-nuances.md` | Every nuance in the two Looms (151), frame by frame, with evidence and what each segment left open |
| `sops/loom-timelines.md` | Second-by-second timeline of both Looms: clicks, on-screen text, narration |
| `sops/source/` | Mini-SOPs, Loom transcripts and SRTs |
| `dist/longform-batch-autopilot.skill` | The packaged skill to install on your Claude account |

### Install

1. Install the skill on your account: click **Save skill** on the `.skill` file Claude sent, or upload `dist/longform-batch-autopilot.skill` in claude.ai › Customize › Skills. Scheduled runs only see installed skills; they don't have this repo.
2. The routine "Longform Batch Autopilot" runs at 9:52 AM and 9:52 PM Manila once you resume it (it starts paused). If a run ever stops on a permission prompt, open claude.ai › Customize › Connectors and set the tools it names to "Always allow". These are the ClickUp, Fireflies, Google Drive, Google Docs and Claude Docs tools listed in the routine file.
3. Run it by hand from the dashboard at any time, or say "run longforms", "longforms for Caulen", "test flight for Mason" or "dry run for everyone due" in any chat.

### Tests

```
python3 -I .claude/skills/longform-batch-autopilot/tests/run_tests.py
```
Every golden case must print its real lines exactly, and every check test must pass.
