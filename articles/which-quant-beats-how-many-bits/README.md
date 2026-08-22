# Two Bits Killed the Dense Model and the Mixture Barely Noticed

A one-bit 35B mixture-of-experts loses four points; a two-bit 12B dense model loses thirty-six. The largest speed difference measured was whether the file fit.

## Status

Held for further testing. Not a publication candidate, and deliberately not
marked as one, so the voice gate and `tools/publish.py` no longer offer it.

`article/which-quant-beats-how-many-bits.md` was gated and provenance-complete on
2026-08-09, and nothing in it is known to be wrong. It was held because its
conclusions rested on too little measurement to publish as guidance: two of five
bit-width comparisons separated, the 12B and 26B pairs crossed machines, and
every ladder shared one corpus lineage, so a stable effect could still be a
stable artifact of that corpus.

The 31B pair showed what that costs. Its same-card 3,002-note rerun moved the
difference from +0.0108 to +0.0009 and closed the interval around zero, because
most of what the earlier pair measured was the hardware.

The parse-floor bound that this article was to carry for the series has moved to
`the-harness-measured-itself`, so holding this one back does not strand it.

## The campaign that answers it

**COMPLETE as of 2026-08-22: 37 of 37 runs, both tasks, zero failed, zero gated,
zero invalid.** Audited independently, every run has full prediction rows and a
synthesis success rate of 1.0. It ran 37 runs across seven models on one RTX
5080, each scored on both the 1,001-note extraction corpus and the 1,000-case
synthesis fixture, and it supplies what v1 lacks: ladders on mixture-of-expert
models and above 12B, a second task, Q2 and Q1 rungs, QAT runs beside their
non-QAT rungs at the same width, BF16 on every model that could hold it, and
same-card throughput for every rung.

**Both tasks carry paired intervals**: 45 extraction comparisons at 20,000
replicates, of which 15 separate, and 44 synthesis comparisons at 5,000
replicates, of which 10 separate. The synthesis half had none until 2026-08-22.
The series' paired bootstrap lived in the `synthesis-model-selection` ab-v1
harness, hardcoded to two fixture directories and a 10,000-case population, so it
could not be pointed at a campaign run; `campaign/synth_pair_ci.py` is that
computation with its inputs made arguments, validated by reproducing the
published ab-v1 pair bit for bit.

The campaign contradicts v1 in three places, which is why v1 stays held rather
than being published while a successor is written:

- v1 withdraws the claim that LFM2.5 worsens with more bits, "because its range
  crosses zero". The campaign measures Q8 minus Q4 at −0.0327 [−0.0592, −0.0063],
  which clears zero.
- v1's QAT section rests on gemma-4 E2B alone. Four models now have matched QAT
  and non-QAT runs, and the two-bit QAT collapse, the largest effect measured
  anywhere in this work at −0.3511 and −0.2982, is a rung v1 never ran.
- v1 has no two-bit data, and two bits is where the cliff is: −0.357 on gemma-4
  12B against −0.033 on E4B.

The successor is `article/which-quant-beats-how-many-bits.v2-draft.md`, complete
against its evidence and awaiting review. v1 is retained unmodified because it is
the reference the v2 draft reproduces findings against, not because it is ready.

The KV-cache precision sweep this campaign also ran belongs to
`articles/kv-cache-precision/` and is excluded from this ladder.

- `evidence/moe-ladder-plan-2026-08-16.md` — the plan, registered before any run
  started, including the availability findings that changed the design three
  times and the reason the campaign is not parallelised across hosts.
- `article/which-quant-beats-how-many-bits.v2-draft.md` — the successor, carrying
  the campaign's findings. Marked `draft: true`. Kept beside v1 so the earlier
  claims stay readable for comparison, since the revision reproduces two of them
  independently.
- `evidence/moe-ladder-measurement-log-2026-08-16.md` — the defect log. Eleven
  faults, every one of which produced output indistinguishable from success; two
  campaigns discarded; the results standing with their paired intervals.
- `evidence/campaign-results/arms-2026-08-22.json` — all 37 runs, both tasks,
  with throughput and offload state.
- `evidence/campaign-results/extraction-pairs-2026-08-22.json` and
  `synthesis-pairs-2026-08-22.json` — every paired interval, so a figure can read
  its range from evidence rather than have it retyped.

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
