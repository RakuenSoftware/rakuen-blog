---
title: "Repeatability Belonged to the Configuration, Not the Model"
date: 2026-08-09
author: Rakuen Software
tags: [reproducibility, benchmarks, local-models, aimee]
excerpt: "Speculative decoding and isolated processes repeated exactly. Shared slots did not. Process count, cache state and sequence position were part of run identity."
---

*Rakuen builds aimee, the system measured here. Reproduction artifacts and
single-source probes are listed in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/repeatable-is-not-identical/evidence/figures.md).*

Speculative decoding changed 26 of 100 completions and still repeated itself
exactly. Thirty-two shared slots were faster and failed to repeat. One and three
isolated processes each repeated exactly while remaining 0.0105 apart on the
harmonic mean of precision and recall (F1).

The model was not the reproducibility unit. The serving configuration was.

## Self-reproduction separated useful speed from noise

Multi-token prediction (MTP) is the speculative method used in two configurations
below.

| configuration | speed | matches sequential | repeats itself |
|---|---:|---:|---:|
| sequential | 1.00× | reference | yes, four confirmations |
| speculative decoding | 1.83× | 74 of 100 | **100 of 100 on two models** |
| 32 slots | 4.54× | 804 of 1,001 | no |
| 32 slots with multi-token prediction (MTP) | 4.34× | 64 of 100 | **75 of 100 facts** |
| 3 isolated processes with MTP | unmatched hardware | unmeasured | **1,001 of 1,001** |

A benchmark need not reproduce a different configuration. It must reproduce
itself and use the same configuration for every compared run.

The 32-slot MTP setup failed that test. Two executions matched on 63 of 100 raw
completions and 75 of 100 extracted fact sets. Wall time also moved from 71 to 61
seconds. The 804-of-1,001 sequential comparison in the table is single-sourced in
the reporting ledger because its derived file was not retained.

The measurements show scheduling-sensitive output; they do not identify the
internal numerical mechanism.

Isolated processes held. A single-sourced ledger probe matched two processes on 60
of 60 notes. Three executions of a three-process run matched byte for byte on all
1,001 notes in all three pairwise comparisons and scored 0.6138 each time. Two
prediction pairs are banked; the third execution is single-sourced in the article
notes.

One process also repeated 1,001 of 1,001 at 0.6033.

## Two stable process counts stayed 0.0105 apart

The one- and three-process runs used the same model, quantization, prompt and
decoding settings. They matched on 652 of 1,001 completions and differed by
**0.0105 F1**.

Neither configuration drifted. Comparing across them would still mix serving
effects with the model variable. Sample size cannot repair a configuration
boundary.

An earlier 0.6114 reference looked like a one-slot result but its device record
showed four slots. It moved 645 completions against one honest configuration and
688 against the other. A recorded field that analysis ignores does not protect a
comparison.

## Warm state, batching and cache state changed text

A cold server reproduced 20 of 20 notes across restarts. Compared with a warm
server, it reproduced 14 of 20, with the same six notes changing each time. That
probe is single-sourced in the reporting ledger and does not isolate which live
state caused the changes.

Speculative verification changed the target batch shape and 26 of 100
completions, consistently. Cache on versus cache off matched 792 of 1,001.
Turning the cache off took 38 minutes rather than 41 on this workload, so its
expected cost did not appear in the measurement.

Each change moved text without moving F1 outside its paired range. Output identity
and score stability answer different questions.

## Sequence position made a subset a different run

The same 1,001 notes matched on only 529 completions when executed alone and
inside a 3,002-note corpus. Two plausible explanations failed their controls.

| hypothesis | test | result |
|---|---|---|
| preceding note | split churn by predecessor identity | 44.8% vs 48.3%, refuted |
| prompt-cache history | rerun with cache disabled | 49.9% vs 52.8%, refuted |
| sequence position | seeded shuffle with cache disabled | supported |

| cache-disabled comparison | byte-identical completions |
|---|---:|
| same notes, same order | **1,001 of 1,001** |
| same notes, shuffled | **524 of 1,001** |
| same notes inside 3,002-note corpus | 499 of 1,001 |

Shuffling reproduced the cross-corpus churn to within 25 notes. Sequence position
is therefore the supported variable. The test does not show which server state
carries across requests, so the article does not assign a mechanism.

## The concurrency result lacked its control

Thirty-two slots were 4.54 times faster and changed extracted facts on 197 of
1,001 notes relative to the reference. Moving from one to 32 slots also changed
cache reuse, and the warm-server probe had already shown six changes in 20 notes.
The 197 is an upper bound on the concurrency effect, not a measurement of it.

## Hardware changed text within the measured score range

One cross-card test ran the same configuration on an RTX 3090 and RTX 5080. The
cards matched on 640 of 1,001 completions. The score difference was **+0.0057**,
with a 95% range from **−0.0136 to +0.0251**.

The paired prediction files were not retained together, so this result is
single-sourced in the campaign ledger. No matched Vulkan-to-CUDA crossing exists
for the RX 7900 XTX and RTX 5080. Long-generation identity was also not tested.
Throughput for isolated processes and single-process speculation was measured on
different cards and cannot be divided into a valid speed comparison.

## Record the full configuration and make it reproduce itself

Run one configuration three times before trusting it. Record and consume slot
count, process count, cache setting, hardware, server build and decoding mode.
Keep shared notes at the same sequence positions. Never compare a native run with
a subset extracted from a larger one.

Use output identity to detect execution changes and paired score ranges to decide
whether those changes affect the metric. For this workload, isolated processes
and speculation passed self-reproduction; shared slots did not.
