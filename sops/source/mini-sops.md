# Mini-SOPs (as written by Jeremiah, Oct 9 2026)

## Generate Mason L topic brief

Loom: https://www.loom.com/share/03a9ded0933b4076b39b59c3bda9352b

1. **Rename the schedule session**
   - Open conversation options for session `https://claude.ai/chat/f6da90a8-f5ac-80f7-905d-050254f551d3`.
   - Click "Rename" and enter `Client topic batch and long-form schedule`.
   - Click "Save".
   - Acceptance: session header and sidebar reflect "Client topic batch and long-form schedule".
2. **Prompt Claude to generate the updated weekly topic and long-form content schedule table** (01:25)
   - In `https://claude.ai/chat/f6da90a8-f5ac-80f7-905d-050254f551d3`, enter prompt: `Claude, can you give me the updated topic and content batch? By now, there are already new topics (to be submitted next week) and long-form content batch as well, organize them like last time.`
   - Select model `Opus 5.5`.
   - Send the message.
   - Acceptance: Claude generates the "Content batches (long-forms)" table with ClickUp task links including `OCT WK2 Longforms` for client Mason.
3. **Download the client meeting transcript in Markdown format from Fireflies** (02:27)
   - Open the ClickUp task at `https://app.clickup.com/t/12439gnqare` ("MASON | OCT WK2 | Longforms").
   - Click the Fireflies recording link `https://app.fireflies.ai/view/MASON-L-X-KYLE::01M3QFNSCKKAC1DWAF55JKP5AH`.
   - Click "Download" and choose `MD` in the "Download Meeting" modal.
   - Acceptance: `MASON-L-X-KYLE-*.md` is downloaded locally.
4. **Export the client topic brief Google Doc as a PDF** (02:53)
   - Navigate to `https://docs.google.com/document/d/17r5OXeW-au98IgFiYhFNOrE9-kohUqGh_WO0XzdDHus/edit?tab=t.mcidewmh8er7` ("Mason L | OCT WK2 | Topics").
   - File › Download › PDF Document (.pdf).
   - Acceptance: `Mason L | OCT WK2 | Topics.pdf` is exported.
5. **Generate a detailed topic brief artifact in the Mason L Claude project** (03:12)
   - Open Claude project `https://claude.ai/project/019ea4df-9219-7701-ae41-474c4ff6e50c` ("Mason L.").
   - Attach `MASON-L-X-KYLE-*.md` and `Mason L | OCT WK2 | Topics.pdf`.
   - Submit the brief prompt (see `README.md`, verbatim) ending with `In a claude doc pls`.
   - Acceptance: Claude outputs artifact `Mason L - Oct Wk2 Topic Brief` classifying topic statuses as KEPT, PIVOT, or NOT DISCUSSED.

## Prepare weekly longform topics document

Loom: https://www.loom.com/share/8b52f2094796445e9f776c19a950c84b

1. **Copy the Week 1 doc as Week 2** (00:52)
   - Open `Mason L. - Oct - Week 1` at `https://docs.google.com/document/d/19fuPiY3pZJlvh_SqEsYlsKyfXztUqEWM0x7yTCw93ik/edit`.
   - File › Make a copy.
   - Title `Mason L. - Oct - Week 2`, destination `My Drive`.
   - Acceptance: `Mason L. - Oct - Week 2` is created at `https://docs.google.com/document/d/167ngEIEU_hgNP-ML1vPBL_NslV7YtK5InF9wQ4s3jOc/edit`.
2. **Clear the old content and update the header** (01:28)
   - Header text → `Mason L - Week 2 - Oct`.
   - Clear the link under `Media Folder:`.
   - Delete all body paragraphs and images beneath `LONGFORMS`.
   - Highlight the remaining list header text and `Clear formatting`.
   - Acceptance: clean template headings under `LONGFORMS`, ready for new entries.
3. **Populate entries from the topic perspectives** (02:11)
   - Open `Mason L | OCT WK2 | Topics` side by side.
   - Read each topic's perspective (e.g. `Operator in his 30s calling out what he sees people in their 60s get wrong. Unapologetic, but never a jab at anyone he knows personally`).
   - Add entries under `LONGFORMS` as `[Number] - (XL/L) - [Perspective] - (Long-form)` for each topic in the batch. (Written "XL/L"; the docs themselves use `(X/LI)`.)
   - Acceptance: every batch topic is listed under `LONGFORMS` with its perspective.
4. **Format, space and star** (03:10)
   - Bold all entry lines.
   - Add a blank line between entries.
   - Star the doc.
   - Acceptance: entry lines are bold with blank lines between them, and the doc is starred in Drive.
