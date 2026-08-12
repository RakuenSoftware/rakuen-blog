#!/usr/bin/env python3
"""Is the aimee cost per-call weight rather than trip count?

The article publishes about 2.3x heavier per call and never cites it. With the
round-trip mechanism retracted, this is the surviving claim, so compute it from
the committed cells.

Reported two ways, because they answer different questions:
  mean context per trip = input_tokens / agent_message
  first-call floor      = the smallest per-trip context any cell in the run shows
"""

import json
from pathlib import Path

CELLS = Path(
    "/home/virant/dev/rakuen-blog/.claude/worktrees/rescue-ten-ready-articles"
    "/articles/three-zeros-and-a-wrong-answer/benchmarks/ct403-results/cells"
)


def metrics(cell):
    s = cell / "summary.json"
    if not s.exists():
        return None
    cx = json.loads(s.read_text()).get("codex") or {}
    u = cx.get("usage") or {}
    inp = u.get("input_tokens")
    trips = (cx.get("item_types") or {}).get("agent_message", 0)
    tools = sum((cx.get("tool_calls") or {}).values())
    if not inp or not trips:
        return None
    return {"input": inp, "trips": trips, "tools": tools, "per_trip": inp / trips}


# All tasks, not just t01_cache, so the per-call figure is not one task's accident.
runs = {}
for cell in sorted(CELLS.glob("*")):
    m = metrics(cell)
    if m:
        runs.setdefault(cell.name.split("__")[0], []).append(m)

print("all tasks in ct403-results")
print(f"{'run':22s} {'cells':>5} {'mean input':>11} {'mean trips':>10} {'tokens/trip':>12} {'vs base':>8}")
base = None
order = ["baseline", "ponytail-addon", "ponytail-instructions", "aimee-gateway",
         "aimee-review", "aimee-noreview", "aimee-lean", "aimee"]
rows = {}
for label in order:
    ms = runs.get(label)
    if not ms:
        continue
    n = len(ms)
    mi = sum(m["input"] for m in ms) / n
    mt = sum(m["trips"] for m in ms) / n
    # per-trip computed per cell then averaged, so a big cell cannot dominate
    pt = sum(m["per_trip"] for m in ms) / n
    rows[label] = (n, mi, mt, pt)
    if label == "baseline":
        base = pt
    ratio = f"{pt/base:.2f}x" if base else "-"
    print(f"{label:22s} {n:>5} {mi:>11,.0f} {mt:>10.1f} {pt:>12,.0f} {ratio:>8}")

print("\nt01_cache only (the article's task)")
print(f"{'run':22s} {'cells':>5} {'tokens/trip':>12} {'vs base':>8}")
base1 = None
for label in order:
    ms = [metrics(c) for c in sorted(CELLS.glob(f"{label}__t01_cache__*"))]
    ms = [m for m in ms if m]
    if not ms:
        continue
    pt = sum(m["per_trip"] for m in ms) / len(ms)
    if label == "baseline":
        base1 = pt
    ratio = f"{pt/base1:.2f}x" if base1 else "-"
    print(f"{label:22s} {len(ms):>5} {pt:>12,.0f} {ratio:>8}")

print("\npublished: about 2.3x heavier per call, from nineteen tool schemas")
print("note: input_tokens is the sum over trips of the whole accumulated context,")
print("so tokens/trip is mean context per trip and rises with conversation length.")
print("It is an upper bound on fixed per-call overhead, not the overhead itself.")
