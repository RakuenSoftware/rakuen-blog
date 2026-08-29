---
title: "From Failed Run to Shared Capability: Production-Grade Organisational Memory Across Heterogeneous Language-Model Agents"
slug: failure-as-shared-capability
date: 2026-08-27
author: Rakuen Software
tags: [language-model-agents, memory, cross-model-transfer, organisational-learning, ai-systems]
excerpt: "A production-oriented memory substrate turns one model's stopped failure into durable organisational knowledge and changes the graded work completed by another model tier."
---

# From Failed Run to Shared Capability

## Production-Grade Organisational Memory Across Heterogeneous Language-Model Agents

**Status:** Working paper. The deterministic recall study is replicated. The
open-ended cross-model study is an exploratory pilot with one task and one run
per arm. It should not be read as a population estimate.

## Abstract

Language-model agents commonly discard operational experience at session and
model boundaries. Prior work shows that episodic reflection, experiential
memory, shared agent memory, negative knowledge and evolved skill packages can
improve later task performance without changing model weights. Less studied is
the production systems problem: how an organisation can retain these lessons
across users and heterogeneous models while preserving provenance, access
scope, correction history, execution isolation and an audit path the learner
does not control.

We describe Aimee, a self-hosted organisational learning substrate deployed
across legal, accounting, software and other professional work. We evaluate one
of its six feedback loops at three levels. First, a live two-service target
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
graders and authors a regression-sensitive test. A learned Qwen retry also
fails, showing that the advisory is not universally sufficient.

Separately, three matched large-repository pairs on the same local model reduce
pooled consumption from 1,819,904 to 1,199,552 tokens, a 34.1% reduction, while
all six runs fail their sealed hidden grader. That result bounds the cost of an
unproductive failure rather than raising capability.

These results establish causal recall efficacy under a fixed consumer and an
observed cross-model completion crossover under open-ended work. They do not
estimate the frequency of transfer. We conclude with a design to be preregistered before
any confirmatory run, for measuring cross-model, cross-user capability and cost
at scale.

## 1. Introduction

An organisation pays for more than model output. It pays for investigation,
failed approaches, corrections, verification and the context needed to reach a
decision. Most agent systems attach that work to a transcript, an individual
agent or a single model's retry loop. When the session ends or the model
changes, the next worker can pay for the same discovery again.

External memory changes that economic unit. A failed trajectory can become a
record that changes later work without fine-tuning the model that consumes it.
The record can outlive model upgrades and can be inspected or withdrawn
independently of model weights. Prior research establishes that this is useful.
[Reflexion](https://arxiv.org/abs/2303.11366) keeps verbal reflections in an
episodic buffer for later trials. [ExpeL](https://arxiv.org/abs/2308.10144)
extracts natural-language insight from prior tasks. [INMS](https://arxiv.org/abs/2404.09982)
shares conversational memories among agents. [Negative Knowledge](https://arxiv.org/abs/2606.21024)
turns failed research attempts into typed shared records. Most directly,
[Recuris](https://arxiv.org/abs/2608.24876) evolves a skill-memory package from
one deployment model and reports gains when that package is loaded unchanged
into other frozen models.

The remaining problem is organisational rather than purely algorithmic. A
production memory record needs an owner, an access boundary, provenance, a
correction path and an accountable consumer. A learner that can expand its own
credentials or rewrite its own audit history is not a governed learning system.
A memory that crosses users without scope is a data leak. A successful result
without a negative-transfer record makes later evaluation unreliable.

This paper studies Aimee as a systems response to that problem. Aimee separates
per-user agent services from a shared knowledge service. It stores learned
records outside model weights, retains their evidence and scope, and routes
execution through controls outside the learner. Memory mutations produce audit
intents that a separately credentialed worker commits to a hash chain.

We ask four questions:

1. Do the implemented feedback loops reach the later consumers they are meant
   to change?
2. Does failed-approach synthesis and recall causally change a later outcome
   when the consumer is fixed?
3. Can a failure produced by one model change the open-ended capability or
   completion of another model tier?
4. Can the same substrate reduce cost per successful task or limit the cost of
   an unproductive failure?

The evidence answers the first two questions directly. It answers the third
with an exploratory occurrence rather than a rate. Existing cost data answers
part of the fourth and defines the next experiment.

Our contributions are:

- a production-oriented organisational memory architecture that separates
  learning from model identity while retaining scope, provenance, correction,
  isolation and independent audit;
- a replicated paired study that isolates the causal effect of one production
  synthesis-and-recall loop;
- an exploratory trace from a stopped local-model failure to changed behaviour
  in two later model tiers, including one hidden-graded completion crossover;
- an economic framing in which failure control, retained negative knowledge and
  cross-user reuse are measured as one organisational learning loop, including
  three matched large-repository pairs that cut the cost of an unproductive
  failure by 34.1% without raising capability;
- a confirmatory protocol for estimating the frequency, cost and security of
  cross-model, cross-user transfer.

We do not claim the first cross-model memory benefit. Recuris and INMS rule out
that broad claim, and earlier work establishes experiential learning more
generally. The contribution here is the production systems combination and its
observed path through a real large repository.

Our review of prior work is bounded rather than exhaustive. We searched the
published literature and the available public documentation of adjacent
commercial products, and found none that documents this complete combination.
Absence from the published record is not evidence of absence, and we make no
claim about unpublished or private production systems.

## 2. System model

### 2.1 The organisation, not the model, owns the state

Aimee has two principal services. An `aimee-server` assists one human and owns
that person's sessions, tools, credentials, delegates and workflows. An
`aimee-kb` holds a corpus for a team or organisation. Many personal services
can use one shared knowledge service while authorisation constrains what each
principal may read or change.

Models are replaceable workers behind this boundary. The model that produces a
record can differ from the model that later consumes it. Source model, session
and user are retained as provenance rather than treated as the owner of the
lesson. Retrieval still respects the caller's authorised KB and scope.

This separation supports a stronger form of amortisation than personal memory.
One user can pay the discovery cost while later authorised users receive the
lesson. A local model can generate a record later consumed by a hosted model.
Replacing either model does not erase the organisation's operational history.

### 2.2 A failed approach is a typed, correctable record

For the loop evaluated here, repeated failed jobs are synthesised into a failed
approach. The record contains a goal, the approach taken, a failure mode,
source provenance and occurrence history. Similar-goal recall returns the
record during later planning. An unrelated goal should not receive it.

The no-progress record deliberately uses stable approach text. A retry
reinforces one record rather than creating an unbounded set of paraphrases. The
originating user, session and model remain attached to the observation, but the
recall query does not filter on those fields. Authorisation is enforced at the
knowledge-service boundary.

Records are not assumed permanently correct. Aimee's memory model supports
later evidence, supersession and correction. This matters because agent memory
has an experience-following effect: similar retrieved examples can induce
similar outputs, which can propagate errors or replay a superficially similar
but misaligned experience ([Xiong et al., 2026](https://aclanthology.org/2026.acl-long.27/)).

### 2.3 The learner does not own execution or audit

Learning changes future preparation and policy, so the controls around it must
remain outside the learner. Aimee routes delegated work through explicit
capabilities, workspace and network boundaries, and separately managed
credentials. The learned record can advise a plan; it cannot grant itself a
new authority.

Memory changes use a separate audit path. The mutation transaction writes an
immutable audit intent. A separately credentialed worker seals committed
intents into a hash chain. Fault-injection tests cover the live seal, a control
with seal calls removed, rollback after an injected crash, recovery and
idempotent restart.

Aimee also classifies the evidence behind self-produced learning. Human
corrections, test exits, external verification, observed version-control
outcomes and official graders are exogenous. Signals inferred only from the
agent's own transcript are endogenous. When the exogenous ratio falls below the
configured gate, the system can refuse automatic admission. This prevents the
learner from making an entirely self-authored history its own yardstick.

## 3. Evaluation

### 3.1 Experiment A: loop closure

The first experiment asks whether six implemented feedback loops reach their
consumers on a live deployment. The target starts `aimee-server`, `aimee-kb`,
their required modules and PostgreSQL against disposable state. It observes:

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

This result establishes closure, not benefit. It demonstrates that an outcome
can change durable state and that a later consumer reads that state. It does not
show that every loop improves a downstream task.

### 3.2 Experiment B: causal efficacy of failed-approach recall

The second experiment separates setup from consumption.

Both conditions receive the same 48 failed `agent_jobs`: two observations for
each of 24 repeated tasks. The control condition withholds the production
synthesis pass. The treatment runs `aimee eval candidates-update scan` and
reads the learned result through the production `aimee learning approaches`
command.

A deterministic consumer begins each task with the same fixed choice. It
changes that choice only if the production recall output identifies the
matching failed approach. An additional 24 novel tasks have no matching
history. They test whether unrelated learned records cause indiscriminate
behaviour change.

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

This design isolates the production synthesis and recall path from stochastic
model behaviour. It establishes causal efficacy for matching task
descriptions. It does not measure whether an open-ended model follows the
advisory or generalises it to a structurally related but lexically different
goal.

### 3.3 Experiment C: exploratory cross-model transfer

The third experiment retains model variance and asks whether the record changes
realised agent capability.

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

The Luna pair is a capability and verification-depth crossover without a
completion crossover. The learned arm reaches build and focused-test execution
that the base arm does not, then still fails the task.

The Terra pair is a completion crossover. The base arm appears successful under
its selected tests and the visible grader but fails the sealed contract. The
learned arm passes that contract and supplies a regression-sensitive test.

The originating Qwen model is also retried with the learned lesson. It fails
again after 519,662 tokens, 1.4% above its source failure, with no patch or test.
This negative result prevents interpreting the lesson as a solution or as a
universal capability increase. Its value is conditional on the later model's
ability to act on it.

The cross-model arms receive the lesson directly to preserve the controlled
contrast. A storage-backed product test covers the organisational path
separately. It records the source under one user/session/local-model reference,
reinforces the same row under another user/session/Terra reference, recalls it
for a similar goal and excludes an unrelated goal. The pilot therefore directly
tests cross-model effect, while the product test establishes source-independent
reuse inside an authorised shared KB. It does not yet exercise both properties
in one live multi-user run.

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

The raw unit count per passing task falls 22.0%. Because billing categories have
different rates, we also price each category at the
[published GPT-5.6 Sol API rates on 27 August 2026](https://developers.openai.com/api/docs/models/gpt-5.6-sol):
$4 per million uncached input tokens, $0.40 per million cached input tokens and
$20 per million output tokens. Every request remains below the model page's
long-context threshold.

The standard arm has a price-equivalent total of $1.7103424, or $0.342068480
per passing task. The Aimee-on arm has a total of $1.6193776, or $0.269896267
per passing task. The price-equivalent reduction per passing task is 21.1%.

The runs used subscription authentication, so these values are not invoice
charges. They reprice preserved provider usage categories at a dated public
rate. The sample contains one recovered task and no regression, but eight tasks
are too few to estimate a stable population effect.

#### Cost of an unproductive failure

A second campaign measures the cost of failure itself rather than the cost of
success. The same local Qwen3.8-27B model attempts three defects drawn from
Aimee's own history: DB2 pool lease attribution, repository-clone ownership and
descriptor handling, and a work-item contract crossing C, Go and JSON. Each
pair uses the same buggy revision, prompt, tools, limits and sealed hidden
grader. The control condition runs the model alone. The treatment passes
canonical history through the production economizer handler and applies the
preregistered progress sequence, which issues a checkpoint, escalates once and
stops after continued retrieval without a mutation.

| task | languages | Qwen alone | Aimee | reduction |
|---|---|---:|---:|---:|
| pool lease attribution | C | 428,483 | 371,687 | 13.3% |
| clone descriptor and owner | C | 616,577 | 321,292 | 47.9% |
| work-item outcome codes | C, Go, JSON | 774,844 | 506,573 | 34.6% |
| pooled | | 1,819,904 | 1,199,552 | 34.1% |

Every control run reaches the context limit. Every treatment run stops under
the progress sequence. All six runs fail the sealed hidden grader and write no
patch.

The result is therefore failure-cost containment, not a capability increase.
Model capability did not rise in this campaign, and the finding must not be read
as one. It is also a combined treatment: the campaign does not attribute the
620,352-token difference between context reduction and progress termination.
Three pairs with one run per cell do not estimate a population effect.

The first attempt at the cross-language pair lacked a required historical build
fixture and failed the visible grader in both conditions. It remains quarantined
in its original artifact and excluded from measurement. A corrected rerun
generates the fixture in both conditions, passes the visible grader in both and
supplies the third retained pair above.

The stopped Qwen run offers a less controlled cost observation. Its 512,545
tokens are 11.2% below an earlier recorded plain failure at 577,214. A fresh
plain arm diverges and reaches its context limit earlier at 333,390 tokens.
Therefore, 11.2% describes two recorded trajectories and is not a paired
estimate. The stronger economic observation is that the stopped failure
produces a reusable lesson whose later value is not zero.

This campaign matters to the paper's economic argument because the option value
of a failure is only positive when the failure is cheap. Progress termination
bounds the immediate loss; the durable record supplies the later return.

## 4. Related work

### 4.1 Learning without weight updates

Reflexion demonstrates that linguistic feedback stored in an episodic buffer
can improve subsequent trials across coding, reasoning and sequential decision
tasks ([Shinn et al., 2023](https://arxiv.org/abs/2303.11366)). ExpeL extracts
insights and experiences from training tasks and retrieves them during later
inference ([Zhao et al., 2023](https://arxiv.org/abs/2308.10144)). Both establish
the value of visible natural-language learning outside model weights.

Aimee adopts that external-learning premise but changes the ownership and
governance model. The record belongs to an authorised organisational scope
rather than an agent's private retry buffer. It is expected to survive changes
of user, session, tool and model.

### 4.2 Shared and negative memory

INMS creates an asynchronous conversational memory pool shared among agents and
reports gains across three datasets ([Gao and Zhang, 2024](https://arxiv.org/abs/2404.09982)).
Learning to Share trains a controller to admit useful intermediate steps to a
global bank shared by parallel teams, reducing runtime while matching or
improving performance ([Fioresi et al., 2026](https://arxiv.org/abs/2602.05965)).
These results preclude any broad claim that Aimee first shares memory among
agents.

Negative Knowledge is closest to the failed-approach mechanism. It converts
failed research attempts into bounded, typed records that a downstream agent
adopts or rejects. It reports same-task, cross-task and cross-problem gains with
fewer tokens ([Wang, 2026](https://arxiv.org/abs/2606.21024)). That work
establishes failure as a collective knowledge asset. The present paper adds a
heterogeneous-model repository repair and the production identity, scope,
correction, isolation and audit substrate around the record.

### 4.3 Cross-model transfer

Recuris is the closest performance precedent. It evolves a benchmark-specific
skill-memory package from failures produced by one deployment model, then loads
the package unchanged into target models that did not participate in evolution.
Across four long-horizon benchmarks and ten models, it reports improvement in
35 of 37 completed model-benchmark pairs ([Yu et al., 2026](https://arxiv.org/abs/2608.24876)).
It therefore rules out a first claim for cross-model experiential memory
increasing task success.

The distinction is deployment scope. Recuris evaluates a memory-control method
on controlled benchmarks. It does not present or evaluate a multi-user
organisational service with access-scoped recall, durable provenance and
correction, independent execution and credential boundaries, or a
tamper-evident audit path. Aimee's contribution is the production system and
the trace from a stopped local-model failure to another model tier's
hidden-graded repository completion.

Cross-Model Memory Transfer studies a different representation: a learned
Engram table moved across backbones and consumed through a compatible or adapted
target-side reader ([Li et al., 2026](https://arxiv.org/abs/2608.17050)). It
establishes portability of learned external knowledge but is not an
experiential failure record or an organisational agent memory.

Structurally aligned subtask-level memory applies memory directly to software
engineering agents and evaluates across model backbones on SWE-bench Verified
([Shen et al., 2026](https://arxiv.org/abs/2602.21611)). It is an important baseline for a
confirmatory Aimee campaign. The present pilot differs by transferring a record
derived from a named failed source trajectory and by testing the production
governance path separately.

## 5. Discussion

### 5.1 Realised capability belongs to the model-harness pair

The Qwen lesson does not change Luna or Terra weights. It also does not make
Qwen succeed on retry. Yet it changes the work reached by both Codex tiers and
changes Terra's final grade. It is therefore useful to distinguish intrinsic
model capability from realised agent capability.

Intrinsic capability is a property of the model under a specified interface.
Realised capability is the work completed by the model, memory, tools, policy
and verification harness together. A durable record can increase the latter
without changing the former.

This distinction is operationally important. Organisations purchase completed
work from systems, not isolated model weights. A memory that lets a less costly
or different model complete a task has economic value even if no model was
fine-tuned.

### 5.2 Failure has option value

Progress termination provides an immediate bound on waste. The durable record
adds option value: a later worker may avoid the failed strategy or reach a
solution. The total return from a failure is therefore:

```text
avoided additional run cost
+ value of later completions changed by the lesson
+ avoided rediscovery across authorised users
- synthesis, retrieval, review and operating cost
- harm from stale or misapplied lessons
```

The three matched large-repository pairs measure the first term directly at
34.1% of pooled consumption on those tasks. The cross-model pilot supplies one
observation of the second. Neither establishes a population expectation. The ACL experience-following result makes the final
negative term especially important. A system that shares lessons widely also
amplifies bad lessons widely. Provenance, scope, correction, admission gates
and future-outcome feedback are part of the efficacy mechanism, not only
enterprise features.

### 5.3 Production breadth is not efficacy breadth

Rakuen reports current Aimee use across legal, accounting, software and other
professional work. Customer identities and records are confidential and are
not experimental data in this paper. This deployment breadth shows that the
substrate is not coding-specific. It does not show that the measured software
effect size transfers to another domain.

Software is used here because a fixed revision, visible test, sealed hidden test
and test-sensitivity check provide unusually strict outcome evidence. Future
domain studies need comparably external criteria, such as adjudicated legal
review, reconciled accounting outcomes or predeclared research replication.

## 6. Threats to validity

The cross-model result has one task and one run per arm. Model stochasticity,
prompt sensitivity and task-specific interaction can explain some or all of an
unreplicated difference. The result proves that the event occurred under the
recorded protocol; it does not estimate its probability.

The lesson is supplied directly in the cross-model arms. Shared-KB persistence
and source-independent recall are tested separately. The experiment does not
yet demonstrate a complete live path from user A's Qwen failure through
authorised retrieval by user B's Terra agent.

Luna and Terra token-usage objects are unavailable from the collaboration
runtime. Their comparison supports capability and completion claims only. It
cannot establish that the learned arm is cheaper.

The Qwen token comparison is not a stable pair. A fresh plain run diverges and
fails earlier than both recorded runs. Any expected stopping benefit requires
repeated randomised trajectories or a deterministic replay environment.

The deterministic study uses matching task descriptions and a fixed consumer.
It has strong internal validity for the synthesis-and-recall path but limited
ecological validity for open-ended reasoning and semantic generalisation.

The failure-cost campaign is a combined treatment. Context reduction and
progress termination are applied together, so the 34.1% reduction cannot be
attributed to either mechanism. All six of its runs fail the hidden grader, so
it supports no capability claim, and three pairs with one run per cell do not
estimate a population effect.

The novelty statement rests on a bounded review of published literature and
public product documentation. A private system with the same combination would
not appear in either source.

The authors build Aimee and operate the reported deployments. The article,
system and experiments are first-party. Public source, artifact hashes, retained
negative results and sealed graders improve auditability but do not substitute
for independent replication.

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

For each source failure, compare consumer base, raw-transcript, generic
failure-warning and typed Aimee-record arms. Repeat each arm enough times to
estimate stochastic variance. This distinguishes the value of the learned
record from extra prompt text or knowledge of failure alone.

### 7.3 Recall generalisation and near-miss controls

The deterministic study in section 3.2 used matching task descriptions. It
therefore establishes recall efficacy for lexical matches and, through its novel
tasks, shows that unrelated goals receive nothing. It does not show that recall
reaches a goal expressing the same problem in different words, and it does not
locate the boundary between the two.

Extend the deterministic consumer with four goal classes against one stored
record:

- the original goal, as already tested;
- a paraphrase preserving meaning and vocabulary;
- a structurally related goal with substantially different vocabulary;
- a near miss that shares vocabulary but requires a different approach, which
  must not recall the record.

Report recall precision and recall separately from consumer outcome, and report
the near-miss class as a false-positive rate rather than folding it into an
aggregate score. This study needs no provider spend and no model variance, so
run it before any hosted campaign.

### 7.4 Mechanism attribution for failure cost

The matched failure-cost campaign in section 3.4 applied context reduction and
progress termination together. Its 34.1% reduction therefore describes a
combined treatment and attributes nothing to either mechanism.

Run the four conditions separately on the same task set and revisions:

| condition | context reduction | progress termination |
|---|---|---|
| control | off | off |
| reduction only | on | off |
| termination only | off | on |
| combined | on | on |

Report tokens at termination and terminal reason for every cell. Both mechanisms
plausibly end a run early for different reasons, so the terminal reason is part
of the result rather than a diagnostic. Until this runs, no published number
should attribute failure-cost savings to progress control alone.

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

External memory can make agent learning portable across model boundaries. Prior
work establishes that principle. The production question is who owns the
lesson, who may receive it, how it is corrected, what it is allowed to change
and whether its effect can be audited.

Aimee treats the organisation as the learning unit. One live target shows six
feedback loops reaching later consumers. A replicated paired study shows one
loop causally changing matched outcomes. An exploratory large-repository pilot
shows a stopped Qwen failure changing later Luna and Terra work, including a
Terra completion that passes a sealed hidden grader and supplies a
regression-sensitive test. The originating Qwen retry and both Luna final
grades remain negative.

The result is not a general effect size. It is a documented occurrence of a
production-oriented path from failed work to shared cross-model capability. The
next step is to measure how often that path pays, how much it costs, and how
safely it crosses users and domains.

## Data and code availability

Aimee is published under the GNU Affero General Public License at
[github.com/RakuenSoftware/aimee](https://github.com/RakuenSoftware/aimee).
The cross-model artifacts, failure-cost artifacts and product-test changes
merged on 28 August 2026 through Aimee PR
[#2873](https://github.com/RakuenSoftware/aimee/pull/2873) at commit
[`faaf05298ce4d3b484f24cb00ccc402c62128e69`](https://github.com/RakuenSoftware/aimee/tree/faaf05298ce4d3b484f24cb00ccc402c62128e69).
Every SHA-256 in the evidence inventory is verified against that commit. The article's
[evidence inventory](../evidence/figures.md) records source paths, artifact
hashes, invalid attempts, negative results and claim limits. Full provider
transcripts are not placed in the blog repository because they contain agent
conversation data; their hashes and usage fields are retained.

## Conflict of interest

The authors build Aimee. Rakuen offers commercial licence terms and services
for deployments that do not use the AGPL terms. All product and deployment
claims in this paper are first-party.

## References

Every entry was verified against its primary source on 29 August 2026. The list
is deliberately style-neutral and carries author, title, venue and identifier so
it can be converted to a venue's citation style without returning to the
sources.

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
Aligned Subtask-Level Memory for Software Engineering Agents.* arXiv:2602.21611.
Submitted 25 February 2026. <https://arxiv.org/abs/2602.21611>

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
623-645, San Diego, California.
<https://aclanthology.org/2026.acl-long.27/>

Yu, Z., Wu, Y., Yin, Z., Chen, K., Zhao, Z., Wang, M., Yan, S., and Yang, L.
(2026). *Recursive Experiential-Working Memory Evolution for Long-Horizon Agent
Harnesses.* arXiv:2608.24876. Submitted 25 August 2026. The system is named
Recuris. <https://arxiv.org/abs/2608.24876>

Zhao, A., Huang, D., Xu, Q., Lin, M., Liu, Y.-J., and Huang, G. (2023). *ExpeL:
LLM Agents Are Experiential Learners.* arXiv:2308.10144. Submitted 20 August
2023. Published at the 38th AAAI Conference on Artificial Intelligence
(AAAI-24). <https://arxiv.org/abs/2308.10144>
