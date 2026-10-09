# Routine: Longform Batch Autopilot

- **Routine:** "Longform Batch Autopilot", `trig_01KHnmqSHRLJhaURiFFbgoyG`. It was made from a Cowork chat on Oct 9 as "Longform prep autopilot" and repointed to this prompt on Oct 9. It is the only routine that has the connectors (see "Where it lives").
- **Schedule:** `CRON_TZ=Asia/Manila 52 9,21 * * *`, every day at 9:52 AM and 9:52 PM Manila.
  - The 9:52 PM run lands before Jeremiah's night shift, after Kyle's US-morning calls.
  - The 9:52 AM run picks up anything posted overnight.
  - Each run skips what is already done, so running twice a day is safe.
- **State:** paused (enabled = false) until Jeremiah has checked a run. A paused routine still runs when started by hand (tested Oct 9), so the dashboard works while it is paused.
- **Mode:** a fresh session on each fire, auto permission mode, the model set on the routine, push notification on finish.
- **Connectors:** Claude_Docs, ClickUp, Fireflies, Google_Drive, Google_Docs and Claude_Code_Remote are the ones a run uses. Claude_Code_Remote sends the update request to the schedule chat. The routine also carries Canva, Notion, Slack, Gmail and Google_Calendar from the chat that made it; the prompt forbids messaging, and they are unused.
- **Needs:** the `longform-batch-autopilot` skill installed on the account (Save skill on the .skill file, or upload it in claude.ai › Customize › Skills). Without it a run ends with one line saying so.

## Where it lives

- A routine created from a Claude Code session gets no connectors: it would fire and do nothing (tried Oct 9, deleted). So this routine must stay the one made from the Cowork chat. Change its prompt, name or schedule with `update_trigger`; never delete and recreate it from here.
- To change the process, edit the skill in this repo and reinstall it (`DECISIONS.md` § How to change it). The prompt below rarely needs to change.

## Dashboard runs

The dashboard (`dashboard/longform-autopilot.html`, published as an artifact) starts runs by hand:
1. It reads the routine's prompt and refuses to go on unless it is this prompt (it names the skill). It appends a section, `---`, a line `[dashboard-run]`, a line `Valid until: <now + 10 minutes>`, and the instruction ("Test flight for Mason.", "Dry run for everyone due: …", or whatever was typed), saves it, and reads it back.
2. Only if the read-back matches, it fires the routine; the new session starts with that prompt.
3. It always puts the prompt back as it was, even when a step failed. If that fails too, it shows "Restore the normal prompt", and it removes any leftover section before its next run. A leftover section that slipped through expires after 10 minutes: a scheduled run then ignores it and runs everyone due.
4. It matches the section only on a line of its own, because the prompt's own text mentions `[dashboard-run]` in a sentence (the first draft cut the prompt there; caught in the Oct 10 audit).

Why the instruction goes in the prompt: text passed to `fire_trigger` arrives as a second message, wrapped as data, only after the first turn has finished (tested Oct 9). The first turn would already have run everyone due.

"Run everyone due" fires the routine with its normal prompt, as the schedule does.

## Prompt

```
Load the longform-batch-autopilot skill with the Skill tool and follow it.

Run the longform batch autopilot for everyone due. This is an unattended run: never stop to ask; decide, note the decision in the summary, and keep going.

If this prompt ends with a dashboard section (a line "---", then a line "[dashboard-run]", then "Valid until: <time>"), Jeremiah started this run from his dashboard. For this run only, that section's instruction replaces "everyone due": one client, a test flight, brief only, doc only, a dry run, or a question about the queue. Follow it as if he had typed it, within the limits below. If its "Valid until" time has already passed, ignore the section, run everyone due, and say so in the summary. A dry run writes nothing at all: no schedule chat message, no brief, no doc, no run log entry.

Jeremiah authorizes these writes for this run, and only these:
- send the update request to his schedule chat "Client topic batch and long-form schedule" (session cse_01VT4cAcAw8Wrd4LPaCmyNiQ), as he does in his Loom, only when the skill's Step 1.0 says to (an everyone-due run whose schedule doc is stale or over a day old) and the chat isn't busy;
- create one post-call topic brief Claude Doc per client per week (skip any client-week that already has one);
- copy last week's longform Google Doc into his My Drive as this week's doc (skip any week that already has one), and edit only that new copy: header, empty Media Folder, clear everything under LONGFORMS, add the entry lines. For a new client with no earlier doc, create an empty Google Doc in his My Drive instead and fill only that;
- create or append to the Claude Doc "Longform Autopilot — Run Log";
- in a test flight, the same brief and doc as copies whose titles start with "[Autopilot test] " (or the label the instruction gives), even when the real ones exist; a test flight adds no run log entry.

Everything else is read-only. Never edit, tick or comment on the schedule doc, ClickUp, the Topics docs, last week's docs, Fireflies or Krisp. Never message anyone, share, move or trash a file. Never change this routine.

If the longform-batch-autopilot skill is not available in this session, do nothing else and end with exactly: "Longform autopilot didn't run: install the longform-batch-autopilot skill (Save skill on the file Claude sent, or claude.ai › Customize › Skills)."

End with the summary from the skill's Step 7, at most 8 lines (a test flight or dry run may print its report above it). It becomes Jeremiah's push notification.
```
