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

The intervals used to be typed into this file as literal strings, twice per
comparison -- once in the chart tuple and once in the table cell -- which made
the promise above false for exactly the numbers that matter most. The QAT figure
drifted that way: its caption and verdict column went on asserting a tie after
the prose beside it had been corrected. They are now read from
`evidence/campaign-results/{extraction,synthesis}-pairs-*.json`, so a figure
cannot state an interval no bootstrap produced.

Usage:
    build_figures.py <results.json> [pairs-dir] > figures.html
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


MINUS = "\u2212"


def fmt_delta(v: float) -> str:
    """Signed to four places, using the typographic minus the article uses."""
    return f"+{v:.4f}" if v >= 0 else f"{MINUS}{abs(v):.4f}"


def fmt_range(lo: float, hi: float) -> str:
    return f"[{fmt_delta(lo)}, {fmt_delta(hi)}]"


def load_pairs(pairs_dir: Path) -> dict:
    """(task, baseline, comparison) -> row, from the vendored pair evidence."""
    table: dict = {}
    for task, pattern in (("extraction", "extraction-pairs-*.json"),
                          ("synthesis", "synthesis-pairs-*.json")):
        for path in sorted(pairs_dir.glob(pattern)):
            for row in json.loads(path.read_text()):
                if row.get("error"):
                    continue
                table[(task, row["baseline"], row["comparison"])] = row
    if not table:
        raise SystemExit(f"no pair evidence found under {pairs_dir}")
    return table


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    results = Path(sys.argv[1])
    arms = json.loads(results.read_text())
    arms = {k: v for k, v in arms.items() if not k.startswith("_")}
    pairs_dir = Path(sys.argv[2]) if len(sys.argv) == 3 else results.parent
    pair_rows = load_pairs(pairs_dir)

    def pair(baseline, comparison, task="extraction"):
        """delta, lo, hi for a measured pair, in the direction asked for.

        A pair is stored once. Asking for it the other way round negates the
        delta and swaps the reversed endpoints, which is the same measurement
        read from the other side.
        """
        row = pair_rows.get((task, baseline, comparison))
        if row is not None:
            lo, hi = row["paired_bootstrap_95_range"]
            return row["comparison_minus_baseline"], lo, hi
        row = pair_rows.get((task, comparison, baseline))
        if row is None:
            raise SystemExit(
                f"no {task} pair for {comparison} vs {baseline}; "
                "run the sweep before rebuilding figures")
        lo, hi = row["paired_bootstrap_95_range"]
        return -row["comparison_minus_baseline"], -hi, -lo

    def verdict(baseline, comparison, task="extraction"):
        d, lo, hi = pair(baseline, comparison, task)
        return "separates" if (lo > 0 or hi < 0) else "tie"

    def arm(label):
        return arms[label]

    def f1(label):
        return arm(label)["extraction"]["strict"]["f1"]

    def gen(label):
        t = (arm(label).get("throughput") or {}).get("generation_tok_per_s") or {}
        return t.get("median")

    out = []

    # 1. The headline: dense collapses, mixtures do not.
    headline = [
        ("gemma-4 12B (dense) Q2", "gemma-4 12B — dense", "Q2",
         "gemma4-12b.base.q4", "gemma4-12b.base.q2", "1"),
        ("gemma-4 26B-A4B (MoE) Q2", "gemma-4 26B-A4B — MoE", "Q2",
         "gemma4-26b-a4b.base.q4", "gemma4-26b-a4b.base.q2", "2"),
        ("Qwen3.6 35B-A3B (MoE) Q1", "Qwen3.6 35B-A3B — MoE", "Q1",
         "qwen36-35b-a3b.base.q4", "qwen36-35b-a3b.base.q1", "2"),
    ]
    rows = []
    trows = []
    for chart_label, table_label, rung, base, comp, series in headline:
        d, lo, hi = pair(base, comp)
        rows.append((chart_label, d, lo, hi, series))
        trows.append([table_label, rung, f"{f1(comp):.4f}",
                      fmt_delta(d), fmt_range(lo, hi)])
    tbl = table_html(
        ["model", "rung", "F1", "vs own Q4", "95% range"],
        trows,
        ["left", "left", "right", "right", "left"])
    out.append(figure(
        "fig-dense-vs-moe",
        "dense vs moe",
        delta_chart(rows, aria="Accuracy change at the most aggressive rung, dense against mixture of experts"),
        tbl,
        "Each dot is the accuracy change against that model's own four-bit rung; "
        "each line is its paired 95% range. The dense model loses more than half "
        "its accuracy at two bits. Both mixtures lose under four points, one of "
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
    qat = [
        ("E2B: QAT Q4 − Q4", "gemma-4 E2B, QAT Q4 − non-QAT Q4",
         "gemma4-e2b.base.q4", "gemma4-e2b.qat.q4", "2"),
        ("E4B: QAT Q4 − Q4", "gemma-4 E4B, QAT Q4 − non-QAT Q4",
         "gemma4-e4b.base.q4", "gemma4-e4b.qat.q4", "2"),
        ("12B: QAT Q4 − Q4", "gemma-4 12B, QAT Q4 − non-QAT Q4",
         "gemma4-12b.base.q4", "gemma4-12b.qat.q4", "2"),
        ("26B: QAT Q4 − Q4", "gemma-4 26B-A4B, QAT Q4 − non-QAT Q4",
         "gemma4-26b-a4b.base.q4", "gemma4-26b-a4b.qat.q4", "2"),
        ("E4B: QAT Q2 − Q2", "gemma-4 E4B, QAT Q2 − non-QAT Q2",
         "gemma4-e4b.base.q2", "gemma4-e4b.qat.q2", "1"),
        ("E2B: QAT Q2 − Q2", "gemma-4 E2B, QAT Q2 − non-QAT Q2",
         "gemma4-e2b.base.q2", "gemma4-e2b.qat.q2", "1"),
    ]
    rows = []
    trows = []
    for chart_label, table_label, base, comp, series in qat:
        d, lo, hi = pair(base, comp)
        rows.append((chart_label, d, lo, hi, series))
        # A pair that ties on extraction may still resolve on synthesis. The
        # 12B QAT Q4 pair does, and showing only the extraction verdict is what
        # let this figure go on contradicting the section it sits in.
        v = verdict(base, comp)
        if v == "tie":
            try:
                if verdict(base, comp, "synthesis") == "separates":
                    v = "separates on synthesis"
            except SystemExit:
                pass
        trows.append([table_label, fmt_delta(d), fmt_range(lo, hi), v])
    tbl = table_html(
        ["pair", "delta", "95% range", "verdict"],
        trows,
        ["left", "right", "left", "left"])
    out.append(figure(
        "fig-qat",
        "qat",
        delta_chart(rows, aria="Quantization-aware training against its non-QAT twin at matched width"),
        tbl,
        "At four bits QAT is a tie on accuracy for three of the four models and "
        "worth taking for speed and fit; the 12B separates on synthesis. At two "
        "bits both models that publish a QAT build collapse, and they collapse "
        "in opposite directions: one stops producing output, the other will "
        "not stop."))

    print("\n\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
