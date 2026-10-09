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

`entries.py` reproduces the real Mason Oct Wk2 doc exactly (`tests/`). The rules:

1. **Which topics get lines.**
   - **With a call:** KEPT and PIVOT topics get lines. NOT DISCUSSED topics get lines only if they are Type B. KILLED and PARKED topics don't. A NEW topic gets a line only if the call set its vehicle.
   - **Without a call (no transcript):** every topic gets a line.
2. **Perspective.** The topic's PERSPECTIVE field, word for word, minus its final period. Keep curly and straight apostrophes as they are ("who’s", "won't").
3. **Platform.**
   - A tag inside VEHICLE moves into the platform slot: `Longform (X/LI)` gives `(X/LI)`, and `Long form numbered listicle (LI)` gives `(LI)`.
   - With no tag, use the sheet's PLATFORMS row: X + LinkedIn gives `X/LI`, X only gives `X`, LinkedIn only gives `LI`.
4. **Vehicle wording.**
   - "Longform", "Long form" and "Long-form" all become `Long-form`.
   - "Medium form" becomes `Medium-form`.
   - Everything else stays as written ("Value tweet + screenshot", "Quote tweet + listicle").
5. **Numbers.** Numbers run 1, 2, 3 … over the lines written, not the sheet's topic numbers. In Mason Oct Wk2, sheet T3 became line 4 and T7 became 7.1/7.2.
6. **"2 POSTS".** A topic whose header says `TYPE A  2 POSTS` gives two consecutive numbers with identical lines.
7. **Split vehicles.** `Thread (X) / Long form (LI)` gives one number split into `n.1 - (X) - (…) - (Thread)` and `n.2 - (LI) - (…) - (Long-form)`. A bare `Thread` for an X + LinkedIn client splits the same way (LinkedIn has no threads).
8. **Not automatic.** Strategist comments, schedule notes and NEW posts with no vehicle never add or change lines. They go in the summary for Jeremiah to decide. Two examples:
   - Kyle's comment "Make a pivot to long-form for this week" on Mason's T2 did not change the Week 2 lines.
   - "Make a 2nd post on Boxing and chad mentality" in Week 1 did add one, by hand.

`topics.json` input, one object per topic on the sheet, in sheet order:

```json
{"platforms": "X, LinkedIn", "call": true,
 "topics": [{"n": 1, "type": "A", "posts": 1, "vehicle": "Longform (X/LI)",
             "perspective": "Operator in his 30s ... personally.", "status": "KEPT",
             "vehicle_override": null, "posts_override": null}]}
```

- Use `vehicle_override` and `posts_override` only when the call explicitly set a new vehicle or post count. The script lists every override in `notes`, so each one shows up in the summary.
- Save the printed `entries[].line` values as a JSON list (`lines.json`) for the next step.

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

- **Ben K's docs** have an extra H1 block above LONGFORMS ("Quick Response Post (from yesterday's call)" + "X/LI"). The script only clears below LONGFORMS, so that block stays. Empty its contents only if the rest of the doc is empty, and mention it.
- **No earlier doc** (a new client's first batch, e.g. Nathan C):
  - Create the doc with Drive `create_file` from HTML: `<h1><b>Name - Week N - Mon</b></h1><h1><b>Media Folder:</b> </h1><h1><b>LONGFORMS</b></h1>`. Set `parentId` to My Drive.
  - Then read it and run the same batch.
  - Say "first batch: built from a blank skeleton" in the summary.
- **Copy lands in the wrong folder.** If `get_file_metadata` shows a different parent, report it. Don't move or trash anything.
