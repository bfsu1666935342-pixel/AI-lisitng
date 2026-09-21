# Alexa Shopping runbook

## Marketplace defaults

| Market | Amazon front end | Question language | Locale note |
| --- | --- | --- | --- |
| Amazon-US | amazon.com | English | Use the active US delivery location visible in the session; record it in the summary when available. |
| Amazon-DE | amazon.de | German | Use the active German delivery location visible in the session; record it in the summary when available. |

Do not silently switch marketplace, language, device context, or delivery location during one run.

## Browser procedure

1. Open the target ASIN on the selected Amazon marketplace.
2. Confirm the visible ASIN and product identity match the input.
3. Open the Amazon front-end Alexa Shopping assistant available in that session.
4. If login is required, pause and ask the user to log in. Never ask for credentials.
5. Create one `运行ID` and one observation timestamp for the run.
6. Ask the neutral questions for each atomic Listing fact.
7. Ask one pain-point question for each enabled, matching entry in the category pain-point library. Skip this block when the library is empty or unmatched; do not invent replacement pain points.
8. Capture the answer text and evidence reference immediately after each answer.
9. Append the appropriate history row for every attempt, including failures.
10. Stop on CAPTCHA, verification, blocked access, or repeated assistant failure and report the concrete blocker.

## Neutral question patterns

Adapt wording to the marketplace language. Replace `<ASIN or product>` with the visible target and avoid embedding the expected value.

| Category | English pattern | German pattern |
| --- | --- | --- |
| 产品类型 | What type of product is `<ASIN or product>`? | Um welche Art von Produkt handelt es sich bei `<ASIN or product>`? |
| 产品人群画像 | Who is `<ASIN or product>` intended or suitable for? | Für wen ist `<ASIN or product>` gedacht oder geeignet? |
| 使用场景 | In what situations or environments can `<ASIN or product>` be used? | In welchen Situationen oder Umgebungen kann `<ASIN or product>` verwendet werden? |
| 用途 | What is `<ASIN or product>` designed to be used for? | Wofür ist `<ASIN or product>` vorgesehen? |
| 核心卖点/卖点 | What are the main features and benefits of `<ASIN or product>`? | Was sind die wichtigsten Eigenschaften und Vorteile von `<ASIN or product>`? |
| 产品尺寸参数 | What are the product dimensions and relevant specifications of `<ASIN or product>`? | Welche Produktabmessungen und relevanten Spezifikationen hat `<ASIN or product>`? |
| 产品包装参数 | What are the package dimensions, package weight, and package quantity for `<ASIN or product>`? | Welche Verpackungsmaße, welches Verpackungsgewicht und welche Packungsmenge hat `<ASIN or product>`? |
| 包含配件/组件 | What accessories or components are included with `<ASIN or product>`? | Welches Zubehör oder welche Komponenten sind bei `<ASIN or product>` enthalten? |

## Category pain-point question

Use the exact enabled pain-point wording from the library. The pain point must appear in this question because it is the subject being tested; do not add an expected answer or an assumed product feature.

| Language | Fixed pattern |
| --- | --- |
| English | Does `<ASIN or product>` help solve or reduce the problem of `<pain point>`? What product feature or capability supports your answer? |
| German | Hilft `<ASIN or product>` dabei, das Problem `<pain point>` zu lösen oder zu mindern? Welche Produkteigenschaft oder Fähigkeit stützt deine Antwort? |

For a marketplace with another language, translate the fixed intent faithfully and record the language/locale. Do not replace the library pain point with a broader or adjacent concern.

These are starting patterns. When several facts share one Alexa answer, reuse the same evidence but judge each atomic row independently.

## Rephrase limit

- Ask the standard neutral question once.
- If the response is ambiguous, ask one narrower but still non-leading rephrase.
- Do not state the expected value, offer multiple-choice answers, or repeatedly prompt until Alexa agrees.
- If both successful answers omit the fact, judge `否`.
- If the answers conflict with each other, mark the run `需要人工复核` for the affected item.
- For pain-point questions, if both successful answers remain noncommittal or omit the feature-to-pain-point link, judge `不明确`, not `否`.

## Evidence

Preferred evidence order:

1. Stable assistant conversation URL or evidence ID.
2. Screenshot reference tied to the run and item.
3. Saved transcript reference.

Evidence should show the question, answer, marketplace context, and timestamp when possible. Never use the expected input itself as evidence of Alexa capture.
