# Reporting disposition for the 2026-08-02 rewrite

This ledger inventories the first-party reporting in the 2026-07-31 article
before the clarity rewrite. It records where each item went. No raw artifact was
deleted, changed, or replaced.

The rewrite narrows the article to one finding: the reranker made the
dense-ordered production result worse in nearly every tested configuration.
Candidate-pool recall is a separate measured problem and explains the hybrid
retrieval opportunity, not the reranker's negative delta. Measurements cut from
the article remain in their original evidence documents and artifacts.

## Corpus and embedder reporting

| ID | reporting in the 2026-07-31 article | type | disposition |
| --- | --- | --- | --- |
| C1 | Construction and use of frozen-ab-v1: 10,000 queries, one silver positive per query, prose/code/cited categories, manifest hash, and the 23,688 versus 26,473 candidate-pool difference between runs | test design and document review | **Retained in part.** The rewrite keeps the 10,000-query, 26,473-document production-suite facts and the silver-label limit. It cuts the manifest and earlier pool cardinality because no cross-run comparison remains. Full record stays in `README.md`, `evidence/embedder-selection-frozen-ab-v1.md`, and `benchmarks/fixtures/ab-v1/`. |
| C2 | June LoCoMo screen across nomic-v1.5, Qwen3, and bge-base | first-party benchmark | **Cut as a separate decision.** It does not bear on candidate membership. Preserved in `evidence/embedder-gate-locomo.md` and `benchmarks/embedder-gate/`. |
| C3 | June SciFact, NFCorpus, ArguAna, published MTEB code comparison, and aimee-own-code runs | first-party benchmarks plus external-source review | **Cut as a separate decision.** These selected an embedder on a different suite. Preserved in `evidence/embedder-gate-scifact.md` and `benchmarks/embedder-gate/`. |
| C4 | Gemma-4 E2B/E4B embedding controls and Ettin 68M/400M hard-negative controls | first-party benchmarks | **Cut as a separate model-selection history.** Preserved in `benchmarks/gemma4-unified/ab-v1/README.md` and its raw logs. |
| C5 | Late-July full-corpus comparison of nomic-v2-moe, Qwen3-4B, a25m, and Qwen3-0.6B, including category scores, vector width, and GPU throughput | first-party benchmark | **Cut from the article.** The rewrite uses the selected embedders only to show that the pool-recall result reproduced across two dense legs. Full table remains in `evidence/embedder-selection-frozen-ab-v1.md`. |
| C6 | Comparison of Qwen3 publisher code scores with frozen-ab-v1 code results | external-source review plus first-party benchmark | **Cut.** It is a different benchmark-validity argument. The original figures and source trail remain in `evidence/embedder-gate-scifact.md` and `evidence/embedder-selection-frozen-ab-v1.md`. |
| C7 | Inference that old public code benchmarks were present in Qwen3 training data | analysis from benchmark age and score pattern | **Cut.** The campaign did not establish training-set membership directly, so it cannot carry a load-bearing claim in the rewrite. The prior reasoning remains legible in the archived evidence. |
| C8 | bge-family failures by LoCoMo quality, CPU throughput, multi-vector storage, and reranker headroom | first-party benchmarks | **Cut as model-selection detail.** The bge reranker capability result remains where it establishes the benchmark trap. Other results remain in the LoCoMo and reranker reports. |

## Serving and deployment reporting

| ID | reporting in the 2026-07-31 article | type | disposition |
| --- | --- | --- | --- |
| S1 | Source audit showing `last` pooling in serving while nomic required `mean` | static source and model-card audit | **Cut as a separate silent-configuration finding.** Preserved in `evidence/embedder-selection-frozen-ab-v1.md` and the decision record. |
| S2 | Prefix audit and with-prefix versus prefix-free ablation for nomic, Qwen3, and a25m | static source audit plus first-party benchmark | **Cut as a separate deployment-parity finding.** Preserved in `evidence/proposal-embedder-query-document-prefixes.md` and the selection report. |
| S3 | a25m versus nomic CPU throughput, vector width, prefix work, re-embed cost, model maturity, and Q8_0 quality loss | runtime tests, model-card review, and operational analysis | **Cut as embedder-selection detail.** Preserved in `evidence/embedder-selection-frozen-ab-v1.md` and `evidence/retrieval-stack-report-2026-07-30.md`. |
| S4 | Source audit of hardcoded context, query/document polarity, model registry behaviour, and the shipped a25m default; observation that bundling nomic added 1.8 GB | static source audit, build observation, and implementation record | **Cut.** It explains the bundled embedder, not reranker removal. Preserved in `evidence/decision-nomic-cutover-and-reranker-removal.md` and the original implementation history named there. |

## Reranker reporting

| ID | reporting in the 2026-07-31 article | type | disposition |
| --- | --- | --- | --- |
| R1 | Model-card and licence audit of Ettin, GTE, bge-v2-m3, bge-m3, and colbert-xm | external document review | **Cut except for model identity.** The rewrite does not make multilingual coverage or licence the reason for removal. Full audit remains in `evidence/reranker-and-pipeline-2026-07-29.md`. |
| R2 | CPU latency grids for GTE and bge-v2-m3, including the corrected 10x feasibility estimate and superlinear token cost | runtime tests | **Cut.** Latency did not decide the article once usefulness was near zero. Preserved in the reranker report and `benchmarks/reranker-2026-07-29/cpu-rerank-latency-grid.json`. |
| R3 | Arbitrary-order capability view: no rerank, Ettin, bge-v2-m3, and GTE | first-party benchmarks | **Retained in part.** The matched 10,000-case no-rerank, Ettin, and bge rows remain to give the strongest case for reranking. GTE's 1,000-case row is cut to avoid mixing sample sizes in the table. |
| R4 | Invalid GTE torch run that returned constant scores | failed runtime test and validation observation | **Cut from the article, retained as a warning in the reporting record.** It remains marked invalid in `evidence/reranker-and-pipeline-2026-07-29.md`; only ONNX results carry published claims. |
| R5 | Dense-ordered bge pipeline tests over 2,000 queries at 128, 256, and 512 document tokens | first-party end-to-end benchmarks | **Cut from the main argument after serving as corroboration.** They show degradation but the later GTE full-suite sweep is closer to the final decision. Preserved in the reranker and retrieval-stack reports. |
| R6 | GTE dense-ordered 600-query run, including +0.020 for a25m at 20x512 and compression of the nomic/a25m gap | first-party end-to-end benchmark | **Retained only as the contrary subsample.** The rewrite keeps +0.020 because it damages the case and explains why the 10,000-query run was necessary. The embedder-gap analysis is cut. Raw summary remains in `benchmarks/reranker-2026-07-29/gte-pipeline-dense-ordered.json`. |
| R7 | Full-suite GTE depth sweep and the campaign summary of twenty configurations over two embedders, with a best result of +0.0032 NDCG@10 | first-party end-to-end benchmark summary | **Retained and made central.** Provenance is limited: the decision record carries the figures, but the underlying depth-sweep raw artifact is not committed separately. The article states that limit next to the table. |
| R8 | 600-query +0.020 result versus 10,000-query −0.0048 result at depth 20 | comparison of first-party benchmarks | **Retained.** The sign flip is the reason the small run does not carry the decision. |
| R9 | bge-m3 late-interaction quality, query/index time, and 743 GB per million-document storage measurement | first-party benchmark and storage observation | **Cut as a separate architecture investigation.** Preserved in `benchmarks/reranker-2026-07-29/late-interaction-bge-m3.json` and the retrieval-stack report. |
| R10 | colbert-xm storage arithmetic and abandoned pipeline direction | calculation plus incomplete first-party test | **Cut.** The pipeline numbers remain unpublished because no committed artifact produces them and surviving notes disagree. The disposition remains recorded in the article `README.md`. |
| R11 | Cascade and RRF-fusion combinations of the cross-encoder and late-interaction rerankers | first-party hybrid reranking tests | **Retained qualitatively and made load-bearing.** Every combined variant was negative, which rules against a single-model or single-configuration explanation. No separate raw artifact survives and colbert-xm notes disagree on the deltas, so the rewrite publishes the consistent sign but no numeric result. The decision record is the surviving source. |

## Hybrid retrieval and implementation reporting

| ID | reporting in the 2026-07-31 article | type | disposition |
| --- | --- | --- | --- |
| H1 | Full-corpus dense, BM25, and BM25+RRF comparison for a25m and nomic | first-party end-to-end benchmark | **Retained and narrowed to the matched nomic configuration.** This supplies the alternative investment and the +0.0262 NDCG@10 / +0.0662 Recall@10 comparison. It is not used to explain the reranker's negative delta. |
| H2 | Dense top-50 versus dense-union-BM25 top-50 pool recall for both embedders | first-party candidate-membership measurement | **Retained as a separate constraint.** It explains why a second retriever had room to help, not why reranking worsened the documents it received. |
| H3 | Prediction recorded before the hybrid run that a recall ceiling should move Recall@10 more than NDCG@10 | pre-registered analysis plus first-party benchmark | **Retained through the matched metric comparison, without making the prediction itself part of the narrative.** Full chronology remains in `evidence/retrieval-stack-report-2026-07-30.md`. |
| H4 | RRF `k=10` versus `k=60`, the Recall@1 tradeoff, and the tiered variant | first-party parameter sweep | **Retained with limits.** The rewrite says `k=10` has no NDCG@10 measurement and keeps the tiered replacement because criticism must specify what stands in place of plain RRF. Raw values remain in `benchmarks/reranker-2026-07-29/fusion-frontier-nomic.json`. |
| H5 | Source audit showing lexical retrieval and RRF already existed, plus the inventory of fusion, ranking, and learning machinery | static source audit | **Retained only as the fact that the replacement used existing infrastructure.** The wider LTR and bandit inventory is outside this article and remains in `evidence/retrieval-fusion-and-learning-inventory-2026-07-30.md`. |
| H6 | Reranker removal on serving and KB sides, including removal of the model, score head, conversion/release workflow, endpoint, and call sites | implementation observation and commit review | **Retained as consequence.** Commit identifiers and file-level detail remain in the decision record. |

## Corrections and silent-failure observations

| ID | reporting in the 2026-07-31 article | type | disposition |
| --- | --- | --- | --- |
| F1 | Six corrected claims: CPU feasibility, late-interaction speedup, storage estimate, linear latency, truncation advice, and uniform-dimension benefit | corrections to runtime tests, calculations, and analysis | **Cut as a competing article spine.** Each correction remains in the relevant evidence document. None is used silently in the rewrite. |
| F2 | Silent-wrong observations: pooling, prefixes, `-ngl 0` auto-fit, `-np 4` context division, ONNX provider fallback, and constant reranker scores | runtime observations and static source audit | **Cut as a competing article spine.** The rewrite uses only verified results produced after those failures were detected. The observations remain in the selection, reranker, and decision records. |
| F3 | nomic's 0.6058, 0.6072, and 0.6075 run-to-run values and the handoff that mixed them in one delta | source audit of first-party notes | **Cut from prose.** The rewrite uses 0.6075 only inside the exact `hybrid-nomic.json` run and does not compute across runs. |

## Publication check

- **Raw artifacts:** unchanged. No file under `benchmarks/` was edited.
- **Interviews:** none appeared in the original article.
- **Material criticism:** the rewrite criticises Rakuen's own measurement and
  system design. Vendor-specific benchmark criticism was removed.
- **Uncommitted result:** the 10,000-query reranker depth sweep remains sourced
  to the first-party decision record and is labelled as lacking a separate raw
  artifact.
- **Scope:** all retained numbers describe this corpus and suite. The finding is
  that these rerankers generally worsened this production path, not that
  rerankers are invalid when the labelled document is absent.
