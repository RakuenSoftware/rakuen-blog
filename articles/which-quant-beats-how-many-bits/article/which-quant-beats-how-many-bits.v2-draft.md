---
title: "Two Bits Killed the Dense Model and the Mixture Barely Noticed"
date: 2026-08-22
author: Rakuen Software
tags: [quantization, local-models, benchmarks, aimee]
excerpt: "Thirty-four arms, six models, two tasks, one card. A one-bit 35B mixture-of-experts loses four points. A two-bit 12B dense model loses thirty-six. And the largest speed difference measured had nothing to do with arithmetic — it was whether the file fit."
draft: true
---

*Rakuen builds aimee, the system measured here. Every figure below is traceable
through the [measurement log](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/which-quant-beats-how-many-bits/evidence/moe-ladder-measurement-log-2026-08-16.md),
which also records the harness defects found while producing them. Several would
have put wrong numbers in this article, and two of them did before being caught.*

The first version of this piece compared five bit-width steps on four small
dense models. Two separated and they pointed opposite ways, which is a thin
result to build a recommendation on.

This is thirty-four arms across six models, every one scored on two different
tasks, on one RTX 5080. It adds what the original could not reach: two bits, one
bit, quantization-aware training at matched width, and mixture-of-expert models
up to 35B.

The finding that matters is not about bit width at all. It is that **the same
bit width means completely different things to a dense model and to a mixture of
experts**, and the gap between them is an order of magnitude.

## A one-bit mixture beats a two-bit dense model by nine to one

| model | rung | delta vs its own Q4 | 95% CI |
|---|---|---:|---|
| gemma-4 12B — **dense** | Q2 | **−0.3572** | [−0.4012, −0.3131] |
| gemma-4 26B-A4B — MoE | Q2 | −0.0354 | [−0.0569, −0.0144] |
| Qwen3.6 35B-A3B — MoE | **Q1** | −0.0377 | [−0.0577, −0.0182] |

All three separate. All three are real. And they are not the same kind of
result: the dense model loses more than half its accuracy at two bits, while a
mixture of experts loses under four points at *one*.

Qwen3.6-35B-A3B at one bit scores **0.6817**, higher than every gemma-4 arm in
this campaign at any width, including full four-bit builds.

The small dense models sit in between and closer to the mixtures — gemma-4 E2B
loses 0.069 at two bits, E4B loses 0.033 — so this is not simply "bigger models
break harder". The 12B is the only dense model here large enough to be
interesting and small enough to fit, and it is the one that falls apart.

Two bits also destroys the 12B's output discipline in a way no other arm shows.
It **generates faster than any other rung on its own ladder** — 233.2 tokens per
second against 213.1 at Q4 — and takes two and a half times as long to finish,
because it emits a median of **7,609 tokens per note against 958**. Eight times
the output for less than half the accuracy.

## Above four bits, nothing happens anywhere

Six ladders. In the region people actually argue about, almost nothing
separates:

| model | Q4 | Q6 | Q8 | BF16 |
|---|---:|---:|---:|---:|
| gemma-4 E2B | 0.6091 | 0.6202 | 0.6282 | — |
| gemma-4 E4B | 0.6183 | **0.6393** | 0.6158 | — |
| gemma-4 12B | 0.6754 | 0.6646 | 0.6798 | — |
| gemma-4 26B-A4B | 0.6852 | 0.6827 | 0.6825 | — |
| LFM2.5-2.6B | **0.5952** | 0.5714 | 0.5625 | 0.5825 |
| LFM2.5-8B-A1B | 0.5091 | 0.5341 | **0.5470** | — |
| Qwen3.6 35B-A3B | 0.7194 | **0.7303** | 0.7255 | — |

On the two largest models the top of the ladder is flat to within noise:
26B-A4B Q8 minus Q4 is −0.0028 [−0.0170, +0.0115]; Qwen Q8 minus Q4 is +0.0061
[−0.0084, +0.0210].

Three comparisons here do separate, and they disagree with each other. gemma-4
E4B peaks at six bits, Q6 over Q8 by **+0.0235 [+0.0068, +0.0403]** —
independently reproducing the first version of this article, which measured
+0.0245 [+0.0091, +0.0405] on different hardware in a different campaign.
LFM2.5-8B-A1B improves with width, Q8 over Q4 by **+0.0378 [+0.0080, +0.0675]**.
And its dense sibling LFM2.5-2.6B goes the other way, Q8 under Q4 by −0.0327
[−0.0592, −0.0063] — same publisher, same quant family, same card, opposite
direction.

## Quantization-aware training: take it at its own width, never below

At four bits QAT is free or slightly better on all four models that publish one:

| model | non-QAT Q4 | QAT Q4 | delta | 95% CI |
|---|---:|---:|---:|---|
| gemma-4 E2B | 0.6091 | 0.6219 | +0.0128 | [−0.0095, +0.0355] |
| gemma-4 E4B | 0.6183 | 0.6217 | +0.0034 | — |
| gemma-4 12B | 0.6754 | 0.6932 | +0.0178 | [+0.0000, +0.0363] |
| gemma-4 26B-A4B | 0.6852 | 0.6804 | −0.0048 | [−0.0235, +0.0139] |

Only the 12B pair approaches separation, and its lower bound is zero to four
decimal places — a knife-edge, not a result. Treat all four as ties on accuracy.
QAT is still worth taking, because it is faster in every case and at 26B it
decides whether the model fits at all.

**Below four bits it inverts violently.** Both models publishing a QAT two-bit
build collapse:

| pair | delta | 95% CI |
|---|---:|---|
| E2B: QAT Q2 − non-QAT Q2 | **−0.3511** | [−0.3830, −0.3187] |
| E4B: QAT Q2 − non-QAT Q2 | **−0.2982** | [−0.3317, −0.2638] |

They are also slower — 126.3 tok/s against 459.4 on E2B — so nothing is bought
with the loss.

The two models fail in opposite ways, which argues instability rather than
degradation. E2B **goes quiet**, emitting a median of 65 tokens a note against
its non-QAT twin's 520. E4B **will not stop**, emitting 611 against 297. Same
intervention, same magnitude of damage, opposite symptoms.

## The largest speed difference measured was not about arithmetic

gemma-4 26B-A4B's non-QAT four-bit build is 16,222 MiB. The card has roughly
15,600 MiB usable. It is **600 MiB too large**, so some experts must compute on
the CPU.

| gemma-4 26B-A4B Q4 | file | on card | expert offload | generation | wall clock |
|---|---:|---:|---|---:|---:|
| non-QAT | 16,222 MiB | 14,166 | first 8 layers on CPU | 109.9 tok/s | 3 h 46 m |
| **QAT** | **13,588 MiB** | 14,746 | **none** | **359.6 tok/s** | **1 h 17 m** |

Accuracy between them is indistinguishable. Throughput differs by **3.3x**, and
the entire difference is that one file crosses a capacity threshold.

The effect compounds up the ladder. On the same model, Q6 and Q8 need 15 and 19
layers offloaded and run at 57.5 and 42.4 tok/s — **eight times slower than the
resident QAT build**, for accuracy that does not separate from it. Qwen shows
the same shape: Q2 is card-resident at 319.6 tok/s, while Q8 needs 29 layers
offloaded and manages 39.4.

So on a fixed card the useful question is not which bit width is most accurate.
It is which bit width still fits.

It is worth being precise about how the offload is done, because the obvious
approach is expensive. An earlier run of the 26B Q4 arm offloaded **every**
expert rather than the minimum needed, served from 4,094 MiB of a 16 GiB card,
and produced 41 tok/s. Choosing the smallest offload that fits was worth 2.1x
before QAT was considered at all.

## The two tasks disagree about which quantization to use

Every arm is scored twice: 1,001-note fact extraction, and a frozen 1,000-case
synthesis fixture.

| model | task | Q1 | Q2 | Q4 | Q6 | Q8 |
|---|---|---:|---:|---:|---:|---:|
| 12B | extraction | — | **0.3182** | 0.6754 | 0.6646 | 0.6798 |
| 12B | synthesis | — | **0.3128** | 0.3498 | 0.3548 | 0.3544 |
| 26B-A4B | extraction | — | 0.6498 | 0.6852 | 0.6827 | 0.6825 |
| 26B-A4B | synthesis | — | 0.3326 | 0.3318 | 0.3333 | 0.3340 |
| Qwen 35B-A3B | extraction | 0.6817 | 0.7001 | 0.7194 | 0.7303 | 0.7255 |
| Qwen 35B-A3B | synthesis | 0.3238 | 0.3309 | 0.3293 | 0.3307 | 0.3323 |

The starkest case is the 12B at two bits: **extraction falls by 0.357 while
synthesis falls by 0.037.** Same weights, same card, same hour. One task barely
notices what the other cannot survive.

The reason is what each task rewards. Extraction is scored strictly with false
positives counted against you, so a model emitting 7,609 tokens of loosely
grounded output is punished hard. Synthesis rewards producing complete,
well-formed output, and a verbose model still produces that.

**These synthesis figures carry no paired intervals.** The synthesis harness
ships a paired bootstrap that was never wired into this campaign, so what is
shown is a consistent pattern across six models rather than a set of separated
comparisons. That is the largest remaining gap in this work.

## Speed falls with width, predictably, until capacity intervenes

Within a model, generation throughput tracks memory bandwidth closely:

| model | Q4 | Q6 | Q8 | BF16 |
|---|---:|---:|---:|---:|
| gemma-4 E2B | 479.0 | 444.8 | 412.5 | — |
| gemma-4 E4B | 341.7 | 310.5 | 274.3 | — |
| gemma-4 12B | 213.1 | 183.8 | 157.6 | — |
| LFM2.5-2.6B | 372.3 | 302.5 | 252.2 | 150.3 |

LFM2.5-2.6B is the clean case: weights grow 1,596 → 2,118 → 2,741 MiB and
throughput falls 372 → 303 → 252, tracking byte count to within 8%. BF16 costs
2.5x the throughput of Q4 for accuracy that is statistically identical.

That regularity holds only while the model fits. The 26B and Qwen ladders break
it completely — a 2.6 GiB *smaller* file runs 3.3x faster, not 1.2x.

## What this does not establish

- **The synthesis half has no intervals.** A consistent pattern across six
  models, not a set of resolved comparisons.
- **The offloaded throughput figures are a lower bound.** All six expert-offload
  arms ran with memory mapping enabled, and llama.cpp warns at load that
  `tensor overrides to CPU are used with mmap enabled — consider using
  --no-mmap`. That warning was not acted on. It affects speed only, so accuracy
  is untouched, and the capacity finding's direction is safe — the resident
  model won while the offloaded side was handicapped — but the magnitudes are
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
  publishing a one-bit build, so the striking Q1 result rests on a single model
  and a single imatrix quantization method.

## What to do with this

**Check whether it fits before arguing about bits.** That threshold was worth
3.3x on one model and 8x across a ladder — more than any accuracy difference
measured anywhere in this campaign.

**On a mixture of experts, quantize aggressively.** Two bits cost 26B-A4B three
and a half points; one bit cost Qwen under four. Both stayed card-resident and
ran three to eight times faster than their own higher-width rungs.

**On a dense model, do not go below four bits without measuring.** The 12B lost
more than half its accuracy at two bits and hid it behind a healthy tokens per
second.

**Take the QAT build at the width it ships for, and never quantize it further.**
Free-to-better at four bits, catastrophic at two.

**Above four bits, choose on throughput.** Accuracy did not separate on either
large model, and the speed differences are large and monotonic.

**And score the task you actually run.** Extraction and synthesis do not want the
same quantization, and on the 12B at two bits the gap between what they say is
larger than the gap between most bit widths.
