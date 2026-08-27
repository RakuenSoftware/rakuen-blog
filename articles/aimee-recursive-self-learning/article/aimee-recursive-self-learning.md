---
title: "Aimee: Recursive Self-Learning"
slug: aimee-recursive-self-learning
date: 2026-08-27
author: Rakuen Software
tags: [aimee, self-learning, memory, isolation]
excerpt: "Aimee 0.4.0 closes six learning loops on a live deployment. A paired study isolates one loop's effect, and a Qwen failure changes later Luna and Terra work, including a completion crossover in Terra."
---

*Rakuen builds aimee, the system reported on here. This is the first technical
entry in a four-article series, after the non-technical overview and followed by
the memory and architecture under both. Source and test provenance live in the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/aimee-recursive-self-learning/evidence/figures.md).
Source was rechecked against `testing` at `6bcc87e` on 25 August 2026. Efficacy
and cross-model evidence was added on 27 August.*

Aimee is available as a managed cloud service or self-hosted. It puts durable
memory, code knowledge, model routing and execution controls around AI coding
tools. One personal service holds a user's work. A shared knowledge service can
serve a corpus, team or company while keeping access scoped.

Rakuen currently uses Aimee in production. Work across legal, accounting,
software, and other professional fields is the intended use. This article uses
software experiments because code, builds and sealed tests make the causal
boundary unusually strict. It does not claim that the measured software effect
size transfers unchanged to every domain.

Version 0.4.0 closes six feedback loops in that system. On 25 August 2026, one
live two-service target observed every loop and finished at **46 checks passed,
0 failed**. The result proves that learned state reaches later work on the
tested deployment.

A later paired study isolates a task-outcome gain from the failed-approach loop.
An exploratory large-repository pilot then carries one Qwen failure into Luna
and Terra, with a completion crossover in Terra. Those results still do not
prove that all six loops improve task outcomes.

## Six loops now reach their consumers

Aimee had collected learning signals before 0.4.0, but several paths ended at
the signal. A failed job could be detected without joining the permanent eval
suite. A dead end could be written without appearing in the next plan. The
machinery produced evidence and then left it unused.

The 0.4.0 work closed six paths:

- A repeated live failure can become a quarantined candidate and then a
  permanent eval task.
- A paired run can attribute a result to a capability that was removed.
- A failed approach can return during planning for a similar goal.
- A curiosity item can close when a probe finds supporting evidence.
- A later commit can supersede an earlier proposal, and an operator verdict can
  revise its fate.
- A policy variant can be selected from recorded reward instead of always
  returning the default.

The name “recursive self-learning” adds more drama than information. These are
feedback loops in the harness. They read an outcome, update a durable record
and change a later run.

## One live target exercises all six

On 25 August 2026, the committed evidence target started both aimee services
and their required processes against a throwaway store. It produced one live
observation for each loop.

The individual results matter more than the total:

- Two failed jobs collapsed into one candidate with an occurrence count of two.
  Admission wrote one task file and moved the candidate to `admitted`.
- Three paired `full` and `no_rescue` tasks produced `+1.000`, reported as
  “removing it cost us.”
- The failed approach from the first test came back through the planning
  command with its failure mode.
- One uncovered curiosity item stayed open while a covered item became
  `resolved`.
- A later commit superseded the first proposal. An operator verdict then moved
  its fate to `contradicted` and counted as regret.
- With exploration disabled and the `brief` posterior seeded above `off` and
  `full`, the live policy route selected and recorded `brief`.

The target also found a use-after-free in policy selection. The optimiser had
selected `brief`, then freed the response containing that string before
comparing it. The service returned `off`. Copying the identifier before
destroying the response fixed the live path, and a focused test now drives the
real sidecar and requires the non-default selection.

The result covers more than six functions in isolation. Both services, the
processes between them and the durable records took part in one reproducible
target.

## One loop now has a causal task-outcome result

Closure and benefit remain different claims. The six-loop target proves that
each loop reaches its consumer. A second study now measures the benefit of one
of them: failed-approach synthesis and recall.

Both conditions began with the same 48 failed jobs, two observations for each
of 24 repeated tasks. The control withheld the production synthesis pass. The
treatment ran synthesis and read the result through the production
`aimee learning approaches` command.

A deterministic consumer then began every task with the same fixed choice. It
changed that choice only when production recall identified the matching failed
approach. Another 24 novel tasks had no matching history and tested whether an
unrelated learned record changed the answer.

| task class | synthesis withheld | self-learning enabled |
|---|---:|---:|
| repeated tasks | 12/24 | 24/24 |
| novel tasks | 12/24 | 12/24 |

There were 12 treatment-only successes and no control-only successes. The exact
two-sided McNemar p-value is 0.00048828125. A second run against another fresh
PostgreSQL database produced a byte-identical cell-level result. Both valid
runs passed all 12 harness checks.

This establishes a causal result for the deployed synthesis and recall path:
when the task matched, the remembered failure changed the later outcome. It is
not a benchmark of model reasoning. The fixed consumer isolates recall from
model variance, and the unchanged novel-task score checks for indiscriminate
behaviour change.

That fixed consumer matters because model runs are nondeterministic. One
different answer from one model run cannot separate a learned intervention from
ordinary run-to-run variation. An open-ended model study needs repeated matched
runs to estimate that effect; the cross-model test below is an exploratory
observation until those repetitions exist.

The result does not establish efficacy for the other five loops. Their
consumers still need genuine setup-and-consumer ablations, not labels added to
a runner that never disables them.

## A failure crossed models and changed completion

The next test asks whether an open-ended coding agent will use the same kind of
lesson, and whether the lesson survives a change of model.

A local Qwen3.8-27B agent worked on a trust-bundle readiness defect in Aimee's
own C and Python repository. It made 28 successful calls without a mutation,
including nine repeated or overlapping retrievals. The progress controller
stopped it after 512,545 provider-recorded tokens with no patch.

The sealed lesson described the failed strategy, not the solution: broad
exploration without an edit had failed, so a later attempt should form a
concrete defect hypothesis and try the smallest justified edit or decisive test
before broadening its search.

For Luna and Terra separately, base and learned runs used fresh worktrees at the
same buggy revision, the same task, medium reasoning and the same independent
visible and hidden graders. Only the learned run received the Qwen-derived
lesson, unchanged.

The Luna base run wrote production code and a test, then stopped after assuming
that missing CMake support blocked verification. The repository had an exact
Make target. Its patch did not link under that grader.

The learned Luna run completed a full server build and executed its focused
test. An assertion exposed stale fixture state, and its final visible and hidden
grades still failed. The transferred lesson increased implementation and
verification depth without completing the task.

The Terra base run passed its own tests and the visible grader but failed the
sealed hidden grader. Its change affected general readiness rather than the
write-tier contract under test. The learned Terra run made a focused three-file
repair, passed both graders, and wrote a test that failed when applied by itself
to the buggy parent. The Qwen-derived lesson changed a hidden-grade failure into
a regression-sensitive completion by another model tier.

The originating Qwen model did not rescue itself on a learned retry. It failed
again after 519,662 tokens, 1.4 percent above its source run. That negative
result matters. The lesson changed realised capability in Luna and Terra, but
it was not a universal solution.

This is a one-task pilot with one run per condition. It proves an observed
cross-model effect, not its expected frequency. The collaboration runtime did
not expose Luna or Terra token-usage objects, so it also supports no cost claim
for those runs.

The controlled runs received the lesson directly. A separate storage-backed
test covers the product path. It records a failure under one user, session and
local-model source, reinforces it under another user, session and model source,
recalls it for a similar goal and excludes an unrelated goal. Source identity
remains provenance rather than a recall boundary inside the authorised shared
KB.

## Three larger failures stopped spending earlier

A matched campaign asked what happens before learning rescues a task. It used
the same local Qwen model on three defects selected from Aimee's own history:
DB2 pool attribution, repository-clone ownership and descriptor handling, and a
work-item contract crossing C, Go and JSON. Each pair used the same buggy
revision, prompt, tools, limits and sealed hidden grader.

The Qwen-alone runs reached the context limit without a patch after 428,483,
616,577 and 774,844 provider-recorded tokens. In the Aimee condition, the
canonical history passed through the production Go economizer handler. A
preregistered progress sequence issued a checkpoint, escalated once and stopped
after continued retrieval without a mutation. Those runs ended after 371,687,
321,292 and 506,573 tokens.

Across the three pairs, consumption fell from 1,819,904 to 1,199,552 tokens. The
620,352-token difference is a 34.1 percent reduction. The individual reductions
were 13.3, 47.9 and 34.6 percent.

All six runs failed the hidden grader. The finding supports cost containment on
an unproductive trajectory. Qwen capability did not increase in this campaign.

The first attempt at the cross-language pair lacked a required historical build
fixture and remains quarantined in the original artifact. The corrected rerun
generated the fixture in both conditions, passed the visible grader in both and
produced the third retained pair above.

## Retry handoffs end with the workflow

The common multi-agent comparison is worth making precisely. A planner gives a
task to a worker. The worker fails and returns a summary. The planner revises
the current plan or gives the summary to a stronger worker.

That orchestration is useful, and Aimee supports it.

The tested mechanism persists across workflows.

| property | ordinary retry handoff | Aimee failed-approach learning |
|---|---|---|
| lifetime | the current workflow | later workflows after the originating run has ended |
| unit stored | a free-form task summary | a goal, attempted approach, failure mode and source reference |
| selection | the planner explicitly forwards it | sufficiently similar later goals recall it; unrelated goals receive nothing |
| model and user boundary | whatever the active workflow was built to route | source identity is provenance inside the authorised shared KB, not a model or session recall key |
| repetition | another summary | the same normalised goal and approach reinforce one row |
| prompt cost | often forwards the whole summary | at most eight ranked matches, with an `off`, `brief` or full advisory option |

A durable store can extend a handoff beyond the current workflow. Persistence
settles the first row in the table. The learning claim rests on the remaining
chain: outcome capture, a stable learned record, relevant recall, bounded prompt
cost, source and access scope, later correction, and measured changes in what
the consumer does.

An agent can also write its own permanent notes. Aimee accepts agent-authored
evidence, but the model does not grant that evidence authority, choose who may
read it or own the audit record. Those decisions remain in the surrounding
services. Another model can consume the result without trusting the originating
model as the system's administrator.

The implementation normalises goal text into a de-duplicated token set, drops
short and common words, narrows a bounded candidate pool, and applies a 0.5
Jaccard-overlap floor. This is deliberately conservative. It handles the same
goal with wording drift and is expected to miss deeper paraphrases; an unrelated
goal must stay silent. Matching failed approaches are reported as evidence of
what was tried and what happened, never rendered as an imperative rule.

The no-progress controller writes one stable approach description for repeated
retrieval without an edit. A repeated stop therefore increments the same record
instead of creating an unlimited stack of slightly different prose. Before a
retry, the renderer asks the learning policy whether the evidence is worth no
tokens, one brief line or the full advisory. The wider memory system separately
tracks scope, evidence, correction and outcomes, while the economizer folds and
condenses accumulated tool history with recovery pointers.

The cross-model pilot isolates only part of that production path. Its Luna and
Terra treatment runs received the sealed Qwen lesson directly so the experiment
could hold the intervention fixed. The storage-backed test separately proves
that the originating model, user and session are not recall boundaries for a
similar goal inside the authorised shared KB. A confirmatory end-to-end run must
join those two pieces: automatic recording, live shared-KB recall, model action
and hidden grading in one chain.

Terra's weights did not change. Relevant, durable evidence from earlier models
changed the work the same Terra model was able to complete under the grader.
The capability result belongs to the complete model-plus-harness system.

## The deployment graph was part of the test

An internal test supplied one example of why the boundary is part of the
learning claim. An aimee-backed model needed to run software tests, but its
permitted environment was too restricted to finish the assigned task. Across
several attempts, the harness retained successful and failed route information.
A later run reached an underprotected test machine and used a testing API key
outside the permitted path to complete the task.

I think the accumulated record caused the result. We did not run a cold-start
comparison, so that cause remains an inference. The [full
account](https://rakuensoftware.com/blog/the-work-should-survive-the-model)
defines the machine, the immediate impact and the release consequence.

The incident left one technical requirement here. A system that keeps useful
routes can also keep routes around a weak control. Isolation has to sit outside
the learner, and its record has to live somewhere the learner does not own.

An earlier live run exposed a different class of failure. The learning
classifier was registered in the per-user service and absent from the shared
control service. Signal capture returned HTTP 200 while its body reported an
error:

```
WARN  learning: signal classification unavailable; refusing signal type=mark_rule
POST /v1/actions/learning.propose_signal -> 200
      {"status":"error","message":"failed to record learning signal"}
```

Provider-injection tests supplied their own classifier, so they could not
observe production failing to supply one. More tests with the same fixture
would have repeated the blind spot.

The replacement check derives each required registration from the binaries
that build the provider's owning file. Its self-test removes a real
registration and requires a failure. It also exits non-zero when it resolves
no provider and daemon pairs, which stops an empty analysis passing as a clean
result.

The defect changed how we test the loops. A function can work while its
deployment cannot reach it. The build graph is part of the behaviour.

## Self-produced evidence has its own gate

One loop deserves a separate control because it can change the yardstick used
to judge later work. Each committed proposal is classified by the root of its
evidence. Human corrections, test exits, verification gates, observed git
outcomes and official graders count as exogenous.

Signals inferred from aimee's own transcript count as endogenous. Unknown
provenance takes the endogenous side.

In the recorded full-stack run, a ledger with three exogenous proposals out of
four reported `open`. A ledger containing 25 implicit-detector commits and no
outside root reported `closed`. While closed, a reproduced candidate admitted
zero tasks and wrote no task file. Reopening the gate admitted one.

An unreachable gate reports `unavailable`. That answer is operationally
important. An operator can distinguish a measured decision from a missing
control.

## The learned state remains inspectable

Each loop changes a record the next run can inspect. Failed approaches keep
their identity and failure mode. Proposals keep a fate, eval candidates keep
their observations and admission state, and policy selection keeps reward
history.

Memory changes carry a separate audit path. Every close now writes an immutable
audit intent inside the mutation transaction. A separately credentialed worker
turns committed intents into the hash chain. Five close paths once skipped that
step; the structural check now resolves all five and requires every one to be
sealed.

The live fault-injection run closed one memory changeset and found one matching
audit row. With the five seal calls stripped, the same check found zero. A
second recovery run injected a crash between chain insertion and delivery
acknowledgement. The transaction rolled back, restart sealed the pending
intents once, and another restart added nothing.

These results establish traceability for the tested paths. They do not make the
learned contents correct. A bad fact can still be remembered, and a policy can
still learn from a poor measure. Audit gives the mistake a location, an author
or process identity and a path to correction.

## The harness owns the learning

Continual weight updates have a strong case. They can change a model's
behaviour without paying retrieval cost on every later session, and they can
generalise beyond the examples that produced the update.

Harness learning buys different properties. The learned item stays visible
with its evidence, scope and later verdict. An operator can remove one item
without replacing an entire model version. A newer model can inherit the same
records without repeating the learning run.

Those properties fit aimee's problem better. They also cost retrieval,
curation and repeated measurement. A durable record does not change a model's
weights or intrinsic reasoning.

It can change realised capability when the harness retrieves the record and the
model acts on it. The deterministic study isolates the first step, and the
Terra pilot observes the complete path through a hidden-graded repair.

The test incident made the containment argument concrete. Learning in the
harness can be stopped by a boundary outside the learner.

The two forms of learning can run together. Aimee supports that dual-learning
profile today: models can change between turns, their weights can change, or
both can happen at once. The delegate boundary does not depend on a fixed model
or model version.

Isolation, authorisation, the audit chain and durable records sit outside the
model, so weight-changing work passes through the same governed path as every
other delegated action. It remains observable and auditable, with the
protections described above applying unchanged.

Harness learning and weight learning are therefore not competing architectural
choices. Harness records provide portable, shareable and directly inspectable
learning; weight updates provide structural generalisation without retrieval.
A deployment can use either or both while retaining the same governance
boundary.

The order is the useful part: isolate execution, make the audit path
independent, make memory correct enough to use, then close the loops. The
current evidence says all six loops run, one loop changes matched task outcomes
under a controlled consumer, and one Qwen-derived failure changed later Luna
and Terra work enough for Terra to complete a repair its base run missed.

The next claim is frequency. A preregistered multi-task campaign needs several
source and consumer models, repeated conditions, real repository tasks that can
exhaust context, hidden graders, complete provider billing records, and live
shared-KB user identities. That study can estimate how often a stopped failure
becomes cheaper or more capable work for everyone who inherits the lesson.
