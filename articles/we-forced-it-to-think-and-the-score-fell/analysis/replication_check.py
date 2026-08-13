#!/usr/bin/env python3
"""Does the silent-vs-reasoned split replicate in the independent QAT mid3k run?"""

import json
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


def f1(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def load(gold_rel, pred_rel):
    gold, pred = RAW / gold_rel, RAW / pred_rel
    counts = {i: (tp, fp, fn) for i, tp, fp, fn in B.per_note_counts(str(gold), str(pred))}
    reasoned, cats = {}, {}
    for line in open(pred):
        line = line.strip()
        if line:
            r = json.loads(line)
            reasoned[r["id"]] = bool(r.get("reasoning_chars") or 0)
    for line in open(gold):
        line = line.strip()
        if line:
            g = json.loads(line)
            cats[g["id"]] = g.get("category")
    return counts, reasoned, cats


results = {}
for label, gold_rel, pred_rel in RUNS:
    counts, reasoned, cats = load(gold_rel, pred_rel)
    by_cat = {}
    for i, (tp, fp, fn) in counts.items():
        if i not in reasoned or i not in cats:
            continue
        d = by_cat.setdefault(cats[i], {True: [0, 0, 0, 0], False: [0, 0, 0, 0]})[reasoned[i]]
        d[0] += tp
        d[1] += fp
        d[2] += fn
        d[3] += 1
    results[label] = by_cat

print("delta = F1(silent) - F1(reasoned), per category, both runs")
print(f"{'category':16s} {'10k Q6 delta':>14} {'n_sil':>6} | {'mid3k delta':>13} {'n_sil':>6}  agree")
cats = sorted(set(results["10k Q6"]) | set(results["qat mid3k"]))
agree = same = 0
for c in cats:
    row = []
    for label in ("10k Q6", "qat mid3k"):
        d = results[label].get(c)
        if not d or d[False][3] < 20 or d[True][3] < 20:
            row.append((None, d[False][3] if d else 0))
            continue
        row.append((f1(*d[False][:3]) - f1(*d[True][:3]), d[False][3]))
    a, b = row
    mark = ""
    if a[0] is not None and b[0] is not None:
        agree += 1
        if (a[0] > 0) == (b[0] > 0):
            same += 1
            mark = "yes"
        else:
            mark = "NO"
    fa = f"{a[0]:+.4f}" if a[0] is not None else "n/a"
    fb = f"{b[0]:+.4f}" if b[0] is not None else "n/a"
    print(f"{c:16s} {fa:>14} {a[1]:>6} | {fb:>13} {b[1]:>6}  {mark}")

print(f"\ncategories comparable in both runs: {agree}, sign agrees in {same}")
