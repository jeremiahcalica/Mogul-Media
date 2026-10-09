# Mogul Media automations

Before changing the longform autopilot, read `DECISIONS.md`. It records every rule Jeremiah set and why, what is still open, and the steps for shipping a change. Add a row there for every new decision.

- The skill (`.claude/skills/longform-batch-autopilot/`) is the source of truth. The installed copy on Jeremiah's account is a packaged snapshot (`dist/longform-batch-autopilot.skill`), so any change ships only after repackaging and reinstalling.
- Run the tests before every commit: `python3 -I .claude/skills/longform-batch-autopilot/tests/run_tests.py`.
- Never delete or recreate the routine `trig_01KHnmqSHRLJhaURiFFbgoyG` from Claude Code: a routine made here gets no connectors. Change it with `update_trigger`.
- Jeremiah checks every output. Quote his words for rules, and cite the real case (client + week) a rule comes from.
