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


def require_count(text: str, value: str, minimum: int, subject: str) -> None:
    count = text.count(value)
    if count < minimum:
        raise SystemExit(f"expected at least {minimum} {subject}, got {count}: {value}")


def main() -> int:
    article = ARTICLE.read_text(encoding="utf-8")
    analysis = json.loads(ANALYSIS.read_text(encoding="utf-8"))

    figures = article.count('<figure class="sg-figure">')
    chart_tabs = article.count(">Chart</label>")
    number_tabs = article.count(">Numbers</label>")
    chart_panes = article.count("sg-figure__pane--chart")
    number_panes = article.count("sg-figure__pane--table")
    if (figures, chart_tabs, number_tabs, chart_panes, number_panes) != (10, 10, 10, 10, 10):
        raise SystemExit(
            "expected ten complete Chart/Numbers figures, got "
            f"figures={figures} chart_tabs={chart_tabs} number_tabs={number_tabs} "
            f"chart_panes={chart_panes} number_panes={number_panes}"
        )

    ids = re.findall(r'id="([^"]+)"', article)
    if len(ids) != 20 or len(set(ids)) != len(ids):
        raise SystemExit(f"expected 20 unique figure radio ids, got {len(ids)} ids")

    figure_blocks = re.findall(r'<figure class="sg-figure">.*?</figure>', article, re.DOTALL)
    task_figures = {
        task: next(
            (block for block in figure_blocks if f'name="synth-task-{slug}"' in block),
            None,
        )
        for task, slug in {
            "claim": "claim",
            "code_unit": "code-unit",
            "doc_summary": "doc-summary",
            "entity": "entity",
            "synthesis": "synthesis",
        }.items()
    }
    missing_task_figures = [task for task, block in task_figures.items() if block is None]
    if missing_task_figures:
        raise SystemExit(f"missing task figures: {', '.join(missing_task_figures)}")
    for task, block in task_figures.items():
        if block.count('class="sg-chart__label"') != 9 or block.count("<tbody><tr>") != 1:
            raise SystemExit(f"{task} figure does not contain nine plotted labels and a Numbers body")
        tbody = block.split("<tbody>", 1)[1].split("</tbody>", 1)[0]
        if tbody.count("<tr>") != 9:
            raise SystemExit(f"{task} Numbers tab does not contain nine configurations")

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
            displayed = f'{result["content_f1"]:.4f}'
            require_count(
                task_figures[task],
                displayed,
                2,
                f"{label} {task} content F1 values in its Chart and Numbers views",
            )

    forbidden = ("Correction:", "Retraction:", "Withdrawal:")
    for marker in forbidden:
        if marker in article:
            raise SystemExit(f"presentation-only update contains {marker}")

    print("PASS synthesis-model-selection figures: 10 Chart/Numbers pairs, canonical values present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
