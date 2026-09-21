# Decomposition and judgment guide

## General rule

An atomic fact must be independently askable and independently judgeable as `是`、`否`、`不一致`. Split conservatively. Do not create extra rows from decorative adjectives, repeated wording, or facts that Alexa would naturally answer only as one relationship.

Preserve the original source phrase in `输入内容（期望）`. Normalization is used only to identify duplicates and build `记录ID`.

## Decomposition by category

### 产品类型

- Usually one row for the primary product identity.
- Split only when the source intentionally claims multiple independently meaningful product types.
- Do not turn style, material, or audience modifiers into product types.

Example: `inflatable stand up paddle board` remains one product-type fact.

### 产品人群画像

- Create one row per independently identifiable audience group.
- Keep modifiers with the group: `初学者女性` is one audience, not `初学者` plus `女性`, unless both are separately claimed.
- Split coordinated groups when each can be answered separately: `初学者和家庭用户` becomes two rows.
- Keep a composite persona together when splitting changes its meaning: `带孩子出行的家庭` remains one row.

### 使用场景

- One row per independently recognizable setting, location, time, or activity context.
- Split lists such as `湖泊、平静海湾和慢速河流` into separate rows.
- Keep necessary qualifiers together: `平静水域瑜伽` is one scenario if the intended claim is specifically yoga in calm water.

### 用途

- One row per distinct job or intended outcome.
- Examples: leisure paddling, fishing, yoga, touring, family recreation.
- Do not split a feature from the purpose it enables unless both are independently claimed elsewhere.

### 核心卖点 and 卖点

- One row per claim that could independently be true or false.
- Keep a feature and its stated benefit together when the relationship is the claim: `加宽甲板，提高初学者稳定性` stays one row.
- Split unrelated claims joined by punctuation or conjunctions: `轻量便携，并配有防滑甲板` becomes two rows.
- Preserve explicit thresholds, capacities, quantities, materials, certifications, and comparative qualifiers.
- Do not merge duplicate-looking rows across `核心卖点` and `卖点`; preserve source lineage. Flag exact semantic duplicates in `备注` if useful.
- Marketing superlatives without a verifiable referent, such as `最佳` or `终极`, should not become independent facts. Retain them only when part of a concrete claim and note that the superlative itself is not evidence.

### 产品尺寸参数

- One named measurement per row: length, width, height/thickness, weight, capacity, or another explicit specification.
- A standard dimension tuple such as `10'6" × 32" × 6"` may remain one row only when labels or order are clear and Alexa is expected to state the tuple together. Otherwise split by named dimension.
- Preserve numbers and units. Accept mathematically equivalent unit conversions only after checking the conversion.

### 产品包装参数

- Separate package dimensions, package weight, package quantity, and packing method.
- Never compare a package measurement with a product measurement.
- Keep an `L × W × H` package tuple together when clearly labeled as package size.

### 包含配件/组件

- One row per component and quantity.
- `桨、手泵、背包和3个鳍片` becomes four rows; the fin row retains quantity `3`.
- A bundled assembly that is sold as one named component can remain one row.

## Normalization for identity

Before producing a deterministic `记录ID`:

1. Trim leading and trailing whitespace.
2. Collapse repeated spaces and line breaks.
3. Normalize full-width/half-width punctuation and case where appropriate.
4. Preserve numbers, units, negation, quantities, and comparative qualifiers.
5. Do not translate the fact merely to create the identity key.

Material wording changes create a new fact and therefore a new `记录ID`. Punctuation-only or whitespace-only changes should retain the prior ID.

## Judgment standard

### 是

Use `是` only when Alexa's answer communicates the same material fact.

- Paraphrases and synonyms are acceptable.
- A valid unit conversion is acceptable when the values match within ordinary rounding.
- All material quantities and qualifiers must match.
- The answer may be more concise than the input but cannot drop a qualifier that changes the claim.

### 否

Use `否` when Alexa responds successfully but does not state or support the atomic fact.

- General product praise is not capture evidence.
- Mentioning an adjacent fact is not capture evidence.
- Silence after a successful, relevant response is `否`.
- Do not use `否` for page errors, login blocks, timeouts, CAPTCHA, or unavailable Alexa features.

### 不一致

Use `不一致` when Alexa addresses the same fact but conflicts materially.

- Different number, dimension, quantity, or capacity.
- Different included component.
- Different audience, use, or scenario meaning.
- Missing or altered qualifier that reverses or materially narrows/broadens the claim.

Write `不一致说明` as: `输入：<expected>；Alexa：<observed>；差异：<specific conflict>`.

### Needs review

When the answer is too ambiguous to distinguish omission from contradiction, record the history run as `需要人工复核`. Do not force a content judgment. Ask the user only if the ambiguity changes the final result materially.

## Repeat-run expression comparison

Compare only the same `记录ID` across the current run and its immediately preceding run. Expression quality is evaluated only when both adjacent runs succeeded and both were judged `是`. It measures how well Alexa explains an already-correct fact; it does not absorb correctness changes. A failed or empty adjacent run produces `无法比较` and must not be skipped in favor of an older run.

Allowed values:

- `更好`: both answers are correct, and the current wording adds materially useful mechanism, reason, relationship, qualifier, specificity, or clarity. Example: the prior answer only says `人体工学`, while the current answer correctly explains how the shape or support aligns the wrist or reduces strain.
- `持平`: both answers are correct and have no material difference in useful detail, specificity, qualifier retention, or clarity.
- `更差`: both answers remain correct, but the current wording loses useful detail, specificity, a material qualifier, or clarity.
- `无法比较`: either answer lacks comparable content, the prior/current attempt failed, or the meanings are not aligned enough for a fair comparison.
- `不适用`: no preceding run exists, or one or both completed judgments are not `是`.

More words alone are not an improvement. The added wording must help a shopper understand how, why, under what condition, or to what extent the correct fact applies. Explain the specific difference in `表达对比说明`; do not write only the label.

## Correctness regression

Judge correctness regression independently from expression quality, always against the immediately preceding run for the same `记录ID`.

- `是`: the previous successful judgment was `是`, and the current successful judgment is `否` or `不一致`.
- `否`: the previous successful judgment was `是`, and the current successful judgment remains `是`.
- `无法判断`: the previous successful judgment was `是`, but the current attempt failed or requires human review.
- `不适用`: no previous run exists, or the previous completed judgment was not `是`.

When `正确性回退=是`, write `回退说明` with the prior correct meaning and the current omission or conflict. Do not call a correctness regression `更差`; set expression comparison to `不适用` because both runs are not correct.
