#!/usr/bin/env python3
"""Parse pair_ci.sh sweep output into structured extraction intervals.

pair_ci.sh prints a human-readable report and stores nothing. The sweep captures
those reports concatenated with a '### comparison - baseline' header per block;
this turns them back into records the evidence bundle and the figures can use.

A block that does not end in PAIROK is recorded as an error rather than dropped,
so a partial sweep cannot masquerade as a complete one.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / ".pairs_raw.txt"
OUT = ROOT / ".pairs_parsed.json"

DELTA = re.compile(
    r"^(\S+) - (\S+)\s+([+-]?\d*\.\d+)\s+\[\s*([+-]?\d*\.\d+),\s*([+-]?\d*\.\d+)\]\s+(\w+)",
    re.M,
)
SCORE = re.compile(r"^(\S+)\s+(\d\.\d+)\s+\[(\d\.\d+),(\d\.\d+)\]\s+(\d+)\s+(\d+)\s+(\d+)", re.M)


def main() -> int:
    text = RAW.read_text()
    out = []
    for block in text.split("### ")[1:]:
        header = block.split("\n", 1)[0].strip()
        if "PAIROK" not in block:
            out.append({"pair": header, "error": "no PAIROK"})
            continue
        m = DELTA.search(block)
        if not m:
            out.append({"pair": header, "error": "delta line unparsed"})
            continue
        comp, base, delta, lo, hi, verdict = m.groups()
        scores = {s.group(1): float(s.group(2)) for s in SCORE.finditer(block)}
        lo_f, hi_f = float(lo), float(hi)
        out.append({
            "baseline": base,
            "comparison": comp,
            "baseline_strict_f1": scores.get(base),
            "comparison_strict_f1": scores.get(comp),
            "comparison_minus_baseline": float(delta),
            "paired_bootstrap_95_range": [lo_f, hi_f],
            "separates": bool(lo_f > 0 or hi_f < 0),
            "tool_verdict": verdict,
            "replicates": 20000,
            "seed": 20260809,
        })
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    errs = [r for r in out if r.get("error")]
    sep = [r for r in out if r.get("separates")]
    print(f"parsed: {len(out)}  errors: {len(errs)}")
    print(f"separates: {len(sep)}  nulls: {len(out) - len(sep) - len(errs)}")
    for e in errs:
        print("   ", e)
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())
