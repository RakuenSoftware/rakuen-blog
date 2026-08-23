#!/usr/bin/env python3
"""Check every tokens-per-second and F1 figure in the article against evidence.

check_article_intervals.py covers intervals only. The two ladder matrices are
the largest blocks of numbers in the article and nothing validated them, which
is the same gap that let completion-token stats go null while the prose still
quoted them.

Both ladders now live inside generated sg-figure blocks rather than as
hand-maintained markdown, so this reads the Numbers pane of each figure. That is
the pane a reader checks the chart against, so it is the one worth gating.
"""

from __future__ import annotations

import html
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

FIG = re.compile(r'<figure class="sg-figure">.*?</figure>', re.S)
ROW = re.compile(r"<tr>(.*?)</tr>", re.S)
CELL = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S)

full = ART.read_text()


def tps(label):
    a = arms.get(label)
    if not a:
        return None
    return ((a.get("throughput") or {}).get("generation_tok_per_s") or {}).get("median")


def f1(label):
    a = arms.get(label)
    return a["extraction"]["strict"]["f1"] if a else None


def numbers_pane(fid):
    """The Numbers-tab table of one figure, as {row label: [cells]}."""
    block = next((m.group(0) for m in FIG.finditer(full) if f'name="{fid}"' in m.group(0)), None)
    if block is None:
        return None
    out = {}
    for r in ROW.finditer(block):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                 for c in CELL.findall(r.group(1))]
        if cells:
            out[cells[0]] = cells[1:]
    return out


def check(fid, getter, places, what):
    pane = numbers_pane(fid)
    if pane is None:
        print(f"MISSING FIGURE: {fid}")
        return 1, 0
    bad = checked = 0
    for display, model in ROWS.items():
        cells = pane.get(display)
        if cells is None:
            print(f"BAD {what}: no row for {display}")
            bad += 1
            continue
        if len(cells) != len(WIDTHS):
            print(f"BAD {what} {display}: {len(cells)} cells, expected {len(WIDTHS)}")
            bad += 1
            continue
        for cell, width in zip(cells, WIDTHS):
            actual = getter(f"{model}.base.{width}")
            checked += 1
            if cell == "not run":
                if actual is not None:
                    print(f"BAD {what} {display} {width}: 'not run' but evidence has {actual}")
                    bad += 1
                continue
            if actual is None:
                print(f"BAD {what} {display} {width}: article {cell}, evidence none")
                bad += 1
            elif f"{float(actual):.{places}f}" != cell:
                print(f"BAD {what} {display} {width}: article {cell} vs evidence {actual}")
                bad += 1
    return bad, checked


def detail_check(fid, columns, what):
    """Gate a per-model detail table whose columns are different measures."""
    pane = numbers_pane(fid)
    if pane is None:
        print(f"MISSING FIGURE: {fid}")
        return 1, 0
    bad = checked = 0
    for display, model in ROWS.items():
        cells = pane.get(display)
        if cells is None:
            continue
        if len(cells) != len(columns):
            print(f"BAD {what} {display}: {len(cells)} cells, expected {len(columns)}")
            bad += 1
            continue
        for cell, (getter, places) in zip(cells, columns):
            actual = getter(f"{model}.base.q4")
            checked += 1
            if actual is None:
                print(f"BAD {what} {display}: article {cell}, evidence none")
                bad += 1
            elif f"{float(actual):.{places}f}" != cell:
                print(f"BAD {what} {display}: article {cell} vs evidence {actual}")
                bad += 1
    return bad, checked


def ex(label, *path):
    a = arms.get(label)
    if not a:
        return None
    node = a["extraction"]
    for k in path:
        node = (node or {}).get(k)
    return node


def sy(label, key):
    a = arms.get(label)
    if not a:
        return None
    s = a.get("synthesis") or {}
    return (s.get("overall") or s).get(key)


bad, checked = check("fig-throughput-ladder", tps, 1, "throughput")
b2, c2 = check("fig-accuracy-ladder", f1, 4, "accuracy")
bad += b2
checked += c2

b3, c3 = detail_check("fig-accuracy-detail", [
    (lambda l: ex(l, "strict", "precision"), 4),
    (lambda l: ex(l, "strict", "recall"), 4),
    (lambda l: ex(l, "strict", "f1"), 4),
    (lambda l: ex(l, "lenient", "f1"), 4),
    (lambda l: ex(l, "relation_agnostic", "f1"), 4),
    (lambda l: (ex(l, "fabrication", "fabrication_rate") or 0), 4),
], "accuracy-detail")
bad += b3
checked += c3

b4, c4 = detail_check("fig-synthesis-detail", [
    (lambda l: sy(l, "content_f1"), 4),
    (lambda l: sy(l, "required_field_recall"), 4),
    (lambda l: sy(l, "schema_valid_rate"), 4),
    (lambda l: sy(l, "empty_rate"), 4),
    (lambda l: sy(l, "truncated_rate"), 4),
], "synthesis-detail")
bad += b4
checked += c4

b5, c5 = check("fig-synthesis-ladder", lambda l: sy(l, "content_f1"), 4, "synthesis-ladder")
bad += b5
checked += c5

# The QAT speed table is still hand-written markdown in the prose.
for base, qat, model in [("479.0", "564.9", "gemma4-e2b"),
                         ("341.7", "418.9", "gemma4-e4b"),
                         ("213.1", "257.1", "gemma4-12b"),
                         ("109.9", "359.6", "gemma4-26b-a4b")]:
    for value, label in ((base, f"{model}.base.q4"), (qat, f"{model}.qat.q4")):
        actual = tps(label)
        checked += 1
        if actual is None or f"{float(actual):.1f}" != value:
            print(f"BAD qat-speed {label}: article {value} vs evidence {actual}")
            bad += 1
        if value not in full:
            print(f"BAD qat-speed {label}: {value} absent from the article")
            bad += 1

print(f"\nchecked {checked} figures, {bad} wrong")
raise SystemExit(1 if bad else 0)
