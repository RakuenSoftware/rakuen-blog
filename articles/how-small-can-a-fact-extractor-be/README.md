# A 2B Fact Extractor Came Within 0.047 of a 31B One

Size changed the endpoint score, while architecture and output discipline changed the deployment decision.

## Status

Publication-ready as of 2026-08-09. Not yet published. Every figure in the article
is accounted for in the local provenance map.

## Evidence

Raw artifacts for the whole series live under
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`:

| directory | contents |
|---|---|
| `results/` | every prediction file, score file and run log produced by the benchmark |
| `corpus/` | corpus v5, the gold sets at 1,001, 3,002 and 10,000 notes |
| `harness/` | the runner, scorer, bootstrap and orchestration scripts that produced them |
| `ARTICLE_NOTES.md` | the running findings ledger |
| `MEASUREMENT_LOG.md` | the defect log, including every retracted claim |

`evidence/figures.md` maps the article's measurements to raw artifacts or marks
them as single-sourced. It also records the disposition of every first-party test
used in the draft.

## Reporting record

This article reports first-party measurement only. There are no external sources,
interviews or vendor claims in it, so there is no right-of-reply obligation
outstanding. Where a prior claim was withdrawn, the withdrawal is stated in the
article at the point the claim appeared, and the superseded run is retained under
`results/`.
