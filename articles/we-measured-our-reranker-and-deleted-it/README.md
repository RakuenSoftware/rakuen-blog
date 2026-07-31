# We spent a night measuring our retrieval stack, and deleted the reranker

**Status: draft, unpublished.** Campaign ran 2026-07-26 to 2026-07-30.

The post argues that a benchmark number is only a deployment number if the
consumer reproduces the benchmark's input conditions — and that on a retrieval
stack the dominant failure mode is silent-wrong, not loud-wrong. Everything it
claims is measured, and the measurements are here.

## Where each claim's evidence lives

| the post claims | evidence |
| --- | --- |
| the embedder field and its eliminations | `evidence/embedder-selection-frozen-ab-v1.md` |
| Gemma-4 E2B/E4B and the Ettin reranking controls | `benchmarks/gemma4-unified/ab-v1/README.md` |
| the June rounds that reached different answers | `evidence/embedder-gate-locomo.md`, `evidence/embedder-gate-scifact.md` |
| reranking degrades a dense-ordered list | `evidence/reranker-and-pipeline-2026-07-29.md` |
| the synthesis, and the hybrid BM25+RRF addendum | `evidence/retrieval-stack-report-2026-07-30.md` |
| what was decided and what shipped | `evidence/decision-nomic-cutover-and-reranker-removal.md` |
| the prefix work the decision depended on | `evidence/proposal-embedder-query-document-prefixes.md` |
| where the remaining quality lives | `evidence/retrieval-fusion-and-learning-inventory-2026-07-30.md` |

## The suites, and what is comparable to what

Two things in this folder are easy to misread together. They are not comparable,
and the post says so in its own text.

**The frozen `ab-v1` suite**, manifest SHA-256
`16d2c16add86052ff24be410699ab9452ee1a36252de6dba31ab5391de7ab81c`, 10,000
paired cases. Fixtures in `benchmarks/fixtures/ab-v1/`. Everything in the
late-July block ran against it. Note the two runs used different candidate
pools: the Gemma baselines ranked against 23,688 documents, the Jul 29 embedder
selection against 26,473. Do not take a margin across those.

**The June rounds** (`embedder-gate-*`) are a different suite entirely — LoCoMo
conversational turns, and BEIR plus published MTEB code. Their numbers do not
belong in a table with any late-July figure.

Within the reranker work there is a third trap: Ettin 68M scores 0.607353 on the
ab-v1 reranking view (positive plus 19 fixed BM25 hard negatives) and 0.2969 on
the arbitrary-order view in `reranker-and-pipeline-2026-07-29`. Same model,
different candidate construction.

## Artifact sets

| folder | what it is |
| --- | --- |
| `benchmarks/gemma4-unified/ab-v1/` | the frozen-suite baselines: Gemma-4 E2B/E4B embedding, Ettin 68M/400M reranking. Includes raw append-only logs — select the last row per `case_id` before computing metrics. |
| `benchmarks/fixtures/ab-v1/` | the frozen suite: corpus, plus the embedding and reranking views |
| `benchmarks/reranker-2026-07-29/` | the reranker campaign: config sweeps, GTE ONNX quality, late interaction, hybrid fusion, CPU latency grid |
| `benchmarks/embedder-gate/` | the June rounds: LoCoMo, SciFact, multi-BEIR, and the aimee-own-code task |
| `benchmarks/rank-gate-2026-07-30/` | the fusion follow-on: RRF constant sweep, deltas against production |

## Resolved provenance questions

Two figures were queried during review. Both are settled; recorded here so the
next reader does not re-open them.

**colbert-xm's query cost and storage — withdrawn from the article.** The draft
quoted 3.2 ms per query and 41 GB per million documents, alongside a table of
pipeline quality figures. No artifact in this folder produces any of them, and
the surviving prose disagrees with itself: `retrieval-stack-report-2026-07-30.md`
computes 66 GB/million at fp16 and 33 GB at int8, while the decision record says
42 GB. The colbert-xm pipeline run was never committed. The article now states
the direction was abandoned and declines to quote the numbers, which is the only
position consistent with what it argues everywhere else.

**bge-v2-m3 at 20x512 — not a discrepancy.** `config-sweep-bge.json` records
0.622698 over 3,000 cases. `reranker-and-pipeline-2026-07-29.md` records 0.6174.
These are two different runs at different sample sizes, not two values for one
run. The article's reranker table is the capability view, where 0.6174 is the
correct figure; the config sweep is a separate later run. Both stand.

## Scope: retrieval only

The ab-v1 suite exposes one 10,000-case population through three views —
embedding, reranking, and synthesis. Only the first two are retrieval, and only
those are kept here. The synthesis view and the Gemma-4 12B synthesis results
belong to the Tier-A extraction question, which is a different decision with a
different gold set, and they were removed from this folder rather than left to
imply they informed the embedder choice.
