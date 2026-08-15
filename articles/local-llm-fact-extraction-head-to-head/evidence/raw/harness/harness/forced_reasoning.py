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

    def delta(ids):
        return (sum(b_f1.get(i, 0.0) for i in ids)
                - sum(a_f1.get(i, 0.0) for i in ids)) / len(ids) if ids else 0.0

    df = delta(groups["FORCED"])
    dc = delta(groups["CONTROL"])
    ds = delta(groups["STUBBORN"])

    if groups["FORCED"] and groups["CONTROL"]:
        print(f"\nforced delta        {df:+.4f}")
        print(f"wording control     {dc:+.4f}   reasoned under both, so this is "
              "the sentence alone")
        print(f"selection control   {ds:+.4f}   silent under both, so this is "
              "the selection alone")
        print(f"net of both         {df - dc - ds:+.4f}")
        if abs(dc) >= abs(df):
            print("\nThe wording control moved at least as far as the forced "
                  "group. This\ncomparison measures the sentence, not the "
                  "reasoning, and nothing here\nsupports a claim about what the "
                  "skipped notes cost.")
        if abs(ds) >= abs(df):
            print("\nThe selection control moved at least as far as the forced "
                  "group. Silent\nnotes drift this much between two runs "
                  "regardless, so the forced result is\nregression to the mean "
                  "and not an effect.")

    # THE SELECTION PROBLEM, and why STUBBORN is the control that answers it.
    #
    # FORCED notes are picked for having gone silent, and silent notes score far
    # above the corpus mean. Measure any high-scoring selection a second time and
    # it falls, effect or no effect, so a drop here proves nothing on its own.
    #
    # STUBBORN is picked the same way -- silent under the live prompt -- and then
    # does not get the treatment, because it stayed silent under the forced
    # prompt too. Whatever it drops is what this selection drops without a cause.
    # The two groups are not matched on their starting score, so this bounds the
    # artefact rather than removing it.
    if groups["FORCED"]:
        import bootstrap_ci as boot  # noqa: F811  (same module, named for clarity)
        rng = boot.random.Random(20260809)
        ids = groups["FORCED"]
        per_note = [b_f1.get(i, 0.0) - a_f1.get(i, 0.0) for i in ids]
        reps = []
        for _ in range(20000):
            sample = [per_note[rng.randrange(len(per_note))] for _ in per_note]
            reps.append(sum(sample) / len(sample))
        reps.sort()
        lo, hi = reps[int(0.025 * len(reps))], reps[int(0.975 * len(reps))]
        print(f"\nforced delta 95%    [{lo:+.4f}, {hi:+.4f}]  "
              f"bootstrap over {len(ids)} notes, 20,000 replicates, seed 20260809")

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
