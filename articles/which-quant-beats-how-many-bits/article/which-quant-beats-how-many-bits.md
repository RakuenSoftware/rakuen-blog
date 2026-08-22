---
title: "Quantization Barely Mattered Until Two Bits"
date: 2026-08-22
author: Rakuen Software
tags: [quantization, local-models, benchmarks, aimee]
excerpt: "Thirty-seven runs, seven models, two tasks, one RTX 5080. Thirty of forty-five accuracy comparisons did not separate. The ones that did are almost all below four bits, where dense models pay roughly five times what mixtures pay and a quantization-aware build is the worst thing you can touch. Speed moved far more than accuracy, and it moved on whether the file fit."
draft: true
---

*Rakuen builds aimee, the system measured here. Every figure below is traceable
through the [measurement log](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/which-quant-beats-how-many-bits/evidence/moe-ladder-measurement-log-2026-08-16.md),
which also records the harness defects found while producing them. Several would
have put wrong numbers in this article, and two of them did before being caught.*

Thirty-seven runs, seven models, two tasks, one card. That is 45 paired accuracy
comparisons on 1,001-note fact extraction and 44 on a 1,000-case synthesis
fixture.

**Thirty of the 45 do not separate.** Fifteen do, six of those are large, and
every one of the six is below four bits. Above four bits, the largest difference
that resolved anywhere in the campaign is **0.038**.

Bit width mostly did not decide accuracy. It decided two things: what happens to
a dense model below four bits, and how fast the model runs.

## System under test

We ran everything below on one machine, one card, one build. Nothing is compared
across hosts.

| | |
|---|---|
| GPU | NVIDIA RTX 5080, 16,303 MiB, roughly 15,600 MiB usable, compute capability 12.0 |
| Driver | 610.43.02 |
| Host | 16 threads, 96 GiB RAM, Ubuntu 24.04, kernel 7.0.14-4-pve |
| Server | llama.cpp version 1 (`f9e832c`), CUDA 13, compiled `sm_120a` with no PTX fallback |
| Serving | `-ngl 99 -np 1 -c 8192 --cache-ram 1024 -ctk f16 -ctv f16`, multi-token prediction where the model publishes a draft |
| Offload | `-ncmoe N` tuned per run to the smallest N that fits, never `-cmoe` |
| Extraction | 1,001 notes, corpus v5, scored strictly with false positives counted against the model |
| Synthesis | 1,000-case frozen fixture, mean content F1 |
| Intervals | paired bootstrap, seed `20260809`, 20,000 replicates on extraction and 5,000 on synthesis |

A comparison *separates* when its paired 95% range excludes zero.
*Indistinguishable* means the range includes zero, which is not the same as
equal: 1,001 notes could not tell the two apart. Score tables are point
estimates, so read differences from the comparison tables, never by subtracting
two cells.

## Below four bits, dense models pay and mixtures shrug

Every rung below four bits that is not a quantization-aware training (QAT)
build, measured against its own model's Q4:

| model | architecture | rung | delta | 95% range |
|---|---|---|---:|---|
| gemma-4 12B | dense | Q2 | −0.3572 | [−0.4012, −0.3131] |
| gemma-4 E2B | dense | Q2 | −0.0691 | [−0.0969, −0.0414] |
| Qwen3.6 35B-A3B | MoE | Q1 | −0.0377 | [−0.0577, −0.0182] |
| gemma-4 26B-A4B | MoE | Q2 | −0.0354 | [−0.0569, −0.0144] |
| gemma-4 E4B | dense | Q2 | −0.0325 | [−0.0576, −0.0081] |
| Qwen3.6 35B-A3B | MoE | Q2 | −0.0194 | [−0.0355, −0.0031] |

All six separate. The dense mean is **0.153** against **0.031** for the
mixtures, and the worst dense case is **9.5x** the worst mixture. No mixture
loses more than four points, including at a single bit.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-dense-vs-moe" id="fig-dense-vs-moe-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-dense-vs-moe" id="fig-dense-vs-moe-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-dense-vs-moe-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-dense-vs-moe-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 160" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Accuracy change at the most aggressive rung, dense against mixture of experts"><line class="sg-chart__grid" x1="275.0" x2="275.0" y1="14" y2="120"/><text class="sg-chart__value" x="275.0" y="138" text-anchor="middle" opacity=".7">-0.4</text><line class="sg-chart__grid" x1="325.0" x2="325.0" y1="14" y2="120"/><text class="sg-chart__value" x="325.0" y="138" text-anchor="middle" opacity=".7">-0.3</text><line class="sg-chart__grid" x1="375.0" x2="375.0" y1="14" y2="120"/><text class="sg-chart__value" x="375.0" y="138" text-anchor="middle" opacity=".7">-0.2</text><line class="sg-chart__grid" x1="425.0" x2="425.0" y1="14" y2="120"/><text class="sg-chart__value" x="425.0" y="138" text-anchor="middle" opacity=".7">-0.1</text><line class="sg-chart__rule" x1="475.0" x2="475.0" y1="14" y2="120"/><text class="sg-chart__value" x="475.0" y="138" text-anchor="middle" opacity=".7">no change</text><line class="sg-chart__grid" x1="525.0" x2="525.0" y1="14" y2="120"/><text class="sg-chart__value" x="525.0" y="138" text-anchor="middle" opacity=".7">+0.1</text><text class="sg-chart__label" x="238" y="36" text-anchor="end" font-size="11">gemma-4 12B (dense) Q2</text><line class="sg-chart__line sg-chart__line--1" x1="274.4" x2="318.5" y1="32" y2="32"/><line class="sg-chart__line sg-chart__line--1" x1="274.4" x2="274.4" y1="28" y2="36"/><line class="sg-chart__line sg-chart__line--1" x1="318.5" x2="318.5" y1="28" y2="36"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="296.4" cy="32" r="4"/><text class="sg-chart__value" x="708" y="36">-0.3572</text><text class="sg-chart__label" x="238" y="66" text-anchor="end" font-size="11">gemma-4 26B-A4B (MoE) Q2</text><line class="sg-chart__line sg-chart__line--2" x1="446.5" x2="467.8" y1="62" y2="62"/><line class="sg-chart__line sg-chart__line--2" x1="446.5" x2="446.5" y1="58" y2="66"/><line class="sg-chart__line sg-chart__line--2" x1="467.8" x2="467.8" y1="58" y2="66"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="457.3" cy="62" r="4"/><text class="sg-chart__value" x="708" y="66">-0.0354</text><text class="sg-chart__label" x="238" y="96" text-anchor="end" font-size="11">Qwen3.6 35B-A3B (MoE) Q1</text><line class="sg-chart__line sg-chart__line--2" x1="446.1" x2="465.9" y1="92" y2="92"/><line class="sg-chart__line sg-chart__line--2" x1="446.1" x2="446.1" y1="88" y2="96"/><line class="sg-chart__line sg-chart__line--2" x1="465.9" x2="465.9" y1="88" y2="96"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="456.1" cy="92" r="4"/><text class="sg-chart__value" x="708" y="96">-0.0377</text><text class="sg-chart__axis" x="475" y="156" text-anchor="middle">STRICT F1 CHANGE, WITH 95% RANGE</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">model</th><th style="text-align:left">rung</th><th style="text-align:right">F1</th><th style="text-align:right">vs own Q4</th><th style="text-align:left">95% range</th></tr></thead><tbody><tr><td style="text-align:left">gemma-4 12B — dense</td><td style="text-align:left">Q2</td><td style="text-align:right">0.3182</td><td style="text-align:right">−0.3572</td><td style="text-align:left">[−0.4012, −0.3131]</td></tr><tr><td style="text-align:left">gemma-4 26B-A4B — MoE</td><td style="text-align:left">Q2</td><td style="text-align:right">0.6498</td><td style="text-align:right">−0.0354</td><td style="text-align:left">[−0.0569, −0.0144]</td></tr><tr><td style="text-align:left">Qwen3.6 35B-A3B — MoE</td><td style="text-align:left">Q1</td><td style="text-align:right">0.6817</td><td style="text-align:right">−0.0377</td><td style="text-align:left">[−0.0577, −0.0182]</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">Each dot is the accuracy change against that model&#x27;s own four-bit rung; each line is its paired 95% range. The dense model loses more than half its accuracy at two bits. Both mixtures lose under four points, one of them at a single bit.</figcaption></figure>

Qwen3.6-35B-A3B at one bit scores **0.6817**, higher than every gemma-4 run in
this campaign at any width, including full four-bit builds.

The ordering is not clean and the gap is not a law. gemma-4 E4B is dense and
loses less than either mixture, so the aggregate is carried by the 12B. What the
data supports is that the catastrophic case was dense and no mixture had one,
not that every dense model is fragile.

The 12B also loses its output discipline at two bits. It generates faster than
any other rung on its own ladder and takes two and a half times as long to
finish, because it emits a median of **7,609 tokens per note against 958**.

## Quantization-aware training is the exception that inverts

At four bits QAT is a tie on three of four models, worth taking because it is
faster and at 26B decides whether the model fits at all. The 12B is the
exception, positive on both tasks and separating on synthesis at **+0.0088
[+0.0015, +0.0164]**. Below the width it ships for, QAT is the worst thing
measured anywhere in this campaign.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-qat" id="fig-qat-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-qat" id="fig-qat-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-qat-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-qat-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 310" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Quantization-aware training against its non-QAT twin at matched width"><line class="sg-chart__grid" x1="275.0" x2="275.0" y1="14" y2="270"/><text class="sg-chart__value" x="275.0" y="288" text-anchor="middle" opacity=".7">-0.4</text><line class="sg-chart__grid" x1="325.0" x2="325.0" y1="14" y2="270"/><text class="sg-chart__value" x="325.0" y="288" text-anchor="middle" opacity=".7">-0.3</text><line class="sg-chart__grid" x1="375.0" x2="375.0" y1="14" y2="270"/><text class="sg-chart__value" x="375.0" y="288" text-anchor="middle" opacity=".7">-0.2</text><line class="sg-chart__grid" x1="425.0" x2="425.0" y1="14" y2="270"/><text class="sg-chart__value" x="425.0" y="288" text-anchor="middle" opacity=".7">-0.1</text><line class="sg-chart__rule" x1="475.0" x2="475.0" y1="14" y2="270"/><text class="sg-chart__value" x="475.0" y="288" text-anchor="middle" opacity=".7">no change</text><line class="sg-chart__grid" x1="525.0" x2="525.0" y1="14" y2="270"/><text class="sg-chart__value" x="525.0" y="288" text-anchor="middle" opacity=".7">+0.1</text><text class="sg-chart__label" x="238" y="36" text-anchor="end" font-size="11">E2B: QAT Q4 − Q4</text><line class="sg-chart__line sg-chart__line--2" x1="470.2" x2="492.8" y1="32" y2="32"/><line class="sg-chart__line sg-chart__line--2" x1="470.2" x2="470.2" y1="28" y2="36"/><line class="sg-chart__line sg-chart__line--2" x1="492.8" x2="492.8" y1="28" y2="36"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="481.4" cy="32" r="4"/><text class="sg-chart__value" x="708" y="36">+0.0128</text><text class="sg-chart__label" x="238" y="66" text-anchor="end" font-size="11">E4B: QAT Q4 − Q4</text><line class="sg-chart__line sg-chart__line--2" x1="467.5" x2="485.8" y1="62" y2="62"/><line class="sg-chart__line sg-chart__line--2" x1="467.5" x2="467.5" y1="58" y2="66"/><line class="sg-chart__line sg-chart__line--2" x1="485.8" x2="485.8" y1="58" y2="66"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="476.6" cy="62" r="4"/><text class="sg-chart__value" x="708" y="66">+0.0033</text><text class="sg-chart__label" x="238" y="96" text-anchor="end" font-size="11">12B: QAT Q4 − Q4</text><line class="sg-chart__line sg-chart__line--2" x1="475.0" x2="493.1" y1="92" y2="92"/><line class="sg-chart__line sg-chart__line--2" x1="475.0" x2="475.0" y1="88" y2="96"/><line class="sg-chart__line sg-chart__line--2" x1="493.1" x2="493.1" y1="88" y2="96"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="483.9" cy="92" r="4"/><text class="sg-chart__value" x="708" y="96">+0.0178</text><text class="sg-chart__label" x="238" y="126" text-anchor="end" font-size="11">26B: QAT Q4 − Q4</text><line class="sg-chart__line sg-chart__line--2" x1="463.2" x2="482.0" y1="122" y2="122"/><line class="sg-chart__line sg-chart__line--2" x1="463.2" x2="463.2" y1="118" y2="126"/><line class="sg-chart__line sg-chart__line--2" x1="482.0" x2="482.0" y1="118" y2="126"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="472.6" cy="122" r="4"/><text class="sg-chart__value" x="708" y="126">-0.0048</text><text class="sg-chart__label" x="238" y="156" text-anchor="end" font-size="11">E4B: QAT Q2 − Q2</text><line class="sg-chart__line sg-chart__line--1" x1="309.1" x2="343.1" y1="152" y2="152"/><line class="sg-chart__line sg-chart__line--1" x1="309.1" x2="309.1" y1="148" y2="156"/><line class="sg-chart__line sg-chart__line--1" x1="343.1" x2="343.1" y1="148" y2="156"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="325.9" cy="152" r="4"/><text class="sg-chart__value" x="708" y="156">-0.2982</text><text class="sg-chart__label" x="238" y="186" text-anchor="end" font-size="11">E2B: QAT Q2 − Q2</text><line class="sg-chart__line sg-chart__line--1" x1="283.5" x2="315.7" y1="182" y2="182"/><line class="sg-chart__line sg-chart__line--1" x1="283.5" x2="283.5" y1="178" y2="186"/><line class="sg-chart__line sg-chart__line--1" x1="315.7" x2="315.7" y1="178" y2="186"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="299.4" cy="182" r="4"/><text class="sg-chart__value" x="708" y="186">-0.3511</text><text class="sg-chart__label" x="238" y="216" text-anchor="end" font-size="11">E4B: QAT Q2 − QAT Q4</text><line class="sg-chart__line sg-chart__line--1" x1="291.5" x2="324.1" y1="212" y2="212"/><line class="sg-chart__line sg-chart__line--1" x1="291.5" x2="291.5" y1="208" y2="216"/><line class="sg-chart__line sg-chart__line--1" x1="324.1" x2="324.1" y1="208" y2="216"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="307.9" cy="212" r="4"/><text class="sg-chart__value" x="708" y="216">-0.3341</text><text class="sg-chart__label" x="238" y="246" text-anchor="end" font-size="11">E2B: QAT Q2 − QAT Q4</text><line class="sg-chart__line sg-chart__line--1" x1="242.9" x2="274.0" y1="242" y2="242"/><line class="sg-chart__line sg-chart__line--1" x1="242.9" x2="242.9" y1="238" y2="246"/><line class="sg-chart__line sg-chart__line--1" x1="274.0" x2="274.0" y1="238" y2="246"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="258.5" cy="242" r="4"/><text class="sg-chart__value" x="708" y="246">-0.4330</text><text class="sg-chart__axis" x="475" y="306" text-anchor="middle">STRICT F1 CHANGE, WITH 95% RANGE</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">pair</th><th style="text-align:right">delta</th><th style="text-align:left">95% range</th><th style="text-align:left">verdict</th></tr></thead><tbody><tr><td style="text-align:left">gemma-4 E2B, QAT Q4 − non-QAT Q4</td><td style="text-align:right">+0.0128</td><td style="text-align:left">[−0.0095, +0.0355]</td><td style="text-align:left">tie</td></tr><tr><td style="text-align:left">gemma-4 E4B, QAT Q4 − non-QAT Q4</td><td style="text-align:right">+0.0033</td><td style="text-align:left">[−0.0149, +0.0215]</td><td style="text-align:left">tie</td></tr><tr><td style="text-align:left">gemma-4 12B, QAT Q4 − non-QAT Q4</td><td style="text-align:right">+0.0178</td><td style="text-align:left">[+0.0000, +0.0363]</td><td style="text-align:left">separates on synthesis</td></tr><tr><td style="text-align:left">gemma-4 26B-A4B, QAT Q4 − non-QAT Q4</td><td style="text-align:right">−0.0048</td><td style="text-align:left">[−0.0235, +0.0139]</td><td style="text-align:left">tie</td></tr><tr><td style="text-align:left">gemma-4 E4B, QAT Q2 − non-QAT Q2</td><td style="text-align:right">−0.2982</td><td style="text-align:left">[−0.3317, −0.2638]</td><td style="text-align:left">separates</td></tr><tr><td style="text-align:left">gemma-4 E2B, QAT Q2 − non-QAT Q2</td><td style="text-align:right">−0.3511</td><td style="text-align:left">[−0.3830, −0.3187]</td><td style="text-align:left">separates</td></tr><tr><td style="text-align:left">gemma-4 E4B, QAT Q2 − QAT Q4</td><td style="text-align:right">−0.3341</td><td style="text-align:left">[−0.3671, −0.3019]</td><td style="text-align:left">separates</td></tr><tr><td style="text-align:left">gemma-4 E2B, QAT Q2 − QAT Q4</td><td style="text-align:right">−0.4330</td><td style="text-align:left">[−0.4643, −0.4020]</td><td style="text-align:left">separates</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">At four bits QAT is a tie on accuracy for three of the four models and worth taking for speed and fit; the 12B separates on synthesis. Taken below the width it ships for, QAT is the most destructive change measured anywhere in this campaign, and the two models fail in opposite directions: one stops producing output, the other will not stop.</figcaption></figure>

Dropping a QAT build from four bits to two costs **−0.4330** on E2B and
**−0.3341** on E4B. The same drop on their non-QAT twins costs −0.0691 and
−0.0325. That is six to ten times the penalty for the same change of width, on
the build chosen for its resistance to exactly that change.

The two models fail in opposite ways, which argues instability rather than
degradation. E2B goes quiet, emitting a median of 65 tokens a note against its
twin's 520. E4B will not stop, emitting 611 against 297.

## Speed moved more than accuracy did

Generation throughput, median tokens per second over roughly 1,003 generations
per run, under 2% spread:

| model | Q1 | Q2 | Q4 | Q6 | Q8 | BF16 |
|---|---:|---:|---:|---:|---:|---:|
| gemma-4 E2B | not run | 459.4 | 479.0 | 444.8 | 412.5 | 321.6 |
| gemma-4 E4B | not run | 330.3 | 341.7 | 310.5 | 274.3 | 201.4 |
| gemma-4 12B | not run | 233.2 | 213.1 | 183.8 | 157.6 | not run |
| gemma-4 26B-A4B | not run | 329.5 | 109.9 | 57.5 | 42.4 | not run |
| LFM2.5-2.6B | not run | not run | 372.3 | 302.5 | 252.2 | 150.3 |
| LFM2.5-8B-A1B | not run | not run | 510.5 | 433.2 | 364.9 | 66.9 |
| Qwen3.6 35B-A3B | 324.0 | 319.6 | 85.2 | 50.7 | 39.4 | not run |

Within a model that stays on the card, throughput tracks byte count. LFM2.5-2.6B
is the clean case: weights grow 1,596 to 2,118 to 2,741 MiB and throughput falls
372.3 to 302.5 to 252.2, tracking to within 8%.

That regularity holds only while the model fits, and the two largest mixtures
break it. Both rows fall off a cliff between Q2 and Q4, in the wrong direction
for arithmetic: fewer bits runs faster because fewer bits still fits.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-capacity" id="fig-capacity-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-capacity" id="fig-capacity-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-capacity-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-capacity-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 166" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Throughput against how much of the model fits on the card"><line class="sg-chart__grid" x1="325.0" x2="325.0" y1="12" y2="132"/><text class="sg-chart__value" x="325.0" y="148" text-anchor="middle" opacity=".7">90</text><line class="sg-chart__grid" x1="440.0" x2="440.0" y1="12" y2="132"/><text class="sg-chart__value" x="440.0" y="148" text-anchor="middle" opacity=".7">180</text><line class="sg-chart__grid" x1="555.0" x2="555.0" y1="12" y2="132"/><text class="sg-chart__value" x="555.0" y="148" text-anchor="middle" opacity=".7">270</text><line class="sg-chart__grid" x1="670.0" x2="670.0" y1="12" y2="132"/><text class="sg-chart__value" x="670.0" y="148" text-anchor="middle" opacity=".7">360</text><text class="sg-chart__label" x="198" y="30" text-anchor="end" font-size="11">26B-A4B QAT Q4 — fits</text><rect class="sg-chart__mark sg-chart__mark--2" x="210" y="21.5" width="460.0" height="9" rx="4"/><text class="sg-chart__value" x="678.0" y="30">359.6</text><text class="sg-chart__label" x="198" y="57" text-anchor="end" font-size="11">26B-A4B Q4 — 8 layers off</text><rect class="sg-chart__mark sg-chart__mark--1" x="210" y="48.5" width="140.6" height="9" rx="4"/><text class="sg-chart__value" x="358.6" y="57">109.9</text><text class="sg-chart__label" x="198" y="84" text-anchor="end" font-size="11">26B-A4B Q6 — 15 layers off</text><rect class="sg-chart__mark sg-chart__mark--1" x="210" y="75.5" width="73.5" height="9" rx="4"/><text class="sg-chart__value" x="291.5" y="84">57.5</text><text class="sg-chart__label" x="198" y="111" text-anchor="end" font-size="11">26B-A4B Q8 — 19 layers off</text><rect class="sg-chart__mark sg-chart__mark--1" x="210" y="102.5" width="54.3" height="9" rx="4"/><text class="sg-chart__value" x="272.3" y="111">42.4</text><text class="sg-chart__axis" x="440" y="162" text-anchor="middle">GENERATION TOKENS PER SECOND</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">gemma-4 26B-A4B</th><th style="text-align:right">file</th><th style="text-align:right">on card</th><th style="text-align:left">expert offload</th><th style="text-align:right">generation</th></tr></thead><tbody><tr><td style="text-align:left">QAT Q4</td><td style="text-align:right">13,588 MiB</td><td style="text-align:right">14,746 MiB</td><td style="text-align:left">none</td><td style="text-align:right">359.6 tok/s</td></tr><tr><td style="text-align:left">Q4</td><td style="text-align:right">16,222 MiB</td><td style="text-align:right">14,166 MiB</td><td style="text-align:left">first 8 layers</td><td style="text-align:right">109.9 tok/s</td></tr><tr><td style="text-align:left">Q6</td><td style="text-align:right">22,216 MiB</td><td style="text-align:right">14,102 MiB</td><td style="text-align:left">first 15 layers</td><td style="text-align:right">57.5 tok/s</td></tr><tr><td style="text-align:left">Q8</td><td style="text-align:right">26,355 MiB</td><td style="text-align:right">13,516 MiB</td><td style="text-align:left">first 19 layers</td><td style="text-align:right">42.4 tok/s</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">One model, one card, four builds. Accuracy across these four does not separate. Throughput spans eight times, set entirely by how many layers had to compute their experts on the CPU.</figcaption></figure>

gemma-4 26B-A4B's four-bit build is 16,222 MiB against roughly 15,600 usable. It
is **600 MiB too large**, so some experts compute on the CPU, and throughput
differs by **3.3x** from the QAT build that fits. Accuracy between them is
indistinguishable.

LFM2.5-8B-A1B shows the same break on a small model. It falls gently from 510.5
to 364.9 across Q4 to Q8, all card-resident, then drops to 66.9 at BF16 when six
layers of experts move off. That last step is 5.5x, against 1.4x for the three
steps before it combined.

QAT is faster at four bits on every model that publishes it: 564.9 against 479.0
on E2B, 418.9 against 341.7 on E4B, 257.1 against 213.1 on the 12B, and 359.6
against 109.9 on the 26B where it is also the difference between fitting and not.

On a fixed card the useful question is not which bit width is most accurate. It
is which bit width still fits.

## Four bits and up: five of thirty separate, and they disagree

Pairing every rung against every other gives thirty comparisons at four bits and
above, across seven ladders. Five separate, none by much:

| comparison | delta | 95% range |
|---|---:|---|
| LFM2.5-8B-A1B, Q8 − Q4 | +0.0378 | [+0.0080, +0.0675] |
| LFM2.5-2.6B, Q8 − Q4 | −0.0327 | [−0.0592, −0.0063] |
| gemma-4 E4B, BF16 − Q6 | −0.0242 | [−0.0409, −0.0080] |
| gemma-4 E4B, Q8 − Q6 | −0.0235 | [−0.0403, −0.0068] |
| gemma-4 E4B, Q6 − Q4 | +0.0210 | [+0.0034, +0.0386] |

They also disagree. gemma-4 E4B peaks at six bits, beating Q4, Q8 and full
precision, and it is the best-established result here: an earlier campaign on
different hardware measured the same pair at +0.0245 [+0.0091, +0.0405].
LFM2.5-8B-A1B improves with width, and its dense sibling LFM2.5-2.6B gets worse
with width, same publisher and same quant family.

On the two largest models nothing separates: 26B-A4B Q8 minus Q4 is −0.0028
[−0.0170, +0.0115], Qwen Q8 minus Q4 is +0.0061 [−0.0084, +0.0210].

Full precision bought nothing measurable. BF16 beat no model's best quantized
rung and on E4B it lost, but three of those four comparisons are nulls and the
comparator was picked after seeing the data, so I read it as no gain rather than
as evidence that quantizing helps.

The synthesis half agrees and resolves even less: 10 of 44 separate, and no pair
separates in opposite directions on the two tasks. Synthesis is the weaker
discriminator by roughly an order of magnitude, moving 0.004 where extraction
moves 0.036.

## Limits

- One corpus lineage. Every extraction figure shares corpus v5, and a second
  independently built corpus remains the gate for stronger claims.
- Three dense models and three mixtures have a sub-four-bit rung, so the
  architecture comparison rests on six points and one of them dominates it.
- One card. The capacity thresholds move with the hardware even though the
  mechanism does not.
- The offloaded throughput figures are a lower bound. All six expert-offload
  runs used memory mapping against llama.cpp's own warning, which costs speed
  only, so the capacity finding's direction is safe and its magnitudes are upper
  bounds.
- One bit was measured once, on Qwen3.6-35B-A3B, the only model here publishing
  a one-bit build.
- The two tasks use different replicate counts, 20,000 for extraction and 5,000
  for synthesis, each matching its own published series.
- LFM2.5 differs in two ways at once, with no dynamic UD builds and no draft
  model, so those ladders support statements about their own shape rather than a
  ranking against gemma-4.

## What to do

**Check whether it fits before arguing about bits.** That threshold was worth
3.3x on one model and 8x across a ladder, more than any accuracy difference
measured anywhere here.

**Never quantize a QAT build below the width it ships for.** It costs six to ten
times what the same step costs on the ordinary build.

**Never take a dense model below four bits without measuring it.** One of the
three here lost more than half its accuracy at two bits, behind a healthy tokens
per second.

**Run a mixture of experts at the lowest width that still fits.** None of the
three lost more than four points below four bits, and all stayed card-resident
at three to eight times the speed of their higher rungs.

**Check throughput rather than accuracy above four bits.** Twenty-five of the
thirty comparisons there do not separate and the five that do point three ways.
The exception is a model with a demonstrated peak, and E4B at six bits is the
only one here that has one.

## Postscript: NVFP4 could not be tested

Blackwell has native four-bit float tensor cores, and this build supports the
format: NVFP4 quantize and dequantize paths in `libggml-base`, 56 NVFP4 symbols
in the CUDA backend, `sm_120a` throughout. A load probe served an NVFP4 file at
2,028 MiB against 2,104 for the same model's Q4.

There is still no way to measure it honestly here. **No official publisher ships
an NVFP4 GGUF.** Checked on 2026-08-22, the NVFP4 repositories from NVIDIA, Red
Hat and unsloth carry safetensors and zero GGUF, which llama.cpp cannot load.
Converting one does not help, because `convert_hf_to_gguf.py` has no NVFP4
support and its output types stop at 16-bit, so the result would carry an NVFP4
label while measuring BF16.

That leaves third-party conversions, and the four measured were not sound. Two
were broken rather than merely worse: one failed JSON parsing on 29% of notes,
and another emitted a median of 33 tokens per note against 369 for its Q4
sibling. The two healthy ones lost 0.05 to 0.07 against Q4, which measures those
files and not the format.

So NVFP4 on llama.cpp is currently a question about who converted your file. It
is left out of the ladder above rather than reported as a width.
