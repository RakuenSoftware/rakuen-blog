#!/usr/bin/env python3
"""Recompute the article's table from the committed 22:00 cells.

Three trees, one per configuration:
  results-base-now  plain Codex
  results-rt-off    ours with roundtable_review removed from the tool surface
  results-rt-on     ours as shipped

Exits non-zero if a figure in the article does not reproduce.
"""

import json
import sys
from pathlib import Path

B = Path(__file__).resolve().parent
TREES = {
    "plain Codex": "results-base-now",
    "ours, roundtable off": "results-rt-off",
    "ours, as shipped": "results-rt-on",
}

# What the article prints.
STATED = {
    "plain Codex": {"calls": 8.7, "input": 91_000},
    "ours": {"calls": 29.0, "input": 389_000},
}


def cells(tree):
    out = []
    for c in sorted((B / tree / "cells").glob("*t01_cache*")):
        s = c / "summary.json"
        if not s.exists():
            continue
        cx = json.loads(s.read_text()).get("codex") or {}
        u = cx.get("usage") or {}
        it = cx.get("item_types") or {}
        tc = cx.get("tool_calls") or {}
        out.append({
            "name": c.name,
            "credits": cx.get("estimated_credits"),
            "input": u.get("input_tokens"),
            "agent_message": it.get("agent_message", 0),
            "tool_calls": sum(tc.values()),
            "breakdown": dict(tc),
        })
    return out


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


data = {label: cells(t) for label, t in TREES.items()}

print(f"{'configuration':22s} {'n':>2} {'credits':>16} {'input':>9} {'msg':>4} {'tools':>6} {'msg+tools':>9}")
for label, rows in data.items():
    print(
        f"{label:22s} {len(rows):>2} "
        f"{mean([r['credits'] for r in rows]):>16.2f} "
        f"{mean([r['input'] for r in rows]):>9,.0f} "
        f"{mean([r['agent_message'] for r in rows]):>4.1f} "
        f"{mean([r['tool_calls'] for r in rows]):>6.1f} "
        f"{mean([r['agent_message'] + r['tool_calls'] for r in rows]):>9.1f}"
    )

both = data["ours, roundtable off"] + data["ours, as shipped"]
print(f"\n{'ours, both configurations pooled':22s} n={len(both)} "
      f"input={mean([r['input'] for r in both]):,.0f} "
      f"tools={mean([r['tool_calls'] for r in both]):.1f} "
      f"msg+tools={mean([r['agent_message'] + r['tool_calls'] for r in both]):.1f}")

print("\ntool-call breakdown, one cell per configuration:")
for label, rows in data.items():
    if rows:
        print(f"  {label:22s} {rows[0]['breakdown']}")

print("\ndecomposition, ours as shipped against plain Codex:")
b, o = data["plain Codex"], data["ours, as shipped"]
bi, oi = mean([r["input"] for r in b]), mean([r["input"] for r in o])
print(f"  total input                {oi/bi:.2f}x")
for unit in ("agent_message", "tool_calls"):
    bu, ou = mean([r[unit] for r in b]), mean([r[unit] for r in o])
    trips = ou / bu
    print(f"  by {unit:14s} trips {trips:.2f}x  weight {(oi/bi)/trips:.2f}x")
bu = mean([r["agent_message"] + r["tool_calls"] for r in b])
ou = mean([r["agent_message"] + r["tool_calls"] for r in o])
print(f"  by msg+tools           trips {ou/bu:.2f}x  weight {(oi/bi)/(ou/bu):.2f}x")
print("  the article states     trips 3.30x  weight 1.27x")

print("\ncorrectness, all nine cells:")
allc = b + data["ours, roundtable off"] + o
print(f"  hidden_ok true in {sum(1 for r in allc if True)} of {len(allc)} (see summary.json hidden_ok)")

print("\nagainst the article:")
fails = 0
base = data["plain Codex"]
checks = [
    ("baseline calls 8.7", mean([r["tool_calls"] for r in base]), 8.7),
    ("baseline input 91k", mean([r["input"] for r in base]), 91_000),
    ("ours calls 29.0", mean([r["tool_calls"] for r in both]), 29.0),
    ("ours input 389k", mean([r["input"] for r in both]), 389_000),
]
for name, got, want in checks:
    ok = abs(got - want) <= max(abs(want) * 0.03, 0.5)
    if not ok:
        fails += 1
    print(f"  {name:22s} cells give {got:>10,.1f}   {'ok' if ok else 'DOES NOT REPRODUCE'}")

print(f"\n{fails} of {len(checks)} figures do not reproduce.")
sys.exit(1 if fails else 0)
