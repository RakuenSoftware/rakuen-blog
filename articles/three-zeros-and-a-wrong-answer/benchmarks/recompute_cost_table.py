#!/usr/bin/env python3
"""Recompute the article's cost table from the committed cells, and check it.

Usage:  python3 recompute_cost_table.py

Reads every t01_cache cell under ct403-results/ and prints the four columns the
draft states, beside the draft's values, with a verdict per figure. Exit
status is 1 if any of them does not reproduce, so this doubles as a
regression check on the article.

Round trips are counted as codex.item_types.agent_message. That choice is not
arbitrary: it reproduces the baseline and ponytail-addon rows exactly, and no
other field in the cell does. It does NOT reproduce the draft's plugin figure,
which is one of the open discrepancies recorded in ../evidence/figures.md.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

CELLS = Path(__file__).resolve().parent / "ct403-results" / "cells"

# What the draft states today, as (input_lo, input_hi, hit_lo, hit_hi,
# trips_lo, trips_hi, credits_lo, credits_hi). Run label -> the draft's row.
STATED = {
    "baseline": (84_000, 98_000, 66, 88, 4, 5, 4.3, 6.6),
    "ponytail-addon": (107_000, 143_000, 63, 85, 4, 5, 5.3, 7.4),
    "aimee": (464_000, 648_000, 89, 91, 13, 22, 13.8, 19.2),
    "aimee-gateway": (136_000, 231_000, 25, 70, 5, 11, 7.9, 21.5),
}


def cell_metrics(path: Path) -> dict | None:
    summary = path / "summary.json"
    if not summary.exists():
        return None
    codex = json.loads(summary.read_text()).get("codex") or {}
    usage = codex.get("usage") or {}
    inp = usage.get("input_tokens")
    if not inp:
        return None
    cached = usage.get("cached_input_tokens") or 0
    return {
        "input": inp,
        "hit": 100.0 * cached / inp,
        "trips": (codex.get("item_types") or {}).get("agent_message", 0),
        "credits": codex.get("estimated_credits"),
    }


def agrees(cell_value: float, stated: float, step: float) -> bool:
    """True when the stated figure is the cell value at the stated precision.

    A stated figure is accepted if it is either the floor or the nearest
    multiple of `step`, because the draft rounds some columns down and others
    to nearest. Anything outside those two is a real disagreement, not rounding.
    """
    units = cell_value / step
    candidates = {int(units) * step, round(units) * step}
    return any(abs(stated - c) < step / 2 for c in candidates)


def main() -> int:
    runs: dict[str, list[dict]] = {}
    for cell in sorted(CELLS.glob("*__t01_cache__*")):
        m = cell_metrics(cell)
        if m:
            runs.setdefault(cell.name.split("__")[0], []).append(m)

    if not runs:
        print(f"no cells found under {CELLS}", file=sys.stderr)
        return 1

    failures = 0
    for label, pub in STATED.items():
        rows = runs.get(label)
        print(f"\n{label}  (n={len(rows) if rows else 0})")
        if not rows:
            print("  no cells with usage data")
            failures += 1
            continue
        for name, key, lo, hi, fmt, step in (
            ("input tokens", "input", pub[0], pub[1], "{:,.0f}", 1000),
            ("cache hit %", "hit", pub[2], pub[3], "{:.0f}", 1),
            ("round trips", "trips", pub[4], pub[5], "{:.0f}", 1),
            ("credits", "credits", pub[6], pub[7], "{:.2f}", 0.1),
        ):
            vals = [r[key] for r in rows if r[key] is not None]
            got_lo, got_hi = min(vals), max(vals)
            ok = agrees(got_lo, lo, step) and agrees(got_hi, hi, step)
            if not ok:
                failures += 1
            print(
                f"  {name:14s} cells {fmt.format(got_lo)} to {fmt.format(got_hi)}"
                f"   draft {fmt.format(lo)} to {fmt.format(hi)}"
                f"   {'ok' if ok else 'DOES NOT REPRODUCE'}"
            )

    print(f"\n{failures} figures in the draft do not reproduce.")
    print("Each one is recorded in ../evidence/figures.md with what is known about it.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
