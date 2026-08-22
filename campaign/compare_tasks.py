#!/usr/bin/env python3
"""Put the extraction and synthesis intervals for the same pair side by side.

The article's two-task section previously rested on point estimates, because the
synthesis half had no intervals. With both halves resampled, a disagreement
between the tasks can be stated as a disagreement between two RESOLVED results
rather than as a pattern, which is a much stronger claim and needs to be checked
rather than assumed.

Prints, in order of usefulness to the article:
  1. pairs where both tasks separate and point OPPOSITE ways
  2. pairs where one task separates and the other is a null
  3. everything, for the record
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def key(r):
    return (r["baseline"], r["comparison"])


def main() -> int:
    ext = {key(r): r for r in json.loads((ROOT / ".pairs_parsed.json").read_text())
           if not r.get("error")}
    syn = {key(r): r for r in json.loads((ROOT / ".synth_pairs.json").read_text())}
    both = sorted(set(ext) & set(syn))

    opposite, only_ext, only_syn = [], [], []
    for k in both:
        a, b = ext[k], syn[k]
        da = a["comparison_minus_baseline"]
        db = b["comparison_minus_baseline"]
        if a["separates"] and b["separates"] and (da > 0) != (db > 0):
            opposite.append((k, da, db))
        elif a["separates"] and not b["separates"]:
            only_ext.append((k, da, db))
        elif b["separates"] and not a["separates"]:
            only_syn.append((k, da, db))

    def show(title, rows):
        print(f"\n=== {title} ({len(rows)}) ===")
        for (base, comp), da, db in rows:
            print(f"  {comp} - {base}")
            print(f"      extraction {da:+.4f}   synthesis {db:+.4f}")

    print(f"pairs measured on both tasks: {len(both)}")
    show("BOTH SEPARATE, OPPOSITE DIRECTIONS", opposite)
    show("SEPARATES ON EXTRACTION ONLY", only_ext)
    show("SEPARATES ON SYNTHESIS ONLY", only_syn)

    agree = sum(1 for k in both
                if ext[k]["separates"] and syn[k]["separates"]
                and (ext[k]["comparison_minus_baseline"] > 0)
                == (syn[k]["comparison_minus_baseline"] > 0))
    print(f"\nboth separate, same direction: {agree}")
    print(f"neither separates: {sum(1 for k in both if not ext[k]['separates'] and not syn[k]['separates'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
