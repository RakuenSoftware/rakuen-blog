---
title: "We Forced It to Think and the Score Fell"
date: 2026-08-13
author: Rakuen Software
tags: [local-models, quantization, reasoning, benchmarks, aimee]
excerpt: "One quantization answered 13% of notes with no reasoning pass. Forcing it to reason cost 0.21 F1 on those notes, and most of that turned out to be our corpus rather than the model."
---

*Rakuen builds aimee, the system measured here. Every run behind these figures is
listed in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/we-forced-it-to-think-and-the-score-fell/evidence/figures.md).*

A model that declines to reason looks broken. Ours declined on 13% of notes, and
whether that was a fault worth fixing is a question our benchmark turned out to
answer badly.

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

A reader who meets this in their own logs will reach for the prompt or the
sampler. Neither is where it lives.

## Removing the choice made the score worse

Silent notes scored **0.8507** on the harmonic mean of precision and recall (F1).
The 863 notes the model reasoned about scored **0.4212**. That gap cannot be read
on its own, because the model is the thing choosing which notes go into which
group.

So we changed one clause, from "Reason first if it helps" to "Reason first on
every note", and ran both against a single server process with the same weights,
cache size and concurrency.

Of 134 silent notes, 67 then reasoned. They fell to 0.6418: **−0.2090**, with a
95% range of **−0.3284 to −0.0896** over 20,000 bootstrap replicates. The 863
notes that reasoned under both prompts moved −0.0028, so the new sentence is
worth almost nothing by itself, and the 67 notes that stayed silent under both
moved −0.0448, which bounds how much of this is a high-scoring group falling back
toward the mean.

We were ready to publish that as the model knowing which notes were easy.

## Then we looked at the notes

The loss is not spread across 67 notes. Forty-seven are unchanged, three improve,
and **17 go from 1.00 to zero**. Every note that got worse got worse completely.

Those seventeen have a shape:

```
Aldridge Chemicals signed as a customer.
  gold      customer_of -> "user"
  silent    customer_of -> "user"
  reasoned  customer_of -> "customer"
```

The gold object is `user`, the implicit other party. Answering directly, the
model produced the convention. Forced to reason, it produced the more literal
reading of the sentence and scored zero.

**10 of the 17 are that case.** The remaining seven are ordinary errors,
of which this is the clearest:

```
Ming Lei contributes to linux.
  gold      member_of, with contributes_to accepted
  silent    contributes_to
  reasoned  works_for
```

## What the benchmark can and cannot say

**Never read a paired delta without opening the notes underneath it.** The
headline is a real measurement and it survives both controls, and it is still
mostly our corpus. Ten of seventeen damaged notes are the model reasoning its way
off a labelling convention, not off the fact.

So the honest result is narrower than the one we had. Forcing reasoning cost 0.21
F1 on the skipped notes. Under 0.12 of that is the model getting anything wrong,
and the rest is a scoring convention that rewards a model for not thinking about
what the object should be.

**Check whether the corpus has an implicit party before scoring objects.** A gold
object of `user` is unrecoverable from the sentence, so it measures whether the
model guessed the house style. The second corpus we are building specifies notes
that name both ends.

**Never let a skip stand as a defect on this evidence alone.** We cannot say the
model was right to skip. We can say that forcing it stopped it matching our
conventions, that we would have reported the stronger claim if we had stopped at
the mean, and that the seventeen notes were three minutes of reading away.

One more thing survived, and it has nothing to do with scoring. Exactly half the
silent notes ignored the instruction: 67 reasoned, 67 did not, under a prompt
telling them to reason on every note. Whatever decides this sits below the level
a sentence reaches, which is the same thing the quantization table says.
