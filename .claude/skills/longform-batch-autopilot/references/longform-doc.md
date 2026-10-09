# The weekly longform doc

## What it looks like

Every client's weekly doc has the same skeleton (checked on Mason, Abdul, Lior, Caulen, Keval, Ben K, Teddy and Josh C):

| Part | Text | Style |
|---|---|---|
| File title | `<Name> - <Mon> - Week <N>`, e.g. `Mason L. - Oct - Week 2` | — |
| Header | `<Name> - Week <N> - <Mon>`, e.g. `Mason L. - Week 2 - Oct` (week before month, unlike the title) | Heading 1, bold |
| Media folder | `Media Folder: ` followed by a Drive folder chip titled `<Name> - <Mon> - Week <N> - 2026` | Heading 1, label bold |
| Section | `LONGFORMS` | Heading 1, bold |
| Entries | `<n> - (<platform>) - (<perspective>) - (<vehicle>)`, each followed by the post body | Heading 2, bold |

- `<Name>` is the client's doc name from `references/clients.md` (Mason L., Keval S., Caulen F., …).
- Month tokens are Jan, Feb, March, April, May, June, July, Aug, Sept, Oct, Nov, Dec. "Sept" is not "Sep". The forms for Jan to May and Nov to Dec haven't been seen yet; reuse whatever last week's title used for the same month.
- Weeks run 1 to 5. Oct Week 1 follows Sept Week 5.

## What this week's doc starts as (the Loom 2 result)

```
Mason L. - Week 2 - Oct                     (H1, bold)
Media Folder:                               (H1, label bold, chip removed, a trailing space)
LONGFORMS                                   (H1, bold)
1 - (X/LI) - (Operator in his 30s ...) - (Long-form)       (H2, bold)
                                            (empty normal paragraph)
2 - (X/LI) - (Operator posting a receipt) - (Value tweet + screenshot)
…
```

- **Media folder:** "keep it empty for now" (Loom 2, 1:15). Someone adds the folder later.
- **Under LONGFORMS:** "delete all of this … clear formatting" (Loom 2, 1:37). Every old entry, post body, image and strikethrough goes, and no old formatting carries into the new lines.
- **The new lines:** "bold it … then space it out" (Loom 2, 3:00). Each line is bold, with one blank line after it. In the finished Week 2 doc the lines are Heading 2 + bold (like every earlier week), so the outline still lists them.
- **Star:** "so it should appear on my Starred" (Loom 2, 3:14). The Drive connector can't star a file, so do it in Chrome or list it in the summary.

## The line rules (scripts/entries.py)

`entries.py` was checked against real docs:
- **Exact matches (the golden tests in `tests/`):** Mason Oct Wk1 and Wk2, Keval Oct Wk2 and Teddy Oct Wk1.
- **Also checked line by line:** Josh C, Ben K, Abdul, Lior and Jason. The only remaining differences are hand edits no rule can predict.
- Run `python3 -I tests/run_tests.py` after any change.

1. **Who gets a line.** The first match wins.

   | Topic | Line? |
   |---|---|
   | Header label or VEHICLE says **Snipe** or **Quick Response** | **No.** These go in their own doc, "<Name> - <Mon> - Week <N> (Snipes)" / "(Quick response posts)". A plain "quote tweet" is not a snipe. |
   | Struck through, or ❌ on the sheet | No |
   | Folded into another topic (`merged_into`, only when the brief says so) | No, flagged |
   | **No transcript** | **Yes, every other topic** |
   | KEPT, PIVOT, KILLED and REPLACED (keeps its slot), COVERED ("already touched on"), BLOCKED (still this batch), RESOLVED | Yes |
   | NOT DISCUSSED, Type B | Yes |
   | NOT DISCUSSED, Type A | No |
   | KILLED / skipped / dropped | No |
   | PARKED | No. Exception: a screenshot topic where the client sends the screenshots (Keval T4). That one is yes, flagged. |
   | ON HOLD | No, flagged |
   | NEW, with a vehicle set on the call | Yes |
   | NEW, no vehicle | No, flagged "decide" |
   | A status the script doesn't recognise | Yes, flagged |

   Briefs word statuses freely ("Go, with gaps", "Draftable", "No pivot called", "Skipped on call"); `status_norm()` maps them. Put the brief's status in `status` as written.
2. **Extra posts the strategist asked for.** A comment on the topic sheet like "Make a 2nd post on Boxing and chad mentality" (Mason Wk1), or "3 posts / 1/ … 2/ … 3/ …" (Abdul), adds lines right after the parent topic's own lines.
   - Put each one in the parent's `extra_posts`, with a short perspective label taken from the comment ("Chad mentality").
   - The vehicle defaults to the parent's.
   - These are always flagged.
   - A comment that asks for a *pivot* ("Make a pivot to long-form for this week", Mason Wk2 T2) changes nothing. It goes in the brief's Note, and the line stays as the sheet has it.
3. **Perspective.** The topic's PERSPECTIVE field, word for word, minus its final period. Keep curly and straight apostrophes as they are ("who’s", "won't").
   - A PIVOT never rewrites the perspective (6 of 8 cases had pivots; none changed the line).
   - Never take line text from the brief's headings.
   - No PERSPECTIVE (a freeform "Topic 0", a NEW post): put a short label in `perspective_override` (e.g. "Toronto event", "Repurposed", "Carro Holiday Season"). Otherwise the title is used. Either way it is flagged.
4. **Platform.**
   - A tag in VEHICLE moves into the platform slot. `(X/LI)`, `(X and LI)`, `(X & LinkedIn)` and "for X and LinkedIn" all give `X/LI`; `(LI)` gives `LI`.
   - A tag glued to an image request ("with image (LI)") is not the platform.
   - With no tag, use the sheet's PLATFORMS row: X + LinkedIn gives `X/LI`, X only gives `X`. Lior and Zarak are X only.
5. **Splits** give one number with n.1 (X) / n.2 (LI), in the order written:
   - per-platform vehicles separated by `/`, `,`, `;` or `·` after a tag (`Thread (X), Long-form listicle (LinkedIn)`), written as prefixes (`X article + Doc SS QT / LI Longform`), or as bullets (`•X: … •LinkedIn: …`);
   - a bare `Thread`, or a thread inside brackets, for an X + LinkedIn client: X `Thread`, LI `Long-form` (Abdul: `Long-form listicle`);
   - `X article, then quote tweet` is a different case: two numbers, `(X) … (Article)` then `(X) … (Article wrapper)` (Keval T6).
6. **Post counts.** "2 POSTS" in the header, or ", x2" / "two posts" in VEHICLE, gives consecutive numbers with identical lines.
7. **Vehicle wording.**
   - Longform / Long form → `Long-form`; Medium form → `Medium-form`. Inside a phrase they stay lowercase ("Opinion-led long-form post").
   - "Listicle long-form" → `Long-form listicle`.
   - Format nouns after the first word are lowercase ("Side-by-side comparison thread", "+ infographic"). Named things keep their capitals ("Apple Notes Screenshot").
   - Dropped: trailing ALL-CAPS instructions, bare "with image" requests, and noise brackets like (organic), (dash), (GDS).
   - Any other bracket becomes a comma qualifier ("Listicle (greentext)" → "Listicle, greentext"), flagged.
   - Straight double quotes become curly (`“hack”`).
8. **Numbers.** Numbers run 1, 2, 3 … over the lines written, not the sheet's topic numbers.
9. **Per-client habits** (`CLIENTS` in `entries.py`, chosen by `"client"`):

   | Client | Habit |
   |---|---|
   | Jason G. | Perspective drops its last sentence. "Doc SS" / "Google Doc Screenshot" → "Apple Notes …" |
   | Abdul F. | "+ photo" is dropped, a thread's LinkedIn half is "Long-form listicle", "Doc SS" → "Apple Notes …" |
   | Ben K. | Every X/LI post splits into n.1 (X) / n.2 (LI) because of the DM CTA, except a value tweet with no CTA (flagged). A "FOR LINKEDIN" note sets the LI vehicle (`li_vehicle`). |
   | Joshua C. | Promo posts split X / LI |
   | Lior P., Zarak A. | X only |

10. **Checks.** If the brief states a total post count, set `expected_posts`; a mismatch is reported in `problems`. A line can never have an empty slot: a missing value becomes `TBD` and goes in `problems`.

`topics.json` input, one object per topic on the sheet, in sheet order (the full schema is at the top of `entries.py`):

```json
{"client": "Mason L.", "platforms": "X, LinkedIn", "call": true, "expected_posts": null,
 "topics": [{"n": 1, "type": "A", "label": null, "title": "Being Stupid In Your 60s", "posts": 1,
             "vehicle": "Longform (X/LI)", "perspective": "Operator in his 30s ... personally.",
             "status": "KEPT", "struck": false, "check": null,
             "vehicle_override": null, "posts_override": null, "perspective_override": null,
             "extra_posts": []}]}
```

- Copy `vehicle`, `perspective` and `label` exactly as the sheet has them, including bullets and line breaks. The script does all the cleaning.
- Read the VEHICLE field, not the italic vehicle in the topic's header row.
- Use `vehicle_override` and `posts_override` only when the call clearly settled a new vehicle or post count, not when it was only floated (Josh T4 "listable format"). The script lists every override in `notes`.
- Save the printed `entries[].line` values as a JSON list (`lines.json`) for the next step. Put every `notes`, `problems` and `left_out` item in the run summary.

## The copy and the edit, step by step

1. **Last week's doc.**
   - Search the client's Content folder: `search_files` with `parentId = '<content folder id>' and title contains ' - Week '`. Mason's is the `2026` subfolder; most clients have no year folder.
   - Keep docs titled exactly `<Name> - <Mon> - Week <n>`, trimming a trailing space. Drop suffixed siblings: (Snipes), (Snipe), (Design Request), (Design Requests), (Quick Response), (Quick response posts), (Topic N), (Ad Hoc Post), Longforms.
   - Take the newest by createdTime.
   - The shared copy there usually belongs to writing@mogulmedia.ca; Jeremiah's own draft of the same week sits in his My Drive. Either works as the source, since everything under LONGFORMS is deleted. Prefer the Content-folder copy, as in the Loom.
   - If two docs share a title (Ben K has two "Oct - Week 1"), take the newer one.
2. **Copy.** Call `copy_file` with `{"fileId": <last week>, "title": "<Name> - <Mon> - Week <N>", "parentId": <My Drive root id>}`. Then call `get_file_metadata` on the new ID and check the parent and the title.
   - Comments and sharing don't carry over, which is what the Copy dialog does with its boxes unticked.
3. **Read the copy.** Call `read_doc` on the NEW id. A result over about 50K characters is saved as `{"content": {...}}`; the script unwraps it.
4. **Build the batch.** Run `python3 -I scripts/longform_batch.py <saved read> "<Name> - Week <N> - <Mon>" lines.json`. It:
   - finds the header, the Media Folder line and the LONGFORMS heading itself, and stops if the doc doesn't have exactly one of each or has more than one tab;
   - deletes everything after LONGFORMS except the body's final newline;
   - inserts `line\n\n` for each line, resets styles to normal, then makes each line Heading 2 + bold;
   - deletes anything between the Media Folder line and LONGFORMS (Ben's leftover Quick Response block);
   - removes the chip or link from the Media Folder line, keeping "Media Folder: ";
   - replaces the old header text last, so its length can't shift the other ranges;
   - prints `{"documentId","requests","writeControl"}`. `writeControl.requiredRevisionId` comes from the read, so Google refuses the whole batch if the doc changed in between.
5. **Send it** with `update_doc`. It is one atomic call: if it fails, nothing changed. Read the copy again and rebuild; never resend stale indexes.
6. **Verify** with `read_doc` again:
   - the header is the new text;
   - the Media Folder paragraph has no richLink or link;
   - the body holds no `inlineObjectElement`;
   - the lines match `lines.json` exactly, each Heading 2 and bold, each followed by an empty normal paragraph.

### Exceptions

- **Ben K's shared docs** carry last week's "Quick Response Post (from yesterday's call)" block between Media Folder and LONGFORMS. It isn't skeleton (his My Drive drafts don't have it), so `longform_batch.py` deletes whatever sits between those two lines.
- **No earlier doc** (a new client's first batch; tested on Nathan C, Oct 9):
  - Create the doc with Drive `create_file` from HTML, `contentMimeType` `application/vnd.google-apps.document`, `parentId` = My Drive. The HTML is `<h1><b>Nathan C. - Week 2 - Oct</b></h1><h1><b>Media Folder:</b></h1><h1><b>LONGFORMS</b></h1>`.
  - Read it with `read_doc`, then run the batch with the full header text (not `auto:`) and `--explicit-fonts`, e.g. `longform_batch.py <read> "Nathan C. - Week 2 - Oct" lines.json --explicit-fonts`.
    - `--explicit-fonts` gives the header block Arial 20 and the lines Arial 16 bold, matching the copied docs (the HTML import comes in at 24/18).
    - The script also handles LONGFORMS being the last paragraph, and puts back the space after "Media Folder:" that the import drops.
  - Say "first batch: built from a blank skeleton" in the summary.
- **Copy lands in the wrong folder.** If `get_file_metadata` shows a different parent, report it. Don't move or trash anything.
