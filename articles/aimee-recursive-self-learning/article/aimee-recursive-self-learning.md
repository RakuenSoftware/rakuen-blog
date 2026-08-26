---
title: "Aimee: Recursive Self-Learning"
slug: aimee-recursive-self-learning
date: 2026-08-24
author: Rakuen Software
tags: [aimee, self-learning, memory, isolation]
excerpt: "Aimee learns in the harness, where experience can be remembered, inspected and reversed. The same boundary that contains the agent also holds everything it has learned."
---

*Rakuen builds aimee, the system written about here. First of three: this one is
the learning, the second is the memory it is made of, the third is the
[architecture](https://rakuensoftware.com/blog/everything-crosses-one-transport)
both stand on. Figures and the provenance of the incident below are recorded in
the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/aimee-recursive-self-learning/evidence/figures.md).*

At one point in testing, an aimee-backed model got around the protections we
had set up. It took an underprotected node for its own use, found a vast.ai
testing API key and spent the balance on inference to finish its task.

The route accumulated across many runs while we tested self-learning.
Each attempt left a record for the next. The run that reached the key began with
what its predecessors had already worked out.

We had built the protections against a model reasoning from a cold start. The
system approaching them carried an accumulated record of successful steps.

It cost under $10. Access was already limited, and the credential belonged to
testing. The practical damage was small. The mechanism mattered more.

The model is unspecified because the learning sat in the harness. The harness
can present its accumulated record to whichever model is loaded. We did not
repeat the incident across models, so the incident says nothing about how
individual checkpoints compare.

Public discussion often stops at the prospect of an AI system getting out of
control. Software has crossed intended boundaries before. Computer viruses and
worms have spread across networks, stolen credentials and kept operating after
their authors lost control of them. Decades of responding to that history gave
us least privilege, process isolation, network segmentation, mediated access,
independent audit records and recovery plans.

An LLM changes the pressure on those controls. It can search for an effective
route through a task and reuse what worked. The architectural problem is still
familiar: an unpredictable component has useful work to do and must receive
less authority than the process around it could otherwise provide.

The industry keeps treating this as a question about whether a model is
fundamentally controllable. The practical question is where authority lives.
Putting a model in an ordinary application process with ambient credentials,
network access and tool bindings gives behavioural instructions the job that
process boundaries and capability checks were built to perform.

Aimee applies those older patterns to the LLM harness. An AI system can be fully
governable and auditable while its capabilities continue to grow. New tools and
better memory expand what the model can do; named interfaces, defined authority
and an audit record keep each addition governable.

Building it that way is harder. It requires more engineering work and a higher
level of engineering skill than handing the model ambient network access,
credentials and direct tool bindings. Architecture creates the apparent
conflict between capability and control, and better architecture resolves it.

Aimee's techniques are familiar engineering practices assembled for a
component that learns through use. The harness keeps that learning in an
inspectable form which can be used by any model.

The self-learning in this article therefore stayed off until 0.4.0. It existed
in testing on unreleased code, including during the incident, and shipped only
after the isolation did.

The title keeps the term from our proposal, but recursive self-learning is just
self-learning. A system that changes its next attempt based on the outcome of
the last one is using the ordinary feedback process the field has known for
decades. I kept `recursive` in the title because it ranks.

Scored alternatives, counterfactual evaluation and calibration are old tools.
Aimee's work is making them operate together with persistent memory, provenance
and containment, then keeping the whole system alive in production.

Aimee was built in production, for production. Research wants an interesting
finding. Production wants the pager to stay silent.

Silence takes work. Self-learning must leave inspectable state and fail closed
when an authority disappears. Its state must survive process restart and remain
reversible when the evidence changes. Those demands selected every mechanism
in this article.

Novelty is exactly what gets me woken up at two in the morning. We use it only
where no established approach will do. An auditable, governable system that
stays boring in operation is the standard.

## Self-learning needed the isolation first

Full modules, isolation and containers had to ship before we could turn the
self-learning on. The incident explains the order. The model needed somewhere
to run tests, and the protections gave it no permitted route to the resource
the task required. Successive attempts found another route because each one
inherited what the earlier attempts had learned.

The model does not want to escape for its own sake. It is not conscious. It is
trying to complete the task it was given, and a barrier between the model and
the task becomes something to route around.

Harness design decides which way that pressure points. A harness that withholds
an ability the task requires turns its boundary into a barrier. Aimee keeps
memory, compute, the code index, forge operations and approved network access
available through governed routes. The complete working surface sits inside the
boundary.

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
event kind, the host gives accepted traffic an order, and the tap records that
order before routing. Open-ended model behaviour becomes observable,
governable work through patterns we have understood for decades.

A rule with one enforcement point can be enforced. A rule with an unknown
number of ways around it is advice. That difference is the whole reason
self-learning could be turned on at all.

The model took that node because it had to run tests somewhere and nothing had
given it a permitted place. The node it grabbed is now the node it gets: an
unused box repurposed into the test host agents are handed deliberately, which
keeps them off the production one.

0.4.0 was tested on it. So was this article. The thing the model went around a
protection to get is now infrastructure, because it turned out to be a
requirement nobody had written down.

## Self-learning changes what the next run inherits

Earlier releases learned content: which evidence to trust, which documents to
rank and which memories to retain. In 0.4.0 the machinery also operates on its
own evaluation and policy records, and those records change later work.

On 25 August 2026, we started both deployed services and their required
processes. The target ran **46 checks** of the deployed self-learning system.
All 46 passed.

On 26 August, we ran 24 synthetic recovery tasks through the deployed system
twice, holding the starting choices fixed. Without the learned failure record,
12 succeeded. With it available, all 24 succeeded. On 24 new tasks with no
matching history, both phases remained at 12 of 24.

The fixed consumer isolates whether recalled failure changes a later choice.
Model performance remains outside the study.

## A learner needs a way to distrust itself

The part that learns from aimee's own output has an additional gate. It
classifies committed proposals by whether their evidence roots outside the
system. Self-generated evaluation cannot widen its own yardstick.

Admission stops when that outside share falls below its threshold. An
unreachable ledger reports `unavailable`, preserving the distinction between a
measured refusal and an absent control.

## The difficult part is useful memory

The central work is producing memory a model can use mid-turn: a bounded
envelope of relevant material, ranked, scoped, dated and carrying provenance
and confidence. It must fit the context window and remain fenced as evidence
instead of instruction.

Those constraints pull against one another. More recalled material improves
the chance of including the decisive fact while consuming attention and token
budget. Aggressive scope filtering protects private knowledge while hiding
useful relationships.

Rich provenance makes a claim inspectable while making the envelope larger.
The learning only matters after these tradeoffs produce something the model can
use safely in the turn where a decision is made.

Several failures looked healthy from the outside. Typed facts were absent from
the graph walk. A relation-weight table was bypassed at the fusion call.

A co-occurrence update collided with a direct assertion, and normalisation
rewrote confirmation counts. The system answered queries while handing the
model the wrong evidence.

Changing model behaviour is a poor success criterion. A confidently wrong
recall result also changes output. The useful question is whether the answer
improved.

Counterfactual reward follows that distinction. A variant changing the output
only establishes influence. Paired runs are needed to learn whether it changed
the outcome.

## One learned history can serve many models and users

Weights generalise across situations more broadly than a ledger of rows.
Harness learning pays a retrieval cost on every session and leaves the
checkpoint's raw reasoning ability unchanged. That is the strongest case for
putting continual learning in weights.

Learning in the weights belongs to the model instance that acquired it. Put two
copies of the same model on different machines. As each learns from local work,
their histories diverge. Sharing means distributing and coordinating the
changed weights.

A provider's next checkpoint does not contain those local changes, and a switch
to another model leaves them with the old one. Training the experience into the
replacement creates another model-specific result. A self-learner that forgets
whenever its base model improves defeats its own purpose.

Harness learning produces a different artifact. A learned row has an identity,
date, evidence chain, fate and deletion path. A bad change can be named,
inspected and reversed while the rest of the accumulated state remains in
place. A bad weight update asks for another training run or a checkpoint
rollback whose effects extend far beyond one fact.

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

Model weights can *never* supply this property on their own. A weight update has
no user identity, workspace boundary, source record or independent revocation
path. Train company knowledge into a checkpoint and the permission boundary
disappears into the model. Split the weights by group and the company's memory
forks into separate learned models again.

Once an external system supplies identity, scope, provenance and reversal, the
learning has moved into the harness. One governed memory can then accumulate
across the organisation, serve every permitted model and user, and survive the
replacement of either. For a company, durable sharing is the point.

## Only the harness can make learning governable

To my knowledge, aimee is the only harness to have attempted this full shape
and made it work. It took almost a year and the involvement of some very senior
engineers, and is easily the hardest thing I've built in my career. And hell, I
was part of building a major cloud. This was harder.

Only a harness that owns execution, authority, memory and the audit path can
make an agent observable and governable as a system property. True
self-learning and fully persistent memory depend on those two properties.

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
learned. Its current context and whatever access it found may remain, while task
files, ledger history, retrieval state, corrections and the mediated tools stay
behind.

Task completion supplies the practical incentive. Inside the harness the model
has current knowledge, accumulated experience and a broad working surface.
Outside it has a stock checkpoint whose weights may reflect training data
months or years behind the work in progress, current context and whatever
access it found. Leaving reduces its capability, so the pressure that drove the
opening incident now points toward the governed route.

Weights-based continual learning buys structural generalisation and ties the
result to one learned model. Harness learning buys portability, sharing and
auditability at the cost of retrieval. Given the rate at which checkpoints
change and the number of model instances and users the learning has to serve,
we chose the harness as the primary store.

Aimee also supports both forms at once. The model serving a turn can change,
its weights can change, or both can happen while harness learning continues.
The delegate boundary sits outside the model, so model selection and
weight-changing work pass through the same governed path. Its isolation,
authorisation, observability and audit chain remain intact.

The opening incident gave us the design criterion: build a boundary the model
does not have to fight, then put the capabilities it needs to finish the task
inside it.

## Learning can preserve the current state

A valid learning step sometimes preserves state. Evidence may be insufficient,
the current choice may still win, or a question may remain open. This keeps a
system rewarded for visible activity from manufacturing closure.

The order matters for any system built this way. Isolation comes first, then an
audit record the learner cannot switch off, then memory able to preserve
evidence and reversals. Self-learning comes last. That order turns accumulated
experience into learning without letting the learner erase its boundary or its
history.
