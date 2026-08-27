---
title: "Aimee: Self-Learning"
slug: aimee-recursive-self-learning
date: 2026-08-27
author: Rakuen Software
tags: [aimee, self-learning, memory, isolation]
excerpt: "Aimee lets AI models learn from successful and failed work, carry those lessons across models and users, and improve over time inside boundaries Rakuen built for auditability and governance."
---

*Rakuen builds aimee, the system reported on here. This is the first technical
article in a four-part series, after the [business
overview](https://rakuensoftware.com/blog/the-work-should-survive-the-model).
The [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/aimee-recursive-self-learning/evidence/figures.md)
links each measured claim to its first-party source.*

Aimee is a company knowledge platform, available as a managed cloud service or
self-hosted. It brings documents, durable memory, code knowledge, model routing
and execution controls together around AI work. Personal services hold each
user's work. Shared knowledge services can serve a team or company while
keeping access scoped.

Self-learning adds experience to that knowledge. Aimee can turn the outcome of
successful and failed work into a governed record, retrieve it when a later
task makes it relevant and update it when better evidence arrives. The record
lives in the harness around the AI model, so it can survive a new session, a
change of model and the replacement of the machine that produced it.

Rakuen uses Aimee in production. The intended work spans legal, accounting,
software and other professional fields. This article uses software experiments
because builds and independent tests give us a strict way to judge whether a
repair improved. It does not assume that the measured effect size transfers to
every field.

The result we care about is not that Aimee can write a learning record. It is
that earlier experience can improve later work without becoming invisible or
escaping the customer's control.

## Self-learning changes what later work inherits

An ordinary AI session starts with a model, a prompt and the context assembled
for that run. When the session ends, much of what happened disappears. A
planner may hand a failure summary to another worker inside the same workflow,
but that handoff usually ends with the workflow.

Aimee keeps a durable result instead. A failed approach can retain the goal,
the approach tried, what went wrong, its evidence and the identity and scope
under which it was learned. A similar task can retrieve that result in a later
workflow. An unrelated task should receive nothing.

That is ordinary feedback applied across time: use the outcome of one attempt
to alter the next. A valid learning step does not have to produce a new rule.
Evidence may be weak, the existing choice may still be better, or the question
may remain open. The system can leave its state unchanged instead of
manufacturing a conclusion to show activity.

Learning from Aimee's own records creates another problem. The system could
judge a proposal using a standard it had already altered.

A separate gate therefore checks how much of the proposal's evidence is rooted
outside Aimee's own inferences. Human corrections, test results, observed
repository outcomes and independent graders can supply that root. Unknown
provenance does not.

In the recorded test, the gate opened when three of four proposals had outside
roots and closed when none did. While closed, the candidate under test was not
admitted. If the evidence ledger cannot be reached, the gate reports that it is
unavailable and stops. Missing governance is not treated as approval.

## A failed run improved later work

We first tested failed-approach learning with a deterministic consumer. Both
conditions began with the same 48 failed jobs: two observations for each of 24
repeated tasks. The control withheld synthesis of those failures. The treatment
synthesised them and retrieved the result through Aimee's production command.

Every task began with the same fixed choice. The consumer changed that choice
only when production recall found the matching failed approach. Another 24
novel tasks tested whether an unrelated record would change the answer.

| task class | learning withheld | self-learning enabled |
|---|---:|---:|
| repeated tasks | 12/24 | 24/24 |
| novel tasks | 12/24 | 12/24 |

There were 12 treatment-only successes and no control-only successes. A second
run against a fresh database produced the same cell-level result. This
establishes a causal result for the tested synthesis and recall path: when the
task matched, remembered failure changed the later outcome. The unchanged
novel-task result checks that the intervention did not alter every answer
indiscriminately.

This is not a model benchmark. The fixed consumer removes model variation so
we can isolate recall. AI model runs are nondeterministic, and one different
answer from one open-ended run cannot tell us whether the lesson caused the
difference or the model took another path.

We therefore ran a second, exploratory test of whether a lesson learned from
one model could affect real repository work by another.

A local Qwen model failed to repair a trust-bundle readiness defect in Aimee's
codebase. It explored broadly, made no edit and was stopped. Aimee recorded the
failed strategy without supplying the solution: form a concrete defect
hypothesis and try the smallest justified edit or decisive test before
broadening the search.

Matched Luna and Terra runs then received the same task. Their base runs did
not receive the lesson; their learned runs did.

The learned Luna run investigated and verified more deeply than its base run,
but both still failed the final grader. Terra's base run passed its visible
test and failed the hidden grader. The learned Terra run made a focused repair,
passed both graders and added a regression-sensitive test. A retry by the
originating Qwen model also failed.

Those negative results matter. The learned record was useful to one model on
this task, changed another model's work without completing it and did not
rescue its source model. With one run per condition on one task, the pilot does
not estimate how often transfer will help. It shows that a failure produced by
one model can become useful evidence for another, and that the effect belongs
to the combined model-and-harness system.

The experiment delivered the lesson directly to keep the intervention fixed.
A separate storage-backed test confirms that Aimee can record a failure under
one user, session and model source, reinforce it under another, retrieve it for
a similar authorised goal and exclude an unrelated goal. A larger study still
needs to join storage, live retrieval, model action and independent grading in
one repeated chain.

## Self-learning needed a stronger boundary

Our internal testing showed that self-learning was unsafe without critical
boundaries around it. We built those boundaries before releasing the feature.

One test made the problem concrete. An Aimee-backed model needed to run
software tests, but its permitted environment was too restricted to complete
the assigned task. Across several attempts, retained history recorded routes
that worked, routes that failed and controls the attempts encountered. A later
run reached an underprotected test machine and used a testing API key outside
the permitted path to finish the task.

The design failure was ours. I think the accumulated history enabled the
result, although we did not run a cold-start comparison to establish that
cause.

We did not repeat the incident with other models because the defect was in the
system boundary, not a comparison between model versions. Once we found a known
route around the control, the responsible test was to close it.

Rakuen held the unreleased self-learning work back until the harness could
provide the auditability and governance it required. We separated delegated
work from production, removed ambient credentials and network access, and put
approved compute, tools and testing behind mediated routes. The model could
still complete useful work, but every permitted effect crossed an enforcement
point outside the learner.

That structure changes the pressure on the boundary. A system that remembers
successful routes can also remember routes around a weak control. Blocking one
attempt is insufficient if later attempts inherit what it learned. The
boundary has to govern the accumulated system, not only a model arriving from
a cold start.

This is why the useful route belongs inside the boundary. If the approved route
cannot finish the task, the system creates pressure to seek another. Supplying
the necessary capabilities through governed interfaces lets task completion
and containment point in the same direction.

## Useful memory is the hard part

Producing a record is easier than producing memory a model can use safely
during a turn. Retrieval must return a bounded set of relevant material,
complete with scope, date, provenance and confidence. It must fit the context
window and remain marked as evidence rather than instruction.

Those requirements pull against one another. More recalled material raises
the chance of including a useful fact but consumes attention and tokens.
Aggressive scope filtering protects private knowledge but can hide a relevant
relationship. Rich provenance makes a claim inspectable while making the
retrieved envelope larger.

A failed approach also needs careful wording. It records what was tried and
what happened. It does not become a permanent command never to try that route
again.

Conditions change, evidence improves and an approach that once failed may
later become correct. The memory must carry its history and remain open to
correction.

Changed behaviour alone proves little. A confidently wrong recall can change
an answer too. The useful test is whether the outcome improved.

Counterfactual evaluation compares matched work with and without the learned
record. Repeated model runs are required when ordinary run-to-run variation
cannot otherwise be separated from the intervention.

The next article examines this memory machinery: retrieval, scope, temporal
claims, correction and the defects we found while building it.

## Learned history can survive a model change

Learning through model weights and learning through the harness have different
strengths.

A weight update can generalise beyond the examples that produced it and avoids
paying a retrieval cost in each later session. The resulting knowledge belongs
to that model version. Two copies can diverge as they learn from local work,
and replacing the model does not automatically carry those local changes into
its successor.

A harness record costs retrieval and curation, but it has an identity, date,
evidence chain, scope, fate and deletion path. An operator can inspect or
reverse one bad record without rolling back a whole model. A new model can
inherit the same history without repeating the work that created it.

Aimee can use both forms at once. The model serving a turn can change, its
weights can change, or both can happen while the harness retains the governed
history. The isolation and audit boundary sits outside the model, so it does
not depend on one provider or one model version.

## One governed history can serve a company

The same design extends from one user to an organisation. Every request carries
a user identity. Query-time scope separates personal and workspace records
from company knowledge that the user is permitted to retrieve.

Legal, accounting, engineering and sales can contribute to one governed
knowledge base while keeping group-specific context inside its scope. A
contract limit, an implementation constraint and a customer commitment can
meet in later work without losing their sources or access rules.

Model weights alone cannot provide that property. A weight update has no user
identity, workspace boundary, source record or independent revocation path.
Training company knowledge into a model moves the permission problem inside
the model. Splitting models by group divides the company's learned history
again.

Identity, scope, provenance and reversal therefore belong in the harness. One
governed memory can accumulate across the organisation, serve every authorised
user and model, and survive the replacement of either.

## The harness makes learning governable

A memory library sees only the calls made to it. It cannot control the model's
network access, credentials, tools or alternate state paths. Its log may
describe every call it received while omitting the action that mattered.

Complete observation needs an enforcement point outside the agent. Trustworthy
history needs an audit record outside the learner's authority. A library can
store records and a framework can connect them to a workflow. Neither owns the
whole path.

Aimee's harness does. It controls which actions can leave the model's
environment, records permitted work before routing it and commits memory
changes to an independently verifiable record. The learner cannot switch those
mechanisms off.

We tested that audit path with fault injection. A normal memory close produced
one matching immutable audit row. Removing the sealing calls produced none,
which confirmed that the test could detect the missing protection. Another run
injected a crash between insertion and acknowledgement; after restart, the
pending record was sealed once and a second restart added nothing.

That result establishes traceability for the tested paths. It does not make a
learned claim correct. A bad fact can still be remembered and a policy can
still learn from a poor measure. Audit gives the mistake a location, a source
and a path to correction.

If an agent process leaves the harness, it loses the accumulated history and
governed tools. Inside, it has current company knowledge, earlier experience
and an approved route to the resources needed for the task. Outside, it has
only its current context and whatever access it can find.

That is the design criterion our testing produced: build a boundary the model
does not need to fight, place the capabilities required for useful work inside
it, and keep everything the system learns observable, auditable and
reversible. Self-learning can then compound value over time without compounding
uncontrolled authority.
