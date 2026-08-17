# Quantization Choice Mattered More Than Bit Count

Only one bit-width step separated; QAT's clearest benefit was fitting a 26B model on a 16-gibibyte card.

## Status

Held for further testing. Not a publication candidate, and deliberately not
marked as one, so the voice gate and `tools/publish.py` no longer offer it.

The article was gated and provenance-complete on 2026-08-09, and nothing here is
known to be wrong. It is held because the conclusions rest on too little
measurement to publish as guidance. Two of five bit-width comparisons separated,
the 12B and 26B pairs still cross machines, the 26B dynamic-packing result needs
a same-card rerun, and the 12B repair bound behind the parse floors was never
computed. Every ladder also shares one corpus lineage, so a stable effect can
still be a stable artifact of that corpus.

The 31B pair shows what the remaining work looks like: its same-card 3,002-note
rerun moved the difference from +0.0108 to +0.0009 and closed the interval around
zero, because most of what the earlier pair measured was the hardware.

The parse-floor bound that this article was to carry for the series has moved to
`the-harness-measured-itself`, so holding this one back does not strand it.

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
