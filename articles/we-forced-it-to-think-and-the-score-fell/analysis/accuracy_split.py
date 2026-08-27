#!/usr/bin/env python3
"""Does declining to reason cost accuracy?

Uses the harness's own per-note scorer so the numbers are the published ones,
then splits notes by whether the model reasoned on them.
"""

import json
import sys
from pathlib import Path

RAW = Path(
    "/home/virant/dev/rakuen-blog/.claude/worktrees/rescue-ten-ready-articles"
    "/articles/local-llm-fact-extraction-head-to-head/evidence/raw"
)
sys.path.insert(0, str(RAW / "harness" / "harness"))
import bootstrap_ci as B  # noqa: E402

GOLD = RAW / "corpus/data/corpora/v5/gold_large.jsonl"
PRED = RAW / "results/10k-sharded/E4B.UD-Q6_K_XL.10k.pred.jsonl"


def f1(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


counts = {i: (tp, fp, fn) for i, tp, fp, fn in B.per_note_counts(str(GOLD), str(PRED))}

reasoned = {}
for line in open(PRED):
    line = line.strip()
    if line:
        r = json.loads(line)
        reasoned[r["id"]] = bool(r.get("reasoning_chars") or 0)

cats = {}
for line in open(RAW / "corpus/data/corpora/v5/gold_large.jsonl"):
    line = line.strip()
    if line:
        g = json.loads(line)
        cats[g["id"]] = g.get("category")

groups = {True: [0, 0, 0, 0], False: [0, 0, 0, 0]}
by_cat = {}
for i, (tp, fp, fn) in counts.items():
    if i not in reasoned:
        continue
    g = groups[reasoned[i]]
    g[0] += tp
    g[1] += fp
    g[2] += fn
    g[3] += 1
    c = cats.get(i)
    if c:
        d = by_cat.setdefault(c, {True: [0, 0, 0, 0], False: [0, 0, 0, 0]})[reasoned[i]]
        d[0] += tp
        d[1] += fp
        d[2] += fn
        d[3] += 1

print("=== E4B 10k Q6, split by whether the model reasoned ===")
print(f"{'':10s} {'notes':>6} {'tp':>7} {'fp':>7} {'fn':>7} {'F1':>8}")
for key, label in ((True, "reasoned"), (False, "silent")):
    tp, fp, fn, n = groups[key]
    print(f"{label:10s} {n:>6} {tp:>7} {fp:>7} {fn:>7} {f1(tp, fp, fn):>8.4f}")

print("\n=== per category, only where both groups have notes ===")
print(f"{'category':16s} {'n_sil':>6} {'F1 silent':>10} {'n_rea':>6} {'F1 reasoned':>12}  delta")
for c, d in sorted(by_cat.items()):
    s, r = d[False], d[True]
    if s[3] < 20 or r[3] < 20:
        continue
    fs, fr = f1(*s[:3]), f1(*r[:3])
    print(f"{c:16s} {s[3]:>6} {fs:>10.4f} {r[3]:>6} {fr:>12.4f}  {fs-fr:+.4f}")
