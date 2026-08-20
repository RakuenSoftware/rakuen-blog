---
title: "Quantization Choice Mattered More Than Bit Count"
date: 2026-08-19
author: Rakuen Software
tags: [quantization, local-models, benchmarks, aimee]
excerpt: "Thirty arms across six models on one card. Above four bits almost nothing separates. Below it, two bits costs a 3B model seven points and a 12B model thirty-six. And the largest speed difference measured had nothing to do with arithmetic: it was whether the file fit."
draft: true
---

*Rakuen builds aimee, the system measured here. This is a revision in progress:
the campaign behind it is still running, and the sections marked **pending** are
not yet measured. Every figure is traceable through the
[measurement log](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/which-quant-beats-how-many-bits/evidence/moe-ladder-measurement-log-2026-08-16.md),
which also records eleven harness defects found while producing them, several of
which would have put wrong numbers in this article.*

The first version of this piece compared five bit-width steps on four small
dense models and found that two of them separated, pointing opposite ways. This
revision runs thirty-odd arms across six models, scores each on two different
tasks, and adds the rungs the original could not reach: two bits, one bit,
quantization-aware training at matched width, and mixture-of-expert models above
12B.

The short answer is that bit width is the least interesting variable in the set.

## Above four bits, almost nothing happens

Six ladders, and in the region everyone argues about — four bits against six
against eight — the differences are mostly inside the noise.

| model | Q4 | Q6 | Q8 | BF16 |
|---|---:|---:|---:|---:|
| gemma-4 E2B | 0.6091 | 0.6202 | 0.6282 | — |
| gemma-4 E4B | 0.6183 | **0.6393** | 0.6158 | — |
| gemma-4 12B | 0.6754 | 0.6646 | 0.6798 | — |
| LFM2.5-2.6B | **0.5952** | 0.5714 | 0.5625 | 0.5825 |
| LFM2.5-8B-A1B | 0.5091 | 0.5341 | **0.5470** | — |

Strict F1 on 1,001 notes. Three of those five ladders peak somewhere other than
the top, and they disagree about where.

Two comparisons in this region separate under a paired bootstrap at 20,000
replicates. gemma-4 E4B peaks at six bits, Q6 over Q8 by **+0.0235
[+0.0068, +0.0403]** — which independently reproduces the finding in the first
version of this article, +0.0245 [+0.0091, +0.0405], from different hardware and
a different campaign. And LFM2.5-8B-A1B improves with width, Q8 over Q4 by
**+0.0378 [+0.0080, +0.0675]**.

That second one matters because its dense sibling goes the other way.
LFM2.5-2.6B declines across the same ladder, Q8 under Q4 by −0.0327
[−0.0592, −0.0063]. Same publisher, same quant family, same card, opposite
direction. Whatever is happening to the small dense model is not a property of
the family.

## Two bits is where the cliff is, and it gets steeper with size

| model | Q2 | Q4 | drop |
|---|---:|---:|---:|
| gemma-4 E2B | 0.5399 | 0.6091 | −0.069 |
| gemma-4 E4B | 0.5858 | 0.6183 | −0.033 |
| **gemma-4 12B** | **0.3182** | **0.6754** | **−0.357** |

The 12B model loses more than half its accuracy at two bits. The two small
models lose a few points. Whatever two-bit quantization costs, it is not a fixed
tax — on this evidence it scales sharply with model size, and the campaign's
larger models are where it becomes disqualifying rather than merely expensive.

It also destroys output discipline, in a way that is invisible to a throughput
measurement. gemma-4 12B at two bits **generates faster than any other rung on
its ladder** — 233.2 tokens per second against 213.1 at Q4 — and takes two and a
half times as long to finish, because it emits a median of **7,609 tokens per
note against 958**. Eight times the output, for less than half the accuracy.

That behaviour is model-specific and does not follow width. gemma-4 E4B writes
*less* at two bits than at four (297 tokens against 369); E2B writes slightly
more (520 against 464). Only the 12B runs away.

## Quantization-aware training is worth taking, at the width it was trained for

At four bits, QAT is free or better on every model that publishes one:

| model | non-QAT Q4 | QAT Q4 | delta |
|---|---:|---:|---:|
| gemma-4 E2B | 0.6091 | 0.6219 | +0.0128 |
| gemma-4 E4B | 0.6183 | 0.6217 | +0.0034 |
| gemma-4 12B | 0.6754 | 0.6932 | +0.0178 |
| gemma-4 26B-A4B | 0.6852 | 0.6804 | −0.0048 |

None of those separate — the E2B pair is +0.0128 [−0.0095, +0.0355] and the 26B
pair −0.0048 [−0.0235, +0.0139] — but QAT is faster in every case, so the trade
is one-sided even when the accuracy is a wash.

**Below four bits it inverts completely.** Both models that publish a QAT
two-bit build collapse:

| pair | delta | 95% CI | verdict |
|---|---:|---|---|
| E2B: QAT Q2 − non-QAT Q2 | **−0.3511** | [−0.3830, −0.3187] | significant |
| E4B: QAT Q2 − non-QAT Q2 | **−0.2982** | [−0.3317, −0.2638] | significant |

These are the largest effects in the campaign. They are also slower — 126.3
tok/s against 459.4 on E2B — so nothing is being bought with the loss.

The two models fail in opposite ways, which argues instability rather than
degradation. E2B **goes quiet**, emitting a median of 65 tokens a note against
its non-QAT twin's 520. E4B **will not stop**, emitting 611 against 297. Same
intervention, same magnitude of damage, opposite symptoms.

The practical rule: take the QAT build at the width it ships for, and do not
quantize it further.

## The largest speed difference measured was not about arithmetic

gemma-4 26B-A4B is a mixture-of-experts model with about 4B active parameters.
Its non-QAT four-bit build is 16,222 MiB. The card has roughly 15,600 MiB
usable. It is **600 MiB too large**, so some of its experts must compute on the
CPU.

| gemma-4 26B-A4B Q4 | file | on card | expert offload | generation | wall clock |
|---|---:|---:|---|---:|---:|
| non-QAT | 16,222 MiB | 14,166 | first 8 layers on CPU | 109.9 tok/s | 3 h 46 m |
| **QAT** | **13,588 MiB** | 14,746 | **none** | **359.6 tok/s** | **1 h 17 m** |

Accuracy between them is indistinguishable. Throughput differs by **3.3x**, and
the entire difference is that one file crosses a capacity threshold and the
other does not.

This is the same claim the first version of this article made — that QAT's
clearest benefit was fitting a 26B model on a 16-gibibyte card — measured again
on different weights, with the consequence quantified. It is not a marginal fit
advantage. On this card it is the difference between a model you would deploy
and one you would not.

It is worth being precise about what is being measured, because the obvious
mistake is expensive. An earlier run of this arm offloaded **every** expert to
system RAM rather than the minimum needed, served from 4,094 MiB of a 16 GiB
card, and produced 41 tok/s. Choosing the smallest offload that fits, rather
than the simplest one, was worth 2.1x on its own before QAT was considered at
all.

## The two tasks disagree about which quantization to use

Every arm is scored twice: on 1,001-note fact extraction, and on a frozen
1,000-case synthesis fixture.

| model | task | Q2 | Q4 | Q6 | Q8 |
|---|---|---:|---:|---:|---:|
| E2B | extraction | 0.5399 | 0.6091 | 0.6202 | 0.6282 |
| E2B | synthesis | 0.2861 | 0.3300 | 0.3325 | 0.3350 |
| E4B | extraction | 0.5858 | 0.6183 | **0.6393** | 0.6158 |
| E4B | synthesis | 0.3009 | 0.3222 | 0.3226 | 0.3246 |
| 12B | extraction | 0.3182 | 0.6754 | 0.6646 | 0.6798 |
| 12B | synthesis | 0.3128 | 0.3498 | 0.3548 | 0.3544 |

Synthesis rises with width, monotonically or flat, on every model measured. It
never inverts. Extraction inverts on two of five ladders.

The starkest case is 12B at two bits: extraction falls by 0.357 while synthesis
falls by 0.037. The same weights, on the same card, in the same hour — one task
barely notices what the other cannot survive.

**These synthesis figures do not yet carry paired intervals.** The synthesis
harness ships a paired bootstrap that is not yet wired into this campaign, so
what is shown is a consistent direction across five models rather than a set of
separated comparisons. That is the next thing to close and this section will be
revised when it is.

## Speed falls with width, predictably, until capacity intervenes

Within a model, generation throughput declines with bit width almost exactly as
memory bandwidth predicts:

| model | Q4 | Q6 | Q8 | BF16 |
|---|---:|---:|---:|---:|
| gemma-4 E2B | 479.0 | 444.8 | 412.5 | — |
| gemma-4 E4B | 341.7 | 310.5 | 274.3 | — |
| gemma-4 12B | 213.1 | 183.8 | 157.6 | — |
| LFM2.5-2.6B | 372.3 | 302.5 | 252.2 | 150.3 |

Tokens per second, median over ~1,003 generations per arm, spread under 2%.

LFM2.5-2.6B is the clean case: weights grow 1,596 → 2,118 → 2,741 MiB and
throughput falls 372 → 303 → 252, tracking the byte count to within 8%. Going
to BF16 costs 2.5x the throughput of Q4 for accuracy that is statistically
identical.

That regularity holds only while the model fits. The 26B pair above breaks it
completely: a 2.6 GiB **smaller** file runs 3.3x faster, not 1.2x, because the
smaller one stops paying for CPU expert compute.

## What this does not establish

- **The synthesis half has no intervals yet.** Direction across five models is
  suggestive, not resolved.
- **Mixture-of-expert coverage is thin.** LFM2.5-8B-A1B and gemma-4 26B-A4B are
  measured; Qwen3.6-35B-A3B and the remaining 26B rungs are **pending**, along
  with the campaign's only one-bit arm.
- **One corpus lineage.** Every extraction figure shares corpus v5. A second
  independently built corpus remains the gate for stronger claims.
- **LFM2.5 differs in two ways at once.** LiquidAI publishes no dynamic UD
  builds and no draft model, so those ladders run stock K-quants without
  speculation. They support statements about the *shape* of an LFM ladder, not a
  like-for-like ranking against gemma-4.
- **The offloaded arms left VRAM unused.** The expert-offload tuner capped
  itself at 14,200 MiB of a card with roughly 15,600 usable, so the 26B arms ran
  with 1.7 to 2.4 GiB idle. Configurations up to 15,074 MiB loaded cleanly in
  testing and two arms ran for hours above the cap without incident, so those
  arms are 10 to 15% slower than the hardware allows. The cap was left in place
  because changing it mid-campaign would have given one ladder two different
  serving budgets.
- **One card.** Everything here is an RTX 5080 with roughly 15.6 GiB usable. The
  capacity findings are findings about that card; the thresholds move with the
  hardware, even if the mechanism does not.

## What to do with this

Take the QAT build if one exists at the width you want, and do not quantize it
further. Check whether your model fits the card before arguing about bit width,
because that threshold is worth more than any width choice measured here. Above
four bits, pick on throughput, since accuracy is unlikely to separate. Below
four bits, measure on your own task before deploying — two bits cost one model
seven points and another thirty-six.

And score the task you actually run. On this evidence, extraction and synthesis
do not want the same quantization, and the gap between them is larger than the
gap between most bit widths.
