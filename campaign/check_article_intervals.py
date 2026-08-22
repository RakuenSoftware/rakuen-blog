#!/usr/bin/env python3
"""Check that every interval printed in the article exists in the evidence.

WHY. The article's figures carry their numbers as literal strings, in prose, in
markdown tables and inside inline SVG. Nothing tied those strings to the
bootstrap output, so a corrected paragraph could sit next to a stale figure
caption asserting the opposite, which is exactly what happened to the QAT
section. This walks every '[+x.xxxx, +y.yyyy]' in the draft and asks whether
some measured pair actually reports that interval.

Matching is on the interval endpoints, not on the label, because the article
names pairs in prose style ("gemma-4 E4B, Q6 - Q8") and the evidence names them
by arm label. Endpoints at four decimal places are specific enough that a
collision is not a practical concern, and a wrong-but-real interval attached to
the wrong pair is a different defect than the one this is built to catch.

Exit 1 on any interval with no evidence behind it.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "articles/which-quant-beats-how-many-bits/article/which-quant-beats-how-many-bits.v2-draft.md"
EVID = ROOT / "articles/which-quant-beats-how-many-bits/evidence/campaign-results"

# Intervals that are deliberately not from this campaign's pair sweep.
ALLOWED_FOREIGN = {
    (0.0091, 0.0405): "v1 of this article, different hardware and campaign",
}

INTERVAL = re.compile(r"\[\s*([+-]?\d*\.\d+)\s*,\s*([+-]?\d*\.\d+)\s*\]")


def load_evidence() -> dict[tuple[float, float], list[str]]:
    found: dict[tuple[float, float], list[str]] = {}
    for name in ("extraction-pairs-2026-08-22.json", "synthesis-pairs-2026-08-22.json"):
        path = EVID / name
        if not path.exists():
            print(f"missing evidence file: {name}", file=sys.stderr)
            continue
        task = "extraction" if "extraction" in name else "synthesis"
        for row in json.loads(path.read_text()):
            rng = row.get("paired_bootstrap_95_range")
            if not rng:
                continue
            key = (round(rng[0], 4), round(rng[1], 4))
            found.setdefault(key, []).append(
                f"{task}: {row['comparison']} - {row['baseline']}")
    return found


def main() -> int:
    text = ART.read_text().replace("−", "-").replace("−", "-")
    evidence = load_evidence()

    seen: set[tuple[float, float]] = set()
    missing = []
    for m in INTERVAL.finditer(text):
        lo, hi = round(float(m.group(1)), 4), round(float(m.group(2)), 4)
        if hi < lo:
            continue  # not an interval
        key = (lo, hi)
        if key in seen:
            continue
        seen.add(key)
        # The article states a pair in whichever direction reads better
        # ("Q6 over Q8" rather than "Q8 minus Q6"), which negates and reverses
        # the interval. Both orientations describe the same measurement.
        flipped = (-hi, -lo)
        if key in evidence or key in ALLOWED_FOREIGN or flipped in evidence:
            continue
        ctx = re.sub(r"<[^>]+>", " ", text[max(0, m.start() - 90):m.start()])
        missing.append((key, " ".join(ctx.split())[-70:]))

    print(f"intervals in article: {len(seen)}")
    print(f"backed by evidence:   {len(seen) - len(missing)}")
    for key, ctx in missing:
        print(f"  UNBACKED [{key[0]:+.4f}, {key[1]:+.4f}] ... {ctx}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
