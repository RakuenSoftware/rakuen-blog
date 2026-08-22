# KV Cache Precision

## Status

**Not an article yet. A recorded measurement and a design for the campaign that
would become one.**

What exists is a single-point study: one model, one weight format, one context
length, four cache configurations, extraction task only. It supports a narrow
but real finding, recorded below. It does not support a piece about KV cache
precision, because it holds fixed the variable that makes the subject
interesting.

This folder exists so the measurement is not lost, and so the campaign that
would complete it starts from a registered design rather than from memory.

## What was measured

LFM2.5-2.6B at BF16 weights, 8,192 context, on one RTX 5080, 1,001 notes of
corpus v5, four KV cache configurations varying only `-ctk` / `-ctv`.

Accuracy is unchanged. All three quantised configurations are indistinguishable
from the f16 default, and the q8_0/q8_0 interval is tight enough to be a real
null rather than an underpowered one:

| cache | delta vs f16 | 95% CI | verdict |
|---|---:|---|---|
| bf16 / bf16 | +0.0121 | [−0.0033, +0.0275] | indistinguishable |
| q8_0 / q8_0 | **−0.0007** | **[−0.0192, +0.0178]** | indistinguishable |
| q8_0 / q4_0 | +0.0085 | [−0.0145, +0.0317] | indistinguishable |

The cost is throughput, and it is not evenly distributed. Eight-bit is free;
four-bit V is a cliff:

| cache | KV size | vs f16 | generation tok/s | prefill tok/s |
|---|---:|---:|---:|---:|
| f16 | ~136 MiB | — | 150.28 | 13,086 |
| bf16 | ~136 MiB | 0% | 150.34 | 13,037 |
| **q8_0 / q8_0** | ~76 MiB | **−45%** | **149.13** | **12,936** |
| q8_0 / q4_0 | ~50 MiB | −60% | 112.14 | **3,338** |

`q8_0/q8_0` costs 0.8% of generation and 1.1% of prefill for a 45% smaller
cache, with an accuracy delta of −0.0007 in a range of [−0.0192, +0.0178]. On
this evidence it is free.

Taking V to four bits buys 26 MiB more and **collapses prefill by a factor of
four**, 13,086 to 3,338 tok/s, with generation down 25%. That arm took 13,173 s
against 8,672 s for the bf16 cache — the difference is prefill, on a
prefill-dominated task.

The generation spread widens too: q8_0/q4_0 ranges 74.1 to 131.5 tok/s across
1,003 samples, against 147.0 to 151.2 for bf16. Whatever the four-bit V path
costs, it costs it unevenly.

**The headline is therefore not "KV quantisation is the wrong lever." It is that
eight-bit KV is free and four-bit V is not**, at least here. Which of those
generalises is the question the campaign below exists to answer.

## Why this is not yet an article

**Context is fixed at 8,192, and context is the whole subject.** KV scales with
`context × layers × heads`; weights do not. Every interesting claim about cache
precision lives in that scaling, and this measures a single point on it — the
point where the technique is designed to look least useful, because the cache is
~136 MiB against 5,152 MiB of weights. Saving 60% of 2.5% of residency is not a
result about KV quantisation; it is a result about small models at short context.

**One model, and the smallest in the fleet.** Layer and head counts drive cache
size directly, so a 2.6B hybrid says little about a 35B mixture-of-experts.

**One task.** The synthesis half of these arms was collected and discarded twice
over, under two separate harness defects. No synthesis result stands.

## What the campaign needs, in value order

1. **A context sweep.** The same cache configurations at 8k / 32k / 128k on one
   model. This is the spine of the study and the only way to say whether the
   "wrong lever" reading above inverts or holds.

   This needs a different fixture. The extraction corpus is ~400-token notes, so
   it cannot exercise long context at any setting; running it at 128k would
   measure allocation, not use. Designing that fixture is the largest single
   piece of work here and should not be improvised.

2. **A large model.** 26B-A4B or Qwen3.6-35B-A3B, where the cache is a real share
   of residency and VRAM is already the binding constraint that forces expert
   offload. A 60% cache cut there may decide whether an arm fits on the card at
   all, which is worth 25% of throughput in a way that 86 MiB is not.

3. **The q4_0/q4_0 rung**, closing the low end. Queued in the quant campaign as
   arm 8 and will be folded in here when it lands.

4. **Both tasks**, once the synthesis harness is trusted. See the quant article's
   measurement log for why it currently is not.

The 2.6B measurement then stops being the study and becomes its control point —
the small-model, short-context case that explains why the question is worth
asking at scale.

## Provenance

Collected as part of the quant ladder campaign; see
`articles/which-quant-beats-how-many-bits/evidence/moe-ladder-plan-2026-08-16.md`
for the harness, the hardware and the serving configuration, and
`moe-ladder-measurement-log-2026-08-16.md` for the defects found while running
it, several of which apply to any future use of the same harness.

`evidence/arm-records-2026-08-17.json` holds the complete per-arm records as
written by the harness: served model path and file type, cache types, resident
and GPU memory, the full score object, and the throughput distributions — 1,003
generation and 1,003 prefill samples per arm — that the tables above summarise.

Larger artifacts (predictions, scores, server logs) remain on the benchmark host
in the campaign results directory, under labels beginning `lfm25-2.6b.base.bf16`.

The KV cache sizes quoted above are **derived, not logged**. This llama.cpp build
emits no `KV self size` line at any verbosity, so cache size is solved from the
VRAM deltas against the known bits-per-element of each format: f16 is 16, q8_0
is 8.5, q4_0 is 4.5. The q8_0/q8_0 and q8_0/q4_0 observations independently imply
~128 MiB and ~145 MiB, which is the basis for quoting ~136 MiB. Treat the cache
sizes as ±10%. The throughput, accuracy and total-VRAM figures are measured
directly.
