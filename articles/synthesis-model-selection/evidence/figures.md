# Figure provenance and reporting record

Paths below are relative to `articles/synthesis-model-selection/`.

## Completed nine-configuration matrix

The canonical result root is
`evidence/raw/candidate-matrix-20260814/canonical/`. Each named directory holds
1,000 latest successful rows, its generated summary, the model and load record,
and the unedited runner and server logs. `RUN_STATE.json` records a completed
nine-configuration controller run.

The independent result is `canonical/analysis-20260815.json`, SHA-256
`c825f90f1a4a8d5e6ef4d9e9de2a9cba43c17527025d9fd7a2c71201b615c095`.
`benchmarks/ab-v2/analyze_candidate_matrix.py` produced it with 10,000 paired
case resamples, seed 20260815 and NumPy 2.5.0. Before analysis, the script
requires identical case populations and suite hashes, 1,000 successful latest
rows per configuration, a completed controller state, the pinned load profile,
the expected loaded model and the expected MTP state. It records SHA-256 hashes
for every raw, summary and hardware file.

### Observed synthesis ladder

| article figure or claim | artifact and field |
|---|---|
| nine content scores and observed order | `analysis-20260815.json`, `models[].content_f1` and `content_rank` |
| median and 95th-percentile latency | `models[].latency_s.p50` and `.p95` |
| required-field recall | `models[].required_field_recall` |
| post-run GPU memory | `models[].vram_after_run_bytes`, converted from bytes to gibibytes |
| 12B median is 44% lower than 31B; post-run allocation is 59% lower | ratios calculated from the unrounded fields above |
| E2B median is 0.554 seconds against 12B's 1.335 seconds | the same unrounded latency fields |

The figure's chart ranks observed content scores. It does not present those
point estimates as statistical ranks. Its Numbers tab carries the selection
measurements that the chart omits.

### Content, latency and memory frontier

| article figure or claim | artifact and field |
|---|---|
| content score against median request latency | `analysis-20260815.json`, `models[].content_f1` and `latency_s.p50` |
| circle area | `models[].vram_after_run_bytes`, converted from bytes to gibibytes before area scaling |
| measured frontier line | `content_latency_pareto_frontier` |
| logarithmic horizontal positions | base-10 transform of `latency_s.p50`, bounded from 0.5 to 12 seconds |

The line joins the configurations named by the analysis as the observed
content-latency Pareto frontier. It is descriptive, not a confidence interval.
The Numbers tab carries the untransformed median, 95th percentile and memory
measurements.

### Paired decisions

| article comparison | `right_minus_left` orientation in artifact | observed difference | 95% paired range |
|---|---|---:|---:|
| 31B minus 12B | `gemma4_31b_qat_udq4_mtp` minus `gemma4_12b_qat_udq4_mtp` | +0.0053 | -0.0039 to +0.0147 |
| 31B minus Qwen3.6-27B | reverse of stored Qwen3.6 minus 31B | +0.0107 | +0.0007 to +0.0207 |
| 12B minus Qwen3.6-27B | reverse of stored Qwen3.6 minus 12B | +0.0054 | -0.0048 to +0.0155 |
| 12B minus E2B | stored orientation | +0.0299 | +0.0197 to +0.0401 |
| Qwen3.6-27B minus Qwen3.8-27B | reverse of stored Qwen3.8 minus Qwen3.6 | +0.0119 | +0.0022 to +0.0216 |
| 26B-A4B minus E2B | stored orientation | +0.0017 | -0.0094 to +0.0127 |
| Qwen3.6-35B-A3B minus E2B | stored orientation | +0.0008 | -0.0100 to +0.0114 |
| E2B minus E4B | reverse of stored E4B minus E2B | +0.0070 | -0.0027 to +0.0166 |
| E2B minus Muse | reverse of stored Muse minus E2B | +0.0381 | +0.0253 to +0.0510 |

Differences and endpoints in the article are rounded from the unrounded JSON
fields. A range containing zero is described as not statistically separated.
No equivalence margin or equivalence test was used.

### Task-level point estimates

| article figure or claim | artifact and field |
|---|---|
| five task charts and their 45 displayed scores | `analysis-20260815.json`, `models[].by_task.<task>.content_f1` |
| nine configurations in each Chart and Numbers view | all nine `models[]` rows, ordered by descending observed score within that task |
| task-specific horizontal scales | zero to 0.25 for claim, zero to 0.15 for entity, and zero to 0.50 for code unit, document summary and synthesis |
| 31B leads claim and code unit; 12B leads document summary; 26B-A4B leads entity; Qwen3.8 leads synthesis | maxima of those five task columns |

The five task charts are descriptive. No task-level paired interval was
calculated, so the article does not turn these observed leaders into five
additional model-selection claims. Each chart and its Numbers tab show all nine
tested configurations. The article tells readers to compare printed values and
within-task order rather than bar length across charts with different scales.

### Qwen3.8 and Muse mechanisms

| claim | artifact and field |
|---|---|
| Qwen3.8 generated 136,535 completion tokens; Qwen3.6-27B generated 122,389 | `models[].completion_tokens` |
| Qwen3.8 decoded 85.49 tokens per second; Qwen3.6-27B decoded 83.75 | `models[].decode_tokens_per_second` |
| Qwen3.8 median latency was 2.218 seconds against 2.073 seconds | `models[].latency_s.p50` |
| Muse parsed and met the schema on 99.9%; required-field recall was 89.46% | `models[].raw_parse_rate`, `.schema_valid_rate` and `.required_field_recall` |
| Muse document-summary content score was 0.2026; next-lowest was Qwen3.6-35B-A3B at 0.4167 | `models[].by_task.doc_summary.content_f1` |
| Muse generated 415,197 completion tokens, 2.94 times E2B's next-highest total of 141,295 | `models[].completion_tokens` and the unrounded ratio |
| Muse median latency was 10.115 seconds | `models[].latency_s.p50` |

### Output volume and required-field completeness

| article figure or claim | artifact and field |
|---|---|
| completion-token bars for all nine configurations | `analysis-20260815.json`, `models[].completion_tokens` |
| decode rate and median request time in Numbers | `models[].decode_tokens_per_second` and `latency_s.p50` |
| required-field recall dots for all nine configurations | `models[].required_field_recall` |
| raw-parse and schema-valid rates in Numbers | `models[].raw_parse_rate` and `schema_valid_rate` |

The completeness chart uses an explicitly labelled 88% to 100% scale. It uses
dots rather than bars so the truncated scale cannot be read as magnitude from
zero. The completion-token chart uses a zero baseline.

The ten-figure presentation replaces no measurement, finding or recommendation.
It draws additional views from the same canonical analysis and retains the same
publication date. This is a presentation completion, not a new benchmark run.

The earlier fact-extraction scores are candidate-selection context, not inputs
to the synthesis result. They trace through
`articles/local-llm-fact-extraction-head-to-head/evidence/figures.md`. The Muse
reasoning claim is a vendor model-card statement, read August 14, 2026, and is
linked inline in the article.

## Earlier unpublished two-run draft

The tables below document inputs used by an earlier unpublished draft. They are
retained as reporting records and do not support the nine-configuration
selection.

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
- **Absolute quality:** not claimed. The fixture identifies its labels as silver,
  not human-audited gold.

There are no interviews or external benchmark results. No material criticism of
an outside party carries the conclusion.
