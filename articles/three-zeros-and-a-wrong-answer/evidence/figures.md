# Figure provenance and reporting record

**This map is incomplete and the article cannot be published against it yet.**
Every first-party figure below is currently sourced to a repository other than
this one. The rule this repository exists to enforce is that a figure traces to
an artifact in the same article folder or to a named external source in the post.
Nothing has been copied in yet, so each row names where the artifact lives today
and what has to move.

## Cost and volume table

The table is one task, `t01_cache`, three replicates per run, four runs.

| figure | artifact, and where it lives today |
|---|---|
| baseline input tokens, cache hit, round trips, credits | `ponytail-codex-benchmark`, `battery/codex_results/cells/baseline__t01_cache__r{1,2,3}/summary.json` |
| ponytail add-on row | the same tree, `ponytail-addon__t01_cache__r{1,2,3}/` |
| aimee plugin row | the same tree, `aimee__t01_cache__r{1,2,3}/` |
| aimee gateway row | not yet located as a distinct cell prefix in that tree |
| round trips | `num_turns` in each cell's `summary.json` |
| input tokens, cache hit and credits | not present in `summary.json`; the field that carries them has not been identified |

`battery/matrix_results/cells/` holds a second corpus with the same task and
replicate naming but only three run prefixes, `baseline`, `ponytail-addon` and
`ponytail-instructions`. Which of the two trees the published table was computed
from is not yet established, and the two must not be mixed.

## The three retracted readings

| figure | artifact, and where it lives today |
|---|---|
| `files_indexed: 0` in benchmark cells, and the comment three lines above it | the benchmark harness source; file and line not yet cited |
| semantic round-trip readiness gate passed in 27 of 27 cells | not yet cited to an artifact |
| `cached_input_tokens: 0` in 8 of 8 cells | not yet cited to an artifact |
| the 6× input-cost penalty, withdrawn | withdrawn. It was computed from the zero, and the zero was not a measurement |
| about 13% recovered by correcting the accounting | not yet cited to an artifact |
| 14.9% cache hit rate, withdrawn as a contaminated average | withdrawn. The window straddled the deploy of the recording path |
| 0.0% across 1.5M prompt tokens before the deploy | `token_audit` in `aimee.db`, bucketed by `created_at` against deploy time |
| 80–96% on warm turns after the deploy | the same table and query |
| production at 80.5%, historical at 96% | the same table and query |

The corroborating query is recorded as
`SELECT source, SUM(prompt_tokens), SUM(cache_read_tokens) FROM token_audit GROUP BY source`,
always bucketed by `created_at` against deploy times. The database is not in this
repository and was not found at the path the reporting record names.

## The serialisation defect

| figure | artifact, and where it lives today |
|---|---|
| the gateway rebuilt the usage block from five scalars and dropped the nested cached-token field | `aimee`, `src/openai_shape.c` |
| three hand-parsing sites read only the flat counters | `aimee`, `src/agent_runtime.c` |
| the Anthropic-facing path carried the field across | `aimee`, the Anthropic path in the same tree |
| fixed | `aimee` PR 2569, merged |

## Process and tool-use figures

| figure | artifact, and where it lives today |
|---|---|
| `roundtable_review` called 52 times across the corpus | not yet cited to an artifact |
| `delegate` called zero times | not yet cited to an artifact. This is a zero, and the article's own argument requires showing it is a measured zero rather than an unrecorded one |
| ~2.3× heavier per call, nineteen tool schemas plus a context envelope | not yet cited to an artifact |
| ~2.5× more round trips | derivable from `num_turns` across the cells above; the derivation is not yet written down |
| our tools batch within a capability but not across them, so following the guidance tripled trips | not yet cited to an artifact |

## Reporting inventory and disposition

- **Three retracted readings:** kept in the article as retractions, with the
  corrected value beside each. This is the article's subject and must not be
  compressed into a summary.
- **The 6× and the 14.9%:** withdrawn, and preserved in the article as withdrawn
  rather than removed.
- **The serialisation defect:** kept. It is a source audit plus a merged fix, not
  a runtime measurement, and is labelled as such.
- **The cost table:** kept, and it carries the article's central claim. It is the
  row most in need of a committed artifact.
- **The `delegate` zero:** kept, and flagged. An article whose thesis is that a
  zero can be an absence of recording has to hold its own zeros to that standard.
- **Third-party comparison:** the baseline is a competitor product's default
  behaviour. No right of reply has been sought, and the article draws a
  comparative cost conclusion about it.

## What has to happen before this can be published

1. Copy the `t01_cache` cells for all four runs into this article's
   `benchmarks/`, and record which of the two result trees they came from.
2. Identify the field carrying input tokens, cache hit rate and credits, since
   `summary.json` does not appear to hold them, and show the table is computed
   from it.
3. Locate the gateway run's cells, or correct the table if that row was derived
   some other way.
4. Export the `token_audit` rows behind 0.0%, 80–96%, 80.5% and 96%, with their
   deploy boundary, into `evidence/raw/`.
5. Cite the `files_indexed` comment and the 27-cell readiness result to files and
   lines.
6. Establish that the `delegate` zero and the 52 `roundtable_review` calls are
   counted from a recorded field.
7. Decide the right-of-reply question on the third-party comparison.
