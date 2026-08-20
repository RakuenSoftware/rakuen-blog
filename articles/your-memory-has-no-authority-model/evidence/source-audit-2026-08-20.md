# Source audit: seven agent memory systems

Date of audit: 2026-08-20.

Method: each repository was cloned with `git clone --depth 1` from its public
GitHub origin on 2026-08-20 and the resulting `HEAD` was recorded before
reading. No repository was modified. Every verdict below cites a file and line
range in the committed tree at that commit. Nothing here was read from a
summary, a blog post or a model's description of a project.

`aimee` was read from the local checkout at
`50c5d88d37bae618ee08b0101f163682e864ace9`, which is public and reachable from
`origin/agent/human-trigger-workflows`. Every `aimee` file cited by the article
was verified byte-identical to that commit with `git diff --quiet HEAD -- <path>`
before writing. Files carrying unrelated working-tree modifications were not
cited.

## Commits

| system | repository | commit | commit date |
|---|---|---|---|
| `aimee` | `RakuenSoftware/aimee` | `50c5d88d37bae618ee08b0101f163682e864ace9` | 2026-08-06 |
| Graphiti | `getzep/graphiti` | `c406932767ee490ad2311fd694a6b2ac3b164599` | 2026-08-20 |
| cognee | `topoteretes/cognee` | `fd5045f6b60522c1953fc1ae258e041ba53602d8` | 2026-08-19 |
| mem0 | `mem0ai/mem0` | `3599aa75ed64ee41c3b1d8133a8b39403fb8f703` | 2026-08-20 |
| Letta Code | `letta-ai/letta-code` | `d1dc6880971dc55a5e5dfcf845d4cba740b14585` | 2026-08-20 |
| LangMem | `langchain-ai/langmem` | `29cbe41e58528f92e9efa773c12e15c47be3808c` | 2026-08-10 |
| Memobase | `memodb-io/memobase` | `358c16bbc6d687937d79bc2f984a11c3be8da901` | 2026-01-11 |
| A-MEM | `agiresearch/A-mem` | `ceffb860f0712bbae97b184d440df62bc910ca8d` | 2025-12-12 |

`letta-ai/letta` was also cloned (`87fd37aa`, 2026-08-15) and found to contain no
source. Its README states the repository "now serves as a landing page" and that
the V1 server source is preserved on an `archive` branch that "receives no fixes
or security updates, and should not be used in production." The audit therefore
covers `letta-ai/letta-code`, which the README names as the current source. The
`archive` branch was not read.

## Column definitions

The article's table has five judged columns. Each is a yes/no question with a
stated test, so a reader can disagree with the verdict by applying the same
test.

- **Typed write gate.** Does a candidate relation get checked against declared
  subject/object type constraints, with a failing candidate refused a row? A
  constraint that only shapes what an extraction prompt is shown is not a write
  gate, because the store still accepts whatever the model returns.
- **Authority classes.** Does a stored fact carry a field, enforced at write,
  that separates a user assertion from a model inference and ranks them?
- **Valid time.** Can the store answer "when was this true in the world",
  separately from "when did the system believe it"?
- **Model may remove a fact.** Can a tool call or pipeline step the model
  controls make the prior content unreadable?
- **Commit.** The pinned tree the answer was read from.

## Per-system findings

### `aimee`

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
- Model removal: no. `db2_fact_retract` skips Class A rows for a non-user
  authority and `hard_delete` is a `suppressed` flag with the row retained
  (`src/db2/fact_lifecycle.h:62-85`).

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

## Limits of this audit

- **Static reading only.** No system was installed, run, or exercised against a
  workload. Every verdict is about what the committed source permits. What a
  deployment does is outside it.
- **Hosted products are out of scope.** Mem0 Platform, Zep's hosted service and
  Letta Cloud are named where their existence changes what the open source can
  do, and no claim is made about their internals, which I cannot read.
- **`grep` for an absent field is weaker than reading a present one.** Where the
  finding is "no authority field", the evidence is a search of the model or
  schema definition plus a read of the write path. A field stored inside a
  free-form `attributes` dict or a JSON payload would not necessarily surface.
  This is the most likely place for the audit to be wrong, and it is the reason
  the article's claim is scoped to my search.
- **A single commit is a snapshot.** Six of the eight repositories were at a
  commit less than two weeks old on the audit date. Any of these findings can
  be made obsolete by one merge, which is why every one carries its commit.

## Right of reply

**Outstanding, and not satisfied.** The repository's reporting rules require a
materially criticised subject to receive the specific claim with a fair chance
to respond. That has not been done for any of the seven projects named here.

The mitigating facts, stated so a reader can weigh the gap: every criticism is a quotation or a line reference against a public
commit, so each project's maintainers and any reader can check it without
relying on this article's characterisation; no claim is made about intent,
competence or roadmap; and the two cells that most flatter this article's
argument, cognee's and Graphiti's, are the two where the article spends the most
words explaining what a one-word verdict understates.

A correction to any finding here will be made in place, dated, with the
superseded claim left legible.
