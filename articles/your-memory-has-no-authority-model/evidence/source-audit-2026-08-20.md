# Source audit: thirteen-system comparison and one research reference

Dates of audit: 2026-08-20 and 2026-08-21.

Method: each external repository was cloned with `git clone --depth 1` from its
public GitHub origin on the audit date and the resulting `HEAD` was recorded
before reading. The six added inspectable systems and Supermemory were cloned
on 2026-08-21. `aimee` was read from the local checkout as described below. No
repository was modified. Every comparison-table verdict below cites a file and
line range in the committed tree at that commit. First-party documentation in
those trees was read to establish each project's own product and architecture
claims; implementation verdicts were checked against source rather than inferred
from a third-party summary or a model's description of a project.

Thirteen inspectable systems appear in the article's comparison table. A-MEM
was read as a research-only reference and is recorded below without a table
row. Supermemory was also reviewed, but its self-hosted memory engine is a
packaged binary whose implementation is not present in the public repository.
It is recorded as an audit limit, not scored as a negative row.

The baseline `aimee` audit used
`50c5d88d37bae618ee08b0101f163682e864ace9`, which is public and reachable from
`origin/agent/human-trigger-workflows`. Every file in that audit was verified
byte-identical to the commit before writing. The article's provisional `aimee`
row was then re-read from the head of open PR 2824,
`5a5350b99ad610cef2e6c7b758c35ad2cd8fdc9d`. That second read was static: the PR's
PostgreSQL end-to-end script was inspected but not run. Files carrying unrelated
working-tree modifications were not cited.

## Commits

| system | repository | commit | commit date |
|---|---|---|---|
| `aimee` baseline | `RakuenSoftware/aimee` | `50c5d88d37bae618ee08b0101f163682e864ace9` | 2026-08-06 |
| `aimee` article row, open PR 2824 | `RakuenSoftware/aimee#2824` | `5a5350b99ad610cef2e6c7b758c35ad2cd8fdc9d` | 2026-08-20 |
| Graphiti | `getzep/graphiti` | `c406932767ee490ad2311fd694a6b2ac3b164599` | 2026-08-20 |
| cognee | `topoteretes/cognee` | `fd5045f6b60522c1953fc1ae258e041ba53602d8` | 2026-08-19 |
| mem0 | `mem0ai/mem0` | `3599aa75ed64ee41c3b1d8133a8b39403fb8f703` | 2026-08-20 |
| Letta Code | `letta-ai/letta-code` | `d1dc6880971dc55a5e5dfcf845d4cba740b14585` | 2026-08-20 |
| LangMem | `langchain-ai/langmem` | `29cbe41e58528f92e9efa773c12e15c47be3808c` | 2026-08-10 |
| Memobase | `memodb-io/memobase` | `358c16bbc6d687937d79bc2f984a11c3be8da901` | 2026-01-11 |
| A-MEM | `agiresearch/A-mem` | `ceffb860f0712bbae97b184d440df62bc910ca8d` | 2025-12-12 |
| Hindsight | `vectorize-io/hindsight` | `3de41af867582c810309d6ea4c1b1de9d0ed9b7e` | 2026-08-21 |
| MemOS | `MemTensor/MemOS` | `be68e2fb5370866bd5e2b188bb3d22bd13b49e09` | 2026-08-20 |
| mnem | `Uranid/mnem` | `2a8a36985dbcf107378a76daeeef7154691220e7` | 2026-06-01 |
| Menhir | `Archolith/menhir` | `4e4f39ed388a1c689740a7d48daade9fbc79c000` | 2026-08-20 |
| Neo4j Agent Memory | `neo4j-labs/agent-memory` | `5b4e00af88342707d011bb9d4f2b34503f43a8c3` | 2026-08-19 |
| Memori | `MemoriLabs/Memori` | `538b61f245295aa1a43df8033879f8293627f74d` | 2026-07-28 |
| Supermemory, engine not scored | `supermemoryai/supermemory` | `34876664810a43a55954a0a83571662a3bd333b8` | 2026-08-20 |

`letta-ai/letta` was also cloned (`87fd37aa`, 2026-08-15) and found to contain no
source. Its README states the repository "now serves as a landing page" and that
the V1 server source is preserved on an `archive` branch that "receives no fixes
or security updates, and should not be used in production." The audit therefore
covers `letta-ai/letta-code`, which the README names as the current source. The
`archive` branch was not read.

## Column definitions

The article's table has six judged columns. Each is a question with a stated
test, so a reader can disagree with a verdict by applying the same test.

- **Typed write gate.** Does a candidate relation get checked against declared
  subject/object type constraints, with a failing candidate refused a row? A
  constraint that only shapes what an extraction prompt is shown is not a write
  gate, because the store still accepts whatever the model returns.
- **Authority classes.** Does a stored fact carry a field, enforced at write,
  that separates a user assertion from a model inference and ranks them?
- **Valid time.** Can the store answer "when was this true in the world",
  separately from "when did the system believe it"?
- **Correction or removal path.** Can a tool call or pipeline step available to
  the model make prior content non-current or unreadable? Does the old content
  survive as an expired row, archive, tombstone or version? A destructive tool
  requiring an operator credential is recorded as operator-only rather than as
  an ordinary model permission.
- **Fragment points at its source.** Can the unit retrieval returns be used to
  reach the whole source it came from? Retaining the source somewhere in the
  system is not sufficient; the question is whether the retrieved thing carries
  a path back.
- **Commit.** The pinned tree the answer was read from.
- **Memory and code in one graph.** Does the implementation natively ingest
  source code into the same queryable graph as semantic memory? Code stored as
  an undifferentiated text blob does not pass. Function- or class-level code
  chunks do pass, but are distinguished from a call/import structure graph in
  the cell text.

## Per-system findings

### `aimee`

#### Baseline audit: `50c5d88d`

- Write gate: `src/modules/memory/memory_fact_gate.c:14-22` returns
  `FACT_GATE_REJECT_KIND` on a kind violation;
  `src/db2/rel_types_store.c:207-208` returns before any write on that verdict.
  The gate is the only setter of `edge_class = 'semantic'`.
- Authority classes: `src/db2/fact_lifecycle.c:48-59`. `FACT_CLASS_A` is
  unreachable from `FACT_AUTHORITY_MODEL`. `db2_fact_promote_durable` raises a
  Class B confidence to 0.8 and is documented as never promoting to A
  (`src/db2/fact_lifecycle.h:58-61`).
- Valid time: `valid_from` / `valid_until` on `entity_edges`, separate from
  `superseded_at` (`src/db2/schema.sql:1400-1409`).
- Model removal: no at the storage primitive. `db2_fact_retract` skips Class A
  rows for a non-user authority and `hard_delete` is a `suppressed` flag with
  the row retained (`src/db2/fact_lifecycle.h:62-85`). The audit later found
  that this primitive had no production caller at the baseline.

The baseline did not deliver the product behaviour the row implied. Typed facts
were excluded from graph traversal, relation gravity was not passed into fusion,
the fact lifecycle was not scheduled, and there was no production retraction or
entity-unmerge surface. Generic maintenance could also delete semantic facts or
rewrite their confirmation counts.

#### Provisional article row: PR 2824 head `5a5350b9`

- Write gate: `src/modules/memory/memory_fact_gate.c:12-42` checks both endpoint
  kinds. `src/modules/db2/c/rel_types_store.c:199-234` refuses kind failures and
  bad arguments before the semantic-edge write.
- Authority classes: `src/modules/db2/c/fact_lifecycle.c:26-60` assigns A, B or
  C, with Class A unreachable from model authority. Promotion and expiry retain
  the class and the row (`:62-121`).
- Valid time: `valid_from` / `valid_until` remain on `entity_edges`, while
  `asserted_at`, `superseded_at` and `suppressed` carry transaction-time and
  correction state (`src/modules/db2/c/schema.sql:88, 1794-1803`).
- Model removal: yes, by conflicting commit. The explicit retraction contract
  skips Class A rows for non-user authority and retains the row under a
  supersession stamp or tombstone (`src/modules/db2/c/fact_lifecycle.h:63-85`).
  PR 2824 exposes that contract through `facts.retract`
  (`src/server/server_facts.c:18-69`). The ordinary semantic upsert is different:
  for a functional relation it supersedes a prior object without comparing the
  old and new authority classes (`src/modules/db2/c/entity_edges.c:275-320`).
  The model extractor reaches that path with `FACT_AUTHORITY_MODEL`
  (`src/kb/kb_memory_facts.c:358-378`). The old Class A row remains stored but is
  no longer current.
- Recall: graph readers admit current semantic rows and exclude superseded or
  suppressed ones (`src/modules/db2/c/entity_edges.c:27-39, 1102-1110`). Fusion
  now scores the traversed relation and the fact's A/B/C class
  (`src/modules/memory/memory_graph_fusion.c:26-117, 262-277`).
- Lifecycle and maintenance: fact promotion and speculative expiry are scheduled
  in the normal maintenance cycle (`src/modules/memory/memory_health.c:390-413`).
  Orphan pruning and weight normalization exclude semantic rows, and the generic
  co-occurrence upsert cannot increment a fact's confirmation count
  (`src/modules/db2/c/entity_edges.c:78-96, 749-824`).
- Extractor confidence: the current extractor ignores the model's reported
  confidence and instead requires both endpoints to occur in the source note
  (`src/kb/kb_memory_facts.c:39-54, 338-346`). This corrects the baseline audit's
  description of a 0.6 floor.

PR 2824 adds `tests/e2e/typed-facts-pg-e2e.sh`, which contains forty-two calls to
its assertion helper over the PostgreSQL typed-fact path. This audit did not
execute the script. The PR remains open, so its head is evidence for a draft
product tour, not a final publication pin.

Scope: this row covers the typed-fact layer only, which is the layer the article
describes. Free-text prose memory has separate write semantics and is not
audited here.

### Graphiti

- Write gate: no. `extract_edges` validates that the LLM's entity names appear
  in the node list and drops self-edges
  (`graphiti_core/utils/maintenance/edge_operations.py:210-241`); the relation
  name is taken as returned and becomes the edge's `name`
  (`:300-303`). `edge_type_map` selects which custom type definitions are put in
  the extraction prompt's context (`:458-486`). That shapes the request. The
  response is written as returned.
- Authority classes: no. `EntityEdge`
  (`graphiti_core/edges.py:262-283`) carries `name`, `fact`, `episodes`,
  temporal fields and free-form `attributes`. `grep` for `provenance`,
  `authority` and `confidence` across `edges.py` and `nodes.py` returns nothing.
- Valid time: yes. `valid_at` and `invalid_at` are the real-world interval;
  `expired_at` is the transaction-time close.
- Model removal: contradicted edges are expired and the rows kept
  (`resolve_edge_contradictions`, `edge_operations.py:538+`). `EntityEdge.delete`
  exists as an explicit API call and is not on the ingestion path.

This is the strongest competing design in the set and the article says so.

### cognee

- Write gate: optional and used for enrichment. The default resolver is built
  with `ontology_file=None`
  (`cognee/modules/ontology/get_default_ontology_resolver.py:10-12`). When a
  file is supplied, extracted names are fuzzy-matched to ontology nodes to
  attach a canonical name, URI and subgraph
  (`cognee/modules/ontology/construct_data_points_and_edges_with_ontology.py:32-55`);
  a name with no match returns `None` and the extracted node is still
  constructed.
- Authority classes: no field found.
- Valid time: partial. `temporal_conflict_resolver` ranks by the edge's own
  `updated_at`, which records assertion recency. There is no real-world
  interval.
- Model removal: no. Superseded edges are tagged `superseded`, `superseded_by`
  and `supersession_reason` and retained
  (`cognee/modules/graph/utils/temporal_conflict_resolver.py:39-95`).
- Contradiction detection defaults to `False`
  (`cognee/modules/cognify/config.py:13-17`), and the temporal resolver is an
  opt-in task requiring the caller to name single-valued relationships.

The docstring quoted in the article is at
`cognee/modules/graph/utils/temporal_conflict_resolver.py:13-16`.

### mem0

- Write gate: no. Memories are free-text sentences.
- Authority classes: no. The additive extraction prompt asks the model to
  attribute in prose ("use \"User\" for user-stated facts"), which is a string
  convention. No field carries it
  (`mem0/configs/prompts.py:472-495`).
- Valid time: no. An observation-date anchor resolves relative references
  during extraction and is not stored as an interval.
- Model removal: not on the current OSS path. `main.py:940-1010` calls
  `generate_additive_extraction_prompt` and the release notes describe
  "Single-pass ADD-only (one LLM call, no UPDATE/DELETE)"
  (`docs/migration/oss-v2-to-v3.mdx:19`). The prior design's `_delete_memory`
  (`mem0/memory/main.py:2100-2122`) removes the vector row and writes a history
  row with the prior value and `is_deleted=1`. It is retained in the tree and
  its only remaining callers are the explicit `delete(memory_id)` (`:1882`) and
  `delete_all()` (`:1934`) API calls. The extraction path does not reach it.
- Graph memory removed from OSS: `docs/migration/oss-v2-to-v3.mdx:41`.

The article credits ADD-only as an improvement on the LLM-chooses-DELETE design
and notes what it costs: nothing reconciles two memories that contradict.

### Letta Code

- Write gate, authority classes, valid time: none found. Memory is text in
  blocks.
- Model removal: yes. `MEMORY_TOOL_NAMES` is `memory`, `memory_apply_patch`,
  `memory_insert`, `memory_replace`, `memory_rethink`
  (`src/tools/toolset.ts:61-68`), described in the file's own comment as
  "Server-side memory tool names that can mutate memory blocks."
- Mitigation credited in the article: MemFS tracks all context including memory
  blocks in git (`README.md:24`), so a destructive rewrite leaves a commit.

The server that stores the blocks is not in this repository, so no claim is made
about its schema.

### LangMem

- Write gate, authority classes, valid time: none found.
- Model removal: yes, unconditional. `create_manage_memory_tool` permits
  `create`, `update` and `delete` by default
  (`src/langmem/knowledge/tools.py:34-36`); the delete branches are
  `await store.adelete(namespace, key=str(id))` (`:293-294`) and
  `store.delete(namespace, key=str(id))` (`:327-328`). No history row is
  written by either.

### Memobase

- Write gate: a slot schema. Profiles are topic/subtopic slots
  (`src/server/api/example_config/`), which constrains where an attribute lands.
  It says nothing about the types of two entities in a relation.
- Authority classes: no field found.
- Valid time: no. Dates appear inside the memo text as `[mentioned on ...]`
  annotations. No column carries them.
- Model removal: yes. `UPDATE` in the merge prompt means "rewrite the updated
  memo"
  (`src/server/api/memobase_server/prompts/merge_profile.py:34-46`); the prior
  text does not survive.

### A-MEM

Read but excluded from the table. Memories are notes with LLM-generated
Zettelkasten links (`agentic_memory/memory_system.py`). No ontology, authority
or temporal layer. The README states the paper-reproduction code lives in a
different repository. Last commit 2025-12-12. The article names it and states
that it is not being held to a production bar.

### Hindsight

- Product status and retrieval: the repository presents Hindsight as persistent
  agent memory, including a built-in MCP endpoint, rather than as a research
  implementation (`README.md:201-267`;
  `hindsight-docs/blog/2026-03-04-mcp-agent-memory.md:22-66`). Its first-party
  guide describes semantic search, BM25, graph traversal and temporal filtering
  as four parallel recall strategies (`:73-91`). World facts, experiences,
  observations and mental models are stored with entity, relationship, temporal,
  sparse and dense representations (`README.md:271-324`). Those are memory
  content types, not fields ranking who asserted a fact.
- Source path: `memory_units.document_id` has a composite foreign key to
  `documents`, whose row retains `original_text` and a content hash
  (`hindsight-api-slim/hindsight_api/alembic/versions/5a366d414dce_initial_schema.py:199-214,264-305`).
- Valid time: `occurred_start` and `occurred_end` are separate from
  `created_at` and `updated_at` in the same schema (`:273-284`).
- Correction: the curation migration moves invalidated facts out of the live
  table into a cold archive, excludes them from recall, consolidation and graph
  queries, retains the reason and time, and supports restoring entity links
  (`hindsight-api-slim/hindsight_api/alembic/versions/c9a1b2d3e4f5_add_invalidated_memory_units.py:1-26,50-89`).
  `invalidate_memory` is an MCP tool and describes the operation as fully
  reversible (`hindsight-api-slim/hindsight_api/mcp_tools.py:3492-3574`).
- Document management: the MCP surface also registers `delete_document`, whose
  contract permanently removes the document and all associated memories
  (`hindsight-api-slim/hindsight_api/mcp_tools.py:3742-3803`). The SQL store
  explicitly deletes every linked memory unit before the document row
  (`hindsight-api-slim/hindsight_api/engine/memories/pg/writes.py:137-155`).
  This is a hard-removal path beside reversible fact invalidation.
- Gate and authority: no stored user-versus-model authority rank or
  endpoint-kind relation gate was found. `fact_type` distinguishes world,
  opinion, observation and bank facts; it does not identify the declarant.

### MemOS

- Provenance: `SourceMessage` carries role, message ID, source snippet,
  document path, file information and arbitrary extra locators
  (`src/memos/memories/textual/item.py:16-46`). A memory node can carry a list
  of those sources (`:175-214`).
- History: `ArchivedTextualMemory` preserves the prior content, version,
  update type and a link to a full archived node with sources and embedding
  (`:49-92`). Current metadata stores status, version, history, confidence,
  source, visibility and update time (`:94-168`).
- Retrieval: `GraphMemoryRetriever` combines graph and vector retrieval and
  can add BM25; it returns history and source fields
  (`src/memos/memories/textual/tree_text_memory/retrieve/recall.py:16-52` and
  the `GraphMemoryRetriever` implementation in the same file).
- Deletion: the shipped MCP server registers `delete_memory` and calls the MOS
  delete path (`src/memos/api/mcp_serve.py:399-416`). The Neo4j store executes
  `DETACH DELETE` for individual and filtered memory deletion
  (`src/memos/graph_dbs/neo4j.py:412-429,1896-2020`).
- Governance limit: the architecture introduction says every lifecycle step is
  versioned with provenance and audit logs, and names `MemLifecycle` and
  `MemGovernance` for access control, redaction, compliance and audit
  (`docs/en/open_source/home/memos_intro.md:39-66`). The core source search found
  those two names only in descriptive prompts, not like-for-like runtime
  modules. The table therefore credits implemented provenance and archived
  versions, but not a general audit or governance enforcement layer.
- Gate, authority and time: source role and confidence do not form an enforced
  assertion-authority order. The graph edge writer accepts a caller-provided
  type after matching two `Memory` nodes, with no endpoint-kind constraint
  (`src/memos/graph_dbs/neo4j.py:431-450`). Event metadata and an archived
  `timespec` exist, but the general current memory model has no world-valid
  interval separate from its created and updated timestamps.

### mnem

- Fused graph: the public ingest path accepts source code, PDFs, Markdown,
  conversation exports and directories. Code is split at functions and classes;
  skills, decisions and conventions live as nodes and typed edges in the same
  knowledge graph (`README.md:23-31`). The pipeline writes each chunk and a
  `chunk_of` edge back to its document (`crates/mnem-ingest/src/pipeline.rs:270-320,354-402`).
- Versioning and provenance: every commit points to node, edge and schema tree
  roots and carries author, agent, task and time provenance
  (`crates/mnem-core/src/objects/commit.rs:1-52` and the remaining `Commit`
  fields in that file). This versions the graph as a whole; it does not rank the
  authority of each assertion.
- Deletion: tombstones leave the node and prior commits intact while default
  retrieval filters it, and the MCP surface exposes both deletion and
  tombstoning (`crates/mnem-core/src/objects/tombstone.rs:1-21`;
  `crates/mnem-mcp/src/tools/descriptions.rs:281-319`). The result is
  reversible history, not hard erasure.
- Gate and time: transaction validation checks graph integrity, but the schema
  tree is unchanged because schema mutation and endpoint validation are not yet
  implemented (`crates/mnem-core/src/repo/transaction.rs:704-793`). Creation and
  commit times are not a separate world-valid interval.

### Menhir

- Fused graph: files, symbols, imports, calls, tests, endpoints, dependencies
  and cross-project references share one Neo4j graph with semantic memory
  (`README.md:24-58,84-108`). `ANCHORED_TO` links memories to resolved code
  paths while the original episode remains provenance (`README.md:116-126`).
- Authority: `NodeScope` includes `CANDIDATE`, `SESSION`, `PERSISTENT` and
  `PROMOTED` (`src/menhir/domain/models.py:21-31`). A claimed user or manual
  source must be grounded in retained turn evidence; failures downgrade it to
  `agent_inference` (`src/menhir/domain/truth/admission_gate.py:1-5,57-154`).
  The ordinary `add_memory` tool documents the same fail-closed rule
  (`src/menhir/mcp/tools/ingest/add_memory.py:22-35`).
- Operator controls: `promote_memory` requires the operator tier and only
  promotes persistent memory (`src/menhir/mcp/tools/ingest/promote_memory.py:9-71`).
  `delete_memory` also requires the operator tier and runs an erasure path that
  reports residual content instead of claiming a complete purge
  (`src/menhir/mcp/tools/ingest/delete_memory.py:9-92`).
- Provenance and history: candidates are withheld pending review, promoted
  memory is protected from normal merge handling, and superseded content is
  retained for historical queries (`README.md:141-170`). Typed assertions keep
  source spans and contribute to rebuildable current and history views
  (`README.md:208-233`).
- Time: the temporal and typed-assertion paths carry world-valid timestamps and
  preserve belief-time metadata separately. The temporal test suite exercises
  `valid_at` and `invalid_at` as distinct fields.
- Typed gate: work-artifact relations have declared source and target artifact
  types, and the repository reads the stored types before refusing an illegal
  pairing (`src/menhir/domain/work_artifact.py:315-379`;
  `src/menhir/infrastructure/work_artifact_repository.py:1250-1304`). This gate
  does not cover arbitrary edges extracted into the general semantic-memory
  graph.
- Limits: scalar-state recall authority and event-history recall authority are
  shipped but default-off
  (`.agent/default-off-features.md:1-13,35-38`). Menhir therefore falsifies the
  broad authority and code-memory claims, but not the narrower conjunction in
  the article.

### Neo4j Agent Memory

- Graph scope: conversations, messages, entities, preferences, facts,
  reasoning traces and tool usage are first-class Neo4j nodes. The system can
  adopt an existing graph, but it has no native source-code structure model
  (`README.md:1-43`).
- Source: entity and fact models include a source message or document ID
  (`src/neo4j_agent_memory/memory/long_term.py:228-251,299-308`), and extracted
  entities receive `EXTRACTED_FROM` edges to messages
  (`src/neo4j_agent_memory/graph/queries.py:865-925`). The direct MCP fact tool,
  however, does not accept or populate `source_id`
  (`src/neo4j_agent_memory/mcp/_tools.py:243-278`).
- Time and correction: fact and relationship models carry `valid_from` and
  `valid_until` (`src/neo4j_agent_memory/memory/long_term.py:274-308`). Preference
  consolidation retains a `SUPERSEDED_BY` edge and closes `valid_until`
  (`src/neo4j_agent_memory/memory/consolidation.py:245-301`).
- Gate and authority: the MCP fact tool accepts subject, predicate and object
  strings plus confidence and arbitrary metadata. No endpoint-kind refusal or
  enforced user-versus-model authority rank was found. Explicit and inferred
  preferences share the same confidence field.
- Removal: no fact-delete tool was found in the shipped MCP profiles. Archival
  and consolidation operations do not establish that an ordinary model can
  hard-delete an individual fact.

### Memori

- Data model: BYODB stores entity facts and subject-predicate-object graph rows
  in relational tables. Facts carry frequency and transaction timestamps but no
  assertion authority or world-valid interval
  (`core/src/storage/migrations/sqlite.rs:75-173`).
- Source path: `memori_entity_fact_mention` links a fact to the conversation in
  which it appeared (`core/src/storage/migrations/sqlite.rs:177-197`).
- Classification is not authority: the OpenClaw recall tool validates pairs
  such as `fact` / `verification` and `insight` / `inference`, but these are
  retrieval filters, not a field deciding which speaker may overrule another
  (`integrations/openclaw/src/tools/memori-recall.ts:34-127`).
- Deletion: the host library can hard-delete the knowledge graph and facts for
  an entity (`memori/memory/recall.py:193-211`). The shipped OpenClaw agent tools
  expose recall, summaries, compaction and feedback, not this delete method.
- Code and gate: no native code parser or code-structure graph was found. Triple
  insertion accepts extracted subject, predicate and object values without an
  endpoint-kind schema gate (`core/src/storage/drivers/sqlite.rs:430-520`).

### Supermemory: documentation reviewed, engine not auditable

- The self-hosting overview says the local product uses the same ingestion,
  extraction, hybrid-search and graph engine as the hosted platform, delivered
  as one self-contained binary (`apps/docs/self-hosting/overview.mdx:1-31`).
  The quickstart says the installer downloads an architecture-specific binary
  and points to `server-v*` release tags (`apps/docs/self-hosting/quickstart.mdx:8-58`).
- The documentation describes `isInference`, down-ranking inferred memories
  below stated facts, and approve, decline and undo review operations
  (`apps/docs/recall/memory-review.mdx:8-36`). It also describes update,
  extension and derivation edges with retained history
  (`apps/docs/concepts/graph-memory.mdx:41-101`).
- The documentation also says code is split at AST boundaries so functions,
  classes and imports stay coherent (`apps/docs/concepts/super-rag.mdx:95-122`).
  That is code-aware ingestion, but it does not by itself show a native code
  relationship graph joined to temporal memory.
- A recursive tree listing at `34876664` found the web applications,
  documentation, SDK-facing code and MCP server, but no implementation source
  for `supermemory-server` or its embedded graph engine. The advertised
  authority, temporal and correction behavior therefore cannot be verified at
  the write or recall paths from this repository. Supermemory is excluded from
  the scored denominator rather than marked no.

## Source retention and fragment provenance

Added 2026-08-20 as a judged column. The test: can the unit retrieval returns be
used to reach the whole source it came from?

- **`aimee`** — the fragment carries source path, whole-file content hash,
  heading path and line span, and is doubly linked to its neighbours in reading
  order (`src/db2/schema.sql:136`, `src/db2/kb_payload.c:1708-1716`).
- **Graphiti** — `EpisodicNode.content` holds raw episode data
  (`graphiti_core/nodes.py:319-321`). Episodes are themselves the ingest unit;
  there is no document object above them to return to.
- **cognee** — `DocumentChunk.is_part_of` names its `Document`
  (`cognee/modules/chunking/models/DocumentChunk.py:10-25`), and `Document`
  carries `raw_data_location`, a path, rather than the text
  (`cognee/modules/data/processing/document_types/Document.py:6-14`). The chain
  is complete only while that location resolves.
- **mem0** — `save_messages` writes role and content to a `messages` table
  (`mem0/memory/storage.py:134-141, 257-269`). No `message_id` or equivalent
  appears on a memory, so nothing leads from a retrieved memory to its source
  turn.
- **Letta Code** — MemFS tracks blocks in git, so prior versions are
  recoverable through git rather than through the store.
- **LangMem** — namespace and key over a store value; no document or fragment
  model found.
- **Memobase** — `GeneralBlob` retains raw input and `BufferZone` references a
  `blob_id` (`models/database.py:286-297, 346-362`). Profile slots, which are
  the retrieval unit, carry no blob reference.
- **Hindsight:** `memory_units.document_id` points to a retained document with
  `original_text` and a content hash.
- **MemOS:** each tree memory can carry source snippets, roles, message IDs,
  document paths and file information. Archived versions link to a full prior
  node.
- **mnem:** `chunk_of` links a retrieved chunk to its document node, with
  source offsets and content-addressed graph history.
- **Menhir:** provenance expansion reaches source episodes, typed evidence
  spans and structural code anchors.
- **Neo4j Agent Memory:** extracted entities link to source messages, but the
  direct MCP fact tool leaves its modeled `source_id` unset.
- **Memori:** `memori_entity_fact_mention` links facts back to conversations.

**The claim this column supports is narrow.** It is not that the field discards
source text. The expanded set shows that paths back to documents, episodes and
conversations are common enough to deserve a separate column.

## Limits of this audit

- **Static reading only.** No system was installed, run, or exercised against a
  workload. Every verdict is about what the committed source permits. What a
  deployment does is outside it.
- **Hosted and packaged internals are out of scope.** Mem0 Platform, Zep's
  hosted service and Letta Cloud are named where their existence changes what
  the open source can do. Supermemory's documented self-hosted engine is also
  excluded from scoring because its implementation is distributed as a binary
  rather than present in the inspected repository.
- **`grep` for an absent field is weaker than reading a present one.** Where the
  finding is "no authority field", the evidence is a search of the model or
  schema definition plus a read of the write path. A field stored inside a
  free-form `attributes` dict or a JSON payload would not necessarily surface.
  This is the most likely place for the audit to be wrong, and it is the reason
  the article's claim is scoped to my search.
- **A single commit is a snapshot.** Most repositories were at recent commits
  on their audit date. Any of these findings can
  be made obsolete by one merge, which is why every one carries its commit.

## Right of reply

**Outstanding, and not satisfied.** The repository's reporting rules require a
materially criticised subject to receive the specific claim with a fair chance
to respond. That has not been done for any of the fourteen external projects
named here.

The mitigating facts, stated so a reader can weigh the gap: every criticism is a quotation or a line reference against a public
commit, so each project's maintainers and any reader can check it without
relying on this article's characterisation; no claim is made about intent,
competence or roadmap; and the article now gives its strongest counterexamples,
mnem and Menhir, more space than any negative cell.

A correction to any finding here will be made in place, dated, with the
superseded claim left legible.
