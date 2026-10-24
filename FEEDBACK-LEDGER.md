# Client Feedback Ledger: decisions

The second automation in this repo. The skill
(`.claude/skills/client-feedback-ledger/`) is the source of truth. The
installed copy is a packaged snapshot (`dist/client-feedback-ledger.skill`),
so a change ships only after repackaging and reinstalling, the same as the
longform autopilot.

Change → run tests → repackage → commit → reinstall:
```
python3 -I .claude/skills/client-feedback-ledger/tests/run_tests.py
cd /mnt/skills/examples/skill-creator && python3 -m scripts.package_skill /home/user/Mogul-Media/.claude/skills/client-feedback-ledger /home/user/Mogul-Media/dist
```

## Decisions

| Date | Jeremiah | Decision | Where |
|---|---|---|---|
| 2026-10-24 | (his full prompt) | His prompt is the spec, kept word for word in SKILL.md. Additions are marked [Added] and never loosen a rule. | `SKILL.md` |
| 2026-10-24 | "Ideally a main agent too with mini agents (dynamic workflow)" | A main agent coordinates and never collects. Connector Collectors run in parallel; one Browser Collector drives Chrome; separate Verifiers; one Logger. About 10 agents at a time. | `SKILL.md` § How the run is organised |
| 2026-10-24 | "we were notified to start logging … the 13 writing clients" | A cloud connector pass ran at once for all 13 (comments, replies, Slack text): 142 entries logged. Its sections say "Browser pass pending" so the Saturday run goes back for version history. | `ledger-runs/2026-10-24.md` |
| 2026-10-24 | "for josh maybe not all imo - important is september to october ish" | Joshua C. never goes earlier than SEP WK1. | `references/browser-pass-start.md` |
| 2026-10-24 | "they kind of represent the client as they're the reviewer of the content" | Kevin Tan (Shane), Reut Amariyo (Lior), Sean Goh (Josh C), Mohit Sharma (Teddy) count as the client. | `references/sources.md` § Attribution |
| 2026-10-24 | "Stay out" | Anonymous "scheduled" replies under scheduling notes are team and never logged. | `references/sources.md` § Attribution |
| 2026-10-24 | "Sure yeah" | Add Jeremiah's Keval Oct Wk 2 ledger (posted in Slack Oct 10) and Mason's Sept Wk 5 Slack feedback (Oct 1) to their logs. | `ledger-runs/2026-10-24.md` |
| 2026-10-24 | "it's kind of pointless to do the feedback log without their direct edits, because it's their thinking" / "we also can't include team fixes" | No team fixes anywhere in the log. The Net change block is dropped; mixed-version changes that can't be attributed to the client are left out and only counted; no draft-vs-client-copy diffs. Overrides the prompt's "keep them in the net change" and "mixed version" tag. | `SKILL.md` Stage 1, `references/format.md` |
| 2026-10-24 | "I'm completely fine if I turn on my computer if it has a better output … every week on Saturdays" | Runs on his Mac, weekly on Saturday, as a Claude Desktop scheduled task, not a cloud routine. | `routines/client-feedback-ledger.md` |

## What testing showed (2026-10-24, Mason L. docs)

- **Version history is browser-only.** Drive `download_file_content` with a
  `revisionId` returns "Attempting to download a file at a given revision is not
  yet supported." No connector names who made an edit.
- **Comments work through the connector.** `read_doc` with `commentsIncluded`
  returned Mason's "Don't post this." and "Dont post this." with author, time,
  status, anchor and replies.
- **Suggestions don't.** The connector shows no suggestion data, so they are
  read in the browser.
- **"Anonymous" is not always the client.** Anonymous replies on Mason's Sept
  Wk 5 doc read "scheduled - claudia".
- **The ClickUp log can be appended to directly** (`content_edit_mode:
  "append"`), so the old ledger is never rewritten.
- **One timestamp in Mason's manual ledger is off.** It gives "Oct 1, 9:57 AM"
  for "Dont post this." (LF 1.2 X). The comment was made at 6:13 AM; 9:57 AM is
  when Mogul Writer replied. It is left as is: manual entries are never edited.

## Open

- Whether resolved and deleted comments come back through the connector
  (Mason's test doc had none). The Browser Collector covers them either way.
- How long the first run takes. Mason starts at Oct Wk 1. The other 12 clients'
  starting points are read at run time.
