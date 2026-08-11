# Figure provenance and reporting record

Paths below are relative to the shared series evidence base at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## Prompt-clause experiment

| figure | artifact |
|---|---|
| four 20-note prompt probes | `MEASUREMENT_LOG.md`, prompt-clause experiment; raw probe output was not retained |
| 10,000-note banked v4 run | `results/v4-large/E4B.UD-Q4_K_XL.pred.jsonl` |
| v4 scored on the matched 955 | `results/v5-large/E4B.v4-same955.score.json` |
| thinking-restored matched run | `results/v5-large/E4B.v5-955.score.json` |
| strict difference +0.0103, range −0.0201 to +0.0404 | `harness/harness/bootstrap_ci.py`; recorded in `MEASUREMENT_LOG.md` |
| relation-agnostic 0.7783 and 0.8390 | the two matched prediction files above, rescored relation-agnostically |
| 770/770 reasoning restoration | `results/promptfix/google_gemma-4-E4B-it.log` |
| E4B `v4clause` 0/1,001 | `results/vast/gemma-4-E4B.v4clause.pred.jsonl` |
| partial E4B QAT reasoning, 2,523/3,002 | `results/qat-mid-3k/gemma-4-E4B-it.qat.mid.pred.jsonl` |
| granite, SmolLM3 and LFM2.5 no-clause probes | `results/vast/granite-4.1-3b.noclause.pred.jsonl`; `results/newcomers-1k/`; `results/vast/LFM2.5-230M.noclause.pred.jsonl` |

Median latency, completion length and throughput for the original 10,000-note run
come from the banked prediction file. The restored 20-note medians and the original
34-minute wall clock are single-sourced in `MEASUREMENT_LOG.md`.

## Reporting inventory and disposition

- **Prompt ablations:** kept. They isolate the sentence from the JSON-only
  requirement.
- **Matched-score comparison:** kept. The former +0.084 constant was replaced by
  +0.0103 with its paired range.
- **Relation-agnostic comparison:** kept, explicitly without an interval.
- **Cross-model no-clause probes:** kept. They refute a universal prompt-clause
  explanation.
- **Quantisation explanation for partial E4B reasoning:** withdrawn. A non-QAT
  build showed the same partial rate.
- **Category split:** kept as analysis of the matched predictions, not as a new
  independent run.

No external source or interview carries a material conclusion.
