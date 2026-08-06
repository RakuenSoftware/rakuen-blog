# Figure provenance

Every number in the article, and the artifact it came from. Paths are relative to
the series evidence base at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`, which the whole
series shares rather than copying 173 MB of prediction files per article.

Built the same way as the head-to-head's map: each printed score was matched
against the strict F1 in every scored artifact in the results tree, and the
acceptance figures were recomputed from the prediction files rather than
transcribed. All twelve scores and all six acceptance rates reproduce exactly.

## The paired table: guessing on against guessing off

Twelve scores, six pairs. Every one is 10,000 notes. The two directories are the
whole experiment: `10k-sharded` ran with guessing on, `10k-nomtp` ran with it off,
and nothing else differs.

| cell | value | artifact |
|---|---|---|
| E2B Q4, on | 0.6246 | `results/10k-sharded/E2B.UD-Q4_K_XL.10k.score.json` |
| E2B Q4, off | 0.6207 | `results/10k-nomtp/E2B.UD-Q4_K_XL.10k.score.json` |
| E2B Q6, on | 0.6344 | `results/10k-sharded/E2B.UD-Q6_K_XL.10k.score.json` |
| E2B Q6, off | 0.6331 | `results/10k-nomtp/E2B.UD-Q6_K_XL.10k.score.json` |
| E2B Q8, on | 0.6329 | `results/10k-sharded/E2B.UD-Q8_K_XL.10k.score.json` |
| E2B Q8, off | 0.6351 | `results/10k-nomtp/E2B.UD-Q8_K_XL.10k.score.json` |
| E4B Q4, on | 0.6301 | `results/10k-sharded/E4B.UD-Q4_K_XL.10k.score.json` |
| E4B Q4, off | 0.6306 | `results/10k-nomtp/E4B.UD-Q4_K_XL.10k.score.json` |
| E4B Q6, on | 0.6452 | `results/10k-sharded/E4B.UD-Q6_K_XL.10k.score.json` |
| E4B Q6, off | 0.6435 | `results/10k-nomtp/E4B.UD-Q6_K_XL.10k.score.json` |
| E4B Q8, on | 0.6337 | `results/10k-sharded/E4B.UD-Q8_K_XL.10k.score.json` |
| E4B Q8, off | 0.6327 | `results/10k-nomtp/E4B.UD-Q8_K_XL.10k.score.json` |

Throughput percentages on the same rows come from the run logs beside those score
files, not from the score files themselves.

## The ranges

Three of the six pairs carry a resampled range, from
`harness/harness/bootstrap_ci.py`, paired, resampling notes, fixed seed, 20,000
replicates over the same 10,000 notes.

| pair | difference, off minus on | range |
|---|---|---|
| E4B Q4 | +0.0005 | −0.0028 to +0.0036 |
| E4B Q6 | −0.0017 | −0.0048 to +0.0013 |
| E4B Q8 | −0.0010 | −0.0041 to +0.0021 |

The other three pairs have no range. The article says so where it uses them.

## Acceptance

Recomputed from `draft_n` and `draft_n_accepted` summed over every row of each
prediction file. All six reproduce the published figure exactly.

| run | guessed | kept | artifact |
|---|---|---|---|
| gemma-4-12B non-QAT | 1,510,235 | 82.0% | `results/ct140/gemma-4-12B-it.UD-Q4_K_XL.5080.pred.jsonl` |
| gemma-4-12B QAT | 1,414,986 | 81.2% | `results/vast/gemma-4-12B-it.qat-UD-Q4_K_XL.live.pred.jsonl` |
| gemma-4-26B-A4B unsloth QAT | 1,360,556 | 79.2% | `results/ct140/gemma-4-26B-A4B.qat-unsloth-UDQ4.5080.pred.jsonl` |
| gemma-4-26B-A4B google q4_0 | 1,367,766 | 79.1% | `results/vast/gemma-4-26B-A4B.qat-google-q4_0.mtp.live.pred.jsonl` |
| gemma-4-31B QAT | 539,715 | 79.1% | `results/ct140/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.pred.jsonl` |
| gemma-4-31B non-QAT | 620,046 | 78.5% | `results/vast/gemma-4-31B-it.UD-Q4_K_XL.live.pred.jsonl` |

## The Qwen comparison

| figure | value | artifact |
|---|---|---|
| 35B-A3B throughput | 234.0 words/s | `results/vast/Qwen3.6-35B-A3B.UD-Q4_K_XL.live.pred.jsonl` |
| 35B-A3B median written | 1,100 words | same file |
| 27B dense throughput | 67.8 words/s | `results/vast/Qwen3.6-27B.UD-Q4_K_XL.live.pred.jsonl` |
| 27B dense median written | 1,256 words | same file |
| the two are a tie | −0.0106, range −0.0294 to +0.0088 | `harness/harness/bootstrap_ci.py`, 20,000 replicates |
| neither uses guessing | no `draft_n` on any row | both prediction files above |

## Not traced to an artifact in this folder

These are in the article and are **not** reproducible from anything committed
here. Each is single-sourced.

- **Identical-output counts** (100/100 and 74/100) come from a 100-note
  comparison run with the randomness turned off, recorded in
  `MEASUREMENT_LOG.md` rather than kept as prediction files.
- **Startup seconds by process count** come from the two sweep logs, which the
  sweep computed and discarded rather than saving as an artifact. That is the
  same discarded column the article is about.
- **Notes per minute** for the sequential and guessing runs (22.9, 41.9, 27.0,
  43.0) come from run logs, not score files.
- **The concurrency figures** (4.54x and 4.34x at thirty-two at a time) come from
  `ARTICLE_NOTES.md`.
- **Card bandwidth** of 1.79 TB/s is a vendor specification, not a measurement.
- **Per-word read sizes** (16.4 GiB, about 1.5 GiB) are derived from model size
  and quantisation, not measured.
