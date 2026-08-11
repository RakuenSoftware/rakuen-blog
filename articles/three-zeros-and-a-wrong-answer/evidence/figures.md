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

**Source tree located on 2026-08-11:**
`ponytail-reanalysis/.claude/worktrees/aimee-review-arm/ct403-results/cells/`,
81 cells across eight run labels. Three earlier candidate trees were checked and
rejected: `codex_results` has no aimee run, `matrix_results` has no `codex` usage
block, and the `/tmp/ptcodex` copies are fixtures with no `summary.json`.

The columns come from `summary.json`: `codex.usage.input_tokens`,
`codex.usage.cached_input_tokens` and `codex.estimated_credits`.

### Reproduces exactly

| figure | recomputed from the cells |
|---|---|
| baseline 84k to 98k, 66% to 88%, 4.3 to 6.6 credits | 84,546 / 98,310, 66% to 88%, 4.33 / 6.56. Three replicates |
| aimee plugin 464k to 648k input, 13.8 to 19.2 credits | 464,169 / 647,820, 13.84 / 19.15. Three replicates |
| baseline and add-on round trips, 4 to 5 | `codex.item_types.agent_message`, 4 to 5 in both |

### Does not reproduce

| published | what the cells give |
|---|---|
| ponytail add-on credits 5.3 to 7.4 | 5.95, 6.83, 7.40. The lower bound 5.3 is not an add-on cell. `ponytail-instructions__r2` is 5.31 |
| aimee plugin cache hit 89% to 91% | 90%, 91%, 91%. 89% appears in `aimee-lean__r3` and `aimee-review__r1`, which are different run labels |
| aimee plugin round trips 13 to 22 | `agent_message` gives 6 to 8. No metric tested reproduces 13 to 22: `item.started` 12 to 14, `item.completed` 21 to 22, `tool_calls` 24 to 28 |
| aimee gateway 136k to 231k, 25% to 70%, 7.9 to 21.5 | the four gateway cells give 63k to 77k input, **0%** cache, 10.29 to 12.01 credits |

The round-trip column is the sharpest of these. `agent_message` reproduces
baseline and add-on to the digit, which is strong evidence it is the intended
metric, and under that same metric the plugin is 6 to 8 rather than 13 to 22.
That changes the multiplier the article derives.

### The gateway row cannot come from client-reported usage

All four `aimee-gateway` cells record `cached_input_tokens: 0`. They were written
between 05:43 and 06:49 on 2026-08-11, before the recording fix deployed at
17:58. No cell anywhere on this machine was written after that deploy.

So the published gateway cache range of 25% to 70% cannot have come from these
cells, because these cells report the unrecorded zero that the article is about.
It most likely came from the `token_audit` ledger after the fix, which is a
server-side measurement.

If so, the table mixes two measurement bases: three rows from client-reported
usage and one row from our own ledger. That is a methodological point the article
does not currently make, and it bears directly on the row carrying the natural
experiment.

This also confirms the article's own mechanism. `baseline` and `aimee` cells
record real cache rates because those runs report from OpenAI directly. Only the
gateway run, the one where our code sits in the reporting path, reads zero.

## Counts from the corpus

Recomputed on 2026-08-11 by summing `codex.tool_calls` across all 81 cells in
`ct403-results`.

| figure | recomputed |
|---|---|
| `roundtable_review` called 52 times across the corpus | **52.** Reproduces exactly |
| `delegate` called zero times | **absent from every cell.** No `delegate` key appears in any `tool_calls` map |

The full tool-call census is `preview_blast_radius` 68, `index` 56,
`roundtable_review` 52, `find_symbol` 18, `find_tools` 2.

The `delegate` zero is a measured zero, and this is the artifact that shows it.
`tool_calls` records every tool actually invoked, so a tool that never appears was
never called. The article marks that zero as measured in the text, and the
marking now has a source behind it.

| figure | source |
|---|---|
| about 2.3× heavier per call, from nineteen tool schemas and a context envelope | not yet cited |
| about 2.5× more round trips | see the round-trip discrepancy above. Under `agent_message`, the metric that reproduces baseline and add-on exactly, the plugin ratio is nearer 1.5× than 2.5× |

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

1. Copy the 81 `ct403-results` cells into this article's `benchmarks/`. They are
   currently inside a `.claude/worktrees/` directory, which is not a durable home
   for the only copy of the evidence.
2. Resolve the round-trip column. `agent_message` reproduces baseline and add-on
   exactly and gives the plugin 6 to 8, not 13 to 22. Either name the metric that
   gives 13 to 22 or correct the figure and the multiplier derived from it.
3. Say where the gateway row came from. If it is `token_audit` rather than
   client-reported usage, the table mixes measurement bases and should say so.
4. Check the add-on credit lower bound of 5.3 and the plugin cache lower bound of
   89%. Neither appears in its own run's cells, and both appear in a neighbouring
   run label.
5. Export the `token_audit` rows behind the cache figures, with their deploy
   boundary, into `evidence/raw/`.
6. Cite the 2.3× per-call figure.
7. Decide whether the `ponytail add-on` run is a third party's product. If it is,
   the article makes an adverse comparative claim and right of reply applies.

Items 2, 3 and 4 change what the article says. The rest are filing.
