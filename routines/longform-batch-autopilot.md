# Routine: Longform Batch Autopilot

- **Schedule:** `CRON_TZ=Asia/Manila 52 9,21 * * *`, every day at 9:52 AM and 9:52 PM Manila.
  - The 9:52 PM run lands before Jeremiah's night shift, after Kyle's US-morning calls.
  - The 9:52 AM run picks up anything posted overnight.
  - Each run skips what is already done, so running twice a day is safe.
- **Mode:** a fresh session on each fire, in the Cowork environment (like the Learning Pass routines), auto permission mode, model claude-opus-5-5, push notification on finish.
- **Connectors:** Claude_Docs, ClickUp, Fireflies, Google_Drive, Google_Docs, Claude_Code_Remote. The last one sends the update request to the schedule chat.
- **Needs:** the `longform-batch-autopilot` skill installed on the account (Save skill on the .skill file, or upload it in claude.ai › Customize › Skills).
- **Where to create it:** in claude.ai's Routines page, or from a Cowork chat that has the connectors. A routine created from a Claude Code session gets no connectors: it would fire and do nothing (tried Oct 9, deleted). The "Longform prep autopilot" routine made from a Cowork chat on Oct 9 already has every connector, so pointing it at this prompt (and this schedule) is the quickest route.

## Prompt

```
/longform-batch-autopilot

Run the longform batch autopilot for everyone due. This is an unattended scheduled run: never stop to ask; decide, note the decision in the summary, and keep going.

Jeremiah authorizes these writes for this run, and only these:
- send the weekly update request to his schedule chat "Client topic batch and long-form schedule" (session cse_01VT4cAcAw8Wrd4LPaCmyNiQ), as he does in his Loom, unless that chat is busy;
- create one post-call topic brief Claude Doc per client per week (skip any client-week that already has one);
- copy last week's longform Google Doc into his My Drive as this week's doc (skip any week that already has one), and edit only that new copy: header, empty Media Folder, clear everything under LONGFORMS, add the entry lines. For a new client with no earlier doc, create an empty Google Doc in his My Drive instead and fill only that;
- create or append to the Claude Doc "Longform Autopilot — Run Log".

Everything else is read-only. Never edit, tick or comment on the schedule doc, ClickUp, the Topics docs, last week's docs, Fireflies or Krisp. Never message anyone, share, move or trash a file.

If the longform-batch-autopilot skill is not available in this session, do nothing else and end with exactly: "Longform autopilot didn't run: install the longform-batch-autopilot skill (Save skill on the file Claude sent, or claude.ai › Customize › Skills)."

End with the summary from the skill's Step 7, at most 8 lines. It becomes Jeremiah's push notification.
```
