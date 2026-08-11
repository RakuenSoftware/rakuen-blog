#!/usr/bin/env python3
"""Reproduce the paired mean-content-F1 difference for the two synthesis runs."""

from __future__ import annotations

import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEED = 20260809
REPLICATES = 5000


def load(path: Path) -> dict[str, dict]:
    latest: dict[str, dict] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                latest[row["case_id"]] = row
    return latest


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[int(fraction * (len(ordered) - 1))]


def main() -> None:
    e2b = load(HERE / "gemma4_e2b" / "raw_gemma4_e2b.jsonl")
    b12 = load(HERE / "gemma4_12b" / "raw_gemma4_12b.jsonl")
    if set(e2b) != set(b12) or len(e2b) != 10_000:
        raise RuntimeError("paired case populations differ")

    case_ids = sorted(e2b)
    differences = [
        float(b12[case_id]["metrics"]["content_f1"])
        - float(e2b[case_id]["metrics"]["content_f1"])
        for case_id in case_ids
    ]
    rng = random.Random(SEED)
    means = [
        sum(differences[rng.randrange(len(differences))] for _ in differences)
        / len(differences)
        for _ in range(REPLICATES)
    ]
    result = {
        "cases": len(differences),
        "right_minus_left": sum(differences) / len(differences),
        "paired_bootstrap_95_range": [
            percentile(means, 0.025),
            percentile(means, 0.975),
        ],
        "replicates": REPLICATES,
        "seed": SEED,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
