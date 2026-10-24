# Sources: what each route can reach

Tested 2026-10-24 against real Mason L. docs. "Connector" means the
Google/Slack/ClickUp/Fireflies tools. "Chrome" means Claude in Chrome on
Jeremiah's Mac (`mcp__claude-in-chrome__*`); read the chrome-browser skill
before the first Chrome step. A run without Chrome does the connector parts
and lists every Chrome part under Needs Jeremiah.

| Source | Connector | Chrome |
|---|---|---|
| Version history (who changed what, when) | **No.** Drive `download_file_content` with `revisionId` returns "Attempting to download a file at a given revision is not yet supported." No tool lists revisions or names an editor. | **Yes**: File → Version history → Show changes |
| Current doc text, killed posts | Yes: `read_file_content`. A killed post shows as `~~**❌1.1 - (X) …**~~` | Yes |
| Comments + replies | **Yes** (see below) | Yes, including resolved ones |
| Suggestions (open or resolved) | **No.** `read_doc` returns no suggestion fields at all | **Yes**: open suggestions in the doc; resolved ones in version history |
| Slack threads and text | Yes: `slack_read_thread`, `slack_search_public_and_private` | Fallback |
| Slack screenshots and images | Not readable as images | Open the message permalink in Chrome and read the image |
| Loom | No connector | Yes: open the link, read the transcript panel |
| Fireflies (Kyle's clients) | Yes: Fireflies connector | Fallback |
| Krisp (Devin's clients) | No | Yes: open `app.krisp.ai/m/…` (the "Call:" link in the batch task), Transcript tab |
| ClickUp write (the log) | Yes: `clickup_update_document_page` with `content_edit_mode: "append"` | — |

## Comments: how to read them

Use `mcp__Google_Docs__read_doc` with `commentsIncluded: true` for the data:
author `displayName`, created time, `status`, `plainTextQuote` (the anchor),
and replies. Use `mcp__Google_Drive__read_file_content` (it supports
`includeComments`) to see where each comment sits now: it marks anchors inline
as `<comment_start id=…>…<comment_end id=…>`.

Watch for these:
- **`plainTextQuote` is the anchor as it was when the comment was made.**
  Mason's X comment still quotes "1.2 - (X) …" although the heading now reads
  "❌1.1 - (X) …". Record the quote exactly as the "Anchored on" text. Assign
  the post from the inline marker's current position, and note a renamed
  heading when the two differ.
- The created time is when the comment was made. `updateTime` /
  `modifiedTime` change when someone replies. Mason's "Dont post this." was
  made Oct 1, 6:13 AM PHT; 9:57 AM is when Mogul Writer replied.
- Resolved and deleted comments were not seen in the test, because that doc had
  none. If the connector does not return them, open the comment history in
  Chrome (the comments icon → "Show all" / resolved). If a deleted comment's text
  is not recoverable, write "deleted; text not recoverable".
- Comments carry a display name and no email. Mason's own comments come through
  as "Mason Littlejohn".

## Attribution

**Client-side reviewers count as the client.** Jeremiah, 2026-10-24: "they kind of
represent the client as they're the reviewer of the content". Log them as
the client, tagged `[client side: <name>]`, and don't raise a Needs Jeremiah
question about them:

| Client | Reviewer(s) |
|---|---|
| Shane H. | Kevin Tan |
| Lior P. | Reut Amariyo (writes every comment; Lior rarely comments himself) |
| Joshua C. | Sean Goh |
| Teddy T. | Mohit Sharma (as well as Teddy Truong himself) |

A new named account outside Mogul on a client's doc is still tagged
`[client side: <name>]` and raised once under Needs Jeremiah. If he confirms
it, add it to this table.

**Anonymous "scheduled" replies are team, never logged.** Jeremiah, 2026-10-24:
"Stay out". These are the anonymous "scheduled" / "schedule" / "x tagged"
replies under Kyle's scheduling notes, which Claudia or the scheduler post
signed out.

Client: a comment or edit by the client's own named account, or by "All
anonymous users", **with one exception**. An anonymous author whose words
identify a team member is team, not client. Real case: on Mason's Sept Wk 5
doc, anonymous replies read "scheduled - claudia". If an anonymous item cannot
be told apart from team, tag it `[anonymous: unconfirmed]` instead of
attributing it to the client.

Team: Jeremiah Calica, Kyle Meng, Devin Downs, Mariana Botello, Claudia (Yau),
Oriana T., Martin DHers, Manaal, Arooba Asim, Luciany (Gissele) Gomez, Sam
Elsner, Ymarie, Nerissa, Mogul Writer / writing@mogulmedia.ca, Mogul
Scheduler, and any other Mogul Media member. Kyle's scheduling comments ("Oct
12 both", "Oct 9 LI") are team, as are the source-quote notes Mogul Writer
leaves.

## Version history in Chrome

Never restore, name or change a version. **Jeremiah opens nothing.** His
words: "we ideally want the prompt to go the masterfile and find it instead of
me opening it manually since it beats the point of handing this to claude".
The agent finds and opens every doc itself.

0. Find the doc. Use the doc IDs the Connector Collector found (plan.json),
   or navigate in Chrome yourself:
   - MASTER FILE: https://drive.google.com/drive/folders/13oJ5I0-1B2tJVEu6Oy3ybAtmkZj-gwf4
   - → POD 2 (Kyle M Team) or POD 1 (Devin Team)
   - → <Client> → CONTENT (the content folder IDs are in clients.md, so you can
     also open https://drive.google.com/drive/folders/<content folder id>
     directly)
   - → the batch docs ("<Client> - <Mon> - Week <n>", "(Snipes)", "(Quick
     response posts)"). Open every doc that matches the name.
1. Open `docs.google.com/document/d/<id>/edit` → File → Version history → See
   version history.
2. Tick **Show changes**. Expand each grouped version (▸) so every edit shows
   with its editor color.
3. For each version whose editors include "All anonymous users" or the client's
   named account:
   - read every colored insertion and every struck-through deletion;
   - map each one to the nearest heading above it (LF2, 2.1, Snipe 3, QR 1);
   - write it in `[-removed-]{+added+}` markup with enough words around it to
     find it.
4. A mixed version (e.g. "All anonymous users, Claudia Yau, Kyle Meng"): attribute
   each change by its editor color. If you can't, tag it `mixed version`.
5. Tag every change read this way `[from version-history UI]`.
6. A version made only of formatting changes (no text) is noted as one line
   ("formatting-only anonymous run, no text changed") and is not feedback. The
   existing Mason log does the same.

## Slack

Task Update posts come from PMwazowski. Examples:
"MATT | OCT WK4 | New Topics | internal qa | *Due:* 10/22/2026", and
"SHANE | OCT WK3 | Longforms | scheduled". Client feedback is in the thread
replies, mostly under "client feedback recieved" (that spelling) and
"approved".

`slack_read_thread` gives no permalinks. Get each message's permalink from
`slack_search_public_and_private` (with `channel_types:
"public_channel,private_channel"`, because every internal-<client> channel is
private).

## ClickUp

Never pass `workspace_id`. With it, `clickup_search` returns 0 results and the
hierarchy returns 0 spaces, even though everything is there.
