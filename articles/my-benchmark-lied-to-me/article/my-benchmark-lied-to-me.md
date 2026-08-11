---
title: "Eight of Nine Benchmark Failures Were Visible in Discarded Data"
date: 2026-08-09
author: Rakuen Software
tags: [benchmarks, measurement, local-models, aimee]
excerpt: "Startup time, client count, sequence position and mechanism counters exposed eight failures that the headline score concealed. The ninth never had an interval."
---

*Rakuen builds aimee, the system measured here. Evidence types and missing raw
artifacts are identified in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/my-benchmark-lied-to-me/evidence/figures.md).*

Nine benchmark defects pushed my conclusions in a convenient direction. In eight
cases, the output already contained the field that could have caught the error.
The ninth began with a number that never had an interval.

The repeated failure was not a bad score. It was printing the score and discarding
the denominator, timer, state or mechanism counter needed to interpret it.

## Startup time reversed the throughput curve

I measured throughput as completed rows divided by wall time. Wall time included
server startup, which increased with process count.

| card | 1 process | 2 processes | 3 processes | 4 processes |
|---|---:|---:|---:|---:|
| RTX 5080 | 56 s | 84 s | 107 s | 137 s |
| RX 7900 XTX | 61 s | 67 s | 83 s | 99 s |

On a 200-note sweep, startup occupied a third to a half of the measurement. The
biased calculation said throughput peaked at two processes and that four were
slower than one. Removing startup and using per-request latency times process
count changed the decline into a plateau; four processes were 30% to 100% faster
than one.

The exact startup seconds are single-sourced in the campaign ledger because the
sweep computed the column and then discarded it. They require a banked rerun.

## Orphaned clients made the card look four times slower

One run fell to 8.8 notes per minute. Fifteen clients left by killed runs were
still sending valid requests through the same three ports. The server looked
healthy because it served every request; the client queue absorbed the delay.
After I killed the orphans, the same in-flight run reached 38.7 notes per minute.

This is a single-sourced host observation. No process snapshot survives. The
ledger does retain the clue: a load average of 27 for six hours on a machine used
only to shuttle structured data through three secure-shell tunnels.

The cleanup handler now reaps children on exit and signals. The run report also
compares the observed client count with the configured process count.

## A borrowed effect size became a significance rule

I used 0.0105 as the threshold for a meaningful difference. It was not an
uncertainty bound. It was the measured effect of process count in another test.
At 1,001 notes, paired ranges in this campaign were often about ±0.024.

Replacing 0.0105 with 0.024 would repeat the mistake. Each comparison now gets
its own paired bootstrap range. The bootstrap tool was already in the repository;
I had stopped consulting it.

## Sequence position made a subset a different run

The same model processed 1,001 notes alone and inside a 3,002-note run.

| measurement | result |
|---|---:|
| native 1,001-note score | 0.6406 |
| same notes inside the 3,002-note run | 0.6327 |
| byte-identical completions | **529 of 1,001** |

Changing the preceding note did not explain the churn: identity failures were
44.8% with the same predecessor and 48.3% with a different one. Disabling the
prompt cache also failed, reducing identity from 52.8% to 49.9%. A seeded shuffle
with the cache disabled reproduced 52.3% identity.

The surviving explanation is sequence position. That is an inference from the
controls, not a demonstrated internal mechanism. The score difference was
−0.0079 and did not move a ranking, but the comparison was still invalid. Shared
notes now retain the same sequence positions.

## A 70-note estimate spread without an interval

The source files said reasoning was worth +0.084 on the harmonic mean of precision
and recall (F1) to E4B. The estimate reached their commit messages too. It came
from 53 true positives across about 70 notes and had no uncertainty interval.

Remeasured on 955 paired notes, the gain was **+0.0103**, with a 95% range from
**−0.0201 to +0.0404**. Only its sign survived. A measured constant now enters
source code only with its sample, interval and provenance.

This was the sole failure with no discarded diagnostic column. The interval was
never computed.

## My display recreated a scorer bug that source had prevented

Three factless categories appeared as 0.0000 in every run, which I described as a
blind spot in F1. The scorer already returned `null` for those categories and
explained why in a comment. My analysis script converted `null` back to 0.0.

Those rows were also present in overall F1. Removing their false positives added
**0.040 to 0.053** across six runs. The metric was not blind; the display and my
story were.

## A deprecated endpoint concealed rented machines

During the recorded rental campaign, `GET /api/v0/instances/` returned a
successful empty fleet. Adding a query string exposed a deprecation response that
pointed to version 1. That endpoint showed **25 running instances billed at $2.68
per hour**, while two were doing work. Four had been running for about ten hours.

The raw application programming interface responses were not retained, so these
figures are single-sourced operational observations from the campaign ledger.
The prevention does not depend on that provider: compare each instance start time
with the oldest running orchestrator. An older instance cannot belong to it.

## Duration thresholds diagnosed slow hosts as dead

I abandoned rented hosts after 420 seconds, then 900, then 600 from container
start, and finally after a 3,600-second cap. All four rules discarded hosts that
were still working. Larger models took longer to download, so the false-positive
rate grew with the tested variable and each replacement restarted billing.

The useful signals were categorical: an exited instance, a container-engine
error, disappearance from the provider response, or absent disk activity while a
later sibling reported progress. These observations survive only in the campaign
ledger, not raw provider snapshots. A duration can enforce a budget; it cannot by
itself diagnose a dead host.

## Throughput did not prove speculative decoding

Qwen3.6-35B-A3B produced 234 tokens per second. I attributed that speed to
multi-token prediction (MTP), a speculative-decoding method, without checking the
mechanism fields. The measured prediction rows contain no draft counters and the
server properties reported speculation as null. The run therefore provides no
evidence that speculation was active.

The repository fact also changed. As of 2026-08-09, the primary ggml-org
[Qwen3.6-27B repository](https://huggingface.co/ggml-org/Qwen3.6-27B-GGUF/tree/main)
and [Qwen3.6-35B-A3B repository](https://huggingface.co/ggml-org/Qwen3.6-35B-A3B-GGUF/tree/main)
publish MTP sidecars. Their present availability does not show that the measured
run used one. The original claim is narrowed to the run: no observed draft
counters, no mechanism claim.

On 2026-08-10 both models were rerun on one card as explicit speculation-on and
speculation-off pairs. With speculation on, all 1,001 rows carry a draft count:
the 27B accepted 79.0% of 1,020,888 drafted tokens, the 35B-A3B 76.6% of
1,034,913. With it off, no row carries one.

That is the signature the 234-tokens-per-second run lacked. Accuracy moved by
0.0003 and 0.0068 across the two pairs, so the mechanism was legible in a
recorded field and never in the throughput number.

## Print the fields that can falsify the score

- Print process count, startup time, sample size, client count, slot count and
  draft acceptance beside throughput and accuracy.
- Give every comparison its own paired uncertainty range.
- Keep shared notes at the same sequence positions or treat the executions as
  different configurations.
- Put a sample, interval and source beside every measured constant in code.
- Use duration as a budget limit, not as a diagnosis.
- Treat a successful empty response as a claim to verify against billing and
  local process state.

Eight failures needed one more printed field. The ninth needed an interval before
the number was allowed to travel.
