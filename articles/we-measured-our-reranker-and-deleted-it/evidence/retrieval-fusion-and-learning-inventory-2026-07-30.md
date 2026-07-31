# Inventory: what already exists for retrieval fusion, ranking and learning

- **Date:** 2026-07-30. **Method:** read of the shipped tree, not of proposals.
  Every claim carries a `file:line`. Where a proposal and the code disagree, the
  code wins and the disagreement is recorded.
- **Why:** the 2026-07-29/30 retrieval campaign concluded that hybrid fusion and
  learned ranking are where the remaining quality sits, and drafted proposals for
  both. Those proposals were written **without** surveying the tree. This document
  establishes what is actually built, so the proposals describe the remaining work
  rather than work already done.

## Executive summary

Five things that change the shape of the work:

1. **Hybrid fusion is not a new capability.** `kb_search_fused` already runs a real
   dense leg and a real Postgres-FTS lexical leg and fuses them, with **three
   selectable modes** (`rrf`, `static_alpha`, `dynamic_alpha`).
2. **The KB path's RRF constant is a hardcoded `#define RRF_K 60`** — the exact
   value the campaign measured as wrong. The *code* path's equivalent is
   config-tunable (`code_hybrid_rrf_k`). This asymmetry is the single cheapest
   quality change available.
3. **A learned linear ranker is shipped and live**, with a feature store, a fitter
   sidecar, and a benchmark-gated promotion path. Its weights are the hand-set
   `{dense 0.6, lex 0.4}` because the fitting loop cannot be trained.
4. **A bandit over fusion modes is shipped and live** — and its reward function is
   *provably identical across its three arms*. It cannot learn. Verified below.
5. **`feature_rows` is a snapshot table, not an event log.** It upserts one row
   per document. No training set for ranking can be assembled from it, and adding
   a grouping key would not fix that. This is the hard blocker for all learning
   work, and it is a schema change.

`HyDE` and query decomposition also already exist (for memory search), so two
items on the campaign's "alternatives" list are partly built.

---

## 1. The retrieval legs

`kb_search_fused` (`src/kb/kb.c`) runs two genuine, decorrelated legs.

| leg | function | mechanism |
| --- | --- | --- |
| dense | `vec_search` | pgvector, project-scoped |
| lexical | `lexical_search_fts` (`src/kb/kb.c:1276`) | Postgres FTS over `kb_documents.kb_fts_tsv` via `db2_kb_documents_fts_search` |

The lexical leg is real term search. It **used not to be**: it previously embedded
the query and called the same pgvector search, so the two legs were byte-identical
and every fusion mode collapsed to the identity. The comment at `src/kb/kb.c:1270`
records this, and it is worth reading before trusting any historical fusion
measurement taken on this path:

> *"previously it embedded the query and called the same pgvector search as
> vec_search, so the two legs were byte-for-byte identical and alpha_merge
> collapsed to the identity (rrf/static_alpha/dynamic_alpha all produced the same
> ranking)."*

## 2. Fusion: three modes, already selectable

Config `kb_fusion_mode` (`src/modules/config/config_fields.c:179`), values
`rrf` (default) `| static_alpha | dynamic_alpha`, with a per-request
`fusion_mode_override` (`src/headers/kb.h:144`).

| mode | implementation | parameter |
| --- | --- | --- |
| `rrf` | `rrf_merge` (`src/kb/kb.c:1477`) | **hardcoded `#define RRF_K 60`** (`src/kb/kb.c:1242`) |
| `static_alpha` | `alpha_merge` (`src/kb/kb.c:1338`) | `kb_fusion_static_alpha`, default 0.5 |
| `dynamic_alpha` | `alpha_merge` with a predicted alpha | `kb_fusion_predict_alpha` (`src/kb/kb_fusion.c:6`) |

### `dynamic_alpha` is a hand-written heuristic, not a model

`kb_fusion_predict_alpha` counts "lexical-looking" tokens in the query —
ALL-CAPS words ≥3 chars, `snake_case`/`kebab-case`, dotted identifiers — plus a
bonus for quotes and slashes, then returns `alpha = 0.15 + ratio * 0.70`
(`src/kb/kb_fusion.c`). It is deterministic, unit-tested
(`src/tests/test_kb_fusion.c`), and entirely un-fitted: every constant is a guess.

This is a reasonable prior and a natural first thing to *replace with a fitted
function*, since the plumbing that consumes an alpha already exists.

### The KB path cannot be tuned; the code path can

| path | RRF constant | tunable? |
| --- | --- | --- |
| `kb_search_fused` (docs/prose) | `#define RRF_K 60` (`src/kb/kb.c:1242`) | **no — recompile** |
| `kb_rrf_fuse` (code hybrid) | `KB_RRF_DEFAULT_K 60` (`src/kb/kb_rrf.h`), overridden by `code_hybrid_rrf_k` | **yes, hot-reloadable** |

## 3. Code-hybrid fusion is a second, richer fusion implementation

`src/kb/kb_rrf.c` / `.h` fuses **three** signals — graph neighbourhood, vector
similarity, memory recall — by rank, with per-signal weights
(`code_hybrid_weight_{code,graph,vector,memory}`) and a tunable `k`. It also has
`kb_rrf_fuse_trust`, which inserts earned trust from the lessons pipeline as a
**tie-break only**, deliberately never moving a candidate across a real score gap.

Two notes for any fusion proposal:

- The weighted-RRF and multi-leg-RRF machinery the campaign proposed **already
  exists here**, and is a better base than writing new fusion code.
- Its interface is rank-only (`kb_rrf_item_t` carries an id and a structural
  weight, no score), so it cannot express score fusion without a signature change.

## 4. Memory retrieval has its own blend — and already has HyDE

| capability | config | status |
| --- | --- | --- |
| lexical/semantic blend | `memory_bm25_weight`, `memory_semantic_weight` | shipped |
| query expansion | `memory_query_expansion_mode`, `_k` | shipped |
| **HyDE** | `memory_rewrite_hyde` | **shipped** (`src/modules/memory/memory_core_search_c.c:293-341`) |
| **query decomposition** | `memory_rewrite_decompose`, `memory_rewrite_max_subqueries` | **shipped** |

HyDE and decomposition are implemented as an LLM rewrite sidecar returning
`{hyde_answer, sub_questions}`. The campaign listed HyDE as an unbuilt option
deprioritised for query-path latency; in fact it exists, gated off, for memory
search but **not** for KB search. Whether to extend it to KB is a much smaller
question than building it.

## 5. Learned ranking: shipped, live, and untrainable

### What is built

| piece | where | status |
| --- | --- | --- |
| linear inference + reorder | `kb_ranker_rerank_with_sketch` (`src/kb/kb_ranker.c:53`) | shipped |
| model artifact write/load/commit | `src/kb_ranker.h` | shipped |
| `proposed → committed` promotion gate | `kb_ranker_model_write_proposed`, `_commit` | shipped |
| per-candidate features | `kb_features_upsert_with_sketch` (`src/kb_features.h`) | shipped |
| feature-set versioning | `KB_FEATURE_SET_VERSION "v1"` | shipped |
| fitter sidecar | `scripts/rank-fit.py` | shipped |
| replay tooling | `tools/rank_replay.py` | shipped |
| flag | `intelligence.ranking.fit.enabled` | shipped, default off |

The model scores
`w_dense·dense + w_lex·lex + w_recency·recency + w_sketch_frequency·f + w_sketch_distinct·d`
and reorders. Live weights are the hand-set literals
`{w_dense=0.6, w_lex=0.4, w_recency=0, w_sketch_frequency=0, w_sketch_distinct=0}`
(`src/kb/kb_ranker.c:32`). **The two sketch features are computed, stored, and
multiplied by zero.**

### Why it cannot be trained — the hard blocker

`docs/proposals/done/learning-to-rank-weight-fitting.md` states the loop is
bench-only because the training-view join is empty: features are keyed to
`subject_kind='kb_document'` while outcomes attribute to `memory` ids, and
`feature_rows` carries no `retrieval_event_id`.

**The schema shows a more fundamental problem than a join.** `feature_rows`
(`src/db2/schema.sql:594`):

```sql
PRIMARY KEY (subject_id, subject_kind, feature_set_version)
```

and the write (`src/db2/feature_rows.c:39`):

```sql
ON CONFLICT (subject_id, subject_kind, feature_set_version)
DO UPDATE SET features = EXCLUDED.features, computed_at = EXCLUDED.computed_at
```

There is **exactly one row per (document, kind, feature-set version)**, and every
retrieval that touches a document **overwrites** it. The table is a
latest-value snapshot, not an event log.

The consequences are decisive and are not what the `done` proposal describes:

- A training set requires *(query, candidate) → features, label* tuples. This
  table can only answer "what were this document's features the last time anyone
  retrieved it."
- **Adding a `retrieval_event_id` column would not fix it.** Unless it enters the
  primary key, the upsert still collapses every event into one row.
- The same query's candidates cannot be grouped, so pairwise/listwise objectives
  have no groups — but that is downstream of there being no per-event rows at all.
- Historical data is not merely unjoinable; it has already been destroyed and is
  being destroyed continuously.

Any learning proposal must therefore start with a **schema migration turning
`feature_rows` into an append-only event log** (or adding a sibling log). That is
the prerequisite, and it is larger than the fitter that consumes it.

## 6. Bandits: shipped, live — and the fusion arm cannot learn

### What is built

`src/kb_bandit.h`, `src/kb/kb_bandit.c`, `src/db2/bandit.c`, registry at
`src/kb/kb_bandit_registry.c`. Thompson sampling via a sidecar
(`kb_bandit_sample`), reward closing (`kb_bandit_reward`), operator lock-in
(`db2_bandit_promotion_get`), IPW offline replay (`tools/bandit_replay.py`) lifted
into `benchmark_trace` artifacts (`kb_bandit_record_replay_evidence`).

Six registered decision points; two are relevant here:

| id | arms | reward_fn | status |
| --- | --- | --- | --- |
| `kb_memory_retrieval_limit` | `10`, `20` | `recall_sufficiency_v1` | live |
| **`kb_fusion_mode`** | `rrf`, `static_alpha`, `dynamic_alpha` | `recall_sufficiency_v1` | **live** |

The loop is genuinely wired: sampled at `src/kb/kb.c:1716`, rewarded at
`src/kb/kb.c:1907`.

### The defect: the reward is invariant across the arms

The reward is
`kb_bandit_recall_sufficiency_reward(n_results, max_results)` (`src/kb/kb.c:1906`),
defined in `src/kb_bandit.h` as a function of **result count only**:

| condition | reward |
| --- | ---: |
| `n_results == 0` | 0.0 |
| `n_results >= limit` | 0.5 |
| `0 < n_results < limit` | 1.0 |

Now the ordering functions. Both `alpha_merge` (`src/kb/kb.c:1451`) and
`rrf_merge` (`src/kb/kb.c:1561`) end with:

```c
int n = (n_entries < max) ? n_entries : max;
```

where `n_entries` is the **union of the same two input lists** in both functions.
Neither `alpha` nor the RRF constant affects `n_entries` — they affect only the
order in which candidates are written.

**Therefore, for any given query, all three arms return an identical
`n_results`, and so receive an identical reward.** The bandit's posteriors are
updated with a signal that is constant across its action space. It cannot prefer
any fusion mode, and whatever it converges to is an artifact of sampling noise
and the prior.

This is a silent failure of exactly the class the campaign's blog post is about:
nothing errors, the loop runs, decisions and rewards are logged, and the evidence
trail looks healthy. The reward is simply blind to what the arms do.

`recall_sufficiency_v1` is *appropriate* for `kb_memory_retrieval_limit`, where the
arms are limits and truncation is the thing being decided. It was reused for
`kb_fusion_mode`, where it measures nothing. The comment at `src/kb/kb.c:1901`
records the reuse as intentional — "same proxy as `kb_memory_retrieval_limit`" —
so this is a design slip, not an implementation bug.

### Related, and unverified by me

`learning_implicit_retrieval_outcome` (`src/modules/config/config_fields.c:297`)
and `kb_handle_memory_record_retrieval_outcome`
(`src/kb/kb_service_agent.c:520`, requires a `retrieval_event_id`) exist, and
`retrieval_event` is an **artifact kind keyed by `turn_id`**
(`src/db2/schema.sql:688-694`), not a table. I have not traced whether outcomes
recorded through that path are recoverable per candidate; that trace is a
prerequisite for the labelling half of any learning work and is called out as an
open question rather than assumed.

---

## What this means for the proposals

| campaign proposal item | actual status |
| --- | --- |
| "add BM25 + RRF hybrid retrieval" | **built.** Tune it; do not build it. |
| "RRF k=10 beats k=60" | KB path needs `RRF_K` made configurable — a small code change, not a config edit |
| "weighted RRF / multi-leg fusion" | **built** in `kb_rrf.c` for the code path |
| "score fusion preserves magnitude" | `alpha_merge` **is** score fusion; `kb_rrf`'s interface cannot express it |
| "learned fusion weights" | consumer exists (`alpha_merge`); the alpha predictor is an unfitted heuristic |
| "LTR from interactions" | inference, features, fitter, promotion gate all **built**; untrainable due to §5 |
| "use the bandit infrastructure" | **built, and live over fusion modes with a broken reward** |
| HyDE / query expansion | **built** for memory, absent for KB |
| doc2query, SPLADE, re-chunking | genuinely absent — real new work |

The remaining work is therefore mostly **repair and instrumentation**, not
construction: make the fusion reward informative, make `feature_rows` an event
log, make `RRF_K` tunable, and fit the constants that are currently guesses.
