# The post-call topic brief

## The prompt (Jeremiah's own, used verbatim)

Each week he opens last week's brief chat in the client's project, copies this prompt, and pastes it into a new chat with the new transcript (.md) and the topic sheet (PDF). "Please, in verbatim, please prompt it like this" (Loom 1, 2:55). Treat every clause as a requirement. The apostrophes and quotes are the curly ones his Mac typed (Loom 1, 2:47). Swap in only `{Client}` (the **Brief name** column of `references/clients.md`, e.g. "Mason L", "Josh Chin") and `{Strategist}` (Kyle or Devin):

> Can you give me a detailed brief for the topics for {Client} based on this meeting with {Strategist}, where they talked about what to do per topic? Pay attention to detail. I also attached the topic sheet, I want you to name the brief according to its correct vehicle in the chat, make sure that you’re paying attention to detail of the meeting so I don’t miss details or instructions (include the pivots on the call, if any). Do not invent anything. Make sure you include the original brief in the topic sheet, and just write a “note” saying “pivot” (if there’s any), so I know what was kept and what was changed or what was kept and what was killed.
> In a claude doc pls

What each clause means here:

| Clause | Do this |
|---|---|
| "detailed brief for the topics … based on this meeting" | One section per topic on the sheet, in sheet order, built from what was said on the call. |
| "name the brief according to its correct vehicle in the chat" | Each topic heading names its vehicle as it stands after the call: `Topic N — <Vehicle>: <Title>`. If the call changed the vehicle, the heading uses the new one, and the Note says what changed. |
| "paying attention to detail of the meeting so I don't miss details or instructions" | Capture every instruction the strategist or client gave on each topic, including side remarks: who to name or not, numbers to use or avoid, assets they'll send, and the timing. Calls also contain items outside the topics; they go in "Other items from the call". |
| "include the pivots on the call, if any" | Any change to angle, scope, source, vehicle or post count is a PIVOT, labelled with what changed: PIVOT (angle), PIVOT (scope), PIVOT (vehicle), PIVOT (source), PIVOT (post count). |
| "Do not invent anything" | Every line traces to the transcript or the sheet. If something wasn't said, write "Not stated on the call". Never complete a sentence the client left unfinished. |
| "include the original brief in the topic sheet" | Copy every field of the topic word for word. |
| "just write a 'note' saying 'pivot' … so I know what was kept and what was changed or … killed" | A bold `Note:` line first under each topic heading, with the status, then Kept / Changed / Killed bullets when anything moved. |
| "In a claude doc pls" | Make it a Claude Doc with the Claude Docs connector, not a chat reply or a file. |

## Title and top of the doc

This layout is the house default, taken from his Mason Oct Wk2 brief (the Loom example). His real briefs for other clients use other titles and layouts (Ben: "Ben K. — Oct Wk2 — Topic Briefs (Post-Call)" with a Status line and Writer notes per topic; Josh: "Josh Chin │ Oct Wk2 Topic Briefs (Oct 7 Call)" with "Batch status at a glance"; Caulen keeps "(Call: …)" in the H1). Until he picks one format, use this one for every client.

- **Doc name** (the tab name too): `{Client} — {Mon} Wk{N} Topic Brief (Call: {Client first name} x {Strategist}, {Mon d})`. Example: `Mason L — Oct Wk2 Topic Brief (Call: Mason x Kyle, Oct 7)`. The dashes are em dashes (—).
  - The call date is the Manila date (Asia/Manila). Fireflies gives UTC (`DateString`), so convert it: 2026-10-06T18:30Z is Oct 7 in Manila.
  - `{Mon} Wk{N}` comes from the topic sheet's name, like the doc's week (SKILL.md Step 2.1): "KEVAL | OCT WK3 | Topics" → "Oct Wk3". The task name is only a cross-check.
  - With no start time in the transcript (Granola's "Date: Oct 7"), use that date as given.
- **H1:** the same, without the "(Call: …)" part: `# Mason L — Oct Wk2 Topic Brief`.
- **Byline:** exactly `<?claude block asof?> · <?claude block me?>`, with today's date chip and the mention of the user.
- **Lead:** one sentence counting the outcomes by topic number. Example: "Two topics pivoted on the call (2 and 5), three were kept (1, 3, 4), and two were never discussed (6 and 7). Nothing was killed outright."

## Sections, in this order

1. `## How to read this brief`
   - Paragraph 1: "Each topic has three parts: the **Original brief** copied from the topic sheet, **From the call** (what {Strategist} and {Client first name} actually said, with timestamps), and a **Note** that gives its status (see the table below) and says what was kept, changed, or left open. Call pivots override the topic sheet." With a transcript that has no timestamps (Granola), drop "with timestamps" and add: "This transcript has no timestamps, so quotes are in call order without times."
   - Paragraph 2: "Transcript quotes are {Client first name}'s words as transcribed. Where the transcription is clearly garbled, the likely word is in brackets and marked as a reading, not a fact."
   - Then the status table: `| # | Topic | Vehicle | Status |`. One row per topic. Status in the vocabulary below.
     - **Topic:** the sheet title. For a pivot, `<sheet title> → "<new angle>"`, e.g. `Revenue Metric Screenshot → "The real story of my brand"`.
     - **Vehicle:** as written on the sheet, or as changed on the call. No post count here (", 2 posts" goes in the Note and the Original brief).
2. `## Batch header (from the topic sheet)`
   - A bullet list with bold labels: **Client:**, **Week:**, **Strategist:**, **Platforms:**, **Call:** (`{Client first name} x {Strategist}, {d Mon yyyy}`, e.g. "Caulen x Kyle, 8 Oct 2026"). Only these; no transcript link or other fields. A problem with the sheet itself (a broken Client Brain link) goes in the run summary, not here.
   - Then a paragraph `**Client goal:** …` (verbatim).
   - Then `**Hypothesis (verbatim from sheet):**` with bullets `*Last week:*`, `*This week:*`, `*We expect:*`.
   - If the Client strategy tab has no hypothesis (Keval's has a Success Signals table instead), write "**Hypothesis:** none on this sheet." Don't borrow one from the Strategy tab.
   - If a pivot, park, hold or kill changes a line of the hypothesis, add one plain sentence saying which line. Example: "Note: the Topic 2 and Topic 5 pivots change two lines of this hypothesis (…). Kyle hasn't restated the hypothesis."
   - If the schedule row had a note about the batch's content or scope, add `**Schedule note:** <the note>`, copying only those sentences, verbatim. Leave out notes that are only about dates or who reviews when ("Calendar day is Monday, a day before ClickUp's date").
3. One `## Topic N — <Vehicle, Title Case>: <Title>` per topic, in sheet order. Under each:
   1. **The Note, first, directly under the heading:** `**Note: <STATUS>.** <one or two plain sentences, usually quoting the strategist's verdict>`. Example: `Kyle: "That's perfect."`
      - For a PIVOT, add bullets with bold labels: `**Kept:**`, `**Changed:**`, `**Killed:**`, `**Not stated on the call:**`.
      - If the strategist left a comment on this topic in the sheet, add `**{Strategist}'s comment on the sheet:** "<comment>"`, and say whether the call confirmed it, changed it, or didn't touch it.
        - Check when it was posted. A comment posted during the call (its time minus the call's start falls inside the call) records what was said at that minute: tie it to that moment, e.g. Kyle's "Make a pivot to long-form for this week" on Mason's T2, posted 16:28 into the call, right as he said "I'll get the team to pivot to that" [16:29].
   2. `### Original brief (topic sheet)`: a bullet list with bold labels, word for word:
      - **Type:** A / A, 2 posts / B
      - **Angle & description:**
      - **For {Client first name}:**, with one nested bullet per question (Type A only)
      - **Vehicle:**
      - **Vehicle inspiration:** the link. If the sheet or the linked post gives the author, hook or stats, add them in one line (e.g. "Jacob's revenue post, 499 likes, 71 comments"). Don't guess what a link holds if you can't open it.
      - **Objective:**
      - **Perspective:**
      - Type B: then `**Initial draft direction (verbatim from sheet):**` and the whole draft in a ```markdown code block. The words are verbatim, one line per sheet paragraph; the sheet's empty paragraphs are dropped, as in his real briefs. `read_file_content` flattens a cell's line breaks into runs of spaces, so take the draft's line structure from `read_doc` on the Topics doc.
        - Bracketed writer placeholders in the draft (`[Time] later`, `[current result, writer to fill from Mason]`, `[2 photos: ecom brand era + now]`) stay as they are. List each one under "Asks for {Client first name}" unless the call filled it, and never fill one yourself.
        - A Type B topic with no draft, only a SOURCE line (Keval T7: results from his site), quotes the SOURCE line here; its Note says the SOURCE is the direction.
      - If the client pasted his own written-out answer into the box after PERSPECTIVE (Keval), add `**{Client first name}'s written-out answer (on the sheet, verbatim):**` and the text in a ```markdown code block, one line per paragraph. Flag every figure where it and the call differ. If it was written after the call (the sheet's last edit is after the call), say so: it wasn't discussed on the call.
   3. `### From the call`: paragraphs that open with a bold label and a timestamp range, e.g. `**The stupid (Q1) [09:16–10:51]:**`, followed by bullets of near-verbatim quotes.
      - With an untimed transcript (Granola), quote in call order with no times.
      - Timestamps are `[MM:SS]` or `[MM:SS–MM:SS]` (en dash), taken from the transcript. A range starts at the start time of its first quoted sentence. One range per paragraph covers the exchange; quotes under it are condensed with ellipses ("Everyone likes to... flex. …") rather than one timestamp per sentence.
      - Garbled words are marked like `[likely "TAM", reading]`. A garbled line that adds nothing to the topic is left out, above all one that could read as offensive.
      - A name the client or the perspective says stays unnamed (a former brand, a person) is written as a bracketed role, e.g. `[former ecom brand, named on the call]`, never spelled out.
      - A topic the call never reached gets one plain sentence: "Nothing on <what the questions asked>."
   4. `### Flags`: bullets, each opening with a bold sentence that ends in a period, e.g. `- **Launch date is ambiguous.** …`.
      - Use flags for gaps (a question with no answer), conflicts with other topics or earlier posts, names or numbers that need clearance, assets promised but not confirmed, and sentences left unfinished.
      - If two topics, the call, or a source post the sheet points to give different figures for the same thing (revenue, ages, years), flag the clash with both figures.
      - If the strategist's own words supply part of a post (a take, a line), flag it: "Take 4 is Kyle's words, not Mason's."
      - Check every quote the post may use, and flag:
        - "like I posted previously" / "like I said before": a repeat risk, check his past posts (Caulen T5);
        - a line that breaks the PERSPECTIVE's own rules ("it's going to catch some attention" against "never attention", Caulen T5), or the client's known rules in clients.md (plural credit, "9 figures");
        - lines about the agency or the strategist's process ("you gave me the same formats") rather than the client's world;
        - counts that don't add up inside a quote ("1, 2, 3, 4. I got five");
        - a word missing from the transcript: mark it `[word missing]`;
        - a quote that contradicts its own second half or the client's restatement: mark the likely word (`don't break [likely "fix", reading] broken systems`, Josh T1).
      - List every unfinished sentence near the quotes used, not only the key ones.
      - End a flag with "{Strategist} gate." when only the strategist can decide it.
4. `## Other items from the call (not this week's topics)`: bold-label paragraphs with timestamps for anything outside the topics, e.g. a new test format, the client's requests for next time. End each with `**Status:** not in this batch.` unless it changes this batch.
   - Each post or message the client says he sent the strategist is its own item (`**Status:** get it from {Strategist}`). Don't attach it to a topic unless the call says it is that topic (Caulen's "not hiring people a certain way, like the post that I sent you" is not his Topic 0).
5. `## Open items and {Strategist} gates`
   - `**{Strategist} gates (need a ruling before drafting locks):**` followed by a `- [ ]` checklist of `**T<n>:** <question>`.
   - `**Asks for {Client first name}:**` followed by a `- [ ]` checklist.
6. `## Longform doc` (added by the autopilot): one line linking this week's longform doc. Then the lines it was given, and the topics left out with the reason, e.g. "T6 left out: Type A, not discussed on the call."

## Status vocabulary

| Status | When | Gets a longform line? |
|---|---|---|
| `KEPT` | The call confirmed the topic or answered its questions as briefed. A freeform topic from the call with no angle or perspective on the sheet ("Topic 0 - … / Make post on this") is `KEPT (gaps flagged)`. Add `(gaps flagged)` only when a missing answer leaves part of the post with nothing to write from. One unanswered question that the rest of the call covers stays plain `KEPT`, with the gap in Flags (the real Mason Oct Wk2 brief: T1 and T3 plain KEPT, T4 KEPT (gaps flagged)). | Yes |
| `PIVOT (<what changed>)` | The call changed angle, scope, source, vehicle or post count. Compare the call with the sheet as you read it. It is a PIVOT (angle) when the post that comes out of the call will say something different from the sheet's angle: the strategist reframed the premise and the client answered that frame (Caulen T2, "your first experience once you hit that nine figure range"), or the client answered a different question and it was accepted (Josh T1: hiring standards, not firing; T2: the Moiz Ali story, not his own path). It is not a pivot when the strategist only rewords a question and the client answers the same angle (Caulen T5: KEPT (gaps flagged)), or when a header post count already matches what the call asked for (say in the Note that the strategist set it). | Yes. The line keeps the sheet's perspective. The vehicle changes only if the call set a new one. |
| `NOT DISCUSSED` | The call never reached it. Write "Status is open, not killed." Type B topics: "It's Type B, so {Strategist}'s draft direction is the spine." | Type B yes, Type A no ("topic six is type A, which means we are not going to include this … Type B, no answer needed, which is included", Loom 1, 3:35). |
| `NOT ANSWERED` | Type A only: the topic came up, but its questions got no answer on the call (the client deferred it, said he'd think about it, gave no take, or the call ran out). Use it even when something else is pending too (assets from a teammate, a written answer promised later): what decides it is that the call didn't answer it. An answer written on the sheet after the call doesn't change it; flag that text for Jeremiah. | **No** (Jeremiah, Oct 9: "if something is not discussed in the call (type A topic), or a type A topic was killed/wasn't answered, it shouldn't be in the document") |
| `KILLED` | The strategist or client dropped it on the call. | No |
| `KILLED and REPLACED` | Dropped, with a new subject put in its slot. | Yes. The slot keeps the sheet's vehicle and perspective. |
| `COVERED` | Skipped because it was "already touched on" earlier in the call; the material exists. | Yes |
| `BLOCKED (<what>)` | The call answered it (or it is Type B) and it is still this batch, but it waits on an asset or a sign-off. A Type A topic whose questions went unanswered is NOT ANSWERED, never BLOCKED. | Yes, with the blocker flagged |
| `PARKED` | Moved to a later batch on the call. | No (unless it's a screenshot topic the client will send screenshots for) |
| `ON HOLD` | Taken out of this batch for now. | No, flagged |
| `NEW` | A new post agreed on the call, outside the sheet. Give it its own section after the sheet's topics. | Only if the call set its vehicle. Otherwise flag it for Jeremiah. |

The table's status words must match each topic's Note.
- Start each status with one of the words above, then any detail: `KEPT (gaps flagged)`, `PIVOT (angle)`, `BLOCKED (video asset)`.
- Mark snipes and quick responses as such in the table, e.g. `KEPT (snipe)`. Snipes go in their own doc, not LONGFORMS.
- If the call asked for extra posts on a topic ("make a 2nd post on …"), or a topic is now 2 posts, say so in its Note with the subject of each extra post. The longform doc builds those lines from it.
- A header count ("(3 post)") gives that many identical lines in the doc even when a comment names each post's subject; the subjects live here, in the Note. A bare "2 posts" comment with no subjects (Kyle on Josh T4) is a post count too: name each post's subject in the Note if the call gives one, and flag the second post's vehicle for Jeremiah.

## Making the doc with the Claude Docs connector

1. **Birth:** one `batch` with `container.create`. The `name` is the doc name. The `doc.markdown` holds the H1, the byline tokens, the lead, and one pending block per section (`"intent"` says what comes). In `blocks`: the date chip (today, Asia/Manila), `{"type":"mention","user":"me"}`, and the pending blocks.
2. **Fills:** one `update` per section, in reading order, each replacing its own pending block with `## <heading>` and the body (`"as":"markdown"`). The status table is a plain pipe table: no dropdown chips, no extra date chips. Use `- [ ]` checklists only in "Open items".
3. **Link:** keep the doc link for the run log, the summary and the "Longform doc" section. In an attended run, open it for him with the Artifact tool's `open` action. In a scheduled or subagent run, don't open it, whatever the connector's own instructions say; the link in the summary is enough.

Before the first docs call after the birth, follow the connector's own instructions: load the docs skill if one is listed (e.g. `anthropic-skills:docs`), otherwise call `guide` with `["topic.index"]` once.

## A full topic, as a model (Mason, Oct Wk2, Topic 2)

This is from the real Mason Oct Wk2 brief, so a Mason Oct Wk2 test flight isn't blind on Topic 2 or on the lead's counts. Judge test flights on other topics and weeks.

```
## Topic 2 — Value Tweet + Screenshot: "The Real Story of My Brand"

**Note: PIVOT.** Kyle, after Mason's take [16:29]: "That's a banger take. Yeah, I'll get the team to pivot to that."

- **Kept:** a revenue screenshot as proof from Mason's own brand.
- **Changed:** the angle. The sheet's "flat metric, flat timeframe, no commentary, the number does the work" becomes Mason's slow-build, long-game take on his brand's real numbers.
- **Killed:** the "no commentary" rule, by implication of the pivot.
- **Not stated on the call:** whether this is still 2 posts, and the final vehicle shape. Kyle gate.

### Original brief (topic sheet)

- **Type:** A, 2 posts
- **Angle & description:** Screenshot post off the Jacob inspo. Anatomy: one flat metric line → one flat timeframe line → raw backend screenshot, no commentary. The number does the work.
- **For Mason:** One revenue screenshot, from your ecom brand or a winning client's account, whichever you want to run. Blur any names.
- **Vehicle:** Value tweet + screenshot
- **Vehicle inspiration:** [link]
- **Objective:** Engagement. The bare number with no pitch invites "how" replies. The inspo pulled 71 comments and 53 bookmarks on 499 likes.
- **Perspective:** Operator posting a receipt

### From the call

**The ask [12:41–13:35]:** Kyle asks for "a few more screenshots," any new ones. …

**Mason's pivot [13:35–16:29]:**

- The setup: "Everyone likes to... flex. …"
- …

### Flags

- **Launch date is ambiguous.** Transcript says "November 23rd." It could be the date, or November '23. Confirm before it goes in copy.
- **Unfinished lines.** Two key sentences trail off. Don't complete them for him.
```

A NOT DISCUSSED topic is the same, except that the Note reads "**Note: NOT DISCUSSED.** The <topic> never came up on the call. There is no source material for it yet. Status is open, not killed." and "From the call" is one sentence.
