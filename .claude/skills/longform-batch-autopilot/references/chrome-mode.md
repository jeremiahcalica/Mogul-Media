# Chrome mode (only when Claude in Chrome is available)

A scheduled cloud run has no browser. These steps apply only when the session has the Claude in Chrome tools (`mcp__claude-in-chrome__*`), i.e. a run on Jeremiah's Mac with the extension on and his logins. Read the `chrome-browser` skill first.
- Load the tools in one search: `tabs_context_mcp`, `tabs_create_mcp`, `navigate`, `read_page`, `computer`, `find`, `tabs_close_mcp`.
- Work in tabs you open, and close them when done.
- If a site asks for permission or a login, stop that step and report it. Don't work around it.

A file downloaded in his Chrome lands on his Mac, where a cloud session can't read it. So read what the file would contain directly from the page.

## Krisp transcript (Devin's clients)

Jeremiah exports these with "Export as transcript". In Chrome:
1. Open the `app.krisp.ai/m/…` link from the ClickUp task description (`Call:`).
2. Open the meeting's **Transcript** tab and scroll until the whole transcript has loaded.
3. Read it with `read_page` (or `get_page_text`). Keep the speaker names and timestamps exactly as shown.
4. If the page only offers the transcript through Export:
   - choose "Export as transcript" in Markdown or text, then tell Jeremiah where the file went;
   - in an unattended run, mark the client "Krisp transcript exported to Downloads: drop it in My Drive › Autopilot Transcripts", and move on.

## Fireflies (only if the connector fails)

The connector gives the same text, so this is a fallback. Loom 1, 2:03–2:14:
1. Open `app.fireflies.ai/view/<slug>::<id>` from the ClickUp comment.
2. Click the **"…"** button to the right of the meeting title and choose **Download**. Don't use the download icon in the player bar.
3. In "Download Meeting", on the **Transcript** tab, choose **MD**.
   - Leave **Include timestamp** and **Show speaker name** ticked, as they are by default.
   - Tick **Remove Fireflies Branding**.
4. Click **Download**. The file is `<TITLE-SLUG>-<hash>.md` (e.g. `MASON-L-X-KYLE-bd7e113d-c191.md`) and lands on his Mac, so read the transcript panel on the page instead where you can.
5. Never use Kyle's transcript PDF in ClickUp, or any other Fireflies format.

## Star the new longform doc

1. Open the new doc (`docs.google.com/document/d/<id>/edit`).
2. Click the star icon to the right of the doc title, next to the "move" and "cloud" icons.
3. Check the icon is now filled (the tooltip reads "Starred"). Only then count it as starred.

## The brief inside the client's Claude project (optional)

The default is the Claude Doc the cloud run makes with the connector, which is the same output. Do this only if Jeremiah asks for the brief chat to live in the client's project, as in Loom 1 (2:20–3:00). Order matters:
1. Open claude.ai, then the client's project from the sidebar's Pinned list. Project names are in `references/clients.md` (e.g. "Mason L.", claude.ai/project/019ea4df-9219-7701-ae41-474c4ff6e50c).
   - Use the project page's composer ("New session in Mason L."), not claude.ai/new.
2. Attach the **transcript first**, then the **topic sheet**, to the message itself. Never use the project-knowledge drop zone or Context › Add.
   - **Topic sheet:** in the Loom he uploads `File › Download › PDF Document (.pdf)`, with Tab = "Current Tab" (Client strategy). The extension can't drive a native file picker, so use the composer's **+** › Add from Google Drive › the Topics doc instead.
   - **Transcript:** paste the transcript text; long pastes become an attachment card.
3. Wait until every attachment has finished processing (the PDF card shows its page thumbnail).
4. Paste the prompt from `references/brief.md` word for word, with the client and strategist swapped in, keeping its last line "In a claude doc pls". In the Loom he copies it from last week's chat "<Client> brief from <Strategist> meeting", the most recent one, using its last successful message (the one ending with that line). The text in `brief.md` is that message.
5. Leave the model as it is (Opus 5.5, High, Auto) and send.
6. Wait until Claude has finished building the doc; the summary changes while it edits (Loom 1, 3:02). Only then read its status table and record the link.
