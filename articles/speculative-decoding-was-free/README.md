# Local LLMs: Speculative Decoding

Eleven matched MTP pairs, plus a bounded Muse Glimmer DFlash regression on
Vulkan.

## Status

Republished 2026-08-11 after the missing Gemma 12B, 26B and 31B pairs and the
Qwen3.6-35B-A3B pair completed. The article was withdrawn on 2026-08-10 because
the larger Gemma results lacked same-condition MTP-off partners.

## Evidence

Raw artifacts for the series live under
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`:

| directory | contents |
|---|---|
| `results/10k-sharded/` and `results/10k-nomtp/` | six earlier 10,000-note Gemma pairs |
| `results/gemma4-mtp-pairs-20260810/` | Gemma 12B, 26B and 31B UD-QAT pairs |
| `results/qwen36-mtp-xtx/` | Qwen3.6 27B and 35B pairs |
| `results/muse-glimmer-30b-xtx-20260810/` | complete DFlash-off run and stopped 22-row DFlash-on diagnostic |
| `harness/` | runners, scorer and paired bootstrap script |

`evidence/figures.md` maps each published number to an artifact.
`evidence/rewrite-disposition-2026-08-11.md` records what the rewrite kept,
cut or narrowed. `evidence/paired-ranges-2026-08-11.md` records the four new
paired bootstrap calculations.

## Reporting record

This article combines first-party measurement with Meta's model card and public
llama.cpp issue reports. The Glimmer DFlash run is explicitly partial and carries
no accuracy claim. Prior invalid speedups remain visible in the article and raw
logs.
