# Scanner rules

Paste these into every scanner's prompt (Agents A, B and C) on top of the
brief. Each rule came from a real miss.

## S-1 — Report Jeremiah's own latest reply

For every thread or task a candidate comes from, also return
`jeremiah_last_reply`: his most recent message or comment there (exact text +
time), or `null` if he hasn't replied. Do not drop his messages as "his own
outbound".

Why (2026-10-24): two items reached the verifier as P0 although he had already
done them. Shane H: Kyle asked him to fix a LinkedIn comment, and he had
replied "ive edited it!". Marco B: Devin asked for inspo links, and he had
replied "added inspos @Devin Downs". The scanners could not see either reply.

## S-2 — Keep strikethrough in quotes

Copy `~text~` exactly, crossed-out marks included. A crossed-out line in a
list means that item is done.

Why (2026-10-24): Kyle's EOD had "~Phil (Due this Monday) Meet on Tuesday~"
crossed out. The scanner returned it as plain text, so a finished item looked
open.

## S-3 — Never pass workspace_id to ClickUp

See connectors.md. With it, every ClickUp search comes back empty.

## S-4 — Read only

No scanner calls any tool that writes to Slack or ClickUp. See FM-001.
