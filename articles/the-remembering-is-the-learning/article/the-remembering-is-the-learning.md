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

This matters more than it sounds, because the class is the weight. It is what
the recall walk multiplies by later. Getting a fact into the wrong class is not
a bookkeeping error, it is teaching the system something with the wrong
confidence.

## Promotion is learning. Expiry is forgetting

A fact that keeps being confirmed is promoted to durable by a scheduled
maintenance pass. A speculation that stops being confirmed runs out its clock
and is stamped as no longer believed.

Nothing decided that. No loop reasoned about it. Those two passes are the
system changing what it believes on the evidence, and they are ordinary memory
operations on a schedule.

The rule that keeps it honest: **repetition buys durability, it does not buy
authority.** Reinforcement can make a model inference durable and it stays
Class B. A new relation remains speculation even when a person asserted it,
because the unsettled part is the vocabulary and personal authority cannot
settle that.

Getting this wrong is not hypothetical. Scheduling those two passes for the
first time exposed a maintenance job that rewrote confirmation counts on
semantic edges, taking a Class A fact from 1 to 20 and a Class C fact from 2 to
100. Weight on those edges is a confirmation count and the lifecycle reads it
as one, so that rewrite promoted things nothing had confirmed and stopped
anything ever expiring: precisely the two outcomes the lifecycle exists to
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
A value, and it cannot sit beside it either, because a single-valued relation
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

## The vocabulary itself is learned, and slowly

Facts are triples, and each kind of relationship declares what may sit on
either end. Employment joins a person to an organisation; an address joins a
device to an address. The write gate looks up the relation and checks both
ends. If the model says the printer works for the kernel, the commit stops
before a row is written.

Seventeen relationships ship with the system so a fresh install can validate
before it has learned anything. The live set sits in a table the running system
can extend, with cardinality and endpoint rules on each relation.

A relation nothing has seen enters as speculation, and the sighting is counted.
A sighting registers only after its fact commits, so failed writes do not raise
a candidate's standing and a rejected relation keeps that verdict. Three
committed sightings let the maintenance pass promote the relation. Catch-alls
such as `misc` never qualify, because they cannot later reconcile to anything
specific.

A person can also teach a domain from its documentation before any evidence has
accumulated. That is the human path into the vocabulary, and it is deliberate:
the slow evidential path is the default, and there is a second door.

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

Lexical matching and dense vectors produce the first candidates. The top twelve
supply up to forty-eight canonical entities as seeds. Expansion collects the
memories attached to each seed, then follows direct neighbours using the
relation and authority class of each edge.

The graph adds memories that both lexical and vector search missed. A question
can share no words with its answer if an entity connects the two.

One fourteen-part score ranks the result: lexical and dense match, graph and
code proximity, confidence, evidence, time, query intent. A typed fact, a
conversation from March and a function edited last week compete on one scale.
Reserved slots keep summaries and facts from being crowded out. The winners
pull in neighbouring turns, and then scope removes anything the caller cannot
see.

The weights are fitted from feature rows and recorded retrieval outcomes. A new
ranking model lands as a proposal until a benchmark gate promotes it.

Read that last paragraph again as a learning operation. What the system has
learned about which evidence to trust is the weight vector, and applying it is
what happens on every turn.

Confidence class enters here too, and once did not. Typed facts were excluded
from this walk altogether, so a user-stated, type-validated fact contributed
nothing to it. Worse, the gravity table was dead at the fusion call site, which
passed no relation at all and so took the unknown-relation default of 0.45 for
**every** edge. Nothing was being weighted by what it was. Fixed, a typed fact
takes a semantic baseline of 0.80 and its class multiplies that: A at 1.0, B at
0.75, C at 0.5.

## Scope ranks inside the query

Memory shares one graph, and query-time scope separates projects and
workspaces.

A recall carries the caller's active project and workspace. Active-project
memory takes the first visibility band, the workspace the second, shared or
global memory the third. Anything else scores zero. The database query receives
that ranking as parameters, because a filter applied afterwards leaks through
timing and through which candidates reached the scorer at all. A stable sort
preserves relevance inside each band, so the caller gets the best match they
may see with no signal that a stronger hidden one exists.

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

Tier records how settled a memory is. Scope records where it may appear. They
are different questions, and I think conflating them is how a system ends up
either leaking or forgetting.

## What a team knows, distilled out of work nobody filed

The design goal is refinement under use. Something one engineer established can
climb out of its original scope after independent work corroborates it, and
nobody has to file or curate anything.

Three is the default threshold in three places, and the units differ. A durable
fact seen in three distinct sessions can become a pattern. An entity
corroborated by three distinct sources can move out of local scope. A novel
relation joins the vocabulary after three committed sightings.

That last counter does not record distinct sources. One participant can repeat
a relation to the threshold. The fact still enters as speculation, but
vocabulary promotion is weaker evidence than the other two paths, and it is
worth knowing which of the three you are looking at.

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

A model reading its own memory is reading evidence about the world, not
receiving orders. Without that boundary the recall path would be an injection
surface pointed directly at the learning loops, since anything that could get
itself remembered could later instruct the thing that remembered it.

## Every decision is answered somewhere with a name

Memory is required core. Its descriptor sets `runtime_toggle.supported` to
false: it cannot be removed from a running profile. Readiness means durable
storage opens and the configured embedding path has a compatible dimension. A
lexical fallback preserves a degraded lookup and does not make the deployment
compliant, which is the difference between a thing that answers and a thing
that remembers.

Five decisions cross the transport, each on its own event: whether a candidate
triple may commit as a semantic edge, extraction and the retraction pre-scan,
the PII recall gate, the confidence band, and embedding.

Four of those are pure decisions, and each is served by a registered provider
that is authoritative and never falls back to the local implementation, on the
stated grounds that a silent fallback lets a broken module look healthy.
Embedding is the exception and is arranged differently: the module serves HTTP
embedders behind its own circuit breaker, while program-based embedders remain
in the host path by explicit contract, with the module returning a decline on
those commands.

What a failure does is chosen per seam, and the set is worth reading together.
The write gate defers, so nothing is written and the caller retries. Extraction
returns an error, because an error and "no facts" are different answers. Both
halves of the PII gate fail closed, withholding. The retraction pre-scan does
not retract, because that path deletes, and a fact left behind is recoverable
where one deleted by mistake is not.

Ported decisions are held to the original implementation by differential
fixtures generated from it, so no expectation is transcribed by hand from
reading it.

## A learned thing has an identity, a date, and a delete

Underneath all of the above, every knowledge object writes to one append-only
evidence ledger, with transactional mutation guards and an authenticated actor
on each row. Changes group into changesets that can be shown, diffed, previewed
and reverted by compensation. Documents move through active, invalidated,
retired and purged, with a bounded blast-radius preview before and a
content-free purge receipt after. Derived memories declare what they were
derived from, so staleness propagates and a rederivation queue picks them up.
Recall explanations are persisted and scoped, carrying lane, contribution,
gate, staleness and provenance. The ledger writes 10,000 events in 5.397 s at
812 bytes an event.

What makes a learned thing a thing at all is an identity, a date, an evidence
chain, a fate, and a delete. The first article argued that none of the loops
survives translation into model weights. This is the reason. You cannot walk a
gradient step's evidence chain to its roots, and you cannot revert one commit's
worth of weight update because someone later said it was wrong.

## The default store is boring on purpose, and you can replace it

Aimee installs by default onto PostgreSQL with pgvectorscale, and that is not
an accident or a shrug. It is one instance of the rule the whole system is
built on: almost unlimited customisation, over defaults chosen to be sensible
and boring. Everything in this article behaves the same way. The thresholds,
the class weights, the promotion and expiry clocks, the tiers and the scope
bands are all constants somebody can change, and the values shipped are the
ones we were willing to be woken up by.

I am not claiming it is the fastest way to do this. It is not. There are vector
databases built specifically for this workload that will beat it, some of them
substantially, and an end user who moves to one can expect a real improvement.

What we are unwilling to trade for that is the shape of the bad case. A store
that wins on the median and can stall for ten seconds under conditions nobody
has characterised is worth less to us than a slower one whose worst day is
written down, because the ten seconds is what a person sits through and what
somebody gets woken up about. This is not a claim that speed does not matter.
It is a claim about which number decides, and it is the same rule the transport
is held to in the third article, where the committed figure is a ceiling rather
than an average.

A published best-case figure for a vector store is not the number we are asking
for. The measurement itself is fine; the wrong end of the distribution was
published. Give us the worst case instead: where it stalls, what provokes it,
how long it lasts, how often. Then there is a real conversation to have, and it
could end with us moving.

So the vector store is a module you can swap.

What the default buys is the same thing the rest of this article keeps
choosing. The performance limits are known. How to improve them is thoroughly
understood. The documentation is extensive and mostly written by people who
were not selling anything. When it misbehaves, the shape of the misbehaviour
has a name and a mailing list thread from 2015.

The honest version of the reason is that the people who wrote aimee are the
people who get woken up by it, and we would rather be woken up by a mechanism
we understand than by a faster one we do not. That is a judgement about which
risk to carry, and if your operational situation is different then so is the
right answer. The module is there for exactly that.

The swap is genuinely supported, and that distinction is worth drawing. Someone
else's worst case may genuinely be a different one. Or they may have
characterised a faster store's tail on their own workload and know precisely
what they are carrying, which is a better-informed position about their
deployment than ours could be. If a purpose-built vector database is what a
user wants, that is a legitimate engineering decision and we back it, because
the criterion above belongs to us and to our situation.

## Slow on purpose, and thin in two named places

The discipline is not free and some of it is slow on purpose. A novel relation
needs three committed sightings before it joins the vocabulary. A memory climbs
tiers on evidence. An operator approval gates policy.

I will defend the slowness, and the reason is not caution in the abstract.

A system with no memory is useless. A system with fast, bad memory is worse
than useless, because it is confidently wrong and it stays that way. The
failure does not announce itself as a failure: recall keeps answering, the
answers keep sounding reasonable, and the wrong thing propagates into
everything downstream that treats memory as settled. No memory costs you
capability. Bad memory learned quickly costs you the ability to trust anything
the system says, including the parts that were fine. Given the choice I would
take the first one, and none of these thresholds exists to make that choice
unnecessary.

We did not reason our way to that position. Every constraint in this article
came out of running aimee in production and watching what went wrong: the
thresholds, the class ordering, the reversible merge, the outcome-only
demotion. The gravity default and the confirmation-count rewrite described
above are the same story at a smaller scale. Each of them is a rule that exists
because something happened without it.

Two limits worth stating plainly. The extractor's endpoint check catches
invented endpoints and does not catch a false relation between two names that
are genuinely present in the note. And the vocabulary-promotion counter does
not require distinct sources, so one determined participant can reach that
threshold alone.

Both are known, both are narrower than the guarantees around them, and neither
is fixed by anything in this release.

If you are building memory for a model to use, settle what a learned thing is
before settling where to put it. An identity, a date, an evidence chain, a fate
and a delete are the five fields that make every later correction possible, and
they are cheap to write on the first day. Adding them afterwards means going
back through rows that were stored without them, deciding what each one meant,
and guessing at the provenance of anything already acted on. That is the
expensive version, and it is the one most systems end up buying.
