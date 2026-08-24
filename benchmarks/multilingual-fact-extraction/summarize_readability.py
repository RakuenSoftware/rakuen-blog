#!/usr/bin/env python3
"""Report JSON readability and schema validity overall and by language."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


EUROBERT_LANGUAGES = (
    "en",
    "fr",
    "de",
    "es",
    "zh",
    "it",
    "ru",
    "pl",
    "pt",
    "ja",
    "vi",
    "nl",
    "ar",
    "tr",
    "hi",
)


class ReadabilityError(ValueError):
    """Gold or prediction rows cannot produce a valid readability report."""


def load_rows(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise ReadabilityError(f"input does not exist: {path}") from exc
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for number, line in enumerate(lines, 1):
        if not line.strip():
            raise ReadabilityError(f"blank JSONL row at {path}:{number}")
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ReadabilityError(f"invalid JSON at {path}:{number}: {exc}") from exc
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise ReadabilityError(f"row at {path}:{number} needs a string id")
        if row["id"] in seen:
            raise ReadabilityError(f"duplicate id {row['id']!r} in {path}")
        seen.add(row["id"])
        rows.append(row)
    return rows


def derive_schema_ok(row: dict[str, Any]) -> bool:
    """Match the existing scorer's definition of a readable response shape.

    Empty JSON objects and arrays are terse abstentions and therefore valid.
    Content in any other shape is a schema failure even when it is valid JSON.
    """
    raw = (row.get("raw") or "").strip()
    if raw in ("{}", "[]", "{ }", "[ ]", ""):
        return True
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end < start:
        return False
    try:
        value = json.loads(raw[start : end + 1])
    except json.JSONDecodeError:
        return False
    if isinstance(value, dict) and isinstance(value.get("facts"), list):
        return True
    return isinstance(value, dict) and not value


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    count = len(rows)
    parsed = sum(bool(row.get("parse_ok")) for row in rows)
    schema = sum(derive_schema_ok(row) for row in rows)
    errors = sum(bool(row.get("error")) for row in rows)
    truncated = sum(bool(row.get("truncated")) for row in rows)
    return {
        "notes": count,
        "json_parse_ok": parsed,
        "json_parse_rate": round(parsed / count, 4) if count else None,
        "json_parse_failures": count - parsed,
        "schema_ok": schema,
        "schema_rate": round(schema / count, 4) if count else None,
        "schema_failures": count - schema,
        "transport_errors": errors,
        "truncated_rows": truncated,
        "valid_for_scoring": errors == 0 and truncated == 0,
    }


def summarize(
    gold_rows: list[dict[str, Any]], pred_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    gold_by_id = {row["id"]: row for row in gold_rows}
    pred_by_id = {row["id"]: row for row in pred_rows}
    if set(gold_by_id) != set(pred_by_id):
        missing = sorted(set(gold_by_id) - set(pred_by_id))
        extra = sorted(set(pred_by_id) - set(gold_by_id))
        detail = []
        if missing:
            detail.append(f"missing prediction {missing[0]!r}")
        if extra:
            detail.append(f"unknown prediction {extra[0]!r}")
        raise ReadabilityError("prediction IDs do not match gold: " + "; ".join(detail))

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    ordered_predictions: list[dict[str, Any]] = []
    for gold in gold_rows:
        language = gold.get("language", "en")
        if language not in EUROBERT_LANGUAGES:
            raise ReadabilityError(
                f"gold row {gold['id']!r} has language outside EuroBERT-15: {language!r}"
            )
        prediction = pred_by_id[gold["id"]]
        if not isinstance(prediction.get("parse_ok"), bool):
            raise ReadabilityError(
                f"prediction {gold['id']!r} needs a boolean parse_ok field"
            )
        if not isinstance(prediction.get("raw"), str):
            raise ReadabilityError(
                f"prediction {gold['id']!r} needs a string raw field"
            )
        grouped[language].append(prediction)
        ordered_predictions.append(prediction)

    by_language = {
        language: _summary(grouped.get(language, []))
        for language in EUROBERT_LANGUAGES
    }
    observed_parse_rates = [
        summary["json_parse_rate"]
        for summary in by_language.values()
        if summary["notes"]
    ]
    observed_schema_rates = [
        summary["schema_rate"]
        for summary in by_language.values()
        if summary["notes"]
    ]
    report = {
        "language_set": "eurobert-15",
        "overall": _summary(ordered_predictions),
        "by_language": by_language,
        "macro_json_parse_rate": (
            round(sum(observed_parse_rates) / len(observed_parse_rates), 4)
            if observed_parse_rates
            else None
        ),
        "macro_schema_rate": (
            round(sum(observed_schema_rates) / len(observed_schema_rates), 4)
            if observed_schema_rates
            else None
        ),
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", required=True, type=Path)
    parser.add_argument("--pred", required=True, type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args(argv)
    try:
        report = summarize(load_rows(args.gold), load_rows(args.pred))
    except ReadabilityError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
