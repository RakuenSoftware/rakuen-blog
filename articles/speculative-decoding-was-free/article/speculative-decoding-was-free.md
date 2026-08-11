---
title: "Local LLMs: Speculative Decoding"
date: 2026-08-11
author: Rakuen Software
tags: [benchmarks, local-models, speculative-decoding, throughput, aimee]
excerpt: "Eleven matched Gemma and Qwen pairs made generation 1.65x to 2.54x faster without a resolved accuracy change. Glimmer shows why that result still has to be earned per deployment."
---

Native multi-token prediction made all eleven matched Gemma and Qwen runs
**1.65x to 2.54x faster**. Not one produced an accuracy change the paired test
could separate from ordinary run-to-run movement.

That looks like a free speed setting. It is not.

Muse Glimmer's matching DFlash drafter made the same RX 7900 XTX **9% slower**.
The target, draft and backend are the unit that matters. "Speculative decoding"
is only the name of the mechanism they share.

*Rakuen builds aimee, the fact-extraction system measured here. Every figure
traces through the
[figure map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/speculative-decoding-was-free/evidence/figures.md).*

## The target can check several guesses at once

Without a draft, a model produces one token, adds it to the prompt, then runs
again for the next one. Most of the work is reading the same model weights for
each step.

Speculative decoding puts a cheaper guess in front of that loop. The draft
proposes several tokens. The target checks the block in one pass, keeps the
matching prefix, then resumes at the first disagreement. A kept token skips a
full one-at-a-time target step.

Gemma 4 and Qwen3.6 ship native multi-token prediction (MTP) heads trained for
that job. Muse Glimmer uses a separate diffusion drafter called DFlash. The
mechanism is related. The cost is not. The draft still consumes time, so its
guesses must be accepted often enough to repay it.

That gives the experiment two separate gates. Throughput must rise. Accuracy
must not move further than the paired data can support. Accuracy here is strict
extraction F1, the harmonic mean of precision and recall.

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

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-accuracy" id="fig-accuracy-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-accuracy" id="fig-accuracy-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-accuracy-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-accuracy-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 382" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Paired F1 change with MTP on minus off for eleven runs"><line class="sg-chart__grid" x1="270.0" x2="270.0" y1="18" y2="330"/><text class="sg-chart__value" x="270.0" y="350" text-anchor="middle" opacity=".7">−0.0200</text><line class="sg-chart__grid" x1="350.0" x2="350.0" y1="18" y2="330"/><text class="sg-chart__value" x="350.0" y="350" text-anchor="middle" opacity=".7">−0.0100</text><line class="sg-chart__rule" x1="430.0" x2="430.0" y1="18" y2="330"/><text class="sg-chart__value" x="430.0" y="350" text-anchor="middle" opacity=".7">no change</text><line class="sg-chart__grid" x1="510.0" x2="510.0" y1="18" y2="330"/><text class="sg-chart__value" x="510.0" y="350" text-anchor="middle" opacity=".7">+0.0100</text><line class="sg-chart__grid" x1="590.0" x2="590.0" y1="18" y2="330"/><text class="sg-chart__value" x="590.0" y="350" text-anchor="middle" opacity=".7">+0.0200</text><text class="sg-chart__label" x="216" y="38" text-anchor="end" font-size="11">Gemma 4 E2B Q4</text><line class="sg-chart__line sg-chart__line--1" x1="418.0" x2="503.6" y1="34" y2="34"/><line class="sg-chart__line sg-chart__line--1" x1="418.0" x2="418.0" y1="30" y2="38"/><line class="sg-chart__line sg-chart__line--1" x1="503.6" x2="503.6" y1="30" y2="38"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="461.2" cy="34" r="4"/><text class="sg-chart__value" x="646" y="38">+0.0039</text><text class="sg-chart__label" x="216" y="65" text-anchor="end" font-size="11">Gemma 4 E2B Q6</text><line class="sg-chart__line sg-chart__line--1" x1="402.8" x2="478.0" y1="61" y2="61"/><line class="sg-chart__line sg-chart__line--1" x1="402.8" x2="402.8" y1="57" y2="65"/><line class="sg-chart__line sg-chart__line--1" x1="478.0" x2="478.0" y1="57" y2="65"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="440.4" cy="61" r="4"/><text class="sg-chart__value" x="646" y="65">+0.0013</text><text class="sg-chart__label" x="216" y="92" text-anchor="end" font-size="11">Gemma 4 E2B Q8</text><line class="sg-chart__line sg-chart__line--1" x1="371.6" x2="454.8" y1="88" y2="88"/><line class="sg-chart__line sg-chart__line--1" x1="371.6" x2="371.6" y1="84" y2="92"/><line class="sg-chart__line sg-chart__line--1" x1="454.8" x2="454.8" y1="84" y2="92"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="413.2" cy="88" r="4"/><text class="sg-chart__value" x="646" y="92">−0.0021</text><text class="sg-chart__label" x="216" y="119" text-anchor="end" font-size="11">Gemma 4 E4B Q4</text><line class="sg-chart__line sg-chart__line--1" x1="401.2" x2="452.4" y1="115" y2="115"/><line class="sg-chart__line sg-chart__line--1" x1="401.2" x2="401.2" y1="111" y2="119"/><line class="sg-chart__line sg-chart__line--1" x1="452.4" x2="452.4" y1="111" y2="119"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="426.0" cy="115" r="4"/><text class="sg-chart__value" x="646" y="119">−0.0005</text><text class="sg-chart__label" x="216" y="146" text-anchor="end" font-size="11">Gemma 4 E4B Q6</text><line class="sg-chart__line sg-chart__line--1" x1="419.6" x2="468.4" y1="142" y2="142"/><line class="sg-chart__line sg-chart__line--1" x1="419.6" x2="419.6" y1="138" y2="146"/><line class="sg-chart__line sg-chart__line--1" x1="468.4" x2="468.4" y1="138" y2="146"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="443.6" cy="142" r="4"/><text class="sg-chart__value" x="646" y="146">+0.0017</text><text class="sg-chart__label" x="216" y="173" text-anchor="end" font-size="11">Gemma 4 E4B Q8</text><line class="sg-chart__line sg-chart__line--1" x1="413.2" x2="462.8" y1="169" y2="169"/><line class="sg-chart__line sg-chart__line--1" x1="413.2" x2="413.2" y1="165" y2="173"/><line class="sg-chart__line sg-chart__line--1" x1="462.8" x2="462.8" y1="165" y2="173"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="438.0" cy="169" r="4"/><text class="sg-chart__value" x="646" y="173">+0.0010</text><text class="sg-chart__label" x="216" y="200" text-anchor="end" font-size="11">Gemma 4 12B QAT Q4</text><line class="sg-chart__line sg-chart__line--1" x1="390.0" x2="597.2" y1="196" y2="196"/><line class="sg-chart__line sg-chart__line--1" x1="390.0" x2="390.0" y1="192" y2="200"/><line class="sg-chart__line sg-chart__line--1" x1="597.2" x2="597.2" y1="192" y2="200"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="493.2" cy="196" r="4"/><text class="sg-chart__value" x="646" y="200">+0.0079</text><text class="sg-chart__label" x="216" y="227" text-anchor="end" font-size="11">Gemma 4 26B-A4B QAT Q4</text><line class="sg-chart__line sg-chart__line--1" x1="258.0" x2="557.2" y1="223" y2="223"/><line class="sg-chart__line sg-chart__line--1" x1="258.0" x2="258.0" y1="219" y2="227"/><line class="sg-chart__line sg-chart__line--1" x1="557.2" x2="557.2" y1="219" y2="227"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="406.8" cy="223" r="4"/><text class="sg-chart__value" x="646" y="227">−0.0029</text><text class="sg-chart__label" x="216" y="254" text-anchor="end" font-size="11">Gemma 4 31B QAT Q4</text><line class="sg-chart__line sg-chart__line--1" x1="342.0" x2="474.0" y1="250" y2="250"/><line class="sg-chart__line sg-chart__line--1" x1="342.0" x2="342.0" y1="246" y2="254"/><line class="sg-chart__line sg-chart__line--1" x1="474.0" x2="474.0" y1="246" y2="254"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="409.2" cy="250" r="4"/><text class="sg-chart__value" x="646" y="254">−0.0026</text><text class="sg-chart__label" x="216" y="281" text-anchor="end" font-size="11">Qwen3.6-27B Q4</text><line class="sg-chart__line sg-chart__line--2" x1="342.8" x2="510.8" y1="277" y2="277"/><line class="sg-chart__line sg-chart__line--2" x1="342.8" x2="342.8" y1="273" y2="281"/><line class="sg-chart__line sg-chart__line--2" x1="510.8" x2="510.8" y1="273" y2="281"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="427.6" cy="277" r="4"/><text class="sg-chart__value" x="646" y="281">−0.0003</text><text class="sg-chart__label" x="216" y="308" text-anchor="end" font-size="11">Qwen3.6-35B-A3B Q4</text><line class="sg-chart__line sg-chart__line--2" x1="267.6" x2="484.4" y1="304" y2="304"/><line class="sg-chart__line sg-chart__line--2" x1="267.6" x2="267.6" y1="300" y2="308"/><line class="sg-chart__line sg-chart__line--2" x1="484.4" x2="484.4" y1="300" y2="308"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="375.6" cy="304" r="4"/><text class="sg-chart__value" x="646" y="308">−0.0068</text><text class="sg-chart__axis" x="430" y="374" text-anchor="middle">MTP-ON F1 MINUS MTP-OFF F1, WITH 95% RANGE</text></svg><div class="sg-figure__legend"><span><i style="background:var(--sg-chart-1)"></i>Gemma</span><span><i style="background:var(--sg-chart-2)"></i>Qwen</span></div></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">pair</th><th style="text-align:right">notes</th><th style="text-align:left">GPU</th><th style="text-align:right">MTP off F1</th><th style="text-align:right">MTP on F1</th><th style="text-align:right">change</th><th style="text-align:left">95% range</th><th style="text-align:right">faster</th></tr></thead><tbody><tr><td style="text-align:left">Gemma 4 E2B Q4</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6207</td><td style="text-align:right">0.6246</td><td style="text-align:right">+0.0039</td><td style="text-align:left">[−0.0015, +0.0092]</td><td style="text-align:right"><strong>1.89x</strong></td></tr><tr><td style="text-align:left">Gemma 4 E2B Q6</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6331</td><td style="text-align:right">0.6344</td><td style="text-align:right">+0.0013</td><td style="text-align:left">[−0.0034, +0.0060]</td><td style="text-align:right"><strong>1.87x</strong></td></tr><tr><td style="text-align:left">Gemma 4 E2B Q8</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6351</td><td style="text-align:right">0.6329</td><td style="text-align:right">−0.0021</td><td style="text-align:left">[−0.0073, +0.0031]</td><td style="text-align:right"><strong>1.98x</strong></td></tr><tr><td style="text-align:left">Gemma 4 E4B Q4</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6306</td><td style="text-align:right">0.6301</td><td style="text-align:right">−0.0005</td><td style="text-align:left">[−0.0036, +0.0028]</td><td style="text-align:right"><strong>2.09x</strong></td></tr><tr><td style="text-align:left">Gemma 4 E4B Q6</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6435</td><td style="text-align:right">0.6452</td><td style="text-align:right">+0.0017</td><td style="text-align:left">[−0.0013, +0.0048]</td><td style="text-align:right"><strong>2.17x</strong></td></tr><tr><td style="text-align:left">Gemma 4 E4B Q8</td><td style="text-align:right">10,000</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6327</td><td style="text-align:right">0.6337</td><td style="text-align:right">+0.0010</td><td style="text-align:left">[−0.0021, +0.0041]</td><td style="text-align:right"><strong>2.32x</strong></td></tr><tr><td style="text-align:left">Gemma 4 12B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:left">RTX 5080</td><td style="text-align:right">0.6854</td><td style="text-align:right">0.6932</td><td style="text-align:right">+0.0079</td><td style="text-align:left">[−0.0050, +0.0209]</td><td style="text-align:right"><strong>2.54x</strong></td></tr><tr><td style="text-align:left">Gemma 4 26B-A4B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:left">RTX 5080</td><td style="text-align:right">0.6833</td><td style="text-align:right">0.6804</td><td style="text-align:right">−0.0029</td><td style="text-align:left">[−0.0215, +0.0159]</td><td style="text-align:right"><strong>1.72x</strong></td></tr><tr><td style="text-align:left">Gemma 4 31B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.6898</td><td style="text-align:right">0.6872</td><td style="text-align:right">−0.0026</td><td style="text-align:left">[−0.0110, +0.0055]</td><td style="text-align:right"><strong>2.05x</strong></td></tr><tr><td style="text-align:left">Qwen3.6-27B Q4</td><td style="text-align:right">1,001</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.7180</td><td style="text-align:right">0.7177</td><td style="text-align:right">−0.0003</td><td style="text-align:left">[−0.0109, +0.0101]</td><td style="text-align:right"><strong>2.35x</strong></td></tr><tr><td style="text-align:left">Qwen3.6-35B-A3B Q4</td><td style="text-align:right">1,001</td><td style="text-align:left">RX 7900 XTX</td><td style="text-align:right">0.7495</td><td style="text-align:right">0.7427</td><td style="text-align:right">−0.0068</td><td style="text-align:left">[−0.0203, +0.0068]</td><td style="text-align:right"><strong>1.65x</strong></td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">Eleven same-card pairs. Each dot is the observed accuracy change after enabling MTP; each line is its paired 95% range. Every line crosses zero.</figcaption></figure>

A point estimate is the score one saved run produced. It is not the whole
result. Gemma 4 12B moved by +0.0079, which looks like an accuracy gain until its
range is included: −0.0050 to +0.0209. Qwen3.6-35B-A3B moved by −0.0068, which
looks like a loss until its range is included: −0.0203 to +0.0068.

Both ranges cross zero. The data allow a small gain, no change, or a small loss.
Calling either direction a result would rank noise.

The same holds for all eleven pairs. This does not prove that MTP produces
identical accuracy. It bounds what this experiment can see. The 10,000-note
ranges are tighter because they contain more observations, and all still cross
zero. The speed result is resolved. The accuracy direction is not.

The E2B ranges were recomputed from the stored per-note predictions on 2026-08-11
with the same paired bootstrap used for the other rows. The graph uses those
recomputed ranges.

## Acceptance explains the speed, but not the exact multiple

The server records how many tokens the draft proposes and how many the target
keeps. Those counters survive in the 12B, 26B-A4B, 31B and Qwen artifacts. They
range from **76.63% to 80.39%**: about four guesses in five. The 10,000-note E2B
and E4B prediction files did not retain the counters, so the table leaves those
cells blank.

That narrow band matters. It confirms that Gemma and Qwen were drafting, and
that the target accepted about four guesses in five. It does not turn acceptance
into a speedup calculator.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-pairs" id="fig-pairs-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-pairs" id="fig-pairs-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-pairs-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-pairs-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 382" preserveAspectRatio="xMidYMid meet" role="img" aria-label="MTP speedup for eleven matched model pairs"><line class="sg-chart__rule" x1="220.0" x2="220.0" y1="18" y2="330"/><text class="sg-chart__value" x="220.0" y="350" text-anchor="middle" opacity=".7">1x</text><line class="sg-chart__grid" x1="345.0" x2="345.0" y1="18" y2="330"/><text class="sg-chart__value" x="345.0" y="350" text-anchor="middle" opacity=".7">1.5x</text><line class="sg-chart__grid" x1="470.0" x2="470.0" y1="18" y2="330"/><text class="sg-chart__value" x="470.0" y="350" text-anchor="middle" opacity=".7">2x</text><line class="sg-chart__grid" x1="595.0" x2="595.0" y1="18" y2="330"/><text class="sg-chart__value" x="595.0" y="350" text-anchor="middle" opacity=".7">2.5x</text><text class="sg-chart__label" x="208" y="38" text-anchor="end" font-size="11">Gemma 4 E2B Q4</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="29.5" width="222.5" height="9" rx="4"/><text class="sg-chart__value" x="450.5" y="38">1.89x</text><text class="sg-chart__label" x="208" y="65" text-anchor="end" font-size="11">Gemma 4 E2B Q6</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="56.5" width="217.5" height="9" rx="4"/><text class="sg-chart__value" x="445.5" y="65">1.87x</text><text class="sg-chart__label" x="208" y="92" text-anchor="end" font-size="11">Gemma 4 E2B Q8</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="83.5" width="245.0" height="9" rx="4"/><text class="sg-chart__value" x="473.0" y="92">1.98x</text><text class="sg-chart__label" x="208" y="119" text-anchor="end" font-size="11">Gemma 4 E4B Q4</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="110.5" width="272.5" height="9" rx="4"/><text class="sg-chart__value" x="500.5" y="119">2.09x</text><text class="sg-chart__label" x="208" y="146" text-anchor="end" font-size="11">Gemma 4 E4B Q6</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="137.5" width="292.5" height="9" rx="4"/><text class="sg-chart__value" x="520.5" y="146">2.17x</text><text class="sg-chart__label" x="208" y="173" text-anchor="end" font-size="11">Gemma 4 E4B Q8</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="164.5" width="330.0" height="9" rx="4"/><text class="sg-chart__value" x="558.0" y="173">2.32x</text><text class="sg-chart__label" x="208" y="200" text-anchor="end" font-size="11">Gemma 4 12B QAT</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="191.5" width="385.0" height="9" rx="4"/><text class="sg-chart__value" x="613.0" y="200">2.54x</text><text class="sg-chart__label" x="208" y="227" text-anchor="end" font-size="11">Gemma 4 26B-A4B QAT</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="218.5" width="180.0" height="9" rx="4"/><text class="sg-chart__value" x="408.0" y="227">1.72x</text><text class="sg-chart__label" x="208" y="254" text-anchor="end" font-size="11">Gemma 4 31B QAT</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="245.5" width="262.5" height="9" rx="4"/><text class="sg-chart__value" x="490.5" y="254">2.05x</text><text class="sg-chart__label" x="208" y="281" text-anchor="end" font-size="11">Qwen3.6-27B</text><rect class="sg-chart__mark sg-chart__mark--2" x="220" y="272.5" width="337.5" height="9" rx="4"/><text class="sg-chart__value" x="565.5" y="281">2.35x</text><text class="sg-chart__label" x="208" y="308" text-anchor="end" font-size="11">Qwen3.6-35B-A3B</text><rect class="sg-chart__mark sg-chart__mark--2" x="220" y="299.5" width="162.5" height="9" rx="4"/><text class="sg-chart__value" x="390.5" y="308">1.65x</text><text class="sg-chart__axis" x="470" y="374" text-anchor="middle">THROUGHPUT WITH MTP DIVIDED BY THROUGHPUT WITHOUT IT</text></svg><div class="sg-figure__legend"><span><i style="background:var(--sg-chart-1)"></i>Gemma</span><span><i style="background:var(--sg-chart-2)"></i>Qwen</span></div></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">pair</th><th style="text-align:right">notes</th><th style="text-align:right">MTP off</th><th style="text-align:right">MTP on</th><th style="text-align:right">faster</th><th style="text-align:right">F1 change</th><th style="text-align:right">kept</th></tr></thead><tbody><tr><td style="text-align:left">Gemma 4 E2B Q4</td><td style="text-align:right">10,000</td><td style="text-align:right">98.56 tok/s</td><td style="text-align:right">185.79 tok/s</td><td style="text-align:right"><strong>1.89x</strong></td><td style="text-align:right">+0.0039</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 E2B Q6</td><td style="text-align:right">10,000</td><td style="text-align:right">90.79 tok/s</td><td style="text-align:right">170.05 tok/s</td><td style="text-align:right"><strong>1.87x</strong></td><td style="text-align:right">+0.0013</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 E2B Q8</td><td style="text-align:right">10,000</td><td style="text-align:right">78.86 tok/s</td><td style="text-align:right">155.88 tok/s</td><td style="text-align:right"><strong>1.98x</strong></td><td style="text-align:right">−0.0021</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 E4B Q4</td><td style="text-align:right">10,000</td><td style="text-align:right">64.10 tok/s</td><td style="text-align:right">134.07 tok/s</td><td style="text-align:right"><strong>2.09x</strong></td><td style="text-align:right">−0.0005</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 E4B Q6</td><td style="text-align:right">10,000</td><td style="text-align:right">52.50 tok/s</td><td style="text-align:right">113.92 tok/s</td><td style="text-align:right"><strong>2.17x</strong></td><td style="text-align:right">+0.0017</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 E4B Q8</td><td style="text-align:right">10,000</td><td style="text-align:right">43.82 tok/s</td><td style="text-align:right">101.48 tok/s</td><td style="text-align:right"><strong>2.32x</strong></td><td style="text-align:right">+0.0010</td><td style="text-align:right">not retained</td></tr><tr><td style="text-align:left">Gemma 4 12B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:right">96.33 tok/s</td><td style="text-align:right">244.73 tok/s</td><td style="text-align:right"><strong>2.54x</strong></td><td style="text-align:right">+0.0079</td><td style="text-align:right">80.39%</td></tr><tr><td style="text-align:left">Gemma 4 26B-A4B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:right">193.04 tok/s</td><td style="text-align:right">332.36 tok/s</td><td style="text-align:right"><strong>1.72x</strong></td><td style="text-align:right">−0.0029</td><td style="text-align:right">79.21%</td></tr><tr><td style="text-align:left">Gemma 4 31B QAT Q4</td><td style="text-align:right">1,001</td><td style="text-align:right">33.54 tok/s</td><td style="text-align:right">68.93 tok/s</td><td style="text-align:right"><strong>2.05x</strong></td><td style="text-align:right">−0.0026</td><td style="text-align:right">79.09%</td></tr><tr><td style="text-align:left">Qwen3.6-27B Q4</td><td style="text-align:right">1,001</td><td style="text-align:right">34.82 tok/s</td><td style="text-align:right">81.78 tok/s</td><td style="text-align:right"><strong>2.35x</strong></td><td style="text-align:right">−0.0003</td><td style="text-align:right">79.04%</td></tr><tr><td style="text-align:left">Qwen3.6-35B-A3B Q4</td><td style="text-align:right">1,001</td><td style="text-align:right">112.97 tok/s</td><td style="text-align:right">186.78 tok/s</td><td style="text-align:right"><strong>1.65x</strong></td><td style="text-align:right">−0.0068</td><td style="text-align:right">76.63%</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">The same eleven pairs, using one throughput definition for every row. MTP increased generation speed in all eleven.</figcaption></figure>

All eleven rows use the same throughput calculation: total completion tokens
divided by summed request latency. The gains span 1.65x to 2.54x. Similar
acceptance can still produce different gains because the avoided target step and
the cost of the draft differ by model and architecture.

Within E2B and E4B, Q4, Q6 and Q8 all became faster, and their accuracy ranges
all crossed zero. That supports two separate decisions: pick the quant for fit
and measured task quality, then test MTP on that exact build.

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

## Score-stable does not mean byte-identical

MTP is designed to preserve the target model's decision. A proposed token only
survives when the target accepts it. That does not guarantee the same bytes from
two inference paths.

Checking a block changes the shape and order of floating-point arithmetic. Near
a tie between candidate tokens, that can change which one lands first. A
deterministic 100-note Gemma diagnostic recorded 100 identical outputs when MTP
was off and 74 identical outputs when MTP was on.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-2" id="fig-2-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-2" id="fig-2-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-2-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-2-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 128" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Magnitude per run"><line class="sg-chart__grid" x1="336.6" x2="336.6" y1="16" y2="96"/><text class="sg-chart__value" x="336.6" y="112" text-anchor="middle" opacity=".7">30</text><line class="sg-chart__grid" x1="463.2" x2="463.2" y1="16" y2="96"/><text class="sg-chart__value" x="463.2" y="112" text-anchor="middle" opacity=".7">60</text><line class="sg-chart__grid" x1="589.8" x2="589.8" y1="16" y2="96"/><text class="sg-chart__value" x="589.8" y="112" text-anchor="middle" opacity=".7">90</text><text class="sg-chart__label" x="198" y="45.0" text-anchor="end">guessing off</text><rect class="sg-chart__mark sg-chart__mark--1" x="210.0" y="36.5" width="422.0" height="9" rx="4"/><text class="sg-chart__value" x="641.0" y="45.0">100/100</text><text class="sg-chart__label" x="198" y="79.0" text-anchor="end">MTP on</text><rect class="sg-chart__mark sg-chart__mark--2" x="210.0" y="70.5" width="312.3" height="9" rx="4"/><text class="sg-chart__value" x="531.3" y="79.0">**74/100**</text><text class="sg-chart__axis" x="421.0" y="122" text-anchor="middle">NOTES IDENTICAL TO THE ONE-AT-A-TIME RUN, OUT OF 100</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left"></th><th style="text-align:right">identical to the one-at-a-time run</th></tr></thead><tbody><tr><td style="text-align:left">guessing off</td><td style="text-align:right">100/100</td></tr><tr><td style="text-align:left">guessing on</td><td style="text-align:right"><strong>74/100</strong></td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">MTP is supposed to preserve the target model’s choice. It changes twenty-six notes in a hundred, because checking several guesses at once changes the order the arithmetic happens in.</figcaption></figure>

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
about 22% over the next five. It fell instead of climbing. The run was stopped
after 22 matched notes because the speed and acceptance result had stabilised.
That is enough to reject this deployment. It is not enough for an accuracy
comparison, so the partial DFlash-on run carries no F1 claim.

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

## Concurrency can spend the same idle capacity

MTP is not the only way to keep a card busy. Sending more requests at once can
fill the same unused compute. In one logged Gemma test, 32 simultaneous requests
gave 4.54x the single-request throughput. Adding MTP produced 4.34x instead.

Those figures are single-sourced in the experiment notes, not a retained paired
artifact, so they set a deployment warning rather than a general limit. The
mechanism is coherent: once concurrency has filled the idle capacity, draft
checking becomes added work with less room to hide.

Test the operating mode you will use. A single-request win does not establish a
32-request win.

## Turn it on only after the pair wins

The replacement for a universal speedup number is a short gate:

- **Hold the target still.** Use the same model, quant, card, notes and
  concurrency on both sides.
- **Count generation.** Keep model loading and server startup outside the
  throughput denominator.
- **Read the mechanism.** Record proposed and accepted draft tokens. Low
  acceptance explains a loss before a long run can.
- **Pair the accuracy test.** Score the same notes and report the range around
  the difference, not only the two rounded scores.

Gemma and Qwen pass that gate here. Enable MTP, then keep the measured gain tied
to the pair that produced it.

Glimmer on llama.cpp's Vulkan path fails it. Leave DFlash off until that backend
changes, then run the pair again.
