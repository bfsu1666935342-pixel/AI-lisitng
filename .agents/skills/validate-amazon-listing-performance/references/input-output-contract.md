# Fixed input and output contract

Output contract version: `v3`

This version validates organic position, exact-ad position and CPC, and automatic-campaign expansion terms. It intentionally replaces the broad traffic/conversion `v2` contract. Do not silently migrate a v2 workbook.

## Ordinary invocation and Feishu sources

The ordinary user input is one target ASIN. Use `feishu-sheet-io.md` to resolve exactly one row in the fixed project tracking sheet, then read both business inputs from that row:

1. product and marketplace information from the Drive workbook referenced by `输入文档`;
2. advertising campaign, type, keyword, and configured CPC from the online sheet referenced by `测试广告信息`.

Do not ask the user to upload either source while both references are accessible. The bundled input assets define the accepted schemas and remain fallback examples, not the normal invocation interface.

The tracking-sheet target ASIN is the operational input ASIN. For `新品` and `老品新listing测试`, the ASIN inside `输入文档` is source-product metadata and may intentionally differ. Use the same row's `第1天上传时间` as the target Listing upload-date source.

## Listing input workbook

Keep the existing three sheets and fixed headers.

### `新品基础信息`

Exactly one nonblank product row. Fixed headers:

1. `ASIN`
2. `Listing首次上传时间（站点当地时间）`
3. `产品类型`
4. `产品人群画像`
5. `使用场景`
6. `用途`
7. `核心卖点`
8. `目标 Amazon 类目`
9. `类目是否存在多个稳定产品类型细分，必须明确填写“是”或“否”。`
10. `自有品牌名称及品牌别名声明。`
11. `站点`

For Feishu-resolved runs, the workbook's source ASIN and marketplace are blocking. The target ASIN and target upload date come from the matched tracking row. For a manual fallback run with no tracking row, ASIN, Listing first-upload time, and marketplace remain blocking.

### `新品基础配置`

Fixed headers: `产品尺寸参数`、`产品包装参数`、`包含配件/组件`、`卖点`.

### `竞品对标ASIN`

Fixed headers: `价格竞品`、`颜色竞品`、`尺寸竞品`、`材质竞品`、`风格竞品`.

Competitors provide context only and never become target position rows.

## Advertising input sheet

The matched row's `测试广告信息` reference must resolve to a Feishu Sheet whose first data row contains these exact headers in order:

1. `广告活动名称`
2. `广告类型`
3. `关键词`
4. `CPC`

Select the only visible grid containing the required headers. A name such as `广告信息` or `Sheet1` is allowed; never choose a tab by index alone.

- `广告活动名称`: required, preserved exactly.
- `广告类型`: `精准`/`EXACT` or `自动`/`AUTO`, normalized to `精准` or `自动`.
- `关键词`: required for exact rows; optional for automatic rows.
- `CPC`: positive numeric configured bid, stored as `input_bid_cpc`.

Do not interpret the input CPC as Lingxing actual CPC.

## Output filename

`<TARGET_ASIN>_<YYYYMMDD>.xlsx`

Example: `B0HK3MFZ5S_20260921.xlsx`. Do not add a descriptive prefix or time-of-day suffix unless the user explicitly requests it.

## Fixed output worksheets

1. `验证结果`
2. `验证配置`
3. `运行记录`
4. `精准词运行快照`
5. `关键词首次自然位`
6. `自动扩词快照`
7. `字段字典`

## `验证结果`

Formula-driven latest summary with these blocks:

1. identity: input ASIN, parent ASIN, Listing upload time, latest run ID, latest capture time, actual-CPC report period;
2. KPIs: exact input rows, exact keywords with organic position, first-organic events, exact keywords with advertising position, automatic expansion terms;
3. latest exact-keyword table: keyword, campaign, input bid CPC, period actual CPC, first organic time, current organic page/row, current ad page/row, capture time and status;
4. latest automatic-term table: campaign, input bid CPC, expansion term, first detected time and capture time.

## `验证配置`

Configuration block fields:

1. `Listing输入文件`
2. `广告输入文件`
3. `输入ASIN`
4. `站点`
5. `站点时区`
6. `Listing首次上传时间`
7. `父ASIN`
8. `父ASIN匹配来源`
9. `Listing版本ID`
10. `实际CPC开始日期`
11. `实际CPC结束日期`
12. `请求天数`
13. `范围确认`

For Feishu-resolved runs:

- `Listing输入文件` records the `输入文档` display name and source token or URL;
- `广告输入文件` records the resolved `测试广告信息` sheet title and token or URL;
- `输入ASIN` is the tracking-sheet target ASIN, not a different source ASIN inside the product workbook;
- `Listing首次上传时间` comes from the tracking row's `第1天上传时间`; preserve date-only precision and do not invent a clock time.

Advertising-plan table headers:

`广告活动名称`, `广告类型`, `关键词`, `设置CPC`, `是否启用`, `规范化结果`, `备注`

## `运行记录`

One row per invocation. Fixed fields:

1. `run_id`
2. `开始时间`
3. `完成时间`
4. `运行状态`
5. `领星ASIN状态`
6. `领星精准词状态`
7. `领星自动扩词状态`
8. `SIF状态`
9. `Listing首次上传时间`
10. `实际CPC开始日期`
11. `实际CPC结束日期`
12. `精准输入行数`
13. `精准快照行数`
14. `自动扩词行数`
15. `备注`

Generate a unique `RUN-<YYYYMMDD-HHMMSS>-<suffix>` value.

## `精准词运行快照`

Append-only. Unique grain:

`run_id + parent_asin + campaign_name + normalized keyword + input_bid_cpc`

Fixed fields:

1. `run_id`
2. `captured_at_beijing`
3. `captured_at_marketplace`
4. `listing_version_id`
5. `parent_asin`
6. `campaign_name`
7. `keyword`
8. `input_bid_cpc`
9. `cpc_period_start`
10. `cpc_period_end`
11. `exact_clicks`
12. `exact_spend`
13. `actual_cpc`
14. `organic_ranked_asin`
15. `organic_rank`
16. `organic_page`
17. `organic_row`
18. `ad_ranked_asin`
19. `ad_rank`
20. `ad_page`
21. `ad_row`
22. `organic_visible`
23. `ad_visible`
24. `scan_depth`
25. `sif_status`
26. `lingxing_status`
27. `ad_position_attribution`
28. `quality_flag`

## `关键词首次自然位`

Append-only, immutable event table. Unique event identity:

`listing_version_id + parent_asin + normalized keyword`

Fixed fields:

1. `listing_version_id`
2. `parent_asin`
3. `keyword`
4. `listing_upload_at`
5. `first_detected_at`
6. `first_run_id`
7. `first_ranked_asin`
8. `first_organic_rank`
9. `first_organic_page`
10. `first_organic_row`
11. `hours_to_first_rank`
12. `input_bid_cpc_at_first_seen`
13. `actual_cpc_at_first_seen`
14. `ad_page_at_first_seen`
15. `ad_row_at_first_seen`
16. `scan_depth`
17. `detection_note`

## `自动扩词快照`

Append-only. Unique grain:

`run_id + parent_asin + campaign_name + input_bid_cpc + normalized search_term`

Fixed fields:

1. `run_id`
2. `captured_at_beijing`
3. `captured_at_marketplace`
4. `listing_version_id`
5. `parent_asin`
6. `campaign_name`
7. `input_bid_cpc`
8. `search_term`
9. `cpc_period_start`
10. `cpc_period_end`
11. `first_detected_at`
12. `is_new_term`
13. `data_source`
14. `lingxing_status`
15. `quality_flag`

When a successful report contains no term, retain one placeholder row with blank `search_term` and `quality_flag=未发现扩词`.

## `字段字典`

Fixed columns:

`模块`, `字段/规则`, `中文含义`, `来源`, `计算/处理`, `粒度`, `空值条件`, `限制`

## Updating an existing output

- Accept only a workbook that already matches v3.
- Before starting, scan all keyword-detection cells in the same matched Feishu row and select the newest valid v3 workbook whose `验证配置.输入ASIN` matches the target ASIN. Never use a `listing检测` workbook as the baseline.
- Update a copy, never the user's only file.
- Append one run record for every attempt.
- Append exact and automatic snapshots by run.
- Never edit or delete a first-organic event.
- Recalculate the current summary from the latest successful run.
- Resolve the current run date in the user's timezone as `YYYY-MM-DD`. Reuse the rightmost exact adjacent `<YYYY-MM-DD>listing检测` / `<YYYY-MM-DD>关键词检测` pair for that run date whose matched-row keyword cell is blank. If none exists, append that exact date-specific pair, leave the new Listing column blank, and write the verified copy only to the matched-row keyword cell.
- Never overwrite an earlier keyword attachment or alter a paired Listing attachment. Completion requires header, filename, token, paired-cell, and source-row readback.
