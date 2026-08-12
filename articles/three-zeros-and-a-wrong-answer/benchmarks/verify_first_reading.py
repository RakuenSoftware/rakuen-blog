#!/usr/bin/env python3
"""Verify the article's first reading from the committed cells.

Claim: files_indexed reads 0 in every cell, the real readiness gate is a semantic
round-trip, and it passed everywhere.
"""

import json
from collections import Counter
from pathlib import Path

CELLS = Path(
    "/home/virant/dev/rakuen-blog/.claude/worktrees/rescue-ten-ready-articles"
    "/articles/three-zeros-and-a-wrong-answer/benchmarks/ct403-results/cells"
)

files_indexed = Counter()
queued = Counter()
statuses = Counter()
semantic_hits = []
scan_reindexed = []
n = 0

for cell in sorted(CELLS.glob("*")):
    p = cell / "aimee-readiness.json"
    if not p.exists():
        continue
    n += 1
    d = json.loads(p.read_text())
    b = d.get("build") or {}
    files_indexed[b.get("files_indexed")] += 1
    queued[b.get("queued")] += 1
    for probe in ("callers", "blast_radius", "semantic"):
        s = (d.get(probe) or {}).get("result_status")
        statuses[f"{probe}={s}"] += 1
    sem = d.get("semantic") or {}
    hits = sem.get("hits")
    if isinstance(hits, list):
        semantic_hits.append(len(hits))
    scan = d.get("scan") or ""
    if "re-indexed" in scan:
        scan_reindexed.append(scan)

print(f"cells with a readiness artifact: {n}")
print(f"build.files_indexed values     : {dict(files_indexed)}")
print(f"build.queued values            : {dict(queued)}")
print(f"probe result_status            : {dict(statuses)}")
if semantic_hits:
    print(f"semantic hits per cell         : min {min(semantic_hits)}, max {max(semantic_hits)}, "
          f"cells with zero {sum(1 for h in semantic_hits if h == 0)}")
print(f"cells whose scan line reports re-indexing: {len(scan_reindexed)}")
if scan_reindexed:
    print(f"  example: {scan_reindexed[0]}")
