# Source map

Every claim and quoted line in
[`your-memory-has-no-authority-model.md`](../article/your-memory-has-no-authority-model.md),
and the source line behind it.

This article is an architecture piece. It contains no measurement, first-party
or otherwise, and makes no performance or accuracy claim about any system. All
source was read on 2026-08-20 at the commits pinned in
[`source-audit-2026-08-20.md`](source-audit-2026-08-20.md).

## `aimee` source citations

Commit `50c5d88d37bae618ee08b0101f163682e864ace9`, 2026-08-06, public, reachable
from `origin/agent/human-trigger-workflows`. Every file cited was verified clean
against that commit before the article was written; the working tree carried
unrelated modifications in files not cited here.

### Fusion and retrieval

| claim in the article | source |
|---|---|
| top candidates supply canonical entities as walk seeds; graph-reachable memories the vectors missed are added | `src/modules/memory/memory_core_search_c.c:846-905` |
| two hops by default, utility-weighted, bounded seed and neighbour counts | same |
| one score with fourteen named parts | `src/modules/memory/memory_core_search_b.c:248-340` |
| lane floors for summaries and facts, session-window expansion, hard scope buckets | `src/modules/memory/memory_core_search_c.c:920-945` |

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

### Documents in the same graph

| claim in the article | source |
|---|---|
| ingestion routes by format and falls through to passthrough | `src/kb/kb_ingest_normalize.c:20-47` |
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
| four scope kinds, ranked project over workspace over global, zero outside context | `src/db2/memory_scope_query.c:40-59` |
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
| auto-promotion sweep, catch-all exclusion | `src/kb/kb_curator_drain.c:800-828` |
| auto-promote default on, threshold 3 | `src/modules/config/config_kb_curator.c:74-76` |
| the class a fact is born into, and Class A unreachable from a model | `src/db2/fact_lifecycle.c:48-59` |
| Class A carries full confidence; B and C sit below it | `src/db2/fact_lifecycle.c:26-32` |
| a confirmed Class B fact stops expiring and never becomes A | `src/db2/fact_lifecycle.h:58-61` |
| extractor pinned to `FACT_AUTHORITY_MODEL` | `src/kb/kb_memory_facts.c:300-305` |
| model confidence used only as a 0.6 floor | `src/kb/kb_memory_facts.c:39`, applied at `:281` |
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

## Claims that are not code citations

Three claims in the piece do not resolve to a line, and each is marked here
rather than left to look like the others.

**"in production for about a year."** First-party, supplied by the author on
2026-08-20 and not independently verifiable. The public repository's first
commit is 2026-06-03 and is a snapshot import, so the public git history neither
corroborates nor contradicts it. The article states the snapshot fact in the
same paragraph so a reader who checks the repository is not left with an
apparent conflict.

**"the system Rakuen runs."** First-party, same basis. The article's standfirst
discloses the interest.

**The build order.** That the memory layer grew out of code intelligence, and
was built to make it better, is the author's account of his own project,
supplied 2026-08-20. The public repository begins at a snapshot import so the
history that would show it is not visible. What the source does corroborate is
the shape the claim predicts: code nodes are first-class in the shared edge
table, and the relation weights rank code relations above conversational ones.

**"34,000 lines of C."** Computed, not read off a line. A `wc -l` over the file
set above on the working tree on 2026-08-20, counting comments and blank lines,
where the file set is a judgement about what counts as the memory subsystem. It
is an order-of-magnitude claim in the piece and is used as one.

## Comparison-table cells

Each cell of the seven-system table is sourced in
[`source-audit-2026-08-20.md`](source-audit-2026-08-20.md), which records the
commit, the file and the reasoning for every verdict, including the cells where
a one-word answer understates a project's design.
