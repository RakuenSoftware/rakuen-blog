---
title: "One Prompt Sentence Suppressed 10,000 Reasoning Passes"
date: 2026-08-09
author: Rakuen Software
tags: [prompting, local-models, benchmarks, aimee]
excerpt: "A formatting instruction cut a model's reasoning pass to zero while every answer parsed. The run looked ten times faster because it was doing different work."
---

*Rakuen builds aimee, the system measured here. Run sources and single-source
observations are listed in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/one-sentence-turned-the-reasoning-off/evidence/figures.md).*

A 10,000-note extraction run finished in 34 minutes instead of the expected six
hours. Every answer parsed and the score looked plausible. In this article, F1
means the harmonic mean of precision and recall. The model had emitted no
reasoning tokens because the prompt ended with:

    No prose, no markdown.

The sentence was intended to constrain the answer. Gemma-4-E4B applied it to its
reasoning channel.

## Prompt ablations isolated one sentence

Every row in the banked run recorded `thinking: true`; none contained reasoning.
Ablations separated the suspect instruction from the other formatting rules.

| system prompt | notes that reasoned |
|---|---:|
| version 4, unchanged | 0 of 20 |
| without `No prose, no markdown.` | 20 of 20 |
| without `Return ONLY a JSON object:` | 0 of 20 |
| answer rescoped to JSON only | 0 of 20 |
| version 5, reasoning explicitly permitted | 20 of 20 |

These four 20-note probes are single-sourced in the reporting ledger because
their raw outputs were not retained. A later banked control restored the original
clause and suppressed reasoning on **1,001 of 1,001** notes. Removing the output
constraint restored reasoning on **770 of 770**.

Deleting the sentence was not sufficient for production. It brought fenced JSON
back on 14 of 20 notes. The replacement explicitly permits reasoning and limits
only the final answer. Two attempted rewrites failed before that wording held.

Two independent quantized builds with different chat templates both reproduced
the suppression. That rules out those two builds as the cause; it does not prove
that every E4B serving stack behaves the same way.

## The answer channel concealed the missing work

The original run parsed 10,000 of 10,000 answers. Its median completion was 27
tokens, plausible for a corpus that was one-third factless. The contradiction was
already present in each prediction row:

```json
{"thinking": true, "reasoning_chars": 0, "parse_ok": true, "truncated": false}
```

| measurement | banked run | reasoning restored |
|---|---:|---:|
| median completion | 27 tokens | about 390 tokens |
| median latency | 214 ms | about 1,790 ms |
| notes that reasoned | 0 of 10,000 | 20 of 20 |
| throughput | 280/min | 27/min |

The restored 20-note medians and the 34-minute wall time are single-sourced
ledger observations. The banked prediction rows independently preserve the
missing reasoning. An unexpectedly fast run is now treated as a diagnostic, not
as a free performance gain.

## A small estimate became a source-code constant

The reason for enabling reasoning had also drifted. “Thinking is worth +0.084 F1
to E4B” appeared in two source files and their commit messages. It came from 53
true positives across about 70 notes, with no interval.

On 955 paired notes, using the same model, quantization, card and corpus, the
strict score changed by **+0.0103**, with a 95% range from **−0.0201 to
+0.0404**.

| mode | strict F1 | precision | recall |
|---|---:|---:|---:|
| reasoning suppressed | 0.5990 | 0.6607 | 0.5478 |
| reasoning restored | 0.6093 | 0.6175 | 0.6014 |

The original constant was eight times the remeasured difference and lacked the
uncertainty needed to support the design decision.

## Production scoring found a gain that strict F1 blurred

Of the 93 additional false positives produced with reasoning restored, 68 could
be reconciled by production's relation-name canonicalizer and entity graph. When
scored on entity pairs without requiring the exact predicate name:

| mode | relation-agnostic F1 | precision | recall |
|---|---:|---:|---:|
| reasoning suppressed | 0.7783 | 0.8585 | 0.7118 |
| reasoning restored | 0.8390 | 0.8503 | 0.8280 |

Recall increased by **0.116** at similar precision. Both runs had a fabrication
rate of 0.0, while silence on factless notes fell from 0.907 to 0.870.

The 0.116 difference has no uncertainty interval because the bootstrap tool
scores strict F1 only. It is a first-party measurement and the largest unbounded
effect in this article. It supports a follow-up test, not a portable constant.

## Reasoning behavior varied by model and note category

Seven of fourteen small models emitted no reasoning at all. A no-constraint probe
left Granite-4.1-3B at 0 of 1,001, SmolLM3-3B at 0 of 798 and LFM2.5-230M at 0 of
570. The E4B positive control reasoned on 770 of 770, so the three zeroes were not
caused by this formatting clause.

Gemma-4 E4B under quantization-aware training skipped reasoning on 479 of 3,002
notes, a stable 16% at two corpus sizes. On the 2,523 rows where it did reason, it
scored 0.6238 against E2B's 0.6420. The missing pass is real but does not explain
the model gap. Context exhaustion, truncation and output-envelope failure were
also absent, leaving the cause open.

The aggregate strict-score change also hid opposing category effects: about
**+0.24 F1** on one subset and **−0.02** on another. Those category results have
no reported intervals. They show why the aggregate needs stratification; they do
not establish two population effects.

Six larger runs reasoned on every row, while seven smaller models reasoned on
none. I tested the clause diagnosis on only four of twenty-two models. The pattern
could reflect capability, resistance to the prompt, or both.

## Make observed reasoning a run gate

Print the share of rows with reasoning, not only the requested configuration.
Refuse to score a run that requests reasoning and observes none. Treat a major
speed increase as evidence that the workload may have changed.

Measured constants should enter source only with their sample, interval and
provenance. Aggregate nulls should be split by the corpus strata selected before
the comparison. The partial E4B behavior and the unbounded relation-agnostic gain
remain open tests, so neither belongs in a default setting yet.
