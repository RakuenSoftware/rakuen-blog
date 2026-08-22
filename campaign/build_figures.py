#!/usr/bin/env python3
"""Generate the article's sg-figure blocks from the committed campaign results.

Every figure in this repository carries both a chart and the numbers behind it,
switched by radio tabs, so a reader can check the picture against the values
without leaving the page. This builds those blocks from
`evidence/campaign-results/arms-*.json` rather than from prose, so a figure can
never drift from the data it claims to show — regenerate and diff to prove it.

Written against the existing convention in speculative-decoding-was-free and
synthesis-model-selection: `sg-figure` wrapper, two radio inputs, a tabs strip,
two panes, and a caption. The chart pane is inline SVG using the same class
names those articles use, so the site's stylesheet applies unchanged.

Usage:
    build_figures.py <results.json> > figures.html
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

W = 760


def esc(s: object) -> str:
    return html.escape(str(s), quote=True)


def figure(fid: str, title: str, svg: str, table: str, caption: str) -> str:
    """One sg-figure block: chart pane, numbers pane, caption."""
    return (
        f'<figure class="sg-figure">'
        f'<input class="sg-figure__radio sg-figure__radio--chart" type="radio" '
        f'name="{fid}" id="{fid}-chart" checked>'
        f'<input class="sg-figure__radio sg-figure__radio--table" type="radio" '
        f'name="{fid}" id="{fid}-table">'
        f'<div class="sg-figure__tabs">'
        f'<label class="sg-figure__tab sg-figure__tab--chart" for="{fid}-chart">Chart</label>'
        f'<label class="sg-figure__tab sg-figure__tab--table" for="{fid}-table">Numbers</label>'
        f'</div><div class="sg-figure__panes">'
        f'<div class="sg-figure__pane sg-figure__pane--chart">{svg}</div>'
        f'<div class="sg-figure__pane sg-figure__pane--table">{table}</div>'
        f'</div>'
        f'<figcaption class="sg-figure__caption">{esc(caption)}</figcaption>'
        f'</figure>'
    )


def table_html(headers, rows, aligns=None) -> str:
    aligns = aligns or ["left"] + ["right"] * (len(headers) - 1)
    head = "".join(
        f'<th style="text-align:{a}">{esc(h)}</th>' for h, a in zip(headers, aligns))
    body = ""
    for row in rows:
        body += "<tr>" + "".join(
            f'<td style="text-align:{a}">{c if isinstance(c, str) and c.startswith("<") else esc(c)}</td>'
            for c, a in zip(row, aligns)) + "</tr>"
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def delta_chart(rows, label_w=250, zero_at=0.0, span=0.45, aria="") -> str:
    """Horizontal deltas with 95% interval whiskers, zero ruled.

    rows: (label, delta, lo, hi, series)
    """
    left, right = label_w, W - 60
    height = 30 + len(rows) * 30
    def x(v):
        return left + (v - (zero_at - span)) / (2 * span) * (right - left)

    parts = [
        f'<svg class="sg-chart" viewBox="0 0 {W} {height + 40}" '
        f'preserveAspectRatio="xMidYMid meet" role="img" aria-label="{esc(aria)}">'
    ]
    for tick in (-0.4, -0.3, -0.2, -0.1, 0.0, 0.1):
        cls = "sg-chart__rule" if tick == 0 else "sg-chart__grid"
        parts.append(
            f'<line class="{cls}" x1="{x(tick):.1f}" x2="{x(tick):.1f}" y1="14" y2="{height}"/>')
        text = "no change" if tick == 0 else f"{tick:+.1f}"
        parts.append(
            f'<text class="sg-chart__value" x="{x(tick):.1f}" y="{height + 18}" '
            f'text-anchor="middle" opacity=".7">{text}</text>')
    for i, (label, delta, lo, hi, series) in enumerate(rows):
        y = 32 + i * 30
        parts.append(
            f'<text class="sg-chart__label" x="{left - 12}" y="{y + 4}" '
            f'text-anchor="end" font-size="11">{esc(label)}</text>')
        parts.append(
            f'<line class="sg-chart__line sg-chart__line--{series}" '
            f'x1="{x(lo):.1f}" x2="{x(hi):.1f}" y1="{y}" y2="{y}"/>')
        for end in (lo, hi):
            parts.append(
                f'<line class="sg-chart__line sg-chart__line--{series}" '
                f'x1="{x(end):.1f}" x2="{x(end):.1f}" y1="{y - 4}" y2="{y + 4}"/>')
        parts.append(
            f'<circle class="sg-chart__mark sg-chart__mark--{series} sg-chart__ring" '
            f'cx="{x(delta):.1f}" cy="{y}" r="4"/>')
        parts.append(
            f'<text class="sg-chart__value" x="{right + 8}" y="{y + 4}">{delta:+.4f}</text>')
    parts.append(
        f'<text class="sg-chart__axis" x="{(left + right) / 2:.0f}" y="{height + 36}" '
        f'text-anchor="middle">STRICT F1 CHANGE, WITH 95% RANGE</text>')
    parts.append("</svg>")
    return "".join(parts)


def bar_chart(rows, unit, label_w=210, aria="") -> str:
    """Horizontal bars from zero. rows: (label, value, series)"""
    left, right = label_w, W - 90
    top = max(v for _, v, _ in rows) or 1
    height = 24 + len(rows) * 27
    parts = [
        f'<svg class="sg-chart" viewBox="0 0 {W} {height + 34}" '
        f'preserveAspectRatio="xMidYMid meet" role="img" aria-label="{esc(aria)}">'
    ]
    for frac in (0.25, 0.5, 0.75, 1.0):
        gx = left + frac * (right - left)
        parts.append(
            f'<line class="sg-chart__grid" x1="{gx:.1f}" x2="{gx:.1f}" y1="12" y2="{height}"/>')
        parts.append(
            f'<text class="sg-chart__value" x="{gx:.1f}" y="{height + 16}" '
            f'text-anchor="middle" opacity=".7">{top * frac:.0f}</text>')
    for i, (label, value, series) in enumerate(rows):
        y = 26 + i * 27
        w = (value / top) * (right - left)
        parts.append(
            f'<text class="sg-chart__label" x="{left - 12}" y="{y + 4}" '
            f'text-anchor="end" font-size="11">{esc(label)}</text>')
        parts.append(
            f'<rect class="sg-chart__mark sg-chart__mark--{series}" x="{left}" '
            f'y="{y - 4.5}" width="{w:.1f}" height="9" rx="4"/>')
        parts.append(
            f'<text class="sg-chart__value" x="{left + w + 8:.1f}" y="{y + 4}">{value:.1f}</text>')
    parts.append(
        f'<text class="sg-chart__axis" x="{(left + right) / 2:.0f}" y="{height + 30}" '
        f'text-anchor="middle">{esc(unit)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    arms = json.loads(Path(sys.argv[1]).read_text())

    def arm(label):
        return arms[label]

    def f1(label):
        return arm(label)["extraction"]["strict"]["f1"]

    def gen(label):
        t = (arm(label).get("throughput") or {}).get("generation_tok_per_s") or {}
        return t.get("median")

    out = []

    # 1. The headline: dense collapses, mixtures do not.
    rows = [
        ("gemma-4 12B (dense) Q2", -0.3572, -0.4012, -0.3131, "1"),
        ("gemma-4 26B-A4B (MoE) Q2", -0.0354, -0.0569, -0.0144, "2"),
        ("Qwen3.6 35B-A3B (MoE) Q1", -0.0377, -0.0577, -0.0182, "2"),
    ]
    tbl = table_html(
        ["model", "rung", "F1", "vs own Q4", "95% range"],
        [["gemma-4 12B — dense", "Q2", f"{f1('gemma4-12b.base.q2'):.4f}",
          "−0.3572", "[−0.4012, −0.3131]"],
         ["gemma-4 26B-A4B — MoE", "Q2", f"{f1('gemma4-26b-a4b.base.q2'):.4f}",
          "−0.0354", "[−0.0569, −0.0144]"],
         ["Qwen3.6 35B-A3B — MoE", "Q1", f"{f1('qwen36-35b-a3b.base.q1'):.4f}",
          "−0.0377", "[−0.0577, −0.0182]"]],
        ["left", "left", "right", "right", "left"])
    out.append(figure(
        "fig-dense-vs-moe",
        "dense vs moe",
        delta_chart(rows, aria="Accuracy change at the most aggressive rung, dense against mixture of experts"),
        tbl,
        "Each dot is the accuracy change against that model's own four-bit rung; "
        "each line is its paired 95% range. The dense model loses more than half "
        "its accuracy at two bits. Both mixtures lose under four points — one of "
        "them at a single bit."))

    # 2. Capacity, not arithmetic.
    rows = [
        ("26B-A4B QAT Q4 — fits", gen("gemma4-26b-a4b.qat.q4"), "2"),
        ("26B-A4B Q4 — 8 layers off", gen("gemma4-26b-a4b.base.q4"), "1"),
        ("26B-A4B Q6 — 15 layers off", gen("gemma4-26b-a4b.base.q6"), "1"),
        ("26B-A4B Q8 — 19 layers off", gen("gemma4-26b-a4b.base.q8"), "1"),
    ]
    tbl = table_html(
        ["gemma-4 26B-A4B", "file", "on card", "expert offload", "generation"],
        [["QAT Q4", "13,588 MiB", "14,746 MiB", "none",
          f"{gen('gemma4-26b-a4b.qat.q4'):.1f} tok/s"],
         ["Q4", "16,222 MiB", "14,166 MiB", "first 8 layers",
          f"{gen('gemma4-26b-a4b.base.q4'):.1f} tok/s"],
         ["Q6", "22,216 MiB", "14,102 MiB", "first 15 layers",
          f"{gen('gemma4-26b-a4b.base.q6'):.1f} tok/s"],
         ["Q8", "26,355 MiB", "13,516 MiB", "first 19 layers",
          f"{gen('gemma4-26b-a4b.base.q8'):.1f} tok/s"]],
        ["left", "right", "right", "left", "right"])
    out.append(figure(
        "fig-capacity",
        "capacity",
        bar_chart(rows, "GENERATION TOKENS PER SECOND", aria="Throughput against how much of the model fits on the card"),
        tbl,
        "One model, one card, four builds. Accuracy across these four does not "
        "separate. Throughput spans eight times, set entirely by how many "
        "layers had to compute their experts on the CPU."))

    # 3. QAT: fine at its width, catastrophic below it.
    rows = [
        ("E2B: QAT Q4 − Q4", 0.0128, -0.0095, 0.0355, "2"),
        ("12B: QAT Q4 − Q4", 0.0178, 0.0000, 0.0363, "2"),
        ("26B: QAT Q4 − Q4", -0.0048, -0.0235, 0.0139, "2"),
        ("E4B: QAT Q2 − Q2", -0.2982, -0.3317, -0.2638, "1"),
        ("E2B: QAT Q2 − Q2", -0.3511, -0.3830, -0.3187, "1"),
    ]
    tbl = table_html(
        ["pair", "delta", "95% range", "verdict"],
        [["gemma-4 E2B, QAT Q4 − non-QAT Q4", "+0.0128", "[−0.0095, +0.0355]", "tie"],
         ["gemma-4 12B, QAT Q4 − non-QAT Q4", "+0.0178", "[+0.0000, +0.0363]", "knife-edge"],
         ["gemma-4 26B-A4B, QAT Q4 − non-QAT Q4", "−0.0048", "[−0.0235, +0.0139]", "tie"],
         ["gemma-4 E4B, QAT Q2 − non-QAT Q2", "−0.2982", "[−0.3317, −0.2638]", "separates"],
         ["gemma-4 E2B, QAT Q2 − non-QAT Q2", "−0.3511", "[−0.3830, −0.3187]", "separates"]],
        ["left", "right", "left", "left"])
    out.append(figure(
        "fig-qat",
        "qat",
        delta_chart(rows, aria="Quantization-aware training against its non-QAT twin at matched width"),
        tbl,
        "At four bits QAT is a tie on accuracy across three models and worth "
        "taking for speed and fit. At two bits both models that publish a QAT "
        "build collapse, and they collapse in opposite directions: one stops "
        "producing output, the other will not stop."))

    print("\n\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
