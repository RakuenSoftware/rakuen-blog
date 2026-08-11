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

**Committed here** at `benchmarks/ct403-results/`, 81 cells across eight run
labels, 841 files. Copied 2026-08-11 from
`ponytail-reanalysis/.claude/worktrees/aimee-review-arm/ct403-results/` and
verified byte-identical file by file. The source sat inside a `.claude/worktrees/`
directory, which is disposable by design, and was the only copy.

Three earlier candidate trees were checked and rejected: `codex_results` has no
aimee run, `matrix_results` has no `codex` usage block, and the `/tmp/ptcodex`
copies are fixtures with no `summary.json`.

The columns come from `summary.json`: `codex.usage.input_tokens`,
`codex.usage.cached_input_tokens` and `codex.estimated_credits`.

### Reproduces exactly

Reproduce them with `benchmarks/recompute_cost_table.py`, which reads the
committed cells and exits non-zero if any published figure fails to reproduce.

| figure | recomputed from the cells |
|---|---|
| baseline 84k to 98k, 66% to 88%, 4.3 to 6.6 credits | 84,546 / 98,310, 66% to 88%, 4.33 / 6.56. Three replicates |
| aimee plugin 464k to 648k input, 13.8 to 19.2 credits | 464,169 / 647,820, 13.84 / 19.15. Three replicates |
| aimee plugin cache hit 89% to 91% | 89.66% to 91.28%. Three replicates |
| baseline and add-on round trips, 4 to 5 | `codex.item_types.agent_message`, 4 to 5 in both |

### Does not reproduce

| published | what the cells give |
|---|---|
| ponytail add-on credits 5.3 to 7.4 | 5.95, 6.83, 7.40. The lower bound 5.3 is not an add-on cell. `ponytail-instructions__r2` is 5.31 |
| aimee plugin round trips 13 to 22 | `agent_message` gives 6 to 8. No metric tested reproduces 13 to 22: `item.started` 12 to 14, `item.completed` 21 to 22, `tool_calls` 24 to 28 |
| aimee gateway 136k to 231k, 25% to 70%, 5 to 11 trips, 7.9 to 21.5 | the one `t01_cache` gateway cell gives 77,163 input, **0%** cache, 1 trip, 11.74 credits |

An earlier version of this map listed the plugin cache floor of 89% as a
discrepancy. That was wrong and is withdrawn. The cells give 89.66% to 91.28%,
and the article floors the lower bound, so 89% to 91% is correct. The error came
from comparing values already rounded for display rather than the underlying
ratios, which is the same mistake in miniature that the article is about.

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

## Retracted by a later measurement, 2026-08-11 22:00

The article's natural experiment is withdrawn. It argued that the gateway run and
the plugin run expose the same tools, that only the plugin installs the persona,
and that the round-trip gap between them therefore isolates the persona as the
cause.

The author re-measured at 22:00 on 2026-08-11, all runs on one image
`sha256:239f6b3e`, `t01_cache`, three replicates, and retracted it:

- **The Codex MCP run receives no aimee persona at all.** Grepping the transcript
  for the manager text returns nothing, and the harness sends a plain prompt. So
  there was never a persona difference between those two runs to attribute
  anything to.
- **The gateway run's lower round-trip count was a gateway tool-routing defect**,
  fixed earlier the same day.

This is the author's measurement and is recorded here as reported. The cells were
run on CT403 and are not on the machine where this map was written, so nothing in
this section has been reproduced here.

It does independently explain the unreconcilable gateway row above. That row was
measured while the tool-routing defect was live, which is why its figures sit
nowhere near the other three runs.

### What the re-measurement puts in its place

| run | credits, three replicates | mean | against baseline |
|---|---|---:|---:|
| baseline | 4.48, 5.24, 5.62 | 5.11 | 1.00× |
| aimee with `roundtable_review` removed | 10.66, 11.38, 11.82 | 11.29 | 2.21× |
| aimee as shipped | 14.13, 15.04, 16.31 | 15.16 | 2.97× |

All nine cells returned `hidden_ok` true, `compile` 0 and `smoke` 0, so
correctness is identical across every run and the extra spend bought nothing
measurable on this task.

Removing `roundtable_review` is 26% cheaper and 15% faster, and the ranges do not
overlap: the worst run without it, 11.82, is below the best run with it, 14.13.

**It did not cut round trips.** One cell still made 28 aimee calls. The saving is
per-call cost, because `roundtable_review` blocks on a delegate and returns a
large result. That is a different mechanism from the one the article publishes.

The author's own caveat: this task's patch is correct either way, so a reviewer
has nothing to catch. It measures what `roundtable_review` costs, not that it is
worthless.

### What survives

The headline. The layer costs about three times baseline, and the re-measurement
puts it at 2.97× on credits with identical correctness.

What does not survive is the mechanism. The article attributes the cost to the
persona generating round trips. The persona was not in that comparison, and
removing the most expensive tool does not change the round-trip count at all.

Restructuring the article around per-call weight rather than round-trip count is
an editorial decision for the author, not a filing correction.

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

One nuance the article should not lose. The 22:00 re-measurement notes that
`roundtable_review` blocks on a delegate internally. That does not contradict the
zero: `tool_calls` records what the agent invoked, and the agent never invoked
`delegate` itself. Both are true, and the article's point stands, that an
instruction to always delegate was shipped into a mode that cannot honour it.

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

1. Resolve the round-trip column. `agent_message` reproduces baseline and add-on
   exactly and gives the plugin 6 to 8, not 13 to 22. Either name the metric that
   gives 13 to 22 or correct the figure and the multiplier derived from it.
2. Say where the gateway row came from. If it is `token_audit` rather than
   client-reported usage, the table mixes measurement bases and should say so.
3. Check the add-on credit lower bound of 5.3. It is not in any add-on cell, and
   `ponytail-instructions__r2` is 5.31.
4. Export the `token_audit` rows behind the cache figures, with their deploy
   boundary, into `evidence/raw/`.
5. Cite the 2.3× per-call figure.
6. Decide whether the `ponytail add-on` run is a third party's product. If it is,
   the article makes an adverse comparative claim and right of reply applies.

Items 1, 2 and 3 change what the article says. The rest are filing.
