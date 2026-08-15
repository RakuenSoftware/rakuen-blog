---
title: "The Benchmark Exposed Four Production Contract Failures"
date: 2026-08-09
author: Rakuen Software
tags: [benchmarks, production, knowledge-graphs, aimee]
excerpt: "The scorer normalized identities and represented negation more carefully than production. Its ontology was also incomplete, so the audit had to run both ways."
---

*Rakuen builds aimee, the system audited here. Production observations without
banked source snapshots are labelled in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/the-benchmark-audited-production/evidence/figures.md).*

The benchmark ranked models and specified how a knowledge graph should behave.
Production disagreed with it on identity, migration, negation and relation names.
Production was wrong in the first three cases. The benchmark and production were
both wrong in the fourth.

## The scorer normalized names that production split apart

Production lowercased entity names and collapsed whitespace. It still treated
`Sunshine`, `Sunshine team` and `sunshine_team` as three canonical identities, so
a fact stored under one could be invisible to a query for another.

The scorer already folded separators, articles, honorifics and edge punctuation.
The corpus was cloned from production data, so those variations came from the
system's note stream rather than a grading convenience. Extraction could receive
credit for a fact that production filed under an unreachable name.

The fix moved conservative folds into production. Words such as `van`, `gateway`,
`router`, `server`, `box` and `project` remain because they can be part of a real
product name. A missed fold can later be joined with an alias; a false fold erases
the distinction. The operating rule is to under-fold when evidence is ambiguous.

This finding comes from a static source audit and production observation. The
source snapshot is not committed here, so it remains single-sourced to the
reporting ledger.

## The identity migration left edges unreachable

The registry migration merged aliases but did not rewrite edge endpoints stored
as text. Recall paths then compared those endpoints literally. A fact could remain
in the table under the discarded display name and become invisible to every
query.

A substitute-database test passed because it seeded a legacy alias without a
legacy edge. A PostgreSQL integration test that created both failed on its first
run. The migration was intended to prevent memory loss and produced it instead.

Substitute-engine tests now check syntax for migrations. Behavior involving
constraints, types or stored identity runs against the production engine.

## The model extracted negation that the pipeline discarded

Production already had a tested retraction operation with bitemporal supersession,
immutable-edge protection and an authority guard. The language-model path never
called it. A pattern extractor handled a narrow first-person form; third-party
statements such as a company no longer being a customer were discarded.

The prompt now requests the original fact plus a polarity flag. Keeping the object
allows retraction of one `(source, relation, target)` edge instead of every target
for that source and relation.

On the 132-note retraction slice of corpus version 5:

| model | retractions flagged | usable by production | polarity errors on 869 ordinary notes |
|---|---:|---:|---:|
| E4B | 115 of 132 | 92 | 0 |
| E2B | 85 of 132 | 85 | 1 |

Across the two runs, one of 1,738 ordinary notes received an incorrect polarity
flag. Relocation notes emitted both halves correctly paired 85% of the time.
These are first-party measurements on two models and one corpus, not a general
safety rate. They require expansion before an automatic deletion policy.

## The gold set used relations missing from its ontology

The seed ontology defined 17 relations. The gold set used 12 undefined predicates
for **167 of 880 triples**, or 19%. `owns_account` and `subscription_tier`
appeared 39 times each, `customer_of` 26 times and `purchased` 17 times.

The benchmark asked models to invent names and then penalized them for differing
from its inventions. Production still wrote novel edges, so the immediate failure
was fragmentation rather than data loss.

| meaning | facts | relation names |
|---|---:|---|
| hosting and deployment | 112 | `runs_on` 45, `has_hostname` 46, `operates` 16, `hosts` 5 |
| ownership | 89 | `owns` 59, `acquired` 30 |
| membership | 396 | `works_for` 205, `member_of` 167, `contributes_to` 24 |

An automatic rule promoted a novel relation after three uses. Twenty-three of 89
novel names qualified, putting the ontology on course for about 40 overlapping
entries. Seven relations and 15 aliases were added conservatively. Generic or
distinct verbs such as `owns`, `operates`, `runs` and `contributes_to` were not
folded merely to reduce the count.

The complete test ran on 2026-08-12 over 1,001 notes, both halves on one card,
differing only in whether the prompt listed 17 relations or 24. The
novel-predicate rate fell from **21.0% to 13.0%**, and an interrupted 223-note
run that reported 23.5% to 10.0% is superseded by it.

That fall divides, and the division is the useful part. Rescoring the same
predictions against the larger ontology accounts for 5.68 of the 8.02 points.
The model reaching for a listed name rather than inventing a synonym accounts
for 2.34. Seven tenths of the gain was definitional, available by editing the
ontology and rescoring, with no rerun.

Two relations stopped being invented outright: `runs_on` fell from 24 uses to
zero and `mentors` from 9 to zero. What remains is mostly the generic verbs that
were deliberately not folded.

## Audit the benchmark and production in both directions

Diff every scorer normalization against the production path. Test absence,
retractions and deletions rather than only facts that should exist. Run identity
migrations against the real database engine. Compare the gold predicates with
the ontology before using them to rank models.

The identity, migration and unreachable-negation findings are structural: the
relevant production paths could not perform the requested behavior. The polarity
rate and ontology improvement are statistical claims from small or incomplete
samples. They remain validation tasks, not production guarantees.
