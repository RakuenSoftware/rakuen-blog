# Figure provenance and reporting record

Paths below are relative to the shared series evidence base at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## Size and architecture tables

| figure | value | artifact |
|---|---|---|
| gemma-4-E2B QAT | 0.6406 | `results/qat-vs-ud/gemma-4-E2B-it.qat.score.json` |
| gemma-4-26B-A4B QAT | 0.6804 | `results/ct140/gemma-4-26B-A4B.qat-unsloth-UDQ4.5080.score.json` |
| gemma-4-12B QAT | 0.6854 | `results/vast/gemma-4-12B-it.qat-UD-Q4_K_XL.live.score.json` |
| gemma-4-31B QAT | 0.6872 | `results/ct140/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.score.json` |
| E2B to 31B | +0.0465, range +0.0220 to +0.0712 | `harness/harness/bootstrap_ci.py`; mapped in the head-to-head `evidence/figures.md` |
| Qwen3.6-35B-A3B | 0.7257 and 234.0 tok/s | `results/vast/Qwen3.6-35B-A3B.UD-Q4_K_XL.live.score.json` and matching prediction file |
| Qwen3.6-27B | 67.8 tok/s | `results/vast/Qwen3.6-27B.UD-Q4_K_XL.live.pred.jsonl` |
| 35B against 31B | +0.0386, range +0.0194 to +0.0577 | `harness/harness/bootstrap_ci.py`; `ARTICLE_NOTES.md` |

Every adjacent-model interval printed in the article is reproduced in
`articles/local-llm-fact-extraction-head-to-head/evidence/figures.md` under
“Intervals”.

## Small-model diagnostics

| figure | artifact |
|---|---|
| LFM2.5-1.2B parse rates and scores | `results/lfm25-family/LFM2.5-1.2B-Instruct.*.score.json` |
| MiniCPM5-1B parse rate and score | `results/newcomers-1k/MiniCPM5-1B.Q8_0.score.json` |
| LFM2.5-230M parse rate and score | `results/lfm25-family/LFM2.5-230M.*.score.json` |
| reasoning-row counts across the field | per-run prediction files above; summary in `ARTICLE_NOTES.md` |
| cost span of sixteen | observed run logs summarised in `ARTICLE_NOTES.md`; single-sourced because no billing artifact was retained |

## Reporting inventory and disposition

- **Twenty-two models across 32 run configurations:** kept. Scores, parse rates
  and reasoning counts remain in the article. The prompt-clause diagnostic was
  completed for four configurations; 28 remain unchecked.
- **Paired bootstrap comparisons:** kept. Adjacent nulls and the endpoint
  difference remain distinct.
- **Architecture comparison:** kept. Active parameters, resident parameters and
  throughput are not collapsed into one size measure.
- **Sub-2B capability claim:** narrowed. Parse failures are described as score
  floors, and the second-corpus test remains explicitly open.
- **Load-time observations:** preserved as an open measurement, not promoted to a
  figure because the article has no banked load-time artifact.

No external source carries a material conclusion. Parameter counts come from the
model identities recorded by the run harness.
