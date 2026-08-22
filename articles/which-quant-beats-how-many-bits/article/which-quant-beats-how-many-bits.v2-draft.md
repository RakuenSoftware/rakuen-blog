---
title: "Two Bits Killed the Dense Model and the Mixture Barely Noticed"
date: 2026-08-22
author: Rakuen Software
tags: [quantization, local-models, benchmarks, aimee]
excerpt: "Thirty-seven arms, seven models, two tasks, one card. A one-bit 35B mixture-of-experts loses four points. A two-bit 12B dense model loses thirty-six. And the largest speed difference measured had nothing to do with arithmetic. It was whether the file fit."
draft: true
---

*Rakuen builds aimee, the system measured here. Every figure below is traceable
through the [measurement log](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/which-quant-beats-how-many-bits/evidence/moe-ladder-measurement-log-2026-08-16.md),
which also records the harness defects found while producing them. Several would
have put wrong numbers in this article, and two of them did before being caught.*

The first version of this piece compared five bit-width steps on four small
dense models. Two separated and they pointed opposite ways, which is a thin
result to build a recommendation on.

We ran thirty-seven arms across seven models, scoring every one on two
different tasks, on a single RTX 5080. It reaches what the original could not:
two bits, one bit, quantization-aware training at matched width, and
mixture-of-expert models up to 35B.

The finding that matters is not about bit width at all. It is that **the same
bit width means completely different things to a dense model and to a mixture of
experts**, and the gap between them is an order of magnitude.

## Reading these numbers: most differences do not separate

Most of the differences in this campaign **do not separate**, and saying which
do is the whole job. Two labels are used throughout and they mean different
things:

- **separates**: the paired 95% range excludes zero. The comparison resolved.
- **indistinguishable**: the range includes zero. **This does not mean the
  models are equal.** It means 1,001 notes could not tell them apart, and a
  larger corpus might.

Every accuracy comparison is a paired bootstrap over the same notes, seed
`20260809`, 20,000 replicates, one comparison per process. Bare score tables are
**point estimates only**. Read the differences from the comparison tables, not
by subtracting two cells.

That distinction carries real weight here. Of the seventeen comparisons with
intervals, nine separate and eight are honest nulls. Several of the
recommendations at the end rest on those nulls rather than on differences.
"These are the same, so take the cheaper one" is a legitimate conclusion, but
only if the reader knows that is what is being said.

## Dense against mixture: one bit beats two bits by nine to one

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-dense-vs-moe" id="fig-dense-vs-moe-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-dense-vs-moe" id="fig-dense-vs-moe-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-dense-vs-moe-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-dense-vs-moe-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 160" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Accuracy change at the most aggressive rung, dense against mixture of experts"><line class="sg-chart__grid" x1="275.0" x2="275.0" y1="14" y2="120"/><text class="sg-chart__value" x="275.0" y="138" text-anchor="middle" opacity=".7">-0.4</text><line class="sg-chart__grid" x1="325.0" x2="325.0" y1="14" y2="120"/><text class="sg-chart__value" x="325.0" y="138" text-anchor="middle" opacity=".7">-0.3</text><line class="sg-chart__grid" x1="375.0" x2="375.0" y1="14" y2="120"/><text class="sg-chart__value" x="375.0" y="138" text-anchor="middle" opacity=".7">-0.2</text><line class="sg-chart__grid" x1="425.0" x2="425.0" y1="14" y2="120"/><text class="sg-chart__value" x="425.0" y="138" text-anchor="middle" opacity=".7">-0.1</text><line class="sg-chart__rule" x1="475.0" x2="475.0" y1="14" y2="120"/><text class="sg-chart__value" x="475.0" y="138" text-anchor="middle" opacity=".7">no change</text><line class="sg-chart__grid" x1="525.0" x2="525.0" y1="14" y2="120"/><text class="sg-chart__value" x="525.0" y="138" text-anchor="middle" opacity=".7">+0.1</text><text class="sg-chart__label" x="238" y="36" text-anchor="end" font-size="11">gemma-4 12B (dense) Q2</text><line class="sg-chart__line sg-chart__line--1" x1="274.4" x2="318.5" y1="32" y2="32"/><line class="sg-chart__line sg-chart__line--1" x1="274.4" x2="274.4" y1="28" y2="36"/><line class="sg-chart__line sg-chart__line--1" x1="318.5" x2="318.5" y1="28" y2="36"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="296.4" cy="32" r="4"/><text class="sg-chart__value" x="708" y="36">-0.3572</text><text class="sg-chart__label" x="238" y="66" text-anchor="end" font-size="11">gemma-4 26B-A4B (MoE) Q2</text><line class="sg-chart__line sg-chart__line--2" x1="446.5" x2="467.8" y1="62" y2="62"/><line class="sg-chart__line sg-chart__line--2" x1="446.5" x2="446.5" y1="58" y2="66"/><line class="sg-chart__line sg-chart__line--2" x1="467.8" x2="467.8" y1="58" y2="66"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="457.3" cy="62" r="4"/><text class="sg-chart__value" x="708" y="66">-0.0354</text><text class="sg-chart__label" x="238" y="96" text-anchor="end" font-size="11">Qwen3.6 35B-A3B (MoE) Q1</text><line class="sg-chart__line sg-chart__line--2" x1="446.1" x2="465.9" y1="92" y2="92"/><line class="sg-chart__line sg-chart__line--2" x1="446.1" x2="446.1" y1="88" y2="96"/><line class="sg-chart__line sg-chart__line--2" x1="465.9" x2="465.9" y1="88" y2="96"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="456.1" cy="92" r="4"/><text class="sg-chart__value" x="708" y="96">-0.0377</text><text class="sg-chart__axis" x="475" y="156" text-anchor="middle">STRICT F1 CHANGE, WITH 95% RANGE</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">model</th><th style="text-align:left">rung</th><th style="text-align:right">F1</th><th style="text-align:right">vs own Q4</th><th style="text-align:left">95% range</th></tr></thead><tbody><tr><td style="text-align:left">gemma-4 12B — dense</td><td style="text-align:left">Q2</td><td style="text-align:right">0.3182</td><td style="text-align:right">−0.3572</td><td style="text-align:left">[−0.4012, −0.3131]</td></tr><tr><td style="text-align:left">gemma-4 26B-A4B — MoE</td><td style="text-align:left">Q2</td><td style="text-align:right">0.6498</td><td style="text-align:right">−0.0354</td><td style="text-align:left">[−0.0569, −0.0144]</td></tr><tr><td style="text-align:left">Qwen3.6 35B-A3B — MoE</td><td style="text-align:left">Q1</td><td style="text-align:right">0.6817</td><td style="text-align:right">−0.0377</td><td style="text-align:left">[−0.0577, −0.0182]</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">Each dot is the accuracy change against that model&#x27;s own four-bit rung; each line is its paired 95% range. The dense model loses more than half its accuracy at two bits. Both mixtures lose under four points — one of them at a single bit.</figcaption></figure>

All three separate. All three are real. And they are not the same kind of
result: the dense model loses more than half its accuracy at two bits, while a
mixture of experts loses under four points at *one*.

Qwen3.6-35B-A3B at one bit scores **0.6817**, higher than every gemma-4 arm in
this campaign at any width, including full four-bit builds.

The small dense models sit in between and closer to the mixtures. gemma-4 E2B
loses 0.069 at two bits and E4B loses 0.033, so this is not simply "bigger models
break harder". The 12B is the only dense model here large enough to be
interesting and small enough to fit, and it is the one that falls apart.

Two bits also destroys the 12B's output discipline in a way no other arm shows.
It **generates faster than any other rung on its own ladder**, 233.2 tokens per
second against 213.1 at Q4, and takes two and a half times as long to finish,
because it emits a median of **7,609 tokens per note against 958**. Eight times
the output for less than half the accuracy.

## Four bits and up: four comparisons separate, and they disagree

Seven ladders. In the region people actually argue about, almost nothing
separates:

Point estimates first. **Do not read differences off this table.** The
comparisons that resolve are listed underneath it.

| model | Q4 | Q6 | Q8 | BF16 |
|---|---:|---:|---:|---:|
| gemma-4 E2B | 0.6091 | 0.6202 | 0.6282 | 0.6252 |
| gemma-4 E4B | 0.6183 | 0.6393 | 0.6158 | 0.6151 |
| gemma-4 12B | 0.6754 | 0.6646 | 0.6798 | not run |
| gemma-4 26B-A4B | 0.6852 | 0.6827 | 0.6825 | not run |
| LFM2.5-2.6B | 0.5952 | 0.5714 | 0.5625 | 0.5825 |
| LFM2.5-8B-A1B | 0.5091 | 0.5341 | 0.5470 | 0.5365 |
| Qwen3.6 35B-A3B | 0.7194 | 0.7303 | 0.7255 | not run |

Which of those differences are real:

| comparison | delta | 95% range | verdict |
|---|---:|---|---|
| gemma-4 E4B, Q6 − Q8 | +0.0235 | [+0.0068, +0.0403] | **separates** |
| LFM2.5-8B-A1B, Q8 − Q4 | +0.0378 | [+0.0080, +0.0675] | **separates** |
| LFM2.5-2.6B, Q8 − Q4 | −0.0327 | [−0.0592, −0.0063] | **separates** |
| gemma-4 E4B, BF16 − Q6 | −0.0242 | [−0.0409, −0.0080] | **separates** |
| gemma-4 26B-A4B, Q8 − Q4 | −0.0028 | [−0.0170, +0.0115] | indistinguishable |
| Qwen3.6 35B-A3B, Q8 − Q4 | +0.0061 | [−0.0084, +0.0210] | indistinguishable |
| gemma-4 E2B, BF16 − Q8 | −0.0030 | [−0.0210, +0.0152] | indistinguishable |
| LFM2.5-2.6B, BF16 − Q4 | −0.0127 | [−0.0393, +0.0137] | indistinguishable |
| LFM2.5-8B-A1B, BF16 − Q8 | −0.0105 | [−0.0367, +0.0164] | indistinguishable |

Four separate and five do not, and the four that separate **point in different
directions**. gemma-4 E4B peaks at six bits, Q6 over Q8 by **+0.0235 [+0.0068,
+0.0403]**, independently reproducing the first version of this article, which
measured +0.0245 [+0.0091, +0.0405] on different hardware in a different
campaign. LFM2.5-8B-A1B improves with width, Q8 over Q4 by **+0.0378 [+0.0080,
+0.0675]**. Its dense sibling LFM2.5-2.6B goes the other way, Q8 under Q4 by
−0.0327 [−0.0592, −0.0063]: same publisher, same quant family, same card,
opposite direction. There is no consistent direction to extract.

On the two largest models nothing separates at all. 26B-A4B Q8 minus Q4 is
−0.0028 [−0.0170, +0.0115]; Qwen Q8 minus Q4 is +0.0061 [−0.0084, +0.0210].

Full precision is the fourth, and the one worth stating carefully because it is
easy to overclaim. BF16 did not beat the best quantized rung on any of the four models
that have one, and on gemma-4 E4B it lost measurably. But three of those four
comparisons are nulls, and **the comparator was chosen after seeing the data**:
each model's best quantized rung, which is the maximum of a noisy set and biased
toward making BF16 look worse. Against Q4 instead, E4B's BF16 is −0.0032 and
nowhere near separating. I read that as full precision buying nothing
measurable on three models and losing on one. It is not evidence that
quantization improves a model, and I would not write it up that way.

## Quantization-aware training: take it at its own width, never below

At four bits, **no QAT pair separates**. Three are clean ties and one sits on the
boundary:

| model | non-QAT Q4 | QAT Q4 | delta | 95% CI |
|---|---:|---:|---:|---|
| gemma-4 E2B | 0.6091 | 0.6219 | +0.0128 | [−0.0095, +0.0355] |
| gemma-4 E4B | 0.6183 | 0.6217 | +0.0034 | not run |
| gemma-4 12B | 0.6754 | 0.6932 | +0.0178 | [+0.0000, +0.0363] |
| gemma-4 26B-A4B | 0.6852 | 0.6804 | −0.0048 | [−0.0235, +0.0139] |

Only the 12B pair approaches separation, and its lower bound is zero to four
decimal places. The bootstrap calls that significant. I do not, and I am flagging
the disagreement because it is the only QAT pair that comes near separating: I
read all four as ties on accuracy. A second corpus putting that lower bound
clearly above zero would change my mind.

QAT is still worth taking. It is faster on every model measured, and at 26B it
decides whether the model fits the card at all.

**Below four bits it inverts violently.** Both models publishing a QAT two-bit
build collapse:

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-qat" id="fig-qat-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-qat" id="fig-qat-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-qat-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-qat-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 220" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Quantization-aware training against its non-QAT twin at matched width"><line class="sg-chart__grid" x1="275.0" x2="275.0" y1="14" y2="180"/><text class="sg-chart__value" x="275.0" y="198" text-anchor="middle" opacity=".7">-0.4</text><line class="sg-chart__grid" x1="325.0" x2="325.0" y1="14" y2="180"/><text class="sg-chart__value" x="325.0" y="198" text-anchor="middle" opacity=".7">-0.3</text><line class="sg-chart__grid" x1="375.0" x2="375.0" y1="14" y2="180"/><text class="sg-chart__value" x="375.0" y="198" text-anchor="middle" opacity=".7">-0.2</text><line class="sg-chart__grid" x1="425.0" x2="425.0" y1="14" y2="180"/><text class="sg-chart__value" x="425.0" y="198" text-anchor="middle" opacity=".7">-0.1</text><line class="sg-chart__rule" x1="475.0" x2="475.0" y1="14" y2="180"/><text class="sg-chart__value" x="475.0" y="198" text-anchor="middle" opacity=".7">no change</text><line class="sg-chart__grid" x1="525.0" x2="525.0" y1="14" y2="180"/><text class="sg-chart__value" x="525.0" y="198" text-anchor="middle" opacity=".7">+0.1</text><text class="sg-chart__label" x="238" y="36" text-anchor="end" font-size="11">E2B: QAT Q4 − Q4</text><line class="sg-chart__line sg-chart__line--2" x1="470.2" x2="492.8" y1="32" y2="32"/><line class="sg-chart__line sg-chart__line--2" x1="470.2" x2="470.2" y1="28" y2="36"/><line class="sg-chart__line sg-chart__line--2" x1="492.8" x2="492.8" y1="28" y2="36"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="481.4" cy="32" r="4"/><text class="sg-chart__value" x="708" y="36">+0.0128</text><text class="sg-chart__label" x="238" y="66" text-anchor="end" font-size="11">12B: QAT Q4 − Q4</text><line class="sg-chart__line sg-chart__line--2" x1="475.0" x2="493.1" y1="62" y2="62"/><line class="sg-chart__line sg-chart__line--2" x1="475.0" x2="475.0" y1="58" y2="66"/><line class="sg-chart__line sg-chart__line--2" x1="493.1" x2="493.1" y1="58" y2="66"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="483.9" cy="62" r="4"/><text class="sg-chart__value" x="708" y="66">+0.0178</text><text class="sg-chart__label" x="238" y="96" text-anchor="end" font-size="11">26B: QAT Q4 − Q4</text><line class="sg-chart__line sg-chart__line--2" x1="463.2" x2="482.0" y1="92" y2="92"/><line class="sg-chart__line sg-chart__line--2" x1="463.2" x2="463.2" y1="88" y2="96"/><line class="sg-chart__line sg-chart__line--2" x1="482.0" x2="482.0" y1="88" y2="96"/><circle class="sg-chart__mark sg-chart__mark--2 sg-chart__ring" cx="472.6" cy="92" r="4"/><text class="sg-chart__value" x="708" y="96">-0.0048</text><text class="sg-chart__label" x="238" y="126" text-anchor="end" font-size="11">E4B: QAT Q2 − Q2</text><line class="sg-chart__line sg-chart__line--1" x1="309.1" x2="343.1" y1="122" y2="122"/><line class="sg-chart__line sg-chart__line--1" x1="309.1" x2="309.1" y1="118" y2="126"/><line class="sg-chart__line sg-chart__line--1" x1="343.1" x2="343.1" y1="118" y2="126"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="325.9" cy="122" r="4"/><text class="sg-chart__value" x="708" y="126">-0.2982</text><text class="sg-chart__label" x="238" y="156" text-anchor="end" font-size="11">E2B: QAT Q2 − Q2</text><line class="sg-chart__line sg-chart__line--1" x1="283.5" x2="315.7" y1="152" y2="152"/><line class="sg-chart__line sg-chart__line--1" x1="283.5" x2="283.5" y1="148" y2="156"/><line class="sg-chart__line sg-chart__line--1" x1="315.7" x2="315.7" y1="148" y2="156"/><circle class="sg-chart__mark sg-chart__mark--1 sg-chart__ring" cx="299.4" cy="152" r="4"/><text class="sg-chart__value" x="708" y="156">-0.3511</text><text class="sg-chart__axis" x="475" y="216" text-anchor="middle">STRICT F1 CHANGE, WITH 95% RANGE</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">pair</th><th style="text-align:right">delta</th><th style="text-align:left">95% range</th><th style="text-align:left">verdict</th></tr></thead><tbody><tr><td style="text-align:left">gemma-4 E2B, QAT Q4 − non-QAT Q4</td><td style="text-align:right">+0.0128</td><td style="text-align:left">[−0.0095, +0.0355]</td><td style="text-align:left">tie</td></tr><tr><td style="text-align:left">gemma-4 12B, QAT Q4 − non-QAT Q4</td><td style="text-align:right">+0.0178</td><td style="text-align:left">[+0.0000, +0.0363]</td><td style="text-align:left">knife-edge</td></tr><tr><td style="text-align:left">gemma-4 26B-A4B, QAT Q4 − non-QAT Q4</td><td style="text-align:right">−0.0048</td><td style="text-align:left">[−0.0235, +0.0139]</td><td style="text-align:left">tie</td></tr><tr><td style="text-align:left">gemma-4 E4B, QAT Q2 − non-QAT Q2</td><td style="text-align:right">−0.2982</td><td style="text-align:left">[−0.3317, −0.2638]</td><td style="text-align:left">separates</td></tr><tr><td style="text-align:left">gemma-4 E2B, QAT Q2 − non-QAT Q2</td><td style="text-align:right">−0.3511</td><td style="text-align:left">[−0.3830, −0.3187]</td><td style="text-align:left">separates</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">At four bits QAT is a tie on accuracy across three models and worth taking for speed and fit. At two bits both models that publish a QAT build collapse, and they collapse in opposite directions: one stops producing output, the other will not stop.</figcaption></figure>

They are also slower, 126.3 tok/s against 459.4 on E2B, so nothing is bought
with the loss.

The two models fail in opposite ways, which argues instability rather than
degradation. E2B **goes quiet**, emitting a median of 65 tokens a note against
its non-QAT twin's 520. E4B **will not stop**, emitting 611 against 297. Same
intervention, same magnitude of damage, opposite symptoms.

## Capacity: the largest speed difference measured was not arithmetic

gemma-4 26B-A4B's non-QAT four-bit build is 16,222 MiB. The card has roughly
15,600 MiB usable. It is **600 MiB too large**, so some experts must compute on
the CPU.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-capacity" id="fig-capacity-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-capacity" id="fig-capacity-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-capacity-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-capacity-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 166" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Throughput against how much of the model fits on the card"><line class="sg-chart__grid" x1="325.0" x2="325.0" y1="12" y2="132"/><text class="sg-chart__value" x="325.0" y="148" text-anchor="middle" opacity=".7">90</text><line class="sg-chart__grid" x1="440.0" x2="440.0" y1="12" y2="132"/><text class="sg-chart__value" x="440.0" y="148" text-anchor="middle" opacity=".7">180</text><line class="sg-chart__grid" x1="555.0" x2="555.0" y1="12" y2="132"/><text class="sg-chart__value" x="555.0" y="148" text-anchor="middle" opacity=".7">270</text><line class="sg-chart__grid" x1="670.0" x2="670.0" y1="12" y2="132"/><text class="sg-chart__value" x="670.0" y="148" text-anchor="middle" opacity=".7">360</text><text class="sg-chart__label" x="198" y="30" text-anchor="end" font-size="11">26B-A4B QAT Q4 — fits</text><rect class="sg-chart__mark sg-chart__mark--2" x="210" y="21.5" width="460.0" height="9" rx="4"/><text class="sg-chart__value" x="678.0" y="30">359.6</text><text class="sg-chart__label" x="198" y="57" text-anchor="end" font-size="11">26B-A4B Q4 — 8 layers off</text><rect class="sg-chart__mark sg-chart__mark--1" x="210" y="48.5" width="140.6" height="9" rx="4"/><text class="sg-chart__value" x="358.6" y="57">109.9</text><text class="sg-chart__label" x="198" y="84" text-anchor="end" font-size="11">26B-A4B Q6 — 15 layers off</text><rect class="sg-chart__mark sg-chart__mark--1" x="210" y="75.5" width="73.5" height="9" rx="4"/><text class="sg-chart__value" x="291.5" y="84">57.5</text><text class="sg-chart__label" x="198" y="111" text-anchor="end" font-size="11">26B-A4B Q8 — 19 layers off</text><rect class="sg-chart__mark sg-chart__mark--1" x="210" y="102.5" width="54.3" height="9" rx="4"/><text class="sg-chart__value" x="272.3" y="111">42.4</text><text class="sg-chart__axis" x="440" y="162" text-anchor="middle">GENERATION TOKENS PER SECOND</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">gemma-4 26B-A4B</th><th style="text-align:right">file</th><th style="text-align:right">on card</th><th style="text-align:left">expert offload</th><th style="text-align:right">generation</th></tr></thead><tbody><tr><td style="text-align:left">QAT Q4</td><td style="text-align:right">13,588 MiB</td><td style="text-align:right">14,746 MiB</td><td style="text-align:left">none</td><td style="text-align:right">359.6 tok/s</td></tr><tr><td style="text-align:left">Q4</td><td style="text-align:right">16,222 MiB</td><td style="text-align:right">14,166 MiB</td><td style="text-align:left">first 8 layers</td><td style="text-align:right">109.9 tok/s</td></tr><tr><td style="text-align:left">Q6</td><td style="text-align:right">22,216 MiB</td><td style="text-align:right">14,102 MiB</td><td style="text-align:left">first 15 layers</td><td style="text-align:right">57.5 tok/s</td></tr><tr><td style="text-align:left">Q8</td><td style="text-align:right">26,355 MiB</td><td style="text-align:right">13,516 MiB</td><td style="text-align:left">first 19 layers</td><td style="text-align:right">42.4 tok/s</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">One model, one card, four builds. Accuracy across these four does not separate. Throughput spans eight times, set entirely by how many layers had to compute their experts on the CPU.</figcaption></figure>

Accuracy between them is indistinguishable. Throughput differs by **3.3x**, and
the entire difference is that one file crosses a capacity threshold.

The effect compounds up the ladder. On the same model, Q6 and Q8 need 15 and 19
layers offloaded and run at 57.5 and 42.4 tok/s, **eight times slower than the
resident QAT build**, for accuracy that does not separate from it. Qwen shows
the same shape: Q2 is card-resident at 319.6 tok/s, while Q8 needs 29 layers
offloaded and manages 39.4.

So on a fixed card the useful question is not which bit width is most accurate.
It is which bit width still fits.

How the offload is done matters, because the obvious approach is expensive. We
first ran the 26B Q4 arm offloading **every** expert rather than the minimum
needed: it served from 4,094 MiB of a 16 GiB card and produced 41 tok/s.
Choosing the smallest offload that fits was worth 2.1x before QAT was considered
at all.

## Two tasks: they do not want the same quantization

Every arm is scored twice: 1,001-note fact extraction, and a frozen 1,000-case
synthesis fixture.

**None of the synthesis numbers below carry intervals.** Every extraction figure
in this article has been through a paired bootstrap; no synthesis figure has.
Read the synthesis rows as directions, not as differences.

| model | task | Q1 | Q2 | Q4 | Q6 | Q8 |
|---|---|---:|---:|---:|---:|---:|
| 12B | extraction | not run | **0.3182** | 0.6754 | 0.6646 | 0.6798 |
| 12B | synthesis | not run | **0.3128** | 0.3498 | 0.3548 | 0.3544 |
| 26B-A4B | extraction | not run | 0.6498 | 0.6852 | 0.6827 | 0.6825 |
| 26B-A4B | synthesis | not run | 0.3326 | 0.3318 | 0.3333 | 0.3340 |
| Qwen 35B-A3B | extraction | 0.6817 | 0.7001 | 0.7194 | 0.7303 | 0.7255 |
| Qwen 35B-A3B | synthesis | 0.3238 | 0.3309 | 0.3293 | 0.3307 | 0.3323 |

The starkest case is the 12B at two bits: **extraction falls by 0.357 while
synthesis falls by 0.037.** Same weights, same card, same hour. One task barely
notices what the other cannot survive.

The reason is what each task rewards. Extraction is scored strictly with false
positives counted against you, so a model emitting 7,609 tokens of loosely
grounded output is punished hard. Synthesis rewards producing complete,
well-formed output, and a verbose model still produces that.

The synthesis harness ships a paired bootstrap that was never wired into this
campaign. That is the largest remaining gap in this work, and it is why nothing
above is stated as a separation.

## Throughput: falls with width, predictably, until capacity intervenes

Throughput carries no intervals because it does not need them: each figure is
the median of roughly 1,003 generations with under 2% spread, on fixed hardware.
These are measurements, not estimates. Within a model, generation throughput
tracks memory bandwidth closely:

| model | Q4 | Q6 | Q8 | BF16 |
|---|---:|---:|---:|---:|
| gemma-4 E2B | 479.0 | 444.8 | 412.5 | not run |
| gemma-4 E4B | 341.7 | 310.5 | 274.3 | not run |
| gemma-4 12B | 213.1 | 183.8 | 157.6 | not run |
| LFM2.5-2.6B | 372.3 | 302.5 | 252.2 | 150.3 |

LFM2.5-2.6B is the clean case: weights grow 1,596 → 2,118 → 2,741 MiB and
throughput falls 372 → 303 → 252, tracking byte count to within 8%. BF16 costs
2.5x the throughput of Q4 for accuracy that is statistically identical.

That regularity holds only while the model fits. The 26B and Qwen ladders break
it completely. A 2.6 GiB *smaller* file runs 3.3x faster, not 1.2x.

## Limits: what this does not establish

- **The synthesis half has no intervals.** A pattern across seven models, not a
  set of resolved comparisons.
- **The offloaded throughput figures are a lower bound.** All six expert-offload
  arms ran with memory mapping enabled, and llama.cpp warns at load that
  `tensor overrides to CPU are used with mmap enabled - consider using
  --no-mmap`. That warning was not acted on. It affects speed only, so accuracy
  is untouched, and the capacity finding's direction is safe, because the
  resident model won while the offloaded side was handicapped. The magnitudes are
  upper bounds on the cost.
- **The offloaded arms left VRAM unused.** The tuner capped itself at 14,200 MiB
  of roughly 15,600 usable, so those arms are perhaps 10–15% slower than the
  hardware allows. The cap stayed because changing it mid-campaign would have
  given one ladder two serving budgets.
- **One corpus lineage.** Every extraction figure shares corpus v5. A second
  independently built corpus remains the gate for stronger claims.
- **LFM2.5 differs in two ways at once.** LiquidAI publishes no dynamic UD
  builds and no draft model, so those ladders run stock K-quants without
  speculation. They support statements about the shape of an LFM ladder, not a
  like-for-like ranking against gemma-4.
- **One card.** Everything is an RTX 5080 with roughly 15.6 GiB usable. The
  capacity thresholds move with the hardware even though the mechanism does not.
- **One bit was measured once.** Qwen3.6-35B-A3B is the only model in the set
  publishing a one-bit build, so the Q1 result rests on a single model
  and a single imatrix quantization method.

## What to do, and which parts rest on a null

**Check whether it fits before arguing about bits.** That threshold was worth
3.3x on one model and 8x across a ladder, more than any accuracy difference
measured anywhere in this campaign.

**On a mixture of experts, quantize aggressively.** Two bits cost 26B-A4B three
and a half points; one bit cost Qwen under four. Both stayed card-resident and
ran three to eight times faster than their own higher-width rungs.

**On a dense model, do not go below four bits without measuring.** The 12B lost
more than half its accuracy at two bits and hid it behind a healthy tokens per
second.

**Take the QAT build at the width it ships for, and never quantize it further.**
The four-bit half of that is a null. No QAT pair separates at Q4, so take it for
speed and fit rather than accuracy. The two-bit half is not a null: −0.3511 and
−0.2982, both clearing zero by a wide margin on two independent models.

**Above four bits, choose on throughput.** This rests on a *null*: accuracy did
not separate on either large model, and four of nine comparisons in that region
that did separate point in three different directions. The speed differences, by
contrast, are measured and large. Choosing on the thing that resolved rather
than the thing that did not is the point.

**And score the task you actually run.** Extraction and synthesis do not want the
same quantization, and on the 12B at two bits the gap between what they say is
larger than the gap between most bit widths.
