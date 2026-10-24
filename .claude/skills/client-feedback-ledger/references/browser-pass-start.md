# Where the first browser pass starts

On 2026-10-24 a cloud run without a browser logged comments, replies and Slack
text for every writing client. Its sections are marked "Browser pass pending".
The first run with Chrome must cover version history (and the other browser
sources) starting from the batch below.

These start points are not read from the log headings. Several manual logs
can't be read automatically: Josh's has no batch headings, Teddy's stop at Jul
Wk 5 although the entries run through Sept Wk 4, and Caulen's read "Weeks 2 &
3, Sept 2026". The 2026-10-24 collectors read each log and chose these.

| Client | Start at | Why |
|---|---|---|
| Abdul F. | OCT WK1 | log ends Sept Wk 5 |
| Ben K. | SEP WK4 | log ends Sept Wk 3 |
| Caulen F. | SEP WK5 | log ends Sept Wk 4 (heading "Week 4, Sept 2026") |
| Jason G. | SEP WK5 | log ends Sept Wk 4 |
| Joshua C. | SEP WK4 | log has dated entries through Sept Wk 3 and no batch headings |
| Keval S. | OCT WK2 | log's Oct Wk 2 section covers only the Snipes doc |
| Lior P. | OCT WK1 | log ends Sept Wk 5 |
| Marco B. | SEP WK3 | headings stop at Aug Wk 4, but entries run through Sept Wk 2 |
| Mason L. | OCT WK1 | log ends Sept Wk 5 |
| Michael K. | SEP WK3 | log ends Sept Wk 2 (headings like "September, Week 2") |
| Nathan C. | OCT WK2 | log was empty. The earliest batch doc in his current naming is Oct Wk 2; older "Nathan \| Jan Wk2 \| Content" docs predate the roster and wait on Jeremiah's answer |
| Shane H. | OCT WK1 | log ends Sept Wk 5 |
| Teddy T. | SEP WK5 | headings stop at Jul Wk 5, but entries run through Sept Wk 4 |

Rule: while a client's log still holds any "Browser pass pending" section, the
browser pass starts at this table's batch. Once every pending batch has a
"Pass: browser" section, this table no longer applies; from then on Stage 0
uses `last_complete_batch()`.
