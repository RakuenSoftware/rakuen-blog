#!/usr/bin/env python3
"""Is the silence a property of the note, or of the run?

If the same notes go silent across two independent runs at different quants, the
cause is in the note. If the overlap is what chance predicts, it is not.
"""

import json
from collections import Counter
from pathlib import Path

RAW = Path(
    "/home/virant/dev/rakuen-blog/.claude/worktrees/rescue-ten-ready-articles"
    "/articles/local-llm-fact-extraction-head-to-head/evidence/raw"
)
RES = RAW / "results"
GOLD = RAW / "corpus/data/corpora/v5"


def silent_ids(rel):
    out = set()
    allids = set()
    for line in open(RES / rel):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        i = r.get("id")
        allids.add(i)
        if not (r.get("reasoning_chars") or 0):
            out.add(i)
    return out, allids


a_sil, a_all = silent_ids("10k-sharded/E4B.UD-Q6_K_XL.10k.pred.jsonl")
b_sil, b_all = silent_ids("qat-mid-3k/gemma-4-E4B-it.qat.mid.pred.jsonl")

shared = a_all & b_all
a_s = a_sil & shared
b_s = b_sil & shared
both = a_s & b_s

pa = len(a_s) / len(shared)
pb = len(b_s) / len(shared)
expected = pa * pb * len(shared)

print(f"notes in both runs           : {len(shared)}")
print(f"silent in 10k Q6             : {len(a_s)}  ({100*pa:.1f}%)")
print(f"silent in qat mid3k          : {len(b_s)}  ({100*pb:.1f}%)")
print(f"silent in BOTH               : {len(both)}")
print(f"expected by chance           : {expected:.0f}")
print(f"ratio observed/expected      : {len(both)/expected:.1f}x" if expected else "")
if b_s:
    print(f"of mid3k's silent notes, share also silent in 10k: {100*len(both)/len(b_s):.1f}%")

# Category from the gold corpus
cats = {}
for name in ("gold_large.jsonl", "gold_mid.jsonl"):
    p = GOLD / name
    if not p.exists():
        continue
    for line in open(p):
        line = line.strip()
        if not line:
            continue
        g = json.loads(line)
        if g.get("id") and g.get("category"):
            cats.setdefault(g["id"], g["category"])

if cats:
    print("\n=== silence by gold category, 10k Q6 ===")
    tot = Counter(cats.get(i) for i in a_all if i in cats)
    sil = Counter(cats.get(i) for i in a_sil if i in cats)
    print(f"{'category':18s} {'silent':>7} {'total':>7} {'rate':>7}")
    for c in sorted(tot, key=lambda c: -(sil[c] / tot[c] if tot[c] else 0)):
        if tot[c]:
            print(f"{str(c):18s} {sil[c]:>7} {tot[c]:>7} {100*sil[c]/tot[c]:>6.1f}%")
