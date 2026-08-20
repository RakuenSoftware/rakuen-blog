---
title: "Your agent's memory has no authority model"
date: 2026-08-20
author: Rakuen Software
tags: [memory, agents, knowledge-graph, ontology, aimee]
excerpt: "Seven publicly available memory systems, read at a pinned commit. In six of them a language model's guess and a person's statement are the same kind of row, and the model's own output decides which rows survive. That is a property of the write path, settled when the fact is stored."
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

Better retrieval leaves that where it is. What the store accepts, and what it
lets go, is settled at the write, and it survives any amount of context you
throw at the read.

`aimee` is the exception, and the rest of this is the mechanism that makes it
one: a write gate that validates a triple against a typed ontology before
commit, a provenance-keyed authority class a model can never reach, and a store
where a correction stamps the old row and leaves it there.

Everything below describes `aimee`'s typed-fact layer, which is where identity
and world facts live. Free-text prose memory, which carries episodic and code
recall, has different write semantics and is out of scope here.

## A model's guess never outranks what you told it

Every fact in the store is born into one of three classes, and the class is
decided by who asserted it, not by how sure anyone sounds.

Say something yourself, using a relation the system already understands, and the
fact is Class A. It carries full confidence, it wins every conflict about the
same subject and relation, and it never expires. Let the background extractor
infer something from a note you wrote, and the best it can earn is Class B.
Everything else is Class C, which is to say speculation, and speculation is on a
clock.

The rule that assigns the class is eleven lines long and has no way to reach
Class A from a model
([`fact_lifecycle.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/fact_lifecycle.c#L48-L59)).
The extractor's calls pass their authority as a constant
([`kb_memory_facts.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_memory_facts.c#L300-L305)),
so there is no argument a prompt could win.

The model is asked how confident it is, and the answer is used once, as a floor:
below six-tenths the triple is dropped
([`kb_memory_facts.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_memory_facts.c#L39)).
Above the floor the number buys nothing. A model that returns perfect confidence
on a hallucinated triple lands exactly where a hedging one does.

The awkward branch is the first one. A relation nobody has established yet is
speculation even when you asserted it personally, because what is unproven there
is the vocabulary and your authority cannot cure that. It costs you something
real. It is still the right trade, because the alternative is letting a word
become permanent the first time somebody uses it.

Reinforcement moves a fact along that scale and never off the end of it. A model
inference confirmed enough times stops expiring and stays Class B
([`fact_lifecycle.h`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/fact_lifecycle.h#L58-L61)).
Repetition buys durability. It does not buy authority.

Speculation that never gets confirmed runs out its clock, and even then the row
is only stamped as no longer believed
([`fact_lifecycle.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/fact_lifecycle.c#L83-L86)).
Expiry is a change of standing. It is never a deletion.

## Correcting a fact leaves the old one where it is

Tell the system something that contradicts what it holds, and the old value is
stamped with the moment it stopped being believed. Then the new one is written
beside it. Nothing is removed, and the fact you superseded is still there to be
asked about.

What a correction means is a property of the fact being corrected. Most
relations supersede. A few are marked so that a stale value stops
matching queries while the row itself is kept for the record, which is what an
old nickname needs: it has to stop resolving, and it should not vanish. A few
more refuse to be quietly rewritten at all
([`fact_lifecycle.h`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/fact_lifecycle.h#L62-L85)).

That last kind does not mean you are locked out. It means no model may rewrite
the value behind your back. You can still supersede it yourself, and the new
value arrives with your authority on it. The guard runs in both directions: an
inferred correction cannot retract something you stated, on any relation at all.

Because the old rows survive, two different questions have somewhere to look.
What was true in the world last year is one axis, held on the fact itself. What
the system believed last week is the other, held in the stamp. A store that
overwrites has neither, and it will answer both questions with whatever it
happens to hold right now.

## The model cannot invent its way around the rules

None of the above would matter if a model could route around it by making up a
relation. So the vocabulary is checked before anything is written.

Facts are triples, and each kind of relationship declares what may sit on either
end of it. Employment joins a person to an organisation, an address joins a
device to an address.

When a triple arrives, the relationship is looked up and the two ends are
checked against what it permits
([`memory_fact_gate.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/modules/memory/memory_fact_gate.c#L14-L22)).
A model that proposes the printer works for the kernel gets a rejection, and the
commit path stops before writing anything, under a comment that says never to
write an unvalidated edge
([`rel_types_store.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/rel_types_store.c#L207-L208)).

Seventeen relationships ship with the system so a fresh install can validate
before it has learned anything
([`rel_types.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/rel_types.c#L18)),
and the live set lives in a table that the running system extends
([`schema.sql`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/schema.sql#L1412)).
Each one carries its own rules with it, which is why nothing downstream ever has
to be told, case by case, that a person has one employer and many acquaintances.

The obvious objection is that seventeen relationships is a rounding error
against the world, and an ontology that is wrong rejects things that are true.

## The vocabulary grows without anyone approving it

A relationship the system has never seen is not thrown away. It is admitted as
speculation, with a provisional entry created so the fact has something to hang
on, and the sighting is counted
([`rel_types_store.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/rel_types_store.c#L255-L270)).

The counting is careful in two ways worth noticing. A sighting registers only
after the fact it came from actually committed, so a failed write cannot inflate
a candidate's standing. And a relationship already rejected keeps that verdict,
so it cannot creep back onto the shortlist by being proposed again
([`ontology_evolution.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/ontology_evolution.c#L41-L46)).

Recur across enough separate sources and the maintenance pass promotes the
relationship to a real one, on its own, with nobody asked
([`kb_curator_drain.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_curator_drain.c#L800-L828)).
Three sightings is the default and promotion is on out of the box
([`config_kb_curator.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/modules/config/config_kb_curator.c#L74-L76)).

One family of words is barred from ever making it. A model that falls back on a
catch-all is refused promotion no matter how often it does so, because a durable
relationship called `misc` can never be reconciled to a real one later. The
extractor is told not to reach for those, and the promotion pass excludes them
anyway.

This is the only version of a self-extending vocabulary that seems worth having.
A word earns permanence by turning up again in work nobody staged, and no one
signs off on it. The one path that does want a human is teaching a whole domain
up front from its documentation, which changes the shape of the vocabulary
before any evidence has accumulated to justify it.

## Two spellings of a name are one thing, and a bad guess is reversible

A graph keyed on names splits under ordinary use. Call the same machine DevBox
one day and the workstation the next and you have two unrelated nodes that never
learn about each other.

So the ends of a fact are resolved to an identity before the fact is stored
([`rel_types_store.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/rel_types_store.c#L155-L183)).
Names point at that identity and never at each other, which makes a circular
chain of nicknames impossible by construction instead of something to be
detected later
([`schema.sql`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/schema.sql#L1443-L1456)).

Values are left alone. An address or an age is not somebody, and running it
through an identity register would invent a person where there is none.

Two things about this matter more than the matching itself. Every close-call
merge is written down and can be undone
([`entity_registry.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/entity_registry.c#L242-L408)),
which is the difference between a system that is confident and one that can be
wrong safely. And a name with several plausible owners is not guessed at. It
goes on a queue with a status and a bounded number of retries, blocking neither
the write nor the recall
([`schema.sql`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/schema.sql#L1465-L1472)).

## What survives is decided by how it turned out

Recall is not free of consequences. Each one records which facts it put in front
of the model, and each fact that shaped an answer gets a verdict written against
it: accepted, corrected, contradicted, rolled back, or beside the point.

Whether a memory keeps its standing is then decided from a time-decayed window
of those verdicts and nothing else. The contract spells out what is deliberately
excluded:

```text
The scorer reads only attributed outcome evidence — not source tags, declared
confidence, author id, or retrieval frequency.
```

[`demotion.h`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/demotion.h#L104-L112).
That exclusion list is the whole idea. A memory pulled up constantly and wrong
every time sinks, because being popular is not evidence. A memory wearing a
respectable provenance tag earns nothing for it.

Under a floor of recorded outcomes the scorer declines to judge at all and says
so
([`demotion.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/demotion.c#L690-L774)).
It is the same instinct as abstaining on a weak answer, pointed at housekeeping.

Contradictions are not resolved by picking a winner. Both claims stay, linked,
with their sources intact, and the current value is a matter of policy rather
than of whichever arrived last
([`CURATOR_PIPELINE.md`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/docs/CURATOR_PIPELINE.md)).
An unresolved one also raises a question on a backlog of things the system knows
it does not know, alongside gaps like a fact that has gone stale and a topic it
has thin coverage of
([`curiosity.h`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/curiosity.h#L25-L29)).

## Six of seven systems have no field that distinguishes the two kinds of fact

Every row below was read from the project's own source at the commit named, on
20 August 2026. The `aimee` row describes its typed-fact layer, which is the
layer this piece is about. Where a project's design differs from what a summary
line can carry, the paragraphs after the table say so.

| system | commit | typed write gate | authority classes | valid time | model may remove a fact |
| --- | --- | --- | --- | --- | --- |
| `aimee` typed facts | `50c5d88d` | yes, kind-validated | A / B / C, enforced | yes | no, superseded |
| Graphiti (Zep) | `c4069327` | no | none | yes | expired, retained |
| cognee | `fd5045f6` | optional, enrichment only | none | edge `updated_at` | tagged, retained |
| mem0 OSS | `3599aa75` | no | none | no | not in v3, ADD-only |
| Letta Code | `d1dc6880` | no | none | no | yes, block rewrite |
| LangMem | `29cbe41e` | no | none | no | yes, hard delete |
| Memobase | `358c16bb` | slot schema | none | no | yes, slot rewrite |

Graphiti is the closest architecture and the fairest comparison. It is
bitemporal: `valid_at`, `invalid_at` and `expired_at` all sit on `EntityEdge`,
and a contradicted edge is expired, with the row kept
([`edges.py:262-283`](https://github.com/getzep/graphiti/blob/c406932767ee490ad2311fd694a6b2ac3b164599/graphiti_core/edges.py#L262-L283)).

Custom edge types are supported and filtered per node-label pair. What that
filtering does is choose which type definitions the extraction prompt is shown
([`edge_operations.py:458-486`](https://github.com/getzep/graphiti/blob/c406932767ee490ad2311fd694a6b2ac3b164599/graphiti_core/utils/maintenance/edge_operations.py#L458-L486)).
Nothing then checks the relation the model returns against them. The validation
that does run on the way in checks that the LLM's entity names exist in the node
list and drops self-edges
([`edge_operations.py:210-241`](https://github.com/getzep/graphiti/blob/c406932767ee490ad2311fd694a6b2ac3b164599/graphiti_core/utils/maintenance/edge_operations.py#L210-L241));
the relation name is taken as given and becomes the edge's `name`.

There is no confidence, provenance or authority field on `EntityEdge` at all, so
an edge the user dictated and an edge the model inferred are indistinguishable
rows.

cognee has arrived at the same problem and named it. Its temporal conflict
resolver tags superseded edges and keeps them, which is the right behaviour, and
its module docstring explains why it cannot do that automatically:

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
An operator-supplied OWL file is matched fuzzily to enrich extracted entities,
and a name with no match is still constructed. Contradiction detection defaults
to `False`
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
an audit trail. The store itself still has no idea which line came from the
user.

LangMem lets the model delete a memory outright. `create_manage_memory_tool`
permits `create`, `update` and `delete` by default, and the delete branch is one
line: `await store.adelete(namespace, key=str(id))` on the async path
([`tools.py:293-294`](https://github.com/langchain-ai/langmem/blob/29cbe41e58528f92e9efa773c12e15c47be3808c/src/langmem/knowledge/tools.py#L293-L294)),
`store.delete(namespace, key=str(id))` on the sync one
([`tools.py:327-328`](https://github.com/langchain-ai/langmem/blob/29cbe41e58528f92e9efa773c12e15c47be3808c/src/langmem/knowledge/tools.py#L327-L328)).
No history row, no tombstone, no class check on what is being removed.

It is the plainest case in the set. A tool call the model chooses to emit
removes a fact a person stated, and afterwards the store cannot tell you it
happened.

Memobase does have a schema, and it is the closest thing here to an ontology.
Profiles are topic and subtopic slots and extraction fills them. Reconciliation
is an LLM choosing `APPEND`, `UPDATE` or `ABORT`, where `UPDATE` means rewriting
the slot's memo text
([`merge_profile.py:34-46`](https://github.com/memodb-io/memobase/blob/358c16bbc6d687937d79bc2f984a11c3be8da901/src/server/api/memobase_server/prompts/merge_profile.py#L34-L46)).
A slot holds one attribute of one profile, and the prior text does not survive
the rewrite.

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
object kind violates the relation's ontology is refused a row.

I looked for a counterexample among the systems I could read and did not find
one. That is a claim about what I searched. Hosted systems whose source I cannot
read are outside it, and so is any system I did not think to clone. One system with an authority column enforced on the write path would
settle it, and I would rather be shown one than keep the claim.

## What this design costs, and what it does not cover

An ontology that is wrong rejects facts that are true. The seed is seventeen
relations, so on a fresh corpus most of what arrives is novel, lands at Class C,
and has to earn its way to durable through three sightings across sources. A
fact stated once, in a domain nobody has taught the ontology, expires. That is
the deliberate trade for never letting speculation calcify, and it is a real
cost paid by the user who says something true once.

Retaining everything has a price too. Nothing is deleted, so `entity_edges`
grows with every correction, and a store that has been running for a year
carries every value each fact has ever held. Superseded rows are cheap to filter and they
still occupy disk.

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

Three checks to run against whatever memory system you have. The third should
worry you most.

Open the schema for a stored fact and look for a field recording who asserted
it, distinct from the model that wrote it down. If there is no such column, the
distinction does not exist at runtime, whatever the prompt says.

Follow the delete path from the model's tool surface and see what survives it. A
history table is worth having. A tombstone the recall path walks past is worth
more, because the fact is still in the graph.

Then try to write the two queries "what did you believe last week" and "what was
true last year" against different columns. If they are the same query,
corrections are overwrites and you cannot audit one.

If all three come back clean on something I have not read, send it to me. That is
the counterexample, and the claim above is written so it can lose to one.
