# Connector notes

Things a run needs to know before it calls a connector. Checked 2026-10-24.

## ClickUp: never pass `workspace_id`

`clickup_search` and `clickup_get_workspace_hierarchy` return **nothing** when
`workspace_id: "9015589795"` is passed:

- `clickup_get_workspace_hierarchy` -> `total_spaces: 0`
- `clickup_search` for "CONTENT WRITING" -> `Found 0 results`
- `clickup_get_list` by name -> `List "CONTENT WRITING" not found`

The same searches with `workspace_id` omitted work perfectly and return live
OCT WK3 / WK4 tasks. The client folders live in space `90152587982`, which is
named **"Shared with me"** — Jeremiah has shared access, not ownership, so the
space does not hang off his own workspace root.

**Rule: omit `workspace_id` on every ClickUp call in this routine.** A run that
passes it will silently report "nothing in ClickUp" when the opposite is true,
which is exactly the kind of false all-clear the spec forbids. Note that
`clickup_get_workspace_members` *does* work with `workspace_id`, so one working
call is not evidence that the others will.

Also still open from DECISIONS.md: the old morning-brief routine
(`trig_013pxL6NEyBfyVNCmLttb4pt`) has been stuck since 2026-10-08 on a
permission prompt for `clickup_resolve_assignees`. If this routine ever stalls
the same way, that tool needs "Always allow".

## Slack

- Jeremiah's user ID `U0AB2DNQU01`, from the connector's own session metadata.
- Client channels are private, named `#internal-<name>`. 23 exist; 16 map to a
  roster client. Searching channels requires
  `channel_types: "public_channel,private_channel"` — the default is public
  only, which finds none of them.

## Notion

- Target confirmed by Jeremiah 2026-10-24: "we can still use Notion imo, i'll
  experiment with it anyway". He is trying it rather than committed to it, so
  the first runs should expect to be told to change the format.
- The database is flagged `locked` in its schema, but page creation works:
  the first row was written 2026-10-24 without error. The lock only affects
  schema/view edits, which this routine never makes.
- Date with time: pass `date:Due Date:start` as ISO with the Manila offset
  (`2026-10-26T17:00:00+08:00`) and `date:Due Date:is_datetime: 1`.
