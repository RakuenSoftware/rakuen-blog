# Local Llm Fact Extraction Head To Head

Twenty-four local models on one 1,001-note fact-extraction corpus, with a paired bootstrap on every ordering claim.

## Status

Published 2026-08-06 and updated 2026-08-14 with Qwen3.8-27B Q4_K_M. Every
figure in the article traces to a raw artifact in the series evidence base.

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

`evidence/figures.md` maps each figure in the article to the artifact behind it.
Every path in it was checked to resolve. Two figures are marked there as
single-sourced rather than traced: the VRAM readings and the card bandwidth.

## Reporting record

This article reports first-party measurement only. There are no external sources,
interviews or vendor claims in it, so there is no right-of-reply obligation
outstanding. Where a prior claim was withdrawn, the withdrawal is stated in the
article at the point the claim appeared, and the superseded run is retained under
`results/`.
