# Quantization Choice Mattered More Than Bit Count

Only one bit-width step separated; QAT's clearest benefit was fitting a 26B model on a 16-gibibyte card.

## Status

Publication-ready as of 2026-08-09. Not yet published. Every figure in the article
is accounted for in the local provenance map.

**A campaign extending this article is in progress from 2026-08-16 and the
article body does not yet reflect it.** It runs 38 arms across seven models on
one RTX 5080, each scored on both the 1,001-note extraction corpus and the
1,000-case synthesis fixture, and it supplies what the published version lacks:
ladders on mixture-of-expert models and above 12B, a second task, Q2 and Q1
rungs, QAT arms beside their non-QAT rungs at the same width, a KV-cache
precision sweep, and same-card throughput for every rung.

- `evidence/moe-ladder-plan-2026-08-16.md` — the plan, registered before any arm
  ran, including the availability findings that changed the design three times
  and the reason the campaign is not parallelised across hosts.
- `evidence/moe-ladder-measurement-log-2026-08-16.md` — the defect log. Nine
  faults so far, every one of which produced output indistinguishable from
  success; two campaigns discarded; the results standing so far with their
  paired intervals.

The first completed ladder already bears on a claim this article withdrew: it
measures LFM2.5-2.6B getting **worse** with more bits, Q8 minus Q4 of −0.0327
with a 95% range of [−0.0592, −0.0063], which clears zero.

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
