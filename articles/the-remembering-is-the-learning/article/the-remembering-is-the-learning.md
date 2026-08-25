---
title: "The Remembering Is The Learning"
slug: the-remembering-is-the-learning
date: 2026-08-24
author: Rakuen Software
tags: [aimee, memory, knowledge-graph, ontology, authority]
excerpt: "A fact is born into a class, climbs to durable by being confirmed, expires when it stops being confirmed, and is superseded with its old value still legible. Those are what learning is, and aimee's memory is where it happens."
---

*Rakuen builds aimee, the system written about here. Second of three: the
[self-learning loops](https://rakuensoftware.com/blog/aimee-recursive-self-learning)
come first, the
[architecture](https://rakuensoftware.com/blog/everything-crosses-one-transport)
third. Source read from `testing` on 24 August 2026; figures are traced in the
[reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/the-remembering-is-the-learning/evidence/figures.md).*

The first article in this series made a claim it did not fully show: that there
is no separate thing called learning which uses memory to store its results.
Remembering, done properly, is the learning.

This is the machinery that makes that true. Read it with the verbs in mind.
Each of these looks like a storage feature and is doing something else.

## A fact is born into a class, and authority picks the class

Every fact enters in one of three classes. The asserted authority and the
write-gate verdict choose it.

Say something yourself, through a relation the system understands, and the fact
is Class A. It carries full confidence and is exempt from expiry. A background
extraction can reach Class B. Novel relations and other unconfirmed claims
begin in Class C.

The extraction path has no route from model authority to Class A. The extractor
passes model authority as a constant, so a fact-extraction prompt cannot claim
the user's class. Stored-note provenance is stamped from the authenticated
writer and defaults to agent-authored.

The extractor also ignores the model's self-reported confidence. It commits
only when both endpoints occur in the source note. That catches invented
endpoints. It does not catch a false relation drawn between two names that are
both really there.

The class feeds the weight that the recall walk applies later. Getting a fact
into the wrong class is not
a bookkeeping error, it is teaching the system something with the wrong
confidence.

## Promotion is learning. Expiry is forgetting

A fact that keeps being confirmed is promoted to durable by a scheduled
maintenance pass. A speculation that stops being confirmed runs out its clock
and is stamped as no longer believed.

Nothing decided that. No loop reasoned about it. Those two passes are the
system changing what it believes on the evidence, and they are ordinary memory
operations on a schedule.

The rule that keeps it honest is that repetition buys durability, not
authority. Reinforcement can make a model inference durable and it stays
Class B. A new relation remains speculation even when a person asserted it,
because the unsettled part is the vocabulary and personal authority cannot
settle that.

Getting this wrong is not hypothetical. Scheduling those two passes for the
first time exposed a maintenance job that rewrote confirmation counts on
semantic edges, taking a Class A fact from 1 to 20 and a Class C fact from 2 to
100. Weight on those edges is a confirmation count and the lifecycle reads it
as one, so that rewrite promoted things nothing had confirmed and stopped
anything ever expiring: the two outcomes the lifecycle exists to
prevent. A separate defect had co-occurrence upserts landing on the same unique
triple as real assertions, so two words appearing in one session counted as
somebody repeating themselves.

Both of those are learning defects wearing storage clothes. The store was
working correctly the entire time.

## Correction leaves the old value where it is

Each relation carries its correction policy. Most supersede: stamp the old
value and write the new one beside it. Some retire a stale value from matching
while keeping its row. Others refuse quiet rewrites.

The ordinary commit path applies class ordering. If a model extracts a
different object for a single-valued relation, the write compares the old and
new classes first. A Class B `works_for` write cannot supersede a current Class
A value.

It cannot sit beside it either, because a single-valued relation
must not end up holding two current values. A user write can replace a model
value. Equal-ranked writes fall back to the relation's ordinary policy.

A person can still supersede a protected value, and the authority for that is
derived. Retraction treats the request's authority as a ceiling: user authority
is granted only when the transport attested a person, and the knowledge service
repeats the check against its authenticated actor. Model-composed context-block
text is forced to model authority even when the turn around it belongs to a
user. A request body may lower its authority and never raise it.

That last rule closed a real hole. Four places had let a write decide for
itself that it spoke for the user, including a typed-fact ingress whose only
caller is a tool whose query the model composes. An agent could have retracted
the user's facts by writing "forget my email" into a query nobody asked for.

The retained rows carry two clocks. Valid time records when the fact held in
the world. Transaction time records when the system believed it. "What was true
last year" and "what did you believe last week" become different questions with
different answers, which is the difference between a memory and a log.

## The vocabulary is learned, and every addition is signed

Facts are triples, and each kind of relationship declares what may sit on
either end. Employment joins a person to an organisation; an address joins a
device to an address. The write gate looks up the relation and checks both
ends. If the model says the printer works for the kernel, the commit stops
before a row is written.

A shipped vocabulary lets a fresh system validate before it has learned
anything. The live set can grow, with cardinality and endpoint rules on each
relation.

A relation nothing has seen enters as speculation. Facts using it still commit,
as Class C, and the sighting is counted. A sighting registers only after its
fact commits, so failed writes do not raise a candidate's standing and a
rejected relation keeps that verdict.

What the count buys is position in a review queue, not entry to the vocabulary.
Activating a relation is an authenticated decision, written to the ledger with
the actor and the transport identity on the row, however often extraction saw
it. That is a change. Three committed sightings used to promote a relation on
their own, and this release replaced the counter with a decision that has to be
signed, on the stated grounds that activating a predicate is not something
recurrence should settle.

The actor is a credential, not necessarily a person. An automation holding that
credential can work the queue, so the design does not require a person at a
console.

What it refuses is an activation attributed to nobody. Evidence sets the
queue's priority, something named signs, and the ledger records which identity
made the decision.

Catch-alls such as `misc` are excluded by an instruction in the extractor's
prompt. The code guard that used to drop them went out with the counter it
guarded, and a prompt is a weaker thing than a check. Whatever works the queue
inherits that job, and an automation approving on a count alone is back to
where the old sweep was, minus the guard.

A person can also teach a domain from its documentation before any evidence has
accumulated. That door and the queue differ in bulk rather than in kind: a
whole vocabulary at once from a document, or one relation at a time as evidence
raises it.

## Identity comes before storage, and a bad guess is reversible

The graph walk starts from the entities a candidate mentions, so splitting one
person across three nodes loses paths that should have been found.

The ends of a fact are resolved to an identity before the fact is stored. Names
point at that identity, never at other names. Values such as an address or an
age bypass the identity register entirely.

Every completed merge is recorded and reversible. A name with several plausible
owners goes to a queue with bounded retries, and blocks neither write nor
recall. That is deliberate and I would argue for it anywhere: learning that
cannot be undone is not learning, it is damage.

## One recall, one score, and that score is the learned model being applied

Lexical matching and dense retrieval produce the first candidates. When graph
fusion is enabled, the top twelve supply up to forty-eight canonical entities
as seeds. Expansion collects the memories attached to each seed and follows
direct neighbours using the relation and authority class of each edge.

The graph adds memories that both lexical and vector search missed. A question
can share no words with its answer if an entity connects the two.

One score of thirteen summed parts ranks the result: lexical match, coverage,
entity overlap, time, evidence, semantic match, state, query intent, salience,
surprise, graph proximity, PageRank and recorded outcome. Code proximity is a
label for the graph term when the path ran through code. Display confidence is
filled after ranking and is not a fourteenth term.

The weights are fitted from feature rows and recorded retrieval outcomes. A new
ranking model lands as a proposal until a benchmark gate promotes it.

The weight vector records what the system has learned about which evidence to
trust. Applying it on every turn is the learning operation.

Confidence class enters graph expansion. A semantic edge begins at 0.80. Class
A multiplies it by 1.0, Class B by 0.75 and Class C by 0.5.

That path once had two defects. Typed facts never entered graph expansion, and
the fusion call omitted the relation name, so every edge took the
unknown-relation default of 0.45. The memory held the facts while recall used
neither their type nor their intended relation weight.

## Scope ranks inside the query

Memory shares one graph, and query-time scope separates projects and
workspaces.

A recall carries the caller's active project and workspace. Normal recall puts
the active project in the first visibility band, the workspace in the second,
and shared or global memory in the third. A caller requesting one exact scope
adds a narrower band above those three.

The query receives scope as bound parameters. A matching predicate removes
other rows before ranking, and stable sorting preserves relevance inside each
band. Filtering afterwards would leak through timing and through which hidden
candidates reached the scorer.

Underneath runs a second axis: how settled a memory is. Five functional tiers,
from Experience through Observation, World and Mental Models to Patterns. Raw
session logs and atomic actions are Experience; facts deduplicated out of them
are Observation; slow-changing environment context is World; approved
directives are Mental Models, injected at the highest prompt priority; and
patterns synthesised across sessions are the top. A memory climbs that ladder
through evidence, and a directive can require a recorded operator approval
because it changes future work.

Experience occupies two storage levels, which is worth knowing if you go
looking at the rows: L0 and L1 carry different promotion and expiry constants
and rank differently, and both answer to the same functional name. Five tiers,
six levels.

Tier records how settled a memory is. Scope records where it may appear. Mixing
the two causes a system to leak information or discard useful memory.

## What a team knows, distilled out of work nobody filed

The design goal is refinement under use. Something one engineer established can
climb out of its original scope after independent work corroborates it, and
nobody has to file or curate anything. That is the goal. Two of the three
mechanisms under it sit behind their own switches.

Three was the default threshold in three places, and the units differed. Two of
them still run on a count. A durable fact seen in three distinct sessions can
become a pattern, and that pass runs inside the maintenance cycle. An entity
corroborated by three distinct sources can move one step up the scope lattice,
and its own header records that pass as off by default.

The third is gone. A novel relation used to join the vocabulary on three
committed sightings, and the count now orders a review queue instead. Of the
three thresholds this article started with, one is automatic, one is available
and off, and one has become a decision that carries a name.

Months later, somebody who never spoke to the first engineer can receive an
answer carrying what that work established. That is the loop closing on a
timescale no session can see.

## Demotion reads outcomes

Each recall records which memories were placed in front of the model. Memories
that shaped the answer receive an outcome: accepted, corrected, contradicted,
rolled back, or beside the point.

Demotion reads a time-decayed window of those outcomes, and its contract admits
attributed outcome evidence and nothing else. Source tags, declared confidence,
author id and retrieval frequency are each excluded by name.

So a frequently retrieved memory that keeps failing sinks. Independent sources
asserting the same thing still count as corroboration, because retrieval
frequency is a property of ranking while source count is evidence about the
claim. Under a floor of recorded outcomes the scorer declines to judge at all,
and says so.

This is the counterfactual discipline from the first article, arriving in the
memory layer. What a memory is worth is what happened when it was used.

Contradictions are not resolved by picking a winner. Both claims stay, linked,
with their sources intact. Policy chooses the current value, and unresolved
conflicts join a backlog beside stale facts and thinly covered topics.

## One bad write spreads, which is what the discipline is for

A wrong fact in an isolated fact store harms the queries that retrieve it. In a
fused graph an edge changes what the walk reaches and what enters the ranking,
including queries that mention neither endpoint. On a shared deployment, later
sessions can carry it into pattern synthesis.

A bad write spreads. That is the entire reason for the gate, the classes, the
identity resolution and the reversible merge, and it is why those cost what
they cost.

## Recall hands back evidence

What memory returns is fenced. Injected context is untrusted evidence, not
authorization and not executable instruction.

The fence marks recalled text as evidence rather than authorization. It does
not prove a model will never follow a malicious instruction embedded in that
text. Without the distinction, anything that got itself remembered would enter
later turns in the same role as an instruction from the harness.

## Every decision is answered somewhere with a name

The decisions around a memory write or recall have named providers. The caller
does not quietly replace an unavailable answer with a permissive local one.

Failure behaviour depends on what is at risk. The write gate defers so the
caller can retry. Extraction returns an error because an error and no facts are
different answers. Privacy gates withhold, and the retraction pre-scan leaves a
fact in place because an extra retained fact is recoverable while a mistaken
deletion is not.

This is where the architecture in part three meets the lifecycle in this
article: the memory rules are only useful if an unavailable decision cannot
masquerade as approval.

## A learned thing has an identity, a date, and a delete

Underneath all of the above, every knowledge object writes to one append-only
evidence ledger, with transactional mutation guards and an authenticated actor
on each row. Changes group into changesets that can be shown, diffed, previewed
and reverted by compensation. Documents move through active, invalidated,
retired and purged, with a bounded blast-radius preview before and a
content-free purge receipt after.

Derived memories declare what they were
derived from, so staleness propagates and a rederivation queue picks them up.
Recall explanations are persisted and scoped, carrying lane, contribution,
gate, staleness and provenance.

What makes a learned thing a thing at all is an identity, a date, an evidence
chain, a fate, and a delete. The first article argued that none of the loops
survives translation into model weights. This is the reason. You cannot walk a
gradient step's evidence chain to its roots, and you cannot revert one commit's
worth of weight update because someone later said it was wrong.

## Slow on purpose, and thin in two named places

The discipline is not free and some of it is slow on purpose. A novel relation
waits for a signed approval. A memory climbs tiers on evidence. An operator
approval gates policy.

I will defend the slowness, and the reason is not caution in the abstract.

A system with no memory is limited. A system with fast, bad memory is more
dangerous because it is confidently wrong and stays that way. The
failure does not announce itself as a failure: recall keeps answering, the
answers keep sounding reasonable, and the wrong thing propagates into
everything downstream that treats memory as settled.

No memory costs capability. Bad memory learned quickly costs the ability to trust anything
the system says, including the parts that were fine. Given the choice I would
take the first one, and none of these thresholds exists to make that choice
unnecessary.

Two limits remain. The extractor's endpoint check catches
invented endpoints and does not catch a false relation between two names that
are genuinely present in the note. And the bar against catch-all predicates is
now an instruction in a prompt rather than a check in code, so what stops a
`misc` reaching the review queue is a model following an instruction.

Both are known and both are narrower than the guarantees around them. The
first is unfixed in this release. The second this release created, by removing
the check and keeping the requirement.

If you are building memory for a model to use, settle what a learned thing is
before settling where to put it. An identity, a date, an evidence chain, a fate
and a delete are the five fields that make every later correction possible, and
they are cheap to write on the first day. Adding them afterwards means going
back through rows that were stored without them, deciding what each one meant,
and guessing at the provenance of anything already acted on. That is the
expensive version, and it is the one most systems end up buying.
