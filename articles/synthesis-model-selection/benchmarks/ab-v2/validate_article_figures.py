#!/usr/bin/env python3
"""Check the published synthesis figures against the canonical analysis."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / "article" / "synthesis-model-selection.md"
ANALYSIS = (
    ROOT
    / "evidence"
    / "raw"
    / "candidate-matrix-20260814"
    / "canonical"
    / "analysis-20260815.json"
)


def require(text: str, value: str, subject: str) -> None:
    if value not in text:
        raise SystemExit(f"missing {subject}: {value}")


def main() -> int:
    article = ARTICLE.read_text(encoding="utf-8")
    analysis = json.loads(ANALYSIS.read_text(encoding="utf-8"))

    figures = article.count('<figure class="sg-figure">')
    chart_tabs = article.count(">Chart</label>")
    number_tabs = article.count(">Numbers</label>")
    chart_panes = article.count("sg-figure__pane--chart")
    number_panes = article.count("sg-figure__pane--table")
    if (figures, chart_tabs, number_tabs, chart_panes, number_panes) != (6, 6, 6, 6, 6):
        raise SystemExit(
            "expected six complete Chart/Numbers figures, got "
            f"figures={figures} chart_tabs={chart_tabs} number_tabs={number_tabs} "
            f"chart_panes={chart_panes} number_panes={number_panes}"
        )

    ids = re.findall(r'id="([^"]+)"', article)
    if len(ids) != 12 or len(set(ids)) != len(ids):
        raise SystemExit(f"expected 12 unique figure radio ids, got {len(ids)} ids")

    for model in analysis["models"]:
        label = model["label"]
        require(article, f'{model["content_f1"]:.4f}', f"{label} content F1")
        require(article, f'{model["latency_s"]["p50"]:.3f}', f"{label} median latency")
        require(article, f'{model["latency_s"]["p95"]:.3f}', f"{label} p95 latency")
        require(
            article,
            f'{model["vram_after_run_bytes"] / 2**30:.2f}',
            f"{label} post-run GPU memory",
        )
        require(
            article,
            f'{model["required_field_recall"] * 100:.2f}%',
            f"{label} required-field recall",
        )
        require(
            article,
            f'{model["completion_tokens"]:,}',
            f"{label} completion-token total",
        )
        require(
            article,
            f'{model["decode_tokens_per_second"]:.2f}',
            f"{label} decode rate",
        )
        for task, result in model["by_task"].items():
            require(article, f'{result["content_f1"]:.4f}', f"{label} {task} content F1")

    forbidden = ("Correction:", "Retraction:", "Withdrawal:")
    for marker in forbidden:
        if marker in article:
            raise SystemExit(f"presentation-only update contains {marker}")

    print("PASS synthesis-model-selection figures: 6 Chart/Numbers pairs, canonical values present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
