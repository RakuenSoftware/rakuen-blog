#!/usr/bin/env python3

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("generate_corpus", ROOT / "generate_corpus.py")
assert SPEC and SPEC.loader
generate_corpus = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generate_corpus)

BENCH_SPEC = importlib.util.spec_from_file_location(
    "long_session_bench", ROOT / "long_session_bench.py"
)
assert BENCH_SPEC and BENCH_SPEC.loader
long_session_bench = importlib.util.module_from_spec(BENCH_SPEC)
BENCH_SPEC.loader.exec_module(long_session_bench)


class GenerateCorpusTests(unittest.TestCase):
    def test_conversation_shape_and_nested_checkpoints(self):
        item = generate_corpus.build_conversation(1)
        self.assertEqual(item["id"], "LSC-001")
        self.assertEqual(len(item["probes"]), 20)
        checkpoints = [probe["checkpoint_tokens"] for probe in item["probes"]]
        self.assertEqual(checkpoints, [value for value in generate_corpus.CHECKPOINTS for _ in range(4)])
        positions = {turn["id"]: index for index, turn in enumerate(item["turns"])}
        prefixes = [positions[probe["after_turn_id"]] for probe in item["probes"]]
        self.assertEqual(prefixes, sorted(prefixes))

    def test_generation_is_byte_deterministic(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_path = Path(first)
            second_path = Path(second)
            generate_corpus.generate(first_path / "corpus.jsonl", first_path / "manifest.json")
            generate_corpus.generate(second_path / "corpus.jsonl", second_path / "manifest.json")
            self.assertEqual(
                (first_path / "corpus.jsonl").read_bytes(),
                (second_path / "corpus.jsonl").read_bytes(),
            )
            self.assertEqual(
                (first_path / "manifest.json").read_bytes(),
                (second_path / "manifest.json").read_bytes(),
            )

    def test_generated_corpus_validates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            corpus = root / "conversations.jsonl"
            manifest = root / "manifest.json"
            generate_corpus.generate(corpus, manifest)
            summary = long_session_bench.validate(corpus, manifest)
            self.assertEqual(summary["conversation_count"], 100)
            self.assertEqual(summary["probe_count"], 2000)


if __name__ == "__main__":
    unittest.main()

