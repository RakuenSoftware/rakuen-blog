# Local LLMs: Speculative Decoding

Eleven matched MTP pairs, plus a bounded Muse Glimmer DFlash regression on
Vulkan.

## Status

Publication candidate dated 2026-08-11.

## Evidence

Raw artifacts for the series live under
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`:

| directory | contents |
|---|---|
| `results/10k-sharded/` and `results/10k-nomtp/` | E2B and E4B rows in the eleven-pair experiment |
| `results/gemma4-mtp-pairs-20260810/` | Gemma 12B, 26B and 31B UD-QAT pairs |
| `results/qwen36-mtp-xtx/` | Qwen3.6 27B and 35B pairs |
| `results/muse-glimmer-30b-xtx-20260810/` | complete DFlash-off run and stopped 22-row DFlash-on diagnostic |
| `harness/` | runners, scorer and paired bootstrap script |

`evidence/figures.md` maps each article number to an artifact.
`evidence/paired-ranges-2026-08-11.md` records all eleven paired bootstrap
calculations.

## Reporting record

This article combines first-party measurement with Meta's model card and public
llama.cpp issue reports. The Glimmer DFlash-on run is explicitly partial and
carries no accuracy claim. Only matched on/off pairs support MTP claims.

Four results are carried as single-sourced, each named as such in the article and
listed with its source in `evidence/figures.md`: the 100/74 identical-output
diagnostic, the 32-slot concurrency and repeatability figures, the QAT against
post-hoc acceptance comparison whose prediction files were deleted before commit,
and the Qwen draft-head quant override that b10210 accepts and ignores.

The 32-slot section reports 4.54x against 4.34x without calling the difference a
slowdown. `harness/harness/mtp_speed_matrix_xtx.sh` records that the same
configuration varied by 16% between two runs, which is wider than that gap, and
retracts the earlier slowdown claim. The article states the retraction rather
than repeating the claim.
