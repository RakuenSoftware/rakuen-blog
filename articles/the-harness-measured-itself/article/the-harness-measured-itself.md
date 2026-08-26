---
title: "The Harness Measured Itself"
date: 2026-08-26
author: Rakuen Software
tags: [benchmarks, measurement, local-models, aimee]
excerpt: "A confidence gate, a parser, a truncation flag, a name guard, a throughput figure, a size ladder and three kinds of zero each returned a plausible number about the harness rather than the model."
---

*Rakuen builds aimee, the system measured here. Run identities and figure sources
are recorded in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/the-harness-measured-itself/evidence/figures.md).*

A run of this benchmark returns a score for the model. Several times in this
campaign it returned a score for the benchmark instead, and the number looked the
same either way. In this article, F1 means the harmonic mean of precision and
recall.

Almost every one of those failures had a signal that could have caught it, already
being written to the prediction rows and not being read. The exception was a
comparison the ladder never made.

## A confidence gate inverted the ranking

`Qwen3-0.6B` scored 0.000 with the confidence floor and 0.403 without it.
`granite-4.0-350m` moved from 0.000 to 0.206. Both extracted facts and assigned
them confidence 0.0; the gate discarded every one.

Self-reported confidence carried almost no signal across the sixteen models. Most
wrote 0.0 or 0.9 and nothing between. I replaced the floor with a check that both
endpoints appear in the note.

The gate also reversed a size comparison. Floored, a 1B Granite model beat a 3B
one, 0.600 to 0.571. Unfloored, the 3B won, 0.648 to 0.592. That table measured
the gate, not model size.

Two other zeroes had the opposite cause. `SmolLM2-360M` and `gemma-3-270m` parsed
every answer but never used the required `{"facts": [...]}` schema. `Qwen3-0.6B`
parsed and matched the schema, then lost its facts at the floor. Parse rate and
schema rate separate those diagnoses.

## The parser and the guard each hid a working run

The output used the wrong envelope. One model returned a valid extraction inside
a tool-call wrapper. Completion length stayed normal while parse rate collapsed.
The model understood the note; the parser could not see its answer.

The raw wrapper output was not retained, so this diagnosis is single-sourced in
the reporting ledger.

The context ended before the completion limit. My truncation guard compared
completion tokens with `max_tokens`. A request that exhausted the total context
never reached that completion limit, so the guard could not fire. Prompt tokens
plus completion tokens must be compared with context size.

Both failures scored as incapacity. Neither model was incapable, and in both
cases the run had already recorded the number that separates the two.

## A valid model failed the identity guard

My model guard derived an expected family name from a repository name. Google's
file `gemma-4-E2B_q4_0-it.gguf` did not contain the generated stem, so the guard
blocked a model that had loaded correctly. The refusal survives only as a
single-sourced host observation in the reporting ledger.

The replacement keeps the guard and permits an explicit, documented identity
override. A guard around a naming convention you do not control needs a path for
the valid exception.

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

Those two pairs are part of the eleven reported in
[Local LLMs: Speculative Decoding](https://rakuensoftware.com/blog/speculative-decoding-was-free),
which measures what speculation is worth when it is switched on deliberately.
This article uses them only as the control that shows what the earlier run failed
to record.

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

The endpoint comparison still found **+0.0465**, with a 95% range from **+0.0220
to +0.0712**. Each rung carried about 0.020 of uncertainty in either direction,
enough to hide a cumulative change while no single step separated. A ladder needs
both adjacent and endpoint comparisons.

## A zero can be a measurement, a floor, or a field nobody wrote

A number that reads zero meant one of three things in this campaign. The value
was measured and it was zero, a run failed in a way the scorer counts as zero, or
nobody wrote the field. All three print the same character.

One run had 40 unreadable rows, and I compared its score against models that
parsed everything. Those rows held 15 gold facts, while 26 correctly contained
none. Perfectly repairing all 40 could add at most **0.0038**, inside that
comparison's **±0.013** range. The floor was real and could not carry the claimed
gap.

The same problem is larger at 12B. Two runs parsed **0.90 and 0.92** of their
rows with no context exhaustion. Between 83 and 98 malformed answers became
failures against neighbouring models that parsed every row, so those scores stay
lower bounds until the prompts are matched to their formats.

The third kind of zero was not a run at all. A separate cost benchmark reported
`cached_input_tokens: 0` in every committed cell, and I read that as the layer
defeating prompt caching. Caching worked, and the client never recorded the
field.

A source audit found the mechanism. The gateway rebuilt its usage block from five
scalar fields and dropped the nested cached-token count, and three hand-parsing
sites read only the flat counters. The path facing a different provider carried
the field across, which is why the defect was not universal. The fix merged as
aimee PR 2569 on 2026-08-11.

The tell was in the shape of the number. A cache that genuinely fails still hits
sometimes. A field that is never serialised is always precisely nothing.

## Print the fields that can falsify the score

- **Print parse and schema rates.** They separate an incapable model from a
  parser disagreement.
- **Check the raw output when parse rate falls while completion length holds.** A
  valid answer in the wrong envelope reads as a failed one.
- **Print prompt and completion tokens against context size.** A completion-only
  truncation flag cannot catch context exhaustion.
- **Print the unfloored score beside the floored one.** A precision gate can turn
  a working extraction into zero.
- **Print draft counts beside throughput.** A speed number does not identify the
  mechanism that produced it.
- **Read every guard input.** A recorded model name has no value if nothing
  compares it with the loaded file.
- **Report adjacent and endpoint comparisons together.** Adjacent nulls can hide
  a cumulative difference that neither rung shows.
- **Read a zero as three possibilities before treating it as a result.** A
  measured zero, a floored score and an unwritten field print the same character.
- **Never let a measured constant enter source without its sample, interval and
  provenance.**

The other measurement failures in this campaign are reported where their evidence
lives. Startup time inside throughput, orphaned clients, rented-fleet accounting
and timeout diagnoses are in `the-parallelism-limit-was-never-vram`. Sequence
position, process count and self-reproduction are in `repeatable-is-not-identical`.

The suppressed reasoning pass and the withdrawn +0.084 constant are in
`one-sentence-turned-the-reasoning-off`. The factless strata and the scorer's null
categories are in `the-corpus-is-the-experiment`.

One result in this set is unexplained here. Gemma-4 E4B skips reasoning on 16% of
rows, and the usual causes are absent. That thread continues in
`the-model-decides-when-to-think`, which is recorded as an investigation rather
than an article because the result that would have led it reversed sign on its
only replication.
