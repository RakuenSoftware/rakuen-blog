#!/usr/bin/env python3
"""Bootstrap intervals on the silent-against-reasoned F1 delta, per category.

The split is not paired: silent and reasoned notes are different notes, chosen by
the model. So each group is resampled independently within its category, which is
the right resampling unit and also the one that admits how weak the design is.

Run from anywhere; paths are absolute.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

RAW = Path(
    "/home/virant/dev/rakuen-blog/.claude/worktrees/rescue-ten-ready-articles"
    "/articles/local-llm-fact-extraction-head-to-head/evidence/raw"
)
sys.path.insert(0, str(RAW / "harness" / "harness"))
import bootstrap_ci as B  # noqa: E402

RUNS = [
    ("10k Q6", "corpus/data/corpora/v5/gold_large.jsonl",
     "results/10k-sharded/E4B.UD-Q6_K_XL.10k.pred.jsonl"),
    ("qat mid3k", "corpus/data/corpora/v5/gold_mid.jsonl",
     "results/qat-mid-3k/gemma-4-E4B-it.qat.mid.pred.jsonl"),
]
BOOT = 20000
SEED = 20260812
MIN_NOTES = 20


def f1(tp: int, fp: int, fn: int) -> float:
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def has_gold(rows) -> bool:
    """True when the category contains at least one gold triple.

    ambiguous, transient and negation carry no gold triples by construction, so
    F1 is undefined for them and the scorer reports None. Computing 0.0 instead
    turns 'not applicable' into 'no difference' and yields a delta of exactly
    zero with a zero-width interval, which reads as the strongest result in the
    table and means nothing. Excluded rather than reported.
    """
    return any(tp + fn > 0 for tp, _, fn in rows)


def pooled_f1(rows) -> float:
    tp = sum(r[0] for r in rows)
    fp = sum(r[1] for r in rows)
    fn = sum(r[2] for r in rows)
    return f1(tp, fp, fn)


def interval(silent, reasoned, rng):
    """Percentile interval on f1(silent) - f1(reasoned), resampling each group."""
    deltas = []
    ns, nr = len(silent), len(reasoned)
    for _ in range(BOOT):
        s = [silent[rng.randrange(ns)] for _ in range(ns)]
        r = [reasoned[rng.randrange(nr)] for _ in range(nr)]
        deltas.append(pooled_f1(s) - pooled_f1(r))
    deltas.sort()
    lo = deltas[int(0.025 * BOOT)]
    hi = deltas[int(0.975 * BOOT) - 1]
    return lo, hi


for label, gold_rel, pred_rel in RUNS:
    gold, pred = RAW / gold_rel, RAW / pred_rel
    counts = {i: (tp, fp, fn) for i, tp, fp, fn in B.per_note_counts(str(gold), str(pred))}
    reasoned = {}
    for line in open(pred):
        line = line.strip()
        if line:
            row = json.loads(line)
            reasoned[row["id"]] = bool(row.get("reasoning_chars") or 0)
    cats = {}
    for line in open(gold):
        line = line.strip()
        if line:
            g = json.loads(line)
            cats[g["id"]] = g.get("category")

    groups: dict[str, dict[bool, list]] = {}
    for i, c in counts.items():
        if i in reasoned and i in cats:
            groups.setdefault(cats[i], {True: [], False: []})[reasoned[i]].append(c)

    print(f"\n=== {label}, {BOOT:,} replicates, seed {SEED} ===")
    print(f"{'category':16s} {'n_sil':>6} {'n_rea':>6} {'delta':>9} {'95% interval':>22}  verdict")
    rng = random.Random(SEED)
    for c in sorted(groups):
        s, r = groups[c][False], groups[c][True]
        if len(s) < MIN_NOTES or len(r) < MIN_NOTES:
            continue
        if not has_gold(s + r):
            print(f"{c:16s} {len(s):>6} {len(r):>6} {'no gold triples, F1 undefined':>42}")
            continue
        d = pooled_f1(s) - pooled_f1(r)
        lo, hi = interval(s, r, rng)
        verdict = "separates" if (lo > 0) == (hi > 0) else "crosses zero"
        print(
            f"{c:16s} {len(s):>6} {len(r):>6} {d:>+9.4f} "
            f"{f'{lo:+.4f} to {hi:+.4f}':>22}  {verdict}"
        )
