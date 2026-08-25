---
title: "The Remembering Is The Learning"
slug: the-remembering-is-the-learning
date: 2026-08-24
author: Rakuen Software
tags: [aimee, memory, knowledge-graph, ontology, authority]
excerpt: "Aimee learns by changing durable, evidenced records. Promotion, expiry, supersession and outcome-weighted recall decide what a later turn receives."
---

*Rakuen builds aimee, the system reported on here. Second in a three-article
series, after the
[self-learning loops](https://rakuensoftware.com/blog/aimee-recursive-self-learning)
and before the
[architecture](https://rakuensoftware.com/blog/everything-crosses-one-transport).
Source was rechecked against `testing` at `6bcc87e` on 25 August 2026.
Figures and source pins live in the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/the-remembering-is-the-learning/evidence/figures.md).*

The first article said that memory carries aimee's learning. Here is the
mechanism.

A later turn changes because a fact was promoted, expired, corrected, scoped or
demoted after use. Each change remains inspectable. “Learning” names those
changes and their effect on recall.

## Authority sets a fact's starting class

Every fact enters one of three confidence classes. The authenticated writer,
the asserted authority and the write-gate verdict choose the class.

A person asserting a recognised relation can create Class A evidence.
Background extraction can reach Class B. A new relation or another unconfirmed
claim begins in Class C.

The extraction path passes model authority as a constant. It cannot claim the
person's class from prompt text. Stored-note provenance comes from the
authenticated writer and defaults to agent-authored when that attestation is
absent.

The extractor also ignores confidence reported by the model. It commits a
triple only when both endpoints appear in the source note. This blocks invented
endpoints. A false relation between two names that are both present still
passes that check.

Class affects later recall, so a wrong class changes behaviour. It determines
how strongly the graph walk treats the edge.

## Repetition can buy durability

A scheduled maintenance pass promotes a repeatedly confirmed fact to durable.
A speculative fact that receives no further confirmation reaches its expiry
clock and stops matching current recall.

The rule is narrow: repetition buys durability. It does not raise authority. A
model inference can become durable while remaining Class B. A person asserting
a relation the vocabulary has not admitted still produces Class C evidence,
because the unsettled part is the relation itself.

Two defects show why the distinction matters. One maintenance job rewrote
confirmation counts on semantic edges, moving one Class A fact from 1 to 20 and
one Class C fact from 2 to 100. The lifecycle read those weights as
confirmations, so unsupported facts could promote and speculative facts could
avoid expiry.

A second defect let a co-occurrence update hit the same unique triple as a
direct assertion. Two names appearing in one session could count as another
assertion. In both cases the write completed. The learned confidence was wrong.

## Correction keeps the prior value legible

Each relation declares a correction policy. One policy supersedes the old
value and writes the replacement beside it. Another retires the old value from
current matching while retaining the row. A third refuses an unapproved
rewrite.

Single-valued relations compare confidence classes before applying that policy.
A Class B `works_for` write cannot displace a current Class A value or sit
beside it as a second current value. A person can replace a model value. Equal
classes use the relation's ordinary policy.

Retraction treats authority in the request body as a ceiling. The transport
must attest a person before the person-level path is available, and the memory
service repeats the check against its authenticated actor. Model-composed
context remains model authority even when it appears inside a user's turn. A
request may lower its authority and cannot raise it.

That rule closed four paths where a write could claim person-level authority
for itself. One was typed-fact ingress called by a model-composed tool query.
Before the fix, an agent could have used that route to retract a person's
fact.

Retained facts carry valid time and transaction time. One answers when the fact
held in the world. The other answers when the system believed it. Correction
therefore preserves both the old claim and the period during which it was
current.

## New vocabulary waits for an attributable decision

Facts are triples. Each relation declares the allowed types at both ends and
its cardinality. A relation connecting the wrong kinds of entity is refused
before the semantic edge is written.

The shipped vocabulary gives a fresh system enough relations to validate
immediately. Extraction may also propose a new relation. Facts using it commit
as Class C, and a sighting is counted only after the fact itself commits.

The count orders a review queue. It cannot activate the relation. Activation
requires an authenticated decision, and the ledger records the actor and
transport identity.

An automation can hold that credential and work the queue. The design requires
attribution, not a person at a console. Evidence sets priority, something named
signs, and the record shows which.

The extractor prompt tells the model to avoid catch-all relations such as
`misc`. The previous code guard disappeared when automatic count-based
activation was removed. A prompt instruction is weaker than a check, so a
catch-all can still reach the review queue. That remains a known limit.

## Identity is resolved before the write

Recall starts from entities named in the query. Splitting one person across
several nodes loses paths that should connect.

Aimee resolves the endpoints of a fact to canonical identities before storing
the relation. Names point to those identities. Literal values such as an age or
address take a separate path.

Completed merges are recorded and reversible. Ambiguous names enter a queue
with bounded retries while write and recall continue. Reversibility matters
because identity resolution is a learned judgement, and some judgements will
be wrong.

## Recall applies one learned score

Lexical and dense retrieval produce the first candidates. When graph fusion is
enabled, the top twelve candidates supply up to forty-eight canonical entity
seeds. Expansion collects their memories and follows direct neighbours.

One score ranks the result from **13 summed terms**: lexical match, coverage,
entity overlap, time, evidence, semantic match, state, query intent, salience,
surprise, graph proximity, PageRank and recorded outcome. Code proximity is a
label for the graph term when the path ran through code. Display confidence is
filled after ranking and is not a fourteenth ranking term.

The weights are fitted from retrieval features and recorded outcomes. A new
ranking model remains a proposal until it passes the benchmark gate. Applying
those weights on every turn is the learned retrieval model in use.

Confidence class changes that graph expansion. A semantic edge begins at 0.80.
Class A multiplies it by 1.0, Class B by 0.75 and Class C by 0.5.

That path once had two separate defects. Typed facts never entered graph
expansion. The fusion call also omitted the relation name, so every edge took
the unknown-relation default of 0.45. The store held the facts, yet recall used
neither their type nor their intended relation weight.

## Scope filters before ranking

Memory shares one graph across work. Query-time scope decides which rows the
caller may see.

Normal recall orders the active project first, its workspace second, and shared
or global memory third. A caller requesting one exact scope adds a narrower
band above those three. Rows outside the allowed bands are removed by a
predicate inside the query, and stable sorting preserves relevance within each
band.

Filtering inside the query avoids a signal from stronger hidden candidates
reaching the scorer. Applying scope after retrieval would reveal information
through timing and through which rows displaced visible ones.

Scope and maturity are separate axes. Five functional tiers describe how
settled an item is: Experience, Observation, World, Mental Models and Patterns.
Experience occupies two internal levels with different promotion and expiry
constants, so the implementation has six levels under five names.

A directive can require recorded operator approval because it changes later
work at the highest prompt priority. Scope still decides where that directive
may appear.

## Some knowledge can rise beyond one session

Pattern synthesis runs inside the maintenance cycle. A durable fact seen in
three distinct sessions can become a pattern when the other eligibility
conditions hold.

Entity-scope promotion uses a different count. Three distinct sources can move
an entity one step up the scope lattice, but that pass sits behind its own
configuration switch. The source header describes it as off by default.

Vocabulary growth takes the signed-review path described above. The three
mechanisms therefore resolve to one maintenance rule, one gated scope rule and
one attributable decision.

The consequence is slow learning across sessions. Work established by one
person can later help another after corroboration and scope promotion. The
system also keeps the origin of that knowledge, which is what lets a later
correction travel back through it.

## Outcomes can demote a memory

Recall records which memories were placed before the model. Later outcomes can
mark them accepted, corrected, contradicted, rolled back or irrelevant.

Demotion reads a time-decayed window of attributed outcomes. Its contract
excludes source tags, declared confidence, author id and retrieval frequency.
A popular memory therefore gains no protection from being popular. Under a
minimum number of outcomes, the scorer declines to judge.

Contradictions keep both claims and their sources. Policy may choose a current
value, while unresolved conflicts join a review backlog.

Memory quality becomes an outcome claim here. Retrieval frequency describes
use. Recorded outcomes describe what happened after use.

## Recalled text remains evidence

The context returned to a model is fenced as untrusted evidence. It does not
carry authorization and cannot become executable instruction merely by being
remembered.

The fence establishes protocol semantics only. It prevents the memory path
from granting authority by type. Models can still follow text they should have
treated as evidence, which has to be tested at the behaviour level.

## Every change leaves a correction path

Knowledge objects write into an append-only evidence ledger. Changesets group
mutations for display, diff and compensating revert. Documents move through
active, invalidated, retired and purged states. Derived memories name their
sources so staleness can queue them for rederivation.

Every close now submits an immutable audit intent in the same transaction as
the mutation. A separately credentialed worker builds the hash chain from
committed intents. The live test found one matching audit row for one closed
memory changeset; removing the five seal calls reduced that to zero.

Those mechanisms give a learned item an identity, evidence, time, scope and a
fate. They make a specific mistake traceable and reversible. They do not prove
the item is true, and they cannot recover information that was never recorded.

## The discipline is the product

The constraints cost time: a new relation waits for approval, and a memory
climbs on evidence. A correction retains the record it superseded. Outcome
demotion waits for enough outcomes to judge.

Fast, bad memory is the more expensive failure. It keeps returning plausible
answers, and each bad edge can change what the graph reaches for unrelated
queries. Later synthesis can spread the error further.

Two thin places remain visible. Endpoint checks miss a false relation between
names genuinely present in the note. Catch-all vocabulary is blocked by a
prompt instruction instead of code before review.

Settle the shape of a learned item before optimising where it lives. Identity,
evidence, time, scope and fate make later correction possible. Retrofitting
them means guessing what old rows meant after the system may already have acted
on them.
