# Source map

Every claim and quoted line in
[`your-memory-has-no-authority-model.md`](../article/your-memory-has-no-authority-model.md),
and the source line behind it.

This article is an architecture piece. It contains no runtime measurement and
makes no performance or accuracy claim about any system. Source was read on 20
and 21 August 2026 at the commits pinned in
[`source-audit-2026-08-20.md`](source-audit-2026-08-20.md).

## `aimee` source citations

The original source map is pinned to
`50c5d88d37bae618ee08b0101f163682e864ace9`, 2026-08-06, public and reachable
from `origin/agent/human-trigger-workflows`. Every file cited was verified clean
against that commit before the article was written; the working tree carried
unrelated modifications in files not cited here.

The changed typed-fact and fusion behaviour was then read at open PR 2824 head
`5a5350b99ad610cef2e6c7b758c35ad2cd8fdc9d`, 2026-08-20. Those provisional
citations are recorded below. The PR's PostgreSQL end-to-end script was inspected
but not run. This is not a publication pin: after merge, every `aimee` citation
must be repointed and re-verified against the resulting commit.

### Fusion and retrieval

| claim in the article | source |
|---|---|
| the top twelve candidates supply up to forty-eight canonical-entity seeds | PR 2824 `5a5350b9`, `src/modules/memory/memory_core_search_c.c:854-910` |
| expansion collects memories attached to a seed, then follows its direct neighbours; relation and A/B/C class affect the edge score | PR 2824 `5a5350b9`, `src/modules/memory/memory_graph_fusion.c:208-305` |
| `max_hops` is defaulted to two but is not used by the expansion; the separate two-hop helper has no production caller | PR 2824 `5a5350b9`, `src/modules/memory/memory_graph_fusion.c:208-218`; `src/modules/db2/c/entity_edges.c:1147-1166`; repository-wide caller search |
| one score with fourteen named parts | `src/modules/memory/memory_core_search_b.c:248-340` |
| lane floors for summaries and facts, session-window expansion, hard scope buckets | `src/modules/memory/memory_core_search_c.c:920-945` |

### PR 2824: provisional typed-fact repair

| claim in the article | source at `5a5350b9` |
|---|---|
| current typed facts participate in graph reads; superseded and suppressed facts do not | `src/modules/db2/c/entity_edges.c:27-39, 1102-1110` |
| relation gravity and A/B/C confidence class reach the fusion score | `src/modules/memory/memory_graph_fusion.c:26-117, 262-277` |
| fact promotion and speculative expiry run in the normal maintenance cycle | `src/modules/memory/memory_health.c:390-413` |
| `facts.retract`, `entities.merge` and `entities.unmerge` have production command handlers | `src/server/server_facts.c:18-123` |
| the storage-level retraction guard protects Class A from model authority, but the server accepts caller-declared `user` authority from a memory-write client | `src/modules/db2/c/fact_lifecycle.h:63-85`; `src/server/server_facts.c:18-47`; `src/server/server_auth.c:43-64`; `src/headers/server.h:157-164` |
| a conflicting model-authored commit on a functional relation can supersede Class A without comparing authority | `src/modules/db2/c/entity_edges.c:275-320`; `src/kb/kb_memory_facts.c:358-378` |
| orphan pruning cannot delete semantic facts | `src/modules/db2/c/entity_edges.c:749-784` |
| co-occurrence upsert and normalization cannot change a semantic fact's confirmation count | `src/modules/db2/c/entity_edges.c:78-96, 787-824` |
| the PR adds a PostgreSQL typed-fact end-to-end script containing forty-two calls to its assertion helper | `tests/e2e/typed-facts-pg-e2e.sh`; inspected, not executed for this article |
| the extractor ignores self-reported confidence and requires both endpoints to occur in the source note | `src/kb/kb_memory_facts.c:39-54, 338-346` |

### Ranking and evaluation

| claim in the article | source |
|---|---|
| the score weights are fitted from feature rows and recorded retrieval outcomes | `src/kb/kb_ranker_fit.h` |
| fitting runs from a background worker | `src/kb/kb_service_workers.c:119-130` |
| a fitted model lands as proposed and a benchmark gate must promote it | `src/kb/kb_ranker.c:155-180` |
| shadow mode records per-query rank and score deltas for fused against unfused, and is an evaluation harness rather than a production path | `src/db2/shadow_delta.h` |

### Prospective memory

| claim in the article | source |
|---|---|
| a reminder carries trigger, action, anchor entity, anchor file, recurrence, state and validity | `src/db2/schema.sql:185` |
| context assembly matches the current turn against the armed set | `src/modules/memory/memory_context.c:892` |

### The code graph

| claim in the article | source |
|---|---|
| tree-sitter extractors pull symbols, references, calls, imports and git co-change into the graph | `docs/CODE_INTELLIGENCE.md:1-4, 32` |
| the memory layer was built on top of code intelligence to make it better | first-party, supplied by the author 2026-08-20; see below |

| claim in the article | source |
|---|---|
| code nodes are prefixed keys in the same edge table | `src/modules/memory/memory_graph_fusion.c:158-165` |
| relation weights: `defines` 1.00, `contains` 0.85, `depends_on` 0.75, `calls` 0.55, `co_edited` 0.60, `co_discussed` 0.45 | `src/modules/memory/memory_graph_fusion.c:26-50` |
| a non-code-shaped query is refused entry to code subgraphs, checked per node | `src/modules/memory/memory_graph_fusion.c:186-189, 226-227` |
| mnem and Menhir also connect code and semantic memory, so the broad uniqueness claim is false | mnem `README.md:23-31`; Menhir `README.md:24-58`, at the commits in the audit |
| the narrower conjunction retained for `aimee`: native call/import graph, source-linked document fragments, endpoint-kind gate and stored assertion authority | conjunction of the code, document and write-path rows below and the expanded comparison audit |

### Documents in the same graph

| claim in the article | source |
|---|---|
| ingestion routes by format and falls through to passthrough | `src/kb/kb_ingest_normalize.c:20-47` |
| a stored fragment carries source path, whole-file content hash, heading path and line span | `src/db2/schema.sql:136`, `kb_documents` |
| fragments are doubly linked in reading order and neighbours are one hop away | `src/db2/kb_payload.c:1708-1716`, `prev_chunk_id`/`next_chunk_id` |
| office formats and HTML go through a converter; PDFs get their own extraction layer | same, plus `docs/STRUCTURED_PDF.md` |
| PDF layers are separate dependencies that degrade individually without claiming the lost capability | `docs/STRUCTURED_PDF.md` degradation table |
| structured PDF ingestion keeps page coordinates, reading order, tables as cells, OCR, extractor identity and confidence | `docs/STRUCTURED_PDF.md` layers and evidence model |
| a citation is a document hash, a page and a bounding box | same, evidence model |
| re-ingesting changed bytes creates a new version and does not move old coordinates | same |
| answerability reports weak coverage instead of producing an answer | same, retrieval |
| document mentions are embedded and resolved against canonical entities, searching up the scope lattice | `src/kb/kb_curator_resolve_entities.c:1-12` |
| the uncertain band is adjudicated by a judge rather than merged | same |
| doc to entity to code unit is a graph traversal | `src/kb/kb_curator_link_artifacts.c:5-9` |
| an endpoint answers that question | `src/kb/http/kb_http.c:997-998`, `POST /v1/implements` |
| ordinary recall refuses code subgraphs for a query with no code-shaped token, checked per token | `src/modules/memory/memory_graph_fusion.c:119-153` |
| scope is an authorisation band inside the ranking, not a filter applied afterwards | `src/db2/memory_scope_query.c:40-59`, `docs/retrieval-stack.md` |

### Cross-repo resolution

| claim in the article | source |
|---|---|
| symbols are keyed per project, so a call and its definition in another repo are unrelated nodes | `docs/proposals/done/cross-repo-dependency-graph.md` thesis |
| forty repositories on the reference deployment | same |
| the `LiStartConnection` example | same |
| every edge carries a confidence tier and its evidence, never a bare boolean | `src/db2/cross_repo_resolver.h`, §3.2 |
| top tier needs trusted-rooted corroboration by import resolution or export membership plus three call sites across three files | `cross-repo-dependency-graph.md` §3.2 (a)/(b) |
| single call site is tentative and excluded from default output | same, LOW/TENTATIVE |
| several plausible definers, or an import resolving to several files, is routed to a review queue and never guessed | `src/db2/cross_repo_resolver.h:80-99`, §3.5/§3.7 |
| a vendored copy colliding with the original routes to ambiguous | `cross-repo-dependency-graph.md` §3.7 tie-break |
| untrusted caller caps at the middle tier; untrusted definer can never lend top-tier export corroboration | same, §0 untrusted signal caps |

**One claim rests on a proposal rather than a line.** The forty-repository
figure and the `LiStartConnection` example come from the proposal's thesis
statement, which is a first-party description of the author's own deployment
rather than something the source can show. The tier machinery it describes is
verified in `cross_repo_resolver.h`.

### Time

| claim in the article | source |
|---|---|
| valid time and transaction time as separate columns | `src/db2/schema.sql:1400-1409` |
| the walk traverses only edges whose projection generation is visible on a current project | `src/db2/entity_edges.c:21-32` |
| generations move pending, visible, superseded, one visible per project | `src/db2/schema.sql:1503-1520` |

### Scope and tier

| claim in the article | source |
|---|---|
| three read-side visibility bands: active project, active workspace, shared/global; zero outside context | `src/db2/memory_scope_query.c:40-59` |
| the ranking is bound into the query as parameters | `src/db2/memory_scope_query.h:13-30`, `db2_memory_scope_bind_current` |
| scope and authorisation apply before candidates reach the result | `docs/retrieval-stack.md` |
| stable sort preserves reranker order inside a visibility band | `src/modules/memory/memory_core_search_c.c:949-985` |
| tiers L0 to L5; stable L2 promotes on confidence; L5 patterns condense across at least three sessions | `src/headers/memory.h:323-345` |
| promotion into the policy tier can require a recorded operator approval | `src/db2/memory_promotion.h:76-84`, `memory_promotion_approvals` |

### Distillation

| claim in the article | source |
|---|---|
| a durable fact in three distinct sessions is synthesised into a pattern | `src/db2/memory_promotion.c:386-410`, `COUNT(DISTINCT p.session_id) >= 3` |
| an entity corroborated by three distinct sources is promoted out of local scope | `src/kb/kb_curator_promote.c:85-95`, `HAVING COUNT(DISTINCT l.from_id) >= :minsrc`, `scope_kind <> 'global'` |
| promotion default minimum sources is three | `src/modules/config/config_kb_curator.c`, `kb_curator_promote_min_sources` |
| one store serves a person, a team or a company | `docs/STORAGE_TIERS.md` |
| promotion into a broader scope is an explicit audited write | `docs/KNOWLEDGE.md` |
| demotion runs on verdicts attributed across recalls | `src/db2/demotion.h:106-110` |

### The write path

| claim in the article | source |
|---|---|
| the write gate checks both ends against what the relation permits | `src/modules/memory/memory_fact_gate.c:14-22` |
| "never write an unvalidated semantic edge" | `src/db2/rel_types_store.c:208` |
| seventeen relations ship with the system | `src/rel_types.c:18` onward |
| the live relation set lives in a table the running system extends | `src/db2/schema.sql:1412` |
| provisional staging of a novel relation | `src/db2/rel_types_store.c:255-270` |
| a sighting counts only after its fact committed; a rejected relation keeps that verdict | `src/db2/ontology_evolution.c:41-46` |
| relation sightings are an occurrence count keyed only by relation type, with no distinct-source field | `src/db2/ontology_evolution.c:24-55` |
| auto-promotion sweep, catch-all exclusion | `src/kb/kb_curator_drain.c:800-828` |
| auto-promote default on, threshold 3 | `src/modules/config/config_kb_curator.c:74-76` |
| the class a fact is born into, and Class A unreachable from a model | `src/db2/fact_lifecycle.c:48-59` |
| Class A carries full confidence; B and C sit below it | `src/db2/fact_lifecycle.c:26-32` |
| a confirmed Class B fact stops expiring and never becomes A | `src/db2/fact_lifecycle.h:58-61` |
| extractor pinned to `FACT_AUTHORITY_MODEL` | `src/kb/kb_memory_facts.c:300-305` |
| at the baseline commit, model confidence was used as a 0.6 floor | `src/kb/kb_memory_facts.c:39`, applied at `:281`; superseded by the PR-head finding above |
| unconfirmed speculation expires by being stamped, not removed | `src/db2/fact_lifecycle.c:83-86` |
| `supersede` / `hard_delete` / `immutable` semantics | `src/db2/fact_lifecycle.h:62-85` |
| a model authority cannot retract a Class A edge | `src/db2/fact_lifecycle.h:77-82` |
| endpoint canonicalisation before the edge write | `src/db2/rel_types_store.c:155-183` |
| surrogate `canonical_id`, single-hop aliases | `src/db2/schema.sql:1443-1456` |
| merge audit and `unmerge` | `src/db2/entity_registry.c:242-408` |
| ambiguity queued in `entity_name_conflicts` | `src/db2/schema.sql:1465-1472` |

### Curation

| claim in the article | source |
|---|---|
| demotion verdict tokens | `src/db2/demotion.h:28-32` |
| "reads only attributed outcome evidence", quoted | `src/db2/demotion.h:106-110` |
| the scorer declines below a floor of recorded outcomes | `src/db2/demotion.c:771-773` |
| contradiction keeps both claims | `docs/CURATOR_PIPELINE.md` |
| curiosity gap types | `src/db2/curiosity.h:25-29` |
| abstention default-off, threshold uncalibrated | `docs/proposals/done/retrieval-abstention-confidence-gate.md` |

### Product facts

| claim in the article | source |
|---|---|
| memory subsystem is 34,000 lines of C | `wc -l` over `src/modules/memory/*.c`, `src/db2/memory_*.c`, `src/db2/{typed_facts,rel_types_store,ontology_evolution,demotion}.c`, `src/db2/fact_*.c`, `src/db2/entity_*.c`, `src/rel_types.c`: 34,115 lines, rounded down |
| thirty-one memory test files | `ls src/tests/ \| grep -icE '^test_(memory\|fact\|entity\|ontology\|rel_types\|curiosity\|demotion\|directive\|kb_curator\|extract)'` |
| AGPL-3.0 | `LICENSE`, `NOTICE` |
| clone, `docker compose up`, browser wizard | `docs/QUICKSTART.md:5-14, 80-102` |
| seven wizard steps, one optional and two local-only | `frontend/src/setup/wizardSteps.ts:39-55` |
| Graphiti requires an external graph database | `graphiti` README:169-184, `c4069327` |
| PostgreSQL with pgvector | `docs/STORAGE_TIERS.md` |
| teaching a domain up front from its documentation is human-approvable | `docs/proposals/done/typed-fact-knowledge-layer.md` §2 |

## First-party development history

Rakuen is the primary source for how and why it built its own software. The
article states that history directly in first person.

**Origin and name.** The software began about a year ago as `aimem`, a code
graph with a small fact memory built to meet a production need. Supplied by the
author on 2026-08-21.

**Production-driven expansion.** Engineers used it on live work, and the
failures they found drove the subsequent memory features. The author describes
those users as demanding and the resulting code as heavily exercised in
production. Supplied 2026-08-21.

**The build order.** Memory grew on top of code intelligence rather than the
other way around. Supplied 2026-08-20 and expanded 2026-08-21. The source
corroborates the resulting shape: code nodes are first-class in the shared edge
table, and the relation weights rank code relations above conversational ones.

**Current product scope.** `aimee` is a general-purpose memory solution for use
across an organisation, not a code-memory product. Supplied by the author on
2026-08-21. The article's tours of documents, scoped team memory and prospective
memory show what that scope includes. Its code graph is valuable because that
broader memory lets an implementation connect to source documents and
real-world consequences.

**Core product goal.** Connect any part of an organisation to any other, and
retain the historical record of decisions: how the organisation arrived at the
current position, what is running now, and its exact behaviour. Supplied by the
author on 2026-08-21. The article grounds that goal in versioned documents,
conversation history, visible code generations and line-level citations.

The public repository begins with a snapshot import on 2026-06-03. That git
history does not contain the preceding development period; it neither
corroborates nor contradicts the author's account.

**"the system Rakuen runs."** First-party, supplied 2026-08-20. This claim was
cut from the article, but remains recorded here.

**"34,000 lines of C."** Computed, not read off a line. A `wc -l` over the file
set above on the working tree on 2026-08-20, counting comments and blank lines,
where the file set is a judgement about what counts as the memory subsystem. It
is an order-of-magnitude claim in the piece and is used as one.

## Expanded comparison sources

| article claim | source |
| --- | --- |
| Hindsight is persistent MCP agent memory with world facts, experiences, observations and mental models, plus semantic, keyword, graph and temporal recall | Hindsight `README.md:201-324`, `3de41af8` |
| Hindsight facts point to retained documents and carry occurred start/end; MCP invalidation archives reversibly, while MCP document deletion permanently removes linked facts | Hindsight initial schema `:199-214,264-305`; invalidation migration `:1-26`; `mcp_tools.py:3492-3574,3742-3803`; `writes.py:137-155`, `3de41af8` |
| MemOS stores source roles and locators plus archived versions; MCP deletion reaches hard graph deletion | MemOS `item.py:16-214`; `mcp_serve.py:399-416`; `neo4j.py:412-429`, `be68e2fb` |
| mnem ingests code, documents and conversations into a versioned graph; its schema tree does not yet enforce endpoint kinds | mnem `README.md:23-31`; `pipeline.rs:270-402`; `commit.rs:1-52`; `repo/transaction.rs:704-793`, `2a8a3698` |
| Menhir shares structural code and semantic memory in Neo4j, grounds claimed user authority in turn evidence, reserves promotion and erasure for operator tier, and type-checks work-artifact links | Menhir `README.md:24-58,116-170`; `admission_gate.py:1-154`; `promote_memory.py:9-71`; `delete_memory.py:9-92`; `work_artifact.py:315-379`; `work_artifact_repository.py:1250-1304`, `4e4f39ed` |
| Menhir's scalar-state and event-history recall authority remain default-off | Menhir `.agent/default-off-features.md:1-13,35-38`, `4e4f39ed` |
| Neo4j Agent Memory carries source IDs and valid-time bounds, while its MCP fact tool accepts an untyped triple and no source ID | Neo4j Agent Memory `long_term.py:228-308,825-920`; `_tools.py:243-278`, `5b4e00af` |
| Memori links facts to conversations but has no authority or valid-time field; host deletion is not in the shipped agent tool | Memori SQLite migration `:75-197`; `recall.py:193-211`; OpenClaw tool inventory and `memori-recall.ts:1-145`, `538b61f2` |
| Supermemory docs claim `isInference`, down-ranking, review and AST-aware code chunking, but self-hosting installs a packaged binary whose engine source is absent from the repository | Supermemory `memory-review.mdx:8-36`; `super-rag.mdx:95-122`; `self-hosting/overview.mdx:1-31`; `self-hosting/quickstart.mdx:8-58`; repository tree at `34876664` |

## Comparison-table cells

Each cell of the thirteen-system table is sourced in
[`source-audit-2026-08-20.md`](source-audit-2026-08-20.md), which records the
commit, the file and the reasoning for every verdict, including the cells where
a one-word answer understates a project's design.
