# We measured the wrong part of retrieval, then deleted the reranker

*2026-07-31. Every figure here traces to a document or artifact in the
[evidence repository](https://github.com/RakuenSoftware/rakuen-blog/tree/main/articles/we-measured-our-reranker-and-deleted-it): the validation writeups under
[`evidence/`](https://github.com/RakuenSoftware/rakuen-blog/tree/main/articles/we-measured-our-reranker-and-deleted-it/evidence), the raw result artifacts under
[`benchmarks/`](https://github.com/RakuenSoftware/rakuen-blog/tree/main/articles/we-measured-our-reranker-and-deleted-it/benchmarks), and the frozen suite itself under
[`benchmarks/fixtures/ab-v1/`](https://github.com/RakuenSoftware/rakuen-blog/tree/main/articles/we-measured-our-reranker-and-deleted-it/benchmarks/fixtures/ab-v1). Run your own
model against it and check the numbers.*

The number I was watching was reranker quality. The constraint was candidate
membership.

Dense retrieval missed the labelled document entirely for **11-13%** of queries,
which meant no reranker could recover it, and across **twenty** reranking
configurations the best reranker bought **+0.0032 NDCG@10** because it was
reordering a pool whose problem was what it contained.

So we deleted the reranker.

What stands in its place is not a better cross-encoder. It is hybrid retrieval:
BM25 fused with the dense leg by Reciprocal Rank Fusion, with `k=10` beating the
textbook `k=60` on every metric, and a `tiered` variant that has **zero** top-1
regression by construction.

This is the shape of the work: the embedder choice, the benchmark trap, the
reranker trap, the replacement, and the thing that shipped.

This is not a general law of retrieval. It is one corpus, silver labels, one
positive per query, and queries that may be lexically derived from their
documents, which flatters BM25. Speaking from this corpus, the first question is
not whether the retrieved list is in the right order, it is whether the right
document is in the list at all.

## The corpus made candidate membership the binding constraint

Our KB does dense retrieval over ~26k documents, then reranked the top
candidates with a cross-encoder before answering.

I had a new evaluation suite: 10,000 queries against the full corpus, built from
our own content, with prose, code, and cited artifacts.

The plan was to pick an embedder and move on.

The plan was wrong.

## The embedder field did not stay ordered

The shortlist took three rounds across two suites.

June explains the starting point. LoCoMo ranked nomic-v1.5 above Qwen3, and I
later marked that screen as under-discriminating and superseded. The June
BEIR-plus-code round leaned on published MTEB code scores and dropped nomic for
the Qwen3 ladder, but that dropped model was nomic-embed-text-v1.5: text-only,
no code training. It was not nomic-embed-text-v2-moe, the retrieval-trained
model that won on code in July.

Those June rounds used different suites, so they are not comparable to July. The
late-July campaign is the comparable block: 2026-07-26 through 2026-07-30,
frozen-ab-v1, manifest SHA-256
`16d2c16add86052ff24be410699ab9452ee1a36252de6dba31ab5391de7ab81c`, 10,000
paired cases over the same corpus. Jul 30 closed it with the full-length GTE
pipeline result and the hybrid BM25+RRF work.

Jul 26-28 started with the ab-v1 baselines, where I tested the Gemma-4
unified-base idea as configured.

It was not close.

| model | width | NDCG@10 | MRR@10 | R@10 | vectors/s |
| --- | ---: | ---: | ---: | ---: | ---: |
| Gemma 4 E2B | 1,536 | 0.362803 | 0.269053 | 0.6735 | 5.4347 |
| Gemma 4 E4B | 2,560 | 0.422186 | 0.328657 | 0.7275 | 2.2839 |

*Source: ab-v1 results README, Gemma 4 E2B/E4B embedding summaries.*

These are their own result: same manifest, 10,000 cases, ranked against
**23,688** candidate documents. The Jul 29 selection run ranked against
**26,473** documents, so I do not take a numeric margin between the two,
although the Gemma result was still far short of the field I needed to choose
from.

The E2B run was a stock untrained instruction checkpoint, a pre-training control
rather than evidence that Gemma-4 was ready to replace the supported embedder.
This eliminated the unified-base idea as I had configured it. It did not prove
that Gemma-4 can never embed.

The same ab-v1 block also ran the incumbent-family reranking controls, on the
ab-v1 reranking view: Ettin 68M at **0.607353** NDCG@10, and Ettin 400M at
0.643879. That view is the positive plus 19 fixed BM25 hard negatives. Do not
mix those numbers with the arbitrary-order reranking view used later in this
post. Different negatives. Different difficulty. Different scale.

*Source: ab-v1 results README, completed reranking controls.*

Jul 29 was the embedder selection run: same frozen suite, all 26,473 corpus
documents, each model at its best, card prefix, native pooling, full corpus.

| model | NDCG@10 | R@10 | dim | code | prose | cited | GPU vec/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| nomic-embed-text-v2-moe | **0.6072** | 0.8007 | 768 | **0.8104** | 0.5157 | 0.6344 | 82.7 |
| Qwen3-Embedding-4B | 0.6061 | **0.8100** | 2560 | 0.7394 | **0.5274** | 0.6988 | 26.4 |
| bekko-embedding-v1-a25m | 0.5909 | 0.7816 | 384 | 0.7718 | 0.4841 | **0.7170** | **510.7** |
| Qwen3-Embedding-0.6B | 0.5810 | 0.7765 | 1024 | 0.7325 | 0.4930 | 0.6804 | 113.1 |

*Source: `embedder-selection-frozen-ab-v1`, "Results, every model at its best".*

Qwen3 was out on this corpus. The 0.6B model was the weakest finalist, while the
4B model tied nomic, cost 3.3x the vector storage, embedded 3.1x slower, and
topped out at parity with a 475M model.

## Qwen3's public scores are real scores on the wrong condition

Qwen3's publishers are not lying about their code figures. Their reported code
retrieval numbers are near-perfect, and the same family also reproduced our
harness on SciFact and NFCorpus.

That is the strong case for Qwen3.

It still did not survive our corpus.

Every query a deployed model answers is data it has never seen. A production
retrieval model sees documents outside its training set, and if it only works on
material it has absorbed, it fails the moment you point it at your corpus.

A benchmark measures that condition only when the model could not have trained
on it. Otherwise it scores a situation production does not use.

Novelty is the requirement, not secrecy. frozen-ab-v1 did not exist when these
models were trained, so a score on it measures capability rather than recall,
and nothing is withheld because the data is newer than the weights.

The suite ships with this article: corpus, all views, manifest hashes. A
measurement nobody can reproduce is not evidence, and hiding the data would buy
nothing the timing has not already bought.

Publication changes the next generation. Once the suite is public, it can enter
a future training set, so a model trained after today tells you nothing by
scoring well on it. That is the lifecycle of every benchmark. Ours is now in it.

That lifecycle already ran to completion on the public code benchmarks.
CodeSearchNet and its relatives have been public for years, with every incentive
pointing at topping them, so a near-perfect score on a benchmark that old tells
you the model has seen it. It cannot tell you anything about unseen code. This
is not a claim about one vendor. It is what happens to any benchmark that
predates the models being scored on it.

The harness is durable; the data is the consumable. The builder, scoring,
validation records, and acceptance checks are reusable, so point them at content
created since the last model generation, publish that too, then cut the next
sample.

Qwen3's publishers report near-perfect code retrieval on MTEB:

| task | 0.6B | 4B | 8B |
| --- | ---: | ---: | ---: |
| CodeSearchNet | 0.943 | 0.960 | 0.966 |
| CodeSearchNet-CC | 0.933 | 0.967 | 0.971 |
| StackOverflowQA | 0.900 | 0.943 | 0.948 |
| CodeFeedback-MT | 0.908 | 0.932 | 0.937 |

Those are the publishers' figures, not mine.

Then I put the same family on code it could not have trained on when I measured:

| model | dim | code |
| --- | ---: | ---: |
| nomic-embed-text-v2-moe | 768 | **0.8104** |
| bekko-embedding-v1-a25m | 384 | **0.7718** |
| Qwen3-Embedding-4B | 2,560 | **0.7394** |
| Qwen3-Embedding-0.6B | 1,024 | **0.7325** |

*Source: `embedder-selection-frozen-ab-v1`, code category of the selection run.*

Both Qwen3 models came last, behind nomic-v2-moe and behind bekko-a25m: a
384-dimension model, ten days old at the time, with no published baselines of
any kind.

I did not run Qwen3-8B on frozen-ab-v1. I did not need it to see the failure
shape.

On this corpus, a model that publishes near-perfect code retrieval and then
places last on unseen code has not demonstrated code retrieval for our use.
Whatever the mechanism, the published number did not survive contact with unseen
data. It describes the benchmark, not this deployment.

The broader rule is narrower than it sounds: every figure a model publishes is
measured on a test set the publisher chose and could have trained on, while the
only figure that tells you what a model will do on your data is one measured on
your data.

Measure on data that postdates the weights. Publish it, so the measurement can
be checked. Cut the next sample against the next generation. Keep the harness.
Keep making data.

This is the same lesson as the prefix trap, on a different axis. There, a
benchmark number stopped being a deployment number because the serving path did
not reproduce the benchmark's input conditions; here, it stops being one because
the benchmark does not reproduce deployment's data condition: material the model
has never seen.

bge lost differently each time:

- bge-base-en-v1.5 went out with the June LoCoMo screen.
- bge-m3 as a dense embedder was the slowest embedder measured: **316 tok/s** on CPU.
- bge-m3 multi-vector posted NDCG@10 0.7014 and Recall@10 0.946 on its
  800-case reranking-view run, recorded in `reranker-and-pipeline-2026-07-29`.
  It was unshippable at **743 GB per million documents**, because it emits
  1024-dim token vectors.
- bge-reranker-v2-m3 had capability roughly at parity with dense retrieval, so
  it could only shuffle. It degraded the pipeline at every configuration tested.

One family had separate disqualifications by benchmark, throughput, storage, and
headroom. No two failed for the same reason.

That left the embedder choice: a25m, the cheap model that needed no machinery,
or nomic-v2-moe, the stronger model that only wins if we serve it correctly.
Serving it correctly meant per-model settings the harness applied and the
serving path did not.

## Pooling can be wrong without looking wrong

Before prefixes, I hit the smaller version of the same failure.

`AIMEE_LLM_EMBED_POOLING` defaulted to `last`, which is correct for Qwen3 and
silently wrong for nomic, which needs `mean`.

Nothing crashed. The vectors had the right dimension, the API returned success,
the index would have accepted them, and we would have shipped well-formed wrong
vectors with no error and no warning.

Loud-wrong is easy. Silent-wrong looks like a number.

## Benchmark scores are not deployed scores unless serving matches the harness

I assumed the number I measured was the number we would serve.

It was not.

The first candidate won its benchmark, then I noticed the harness was scoring
every model **with its card-recommended prefix**: `search_query:` /
`search_document:` for one model, an instruction sentence for another, nothing
for a third.

Our serving code applied no prefixes.

| model | with card prefix | prefix-free (as served) |
| --- | ---: | ---: |
| nomic-embed-text-v2-moe | 0.6072 | **0.5823** |
| Qwen3-Embedding-0.6B | 0.5810 | **0.5275** |
| bekko-a25m | 0.5909 | 0.5909 *(card defines none)* |

The ranking **inverts** between the two columns. A model that needs no prefix
carries its benchmark score into production intact, while a prefix-dependent one
does not. I was about to select on the left column and ship the right one.

A benchmark number is only a deployment number if the consumer reproduces the
benchmark's input conditions.

## Operational cost put a25m back in contention

I had ranked on score and treated cost as bookkeeping. That order was wrong, and
cost put a25m back in contention.

After the prefix trap, the question was no longer "which model scores highest?"
It was "which model scores highest after paying its operational costs?"

| | a25m | nomic-v2-moe |
| --- | ---: | ---: |
| CPU throughput | **2,155 tok/s** | 598 tok/s |
| relative CPU cost |  | **3.6x slower** |
| vector width | **384** | 768 |
| prefix machinery | none | required |
| migration | none | full re-embed |
| maturity | 10 days old, no published baselines | 18 months, MTEB-checkable |
| Q8_0 quality cost |  | **−0.0037** vs bf16 |

a25m is faster, smaller, simpler, and carries its score into production as-is.
nomic is slower and wider, and its lead exists only after prefix plumbing plus a
full re-embed. Without that work, nomic falls to 0.5823, a **−0.0249**
regression against its own 0.6072 prefixed run.

nomic had quality and maturity. a25m had cost and simplicity. Both were
defensible.

## The reranker briefly made the cheaper embedder look like the right one

I treated the embedder and reranker as independent choices. Measuring them
together showed they were coupled.

A good reranker compressed the embedder gap in the 600-case dense-ordered view:

| embedder | dense | after GTE 20x512 |
| --- | ---: | ---: |
| a25m | 0.5934 | 0.6136 |
| nomic + prefix | 0.6092 | 0.6172 |
| nomic minus a25m | 0.0158 | **0.0036** |

*Source: `reranker-and-pipeline-2026-07-29`, 600-case dense-ordered GTE pipeline
view.*

That view is not comparable to the 10,000-case selection run above. It is the
same-run view where the reranker and embedder decision collided.

Reranking removed 77% of the difference between the two embedders, which was the
strongest argument for a25m: with GTE in the pipeline, a25m was within 0.004 of
nomic while being 3.6x faster on CPU, half the vector width, and needing no
prefix machinery.

That argument only appeared when I measured embedder and reranker together. An
embedder-only table or reranker-only table would not show it.

Deleting the reranker deleted that argument. In this same view, with no
reranker, the embedder gap returns to **0.0158**, and the case for nomic returns
with it.

## Reranking looked transformative on the reranking view

The strongest case for reranking is not subtle.

The incumbent reranker was English-only and had to be replaced for multilingual
support. Measured against the suite's reranking view, 20 candidates in arbitrary
order, one relevant, reranking looked like a win:

| reranker | NDCG@10 |
| --- | ---: |
| no rerank | 0.2279 |
| ettin-68m (incumbent) | 0.2969 |
| bge-reranker-v2-m3 | 0.6174 |
| gte-multilingual-reranker-base | **0.7178** |

GTE scores 0.7178 against 0.2279 for no rerank, and in that view reranking is
transformative because it sorts a randomly ordered candidate list.

That view is not production.

Production feeds the reranker the dense top-k, which is already ordered, so I
ran the pipeline end to end, over the full corpus, 10,000 queries:

| pipeline | NDCG@10 | vs dense |
| --- | ---: | ---: |
| dense only | **0.5909** |  |
| + GTE @ depth 10 | 0.5803 | −0.0106 |
| + GTE @ depth 20 | 0.5861 | −0.0048 |
| + GTE @ depth 50 | 0.5942 | **+0.0032** |

Reranking degrades the result at every depth anyone would run.

The mechanism is visible. The reranker's standalone capability tops out around
0.59-0.62 at these truncations, where dense retrieval already sits. **Its
ceiling is below the ranking it is being asked to improve**, so on average every
reordering is a step backwards.

The two tables answer different questions. Can this model sort a random list is
not the same as can this model beat my embedder, and only the second is the
production question.

It had not been run.

## The 600-query fix was not a fix

An earlier run on a 600-query subsample showed reranking helping by **+0.020**.
At 10,000 queries the same configuration measured **−0.0048**.

A sign flip.

I nearly shipped a recommendation on the subsample.

## Late interaction had the right cost shape and no viable model for us

Cross-encoders are expensive because cost scales with `candidates × tokens`,
paid per query, uncacheable. Late interaction, ColBERT-style, precomputes
document token vectors at index time, then query time is one encode plus MaxSim.

Storage is the common mistake. Late interaction stores one vector per token, so
the bill is `tokens × dims × bytes`. I measured bge-m3 in this shape, and it
cost **743 GB per million documents** because it emits 1024-dimension token
vectors. That figure got quoted as the cost of the architecture. It is the cost
of that model.

A purpose-built ColBERT is an order of magnitude cheaper, by arithmetic rather
than measurement:

| model | vectors/doc | dims | per million docs |
| --- | ---: | ---: | ---: |
| bge-m3 (measured) | 363 | 1024 | **743 GB** |
| colbert-xm (fp16, calculated) | 256 | 128 | 66 GB |
| colbert-xm (int8, calculated) | 256 | 128 | **33 GB** |
| *dense embedding, for scale* | 1 | 768 | 1.5 GB |

*Source: `retrieval-stack-report-2026-07-30`. The colbert-xm rows are computed
from its published vector shape, not measured.*

33 GB per million is an ordinary index size. Late interaction is not inherently
storage-prohibitive. bge-m3 was.

I did run colbert-xm through the pipeline. It was bad: worse than dense
retrieval, and worse at depth 50 than at depth 20, which is the signature of a
model promoting irrelevant documents. Cascade and fusion variants failed too.

**Rule: I am not going to quote those numbers, because I cannot produce the
run.** No artifact for it was committed, and the figures that survive in my
notes disagree with each other. By the standard the rest of this post is written
to, that makes them unusable. Treat the colbert-xm result as a direction I
abandoned, not as a measurement you can check.

What stands: it is the only licence-clean multilingual ColBERT available, so the
architecture has no viable candidate for us today. The cost profile still argues
for it. Somebody should measure it properly.

## Hybrid retrieval fixed the pool instead of reordering it

I spent the night on the component that reorders results, not the component that
chooses them.

So I added a second retrieval leg: BM25 over the lexical signal our KB already
indexes, fused with the dense leg by Reciprocal Rank Fusion.

| pipeline | NDCG@10 | Recall@10 |
| --- | ---: | ---: |
| a25m dense | 0.5909 | 0.7816 |
| nomic dense | 0.6075 | 0.8006 |
| BM25 alone | 0.6213 | 0.8470 |
| a25m + BM25 (RRF) | 0.6206 | 0.8642 |
| nomic + BM25 (RRF, k=60) | **0.6337** | 0.8668 |
| nomic + BM25 (RRF, k=10) |  | **0.9034** |

**BM25 alone beat every dense embedder I had spent the night choosing between.**
Fusion beat everything. The embedder choice composes with fusion rather than
competing with it: nomic+hybrid leads a25m+hybrid by roughly the margin their
dense scores differ by.

The pool shows why:

| pool | contains the labelled document |
| --- | ---: |
| dense top-50 only | 0.8899 |
| dense ∪ BM25 top-50 | **0.9739** |

Dense retrieval missed the target entirely for **11-13%** of queries. **No
reranker can recover those.** Reranking reorders a fixed pool, a decorrelated
retriever changes the pool, and **twenty** reranking configurations bought at
most **+0.0032** because the candidate set had a membership problem.

I recorded the prediction before measuring: if recall ceiling was the cause,
Recall@10 should move more than NDCG@10. It did, **+0.0662 against +0.0262** in
the same configuration, a factor of 2.5.

Two details carry over. The textbook RRF constant `k=60` is wrong for this
corpus, and `k=10` dominates it on every metric, which is free quality from a
constant nobody tunes. Fusion can also cost top-1 precision because RRF sees
rank position and discards score magnitude, so a `tiered` variant lets the dense
leg own rank 1, has **zero** top-1 regression by construction, and still gains
+0.074 Recall@10.

Of course, this is where the evidence is thinnest against my own conclusion. The
suite's queries read like document summaries with key terms appended, which
flatters BM25. Treat **BM25's absolute win as suspect** and the **+10 points of
pool recall as the part that survives**. Two retrievers finding different
documents is less sensitive to phrasing than one retriever matching words.

## The reranker lost to the replacement by mechanism and by measurement

Across **twenty** reranking configurations spanning two embedders, exactly one
beat dense retrieval: GTE at depth 50, by **+0.0032 NDCG@10**, for 143 ms per
query on GPU and unaffordable on CPU.

Hybrid retrieval used infrastructure we already had. It was worth **+0.0262
NDCG@10 and +0.0662 Recall@10** in the same configuration, **8×** the reranker
on the metric they share, plus a recall gain the reranker cannot produce. Tuning
the fusion constant pushes recall to +0.1028.

So we deleted the reranker. That removes a GGUF conversion pipeline, a separate
score-head artifact, a release workflow, and a serving component, and it makes
the CPU and GPU tiers return identical rankings, which they previously could
not.

Modern retrieval-trained embedders appear to have closed the gap that rerankers
were introduced to fill. Our incumbent reranker was worth "4-5 points" when it
was adopted. Measured against a current embedder on this corpus, it is worth
less than nothing.

## The shipped default is the small model because deployment changed the question

The work landed on `testing`: per-model query/document prefixes, embed polarity
at the remaining call sites, the embedder registry, and reranker removal on both
the serving side and the kb side. The old reranker head script and artifact
workflow are gone.

The model that ships is not nomic. It is **bekko-a25m**.

This is the third time in this post that the benchmark winner is not what ships.
nomic won the selection run at 0.6072. a25m ships at 0.5909.

The prefix lesson still holds. The operational question changed again.

a25m runs from weights baked into the kb container image, needs no inference
service, no GPU, and no network. Bundling nomic cost **1.8 GB** of image for a
MoE that exists only as safetensors or GGUF. A deployment that wants a wider or
stronger embedder points `AIMEE_EMBEDDER_URL` at its own GPU endpoint instead,
which is the supported route above **384** dimensions.

The prefix machinery landed, and today it has no work to do because a25m
declares empty query and document prefixes.

The shape is still right. The failure it prevents is undetectable at runtime,
and an operator overlay can declare a prefixed model. I built the safety rail
for a hazard we then engineered away.

This part is easy: the registry expresses the lesson as code. Every field is
required. Empty prefixes are not missing data, they mean "this model card
defines none", and the system can distinguish "declared none" from "not
registered" and refuse to serve the latter rather than guess.

Implementation found two more silent-wrong failures:

- the embedder was served with `--ctx-size 8192` against nomic's 2,048 trained
  positions
- the query path's builtin fallback declared itself a document

None of these were style bugs. They were plausible configurations that would
have served plausible vectors.

The reranker is gone. The shipped registry has one entry: bekko-a25m, **384**
dimensions, mean pooling, and empty prefixes.

The smallest, youngest, least-credentialled model in the field is the one in
production. It has no published baselines, it was ten days old when I measured
it, it lost the selection run to nomic by **0.0163**, 0.6072 against 0.5909, the
same run, and then it won the deployment because every larger candidate lost on
something that was not the score: an inference service, a GPU, network access,
or **1.8 GB** of image.

nomic remains the stronger measured embedder. It is not the bundled default.
Above **384** dimensions, bring your own endpoint.

## Silent-wrong was the recurring failure mode

Six substantive claims I made during this work were wrong and corrected only by
measuring:

- CPU reranking feasibility, off by **10×** (extrapolated from the wrong runtime)
- late-interaction speedup, off by **3×**
- storage cost, off by **5.7×** (assumed 128-dim vectors, the model emitted 1024)
- "latency is linear in tokens", it is superlinear
- "truncate documents, don't trim candidates", true for capability, false for usefulness
- "uniform embedding dimensions are an architectural win", the system already handled it

The pattern matters: almost every failure was silent, not loud.

- a pooling default that produced well-formed wrong vectors
- a prefix flag worth 0.025 NDCG that nothing warned about
- `-ngl 0` silently overridden by an auto-fit heuristic
- `-np 4` quietly quartering the context window to 512 tokens
- a GPU ONNX provider silently falling back to CPU, a 22-hour run masquerading as a 35-minute one
- a reranker returning **constant scores**, which reproduced the no-rerank baseline to sixteen decimal places

The constant-score failure is the one to keep. I caught it only because matching
the baseline exactly was too perfect to be real. Had it returned 0.21 instead of
0.2279, I would have written off the best reranker I tested and never known.

None of these threw an error. Each produced a plausible number.

**Rule: on a retrieval stack, the dominant failure mode is silent-wrong, not
loud-wrong.** Record provenance, model, precision, device, truncation, sample
size, and harness for every figure. A number without it is not evidence.

I tripped over that while writing this post. nomic's prefixed score appears in
my own notes as 0.6058, 0.6072 and 0.6075: independent runs of the same suite,
agreeing within its documented noise. One handoff document had quietly computed
a delta between two of them. Harmless here. Same shape as every bug above: a
plausible number, no error, and provenance that stopped travelling with the
figure.

The expensive lesson was simpler: measure candidate membership before you
measure candidate ordering. I spent the night improving the ordering of a
candidate set whose problem was its membership, because reranking was the
component I was asked about, so reranking was the component I measured.

On Monday, take your retrieval stack and measure whether the labelled document
is in the candidate pool before the reranker sees it. If dense retrieval misses
it, add a decorrelated retrieval leg and fuse the pools. Tune `k`. Keep a tiered
variant if top-1 regression matters. Only measure reranking after the right
document is in the list.

The suite, the artifacts behind every table, and the validation writeups are in
the [evidence repository](https://github.com/RakuenSoftware/rakuen-blog/tree/main/articles/we-measured-our-reranker-and-deleted-it). The two figures I withdrew are listed there
too, with the reason.
