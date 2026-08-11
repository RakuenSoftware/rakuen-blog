# Figure provenance and reporting record

Paths below are relative to the shared series evidence base at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## Process-count sweeps

| figure | artifact |
|---|---|
| RTX 5080 throughput from one to four processes | `results/mtp-scaling-5080/scale.np*.mtp.pred.jsonl` and run logs |
| RX 7900 XTX throughput from one to four processes | `results/mtp-scaling-xtx/scale.np*.mtp.pred.jsonl` and run logs |
| startup seconds on both cards | `MEASUREMENT_LOG.md`; the sweep computed and discarded the startup column |
| 32-slot throughput and identity | `results/v8-baseline/mtp_np32.log`; `parallel_mtp.log` |

## Model, card and rental measurements

| figure | artifact or record |
|---|---|
| model file and resident-memory sizes | server startup logs under `results/ct140/`, `results/vast/` and `results/llamacpp/`; summary in `ARTICLE_NOTES.md` |
| 26B QAT throughput, 323.1 tok/s | `results/ct140/qat_speed.log` |
| Qwen 35B and 27B throughput | matching prediction files under `results/vast/` |
| rental rates, hours and costs | provider and billing observations in `MEASUREMENT_LOG.md`; raw invoices were not committed |
| fifteen leaked processes and load 27 | host observation in `MEASUREMENT_LOG.md`; no process snapshot retained |
| CUDA card calibration | `MEASUREMENT_LOG.md`, +0.0057 with range −0.0136 to +0.0251 |

## Reporting inventory and disposition

- **CUDA and Vulkan process sweeps:** kept separate. The article does not fit one
  curve across both backends.
- **Startup-time correction:** kept and subtracted from throughput. Exact startup
  seconds are marked single-sourced because the sweep dropped them.
- **Single-server concurrency test:** kept as fast but disqualified for benchmark
  use because it did not reproduce itself.
- **Model-size and active-parameter comparison:** kept as separate memory and speed
  axes.
- **Provider fleet and billing observations:** kept as first-party observations,
  not vendor-independent measurements.
- **Vulkan-to-CUDA accuracy crossing:** remains unmeasured and limits cross-card
  comparisons.
- **Returns above four processes:** remains unmeasured.

There were no interviews. Provider pricing is dated to the recorded campaign and
should not be read as a current market quote.
