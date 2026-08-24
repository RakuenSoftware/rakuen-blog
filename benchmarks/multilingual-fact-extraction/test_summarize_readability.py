#!/usr/bin/env python3
"""Tests for overall and per-language readability reporting."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "summarize_readability", ROOT / "summarize_readability.py"
)
assert SPEC and SPEC.loader
readability = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = readability
SPEC.loader.exec_module(readability)


def gold(row_id: str, language: str | None = None) -> dict:
    row = {"id": row_id, "note": "note", "gold": []}
    if language:
        row["language"] = language
    return row


def pred(
    row_id: str,
    *,
    parse_ok: bool,
    raw: str,
    error: str | None = None,
    truncated: bool = False,
) -> dict:
    return {
        "id": row_id,
        "parse_ok": parse_ok,
        "raw": raw,
        "error": error,
        "truncated": truncated,
    }


class ReadabilityTests(unittest.TestCase):
    def test_reports_weighted_overall_and_per_language_rates(self) -> None:
        report = readability.summarize(
            [gold("en-1"), gold("en-2"), gold("fr-1", "fr"), gold("fr-2", "fr")],
            [
                pred("en-1", parse_ok=True, raw='{"facts":[]}'),
                pred("en-2", parse_ok=True, raw="{}"),
                pred("fr-1", parse_ok=True, raw='{"facts":[]}'),
                pred("fr-2", parse_ok=False, raw="not json"),
            ],
        )
        self.assertEqual(report["overall"]["json_parse_rate"], 0.75)
        self.assertEqual(report["by_language"]["en"]["json_parse_rate"], 1.0)
        self.assertEqual(report["by_language"]["fr"]["json_parse_rate"], 0.5)
        self.assertEqual(report["macro_json_parse_rate"], 0.75)
        self.assertEqual(report["macro_schema_rate"], 0.75)
        self.assertEqual(report["by_language"]["fr"]["schema_failures"], 1)

    def test_empty_json_is_a_valid_terse_abstention(self) -> None:
        report = readability.summarize(
            [gold("en-1")], [pred("en-1", parse_ok=True, raw="[]")]
        )
        self.assertEqual(report["overall"]["schema_rate"], 1.0)

    def test_marks_transport_and_truncation_as_invalid_for_scoring(self) -> None:
        report = readability.summarize(
            [gold("en-1"), gold("fr-1", "fr")],
            [
                pred("en-1", parse_ok=False, raw="", error="timeout"),
                pred("fr-1", parse_ok=False, raw="", truncated=True),
            ],
        )
        self.assertFalse(report["overall"]["valid_for_scoring"])
        self.assertEqual(report["overall"]["transport_errors"], 1)
        self.assertEqual(report["overall"]["truncated_rows"], 1)

    def test_rejects_incomplete_prediction_sets(self) -> None:
        with self.assertRaisesRegex(readability.ReadabilityError, "missing prediction"):
            readability.summarize([gold("en-1"), gold("fr-1", "fr")], [
                pred("en-1", parse_ok=True, raw="{}")
            ])

    def test_rejects_missing_parse_metadata(self) -> None:
        with self.assertRaisesRegex(readability.ReadabilityError, "boolean parse_ok"):
            readability.summarize(
                [gold("en-1")], [{"id": "en-1", "raw": "{}"}]
            )


if __name__ == "__main__":
    unittest.main()
