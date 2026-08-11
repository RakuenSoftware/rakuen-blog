---
title: "A 2B Fact Extractor Came Within 0.047 of a 31B One"
date: 2026-08-09
author: Rakuen Software
tags: [local-models, benchmarks, fact-extraction, aimee]
excerpt: "On one 1,001-note corpus, model size moved the aggregate score less than architecture, prompting and output discipline did. The remaining risk is hidden by that score."
---

*Rakuen builds aimee, the system measured here. Run identities and figure sources
are recorded in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/how-small-can-a-fact-extractor-be/evidence/figures.md).*

A two-billion-parameter model scored 0.6406 on 1,001 notes. A
31-billion-parameter model scored 0.6872. The paired difference in the harmonic
mean of precision and recall (F1) was **+0.0465**, with a 95% bootstrap range
from **+0.0220 to +0.0712**.

That is a real gain on this corpus. It is also smaller than gains I measured from
a prompt change on one model and a quantization change on another. Size was not
the only variable worth buying.

## Rung-by-rung comparisons hid the endpoint gain

Every run below used the same prompt and the same 1,001 notes.

| model | parameters | F1 |
|---|---:|---:|
| gemma-4-E2B | 2B | 0.6406 |
| gemma-4-26B-A4B | 26B total, about 4B active | 0.6804 |
| gemma-4-12B | 12B | 0.6854 |
| gemma-4-31B | 31B | 0.6872 |

I initially compared six adjacent runs down the ranking. Every paired range
crossed zero:

| comparison | difference | 95% range |
|---|---:|---:|
| 31B quantization-aware training (QAT) to 12B QAT | −0.0017 | −0.0202 to +0.0162 |
| 12B QAT to 26B Unsloth | −0.0051 | −0.0256 to +0.0154 |
| 26B Unsloth to 31B non-QAT | −0.0041 | −0.0258 to +0.0176 |
| 31B non-QAT to 12B non-QAT | −0.0009 | −0.0197 to +0.0180 |
| 12B non-QAT to 26B Google | −0.0179 | −0.0434 to +0.0071 |
| 26B Google to E2B QAT | −0.0168 | −0.0406 to +0.0070 |

The endpoint comparison still found +0.0465. Each rung had about 0.020 of
uncertainty in either direction, enough to hide a cumulative change while no
single step separated. A ladder needs both adjacent and endpoint comparisons.

## Equal F1 scores concealed different risks

The 31B and 12B quantization-aware-trained (QAT) runs were indistinguishable on
F1. Their outputs were not.

| model | F1 | recall | silent on factless notes | invented triples |
|---|---:|---:|---:|---:|
| gemma-4-31B QAT | 0.6872 | **0.8000** | **0.463** | **180** |
| gemma-4-12B QAT | 0.6854 | 0.7330 | 0.702 | 97 |

The 31B run found more facts and invented nearly twice as many triples on the
322 notes whose correct answer was silence. Both 31B variants behaved this way,
which points to the model rather than the quantization. That is an inference from
two variants, not a family-wide result.

If a reviewer checks every written fact, the recall may be worth the inventions.
If the model writes directly into a graph, restraint may matter more. F1 alone
does not make that decision.

## Sparse models separated resident size from running cost

Qwen3.6-35B-A3B, a mixture-of-experts model with about 3B parameters active per
token, beat gemma-4-31B QAT by **0.0386**, with a 95% range from **+0.0194 to
+0.0577**. It also produced 234.0 tokens per second, compared with 67.8 for the
dense Qwen3.6-27B. The 35B sparse and 27B dense runs were tied on accuracy:
**−0.0106**, with a range from **−0.0294 to +0.0088**.

That measurement separates two budgets. Total parameters determine how much
memory the model occupies. Active parameters help determine how much model data
is read for each token. A 26B sparse model also reached 323 tokens per second on
the same 16-gibibyte card class, but throughput still depends on the exact model,
quantization and server configuration.

Sparsity does not shrink the resident model. LFM2.5-8B-A1B at Q4_K_M occupied
5.16 gigabytes, so three copies did not fit on a 16-gibibyte card. That run used a
different process count, a known confound worth about 0.0105 F1 in this campaign.
Plan memory from total parameters and test speed from the served configuration.

## Below 2B, format failures set score floors

LFM2.5-1.2B parsed 73% of its answers and MiniCPM5-1B parsed 87%. Neither run hit
the context limit. The missing rows therefore point to malformed output, not
truncation, and their scores are lower bounds until the prompts are matched to
their formats.

LFM2.5-230M parsed every answer and scored 0.1309. Its low score was not a parser
failure. Parse rate distinguishes those cases; it does not prove capability by
itself.

Ten runs emitted no reasoning pass. On gemma-4-E4B, removing the sentence `No
prose, no markdown.` restored reasoning on 770 of 770 notes and added 0.116 to
relation-agnostic recall. I tested that diagnosis on four models. Twenty-eight
runs remain unchecked, so I cannot attribute every silent reasoning pass to the
same clause.

## The 2B result is a shortlist rule, not a universal cutoff

Start the shortlist around 2B to 4B, then compare its endpoint with the largest
model that fits. Report recall, invention rate, parse rate and unfloored F1 beside
the aggregate score. For sparse models, budget memory from total parameters and
measure throughput from active serving behavior.

Two cost observations are single-sourced in the campaign ledger because their
raw logs were not retained: central processing unit time ranged from 2,233 to
35,230 milliseconds per note, and the largest E4B quantization took 420 seconds
to load. Treat those as leads for a timed rerun, not purchasing figures.

The unresolved tests are the sub-2B prompt match, the reasoning-clause check on
the rest of the field, banked load-time measurements and a second corpus from a
different generator. Until those exist, 2B is where this corpus says to start,
not where fact extraction says capability begins.
