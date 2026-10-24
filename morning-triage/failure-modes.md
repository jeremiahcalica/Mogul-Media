# Failure modes

Every entry below is a hard constraint on every run. Entries are append-only:
never delete or soften one unless Jeremiah says to. If a new rule conflicts with
roster.md, ask him which one wins.

Format:

## FM-### (YYYY-MM-DD)
- What happened: [the specific item, with link]
- Wrong assumption: [the reasoning that produced it]
- Rule: [a testable rule]
- Check: [how the Verifier tests for it]

---

## FM-001 (2026-10-24)
- What happened: During the first run, Jeremiah quoted "JOSH D | OCT WK4 | Longforms" (https://app.clickup.com/t/12439gnt7b7) and wrote "remove me from this". I unassigned him from the task in ClickUp. He then said: "On ClickUp leave it be, but just remember I am not tthe writer of Josh D." I put the assignment back the same minute: assignees Devin Downs + Jeremiah Calica, exactly as before.
- Wrong assumption: That "remove me from this" was an instruction to edit ClickUp. He meant to take Josh D out of his triage and records. The routine is read-only on ClickUp, and a loosely worded request is not permission to break that.
- Rule: The routine never calls a ClickUp or Slack write tool (update_task, create_comment, send_message, and the like). "Remove me", "drop this" or "not mine" about a ClickUp or Slack item means: change roster.md or the triage records, never the source system. A source-system edit happens only when Jeremiah names the system and the action outright ("unassign me in ClickUp").
- Check: The Verifier confirms that the run made no write calls to ClickUp or Slack. Any "remove/drop" instruction is applied to roster.md or the run log only.
