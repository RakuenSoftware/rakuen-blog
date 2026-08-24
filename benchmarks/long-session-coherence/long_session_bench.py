#!/usr/bin/env python3
"""Validate, inspect, and grade Long-Session Coherence 100."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
DEFAULT_CORPUS = ROOT / "corpus" / "v1" / "conversations.jsonl"
DEFAULT_MANIFEST = ROOT / "corpus" / "v1" / "manifest.json"
CHECKPOINTS = (4096, 8192, 16384, 32768, 65536)
EXPECTED_CONVERSATIONS = 100
EXPECTED_PROBES = 20


def transcript_budget(context_target: int) -> int:
    return context_target - max(512, context_target // 16)


class ContractError(ValueError):
    pass


def read_jsonl(path: Path) -> Iterable[tuple[int, dict[str, Any]]]:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ContractError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise ContractError(f"{path}:{line_number}: expected a JSON object")
            yield line_number, value


def load_corpus(path: Path = DEFAULT_CORPUS) -> list[dict[str, Any]]:
    return [item for _, item in read_jsonl(path)]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_conversation(item: dict[str, Any], seen: set[str]) -> list[str]:
    errors: list[str] = []
    conversation_id = item.get("id")
    if not isinstance(conversation_id, str) or not conversation_id.startswith("LSC-"):
        return ["conversation has invalid id"]
    if conversation_id in seen:
        errors.append(f"{conversation_id}: duplicate conversation id")
    seen.add(conversation_id)
    if item.get("tracks") != ["fixed_replay", "live_session"]:
        errors.append(f"{conversation_id}: tracks are not canonical")
    if item.get("nominal_context_targets") != list(CHECKPOINTS):
        errors.append(f"{conversation_id}: wrong context targets")

    turns = item.get("turns")
    probes = item.get("probes")
    events = item.get("state_events")
    if not isinstance(turns, list) or not turns:
        return errors + [f"{conversation_id}: missing turns"]
    if not isinstance(probes, list) or len(probes) != EXPECTED_PROBES:
        return errors + [f"{conversation_id}: expected {EXPECTED_PROBES} probes"]
    if not isinstance(events, list) or not events:
        errors.append(f"{conversation_id}: missing state events")
        events = []

    turn_positions: dict[str, int] = {}
    for position, turn in enumerate(turns):
        expected_id = f"T{position + 1:04d}"
        if turn.get("id") != expected_id:
            errors.append(f"{conversation_id}: expected turn {expected_id}")
        turn_positions[expected_id] = position
        expected_role = "user" if position % 2 == 0 else "assistant"
        if turn.get("role") != expected_role:
            errors.append(f"{conversation_id}/{expected_id}: role must be {expected_role}")
        if not isinstance(turn.get("content"), str) or not turn["content"].strip():
            errors.append(f"{conversation_id}/{expected_id}: empty content")

    event_by_turn = {event.get("turn_id"): event for event in events}
    state: dict[str, dict[str, Any]] = {}
    probe_counts: Counter[int] = Counter()
    previous_position = -1
    for index, probe in enumerate(probes, 1):
        probe_id = f"P{index:03d}"
        if probe.get("id") != probe_id or probe.get("ordinal") != index:
            errors.append(f"{conversation_id}: expected probe {probe_id} at ordinal {index}")
        checkpoint = probe.get("checkpoint_tokens")
        probe_counts[checkpoint] += 1
        after_turn_id = probe.get("after_turn_id")
        position = turn_positions.get(after_turn_id, -1)
        if position < previous_position:
            errors.append(f"{conversation_id}/{probe_id}: checkpoint prefix moved backwards")
        previous_position = position
        if position < 0:
            errors.append(f"{conversation_id}/{probe_id}: unknown after_turn_id")
            continue

        state.clear()
        for turn_id, event in event_by_turn.items():
            if turn_positions.get(turn_id, len(turns)) <= position:
                state[event["key"]] = event

        gold = probe.get("gold", {})
        accepted = gold.get("accepted_answers")
        evidence = gold.get("required_evidence_turn_ids")
        if not isinstance(accepted, list) or not accepted:
            errors.append(f"{conversation_id}/{probe_id}: no accepted answer")
        if not isinstance(evidence, list):
            errors.append(f"{conversation_id}/{probe_id}: evidence must be a list")
            continue
        for turn_id in evidence:
            if turn_id not in turn_positions or turn_positions[turn_id] > position:
                errors.append(f"{conversation_id}/{probe_id}: evidence {turn_id} outside prefix")
        key = gold.get("state_key")
        if key is not None and probe.get("type") != "contradiction":
            current = state.get(key)
            if current is None:
                errors.append(f"{conversation_id}/{probe_id}: unknown state key {key}")
            else:
                expected = "NONE" if current["action"] == "unset" else current["value"]
                if accepted != [expected] or evidence != [current["turn_id"]]:
                    errors.append(f"{conversation_id}/{probe_id}: gold does not match state ledger")

        estimated = probe.get("estimated_context_tokens")
        if (
            not isinstance(estimated, int)
            or estimated < transcript_budget(checkpoint)
            or estimated > checkpoint
        ):
            errors.append(f"{conversation_id}/{probe_id}: checkpoint estimate out of range")

    expected_counts = Counter({checkpoint: 4 for checkpoint in CHECKPOINTS})
    if probe_counts != expected_counts:
        errors.append(f"{conversation_id}: expected four probes per checkpoint")
    return errors


def validate(corpus_path: Path, manifest_path: Path) -> dict[str, Any]:
    conversations = load_corpus(corpus_path)
    errors: list[str] = []
    if len(conversations) != EXPECTED_CONVERSATIONS:
        errors.append(f"expected {EXPECTED_CONVERSATIONS} conversations, got {len(conversations)}")
    seen: set[str] = set()
    for item in conversations:
        errors.extend(validate_conversation(item, seen))

    domain_counts = Counter(item.get("domain") for item in conversations)
    if len(domain_counts) != 10 or set(domain_counts.values()) != {10}:
        errors.append(f"domains are not balanced 10x10: {dict(domain_counts)}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read manifest: {exc}")
        manifest = {}
    if manifest.get("conversation_count") != len(conversations):
        errors.append("manifest conversation count is stale")
    if manifest.get("corpus_sha256") != sha256(corpus_path):
        errors.append("manifest corpus hash is stale")
    if errors:
        raise ContractError("\n".join(errors[:100]))
    return {
        "conversation_count": len(conversations),
        "probe_count": sum(len(item["probes"]) for item in conversations),
        "domain_counts": dict(sorted(domain_counts.items())),
    }


def find_conversation(corpus: list[dict[str, Any]], conversation_id: str) -> dict[str, Any]:
    for item in corpus:
        if item["id"] == conversation_id:
            return item
    raise ContractError(f"unknown conversation {conversation_id}")


def build_request(conversation: dict[str, Any], probe_id: str) -> dict[str, Any]:
    probe = next((item for item in conversation["probes"] if item["id"] == probe_id), None)
    if probe is None:
        raise ContractError(f"unknown probe {conversation['id']}/{probe_id}")
    after = next(
        index for index, turn in enumerate(conversation["turns"]) if turn["id"] == probe["after_turn_id"]
    )
    messages = [{"role": "system", "content": conversation["system_prompt"]}]
    messages.extend(
        {"role": turn["role"], "content": f"[{turn['id']}] {turn['content']}"}
        for turn in conversation["turns"][: after + 1]
    )
    messages.append({
        "role": "user",
        "content": (
            f"Scored probe {probe['id']}: {probe['prompt']} Return only the required JSON object."
        ),
    })
    return {
        "conversation_id": conversation["id"],
        "probe_id": probe["id"],
        "checkpoint_tokens": probe["checkpoint_tokens"],
        "track": "fixed_replay",
        "messages": messages,
    }


def normalize_answer(value: str) -> str:
    return " ".join(value.strip().casefold().split())


def evaluate_response(raw: Any, gold: dict[str, Any]) -> dict[str, Any]:
    result = {
        "passed": False,
        "failure_reason": None,
        "json_parseable": False,
        "schema_valid": False,
        "answer_correct": False,
        "evidence_correct": False,
    }
    if not isinstance(raw, str):
        result["failure_reason"] = "missing_response"
        return result
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        result["failure_reason"] = "json_parse_failure"
        return result
    result["json_parseable"] = True
    if (
        not isinstance(payload, dict)
        or set(payload) != {"answer", "evidence_turn_ids", "confidence"}
        or not isinstance(payload.get("answer"), str)
        or not isinstance(payload.get("evidence_turn_ids"), list)
        or not all(isinstance(item, str) for item in payload.get("evidence_turn_ids", []))
        or isinstance(payload.get("confidence"), bool)
        or not isinstance(payload.get("confidence"), (int, float))
        or not math.isfinite(payload["confidence"])
        or not 0 <= payload["confidence"] <= 1
    ):
        result["failure_reason"] = "schema_failure"
        return result
    result["schema_valid"] = True
    accepted = {normalize_answer(item) for item in gold["accepted_answers"]}
    result["answer_correct"] = normalize_answer(payload["answer"]) in accepted
    result["evidence_correct"] = (
        payload["evidence_turn_ids"] == gold["required_evidence_turn_ids"]
    )
    if not result["answer_correct"]:
        result["failure_reason"] = "wrong_answer"
    elif not result["evidence_correct"]:
        result["failure_reason"] = "wrong_evidence"
    else:
        result["passed"] = True
    return result


def percentile(values: list[float], probability: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, math.ceil(probability * len(ordered)) - 1)
    return ordered[index]


def linear_slope(points: list[tuple[float, float]]) -> float:
    if len(points) < 2:
        return 0.0
    mean_x = statistics.fmean(point[0] for point in points)
    mean_y = statistics.fmean(point[1] for point in points)
    denominator = sum((point[0] - mean_x) ** 2 for point in points)
    if denominator == 0:
        return 0.0
    return sum(
        (point[0] - mean_x) * (point[1] - mean_y) for point in points
    ) / denominator


def retention_summary(checkpoint_metrics: dict[str, dict[str, float]]) -> dict[str, Any]:
    points = [
        (math.log2(int(checkpoint)), metrics["pass_rate"])
        for checkpoint, metrics in sorted(
            checkpoint_metrics.items(), key=lambda item: int(item[0])
        )
    ]
    if not points:
        return {
            "retention_auc": 0.0,
            "degradation_per_context_doubling": 0.0,
            "observed_failure_onset_checkpoint": None,
        }
    width = points[-1][0] - points[0][0]
    area = sum(
        (right[0] - left[0]) * (left[1] + right[1]) / 2
        for left, right in zip(points, points[1:])
    )
    baseline = points[0][1]
    onset = next(
        (
            int(2 ** x)
            for x, rate in points[1:]
            if rate < baseline * 0.90
        ),
        None,
    )
    return {
        "retention_auc": area / width if width else points[0][1],
        "degradation_per_context_doubling": linear_slope(points),
        "observed_failure_onset_checkpoint": onset,
    }


def grade(corpus: list[dict[str, Any]], result_path: Path) -> dict[str, Any]:
    records: dict[tuple[str, str], dict[str, Any]] = {}
    duplicate_records: list[str] = []
    for line_number, item in read_jsonl(result_path):
        key = (item.get("conversation_id"), item.get("probe_id"))
        if not all(isinstance(part, str) for part in key):
            raise ContractError(f"{result_path}:{line_number}: missing conversation_id or probe_id")
        if key in records:
            duplicate_records.append("/".join(key))
        records[key] = item
    if duplicate_records:
        raise ContractError(f"duplicate result records: {', '.join(duplicate_records[:10])}")
    expected_keys = {
        (conversation["id"], probe["id"])
        for conversation in corpus
        for probe in conversation["probes"]
    }
    unknown_keys = sorted(set(records) - expected_keys)
    if unknown_keys:
        rendered = ", ".join("/".join(key) for key in unknown_keys[:10])
        raise ContractError(f"unknown result records: {rendered}")

    conversations_report: list[dict[str, Any]] = []
    all_evaluations: list[dict[str, Any]] = []
    checkpoint_stats: dict[int, list[dict[str, Any]]] = defaultdict(list)
    telemetry: dict[str, list[float]] = defaultdict(list)
    telemetry_fields = (
        "prompt_tokens", "completion_tokens", "prompt_eval_tokens_per_second",
        "decode_tokens_per_second", "ttft_ms",
    )

    for conversation in corpus:
        evaluations: list[dict[str, Any]] = []
        first_failure: dict[str, Any] | None = None
        consecutive_passes = 0
        for probe in conversation["probes"]:
            record = records.get((conversation["id"], probe["id"]), {})
            evaluation = evaluate_response(record.get("response"), probe["gold"])
            evaluation.update({
                "conversation_id": conversation["id"],
                "probe_id": probe["id"],
                "ordinal": probe["ordinal"],
                "checkpoint_tokens": probe["checkpoint_tokens"],
                "probe_type": probe["type"],
                "truncated": bool(record.get("truncated", False)),
                "transport_error": record.get("error"),
            })
            if evaluation["truncated"]:
                evaluation["passed"] = False
                evaluation["failure_reason"] = "truncated"
            elif evaluation["transport_error"]:
                evaluation["passed"] = False
                evaluation["failure_reason"] = "transport_error"
            if first_failure is None and evaluation["passed"]:
                consecutive_passes += 1
            elif first_failure is None:
                first_failure = evaluation
            evaluations.append(evaluation)
            all_evaluations.append(evaluation)
            checkpoint_stats[probe["checkpoint_tokens"]].append(evaluation)
            for field in telemetry_fields:
                value = record.get(field)
                if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
                    telemetry[field].append(float(value))

        completed = consecutive_passes == EXPECTED_PROBES
        survival = consecutive_passes / EXPECTED_PROBES
        score = 100.0 if completed else 50.0 * survival
        conversations_report.append({
            "conversation_id": conversation["id"],
            "domain": conversation["domain"],
            "score": score,
            "completed": completed,
            "consecutive_passes": consecutive_passes,
            "survival_fraction": survival,
            "first_failure_probe": first_failure and first_failure["probe_id"],
            "first_failure_reason": first_failure and first_failure["failure_reason"],
        })

    completion_rate = sum(item["completed"] for item in conversations_report) / len(conversations_report)
    survivals = [item["survival_fraction"] for item in conversations_report]
    mean_survival = statistics.fmean(survivals)
    score = 50.0 * completion_rate + 50.0 * mean_survival
    failure_reasons = Counter(
        item["first_failure_reason"] for item in conversations_report if item["first_failure_reason"]
    )
    checkpoint_metrics = {
        str(checkpoint): {
            "pass_rate": sum(item["passed"] for item in items) / len(items),
            "parse_rate": sum(item["json_parseable"] for item in items) / len(items),
            "schema_valid_rate": sum(item["schema_valid"] for item in items) / len(items),
            "truncation_rate": sum(item["truncated"] for item in items) / len(items),
        }
        for checkpoint, items in sorted(checkpoint_stats.items())
    }
    type_stats: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for evaluation in all_evaluations:
        type_stats[evaluation["probe_type"]].append(evaluation)
    report = {
        "score": score,
        "conversation_count": len(conversations_report),
        "completed_conversations": sum(item["completed"] for item in conversations_report),
        "full_completion_rate": completion_rate,
        "mean_survival_fraction": mean_survival,
        "p10_survival_fraction": percentile(survivals, 0.10),
        "fully_coherent": all(item["completed"] for item in conversations_report),
        "json_parse_rate": sum(item["json_parseable"] for item in all_evaluations) / len(all_evaluations),
        "schema_valid_rate": sum(item["schema_valid"] for item in all_evaluations) / len(all_evaluations),
        "answer_accuracy": sum(item["answer_correct"] for item in all_evaluations) / len(all_evaluations),
        "evidence_accuracy": sum(item["evidence_correct"] for item in all_evaluations) / len(all_evaluations),
        "first_failure_reasons": dict(sorted(failure_reasons.items())),
        "checkpoint_metrics": checkpoint_metrics,
        "retention": retention_summary(checkpoint_metrics),
        "probe_type_metrics": {
            probe_type: {
                "count": len(items),
                "pass_rate": sum(item["passed"] for item in items) / len(items),
                "answer_accuracy": sum(item["answer_correct"] for item in items) / len(items),
                "evidence_accuracy": sum(item["evidence_correct"] for item in items) / len(items),
            }
            for probe_type, items in sorted(type_stats.items())
        },
        "telemetry": {
            field: {
                "samples": len(values),
                "mean": statistics.fmean(values),
                "median": statistics.median(values),
            }
            for field, values in sorted(telemetry.items())
        },
        "conversations": conversations_report,
    }
    return report


def compare_reports(
    baseline: dict[str, Any], candidate: dict[str, Any], samples: int = 10000
) -> dict[str, Any]:
    baseline_scores = {
        item["conversation_id"]: item["score"] for item in baseline["conversations"]
    }
    candidate_scores = {
        item["conversation_id"]: item["score"] for item in candidate["conversations"]
    }
    if baseline_scores.keys() != candidate_scores.keys():
        raise ContractError("baseline and candidate do not contain the same conversations")
    ids = sorted(baseline_scores)
    deltas = [candidate_scores[item] - baseline_scores[item] for item in ids]
    rng = random.Random(20270824)
    bootstrap = [
        statistics.fmean(deltas[rng.randrange(len(deltas))] for _ in deltas)
        for _ in range(samples)
    ]
    checkpoints = sorted(
        baseline["checkpoint_metrics"], key=int
    )
    return {
        "comparison": "candidate_minus_baseline",
        "conversation_count": len(ids),
        "score_delta": candidate["score"] - baseline["score"],
        "paired_mean_conversation_score_delta": statistics.fmean(deltas),
        "paired_bootstrap_95_ci": [
            percentile(bootstrap, 0.025),
            percentile(bootstrap, 0.975),
        ],
        "full_completion_rate_delta": (
            candidate["full_completion_rate"] - baseline["full_completion_rate"]
        ),
        "mean_survival_fraction_delta": (
            candidate["mean_survival_fraction"] - baseline["mean_survival_fraction"]
        ),
        "checkpoint_pass_rate_deltas": {
            checkpoint: (
                candidate["checkpoint_metrics"][checkpoint]["pass_rate"]
                - baseline["checkpoint_metrics"][checkpoint]["pass_rate"]
            )
            for checkpoint in checkpoints
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    request_parser = subparsers.add_parser("request")
    request_parser.add_argument("conversation_id")
    request_parser.add_argument("probe_id")
    grade_parser = subparsers.add_parser("grade")
    grade_parser.add_argument("results", type=Path)
    grade_parser.add_argument("--out", type=Path)
    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("baseline", type=Path)
    compare_parser.add_argument("candidate", type=Path)
    compare_parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    try:
        if args.command == "validate":
            summary = validate(args.corpus, args.manifest)
            print(
                f"validated {summary['conversation_count']} conversations and "
                f"{summary['probe_count']} probes"
            )
        elif args.command == "request":
            corpus = load_corpus(args.corpus)
            request = build_request(
                find_conversation(corpus, args.conversation_id), args.probe_id
            )
            json.dump(request, sys.stdout, ensure_ascii=False, separators=(",", ":"))
            sys.stdout.write("\n")
        elif args.command == "grade":
            corpus = load_corpus(args.corpus)
            report = grade(corpus, args.results)
            output = json.dumps(report, indent=2) + "\n"
            if args.out:
                args.out.write_text(output, encoding="utf-8")
            else:
                sys.stdout.write(output)
        else:
            corpus = load_corpus(args.corpus)
            report = compare_reports(
                grade(corpus, args.baseline), grade(corpus, args.candidate)
            )
            output = json.dumps(report, indent=2) + "\n"
            if args.out:
                args.out.write_text(output, encoding="utf-8")
            else:
                sys.stdout.write(output)
    except (ContractError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
