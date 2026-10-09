# Clients: names, pods and folders

Each client goes by several names: one in the schedule doc, one in ClickUp, one on the longform doc, one on the brief and one on the Claude project. This table maps them. IDs were checked on Oct 9 2026.

- If an ID here stops working (a 404, or the wrong folder), find the folder again: search the client folder's children with `parentId = '<client folder>' and mimeType = 'application/vnd.google-apps.folder'`. Use the corrected ID, and say in the summary that this table needs updating.
- A client not listed here: find their folder under the pod folder by name, use the same patterns, and flag "not in clients.md".

## Shared locations

- **Drive MASTER FILE:** `13oJ5I0-1B2tJVEu6Oy3ybAtmkZj-gwf4`
  - POD 2 (Kyle M Team): `1sS6qkBs0RkUERQdx0e6wgpbSTrrecHGR`, strategist Kyle (Kyle Meng, ClickUp 120211600). Calls recorded on **Fireflies**.
  - POD 1 (Devin Team): `1ic67mJ6FyTzSZkwCROilV2YKN5yIVK-j`, strategist Devin (Devin Downs, ClickUp 88679247). Calls recorded on **Krisp**.
- **Jeremiah's My Drive root:** `0APF3ebrWaXbcUk9PVA`. Confirm with `get_file_metadata` `fileId "root"`.
- **ClickUp:** workspace `9015589795`, space `90152587982`. Each client has a folder `<PREFIX> | INTERNAL` with a list `CONTENT WRITING`. Tasks are named `<PREFIX> | <MON> WK<N> | Longforms`, with siblings `| New Topics` and `| Design Request`. Jeremiah is ClickUp user 306644176.
- **Schedule doc:** a Claude Doc titled `Next Week: Topics and Content Batches (<dates>)`. The schedule chat updates it every week and the dates in the title change ("it is updated weekly so keep that in mind", Jeremiah, Oct 9). Known: artifact `5dSKyoafmKQJ93gw67JPi2` (claude.ai/code/artifact/257af056-867b-41ed-98ea-64cc1f8a1a8b), "(Oct 12–16)" on Oct 9. SKILL.md Step 1.1 opens it and checks the Artifact list for a newer one.
- **Schedule chat:** "Client topic batch and long-form schedule", pinned in claude.ai.
  - Cowork session `cse_01VT4cAcAw8Wrd4LPaCmyNiQ` (claude.ai/chat/f6da90a8-f5ac-80f7-905d-050254f551d3).
  - Bypass permissions, his usual model. It refreshes the doc from Slack and ClickUp when asked.

## Jeremiah's long-form clients

| Schedule name | ClickUp prefix | Pod | Longform doc name | Brief name | Claude project | Client folder | Content folder | Topics folder |
|---|---|---|---|---|---|---|---|---|
| Mason | MASON | Kyle | Mason L. | Mason L | Mason L. (claude.ai/project/019ea4df-9219-7701-ae41-474c4ff6e50c) | `13bv-Xyhb8uzd9fSiziOOYlIz4XTRkbo8` | `1g0x6Sv9L8cvKW--00ob1qPPbkkqvOzHz` (Mason Content › 2026) | `16UDGiNWqEBGhcKb75ufWWnDpLD_oCE5Y` (Mason Topics › 2026) |
| Josh C | JOSH | Kyle | Joshua C. | Josh Chin | Joshua C. | `1R2MWxk2qPx0L6V_DMsNUA7AO9ON5yEmr` | `1NArtqUkgRoOSv5Ygi_F5RAMf7im3B-IF` | `1f401d_yJW4FHVPN4I1fBYWZc6LQnrWll` |
| Keval | KEVAL | Kyle | Keval S. | Keval S. | Keval S. | `1Z4h09MIdmAL6xFsgjloovnPxZB_survR` | `1T-ElCqV072D6uMxHJ7e6GuuVPO-2O8-4` | `1sJo17yj48Z86MgwPP0EyuQFW9Lq6c3Rq` |
| Caulen | CAULEN | Kyle | Caulen F. | Caulen F. | Caulen F. | `1oLF1IdOFTvnisRPwozo4Yn9SzRWNwM01` | `1MQElfg2s_CPbABWcj0exromYPoufm7uj` | `1qAngoVF7OUG9lqV_ZXm5gj885W3JwD_v` |
| Lior | LIOR P | Kyle | Lior P. | Lior P. | Lior P. | `1PaJbnDXe8_eBe1IpaM66cOt3EJa8u_eX` | `1MHTy5o2hEXpkO-BabThTvfOpkLxuY1Hr` | `1FipPHEe_rK8PxJbT9mOSawjqOL2PxExz` |
| Abdul | ABDUL | Kyle | Abdul F. | Abdul F. | Abdul F. | `1pu7tDXElP3bGzoURXosZb-gwe76hfyIS` | `1M9CKuCvP8_4OjUXUE5cUt7C352txwRcq` | `1COxH8qKlQmkfrAM4ZFTG_AQtvrit-SQn` |
| Jason | JASON | Kyle | Jason G. | Jason G. | Jason G. | `1yzHdAwr6K3EAueVVtpnC2TMfJHzJpG_p` (title "JASON " with a trailing space) | `1re01CNGNRCvagsSJbOrNhnjlMicaQ_Tw` | `1M5DOSr8lzxkRnj6PT-Knc-lmiLDNE7LE` |
| Shane | SHANE | Kyle | Shane H. | Shane H. | Shane H. | `142xCMHIlTB2GZF0k5OjTNShmYt1mutaS` | `1fwWSovuHqcBkAG69e4cGEwyA9qteAvvB` | `1Wfv6eqKlNXsRwrYbzvT7lv7jLxp2ucqV` (Account Report › Shane Topics › 2026) |
| Michael K | MICHAEL K | Kyle | Michael K. | Michael K. | Michael K. | `1ACSiDehTuauQTII5jLkKoTGWtZthk4fJ` | `17Qdtw5jYhJhmokmtISXxi1Hq4b-3wGUO` | `1s2-jOLhAYbSkW1g3F_aZC9mZirKfebqE` |
| Zarak | ZARAK SARAH | Kyle | Zarak A. | Zarak A. | Zarak A. | `1l6q6dpLfBRLrrhM54fNvGMOeP4VzMnGe` | `1Ac0tWr7JHHPhjXv6zXI8KVLR6kiA16Gn` | `1pWq3WpWj3Ei7PNzTgwi86QdYUraX7YEI` |
| Ben K | BEN K | Devin | Ben K. | Ben K. | Ben K. | `1YWQ8qF4n3sU6hcfGCPdVeGhhZLjPED5e` | `1EevVodfNeQHT0qdHWXIexkxsYsMIJKqw` | `1TGrmHuENr19hW9RprZO1mfu6Fd3fHS1_` |
| Teddy | TEDDY | Devin | Teddy T. | Teddy T. | Teddy T. | `1BSW_ukz05qyUTDDze0qHs0UgFaLNV95m` | `18hrCHizlOUtzlryGWw-LcawyvNNPO8eg` | `12rpupzdU8HtvAaXpwibvCAWWAX77rMYS` |
| Josh D | JOSH D | Devin | Josh D. | Josh D. | Josh D. | `1oaGHaMJbhX9C0vdEEaDIoaPQz4g479g7` | `1t9Q2aNk0MYtoREM0LHGfKNddOwaTMV_M` | `1kb8QtomLcEgSdNmhw98TNXlRgI0qorIn` |
| Marco | MARCO | Devin | Marco B. | Marco B. | Marco B. | `1YCqqTRlU92RCOGBGlVElLUGdF1KP6Cfj` | `1QykvIQ6gvjZBq3iSftVDfFgJycp_jqoy` | `1Z9U2-AUec_9Zou3B0b_Jkd--_AbJunIq` |
| Nathan C | NATHAN C (folder NATHAN; next-week tasks say "NATHAN") | Devin | Nathan C. | Nathan C. | (none yet) | `1D3z_7gjfP0A6Jkb6vcEMSk6GnnuQuccv` | `1LjQtm1TaEU7yxhZ0LzqsdTkw1fiUSuSZ` | `1BNcC5pomnIS10VXdiBHZ7ZSCY3AVbZeS` |

## Per-client notes

- **Kyle's pod:** Fireflies call titles come in two forms, "<FIRST> <LAST INITIAL> X KYLE" and "<First> <Last> and Kyle Meng". Kyle says "quick response" loosely for snipes: keep a topic labelled Snipe as a snipe unless he names the Quick response doc.

- **Mason:** Content and Topics each have a `2026` year folder, so search those, not the parent. Calls are titled "MASON L X KYLE". The client wants no $ numbers in copy (Shift Brief), and must never be cross-referenced with Jason.
  - The scope of "no $ numbers" is unknown. Until Jeremiah settles it, it is one summary line per run, not a gate per topic (Mason Oct Wk2 flight).
  - With no Client Brain or ledger file, his other Client Info files ("Mason feedback sheet" from 2025, "Mason INFO SHEET") are fallback context.
- **Josh C:** OCT WK2's call is on Granola, not Fireflies. The ClickUp comment links the Granola notes, and the transcript is pasted into **the third tab of his Topics doc** (after Client strategy and Strategy; Jeremiah, Oct 9). Use that tab as the transcript, whatever its name.
  - His Topics doc title has no pipes ("Josh OCT Wk2 Topics").
  - A freeform "Topic 0 - <promo>" can sit above the topic tables.
  - Platform tags are written "(X and LI)" or "(X/LI)".
  - In the transcript tab, "Me" is Josh (he records the call), "Kyle Meng" is Kyle and "Them" is anyone else. It has no timestamps.
  - He has no Client Brain or ledger. His context is in "JOSH CLIENT INFO SHEET" (Client Info) and "Josh Writer's Checklist" (client folder root); his sheet's Client Brain link opens an old topic sheet.
- **Keval:** the schedule doc links his next batch as an OCT WK3 task. The Oct W2 doc already exists, so this batch is Week 3. Go by the linked task. Kyle: combine his written-out topics with the call context, and no snipes.
  - Calls are titled "Keval Shah and Kyle Meng". His ClickUp task can be assigned to Ymarie and Kyle rather than Jeremiah. The schedule doc settles it ("Keval's writing is yours even where ClickUp still lists Ymarie"): info only, never flagged weekly.
  - He pastes his own written-out answer into each topic box right after PERSPECTIVE. The perspective ends at the blank line; the rest goes in the brief as his written-out answer.
  - His ledger ("Keval Shah — Client Feedback Ledger") gives the agency as "$2.5M/year" where sheets say "$2M": flag the clash, don't settle it. Some H2s sit inside article bodies; match entry lines with `^✅?\d+(\.\d+)? - \(`.
- **Lior:** calls are titled "Reut Amariyo and Kyle Meng". He is X only, so every line is `(X)` and threads never split.
  - Kyle's Longforms task carries only the Topics doc link (OCT WK2: no Fireflies link, no PDF), though a call happened. Where his call links get posted is still to be confirmed with Jeremiah; until then a run says "call happened, transcript link missing: ask Kyle".
  - Topics can be killed by strikethrough alone.
  - Freeform "Topic 7" / "Topic 8" notes sit under the tables.
- **Jason:** perspectives drop their last sentence; Doc SS becomes "Apple Notes SS". A "✅Topic 0 - <title>" with a "Vehicle:" line can open the sheet.
- **Abdul:** quick-response topics are marked in the TYPE ("TYPE A (… QUICK RESPONSE)") and go in a shared "Quick response" doc, found by his Content folder.
  - "+ photo" is dropped from vehicles; a thread's LinkedIn half is "Long-form listicle".
- **Keval:** "X article, then quote tweet" gives an Article line plus an Article wrapper line. Value-tweet lines copy the sheet's PERSPECTIVE and VEHICLE like any topic (Oct Wk2 happened to read `(Client win) - (Value tweet screenshot)`; it is not a habit).
- **Shane:** repurposed long-forms. His Topics folder sits under Account Report.
- **Zarak:** X only, so the default platform is `(X)`. Last day is Oct 25.
- **Ben K:**
  - His shared docs carry last week's "Quick Response Post" block above LONGFORMS. The batch script deletes it.
  - His Topics doc has a stale STRATEGY tab (tabId `t.0`; in OCT WK2 it sits second). Always pick CLIENT STRATEGY by name.
  - He splits CTA posts into X and LI. Value tweets stay one X/LI line unless a FOR LINKEDIN note gives a LinkedIn format (his Oct Wk1 doc: T8's value tweet unsplit).
  - His snipes and quick responses go in separate "(Snipes) " and "(Quick response posts) " docs; those titles end in a space.
- **Nathan C:** new client, first batch OCT WK2. There is no earlier longform doc, so build it as a new empty doc (`references/longform-doc.md`, Exceptions; never an HTML import). Devin reviews it Tuesday evening, Jeremiah finalizes by Wednesday morning.
  - Another "Nathan" is in Drive (Nathan Snell, nCino / Rayleon). Never use his files (Nathan Oct Wk2 flight).
- **Teddy:** Devin's Oct 7 EOD moves his writing to Ymarie, and Arooba wrote in the group DM (Oct 7): "we're gonna be moving teddy from you to ymarie". The schedule doc still gives the batch to Jeremiah, so follow it, and put "Teddy: confirm he's still yours (Arooba, Oct 7)" in the summary until that's settled.
  - His Topic 1 is usually a Quick Response or Snipe ("bring 2–3 recent wins"), which goes in its own doc, not LONGFORMS. He has used "(Snipe)", "(Snipes)" and "(Quick Response)": name it with last week's exact suffix.
- **Josh D:** his sheets can be titled "JOSH D | <MON> WK<N> | HYPOTHESIS". Devin adds extra posts in comments that aren't on a topic ("EXRA - … turn it into an article with Doc SS QT"): a freeform topic after the last one. His quote-tweet snipes run on X and again on LinkedIn with an image ("Josh D. - Sept - Week 5 (Snipes)"), so X/LI is right for them.
- **Caulen:** calls are titled "caulen Foster and Kyle Meng". Rules from his Claude project memory, as Jeremiah's Oct Wk2 brief applies them: revenue is always "9 figures" in copy; credit is plural ("we") for anything Brello did; the 9 figures belong to Brello, not the agency; don't position him as the DR copywriter. Flag any quote that breaks one.

## Not Jeremiah's long-forms (topics only, or someone else writes)

Brian M (Neri), Matt O (Sam), Laura (Neri), Dana P (Neri), Phil (Neri), Brian C (ends Oct 11) and Toby (paused). If one of them shows up in the long-form table, process it only if the row is unticked and the live task is in progress, and flag it.
