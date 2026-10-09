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

The connector gives the same text, so this is a fallback. Open `app.fireflies.ai/view/<slug>::<id>` and open **Download**. In the "Download Meeting" dialog, on the **Transcript** tab:
- choose **MD**;
- keep **Include timestamp**, **Show speaker name** and **Remove Fireflies Branding** all ticked (as in Loom 1, 2:40);
- click **Download**.

The file is named `<TITLE-SLUG>-<hash>.md`, e.g. `MASON-L-X-KYLE-bd7e113d-c191.md`. It lands on his Mac, so prefer reading the transcript panel on the page.

## Star the new longform doc

1. Open the new doc (`docs.google.com/document/d/<id>/edit`).
2. Click the star icon to the right of the doc title, next to the "move" and "cloud" icons.
3. Check the icon is now filled (the tooltip reads "Starred"). Only then count it as starred.

## The brief inside the client's Claude project (optional)

The default is the Claude Doc the cloud run makes with the connector, which is the same output. Do this only if Jeremiah asks for the brief chat to live in the client's project, as in Loom 1 (2:20–3:00):
1. Open claude.ai and pick the client's project from the sidebar's Pinned list. Project names are in `references/clients.md` (e.g. "Mason L.", URL claude.ai/project/019ea4df-9219-7701-ae41-474c4ff6e50c).
2. In the project page's composer ("New session in Mason L."), add the transcript and the topic sheet:
   - **Topic sheet:** the composer's **+** › Add from Google Drive › the Topics doc.
   - **Transcript:** paste the transcript text into the composer; long pastes become an attachment card. Native file pickers can't be driven from the extension, so don't open them.
3. Paste the prompt from `references/brief.md` word for word, with the client and strategist swapped in. Leave the model on Opus 5.5.
4. Send. Wait until the Claude Doc card appears in the reply, then record its link.
