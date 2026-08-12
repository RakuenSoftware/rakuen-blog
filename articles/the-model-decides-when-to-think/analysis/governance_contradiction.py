#!/usr/bin/env python3
"""Why do the two runs disagree about governance?

Candidate explanations, in order of how boring they would be:
  1. the two runs went silent on different governance notes
  2. the mid3k subset's governance notes are easier or harder
  3. the effect is carried by a handful of notes in one run
"""

import json
import sys
from collections import Counter
from pathlib import Path

RAW = Path(
    "/home/virant/dev/rakuen-blog/.claude/worktrees/rescue-ten-ready-articles"
    "/articles/local-llm-fact-extraction-head-to-head/evidence/raw"
)
sys.path.insert(0, str(RAW / "harness" / "harness"))
import bootstrap_ci as B  # noqa: E402

RUNS = {
    "10k Q6": ("corpus/data/corpora/v5/gold_large.jsonl",
               "results/10k-sharded/E4B.UD-Q6_K_XL.10k.pred.jsonl"),
    "mid3k": ("corpus/data/corpora/v5/gold_mid.jsonl",
              "results/qat-mid-3k/gemma-4-E4B-it.qat.mid.pred.jsonl"),
}


def f1(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def pooled(rows):
    return f1(sum(r[0] for r in rows), sum(r[1] for r in rows), sum(r[2] for r in rows))


data = {}
for label, (gold_rel, pred_rel) in RUNS.items():
    gold, pred = RAW / gold_rel, RAW / pred_rel
    counts = {i: c for i, *c in [(i, tp, fp, fn) for i, tp, fp, fn in
                                 B.per_note_counts(str(gold), str(pred))]}
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
    gov = {i: counts[i] for i in counts if cats.get(i) == "governance"}
    data[label] = {
        "counts": gov,
        "silent": {i for i in gov if not reasoned.get(i, True)},
        "all": set(gov),
    }

a, b = data["10k Q6"], data["mid3k"]
shared = a["all"] & b["all"]
print(f"governance notes: 10k {len(a['all'])}, mid3k {len(b['all'])}, shared {len(shared)}")

sa, sb = a["silent"] & shared, b["silent"] & shared
print(f"silent on shared notes: 10k {len(sa)}, mid3k {len(sb)}, both {len(sa & sb)}")
exp = len(sa) * len(sb) / len(shared) if shared else 0
print(f"expected overlap by chance: {exp:.1f}")

print("\n--- 1. are the silent sets the same notes ---")
if sa and sb:
    print(f"jaccard {len(sa & sb) / len(sa | sb):.3f}   "
          f"{'largely different notes' if len(sa & sb) / len(sa | sb) < 0.4 else 'largely same notes'}")

print("\n--- 2. difficulty of governance in each corpus (all notes, reasoned or not) ---")
for label, d in data.items():
    print(f"  {label:8s} n={len(d['counts']):4d}  pooled F1 {pooled(list(d['counts'].values())):.4f}")

print("\n--- 3. is the 10k effect carried by a few notes ---")
sil = [a["counts"][i] for i in a["silent"]]
rea = [a["counts"][i] for i in a["all"] - a["silent"]]
print(f"  10k Q6 silent  n={len(sil):3d}  F1 {pooled(sil):.4f}")
print(f"  10k Q6 reasoned n={len(rea):3d}  F1 {pooled(rea):.4f}")
zero_sil = sum(1 for tp, fp, fn in sil if tp == 0)
zero_rea = sum(1 for tp, fp, fn in rea if tp == 0)
print(f"  notes with zero true positives: silent {zero_sil}/{len(sil)}, reasoned {zero_rea}/{len(rea)}")
fp_sil = sum(r[1] for r in sil) / len(sil) if sil else 0
fp_rea = sum(r[1] for r in rea) / len(rea) if rea else 0
print(f"  mean false positives per note: silent {fp_sil:.2f}, reasoned {fp_rea:.2f}")

# leave-one-out on the silent group to see if one note dominates
if sil:
    base = pooled(sil) - pooled(rea)
    worst = None
    for k in range(len(sil)):
        loo = sil[:k] + sil[k + 1:]
        d = pooled(loo) - pooled(rea)
        if worst is None or abs(d - base) > abs(worst[1] - base):
            worst = (k, d)
    print(f"  delta {base:+.4f}; most influential single note moves it to {worst[1]:+.4f}")
