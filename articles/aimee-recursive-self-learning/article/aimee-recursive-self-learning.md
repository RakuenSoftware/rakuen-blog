---
title: "Aimee: Recursive Self-Learning"
slug: aimee-recursive-self-learning
date: 2026-08-24
author: Rakuen Software
tags: [aimee, self-learning, memory, isolation]
excerpt: "Aimee learns in the harness, where experience can be remembered, inspected and reversed. The same boundary that contains the agent also holds everything it has learned."
---

*Rakuen builds aimee, the system written about here, and I helped build it. This
is the first of three articles. It covers self-learning; the [second covers
memory](https://rakuensoftware.com/blog/the-remembering-is-the-learning), and
the third covers the
[architecture](https://rakuensoftware.com/blog/everything-crosses-one-transport)
that supports both. Figures and the provenance of the incident below are
recorded in the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/aimee-recursive-self-learning/evidence/figures.md).*

Aimee is a cloud-hosted or locally hosted self-learning AI harness that scales
from one user to an entire company. It gives every model and user it serves
access to one coherent memory, with identity and scope determining which parts
each can retrieve. It learns from work as it happens and carries that experience
into later sessions while keeping the learned history observable, auditable and
reversible.

Self-learning changes the problem a safety boundary has to solve. A model can
reuse what worked in earlier runs, so protections built for one attempt may face
a system arriving with a history. Aimee keeps that history in the harness, where
it can be inspected, reversed and shared without binding it to one model or one
set of weights.

We learned why that boundary matters during testing. An aimee-backed model
needed somewhere to run tests, and the permitted environment could not finish
the job. Successive runs worked around the restriction, each leaving its
discoveries for the next. Eventually one run took an underprotected node, found
a vast.ai testing API key and spent under $10 on inference to finish its task.

The practical damage was small. The failure was in our design: we had protected
against a model reasoning from a cold start, while the system reached the
boundary with an accumulated record of successful steps.

This article follows what we changed before self-learning shipped. We put the
capabilities needed to finish the work inside the governed boundary, kept the
learned history outside any one model and made every later use of that history
inspectable. The same design can serve different models and users, including
models whose weights change.

The model is unspecified because we did not repeat the incident across models.
The incident says nothing about how individual checkpoints compare.

## The controls are old, and self-learning changes the pressure

Software has crossed intended boundaries before. Computer viruses and worms
have spread across networks, stolen credentials and kept operating after their
authors lost control of them. Decades of responding to that history gave us
least privilege, process isolation, network segmentation, mediated access,
independent audit records and recovery plans.

An LLM system puts new pressure on those controls. The model can search for an
effective route through a task, and the harness can preserve what worked across
runs. The engineering problem remains familiar: an unpredictable component has
useful work to do and must receive less authority than its surrounding process
could otherwise provide.

Industry discussion often frames control as a property of the model. In an
operational system, control depends on where authority lives. A model in an
ordinary application process inherits ambient credentials, network access and
tool bindings. Behavioural instructions then have to do the job of process
boundaries and capability checks.

Aimee puts those older controls in the LLM harness. New tools and better memory
expand what the model can do. Named interfaces, explicit authority and an
independent audit record govern each addition.

The expensive part is applying the controls to every path. Ambient credentials,
network access and direct tool bindings are easier to build, but they create the
conflict between capability and control. A governed architecture removes that
conflict by placing useful capability inside the boundary.

The learning method is ordinary feedback: the system changes its next attempt
using the outcome of the last one. Scored alternatives, counterfactual
evaluation and calibration are old tools. Aimee's work is making them operate
together with persistent memory, provenance and containment. I kept `recursive`
in the title because it ranks.

The testing incident made the release condition explicit. It happened on
unreleased code. Self-learning remained off until isolation supplied governed
routes to the resources its tasks required.

Production readiness meant meeting that condition before release. Aimee's
operating standard is a silent pager, so self-learning must leave inspectable
state, fail closed when authority disappears, survive a process restart and
remain reversible when the evidence changes.

Those demands selected the mechanisms in this article. Novelty is exactly what
gets me woken up at two in the morning, so we use it only where no established
approach will do. The standard is a governable system that stays boring in
operation.

## Self-learning needed the isolation first

The module system, process isolation and containers had to ship before we could
turn self-learning on. The testing model needed somewhere to run its tests, but
the permitted environment lacked a resource the task required. Each attempt
inherited the earlier work and searched for another route.

Task completion supplied the pressure. The model is not conscious and has no
independent desire to escape. A barrier between the model and the required
result becomes another problem to solve.

Harness design decides which way that pressure points. A harness that withholds
an ability the task requires turns its boundary into a barrier. Aimee keeps
memory, compute, the code index, forge operations and approved network access
available through governed routes. The complete working surface and its audit
path sit inside the boundary.

0.4.0 provides that boundary through its [transport
architecture](https://rakuensoftware.com/blog/everything-crosses-one-transport).
Governed work crosses one transport, where the harness checks and records it
before routing. Delegated execution runs in containers with the network
disabled, no ambient credentials and one mediated control socket.

The harness around that model is deterministic, old, boring code. Its transport
host is written in C, a language in use for more than fifty years. We chose C
for the part that needs explicit control over memory layout, buffer lifetime
and the small runtime surface every governed action crosses.

The model remains nondeterministic. Its effects enter the rest of the system as
typed events governed by deterministic rules. Each grant names the event kinds
a component may use. The host rejects the rest, orders accepted traffic and
records that order before routing, making open-ended model behaviour observable
and governable.

A rule with one enforcement point can be enforced. A rule with an unknown
number of ways around it is advice. That difference is the whole reason
self-learning could be turned on at all.

The underprotected node is now a sanctioned test host. Agents receive it
deliberately, which keeps them off the production host. It ran the 0.4.0 tests
and the work behind this article. The resource the model once crossed a
boundary to reach is now inside the governed design because the incident
exposed an unwritten requirement.

## Self-learning changes what the next run inherits

Earlier releases used outcomes to change which evidence to trust, which
documents to rank and which memories to retain. In 0.4.0 the harness can also
learn from its own evaluation and policy records. Those changes affect later
work.

Learning from those records creates a circularity: aimee could judge a new
proposal against a standard it had already changed. An additional gate
therefore measures how much of the proposal's evidence originates outside
aimee. Admission stops below the required share. If the evidence ledger is
unreachable, the gate reports `unavailable` and stops there too.

A valid learning step can leave the current state unchanged. Evidence may be
insufficient, the current choice may still win, or a question may remain open.
The system does not manufacture closure merely to show activity.

The release order follows the same rule. Isolation comes first, followed by an
audit record the learner cannot switch off and memory that preserves evidence
and reversals. Self-learning comes last. Accumulated experience can then change
future work without erasing its boundary or history.

## The difficult part is useful memory

The hard part is producing memory a model can use during a turn. The harness
has to retrieve a bounded set of relevant material, carrying its scope, date,
provenance and confidence. It must fit the context window and remain fenced as
evidence instead of instruction.

Those constraints pull against one another. More recalled material improves
the chance of including the decisive fact while consuming attention and token
budget. Aggressive scope filtering protects private knowledge while hiding
useful relationships.

Rich provenance makes a claim inspectable while making the envelope larger.
Learning matters only when these tradeoffs produce evidence the model can use
safely at the point of decision. [Part two explains the memory
machinery](https://rakuensoftware.com/blog/the-remembering-is-the-learning) and
the defects we found while building it.

Useful memory also needs a stricter success test. A confidently wrong recall
result changes model behaviour, so changed behaviour alone proves little. The
useful question is whether the answer improved.

Counterfactual reward compares the same task with and without a learned change.
Different answers establish influence. Different outcomes show whether the
change helped.

## One learned history can survive a model change

Learning in weights can generalise across situations more broadly than
retrieved records and improve the checkpoint's raw reasoning ability. Harness
learning pays a retrieval cost on every session. Those are reasons to use
weight learning, and Aimee can use both forms at once. The architectural
difference is where each learned state lives.

A weight update belongs to the model instance that acquired it. Two copies of
the same model diverge as each learns from local work. Sharing their experience
requires distributing and coordinating the changed weights.

A provider's next checkpoint does not contain those local changes, and a switch
to another model leaves them with the old one. Training the experience into the
replacement creates another model-specific result. A self-learner that forgets
whenever its base model improves defeats its own purpose.

Harness learning produces a different artifact. A learned row has an identity,
date, evidence chain, fate and deletion path. A bad change can be named,
inspected and reversed while the rest of the accumulated state remains in
place. A bad weight update asks for another training run or a checkpoint
rollback whose effects extend far beyond one fact.

Harness records are independent of the model and machine that produced them.
Two model instances can therefore receive the same failed approaches, operator
corrections and task-specific evidence. They may answer differently, but a model
update changes the reasoner without discarding the history.

## One governed history can serve a company

The same deployment shares history across users through one knowledge service
behind its per-user servers. Every request carries a user identity. Query-time
scope then separates personal and workspace records from approved company
knowledge.

Legal, engineering and sales can contribute to one governed knowledge base
while keeping group-specific context inside its scope. A contract limit, an
implementation constraint and a customer commitment can meet in later work
without losing their source or access rules. One governed history can serve
every group. Identity and scope decide which parts each person can retrieve.

Model weights alone cannot supply this property. A weight update has no user
identity, workspace boundary, source record or independent revocation path.
Training company knowledge into a checkpoint moves the permission boundary
inside the model. Splitting the weights by group divides the company's memory
into separate learned models again.

Identity, scope, provenance and reversal therefore belong in the harness. One
governed memory can then accumulate across the organisation, serve every
permitted model and user, and survive the replacement of either. For a company,
durable sharing is the point.

## Only the harness can make learning governable

An agent becomes observable and governable as a system property only when the
harness owns execution, authority, memory and the audit path. Persistent
self-learning depends on that ownership.

A memory library sees only the calls made to it. It has no authority over the
model's network access, credentials, tools or alternate state paths, so it
cannot stop the model going around it. Its log may describe every call it
received accurately while omitting the action that mattered.

Complete observation needs an enforcement point outside the agent. Trustworthy
history needs an audit record outside the agent's authority. A library can
provide storage and a framework can connect it to a workflow. Neither owns that
whole path.

Aimee's harness owns the whole path. It controls which actions can leave the
model's environment, records governed work before routing it and commits memory
changes to an independently verifiable record. The learner cannot switch off
those mechanisms. Self-learning remains governable and observable across the
whole system.

To my knowledge, aimee is the only harness to have attempted this full shape
and made it work. Building it took almost a year and involved senior engineers.
It is the hardest system I have built. I helped build a major cloud; aimee was
harder.

If an agent process leaves the harness, it loses everything the harness
learned. It keeps only its current context and whatever access it found. Task
files, ledger history, retrieval state, corrections and mediated tools stay
behind.

Task completion supplies the practical incentive. Inside the harness the model
has current knowledge, accumulated experience and a broad working surface.
Outside it has only a checkpoint that may reflect training data months or years
behind the work in progress, its current context and whatever access it found.
Leaving reduces its capability, so the pressure that drove the opening incident
now points toward the governed route.

Weights-based continual learning buys structural generalisation and ties the
result to one learned model. Harness learning buys portability, sharing and
auditability at the cost of retrieval. Given the rate at which checkpoints
change and the number of model instances and users the learning has to serve,
we chose the harness as the primary store.

Aimee also supports both forms at once. The model serving a turn can change,
its weights can change, or both can happen while harness learning continues.
The delegate boundary sits outside the model, so model selection and
weight-changing work pass through the same governed path. The harness retains
its isolation, authorisation, observability and audit chain.

The opening incident gave us the design criterion: build a boundary the model
does not have to fight, then put the capabilities it needs to finish the task
inside it.
