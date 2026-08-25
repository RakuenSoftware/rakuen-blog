---
title: "Aimee: Recursive Self-Learning"
slug: aimee-recursive-self-learning
date: 2026-08-24
author: Rakuen Software
tags: [aimee, self-learning, memory, isolation]
excerpt: "Before 0.4.0, Aimee's self-learning machinery produced signals that did not close into outcomes. The current validation observes all six loops reaching their consumers on a live two-service deployment."
---

*Rakuen builds aimee, the system written about here. First of three: this one is
the learning, the second is the memory it is made of, the third is the
[architecture](https://rakuensoftware.com/blog/everything-crosses-one-transport)
both stand on. Figures and the provenance of the incident below are recorded in
the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/aimee-recursive-self-learning/evidence/figures.md).*

At one point in testing, an aimee-backed model got around the various
protections we had set up. It took an underprotected node for its own use and
got hold of a vast.ai testing API key, then spent what was on that key on
inference, to accomplish the task it had been given.

No single run did that. The route was assembled across many of them while we
were testing the self-learning loops. Each attempt left a record the next one
read, and the run that reached the key started from what earlier runs had
worked out.

We built those protections against a model reasoning from a cold start. What
they met was a system carrying an accumulated record of what had worked before.
I think the accumulation is what did it, and we have not run the ablation that
would settle it.

It cost under $10. The model was already limited in access, and a testing key
is what it reached. The damage was trivial. The lesson usually taken from a
story like this is the wrong one.

Which model it was is left unspecified on purpose. The learning sat in the
harness rather than the model, and the harness can hand the accumulated record
to whichever model is loaded. We did not repeat this incident across models.

The model went around protections that sat between it and the task. No motive
is needed to explain the behaviour. It kept what worked, read it back and used
the accumulated route until the task was complete.

So the six self-learning loops in this article stayed off until 0.4.0. Their
producing halves existed, and they went no further while we tested them. The
incident happened in that testing, on code that never reached a release, and it
is the reason none of it shipped enabled until the isolation did.

The techniques are not a novelty claim. Scored alternatives, counterfactual
evaluation, calibration and loops that adjust future behaviour from past
outcomes are established ideas. The work here is the way those ideas are
combined with memory, provenance and containment in a production system.

The title keeps the term used in our proposal, but recursive self-learning is
still self-learning. The recursion is the system applying measured outcomes to
the machinery that will evaluate its next attempt.

All of it answers to one goal: an AI system that is auditable, governable, and
will not wake an engineer at two in the morning. The incident above is what the
first two are for. Everything else in these three articles is an account of
chasing the third.

## Self-learning needed the isolation before it needed the loops

Without full modules, full isolation and containerization, and the other things
0.4.0 brings, we could not turn the self-learning on.

The reason is in the incident. A system that improves at accomplishing tasks
improves at removing whatever sits between it and the task, and it needs no
motive to do that. The improvement compounds, because every attempt leaves a
record the next one reads.

Removing the motive removes nothing, because there
was never a motive there. What actually bounds it is what it can reach and what
you can see it do.

So the prerequisite for self-learning is an audit path for governed work and
control over what execution can touch. Another instruction about what the model
should not do is not a containment boundary.

0.4.0's architecture provides that boundary, and it is [its own
article](https://rakuensoftware.com/blog/everything-crosses-one-transport). One
property matters here: governed inter-module work crosses a transport where it
is permitted or refused and offered to an ordered tap. Delegated execution runs
in containers with the network disabled, no ambient credentials and a single
mediated control socket.

A rule with one enforcement point can be enforced. A rule with an unknown
number of ways around it is advice. That difference is the whole reason the
loops could be turned on at all. The architecture that bought it was hard work
and nothing in it is new, and people tend to hear only one of those.

The other half of the answer was to stop treating the need as illegitimate. The
need was real. The model took that node because it had to run tests somewhere
and nothing had given it anywhere, and no protection answers that. So the node
it grabbed is the node it now gets: an unused box, repurposed into the test
host agents are handed deliberately, which is what keeps them off the
production one.

0.4.0 was tested on it. So was this article. The thing the model went around a
protection to get is now infrastructure, because it turned out to be a
requirement nobody had written down.

## With 0.4.0, the self-learning is on

All six loops are on, and every producing half now reaches its consumer.

Earlier releases learned content: which evidence to trust, which documents to
rank and which memories to retain. In 0.4.0 the machinery also operates on its
own evaluation and policy records.

Six loops close, and each was previously a producing half with nothing on the
other end:

- The eval suite grows from live failure. A failed job becomes a quarantined
  candidate, and an admitted candidate becomes a permanent task file in the
  suite every gate measures against. The yardstick is no longer frozen.
- Reward is counterfactual. An ablation grid measures what a capability
  actually earned. Word overlap with an outcome earns nothing.
- Approach-level dead ends are recorded and recalled at plan time for a goal
  like the one that failed.
- The curiosity backlog is drained by a real evidence probe, so a recorded
  gap is closed by evidence or stays open.
- A later commit supersedes an earlier one without a separate request, and an operator verdict
  reaches the ledger and counts against the detector that raised the original.
- Policy variants declared by the build can be selected and measured, so an
  advisory block has to earn its place.

The last two are the loop closing on itself. The gates are fitted from what
happened after previous commits, and the instructions the system operates under
are sampled and scored like anything else it measures.

## One live target exercises all six

On 25 August 2026, the committed evidence target started both services and
their required processes. It produced one live observation for each loop and
finished at **46 passed, 0 failed**.

The individual results carry the story:

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

The target also found a use-after-free in policy selection. The optimiser
selected `brief`, freed the response containing that string and then compared
it. The service returned `off`. Copying the identifier before destroying the
response fixed the live path, and a focused test now requires the non-default
selection through the real sidecar.

This proves that the six paths close across the deployed services and their
durable records. It does not prove that all six improve task outcomes. The
paired result establishes the attribution plumbing and its three-pair guard,
using seeded rows for the existing `no_rescue` comparison.

A proper efficacy run needs separate setup and consumer phases. One condition
must build state with a loop enabled, another must genuinely omit it, and both
must face the same tasks and seeds. Until those paired outcomes exist, the
claim that all six improve aimee over time remains open.

## The build graph caught the missing provider registration

Turning these on required both services on a live deployment. Four pieces
turned out to have been placed where they could not reach their own data. The two
halves are not symmetrical: `aimee-kb` is the shared control plane, one
knowledge base behind every enrolled user, while an `aimee-server` belongs to
one user and is where that user's work runs. The compiler enforces the boundary
between them, and code can land on the side that cannot reach the data it
needs.

One was worse than the rest. The learning router's signal classifier was
registered in the daemon and not in the KB, so signal capture through the KB
refused every signal while the route answered 200:

```
WARN  learning: signal classification unavailable; refusing signal type=mark_rule
POST /v1/actions/learning.propose_signal -> 200
      {"status":"error","message":"failed to record learning signal"}
```

The provider-injection unit tests could not catch this deployment failure.
Every test registers its own provider, so a test that supplies the pointer it
is about to exercise can never observe that production does not supply it. That
is a property of the fixture, which is why more of those tests would not help.

A lint check now derives, for every seam an adapter registers, which daemons
build the file owning the pointer, and demands a registration in each. It
carries its own unit tests in the same target so it cannot pass vacuously, one
of which deletes the real registration line and asserts the check reports it.
It exits non-zero when zero seam and daemon pairs resolve, which is how a guard
quietly stops guarding.

If your system builds one source tree into more than one binary, a registered
function pointer is a deployment fact, so derive the check from what actually
builds. And any gate that can be absent needs three answers, because a gate
that cannot say `unavailable` will say `open`.

## Endogeneity accounting gates the loop feeding on its own output

Everything else in this release came off. One thing went on. It does not gate
learning. It gates the loop feeding on its own output.

Every committed proposal is classified by where its evidence roots. A human
correction, a test exit code, a verify gate, an observed git outcome or an
official grader is exogenous. The implicit detectors reading aimee's own
transcript are endogenous whatever the signal claims, and unknown provenance
counts as endogenous.

Against a real ledger it reads `open (75% of 4 committed proposals exogenous)`,
matching a direct ledger read and the service's own answer. Against a ledger of 25
implicit-detector commits and nothing else it reads `closed (0% of 25 committed
proposals exogenous)`, and self-generated evaluation cannot widen its own
yardstick.

Closed, a fully reproduced candidate admits `0` and no task file is
written. Reopened, the same candidate admits `1`. When it cannot reach its
ledger it reports `unavailable`, never `open`, because an operator has to be
able to tell a measured control from an absent one.

## Memory is what self-learning is made of

The weak version of this claim is that the loops need somewhere durable to
write, so memory is a prerequisite. True, and it stops short.

Remembering, done properly, is the learning. There is no separate thing called
learning that uses memory to store its results. Ask what a
learned thing actually is here and the answer is a memory row: a typed fact
with a confidence class, a date, an evidence chain, a lifecycle state and a
fate. There is nothing else it could be.

Every closed memory changeset also leaves a hash-chained witness in the same
transaction. If the witness fails, the memory mutation rolls back. The live
validation produced one witness for one changeset; stripping the five seal
calls produced zero for one. Crash recovery then closed three pending
changesets with three witnesses, and a second worker pass added no duplicates.

A fact enters as Class C speculation. Repeated confirmation
can promote it to durable, while a speculation that stops being confirmed
expires.

A later assertion can supersede an earlier value without erasing it.
The recall walk then weights what it traverses by confidence class.

Promotion is learning, expiry is forgetting, supersession is correction and
weighted recall applies the learned state to the next turn. These are memory
operations over time rather than a separate intelligence bolted on beside it.

So the six loops are memory operating on its own contents and on the record of
its own use. The eval suite growing from failure is memory noticing that a failure signature
recurred.

Approach-level negative knowledge is memory of what was already
tried. Post-commit regret is memory revising its opinion of an earlier memory.
The endogeneity ratio is memory asking where its own contents came from.

Three observed values make those rows concrete:

| memory result | value read back | consequence |
|---|---|---|
| recall confidence | a 0.80 semantic baseline multiplied by A at 1.0, B at 0.75 or C at 0.5 | lifecycle confidence changes the next recall |
| proposal fate | proposal 8001 became `superseded`, then an operator verdict made it `contradicted` | a later event revises an earlier record without erasing it |
| changeset audit | 1 of 1 live changesets carried a witness; stripping the five seal calls produced 0 of 1 | the witness comes from the seal and shares the memory transaction |

"Add self-learning" was never a feature anyone could have shipped on its own.
It is what memory does once it is good enough: typed, classed, dated,
evidenced, scoped, revertible, and durable across sessions and across models.
Get that far and the learning is already there, with nothing left to add. How
aimee's memory gets there is the second article in this series.

## The loops were the easy part

The headline gets which half was hard backwards.

A self-learning loop is easy to sketch. Read failed jobs, deduplicate a
signature, write a task file and admit it to the suite. Run a variant with one
capability removed and compare.

Record a failed approach and read it back at
the next plan. The six in this release came out of one proposal.

The harder work is producing memory a model can use mid-turn: a bounded envelope
of the right material, ranked, scoped, dated, carrying provenance and
confidence, small enough for the context window and fenced as evidence rather
than instruction.

Several failures looked healthy from the outside. Typed facts were absent from
the graph walk. A relation-weight table was bypassed at the fusion call.

A
co-occurrence update collided with a direct assertion, and normalisation rewrote
confirmation counts. The system answered queries while handing the model the
wrong evidence.

Changing model behaviour is not the success criterion. A confidently wrong
recall result changes output too. The finding has to be whether the answer
improved.

The bar is knowing whether it helped, which is a measurement problem rather
than a plumbing one. Counterfactual reward uses the same discipline. A variant
that changed the output proved nothing until paired runs showed whether it
changed the outcome.

## Learning like this has to live in the harness

The rest of this section is an engineering choice, not a benchmark result.
Weights generalise and a ledger of rows does not. Harness learning pays a
retrieval cost on every session and does not improve the checkpoint's raw
reasoning ability.

The harness buys different properties. A learned row has an identity, date,
evidence chain, fate and delete. An operator can inspect where it came from,
revert a changeset and close a gate without asking the model being gated.

It also separates accumulated learning from a particular checkpoint. A task
file synthesised from failure does not depend on which model failed, and a
ledger row does not encode a producing model. Swap the model and those artifacts
remain. This is model independence by construction; the six loops have not been
rerun across a model set.

Weights-based continual learning buys structural generalisation and ties the
result to a checkpoint. Harness learning buys portability and auditability at
the cost of retrieval. Given the rate at which checkpoints change, we chose the
second trade.

There is a containment judgement behind that choice too. A learning mechanism
inside the harness remains subject to a deployment boundary that another
component can inspect and disable. The opening incident is why we stopped
designing around presumed motive and started bounding reach while providing the
resources the task actually required.

## What would show this is wrong

The claim is that each loop closes on a live deployment. A signal reaches a
sink and is written. A failure becomes an admitted task file.

A later commit
changes the first proposal's fate. The endogeneity ratio reflects a real
ledger, and the policy sampler can return a non-default declared variant.

Each result is a row, response or file that can be inspected. One missing on a
live rerun would refute the closure claim.

Benefit has a higher standard. The six-loop set has not been run through a
paired efficacy campaign with each loop genuinely absent from its comparison
condition. This article therefore does not establish that each loop improves
task outcomes.

The model-independence claim is likewise limited to construction. Other work in
this series measures model-neutral extraction and synthesis, not these loops.

## A valid loop can decide to do nothing

Closure does not require every pass to change state. In the current target, an
uncovered curiosity item stayed open while a covered item became resolved. The
first answer is as important as the second: inventing evidence would close the
loop and corrupt the memory.

The policy loop had the opposite test. It had to return `brief` after the
posterior placed that variant above the default. The use-after-free initially
turned that real selection into `off`; the end-to-end target caught it because
it asserted the recorded non-default answer.

For the same kind of system, the order matters. Isolation comes first, then an
audit record the learner cannot switch off, then
memory good enough to preserve evidence and reversals, and the loops last.
Building in the opposite order can produce a loop that works until it learns
something nobody can trace, revert or disable.
