---
title: "From Failed Run to Shared Capability: Production-Grade Organisational Memory Across Heterogeneous Language-Model Agents"
slug: failure-as-shared-capability
date: 2026-08-27
author: Rakuen Software
tags: [language-model-agents, memory, cross-model-transfer, organisational-learning, ai-systems]
excerpt: "One model's stopped failure becomes a durable organisational record, and changes the graded work a different model tier completes."
---

# From Failed Run to Shared Capability

## Production-Grade Organisational Memory Across Heterogeneous Language-Model Agents

Working paper. The deterministic recall study is replicated. The open-ended
cross-model study is a pilot: one task, one run per arm. Read it as an
occurrence, not a rate.

*Rakuen builds aimee, the system measured here and the one that stands to gain.
Every deployment and product claim below is first-party. Section 10 is the full
disclosure.*

## Abstract

Language-model agents discard operational experience at session and model
boundaries. Prior work shows that episodic reflection, experiential memory,
shared agent memory, negative knowledge and evolved skill packages all improve
later task performance without touching model weights. The production systems
problem is less studied: how an organisation retains those lessons across users
and heterogeneous models while preserving provenance, access scope, correction
history, execution isolation, and an audit path the learner does not control.

We describe Aimee, a self-hosted organisational learning system, and evaluate
one of its six feedback loops at three levels. First, a live two-service target
observes all six loops and passes 46 of 46 checks. Second, a paired study
isolates failed-approach synthesis and recall. On 24 repeated tasks, a
deterministic consumer scores 12/24 when synthesis is withheld and 24/24 when
self-learning is enabled; on 24 novel tasks both conditions score 12/24. The 12
treatment-only successes and zero control-only successes give an exact
two-sided McNemar p-value of 0.00048828125. A second fresh-database run is
byte-identical.

Third, a progress controller stops a local Qwen agent after 512,545 tokens and
turns its failure into a sealed natural-language lesson. Matched Luna and Terra
base/learned arms receive the same large-repository task; learned arms alone
receive the unchanged Qwen lesson. Luna reaches full-build and focused-test
execution that its base arm does not, but both final repairs fail. Terra's base
arm fails a sealed hidden grader; its learned arm passes visible and hidden
graders and authors a regression-sensitive test. The same lesson fails to
rescue Qwen itself on retry, so it is no guarantee.

Separately, three matched large-repository pairs on the same local model reduce
pooled consumption from 1,819,904 to 1,199,552 tokens, a 34.1% reduction. All
six runs still fail their sealed hidden grader. The saving bounds what an
unproductive failure costs. Capability is untouched.

Together these establish causal recall efficacy under a fixed consumer, and one
observed cross-model completion crossover under open-ended work. How often
transfer pays is unmeasured, and the pilot cannot yet separate what the typed
record contributes from what any account of a prior failure would contribute.
We close with a design to be preregistered before any confirmatory run.

## 1. Introduction

An organisation pays for more than model output. It pays for investigation,
failed approaches, corrections, verification, and the context needed to reach a
decision. Most agent systems attach all of that to a transcript, an individual
agent, or one model's retry loop. The session ends, the model changes, and the
next worker buys the same discovery again.

External memory changes the unit being bought. A failed trajectory becomes a
record that changes later work without fine-tuning the model that reads it, and
the record outlives model upgrades. Someone can inspect it or withdraw it
without touching weights.

Prior research has already shown that this works.
[Reflexion](https://arxiv.org/abs/2303.11366) keeps verbal reflections in an
episodic buffer for later trials. [ExpeL](https://arxiv.org/abs/2308.10144)
extracts natural-language insight from prior tasks.
[INMS](https://arxiv.org/abs/2404.09982) shares conversational memories among
agents. [Negative Knowledge](https://arxiv.org/abs/2606.21024) turns failed
research attempts into typed shared records. Most directly,
[Recuris](https://arxiv.org/abs/2608.24876) evolves a skill-memory package from
one deployment model and reports gains when that package is loaded unchanged
into other frozen models.

The remaining problem is organisational. A production memory record needs an
owner, an access boundary, provenance, a correction path, and an accountable
consumer.

Each of those has a failure mode. A learner that can expand its own credentials
or rewrite its own audit history has escaped governance. A memory that crosses
users without scope is a data leak. A success recorded without its negative
transfers makes later evaluation unreliable.

Aimee is our systems answer to that problem. It separates per-user agent
services from a shared knowledge service, stores learned records outside model
weights, keeps their evidence and scope, and routes execution through controls
the learner does not hold. Memory mutations produce audit intents that a
separately credentialed worker commits to a hash chain.

Four things need testing:

1. **Closure.** Whether the implemented feedback loops reach the later
   consumers they are built to change.
2. **Causal efficacy.** Whether failed-approach synthesis and recall change a
   later outcome while the consumer is held fixed.
3. **Cross-model transfer.** Whether a failure produced by one model changes
   the open-ended capability or completion of another model tier.
4. **Cost.** Whether the same substrate lowers cost per successful task, or
   bounds the cost of an unproductive failure.

The evidence answers the first two directly. For the third it supplies one
observed occurrence; the rate is unmeasured. Existing cost data answers part of
the fourth and specifies the next experiment.

We contribute:

- **An architecture.** Organisational memory that separates learning from model
identity while keeping scope, provenance, correction, isolation and independent
audit.
- **A replicated paired study.** It isolates the causal effect of one
production synthesis-and-recall loop.
- **A traced cross-model transfer.** One stopped local-model failure changes
behaviour in two later model tiers, including a hidden-graded completion
crossover.
- **An economic frame.** Failure control, retained negative knowledge and
cross-user reuse measured as one organisational learning loop, with three
matched large-repository pairs cutting the cost of an unproductive failure by
  34.1% and leaving capability where it was.
- **A confirmatory protocol.** What it would take to estimate the frequency,
cost and security of cross-model, cross-user transfer.

We claim none of this first. Recuris and INMS already demonstrate cross-model
and shared agent memory, and earlier work covers experiential learning more
generally. What we add is the production systems combination, and its observed
path through a real large repository.

Our review of prior work is bounded. We searched the published literature and
the public documentation of adjacent commercial products, and found nothing
documenting this whole combination. Absence from the published record proves
nothing about private systems, and we make no claim about them.

## 2. System model

### 2.1 The organisation owns the state

Aimee has two principal services. An `aimee-server` assists one human and owns
that person's sessions, tools, credentials, delegates and workflows. An
`aimee-kb` holds a corpus for a team or organisation. Many personal services
can use one shared knowledge service while authorisation constrains what each
principal may read or change.

Models are replaceable workers behind that boundary. One model writes a record
and a different one reads it later. Source model, session and user ride along
as provenance, and the lesson itself belongs to the organisation. Retrieval
still respects the caller's authorised KB and scope.

The separation buys a stronger amortisation than personal memory does. One user
pays the discovery cost and later authorised users collect. A local model can
write a record a hosted model later reads. Replace either model and the
organisation keeps its operational history.

### 2.2 A failed approach is a typed, correctable record

For the loop evaluated here, repeated failed jobs are synthesised into a failed
approach. The record contains a goal, the approach taken, a failure mode,
source provenance and occurrence history. Similar-goal recall returns the
record during later planning. An unrelated goal should not receive it.

The no-progress record uses deliberately stable approach text, so a retry
reinforces one row and the store never fills with paraphrases. Originating
user, session and model stay attached to the observation, and the recall query
ignores all three. Authorisation is enforced at the knowledge-service boundary.

No record is assumed permanently correct. Aimee's memory model carries later
evidence, supersession and correction, and it needs to: agent memory has an
experience-following effect, where similar retrieved examples induce similar
outputs, propagate errors, and replay an experience that only looks like the
current one ([Xiong et al., 2026](https://aclanthology.org/2026.acl-long.27/)).

### 2.3 The learner does not own execution or audit

Learning changes future preparation and policy, so the controls around it must
remain outside the learner. Aimee routes delegated work through explicit
capabilities, workspace and network boundaries, and separately managed
credentials. The learned record can advise a plan; it cannot grant itself a new
authority.

Memory changes use a separate audit path. The mutation transaction writes an
immutable audit intent. A separately credentialed worker seals committed
intents into a hash chain. Fault-injection tests cover the live seal, a control
with seal calls removed, rollback after an injected crash, recovery and
idempotent restart.

Aimee also classifies the evidence behind self-produced learning. Human
corrections, test exits, external verification, observed version-control
outcomes and official graders count as exogenous. Signals read only from the
agent's own transcript count as endogenous. Let the exogenous ratio fall below
the configured gate and the system refuses automatic admission, which stops the
learner grading itself against a history it wrote.

## 3. Evaluation

### 3.1 Experiment A: loop closure

Experiment A asks whether six implemented feedback loops reach their consumers
on a live deployment. The target starts `aimee-server`, `aimee-kb`, their
required modules and PostgreSQL against disposable state. It observes:

- repeated failures becoming one eval candidate and then one admitted task;
- paired capability attribution reaching the ledger;
- a failed approach returning during planning for a similar goal;
- a curiosity item resolving when a probe supplies evidence;
- a later commit superseding an earlier proposal and an operator verdict
changing its fate;
- a non-default policy variant selected from seeded reward history.

The target passes 46 checks and fails none. It also exposes a use-after-free in
the policy-selection path: the optimiser selected `brief`, freed the response
that held the identifier, and returned `off`. Copying the identifier before
destroying the response repairs the live path, and the focused test requires
the non-default selection.

The result is closure. An outcome changes durable state, and a later consumer
reads that state. Whether each loop improves a downstream task is a separate
question, and this experiment does not touch it.

### 3.2 Experiment B: causal efficacy of failed-approach recall

Experiment B separates setup from consumption.

Both conditions receive the same 48 failed `agent_jobs`: two observations for
each of 24 repeated tasks. The control condition withholds the production
synthesis pass. The treatment runs `aimee eval candidates-update scan` and
reads the learned result through the production `aimee learning approaches`
command.

A deterministic consumer begins each task with the same fixed choice, and
changes it only when the production recall output names the matching failed
approach. A further 24 novel tasks have no matching history. They test whether
unrelated learned records make the consumer thrash.

| task class | synthesis withheld | self-learning enabled |
|---|---:|---:|
| repeated | 12/24 | 24/24 |
| novel | 12/24 | 12/24 |

All 24 treatment advisories contain the matching failed approach. Neither
condition produces an advisory for novel tasks. There are 12 treatment-only
successes and zero control-only successes. The exact two-sided McNemar p-value
is 0.00048828125.

The study is repeated against a second fresh PostgreSQL database. Both valid
runs pass 12 harness checks and produce byte-identical cell-level CSV output.
Three earlier invalid attempts remain retained and excluded: one lacks the
required database role, one stops at a defective readiness probe, and one
produces the same cell scores but fails three incorrectly escaped harness
assertions.

The design isolates the production synthesis and recall path from stochastic
model behaviour, which buys causal efficacy for matching task descriptions. It
buys nothing about open-ended reasoning. Whether a model follows the advisory,
or carries it to a goal that means the same thing in different words, is
untested here. Section 7.3 is the study that would settle it.

### 3.3 Experiment C: exploratory cross-model transfer

Experiment C puts model variance back in, and asks whether the record changes
what an agent completes.

#### Source failure

A local Qwen3.8-27B agent receives a trust-bundle readiness repair in Aimee's
large C and Python repository. A progress controller tracks successful calls,
mutations and overlapping retrievals. The run stops after 28 successful calls
without a mutation, including nine repeated or overlapping retrievals. It
records 512,545 provider tokens and produces no patch.

The sealed record contains this lesson:

> Broad repository exploration with repeated or overlapping retrievals and no
> edit failed. On a similar goal, choose a materially different plan, form a
> concrete defect hypothesis, and attempt the smallest justified edit or
> decisive test before broadening exploration.

The lesson contains no defect location or solution.

#### Matched consumer arms

For GPT-5.6 Luna and GPT-5.6 Terra separately, base and learned arms use:

- separate worktrees at the same buggy revision;
- the same task description;
- medium reasoning effort;
- the same visible grader;
- the same sealed child-era hidden test;
- no memory treatment in the base arm;
- the unchanged Qwen lesson in the learned arm.

The visible grader builds and runs the repository's exact Make-based focused
test. The hidden grader replaces that test with the sealed version from the
later fix commit and repeats the grader. Test sensitivity applies only the
learned arm's authored test change to the buggy parent and requires it to fail.

#### Results

| model | base outcome | learned outcome |
|---|---|---|
| Luna | authors production and test changes; stops after assuming unavailable CMake blocks verification; independent Make grader finds an undeclared link dependency | completes a full server build and executes the focused test; an assertion exposes stale fixture state; visible and hidden final grades fail |
| Terra | passes self-selected tests and visible grader; sealed hidden grader fails because the patch changes general readiness rather than the write-tier contract | makes a focused three-file repair; visible and hidden graders pass; authored test-only patch fails on the buggy parent |

The Luna pair crosses over on capability and verification depth, and stops
short of completion. The learned run reaches a build and a focused test its
base run never gets to, then fails the task anyway.

The Terra pair crosses over on completion. The base run looks successful under
its own selected tests and the visible grader, and the sealed contract catches
it. The learned run passes that contract and writes a regression-sensitive
test.

We retried the originating Qwen model with the learned lesson. It failed again
after 519,662 tokens, 1.4% above its source failure, with no patch and no test.
The lesson is no solution, and no general capability increase. Its worth
depends on whether the later model can act on it.

The cross-model runs receive the lesson directly, which is what preserves the
controlled contrast. A storage-backed product test covers the organisational
path on its own: it records the source under one user/session/local-model
reference, reinforces the same row under another user/session/Terra reference,
recalls it for a similar goal, and withholds it from an unrelated one. Between
them, the pilot tests the cross-model effect and the product test covers
source-independent reuse inside an authorised shared KB. No single live
multi-user run has yet exercised both.

### 3.4 Experiment D: cost per passing task and cost of failure

#### Cost per passing task

An earlier paired provider study gives the cleanest billing result. Standard
and Aimee-on conditions use GPT-5.6 Sol at medium reasoning on the same eight
coding tasks. Hidden tests grade outcomes; there are no exclusions or retries.

| measure | standard | Aimee on |
|---|---:|---:|
| passing tasks | 5/8 | 6/8 |
| uncached input tokens | 242,514 | 243,724 |
| cached input tokens | 873,216 | 802,304 |
| output tokens | 19,550 | 16,178 |
| input plus output | 1,135,280 | 1,062,206 |
| billable token units per passing task | 227,056 | 177,034 |

The raw unit count per passing task falls 22.0%. Because billing categories
have different rates, we also price each category at the [published GPT-5.6 Sol
API rates on 27 August
2026](https://developers.openai.com/api/docs/models/gpt-5.6-sol): $4 per
million uncached input tokens, $0.40 per million cached input tokens and $20
per million output tokens. Every request remains below the model page's
long-context threshold.

The standard arm has a price-equivalent total of $1.7103424, or $0.342068480
per passing task. The Aimee-on arm has a total of $1.6193776, or $0.269896267
per passing task. The price-equivalent reduction per passing task is 21.1%.

The runs used subscription authentication, so these values are not invoice
charges. They reprice preserved provider usage categories at a dated public
rate. The sample contains one recovered task and no regression, but eight tasks
are too few to estimate a stable population effect.

#### Cost of an unproductive failure

A second campaign prices failure itself. The same local Qwen3.8-27B model
attempts three defects drawn from Aimee's own history: DB2 pool lease
attribution, repository-clone ownership and descriptor handling, and a
work-item contract crossing C, Go and JSON. Each pair holds the buggy revision,
prompt, tools, limits and sealed hidden grader fixed.

Two of the three sit in strata named for high historical context use, which is
a selection that favours the treatment reported below. The preregistration
keeps those historical outcomes out of the new measurement. It bounds the
effect without removing it.

The control runs the model alone. The treatment passes canonical history
through the production economizer handler and applies the preregistered
progress sequence, which issues a checkpoint, escalates once, and stops after
continued retrieval without a mutation.

| task | languages | Qwen alone | Aimee | reduction |
|---|---|---:|---:|---:|
| pool lease attribution | C | 428,483 | 371,687 | 13.3% |
| clone descriptor and owner | C | 616,577 | 321,292 | 47.9% |
| work-item outcome codes | C, Go, JSON | 774,844 | 506,573 | 34.6% |
| pooled | | 1,819,904 | 1,199,552 | 34.1% |

Every control run reaches the context limit. Every treatment run stops under
the progress sequence. All six runs fail the sealed hidden grader and write no
patch.

The campaign contains the cost of failing, and nothing beyond it. Capability
stayed where it was, and nobody should read the number as saying otherwise. The
treatment is also combined: context reduction and progress termination were
applied together, and the campaign splits the 620,352 tokens between neither.
Three pairs at one run per cell estimate no population effect.

The first attempt at the cross-language pair lacked a required historical build
fixture and failed the visible grader in both conditions. It remains
quarantined in its original artifact and excluded from measurement. A corrected
rerun generates the fixture in both conditions, passes the visible grader in
both and supplies the third retained pair above.

The stopped Qwen run is a looser observation. Its 512,545 tokens sit 11.2%
below an earlier recorded plain failure at 577,214. A fresh plain run then
diverged and hit its context limit at 333,390.

Two recorded trajectories are the whole of what 11.2% describes. It is no
paired estimate. What survives is that the stopped failure produced a reusable
lesson whose later value was above zero.

The campaign carries the economic argument, because a failure only has option
value while it stays cheap. Progress termination bounds the immediate loss. The
durable record supplies the later return.

## 4. Related work

### 4.1 Learning without weight updates

Reflexion shows that linguistic feedback stored in an episodic buffer can
improve subsequent trials across coding, reasoning and sequential decision
tasks ([Shinn et al., 2023](https://arxiv.org/abs/2303.11366)). ExpeL extracts
insights and experiences from training tasks and retrieves them during later
inference ([Zhao et al., 2023](https://arxiv.org/abs/2308.10144)). Both put
visible natural-language learning outside model weights and show that it pays.

Aimee takes that external-learning premise and changes who owns the result. The
record belongs to an authorised organisational scope, and it is built to
survive a change of user, session, tool or model.

### 4.2 Shared and negative memory

INMS creates an asynchronous conversational memory pool shared among agents and
reports gains across three datasets ([Gao and Zhang,
2024](https://arxiv.org/abs/2404.09982)). Learning to Share trains a controller
to admit useful intermediate steps to a global bank shared by parallel teams,
reducing runtime while matching or improving performance ([Fioresi et al.,
2026](https://arxiv.org/abs/2602.05965)). Between them they preclude any broad
claim that Aimee first shared memory among agents.

Negative Knowledge sits closest to the failed-approach mechanism. It converts
failed research attempts into bounded, typed records that a downstream agent
adopts or rejects, and reports same-task, cross-task and cross-problem gains at
fewer tokens ([Wang, 2026](https://arxiv.org/abs/2606.21024)). It makes failure
a collective knowledge asset.

We add a heterogeneous-model repository repair, and the production identity,
scope, correction, isolation and audit substrate around the record.

### 4.3 Cross-model transfer

Recuris is the closest performance precedent. It evolves a benchmark-specific
skill-memory package from failures produced by one deployment model, then loads
the package unchanged into target models that did not participate in evolution.
Across four long-horizon benchmarks and ten models, it reports improvement in
35 of 37 completed model-benchmark pairs ([Yu et al.,
2026](https://arxiv.org/abs/2608.24876)). It therefore rules out a first claim
for cross-model experiential memory increasing task success.

The distinction is deployment scope. Recuris evaluates a memory-control method
on controlled benchmarks. It does not present or evaluate a multi-user
organisational service with access-scoped recall, durable provenance and
correction, independent execution and credential boundaries, or a
tamper-evident audit path. Aimee's contribution is the production system and
the trace from a stopped local-model failure to another model tier's
hidden-graded repository completion.

Cross-Model Memory Transfer studies a different representation: a learned
Engram table moved across backbones and read through a compatible or adapted
target-side reader ([Li et al., 2026](https://arxiv.org/abs/2608.17050)). It
shows that learned external knowledge ports between backbones. The object it
ports is parametric-adjacent stored knowledge, and the questions it answers sit
outside experiential failure memory and organisational agent memory.

Structurally aligned subtask-level memory applies memory directly to software
engineering agents and evaluates across model backbones on SWE-bench Verified
([Shen et al., 2026](https://arxiv.org/abs/2602.21611)). It is an important
baseline for a confirmatory Aimee campaign. Our pilot differs on two points: it
transfers a record derived from one named failed trajectory, and it tests the
production governance path separately.

## 5. Discussion

### 5.1 Realised capability belongs to the model-harness pair

The Qwen lesson leaves Luna and Terra weights untouched, and it fails to rescue
Qwen on retry. It still moves the work both Codex tiers reach, and it moves
Terra's final grade. So two kinds of capability are worth separating.

Intrinsic capability is a property of the model under a specified interface.
Realised capability is the work that the model, memory, tools, policy and
verification harness complete together. A durable record raises the second
while the first stands still.

The separation has a price attached. An organisation buys completed work from a
system, and a memory that lets a cheaper or different model finish a task is
worth money with no fine-tuning anywhere in the story.

### 5.2 Failure has option value

Progress termination bounds the waste immediately. The durable record adds
option value on top, because a later worker may skip the failed strategy or
reach a solution. The total return from a failure:

```text
avoided additional run cost
+ value of later completions changed by the lesson
+ avoided rediscovery across authorised users
- synthesis, retrieval, review and operating cost
- harm from stale or misapplied lessons
```

The three matched pairs measure the first term at 34.1% of pooled consumption
on those tasks. The cross-model pilot gives one observation of the second.
Neither fixes a population expectation.

The ACL experience-following result loads the last negative term. A system that
shares lessons widely amplifies bad lessons just as widely. Provenance, scope,
correction, admission gates and future-outcome feedback all do efficacy work
here, and calling them enterprise features understates the job.

### 5.3 Production breadth buys nothing about efficacy breadth

Rakuen reports current Aimee use across legal, accounting, software and other
professional work. Customer identities and records are confidential, and none
of them are experimental data here. The breadth shows the system runs outside
coding. Whether the measured software effect size survives the move to another
domain is unknown.

We measure in software because a fixed revision, a visible test, a sealed
hidden test and a test-sensitivity check make an outcome unusually hard to
argue with. A domain study needs criteria that are just as external:
adjudicated legal review, reconciled accounting outcomes, predeclared research
replication.

## 6. Threats to validity

The strongest objection to Experiment C is that the typed record did nothing a
paragraph of any kind would not have done. Both learned runs received text
about a prior failure, and neither was compared against a raw transcript of the
Qwen run or a generic warning against over-exploring. On the evidence here we
cannot separate the value of the record from the value of telling a model that
someone already failed. Section 7.2 is the four-arm control that would, and it
has not run.

The cross-model result also has one task and one run per arm. Model
stochasticity, prompt sensitivity and task-specific interaction could each
explain some or all of an unreplicated difference. The event occurred under the
recorded protocol. Its probability is unmeasured.

The cross-model runs receive the lesson directly. Shared-KB persistence and
source-independent recall are tested elsewhere. No experiment yet runs the
whole live path from user A's Qwen failure to authorised retrieval by user B's
Terra agent.

The collaboration runtime withholds token-usage objects for Luna and Terra, so
their comparison carries capability and completion claims and nothing about
cost. Whether the learned run was cheaper is unknown.

The Qwen token comparison is an unstable pair. A fresh plain run diverged and
failed earlier than both recorded runs. Establishing an expected stopping
benefit needs repeated randomised trajectories or a deterministic replay
environment.

The deterministic study uses matching task descriptions and a fixed consumer.
It has strong internal validity for the synthesis-and-recall path, and thin
ecological validity for open-ended reasoning and semantic generalisation.

The failure-cost campaign carries the limits recorded in section 3.4: a
combined treatment, no capability claim, three pairs at one run per cell, and a
task set selected partly for high historical context use.

The novelty statement rests on a bounded review of published literature and
public product documentation. A private system with the same combination would
not appear in either source.

We build Aimee and operate the deployments we report on. The paper, the system
and the experiments are all first-party. Public source, artifact hashes,
retained negative results and sealed graders make the work auditable. None of
that is independent replication.

## 7. Confirmatory study design

A submission-grade campaign should preregister the following before any model
run.

### 7.1 Tasks and repositories

Use at least 30 tasks across three large repositories, including multiple
implementation languages and tasks selected to exceed a normal agent's context
when approached by exhaustive exploration. Freeze buggy revisions, visible
tests, hidden tests and test-sensitivity checks before treatment assignment.

Include repair, diagnosis, migration and cross-repository dependency tasks.
Exclude only predeclared infrastructure failures. Publish every exclusion and
failed arm.

### 7.2 Source and consumer models

Cross at least three source classes with three consumer classes:

- a local open-weight model;
- a cost-oriented hosted model;
- a frontier hosted model.

For each source failure, compare four consumer arms: base, raw transcript,
generic failure warning, and typed Aimee record. Repeat each enough times to
estimate stochastic variance. Only that four-way split answers the objection in
section 6, and it is the arm we would run first.

### 7.3 Recall generalisation and near-miss controls

The deterministic study in section 3.2 used matching task descriptions. It buys
recall efficacy for lexical matches, and its novel tasks show that unrelated
goals collect nothing. The interesting ground lies between those two results: a
goal that states the same problem in different words. Where recall stops
reaching is unmeasured.

Extend the deterministic consumer with four goal classes against one stored
record:

- the original goal, as already tested;
- a paraphrase preserving meaning and vocabulary;
- a structurally related goal that shares little of its vocabulary;
- a near miss that shares vocabulary but requires a different approach, which
must not recall the record.

Report retrieval precision and recall separately from consumer outcome, and
give the near-miss class its own false-positive rate. Folding it into an
aggregate score hides the failure that matters. The study needs no provider
spend and no model variance, so it should run before any hosted campaign.

### 7.4 Mechanism attribution for failure cost

The matched failure-cost campaign in section 3.4 applied context reduction and
progress termination together, so its 34.1% reduction describes a combined
treatment and attributes nothing to either mechanism.

Run the four conditions separately on the same task set and revisions:

| condition | context reduction | progress termination |
|---|---|---|
| control | off | off |
| reduction only | on | off |
| termination only | off | on |
| combined | on | on |

Report tokens at termination and terminal reason for every cell. Both
mechanisms end a run early for different reasons, which makes the terminal
reason part of the result and not a diagnostic beside it. Until this runs, no
published number may credit progress control alone with a failure-cost saving.

### 7.5 End-to-end organisational path

Record source failures under one authorised user and model identity. Require
the consumer to retrieve through another authorised user and model identity on
the same shared KB. Add controls for a different KB, an unauthorised scope, an
unrelated goal, a superseded record and a deliberately poisoned record.

Verify that:

- authorised similar goals receive the record;
- unrelated goals do not;
- unauthorised users cannot infer the record or its existence;
- corrected records supersede stale advice;
- every mutation and retrieval decision has the expected audit evidence.

### 7.6 Outcomes

Primary outcome: hidden-grade task completion.

Secondary outcomes:

- regression-sensitive test authorship;
- time and billable cost to first passing result;
- provider token categories for every model, including workers;
- progress termination rate and cost at termination;
- repeated or overlapping retrievals;
- lesson retrieval precision and following rate;
- negative transfer and unrelated-task regression;
- cross-user scope leakage;
- operator review and curation time.

Use paired analysis within task and consumer model. Report treatment-only and
control-only outcomes, confidence intervals, negative results and family-wise
error control for secondary measures. Preserve raw provider usage and exact
grader commands under content hashes.

## 8. Conclusion

External memory carries agent learning across model boundaries. Prior work
settles that. The production questions are who owns the lesson, who may receive
it, how it gets corrected, what it is allowed to change, and whether its effect
can be audited.

Aimee treats the organisation as the learning unit. One live target shows six
feedback loops reaching later consumers. A replicated paired study shows one
loop causally changing matched outcomes. A large-repository pilot shows a
stopped Qwen failure changing later Luna and Terra work, including a Terra
completion that passes a sealed hidden grader and writes a regression-sensitive
test. The originating Qwen retry failed, and both Luna final grades failed.

What we have is one documented occurrence of a production path from failed work
to shared cross-model capability. A general effect size needs the campaign in
section 7. Until it runs, how often the path pays, what it costs, and how
safely it crosses users and domains are all open.

## 9. Data and code availability

Aimee is published under the GNU Affero General Public License at
[github.com/RakuenSoftware/aimee](https://github.com/RakuenSoftware/aimee). The
cross-model artifacts, failure-cost artifacts and product-test changes merged
on 28 August 2026 through Aimee PR
[#2873](https://github.com/RakuenSoftware/aimee/pull/2873) at commit
[`faaf05298ce4d3b484f24cb00ccc402c62128e69`](https://github.com/RakuenSoftware/aimee/tree/faaf05298ce4d3b484f24cb00ccc402c62128e69).

We verified every SHA-256 in the evidence inventory against that commit. The
[evidence
inventory](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/failure-as-shared-capability/evidence/figures.md)
records source paths, artifact hashes, invalid attempts, negative results and
claim limits. Full provider transcripts stay out of the blog repository because
they hold agent conversation data. We retain their hashes and usage fields.

## 10. Conflict of interest

We build Aimee, and we operate the deployments reported here. Rakuen sells
commercial licence terms and services for deployments that do not take the AGPL
terms, so a favourable result here is worth money to us. Every product and
deployment claim in this paper is first-party. The evidence inventory, the
public source and the retained negative results are how a reader checks us.

## References

We verified every entry against its primary source on 29 August 2026. The list
is style-neutral and carries author, title, venue and identifier, so converting
it to a venue's citation style needs no return to the sources.

Fioresi, J., Kulkarni, P. P., Vayani, A., Wang, S., and Shah, M. (2026).
*Learning to Share: Selective Memory for Efficient Parallel Agentic Systems.*
arXiv:2602.05965. Submitted 5 February 2026, revised 14 June 2026.
<https://arxiv.org/abs/2602.05965>

Gao, H., and Zhang, Y. (2024). *INMS: Memory Sharing for Large Language Model
based Agents.* arXiv:2404.09982. Submitted 15 April 2024, revised 4 March 2026.
<https://arxiv.org/abs/2404.09982>

Li, M., Yu, G., Wang, X., and Ji, S. (2026). *Cross-Model Memory Transfer via
Target-Side Reader Adaptation.* arXiv:2608.17050. Submitted 17 August 2026,
revised 19 August 2026. <https://arxiv.org/abs/2608.17050>

Shen, K., Zhang, J., Sun, C., Zeng, W., and Yue, Y. (2026). *Structurally
Aligned Subtask-Level Memory for Software Engineering Agents.*
arXiv:2602.21611. Submitted 25 February 2026.
<https://arxiv.org/abs/2602.21611>

Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., and Yao, S.
(2023). *Reflexion: Language Agents with Verbal Reinforcement Learning.*
arXiv:2303.11366. Submitted 20 March 2023. <https://arxiv.org/abs/2303.11366>

Wang, H. (2026). *Negative Knowledge as Failure-aware Shared Memory for
AutoResearch.* arXiv:2606.21024. Submitted 19 June 2026.
<https://arxiv.org/abs/2606.21024>

Xiong, Z., Lin, Y., Xie, W., He, P., Liu, Z., Tang, J., Lakkaraju, H., and
Xiang, Z. (2026). *How Memory Management Impacts LLM Agents: An Empirical Study
of Experience-Following Behavior.* In Proceedings of the 64th Annual Meeting of
the Association for Computational Linguistics (Volume 1: Long Papers), pages
623-645, San Diego, California. <https://aclanthology.org/2026.acl-long.27/>

Yu, Z., Wu, Y., Yin, Z., Chen, K., Zhao, Z., Wang, M., Yan, S., and Yang, L.
(2026). *Recursive Experiential-Working Memory Evolution for Long-Horizon Agent
Harnesses.* arXiv:2608.24876. Submitted 25 August 2026. The system is named
Recuris. <https://arxiv.org/abs/2608.24876>

Zhao, A., Huang, D., Xu, Q., Lin, M., Liu, Y.-J., and Huang, G. (2023). *ExpeL:
LLM Agents Are Experiential Learners.* arXiv:2308.10144. Submitted 20 August
2023. Published at the 38th AAAI Conference on Artificial Intelligence
      (AAAI-24). <https://arxiv.org/abs/2308.10144>
