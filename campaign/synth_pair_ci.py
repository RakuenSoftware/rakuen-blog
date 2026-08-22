#!/usr/bin/env python3
"""Paired bootstrap interval for ONE pair of synthesis arms.

    synth_pair_ci.py <baseline-raw.jsonl> <comparison-raw.jsonl>

Reports <comparison> minus <baseline> on mean content F1, resampling the SAME
case ids for both runs.

WHY THIS EXISTS. The campaign scored every arm on synthesis and then reported
those numbers without intervals, because the harness it bundled (ab-v2) has no
bootstrap in it. The series' paired bootstrap lives in ab-v1 as
paired_content_bootstrap.py, which is hardcoded to two fixture directories, to a
10,000-case population, and to no CLI at all. It could not be pointed at a
campaign arm without being rewritten, so it never was, and the article shipped a
whole task's worth of figures labelled "directions, not differences".

This is that same computation with the two inputs made arguments. The method is
copied deliberately rather than improved:

  SEED = 20260809 and REPLICATES = 5000 are the SYNTHESIS series' constants.
  They are not the extraction series' constants, which are the same seed at
  20,000 replicates. Raising 5000 to 20000 here would tighten these intervals
  and make them incomparable to the synthesis numbers already published. If that
  is ever wanted it is a deliberate, documented re-baseline of the whole series,
  not a default.

  Resampling draws case-level DIFFERENCES with replacement, which is what makes
  the interval paired: both arms see the same case on every draw, so per-case
  difficulty cancels instead of inflating the variance.

The population check is kept, generalised from "exactly 10,000" to "identical
case sets". A pair where one arm is short is not a paired comparison, and
resampling it silently produces a respectable-looking interval computed over
mismatched cases.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

SEED = 20260809
REPLICATES = 5000


def load(path: Path) -> dict[str, dict]:
    """Last row per case_id, matching the original's de-duplication."""
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


def content_f1(row: dict) -> float:
    return float(row["metrics"]["content_f1"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline", type=Path)
    ap.add_argument("comparison", type=Path)
    ap.add_argument("--label-baseline", default=None)
    ap.add_argument("--label-comparison", default=None)
    ap.add_argument("--replicates", type=int, default=REPLICATES)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    base_label = args.label_baseline or args.baseline.parent.name
    comp_label = args.label_comparison or args.comparison.parent.name

    base = load(args.baseline)
    comp = load(args.comparison)

    if set(base) != set(comp):
        only_base = len(set(base) - set(comp))
        only_comp = len(set(comp) - set(base))
        print(
            f"SYNTHPAIRFAIL: case populations differ "
            f"({len(base)} vs {len(comp)}; {only_base} only in baseline, "
            f"{only_comp} only in comparison)",
            file=sys.stderr,
        )
        return 1
    if not base:
        print("SYNTHPAIRFAIL: no cases", file=sys.stderr)
        return 1

    case_ids = sorted(base)
    differences = [content_f1(comp[c]) - content_f1(base[c]) for c in case_ids]

    rng = random.Random(args.seed)
    n = len(differences)
    means = [
        sum(differences[rng.randrange(n)] for _ in range(n)) / n
        for _ in range(args.replicates)
    ]
    lo = percentile(means, 0.025)
    hi = percentile(means, 0.975)
    delta = sum(differences) / n

    result = {
        "baseline": base_label,
        "comparison": comp_label,
        "cases": n,
        "baseline_mean_content_f1": sum(content_f1(base[c]) for c in case_ids) / n,
        "comparison_mean_content_f1": sum(content_f1(comp[c]) for c in case_ids) / n,
        "comparison_minus_baseline": delta,
        "paired_bootstrap_95_range": [lo, hi],
        "separates": bool(lo > 0 or hi < 0),
        "replicates": args.replicates,
        "seed": args.seed,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    print("SYNTHPAIROK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
