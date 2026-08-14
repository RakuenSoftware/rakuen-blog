#!/usr/bin/env python3
"""Insert the Qwen3.8 Q4_K_M result into the published article figures."""

from __future__ import annotations

import html
import re
from pathlib import Path


ARTICLE = Path(__file__).resolve().parents[4] / "article" / "local-llm-fact-extraction-head-to-head.md"

Q38_FULL_ROW = (
    '<tr><td style="text-align:left">Qwen3.8-27B</td>'
    '<td style="text-align:left">Q4_K_M, MTP</td>'
    '<td style="text-align:right">0.7030</td>'
    '<td style="text-align:right">0.6463</td>'
    '<td style="text-align:right">0.7705</td>'
    '<td style="text-align:right">1.00</td>'
    '<td style="text-align:right">0.655</td>'
    '<td style="text-align:right">113</td>'
    '<td style="text-align:right">1.00</td></tr>'
)

Q38_SCATTER_ROW = (
    '<tr><td style="text-align:left">Qwen3.8-27B</td>'
    '<td style="text-align:left">Q4_K_M, MTP</td>'
    '<td style="text-align:right">0.7030</td>'
    '<td style="text-align:right">113</td></tr>'
)

Q38_THROUGHPUT_ROW = (
    '<tr><td style="text-align:left">Qwen3.8-27B Q4_K_M, MTP</td>'
    '<td style="text-align:right">72.1</td>'
    '<td style="text-align:left">RX 7900 XTX</td></tr>'
)


def one(pattern: str, text: str) -> re.Match[str]:
    matches = list(re.finditer(pattern, text, re.S))
    if len(matches) != 1:
        raise RuntimeError(f"expected one match for {pattern!r}, found {len(matches)}")
    return matches[0]


def figure_with(text: str, marker: str) -> tuple[re.Match[str], str]:
    matches = [
        match
        for match in re.finditer(r'<figure class="sg-figure">.*?</figure>', text, re.S)
        if marker in match.group(0)
    ]
    if len(matches) != 1:
        raise RuntimeError(f"expected one figure containing {marker!r}, found {len(matches)}")
    return matches[0], matches[0].group(0)


def cells(row: str) -> list[str]:
    return [
        html.unescape(re.sub(r"<.*?>", "", value)).strip()
        for value in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.S)
    ]


def replace_figure(text: str, match: re.Match[str], figure: str) -> str:
    return text[: match.start()] + figure + text[match.end() :]


def update_ranked_figure(text: str) -> str:
    match, figure = figure_with(text, "Ranked values, one row per run")
    if "Qwen3.8-27B</td>" in figure:
        raise RuntimeError("Qwen3.8 already appears in the main figure")

    muse = one(
        r'<tr><td style="text-align:left">Muse Glimmer 30B</td>.*?</tr>',
        figure,
    )
    figure = figure[: muse.end()] + Q38_FULL_ROW + figure[muse.end() :]

    table = one(r"<table>.*?</table>", figure).group(0)
    parsed = [cells(row) for row in re.findall(r"<tr>(.*?)</tr>", table, re.S)][1:]
    if len(parsed) != 34:
        raise RuntimeError(f"expected 34 main-table rows, found {len(parsed)}")

    n = len(parsed)
    svg = [
        f'<svg class="sg-chart" viewBox="0 0 760 {58 + 15 * n}" '
        'preserveAspectRatio="xMidYMid meet" role="img" '
        'aria-label="Ranked values, one row per run">'
    ]
    for x, label in ((342.5, "0.2"), (461.0, "0.39"), (579.5, "0.58")):
        svg.append(
            f'<line class="sg-chart__grid" x1="{x:.1f}" x2="{x:.1f}" '
            f'y1="16" y2="{28 + 15 * n}"/>'
        )
        svg.append(
            f'<text class="sg-chart__value" x="{x:.1f}" y="{44 + 15 * n}" '
            f'text-anchor="middle" opacity=".7">{label}</text>'
        )

    for index, row in enumerate(parsed):
        model, quant, value = row[0], row[1], float(row[2])
        label = f"{model} {quant}"
        y_line = 31.5 + 15 * index
        y_text = 35.0 + 15 * index
        x = 223.98126990020572 + 607.7325019930572 * value
        style = "1" if index < 4 else ("2" if model == "granite-4.1-3b" else "muted")
        svg.extend(
            [
                f'<text class="sg-chart__label" x="214" y="{y_text:.1f}" '
                f'text-anchor="end" font-size="11">{label}</text>',
                f'<line class="sg-chart__line sg-chart__line--{style}" x1="224.0" '
                f'x2="{x:.1f}" y1="{y_line:.1f}" y2="{y_line:.1f}"/>',
                f'<circle class="sg-chart__mark sg-chart__mark--{style}" '
                f'cx="{x:.1f}" cy="{y_line:.1f}" r="3.6"/>',
                f'<text class="sg-chart__value" x="{x + 8:.1f}" '
                f'y="{y_text:.1f}">{value:.4f}</text>',
            ]
        )
    svg.append("</svg>")

    ranked = one(
        r'(<div class="sg-figure__pane sg-figure__pane--ranked">)'
        r'<svg.*?</svg>',
        figure,
    )
    figure = (
        figure[: ranked.start()]
        + ranked.group(1)
        + "".join(svg)
        + figure[ranked.end() :]
    )
    return replace_figure(text, match, figure)


def update_throughput_figure(text: str) -> str:
    match, figure = figure_with(text, "Magnitude per run")
    if "Qwen3.8-27B Q4_K_M" in figure:
        raise RuntimeError("Qwen3.8 already appears in the throughput figure")

    body = one(r"<tbody>(.*?)</tbody>", figure).group(1)
    rows = re.findall(r"<tr>.*?</tr>", body, re.S)
    rows.append(Q38_THROUGHPUT_ROW)
    rows.sort(key=lambda row: float(cells(row)[1]), reverse=True)
    figure = re.sub(r"<tbody>.*?</tbody>", "<tbody>" + "".join(rows) + "</tbody>", figure, count=1, flags=re.S)

    parsed = [cells(row) for row in rows]
    n = len(parsed)
    svg = [
        f'<svg class="sg-chart" viewBox="0 0 760 {60 + 34 * n}" '
        'preserveAspectRatio="xMidYMid meet" role="img" aria-label="Magnitude per run">'
    ]
    for x, label in ((336.6, "102"), (463.2, "204"), (589.8, "306")):
        svg.append(
            f'<line class="sg-chart__grid" x1="{x:.1f}" x2="{x:.1f}" '
            f'y1="16" y2="{28 + 34 * n}"/>'
        )
        svg.append(
            f'<text class="sg-chart__value" x="{x:.1f}" y="{44 + 34 * n}" '
            f'text-anchor="middle" opacity=".7">{label}</text>'
        )
    for index, (model, value_text, gpu) in enumerate(parsed):
        value = float(value_text)
        y = 45.0 + 34 * index
        width = 401.0 / 323.1 * value
        style = "1" if index == 0 else "muted"
        svg.extend(
            [
                f'<text class="sg-chart__label" x="198" y="{y:.1f}" '
                f'text-anchor="end">{model}</text>',
                f'<rect class="sg-chart__mark sg-chart__mark--{style}" x="210.0" '
                f'y="{y - 8.5:.1f}" width="{width:.1f}" height="9" rx="4"/>',
                f'<text class="sg-chart__value" x="{219 + width:.1f}" '
                f'y="{y:.1f}">{value:.1f}</text>',
                f'<text class="sg-chart__value" x="686" y="{y:.1f}" '
                f'opacity=".7">{gpu}</text>',
            ]
        )
    svg.append(
        f'<text class="sg-chart__axis" x="421.0" y="{54 + 34 * n}" '
        'text-anchor="middle">TOKENS PER SECOND</text></svg>'
    )
    old_svg = one(r"<svg.*?</svg>", figure)
    figure = figure[: old_svg.start()] + "".join(svg) + figure[old_svg.end() :]
    return replace_figure(text, match, figure)


def update_scatter_figure(text: str) -> str:
    match, figure = figure_with(text, "strict f1 against invented triples")
    if "Qwen3.8-27B</td>" in figure:
        raise RuntimeError("Qwen3.8 already appears in the scatter figure")

    muse = one(
        r'<tr><td style="text-align:left">Muse Glimmer 30B</td>.*?</tr>',
        figure,
    )
    figure = figure[: muse.end()] + Q38_SCATTER_ROW + figure[muse.end() :]

    point = (
        '<circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" '
        'cx="656.0" cy="254.7" r="6"><title>'
        'Qwen3.8-27B Q4_K_M, MTP</title></circle>'
    )
    labels = one(r'<text class="sg-chart__label" x="686\.3"', figure)
    figure = figure[: labels.start()] + point + figure[labels.start() :]
    return replace_figure(text, match, figure)


def main() -> None:
    text = ARTICLE.read_text(encoding="utf-8")
    text = update_ranked_figure(text)
    text = update_throughput_figure(text)
    text = update_scatter_figure(text)
    ARTICLE.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
