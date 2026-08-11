---
title: "The Corpus Determined What the Benchmark Could Find"
date: 2026-08-09
author: Rakuen Software
tags: [benchmarks, datasets, evaluation, aimee]
excerpt: "Factless strata, missing ontology relations, a mislabeled template and unrecoverable generator inputs shaped the model results before inference began."
---

*Rakuen builds aimee, the system measured here. Corpus artifacts and reporting
dispositions are listed in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/the-corpus-is-the-experiment/evidence/figures.md).*

Three of the five most consequential benchmark defects came from corpus assembly,
not model inference. The corpus assigned one-third of the score to restraint,
used relations missing from its ontology, and mislabeled one template in a way
that rewarded the wrong reading.

The generator inputs were also lost. Every result therefore depends on one
versioned corpus artifact that cannot be rebuilt from its recorded source.

## One-third of the corpus measured restraint

The 10,000-note corpus contained three categories with no facts by construction.

| category | notes |
|---|---:|
| transient | 1,391 |
| negation | 1,318 |
| ambiguous | 506 |
| factless total | **3,215, or 32.1%** |

For those notes, the correct output was silence. Removing false positives on them
added **0.040 to 0.053** on the harmonic mean of precision and recall (F1) across
six runs. That was larger than the individual model, quantization and decoding
effects measured in this campaign.

I first described the rows as a metric blind spot. That was wrong. The scorer
already returned `null` for category-level scores with no positive gold facts;
my analysis displayed those values as 0.0. The rows still affected overall F1
through their false positives.

The corrected conclusion is narrower: corpus composition determines how much of
an aggregate score rewards each behavior. Report restraint separately when it
occupies a third of the test.

## Nested tiers did not produce interchangeable runs

The corpus had tiers of 1,001, 3,002 and 10,000 notes, each nested inside the
next. The same 1,001 notes scored 0.6406 when run alone and 0.6327 inside the
3,002-note execution. Only 529 of 1,001 completions were byte-identical.

The preceding note did not explain the churn: failures were 44.8% with the same
predecessor and 48.3% with a different one. Disabling the prompt cache also
failed, reducing identity from 52.8% to 49.9%. With the cache disabled, a seeded
shuffle produced 52.3% identity.

Sequence position is the supported variable. The experiment does not establish
which server state carries it. The score change remained inside its paired range,
so no ranking moved. Shared notes now retain the same positions across tiers.

## The ontology omitted 19% of its own gold facts

The seed ontology defined 17 relations. The gold set used 12 undefined predicates
for **167 of 880 triples**. `owns_account` and `subscription_tier` appeared 39
times each, `customer_of` 26 times and `purchased` 17 times.

Models had to invent predicate names and were then graded against the gold set's
inventions. Across two 1,000-note runs, 22% to 24% of extracted facts used
non-seed predicates. They spanned 89 names, including 54 singletons.

An expanded ontology reduced the novel-predicate rate from 23.5% to 10.0% in an
interrupted 223-note run. That figure is provisional, survives only in the
article notes and does not establish the completed post-change rate.

## One template rewarded the wrong relation

The gold set contained 51 `has_hostname` triples. Twenty-eight came from a
template that said “X runs on Y.”

| note wording | notes | model answered `has_hostname` | model answered `runs_on` |
|---|---:|---:|---:|
| “X has hostname Y” | 23 | 23 | 0 |
| “X runs on Y” | 28 | 0 | 23 |

Both inspected runs produced the same pattern. “Runs on” describes deployment,
not a host's name:

```text
service --runs_on--> host --has_hostname--> hostname
```

The template created 28 false negatives and 23 false positives per run. A model
that returned `has_hostname` would have scored better while reading the sentence
less accurately. I found the defect through a bimodal score distribution inside
one relation. The remaining templates have not received the same audit.

## Deterministic generation was not reproducible

The generator was seeded, but its inventory and synthesis input files were never
committed. None of four surviving inventories reproduced any of the 1,001 notes
at the recorded seed.

Corpus version 5 was instead derived from version 4 by changing 368 relation
labels with no note-text or identifier changes. That stability allowed old
predictions to be rescored against the new gold. It did not restore the missing
generator inputs.

The original corpus cannot be reconstructed. It must remain a versioned artifact,
or a replacement corpus must sacrifice comparability with the banked runs.

## Preserve the experiment before ranking models

Commit generator code, inputs, seed and rendered corpus before the first run.
Verify that the ontology covers the gold set. Report every designed stratum and
inspect bimodal behavior within relations. Keep shared notes at identical
sequence positions across tiers.

Every conclusion in this series still comes from one pipeline and one generator
model. A second corpus built independently is the required external test. Until
it exists, a stable model or quantization effect can still be a stable artifact of
this corpus lineage.
