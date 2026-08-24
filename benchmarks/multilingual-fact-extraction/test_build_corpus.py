#!/usr/bin/env python3
"""Contract tests for the six-tier multilingual corpus builder."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("build_corpus", ROOT / "build_corpus.py")
assert SPEC and SPEC.loader
build_corpus = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = build_corpus
SPEC.loader.exec_module(build_corpus)


def encoded(row: dict) -> bytes:
    return (json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


def english_row(index: int, note: str | None = None) -> dict:
    return {
        "id": f"en-{index}",
        "note": note or f"File {index} is in docs/{index}.",
        "gold": [{"subject": f"File {index}", "relation": "located_in", "object": f"docs/{index}"}],
    }


def multilingual_row(index: int, language: str) -> dict:
    return {
        "id": f"ml-{index}",
        "language": language,
        "note": f"Datei {index}.md befindet sich in docs/{index}.",
        "gold": [{"subject": f"{index}.md", "relation": "located_in", "object": f"docs/{index}"}],
        "source": {
            "repo": "example/docs-de",
            "url": "https://github.com/example/docs-de.git",
            "sha": "a" * 40,
            "paths": [f"docs/{index}/{index}.md"],
        },
        "provenance": "generated-from-open-source",
    }


class CorpusBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="multilingual-corpus-test-")
        self.root = Path(self.temp.name)
        self.english_rows = [english_row(i) for i in range(4)]
        self.english_paths = []
        for name, count in (("one", 2), ("three", 3), ("ten", 4)):
            path = self.root / f"gold_{name}.jsonl"
            path.write_bytes(b"".join(encoded(row) for row in self.english_rows[:count]))
            self.english_paths.append(path)
        pool = [
            multilingual_row(index, language)
            for index, language in enumerate(build_corpus.NON_ENGLISH_LANGUAGES[:4])
        ]
        self.pool_path = self.root / "multilingual.jsonl"
        self.pool_path.write_bytes(b"".join(encoded(row) for row in pool))
        self.output_dir = self.root / "generated"
        self.config_path = self.root / "plan.json"
        self.config_path.write_text(json.dumps({
            "schema_version": 1,
            "language_set": "eurobert-15",
            "multilingual_pool": self.pool_path.name,
            "output_dir": self.output_dir.name,
            "tiers": [
                {"name": "small", "target_count": 3, "english_path": self.english_paths[0].name, "english_output": "one.jsonl", "expanded_output": "two.jsonl"},
                {"name": "mid", "target_count": 5, "english_path": self.english_paths[1].name, "english_output": "three.jsonl", "expanded_output": "five.jsonl"},
                {"name": "large", "target_count": 8, "english_path": self.english_paths[2].name, "english_output": "ten.jsonl", "expanded_output": "twenty.jsonl"},
            ],
        }), encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def build(self) -> build_corpus.Plan:
        plan = build_corpus.load_plan(self.config_path)
        outputs, _ = build_corpus.derive(plan)
        build_corpus.write_outputs(plan.output_dir, outputs)
        return plan

    def ids(self, name: str) -> set[str]:
        return {
            json.loads(line)["id"]
            for line in (self.output_dir / name).read_text(encoding="utf-8").splitlines()
        }

    def test_builds_all_six_exact_counts(self) -> None:
        self.build()
        names = ("one.jsonl", "two.jsonl", "three.jsonl", "five.jsonl", "ten.jsonl", "twenty.jsonl")
        counts = [len((self.output_dir / name).read_text().splitlines()) for name in names]
        self.assertEqual(counts, [2, 3, 3, 5, 4, 8])

    def test_english_outputs_are_byte_identical_to_sources(self) -> None:
        self.build()
        for source, output in zip(self.english_paths, ("one.jsonl", "three.jsonl", "ten.jsonl")):
            self.assertEqual(source.read_bytes(), (self.output_dir / output).read_bytes())

    def test_expanded_tiers_are_nested(self) -> None:
        self.build()
        self.assertLessEqual(self.ids("two.jsonl"), self.ids("five.jsonl"))
        self.assertLessEqual(self.ids("five.jsonl"), self.ids("twenty.jsonl"))

    def test_rebuild_ingests_an_english_update(self) -> None:
        self.build()
        self.english_rows[0] = english_row(0, "File zero is now in docs/zero.")
        for path, count in zip(self.english_paths, (2, 3, 4)):
            path.write_bytes(b"".join(encoded(row) for row in self.english_rows[:count]))
        self.build()
        for output in ("one.jsonl", "two.jsonl", "three.jsonl", "five.jsonl", "ten.jsonl", "twenty.jsonl"):
            first = json.loads((self.output_dir / output).read_text().splitlines()[0])
            self.assertEqual(first["note"], "File zero is now in docs/zero.")

    def test_rejects_a_language_outside_eurobert_15(self) -> None:
        rows = [json.loads(line) for line in self.pool_path.read_text().splitlines()]
        rows[0]["language"] = "sv"
        self.pool_path.write_bytes(b"".join(encoded(row) for row in rows))
        with self.assertRaisesRegex(build_corpus.CorpusError, "unsupported language"):
            build_corpus.derive(build_corpus.load_plan(self.config_path))

    def test_validate_detects_modified_output(self) -> None:
        plan = self.build()
        expected, _ = build_corpus.derive(plan)
        with (plan.output_dir / "two.jsonl").open("ab") as handle:
            handle.write(b"{}\n")
        with self.assertRaisesRegex(build_corpus.CorpusError, "stale or modified"):
            build_corpus.validate_outputs(plan.output_dir, expected)


if __name__ == "__main__":
    unittest.main()
