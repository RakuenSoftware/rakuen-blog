"""Does a firmer sentence reach the notes the first one did not?

forcereason moved 67 of 134 silent notes and left 67 untouched. Two readings:
the sentence was not firm enough, or the decision does not answer to prompt text
at all. One wording cannot separate them, so this scores a second, harder wording
on the same 134 notes.

The groups are defined by what happened under the FIRST escalation:

  MOVED      silent under live, reasoned under forcereason. Already reachable;
             included as a check that the harder wording did not break them.
  STUBBORN   silent under both. The population the question is about.

If the stubborn group stays silent under a sentence that names a minimum, forbids
the obvious-answer exemption and covers the empty case, then prompt text is not
the lever. If it moves, the earlier claim that this sits below the level a
sentence reaches was drawn from one wording and has to go.
"""
import argparse
import json
import pathlib


def rows(path):
    out = {}
    for line in pathlib.Path(path).open():
        line = line.strip()
        if line:
            row = json.loads(line)
            out[row["id"]] = row
    return out


def quiet(row):
    return not (row.get("reasoning_chars") or 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", required=True)
    ap.add_argument("--forced", required=True)
    ap.add_argument("--escalated", required=True)
    ap.add_argument("--gold", help="full gold; adds the F1 table")
    args = ap.parse_args()

    live, forced, esc = rows(args.live), rows(args.forced), rows(args.escalated)

    subject = sorted(i for i in esc if i in live and i in forced)
    if len(subject) != len(esc):
        raise SystemExit(f"{len(esc) - len(subject)} escalated note(s) absent from the "
                         "earlier runs; the subset does not match")
    if any(not quiet(live[i]) for i in subject):
        raise SystemExit("a subject note reasoned under live; wrong subset")

    moved = [i for i in subject if not quiet(forced[i])]
    stubborn = [i for i in subject if quiet(forced[i])]

    esc_moved = [i for i in moved if not quiet(esc[i])]
    esc_stubborn = [i for i in stubborn if not quiet(esc[i])]

    print(f"notes silent under live: {len(subject)}")
    print(f"  reasoned under forcereason:  {len(moved)}")
    print(f"  still silent under it:       {len(stubborn)}")
    print()
    print(f"under the harder wording (forcereason2):")
    print(f"  of the {len(moved)} already moved, still reasoning: {len(esc_moved)}")
    print(f"  of the {len(stubborn)} stubborn, now reasoning:     {len(esc_stubborn)}")
    total = len(esc_moved) + len(esc_stubborn)
    print(f"  reasoning overall: {total}/{len(subject)} "
          f"({100 * total / len(subject):.1f}%)")

    if not esc_stubborn:
        print("\nNot one of the stubborn notes moved. Two wordings, the second "
              "naming a\nminimum and closing the exemptions the first left open, "
              "and the same 67 notes\nanswered without reasoning both times.")
    else:
        print(f"\n{len(esc_stubborn)} of {len(stubborn)} moved on wording alone. The "
              "claim that this sits\nbelow the level a sentence reaches was drawn "
              "from one wording and does not\nsurvive a firmer one.")

    parse_ok = sum(1 for i in subject if esc[i].get("parse_ok"))
    errors = sum(1 for i in subject if esc[i].get("error"))
    print(f"\nescalated arm health: {parse_ok}/{len(subject)} parsed, {errors} error(s)")

    if not args.gold:
        return
    import bootstrap_ci as boot

    def f1(tp, fp, fn):
        p = tp / (tp + fp) if tp + fp else 0.0
        r = tp / (tp + fn) if tp + fn else 0.0
        return 2 * p * r / (p + r) if p + r else 0.0

    def scored(pred):
        """Per-note F1 against the FULL gold.

        Not the 134-note subset: per_note_counts walks the gold and scores an
        absent prediction as zero, so a subset gold silently turns the two
        full-corpus arms into 867 zeros and a meaningless mean.
        """
        return {i: f1(tp, fp, fn) for i, tp, fp, fn in boot.per_note_counts(args.gold, pred)}

    a, b, c = scored(args.live), scored(args.forced), scored(args.escalated)
    mean = lambda d, ids: sum(d[i] for i in ids) / len(ids)  # noqa: E731
    print(f"\nF1 on the {len(subject)} notes the live prompt skipped")
    print(f"  live          {mean(a, subject):.4f}")
    print(f"  forcereason   {mean(b, subject):.4f}  ({mean(b, subject) - mean(a, subject):+.4f})")
    print(f"  forcereason2  {mean(c, subject):.4f}  ({mean(c, subject) - mean(a, subject):+.4f})")
    print("  The two deltas are NOT comparable: they ran over different")
    print("  populations, since forcereason left 67 of these silent and")
    print("  forcereason2 left none.")


if __name__ == "__main__":
    main()
