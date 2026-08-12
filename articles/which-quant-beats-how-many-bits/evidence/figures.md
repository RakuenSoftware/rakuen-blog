# Figure provenance and reporting record

Paths below are relative to the shared series evidence base at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## Bit-width ladders

| comparison | artifacts |
|---|---|
| gemma-4 E2B Q4, Q6 and Q8 | `results/v8-baseline/E2B.UD-Q{4,6,8}_K_XL.mtp.score.json` |
| gemma-4 E4B Q4, Q6 and Q8 | `results/v8-baseline/E4B.UD-Q{4,6,8}_K_XL.mtp.score.json` |
| SmolLM3 Q4 and Q8 | `results/newcomers-1k/SmolLM3-3B.*.score.json` |
| LFM2.5-2.6B Q4, Q6 and Q8 | `results/lfm25-2.6b/LFM2.5-2.6B.*.score.json` |
| 10,000-note E2B ladder, 0.6246, 0.6344, 0.6329 | `results/10k-sharded/E2B.UD-Q{4,6,8}_K_XL.10k.score.json` |
| 10,000-note E4B ladder, 0.6301, 0.6452, 0.6337 | `results/10k-sharded/E4B.UD-Q{4,6,8}_K_XL.10k.score.json` |

The 10k ladder figures were corrected on 2026-08-11. The article previously gave
the E4B ladder as 0.6324, 0.6450 and 0.6321, which are the **quarantined**
`--cache-ram 8192` originals under
`results/10k-sharded/quarantine/E4B-10k-cacheram8192-20260804T0041Z/`. Those arms
were re-taken at `--cache-ram 1024` so both families share one results-affecting
cache value, and only the re-taken runs carry a ladder comparison. The quarantined
files are retained, not deleted; `MEASUREMENT_LOG.md` records the re-run and its
per-arm deltas of −0.0023, +0.0002 and +0.0016. The direction of the finding is
unchanged: both ladders peak at Q6.

All four gemma quants come from the matched `results/v8-baseline/` campaign. An
earlier version of this map paired Q6 and Q8 from `v8-baseline` against Q4 from
`results/v5-rerun-gguf/`. Those are different run campaigns and do not carry a
quant verdict; `quant-clarification-2026-08-09.md` records the correction and
the superseded pairing is retained there.

All paired ranges were produced by `harness/harness/bootstrap_ci.py`, resampling
notes with seed `20260809` and 20,000 replicates, one comparison per process. The
scorer draws the individual-run and paired intervals from one random stream, so a
third `--pred` argument moves a paired endpoint even at the same seed; the
one-pair-per-invocation values in `quant-clarification-2026-08-09.md` are the
published ones. The LFM inverse-ladder claim was withdrawn after its range crossed
zero.

All five rows were recomputed from the prediction files on 2026-08-11 and
reproduce exactly, including both `significant` verdicts. That recomputation was
only possible after the pinned scorer ontology under
`articles/local-llm-fact-extraction-head-to-head/evidence/src/` was restored; see
that folder's README for why the pin is version-specific.

## QAT and packing

| figure | artifact |
|---|---|
| E2B and E4B QAT pairs | `results/qat-vs-ud/*.score.json` |
| 12B QAT and non-QAT | `results/vast/gemma-4-12B-it.qat-UD-Q4_K_XL.live.score.json`; `results/ct140/gemma-4-12B-it.UD-Q4_K_XL.5080.score.json` |
| 31B QAT and non-QAT | `results/ct140/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.score.json`; `results/vast/gemma-4-31B-it.UD-Q4_K_XL.live.score.json` |
| 26B unsloth dynamic and google q4_0 | `results/ct140/gemma-4-26B-A4B.qat-unsloth-UDQ4.5080.score.json`; `results/vast/gemma-4-26B-A4B.qat-google-q4_0.mtp.live.score.json` |
| 12B same-host speed probe | `results/ct140/qat_speed.log`; supporting acceptance counters in the matching prediction files |
| speculative acceptance table | the six prediction files mapped in `articles/speculative-decoding-was-free/evidence/figures.md` |
| model file and resident-memory sizes | server startup logs and `ARTICLE_NOTES.md`; several sizes are single-sourced because no dedicated size artifact was retained |

## The 31B same-card rerun, completed 2026-08-12

| figure | artifact |
|---|---|
| 31B QAT 0.6867 at 3,002 notes | `results/mid3k-rerun-20260811/gemma-4-31B-it.qat.mid3k.score.json` |
| 31B non-QAT 0.6857 at 3,002 notes | `results/mid3k-rerun-20260811/gemma-4-31B-it.nonqat.mid3k.score.json` |
| +0.0009, −0.0064 to +0.0082, indistinguishable | the paired bootstrap the campaign script ran itself, in `results/mid3k-rerun-20260811/mid3k_xtx.log` |

Both halves on one RX 7900 XTX, 3,002 notes, concurrency 1, speculation active on
every row. `results/mid3k-rerun-20260811/PROVENANCE.md` carries the full
collection record, the artifact integrity checks and the registered prediction
quoted verbatim.

The registered prediction called the half-width and missed the effect. It said
0.0072 and the run gave 0.0073, conditional on the point estimate holding, and
the point estimate fell from +0.0108 to +0.0009. The condition was stated in
advance, which is what makes the answer clean rather than arguable.

This supersedes the 1,001-note 31B row, which paired CT140 against a rented host.
That row is kept in the article beside the new one because the comparison between
them is the finding: the difference was mostly the hardware.

## The 12B half was never completed

`harness/harness/mid3k_pairs.sh` registers a 12B pair on the 5080. It has no
prediction or score file anywhere on this machine, searched 2026-08-12.

Its log under `results/mid3k/` records two `START` lines four seconds apart, at
10:55:09Z and 10:55:13Z on 2026-08-10, from two overlapping launcher invocations
that would have contended for port 8300 and the card. After that, nothing: no
`DONE`, no `FAIL`, no stop reason.

Stated precisely, it is not a run that was attempted and failed to finish. It is
a run started twice and abandoned without recording an outcome. Nothing here
supersedes the 12B row.

`results/mid3k/` holds those launch logs and is left untouched. The similarly
named `results/qat-mid-3k/` is an earlier, completed E2B/E4B prediction set used
by the reasoning and subset analyses.

## Reporting inventory and disposition

- **Five bit-width comparisons:** kept. Two clear their paired range, SmolLM3
  Q8-over-Q4 and gemma-4-E4B Q6-over-Q8, and they point opposite ways on width.
  The gemma Q4 rows were repaired to their matched `v8-baseline` runs; the four
  interval endpoints that moved under one-pair-per-process scoring were updated
  with them, and no verdict changed side of zero.
- **Eight historical E2B signs:** kept as a sign test with shared-lineage
  dependence stated against it.
- **Four QAT size comparisons:** kept. Only E2B supports an accuracy benefit.
- **26B packing comparison:** kept but downgraded from a recommendation because
  the pair crossed hardware and the calibration bound nearly covers its lower
  edge.
- **Same-host 12B throughput probe:** kept. The tensor-type explanation remains
  unverified.
- **Floor correction:** kept. Failed rows bound the possible repair below the
  experiment's noise.
- **31B same-card rerun:** completed 2026-08-12 and supersedes the 1,001-note
  cross-machine row. The QAT difference at 31B is indistinguishable from zero
  once both halves run on one card.
- **12B same-card rerun and the second corpus:** remain open and are not
  described as completed evidence.

No interview or external benchmark carries a material conclusion. Model identities
and parameter counts come from the recorded run configuration.
