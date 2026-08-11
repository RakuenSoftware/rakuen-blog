---
title: "The 12B Synthesis Run Scored Higher and Missed the CPU Question"
date: 2026-08-09
author: Rakuen Software
tags: [local-models, synthesis, benchmarks, aimee]
excerpt: "A 12B configuration gained 0.071 on the content score and took four times the median latency. Both used graphics hardware, so neither selected the intended CPU model."
---

*Rakuen builds aimee, the system measured here. Every figure and reporting limit
is listed in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/synthesis-model-selection/evidence/figures.md).*

A 12B synthesis configuration scored 0.3279 against E2B's 0.2567 on 10,000 paired
cases. The content score averages, across required fields, token-overlap or
set-overlap harmonic means of precision and recall (F1), as defined by the
[pinned scorer](https://github.com/RakuenSoftware/aimee/blob/5e1b962491f7fe08a5cf34a9f524aaa4b1157d37/benchmarks/gemma4_baseline/run_synthesis_ab.py#L79-L126).
The gain was **+0.0712 content F1**, with a 95% paired bootstrap range from
**+0.0672 to +0.0750**.

The 12B median request took 42.4 seconds. E2B took 10.7. Both were graphics
processing unit (GPU) runs with different maximum-throughput serving profiles, so
the result does not answer the production question that named this campaign:
which model provides acceptable synthesis on the central processing unit (CPU)
tier.

## The quality gain was concentrated in one task

The frozen suite contains five structured-output tasks drawn from one 10,000-case
population. Every 12B task score was higher, but the size of the gain varied.

| task | cases | E2B content F1 | 12B content F1 | difference |
|---|---:|---:|---:|---:|
| claim | 2,500 | 0.1854 | 0.2117 | +0.0263 |
| code unit | 2,500 | 0.3835 | 0.4134 | +0.0298 |
| document summary | 2,000 | 0.4284 | 0.4711 | +0.0428 |
| entity | 1,500 | 0.0720 | 0.0900 | +0.0180 |
| synthesis | 1,500 | 0.1203 | 0.4261 | **+0.3058** |

Differences use the unrounded run values rather than subtracting the four-decimal
display columns.

The aggregate gain therefore does not describe a uniform model improvement.
The largest movement came from the task named `synthesis`; the other four gains
ranged from 0.0180 to 0.0428. The article reports no task-level intervals, so
those rows describe the measured suite rather than five population effects.

## Schema validity improved while required-field recall fell

| measurement | E2B | 12B |
|---|---:|---:|
| raw parse rate | 99.79% | 100.00% |
| schema-valid rate | 97.41% | 99.96% |
| required-field recall | **99.00%** | 97.57% |
| truncated rows | 21 | 0 |

The 12B run almost always returned every schema key, yet some values were empty
and its required-field recall was lower. The code-unit task carried the
difference: 12B required-field recall was 90.37%, compared with 98.47% for E2B.
A syntactically valid object can still omit usable field content, so schema
validity and field recall must remain separate gates.

## The speed comparison belongs to two serving configurations

| measurement | E2B | 12B |
|---|---:|---:|
| median latency | 10.7 s | 42.4 s |
| 95th-percentile latency | 37.7 s | 91.8 s |
| decode rate | 8.61 tokens/s | 2.41 tokens/s |
| cold load | 12.7 s | 40.9 s |
| slots and workers | 64 | 32 |
| aggregate context | 131,072 tokens | 65,536 tokens |
| memory after run | 4.23 gibibytes | 23.77 gibibytes |

The 12B profile used half as many concurrent slots because its weights left less
room on the 24-gibibyte device. These are deployment configurations tuned to fit,
not a controlled one-variable latency experiment. The observed median ratio is
3.96 times; it cannot be assigned to parameter count alone.

The memory records also rule out the intended local CPU conclusion. They record a
graphics device, not CPU latency, memory pressure or throughput. A GPU comparison
cannot decide whether either model meets the CPU service budget.

## Silver labels support selection, not absolute quality

The expected outputs are de-identified silver labels derived from committed
artifacts and their citations. They are suitable for comparing two runs on the
same cases. They are not a human-audited gold set, so 0.3279 is not an estimate of
absolute semantic correctness.

The two summaries share the same fixture-manifest hash. Validation recomputed
10,000 latest rows per model, verified artifact hashes and passed a secret scan.
The 12B raw file retains 13 superseded attempts; last-row selection prevents those
retries from changing its denominator.

## Keep 12B as the quality candidate and rerun the real decision

The 12B configuration is the quality candidate for this frozen GPU suite. E2B is
the latency and memory candidate. Neither is the selected CPU model.

Run both on the production CPU profile with the same slot count, context and
binary. Set the service latency budget before the run, preserve schema validity
and required-field recall as separate gates, and add the missing model ladder only
after the paired CPU baseline exists. Until then, shipping either model as the
CPU winner would answer a question this benchmark did not measure.
