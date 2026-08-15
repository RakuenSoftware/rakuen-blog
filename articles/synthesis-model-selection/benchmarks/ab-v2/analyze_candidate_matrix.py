#!/usr/bin/env python3
"""Validate and compare a complete matched synthesis candidate matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any

from run_candidate_matrix import CANDIDATES, LOAD_PROFILE


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def latest_rows(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                rows[str(row["case_id"])] = row
    return rows


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def model_summary(rows: list[dict[str, Any]], summary: dict[str, Any]) -> dict[str, Any]:
    latencies = [float(row["latency_s"]) for row in rows]
    metrics = [row["metrics"] for row in rows]
    return {
        "content_f1": statistics.fmean(float(item["content_f1"]) for item in metrics),
        "raw_parse_rate": statistics.fmean(bool(row["raw_parse"]) for row in rows),
        "schema_valid_rate": statistics.fmean(bool(item["schema_valid"]) for item in metrics),
        "required_field_recall": statistics.fmean(
            float(item["required_field_recall"]) for item in metrics
        ),
        "empty_rate": statistics.fmean(bool(row.get("empty")) for row in rows),
        "truncated_rate": statistics.fmean(bool(row.get("truncated")) for row in rows),
        "latency_s": {
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
            "p99": percentile(latencies, 0.99),
        },
        "decode_tokens_per_second": float(summary["overall"]["decode_tokens_per_second"]),
        "prompt_tokens_per_second": float(summary["overall"]["prompt_tokens_per_second"]),
        "completion_tokens": int(summary["overall"]["completion_tokens"]),
        "prompt_tokens": int(summary["overall"]["prompt_tokens"]),
        "requests_retried": int(summary["overall"]["requests_retried"]),
        "by_task": {
            task: {
                "n": int(values["n"]),
                "content_f1": float(values["content_f1"]),
                "raw_parse_rate": float(values["raw_parse_rate"]),
                "schema_valid_rate": float(values["schema_valid_rate"]),
                "required_field_recall": float(values["required_field_recall"]),
                "latency_s": {
                    key: float(value) for key, value in values["latency_s"].items()
                },
            }
            for task, values in sorted(summary["by_task"].items())
        },
    }


def paired_bootstrap(
    scores: list[list[float]], *, replicates: int, seed: int
) -> tuple[list[list[float]], str]:
    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("paired bootstrap requires NumPy") from exc

    values = np.asarray(scores, dtype=np.float64)
    rng = np.random.default_rng(seed)
    result = np.empty((replicates, values.shape[0]), dtype=np.float64)
    chunk_size = max(1, min(32, replicates))
    for start in range(0, replicates, chunk_size):
        count = min(chunk_size, replicates - start)
        indices = rng.integers(0, values.shape[1], size=(count, values.shape[1]))
        result[start : start + count] = values[:, indices].mean(axis=2).T
    return result.tolist(), str(np.__version__)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-root", type=Path, required=True)
    parser.add_argument("--expected-cases", type=int, default=10_000)
    parser.add_argument("--replicates", type=int, default=5_000)
    parser.add_argument("--seed", type=int, default=20_260_814)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.expected_cases < 1:
        parser.error("--expected-cases must be positive")
    if args.replicates < 1:
        parser.error("--replicates must be positive")

    labels = [str(candidate["label"]) for candidate in CANDIDATES]
    by_label = {str(candidate["label"]): candidate for candidate in CANDIDATES}
    rows_by_label: dict[str, dict[str, dict[str, Any]]] = {}
    summaries: dict[str, dict[str, Any]] = {}
    hardware_by_label: dict[str, dict[str, Any]] = {}
    artifacts: dict[str, dict[str, str]] = {}
    suite_hashes: set[str] = set()

    for label in labels:
        directory = args.results_root / label
        raw_path = directory / f"raw_{label}.jsonl"
        summary_path = directory / f"summary_{label}.json"
        hardware_path = directory / "hardware_synthesis.json"
        rows = latest_rows(raw_path)
        if len(rows) != args.expected_cases:
            raise RuntimeError(f"{label}: {len(rows)} cases, expected {args.expected_cases}")
        failed = [case_id for case_id, row in rows.items() if not row.get("ok")]
        if failed:
            raise RuntimeError(f"{label}: {len(failed)} latest rows failed")
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if int(summary["overall"]["n"]) != args.expected_cases:
            raise RuntimeError(f"{label}: summary population mismatch")
        suite_hashes.add(str(summary["suite_manifest_sha256"]))
        hardware = json.loads(hardware_path.read_text(encoding="utf-8"))
        candidate = by_label[label]
        if hardware.get("candidate") != candidate:
            raise RuntimeError(f"{label}: hardware candidate configuration mismatch")
        if hardware.get("load_profile") != LOAD_PROFILE:
            raise RuntimeError(f"{label}: hardware load profile mismatch")
        if str(candidate["expected_model"]).lower() not in str(
            hardware.get("model_path", "")
        ).lower():
            raise RuntimeError(f"{label}: loaded model identity mismatch")
        if hardware.get("speculative") is not bool(candidate["speculative"]):
            raise RuntimeError(f"{label}: speculation state mismatch")
        rows_by_label[label] = rows
        summaries[label] = summary
        hardware_by_label[label] = hardware
        artifacts[label] = {
            "raw_sha256": sha256(raw_path),
            "summary_sha256": sha256(summary_path),
            "hardware_sha256": sha256(hardware_path),
        }

    if len(suite_hashes) != 1:
        raise RuntimeError(f"suite hashes differ: {sorted(suite_hashes)}")
    populations = [set(rows_by_label[label]) for label in labels]
    if any(population != populations[0] for population in populations[1:]):
        raise RuntimeError("candidate case populations differ")

    case_ids = sorted(populations[0])

    state_path = args.results_root / "RUN_STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("status") != "complete":
        raise RuntimeError(f"matrix run state is not complete: {state.get('status')!r}")
    if state.get("candidate_matrix") != list(CANDIDATES):
        raise RuntimeError("matrix run-state candidate configuration mismatch")
    if state.get("load_profile") != LOAD_PROFILE:
        raise RuntimeError("matrix run-state load profile mismatch")
    if int(state.get("max_cases", -1)) != args.expected_cases:
        raise RuntimeError("matrix run-state case count mismatch")
    ordered_rows = {
        label: [rows_by_label[label][case_id] for case_id in case_ids] for label in labels
    }
    models = []
    scores = []
    for label in labels:
        metrics = model_summary(ordered_rows[label], summaries[label])
        candidate = by_label[label]
        hardware = hardware_by_label[label]
        models.append(
            {
                "label": label,
                "family": candidate["family"],
                "target": candidate["target"],
                "target_file": candidate.get("target_file"),
                "target_training": candidate.get("target_training"),
                "target_quantization": candidate.get("target_quantization"),
                "draft": candidate.get("draft"),
                "chat_template_kwargs": candidate.get(
                    "chat_template_kwargs", {"enable_thinking": False}
                ),
                "speculative": bool(candidate["speculative"]),
                "cold_load_seconds": float(hardware["cold_load_seconds"]),
                "vram_after_load_bytes": int(
                    hardware.get("after_load", {}).get("vram_used_bytes", 0)
                ),
                "vram_after_run_bytes": int(
                    hardware.get("after_run", {}).get("vram_used_bytes", 0)
                ),
                **metrics,
            }
        )
        scores.append(
            [float(row["metrics"]["content_f1"]) for row in ordered_rows[label]]
        )

    bootstrap_means, numpy_version = paired_bootstrap(
        scores, replicates=args.replicates, seed=args.seed
    )
    pairwise = []
    for left_index, left in enumerate(models):
        for right_index in range(left_index + 1, len(models)):
            right = models[right_index]
            differences = [
                replicate[right_index] - replicate[left_index]
                for replicate in bootstrap_means
            ]
            pairwise.append(
                {
                    "left": left["label"],
                    "right": right["label"],
                    "right_minus_left": right["content_f1"] - left["content_f1"],
                    "paired_bootstrap_95_range": [
                        percentile(differences, 0.025),
                        percentile(differences, 0.975),
                    ],
                }
            )

    ranked = sorted(models, key=lambda model: model["content_f1"], reverse=True)
    for rank, model in enumerate(ranked, 1):
        model["content_rank"] = rank
    frontier = []
    for model in models:
        dominated = any(
            other["content_f1"] >= model["content_f1"]
            and other["latency_s"]["p50"] <= model["latency_s"]["p50"]
            and (
                other["content_f1"] > model["content_f1"]
                or other["latency_s"]["p50"] < model["latency_s"]["p50"]
            )
            for other in models
            if other is not model
        )
        if not dominated:
            frontier.append(model["label"])

    result = {
        "cases": args.expected_cases,
        "suite_manifest_sha256": next(iter(suite_hashes)),
        "models": ranked,
        "content_winner": ranked[0]["label"],
        "content_latency_pareto_frontier": frontier,
        "pairwise_content_f1": pairwise,
        "bootstrap": {
            "method": "paired case resampling with replacement",
            "replicates": args.replicates,
            "seed": args.seed,
            "numpy_version": numpy_version,
        },
        "artifacts": artifacts,
        "run_state_sha256": sha256(state_path),
        "run_state": {
            "host": state.get("host"),
            "hardware_identity": state.get("hardware_identity"),
            "llama_device_listing": state.get("llama_device_listing"),
            "llama_server_sha256": state.get("llama_server_sha256"),
            "script_sha256": state.get("script_sha256"),
            "load_profile": state.get("load_profile"),
            "started_unix": state.get("started_unix"),
            "completed_unix": state.get("completed_unix"),
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
