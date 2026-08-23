"""Check every tokens-per-second figure in the article against the evidence.

check_article_intervals.py covers intervals only. The throughput table is the
largest block of numbers in the article and nothing validated it, which is the
same gap that let completion-token stats go null while the prose still quoted
them.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / ("articles/which-quant-beats-how-many-bits/article/"
              "which-quant-beats-how-many-bits.md")
EV = ROOT / ("articles/which-quant-beats-how-many-bits/evidence/"
             "campaign-results/arms-2026-08-22.json")

arms = {k: v for k, v in json.loads(EV.read_text()).items()
        if not k.startswith("_")}


def tps(label):
    a = arms.get(label)
    if not a:
        return None
    return ((a.get("throughput") or {}).get("generation_tok_per_s") or {}).get("median")


ROWS = {
    "gemma-4 E2B": "gemma4-e2b",
    "gemma-4 E4B": "gemma4-e4b",
    "gemma-4 12B": "gemma4-12b",
    "gemma-4 26B-A4B": "gemma4-26b-a4b",
    "LFM2.5-2.6B": "lfm25-2.6b",
    "LFM2.5-8B-A1B": "lfm25-8b-a1b",
    "Qwen3.6 35B-A3B": "qwen36-35b-a3b",
}
WIDTHS = ["q1", "q2", "q4", "q6", "q8", "bf16"]

full = ART.read_text()

# Row labels repeat across tables, so scope the search to the throughput table
# by its header. Matching on label alone finds the sub-four-bit table first.
start = full.index("| model | Q1 | Q2 | Q4 | Q6 | Q8 | BF16 |")
end = full.index("\n\n", start)
text = full[start:end]
bad = 0
checked = 0

for display, model in ROWS.items():
    m = re.search(r"^\| " + re.escape(display) + r" \|(.+)\|$", text, re.M)
    if not m:
        print(f"MISSING ROW: {display}")
        bad += 1
        continue
    cells = [c.strip() for c in m.group(1).split("|")]
    if len(cells) != len(WIDTHS):
        print(f"{display}: {len(cells)} cells, expected {len(WIDTHS)}")
        bad += 1
        continue
    for cell, width in zip(cells, WIDTHS):
        actual = tps(f"{model}.base.{width}")
        checked += 1
        if cell == "not run":
            if actual is not None:
                print(f"BAD {display} {width}: article says 'not run', "
                      f"evidence has {actual}")
                bad += 1
            continue
        if actual is None:
            print(f"BAD {display} {width}: article says {cell}, evidence has none")
            bad += 1
            continue
        if f"{float(actual):.1f}" != cell:
            print(f"BAD {display} {width}: article {cell} vs evidence {actual}")
            bad += 1

# QAT throughput claims in prose.
for base, qat, model in [("479.0", "564.9", "gemma4-e2b"),
                         ("341.7", "418.9", "gemma4-e4b"),
                         ("213.1", "257.1", "gemma4-12b"),
                         ("109.9", "359.6", "gemma4-26b-a4b")]:
    for value, label in ((base, f"{model}.base.q4"), (qat, f"{model}.qat.q4")):
        actual = tps(label)
        checked += 1
        if actual is None or f"{float(actual):.1f}" != value:
            print(f"BAD {label}: article {value} vs evidence {actual}")
            bad += 1
        if value not in full:
            print(f"BAD {label}: {value} not present in article text")
            bad += 1

print(f"\nchecked {checked} throughput figures, {bad} wrong")
raise SystemExit(1 if bad else 0)
