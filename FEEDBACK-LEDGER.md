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
