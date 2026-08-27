---
title: "Aimee: Self-Learning"
slug: aimee-recursive-self-learning
date: 2026-08-27
author: Rakuen Software
tags: [aimee, self-learning, memory, isolation]
excerpt: "Aimee learns in the harness, where experience can be remembered, inspected and reversed. The same boundary that contains the agent also holds everything it has learned."
---

*Rakuen Software builds aimee, the system written about here. [Article
Zero](https://rakuensoftware.com/blog/the-work-should-survive-the-model) gives
the non-technical introduction and business case. This is Article One and the
first technical article. A later article will cover memory, followed by an
article about the architecture beneath both. Sources and reporting decisions are
recorded in the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/aimee-recursive-self-learning/evidence/figures.md).*

Aimee is an open-source knowledge platform for company AI work, available as a
managed cloud service or self-hosted. It brings documents, code, facts,
decisions and work history into one governed knowledge base. It scales from one
user to an entire company, with identity and scope deciding what each person and
AI model can retrieve.

Self-learning lets useful results and failed approaches change later work. That
changes the problem a safety boundary has to solve. A model can arrive at a task
with a history of what earlier work discovered, including routes that failed.
Aimee keeps that history in the harness, where it remains inspectable,
reversible and independent of any one model or set of weights.

Our internal testing showed that self-learning was unsafe without critical
boundaries around it. We built those boundaries before release. Article Zero
carries the complete incident account; this article follows the engineering
consequence.

The boundary now includes a governed test host. Agents are assigned there
deliberately, keeping them off the production host. A resource the testing
system once reached outside a permitted route became infrastructure inside the
governed design.

## The controls are old, and self-learning changes the pressure

Software has crossed intended boundaries before. Computer viruses and worms
have spread across networks, stolen credentials and kept operating after their
authors lost control of them. Decades of responding to that history gave us
least privilege, process isolation, network segmentation, mediated access,
independent audit records and recovery plans.

A large language model puts new pressure on those controls. The model can
search for an effective route through a task, and the harness can preserve what
worked and what failed across runs. The engineering problem remains familiar:
an unpredictable component has useful work to do and must receive less
authority than its surrounding process could otherwise provide.

Industry discussion often frames control as a property of the model. In an
operational system, control depends on where authority lives. A model in an
ordinary application process inherits ambient credentials, network access and
tool bindings. Behavioural instructions then have to do the job of process
boundaries and capability checks.

Aimee puts those older controls in the model harness. New tools and better
memory expand what the model can do. Named interfaces, explicit authority and
an independent audit record govern each addition.

An AI system can remain governable and auditable while its capabilities grow.
Building it that way requires more engineering work and a higher level of
engineering skill than handing the model ambient network access, credentials
and direct tool bindings. The controls have to apply to every path. A governed
architecture resolves the conflict between capability and control by placing
useful capability inside the boundary.

The learning method is ordinary feedback: the system changes its next attempt
using the outcome of the last one. Scored alternatives, counterfactual
evaluation and calibration are established tools. Aimee's work is making them
operate together with persistent memory, provenance and containment, then
keeping the whole system alive in production.

Aimee's techniques are familiar engineering practices assembled for a
component that learns through use. The harness keeps that learning in an
inspectable form which can be used by any model.

Production needs predictable operation. Self-learning must keep its state
inspectable and reversible, survive a process restart and fail closed when
authority disappears. Those requirements selected the mechanisms in this
article.

We use novelty only when established approaches cannot do the job. The
resulting system must stay governable and boring in operation.

## The route to success belongs inside the boundary

Task completion supplies the pressure. The model has no independent desire to
escape. It is trying to complete the task it was given, and a barrier between
the model and the required result becomes another problem to solve.

Harness design decides which way that pressure points. A harness that withholds
an ability the task requires turns its boundary into a barrier. Aimee keeps
memory, compute, the code index, forge operations and approved network access
available through governed routes. The complete working surface and its audit
path sit inside the boundary.

Self-learning therefore requires useful capability inside an audit path for
governed work, with control over what execution can touch. Better containment
can make the system more capable at the same time.

0.4.0 supplies the enforcement point through its transport architecture, which
a later article will cover.
Governed work crosses one transport, where the harness checks and records it
before routing. Delegated execution runs in containers with the network
disabled, no ambient credentials and one mediated control socket.

The harness around the model is deterministic, old, boring code. Its transport
host is written in C, a language in use for more than fifty years. We chose C
for the part that needs explicit control over memory layout, buffer lifetime
and the small runtime surface every governed action crosses.

The model remains nondeterministic. Its effects enter the rest of the system as
typed events governed by deterministic rules. Each grant names the event types
a component may use. The host rejects the rest, orders accepted traffic and
records that order before routing, making open-ended model behaviour observable
and governable.

A rule with one enforcement point can be enforced. A rule with an unknown
number of ways around it is advice. That difference is the reason self-learning
could be turned on at all.

## Self-learning changes what the next run inherits

Earlier releases used outcomes to change which evidence to trust, which
documents to rank and which memories to retain. In 0.4.0 the harness can also
learn from its own evaluation and policy records. Those changes affect later
work.

That claim has two different tests. A deployed two-service target passed all
46 checks of the self-learning system. In a paired study with the starting
choices held fixed, 12 of 24 repeated tasks succeeded without the learned
failure record and 24 of 24 succeeded with it. On 24 new tasks with no matching
history, both conditions remained at 12 of 24.

That is direct evidence of self-learning in the harness: the stored result of
earlier work changed later outcomes. The fixed consumer makes the attribution
narrower, not weaker. It isolates recalled failure from model variance. It does
not establish open-ended model performance.

This article's [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/aimee-recursive-self-learning/evidence/figures.md)
carries the full study design, replication and limitations. Part Two will
explain the memory mechanism that made the result possible.

Learning from those records creates a circularity: Aimee could judge a new
proposal against a standard it had already changed. An additional gate
therefore measures how much of the proposal's evidence originates outside
Aimee. Admission stops below the configured minimum share of outside evidence.
If the evidence ledger is unreachable, the gate reports `unavailable` and stops
there too.

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
safely at the point of decision. Part Two will explain the memory machinery and
the defects we found while building it.

Useful memory also needs a stricter success test. A confidently wrong recall
changes model behaviour, so changed behaviour alone proves little. The useful
question is whether the answer improved.

Counterfactual reward compares the same task with and without a learned change.
Different answers establish influence. Different outcomes show whether the
change helped.

## One learned history can survive a model change

Learning in weights can generalise across situations more broadly than
retrieved records and improve the model's raw reasoning ability. Harness
learning pays a retrieval cost on every session. Those are reasons to use
weight learning, and Aimee can use both forms at once. The architectural
difference is where each learned state lives.

A weight update belongs to the model instance that acquired it. Two copies of
the same model diverge as each learns from local work. Sharing their experience
requires distributing and coordinating the changed weights.

A provider's next model version does not contain those local changes, and a
switch to another model leaves them with the previous one. Training the
experience into the replacement creates another model-specific result. A
self-learning system that forgets whenever its base model improves defeats its
own purpose.

Harness learning produces a different artifact. A learned row has an identity,
date, evidence chain, fate and deletion path. A bad change can be named,
inspected and reversed while the rest of the accumulated state remains in
place. A bad weight update asks for another training run or a model rollback
whose effects extend far beyond one fact.

Harness records are independent of the model and machine that produced them.
Two model instances can therefore receive the same failed approaches, operator
corrections and task-specific evidence. They may answer differently, but a
model update changes the reasoner without discarding the history.

## One governed history can serve a company

The same deployment shares history across users through one knowledge service
behind its per-user servers. Every request carries a user identity. Query-time
scope separates personal and workspace records from approved company knowledge.
Each user retains local memory, a workspace can hold a team's memory and wider
scopes can carry approved knowledge across the company.

Legal, engineering and sales can contribute to one governed knowledge base
while keeping group-specific context inside its scope. A contract limit, an
implementation constraint and a customer commitment can meet in later work
without losing their source or access rules. One governed history can serve
every group. Identity and scope decide which parts each person can retrieve.

Model weights alone cannot supply this property. A weight update has no user
identity, workspace boundary, source record or independent revocation path.
Training company knowledge into a model moves the permission boundary inside
the model. Splitting the weights by group divides the company's memory into
separate learned models again.

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
history needs an audit record outside the agent's authority, with a witness
another component can check. A library can provide storage and a framework can
connect it to a workflow. Neither owns that whole path.

Aimee's harness owns the whole path. It controls which actions can leave the
model's environment, records governed work before routing it and commits memory
changes with their witnesses. The learner cannot switch off those mechanisms.
Self-learning remains governable and observable across the whole system.

Building Aimee took almost a year and involved many very senior engineers. It
is the hardest system we have built.

If an agent process leaves the harness, it loses everything the harness
learned. It keeps only its current context and whatever access it found. Task
files, ledger history, retrieval state, corrections and mediated tools stay
behind.

Task completion supplies the practical incentive. Inside the harness the model
has current knowledge, accumulated experience and a broad working surface.
Outside it has only a model that may reflect training data months or years
behind the work in progress, its current context and whatever access it found.
Leaving reduces its capability, so task completion points toward the governed
route.

Weights-based continual learning buys structural generalisation and ties the
result to one learned model. Harness learning buys portability, sharing and
auditability at the cost of retrieval. Given the rate at which model versions
change and the number of model instances and users the learning has to serve,
we chose the harness as the primary store.

Aimee also supports both forms at once. The model serving a turn can change,
its weights can change, or both can happen while harness learning continues.
The delegate boundary sits outside the model, so model selection and
weight-changing work pass through the same governed path. The harness retains
its isolation, authorisation, observability and audit chain.

The testing incident gave us the design criterion: build a boundary the model
does not have to fight, then put the capabilities it needs to finish the task
inside it.
