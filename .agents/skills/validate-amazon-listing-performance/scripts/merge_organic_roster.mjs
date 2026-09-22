// One row per normalized keyword. Caller supplies directly observed page/row only.
export function normalizeKeyword(value) {
  return String(value ?? "").trim().replace(/\s+/g, " ").toLowerCase();
}

export function naturalPosition(page, row) {
  if (!Number.isInteger(page) || page < 1 || page > 3 || !Number.isInteger(row) || row < 1) {
    throw new Error(`Invalid directly observed organic page/row: ${page}/${row}`);
  }
  return `第${page}页第${row}位`;
}

// existing: [{keyword, firstTime, firstPosition, currentTime, currentPosition}]
// observed: [{keyword, page, row, firstTime?, firstPosition?}]
export function mergeOrganicRoster(existing, observed, capturedAt, { complete }) {
  if (!capturedAt || typeof capturedAt !== "string") throw new Error("Actual capture time is required");
  const rows = existing.map((r) => ({ ...r }));
  const index = new Map();
  for (const [i, r] of rows.entries()) {
    const key = normalizeKeyword(r.keyword);
    if (!key || index.has(key)) throw new Error(`Blank or duplicate existing keyword: ${r.keyword}`);
    if (!r.firstTime || !r.firstPosition) throw new Error(`Missing immutable first pair: ${r.keyword}`);
    index.set(key, i);
  }
  const seen = new Set();
  for (const item of observed) {
    const key = normalizeKeyword(item.keyword);
    if (!key) throw new Error("Blank observed keyword");
    const position = naturalPosition(item.page, item.row);
    if (seen.has(key)) throw new Error(`Observation must be deduplicated before roster merge: ${item.keyword}`);
    seen.add(key);
    const i = index.get(key);
    if (i === undefined) {
      rows.push({
        keyword: item.keyword,
        firstTime: item.firstTime || capturedAt,
        firstPosition: item.firstPosition || position,
        currentTime: capturedAt,
        currentPosition: position,
      });
      index.set(key, rows.length - 1);
    } else {
      // Only the current pair changes for an existing row.
      rows[i].currentTime = capturedAt;
      rows[i].currentPosition = position;
    }
  }
  if (complete) {
    for (const row of rows) {
      if (seen.has(normalizeKeyword(row.keyword))) continue;
      row.currentTime = capturedAt;
      row.currentPosition = "无自然位";
    }
  }
  return rows;
}
