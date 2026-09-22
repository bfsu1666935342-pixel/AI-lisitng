# CPC, position, and event logic

## Measurement purpose

The output places four observations together without claiming causation:

- configured CPC bid from the matched Feishu `测试广告信息` sheet;
- period actual CPC from Lingxing exact-match spend and clicks;
- point-in-time exact-keyword organic and advertising positions from SIF;
- a point-in-time reverse-ASIN population of every target-family keyword directly reported on organic pages 1-3.

Always retain their different timestamps and periods.

## Identity normalization

- ASIN: uppercase ten-character value.
- Keyword/search term identity: trim outer whitespace, collapse repeated internal spaces, compare case-insensitively, preserve source spelling for display.
- Campaign identity: preserve displayed name; trim only outer whitespace for matching.
- CPC: positive numeric value in marketplace currency.

## Exact-keyword actual CPC

For each enabled exact input row, match Lingxing evidence on:

`marketplace + campaign_name + exact match type + normalized keyword + confirmed report period`

Aggregate only matched exact rows:

- `exact_clicks = sum(clicks)`
- `exact_spend = sum(spend)`
- `actual_cpc = exact_spend / exact_clicks`

Leave `actual_cpc` blank when clicks are zero or missing. Preserve zero spend when clicks are positive. Never use:

- input bid CPC as actual CPC;
- parent/campaign blended CPC;
- phrase, broad, product-targeting, or automatic rows;
- another period or marketplace.

Use concrete quality flags: `正常`, `精准词未匹配`, `点击为0`, `缺少花费`, `匹配到多条已汇总`, `领星抓取失败`.

## SIF position snapshot

For every enabled exact keyword, inspect the whole resolved ASIN family.

- Best organic result: lowest positive organic rank; retain its child ASIN, page, and row.
- Best advertising result: lowest positive advertising rank; retain its child ASIN, page, and row.
- `organic_visible=是` only when a target child has a positive organic rank.
- `ad_visible=是` only when a target child has a positive advertising rank or directly observed advertising page/row.

Provider values `0`, `-`, `N/A`, and empty text normalize to blank unless explicitly documented as valid.

Capture page and row directly from the SIF result or visible search layout. Do not derive page or row from a guessed results-per-page count. If only an overall rank exists, keep the rank and leave page/row blank with `quality_flag=页行不可可靠换算`.

If several children tie, choose the lexicographically smallest ASIN for deterministic storage.

## Advertising-position attribution

SIF proves that a target-family ASIN occupies an advertising position for the query. It does not expose the campaign that caused it.

- When exactly one enabled exact campaign targets the normalized keyword, use `唯一精准活动`.
- When multiple enabled exact campaigns target it, use `多活动共享观察` and repeat the same SIF observation on each campaign row.
- When the advertising position is absent, use `未观察到广告位`.

Do not claim campaign-level position attribution from SIF alone.

## First organic-position event

Event identity:

`listing_version_id + parent_asin + normalized keyword`

Create the event when no earlier workflow event exists for the identity and either the enabled exact-keyword scan or the page-1-to-3 reverse-ASIN scan currently reports a positive organic position.

Store:

- actual capture time;
- best organic child, rank, page, and row;
- elapsed hours from timezone-normalized Listing upload time;
- input bid CPC, period actual CPC, and simultaneous advertising page/row from the deterministic campaign row selected below.

When the tracking-sheet upload value is date-only, do not invent a time-of-day. Leave `hours_to_first_rank` blank and record `上传时间仅精确到日期`; the report-period calendar dates and day-number calculation remain valid.

If one keyword exists in several campaigns, choose the row with the lowest positive input bid CPC; break a tie by campaign name. State that the first-event CPC row is a deterministic reference, not proof of which campaign caused the organic event.

Once written, never update or duplicate the event. `first_detected_at` means first detected by this workflow; precision is bounded by run frequency and scan depth.

## Page-1-to-3 organic-keyword snapshot

For each run, union SIF reverse-ASIN organic-keyword results across every resolved child ASIN. Keep only rows with a directly reported `organic_page` equal to 1, 2, or 3.

- Normalize keyword identity with the shared keyword rule and deduplicate across the family.
- For duplicates, keep the lowest positive `organic_rank`; break a rank tie with the lowest page, then row, then lexicographically smallest child ASIN.
- Do not require the keyword to exist in `测试广告信息`. Record `is_ad_test_keyword=是` only when it matches an enabled advertising-input keyword after normalization.
- Do not infer page from an assumed results-per-page count. A row without a directly reported page cannot enter the page-1-to-3 population.

First-observation identity:

`listing_version_id + parent_asin + normalized keyword`

On the first successful observation, append one immutable row to `关键词首次自然位` with the actual capture time and run ID. On every later run, read that original time exactly; never replace it with a newer time, a better rank, or a provider-history date.

Maintain the reader-facing `前三页自然位记录` with exactly `关键词`、`首次抓取时间`、`首次自然位置`、`本次抓取时间`、`本次自然位置`. Preserve the first pair and row order forever. Append new keywords at the bottom with both pairs set from their first actual capture. On a complete successful scan, update only the current pair for prior rows: current page/row as `第X页第Y位`, or `无自然位` when absent from the full directly observed pages-1-to-3 set. A reappearing word updates its original row. Partial/failed scans cannot establish disappearance; leave unconfirmed current pairs unchanged and log coverage.

During a v3/v4-to-v5 upgrade, a matching immutable `关键词首次自然位` event is valid earlier workflow evidence and seeds the first time/run and first page/row. Nonmatching keywords begin at their first successful new capture. A v4 reader row's current position/time is migrated as the current pair, not re-labelled with the migration time.

## Automatic expansion terms

For every enabled automatic input row, match the Lingxing customer-search-term report by marketplace and exact campaign name over the confirmed report period.

- Deduplicate terms case-insensitively within `run_id + campaign + input_bid_cpc`.
- Store only terms returned for that automatic campaign.
- `first_detected_at` is the earliest workflow capture containing the term for the same Listing version, parent, campaign, CPC, and normalized term.
- `is_new_term=是` only on that first workflow capture; later captures use `否`.
- Do not calculate automatic actual CPC in v5.

A successful empty report is `未发现扩词`. A failed report remains `领星抓取失败`; do not convert it to an empty success.

## Summary reconciliation

- Exact input rows: enabled `精准` rows in `验证配置`.
- Organic-visible keywords: exact snapshot rows in the latest successful run with `organic_visible=是`.
- First-organic events: distinct immutable event rows.
- Advertising-visible keywords: latest-run exact rows with `ad_visible=是`.
- Automatic expansion terms: nonblank terms in the latest successful run.
- Page-1-to-3 organic keywords: unique rows in `前三页自然位记录` whose latest confirmed `本次自然位置` is a directly observed `第X页第Y位`; exclude `无自然位` and any stale rows when the latest scan is partial/failed. Report the count as unavailable rather than a complete current count if coverage is incomplete.

Count rows at the contract grain. Do not silently deduplicate distinct campaigns that intentionally use the same keyword and CPC.
