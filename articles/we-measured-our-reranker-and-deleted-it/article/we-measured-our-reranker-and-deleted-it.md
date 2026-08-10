---
title: "Our reranker made production retrieval worse"
date: 2026-07-31
author: Rakuen Software
tags: [retrieval, embeddings, benchmarks, aimee]
excerpt: "The reranker looked strong on an arbitrary candidate list, then degraded production output across direct, cascade, and fused configurations."
---

*Rewritten 2026-08-02. Rakuen builds aimee, the system
measured here. Every figure traces to the
[evidence repository](https://github.com/RakuenSoftware/rakuen-blog/tree/main/articles/we-measured-our-reranker-and-deleted-it).*

Our reranker looked good when we asked it to sort an arbitrary candidate list.
It made the result worse in nearly every configuration when we put it behind
production retrieval. Across twenty configurations and two embedders, only one
beat dense retrieval, by **+0.0032 NDCG@10**. Cascade and RRF-fusion
combinations were negative too. We deleted the reranker.

The benchmark had measured whether the model could sort a list with no useful
order. Production asked it to improve a list the dense retriever had already
ordered. Our reranker could do the first job and generally failed the second.

We found a separate problem while looking for the remaining quality. Dense
retrieval omitted the labelled document from its top 50 for **11-13%** of
queries. That does not invalidate the reranker result. It explains why adding a
second retrieval leg produced a larger gain than reordering the first leg's
output.

This is not a general finding about rerankers. It comes from one 10,000-query
suite over our 26,473-document corpus, with one silver-labelled document per
query. The queries may have been derived from the documents in a way that
favours lexical retrieval. The finding is narrower: on this corpus, the tested
rerankers generally degraded the dense-ordered production result.

## The first benchmark measured capability, not usefulness

A retriever chooses the candidate pool. A reranker receives that fixed pool and
changes its order. It can promote a document the retriever ranked badly, but it
cannot introduce a document the retriever never returned.

Our first reranking view contained twenty candidates in arbitrary order. On
10,000 cases, the multilingual bge reranker looked transformative:

| system | NDCG@10 |
| --- | ---: |
| arbitrary candidate order | 0.2279 |
| + incumbent Ettin reranker | 0.2969 |
| + bge-reranker-v2-m3 | **0.6174** |

*Source: [reranker selection and pipeline report](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/we-measured-our-reranker-and-deleted-it/evidence/reranker-and-pipeline-2026-07-29.md), capability view.*

That result is real. It is also the strong case for keeping a reranker: given a
list with no useful order, the model supplied one.

Production does not supply an arbitrary list. Dense retrieval supplies an
already ranked list. The production test must show that the reranker can beat
the ordering the embedder already produced.

## The production test erased the win

We ran the stronger GTE reranker after dense retrieval over the full suite. At
depths 10 and 20 it made the ranking worse. At depth 50 it produced the only
positive result in the twenty-configuration campaign:

| pipeline | NDCG@10 | change from dense |
| --- | ---: | ---: |
| dense only | **0.5909** |  |
| + GTE at depth 10 | 0.5803 | −0.0106 |
| + GTE at depth 20 | 0.5861 | −0.0048 |
| + GTE at depth 50 | 0.5942 | **+0.0032** |

*Source: [reranker removal decision record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/we-measured-our-reranker-and-deleted-it/evidence/decision-nomic-cutover-and-reranker-removal.md), which summarises the 10,000-query campaign. The underlying depth sweep was not committed as a separate raw artifact.*

The smaller run had argued against this conclusion. On 600 queries, GTE at
depth 20 improved NDCG@10 by **+0.020**. On all 10,000, the same depth measured
**−0.0048**. The result changed sign, which is why the full run, not the
subsample, carries the decision.

This does not show that rerankers are useless. It shows that ours usually
damaged the order the dense retriever produced, while adding a second model,
another serving path, and query-time latency. Its impressive benchmark result
came from restoring order to a list that production never generated.

## Hybrid reranking isolated the reranker

One failed configuration would have indicted the configuration. We changed the
embedder and the reranker, then swept candidate depth and document length. We
also cascaded the cross-encoder with a late-interaction reranker and fused their
rankings with RRF. Every combined variant made the production result worse.

That closed the obvious escape hatch. If one reranker were merely mismatched to
the embedder, replacing it or combining it with a second ranking signal could
have recovered the loss. Neither did. The rerankers could sort arbitrary
candidates, but adding their judgement after production retrieval degraded the
end-to-end order.

*Source: [reranker removal decision record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/we-measured-our-reranker-and-deleted-it/evidence/decision-nomic-cutover-and-reranker-removal.md). The combined runs were not committed as separate raw artifacts. Surviving colbert-xm notes disagree on the numeric deltas, so only their consistently negative sign carries into this article.*

At that point the reranker was not merely failing to solve some other retrieval
problem. In this stack, it was the source of the regression.

## Missing candidates were a separate problem

The dense retriever's top 50 contained the labelled document for **88.99%** of
queries with nomic and **87.35%** with a25m. For the rest, the reranker could not
promote the labelled document because it was outside the reranker's input.

BM25 failed on different queries. Taking the union of the dense and BM25 top 50
raised candidate-pool recall to **97.39%** with nomic and **97.35%** with a25m:

| candidate pool | nomic | a25m |
| --- | ---: | ---: |
| dense top 50 | 0.8899 | 0.8735 |
| dense ∪ BM25 top 50 | **0.9739** | **0.9735** |

*Source: [hybrid retrieval addendum](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/we-measured-our-reranker-and-deleted-it/evidence/retrieval-stack-report-2026-07-30.md) and the [nomic raw result](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/we-measured-our-reranker-and-deleted-it/benchmarks/reranker-2026-07-29/hybrid-nomic.json).*

This was not the cause of the reranker's negative production delta. A reranker
can still improve the order of the documents it receives. Ours generally did
not. Candidate-pool recall identified another place the stack was losing
quality, and a second retriever could act on it.

## Hybrid retrieval changed the pool

We fused BM25 and dense retrieval with Reciprocal Rank Fusion. On the same
10,000 queries and 26,473 documents, hybrid retrieval improved both order and
membership:

| pipeline | NDCG@10 | Recall@10 |
| --- | ---: | ---: |
| nomic dense | 0.6075 | 0.8006 |
| BM25 | 0.6213 | 0.8470 |
| nomic + BM25, RRF `k=60` | **0.6337** | **0.8668** |

*Source: [hybrid-nomic.json](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/we-measured-our-reranker-and-deleted-it/benchmarks/reranker-2026-07-29/hybrid-nomic.json).*

The matched hybrid result gained **+0.0262 NDCG@10** and **+0.0662 Recall@10**
over dense retrieval. Its NDCG gain was 8.2 times the best reranker result, and
the recall gain was something a reranker could not produce. These are different
operations, not interchangeable tests. The comparison shows where the next
unit of retrieval work paid on this corpus.

The BM25 result carries a caveat. These queries resemble document
summaries with key terms attached, which may flatter lexical matching. I do not
take BM25 beating dense retrieval here as a general result. I do take the pool
comparison as evidence that the two retrievers missed different documents on
this corpus.

RRF brought its own cost. At `k=60`, Recall@1 fell from **0.3875** to **0.3699**
because rank fusion discards score magnitude. A `tiered` variant left dense
retrieval in first place, preserving Recall@1 by construction, while raising
Recall@10 from **0.8006** to **0.8742**. The safer replacement is not free, but
its tradeoff is visible.

The usual RRF constant was not best here either. `k=10` matched or beat `k=60`
at every recorded recall depth and raised Recall@10 to **0.9034**. We did not
measure NDCG@10 for that variant, so I will not pair its recall gain with the
`k=60` NDCG gain.

## We removed the component that made the result worse

Deleting the reranker removed its model, score-head artifact, conversion and
release workflow, API endpoint, and query-time call. It also made CPU and GPU
tiers return the same ordering. The retrieval system became smaller because the
measurement showed where the quality did not live.

The embedder campaign produced useful findings about pooling, prefixes, and
serving cost. They are recorded in the evidence repository, but they are not the
reason we deleted the reranker. We deleted it because the production
measurement was negative in nearly every case.

Measure reranking on the path that will ship:

1. **Test the ordered production path.** Preserve the actual truncation,
   candidate depth, latency budget, and input order.
2. **Use arbitrary order as a diagnostic.** It shows whether a model can rank,
   not whether it can improve the deployed retriever.
3. **Measure candidate membership separately.** Pool recall identifies losses
   no reranker gets a chance to repair.
4. **Keep reranking only when it wins in production.** A reranker that sorts an
   arbitrary list but cannot beat the deployed retriever is benchmark quality,
   not retrieval quality.
