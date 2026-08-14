#!/usr/bin/env python3
"""Validate and summarize the native Qwen3.8 head-to-head arm."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--pred", type=Path, required=True)
    parser.add_argument("--score", type=Path, required=True)
    parser.add_argument("--server-log", type=Path, required=True)
    parser.add_argument("--run-log", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--context", type=int, default=8192)
    args = parser.parse_args()

    gold = load_jsonl(args.gold)
    pred = load_jsonl(args.pred)
    gold_ids = [str(row["id"]) for row in gold]
    pred_ids = [str(row["id"]) for row in pred]
    if pred_ids != gold_ids:
        raise RuntimeError(
            f"prediction population/order mismatch: {len(pred_ids)} vs {len(gold_ids)}"
        )
    if len(pred_ids) != len(set(pred_ids)):
        raise RuntimeError("duplicate prediction identifiers")
    if any(row.get("error") is not None for row in pred):
        raise RuntimeError("transport errors remain in the completed arm")
    if {row.get("model") for row in pred} != {"Qwen3.8-27B.Q4_K_M.xtx.mtp-on"}:
        raise RuntimeError("model label mismatch")
    if {row.get("runtime") for row in pred} != {"llama.cpp"}:
        raise RuntimeError("runtime mismatch")
    if {row.get("thinking") for row in pred} != {True}:
        raise RuntimeError("thinking state mismatch")
    if {row.get("concurrency") for row in pred} != {1}:
        raise RuntimeError("concurrency mismatch")
    if len({row.get("prompt_version") for row in pred}) != 1:
        raise RuntimeError("prompt version changed within the arm")

    score = json.loads(args.score.read_text(encoding="utf-8"))
    latencies = [float(row["latency_ms"]) / 1000 for row in pred]
    decode_rates = [
        float(row["predicted_per_second"])
        for row in pred
        if row.get("predicted_per_second") is not None
    ]
    completions = [
        int(row["completion_tokens"])
        for row in pred
        if row.get("completion_tokens") is not None
    ]
    context_limited = [
        str(row["id"])
        for row in pred
        if int(row.get("prompt_tokens") or 0)
        + int(row.get("completion_tokens") or 0)
        >= args.context - 1
    ]
    drafted = sum(int(row.get("draft_n") or 0) for row in pred)
    accepted = sum(int(row.get("draft_n_accepted") or 0) for row in pred)

    result = {
        "population": len(pred),
        "model": "Qwen3.8-27B.Q4_K_M.xtx.mtp-on",
        "prompt_version": pred[0]["prompt_version"],
        "thinking": True,
        "concurrency": 1,
        "context_tokens": args.context,
        "transport_errors": 0,
        "parse_failures": sum(not bool(row.get("parse_ok")) for row in pred),
        "schema_failures": sum(not bool(row.get("schema_ok")) for row in pred),
        "context_limited_ids": context_limited,
        "reasoning_rows": sum(int(row.get("reasoning_chars") or 0) > 0 for row in pred),
        "latency_seconds": {
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
            "p99": percentile(latencies, 0.99),
        },
        "decode_tokens_per_second": {
            "median": statistics.median(decode_rates),
            "minimum": min(decode_rates),
            "maximum": max(decode_rates),
        },
        "completion_tokens": {
            "median": statistics.median(completions),
            "maximum": max(completions),
        },
        "mtp": {
            "drafted": drafted,
            "accepted": accepted,
            "acceptance_rate": accepted / drafted,
        },
        "strict_score": score["strict"],
        "artifacts": {
            "gold_sha256": sha256(args.gold),
            "pred_sha256": sha256(args.pred),
            "score_sha256": sha256(args.score),
            "server_log_sha256": sha256(args.server_log),
            "run_log_sha256": sha256(args.run_log),
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "PASS: n={} F1={:.4f} parse_failures={} context_limited={}".format(
            result["population"],
            result["strict_score"]["f1"],
            result["parse_failures"],
            len(context_limited),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
