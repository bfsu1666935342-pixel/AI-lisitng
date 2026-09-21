#!/usr/bin/env python3
"""Create a stable record ID for one atomic Alexa validation fact."""

from __future__ import annotations

import argparse
import hashlib
import re
import unicodedata


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold().strip()
    chars: list[str] = []
    for char in value:
        category = unicodedata.category(char)
        chars.append(" " if category.startswith(("P", "Z")) else char)
    return re.sub(r"\s+", " ", "".join(chars)).strip()


def make_record_id(asin: str, market: str, source_sheet: str, source_field: str, fact: str) -> str:
    identity = "|".join(normalize(part) for part in (asin, market, source_sheet, source_field, fact))
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16].upper()
    return f"ALI-{digest}"


def make_pain_point_record_id(
    asin: str, market: str, category: str, pain_point_id: str, pain_point: str
) -> str:
    identity = "|".join(
        normalize(part) for part in (asin, market, category, pain_point_id, pain_point)
    )
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16].upper()
    return f"PNT-{digest}"


def require_args(parser: argparse.ArgumentParser, args: argparse.Namespace, names: tuple[str, ...]) -> None:
    missing = [f"--{name.replace('_', '-')}" for name in names if not getattr(args, name)]
    if missing:
        parser.error(f"record type {args.record_type!r} requires: {', '.join(missing)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asin", required=True)
    parser.add_argument("--market", required=True)
    parser.add_argument("--record-type", choices=("tag", "pain-point"), default="tag")
    parser.add_argument("--source-sheet")
    parser.add_argument("--source-field")
    parser.add_argument("--fact")
    parser.add_argument("--category")
    parser.add_argument("--pain-point-id")
    parser.add_argument("--pain-point")
    args = parser.parse_args()
    if args.record_type == "tag":
        require_args(parser, args, ("source_sheet", "source_field", "fact"))
        print(make_record_id(args.asin, args.market, args.source_sheet, args.source_field, args.fact))
    else:
        require_args(parser, args, ("category", "pain_point_id", "pain_point"))
        print(
            make_pain_point_record_id(
                args.asin, args.market, args.category, args.pain_point_id, args.pain_point
            )
        )


if __name__ == "__main__":
    main()
