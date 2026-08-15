---
title: "The Highest Synthesis Score Did Not Settle the Choice"
date: 2026-08-15
author: Rakuen Software
tags: [local-models, synthesis, benchmarks, aimee]
excerpt: "Gemma 4 31B posted the highest observed synthesis score, but was not statistically separated from 12B. The 12B configuration answered 44% sooner and used 59% less GPU memory."
---

*Rakuen builds aimee, whose local synthesis route this benchmark is intended to
choose. We ran every test reported below. The [artifact map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/synthesis-model-selection/evidence/figures.md)
traces each figure to the raw rows and paired analysis.*

Gemma 4 12B is the synthesis model we would deploy from this test. Gemma 4 31B
posted the highest observed content score, **0.3645** against **0.3592**, but its
paired lead was only **+0.0053**, with a 95% range from **-0.0039 to +0.0147**.
The run did not statistically separate them. It does not establish equivalence.

The 12B configuration answered 44% sooner at the median and used 59% less
graphics processing unit (GPU) memory after the run. Gemma 4 E2B is the speed
choice. Its **0.3293** content score was measurably
below 12B by 0.0299 points, but its median request took **0.554 seconds** instead
of **1.335 seconds**. The result leaves two useful configurations, not one
unqualified winner: 12B by default, E2B when latency or memory sets the budget.

## The full ladder leaves two useful choices

All nine configurations ran the same 1,000 cases. The score averages the
required fields in each response. Text and list fields use the harmonic mean of
precision and recall (F1) over token or exact-set overlap; scalar fields use
equality.

Every Gemma row used quantization-aware training (QAT) weights packaged as
Unsloth Dynamic `UD-Q4_K_XL`, called UD-QAT here. Gemma and all three Qwen
configurations used multi-token prediction (MTP); each displayed Qwen row uses
`Q4_K_M`. Muse ran with draft flash (DFlash) off. The server constrained output
with a JavaScript Object Notation (JSON) schema, and the table reports graphics
memory in gibibytes (GiB).

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="synth-ladder" id="synth-ladder-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="synth-ladder" id="synth-ladder-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="synth-ladder-chart">Result</label><label class="sg-figure__tab sg-figure__tab--table" for="synth-ladder-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 292" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Observed content scores for nine synthesis configurations"><line class="sg-chart__grid" x1="220" x2="220" y1="16" y2="266"/><text class="sg-chart__value" x="220" y="284" text-anchor="middle" opacity=".7">0</text><line class="sg-chart__grid" x1="330" x2="330" y1="16" y2="266"/><text class="sg-chart__value" x="330" y="284" text-anchor="middle" opacity=".7">0.1</text><line class="sg-chart__grid" x1="440" x2="440" y1="16" y2="266"/><text class="sg-chart__value" x="440" y="284" text-anchor="middle" opacity=".7">0.2</text><line class="sg-chart__grid" x1="550" x2="550" y1="16" y2="266"/><text class="sg-chart__value" x="550" y="284" text-anchor="middle" opacity=".7">0.3</text><line class="sg-chart__grid" x1="660" x2="660" y1="16" y2="266"/><text class="sg-chart__value" x="660" y="284" text-anchor="middle" opacity=".7">0.4 F1</text><text class="sg-chart__label" x="210" y="36" text-anchor="end">Gemma 4 31B</text><line class="sg-chart__line sg-chart__line--1" x1="220" x2="620.9" y1="32" y2="32"/><circle class="sg-chart__mark sg-chart__mark--1" cx="620.9" cy="32" r="4"/><text class="sg-chart__value" x="628.9" y="36">0.3645</text><text class="sg-chart__label" x="210" y="64" text-anchor="end">Gemma 4 12B</text><line class="sg-chart__line sg-chart__line--1" x1="220" x2="615.1" y1="60" y2="60"/><circle class="sg-chart__mark sg-chart__mark--1" cx="615.1" cy="60" r="4"/><text class="sg-chart__value" x="623.1" y="64">0.3592</text><text class="sg-chart__label" x="210" y="92" text-anchor="end">Qwen3.6 27B</text><line class="sg-chart__line sg-chart__line--muted" x1="220" x2="609.2" y1="88" y2="88"/><circle class="sg-chart__mark sg-chart__mark--muted" cx="609.2" cy="88" r="4"/><text class="sg-chart__value" x="617.2" y="92">0.3538</text><text class="sg-chart__label" x="210" y="120" text-anchor="end">Qwen3.8 27B</text><line class="sg-chart__line sg-chart__line--muted" x1="220" x2="596.0" y1="116" y2="116"/><circle class="sg-chart__mark sg-chart__mark--muted" cx="596.0" cy="116" r="4"/><text class="sg-chart__value" x="604.0" y="120">0.3419</text><text class="sg-chart__label" x="210" y="148" text-anchor="end">Gemma 4 26B-A4B</text><line class="sg-chart__line sg-chart__line--muted" x1="220" x2="584.0" y1="144" y2="144"/><circle class="sg-chart__mark sg-chart__mark--muted" cx="584.0" cy="144" r="4"/><text class="sg-chart__value" x="592.0" y="148">0.3309</text><text class="sg-chart__label" x="210" y="176" text-anchor="end">Qwen3.6 35B-A3B</text><line class="sg-chart__line sg-chart__line--muted" x1="220" x2="583.1" y1="172" y2="172"/><circle class="sg-chart__mark sg-chart__mark--muted" cx="583.1" cy="172" r="4"/><text class="sg-chart__value" x="591.1" y="176">0.3301</text><text class="sg-chart__label" x="210" y="204" text-anchor="end">Gemma 4 E2B</text><line class="sg-chart__line sg-chart__line--2" x1="220" x2="582.2" y1="200" y2="200"/><circle class="sg-chart__mark sg-chart__mark--2" cx="582.2" cy="200" r="4"/><text class="sg-chart__value" x="590.2" y="204">0.3293</text><text class="sg-chart__label" x="210" y="232" text-anchor="end">Gemma 4 E4B</text><line class="sg-chart__line sg-chart__line--muted" x1="220" x2="574.4" y1="228" y2="228"/><circle class="sg-chart__mark sg-chart__mark--muted" cx="574.4" cy="228" r="4"/><text class="sg-chart__value" x="582.4" y="232">0.3222</text><text class="sg-chart__label" x="210" y="260" text-anchor="end">Muse Glimmer 30B</text><line class="sg-chart__line sg-chart__line--muted" x1="220" x2="540.3" y1="256" y2="256"/><circle class="sg-chart__mark sg-chart__mark--muted" cx="540.3" cy="256" r="4"/><text class="sg-chart__value" x="548.3" y="260">0.2912</text></svg><div class="sg-figure__legend"><span><i style="background:var(--sg-chart-1)"></i>top observed pair</span><span><i style="background:var(--sg-chart-2)"></i>speed choice</span><span><i style="background:var(--sg-chart-muted)"></i>other configurations</span></div></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">configuration</th><th style="text-align:right">content F1</th><th style="text-align:right">median</th><th style="text-align:right">95th percentile</th><th style="text-align:right">required fields</th><th style="text-align:right">GPU memory</th></tr></thead><tbody><tr><td style="text-align:left">Gemma 4 31B UD-QAT UD-Q4_K_XL, MTP</td><td style="text-align:right"><strong>0.3645</strong></td><td style="text-align:right">2.367 s</td><td style="text-align:right">4.205 s</td><td style="text-align:right">98.64%</td><td style="text-align:right">20.47 GiB</td></tr><tr><td style="text-align:left">Gemma 4 12B UD-QAT UD-Q4_K_XL, MTP</td><td style="text-align:right">0.3592</td><td style="text-align:right">1.335 s</td><td style="text-align:right">2.301 s</td><td style="text-align:right">100.00%</td><td style="text-align:right">8.38 GiB</td></tr><tr><td style="text-align:left">Qwen3.6 27B Q4_K_M, MTP</td><td style="text-align:right">0.3538</td><td style="text-align:right">2.073 s</td><td style="text-align:right">4.413 s</td><td style="text-align:right">99.93%</td><td style="text-align:right">20.23 GiB</td></tr><tr><td style="text-align:left">Qwen3.8 27B Q4_K_M, MTP</td><td style="text-align:right">0.3419</td><td style="text-align:right">2.218 s</td><td style="text-align:right">4.541 s</td><td style="text-align:right">100.00%</td><td style="text-align:right">20.12 GiB</td></tr><tr><td style="text-align:left">Gemma 4 26B-A4B UD-QAT UD-Q4_K_XL, MTP</td><td style="text-align:right">0.3309</td><td style="text-align:right">0.881 s</td><td style="text-align:right">1.736 s</td><td style="text-align:right">99.99%</td><td style="text-align:right">14.96 GiB</td></tr><tr><td style="text-align:left">Qwen3.6 35B-A3B Q4_K_M, MTP</td><td style="text-align:right">0.3301</td><td style="text-align:right">0.853 s</td><td style="text-align:right">1.803 s</td><td style="text-align:right">99.83%</td><td style="text-align:right">20.51 GiB</td></tr><tr><td style="text-align:left">Gemma 4 E2B UD-QAT UD-Q4_K_XL, MTP</td><td style="text-align:right">0.3293</td><td style="text-align:right"><strong>0.554 s</strong></td><td style="text-align:right">1.084 s</td><td style="text-align:right">100.00%</td><td style="text-align:right"><strong>2.01 GiB</strong></td></tr><tr><td style="text-align:left">Gemma 4 E4B UD-QAT UD-Q4_K_XL, MTP</td><td style="text-align:right">0.3222</td><td style="text-align:right">0.754 s</td><td style="text-align:right">1.426 s</td><td style="text-align:right">99.16%</td><td style="text-align:right">3.38 GiB</td></tr><tr><td style="text-align:left">Muse Glimmer 30B K-Quant 17 GB, DFlash off</td><td style="text-align:right">0.2912</td><td style="text-align:right">10.115 s</td><td style="text-align:right">17.068 s</td><td style="text-align:right">89.46%</td><td style="text-align:right">15.80 GiB</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">The chart shows observed scores, not statistical ranks. Numbers contains the latency, required-field and memory measurements used for selection. GPU memory is the recorded post-run allocation in gibibytes. All three Qwen configurations use Q4_K_M; the pending Qwen3.8 UD-Q4 follow-up is excluded.</figcaption></figure>

The 31B configuration did beat Qwen3.6-27B by 0.0107 points, although the lower
end of the paired range was only 0.0007. The run did not separate 12B from
either 31B or Qwen3.6-27B. It also retained every required field and left about
12 GiB more GPU memory than 31B. The highest point estimate was real; it was not
enough to justify the larger configuration.

At the other end, the run did not separate E2B from E4B, Gemma 4 26B-A4B or
Qwen3.6-35B-A3B. E2B was the fastest of them and occupied the least memory. A
larger model can still be the right speed model when it activates few weights,
but that advantage did not survive this comparison against E2B.

## Paired ranges cut the ladder into decisions

Each range below comes from 10,000 resamples of the same case identifiers. A
range that crosses zero is reported as not statistically separated. That is a
failure to detect a difference, not proof of equivalence. It also does not turn
the models into clean tiers: 31B can remain unseparated from 12B while beating a
third model that 12B also does not separate from.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="synth-paired" id="synth-paired-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="synth-paired" id="synth-paired-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="synth-paired-chart">Paired result</label><label class="sg-figure__tab sg-figure__tab--table" for="synth-paired-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 262" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Selected paired content-score differences with 95 percent bootstrap ranges"><line class="sg-chart__grid" x1="280" x2="280" y1="18" y2="230"/><text class="sg-chart__value" x="280" y="250" text-anchor="middle" opacity=".7">-0.02</text><line class="sg-chart__grid" x1="365" x2="365" y1="18" y2="230"/><text class="sg-chart__value" x="365" y="250" text-anchor="middle">0</text><line class="sg-chart__grid" x1="450" x2="450" y1="18" y2="230"/><text class="sg-chart__value" x="450" y="250" text-anchor="middle" opacity=".7">+0.02</text><line class="sg-chart__grid" x1="535" x2="535" y1="18" y2="230"/><text class="sg-chart__value" x="535" y="250" text-anchor="middle" opacity=".7">+0.04</text><line class="sg-chart__grid" x1="620" x2="620" y1="18" y2="230"/><text class="sg-chart__value" x="620" y="250" text-anchor="middle" opacity=".7">+0.06 F1</text><text class="sg-chart__label" x="266" y="42" text-anchor="end">31B minus 12B</text><line class="sg-chart__line sg-chart__line--muted" x1="348.4" x2="427.4" y1="38" y2="38"/><circle class="sg-chart__mark sg-chart__mark--muted" cx="387.5" cy="38" r="4"/><text class="sg-chart__value" x="640" y="42">NO SEP.</text><text class="sg-chart__label" x="266" y="80" text-anchor="end">12B minus Qwen3.6 27B</text><line class="sg-chart__line sg-chart__line--muted" x1="344.6" x2="430.9" y1="76" y2="76"/><circle class="sg-chart__mark sg-chart__mark--muted" cx="388.0" cy="76" r="4"/><text class="sg-chart__value" x="640" y="80">NO SEP.</text><text class="sg-chart__label" x="266" y="118" text-anchor="end">Qwen3.6 minus Qwen3.8</text><line class="sg-chart__line sg-chart__line--1" x1="374.4" x2="456.8" y1="114" y2="114"/><circle class="sg-chart__mark sg-chart__mark--1" cx="415.6" cy="114" r="4"/><text class="sg-chart__value" x="640" y="118">QWEN3.6</text><text class="sg-chart__label" x="266" y="156" text-anchor="end">26B-A4B minus E2B</text><line class="sg-chart__line sg-chart__line--muted" x1="325.1" x2="419.0" y1="152" y2="152"/><circle class="sg-chart__mark sg-chart__mark--muted" cx="372.2" cy="152" r="4"/><text class="sg-chart__value" x="640" y="156">NO SEP.</text><text class="sg-chart__label" x="266" y="194" text-anchor="end">Qwen3.6 35B minus E2B</text><line class="sg-chart__line sg-chart__line--muted" x1="322.6" x2="413.5" y1="190" y2="190"/><circle class="sg-chart__mark sg-chart__mark--muted" cx="368.4" cy="190" r="4"/><text class="sg-chart__value" x="640" y="194">NO SEP.</text><text class="sg-chart__label" x="266" y="232" text-anchor="end">E2B minus Muse</text><line class="sg-chart__line sg-chart__line--2" x1="472.5" x2="581.8" y1="228" y2="228"/><circle class="sg-chart__mark sg-chart__mark--2" cx="526.9" cy="228" r="4"/><text class="sg-chart__value" x="640" y="232">E2B</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">comparison</th><th style="text-align:right">difference</th><th style="text-align:right">95% paired range</th><th style="text-align:left">result</th></tr></thead><tbody><tr><td style="text-align:left">Gemma 4 31B minus Gemma 4 12B</td><td style="text-align:right">+0.0053</td><td style="text-align:right">-0.0039 to +0.0147</td><td style="text-align:left">not separated</td></tr><tr><td style="text-align:left">Gemma 4 31B minus Qwen3.6 27B</td><td style="text-align:right">+0.0107</td><td style="text-align:right">+0.0007 to +0.0207</td><td style="text-align:left">31B higher</td></tr><tr><td style="text-align:left">Gemma 4 12B minus Qwen3.6 27B</td><td style="text-align:right">+0.0054</td><td style="text-align:right">-0.0048 to +0.0155</td><td style="text-align:left">not separated</td></tr><tr><td style="text-align:left">Gemma 4 12B minus Gemma 4 E2B</td><td style="text-align:right">+0.0299</td><td style="text-align:right">+0.0197 to +0.0401</td><td style="text-align:left">12B higher</td></tr><tr><td style="text-align:left">Qwen3.6 27B minus Qwen3.8 27B</td><td style="text-align:right">+0.0119</td><td style="text-align:right">+0.0022 to +0.0216</td><td style="text-align:left">Qwen3.6 higher</td></tr><tr><td style="text-align:left">Gemma 4 26B-A4B minus Gemma 4 E2B</td><td style="text-align:right">+0.0017</td><td style="text-align:right">-0.0094 to +0.0127</td><td style="text-align:left">not separated</td></tr><tr><td style="text-align:left">Qwen3.6 35B-A3B minus Gemma 4 E2B</td><td style="text-align:right">+0.0008</td><td style="text-align:right">-0.0100 to +0.0114</td><td style="text-align:left">not separated</td></tr><tr><td style="text-align:left">Gemma 4 E2B minus Gemma 4 E4B</td><td style="text-align:right">+0.0070</td><td style="text-align:right">-0.0027 to +0.0166</td><td style="text-align:left">not separated</td></tr><tr><td style="text-align:left">Gemma 4 E2B minus Muse Glimmer 30B</td><td style="text-align:right">+0.0381</td><td style="text-align:right">+0.0253 to +0.0510</td><td style="text-align:left">E2B higher</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">Dots are observed differences. Lines are 95% paired bootstrap ranges. Positive values favour the first configuration named. Numbers gives rounded displayed estimates for every paired comparison used in the text.</figcaption></figure>

The useful separation is between 12B and E2B. The 12B content gain was **+0.0299
points**, with a paired range from **+0.0197 to +0.0401**, while its median
request took 2.41 times as long. That is the tradeoff a deployment can choose.
The smaller movements inside either end of the ladder mostly cannot carry that
decision.

## Qwen3.8 moved backwards on synthesis

Our [fact-extraction head-to-head](https://rakuensoftware.com/blog/local-llm-fact-extraction-head-to-head)
reports Qwen3.8-27B and Qwen3.6-27B as tied because their paired range crosses
zero. The synthesis range does not. Qwen3.6 scored **0.3538** against
**0.3419**, a paired lead of **+0.0119** with a 95% range from **+0.0022 to
+0.0216**.

Qwen3.8 was also 7% slower at the median despite decoding 85.49 tokens per
second against Qwen3.6's 83.75. It produced 136,535 completion tokens across the
suite against Qwen3.6's 122,389. More output consumed the token-speed gain. This
result belongs to synthesis and the tested `Q4_K_M` artifacts; it does not
revise the tie on the other task.

The Qwen3.8 `UD-Q4_K_XL` follow-up is not part of this matrix. Its result should
replace no row until the same paired run is complete.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="synth-output" id="synth-output-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="synth-output" id="synth-output-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="synth-output-chart">Outcome</label><label class="sg-figure__tab sg-figure__tab--table" for="synth-output-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 260" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Output and completeness measurements behind the Qwen3.8 and Muse results"><text class="sg-chart__axis" x="0" y="20">QWEN3.6 27B TO QWEN3.8 27B</text><text class="sg-chart__label" x="250" y="50" text-anchor="end">content score</text><text class="sg-chart__value" x="270" y="50">0.3538 to 0.3419</text><text class="sg-chart__axis" x="650" y="50" text-anchor="end">LOWER</text><text class="sg-chart__label" x="250" y="80" text-anchor="end">completion tokens</text><text class="sg-chart__value" x="270" y="80">122,389 to 136,535</text><text class="sg-chart__axis" x="650" y="80" text-anchor="end">MORE</text><text class="sg-chart__label" x="250" y="110" text-anchor="end">decode rate</text><text class="sg-chart__value" x="270" y="110">83.75 to 85.49 tokens/s</text><text class="sg-chart__axis" x="650" y="110" text-anchor="end">FASTER</text><text class="sg-chart__label" x="250" y="140" text-anchor="end">median request</text><text class="sg-chart__value" x="270" y="140">2.073 to 2.218 seconds</text><text class="sg-chart__axis" x="650" y="140" text-anchor="end">SLOWER</text><text class="sg-chart__axis" x="0" y="180">MUSE GLIMMER</text><text class="sg-chart__label" x="250" y="210" text-anchor="end">valid JSON / required fields</text><text class="sg-chart__value" x="270" y="210">99.90% / 89.46%</text><text class="sg-chart__label" x="250" y="240" text-anchor="end">completion tokens</text><text class="sg-chart__value" x="270" y="240">415,197; next highest 141,295</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">subject</th><th style="text-align:left">measurement</th><th style="text-align:right">comparison</th><th style="text-align:right">reported configuration</th></tr></thead><tbody><tr><td style="text-align:left">Qwen3.8 27B</td><td style="text-align:left">content F1</td><td style="text-align:right">Qwen3.6 27B: 0.3538</td><td style="text-align:right">0.3419</td></tr><tr><td style="text-align:left">Qwen3.8 27B</td><td style="text-align:left">completion tokens</td><td style="text-align:right">Qwen3.6 27B: 122,389</td><td style="text-align:right">136,535</td></tr><tr><td style="text-align:left">Qwen3.8 27B</td><td style="text-align:left">decode rate</td><td style="text-align:right">Qwen3.6 27B: 83.75 tokens/s</td><td style="text-align:right">85.49 tokens/s</td></tr><tr><td style="text-align:left">Qwen3.8 27B</td><td style="text-align:left">median request</td><td style="text-align:right">Qwen3.6 27B: 2.073 s</td><td style="text-align:right">2.218 s</td></tr><tr><td style="text-align:left">Muse Glimmer 30B</td><td style="text-align:left">raw parse rate</td><td style="text-align:right">none</td><td style="text-align:right">99.90%</td></tr><tr><td style="text-align:left">Muse Glimmer 30B</td><td style="text-align:left">schema-valid rate</td><td style="text-align:right">none</td><td style="text-align:right">99.90%</td></tr><tr><td style="text-align:left">Muse Glimmer 30B</td><td style="text-align:left">required-field recall</td><td style="text-align:right">next lowest, Gemma 4 E4B: 99.16%</td><td style="text-align:right">89.46%</td></tr><tr><td style="text-align:left">Muse Glimmer 30B</td><td style="text-align:left">document-summary content F1</td><td style="text-align:right">next lowest, Qwen3.6 35B-A3B: 0.4167</td><td style="text-align:right">0.2026</td></tr><tr><td style="text-align:left">Muse Glimmer 30B</td><td style="text-align:left">completion tokens</td><td style="text-align:right">next highest, Gemma 4 E2B: 141,295</td><td style="text-align:right">415,197</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">The Qwen rows compare the two dense 27B Q4_K_M configurations on the same cases. Muse's comparison cells name the next-lowest or next-highest non-Muse result; they do not use one common baseline.</figcaption></figure>

## Muse returned valid objects with missing content

Muse Glimmer earned its place in the matrix after running near the
fact-extraction article's leaders. On synthesis it finished last at **0.2912**,
and E2B beat it by 0.0381 points with the paired range clear of zero.

The failure was not mainly JSON syntax. Muse parsed and met the schema on 99.9%
of cases, but its required-field recall fell to **89.46%**. Its document-summary
score was **0.2026**, less than half the next-lowest configuration's 0.4167. A
valid object can still be an incomplete answer.

The serving cost moved in the same direction. Muse generated 415,197 completion
tokens, 2.94 times E2B's next-highest total of 141,295, and took **10.115
seconds** at the median. We ran the vendor-supported low reasoning setting
because the [Muse
Glimmer model card](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF),
read on August 14, 2026, says reasoning cannot be switched off.

DFlash remained off. That may not be Muse's best possible prompt,
but it is the measured configuration and it does not fit this synthesis route.

## One matched GPU isolates the serving decision

Between August 14 and 15, 2026, one AMD Radeon RX 7900 XTX served every
configuration through the same `llama.cpp` build. Each used one slot, one
worker, an 8,192-token context, temperature zero and strict JSON-schema output.
All nine completed 1,000 requests without a transport failure or retry.

Every Gemma target used the UD-QAT artifact described above. Gemma 4 and both
Qwen families used MTP. The Qwen targets used `Q4_K_M`. Muse used its 17 GB
K-Quant target without DFlash.

These are production-oriented serving configurations, not isolated tests of
model architecture or parameter count.

The cases are a deterministic 1,000-case subset of a frozen 10,000-case suite
covering five structured synthesis tasks. Their expected outputs are
de-identified silver labels from committed aimee artifacts and source
citations. They support paired selection on this suite, not an estimate of
human-audited absolute quality.

One card and fixed model order also make the latency figures descriptive. The
content ranges use paired case resampling; timing has no repeated-run interval.
The raw rows, model files, load profile, hashes, scorer, seed and 10,000
bootstrap replicates are recorded in the artifact map.

## Use 12B unless latency is the budget

Use Gemma 4 12B as the default synthesis configuration on this 24 GB GPU tier.
The run did not show a 31B content gain large enough to outweigh its latency and
memory cost. Use E2B when a 1.335-second median is already too slow and accept
the measured 0.0299-point content loss.

Do not pay for 31B, Qwen3.8 or Muse from this matrix. The run did not separate
31B from 12B; the other two lost their relevant paired comparisons. Rerun the
decision when the labels become human-audited or the production request shape
changes.
