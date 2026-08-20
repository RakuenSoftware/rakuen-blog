# Source map

Every claim and quoted line in
[`your-memory-has-no-authority-model.md`](../article/your-memory-has-no-authority-model.md),
and the source line behind it.

This article is an architecture piece. It contains no measurement, first-party
or otherwise, and makes no performance or accuracy claim about any system. All
source was read on 2026-08-20 at the commits pinned in
[`source-audit-2026-08-20.md`](source-audit-2026-08-20.md).

## Scope

The article describes `aimee`'s **typed-fact layer**: the ontology, the write
gate, confidence classes, correction, entity canonicalisation and
outcome-attributed demotion. Free-text prose memory has different write
semantics and is explicitly out of scope in the article text. No claim is made
about it here or there.

## `aimee` source citations

Commit `50c5d88d37bae618ee08b0101f163682e864ace9`, 2026-08-06, public, reachable
from `origin/agent/human-trigger-workflows`. Every file cited was verified clean
against that commit before the article was written; the working tree carried
unrelated modifications in files not cited here.

| claim in the article | source |
|---|---|
| the pure write-gate validator, quoted in full | `src/modules/memory/memory_fact_gate.c:14-22` |
| "never write an unvalidated semantic edge" | `src/db2/rel_types_store.c:208` |
| seventeen seed relations, and the seven-row extract of them | `src/rel_types.c:18` onward |
| `rel_types` table and its `status` values | `src/db2/schema.sql:1412` |
| provisional staging of a novel relation, sighting counted after commit | `src/db2/rel_types_store.c:255-270` |
| the `ontology_evaluations` upsert, quoted in full | `src/db2/ontology_evolution.c:41-46` |
| auto-promotion sweep, catch-all exclusion | `src/kb/kb_curator_drain.c:800-828` |
| auto-promote default on, threshold 3 | `src/modules/config/config_kb_curator.c:74-76` |
| `fact_class_for`, quoted in full | `src/db2/fact_lifecycle.c:48-59` |
| class confidences 1.0 / 0.6 / 0.4 | `src/db2/fact_lifecycle.c:26-32` |
| durable B raises confidence to 0.8, never to A | `src/db2/fact_lifecycle.h:58-61` |
| extractor pinned to `FACT_AUTHORITY_MODEL` | `src/kb/kb_memory_facts.c:300-305` |
| model confidence used only as a 0.6 floor | `src/kb/kb_memory_facts.c:39`, applied at `:281` |
| Class C expiry SQL, quoted in full | `src/db2/fact_lifecycle.c:83-86` |
| `supersede` / `hard_delete` / `immutable` semantics | `src/db2/fact_lifecycle.h:62-85` |
| a model authority cannot retract a Class A edge | `src/db2/fact_lifecycle.h:77-82` |
| transaction time and valid time columns | `src/db2/schema.sql:1400-1409` |
| endpoint canonicalisation before the edge write | `src/db2/rel_types_store.c:155-183` |
| surrogate `canonical_id`, single-hop aliases | `src/db2/schema.sql:1443-1456` |
| merge audit and `unmerge` | `src/db2/entity_registry.c:242-408` |
| ambiguity queued in `entity_name_conflicts` | `src/db2/schema.sql:1465-1472` |
| demotion verdict tokens | `src/db2/demotion.h:28-32` |
| "reads only attributed outcome evidence", quoted | `src/db2/demotion.h:106-110` |
| `NAN` below `n_min` | `src/db2/demotion.c:771-773` |
| contradiction keeps both claims | `docs/CURATOR_PIPELINE.md` |
| five curiosity gap types | `src/db2/curiosity.h:25-29` |
| abstention default-off, threshold uncalibrated | `docs/proposals/done/retrieval-abstention-confidence-gate.md` |
| memory subsystem is 34,000 lines of C | `wc -l` over `src/modules/memory/*.c`, `src/db2/memory_*.c`, `src/db2/{typed_facts,rel_types_store,ontology_evolution,demotion}.c`, `src/db2/fact_*.c`, `src/db2/entity_*.c`, `src/rel_types.c`: 34,115 lines, rounded down |
| PostgreSQL with pgvector | `docs/STORAGE_TIERS.md` |
| `aimee expand <domain> [url]` is human-approvable | `docs/proposals/done/typed-fact-knowledge-layer.md` §2 |

**One figure is derived rather than read.** "34,000 lines of C" is a `wc -l`
over the file set listed above, taken on the working tree on 2026-08-20. It
counts comments and blank lines, and the file set is a judgement about what
counts as the memory subsystem. It is an order-of-magnitude claim in the piece
and is used as one.

## Comparison-table cells

Each cell of the seven-system table is sourced in
[`source-audit-2026-08-20.md`](source-audit-2026-08-20.md), which records the
commit, the file and the reasoning for every verdict, including the cells where
a one-word answer understates a project's design.
