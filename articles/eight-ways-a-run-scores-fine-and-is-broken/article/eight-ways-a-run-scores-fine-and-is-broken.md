---
title: "Eight Ways a Benchmark Run Can Look Fine and Be Broken"
date: 2026-08-09
author: Rakuen Software
tags: [benchmarks, local-models, evaluation, aimee]
excerpt: "A plausible score can hide a broken parser, an exhausted context, a missing reasoning pass or a gate that discarded the answer. Six columns expose all eight failures."
---

*Rakuen builds aimee, the system measured here. Reporting and run versions are
recorded in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/eight-ways-a-run-scores-fine-and-is-broken/evidence/figures.md).*

Eight benchmark failures gave me plausible numbers. One changed a model ranking.
The harmonic mean of precision and recall (F1) was not the problem. Reporting F1
without the diagnostic columns beside it was.

Those columns already existed. I was not missing measurements. I was discarding
the measurements that could tell a bad model from a bad run.

## F1 priced restraint correctly; my analysis erased it

Three factless note categories appeared to score 0.0000 in every run. I published
that as a structural hole: correct silence could not earn points.

The scorer already emitted `null` for those categories, with a comment explaining
why. My analysis script changed `null` back to 0.0. The notes also affected the
overall score: removing false positives from them added **0.040 to 0.053 F1**
across six runs.

The metric was doing its job. My display was not.

## Four failures made capability look like zero

The output used the wrong envelope. One model returned a valid extraction
inside a tool-call wrapper. Completion length stayed normal while parse rate
collapsed. The model understood the note; the parser could not see its answer.

The raw wrapper output was not retained, so this diagnosis is single-sourced in
the reporting ledger.

The context ended before the completion limit. My truncation guard compared
completion tokens with `max_tokens`. A request that exhausted the total context
never reached that completion limit, so the guard could not fire. Prompt tokens
plus completion tokens must be compared with context size.

The reasoning pass disappeared. The sentence `No prose, no markdown.`
suppressed reasoning across 10,000 notes while every row still recorded
`thinking: true`. A boolean configuration flag described what I requested, not
what the model did. The run needed a reasoning-row count.

A score floor was compared with a capability score. One run had 40 unreadable
rows. They contained 15 gold facts, while 26 correctly contained none. Perfectly
repairing all 40 could add at most **0.0038**, inside that comparison's
**±0.013** range.

The floor mattered, but it could not carry the claimed gap.

The same problem is larger at 12B. Two runs parsed only **0.90 and 0.92** of their
rows, with no context exhaustion. Between 83 and 98 malformed answers became
failures against neighbouring models that parsed every row. I have not measured
the correction, so those scores remain lower bounds.

## A tie hid opposite production risks

Two large models were indistinguishable on F1 and different everywhere a
production choice hurts. Both used weights produced with quantization-aware
training (QAT):

| model | F1 | recall | silent on factless notes | invented triples |
|---|---:|---:|---:|---:|
| gemma-4-31B QAT | 0.6872 | **0.8000** | **0.463** | **180** |
| gemma-4-12B QAT | 0.6854 | 0.7330 | 0.702 | 97 |

The paired difference was **−0.0017**, with a 95% range from **−0.0202 to
+0.0162**. The 31B model found more facts and invented nearly twice as many on
the 322 notes whose correct answer was silence. F1 netted recall against
restraint and called the trade a tie.

That is useful for a leaderboard and insufficient for a system that writes facts
without review. `granite-4.1-3b` makes the alternative concrete: it gives up 0.14
F1, stays silent on 93% of factless notes and invents 24 triples rather than 180.

## A confidence gate inverted the ranking

`Qwen3-0.6B` scored 0.000 with the confidence floor and 0.403 without it.
`granite-4.0-350m` moved from 0.000 to 0.206. Both extracted facts and assigned
them confidence 0.0; the gate discarded every one.

Self-reported confidence carried almost no signal across the sixteen models.
Most wrote 0.0 or 0.9 and nothing between. I replaced the floor with a check that
both endpoints appear in the note.

The gate also reversed a size comparison. Floored, a 1B Granite model beat a 3B
one, 0.600 to 0.571. Unfloored, the 3B won, 0.648 to 0.592. That table measured
the gate, not model size.

Two other zeroes had the opposite cause. `SmolLM2-360M` and `gemma-3-270m`
parsed every answer but never used the required `{"facts": [...]}` schema.
`Qwen3-0.6B` parsed and matched the schema, then lost its facts at the floor.
Parse rate and schema rate separate those diagnoses.

## A valid model failed the identity guard

My model guard derived an expected family name from a repository name. Google's
file `gemma-4-E2B_q4_0-it.gguf` did not contain the generated stem, so the guard
blocked a model that had loaded correctly. The refusal survives only as a
single-sourced host observation in the reporting ledger.

The replacement keeps the guard and permits an explicit, documented identity
override. A guard around a naming convention you do not control needs a path for
the valid exception.

## Six columns catch all eight failures

- **Print parse and schema rates.** They separate an incapable model from a
  parser disagreement.
- **Print prompt and completion tokens against context size.** A completion-only
  truncation flag cannot catch context exhaustion.
- **Print the share of rows that reasoned.** A requested mode is not an observed
  mode.
- **Print abstention with precision and recall.** A single score can net two
  production risks into a tie.
- **Print the unfloored score beside the floored one.** A precision gate can turn
  a working extraction into zero.
- **Read every guard input.** A recorded model name has no value if nothing
  compares it with the loaded file.

One result remains unexplained. Gemma-4 E4B skips reasoning on 16% of rows, and
the usual causes are absent. That is where the report stops.
