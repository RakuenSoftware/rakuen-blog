#!/usr/bin/env python3
"""Run synth_pair_ci.py across the campaign's synthesis comparison matrix.

Reads the same pair list the extraction sweep uses, so the two tasks are
compared on an identical set of pairs and the article can put them side by side.

Arms whose case count is short of the reference population are SKIPPED and
named, not silently dropped: a short arm is a running or failed arm, and
including it would produce an interval over a mismatched case set.
"""

from __future__ import annotations

import glob
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW_DIR = ROOT / ".synthraw"
PAIRS = ROOT / ".pairs_todo.txt"
OUT = ROOT / ".synth_pairs.json"


def raw_for(arm: str) -> str | None:
    hits = glob.glob(str(RAW_DIR / arm / "raw_*.jsonl"))
    return hits[0] if hits else None


def case_count(path: str) -> int:
    with open(path, encoding="utf-8") as fh:
        return sum(1 for line in fh if line.strip())


def main() -> int:
    counts = {
        os.path.basename(os.path.dirname(f)): case_count(f)
        for f in glob.glob(str(RAW_DIR / "*" / "raw_*.jsonl"))
    }
    if not counts:
        print("no synthesis raw files found", file=sys.stderr)
        return 1
    full = max(counts.values())
    short = {a for a, n in counts.items() if n < full}

    pairs = [
        tuple(line.strip().split("\t"))
        for line in PAIRS.read_text().splitlines()
        if line.strip()
    ]

    results = []
    skipped = []
    for base, comp in pairs:
        if base in short or comp in short:
            bad = [a for a in (base, comp) if a in short]
            skipped.append(f"{comp} - {base}: incomplete ({', '.join(bad)})")
            continue
        rb, rc = raw_for(base), raw_for(comp)
        if not rb or not rc:
            skipped.append(f"{comp} - {base}: no synthesis raw")
            continue
        proc = subprocess.run(
            [sys.executable, str(HERE / "synth_pair_ci.py"), rb, rc,
             "--label-baseline", base, "--label-comparison", comp],
            capture_output=True, text=True,
        )
        if "SYNTHPAIROK" not in proc.stdout:
            skipped.append(f"{comp} - {base}: {proc.stderr.strip()[:90]}")
            continue
        results.append(json.loads(proc.stdout.split("SYNTHPAIROK")[0]))

    OUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")

    separates = [r for r in results if r["separates"]]
    print(f"reference population: {full} cases")
    print(f"computed: {len(results)} pairs")
    print(f"separates: {len(separates)} | nulls: {len(results) - len(separates)}")
    print(f"skipped: {len(skipped)}")
    for s in skipped:
        print("   ", s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
