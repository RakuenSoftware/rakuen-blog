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

The route accumulated across many runs while we tested the self-learning loops.
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

The six loops in this article therefore stayed off until 0.4.0. Their producing
halves existed while we tested them, with the consumers disabled. The incident
happened on that unreleased code. The loops shipped only after the isolation
did.

The title keeps the term from our proposal, but recursive self-learning is just
self-learning. A system that changes its next attempt based on the outcome of
the last one is using the ordinary feedback loop the field has known for
decades. I kept `recursive` in the title because it ranks.

Scored alternatives, counterfactual evaluation and calibration are old tools.
Aimee's work is making them operate together with persistent memory, provenance
and containment, then keeping the whole system alive in production.

Aimee was built in production, for production. Research wants an interesting
finding. Production wants the pager to stay silent.

Silence takes work. A loop must leave inspectable state and fail closed when an
authority disappears. Its learning must survive process restart and remain
reversible when the evidence changes. Those demands selected every mechanism
in this article.

Novelty is exactly what gets me woken up at two in the morning. We use it only
where no established approach will do. An auditable, governable system that
stays boring in operation is the standard.

## Self-learning needed the isolation before it needed the loops

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
number of ways around it is advice. That difference is the whole reason the
loops could be turned on at all.

The model took that node because it had to run tests somewhere and nothing had
given it a permitted place. The node it grabbed is now the node it gets: an
unused box repurposed into the test host agents are handed deliberately, which
keeps them off the production one.

0.4.0 was tested on it. So was this article. The thing the model went around a
protection to get is now infrastructure, because it turned out to be a
requirement nobody had written down.

## Closing the loops changes what the next run inherits

Earlier releases learned content: which evidence to trust, which documents to
rank and which memories to retain. In 0.4.0 the machinery also operates on its
own evaluation and policy records.

All six loops now close. Each was previously a producing half with nothing on
the other end:

- The eval suite grows from live failure. A failed job becomes a quarantined
  candidate, and an admitted candidate becomes a permanent task file in the
  suite every gate measures against. The yardstick is no longer frozen.
- Reward is counterfactual. An ablation grid measures what a capability
  actually earned. Word overlap with an outcome earns nothing.
- Approach-level dead ends are recorded and recalled at plan time for a goal
  like the one that failed.
- The curiosity backlog is drained by a real evidence probe, so a recorded
  gap is closed by evidence or stays open.
- A later commit supersedes an earlier one without a separate request, and an
  operator verdict reaches the ledger and counts against the detector that
  raised the original.
- Policy variants declared by the build can be selected and measured, so an
  advisory block has to earn its place.

The last two let the evaluator revise itself. Gates are fitted from what
happened after previous commits. Instructions are selected and scored alongside
the other choices the system measures.

The difference between a producer and a loop is consequence. Writing a failure
signature changes nothing by itself. Admitting that signature as a permanent
task changes the suite that evaluates every later candidate. A dead end becomes
learning when planning recalls it before repeating the approach.

A verdict becomes learning when it changes the fate of the earlier proposal and
the future confidence placed in its detector.

On 25 August 2026, we started both deployed services and their required
processes, then followed each producer into the state consumed by a later run.
The target finished at **46 passed, 0 failed**.

Two failed jobs became one candidate, which admission wrote into the permanent
suite. Three paired tasks attributed a better outcome to the full capability
set. A failed approach returned through the next planning call with its failure
mode. One curiosity item resolved while another stayed open for lack of
evidence.

A later commit superseded an earlier proposal, and an operator verdict changed
its fate to `contradicted`. The policy route selected and recorded the seeded
non-default choice, `brief`.

The same run found a use-after-free in policy selection. The optimiser selected
`brief`, freed the response containing that identifier and then compared it.
The service returned `off`.

Copying the identifier before destroying the response fixed the live path. A
focused test now requires the real sidecar to return the seeded non-default
choice.

The run establishes closure across all six. Measuring outcome improvement
requires paired setup and consumer phases under the same tasks and seeds. We
have not run that study across all six loops.

## A learner needs a way to distrust itself

The isolation removed several old restrictions. One new gate appeared. It
controls the loop that feeds on aimee's own output.

Every committed proposal is classified by where its evidence roots. A human
correction, a test exit code, a verify gate, an observed git outcome or an
official grader is exogenous. The implicit detectors reading aimee's own
transcript are endogenous whatever the signal claims, and unknown provenance
counts as endogenous.

Against a real ledger it reads `open (75% of 4 committed proposals exogenous)`,
matching a direct ledger read and the service's answer. Against a ledger of 25
implicit-detector commits and nothing else it reads `closed (0% of 25 committed
proposals exogenous)`. Self-generated evaluation cannot widen its own
yardstick.

Closed, a fully reproduced candidate admits `0` and no task file is
written. Reopened, the same candidate admits `1`. When it cannot reach its
ledger it reports `unavailable`, never `open`, because an operator has to be
able to tell a measured control from an absent one.

## Remembering is the learning

The loops need durable state, but storage alone explains little. In this
design, remembering is the learning. A learned thing becomes a typed fact with
a confidence class, date, evidence chain, lifecycle state and fate. Future work
changes when those records are promoted, expired, superseded and recalled.

Every closed memory changeset also leaves a hash-chained witness in the same
transaction. If the witness fails, the memory mutation rolls back. Live
validation produced one witness for one changeset, while a control with the seal
calls stripped produced none. Crash recovery then closed three pending
changesets with three witnesses, and a second worker pass added no duplicates.

A fact enters as Class C speculation. Repeated confirmation can promote it to
durable, while a speculation that stops being confirmed expires.

A later assertion can supersede an earlier value without erasing it.
The recall walk then weights what it traverses by confidence class.

Promotion is learning. Expiry is forgetting. Supersession is correction.

Weighted recall applies the learned state to the next turn. The intelligence of
the loop lies in those memory operations over time.

The six loops are memory operating on its contents and the record of its use.
The eval suite grows when memory notices that a failure signature recurred.

Approach-level negative knowledge is memory of what was already tried.
Post-commit regret is memory revising its opinion of an earlier memory. The
endogeneity ratio is memory asking where its own contents came from.

Those memory operations are the learning. The second article follows how aimee
built them.

## The difficult part is useful memory

The six loops came out of one proposal because each is easy to sketch. Admit a
failed job to the suite, compare a run with one capability removed, or recall a
failed approach at the next plan.

The harder work is producing memory a model can use mid-turn: a bounded envelope
of relevant material, ranked, scoped, dated and carrying provenance and
confidence. It must fit the context window and remain fenced as evidence
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
and made it work.

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
we chose the harness.

The opening incident gave us the design criterion: build a boundary the model
does not have to fight, then put the capabilities it needs to finish the task
inside it.

## A valid loop can decide to do nothing

A valid loop sometimes preserves state. In the current target, an uncovered
curiosity item stayed open while a covered item became resolved. Leaving the
first open protects the memory from invented evidence.

A system rewarded for visible activity will manufacture closure. It will turn
an unanswered question into a weak answer, promote a fact because a promotion
looks like progress or change policy because the loop is expected to choose
something. A useful learner has a stable no-op: evidence was insufficient, the
current choice still wins, or the question remains open.

The policy loop supplied the opposite case: a seeded posterior had to select
`brief` instead of preserving the default.

The order matters for any system built this way. Isolation comes first, then an
audit record the learner cannot switch off, then memory able to preserve
evidence and reversals. The loops come last. That order turns accumulated
experience into learning without letting the learner erase its boundary or its
history.
