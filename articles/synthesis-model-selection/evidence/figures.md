# Figure provenance and reporting record

Paths below are relative to `articles/synthesis-model-selection/`.

## Paired quality measurements

| figure | artifact |
|---|---|
| 10,000 paired cases and shared manifest | `benchmarks/fixtures/ab-v1/synthesis.jsonl`; both `summary_*.json` files |
| overall content F1, parse, schema and field recall | `benchmarks/ab-v1/gemma4_e2b/summary_gemma4_e2b.json`; `benchmarks/ab-v1/gemma4_12b/summary_gemma4_12b.json` |
| task-level scores and row counts | the same summary files |
| +0.0712 paired difference, range +0.0672 to +0.0750 | both raw prediction files; `benchmarks/ab-v1/paired_content_bootstrap.py`, 5,000 replicates with seed 20260809 |
| latest-row counts, artifact hashes and secret scans | both `validation_synthesis.json` files |

Content F1 averages each case's required-field scores. String fields use token
overlap, list fields use exact set overlap and scalar fields use equality. The
paired interval resamples the same case identifiers in both runs. The scoring
method is pinned to aimee commit `5e1b962491f7fe08a5cf34a9f524aaa4b1157d37`
and linked inline in the article.

## Serving measurements

| figure | artifact |
|---|---|
| median and tail latency, decode rate and token totals | both summary files and raw rows |
| cold-load time, slots, workers, context and memory | both `hardware_synthesis.json` files |
| E2B truncation count 21; 12B count 0 | both summary and validation files |

The configurations deliberately use different slot counts and aggregate contexts.
Latency is therefore reported as a serving-configuration measurement, not a pure
model-size effect.

## Reporting inventory and disposition

- **E2B 10,000-case run:** kept. Its raw, summary, validation and hardware files
  remain committed.
- **12B 10,013-row run:** kept. Analysis uses the latest row for each of 10,000
  case identifiers; the 13 superseded attempts remain in the raw file.
- **Generated-response redaction:** kept. The E2B row records the redaction flag
  and original response hash while preserving the pre-redaction metrics.
- **Wider model ladder:** excluded. No complete wider campaign is committed in
  this folder, so it contributes no ranking or recommendation.
- **CPU selection:** left open. Both committed runs record graphics-device
  serving and cannot establish CPU affordability.
- **Absolute quality:** not claimed. The fixture identifies its labels as silver,
  not human-audited gold.

There are no interviews or external benchmark results. No material criticism of
an outside party carries the conclusion.
