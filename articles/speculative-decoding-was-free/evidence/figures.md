# Figure provenance

Paths are relative to
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## Five completed same-card pairs

Throughput is total completion tokens divided by summed request latency. Draft
acceptance is accepted tokens divided by proposed tokens. Accuracy ranges use
paired note resampling, seed 42 and 20,000 replicates.

| pair | off / on throughput | off / on F1 | on minus off, 95% range | acceptance | artifacts |
|---|---:|---:|---:|---:|---|
| Gemma 4 12B UD-QAT Q4, RTX 5080 | 96.33 / 244.73 tok/s | 0.6854 / 0.6932 | +0.0079 [−0.0050, +0.0209] | 80.39% | `results/gemma4-mtp-pairs-20260810/gemma-4-12B-it.qat-UD-Q4_K_XL.5080.mtp-{off,on}.{pred.jsonl,score.json}` |
| Gemma 4 26B-A4B UD-QAT Q4, RTX 5080 | 193.04 / 332.36 tok/s | 0.6833 / 0.6804 | −0.0029 [−0.0215, +0.0159] | 79.21% | `results/gemma4-mtp-pairs-20260810/gemma-4-26B-A4B-it.qat-UD-Q4_K_XL.5080.mtp-{off,on}.{pred.jsonl,score.json}` |
| Gemma 4 31B UD-QAT Q4, RX 7900 XTX | 33.54 / 68.93 tok/s | 0.6898 / 0.6872 | −0.0026 [−0.0110, +0.0055] | 79.09% | `results/gemma4-mtp-pairs-20260810/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.mtp-{off,on}.{pred.jsonl,score.json}` |
| Qwen3.6-27B Q4_K_M, RX 7900 XTX | 34.82 / 81.78 tok/s | 0.7180 / 0.7177 | −0.0003 [−0.0109, +0.0101] | 79.04% | `results/qwen36-mtp-xtx/Qwen3.6-27b.Q4_K_M.xtx.mtp-{off,on}.{pred.jsonl,score.json}` |
| Qwen3.6-35B-A3B Q4_K_M, RX 7900 XTX | 112.97 / 186.78 tok/s | 0.7495 / 0.7427 | −0.0068 [−0.0203, +0.0068] | 76.63% | `results/qwen36-mtp-xtx/Qwen3.6-35b.Q4_K_M.xtx.mtp-{off,on}.{pred.jsonl,score.json}` |

The four new ranges were recomputed on 2026-08-11 with
`harness/harness/bootstrap_ci.py` and recorded in
`paired-ranges-2026-08-11.md`. The Qwen3.6-27B range was already banked.

## Six earlier 10,000-note Gemma pairs

| pair | MTP on / off F1 | throughput gain | artifacts |
|---|---:|---:|---|
| E2B Q4 | 0.6246 / 0.6207 | 1.84x | `results/10k-{sharded,nomtp}/E2B.UD-Q4_K_XL.10k.{pred.jsonl,score.json}` |
| E2B Q6 | 0.6344 / 0.6331 | 1.92x | `results/10k-{sharded,nomtp}/E2B.UD-Q6_K_XL.10k.{pred.jsonl,score.json}` |
| E2B Q8 | 0.6329 / 0.6351 | 2.03x | `results/10k-{sharded,nomtp}/E2B.UD-Q8_K_XL.10k.{pred.jsonl,score.json}` |
| E4B Q4 | 0.6301 / 0.6306 | 2.11x | `results/10k-{sharded,nomtp}/E4B.UD-Q4_K_XL.10k.{pred.jsonl,score.json}` |
| E4B Q6 | 0.6452 / 0.6435 | 2.16x | `results/10k-{sharded,nomtp}/E4B.UD-Q6_K_XL.10k.{pred.jsonl,score.json}` |
| E4B Q8 | 0.6337 / 0.6327 | 2.31x | `results/10k-{sharded,nomtp}/E4B.UD-Q8_K_XL.10k.{pred.jsonl,score.json}` |

The paired ranges published for E4B Q4, Q6 and Q8 all cross zero. The E2B pairs
carry point estimates only and are not used to claim an accuracy tie by
themselves.

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

## Single-sourced historical checks

- The 100/100 MTP-off and 74/100 MTP-on identical-output counts are recorded in
  `MEASUREMENT_LOG.md`; their prediction files were not retained.
- The invalid 5.3x and 1.58x claims are documented with their causes in
  `MEASUREMENT_LOG.md` and the run logs. They remain in the article as marked
  corrections, not measurements to reuse.

## Named external sources

- Meta's [Muse Glimmer GGUF model card](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF)
  documents the matching drafter, b10353 minimum and reported RTX 5090 speed.
- llama.cpp issue [#25117](https://github.com/ggml-org/llama.cpp/issues/25117)
  reports a DFlash slowdown on AMD hardware.
- llama.cpp issue [#25792](https://github.com/ggml-org/llama.cpp/issues/25792)
  reports low DFlash acceptance under Vulkan.
