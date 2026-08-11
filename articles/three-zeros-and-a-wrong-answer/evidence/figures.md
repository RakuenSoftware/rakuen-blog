# Figure provenance and reporting record

This article is a first-party post-mortem of our own system. Most of it is an
account of what we did and what we found in our own code, and that kind of
reporting does not need an external artifact to stand up. One part of it is a
benchmark measurement, and that part does.

`articles/AGENTS.md` requires runtime tests, source audits and observations to be
kept as distinct classes of evidence rather than collapsed into one. They are
separated here.

## First-person account: the three retracted readings

The article's spine is a record of the author's own reasoning: what was read,
what was concluded, and what turned out to be true. No artifact makes "I
concluded this and I was wrong" more or less true, and the article is the record.

The corrected values are a different matter and are listed below with their
sources. The retractions themselves are kept in the article rather than
summarised, because the sequence is the subject.

## First-party instrumentation: the cache rates

| figure | source |
|---|---|
| 0.0% across 1,545,665 prompt tokens before the recording path shipped | our own `token_audit` ledger |
| 46.6% overall after it shipped | the same |
| 80% to 96% on warm mid-session turns | the same |
| 80.5% in production over the same window | the same |
| 14.9%, withdrawn | the same, over a window that straddled the deploy |

The query is
`SELECT source, SUM(prompt_tokens), SUM(cache_read_tokens) FROM token_audit GROUP BY source`,
bucketed by `created_at` against deploy times. The bucketing is not optional: the
withdrawn 14.9% is what the same query returns without it.

These are single-sourced to our own instrumentation, which is the point of the
article rather than a weakness in it. The database was not found on this machine
at the path the reporting record names, so the numbers cannot currently be
re-derived here.

## Source audit: the serialisation defect

| figure | source |
|---|---|
| the gateway rebuilt the usage block from five scalars and dropped the nested cached-token field | `aimee`, `src/openai_shape.c` |
| three hand-parsing sites read only the flat counters | `aimee`, `src/agent_runtime.c` |
| the Anthropic-facing path carried the field across | the Anthropic path in the same tree |
| fixed | `aimee` PR 2569, merged 2026-08-11 |

A static source audit plus a merged change. The article names the fix and its
date in the text, which is what this class of claim needs.

## Benchmark measurement: the cost table

This is the one part that needs committed artifacts, and it is the part that does
not yet have them here.

Searched on 2026-08-11 for the `t01_cache` cells behind the table. The columns do
exist in the schema: `summary.json` carries `codex.usage.input_tokens`,
`codex.usage.cached_input_tokens` and `codex.estimated_credits`. What could not be
found is a set of cells that reproduces the published table.

| location | what is there |
|---|---|
| `ponytail-codex-benchmark/battery/codex_results/cells/` | `t01_cache` at `r1` only, for baseline, ponytail-addon and ponytail-instructions. No aimee cell |
| `battery/codex_archive/aimee-kb-8bc6aa5-superseded/cells/` | one aimee `t01_cache` cell, in a directory named superseded |
| `/tmp/ptcodex/cells/` | aimee and aimee-review `t01_cache` working directories with no `summary.json`, so fixtures rather than results |
| `battery/matrix_results/cells/` | `t01_cache` at three replicates, but a different schema with no `codex` block and no aimee run |

What the located cells report, against what the article publishes:

| run | located `r1` input / hit / credits | article's published range |
|---|---|---|
| baseline | 127,833 / 83% / 5.51 | 84k to 98k / 66% to 88% / 4.3 to 6.6 |
| ponytail add-on | 94,948 / 54% / 7.51 | 107k to 143k / 63% to 85% / 5.3 to 7.4 |
| aimee, superseded cell | 148,189 / 84% / 6.46 | 464k to 648k / 89% to 91% / 13.8 to 19.2 |

These do not match, and the round-trip column was not compared because
`turn.completed` reads 1 in every located cell and is plainly not the measure the
article uses.

**This does not establish that the table is wrong.** It establishes that the
artifacts behind it are not among the ones on this machine, and that the located
cells belong to a different campaign. The author ran the measurement and knows
which tree it came from. Until that tree is named, the table is the one claim in
the article without a source anyone else could check.

The article also states three replicates per run. Every located `t01_cache` cell
outside `matrix_results` is `r1` only.

## Counts from the corpus

| figure | source |
|---|---|
| `roundtable_review` called 52 times across the corpus | not yet cited to a counting source |
| `delegate` called zero times | not yet cited to a counting source |
| about 2.3× heavier per call, from nineteen tool schemas and a context envelope | not yet cited |
| about 2.5× more round trips | derivable from the cells once the right tree is named |

The `delegate` zero carries weight in the argument and the article marks it in
the text as a measured zero. That marking needs the counting source behind it,
by the article's own standard.

## Reporting inventory and disposition

- **Three retracted readings:** kept in full. The sequence is the subject and
  must not be compressed.
- **The 6× and the 14.9%:** withdrawn in the article rather than removed.
- **Warm-turn cache figure:** the 46.6% overall rate is published beside the 80%
  to 96% warm-turn figure, because the warm figure alone overstates the recovery.
- **The serialisation defect:** kept as a source audit plus a merged fix, and
  labelled as such rather than as a runtime measurement.
- **The cost table:** kept, and it carries the article's central claim. It is the
  only figure here that a reader could not check, and the only one that blocks
  publication.
- **Adjacent interest:** disclosed in the article, next to the claim, and the
  system that comes off worst is ours.

## What has to happen before this can be published

1. Name the results tree the cost table was computed from, and copy those cells
   into this article's `benchmarks/`.
2. Confirm whether the table spans three replicates or one, and correct the
   article if it is one.
3. Name the counting source for the 52 `roundtable_review` calls and the
   `delegate` zero.
4. Export the `token_audit` rows behind the cache figures, with their deploy
   boundary, into `evidence/raw/`.
5. Decide whether the `ponytail add-on` run is a third party's product. If it is,
   the article makes an adverse comparative claim and right of reply applies.
