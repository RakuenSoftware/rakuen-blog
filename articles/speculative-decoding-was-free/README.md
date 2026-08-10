# Local LLMs: Speculative Decoding

Six paired runs measuring what letting a small model guess ahead costs in
accuracy, what it gains in speed, and what it does not explain.

## Status

Unpublished 2026-08-10. The article mixed seven controlled MTP on/off pairs with
unpaired 12B, 26B and 31B acceptance runs. Those larger-model runs have MTP-on
acceptance and F1 measurements but no same-condition MTP-off partners, so they
cannot support a causal MTP speed or accuracy comparison.

The RX 7900 XTX follow-up now includes a complete Qwen3.6-27B MTP on/off pair.
MTP increased throughput from 34.82 to 81.78 tokens/s, a 2.35x speedup, with
79.04% draft acceptance. Strict F1 was 0.7180 off and 0.7177 on; the paired
difference was −0.0003 with a 95% range of −0.0109 to +0.0101.

The Qwen3.6-35B-A3B follow-up is not part of the article. Its MTP-on run was
still active when the 27B update was prepared, and no incomplete or unmatched
run is interpreted.

## Evidence

Raw artifacts for the whole series live under
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`, which every
article shares rather than copying 173 MB of prediction files per folder:

| directory | contents |
|---|---|
| `results/` | every prediction file, score file and run log produced by the benchmark |
| `corpus/` | the note sets at 1,001, 3,002 and 10,000 notes |
| `harness/` | the runner, scorer, bootstrap and orchestration scripts that produced them |
| `ARTICLE_NOTES.md` | the running findings ledger |
| `MEASUREMENT_LOG.md` | the defect log, including every retracted claim |

`evidence/figures.md` maps each figure in the article to the artifact behind it.
Every path in it was checked to resolve. Twelve scores were matched against the
score files, and all six acceptance rates were recomputed from the prediction
files rather than transcribed. Six figures are marked there as single-sourced
rather than traced, including the identical-output counts and the startup times,
which the sweep computed and discarded.

## Reporting record

This article reports first-party measurement only. There are no external sources,
interviews or vendor claims in it, so there is no right-of-reply obligation
outstanding. Where a prior claim was withdrawn, the withdrawal is stated in the
article at the point the claim appeared, and the superseded run is retained under
`results/`.
