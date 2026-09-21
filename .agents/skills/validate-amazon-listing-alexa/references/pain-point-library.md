# Category pain-point library

## Library schema

Use a workbook containing a sheet named `品类痛点库` with these fixed columns:

`痛点ID | 市场 | 品类 | 痛点 | 痛点库版本 | 是否启用 | 备注`

- `痛点ID` must be stable and unique within the library.
- `市场` uses the Listing market, normally `Amazon-US` or `Amazon-DE`. A row with `全部` may match either market.
- `品类` must match the product category after conservative normalization. Do not use a merely adjacent category.
- `痛点` is the exact shopper problem to ask about. Preserve its wording in output snapshots.
- `痛点库版本` identifies the source version used for the run. Do not invent a version.
- `是否启用` must equal `是` for the row to be queried.

The bundled template may contain only headers. A missing, empty, or unmatched library is a valid state, not a failed Alexa run.

## Selection

1. Filter to `是否启用=是`.
2. Match the selected Listing market or `全部`.
3. Match the Listing product category conservatively.
4. Deduplicate by `痛点ID`. If one ID has conflicting active rows, do not choose silently; flag the conflict for review.
5. Create a stable pain-point record ID from `ASIN + market + category + 痛点ID + 痛点`. Use `scripts/make_record_id.py --record-type pain-point` when available.

Do not generate substitute pain points from general knowledge, Listing text, reviews, competitor pages, or Alexa when the library has no eligible row.

## Alexa judgment

Allowed `是否解决` values are `是`、`否`、`不明确`.

- `是`: Alexa explicitly links a product feature, capability, or benefit to solving or materially alleviating the named pain point.
- `否`: Alexa explicitly states the product does not address it or lacks the relevant capability.
- `不明确`: Alexa gives only general praise, omits the causal link, hedges without support, or provides insufficient information to decide.

Record the supporting answer meaning in `Alexa依据`. Do not infer a solution from the Listing, the pain-point library wording, or model knowledge. On CAPTCHA, login block, timeout, or assistant failure, leave `是否解决` blank and append `运行结果=抓取失败` with the concrete error.

## State and history

- `当前痛点结果` keeps the newest successful judgment for one pain-point `记录ID`.
- `痛点询问历史` is append-only and contains every attempt.
- A later library wording change that materially changes the pain point creates a new record ID. A version-only change with identical meaning retains the record ID while the output stores the new `痛点库版本`.
- Removing or disabling a pain point stops new questions but does not delete its history.
