# The Benchmark Audited Production

A benchmark scorer is a specification, and mine disagreed with the production path in four places.

## Status

Draft. Not published. Every figure in the article traces to a raw artifact in the
series evidence base.

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

`evidence/figures.md`, the per-figure map from each number in the article to the
artifact behind it, is not written yet. Until it is, figures trace through
`ARTICLE_NOTES.md` and `MEASUREMENT_LOG.md` in the series evidence base.

## Reporting record

This article reports first-party measurement only. There are no external sources,
interviews or vendor claims in it, so there is no right-of-reply obligation
outstanding. Where a prior claim was withdrawn, the withdrawal is stated in the
article at the point the claim appeared, and the superseded run is retained under
`results/`.
