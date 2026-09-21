# CPC, position, and event logic

## Measurement purpose

The output places three observations together without claiming causation:

- configured CPC bid from the matched Feishu `测试广告信息` sheet;
- period actual CPC from Lingxing exact-match spend and clicks;
- point-in-time organic and advertising positions from SIF.

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

Create the event when no earlier successful exact snapshot for the identity has a positive organic rank and the current successful snapshot does.

Store:

- actual capture time;
- best organic child, rank, page, and row;
- elapsed hours from timezone-normalized Listing upload time;
- input bid CPC, period actual CPC, and simultaneous advertising page/row from the deterministic campaign row selected below.

When the tracking-sheet upload value is date-only, do not invent a time-of-day. Leave `hours_to_first_rank` blank and record `上传时间仅精确到日期`; the report-period calendar dates and day-number calculation remain valid.

If one keyword exists in several campaigns, choose the row with the lowest positive input bid CPC; break a tie by campaign name. State that the first-event CPC row is a deterministic reference, not proof of which campaign caused the organic event.

Once written, never update or duplicate the event. `first_detected_at` means first detected by this workflow; precision is bounded by run frequency and scan depth.

## Automatic expansion terms

For every enabled automatic input row, match the Lingxing customer-search-term report by marketplace and exact campaign name over the confirmed report period.

- Deduplicate terms case-insensitively within `run_id + campaign + input_bid_cpc`.
- Store only terms returned for that automatic campaign.
- `first_detected_at` is the earliest workflow capture containing the term for the same Listing version, parent, campaign, CPC, and normalized term.
- `is_new_term=是` only on that first workflow capture; later captures use `否`.
- Do not calculate automatic actual CPC in v3.

A successful empty report is `未发现扩词`. A failed report remains `领星抓取失败`; do not convert it to an empty success.

## Summary reconciliation

- Exact input rows: enabled `精准` rows in `验证配置`.
- Organic-visible keywords: exact snapshot rows in the latest successful run with `organic_visible=是`.
- First-organic events: distinct immutable event rows.
- Advertising-visible keywords: latest-run exact rows with `ad_visible=是`.
- Automatic expansion terms: nonblank terms in the latest successful run.

Count rows at the contract grain. Do not silently deduplicate distinct campaigns that intentionally use the same keyword and CPC.
