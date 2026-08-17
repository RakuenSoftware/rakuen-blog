# The Harness Measured Itself

A confidence gate, a parser, a truncation flag, a name guard, a throughput
figure, a size ladder and three kinds of zero each returned a number about the
harness rather than the model.

## Status

Publication-ready as of 2026-08-10. Not yet published. Every figure in the
article is accounted for in the local provenance map.

This article merges the two earlier compilations, `eight-ways-a-run-scores-fine-and-is-broken`
and `my-benchmark-lied-to-me`, and takes the endpoint-versus-rung result from
`how-small-can-a-fact-extractor-be`. Those three folders are removed. Between
them they held eighteen sections, and all but seven restated a finding that
another article in the series measures in more depth.

It also carries two findings that lost their intended home. The parse-floor bound
was routed to `which-quant-beats-how-many-bits`, which was subsequently held back
for further testing, and the unwritten-field zero comes from
`three-zeros-and-a-wrong-answer`, which is retired. Both are measurement-harness
failures and belong with the rest.

Every finding dropped in that merge is still published in the article that owns
its evidence. The closing section names each one, so the checklist remains the
entry point to the series without reprinting figures it did not produce. The
title carries no count on purpose: the set has changed twice already.

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

This article reports first-party measurement only. The two Hugging Face
repository links establish present artifact availability and carry no measurement
conclusion. Where a prior claim was withdrawn, the withdrawal is stated in the
article at the point the claim appeared, and the superseded run is retained under
`results/`.
