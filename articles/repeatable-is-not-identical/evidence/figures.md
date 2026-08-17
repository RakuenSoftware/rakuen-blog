# Figure provenance and reporting record

Paths below are relative to the shared series evidence base at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## Reproduction tests

| figure | artifact |
|---|---|
| 32 slots against sequential, 804/1,001 identical, so 197 changed | `MEASUREMENT_LOG.md`, concurrency test; raw comparison file was not preserved |
| two isolated processes, 60/60 | `MEASUREMENT_LOG.md`, process-isolation test |
| three-process run reproduces 1,001/1,001 three ways | `results/noise-floor/shard3_run1.pred.jsonl`; `shard3_run2.pred.jsonl`; third run recorded in `ARTICLE_NOTES.md` |
| one-process run reproduces 1,001/1,001 | `results/noise-floor/single_run1.pred.jsonl`; `single_run2.pred.jsonl` |
| one against three processes | the four noise-floor files above; scores under the same directory |
| warm against cold, 14/20 | `MEASUREMENT_LOG.md`, warm-server probe |
| cache on against off, 792/1,001 | `results/qat-vs-ud/gemma-4-E2B-it.qat.pred.jsonl`; `results/cache-isolation/E2B.qat.cacheoff.small.pred.jsonl` |
| native against subset, 529/1,001 | `results/qat-vs-ud/` and `results/qat-mid-3k/`; recomputation recorded in `MEASUREMENT_LOG.md` |
| cache-off control, 499/1,001 | `results/cache-isolation/E2B.qat.cacheoff.small.pred.jsonl`; matching `mid` file |
| shuffled sequence, 524/1,001 | `results/cache-isolation/E2B.qat.cacheoff.shuffled.pred.jsonl` |
| cache-off self-reproduction, 1,001/1,001 | `results/cache-isolation/E2B.qat.cacheoff.small.run2.pred.jsonl` |
| CUDA card crossing, 640/1,001 and +0.0057 | `MEASUREMENT_LOG.md`, hardware calibration; source predictions were not retained together |

## Reporting inventory and disposition

- **Process-isolation tests:** kept as distinct configurations, and they carry the
  article's own result.
- **Speculative self-reproduction and shared-slot run-to-run agreement:** cited,
  not reprinted. Both are measured in `speculative-decoding-was-free`, which was
  published after this article was drafted and reports them across eleven pairs.
  Their artifacts remain at `results/v8-baseline/mtp_selfconsistent.log` and
  `results/v8-baseline/mtp_np32.log`.
- **The 197-note concurrency gap:** kept, and distinct from the published
  run-to-run figure. It compares 32 slots against the sequential reference and is
  reported as an upper bound, because slot count and cache reuse moved together.
- **Warm-server and cache tests:** kept. Cache-off cost and accuracy are measured,
  not inferred.
- **Predecessor hypothesis:** refuted and preserved in the article.
- **Prompt-cache-history hypothesis:** refuted and preserved.
- **Sequence-position hypothesis:** confirmed by the seeded-shuffle control.
- **Specific live-state mechanism:** not claimed. The experiment establishes
  sequence position, not which internal state carries it.
- **Long-generation identity and Vulkan-to-CUDA crossing:** left open and stated as
  limits rather than filled with estimates.

No external source or interview carries a material conclusion.
