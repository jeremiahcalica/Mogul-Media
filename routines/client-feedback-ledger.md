# Client Feedback Ledger — weekly run (Saturdays, on Jeremiah's Mac)

Jeremiah, 2026-10-24: "I'm completely fine if I turn on my computer if it has
a better output … I can schedule this to run every week on Saturdays".

This runs **on his Mac**, not in the cloud. Version history (the most
important source), suggestions, Loom and Krisp can only be read through Claude
in Chrome with his logins, and a cloud run has no browser.

## One-time setup (Jeremiah)

1. **Install the skill.** Open `dist/client-feedback-ledger.skill` from this
   repo and choose Save skill (or claude.ai → Customize → Skills → upload).
2. **Make a working folder** on the Mac, e.g. `~/Mogul Feedback Ledger`. Runs
   keep their snapshots, retry state and run files there.
3. **Test flight first.** In Claude Desktop, open a new task with that folder
   selected and paste:
   `Run the client-feedback-ledger skill for Mason L. only, as a test flight. Show me the entries before logging anything.`
   Check the result against Mason's docs before scheduling.
4. **Schedule it.** In Claude Desktop, create a scheduled task:
   - Repeat: weekly, Saturday, at a time the Mac will be on (a morning start
     gives it the day; a run can take about half a day).
   - Folder: the working folder from step 2.
   - Prompt: the block below, pasted exactly.
5. **On Saturdays:** Mac on and awake, Chrome open, Claude in Chrome on and
   signed in to Google, Slack, Loom and Krisp.

## Scheduled-task prompt

```
Run the client-feedback-ledger skill: the weekly Client Feedback Ledger for all 13 writing-roster clients.
Use this folder as the working folder.
Use Claude in Chrome for version history, suggestions, Slack images, Loom and Krisp, one browser agent at a time.
Run on your own, and never stop to ask. Put anything you couldn't settle under "Needs Jeremiah" in the run summary.
Write only to the Client Feedback Log docs listed in the skill's clients.md, and only by appending. Everything else is read-only.
```
