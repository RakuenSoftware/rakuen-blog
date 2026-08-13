"""The paired counterfactual: the same note answered with and without reasoning.

Every earlier comparison of silent against reasoned notes is observational. The
model chooses which notes it skips, so a silent note scoring well is equally
consistent with reasoning being unnecessary there and with the model skipping
notes it already knew. Nothing in a single run separates those.

Forcing reasoning does, because the same note is then answered both ways. The
groups are defined by what the model did under the LIVE prompt:

  FORCED    silent under live, reasoned under forcereason. The population the
            question is about.
  CONTROL   reasoned under both. The wording changed for these too, so whatever
            they move is what the sentence is worth on its own.
  STUBBORN  silent under both. The clause did not reach them.

The FORCED delta minus the CONTROL delta is the part attributable to reasoning
rather than to the new sentence. If CONTROL moves as much as FORCED, the
comparison is dead and this prints so.
"""
import argparse
import json
import pathlib

import bootstrap_ci as B


def f1(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def load(path):
    out = {}
    for line in path.open():
        line = line.strip()
        if line:
            r = json.loads(line)
            out[r["id"]] = r
    return out


def scored(gold, pred):
    """Per-note F1 from the harness scorer, so these are the published numbers."""
    return {i: f1(tp, fp, fn) for i, tp, fp, fn in B.per_note_counts(gold, pred)}


def summarize(name, ids, a_f1, b_f1):
    if not ids:
        return f"{name:<9} {0:>6}" + " " * 26 + "no notes"
    da = sum(a_f1.get(i, 0.0) for i in ids) / len(ids)
    db = sum(b_f1.get(i, 0.0) for i in ids) / len(ids)
    return (f"{name:<9} {len(ids):>6} {da:>9.4f} {db:>9.4f} {db - da:>+9.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--gold", required=True)
    ap.add_argument("--stem", default="gemma-4-E4B-it.Q6")
    args = ap.parse_args()

    d = pathlib.Path(args.out)
    live_p = d / f"{args.stem}.live.pred.jsonl"
    forced_p = d / f"{args.stem}.forcereason.pred.jsonl"
    for p in (live_p, forced_p):
        if not p.exists():
            raise SystemExit(f"missing {p}")

    live, forced = load(live_p), load(forced_p)
    shared = sorted(set(live) & set(forced))
    if len(shared) != len(live) or len(shared) != len(forced):
        raise SystemExit(f"halves disagree on notes: {len(live)}, {len(forced)}, "
                         f"{len(shared)} shared")

    def quiet(row):
        return not (row.get("reasoning_chars") or 0)

    groups = {
        "FORCED": [i for i in shared if quiet(live[i]) and not quiet(forced[i])],
        "CONTROL": [i for i in shared if not quiet(live[i]) and not quiet(forced[i])],
        "STUBBORN": [i for i in shared if quiet(live[i]) and quiet(forced[i])],
        "LOST": [i for i in shared if not quiet(live[i]) and quiet(forced[i])],
    }

    silent_live = sum(1 for i in shared if quiet(live[i]))
    silent_forced = sum(1 for i in shared if quiet(forced[i]))
    print(f"notes {len(shared)}")
    print(f"silent under live       {silent_live:>5} "
          f"({100 * silent_live / len(shared):.1f}%)")
    print(f"silent under forced     {silent_forced:>5} "
          f"({100 * silent_forced / len(shared):.1f}%)")

    a_f1 = scored(args.gold, str(live_p))
    b_f1 = scored(args.gold, str(forced_p))

    print(f"\n{'group':<9} {'notes':>6} {'live F1':>9} {'forced':>9} {'delta':>9}")
    for name in ("FORCED", "CONTROL", "STUBBORN", "LOST"):
        print(summarize(name, groups[name], a_f1, b_f1))

    if groups["FORCED"] and groups["CONTROL"]:
        def delta(ids):
            return (sum(b_f1.get(i, 0.0) for i in ids)
                    - sum(a_f1.get(i, 0.0) for i in ids)) / len(ids)
        df, dc = delta(groups["FORCED"]), delta(groups["CONTROL"])
        print(f"\nforced delta      {df:+.4f}")
        print(f"control delta     {dc:+.4f}   (what the sentence is worth alone)")
        print(f"attributable      {df - dc:+.4f}")
        if abs(dc) >= abs(df):
            print("\nThe control moved at least as far as the forced group. This "
                  "comparison\nmeasures the wording, not the reasoning, and "
                  "nothing here supports a claim\nabout what the skipped notes "
                  "cost.")

    (d / "forced_reasoning.json").write_text(json.dumps({
        "notes": len(shared),
        "silent_live": silent_live, "silent_forced": silent_forced,
        "groups": {k: len(v) for k, v in groups.items()},
        "mean_f1": {k: {"live": (sum(a_f1.get(i, 0.0) for i in v) / len(v)) if v else None,
                        "forced": (sum(b_f1.get(i, 0.0) for i in v) / len(v)) if v else None}
                    for k, v in groups.items()},
    }, indent=1) + "\n")


if __name__ == "__main__":
    main()
