# Two Bits Killed the Dense Model and the Mixture Barely Noticed

A one-bit 35B mixture-of-experts loses four points; a two-bit 12B dense model loses thirty-six. The largest speed difference measured was whether the file fit.

## Status

**DO NOT PUBLISH v1.** Superseded in place by an unfinished campaign, which is a
worse state than either finished or untouched.

`article/which-quant-beats-how-many-bits.md` was marked publication-ready on
2026-08-09 and never published. That status was accurate against the evidence
that existed then and is not accurate now. The campaign begun 2026-08-16 has
measured things v1 asserts:

- v1 **withdraws** the claim that LFM2.5 worsens with more bits, "because its
  range crosses zero". The campaign measures Q8 minus Q4 at −0.0327
  [−0.0592, −0.0063], which clears zero.
- v1's QAT section rests on gemma-4 E2B alone. Four models now have matched
  QAT and non-QAT arms, and the two-bit QAT collapse — the largest effect
  measured anywhere in this work, −0.3511 and −0.2982 — is a rung v1 never ran.
- v1 has **no two-bit data**, and two bits is where the cliff actually is:
  −0.357 on gemma-4 12B, against −0.033 on E4B.
- v1's own figure map already listed the 12B same-card rerun and a second
  corpus as open.

So v1 is not wrong so much as **incomplete in ways that change its emphasis**.
Publishing it now would put a piece into the world that the next revision
immediately contradicts, and the contradiction would be ours rather than a
reader's.

The successor is `article/which-quant-beats-how-many-bits.v2-draft.md`, which is
itself incomplete: seven arms are outstanding and its synthesis figures carry no
paired intervals. Neither file is publishable today. v1 is retained unmodified
because it is the reference the v2 draft reproduces findings against, not
because it is ready.

**The campaign is COMPLETE as of 2026-08-22: 34 of 34 arms, both tasks, zero
failed, zero gated, zero invalid.** Audited independently — every arm has full
prediction rows and a synthesis success rate of 1.0. It ran 34 arms across seven models on
one RTX 5080, each scored on both the 1,001-note extraction corpus and the
1,000-case synthesis fixture, and it supplies what the published version lacks:
ladders on mixture-of-expert models and above 12B, a second task, Q2 and Q1
rungs, QAT arms beside their non-QAT rungs at the same width, a KV-cache
precision sweep, and same-card throughput for every rung.

- `evidence/moe-ladder-plan-2026-08-16.md` — the plan, registered before any arm
  ran, including the availability findings that changed the design three times
  and the reason the campaign is not parallelised across hosts.
- `article/which-quant-beats-how-many-bits.v2-draft.md` — the successor,
  carrying the campaign's findings. Marked `draft: true`. Kept beside v1 rather
  than overwriting it so the earlier claims stay readable for comparison, since
  the revision reproduces two of them independently.
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
