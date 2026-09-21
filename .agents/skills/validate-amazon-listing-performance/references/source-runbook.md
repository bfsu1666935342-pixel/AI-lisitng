# Lingxing and SIF runbook

## Tool discovery

Lingxing and SIF schemas can change. At each new execution session, discover the current available tool and schema before calling it. Do not reuse version identifiers or field names from an earlier session when current discovery returns different values.

Use connected integrations when available. Otherwise use the in-app browser or the user's authenticated Chrome session. Never store credentials in the Skill, workbook, logs, or output.

## Marketplace mapping and ASIN family

Map input `站点` through the current connected catalog or returned Listing record. Filter every query to that marketplace.

Resolve the parent through the current Lingxing Listing-list query:

1. exact-search the input ASIN in the selected marketplace;
2. deduplicate rows across stores by `asin + parent_asin + marketplace`;
3. require exactly one distinct nonblank parent;
4. if input may itself be a parent, retry an exact parent-ASIN query;
5. query that parent to obtain the deduplicated child-ASIN set.

Zero parent matches is `父ASIN未匹配`. Multiple parents is `父ASIN匹配冲突` and requires user direction.

## Lingxing report-period gate

- Default start: Listing upload marketplace-local date.
- Default end: execution marketplace-local date.
- Inclusive days = end - start + 1.
- At 30 days or fewer, record `自动执行（≤30天）`.
- Above 30 days, stop before collection and ask for full period, upload-first 30 days, or most recent 30 days.

Use the same confirmed dates for exact-keyword actual CPC and automatic search terms.

## Exact-keyword advertising report

Use the current Lingxing sponsored-products keyword or targeting performance report that exposes campaign name, match type, keyword, clicks, and spend.

For each enabled exact input row:

1. filter the selected marketplace and confirmed dates;
2. match the exact campaign name;
3. retain only exact keyword match rows;
4. compare normalized keyword identity;
5. sum clicks and spend across legitimate daily or duplicated source rows without double counting;
6. calculate actual CPC under `metric-and-event-logic.md`.

If the source cannot distinguish exact from broad/phrase, mark that row unavailable. Never fill it from blended campaign CPC.

## Automatic customer-search-term report

Use the current Lingxing sponsored-products customer-search-term report.

For each enabled automatic input row:

1. filter marketplace, confirmed dates, and exact campaign name;
2. retain search terms generated under the automatic campaign;
3. case-insensitively deduplicate display-equivalent terms;
4. preserve source spelling and capture time;
5. do not bring search terms from exact, phrase, broad, or another automatic campaign.

The input CPC is the campaign's configured bid supplied by the user. v3 does not calculate automatic actual CPC.

## SIF current-position collection

For each enabled exact keyword:

1. use the selected marketplace and a consistent search context;
2. inspect the resolved parent family, not competitor ASINs;
3. capture the best visible organic target-family result;
4. capture the best visible sponsored target-family result;
5. retain the child ASIN owning each result;
6. capture overall rank when explicitly returned and directly observed page and row;
7. record actual scan depth and exact Beijing and marketplace-local capture times.

Natural and advertising page/row are point-in-time observations. Page layout may vary by device, postcode, session, placement type, and time. Keep the same context within a run and state any context change in `quality_flag`.

When nothing is found within scan depth, retain a placeholder exact snapshot. This means `not found within scan depth`, not `no Amazon rank exists`.

## Failure handling

- Lingxing identity failure: do not query guessed parents.
- Exact-report failure: preserve SIF results, leave actual CPC unavailable, and record the source error.
- Automatic-report failure: do not write `未发现扩词`; write a failure placeholder.
- SIF failure: preserve Lingxing evidence, leave position fields blank, and record the source error.
- Partial keyword success: retain successful rows and identify failed keywords.

Every attempted invocation gets one `运行记录` row.
