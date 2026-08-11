# Figure provenance and reporting record

Paths below are relative to the shared series evidence base at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## Measurements used

| article section | measurement | artifact or record |
|---|---|---|
| F1 is not blind | factless-category scores and the scorer correction | `MEASUREMENT_LOG.md`, defect 24; `harness/harness/score.py` |
| tool-call envelope | parse collapse with normal completion lengths | `MEASUREMENT_LOG.md`, defects 7 and 8 |
| context exhausted | token totals and the missing truncation guard | `ARTICLE_NOTES.md`, context-length audit; affected files under `results/diagnostics/` |
| reasoning stopped | E4B reasoning rows and prompt-clause probes | `results/vast/gemma-4-E4B.v4clause.pred.jsonl`; `results/promptfix/google_gemma-4-E4B-it.log` |
| score was a floor | parse failures, 15 gold facts in 40 failed rows, +0.0038 bound | `results/qat-vs-ud/gemma-4-E2B-it.qat.pred.jsonl`; `MEASUREMENT_LOG.md`, floor audit |
| tied models | 31B and 12B QAT scores, recall, abstention and invention | `results/ct140/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.score.json`; `results/vast/gemma-4-12B-it.qat-UD-Q4_K_XL.live.score.json` |
| tied-model interval | −0.0017, range −0.0202 to +0.0162 | `harness/harness/bootstrap_ci.py`, recorded in the head-to-head `evidence/figures.md` |
| quant behaviour | E2B and E4B abstention and spurious-fact rows | `results/v8-baseline/*.score.json`; `ARTICLE_NOTES.md` |
| confidence floor | floored and unfloored scores, including the zeroed runs | `results/noconf/`; `harness/harness/score.py` |
| two zeroes | parse-success and parse-failure examples that both printed zero | `MEASUREMENT_LOG.md`, scorer and guard audits |
| guard refusal | model-name guard rejecting an otherwise serving model | `MEASUREMENT_LOG.md`, host-placement defect record |

The 31B/12B table reproduces the values already mapped to raw score files in
`articles/local-llm-fact-extraction-head-to-head/evidence/figures.md`.

## Reporting inventory and disposition

- **Scorer audit:** kept. The claim that F1 was blind was corrected in the text.
- **Parse, schema, token and reasoning audits:** kept as separate runtime signals.
- **Confidence-floor probes:** kept, with floored and unfloored results distinguished.
- **Model guard and host observations:** kept as single-sourced observations from
  `MEASUREMENT_LOG.md`; no raw API response was preserved.
- **Causal explanation for E4B's partial reasoning:** withdrawn. The article says
  the cause remains unknown.

No external sources, interviews or vendor claims carry a material conclusion.
