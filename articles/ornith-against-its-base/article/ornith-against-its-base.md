---
title: "Ornith Against the Base It Came From"
date: 2026-08-23
author: Rakuen Software
tags: [finetuning, local-models, benchmarks, aimee]
excerpt: "A finetune can be measured against the exact model it was made from. Three Ornith builds against their Qwen bases, on the same card and the same corpora, with the expectation registered before the first run: that a finetune does not move this work in either direction."
---

*Rakuen builds aimee, the system measured here. This article is a draft: the
design and the setup findings are written, and no accuracy result exists yet.
Sections that will carry numbers say so rather than leaving a space.*

Most model comparisons ask which of several unrelated models is best. A finetune
lets you ask something narrower and more useful: **does this thing do the job
better than the thing it was made from.** Same architecture, same tokenizer,
same weights underneath the post-training. One variable.

Ornith is a Qwen finetune family, so every model in it has an exact base. This
study runs three of those pairs on the two tasks the quantization series already
uses, on one card, at four bits.

The expectation is on record before the first run: **a finetune should not shift
measurably from its base on this work, in either direction.** Not that it fails
to win — that it lands close enough that most of these comparisons do not
separate at all.

## Why base-relative, and not a leaderboard

A leaderboard answers "which model should I download". It cannot answer "was the
post-training worth anything", because every other model on the board differs in
size, architecture, corpus and recipe at the same time.

Against its own base, a finetune differs by the post-training and the
quantization recipe, and nothing else. That is a small enough gap to attribute a
result to, and it is the question somebody choosing between `Qwen3.5-9B` and
`Ornith-1.0-9B` is actually asking — they are the same size, the same shape, and
one is derived from the other.

## Lineage, from the config and not the card

The Ornith cards never name an upstream. Lineage is taken from `config.json`:

- `Ornith-1.0-9B` reports `Qwen3_5ForConditionalGeneration`, `model_type: qwen3_5`
- `Ornith-1.5-35B-A3B` reports `Qwen3_5MoeForConditionalGeneration`, `qwen3_5_moe`

This matters more than it sounds. A pairing asserted from a family name is a
guess; a pairing read out of the architecture string is a fact about the file
that was downloaded.

## The pairs

| finetune | file | base | file |
|---|---|---|---|
| Ornith-1.0-9B | unsloth UD-Q4_K_XL, 5.57 GiB | Qwen3.5-9B | unsloth UD-Q4_K_XL, 5.56 GiB |
| Ornith-1.5-9B | ornith-ai Q4_K_M, 5.24 GiB | Qwen3.5-9B | unsloth UD-Q4_K_XL, 5.56 GiB |
| Ornith-1.5-35B-A3B | ornith-ai Q4_K_M, 20.22 GiB | Qwen3.6-35B-A3B | unsloth UD-Q4_K_XL, 20.82 GiB |

There is no Qwen3.6-9B, so both 9B finetunes pair against Qwen3.5-9B.

Two of these pairs are not matched on quantization recipe. UD-Q4_K_XL is this
series' standard and stays the standard for the base half; where Ornith
publishes nothing above Q4_K_M, the finetune runs at Q4_K_M rather than the base
being downgraded to meet it. **Those two rungs therefore measure the finetune
and the recipe together**, and any result from them carries that caveat wherever
it goes.

## Speculation is measured as shipped

The series rule is multi-token prediction on wherever the publisher provides a
draft, and off wherever they do not. No exceptions here either.

That rule has two consequences worth stating before any throughput number
appears.

**No 9B model in this study can speculate on this build.** This was checked
rather than assumed, after the base probed at 133 tok/s against 213 for a larger
gemma-4 12B. Two MTP shapes exist and only one of them works here. A *separate
draft model* passed with `-hfd` is what the gemma and qwen36 runs use, and it is
why a 12B outruns a model half its size. MTP layers *baked into the model* are
discarded by this llama.cpp build at load —

```
model has unused tensor blk.32.nextn.eh_proj.weight -- ignoring
```

— repeated for every `nextn` tensor. The MTP build serves at **133.11 tok/s**
against **133.6** for the ordinary one: a larger download for no speedup. The
separate head published for the Ornith 9B models fails to load as a draft
outright (`common_speculative_init_result: failed to load draft model`).

So both halves of the 9B pair run unassisted, which leaves the pair matched. 133
tok/s is what a 9B dense at four bits does on this card with no help.

**The 35B pair is not matched on speculation.** The Qwen3.6 base ships a draft;
Ornith-1.5-35B-A3B ships none. Speculation does not change what a model outputs,
so every accuracy comparison here is unaffected. Throughput is affected, and the
gap on that pair includes the fact that one of them comes with a draft and the
other does not. That is a real difference between two things a reader can
download. Shipping no draft is a choice the publisher made, and correcting for
it would report a model nobody can obtain.

## What a null would mean here

The expectation predicts nulls, which is the most dangerous kind of prediction to
hold, because a null is exactly when it is easiest to stop looking.

A null here has to be a *measured* null with an interval. If a comparison does
not separate, this article will say that 1,001 notes could not tell the two
apart — not that the finetune is no better. Those are different statements and
only the first is supported by an interval that contains zero.

The reverse discipline is owed too. A separating result contradicts the
expectation, which is exactly when it is tempting to hunt for a defect until it
goes away. A win gets the same scrutiny a null gets and no more: check output
health, check the pair is matched, report it.

If a large shift does appear, the first question is whether the finetune changed
what the model **knows** or what it **emits**. The harness separates those
already: `score.json` records `output_health` beside the score — JSON parse rate,
schema rate, and the completion-token distribution. A finetune that stops
producing parseable output scores badly without having lost any knowledge, and
that reads as a large shift unless the health fields are read beside it.

That check has earned its place twice in this series. It is what identified two
NVFP4 conversions as broken rather than merely worse — one failing JSON parsing
on 29% of notes, another emitting 33 tokens a note against 369 for its sibling.
It is also what characterised the two-bit QAT collapse as instability rather than
degradation: one model went quiet, the other would not stop.

## Extraction

**No result yet.** Four runs are registered and none has been taken. This section
will carry the 1,001-note strict F1 for each pair with its paired bootstrap
interval, and the output-health fields beside it.

The base half of the 35B pair is already measured and will be reused rather than
re-run: `qwen36-35b-a3b.base.q4`, UD-Q4_K_XL, `-ncmoe 19`, f16 cache, strict F1
**0.7194** on this corpus.

## Synthesis

**No result yet.** Synthesis is a separate suite with its own metrics and its own
interval count, and its numbers do not compare to an extraction F1. Content F1,
required-field recall and the usability columns will be reported as their own
thing, as they are in the quantization article.

This half exists because of a specific failure in this series: a QAT pair was
once called a tie on extraction and a second task later separated it. The
correction came from measuring the other half, not from re-reading the first.

## What this can and cannot support

It can say whether a given Ornith build extracts facts or writes syntheses better
than the Qwen it was made from, on these two tasks, at four bits, on one card.

It cannot rank Ornith against anything outside its own lineage. It cannot
separate the finetune from the quantization recipe on the two rungs where Ornith
publishes only Q4_K_M. And it cannot say anything about the tasks it did not run.

A null is a real result here. "The finetune did not beat its base on this work"
is the outcome most worth stating plainly, if it is what the intervals say.
