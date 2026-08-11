# Figure provenance

Paths are relative to
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## Eleven same-card pairs

Every row changes only MTP inside its pair. Throughput is total completion tokens
divided by summed request latency. Accuracy ranges use paired note resampling
with 20,000 replicates.

| pair | off / on throughput | off / on F1 | on minus off, 95% range | acceptance | artifacts |
|---|---:|---:|---:|---:|---|
| Gemma 4 E2B Q4, RX 7900 XTX | 98.56 / 185.79 tok/s | 0.6207 / 0.6246 | +0.0039 [−0.0015, +0.0092] | not retained | `results/10k-{nomtp,sharded}/E2B.UD-Q4_K_XL.10k.{pred.jsonl,score.json}` |
| Gemma 4 E2B Q6, RX 7900 XTX | 90.79 / 170.05 tok/s | 0.6331 / 0.6344 | +0.0013 [−0.0034, +0.0060] | not retained | `results/10k-{nomtp,sharded}/E2B.UD-Q6_K_XL.10k.{pred.jsonl,score.json}` |
| Gemma 4 E2B Q8, RX 7900 XTX | 78.86 / 155.88 tok/s | 0.6351 / 0.6329 | −0.0021 [−0.0073, +0.0031] | not retained | `results/10k-{nomtp,sharded}/E2B.UD-Q8_K_XL.10k.{pred.jsonl,score.json}` |
| Gemma 4 E4B Q4, RX 7900 XTX | 64.10 / 134.07 tok/s | 0.6306 / 0.6301 | −0.0005 [−0.0036, +0.0028] | not retained | `results/10k-{nomtp,sharded}/E4B.UD-Q4_K_XL.10k.{pred.jsonl,score.json}` |
| Gemma 4 E4B Q6, RX 7900 XTX | 52.50 / 113.92 tok/s | 0.6435 / 0.6452 | +0.0017 [−0.0013, +0.0048] | not retained | `results/10k-{nomtp,sharded}/E4B.UD-Q6_K_XL.10k.{pred.jsonl,score.json}` |
| Gemma 4 E4B Q8, RX 7900 XTX | 43.82 / 101.48 tok/s | 0.6327 / 0.6337 | +0.0010 [−0.0021, +0.0041] | not retained | `results/10k-{nomtp,sharded}/E4B.UD-Q8_K_XL.10k.{pred.jsonl,score.json}` |
| Gemma 4 12B UD-QAT Q4, RTX 5080 | 96.33 / 244.73 tok/s | 0.6854 / 0.6932 | +0.0079 [−0.0050, +0.0209] | 80.39% | `results/gemma4-mtp-pairs-20260810/gemma-4-12B-it.qat-UD-Q4_K_XL.5080.mtp-{off,on}.{pred.jsonl,score.json}` |
| Gemma 4 26B-A4B UD-QAT Q4, RTX 5080 | 193.04 / 332.36 tok/s | 0.6833 / 0.6804 | −0.0029 [−0.0215, +0.0159] | 79.21% | `results/gemma4-mtp-pairs-20260810/gemma-4-26B-A4B-it.qat-UD-Q4_K_XL.5080.mtp-{off,on}.{pred.jsonl,score.json}` |
| Gemma 4 31B UD-QAT Q4, RX 7900 XTX | 33.54 / 68.93 tok/s | 0.6898 / 0.6872 | −0.0026 [−0.0110, +0.0055] | 79.09% | `results/gemma4-mtp-pairs-20260810/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.mtp-{off,on}.{pred.jsonl,score.json}` |
| Qwen3.6-27B Q4_K_M, RX 7900 XTX | 34.82 / 81.78 tok/s | 0.7180 / 0.7177 | −0.0003 [−0.0109, +0.0101] | 79.04% | `results/qwen36-mtp-xtx/Qwen3.6-27b.Q4_K_M.xtx.mtp-{off,on}.{pred.jsonl,score.json}` |
| Qwen3.6-35B-A3B Q4_K_M, RX 7900 XTX | 112.97 / 186.78 tok/s | 0.7495 / 0.7427 | −0.0068 [−0.0203, +0.0068] | 76.63% | `results/qwen36-mtp-xtx/Qwen3.6-35b.Q4_K_M.xtx.mtp-{off,on}.{pred.jsonl,score.json}` |

The E2B ranges were recomputed from the stored per-note artifacts on 2026-08-11
with `harness/harness/bootstrap_ci.py`. Full output is in
`results/10k-nomtp/e2b-mtp-paired-ci-20260811.txt`. The other ranges were
already stored or were computed from their complete paired artifacts.

Paired deltas use unrounded counts. The displayed arm scores are rounded
independently, so subtracting the E2B Q8 cells gives −0.0022 instead of the
bootstrap script's −0.0021.

## Muse Glimmer DFlash diagnostic

The off run completed 1,001 notes. The on run was stopped after 22 notes once the
slowdown and low acceptance remained stable. Speed compares those 22 note IDs on
both sides.

| figure | value | artifact |
|---|---:|---|
| DFlash off median generation | 41.39 tok/s | `results/muse-glimmer-30b-xtx-20260810/Muse-Glimmer-30B.K-Quant-17GB.xtx.dflash-off.pred.jsonl`, matched IDs |
| DFlash on median generation | 37.67 tok/s | `results/muse-glimmer-30b-xtx-20260810/Muse-Glimmer-30B.K-Quant-17GB.xtx.dflash-on.pred.jsonl` |
| off / on aggregate throughput | 40.57 / 35.71 tok/s | same files |
| DFlash acceptance | 9,952 / 40,545 = 24.55% | partial on file |
| complete off strict F1 | 0.7100 | `results/muse-glimmer-30b-xtx-20260810/Muse-Glimmer-30B.K-Quant-17GB.xtx.dflash-off.score.json` |

The partial on run is not scored and supports no accuracy claim. Collection and
stop details are in `results/muse-glimmer-30b-xtx-20260810/PARTIAL-2026-08-11.md`.

## Qwen architecture control

These runs compare architecture with MTP off on both sides. They do not supply
the MTP speedup.

| figure | value | artifact |
|---|---:|---|
| Qwen3.6-35B-A3B throughput | 234.0 tok/s | `results/vast/Qwen3.6-35B-A3B.UD-Q4_K_XL.live.pred.jsonl` |
| Qwen3.6-35B-A3B median completion | 1,100 tokens | same file |
| Qwen3.6-27B throughput | 67.8 tok/s | `results/vast/Qwen3.6-27B.UD-Q4_K_XL.live.pred.jsonl` |
| Qwen3.6-27B median completion | 1,256 tokens | same file |
| 35B-A3B minus 27B F1 | −0.0106 [−0.0294, +0.0088] | `harness/harness/bootstrap_ci.py`, paired, seed 42, 20,000 replicates |
| MTP state | off for both | neither prediction file contains `draft_n` |

## Derived from the eleven-pair table

These need no separate artifact. Each is arithmetic on the throughput columns
above, restated here so the derivation is checkable.

| figure | derivation |
|---|---|
| E2B 1.89x / 1.87x / 1.98x at Q4 / Q6 / Q8 | MTP-on tok/s divided by MTP-off tok/s, E2B rows |
| E4B 2.09x / 2.17x / 2.32x at Q4 / Q6 / Q8 | same, E4B rows |
| the two smallest gains are the two mixture-of-experts pairs | 26B-A4B 1.72x and 35B-A3B 1.65x are the minimum two of the eleven ratios |
| acceptance spans 3.8 points against a 1.65x to 2.54x speedup | 80.39% minus 76.63%, against the ratio column |

## Run configuration and guards

| figure | value | source |
|---|---|---|
| llama.cpp build, every RX 7900 XTX run | b10210 | `harness/harness/arm_qwen36_mtp_xtx.sh` and `shard_run.sh` both pin `bin/llama-b10210/llama-server` |
| llama.cpp build, RTX 5080 pairs | not recorded | `arm_gemma4_mtp_pair.sh` calls an unversioned `/opt/llama.cpp/build-cuda/bin/llama-server` |
| llama.cpp build, Glimmer diagnostic | b10356 | `results/muse-glimmer-30b-xtx-20260810/PARTIAL-2026-08-11.md` |
| 1,001-note pairs ran one request at a time | `--concurrency 1` | `arm_gemma4_mtp_pair.sh`, `arm_qwen36_mtp_xtx.sh` |
| 10,000-note E2B and E4B pairs ran three server processes | `-> running 3 processes` | `results/10k-{nomtp,sharded}/shard_*.10k.log` |
| speculation guard on `/slots`, identity guard on `/props`, and the assertion that an MTP-off artifact carries no `draft_n` | run refuses to start or fails on mismatch | `arm_gemma4_mtp_pair.sh` |
| enabling MTP needs `-hf REPO:QUANT` with `-hfd REPO` and no `-md` | an explicit `-md` suppresses sidecar resolution and yields a non-speculative server | `arm_qwen36_mtp_xtx.sh` header, `ARTICLE_NOTES.md` finding 12 |

The `--mtp` flag being registered for the download example only, and the
`libllama.so` symbol grep that missed Gemma 4, are recorded in `ARTICLE_NOTES.md`
findings 12 and 13 against build `b10201-9-g0005475` (2026-07-31). The article
attributes them to that snapshot rather than to b10210.

## Single-sourced diagnostics

Each of these is recorded in one place, with no retained paired artifact. The
article names each as single-sourced at the point of use.

| figure | value | source |
|---|---:|---|
| identical outputs, MTP off then on, 100 notes | 100/100 and 74/100 | `MEASUREMENT_LOG.md`; prediction files not retained |
| MTP against itself, fresh server each run | 100/100 on E4B and on E2B | `ARTICLE_NOTES.md` finding 12 |
| 32 slots against sequential | 4.54x | `ARTICLE_NOTES.md` finding 12 |
| 32 slots with MTP against sequential | 4.34x | same |
| two runs of the same 32-slot configuration | 71 s and 61 s wall, 63/100 raw and 75/100 extracted facts identical | same, and `harness/harness/mtp_speed_matrix_xtx.sh` comments, which record that the 16% timing spread is wider than the 4.54x-to-4.34x gap and retract reporting that gap as a slowdown |
| MTP against sequential on E4B and E2B | 1.83x and 1.59x | `ARTICLE_NOTES.md` finding 12 |
| draft acceptance, QAT against post-hoc quant, Gemma 4 12B | 82.1% against 82.6% | `ARTICLE_NOTES.md` finding 34. The prediction files were deleted during a fleet relaunch before being committed and are not recoverable. Retained here and marked in the article because the question bears on the recommendation, not because the provenance is adequate. |
| Qwen draft head quant cannot be overridden on b10210 | 664 drafted / 377 accepted, byte-identical with and without the override | `harness/harness/arm_qwen36_mtp_xtx.sh` header |

## Named external sources

- Meta's [Muse Glimmer GGUF model card](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF)
  documents the matching drafter, b10353 minimum and reported RTX 5090 speed.
- llama.cpp issue [#25117](https://github.com/ggml-org/llama.cpp/issues/25117)
  reports a DFlash slowdown on AMD hardware.
- llama.cpp issue [#25792](https://github.com/ggml-org/llama.cpp/issues/25792)
  reports low DFlash acceptance under Vulkan.
