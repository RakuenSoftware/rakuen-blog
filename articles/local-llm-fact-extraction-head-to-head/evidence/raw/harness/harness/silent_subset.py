"""Write the gold subset the model went silent on, so an escalation is cheap.

The question left open by the forced-reasoning run is narrow: 67 of 134 silent
notes ignored an instruction to reason on every note. Whether a firmer sentence
reaches them is answered by those 134 notes and by nothing else, so running the
other 867 costs an hour to measure notes that were never in doubt.

Emits gold rows in their original order and with their original ids, so the
result scores against the same gold and pairs against the same runs.
"""
import argparse
import json
import pathlib


def silent_ids(pred_path):
    ids = []
    for line in pathlib.Path(pred_path).open():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        if not (row.get("reasoning_chars") or 0):
            ids.append(row["id"])
    return set(ids)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--pred", required=True, help="the run whose silent notes to take")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    want = silent_ids(args.pred)
    written = 0
    with pathlib.Path(args.out).open("w") as fh:
        for line in pathlib.Path(args.gold).open():
            line = line.strip()
            if not line:
                continue
            if json.loads(line)["id"] in want:
                fh.write(line + "\n")
                written += 1
    if written != len(want):
        raise SystemExit(f"gold has {written} of {len(want)} silent ids; wrong corpus?")
    print(f"{written} notes -> {args.out}")


if __name__ == "__main__":
    main()
