#!/usr/bin/env python3
"""Recompute the Article Zero token ROI measurements from tracked Aimee data."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def percent_change(before: float, after: float) -> float:
    return (after - before) / before * 100


def stream_usage(stream_path: Path) -> dict[str, Any]:
    completions = []
    for line in stream_path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "turn.completed":
            completions.append(event.get("usage") or {})
    if len(completions) != 1:
        raise ValueError(
            f"expected one turn.completed event in {stream_path}, found {len(completions)}"
        )
    usage = completions[0]
    required = ("input_tokens", "cached_input_tokens", "output_tokens")
    if any(type(usage.get(field)) is not int for field in required):
        raise ValueError(f"incomplete provider usage in {stream_path}")
    return {
        "source_sha256": sha256(stream_path),
        "input_tokens": usage["input_tokens"],
        "cached_input_tokens": usage["cached_input_tokens"],
        "uncached_input_tokens": (
            usage["input_tokens"] - usage["cached_input_tokens"]
        ),
        "output_tokens": usage["output_tokens"],
        "reasoning_output_tokens": usage.get("reasoning_output_tokens", 0),
        "input_plus_output_tokens": (
            usage["input_tokens"] + usage["output_tokens"]
        ),
    }


def quality_adjusted_measure(
    provider_path: Path, stream_root: Path | None
) -> dict[str, Any]:
    data = load_json(provider_path)
    cells = data["coding_cells"]
    arms: dict[str, dict[str, Any]] = {}
    rows_by_arm: dict[str, dict[str, dict[str, Any]]] = {}

    for arm in ("standard", "on"):
        rows = sorted(
            (
                row
                for row in cells
                if row["arm"] == arm and row["score_eligible"]
            ),
            key=lambda row: row["task"],
        )
        if len(rows) != 8:
            raise ValueError(f"expected 8 eligible {arm} cells, found {len(rows)}")
        rows_by_arm[arm] = {row["task"]: row for row in rows}
        token_total = sum(row["uncached_input_tokens"] for row in rows)
        success_count = sum(row["task_success"] for row in rows)
        arm_measure = {
            "eligible_tasks": len(rows),
            "successful_tasks": success_count,
            "success_rate_pct": success_count / len(rows) * 100,
            "uncached_input_tokens_total": token_total,
            "uncached_input_tokens_median": statistics.median(
                row["uncached_input_tokens"] for row in rows
            ),
            "uncached_input_tokens_per_successful_task": token_total / success_count,
        }
        if stream_root is not None:
            usages = []
            for row in rows:
                usage = stream_usage(
                    stream_root / f"{arm}-{row['task']}" / "codex.jsonl"
                )
                if usage["uncached_input_tokens"] != row["uncached_input_tokens"]:
                    raise ValueError(
                        f"stream usage does not match tracked result for {arm}-{row['task']}"
                    )
                usages.append(usage)
            for field in (
                "input_tokens",
                "cached_input_tokens",
                "uncached_input_tokens",
                "output_tokens",
                "reasoning_output_tokens",
                "input_plus_output_tokens",
            ):
                arm_measure[f"provider_{field}_total"] = sum(
                    usage[field] for usage in usages
                )
            arm_measure["provider_tokens_per_successful_task"] = (
                arm_measure["provider_input_plus_output_tokens_total"]
                / success_count
            )
        arms[arm] = arm_measure

    standard = arms["standard"]
    on = arms["on"]
    task_rows = []
    recovered = 0
    regressed = 0
    for task in sorted(rows_by_arm["standard"]):
        baseline = rows_by_arm["standard"][task]
        enabled = rows_by_arm["on"][task]
        if not baseline["task_success"] and enabled["task_success"]:
            recovered += 1
        if baseline["task_success"] and not enabled["task_success"]:
            regressed += 1
        task_measure = {
                "task": task,
                "fixture_task": baseline["fixture_task"],
                "standard_success": baseline["task_success"],
                "on_success": enabled["task_success"],
                "standard_uncached_input_tokens": baseline[
                    "uncached_input_tokens"
                ],
                "on_uncached_input_tokens": enabled["uncached_input_tokens"],
            }
        if stream_root is not None:
            task_measure["standard_provider_usage"] = stream_usage(
                stream_root / f"standard-{task}" / "codex.jsonl"
            )
            task_measure["on_provider_usage"] = stream_usage(
                stream_root / f"on-{task}" / "codex.jsonl"
            )
        task_rows.append(task_measure)

    comparison = {
        "uncached_input_token_change": (
            on["uncached_input_tokens_total"]
            - standard["uncached_input_tokens_total"]
        ),
        "uncached_input_token_change_pct": percent_change(
            standard["uncached_input_tokens_total"],
            on["uncached_input_tokens_total"],
        ),
        "successful_task_change": (
            on["successful_tasks"] - standard["successful_tasks"]
        ),
        "success_rate_percentage_point_change": (
            on["success_rate_pct"] - standard["success_rate_pct"]
        ),
        "uncached_input_tokens_per_successful_task_change": (
            on["uncached_input_tokens_per_successful_task"]
            - standard["uncached_input_tokens_per_successful_task"]
        ),
        "uncached_input_tokens_per_successful_task_change_pct": percent_change(
            standard["uncached_input_tokens_per_successful_task"],
            on["uncached_input_tokens_per_successful_task"],
        ),
        "recovered_tasks": recovered,
        "regressed_tasks": regressed,
    }
    if stream_root is not None:
        for field in (
            "provider_input_tokens_total",
            "provider_cached_input_tokens_total",
            "provider_uncached_input_tokens_total",
            "provider_output_tokens_total",
            "provider_input_plus_output_tokens_total",
            "provider_tokens_per_successful_task",
        ):
            comparison[f"{field}_change"] = on[field] - standard[field]
            comparison[f"{field}_change_pct"] = percent_change(
                standard[field], on[field]
            )

    return {
        "source": str(provider_path),
        "source_sha256": sha256(provider_path),
        "model": next(iter(rows_by_arm["standard"].values()))["model"],
        "reasoning": next(iter(rows_by_arm["standard"].values()))["reasoning"],
        "pinned_commit": next(iter(rows_by_arm["standard"].values()))[
            "pinned_commit"
        ],
        "arms": arms,
        "provider_stream_root": str(stream_root) if stream_root is not None else None,
        "comparison": comparison,
        "tasks": task_rows,
    }


def delegation_measure(per_instance_path: Path, campaign_path: Path) -> dict[str, Any]:
    rows = load_json(per_instance_path)
    campaign = load_json(campaign_path)
    if len(rows) != 50:
        raise ValueError(f"expected 50 delegation rows, found {len(rows)}")

    default_tokens = sum(row["default_tokens"] for row in rows)
    delegate_tokens = sum(row["delegate_tokens"] for row in rows)
    saved_tokens = default_tokens - delegate_tokens
    campaign_summary = campaign["summary"]["levels"]
    if default_tokens != campaign_summary["default"]["tokens"]:
        raise ValueError("per-instance default total does not match campaign summary")
    if delegate_tokens != campaign_summary["aimee_delegates"]["tokens"]:
        raise ValueError("per-instance delegate total does not match campaign summary")

    return {
        "per_instance_source": str(per_instance_path),
        "per_instance_source_sha256": sha256(per_instance_path),
        "campaign_source": str(campaign_path),
        "campaign_source_sha256": sha256(campaign_path),
        "pinned_commit": campaign["provenance"]["aimee_commit"],
        "primary_model": campaign["provenance"]["primary_model"],
        "worker_pool": campaign["provenance"]["pool"],
        "tasks": len(rows),
        "default_frontier_tokens": default_tokens,
        "delegated_frontier_tokens": delegate_tokens,
        "frontier_tokens_displaced": saved_tokens,
        "frontier_token_reduction_pct": saved_tokens / default_tokens * 100,
        "tasks_with_fewer_frontier_tokens": sum(
            row["saved_tokens"] > 0 for row in rows
        ),
        "tasks_with_more_frontier_tokens": sum(
            row["saved_tokens"] < 0 for row in rows
        ),
        "median_per_task_frontier_token_reduction_pct": statistics.median(
            row["saved_pct"] for row in rows
        ),
        "largest_increase": min(rows, key=lambda row: row["saved_pct"]),
        "largest_reduction": max(rows, key=lambda row: row["saved_pct"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aimee-repo", required=True, type=Path)
    parser.add_argument("--provider-stream-root", type=Path)
    args = parser.parse_args()
    repo = args.aimee_repo.resolve()
    provider_path = repo / (
        "benchmarks/code-agent-effectiveness/results/e6-20260730-provider.json"
    )
    per_instance_path = repo / (
        "benchmarks/results/cost_savings/lite50.perinstance.json"
    )
    campaign_path = repo / "benchmarks/results/cost_savings/lite50.json"

    output = {
        "schema_version": 1,
        "quality_adjusted_uncached_input": quality_adjusted_measure(
            provider_path,
            args.provider_stream_root.resolve() if args.provider_stream_root else None,
        ),
        "frontier_delegation": delegation_measure(per_instance_path, campaign_path),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
