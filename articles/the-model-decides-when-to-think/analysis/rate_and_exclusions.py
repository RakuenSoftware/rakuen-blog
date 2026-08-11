#!/usr/bin/env python3
"""What distinguishes the rows where E4B declines to reason?

Establishes the rate per run first, then looks for a discriminator among the
non-reasoning rows: category, note size, sequence position, shard, output health.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

RAW = Path(
    "/home/virant/dev/rakuen-blog/.claude/worktrees/rescue-ten-ready-articles"
    "/articles/local-llm-fact-extraction-head-to-head/evidence/raw"
)
RES = RAW / "results"

RUNS = [
    ("E2B 10k Q4", "10k-sharded/E2B.UD-Q4_K_XL.10k.pred.jsonl"),
    ("E2B 10k Q6", "10k-sharded/E2B.UD-Q6_K_XL.10k.pred.jsonl"),
    ("E2B 10k Q8", "10k-sharded/E2B.UD-Q8_K_XL.10k.pred.jsonl"),
    ("E4B 10k Q4", "10k-sharded/E4B.UD-Q4_K_XL.10k.pred.jsonl"),
    ("E4B 10k Q6", "10k-sharded/E4B.UD-Q6_K_XL.10k.pred.jsonl"),
    ("E4B 10k Q8", "10k-sharded/E4B.UD-Q8_K_XL.10k.pred.jsonl"),
    ("E4B qat mid3k", "qat-mid-3k/gemma-4-E4B-it.qat.mid.pred.jsonl"),
    ("E2B qat mid3k", "qat-mid-3k/gemma-4-E2B-it.qat.mid.pred.jsonl"),
]


def rows(path):
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


print("=== reasoning rate per run ===")
print(f"{'run':16s} {'rows':>6} {'reasoned':>9} {'silent':>7} {'rate':>7}")
loaded = {}
for label, rel in RUNS:
    p = RES / rel
    if not p.exists():
        print(f"{label:16s}  MISSING {rel}")
        continue
    rs = list(rows(p))
    loaded[label] = rs
    silent = [r for r in rs if not (r.get("reasoning_chars") or 0)]
    print(
        f"{label:16s} {len(rs):>6} {len(rs)-len(silent):>9} {len(silent):>7} "
        f"{100*(len(rs)-len(silent))/len(rs):>6.1f}%"
    )

# Focus on the runs that actually show refusal.
TARGETS = [k for k, v in loaded.items() if sum(1 for r in v if not (r.get("reasoning_chars") or 0)) > 50]
print(f"\nruns with material refusal: {TARGETS}")

for label in TARGETS:
    rs = loaded[label]
    silent = [r for r in rs if not (r.get("reasoning_chars") or 0)]
    loud = [r for r in rs if (r.get("reasoning_chars") or 0)]
    print(f"\n=== {label}: {len(silent)} silent of {len(rs)} ===")

    # 1. Does the id tell us anything (category prefix)?
    def cat(r):
        i = str(r.get("id", ""))
        return i.split("_")[0] if "_" in i else i[:8]

    cs, cl = Counter(map(cat, silent)), Counter(map(cat, loud))
    print("  by id prefix (silent / total):")
    for k in sorted(set(cs) | set(cl), key=lambda k: -(cs[k]))[:8]:
        tot = cs[k] + cl[k]
        print(f"    {k:22s} {cs[k]:5d} / {tot:5d}   {100*cs[k]/tot:5.1f}%")

    # 2. Output health
    for field in ("parse_ok", "schema_ok", "truncated"):
        sv = Counter(r.get(field) for r in silent)
        lv = Counter(r.get(field) for r in loud)
        print(f"  {field:10s} silent={dict(sv)}  reasoned={dict(lv)}")

    # 3. Size
    for field in ("prompt_tokens", "completion_tokens"):
        sv = [r.get(field) or 0 for r in silent]
        lv = [r.get(field) or 0 for r in loud]
        if sv and lv:
            print(
                f"  {field:18s} silent mean {sum(sv)/len(sv):8.1f}  "
                f"reasoned mean {sum(lv)/len(lv):8.1f}"
            )

    # 4. Sequence position: are silent rows clustered?
    idx = {id(r): i for i, r in enumerate(rs)}
    pos = [idx[id(r)] for r in silent]
    if pos:
        buckets = Counter(p * 10 // len(rs) for p in pos)
        print("  position decile (0=start):", dict(sorted(buckets.items())))
