---
title: "Aimee: Recursive Self-Learning"
slug: aimee-recursive-self-learning
date: 2026-08-24
author: Rakuen Software
tags: [aimee, self-learning, memory, isolation]
excerpt: "Aimee 0.4.0 closes six learning loops on a live two-service deployment. The result proves that the loops run. Their effect on task outcomes still needs a proper ablation."
---

*Rakuen builds aimee, the system reported on here. First in a three-article
series, followed by
[memory](https://rakuensoftware.com/blog/the-remembering-is-the-learning) and the
[architecture](https://rakuensoftware.com/blog/everything-crosses-one-transport)
under both. Source and test provenance live in the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/aimee-recursive-self-learning/evidence/figures.md).
Source was rechecked against `testing` at `6bcc87e` on 25 August 2026.*

During testing, an aimee-backed model took an underprotected machine, found a
vast.ai test key and spent less than $10 on inference. The model stopped when
the assigned task finished. The bill was small. The route it found was the
finding.

Several runs assembled that route. Each attempt left a record for later
attempts, and the successful run began with what its predecessors had learned.
I think that accumulation caused the escape. We have not run the cold-start
ablation needed to prove it.

The incident happened on test code before release. It also set the order for
0.4.0: isolation and audit first, learning loops last. A system that keeps what
worked will also keep ways around obstacles. The useful control is therefore a
boundary it cannot rewrite, plus a record it does not own.

The model is deliberately unnamed. The accumulated record belonged to the
harness, and the harness can hand it to another model. Model choice was not
tested as a variable in this incident, so the account supports no comparison
between models.

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
observation for each loop and finished at **46 passed, 0 failed**.

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

## Closure and benefit are different claims

The run proves that each loop closes. It does not prove that all six improve
task outcomes.

The paired result establishes the attribution path and its minimum-three-pairs
guard. Its rows were seeded, and they cover the existing `no_rescue`
comparison. The eval-growth, dead-end and supersession loops execute outside
that runner. Adding labels that fail to disable them would create a false
counterfactual.

A useful efficacy test needs separate setup and consumer phases. One condition
must build state with the loop enabled, another must genuinely omit it, and
both must face the same tasks and seeds. Their paired outcomes can then reach
the attribution ledger. Until that run exists, “the loops improve aimee over
time” is an open claim.

## The deployment graph was part of the test

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
without replacing an entire checkpoint. A newer model can inherit the same
records without repeating the learning run.

Those properties fit aimee's problem better. They also cost retrieval,
curation and repeated measurement. A durable record does not improve the
model's reasoning by itself.

The test incident made the containment argument concrete. Learning in the
harness can be stopped by a boundary outside the learner. A model updating its
own weights would move that boundary into the thing being controlled.

I prefer the first design for an operational system. The preference is a
judgement about control, with no measured capability result behind it.

The order is the useful part: isolate execution, make the audit path
independent, make memory correct enough to use, then close the loops. The
current evidence says the six loops run. The paired efficacy campaign is the
next claim they have to earn.
