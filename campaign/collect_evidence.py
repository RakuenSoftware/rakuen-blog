#!/usr/bin/env python3
"""Rebuild the vendored campaign evidence from the runner's own outputs.

Writes three files under evidence/campaign-results/:

  arms-<date>.json            per-arm extraction + synthesis + throughput
  extraction-pairs-<date>.json  paired bootstrap intervals, 20,000 replicates
  synthesis-pairs-<date>.json   paired bootstrap intervals, 5,000 replicates

WHY SEPARATE PAIR FILES. The arms file is per-arm and cannot hold a comparison,
which is how the article ended up quoting intervals that lived only in a
terminal scrollback and in build_figures.py as string literals. A figure should
be able to read its interval from evidence rather than have it retyped.

KV-cache variant arms are excluded here. They belong to the kv-cache-precision
article and mixing them into this ladder is what made an earlier version of this
file report 37 "arms" for a 34-arm ladder.

Refuses to write an arms file containing an arm that is missing extraction or
synthesis, unless --allow-partial is passed, which also records WHICH arms are
partial inside the file. A silently short bundle is worse than no bundle.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARMS_RAW = ROOT / ".armsraw"
SYNTH_RAW = ROOT / ".synthraw"
EVID = ROOT / "articles/which-quant-beats-how-many-bits/evidence/campaign-results"


def load(p) -> dict:
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="date stamp for the filenames")
    ap.add_argument("--allow-partial", action="store_true")
    args = ap.parse_args()

    arms: dict[str, dict] = {}
    partial: list[str] = []

    for arm_json in sorted(glob.glob(str(ARMS_RAW / "*" / "arm.json"))):
        label = os.path.basename(os.path.dirname(arm_json))
        if ".kv-" in label:
            continue
        a = load(arm_json)

        # Two arms finished before throughput.py existed and carry only the
        # single warmed probe in arm.json. throughput.py backfills a real
        # distribution from the server log into throughput.json beside it;
        # prefer that whenever arm.json's copy is missing or has no median, so
        # a backfilled arm stops looking like an uninstrumented one.
        side = os.path.join(os.path.dirname(arm_json), "throughput.json")
        have = ((a.get("throughput") or {}).get("generation_tok_per_s") or {}).get("median")
        if have is None and os.path.exists(side):
            a["throughput"] = load(side)
        rec = {
            "model": a.get("model"),
            "training": a.get("training"),
            "width": a.get("width"),
            "target": a.get("target"),
            "draft": a.get("draft"),
            "speculation": a.get("speculation"),
            "outcome": a.get("outcome"),
            "architecture": a.get("architecture"),
            "offload_mode": a.get("offload_mode"),
            "offload": a.get("offload"),
            "gpu_mem_used_mib": a.get("gpu_mem_used_mib"),
            "server_rss_mib": a.get("server_rss_mib"),
            "extraction_seconds": a.get("extraction_seconds"),
            "cache_type_k": a.get("cache_type_k"),
            "cache_type_v": a.get("cache_type_v"),
            "throughput": a.get("throughput"),
            "extraction": a.get("score"),
            "completion_tokens": a.get("completion_tokens"),
            "output_health": a.get("output_health"),
        }

        summary = glob.glob(str(SYNTH_RAW / label / "summary_*.json"))
        if summary:
            rec["synthesis"] = load(summary[0])
        else:
            rec["synthesis"] = None
            partial.append(label)

        if rec["extraction"] is None:
            partial.append(label)
        arms[label] = rec

    partial = sorted(set(partial))
    if partial and not args.allow_partial:
        print("REFUSING: arms missing a half:", *partial, sep="\n  ")
        print("\nre-run once they finish, or pass --allow-partial")
        return 1

    EVID.mkdir(parents=True, exist_ok=True)

    payload = arms
    if partial:
        payload = {
            "_incomplete_arms": partial,
            "_note": "arms listed in _incomplete_arms are missing a task half",
            **arms,
        }
    (EVID / f"arms-{args.date}.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")

    for src, dst, reps in (
        (ROOT / ".pairs_parsed.json", f"extraction-pairs-{args.date}.json", 20000),
        (ROOT / ".synth_pairs.json", f"synthesis-pairs-{args.date}.json", 5000),
    ):
        if not src.exists():
            print(f"missing {src.name}, skipping {dst}")
            continue
        rows = json.loads(src.read_text())
        (EVID / dst).write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")
        sep = sum(1 for r in rows if r.get("separates"))
        print(f"{dst}: {len(rows)} pairs, {sep} separate ({reps} replicates)")

    print(f"arms-{args.date}.json: {len(arms)} arms"
          + (f", {len(partial)} partial" if partial else ", all complete"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
