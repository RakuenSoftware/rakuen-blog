---
title: "It Skipped the Reasoning and It Was Right"
date: 2026-08-13
author: Rakuen Software
tags: [local-models, quantization, reasoning, benchmarks, aimee]
excerpt: "One quantization of one model answered 13% of notes with no reasoning pass. We made it reason on those notes and its accuracy fell 0.21 F1. The skip was not a defect."
---

*Rakuen builds aimee, the system measured here. Every run behind these figures is
listed in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/it-skipped-the-reasoning-and-it-was-right/evidence/figures.md).*

A model that declines to reason looks broken. Ours declined on 13% of notes, we
forced it to reason on those notes, and the harmonic mean of precision and recall
(F1) fell by 0.21. The behaviour that looked like a defect was the model being
right about which notes were easy.

We would not have gone looking. The skip was found while auditing something else,
and the first assumption was a bug.

## The build decides, not the model

gemma-4-E4B answers some notes with no reasoning pass at all. The rate is stable
enough to be a fingerprint: 13.3% on three separate 10,000-note runs, with and
without speculative decoding, and 15.0% to 16.8% on four 1,001-note campaigns.

The same weights at other bit widths do not do it. The build from
quantization-aware training (QAT) does, at a slightly higher rate.

| build | notes | no reasoning pass |
|---|---:|---:|
| E4B `UD-Q6_K_XL` | 10,000 | **13.3%** |
| E4B QAT | 3,002 | **16.0%** |
| E4B `UD-Q4_K_XL` | 10,000 | 0.1% |
| E4B `UD-Q8_K_XL` | 10,000 | 0.1% |
| E2B, all three widths | 10,000 each | 0.0% |

Same prompt, same corpus, same harness, same card. The only thing that moves is
how the weights were packed, and it moves a behaviour that no quantization
benchmark reports. Perplexity does not have a column for this.

So the first correction is to the framing. A reader who sees this in their own
logs will reach for the prompt or the sampler. Neither is where it lives.

## Silent notes were the easy ones

On the 1,001-note corpus, E4B at Q6 went silent on 134 notes. Those notes scored
**0.8507** F1. The 863 notes it reasoned about scored **0.4212**.

That gap has two readings and they point opposite ways. Either reasoning is
unnecessary on those notes, or the model is skipping the ones it already knows
and would do better if it thought. Every run up to here is observational, and
observation cannot separate them, because the model is the thing choosing which
notes go into which group.

## We removed the choice

The prompt says "Reason first if it helps". We changed that clause and nothing
else to "Reason first on every note, including the ones where the answer looks
immediate", then ran both against one server process with the same weights, cache
size and concurrency.

Of the 134 silent notes, 67 then reasoned. Their F1 fell from 0.8507 to 0.6418,
a change of **−0.2090** with a 95% range of **−0.3284 to −0.0896** over 20,000
bootstrap replicates.

Two things could produce that without any effect from reasoning, and the design
carries a control for each.

**Check the sentence first.** The 863 notes that reasoned under both
prompts also saw the new wording, and they moved −0.0028. The sentence is worth
almost nothing on its own.

**Check the selection next.** Notes picked for scoring 0.85 will fall on a
second measurement whether or not anything was done to them. The control for that
is the 67 notes that stayed silent under both prompts: chosen the same way, never
treated. They moved −0.0448.

Net of both controls the change is **−0.1614**. The two groups do not start from
the same score, so that bounds the artifact rather than removing it.

## The instruction is not a switch

Half the silent notes ignored the new clause. Of 134, exactly 67 began reasoning
and 67 did not, on a prompt that says to reason on every note.

That is the same shape as the quantization result. Whatever decides this sits
below the level a sentence reaches, and an instruction moves some of it and not
the rest.

## What to do with a model that skips

**Never treat a skipped reasoning pass as a fault to repair.** On this model and
this corpus it marked the notes that needed no help, and overriding it cost 0.21
F1 on exactly those notes.

**Check the reasoning rate when you change quantization.** Q6 and the QAT build
skip; Q4 and Q8 do not. Nothing in a quantization comparison surfaces that, and
it changes what the model does rather than how well it does it.

**Check what the skip is worth before pricing it.** The cheap reading is that skipping
saves tokens. Here it also gained accuracy, and the two are not usually the same
decision.

The scope is narrow and worth stating. One model, one corpus, one card, and a
treatment group of 67 notes. What we can say is that on the run where the model
declined to think, thinking made it worse.

Our benchmark spent a month ranking models on how well they answer. It never
asked whether they should have answered that way, and the one time we checked,
the model had made a better call than the prompt did.
