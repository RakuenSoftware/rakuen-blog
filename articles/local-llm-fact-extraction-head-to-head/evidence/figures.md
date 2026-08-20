# Figure provenance

Every number in the article, and the artifact it came from. Paths are relative to
`evidence/raw/` in this folder unless stated otherwise.

Built by matching each printed F1 against the strict F1 in every scored artifact in
the results tree, rather than by transcribing from notes. Two errors in the article
were found that way and corrected: a fourth subset-extracted row that had been
described as three, and a partial-reasoning result attributed to QAT that also
appears on a non-QAT build.

## The corpus and the task

| figure | value | artifact |
|---|---|---|
| notes in the corpus | 1,001 | `corpus/data/corpora/v5/gold_small.jsonl` |
| notes whose correct answer is no facts | 322 | same, rows with empty `gold` |
| gold triples | 880 | same, summed over `gold` |
| note categories | 10 | same, distinct `category` |
| median note length | 53 characters | same |
| canonical predicates offered | 24 | `harness/harness/prompt.py`, seed list from `src/rel_types.c` |
| worked example, Vera Duarte | `member_of` | `corpus/data/corpora/v5/gold_small.jsonl`, id `g000009` |
| worked example, Fairweather Chemicals | empty gold | same corpus, `sales.transient.3` |
| retraction example, Kestrel Freight | `negated: true` | `harness/harness/prompt.py`, the prompt's own example |

## The main table

One row per arm. The `parse`, `abstain` and `spurious` columns come from the same
score file as the F1 on that row. The `reasons` column comes from the corresponding
prediction file.

| arm | F1 | artifact |
|---|---|---|
| Qwen3.6-35B-A3B UD-Q4 MoE | 0.7257 | `results/vast/Qwen3.6-35B-A3B.UD-Q4_K_XL.live.score.json` |
| Qwen3.6-27B dense UD-Q4 | 0.7152 | `results/vast/Qwen3.6-27B.UD-Q4_K_XL.live.score.json` |
| Muse Glimmer 30B K-Quant-17GB, DFlash off | 0.7100 | `results/muse-glimmer-30b-xtx-20260810/Muse-Glimmer-30B.K-Quant-17GB.xtx.dflash-off.{pred.jsonl,score.json}` |
| Qwen3.8-27B Q4_K_M, MTP | 0.7030 | `results/qwen38-27b-xtx-20260814/Qwen3.8-27B.Q4_K_M.xtx.mtp-on.{pred.jsonl,score.json,validation.json}` |
| gemma-4-31B QAT UD-Q4 | 0.6872 | `results/ct140/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.score.json` |
| gemma-4-12B QAT UD-Q4 | 0.6854 | `results/vast/gemma-4-12B-it.qat-UD-Q4_K_XL.live.score.json` |
| gemma-4-26B-A4B QAT UD-Q4 unsloth | 0.6804 | `results/ct140/gemma-4-26B-A4B.qat-unsloth-UDQ4.5080.score.json` |
| gemma-4-31B UD-Q4 | 0.6763 | `results/vast/gemma-4-31B-it.UD-Q4_K_XL.live.score.json` |
| gemma-4-12B UD-Q4 | 0.6754 | `results/ct140/gemma-4-12B-it.UD-Q4_K_XL.5080.score.json` |
| gemma-4-26B-A4B QAT q4_0 google | 0.6575 | `results/vast/gemma-4-26B-A4B.qat-google-q4_0.mtp.live.score.json` |
| gemma-4-E2B QAT q4_0 | 0.6406 | `results/qat-vs-ud/gemma-4-E2B-it.qat.score.json` |
| gemma-4-E4B UD-Q6 | 0.6339 | `results/v8-baseline/E4B.UD-Q6_K_XL.mtp.score.json` |
| gemma-4-E2B UD-Q8 | 0.6226 | `results/v8-baseline/E2B.UD-Q8_K_XL.mtp.score.json` |
| gemma-4-E4B QAT q4_0 | 0.6194 | `results/qat-vs-ud/gemma-4-E4B-it.qat.score.json` |
| gemma-4-E4B UD-Q4 | 0.6189 | `results/v8-baseline/E4B.UD-Q4_K_XL.mtp.score.json` |
| gemma-4-E2B UD-Q6 | 0.6179 | `results/v8-baseline/E2B.UD-Q6_K_XL.mtp.score.json` |
| gemma-4-E2B UD-Q4 | 0.6114 | `results/v8-baseline/E2B.UD-Q4_K_XL.mtp.score.json` |
| gemma-4-E4B UD-Q8 | 0.6094 | `results/v8-baseline/E4B.UD-Q8_K_XL.mtp.score.json` |
| LFM2.5-2.6B Q4_K_M | 0.5854 | `results/lfm25-2.6b/LFM2.5-2.6B.Q4_K_M.score.json` |
| LFM2.5-2.6B Q6_K | 0.5795 | `results/lfm25-2.6b/LFM2.5-2.6B.Q6_K.score.json` |
| LFM2.5-2.6B Q8_0 | 0.5750 | `results/lfm25-2.6b/LFM2.5-2.6B.Q8_0.score.json` |
| granite-4.1-3b UD-Q4 | 0.5432 | `results/subset-1001/granite-4.1-3b.sub1001.score.json` |
| gemma-3n-E4B UD-Q4 | 0.5331 | `results/subset-1001/gemma-3n-E4B.sub1001.score.json` |
| LFM2.5-8B-A1B Q4_K_M | 0.5198 | `results/lfm25-8b/LFM2.5-8B-A1B.Q4_K_M.score.json` |
| Qwen3-1.7B UD-Q4 | 0.4618 | `results/subset-1001/Qwen3-1.7B.sub1001.score.json` |
| SmolLM3-3B Q8_0 | 0.3933 | `results/newcomers-1k/SmolLM3-3B.Q8_0.score.json` |
| granite-4.0-1b UD-Q4 | 0.3911 | `results/subset-1001/granite-4.0-1b.sub1001.score.json` |
| LFM2.5-VL-1.6B Q6_K | 0.2744 | `results/lfm25-family/LFM2.5-VL-1.6B.Q6_K.score.json` |
| LFM2.5-VL-1.6B Q8_0 | 0.2725 | `results/lfm25-family/LFM2.5-VL-1.6B.Q8_0.score.json` |
| LFM2.5-1.2B Q6_K | 0.1771 | `results/lfm25-family/LFM2.5-1.2B-Instruct.Q6_K.score.json` |
| LFM2.5-1.2B Q8_0 | 0.1671 | `results/lfm25-family/LFM2.5-1.2B-Instruct.Q8_0.score.json` |
| MiniCPM5-1B Q8_0 | 0.1652 | `results/newcomers-1k/MiniCPM5-1B.Q8_0.score.json` |
| LFM2.5-230M Q6_K | 0.1363 | `results/lfm25-family/LFM2.5-230M.Q6_K.score.json` |
| LFM2.5-230M Q8_0 | 0.1309 | `results/lfm25-family/LFM2.5-230M.Q8_0.score.json` |

**Four rows are subset extractions**, not native 1,001-note runs: granite-4.1-3b,
gemma-3n-E4B, Qwen3-1.7B and granite-4.0-1b, all from `results/subset-1001/`. The
article states that limit against itself.

## Quant verdict graph and correction

The graph defaults to the supported same-model result rather than sorting the
point estimates. `=` is rendered as a tie; `>` is reserved for a paired range
that excludes zero. The command form, components and all thirteen paired results
are recorded in `raw/quant-clarification-2026-08-09.md`.

| family | graph verdict | artifacts |
|---|---|---|
| gemma-4-E2B | Q4 = Q6 = Q8 | `results/v8-baseline/E2B.UD-Q{4,6,8}_K_XL.mtp.pred.jsonl` |
| gemma-4-E4B | Q4 ties both; Q6 > Q8 | `results/v8-baseline/E4B.UD-Q{4,6,8}_K_XL.mtp.pred.jsonl` |
| LFM2.5-2.6B | Q4 = Q6 = Q8 | `results/lfm25-2.6b/LFM2.5-2.6B.Q{4_K_M,6_K,8_0}.pred.jsonl` |
| LFM2.5-VL-1.6B | Q6 = Q8 | `results/lfm25-family/LFM2.5-VL-1.6B.Q{6_K,8_0}.pred.jsonl` |
| LFM2.5-1.2B | Q6 = Q8 | `results/lfm25-family/LFM2.5-1.2B-Instruct.Q{6_K,8_0}.pred.jsonl` |
| LFM2.5-230M | Q6 = Q8 | `results/lfm25-family/LFM2.5-230M.Q{6_K,8_0}.pred.jsonl` |
| SmolLM3-3B | Q8 > Q4 | `results/newcomers-1k/SmolLM3-3B.Q{4_K_M,8_0}.pred.jsonl` |

The Smol Q4 comparison-only score is 0.3581 from
`results/newcomers-1k/SmolLM3-3B.Q4_K_M.score.json`; it is not one of the 34
leaderboard rows.

**Correction, 2026-08-09.** The original default graph ranked observed F1 and
therefore placed Q4 above Q6 or Q8 in two families whose paired ranges crossed
zero. The scores were observations; the vertical ordering communicated an
unsupported conclusion. The corrected graph states the paired verdict first and
retains the full score table under Numbers. The two Gemma Q4 rows now use the
matched v8-baseline campaign alongside their Q6 and Q8 rows. The same audit found
19 stale `abstain`/`spurious` pairs left from an earlier scorer interpretation;
the Numbers table, restraint comparison and scatter now read those fields from
the score artifacts mapped above. A reproduction pass ran each paired interval
in its own process; several endpoints moved in the fourth decimal and no verdict
changed.

## The matched Qwen3.6 comparison run

The Qwen3.8 paired comparison does not use the leaderboard's Qwen3.6-27B row. It
uses a separate run at the same quant, the same speculation setting and the same
card, so that the comparison holds those three constant.

| figure | value | artifact |
|---|---|---:|
| Qwen3.6-27B Q4_K_M, MTP on, RX 7900 XTX | 0.7177 F1, 0.6545 precision, 0.7943 recall | `results/qwen36-mtp-xtx/Qwen3.6-27b.Q4_K_M.xtx.mtp-on.score.json` |
| its prediction file, used by the bootstrap | 1,001 rows | `results/qwen36-mtp-xtx/Qwen3.6-27b.Q4_K_M.xtx.mtp-on.pred.jsonl` |
| the leaderboard Qwen3.6-27B row, a different run | 0.7152 F1, UD-Q4 | `results/vast/Qwen3.6-27B.UD-Q4_K_XL.live.score.json` |

The two Qwen3.6-27B numbers are different runs and the article now says so where
the comparison appears. The matched run is not a leaderboard row.

## Runtime builds

| campaign | build | source |
|---|---|---|
| `results/qwen38-27b-xtx-20260814/` | `llama.cpp` b10356 | `PROVENANCE.md` in that directory |
| `results/muse-glimmer-30b-xtx-20260810/` | `llama.cpp` b10356 (`0666ad2b2`) | `PARTIAL-2026-08-11.md` in that directory |

No other campaign recorded a build string per run. The article states that limit
instead of inferring a version from campaign dates.

## Intervals

All from `harness/harness/bootstrap_ci.py`, paired, resampling notes, fixed seed.

The Qwen3.8 comparisons use 20,000 replicates at seed 380827. Their captured
command and output are in
`results/qwen38-27b-xtx-20260814/bootstrap-20000-seed-380827.txt`.

| comparison | delta | interval |
|---|---|---|
| Qwen3.6-27B Q4_K_M MTP minus Qwen3.8-27B Q4_K_M MTP | +0.0147 | [−0.0038, +0.0335] |
| Qwen3.6-35B-A3B UD-Q4 minus Qwen3.8-27B Q4_K_M MTP | +0.0228 | [+0.0042, +0.0417] |
| 35B-A3B to 27B dense | −0.0106 | [−0.0294, +0.0088] |
| 27B dense to 31B QAT | −0.0280 | [−0.0456, −0.0106] |
| 31B QAT to 12B QAT | −0.0017 | [−0.0202, +0.0162] |
| 12B QAT to 26B unsloth | −0.0051 | [−0.0256, +0.0154] |
| 26B unsloth to 31B non-QAT | −0.0041 | [−0.0258, +0.0176] |
| 31B non-QAT to 12B non-QAT | −0.0009 | [−0.0197, +0.0180] |
| 12B non-QAT to 26B google | −0.0179 | [−0.0434, +0.0071] |
| 26B google to E2B QAT | −0.0168 | [−0.0406, +0.0070] |
| E2B QAT to 31B QAT | +0.0465 | [+0.0220, +0.0712] |
| E2B QAT to 35B-A3B | +0.0851 | [+0.0609, +0.1095] |

The two top-pair rows were run at 20,000 replicates against the finished 27B arm.
The remaining eight predate them. Muse Glimmer has no paired cross-model interval,
so it is not inserted into the ordering chain and carries no ordering claim.

## Throughput

| figure | value | artifact |
|---|---|---|
| gemma-4-26B-A4B QAT | 323.1 tok/s | `results/ct140/qat_speed.log` |
| Qwen3.6-35B-A3B | 234.0 tok/s | `results/vast/Qwen3.6-35B-A3B.UD-Q4_K_XL.live.pred.jsonl` |
| gemma-4-12B non-QAT | 195.8 tok/s | `results/ct140/arms.log` |
| gemma-4-12B QAT | 142.4 tok/s | `results/vast/gemma-4-12B-it.qat-UD-Q4_K_XL.live.pred.jsonl` |
| gemma-4-31B non-QAT | 80.5 tok/s | `results/vast/gemma-4-31B-it.UD-Q4_K_XL.live.pred.jsonl` |
| Qwen3.8-27B Q4_K_M, MTP | 72.1 tok/s | `results/qwen38-27b-xtx-20260814/Qwen3.8-27B.Q4_K_M.xtx.mtp-on.{pred.jsonl,validation.json}` |
| gemma-4-31B QAT | 67.3 tok/s | `results/ct140/shard_gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.run.log` |
| Qwen3.6-27B dense | 67.8 tok/s | `results/vast/Qwen3.6-27B.UD-Q4_K_XL.live.pred.jsonl`, median `predicted_per_second` over 1,001 rows |
| 27B median completion | 1,256 tok | same file |
| 35B median completion | 1,100 tok | `results/vast/Qwen3.6-35B-A3B.UD-Q4_K_XL.live.pred.jsonl` |
| 3.5x ratio | 234.0 / 67.8 | derived from the two rows above |

**Corrected figure.** The 27B was first reported at 64.7 tok/s from three samples
taken while the arm was still running. The finished arm gives 67.8 across 1,001
rows, flat in every hundred-row slice, 67.7 to 68.0. The earlier value was 4.6%
low. The article marks the correction where the figure appears.

## Reasoning

| figure | value | artifact |
|---|---|---|
| arms with no reasoning pass | 10 of 34 | `reasons` column, per-arm prediction files above; Qwen3.8 reasoned on 1,001 of 1,001 rows |
| gemma-4-E4B QAT q4_0 partial | 0.85 | `results/qat-vs-ud/gemma-4-E4B-it.qat.pred.jsonl` |
| gemma-4-E4B UD-Q6 partial | 0.846 | `results/v8-baseline/E4B.UD-Q6_K_XL.mtp.pred.jsonl`, 847 of 1,001 rows |
| clause removal restored reasoning | 770 of 770 | `MEASUREMENT_LOG.md`, prompt-clause probe |

The 85% result was previously attributed to quantisation-aware training. UD-Q6 is
not a QAT build and shows the same rate, while the same model at UD-Q4 and UD-Q8
reasons on every row. The article no longer claims a cause.

## Cross-hardware and configuration limits

| figure | value | artifact |
|---|---|---|
| rented 3090 against local 5080 | +0.0057 F1, CI [−0.0136, +0.0251] | `MEASUREMENT_LOG.md`, calibration entry |
| byte identity on that pair | 640 / 1001 | same |
| subset against native run | −0.0079, 47% of text differing | same |
| process count worth | about 0.0105 F1 | `ARTICLE_NOTES.md` |
| LFM2.5-8B-A1B file size | 5.16 GB | `results/lfm25-8b/` run log |
| Qwen3.8 context-limited rows | 1 of 1,001 | `results/qwen38-27b-xtx-20260814/Qwen3.8-27B.Q4_K_M.xtx.mtp-on.validation.json` |

## Qwen3.8 update

The collection method, runtime, model revisions, persistent `.254` storage
path, expected result and artifact disposition are recorded in
`results/qwen38-27b-xtx-20260814/PROVENANCE.md`. The figure-update source is
`harness/harness/update_qwen38_figures.py`.

This run is a native 1,001-note result. It adds one leaderboard row, one point
to the F1/restraint plot and one throughput observation. The paired Qwen3.6-27B
comparison is the closest saved configuration but uses an older `llama.cpp`
build. The Qwen3.6-35B-A3B comparison also changes quant, backend and hardware.
The article states both limits where the intervals appear.

## Not traced to an artifact in this folder

- **VRAM figures** (16.4, 13.27 and 15.84 GiB) are read from `llama.cpp` server
  startup output at load time and are not captured in a committed artifact. They
  are single-sourced and should be read as such.
- **The 1.79 TB/s card bandwidth** is a vendor specification, not a measurement.

## Correction, 2026-08-20

Three changes, made while bringing the article to the updated voice and article
guides. No raw artifact was altered, and no score changed.

**The rank ordinal was stale.** granite-4.1-3b was printed as twenty-first on
score with twenty runs above it. The Qwen3.8 row added on 2026-08-14 moved it to
twenty-second with twenty-one above it. Its finding is unchanged: at 69 spurious
triples it still invents fewer than every run scoring above it, the nearest of
which is Muse Glimmer 30B at 93.

**Two comparisons were withdrawn.** The article said the 35B beat a dense 31B by
more than the dense 31B beat a 2B. On observed scores that is false against the
QAT 31B, where 0.7257 minus 0.6872 is +0.0385 against the ladder's +0.0465, and
there is no paired interval between the 35B and either 31B run. The article also
gave per-token weight traffic as 16.4 GiB against roughly 1.5 GiB; 16.4 GiB is
the 35B-A3B's own measured footprint, reused as a dense 27B figure it was never
measured for. Both are marked as withdrawn at the point they appeared.

**The matched Qwen3.6 comparison run is now traced**, above, with its own 0.7177
score and its distinction from the 0.7152 leaderboard row.
