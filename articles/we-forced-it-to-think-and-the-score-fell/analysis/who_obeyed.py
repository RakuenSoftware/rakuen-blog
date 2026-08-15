#!/usr/bin/env python3
"""Exactly half the silent notes ignored an instruction to reason. Which half?

134 notes went silent under the live prompt. Under a prompt saying to reason on
every note, 67 reasoned and 67 did not. A 50/50 split invites the reading that
the instruction landed at random, and that is worth testing rather than assuming,
because the alternative is that the two halves differ and the difference says
what the clause can and cannot reach.

The second question is where the loss sits. A mean of -0.2090 over 67 notes is
consistent with every note dropping a little and with a handful collapsing, and
those are different findings.

Reads committed artifacts. No inference, no card.
"""
import collections
import json
import pathlib
import sys

RAW = pathlib.Path(
    "/home/virant/dev/rakuen-blog/.claude/worktrees/rescue-ten-ready-articles"
    "/articles/local-llm-fact-extraction-head-to-head/evidence/raw")
sys.path.insert(0, str(RAW / "harness" / "harness"))
import bootstrap_ci as B  # noqa: E402

GOLD = RAW / "corpus/data/corpora/v5/gold_small.jsonl"
RUN = RAW / "results/forced-reasoning-20260813"
LIVE = RUN / "gemma-4-E4B-it.Q6.live.pred.jsonl"
FORCED = RUN / "gemma-4-E4B-it.Q6.forcereason.pred.jsonl"


def f1(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def rows(path):
    return {json.loads(l)["id"]: json.loads(l) for l in path.open() if l.strip()}


def main():
    gold = {json.loads(l)["id"]: json.loads(l) for l in GOLD.open() if l.strip()}
    live, forced = rows(LIVE), rows(FORCED)
    a = {i: f1(tp, fp, fn) for i, tp, fp, fn in B.per_note_counts(str(GOLD), str(LIVE))}
    b = {i: f1(tp, fp, fn) for i, tp, fp, fn in B.per_note_counts(str(GOLD), str(FORCED))}

    def quiet(r):
        return not (r.get("reasoning_chars") or 0)

    silent = [i for i in live if quiet(live[i])]
    moved = [i for i in silent if not quiet(forced[i])]
    stayed = [i for i in silent if quiet(forced[i])]
    print(f"silent under live {len(silent)}, obeyed {len(moved)}, "
          f"ignored {len(stayed)}")

    print("\n=== category ===")
    print(f"{'category':<14} {'obeyed':>7} {'ignored':>8} {'all silent':>11} "
          f"{'corpus':>7}")
    corpus = collections.Counter(g["category"] for g in gold.values())
    cm = collections.Counter(gold[i]["category"] for i in moved)
    cs = collections.Counter(gold[i]["category"] for i in stayed)
    for cat in sorted(corpus):
        if cm[cat] or cs[cat]:
            print(f"{cat:<14} {cm[cat]:>7} {cs[cat]:>8} {cm[cat] + cs[cat]:>11} "
                  f"{corpus[cat]:>7}")

    print("\n=== what the two halves look like ===")
    print(f"{'group':<9} {'n':>4} {'live F1':>9} {'note chars':>11} "
          f"{'gold triples':>13}")
    for name, ids in (("obeyed", moved), ("ignored", stayed)):
        if not ids:
            continue
        print(f"{name:<9} {len(ids):>4} "
              f"{sum(a.get(i, 0.0) for i in ids) / len(ids):>9.4f} "
              f"{sum(len(gold[i]['note']) for i in ids) / len(ids):>11.1f} "
              f"{sum(len(gold[i]['gold']) for i in ids) / len(ids):>13.2f}")

    print("\n=== where the loss sits, obeyed notes only ===")
    deltas = sorted(((b.get(i, 0.0) - a.get(i, 0.0), i) for i in moved))
    worse = [d for d, _ in deltas if d < -0.001]
    same = [d for d, _ in deltas if -0.001 <= d <= 0.001]
    better = [d for d, _ in deltas if d > 0.001]
    print(f"got worse {len(worse)}, unchanged {len(same)}, got better "
          f"{len(better)}")
    if worse:
        print(f"mean drop among the {len(worse)} that got worse: "
              f"{sum(worse) / len(worse):+.4f}")
    print("the ten largest drops:")
    for d, i in deltas[:10]:
        print(f"  {d:+.4f}  {gold[i]['category']:<12} "
              f"{a.get(i, 0.0):.2f} -> {b.get(i, 0.0):.2f}  "
              f"{gold[i]['note'][:58]}")

    print("\n=== loss by category, obeyed notes only ===")
    per_cat = collections.defaultdict(list)
    for d, i in deltas:
        per_cat[gold[i]["category"]].append(d)
    print(f"{'category':<14} {'n':>4} {'mean delta':>11}")
    for cat, ds in sorted(per_cat.items(), key=lambda kv: sum(kv[1]) / len(kv[1])):
        print(f"{cat:<14} {len(ds):>4} {sum(ds) / len(ds):>+11.4f}")


if __name__ == "__main__":
    main()
