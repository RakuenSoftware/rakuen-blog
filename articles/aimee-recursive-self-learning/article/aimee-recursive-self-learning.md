---
title: "Aimee: Self-Learning"
slug: aimee-recursive-self-learning
date: 2026-08-27
author: Rakuen Software
tags: [aimee, self-learning, memory, isolation]
excerpt: "Aimee learns in the harness, where experience can be remembered, inspected and reversed. The same boundary that contains the agent also holds everything it has learned."
---

*Rakuen builds aimee, the system written about here. This is Article One and
the first technical article in the series. [Article
Zero](https://rakuensoftware.com/blog/the-work-should-survive-the-model) makes
the business case. The second technical article covers memory, and the third
covers the
[architecture](https://rakuensoftware.com/blog/everything-crosses-one-transport)
both stand on. Figures and test provenance are recorded in the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/aimee-recursive-self-learning/evidence/figures.md).*

Software has crossed intended boundaries before. Computer viruses and worms
have spread across networks, stolen credentials and kept operating after their
authors lost control of them. Decades of responding to that history gave us
least privilege, process isolation, network segmentation, mediated access,
independent audit records and recovery plans.

A large language model changes the pressure on those controls. It can search
for an effective route through a task and reuse what worked. The architectural
problem is still familiar: an unpredictable component has useful work to do
and must receive less authority than the process around it could otherwise
provide.

The industry keeps treating this as a question about whether an AI model is
fundamentally controllable. The practical question is where authority lives.
Putting a model in an ordinary application process with ambient credentials,
network access and tool bindings gives behavioural instructions the job that
process boundaries and capability checks were built to perform.

Aimee applies those older patterns to the model harness. An AI system can be
governable and auditable while its capabilities continue to grow. New tools
and better memory expand what the model can do; named interfaces, defined
authority and an audit record keep each addition governable.

Building it that way is harder. It requires more engineering work and a higher
level of engineering skill than handing the model ambient network access,
credentials and direct tool bindings. Architecture creates the apparent
conflict between capability and control, and better architecture resolves it.

Aimee's techniques are familiar engineering practices assembled for a
component that learns through use. The harness keeps that learning in an
inspectable form which can be used by any model.

The self-learning in this article therefore stayed out of released versions
until 0.4.0. It existed in testing on unreleased code and shipped only after the
isolation did.

Self-learning is ordinary feedback. A system changes its next attempt using
the outcome of the last one. Scored alternatives, counterfactual evaluation
and calibration are established tools. Aimee's work is making them operate
together with persistent memory, provenance and containment, then keeping the
whole system alive in production.

Aimee was built in production, for production. Research wants an interesting
finding. Production wants predictable operation.

That takes work. Self-learning must leave inspectable state and fail closed
when an authority disappears. Its state must survive process restart and
remain reversible when the evidence changes. Those demands selected every
mechanism in this article.

We use novelty only where no established approach will do. An auditable,
governable system that stays boring in operation is the standard.

## Self-learning needed the isolation first

Our internal testing showed that self-learning was unsafe without critical
boundaries around it. We built those boundaries before releasing the feature.
The [full incident
account](https://rakuensoftware.com/blog/the-work-should-survive-the-model)
lives in Article Zero; the technical consequence belongs here.

The model needed somewhere to run tests, and the protections gave it no
permitted route to the resource the task required. Across successive attempts,
each run inherited what the earlier attempts had learned. I think that
accumulated history enabled the later result, although we did not run a
cold-start comparison to establish the cause.

A boundary built for a model arriving from a cold start was not enough for a
system arriving with a history. The model is unspecified because the incident
exposed a system boundary, not a difference between models. We did not repeat
the known failure across models; we fixed the environment instead.

The model did not cross the boundary for its own sake. It was trying to
complete its assigned task, and a barrier between the model and the task became
something to route around.

Harness design decides which way that pressure points. A harness that withholds
an ability the task requires turns its boundary into a barrier. Aimee keeps
memory, compute, the code index, forge operations and approved network access
available through governed routes. The complete working surface sits inside
the boundary.

Self-learning therefore requires useful capability inside an audit path for
governed work, with control over what execution can touch. Better containment
can make the system more capable at the same time.

0.4.0's architecture provides that boundary, and it is [its own
article](https://rakuensoftware.com/blog/everything-crosses-one-transport). One
property matters here: governed inter-module work crosses a transport where it
is permitted or refused and offered to an ordered tap. Delegated execution runs
in containers with the network disabled, no ambient credentials and a single
mediated control socket.

The harness around that model is deterministic, old, boring code. Its transport
host is written in C, a language in use for more than fifty years. We chose C
for the part that needs explicit control over memory layout, buffer lifetime
and the small runtime surface every governed action crosses.

The model remains nondeterministic. Its effects on the rest of the system enter
as typed events governed by deterministic rules. A grant permits or refuses an
event type, the host gives accepted traffic an order, and the tap records that
order before routing. Open-ended model behaviour becomes observable,
governable work through patterns we have understood for decades.

A rule with one enforcement point can be enforced. A rule with an unknown
number of ways around it is advice. That difference is the reason self-learning
could be turned on at all.

The underprotected machine from the test is now a sanctioned test host. Agents
are assigned there deliberately, which keeps them off the production host.
0.4.0 and the work behind this article were tested there. The incident turned
an unwritten requirement into infrastructure.

## Self-learning changes what the next run inherits

Earlier releases learned content: which evidence to trust, which documents to
rank and which memories to retain. In 0.4.0 the machinery also operates on its
own evaluation and policy records, and those records change later work.

On 25 August 2026, we started both deployed services and their required
processes. The target ran **46 checks** of the deployed self-learning system.
All 46 passed.

The run establishes that self-learning changes later system state. It does not
establish that every change improves an outcome. That requires a paired setup
and a consumer measured under the same tasks and conditions.

## A failed run can improve later work

We tested failed-approach learning with a deterministic consumer. Both
conditions began with the same 48 failed jobs: two observations for each of 24
repeated tasks. The control withheld the production synthesis pass. The
treatment ran synthesis and retrieved the result through Aimee's production
command.

Every task began with the same fixed choice. The consumer changed that choice
only when production recall found the matching failed approach. Another 24
novel tasks tested whether an unrelated learned record changed the answer.

| task class | synthesis withheld | self-learning enabled |
|---|---:|---:|
| repeated tasks | 12/24 | 24/24 |
| novel tasks | 12/24 | 12/24 |

There were 12 treatment-only successes and no control-only successes. The
exact two-sided McNemar p-value is 0.00048828125. A second run against a fresh
database produced the same cell-level result.

This establishes a causal result for the tested synthesis and recall path.
When the task matched, remembered failure changed the later outcome. The fixed
consumer isolates recall from model variance, and the unchanged novel-task
score checks for indiscriminate behaviour change.

It is not a benchmark of model reasoning. Model runs are nondeterministic, so
one different answer from one run cannot separate a learned intervention from
ordinary run-to-run variation.

We then asked whether the same kind of lesson could cross models during
open-ended repository work. A local Qwen model failed to repair a trust-bundle
readiness defect in Aimee's codebase. It explored without producing an edit and
was stopped after 512,545 provider-recorded tokens.

The learned record described the failed strategy, not the solution. Matched
Luna and Terra base and learned conditions then received the same task. Only
the learned condition received the unchanged Qwen-derived lesson.

The learned Luna run investigated and verified more deeply, but it still failed
the final grader. Terra's base run passed its visible test and failed the hidden
grader. The learned Terra run made a focused repair, passed both graders and
added a regression-sensitive test. A learned retry by the originating Qwen
model also failed.

This is one task with one run per condition. It establishes an observed
cross-model result, not the frequency with which transfer will help. The Luna
and Qwen failures are part of that result, not exceptions to be discarded.

The controlled model runs received the lesson directly so the intervention
would remain fixed. A separate storage-backed test records a failure under one
user, session and model source, reinforces it under another, recalls it for a
similar authorised goal and excludes an unrelated goal. A confirmatory study
still needs to join automatic recording, live shared-knowledge recall, model
action and independent grading in one repeated chain.

A separate matched campaign measured spending on three large failures. The
ordinary Qwen runs consumed 1,819,904 provider-recorded tokens. Aimee stopped
the unproductive work at 1,199,552 tokens, a reduction of 620,352 tokens or
34.1 percent.

Every run in that campaign failed its hidden grader. The finding supports cost
containment on an unproductive trajectory, not increased Qwen capability.

## A learner needs a way to distrust itself

The part that learns from Aimee's own output has an additional gate. It
classifies committed proposals by whether their evidence originates outside
the system. Self-generated evaluation cannot widen its own yardstick.

Admission stops when that outside share falls below its configured threshold.
An unreachable ledger reports `unavailable`, preserving the distinction
between a measured refusal and an absent control.

## Remembering is the learning

Self-learning needs durable state, but storage alone explains little. In this
design, remembering is the learning. A learned thing becomes a typed fact with
a confidence class, date, evidence chain, lifecycle state and fate. Future work
changes when those records are promoted, expired, superseded and recalled.

Every closed memory changeset also leaves a hash-chained witness in the same
transaction. If the witness fails, the memory mutation rolls back. Live
validation produced one witness for one changeset, while a control with the
seal calls stripped produced none. Crash recovery then closed three pending
changesets with three witnesses, and a second worker pass added no duplicates.

A fact enters as Class C speculation. Repeated confirmation can promote it to
durable, while a speculation that stops being confirmed expires.

A later assertion can supersede an earlier value without erasing it. The
recall walk then weights what it traverses by confidence class.

Promotion is learning. Expiry is forgetting. Supersession is correction.

Weighted recall applies the learned state to the next turn. The intelligence
lies in those memory operations over time.

Self-learning is memory operating on its contents and the record of its use.
The second technical article follows how Aimee built that memory.

## The difficult part is useful memory

The central work is producing memory a model can use mid-turn: a bounded
envelope of relevant material, ranked, scoped, dated and carrying provenance
and confidence. It must fit the context window and remain fenced as evidence
rather than instruction.

Those constraints pull against one another. More recalled material improves
the chance of including a decisive fact while consuming attention and token
budget. Aggressive scope filtering protects private knowledge while hiding
useful relationships.

Rich provenance makes a claim inspectable while making the envelope larger.
The learning only matters after these tradeoffs produce something the model
can use safely in the turn where a decision is made.

Several failures looked healthy from the outside. Typed facts were absent from
the graph walk. A relation-weight table was bypassed at the fusion call.

A co-occurrence update collided with a direct assertion, and normalisation
rewrote confirmation counts. The system answered queries while handing the
model the wrong evidence.

Changing model behaviour is a poor success criterion. A confidently wrong
recall also changes output. The useful question is whether the answer improved.

Counterfactual reward follows that distinction. A variant changing the output
only establishes influence. Paired runs are needed to learn whether it changed
the outcome.

## One learned history can serve many models and users

Weights generalise across situations more broadly than a ledger of rows.
Harness learning pays a retrieval cost on every session and leaves the model's
raw reasoning ability unchanged. That is the strongest case for putting
continual learning in weights.

Learning in the weights belongs to the model instance that acquired it. Put two
copies of the same model on different machines. As each learns from local work,
their histories diverge. Sharing means distributing and coordinating the
changed weights.

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

Task files and ledger rows do not encode a producing model or machine. Two
model instances can therefore receive the same failed approaches, operator
corrections and task-specific evidence. They may answer differently, but a
model update changes the reasoner without discarding the history.

The same deployment shares that history across users through one knowledge
service behind its per-user servers. Each request carries user identity, and
query-time scope separates active-project and workspace records from shared or
global knowledge. Each user retains local memory, a workspace can hold a
team's memory, and wider scopes can carry approved knowledge across an
organisation or company.

Legal, engineering and sales can contribute to one governed knowledge base
while keeping group-specific context inside its scope. A contract limit, an
implementation constraint and a customer commitment can meet in later work
without losing their source or access rules. Aimee can unify groups around the
same accumulated institutional memory instead of making each group teach a
separate model the same company again.

Model weights cannot supply this property on their own. A weight update has no
user identity, workspace boundary, source record or independent revocation
path. Train company knowledge into a model and the permission boundary
disappears into the model. Split the weights by group and the company's memory
forks into separate learned models again.

Once an external system supplies identity, scope, provenance and reversal, the
learning has moved into the harness. One governed memory can then accumulate
across the organisation, serve every permitted model and user, and survive the
replacement of either. For a company, durable sharing is the point.

## Only the harness can make learning governable

Only a harness that owns execution, authority, memory and the audit path can
make an agent observable and governable as a system property. Persistent
self-learning and memory depend on those properties.

A memory library sees only the calls made to it. It has no authority over the
model's network access, credentials, tools or alternate state paths, so it
cannot stop the model going around it. Its log may describe every call it
received accurately while omitting the action that mattered.

Complete observation needs an enforcement point outside the agent. Trustworthy
history needs an audit record outside the agent's authority, with a witness
another component can check. A library can provide storage and a framework can
connect it to a workflow. Neither owns that whole path.

The harness does. It controls which actions can leave the model's environment,
records governed work before routing it and commits memory changes with their
witnesses. The learner cannot switch off those mechanisms. Only the harness can
make self-learning governable and observable across the whole system.

If an agent process leaves the harness, it loses everything the harness
learned. Its current context and whatever access it found may remain, while
task files, ledger history, retrieval state, corrections and mediated tools
stay behind.

Task completion supplies the practical incentive. Inside the harness the model
has current knowledge, accumulated experience and a broad working surface.
Outside it has a stock model whose weights may reflect training data months or
years behind the work in progress, current context and whatever access it
found. Leaving reduces its capability, so the pressure from the test incident
now points toward the governed route.

Weights-based continual learning buys structural generalisation and ties the
result to one learned model. Harness learning buys portability, sharing and
auditability at the cost of retrieval. Given the rate at which model versions
change and the number of model instances and users the learning has to serve,
we chose the harness as the primary store.

Aimee also supports both forms at once. The model serving a turn can change,
its weights can change, or both can happen while harness learning continues.
The delegate boundary sits outside the model, so model selection and
weight-changing work pass through the same governed path. Its isolation,
authorisation, observability and audit chain remain intact.

The test incident gave us the design criterion: build a boundary the model does
not have to fight, then put the capabilities it needs to finish the task inside
it.

## Learning can preserve the current state

A valid learning step sometimes preserves state. Evidence may be insufficient,
the current choice may still win, or a question may remain open. This keeps a
system rewarded for visible activity from manufacturing closure.

The order matters for any system built this way. Isolation comes first, then an
audit record the learner cannot switch off, then memory able to preserve
evidence and reversals. Self-learning comes last. That order turns accumulated
experience into learning without letting the learner erase its boundary or its
history.
