---
title: "Your agent's memory has no authority model"
date: 2026-08-20
author: Rakuen Software
tags: [memory, agents, knowledge-graph, ontology, aimee]
excerpt: "Seven publicly available memory systems, read at a pinned commit. In six of them a language model's guess and a person's statement are the same kind of row, and the model's own output decides which rows survive. That is an architectural property of the write path, not a retrieval quality problem."
---

*Published 2026-08-20. Rakuen builds aimee, one of the seven systems audited
here, and benefits if readers prefer its design. Every claim below is a
quotation or a line reference against a pinned public commit, so it is checkable
without taking my word for any of it. The audit is recorded in
[evidence/source-audit-2026-08-20.md](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/your-memory-has-no-authority-model/evidence/source-audit-2026-08-20.md),
with a per-claim source map in
[evidence/figures.md](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/your-memory-has-no-authority-model/evidence/figures.md).*

Long context retired the question agent memory used to be judged on. Whether the
right turn comes back from a corpus is a question a large enough window answers
by not asking it. Paste the conversation in. The retrieval problem stops
existing.

What a window cannot do is decide which of two contradictory facts is true,
refuse to let a model's guess overwrite a person's statement, or tell you what
it believed last week. Those are properties of a write path, and a context
window does not have one.

I read the source of seven publicly available memory systems on 20 August 2026,
each at a pinned commit. In six of them, a fact a person stated and a fact a
language model inferred are the same kind of row, with no field distinguishing
them, and the model's own output decides which rows survive. In three, a model
tool call destroys the prior content outright.

That is not a quality problem that better retrieval fixes. It is a property of
what the store is allowed to accept and what it is allowed to forget, decided at
the write, and it survives any amount of context you throw at the read.

`aimee` is the exception, and the rest of this is the mechanism that makes it
one: a write gate that validates a triple against a typed ontology before
commit, a provenance-keyed authority class a model can never reach, and a store
where correction stamps a row rather than removing it.

Everything below describes `aimee`'s typed-fact layer, which is where identity
and world facts live. Free-text prose memory, which carries episodic and code
recall, has different write semantics and is out of scope here.

## The write gate: a triple that fails its ontology never becomes a row

`aimee` holds identity and world facts as typed triples on semantic edges, and
every emitter routes through one commit point. The pure validator is twenty-three
lines:

```c
const rel_type_def_t *def = rel_types_seed_lookup(rel_type);
if (!def)
   return FACT_GATE_NOVEL; /* caller consults the live ontology: stage or defer */

if (matched)
   *matched = def;
if (!rel_type_kind_allowed(def, 1, head_kind) || !rel_type_kind_allowed(def, 0, tail_kind))
   return FACT_GATE_REJECT_KIND;
return FACT_GATE_ACCEPT;
```

[`memory_fact_gate.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/modules/memory/memory_fact_gate.c#L14-L22).
The relation is looked up in an ontology that declares which entity kinds may
sit on each end. `works_for` takes a `PERSON` and an `ORG`. A model that emits
`printer works_for kernel` gets `FACT_GATE_REJECT_KIND`, and the commit path
returns before writing anything: "REJECT_KIND / BADARG: never write an
unvalidated semantic edge"
([`rel_types_store.c:208`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/rel_types_store.c#L207-L208)).

The ontology is a table, not code. Seventeen relations ship in the in-code seed
so a fresh install validates before anything has been learned, and each row is
self-describing:

| relation | subject | object | correction policy | sensitivity |
| --- | --- | --- | --- | --- |
| `works_for` | PERSON | ORG | supersede | normal |
| `spouse` | PERSON | PERSON (symmetric) | supersede | pii |
| `parent_of` | PERSON | PERSON (inverse `child_of`) | immutable | pii |
| `born_in` | PERSON | PLACE | immutable | pii |
| `lives_in` | PERSON | PLACE | supersede | pii |
| `device_has_ip` | DEVICE | IP | supersede | normal |
| `also_known_as` | PERSON | ANY | hard_delete | normal |

All seventeen are in
[`rel_types.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/rel_types.c#L18).
The live overlay is the `rel_types` table
([`schema.sql:1412`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/schema.sql#L1412)),
carrying the same columns plus a `status` of `active`, `provisional`, `mapped`
or `rejected`.

Two consequences follow, and the second is the awkward one. Favourable: a
relation's semantics travel with the relation, so nothing downstream has to be
told, per call, that `works_for` holds one value and `knows` holds many.
Awkward: an ontology that is wrong rejects legitimate facts, and a
seventeen-row seed is wrong about most of the world on day one. The next
section is how that stops being fatal.

## Novel relations stage as speculation and promote themselves at three sightings

A relation the seed does not know is not rejected. It is staged: a provisional
`rel_types` row is inserted so the edge's `relation_id` resolves, the edge
commits at the lowest confidence class, and the sighting is counted
([`rel_types_store.c:255-270`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/rel_types_store.c#L255-L270)).
The counter is one statement:

```sql
INSERT INTO ontology_evaluations (rel_type, occurrence_count, status, created_at)
 VALUES (?1, 1, 'pending', ?2)
 ON CONFLICT (rel_type) DO UPDATE
 SET occurrence_count = ontology_evaluations.occurrence_count + 1
 RETURNING occurrence_count
```

The count is bumped only after the edge actually committed, so a failed write
cannot inflate a candidate's standing. A previously rejected relation keeps its
status on conflict, so it cannot resurface as a candidate by being emitted
again.

The curator drain then promotes candidates without asking anyone. At each poll
it pulls pending relations whose `occurrence_count` has reached the threshold
and flips them to `active`
([`kb_curator_drain.c:800-828`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_curator_drain.c#L800-L828)).
Auto-promotion is on by default and the threshold is three
([`config_kb_curator.c:74-76`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/modules/config/config_kb_curator.c#L74-L76)).

The one hard exclusion is a catch-all bucket. `other`, `unknown`, `misc` and
`unspecified` are skipped on the promotion path even when they clear the
threshold, because a durable `misc` relation cannot later be reconciled to a
real predicate. The extractor is separately instructed not to emit one, and the
drain excludes them anyway.

This is what "the ontology extends itself" has to mean to be worth anything. A
relation earns durability by recurring across sources, and nothing about the
promotion needs a person in the loop. Compare `aimee expand kubernetes <url>`,
which seeds a domain's relations up front from its documentation and is
deliberately human-approvable, because it changes the ontology's shape rather
than counting evidence for a shape already in use.

## A model-inferred fact can never reach the class a person's statement gets

This is the load-bearing rule, and it is eleven lines:

```c
const char *fact_class_for(fact_authority_t authority, fact_gate_verdict_t verdict)
{
   if (verdict == FACT_GATE_NOVEL)
      return FACT_CLASS_C;
   if (authority == FACT_AUTHORITY_USER)
      return FACT_CLASS_A; /* a direct user assertion of a known relation earns A */
   if (verdict == FACT_GATE_ACCEPT)
      return FACT_CLASS_B; /* model inference consistent with the ontology */
   return FACT_CLASS_C;    /* anything else (reject/badarg) — conservative */
}
```

[`fact_lifecycle.c:48-59`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/fact_lifecycle.c#L48-L59).
The class is stamped on the edge and drives everything after it.

- Class A is a direct user assertion of a known relation. Confidence 1.0. It
  wins every conflict on the same subject and relation, and it never expires.
- Class B is a model inference the ontology accepted. Confidence 0.6, raised to
  0.8 once the same fact has been observed enough times to become durable.
- Class C is speculation, which includes every fact using a relation the
  ontology has not accepted. Confidence 0.4, and it expires.

The background extractor is wired to Class B or C. It calls
`db2_fact_commit(..., FACT_AUTHORITY_MODEL, 1)`
([`kb_memory_facts.c:300-305`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_memory_facts.c#L300-L305)),
so the authority argument is a constant at that call site. The model is asked for
a confidence score and it is used only as a floor: below 0.6 the triple is
dropped
([`kb_memory_facts.c:39`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_memory_facts.c#L39)).
Above it, the score buys nothing. A model returning `"confidence": 1.0` on a
hallucinated triple gets Class B, the same as a cautious one.

Note the first branch. A novel relation is Class C even when the user asserted
it, because what is unproven there is the ontology rather than the speaker. That
costs the user something and it is the correct trade: an unvalidated relation
should not carry permanent authority because a person used it once.

Expiry does the cleaning, and its SQL is where "unconfirmed speculation cannot
calcify into a remembered fact" stops being a slogan:

```sql
UPDATE entity_edges SET superseded_at = ?2
 WHERE edge_class = 'semantic' AND confidence_class = 'C'
   AND superseded_at = '' AND suppressed = 0 AND weight <= 1
   AND asserted_at <> '' AND asserted_at < ?1
```

Unconfirmed Class C edges past their TTL are stamped, not removed. And a Class B
fact re-observed a hundred times becomes durable B; it never becomes A. Nothing
a model produces reaches the class a person's statement gets, by any path,
including repetition.

## Correction stamps a row. It does not remove one

`correction_behavior` is a column on the relation, so the policy for correcting
a fact is a property of what kind of fact it is.

- `supersede`, the default. `superseded_at` is stamped on the old edge and the
  new one is inserted. Both rows stay.
- `hard_delete`, a name kept for familiarity that is not a delete. The edge and
  its aliases stop resolving via a `suppressed` flag and the row is retained. It
  is used for `also_known_as`, where a stale alias actively misleads and has to
  stop matching.
- `immutable`, which refuses a model or inferred correction to an
  already-asserted value. `born_in` and `parent_of` carry it.

`immutable` does not mean the user cannot change it. It means no model may
silently rewrite it: a direct user assertion supersedes the prior value as a new
Class A fact, and a non-user authority is refused with
`FACT_RETRACT_IMMUTABLE`. The reverse guard sits in the same contract. A model
authority cannot retract a user-stated Class A edge at all, on any relation
([`fact_lifecycle.h:62-85`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/fact_lifecycle.h#L62-L85)).

Because nothing is removed, both time axes have data to answer from.
`superseded_at` is transaction time, meaning when `aimee` stopped believing the
edge. `valid_from` and `valid_until` are valid time, meaning the real-world
interval the fact held. "What IP did the NAS used to have" and "what did `aimee`
believe last week" are different queries against different columns, and a system
that overwrites can answer neither.

## Endpoints resolve to a surrogate id, and a wrong merge is reversible

Name-keyed graphs fragment. "DevBox", "the workstation" and "my main box" become
three unrelated nodes, and "Theo" and "Theodore" either never reconcile or
wrongly merge.

Entity-kind endpoints are canonicalised before the edge is written
([`rel_types_store.c:155-183`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/rel_types_store.c#L155-L183)).
`entity_registry` holds a globally unique surrogate `canonical_id`;
`entity_aliases` maps a normalised name to it and is single-hop by construction,
so an alias can never point at another alias and a circular chain is
structurally impossible rather than guarded after the fact
([`schema.sql:1443-1456`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/schema.sql#L1443-L1456)).

Scalars are left alone. An IP literal or an age is not an entity, and running it
through a registry would invent identity where there is none.

Two properties matter more than the resolution itself. Every near-match merge
writes an `entity_merges` row, and `db2_entity_unmerge` reverses a recorded merge
([`entity_registry.c:242-408`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/entity_registry.c#L242-L408)).

And a genuinely ambiguous name, where several canonical targets are plausible,
lands in `entity_name_conflicts` with a status, a priority and a bounded retry,
blocking neither the write nor recall. Ambiguity is queued. It is not resolved by
guessing.

## What stays is decided by attributed outcomes, not by how often it was read

Every recall writes a `retrieval_event` artifact naming the rows it surfaced.
Each surfaced row that contributed to a response gets a `retrieval_attribution`
row carrying a verdict: `accepted`, `corrected`, `contradicted`, `rolled_back`
or `irrelevant`. The demotion scorer reads a time-decayed window of those
verdicts and nothing else. Its contract states the exclusion list rather than
leaving it to be inferred:

```text
The scorer reads only attributed outcome evidence — not source tags, declared
confidence, author id, or retrieval frequency.
```

[`demotion.h:106-110`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/demotion.h#L104-L112).
That list is the design. A memory retrieved constantly and wrong every time
scores negatively, because frequency is not an input, and a memory carrying a
flattering source tag gets no credit for it.

Below `n_min` attributed outcomes the scorer returns `NAN` and declines to rank
at all, which is the same refusal as abstaining on weak evidence, pointed at
maintenance instead of recall
([`demotion.c:690-774`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/demotion.c#L690-L774)).

Contradiction is not resolution. Both claims stay, the pipeline links them and
preserves their sources, and review or policy decides the current value
([`CURATOR_PIPELINE.md`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/docs/CURATOR_PIPELINE.md)).
An unresolved contradiction also raises a curiosity item, one of five gap types
alongside `missing_fact`, `stale_fact` and `weak_coverage`, so the store carries
a backlog of what it knows it does not know.

## Six of seven systems have no field that distinguishes the two kinds of fact

Every row below was read from the project's own source at the commit named, on
20 August 2026. The `aimee` row describes its typed-fact layer, which is the
layer this piece is about. Where a project's design differs from what a summary
line can carry, the paragraphs after the table say so.

| system | commit | typed write gate | authority classes | valid time | model may remove a fact |
| --- | --- | --- | --- | --- | --- |
| `aimee` typed facts | `50c5d88d` | yes, kind-validated | A / B / C, enforced | yes | no, superseded |
| Graphiti (Zep) | `c4069327` | no | none | yes | expired, not dropped |
| cognee | `fd5045f6` | optional, enrichment only | none | edge `updated_at` | tagged, not dropped |
| mem0 OSS | `3599aa75` | no | none | no | not in v3, ADD-only |
| Letta Code | `d1dc6880` | no | none | no | yes, block rewrite |
| LangMem | `29cbe41e` | no | none | no | yes, hard delete |
| Memobase | `358c16bb` | slot schema | none | no | yes, slot rewrite |

Graphiti is the closest architecture and the fairest comparison. It is genuinely
bitemporal: `valid_at`, `invalid_at` and `expired_at` all sit on `EntityEdge`,
and a contradicted edge is expired rather than deleted
([`edges.py:262-283`](https://github.com/getzep/graphiti/blob/c406932767ee490ad2311fd694a6b2ac3b164599/graphiti_core/edges.py#L262-L283)).

Custom edge types are supported and filtered per node-label pair. What that
filtering does is choose which type definitions the extraction prompt is shown
([`edge_operations.py:458-486`](https://github.com/getzep/graphiti/blob/c406932767ee490ad2311fd694a6b2ac3b164599/graphiti_core/utils/maintenance/edge_operations.py#L458-L486)).
It is not a write-time rejection. The validation that does run on the way in
checks that the LLM's entity names exist in the node list and drops self-edges
([`edge_operations.py:210-241`](https://github.com/getzep/graphiti/blob/c406932767ee490ad2311fd694a6b2ac3b164599/graphiti_core/utils/maintenance/edge_operations.py#L210-L241));
the relation name is taken as given and becomes the edge's `name`.

There is no confidence, provenance or authority field on `EntityEdge` at all, so
an edge the user dictated and an edge the model inferred are indistinguishable
rows.

cognee has arrived at the same problem and named it precisely. Its temporal
conflict resolver tags superseded edges rather than deleting them, which is the
right behaviour, and its module docstring explains why it cannot do that
automatically:

```text
Nothing is applied automatically: the caller names the relationships that are
single-valued. Most cognee relationships (``knows``, ``mentions``, ...) are
legitimately many-valued and must never be collapsed, and there is no
cardinality metadata to tell them apart.
```

[`temporal_conflict_resolver.py:13-16`](https://github.com/topoteretes/cognee/blob/fd5045f6b60522c1953fc1ae258e041ba53602d8/cognee/modules/graph/utils/temporal_conflict_resolver.py#L13-L16).
That missing cardinality metadata is what `rel_types.correction_behavior`
carries, per relation, in the store.

cognee also ships real ontology support, and the default resolver is constructed
with `ontology_file=None`
([`get_default_ontology_resolver.py:10-12`](https://github.com/topoteretes/cognee/blob/fd5045f6b60522c1953fc1ae258e041ba53602d8/cognee/modules/ontology/get_default_ontology_resolver.py#L10-L12)).
An operator-supplied OWL file is matched fuzzily to enrich extracted entities
rather than to reject them, and contradiction detection defaults to `False`
([`cognify/config.py:13-17`](https://github.com/topoteretes/cognee/blob/fd5045f6b60522c1953fc1ae258e041ba53602d8/cognee/modules/cognify/config.py#L13-L17)).

mem0's open-source graph memory no longer exists. The v3 release removed it:
"Graph memory is removed from OSS. It's a built-in, always-on Mem0 Platform
feature"
([`oss-v2-to-v3.mdx:41`](https://github.com/mem0ai/mem0/blob/3599aa75ed64ee41c3b1d8133a8b39403fb8f703/docs/migration/oss-v2-to-v3.mdx#L41)).

The same release made extraction ADD-only: "Single-pass ADD-only (one LLM call,
no UPDATE/DELETE)". That is a real improvement on the previous design, where an
LLM chose between ADD, UPDATE and DELETE per fact and a DELETE removed the
vector row while retaining the prior text in a SQLite history table
([`main.py:2100-2122`](https://github.com/mem0ai/mem0/blob/3599aa75ed64ee41c3b1d8133a8b39403fb8f703/mem0/memory/main.py#L2100-L2122)).

What replaces it is accumulation. Memories are self-contained sentences, related
ones are linked by id, and nothing reconciles two that contradict. The open
source you can run today is free-text memories with hash dedup and hybrid
search; the reconciliation story is on the hosted side.

Letta's V1 server has been retired and its memory is text the model edits. The
repository at `letta-ai/letta` is now a landing page, the source lives in
`letta-ai/letta-code`, and the V1 server sits on an `archive` branch that
"receives no fixes or security updates, and should not be used in production."
The memory surface is a block the agent rewrites through `memory_replace`,
`memory_insert` and `memory_rethink`
([`toolset.ts:61-68`](https://github.com/letta-ai/letta-code/blob/d1dc6880971dc55a5e5dfcf845d4cba740b14585/src/tools/toolset.ts#L61-L68)).

Credit where it is due, and it is a design nobody else here has: MemFS tracks
every block in git, so a rewrite that destroyed a fact leaves a commit. That is
an audit trail. It is not an authority model, and the store itself has no idea
which line came from the user.

LangMem lets the model delete a memory outright. `create_manage_memory_tool`
permits `create`, `update` and `delete` by default, and the delete branch is one
line: `await store.adelete(namespace, key=str(id))` on the async path
([`tools.py:293-294`](https://github.com/langchain-ai/langmem/blob/29cbe41e58528f92e9efa773c12e15c47be3808c/src/langmem/knowledge/tools.py#L293-L294)),
`store.delete(namespace, key=str(id))` on the sync one
([`tools.py:327-328`](https://github.com/langchain-ai/langmem/blob/29cbe41e58528f92e9efa773c12e15c47be3808c/src/langmem/knowledge/tools.py#L327-L328)).
No history row, no tombstone, no class check on what is being removed.

This is the clearest case in the set. A tool call the model chooses to emit
removes a fact a person stated, and afterwards the store cannot tell you it
happened.

Memobase does have a schema, and it is the closest thing here to an ontology.
Profiles are topic and subtopic slots and extraction fills them. Reconciliation
is an LLM choosing `APPEND`, `UPDATE` or `ABORT`, where `UPDATE` means rewriting
the slot's memo text
([`merge_profile.py:34-46`](https://github.com/memodb-io/memobase/blob/358c16bbc6d687937d79bc2f984a11c3be8da901/src/server/api/memobase_server/prompts/merge_profile.py#L34-L46)).
The slot is a place for an attribute, not a typed relation between two entities,
and the prior text does not survive the rewrite.

I also read A-MEM (`ceffb860`), which organises memories as Zettelkasten-style
linked notes with LLM-generated links and carries no temporal, authority or
ontology layer. It is a research implementation and I am not holding it to a
production bar.

## The claim, scoped so one counterexample would settle it

Of the seven systems in the table above, plus A-MEM, all read at a pinned commit
on 20 August 2026, `aimee`'s typed-fact layer is the only one in which all three
of the following hold: a model-extracted fact cannot reach the authority class a
user-stated fact gets, by any path including repetition; a model authority
cannot retract a user-stated fact on any relation; and a triple whose subject or
object kind violates the relation's ontology is refused a row rather than
written and sorted out later.

I looked for a counterexample among the systems I could read and did not find
one. That is a claim about my search, not about the world. Hosted systems whose
source I cannot read are outside it, and so is any system I did not think to
clone. One system with an authority column enforced on the write path would
settle it, and I would rather be shown one than keep the claim.

## What this design costs, and what it does not cover

An ontology that is wrong rejects facts that are true. The seed is seventeen
relations, so on a fresh corpus most of what arrives is novel, lands at Class C,
and has to earn its way to durable through three sightings across sources. A
fact stated once, in a domain nobody has taught the ontology, expires. That is
the deliberate trade for never letting speculation calcify, and it is a real
cost paid by the user who says something true exactly once.

Retaining everything has a price too. Nothing is deleted, so `entity_edges`
grows with every correction, and a store that has been running for a year
carries every value each fact has ever held. Superseded rows are cheap to filter
and they are not free to keep.

Recall abstention exists and is default-off with its threshold uncalibrated,
because calibrating it needs labelled ask-outcome data nobody has collected. I
would rather say that than ship a threshold I guessed.

And the scope: this is the typed-fact layer. Identity and world facts live here.
Code and episodic recall stay in free-text prose memory, which has its own write
semantics that this piece does not describe, and the two are unioned only at
injection.

## Who this is not for

If you want a memory system you can add to an agent this afternoon with a pip
install and an API key, this is the wrong one. `aimee`'s memory subsystem is
34,000 lines of C, it wants PostgreSQL with pgvector, and it is built by one
person. mem0 and LangMem will have you storing memories in ten minutes and this
will not.

If your agent's memory holds preferences that are cheap to be wrong about, the
authority model is overhead you are paying for nothing. Wrong preference, mild
annoyance, next turn corrects it.

The argument starts to bind when a remembered fact drives an action. A device
address, a policy decision, an on-call owner, a customer's stated constraint.
There, "the model rewrote it and the store cannot tell you" is not a quality
issue.

## Go and check your own

Three checks to run against whatever memory system you have, in ascending order
of how much a bad answer should worry you.

Open the schema for a stored fact and look for a field recording who asserted
it, distinct from the model that wrote it down. If there is no such column, the
distinction does not exist at runtime, whatever the prompt says.

Follow the delete path from the model's tool surface and see what survives it. A
history table is better than nothing and is not the same as a tombstone the
recall path walks past.

Then try to write the two queries "what did you believe last week" and "what was
true last year" against different columns. If they are the same query,
corrections are overwrites and you cannot audit one.

If all three come back clean on something I have not read, send it to me. That is
the counterexample, and the claim above is written so it can lose to one.
