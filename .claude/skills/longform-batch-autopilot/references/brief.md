# The post-call topic brief

## The prompt (Jeremiah's own, used verbatim)

Each week he opens last week's brief chat in the client's project, copies this prompt, and pastes it into a new chat with the new transcript (.md) and the topic sheet (PDF). "Please, in verbatim, please prompt it like this" (Loom 1, 2:55). Treat every clause as a requirement. Swap in only `{Client}` (the name he uses for the client's project, e.g. "Mason L") and `{Strategist}` (Kyle or Devin):

> Can you give me a detailed brief for the topics for {Client} based on this meeting with {Strategist}, where they talked about what to do per topic? Pay attention to detail. I also attached the topic sheet, I want you to name the brief according to its correct vehicle in the chat, make sure that you're paying attention to detail of the meeting so I don't miss details or instructions (include the pivots on the call, if any). Do not invent anything. Make sure you include the original brief in the topic sheet, and just write a "note" saying "pivot" (if there's any), so I know what was kept and what was changed or what was kept and what was killed.
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

- **Doc name** (the tab name too): `{Client} — {Mon} Wk{N} Topic Brief (Call: {Client first name} x {Strategist}, {Mon d})`. Example: `Mason L — Oct Wk2 Topic Brief (Call: Mason x Kyle, Oct 7)`. The dashes are em dashes (—).
  - The call date is the Manila date (Asia/Manila). Fireflies gives UTC (`DateString`), so convert it: 2026-10-06T18:30Z is Oct 7 in Manila.
  - `{Mon} Wk{N}` comes from the ClickUp task name (OCT WK2 → "Oct Wk2").
- **H1:** the same, without the "(Call: …)" part: `# Mason L — Oct Wk2 Topic Brief`.
- **Byline:** exactly `<?claude block asof?> · <?claude block me?>`, with today's date chip and the mention of the user.
- **Lead:** one sentence counting the outcomes by topic number. Example: "Two topics pivoted on the call (2 and 5), three were kept (1, 3, 4), and two were never discussed (6 and 7). Nothing was killed outright."

## Sections, in this order

1. `## How to read this brief`
   - Paragraph 1: "Each topic has three parts: the **Original brief** copied from the topic sheet, **From the call** (what {Strategist} and {Client first name} actually said, with timestamps), and a **Note** that marks it KEPT, PIVOT, or NOT DISCUSSED and says what was kept, changed, or left open. Call pivots override the topic sheet."
   - Paragraph 2: "Transcript quotes are {Client first name}'s words as transcribed. Where the transcription is clearly garbled, the likely word is in brackets and marked as a reading, not a fact."
   - Then the status table: `| # | Topic | Vehicle | Status |`. One row per topic. Vehicle as written on the sheet (or as changed on the call). Status in the vocabulary below.
2. `## Batch header (from the topic sheet)`
   - A bullet list with bold labels: **Client:**, **Week:**, **Strategist:**, **Platforms:**, **Call:** (`{Client} x {Strategist}, {d Mon yyyy}`).
   - Then a paragraph `**Client goal:** …` (verbatim).
   - Then `**Hypothesis (verbatim from sheet):**` with bullets `*Last week:*`, `*This week:*`, `*We expect:*`.
   - If a pivot changes a line of the hypothesis, add one plain sentence saying which line. Example: "Note: the Topic 2 and Topic 5 pivots change two lines of this hypothesis (…). Kyle hasn't restated the hypothesis."
   - If the schedule row had a note for this batch, add `**Schedule note:** <the note>`.
3. One `## Topic N — <Vehicle, Title Case>: <Title>` per topic, in sheet order. Under each:
   1. **The Note, first, directly under the heading:** `**Note: <STATUS>.** <one or two plain sentences, usually quoting the strategist's verdict>`. Example: `Kyle: "That's perfect."`
      - For a PIVOT, add bullets with bold labels: `**Kept:**`, `**Changed:**`, `**Killed:**`, `**Not stated on the call:**`.
      - If the strategist left a comment on this topic in the sheet, add `**{Strategist}'s comment on the sheet:** "<comment>"`, and say whether the call confirmed it, changed it, or didn't touch it.
   2. `### Original brief (topic sheet)`: a bullet list with bold labels, word for word:
      - **Type:** A / A, 2 posts / B
      - **Angle & description:**
      - **For {Client first name}:**, with one nested bullet per question (Type A only)
      - **Vehicle:**
      - **Vehicle inspiration:** the link
      - **Objective:**
      - **Perspective:**
      - Type B: then `**Initial draft direction (verbatim from sheet):**` and the whole draft in a ```markdown code block.
   3. `### From the call`: paragraphs that open with a bold label and a timestamp range, e.g. `**The stupid (Q1) [09:16–10:51]:**`, followed by bullets of near-verbatim quotes.
      - Timestamps are `[MM:SS]` or `[MM:SS–MM:SS]` (en dash), taken from the transcript.
      - Garbled words are marked like `[likely "TAM", reading]`.
      - A topic the call never reached gets one plain sentence: "Nothing on <what the questions asked>."
   4. `### Flags`: bullets, each opening with a bold sentence that ends in a period, e.g. `- **Launch date is ambiguous.** …`.
      - Use flags for gaps (a question with no answer), conflicts with other topics or earlier posts, names or numbers that need clearance, assets promised but not confirmed, and sentences left unfinished.
      - End a flag with "{Strategist} gate." when only the strategist can decide it.
4. `## Other items from the call (not this week's topics)`: bold-label paragraphs with timestamps for anything outside the topics, e.g. a new test format, the client's requests for next time. End each with `**Status:** not in this batch.` unless it changes this batch.
5. `## Open items and {Strategist} gates`
   - `**{Strategist} gates (need a ruling before drafting locks):**` followed by a `- [ ]` checklist of `**T<n>:** <question>`.
   - `**Asks for {Client first name}:**` followed by a `- [ ]` checklist.
6. `## Longform doc` (added by the autopilot): one line linking this week's longform doc. Then the lines it was given, and the topics left out with the reason, e.g. "T6 left out: Type A, not discussed on the call."

## Status vocabulary

| Status | When | Gets a longform line? |
|---|---|---|
| `KEPT` | The call confirmed the topic or answered its questions as briefed. Add `(gaps flagged)` when answers are partial. | Yes |
| `PIVOT (<what changed>)` | The call changed angle, scope, source, vehicle or post count. | Yes. The line keeps the sheet's perspective. The vehicle changes only if the call set a new one. |
| `NOT DISCUSSED` | The call never reached it. Write "Status is open, not killed." Type B topics: "It's Type B, so {Strategist}'s draft direction is the spine." | Type B yes, Type A no ("topic six is type A, which means we are not going to include this … Type B, no answer needed, which is included", Loom 1, 3:35). |
| `KILLED` | The strategist or client dropped it on the call. | No |
| `KILLED and REPLACED` | Dropped, with a new subject put in its slot. | Yes. The slot keeps the sheet's vehicle and perspective. |
| `COVERED` | Skipped because it was "already touched on" earlier in the call; the material exists. | Yes |
| `BLOCKED (<what>)` | Still this batch, but waiting on an asset or a sign-off. | Yes, with the blocker flagged |
| `PARKED` | Moved to a later batch on the call. | No (unless it's a screenshot topic the client will send screenshots for) |
| `ON HOLD` | Taken out of this batch for now. | No, flagged |
| `NEW` | A new post agreed on the call, outside the sheet. Give it its own section after the sheet's topics. | Only if the call set its vehicle. Otherwise flag it for Jeremiah. |

The table's status words must match each topic's Note.
- Start each status with one of the words above, then any detail: `KEPT (gaps flagged)`, `PIVOT (angle)`, `BLOCKED (video asset)`.
- Mark snipes and quick responses as such in the table, e.g. `KEPT (snipe)`. Snipes go in their own doc, not LONGFORMS.
- If the call asked for extra posts on a topic ("make a 2nd post on …"), or a topic is now 2 posts, say so in its Note with the subject of each extra post. The longform doc builds those lines from it.

## Making the doc with the Claude Docs connector

1. **Birth:** one `batch` with `container.create`. The `name` is the doc name. The `doc.markdown` holds the H1, the byline tokens, the lead, and one pending block per section (`"intent"` says what comes). In `blocks`: the date chip (today, Asia/Manila), `{"type":"mention","user":"me"}`, and the pending blocks.
2. **Fills:** one `update` per section, in reading order, each replacing its own pending block with `## <heading>` and the body (`"as":"markdown"`). The status table is a plain pipe table: no dropdown chips, no extra date chips. Use `- [ ]` checklists only in "Open items".
3. **Link:** keep the doc link for the run log, the summary and the "Longform doc" section. In an attended run, open it for him with the Artifact tool's `open` action.

## A full topic, as a model (Mason, Oct Wk2, Topic 2)

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
