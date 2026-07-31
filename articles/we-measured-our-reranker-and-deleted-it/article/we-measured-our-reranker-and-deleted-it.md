# We spent a night measuring our retrieval stack, and deleted the reranker

*Draft — 2026-07-31. Every figure traces to a document or artifact published
alongside this post.*

We set out to answer a small question: which embedding model should our knowledge
base use? We came back with two answers we had not asked for.

We went in assuming the reranker was settled. We came out having deleted it — the
component nobody was questioning was making retrieval *worse*.

We went in expecting one of the larger, better-credentialled models to win. We
came out shipping the smallest, youngest thing in the field: 384 dimensions, ten
days old, no published baselines at all.

What follows is the chain of decisions between those two points, including the
four times we were confidently wrong. The numbers live in their sections. The
reasoning is the point.

## The setup

Our KB does dense retrieval over ~26k documents, then reranks the top candidates
with a cross-encoder before answering. Standard architecture. We had a fresh
evaluation suite — 10,000 queries against the full corpus, built from our own
content, with three categories: prose, code, and cited artifacts.

The plan was to pick an embedder and move on.

## The embedder field

We expected this to be a shortlist exercise: score the candidates, take the top
one, move on. It took three rounds across two suites before the field stopped
reordering itself.

June was how we got here, not the campaign. First LoCoMo ranked nomic-v1.5
above Qwen3, and we later marked that screen as under-discriminating and
superseded. Then the June BEIR-plus-code round leaned on published MTEB code
scores and dropped nomic for the Qwen3 ladder. That dropped model was
nomic-embed-text-v1.5: text-only, no code training. It was not
nomic-embed-text-v2-moe, the retrieval-trained model that won on code in July.

The June rounds were different suites. They are not comparable to July. The
late-July campaign is the comparable block: 2026-07-26 through 2026-07-30,
frozen-ab-v1, manifest SHA-256
`16d2c16add86052ff24be410699ab9452ee1a36252de6dba31ab5391de7ab81c`, 10,000
paired cases over the same corpus. Jul 30 closed it with the full-length GTE
pipeline result and the hybrid BM25+RRF work.

Jul 26–28 started with the ab-v1 baselines. We tested the Gemma-4 unified-base
idea as configured, and it was not close.

| model | width | NDCG@10 | MRR@10 | R@10 | vectors/s |
| --- | ---: | ---: | ---: | ---: | ---: |
| Gemma 4 E2B | 1,536 | 0.362803 | 0.269053 | 0.6735 | 5.4347 |
| Gemma 4 E4B | 2,560 | 0.422186 | 0.328657 | 0.7275 | 2.2839 |

*Source: ab-v1 results README, Gemma 4 E2B/E4B embedding summaries.*

These are their own result: same manifest, 10,000 cases, ranked against
**23,688** candidate documents. The Jul 29 selection run ranked against
**26,473** documents, so we do not take a numeric margin between the two. The
Gemma result was still far short of the field we needed to choose from.

The E2B run was a stock untrained instruction checkpoint: a pre-training
control, not evidence that Gemma-4 was ready to replace the supported embedder.
So this eliminated the unified-base idea as we had configured it. It did not
prove that Gemma-4 can never embed.

The same ab-v1 block also ran the incumbent-family reranking controls, on the
ab-v1 reranking view: Ettin 68M at **0.607353** NDCG@10, and Ettin 400M at
0.643879. That view is the positive plus 19 fixed BM25 hard negatives. Do not
mix those numbers with the arbitrary-order reranking view used later in this
post — different negatives, different difficulty, different scale.

*Source: ab-v1 results README, completed reranking controls.*

Jul 29 was the embedder selection run: same frozen suite, all 26,473 corpus
documents, each model at its best — card prefix, native pooling, full corpus.

| model | NDCG@10 | R@10 | dim | code | prose | cited | GPU vec/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| nomic-embed-text-v2-moe | **0.6072** | 0.8007 | 768 | **0.8104** | 0.5157 | 0.6344 | 82.7 |
| Qwen3-Embedding-4B | 0.6061 | **0.8100** | 2560 | 0.7394 | **0.5274** | 0.6988 | 26.4 |
| bekko-embedding-v1-a25m | 0.5909 | 0.7816 | 384 | 0.7718 | 0.4841 | **0.7170** | **510.7** |
| Qwen3-Embedding-0.6B | 0.5810 | 0.7765 | 1024 | 0.7325 | 0.4930 | 0.6804 | 113.1 |

*Source: `embedder-selection-frozen-ab-v1`, "Results — every model at its best".*

Qwen3 was out. The 0.6B model was the weakest finalist. The 4B model tied nomic
while costing 3.3x the vector storage and embedding 3.1x slower. The ladder
topped out at parity with a 475M model.

## The benchmark was the problem

One result would not sit still. A model whose published code scores were close to
perfect kept placing last on ours. We had two options — distrust our corpus, or
distrust the published number — and we went looking at the benchmark first.

Every query a deployed model answers is data it has never seen.

That is not an edge case. It is the entire job. A retrieval model in production
is asked, without exception, about documents that were not in its training set —
and if it were only good at material it had already absorbed, it would be
useless the moment you pointed it at your own corpus.

So a benchmark is only measuring the deployed condition if the model could not
have trained on it. Otherwise it is scoring a situation that never happens.

That is the whole requirement, and it is not secrecy — it is **novelty**.
frozen-ab-v1 did not exist when these models were trained, so a score on it is
capability rather than recall. Nothing is withheld to achieve that. The data is
simply newer than the weights.

So we publish it. The suite ships with this article: corpus, all three views,
manifest hashes. A measurement nobody can reproduce is not evidence, and hiding
the data would buy us nothing the timing has not already bought.

What publication does change is the *next* generation. Once the suite is public
it can be absorbed into a future training set, and a model trained after today
tells you nothing by scoring well on it. That is not a flaw in publishing. It is
the ordinary lifecycle of every benchmark, and ours is now in it.

That lifecycle already ran to completion on the public code benchmarks.

CodeSearchNet and its relatives have been public for years, with every incentive
in the industry pointing at topping them. A near-perfect score on a benchmark
that old tells you the model has seen it. It cannot tell you anything about code
the model has not seen.

That is not a claim about one vendor's conduct. It is what happens to any
benchmark that predates the models being scored on it.

The fix is not to hide anything. It is to keep cutting new data. **The harness is
durable; the data is the consumable.** The builder, the scoring, the validation
records and the acceptance checks are all reusable — point them at content
created since the last model generation and you have a fresh, honest measurement.
Publish that too. Then do it again. You keep the instrument and you keep spending
samples, and the cost of a sample is far below the cost of a number that means
nothing.

Qwen3's publishers report near-perfect code retrieval on MTEB:

| task | 0.6B | 4B | 8B |
| --- | ---: | ---: | ---: |
| CodeSearchNet | 0.943 | 0.960 | 0.966 |
| CodeSearchNet-CC | 0.933 | 0.967 | 0.971 |
| StackOverflowQA | 0.900 | 0.943 | 0.948 |
| CodeFeedback-MT | 0.908 | 0.932 | 0.937 |

Those are the publishers' figures, not ours.

Then we put the same family on code it could not have trained on when we
measured:

| model | dim | code |
| --- | ---: | ---: |
| nomic-embed-text-v2-moe | 768 | **0.8104** |
| bekko-embedding-v1-a25m | 384 | **0.7718** |
| Qwen3-Embedding-4B | 2,560 | **0.7394** |
| Qwen3-Embedding-0.6B | 1,024 | **0.7325** |

*Source: `embedder-selection-frozen-ab-v1`, code category of the selection run.*

Both Qwen3 models came last.

They were behind nomic-v2-moe. They were also behind bekko-a25m: a 384-dimension
model, ten days old at the time, with no published baselines of any kind.

We did not run Qwen3-8B on frozen-ab-v1. We did not need it to see the failure
shape.

A model that publishes near-perfect code retrieval and then places last on code
the moment it meets a corpus it has not seen has not demonstrated code retrieval.
Whatever the mechanism, the published number did not survive contact with unseen
data.

A number that does not survive that is not a measurement of capability. It
describes the benchmark, not the model.

That is the strongest finding in the campaign.

And it generalises. Every figure a model publishes is measured on a test set the
publisher chose and could have trained on. The only figure that tells you what a
model will do on your data is one measured on your data.

Measure on data that postdates the weights. Publish it, so the measurement can be
checked. Then cut the next sample against the next generation. Keep the harness.
Keep making data.

This is the same lesson as the prefix trap, on a different axis. There, a
benchmark number stopped being a deployment number because the serving path did
not reproduce the benchmark's input conditions. Here, it stops being one because
the benchmark does not reproduce deployment's *data* condition — which is, always,
material the model has never seen.

bge lost differently each time:

- bge-base-en-v1.5 went out with the June LoCoMo screen.
- bge-m3 as a dense embedder was the slowest embedder measured: **316 tok/s** on CPU.
- bge-m3 multi-vector posted NDCG@10 0.7014 and Recall@10 0.946 on its
  800-case reranking-view run, recorded in `reranker-and-pipeline-2026-07-29`.
  It was unshippable at **743 GB per million documents**, because it emits
  1024-dim token vectors.
- bge-reranker-v2-m3 had capability roughly at parity with dense retrieval, so
  it could only shuffle. It degraded the pipeline at every configuration tested.

One family, four disqualifications: benchmark, throughput, storage, and headroom.
No two failed for the same reason.

That left the real embedder choice: a25m, the cheap model that needed no
machinery, or nomic-v2-moe, the stronger model that only wins if we serve it
correctly.

The next two sections are what "serve it correctly" turned out to mean. Both are
per-model settings the harness applied and the serving path did not.

## Trap 0: pooling can be wrong without looking wrong

Before prefixes, we hit the smaller version of the same failure.

`AIMEE_LLM_EMBED_POOLING` defaulted to `last`. That is correct for Qwen3. It is
silently wrong for nomic, which needs `mean`.

Nothing crashed. The vectors had the right dimension. The API returned success.
The index would have accepted them. We would have shipped well-formed wrong
vectors, with no error and no warning.

This is the shape of almost every failure below. Loud-wrong is easy. Silent-wrong
looks like a number.

## Trap 1: benchmark scores are not deployed scores

We assumed the number we measured was the number we would serve. It is not, and
the gap is not small enough to ignore.

Our first candidate won its benchmark decisively. Then we noticed the harness was
scoring every model **with its card-recommended prefix** — `search_query:` /
`search_document:` for one model, an instruction sentence for another, nothing at
all for a third.

Our serving code applies no prefixes.

| model | with card prefix | prefix-free (as served) |
| --- | ---: | ---: |
| nomic-embed-text-v2-moe | 0.6072 | **0.5823** |
| Qwen3-Embedding-0.6B | 0.5810 | **0.5275** |
| bekko-a25m | 0.5909 | 0.5909 *(card defines none)* |

The ranking **inverts** between the two columns. A model that needs no prefix
carries its benchmark score into production intact; a prefix-dependent one does
not. We had been about to select on the left column and ship the right one.

**Lesson: a benchmark number is only a deployment number if the consumer
reproduces the benchmark's input conditions.**

## The cost ledger

Up to here we had been ranking on score and treating cost as bookkeeping to settle
afterwards. That order turned out to be backwards, and reversing it put a model we
had nearly dismissed back in contention.

After the prefix trap, the choice was no longer "which model scores highest?" It
was "which model scores highest after paying its operational costs?"

| | a25m | nomic-v2-moe |
| --- | ---: | ---: |
| CPU throughput | **2,155 tok/s** | 598 tok/s |
| relative CPU cost | — | **3.6x slower** |
| vector width | **384** | 768 |
| prefix machinery | none | required |
| migration | none | full re-embed |
| maturity | 10 days old, no published baselines | 18 months, MTEB-checkable |
| Q8_0 quality cost | — | **−0.0037** vs bf16 |

That is a real ledger. a25m is faster, smaller, simpler, and carries its score
into production as-is. nomic is slower and wider, and its lead only exists after
prefix plumbing plus a full re-embed. Without that work, nomic falls to 0.5823 —
a **−0.0249** regression against its own 0.6072 prefixed run.

The case for nomic is quality and maturity. The case for a25m is cost and
simplicity. At this point both were defensible.

## The twist: the reranker changed the embedder decision

We had been treating these as two independent choices: pick the embedder, then
pick the reranker. Measuring them together showed they were not independent at
all, and the direction of the dependency surprised us.

Then the two decisions collided.

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

Reranking removed 77% of the difference between the two embedders. That was the
strongest argument for taking the cheap embedder: with GTE in the pipeline, a25m
was within 0.004 of nomic while being 3.6x faster on CPU, half the vector width,
and needing no prefix machinery.

That argument only appeared when we measured embedder and reranker together. It
would not have shown up in an embedder-only table or a reranker-only table.

Then deleting the reranker deleted that argument too. In this same view, with no
reranker, the embedder gap is back to its full **0.0158**, and the case for nomic
is restored.

So the embedder decision and the reranker decision were coupled. We could not
make either one independently.

## Trap 2: capability is not usefulness

We had a reranker that scored **0.7178** where the incumbent managed 0.2969, and
we took that as settled evidence it would help. We had never asked it the
production question.

With the embedder settled we turned to the reranker, which was English-only and
had to be replaced for multilingual support anyway.

Measured against the suite's reranking view — 20 candidates in arbitrary order,
one relevant — reranking looked transformative:

| reranker | NDCG@10 |
| --- | ---: |
| no rerank | 0.2279 |
| ettin-68m (incumbent) | 0.2969 |
| bge-reranker-v2-m3 | 0.6174 |
| gte-multilingual-reranker-base | **0.7178** |

A clean +0.49 over doing nothing. Obvious win.

Except that view feeds the reranker **randomly ordered** candidates. Production
feeds it the dense top-k, which is already well ordered. So we ran the pipeline
end to end, over the full corpus, 10,000 queries:

| pipeline | NDCG@10 | vs dense |
| --- | ---: | ---: |
| dense only | **0.5909** | — |
| + GTE @ depth 10 | 0.5803 | −0.0106 |
| + GTE @ depth 20 | 0.5861 | −0.0048 |
| + GTE @ depth 50 | 0.5942 | **+0.0032** |

Reranking *degrades* the result at every depth anyone would actually run.

The mechanism is visible in the numbers. The reranker's standalone capability
tops out around 0.59–0.62 at these truncations — which is where dense retrieval
already sits. **Its ceiling is below the ranking it is being asked to improve**,
so on average every reordering is a step backwards.

Those two tables answer different questions. *Can this model sort a random list?*
is not *can this model beat my embedder?* Only the second is the production
question, and it had never been run.

## Trap 3: the fix that was measured on 600 queries

An earlier run on a 600-query subsample showed reranking helping by **+0.020**.
At 10,000 queries the same configuration measured **−0.0048**. A sign flip.

We nearly shipped a recommendation on the subsample.

## Late interaction: right architecture, wrong model

Cross-encoders are expensive because cost scales with `candidates × tokens`, paid
per query, uncacheable. Late interaction (ColBERT-style) precomputes document
token vectors at index time; query time is one encode plus MaxSim.

The storage cost is the thing people get wrong about it, so start there. Late
interaction stores one vector per token, so the bill is `tokens × dims × bytes`.
We measured bge-m3 in this shape and it was ruinous — **743 GB per million
documents**, because it emits 1024-dimension token vectors. That figure got
quoted as the cost of the architecture. It is the cost of that model.

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

33 GB per million is an ordinary index size. So late interaction is not
inherently storage-prohibitive; bge-m3 was.

We did run colbert-xm through the pipeline, and it was bad — worse than dense
retrieval, and worse at depth 50 than at depth 20, which is the signature of a
model actively promoting irrelevant documents. Cascade and fusion variants failed
too.

**We are not going to quote those numbers, because we cannot produce the run.**
No artifact for it was committed, and the figures that survive in our notes
disagree with each other. By the standard the rest of this post is written to,
that makes them unusable. Treat the colbert-xm result as a direction we
abandoned, not as a measurement you can check.

What stands: it is the only licence-clean multilingual ColBERT available, so the
architecture has no viable candidate for us today. The cost profile still argues
for it. Somebody should measure it properly.

## The thing we should have measured first

By this point we had spent the entire night on the component that *reorders*
results and none at all on the component that *chooses* them. This is the section
we would run first if we started again.

At this point we had spent a night on the component that reorders results, and
none on the component that *chooses* them. So we added a second retrieval leg —
BM25 over the lexical signal our KB already indexes — and fused it with the dense
leg by Reciprocal Rank Fusion.

| pipeline | NDCG@10 | Recall@10 |
| --- | ---: | ---: |
| a25m dense | 0.5909 | 0.7816 |
| nomic dense | 0.6075 | 0.8006 |
| BM25 alone | 0.6213 | 0.8470 |
| a25m + BM25 (RRF) | 0.6206 | 0.8642 |
| **nomic + BM25 (RRF, k=60)** | **0.6337** | 0.8668 |
| **nomic + BM25 (RRF, k=10)** | — | **0.9034** |

**BM25 alone beat every dense embedder we had spent the night choosing between.**
Fusion beat everything. And the embedder choice *composes* with fusion rather
than competing with it — nomic+hybrid leads a25m+hybrid by roughly the margin
their dense scores differ by.

The reason is visible in the pool:

| pool | contains the labelled document |
| --- | ---: |
| dense top-50 only | 0.8899 |
| **dense ∪ BM25 top-50** | **0.9739** |

Dense retrieval missed the target entirely for **11–13%** of queries. **No
reranker can recover those.** Reranking reorders a fixed pool; adding a
decorrelated retriever changes what is in the pool. That is the whole story of
why twenty reranking configurations bought us at most +0.0032: we had been
optimising the ordering of a candidate set whose real problem was its membership.

We recorded the prediction before measuring — if the recall-ceiling explanation
was right, Recall@10 should move more than NDCG@10. It did — **+0.0662 against
+0.0262** in the same configuration, a factor of 2.5.

Two details worth stealing. **The textbook RRF constant `k=60` is wrong for this
corpus** — `k=10` dominates it on every metric, which is free quality from a
constant nobody tunes. And fusion can cost top-1 precision, because RRF sees rank
position and discards score magnitude; a `tiered` variant that lets the dense leg
own rank 1 has **zero top-1 regression by construction** and still gains +0.074
Recall@10.

One caveat we can't yet rule out: our suite's queries read like document
summaries with key terms appended, which flatters BM25. So treat **BM25's
absolute win as suspect** and the **+10 points of pool recall as robust** — two
retrievers finding different documents is far less sensitive to phrasing than one
retriever matching words.

## The result

Across **twenty** reranking configurations spanning two embedders, exactly one
beat dense retrieval: GTE at depth 50, by **+0.0032 NDCG@10**, for 143 ms per
query on GPU and unaffordable on CPU.

The hybrid retrieval we bolted on at the end, using infrastructure that already
existed, was worth **+0.0262 NDCG@10 and +0.0662 Recall@10** in the same
configuration — **8×** the reranker on the metric they share, plus a recall gain
the reranker cannot produce at all. Tuning the fusion constant pushes recall to
+0.1028.

So we deleted the reranker. That removes a GGUF
conversion pipeline, a separate score-head artifact, a release workflow, and an
entire serving component — and it makes the CPU and GPU tiers return identical
rankings, which they previously could not.

Modern retrieval-trained embedders appear to have closed the gap that rerankers
were introduced to fill. Our incumbent reranker was worth "4–5 points" when it
was adopted; measured against a current embedder it is worth less than nothing.

## Where this actually stands

This shipped.

The work landed on `testing`: per-model query/document prefixes, embed polarity at
the remaining call sites, the embedder registry, and reranker removal on both the
serving side and the kb side. The old reranker head script and artifact workflow
are gone.

But the model that ships is not nomic. It is **bekko-a25m**.

That is the third time in this post that the benchmark winner is not what ships.
nomic won the selection run at 0.6072. a25m ships at 0.5909.

The reason is not that the prefix lesson was wrong. It is that we changed the
operational question again.

a25m runs from weights baked into the kb container image. It needs no inference
service, no GPU, and no network. Bundling nomic cost **1.8 GB** of image for a
MoE that exists only as safetensors or GGUF. A deployment that wants a wider or
stronger embedder points `AIMEE_EMBEDDER_URL` at its own GPU endpoint instead.
That is the supported route above **384 dimensions**.

So the prefix machinery landed, and today it has no work to do. a25m declares
empty query and document prefixes.

That is still the right shape. The failure it prevents is undetectable at
runtime, and an operator overlay can declare a prefixed model. We built the
safety rail for a hazard we then engineered away.

The registry is the lesson expressed as code: **every field is required**. Empty
prefixes are not missing data. They mean "this model card defines none." That
lets the system distinguish "declared none" from "not registered" and refuse to
serve the latter rather than guess.

Implementation found two more silent-wrong failures:

- the embedder was served with `--ctx-size 8192` against nomic's 2,048 trained
  positions
- the query path's builtin fallback declared itself a document

None of these were style bugs. They were plausible configurations that would have
served plausible vectors.

The reranker is gone. The shipped registry has one entry: bekko-a25m, 384
dimensions, mean pooling, and empty prefixes.

So the smallest, youngest, least-credentialled model in the field is the one in
production. It has no published baselines. It was ten days old when we measured
it. It lost the selection run to nomic by **0.0163** — 0.6072 against 0.5909, the
same run — and then won the deployment anyway, because every larger candidate
lost on something that was not the score: an inference service, a GPU, network
access, or **1.8 GB** of image.

nomic remains the stronger measured embedder. It is not the bundled default.
Above 384 dimensions, bring your own endpoint.

## The lesson that mattered most

Six substantive claims we made during this work were wrong and corrected only by
measuring:

- CPU reranking feasibility — off by **10×** (extrapolated from the wrong runtime)
- late-interaction speedup — off by **3×**
- storage cost — off by **5.7×** (assumed 128-dim vectors, the model emitted 1024)
- "latency is linear in tokens" — it is superlinear
- "truncate documents, don't trim candidates" — true for capability, false for usefulness
- "uniform embedding dimensions are an architectural win" — the system already handled it

But the pattern underneath is the important part. **Almost every failure was
silent, not loud:**

- a pooling default that produced well-formed *wrong* vectors
- a prefix flag worth 0.025 NDCG that nothing warned about
- `-ngl 0` silently overridden by an auto-fit heuristic
- `-np 4` quietly quartering the context window to 512 tokens
- a GPU ONNX provider silently falling back to CPU — a 22-hour run masquerading as a 35-minute one
- a reranker returning **constant scores**, which reproduced the no-rerank baseline to sixteen decimal places

That last one is the one to sit with. We caught it *only* because matching the
baseline exactly was too perfect to be real. Had it returned 0.21 instead of
0.2279, we would have written off the best reranker we tested and never known.

None of these threw an error. Each produced a plausible number.

**If you take one thing from this: on a retrieval stack, the dominant failure
mode is silent-wrong, not loud-wrong.** Record provenance — model, precision,
device, truncation, sample size, harness — for every figure. A number without it
is not evidence.

We can vouch for that last sentence, because we tripped over it while writing
this post. nomic's prefixed score appears in our own notes as 0.6058, 0.6072 and
0.6075 — three independent runs of the same suite, agreeing within its documented
noise — and one of our handoff documents had quietly computed a delta between two
of them. Harmless here. But it is the identical shape to every bug above: a
plausible number, no error, and provenance that had stopped travelling alongside
the figure.

And the second lesson, which cost us the most: **we spent the night improving the
ordering of a candidate set whose problem was its membership.** Reranking was the
component we were asked about, so it was the component we measured. The question
worth asking first is not "is my ranking in the right order?" but "is the right
document in the list at all?" For 11–13% of our queries it simply wasn't, and no
amount of reordering was ever going to find it.
