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
- **Schedule doc:** the newest Claude Doc titled `Next Week: Topics and Content Batches (…)`.
- **Schedule chat:** "Client topic batch and long-form schedule", pinned in claude.ai.
  - Cowork session `cse_01VT4cAcAw8Wrd4LPaCmyNiQ` (claude.ai/chat/f6da90a8-f5ac-80f7-905d-050254f551d3).
  - Bypass permissions, Opus 5.5. It refreshes the doc from Slack and ClickUp when asked.

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

- **Mason:** Content and Topics each have a `2026` year folder, so search those, not the parent. Calls are titled "MASON L X KYLE". The client wants no $ numbers in copy (Shift Brief), and must never be cross-referenced with Jason.
- **Josh C:** OCT WK2's call is a Granola notes link, not Fireflies. Treat it as no transcript. His Topics doc title has no pipes ("Josh OCT Wk2 Topics").
- **Keval:** the schedule doc links his next batch as an OCT WK3 task. The Oct W2 doc already exists, so this batch is Week 3. Go by the linked task. Kyle: combine his written-out topics with the call context, and no snipes. Some H2s sit inside article bodies; match entry lines with `^✅?\d+(\.\d+)? - \(`.
- **Lior:** calls are titled "Reut Amariyo and Kyle Meng".
- **Shane:** repurposed long-forms. His Topics folder sits under Account Report.
- **Zarak:** X only, so the default platform is `(X)`. Last day is Oct 25.
- **Ben K:** his docs have a "Quick Response Post" H1 block above LONGFORMS. Leave it in place.
- **Nathan C:** new client, first batch OCT WK2. There is no earlier longform doc, so build it from the blank skeleton (`references/longform-doc.md`, Exceptions). Devin reviews it Tuesday evening, Jeremiah finalizes by Wednesday morning.
- **Teddy:** Devin's Oct 7 EOD moves his writing to Ymarie, but the schedule doc still gives the batch to Jeremiah. Follow the schedule doc.

## Not Jeremiah's long-forms (topics only, or someone else writes)

Brian M (Neri), Matt O (Sam), Laura (Neri), Dana P (Neri), Phil (Neri), Brian C (ends Oct 11) and Toby (paused). If one of them shows up in the long-form table, process it only if the row is unticked and the live task is in progress, and flag it.
