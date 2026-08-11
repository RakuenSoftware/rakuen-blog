---
title: "Local LLMs: Speculative Decoding"
date: 2026-08-11
author: Rakuen Software
tags: [benchmarks, local-models, speculative-decoding, throughput, aimee]
excerpt: "Eleven matched Gemma and Qwen pairs made generation 1.65x to 2.54x faster with no accuracy change the data can resolve. The multiple is set by how bandwidth-bound the target is, the obvious llama.cpp flag turns the feature off, and Glimmer's drafter lost 9%."
---

A small model guesses the next few tokens. The big one checks the whole block in
one pass instead of producing them one at a time, and every guess it agrees with
is a token you got for nothing. Gemma 4 and Qwen3.6 both ship that small model,
so I ran eleven matched pairs across the two families, changing nothing inside a
pair except whether the guessing was on. Generation came out **1.65x to 2.54x
faster**, and not one of the eleven moved accuracy further than the paired test
could separate from ordinary run-to-run movement.

Then I pointed the same harness at Muse Glimmer, which ships a drafter of its
own, and it ran **9% slower** on the same card.

Both numbers are right. A target, its draft and the backend underneath them
behave as one unit, and speculative decoding is only the name of the mechanism
they have in common. So the multiple is not the thing that transfers between
deployments. What transfers is where the speed comes from, and you can work that
out before you rent a card.

*Rakuen builds aimee, the fact-extraction system measured here. Every figure
traces through the
[figure map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/speculative-decoding-was-free/evidence/figures.md).*

## The target can check several guesses at once

Two details the rest of this needs. The target keeps the matching prefix of the
block and resumes at the first disagreement, so a rejected guess costs a
verification slot rather than a wrong token.

The second is what does the guessing. Gemma 4 and Qwen3.6 ship a native
multi-token prediction (MTP) head, trained alongside the model it drafts for,
where Muse Glimmer uses a separate diffusion drafter called DFlash. The mechanism
is related. The cost is not.

Where the saving comes from decides every result below. Generating one token
means hauling the whole target model out of memory, and on a consumer card that
read finishes long after the arithmetic does. The compute sits idle, waiting for
weights. Checking several guesses in one pass spends that idle time rather than
buying a second read.

What is being sold, then, is the target's idle capacity, and the price is the
draft's own time plus the verified positions that get discarded. A target that
reads more per token has more to reclaim. A draft that guesses badly pays the
price and collects nothing.

That gives the experiment two separate gates. Throughput must rise. Accuracy
must not move further than the paired data can support. Accuracy here is the
harmonic mean of precision and recall (F1), scored strictly over extracted
facts.

## Eleven matched pairs clear both gates

Every pair held the model, quant, card, notes and concurrency fixed. MTP was the
intended difference. E2B and E4B ran 10,000 notes. Gemma 4 12B, 26B-A4B and 31B,
plus both Qwen3.6 models, ran the same 1,001-note extraction set.

The 12B, 26B-A4B and 31B Gemma runs used the same Unsloth Dynamic
quantisation-aware-trained (QAT) 4-bit quant on both sides. E2B and E4B each
tested Q4, Q6 and Q8. The Qwen pairs used Q4_K_M on both sides.

The cards differ between models because the models fit different hardware. They
do not differ inside a pair. This is a relative test, not a 5080-versus-XTX
benchmark.

Concurrency also differs between the two sets and not inside a pair. The
1,001-note runs used one request at a time; the 10,000-note E2B and E4B runs
sharded across three server processes on one card. That the three-process rows
still gained 1.87x to 2.32x tells you a handful of concurrent requests does not
exhaust the idle capacity MTP feeds on. Thirty-two of them is a different
question, and it gets
[its own section](#concurrency-is-faster-and-disqualified).

Every RX 7900 XTX run used llama.cpp b10210, and the Glimmer diagnostic used
b10356. The two RTX 5080 pairs ran a locally built CUDA binary whose version the
artifacts do not record, which is a gap in this experiment rather than a detail I
am withholding. Speculative decoding in llama.cpp changed twice during this
campaign, so treat every build-specific claim below as pinned to b10210 and
check yours.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-accuracy" id="fig-accuracy-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-accuracy" id="fig-accuracy-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-accuracy-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-accuracy-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 382" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Paired F1 change with MTP on minus off for eleven runs"><line class="sg-chart__grid" x1="270.0" x2="270.0" y1="18" y2="330"/><text class="sg-chart__value" x="270.0" y="350" text-anchor="middle" opacity=".7">−0.0200</text><line class="sg-chart__grid" x1="350.0" x2="350.0" y1="18" y2="330"/><text class="sg-chart__value" x="350.0" y="350" text-anchor="middle" opacity=".7">−0.0100</text><line class="sg-chart__rule" x1="430.0" x2="430.0" y1="18" y2="330"/><text class="sg-chart__value" x="430.0" y="350" text-anchor="middle" opacity=".7">no change</text><line class="sg-chart__grid" x1="510.0" x2="510.0" y1="18" y2="330"/><text class="sg-chart__value" x="510.0" y="350" text-anchor="middle" opacity=".7">+0.0100</text><line class="sg-chart__grid" x1="590.0" x2="590.0" y1="18" y2="330"/><text class="sg-chart__value" x="590.0" y="350" text-anchor="middle" opacity=".7">+0.0200</text><text class="sg-chart__label" x="216" y="38" text-anchor="end" font-size="11">Gemma 4 E2B Q4</text><line class="sg-chart__line sg-chart__line--1" x1="418.0" x2="503.6" y1="34" y2="34"/><line class="sg-chart__line sg-chart__line--1" x1="418.0" x2="418.0" y1="30" y2="38"/><line class="sg-chart__line sg-chart__line--1" x1="503.6" x2="503.6" y1="30" y2="38"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="461.2" cy="34" r="4"/><text class="sg-chart__value" x="646" y="38">+0.0039</text><text class="sg-chart__label" x="216" y="65" text-anchor="end" font-size="11">Gemma 4 E2B Q6</text><line class="sg-chart__line sg-chart__line--1" x1="402.8" x2="478.0" y1="61" y2="61"/><line class="sg-chart__line sg-chart__line--1" x1="402.8" x2="402.8" y1="57" y2="65"/><line class="sg-chart__line sg-chart__line--1" x1="478.0" x2="478.0" y1="57" y2="65"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="440.4" cy="61" r="4"/><text class="sg-chart__value" x="646" y="65">+0.0013</text><text class="sg-chart__label" x="216" y="92" text-anchor="end" font-size="11">Gemma 4 E2B Q8</text><line class="sg-chart__line sg-chart__line--1" x1="371.6" x2="454.8" y1="88" y2="88"/><line class="sg-chart__line sg-chart__line--1" x1="371.6" x2="371.6" y1="84" y2="92"/><line class="sg-chart__line sg-chart__line--1" x1="454.8" x2="454.8" y1="84" y2="92"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="413.2" cy="88" r="4"/><text class="sg-chart__value" x="646" y="92">−0.0021</text><text class="sg-chart__label" x="216" y="119" text-anchor="end" font-size="11">Gemma 4 E4B Q4</text><line class="sg-chart__line sg-chart__line--1" x1="401.2" x2="452.4" y1="115" y2="115"/><line class="sg-chart__line sg-chart__line--1" x1="401.2" x2="401.2" y1="111" y2="119"/><line class="sg-chart__line sg-chart__line--1" x1="452.4" x2="452.4" y1="111" y2="119"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="426.0" cy="115" r="4"/><text class="sg-chart__value" x="646" y="119">−0.0005</text><text class="sg-chart__label" x="216" y="146" text-anchor="end" font-size="11">Gemma 4 E4B Q6</text><line class="sg-chart__line sg-chart__line--1" x1="419.6" x2="468.4" y1="142" y2="142"/><line class="sg-chart__line sg-chart__line--1" x1="419.6" x2="419.6" y1="138" y2="146"/><line class="sg-chart__line sg-chart__line--1" x1="468.4" x2="468.4" y1="138" y2="146"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="443.6" cy="142" r="4"/><text class="sg-chart__value" x="646" y="146">+0.0017</text><text class="sg-chart__label" x="216" y="173" text-anchor="end" font-size="11">Gemma 4 E4B Q8</text><line class="sg-chart__line sg-chart__line--1" x1="413.2" x2="462.8" y1="169" y2="169"/><line class="sg-chart__line sg-chart__line--1" x1="413.2" x2="413.2" y1="165" y2="173"/><line class="sg-chart__line sg-chart__line--1" x1="462.8" x2="462.8" y1="165" y2="173"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="438.0" cy="169" r="4"/><text class="sg-chart__value" x="646" y="173">+0.0010</text><text class="sg-chart__label" x="216" y="200" text-anchor="end" font-size="11">Gemma 4 12B QAT Q4</text><line class="sg-chart__line sg-chart__line--1" x1="390.0" x2="597.2" y1="196" y2="196"/><line class="sg-chart__line sg-chart__line--1" x1="390.0" x2="390.0" y1="192" y2="200"/><line class="sg-chart__line sg-chart__line--1" x1="597.2" x2="597.2" y1="192" y2="200"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="493.2" cy="196" r="4"/><text class="sg-chart__value" x="646" y="200">+0.0079</text><text class="sg-chart__label" x="216" y="227" text-anchor="end" font-size="11">Gemma 4 26B-A4B QAT Q4</text><line class="sg-chart__line sg-chart__line--1" x1="258.0" x2="557.2" y1="223" y2="223"/><line class="sg-chart__line sg-chart__line--1" x1="258.0" x2="258.0" y1="219" y2="227"/><line class="sg-chart__line sg-chart__line--1" x1="557.2" x2="557.2" y1="219" y2="227"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="406.8" cy="223" r="4"/><text class="sg-chart__value" x="646" y="227">−0.0029</text><text class="sg-chart__label" x="216" y="254" text-anchor="end" font-size="11">Gemma 4 31B QAT Q4</text><line class="sg-chart__line sg-chart__line--1" x1="342.0" x2="474.0" y1="250" y2="250"/><line class="sg-chart__line sg-chart__line--1" x1="342.0" x2="342.0" y1="246" y2="254"/><line class="sg-chart__line sg-chart__line--1" x1="474.0" x2="474.0" y1="246" y2="254"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="409.2" cy="250" r="4"/><text class="sg-chart__value" x="646" y="254">−0.0026</text><text class="sg-chart__label" x="216" y="281" text-anchor="end" font-size="11">Qwen3.6-27B Q4</text><line class="sg-chart__line sg-chart__line--2" x1="342.8" x2="510.8" y1="277" y2="277"/><line class="sg-chart__line sg-chart__line--2" x1="342.8" x2="342.8" y1="273" y2="281"/><line class="sg-chart__line sg-chart__line--2" x1="510.8" x2="510.8" y1="273" y2="281"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="427.6" cy="277" r="4"/><text class="sg-chart__value" x="646" y="281">−0.0003</text><text class="sg-chart__label" x="216" y="308" text-anchor="end" font-size="11">Qwen3.6-35B-A3B Q4</text><line class="sg-chart__line sg-chart__line--2" x1="267.6" x2="484.4" y1="304" y2="304"/><line class="sg-chart__line sg-chart__line--2" x1="267.6" x2="267.6" y1="300" y2="308"/><line class="sg-chart__line sg-chart__line--2" x1="484.4" x2="484.4" y1="300" y2="308"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="375.6" cy="304" r="4"/><text class="sg-chart__value" x="646" y="308">−0.0068</text><text class="sg-chart__axis" x="430" y="374" text-anchor="middle">MTP-ON F1 MINUS MTP-OFF F1, WITH 95% RANGE</text></svg><div class="sg-figure__legend"><span><i style="background:var(--sg-chart-1)"></i>Gemma</span><span><i style="background:var(--sg-chart-2)"></i>Qwen</span></div></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">pair</th><th style="text-align:right">notes</th><th style="text-align:left">GPU</th><th style="text-align:right">MTP off F1</th><th style="text-align:right">MTP on F1</th><th style="text-align:right">change</th><th style="text-align:left">95% range</th><th style="text-align:right">faster</th></tr></thead><tbody><tr><td style="text-align:left">Gemma 4 E2B Q4</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6207</td><td style="text-align:right">0.6246</td><td style="text-align:right">+0.0039</td><td style="text-align:left">[−0.0015, +0.0092]</td><td style="text-align:right"><strong>1.89x</strong></td></tr><tr><td style="text-align:left">Gemma 4 E2B Q6</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6331</td><td style="text-align:right">0.6344</td><td style="text-align:right">+0.0013</td><td style="text-align:left">[−0.0034, +0.0060]</td><td style="text-align:right"><strong>1.87x</strong></td></tr><tr><td style="text-align:left">Gemma 4 E2B Q8</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6351</td><td style="text-align:right">0.6329</td><td style="text-align:right">−0.0021</td><td style="text-align:left">[−0.0073, +0.0031]</td><td style="text-align:right"><strong>1.98x</strong></td></tr><tr><td style="text-align:left">Gemma 4 E4B Q4</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6306</td><td style="text-align:right">0.6301</td><td style="text-align:right">−0.0005</td><td style="text-align:left">[−0.0036, +0.0028]</td><td style="text-align:right"><strong>2.09x</strong></td></tr><tr><td style="text-align:left">Gemma 4 E4B Q6</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6435</td><td style="text-align:right">0.6452</td><td style="text-align:right">+0.0017</td><td style="text-align:left">[−0.0013, +0.0048]</td><td style="text-align:right"><strong>2.17x</strong></td></tr><tr><td style="text-align:left">Gemma 4 E4B Q8</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6327</td><td style="text-align:right">0.6337</td><td style="text-align:right">+0.0010</td><td style="text-align:left">[−0.0021, +0.0041]</td><td style="text-align:right"><strong>2.32x</strong></td></tr><tr><td style="text-align:left">Gemma 4 12B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:left">RTX 5080</td><td style="text-align:right">0.6854</td><td style="text-align:right">0.6932</td><td style="text-align:right">+0.0079</td><td style="text-align:left">[−0.0050, +0.0209]</td><td style="text-align:right"><strong>2.54x</strong></td></tr><tr><td style="text-align:left">Gemma 4 26B-A4B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:left">RTX 5080</td><td style="text-align:right">0.6833</td><td style="text-align:right">0.6804</td><td style="text-align:right">−0.0029</td><td style="text-align:left">[−0.0215, +0.0159]</td><td style="text-align:right"><strong>1.72x</strong></td></tr><tr><td style="text-align:left">Gemma 4 31B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6898</td><td style="text-align:right">0.6872</td><td style="text-align:right">−0.0026</td><td style="text-align:left">[−0.0110, +0.0055]</td><td style="text-align:right"><strong>2.05x</strong></td></tr><tr><td style="text-align:left">Qwen3.6-27B Q4</td><td style="text-align:right">1,001</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.7180</td><td style="text-align:right">0.7177</td><td style="text-align:right">−0.0003</td><td style="text-align:left">[−0.0109, +0.0101]</td><td style="text-align:right"><strong>2.35x</strong></td></tr><tr><td style="text-align:left">Qwen3.6-35B-A3B Q4</td><td style="text-align:right">1,001</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.7495</td><td style="text-align:right">0.7427</td><td style="text-align:right">−0.0068</td><td style="text-align:left">[−0.0203, +0.0068]</td><td style="text-align:right"><strong>1.65x</strong></td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">Eleven same-card pairs. Each dot is the observed accuracy change after enabling MTP; each line is its paired 95% range. Every line crosses zero.</figcaption></figure>

A point estimate is the score one saved run produced. It is not the whole
result. Gemma 4 12B moved by +0.0079, which looks like an accuracy gain until its
range is included: −0.0050 to +0.0209. Qwen3.6-35B-A3B moved by −0.0068, which
looks like a loss until its range is included: −0.0203 to +0.0068.

Both ranges cross zero. The data allow a small gain, no change, or a small loss.
Calling either direction a result would rank noise.

The same holds for all eleven pairs. This does not prove that MTP produces
identical accuracy; it bounds what this experiment can see. The 10,000-note
ranges are tighter because they contain more observations, and all still cross
zero.

The speed result is resolved. The accuracy direction is not.

The E2B ranges were recomputed from the stored per-note predictions on 2026-08-11
with the same paired bootstrap used for the other rows. The graph uses those
recomputed ranges.

## Acceptance is nearly constant and the speedup is not

The server records how many tokens the draft proposes and how many the target
keeps. Those counters survive in the 12B, 26B-A4B, 31B and Qwen artifacts. They
range from **76.63% to 80.39%**: about four guesses in five. The 10,000-note E2B
and E4B prediction files did not retain the counters, so the table leaves those
cells blank.

Set those two spans beside each other. Acceptance moves 3.8 points across five
models and two families; the speedup moves from 1.65x to 2.54x over the same
runs. So acceptance tells you the draft is working. It tells you almost nothing
about what the draft is worth.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-pairs" id="fig-pairs-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-pairs" id="fig-pairs-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-pairs-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-pairs-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 382" preserveAspectRatio="xMidYMid meet" role="img" aria-label="MTP speedup for eleven matched model pairs"><line class="sg-chart__rule" x1="220.0" x2="220.0" y1="18" y2="330"/><text class="sg-chart__value" x="220.0" y="350" text-anchor="middle" opacity=".7">1x</text><line class="sg-chart__grid" x1="345.0" x2="345.0" y1="18" y2="330"/><text class="sg-chart__value" x="345.0" y="350" text-anchor="middle" opacity=".7">1.5x</text><line class="sg-chart__grid" x1="470.0" x2="470.0" y1="18" y2="330"/><text class="sg-chart__value" x="470.0" y="350" text-anchor="middle" opacity=".7">2x</text><line class="sg-chart__grid" x1="595.0" x2="595.0" y1="18" y2="330"/><text class="sg-chart__value" x="595.0" y="350" text-anchor="middle" opacity=".7">2.5x</text><text class="sg-chart__label" x="208" y="38" text-anchor="end" font-size="11">Gemma 4 E2B Q4</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="29.5" width="222.5" height="9" rx="4"/><text class="sg-chart__value" x="450.5" y="38">1.89x</text><text class="sg-chart__label" x="208" y="65" text-anchor="end" font-size="11">Gemma 4 E2B Q6</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="56.5" width="217.5" height="9" rx="4"/><text class="sg-chart__value" x="445.5" y="65">1.87x</text><text class="sg-chart__label" x="208" y="92" text-anchor="end" font-size="11">Gemma 4 E2B Q8</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="83.5" width="245.0" height="9" rx="4"/><text class="sg-chart__value" x="473.0" y="92">1.98x</text><text class="sg-chart__label" x="208" y="119" text-anchor="end" font-size="11">Gemma 4 E4B Q4</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="110.5" width="272.5" height="9" rx="4"/><text class="sg-chart__value" x="500.5" y="119">2.09x</text><text class="sg-chart__label" x="208" y="146" text-anchor="end" font-size="11">Gemma 4 E4B Q6</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="137.5" width="292.5" height="9" rx="4"/><text class="sg-chart__value" x="520.5" y="146">2.17x</text><text class="sg-chart__label" x="208" y="173" text-anchor="end" font-size="11">Gemma 4 E4B Q8</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="164.5" width="330.0" height="9" rx="4"/><text class="sg-chart__value" x="558.0" y="173">2.32x</text><text class="sg-chart__label" x="208" y="200" text-anchor="end" font-size="11">Gemma 4 12B QAT</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="191.5" width="385.0" height="9" rx="4"/><text class="sg-chart__value" x="613.0" y="200">2.54x</text><text class="sg-chart__label" x="208" y="227" text-anchor="end" font-size="11">Gemma 4 26B-A4B QAT</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="218.5" width="180.0" height="9" rx="4"/><text class="sg-chart__value" x="408.0" y="227">1.72x</text><text class="sg-chart__label" x="208" y="254" text-anchor="end" font-size="11">Gemma 4 31B QAT</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="245.5" width="262.5" height="9" rx="4"/><text class="sg-chart__value" x="490.5" y="254">2.05x</text><text class="sg-chart__label" x="208" y="281" text-anchor="end" font-size="11">Qwen3.6-27B</text><rect class="sg-chart__mark sg-chart__mark--2" x="220" y="272.5" width="337.5" height="9" rx="4"/><text class="sg-chart__value" x="565.5" y="281">2.35x</text><text class="sg-chart__label" x="208" y="308" text-anchor="end" font-size="11">Qwen3.6-35B-A3B</text><rect class="sg-chart__mark sg-chart__mark--2" x="220" y="299.5" width="162.5" height="9" rx="4"/><text class="sg-chart__value" x="390.5" y="308">1.65x</text><text class="sg-chart__axis" x="470" y="374" text-anchor="middle">THROUGHPUT WITH MTP DIVIDED BY THROUGHPUT WITHOUT IT</text></svg><div class="sg-figure__legend"><span><i style="background:var(--sg-chart-1)"></i>Gemma</span><span><i style="background:var(--sg-chart-2)"></i>Qwen</span></div></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">pair</th><th style="text-align:right">notes</th><th style="text-align:right">MTP off</th><th style="text-align:right">MTP on</th><th style="text-align:right">faster</th><th style="text-align:right">F1 change</th><th style="text-align:right">kept</th></tr></thead><tbody><tr><td style="text-align:left">Gemma 4 E2B Q4</td><td style="text-align:right">10,000</td><td style="text-align:right">98.56 tok/s</td><td style="text-align:right">185.79 tok/s</td><td style="text-align:right"><strong>1.89x</strong></td><td style="text-align:right">+0.0039</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 E2B Q6</td><td style="text-align:right">10,000</td><td style="text-align:right">90.79 tok/s</td><td style="text-align:right">170.05 tok/s</td><td style="text-align:right"><strong>1.87x</strong></td><td style="text-align:right">+0.0013</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 E2B Q8</td><td style="text-align:right">10,000</td><td style="text-align:right">78.86 tok/s</td><td style="text-align:right">155.88 tok/s</td><td style="text-align:right"><strong>1.98x</strong></td><td style="text-align:right">−0.0021</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 E4B Q4</td><td style="text-align:right">10,000</td><td style="text-align:right">64.10 tok/s</td><td style="text-align:right">134.07 tok/s</td><td style="text-align:right"><strong>2.09x</strong></td><td style="text-align:right">−0.0005</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 E4B Q6</td><td style="text-align:right">10,000</td><td style="text-align:right">52.50 tok/s</td><td style="text-align:right">113.92 tok/s</td><td style="text-align:right"><strong>2.17x</strong></td><td style="text-align:right">+0.0017</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 E4B Q8</td><td style="text-align:right">10,000</td><td style="text-align:right">43.82 tok/s</td><td style="text-align:right">101.48 tok/s</td><td style="text-align:right"><strong>2.32x</strong></td><td style="text-align:right">+0.0010</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 12B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:right">96.33 tok/s</td><td style="text-align:right">244.73 tok/s</td><td style="text-align:right"><strong>2.54x</strong></td><td style="text-align:right">+0.0079</td><td style="text-align:right">80.39%</td></tr><tr><td style="text-align:left">Gemma 4 26B-A4B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:right">193.04 tok/s</td><td style="text-align:right">332.36 tok/s</td><td style="text-align:right"><strong>1.72x</strong></td><td style="text-align:right">−0.0029</td><td style="text-align:right">79.21%</td></tr><tr><td style="text-align:left">Gemma 4 31B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:right">33.54 tok/s</td><td style="text-align:right">68.93 tok/s</td><td style="text-align:right"><strong>2.05x</strong></td><td style="text-align:right">−0.0026</td><td style="text-align:right">79.09%</td></tr><tr><td style="text-align:left">Qwen3.6-27B Q4</td><td style="text-align:right">1,001</td><td style="text-align:right">34.82 tok/s</td><td style="text-align:right">81.78 tok/s</td><td style="text-align:right"><strong>2.35x</strong></td><td style="text-align:right">−0.0003</td><td style="text-align:right">79.04%</td></tr><tr><td style="text-align:left">Qwen3.6-35B-A3B Q4</td><td style="text-align:right">1,001</td><td style="text-align:right">112.97 tok/s</td><td style="text-align:right">186.78 tok/s</td><td style="text-align:right"><strong>1.65x</strong></td><td style="text-align:right">−0.0068</td><td style="text-align:right">76.63%</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">The same eleven pairs, using one throughput definition for every row. MTP increased generation speed in all eleven.</figcaption></figure>

All eleven rows use one throughput calculation: total completion tokens divided
by summed request latency. Server startup and model loading sit outside that
denominator. Rows over wall clock would fold a 30-to-60-second load into the
measurement, and the MTP side loads a second model, so the bias would point the
way the hypothesis does.

What does predict the multiple is the quantity the mechanism named: how much of
the target's read the draft hides behind. Hold the family and the card still and
it comes through clean.

| Gemma 4 on the RX 7900 XTX | Q4 | Q6 | Q8 |
|---|---:|---:|---:|
| E2B | 1.89x | 1.87x | 1.98x |
| E4B | 2.09x | 2.17x | 2.32x |

Every step that makes the target read more per token pays more. A heavier quant
is a bigger read, so Q8 beats Q4 in both rows. A bigger model is a bigger read,
so E4B beats E2B at all three quants. Q4 and Q6 on E2B sit two hundredths apart
and in the wrong order, which is smaller than this measurement resolves, so read
that row as flat rather than as a dip.

The pattern is worth a forecast and not a formula, because it stops at the family
and the card. Gemma 4 12B on the RTX 5080 returned the best multiple of all eleven
at 2.54x from a 96.33 tok/s baseline, while 31B on the XTX returned 2.05x from
33.54 tok/s. Slower baseline, smaller gain. Different card, different backend and
different draft head size, with no way to separate them from the runs I have.

The signal that does survive both families is architecture. The two mixture-of-experts
pairs, Gemma 4 26B-A4B at 1.72x and Qwen3.6-35B-A3B at 1.65x, are the two
smallest gains in the set, and they are the two models that read the least per
token. Two points agreeing with the mechanism is not a law. If your target is
sparse, expect the low end of this range, and note that you are already getting
the speed somewhere else.

Within E2B and E4B, Q4, Q6 and Q8 all became faster and their accuracy ranges all
crossed zero. So the two choices are separable: pick the quant for fit and
measured task quality, then turn MTP on for whatever you picked. Neither decision
constrains the other.

## Qwen has two speed levers

Qwen3.6 makes the distinction unusually clear. Its dense 27B model ran at 67.8
tokens/s on an RTX 5090-class card with MTP off. The sparse 35B-A3B ran at 234.0
tokens/s, also with MTP off. Their extraction scores were tied: the 35B-minus-27B
difference was −0.0106, with a range from −0.0294 to +0.0088.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-3" id="fig-3-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-3" id="fig-3-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-3-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-3-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 168" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Two runs across several metrics, each on its own scale"><text class="sg-chart__axis" x="0" y="32">TOKENS PER SECOND</text><text class="sg-chart__label" x="168" y="52.0" text-anchor="end" font-size="11">35B-A3B, mixture of experts</text><rect class="sg-chart__mark sg-chart__mark--1" x="178" y="43.5" width="404.4" height="9" rx="4"/><text class="sg-chart__value" x="591.4" y="52.0">234.0</text><text class="sg-chart__label" x="168" y="69.0" text-anchor="end" font-size="11">27B dense</text><rect class="sg-chart__mark sg-chart__mark--2" x="178" y="60.5" width="117.2" height="9" rx="4"/><text class="sg-chart__value" x="304.2" y="69.0">67.8</text><text class="sg-chart__axis" x="0" y="94">MEDIAN COMPLETION TOKENS</text><text class="sg-chart__label" x="168" y="114.0" text-anchor="end" font-size="11">35B-A3B, mixture of experts</text><rect class="sg-chart__mark sg-chart__mark--1" x="178" y="105.5" width="339.4" height="9" rx="4"/><text class="sg-chart__value" x="526.4" y="114.0">1100</text><text class="sg-chart__label" x="168" y="131.0" text-anchor="end" font-size="11">27B dense</text><rect class="sg-chart__mark sg-chart__mark--2" x="178" y="122.5" width="387.6" height="9" rx="4"/><text class="sg-chart__value" x="574.6" y="131.0">1256</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">Qwen3.6, same family, same quant, same card class</th><th style="text-align:right">tok/s</th><th style="text-align:right">median completion</th></tr></thead><tbody><tr><td style="text-align:left">35B-A3B, mixture of experts</td><td style="text-align:right"><strong>234.0</strong></td><td style="text-align:right">1,100 tokens</td></tr><tr><td style="text-align:left">27B dense</td><td style="text-align:right">67.8</td><td style="text-align:right">1,256 tokens</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">The same family, same quant, same class of card, with MTP off on both sides. Each measure on its own scale, because the units differ.</figcaption></figure>

That is an architecture result. The 35B-A3B is a mixture of experts, so it keeps
all its weights available but activates only part of them for each token. It can
outrun the smaller dense model before a draft enters the picture.

MTP is the second lever. On the XTX, dense Qwen3.6-27B rose from 34.82 to 81.78
tokens/s with its matching sidecar. The sparse 35B-A3B rose from 112.97 to
186.78. Qwen therefore supports both claims separately: architecture can change
the baseline, and MTP can improve either architecture from its own baseline.

Do not multiply the RTX 5090 architecture ratio by the XTX MTP ratio and call it
a forecast. They are different experiments on different backends. Measure the
combination that will run.

## The obvious way to load a draft head turns MTP off

On llama.cpp b10210 there are two ways to hand a server a draft model, and the
one that reads like the right answer is the one that cannot work.

`-md path/to/mtp-head.gguf` is the documented flag for an explicit draft file. It
loads the head as a generic draft model, fails to build a context for it, and
carries on serving without speculation. An MTP head is not a standalone model: it
shares the base model's embeddings, so a context for it on its own cannot be
created.

Naming a draft file explicitly also suppresses the sidecar resolution that would
have found the right head. So `-md` does not merely fail to help. It prevents the
path that works.

What works is naming the draft *repository* and letting the server resolve the
sidecar:

```
llama-server -hf unsloth/gemma-4-12B-it-qat-GGUF:UD-Q4_K_XL \
             -hfd unsloth/gemma-4-12B-it-qat-GGUF:MTP/mtp-gemma-4-12B-it-Q8_0.gguf \
             -c 8192 -np 1 -ngl 99
```

Searching the binary or the help text for the feature will not settle it either.
On the b10201 snapshot I investigated first, the speculative type was inferred
from the download plan rather than from the model file, so no `--mtp` flag
appeared in `--help`, and grepping the binary for MTP
symbols listed the architectures with a nested MTP graph while missing Gemma 4,
whose head is a full model of its own. Each of those cost me a confident wrong
answer about whether the feature existed at all.

A failure here looks exactly like a null result. The server prints one line about
failing to build a draft context, then serves every request correctly at the
speed it would have run anyway. Nothing at request time and nothing in the output
tells you the draft is absent, so unless you were reading the startup log you
will benchmark that against a control, measure the same configuration twice, and
conclude speculative decoding does nothing on your hardware.

So verify the state rather than the flag. `/slots` reports `speculative` as a
boolean, and every run above refused to start unless it matched what that run
intended. Two more guards earned their place: `/props` had to return the model
path actually loaded, because `--model` is only a label and a stale server will
happily serve the previous model under the new name, and every MTP-off artifact
had to contain no draft counters at all. That last one is what proves the control
was a control.

## The draft head is a variable, and you may not get to set it

Acceptance is the draft's job, so the draft's own quality is part of the
experiment. The Gemma runs used Q8_0 heads deliberately: a cheaper head guesses
worse, acceptance falls, and the comparison turns on acceptance.

Qwen did not get the same choice. On b10210 the head quant tracks the base quant
and cannot be overridden. Passing `-hfd REPO:mtp-...-Q8_0.gguf` is accepted and
then ignored, which was confirmed by getting byte-identical counters either way,
664 tokens drafted and 377 accepted. So the Qwen pairs ran a Q4_0 head against
Gemma's Q8_0 one.

That is harmless for the eleven-pair result, because both sides of every Qwen
pair share the same head. It is not harmless for the acceptance band. Both Qwen
rows drafted with a Q4_0 head where all three Gemma rows used Q8_0, so any Gemma
to Qwen acceptance gap is partly the head and partly the model, and this data
cannot separate them. No newer build was available to fix it.

One thing the draft does not care about is quantisation-aware training. The worry
was reasonable: QAT moves the target's weights, the head learned to predict the
base model, so acceptance should fall and take the speedup down with it. It does
not.

On Gemma 4 12B with the same head, same corpus and MTP on both sides,
acceptance came out at **82.1% on the QAT build against 82.6% on the post-hoc
one**, over more than sixty thousand drafted tokens. Half a point. The two
choices compose, and you do not have to pick one.

I am taking that pair from the measurement log alone. The prediction files behind
it went during a fleet relaunch, before anything was committed, which is the
condition this project refuses to accept anywhere else. I keep the figures
because a reader will ask the question and silence would be worse. The provenance
is not good enough and I am not going to pretend otherwise.

## Score-stable does not mean byte-identical

MTP is designed to preserve the target model's decision. A proposed token only
survives when the target accepts it. That does not guarantee the same bytes from
two inference paths.

Checking a block changes the shape and order of floating-point arithmetic. Near
a tie between candidate tokens, that can change which one lands first. A
deterministic 100-note Gemma diagnostic recorded 100 identical outputs when MTP
was off and 74 identical outputs when MTP was on.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-2" id="fig-2-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-2" id="fig-2-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-2-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-2-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 128" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Magnitude per run"><line class="sg-chart__grid" x1="336.6" x2="336.6" y1="16" y2="96"/><text class="sg-chart__value" x="336.6" y="112" text-anchor="middle" opacity=".7">30</text><line class="sg-chart__grid" x1="463.2" x2="463.2" y1="16" y2="96"/><text class="sg-chart__value" x="463.2" y="112" text-anchor="middle" opacity=".7">60</text><line class="sg-chart__grid" x1="589.8" x2="589.8" y1="16" y2="96"/><text class="sg-chart__value" x="589.8" y="112" text-anchor="middle" opacity=".7">90</text><text class="sg-chart__label" x="198" y="45.0" text-anchor="end">MTP off</text><rect class="sg-chart__mark sg-chart__mark--1" x="210.0" y="36.5" width="422.0" height="9" rx="4"/><text class="sg-chart__value" x="641.0" y="45.0">100/100</text><text class="sg-chart__label" x="198" y="79.0" text-anchor="end">MTP on</text><rect class="sg-chart__mark sg-chart__mark--2" x="210.0" y="70.5" width="312.3" height="9" rx="4"/><text class="sg-chart__value" x="531.3" y="79.0">74/100</text><text class="sg-chart__axis" x="421.0" y="122" text-anchor="middle">NOTES IDENTICAL TO THE ONE-AT-A-TIME RUN, OUT OF 100</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left"></th><th style="text-align:right">identical to the one-at-a-time run</th></tr></thead><tbody><tr><td style="text-align:left">MTP off</td><td style="text-align:right">100/100</td></tr><tr><td style="text-align:left">MTP on</td><td style="text-align:right"><strong>74/100</strong></td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">MTP is supposed to preserve the target model’s choice. It changes twenty-six notes in a hundred, because checking several guesses at once changes the order the arithmetic happens in.</figcaption></figure>

The prediction files for that diagnostic were not retained, so this is a
single-sourced result from the measurement log. It belongs here as a warning,
not as a family-wide rate. Qwen's paired F1 remained tied, but Qwen did not get a
separate byte-for-byte test.

The stronger result is the paired task score above. Text moved in the Gemma
diagnostic. Across the stored Gemma and Qwen pairs, those movements did not
resolve into an extraction-accuracy change.

## Glimmer lost because the draft did not earn its keep

Muse Glimmer supplies a useful failure case. Its official K-Quant-17GB target
ran at 41.39 tokens/s on the XTX with DFlash off. With Meta's matching DFlash
drafter loaded, the same first 22 notes ran at 37.67 tokens/s. Aggregate
throughput fell from 40.57 to 35.71 tokens/s.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-glimmer" id="fig-glimmer-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-glimmer" id="fig-glimmer-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-glimmer-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-glimmer-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 150" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Muse Glimmer generation speed with DFlash off and on"><text class="sg-chart__axis" x="0" y="24">MUSE GLIMMER 30B K-QUANT-17GB ON THE RX 7900 XTX</text><text class="sg-chart__label" x="180" y="61" text-anchor="end">DFlash off</text><rect class="sg-chart__mark sg-chart__mark--1" x="194" y="52.5" width="350" height="9" rx="4"/><text class="sg-chart__value" x="553" y="61">41.39 tok/s</text><text class="sg-chart__label" x="180" y="94" text-anchor="end">DFlash on</text><rect class="sg-chart__mark sg-chart__mark--2" x="194" y="85.5" width="319" height="9" rx="4"/><text class="sg-chart__value" x="522" y="94">37.67 tok/s</text><text class="sg-chart__axis" x="194" y="132">9% SLOWER · 24.5% OF DRAFT TOKENS KEPT</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">same 22 notes</th><th style="text-align:right">DFlash off</th><th style="text-align:right">DFlash on</th></tr></thead><tbody><tr><td style="text-align:left">median generation</td><td style="text-align:right">41.39 tok/s</td><td style="text-align:right">37.67 tok/s</td></tr><tr><td style="text-align:left">aggregate throughput</td><td style="text-align:right">40.57 tok/s</td><td style="text-align:right">35.71 tok/s</td></tr><tr><td style="text-align:left">draft acceptance</td><td style="text-align:right">not applicable</td><td style="text-align:right">24.55%</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">The DFlash run was stopped after 22 matched notes. That is enough for the bounded speed and acceptance result, not an accuracy comparison.</figcaption></figure>

The target kept **24.55%** of proposed draft tokens. That is about one in four,
against roughly four in five for Gemma and Qwen. Most proposals still had to be
checked and discarded, while the draft's own work remained. The overhead cost
more than the accepted tokens saved.

Pre-warming did not fix it. Acceptance was 28.3% over the first five notes and
about 22% over the next five. It fell instead of climbing.

The run was stopped after 22 matched notes because the speed and acceptance
result had stabilised. That is enough to reject this deployment, and not enough
for an accuracy comparison, so the partial DFlash-on run carries no F1 claim.

The strongest contrary evidence comes from Meta. Its
[August 2026 model card](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF)
reports a 3.1x DFlash gain for the same target and draft on an RTX 5090. Public
llama.cpp reports also describe DFlash
[slowing on AMD hardware](https://github.com/ggml-org/llama.cpp/issues/25117)
and producing
[low acceptance under Vulkan](https://github.com/ggml-org/llama.cpp/issues/25792).
Our run used llama.cpp b10356, after Glimmer support landed in b10353.

The measured claim is narrow: DFlash lost 9% on this Glimmer quant, llama.cpp
build and Vulkan backend. The mismatch with Meta's CUDA result, plus the two
public reports, points to a backend bug. It does not show that Glimmer is slow,
or that MTP is broken.

That distinction is why the pair has to be tested. One failed Glimmer run could
have been presented as proof that speculative decoding hurts. Eleven successful
Gemma and Qwen pairs could have been presented as proof that it always helps.
The evidence supports neither shortcut.

## Concurrency is faster and disqualified

MTP is not the only way to spend a target's idle capacity, and it is nowhere near
the biggest. Sending many requests at once fills the same gap. In a Gemma test
recorded in my notes rather than in a retained artifact, 32 simultaneous requests
ran **4.54x** the single-request throughput, against MTP's 1.83x on the same
model. On throughput alone this section would recommend batching and stop.

Running both gave 4.34x, and I called that a slowdown before asking whether the
measurement could see a gap that size. It cannot. Two runs of the same 32-slot
configuration took 71 and 61 seconds, a 16% spread standing over a 4% difference.
What I can say is that the combination did not beat batching alone.

Which way the difference points is not something these runs resolve. The
mechanism that would make it a genuine loss is worth testing on your hardware:
once
thirty-two requests are in flight there is no idle compute left for a draft to
claim, and verification becomes work with nowhere to hide.

Batching loses on repeatability instead, which is the half of this comparison
worth your attention. Two runs of the same 32-slot configuration, fresh server
each, agreed on **75 of 100** notes' extracted facts. Two MTP runs under the same
conditions agreed on **100 of 100**, on E4B and on E2B.

The cause is the one that moves the bytes at all. Batch shape sets the reduction
order, and with thirty-two requests in flight the batch composition depends on
when each request happened to arrive. MTP's batch shape is fixed by the draft
length, which is a constant. So MTP perturbs the output against a sequential run
and perturbs it identically every time, while concurrency perturbs it differently
every time.

One of those you can measure with. The other you cannot: the quant differences
this project chases sit around 0.01 F1, and a 32-slot configuration disagrees
with itself on a quarter of the notes. No speedup buys that back.

Every figure in this section comes from the experiment notes with no retained
paired artifact, so treat it as a prompt to measure your own operating mode
rather than as a published limit.

## Turn it on only after the pair wins

The replacement for a universal speedup number is a short gate. It costs two runs
and it answers the question for your deployment rather than for mine.

- **Check both sides are what you asked for, before timing anything.** Read
  `speculative` from `/slots` and refuse the run when it disagrees with your
  intent, read the loaded path from `/props`, and assert that the MTP-off
  artifact carries no draft counters. On b10210 the `-md` flag quietly gives you
  a non-speculative server, and a stale one will serve the previous model under
  the new name.
- **Hold the target still.** Same model, quant, card, notes and concurrency on
  both sides. The draft head counts as part of the target: if the build picks its
  quant for you, record which one it picked.
- **Count generation, not wall clock.** Total completion tokens over summed
  request latency. Model loading and server startup belong outside the
  denominator, and the MTP side loads a second model.
- **Read the mechanism.** Record proposed and accepted draft tokens. Acceptance
  near four in five means the draft is doing its job; acceptance near one in four
  explains a loss in twenty notes instead of a thousand.
- **Pair the accuracy test.** Score the same notes on both sides and report the
  range around the difference. Two rounded scores will show you a movement that
  the data cannot resolve.

Gemma and Qwen pass that gate here, and the expected return is predictable enough
to plan around: roughly 1.9x to 2.5x on a dense target, the low end of that on a
mixture of experts, and more as the quant gets heavier. Enable it, then keep the
measured gain tied to the pair that produced it rather than quoting it as the
speedup for the feature.

Glimmer on llama.cpp's Vulkan path fails it, at 24.55% acceptance and 9% slower.
Leave DFlash off on that backend, and rerun the pair when it changes rather than
concluding anything about Glimmer or about speculative decoding.

## What I still cannot tell you

Two gaps, and both limit how far any of this travels.

**Acceptance against accuracy, note by note.** I have an acceptance rate and a
score for every run, and nothing that says whether the notes where the draft gets
rejected are the notes where the target is wrong. That measurement would explain
the zero. Mine only bounds it.

**Whether the zero is a zero.** Eleven ranges crossing zero is a bound, not an
identity. The tightest, at 10,000 notes, still allows a movement of about three
thousandths either way. If your task turns on differences smaller than that, I
have not answered your question.
