# Figure provenance and reporting record

Paths below are relative to the shared series evidence base at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## The nine failures

| failure | evidence | disposition |
|---|---|---|
| startup inside throughput | `results/mtp-scaling-5080/`, `results/mtp-scaling-xtx/`, and `MEASUREMENT_LOG.md` | kept; startup seconds are single-sourced because the sweep discarded that column |
| fifteen leaked processes | `MEASUREMENT_LOG.md`, process-cleanup defect | kept as an observed host state; no process snapshot was preserved |
| shared significance threshold | `harness/harness/bootstrap_ci.py`; interval sweep in `ARTICLE_NOTES.md` | corrected; every comparison now carries its own interval |
| subset treated as a run | `results/cache-isolation/`; `MEASUREMENT_LOG.md`, defect 40 | corrected to sequence position, after predecessor and prompt-cache explanations were refuted |
| +0.084 constant | `results/v5-large/E4B.v4-same955.score.json`; `results/v5-large/E4B.v5-955.score.json` | withdrawn as a general constant |
| F1 called blind | `harness/harness/score.py`; `MEASUREMENT_LOG.md`, defect 24 | corrected; scorer behaviour was read from source |
| provider reported no instances | `MEASUREMENT_LOG.md`, fleet audit | kept as a single-sourced API observation; billing was checked separately |
| four timeout diagnoses | `MEASUREMENT_LOG.md`, placement defect records | kept with download, model-load and host-state signals separated |
| mechanism inferred from throughput | `results/vast/Qwen3.6-35B-A3B.UD-Q4_K_XL.live.pred.jsonl`; matching 27B file | corrected; both files have no draft counters and `/props` reported speculation off |

The current repository check is dated 2026-08-09 and links the primary ggml-org
Qwen3.6 27B and 35B-A3B Hugging Face repositories inline. Both repository pages
currently list multi-token-prediction sidecars. Repository contents establish
availability only; the banked prediction files establish the measured run state.

## Directly reproducible tables

- **Startup curves:** prediction files and run logs live under
  `results/mtp-scaling-5080/` and `results/mtp-scaling-xtx/`. The exact startup
  seconds survive only in `MEASUREMENT_LOG.md`.
- **Subset comparison:** native and 3,002-note files are under
  `results/qat-vs-ud/`, `results/qat-mid-3k/` and `results/cache-isolation/`.
  The cache-off and shuffled controls are committed beside them.
- **Qwen throughput:** the 35B and 27B prediction files under `results/vast/`
  contain per-note throughput and the absence of `draft_n`.

## Reporting inventory and disposition

All nine first-party investigations remain in the article. Two causal stories
were removed or corrected: prompt-cache history did not explain subset churn, and
speculative decoding did not explain Qwen throughput. Runtime tests, static source
audits, provider API observations and billing observations remain labelled as
different kinds of evidence.

There were no interviews. Provider behaviour is described from the captured
reporting ledger because the raw API responses were not retained.
