# Reporting ledger: matched synthesis model selection

This ledger records the reporting that existed before the 2026-08-14 rewrite,
why the 2026-08-09 draft was replaced, and how each item may be used in the
replacement. Paths are relative to the repository root.

## Prior synthesis reporting

| item | kind | artifact | disposition |
|---|---|---|---|
| Gemma 4 E2B, 10,000 structured synthesis cases | first-party runtime test | `articles/synthesis-model-selection/benchmarks/ab-v1/gemma4_e2b/` | Retain. It supports claims about that measured serving configuration. It does not complete a model-selection matrix. |
| Gemma 4 12B, 10,000 latest structured synthesis cases from 10,013 raw rows | first-party runtime test | `articles/synthesis-model-selection/benchmarks/ab-v1/gemma4_12b/` | Retain. Last-row selection and all superseded attempts remain disclosed. It supports claims about that measured serving configuration. |
| E2B versus 12B paired bootstrap | first-party analysis | `articles/synthesis-model-selection/benchmarks/ab-v1/paired_content_bootstrap.py` and both raw files | Retain as a valid comparison of the two old runs. Do not use it to select among the wider candidates. |
| Frozen 10,000-case silver-label suite | committed fixture and source audit | `articles/synthesis-model-selection/benchmarks/fixtures/ab-v1/` | Retain and reuse. `corpus.jsonl` and `manifest.json`, omitted from the original article bundle, were restored byte-for-byte from the pinned aimee fixture on 2026-08-14. The three hashes are recorded by the new controller. |
| 2026-08-09 two-model draft | unpublished analysis draft | `articles/synthesis-model-selection/article/synthesis-model-selection.md` at commit `1186b6a7593fdf11487a3cee147d076dd3f84630` | Replace before publication. The measurements were real, but the draft excluded relevant candidates because their evidence lived in another article folder. |

## Candidate and serving evidence from the head-to-head reporting

These tests used a different fact-extraction corpus. They justify which models
enter the synthesis matrix and how they are served. They do not determine the
synthesis winner.

| item | kind | artifact | disposition |
|---|---|---|---|
| Nine-candidate accuracy ladder, including Qwen 3.6, Qwen 3.8, Muse Glimmer and five Gemma 4 sizes | first-party runtime tests | `articles/local-llm-fact-extraction-head-to-head/evidence/figures.md`, ranked values table and linked raw artifacts | Use only as candidate-selection evidence. The replacement synthesis result comes from the matched suite below. |
| Gemma 4 and Qwen 3.6 multi-token prediction (MTP) tests | first-party paired runtime tests | `articles/local-llm-fact-extraction-head-to-head/evidence/raw/ARTICLE_NOTES.md` and linked `results/gemma4-mtp-pairs-20260810/` and `results/qwen36-mtp-xtx/` artifacts | Use to set MTP on with one slot. Do not transfer their task accuracy scores into this article's synthesis ranking. |
| Muse Glimmer, 1,001 notes with draft flash (DFlash) off | first-party runtime test | `articles/local-llm-fact-extraction-head-to-head/evidence/raw/results/muse-glimmer-30b-xtx-20260810/` | Use as candidate-selection evidence and to set DFlash off. The 22-note DFlash-on probe is incomplete and must not carry an accuracy claim. |
| Quantisation-aware training (QAT) comparisons for Gemma 4 | first-party paired runtime tests | `articles/local-llm-fact-extraction-head-to-head/evidence/figures.md` and linked QAT artifacts | Use to standardise every scored Gemma target on UD-QAT UD-Q4_K_XL. Auxiliary MTP draft heads remain separate from the scored targets. |
| Gemma 4 UD-QAT UD-Q4_K_XL artifact availability | vendor repository audit | Hugging Face model-tree APIs for the `unsloth/gemma-4-{E2B,E4B,12B,26B-A4B,31B}-it-qat-GGUF` repositories, read 2026-08-14 | All five repositories list a QAT UD-Q4_K_XL scored target and an MTP sidecar. No plain-QAT or Q4_0 fallback is needed. |
| Muse Glimmer reasoning controls | vendor model-card audit | [`meta-models/Muse-Glimmer-30B-GGUF`](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF), read 2026-08-14 | The model card says reasoning cannot be disabled and documents `reasoning_strength=low`. Use that setting, retain its reasoning time, and keep DFlash off as the model-specific serving rule. |

## Replacement matched synthesis matrix

The replacement uses one RX 7900 XTX, one pinned `llama.cpp` binary, one slot,
one worker, one request order, one frozen suite and one scorer. Every scored
Gemma target is UD-QAT UD-Q4_K_XL. Gemma 4 and both Qwen families run with MTP on. Muse
Glimmer runs without a draft model, which keeps DFlash off, and uses the
vendor-supported low reasoning setting. Muse cannot disable reasoning, so its
reasoning tokens and time remain part of the measured request cost.

| candidate | scored target | serving rule | status at ledger creation |
|---|---|---|---|
| Gemma 4 E2B | UD-QAT UD-Q4_K_XL | MTP on | 1,000-case matched run complete |
| Gemma 4 E4B | UD-QAT UD-Q4_K_XL | MTP on | 1,000-case matched run complete |
| Gemma 4 12B | UD-QAT UD-Q4_K_XL | MTP on | 1,000-case matched run complete |
| Gemma 4 26B-A4B | UD-QAT UD-Q4_K_XL | MTP on | 1,000-case matched run complete |
| Gemma 4 31B | UD-QAT UD-Q4_K_XL | MTP on | 1,000-case matched run complete |
| Qwen 3.6 27B | Q4_K_M | MTP on | 1,000-case matched run complete |
| Qwen 3.6 35B-A3B | Q4_K_M | MTP on | 1,000-case matched run complete |
| Qwen 3.8 27B | Q4_K_M | MTP on | 1,000-case matched run complete |
| Muse Glimmer 30B | K-Quant 17 GB | DFlash off; low reasoning | 1,000-case matched run complete |

The publishable matrix uses the same 1,000 cases for every candidate. The
fixture builder orders the full 10,000-case population by SHA-256-derived case
identifier; the retained prefix contains all five task strata. The ten-case
smokes are diagnostics only and do not contribute comparative claims.

The controller is
`articles/synthesis-model-selection/benchmarks/ab-v2/run_candidate_matrix.py`.
All nine canonical outputs are retained under
`evidence/raw/candidate-matrix-20260814/canonical/` without replacing the old
`ab-v1` artifacts. Smoke outputs test the harness and cannot carry published
accuracy or speed claims. An initial E2B QAT Q4_0 smoke was stopped before the
server loaded and before any case ran when UD-QAT was requested. Its state and
log remain separate from the replacement smoke.

The first UD-QAT smoke used the copied runner's generic `grammar` request field.
Seven candidates completed ten diagnostic cases, but Muse Glimmer returned HTTP
500 because llama.cpp treated its JSON plus end token as invalid PEG-native
output. Production aimee instead sends a strict `response_format` JSON schema,
as documented in `src/headers/provider_client.h` and built in
`src/provider_client.c`. The seven grammar-smoke scores cannot carry a result.
The replacement runner uses the production mechanism for every candidate and
starts in a clean result root.

## Completed result and disposition

The first seven configurations completed on August 14. Qwen3.8 then completed
1,000 cases with zero failed latest rows. Muse resumed from the 289 raw rows
saved before interruption and completed the same 1,000-case population with
zero failed latest rows. The saved partial remains under `interrupted/`; the
canonical file preserves the resumed run as a separate artifact.

`evidence/raw/candidate-matrix-20260814/canonical/analysis-20260815.json`
validates all nine model identities, load profiles, case populations and raw
hashes. It records 10,000 paired case-bootstrap replicates with seed 20260815
and NumPy 2.5.0. The analysis supports these dispositions:

- **Default selection:** Gemma 4 12B. The run does not statistically separate
  it from the higher 31B point estimate, while its median latency and post-run
  GPU allocation are lower. This is not an equivalence result.
- **Latency selection:** Gemma 4 E2B. The run does not statistically separate
  it from the other fast configurations, and it has the lowest observed median
  latency and GPU allocation.
- **Qwen3.8 Q4_K_M:** retain. Qwen3.6-27B scores 0.0119 points higher, with a
  paired 95% range from +0.0022 to +0.0216 in Qwen3.6's direction. This does not
  alter the separate fact-extraction tie.
- **Muse Glimmer:** retain. Its valid-object rate does not prevent low
  required-field recall, last-place content score or the longest latency in the
  measured synthesis configuration.
- **Qwen3.8 UD-Q4:** pending. It receives a separate canonical run and cannot
  silently replace the Q4_K_M artifact or row.

## Interviews, criticism and interest

There are no interviews or anonymous sources. The article will compare model
artifacts rather than criticise a person or vendor, so no right-of-reply request
is pending. Rakuen builds aimee and benefits from choosing a workable local
synthesis model; that interest belongs in the article beside the finding.
