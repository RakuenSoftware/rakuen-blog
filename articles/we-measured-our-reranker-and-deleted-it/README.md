# Our reranker made production retrieval worse

**Published 2026-07-31** at <https://rakuensoftware.com>. Campaign ran 2026-07-26 to 2026-07-30.

The post reports that the reranker made the dense-ordered production result
worse in nearly every tested configuration. Candidate membership was a separate
problem: dense retrieval omitted the labelled document from its top 50 for
11-13% of queries, and a second retrieval leg changed that pool.

## Where each claim's evidence lives

| the post claims | evidence |
| --- | --- |
| arbitrary-order reranker capability | `evidence/reranker-and-pipeline-2026-07-29.md` |
| the full-suite reranker decision and removal | `evidence/decision-nomic-cutover-and-reranker-removal.md` |
| negative cascade and RRF-fusion reranking results | `evidence/decision-nomic-cutover-and-reranker-removal.md`, with the raw-artifact limit stated in the article |
| candidate-pool recall and hybrid BM25+RRF | `evidence/retrieval-stack-report-2026-07-30.md`, `benchmarks/reranker-2026-07-29/hybrid-nomic.json` |
| RRF constant and tiered-variant results | `benchmarks/reranker-2026-07-29/fusion-frontier-nomic.json` |
| every first-party result cut or retained by the rewrite | `evidence/rewrite-disposition-2026-08-02.md` |

The embedder-selection, serving-parity, late-interaction, and silent-failure
reporting remains in this folder. The rewrite ledger records why it no longer
appears in the article.

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
42 GB. The colbert-xm pipeline run was never committed. The rewrite removes the
digression; the reporting ledger preserves the disposition.

**bge-v2-m3 at 20x512 — not a discrepancy.** `config-sweep-bge.json` records
0.622698 over 3,000 cases. `reranker-and-pipeline-2026-07-29.md` records 0.6174.
These are two different runs at different sample sizes, not two values for one
run. The article's reranker table is the capability view, where 0.6174 is the
correct figure; the config sweep is a separate later run. Both stand.

**The 10,000-query GTE depth sweep is document-sourced.** The decision record
reports 0.5803 at depth 10, 0.5861 at depth 20, and 0.5942 at depth 50 against a
0.5909 dense baseline. No separate raw artifact for that sweep is committed in
this folder. The article retains the result because it carried the production
decision and states the provenance limit next to the table.

## Scope: retrieval only

The ab-v1 suite exposes one 10,000-case population through three views —
embedding, reranking, and synthesis. Only the first two are retrieval, and only
those are kept here. The synthesis view and the Gemma-4 12B synthesis results
belong to the Tier-A extraction question, which is a different decision with a
different gold set, and they were removed from this folder rather than left to
imply they informed the embedder choice.
