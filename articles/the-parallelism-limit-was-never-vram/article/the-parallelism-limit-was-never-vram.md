---
title: "Context Allocation Set the Small-Model Process Limit"
date: 2026-08-09
author: Rakuen Software
tags: [local-models, gpu, benchmarks, aimee]
excerpt: "An eight-gibibyte per-process context default constrained parallelism. CUDA plateaued at two isolated processes while Vulkan continued improving through four."
---

*Rakuen builds aimee, the system measured here. Hardware artifacts and
single-source operational observations are listed in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/the-parallelism-limit-was-never-vram/evidence/figures.md).*

I sized parallel model processes by weight memory. The actual constraint was an
eight-gibibyte key-value (KV) cache reserved for each process by a context default
I had not set. The extraction prompts used hundreds to a few thousand tokens,
while the server allocated for tens of thousands.

Setting context size explicitly changed what fit. It did not make the two graphics
backends scale alike.

## CUDA plateaued while Vulkan kept scaling

Steady-state throughput below uses per-request latency times process count, so
server startup is excluded.

| processes | RTX 5080, CUDA | RX 7900 XTX, Vulkan |
|---|---:|---:|
| 1 | 47.6 notes/min | 40.7 notes/min |
| 2 | 67.4 | 63.8 |
| 3 | 59.9 | 78.1 |
| 4 | 61.8 | **83.3** |

CUDA flattened after two processes. Vulkan continued improving through four and
passed the faster card. The sweep stops there. A six-process launcher cap was
based on an untested bandwidth assumption, so the XTX limit above four remains
unknown.

At one process the 5080 generated 359 tokens per second. At three processes, each
stream produced 148. Multiplying a single-stream number by process count would
overstate total performance by more than twofold.

## Shared slots were faster and failed repeatability

Thirty-two slots in one process reached 4.54 times the sequential speed. Two
executions matched on 63 of 100 raw completions and 75 of 100 extracted fact sets.
The benchmark therefore uses isolated single-slot servers and accepts lower peak
throughput to preserve self-reproduction.

The corpus is distributed round-robin. Its notes are ordered by domain, so
contiguous shards would give different processes different categories and produce
uneven runtimes.

## Startup biased short throughput sweeps

| card | 1 process | 2 processes | 3 processes | 4 processes |
|---|---:|---:|---:|---:|
| RTX 5080 | 56 s | 84 s | 107 s | 137 s |
| RX 7900 XTX | 61 s | 67 s | 83 s | 99 s |

Startup added about 30 seconds per server. It was negligible over 10,000 notes and
occupied a third to a half of a 200-note sweep. Rows divided by total wall time
therefore created a bias that grew with process count.

The exact startup seconds are single-sourced in the reporting ledger because the
sweep computed and discarded that column. They need a banked rerun.

## Quantization moved models across the 16-gibibyte boundary

The table compares builds produced with quantization-aware training (QAT) and
conventional post-training quantization.

| model | file | fits RTX 5080 with 15.92 GiB free | fits 24 GiB XTX |
|---|---:|---|---|
| gemma-4-12B QAT | 6.26 GiB | yes | yes |
| gemma-4-26B-A4B QAT | 13.27 GiB | yes | yes |
| gemma-4-26B-A4B non-QAT | 15.84 GiB | no | yes |
| gemma-4-31B QAT | 16.10 GiB | no | yes |
| Qwen3.6-27B | 16.40 GiB | no | yes |
| gemma-4-31B non-QAT | 17.53 GiB | no | yes |

QAT moved the 26B model from 15.84 to 13.27 gibibytes. On this 16-gibibyte card,
that changed the available model set rather than merely saving memory. The QAT
run produced 323 tokens per second and scored 0.6804.

Several sizes come from server logs and the reporting notes rather than a
dedicated size artifact. They should be remeasured before hardware purchasing.

Mixture-of-experts models still keep all experts resident. LFM2.5-8B-A1B at
Q4_K_M occupied 5.16 gigabytes, so three copies did not fit with their KV caches.
Sparsity instead reduced per-token weight traffic: on one RTX 5090 card class,
Qwen3.6-35B-A3B produced 234.0 tokens per second and dense Qwen3.6-27B produced
67.8. That comparison shows an architecture effect in the served runs; it is not
a universal active-parameter formula.

## Operational leaks cost more than completed rentals

During the recorded rental campaign, four completed 1,001-note runs cost between
$0.14 and $0.54 each. Those historical rates are provider observations, not
current quotes. The larger cost was a fleet of 25 instances billed at $2.68 per
hour while two did work.

The version 0 fleet endpoint returned a successful empty list. A query-string
variant revealed that the endpoint was deprecated, and version 1 exposed the
instances. Raw application programming interface responses and invoices were not
retained, so the figures are single-sourced in the campaign ledger.

Four duration thresholds, from 420 to 3,600 seconds, also abandoned hosts that
were still downloading or loading. File size increased download time while the
fixed deadline did not, so larger models were more likely to be replaced and
restart billing. Host exit state, container errors, disappearance from the fleet
and stalled disk activity relative to a later sibling were more useful signals.

Locally, 15 orphaned clients reduced one run from 38.7 to 8.8 notes per minute.
A finished server also held 14,828 of 16,303 mebibytes on the 5080 until the next
server failed its 6,390-mebibyte allocation. These host states are single-sourced
observations because process snapshots were not retained.

## Measure the whole serving configuration

Set context size from measured prompt and completion lengths. Sweep process count
on each backend rather than transferring a CUDA result to Vulkan. Compute steady
throughput without startup, then report startup separately. Size resident memory
from total parameters and test throughput on the exact served quantization.

Reap every child process from the script that created it. Compare the provider
fleet and local process state with billing rather than with intended work. Use a
duration to cap spending, not to diagnose a dead host.

The process curve above ends at four, and the only cross-card accuracy calibration
is CUDA-to-CUDA: **+0.0057** on the harmonic mean of precision and recall (F1),
with a 95% range from **−0.0136 to +0.0251**, and 640 of 1,001 identical
completions. The XTX uses Vulkan and a different server build. Cross-backend
accuracy remains unmeasured.
