# Mogul Media automations

## Longform Batch Autopilot

This automates the weekly post-call routine shown in two Looms on Oct 9 2026, for every client:

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
- **Krisp, Devin's clients:** "Export as transcript". The run reads it from your browser, the Krisp connector, or a drop folder, whichever is available.
- **No transcript:** no brief, but the longform doc is made straight away with every topic.
- **New client:** with no earlier doc (Nathan C), the doc is built from an empty Google Doc with the same styles as the copied docs (never an HTML import, which breaks Clear formatting).

### Files

| Path | What |
|---|---|
| `.claude/skills/longform-batch-autopilot/SKILL.md` | The pipeline the routine follows |
| `.claude/skills/longform-batch-autopilot/references/` | Brief format and prompt, longform doc rules, client registry, Loom rules, Chrome steps |
| `.claude/skills/longform-batch-autopilot/scripts/` | `schedule_rows.py` (schedule doc table), `entries.py` (LONGFORMS lines), `longform_batch.py` (the Google Docs edit batch) |
| `.claude/skills/longform-batch-autopilot/tests/` | Mason Oct Wk2 fixtures; `entries.py` reproduces the real Week 2 lines exactly |
| `routines/longform-batch-autopilot.md` | The scheduled routine's prompt and settings |
| `sops/loom-nuances.md` | Every nuance in the two Looms (151), frame by frame, with evidence and what each segment left open |
| `sops/loom-timelines.md` | Second-by-second timeline of both Looms: clicks, on-screen text, narration |
| `sops/source/` | Mini-SOPs, Loom transcripts and SRTs |
| `dist/longform-batch-autopilot.skill` | The packaged skill to install on your Claude account |

### Install

1. Install the skill on your account: click **Save skill** on the `.skill` file Claude sent, or upload `dist/longform-batch-autopilot.skill` in claude.ai › Customize › Skills. Scheduled runs only see installed skills; they don't have this repo.
2. The routine "Longform Batch Autopilot" runs at 9:52 AM and 9:52 PM Manila. If a run ever stops on a permission prompt, open claude.ai › Customize › Connectors and set the tools it names to "Always allow". These are the ClickUp, Fireflies, Google Drive, Google Docs and Claude Docs tools listed in the routine file.
3. Run it by hand at any time: "run longforms", "longforms for Caulen", or "test flight for Mason".

### Tests

```
python3 -I .claude/skills/longform-batch-autopilot/scripts/entries.py .claude/skills/longform-batch-autopilot/tests/mason_oct_wk2_topics.json
```
The printed lines must equal `tests/mason_oct_wk2_expected.txt`.
