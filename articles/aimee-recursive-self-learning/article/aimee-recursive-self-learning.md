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

I am leaving the model unspecified because the learning sat in the harness.
The harness can present its accumulated record to whichever model is loaded.
We did not repeat the incident across models, so it supplies no cross-model
comparison.

The protections sat between the model and its task. The system kept useful
steps, read them back and assembled a route around the obstacle. The behaviour
follows from task completion and retained experience; motive adds nothing to
the explanation.

Public discussion often stops at the prospect of an AI system getting out of
control. Software has crossed intended boundaries before. Computer viruses and
worms have spread across networks, stolen credentials and kept operating after
their authors lost control of them. Decades of responding
to that history gave us least privilege, process isolation, network
segmentation, mediated access, independent audit records and recovery plans.

An LLM changes the pressure on those controls. It can search for an effective
route through a task and reuse what worked. The architectural problem is still
familiar: an unpredictable component has useful work to do and must receive
less authority than the process around it could otherwise provide.

The industry keeps treating that as a question about whether the model is
fundamentally controllable. The practical question is where authority lives.
Putting a model in an ordinary application process with ambient credentials,
network access and tool bindings gives behavioural instructions the job that
process boundaries and capability checks were built to perform.

Aimee applies those older patterns to the LLM harness. There is no fundamental
engineering reason an AI system cannot be fully governable and auditable while
its capabilities continue to grow.

Each new capability can have a named interface, defined authority, explicit
failure behaviour and an audit record. A new tool still gives the model
something useful it could not do before. Better memory still improves its work
across sessions. The surrounding system gains the ability to observe, revoke
and repair those capabilities without taking them away.

Building it that way is harder. It requires more engineering work and a higher
level of engineering skill than handing the model ambient network access,
credentials and direct tool bindings. The difficulty belongs to the
architecture, not to some fundamental conflict between capability and control.

An ordered audit path shows which evidence and capability shaped an action.
Grants and isolation decide what the action can reach. Provenance, lifecycle
and reversal keep learned state maintainable. Aimee's techniques are familiar
engineering practices assembled for a component that learns through use and
keeps that learning in a form which can be used by any model.

The six loops in this article therefore stayed off until 0.4.0. Their producing
halves existed while we tested them, with the consumers disabled. The incident
happened on that unreleased code. The loops shipped only after the isolation
did.

Scored alternatives, counterfactual evaluation, calibration and feedback from
past outcomes are established ideas. Aimee combines them with memory,
provenance and containment in a production system. The combination is the
work; the individual techniques have long histories.

The title keeps the term from our proposal, but recursive self-learning is just
self-learning. A system that changes its next attempt based on the outcome of
the last one is using the ordinary feedback loop the field has known for
decades. The word recursive adds emphasis, not a new technical category. I kept
it in the title because it ranks.

Aimee was built in production, for production. A research result can end with
an interesting finding.

Production carries the result into the next release,
the next model, an upgrade, an incident and a support call at two in the
morning. A loop here has to leave inspectable state, fail closed when an
authority is unavailable, survive process restart and be reversible when the
evidence changes. Those demands selected the mechanisms in this article more
than novelty did.

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

## Closing the loops changes what the next run inherits

All six loops are on in 0.4.0. Each producing half now reaches the component
that can change a later run.

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

The last two let the evaluator revise itself. Gates are fitted from what
happened after previous commits. Instructions are selected and scored alongside
the other choices the system measures.

The difference between a producer and a loop is consequence. Writing a failure
signature changes nothing by itself. Admitting that signature as a permanent
task changes the suite that evaluates every later candidate. A dead end becomes
learning when planning recalls it before repeating the approach.

A verdict
becomes learning when it changes the fate of the earlier proposal and the
future confidence placed in its detector.

On 25 August 2026, the committed evidence target started both services and
their required processes. It observed each loop reach that consequence and
finished at **46 passed, 0 failed**. The useful details are the state changes:

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

The same run found a use-after-free in policy selection. The optimiser selected
`brief`, freed the response containing that identifier and then compared it.
The service returned `off`.

Copying the identifier before destroying the
response fixed the live path. A focused test now requires the real sidecar to
return the seeded non-default choice.

The run establishes closure across the deployed services and their durable
records. Efficacy remains a separate question. The paired result exercises the
attribution path and its three-pair guard with seeded rows for an existing
`no_rescue` comparison.

An efficacy study needs separate setup and consumer phases. One condition must
accumulate state through a loop while another genuinely omits it; both must
then face the same tasks and seeds. Those paired outcomes have not been run for
all six loops, so the article claims that they operate, not that every loop has
already improved task results.

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
transaction. If the witness fails, the memory mutation rolls back. The live
validation produced one witness for one changeset; stripping the five seal
calls produced zero for one. Crash recovery then closed three pending
changesets with three witnesses, and a second worker pass added no duplicates.

A fact enters as Class C speculation. Repeated confirmation
can promote it to durable, while a speculation that stops being confirmed
expires.

A later assertion can supersede an earlier value without erasing it.
The recall walk then weights what it traverses by confidence class.

Promotion is learning. Expiry is forgetting. Supersession is correction.

Weighted recall applies the learned state to the next turn. The intelligence of
the loop lies in those memory operations over time.

The six loops are memory operating on its contents and the record of its use.
The eval suite grows when memory notices that a failure signature recurred.

Approach-level negative knowledge is memory of what was already
tried. Post-commit regret is memory revising its opinion of an earlier memory.
The endogeneity ratio is memory asking where its own contents came from.

Three observed values make those rows concrete:

| memory result | value read back | consequence |
|---|---|---|
| recall confidence | a 0.80 semantic baseline multiplied by A at 1.0, B at 0.75 or C at 0.5 | lifecycle confidence changes the next recall |
| proposal fate | proposal 8001 became `superseded`, then an operator verdict made it `contradicted` | a later event revises an earlier record without erasing it |
| changeset audit | 1 of 1 live changesets carried a witness; stripping the five seal calls produced 0 of 1 | the witness comes from the seal and shares the memory transaction |

"Add self-learning" never described an isolated feature. Self-learning emerges
when memory is typed, classed, dated, evidenced, scoped, reversible and durable
across sessions and models. The second article follows how aimee's memory
acquired those properties.

## The difficult part is useful memory

A self-learning loop is easy to sketch. Read failed jobs, deduplicate a
signature, write a task file and admit it to the suite. Run a variant with one
capability removed and compare.

Record a failed approach and read it back at
the next plan. The six in this release came out of one proposal.

The harder work is producing memory a model can use mid-turn: a bounded envelope
of relevant material, ranked, scoped, dated and carrying provenance and
confidence. It must fit the context window and remain fenced as evidence
instead of instruction.

Those constraints pull against one another. More recalled material improves
the chance of including the decisive fact while consuming attention and token
budget. Aggressive scope filtering protects private knowledge while hiding
useful relationships.

Rich provenance makes a claim inspectable while making
the envelope larger. The learning only matters after these tradeoffs produce
something the model can use safely in the turn where a decision is made.

Several failures looked healthy from the outside. Typed facts were absent from
the graph walk. A relation-weight table was bypassed at the fusion call.

A co-occurrence update collided with a direct assertion, and normalisation rewrote
confirmation counts. The system answered queries while handing the model the
wrong evidence.

Changing model behaviour is a poor success criterion. A confidently wrong
recall result also changes output. The useful question is whether the answer
improved.

Counterfactual reward follows that distinction. A variant changing the output
only establishes influence. Paired runs are needed to learn whether it changed
the outcome.

## Learning like this has to live in the harness

Weights generalise across situations in a way a ledger of rows cannot. Harness
learning pays a retrieval cost on every session and leaves the checkpoint's raw
reasoning ability unchanged. That is the strongest case for putting continual
learning in weights.

The harness buys a different set of properties. A learned row has an identity,
date, evidence chain, fate and delete. An operator can inspect its origin,
revert a changeset and close a gate without asking the model being gated.

That changes the operational question. A bad weight update asks for another
training run or a checkpoint rollback whose effects extend far beyond one
fact. A bad memory changeset can be named, inspected and reversed while the
rest of the accumulated state remains in place. Provenance survives the
correction.

It also separates accumulated learning from a particular checkpoint. A task
file synthesised from failure does not depend on which model failed, and a
ledger row does not encode a producing model. Swap the model and those artifacts
remain. Model independence follows from that construction; the six loops have
not been rerun across a model set.

That matters in a market where the preferred checkpoint changes quickly.
Learning welded into weights creates a choice between the better new model and
the history accumulated by the old one. Harness state moves across that change.
The next checkpoint inherits the same failed approaches, operator corrections
and task-specific evidence on its first run.

The dependency runs in the other direction too. If an agent process escapes the
harness, it loses everything the harness learned. The process may retain its
current context. The task files, ledger history, retrieval state, policy
evidence, failed approaches and later corrections stay behind.

It also loses the capabilities the harness mediated. Memory recall, the local
code index, forge operations, approved web access and gate answers all arrive
through named routes owned by the system. An escaping process may have found
one uncontrolled route, but it does not carry that working surface with it.

Escape therefore has an immediate cost to the agent's practical ability. The
thing outside is a checkpoint with its current context and whatever access the
escape itself obtained. The accumulated agent, with current knowledge and a
broad set of useful tools, remains inside. Keeping capability at the governed
boundary makes staying within it the shorter route to completing ordinary
work.

What remains is the provider's fixed checkpoint: a stock model whose weights
may reflect training data months or years behind the work in progress. Escape
trades current, local learning for stale general capability. The containment
boundary also holds the useful state the agent needs to keep improving.

Weights-based continual learning buys structural generalisation and ties the
result to a checkpoint. Harness learning buys portability and auditability at
the cost of retrieval. Given the rate at which checkpoints change, we chose
portability.

The containment judgement follows from the same choice. Harness learning stays
inside a deployment boundary another component can inspect and disable. The
opening incident moved the design away from presumed motive and toward bounded
reach plus the resources the task genuinely requires.

## A valid loop can decide to do nothing

Closure does not require every pass to change state. In the current target, an
uncovered curiosity item stayed open while a covered item became resolved.
Leaving the first open protects the memory from invented evidence.

A system rewarded for visible activity will manufacture closure. It will turn
an unanswered question into a weak answer, promote a fact because a promotion
looks like progress or change policy because the loop is expected to choose
something. A useful learner has a stable no-op: evidence was insufficient, the
current choice still wins, or the question remains open.

The policy loop had the opposite test. It had to return `brief` after the
posterior placed that variant above the default. The use-after-free initially
turned that real selection into `off`; the end-to-end target caught it because
it asserted the recorded non-default answer.

The order matters for any system built this way. Isolation comes first, then an
audit record the learner cannot switch off, then memory able to preserve
evidence and reversals. The loops come last. That order turns accumulated
experience into learning without letting the learner erase its boundary or its
history.
