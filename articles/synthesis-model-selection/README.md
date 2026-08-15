# Synthesis Model Selection

This article reports a matched accuracy-and-speed comparison of nine local
synthesis configurations.

## Status

The earlier unpublished draft narrowed the result to E2B and 12B because only
those runs were stored in this article folder. The project needs model accuracy
and speed on the measured GPU configuration, and relevant candidate evidence
already existed elsewhere in the reporting repository.

All nine configurations completed the same 1,000-case paired run. The committed
analysis validates the case population, load profile, model identity and raw
artifact hashes before calculating 10,000 paired bootstrap replicates. The
article selects Gemma 4 12B as the default and E2B as the latency tier.

The voice gate passes, the raw analysis reproduces, and the fourth roundtable
pass approved the article with no findings. Publication still requires the site
checks and the queued Qwen3.8 UD-Q4 follow-up. That follow-up may update
Qwen3.8's row; it does not invalidate the completed `Q4_K_M` measurement.

## Candidate matrix

Every scored Gemma target uses the UD-QAT artifact at UD-Q4_K_XL, not a plain
QAT fallback. Gemma 4 and both Qwen families use multi-token prediction (MTP)
with one slot. Muse Glimmer runs with draft flash (DFlash) off and its
vendor-supported low reasoning setting. The model cannot disable reasoning, so
that work remains in its measured latency.

| candidate | target quantisation | serving |
|---|---|---|
| Gemma 4 E2B | QAT UD-Q4_K_XL | MTP on |
| Gemma 4 E4B | QAT UD-Q4_K_XL | MTP on |
| Gemma 4 12B | QAT UD-Q4_K_XL | MTP on |
| Gemma 4 26B-A4B | QAT UD-Q4_K_XL | MTP on |
| Gemma 4 31B | QAT UD-Q4_K_XL | MTP on |
| Qwen 3.6 27B | Q4_K_M | MTP on |
| Qwen 3.6 35B-A3B | Q4_K_M | MTP on |
| Qwen 3.8 27B | Q4_K_M | MTP on |
| Muse Glimmer 30B | K-Quant 17 GB | DFlash off; low reasoning |

## Evidence

| path | contents |
|---|---|
| `benchmarks/fixtures/ab-v1/synthesis.jsonl` | 10,000 frozen silver-label cases; canonical matrix uses the first 1,000 cases in SHA-256 case-ID order |
| `benchmarks/ab-v1/gemma4_e2b/` | raw rows, summary, validation and hardware record |
| `benchmarks/ab-v1/gemma4_12b/` | raw rows, summary, validation and hardware record |
| `benchmarks/ab-v1/paired_content_bootstrap.py` | paired content-score interval |
| `benchmarks/ab-v2/run_candidate_matrix.py` | fail-closed matched-matrix controller |
| `benchmarks/ab-v2/analyze_candidate_matrix.py` | complete-population validator and paired analysis |
| `evidence/raw/candidate-matrix-20260814/canonical/` | nine raw runs, summaries, hardware records, controller state and analysis |
| `evidence/reporting-2026-08-14.md` | prior reporting inventory and replacement disposition |
| `evidence/roundtable-2026-08-15.md` | four-pass review findings, fixes and final approval |
| `evidence/figures.md` | figure map and reporting disposition |

Both summaries carry suite manifest SHA-256
`16d2c16add86052ff24be410699ab9452ee1a36252de6dba31ab5391de7ab81c`.
The E2B file has 10,000 rows and cases. The 12B file has 10,013 rows for 10,000
cases; analysis keeps the last row for each `case_id`, preserving failed attempts
and their successful retries.

The E2B response for case `9490bd93bed2a6ceabb59f3f` matched a credential-syntax
scanner after scoring. Its committed row replaces only the response text, records
the original SHA-256 and preserves the pre-redaction metrics.

The old E2B and 12B artifacts remain valid records of their measured serving
configurations. They do not choose the winner of the matched matrix.
