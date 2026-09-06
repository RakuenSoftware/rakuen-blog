---
title: "The Remembering Is The Learning"
slug: the-remembering-is-the-learning
date: 2026-08-24
author: Rakuen Software
tags: [aimee, memory, knowledge-graph, ontology, authority]
excerpt: "Remembered failures can narrow the next attempt. Aimee keeps the evidence, authority and history needed to use those lessons, correct them when conditions change, and carry them into later work."
---

*Pre-print for public review. Not final publication.*

*Rakuen Software builds aimee, the system written about here. This is the
second technical article in the series. The
[overview](https://rakuensoftware.com/blog/the-work-should-survive-the-model)
introduces the project, and
[self-learning](https://rakuensoftware.com/blog/aimee-recursive-self-learning)
reports the task-outcome evidence. Mechanisms described here were read from
source in August 2026, including a recheck at `6bcc87e` on 25 August. Sources,
limits and later editorial changes are traced in the
[reporting record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/the-remembering-is-the-learning/evidence/figures.md).*

Aimee is an open-source knowledge platform for company AI work, available as a
managed cloud service or self-hosted. It brings documents, code, facts,
decisions and work history into one governed knowledge base. It scales from one
user to an entire company, with identity and scope deciding what each person
and AI model can retrieve.

Remembering becomes learning when stored experience changes a later decision.
A failed approach can remove a route from the next attempt. A correction can
replace a premise that earlier work relied on. Aimee preserves those records
with the authority, evidence and history needed to decide when they apply.

## A failed approach can teach more than the successful one

In our use, models have gained more from remembering failed approaches. Knowing
that X, Y and Z failed can narrow the search across different tasks. Knowing
that A succeeded is especially useful when the same task returns; its success
may depend on conditions the next task does not share. This is our observation
from use, and we have not measured failure memory against success memory in a
comparative study.

Consider an illustrative build failure. A command failed because the installed
compiler did not support a flag. A later task builds a different target with
the same compiler. Remembering that constraint can prevent another attempt with
the unsupported flag, even though the successful command for the original
build would not complete the new task.

The useful lesson includes the conditions that made the approach fail. A
compiler upgrade may invalidate it. A timeout establishes less than an explicit
unsupported-flag error. The memory needs to preserve the attempted approach and
observed result, with any established cause and its limits, so a later model
can judge whether the lesson applies.

[Our paired study](https://rakuensoftware.com/blog/aimee-recursive-self-learning)
showed that a recalled failure changed outcomes on repeated tasks under a fixed
consumer. Results on new tasks were unchanged. The study establishes a benefit
from that failure record on tasks it covered; the broader transfer described
above remains an observation and an engineering argument.

A useful record of failure must also remain correctable. If the compiler gains
support for the flag, an old restriction can now prevent useful work. The same
memory machinery that preserves the lesson must let later evidence revise it.

## Authority decides what a new fact can replace

Memory holds several kinds of record. Typed facts express a claim as a subject,
a relation and an object. Each relation declares what may sit on either end:
employment joins a person to an organisation; an address joins a device to an
address. The write gate checks those types before committing a fact.

Every typed fact enters in one of three classes:

| class | what enters it | starting consequence |
| --- | --- | --- |
| A | a direct statement through an established relation | full initial confidence and no expiry |
| B | a background extraction using established vocabulary | an inference that evidence can reinforce or weaken |
| C | a novel relation or another unconfirmed claim | speculation pending confirmation or review |

The authority and write-gate verdict set the starting class, confidence and
lifecycle. These are system rules for handling a claim. A person can make a
false statement even when the system authenticates them correctly.

The extraction path fixes model authority before the prompt runs. Text emitted
by the model cannot claim the user's class. Stored-note provenance comes from
the authenticated writer and defaults to agent-authored.

The extractor ignores the model's self-reported confidence and commits only
when both endpoints occur in the source note. That catches invented endpoints.
It does not catch a false relation between two names genuinely present in the
note. A classification or extraction mistake can therefore give later work an
incorrect premise, even when the checks ran as designed.

For an illustrative correction, suppose a person states that they work for
Acme and the statement enters as Class A. A model then extracts a different
employer as Class B. For the single-valued `works_for` relation, the Class B
write cannot supersede the Class A value or sit beside it as a second current
value. A user write can replace a model value; equal-ranked writes follow the
relation's correction policy.

Retraction also derives authority from the caller. The transport must attest
a person before granting user authority, and the knowledge service repeats the
check against its authenticated actor. Model-composed context-block text keeps
model authority even inside a user's turn. A request body may lower its
authority and cannot raise it.

This check closed four places where a write could claim to speak for the user,
including typed-fact ingress reached through a model-composed tool query. An
agent could have retracted the user's facts by writing "forget my email" into
a query nobody asked for. The
[authority fix](https://github.com/RakuenSoftware/aimee/pull/2828) records the
paths and their correction.

An unavailable decision must remain visible to the caller. The write gate
defers so the caller can retry; extraction returns an error, preserving the
difference between a failed extraction and a successful one that found no
facts. If the retraction pre-scan cannot decide, it leaves the fact in place.

## New vocabulary requires attributable approval

A shipped vocabulary lets a fresh system validate facts immediately. If the
model says the printer works for the kernel, the endpoint check stops the
commit. The vocabulary can grow, with cardinality and endpoint rules attached
to each relation.

Facts using a novel relation enter as Class C. A sighting counts only after its
fact commits, and a rejected relation keeps its verdict. Sighting counts order
a review queue. Activation requires an authenticated decision recorded in the
ledger with the actor and transport identity.

Three committed sightings used to activate a relation automatically. The
[evidence-lifecycle change](https://github.com/RakuenSoftware/aimee/pull/2831)
replaced that threshold with approval. An automation holding the required
credential can work the queue. Every activation must still be attributable to
the identity that approved it.

The change also removed the code guard against catch-all relations such as
`misc`. An instruction in the extractor's prompt still excludes them, but the
model has to follow it. Whatever approves the queue inherits that check; an
automation approving solely on a count would restore the old sweep's behaviour
without its code guard.

A person can also teach a domain from its documentation, supplying a vocabulary
before repeated extraction has accumulated evidence. Established vocabulary
and authenticated authorship answer separate questions. A person's assertion
using an unsettled relation still enters as speculation.

## Confirmation changes durability while authority stays fixed

A scheduled maintenance pass can promote a repeatedly confirmed fact to
durable. Speculation without continued confirmation reaches its expiry and is
marked as no longer believed. Expiry withdraws the system's support for the
claim; it does not establish that the opposite is true.

Reinforcement can make a Class B inference durable. It remains Class B. The
system can retain a useful inference for longer while preserving who supplied
it and what authority it has over conflicting claims.

Scheduling promotion and expiry first exposed a maintenance job that rewrote
confirmation counts on semantic edges. A Class A fact went from 1 to 20 and a
Class C fact from 2 to 100. The lifecycle read those weights as confirmation
counts, so the rewrite could promote unsupported facts and prevent affected
facts from expiring.

A separate defect let co-occurrence upserts land on the same unique triple as
real assertions. Two words appearing in one session then counted as another
confirmation of their relationship. The
[typed-fact and lifecycle repair](https://github.com/RakuenSoftware/aimee/pull/2824)
records both defects and their corrections.

The maintenance jobs had changed what later work would receive as established
knowledge. Reads and writes continued to work throughout.

## Recall determines whether a lesson reaches the next task

The graph walk depends on identity. Splitting one person across three nodes
loses paths that should have been found. Before storing a fact, the system
resolves its endpoints to identities; names point at those identities. Literal
values such as an address or age bypass the identity register.

Completed merges are recorded and reversible. A name with several plausible
owners goes to a queue with bounded retries while writes and recall continue.
Later evidence can undo a mistaken merge.

Lexical matching and dense retrieval produce recall's first candidates. When
graph fusion is enabled, the top twelve supply up to forty-eight canonical
entities as seeds. Expansion collects memories attached to each seed and
follows direct neighbours using the relation and authority class of each edge.
It can add memories that the initial searches missed.

For the illustrative compiler failure, useful recall would connect the later
build task to the constraint even when the target name has changed. Storing the
failure alone does not establish that a different query will retrieve it. That
is the practical requirement the retrieval machinery has to meet.

A score of thirteen summed terms ranks candidates using signals including
lexical and semantic match, graph proximity and recorded outcome. The
[reporting record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/the-remembering-is-the-learning/evidence/figures.md)
lists the terms. Display confidence is filled after ranking and sits outside
the score. Ranking weights are fitted from feature rows and retrieval outcomes;
a proposed replacement must pass an evaluation gate.

Authority class also affects graph expansion through explicit multipliers. A
semantic edge begins at 0.80; Class A multiplies it by 1.0, Class B by 0.75 and
Class C by 0.5. These class rules and the fitted ranking weights are separate
parts of retrieval. Together they determine which records later work sees and
how strongly those records rank.

This path had two defects recorded in the same typed-fact repair. Typed facts
never entered graph expansion, and the fusion call omitted the relation name,
so every edge took the unknown-relation default of 0.45. The memory held the
facts while recall used neither their type nor their intended relation weight.

An incorrect edge can also change which other memories the walk reaches,
including on queries that mention neither endpoint. Later sessions can carry
that error into pattern synthesis. Admission checks and reversible identity
merges limit the routes by which one bad write affects further work.

## A memory of failure can be useful evidence

Each recall records which memories were placed in front of the model. The
outcome system attributes results to memories: accepted, corrected,
contradicted, rolled back, or beside the point. Demotion reads a time-decayed
window of those attributed outcomes.

Its contract excludes source tags, declared confidence, author id and retrieval
frequency. Frequently retrieving a memory supplies no outcome evidence by
itself. Below a minimum number of recorded outcomes, the scorer declines to
judge. This describes the attribution contract; it does not establish a causal
comparison between using and withholding each memory.

For failure learning, the outcome of the original attempt and the usefulness of
its record are separate judgements. A record of an unsuccessful build can help
the next task avoid the unsupported flag. Demoting that record solely because
the build failed would discard the lesson. If conditions later change, evidence
that the remembered restriction is obsolete gives the system a reason to revise
it.

Contradicting claims remain linked with their sources intact. Policy selects
the current value, and unresolved conflicts join a review backlog beside stale
facts and thinly covered topics. Preserving the disagreement lets a later
correction retain the evidence that preceded it.

## Sharing a lesson changes who can receive it

Recall carries the caller's active project and workspace. Normal recall ranks
the active project in the first visibility band, the workspace in the second,
and shared or global memory in the third. An explicitly requested exact scope
gets an additional band above those three.

Bound query parameters supply the scope. A separate predicate excludes
out-of-band rows before ranking, and stable sorting preserves relevance within
each band. Privacy gates withhold recalled material when their decision is
unavailable.

Memory maturity has its own classification. Five functional tiers cover raw
experience, deduplicated observations, slow-changing world context, approved
mental models and patterns synthesised across sessions. Experience occupies
two storage levels, L0 and L1, with different promotion and expiry constants and
ranking priorities. The system therefore has five functional tiers over six
storage levels.

A durable fact seen in three distinct sessions can become a pattern during the
maintenance cycle. That cycle has its own enablement gate. Entity promotion
uses three distinct sources to move an entity one step up the scope lattice;
it has a separate switch, described as off by default in its header.

Those counts establish distinct sessions or sources. They do not by themselves
establish that the evidence is independent.

The design can carry a lesson from one engineer's work into a later colleague's
answer. Moving evidence into wider scope also changes who can receive it.
Corroboration alone cannot establish permission to disclose it. The source
checks recorded here establish the promotion and query-filtering mechanisms;
they leave the complete authorisation path for scope promotion to be verified.

Approved directives in the Mental Models tier can receive the highest prompt
priority, with a recorded operator approval where required. Ordinary recalled
text returns inside an evidence fence as untrusted material, separate from
executable instruction and authorisation. These are different uses of retained
knowledge, and the approval boundary matters when a lesson becomes a directive.

The evidence fence cannot guarantee that a model ignores every malicious
instruction inside recalled text. It marks the role of that text for the model
and surrounding policy to enforce.

## Correction must reach what the old claim produced

Relations carry their own correction policies. Most supersede an old value by
stamping it and writing the replacement beside it. Some retire a stale value
from matching while retaining its row. Others refuse quiet rewrites.

Retained rows carry two clocks. Valid time records when the fact held in the
world. Transaction time records when the system believed it. They let an
operator distinguish what the system believed last week from when the recorded
fact applied.

Knowledge objects write changes to an append-only evidence ledger with
transactional mutation guards and an authenticated actor on each row.
Changesets can be shown, diffed, previewed and reverted through compensating
changes. Documents have active, invalidated, retired and purged states. Purge
has a bounded preview of affected records and leaves a content-free receipt.

Retaining an old value makes supersession inspectable. A purge removes content
and leaves its receipt. Those operations have different recovery consequences;
the availability of compensating changes is not a promise to recover purged
content.

Derived memories declare their sources. When a source becomes stale, that
state propagates and a rederivation queue picks up the affected memories.
Recall explanations are also persisted and scoped, recording contributions,
gates, staleness and provenance. Correcting a source can therefore reach beyond
the original row to work that inherited it.

For the illustrative compiler lesson, an upgrade changes the condition that
made the earlier failure useful. A corrected record needs to preserve why the
old advice applied and when it stopped applying. Otherwise the next model can
repeat either mistake: attempting the unsupported operation in the old
environment or avoiding a valid operation in the new one.

Caution has a cost. A useful new relation may wait for approval, and an outdated
human assertion can outrank a correct model inference until it is corrected.
The operator needs the evidence and a route to revise the decision. Keeping an
incorrect claim durable would preserve the original mistake.

If you are building memory for a model, preserve the source, scope and relevant
conditions when the record is first written. Keep enough history to revise it
after another task has used it, and record which derived memories depend on it.
Later correction needs that information from the earlier work.
