#!/usr/bin/env python3
"""Summarise an arm's real throughput from its llama-server log.

Speed is a reported result of this campaign, not a diagnostic, so it is
measured across the whole arm rather than from the single warmed probe the
slow-arm gate uses. A 1,001-note extraction yields ~1,000 generation timings,
and on the first arm they spanned under 2%, which makes the median a far
stronger figure than one 400-token probe.

THE EXCLUSION IS THE WHOLE POINT. llama.cpp logs two rates per request:

    prompt eval time = ...  (  480 tokens, 17107.42 tokens per second)   <- prefill
           eval time = ...  (  552 tokens,   372.26 tokens per second)   <- generation

Prefill runs ~45x faster. A grep for "eval time" matches both, and mixing them
reported a mean of 8,678 tok/s for a model generating at 372 -- an order of
magnitude wrong, in the flattering direction. Prefill is summarised separately
rather than thrown away: it is the cheap half of this task's cost and worth
reporting on its own.

Run standalone to backfill an arm that completed before this existed:

    throughput.py <server.log> <throughput.json>
"""

from __future__ import annotations

import json
import re
import statistics
import sys

RATE = re.compile(r"([0-9.]+) tokens per second")


def collect(path: str) -> tuple[list[float], list[float]]:
    generation: list[float] = []
    prefill: list[float] = []
    with open(path, errors="replace") as handle:
        for line in handle:
            if "eval time =" not in line:
                continue
            match = RATE.search(line)
            if not match:
                continue
            value = float(match.group(1))
            if value <= 0:
                continue
            if "prompt eval time" in line:
                prefill.append(value)
            else:
                generation.append(value)
    return generation, prefill


def summarise(values: list[float]) -> dict[str, float] | None:
    if not values:
        return None
    values = sorted(values)
    return {
        "n": len(values),
        "median": round(statistics.median(values), 2),
        "mean": round(statistics.mean(values), 2),
        "min": round(values[0], 2),
        "max": round(values[-1], 2),
        "p10": round(values[len(values) // 10], 2),
        "p90": round(values[len(values) * 9 // 10], 2),
    }


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    srvlog, out = sys.argv[1], sys.argv[2]
    generation, prefill = collect(srvlog)
    if not generation:
        # Never write a summary that silently claims zero samples were fine.
        print(f"no generation timings found in {srvlog}", file=sys.stderr)
        return 1
    json.dump(
        {
            "generation_tok_per_s": summarise(generation),
            "prefill_tok_per_s": summarise(prefill),
            "note": "generation excludes 'prompt eval time' lines, which are "
                    "prefill and run roughly 45x faster; conflating them "
                    "inflates the mean by more than an order of magnitude.",
        },
        open(out, "w"),
        indent=2,
    )
    gen = summarise(generation) or {}
    print(f"generation median {gen.get('median')} tok/s over {gen.get('n')} samples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
