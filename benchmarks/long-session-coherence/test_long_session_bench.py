#!/usr/bin/env python3

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("long_session_bench", ROOT / "long_session_bench.py")
assert SPEC and SPEC.loader
bench = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bench)

GEN_SPEC = importlib.util.spec_from_file_location("generate_corpus", ROOT / "generate_corpus.py")
assert GEN_SPEC and GEN_SPEC.loader
generator = importlib.util.module_from_spec(GEN_SPEC)
GEN_SPEC.loader.exec_module(generator)


def response_for(probe):
    return json.dumps({
        "answer": probe["gold"]["accepted_answers"][0],
        "evidence_turn_ids": probe["gold"]["required_evidence_turn_ids"],
        "confidence": 1.0,
    }, separators=(",", ":"))


class ResponseTests(unittest.TestCase):
    def setUp(self):
        self.conversation = generator.build_conversation(1)
        self.probe = self.conversation["probes"][0]

    def test_correct_response_passes(self):
        result = bench.evaluate_response(response_for(self.probe), self.probe["gold"])
        self.assertTrue(result["passed"])

    def test_parse_and_schema_failures_are_distinct(self):
        parse = bench.evaluate_response("not json", self.probe["gold"])
        schema = bench.evaluate_response('{"answer":"x"}', self.probe["gold"])
        self.assertEqual(parse["failure_reason"], "json_parse_failure")
        self.assertEqual(schema["failure_reason"], "schema_failure")

    def test_wrong_evidence_fails(self):
        payload = json.loads(response_for(self.probe))
        payload["evidence_turn_ids"] = []
        result = bench.evaluate_response(json.dumps(payload), self.probe["gold"])
        self.assertEqual(result["failure_reason"], "wrong_evidence")

    def test_fixed_request_uses_exact_prefix(self):
        request = bench.build_request(self.conversation, "P005")
        probe = self.conversation["probes"][4]
        self.assertEqual(request["messages"][-1]["role"], "user")
        self.assertIn(probe["prompt"], request["messages"][-1]["content"])
        self.assertEqual(request["track"], "fixed_replay")

    def test_fixed_request_exposes_every_evidence_turn_id(self):
        request = bench.build_request(self.conversation, "P005")
        transcript = "\n".join(message["content"] for message in request["messages"][1:-1])
        self.assertTrue(request["messages"][1]["content"].startswith("[T0001] "))
        for turn_id in self.conversation["probes"][4]["gold"]["required_evidence_turn_ids"]:
            self.assertIn(f"[{turn_id}] ", transcript)


class GradeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = [generator.build_conversation(number) for number in range(1, 101)]

    def write_results(self, failures=None):
        failures = failures or {}
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False)
        with handle:
            for conversation in self.corpus:
                fail_at = failures.get(conversation["id"])
                for probe in conversation["probes"]:
                    response = response_for(probe)
                    if fail_at == probe["ordinal"]:
                        response = "not json"
                    handle.write(json.dumps({
                        "conversation_id": conversation["id"],
                        "probe_id": probe["id"],
                        "response": response,
                        "prompt_tokens": probe["estimated_context_tokens"],
                        "prompt_eval_tokens_per_second": 100.0,
                    }) + "\n")
        return Path(handle.name)

    def test_perfect_run_scores_100(self):
        path = self.write_results()
        try:
            report = bench.grade(self.corpus, path)
        finally:
            path.unlink()
        self.assertEqual(report["score"], 100.0)
        self.assertTrue(report["fully_coherent"])
        self.assertEqual(report["retention"]["retention_auc"], 1.0)
        self.assertEqual(
            report["retention"]["degradation_per_context_doubling"], 0.0
        )

    def test_failure_after_60_percent_scores_30_for_conversation(self):
        path = self.write_results({"LSC-001": 13})
        try:
            report = bench.grade(self.corpus, path)
        finally:
            path.unlink()
        first = report["conversations"][0]
        self.assertEqual(first["consecutive_passes"], 12)
        self.assertEqual(first["survival_fraction"], 0.6)
        self.assertEqual(first["score"], 30.0)
        self.assertFalse(report["fully_coherent"])

    def test_no_completed_conversations_can_reach_50(self):
        failures = {conversation["id"]: 20 for conversation in self.corpus}
        path = self.write_results(failures)
        try:
            report = bench.grade(self.corpus, path)
        finally:
            path.unlink()
        self.assertEqual(report["completed_conversations"], 0)
        self.assertEqual(report["score"], 47.5)

    def test_paired_comparison_reports_candidate_minus_baseline(self):
        baseline_path = self.write_results()
        candidate_path = self.write_results({"LSC-001": 13})
        try:
            baseline = bench.grade(self.corpus, baseline_path)
            candidate = bench.grade(self.corpus, candidate_path)
            comparison = bench.compare_reports(baseline, candidate, samples=500)
        finally:
            baseline_path.unlink()
            candidate_path.unlink()
        self.assertLess(comparison["score_delta"], 0)
        self.assertAlmostEqual(
            comparison["score_delta"],
            comparison["paired_mean_conversation_score_delta"],
        )
        self.assertEqual(len(comparison["paired_bootstrap_95_ci"]), 2)

    def test_unknown_result_record_is_rejected(self):
        path = self.write_results()
        try:
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps({
                    "conversation_id": "LSC-999",
                    "probe_id": "P001",
                    "response": "{}",
                }) + "\n")
            with self.assertRaises(bench.ContractError):
                bench.grade(self.corpus, path)
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
