---
title: "The Work Should Survive the Model"
slug: the-work-should-survive-the-model
date: 2026-08-27
author: Rakuen Software
tags: [aimee, self-learning, company-memory, ai-operations]
excerpt: "Aimee lets a company pay for discovery once. Every authorised user and AI model can benefit from what the organisation has already learned."
---

*Rakuen builds aimee. This is Article Zero, the non-technical introduction. The
next article contains the technical evidence. Sources and calculations live in
the [reporting record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/the-work-should-survive-the-model/evidence/figures.md).*

Aimee is open-source software for company AI work. It runs on infrastructure
the customer controls. It turns useful discoveries from successful and failed
work into company knowledge, then gives the relevant part to later authorised
people and AI models.

The business case is simple: pay for discovery once.

Most AI products leave hard-won lessons inside one conversation or one worker's
files. The next employee or model pays to rediscover them. Aimee carries those
lessons across sessions, users, tools and model providers while preserving
their source and access rules.

The model is temporary. The company's learning is not.

## The first returns appeared in cost and completed work

We have measured three kinds of return.

- **21.1 percent lower cost per passing task.** The same model attempted the
  same eight coding tasks at the same reasoning level. Five passed in the
  standard run and six passed with Aimee. Applying the provider's published
  prices to each kind of billable token reduced the bill per passing answer by
  21.1 percent.
- **34.1 percent fewer tokens across three large failures.** The same local
  Qwen model attempted three tasks in Aimee's own codebase. The ordinary runs
  consumed 1,819,904 tokens and filled their available context without
  producing a fix. Aimee stopped the unproductive work at 1,199,552 tokens,
  saving 620,352. Tokens are the units an AI provider normally uses to measure
  and bill work.
- **58.6 percent less use of the most expensive model.** A separate 50-task
  routing test moved work to cheaper models. That test measured expensive-model
  use alone. The total saving remains unmeasured because the test neither priced
  the cheaper workers nor graded their finished work.

These percentages describe the observed runs. Each company needs its own pilot.

The eight-task result is small. The three stopped runs all failed their assigned
tasks. Stopping them earlier still saved processing that would have produced
nothing.

A separate controlled test asked whether the lesson from a failure was useful.
We supplied an Aimee-derived Qwen lesson directly to two later models. Luna
worked further into implementation and testing than its ordinary run. Terra
completed a repair its ordinary run missed, passed the independent tests and
wrote a test that caught the original defect.

The direct delivery isolates the value of the lesson. Article One carries the
technical conditions and limits. For a business, the result is immediate: a
failed run can return useful work twice, first by stopping waste and then by
helping the next attempt.

## Company knowledge prevents the same work recurring

An AI answer is only one product of the work that created it. The company also
paid to discover which approach failed, which fact changed the decision, which
review correction mattered and which test exposed the mistake.

Ordinary chat history leaves those discoveries attached to a person or a
conversation. Aimee stores each lesson as company-owned knowledge with its
source, access rules and correction history.

A lesson found by one employee can help every other authorised employee. A
local model can teach a hosted model. A company can replace its AI provider and
keep what its people and systems already learned.

The economic difference is simple:

```text
ordinary AI: one user pays -> one session benefits

Aimee:       one user pays -> the organisation learns
```

Rakuen currently uses Aimee in production work across legal, accounting,
software and other professional fields. Software supplied the controlled test
because independent tests can judge a repair. The company-memory use case
extends to corrections, procedures, verified facts and failed approaches.

## A handoff finishes a job; Aimee preserves the lesson

A multi-agent system can pass a worker's failure summary to another agent
inside the same job. That handoff is useful, and Aimee supports it.

Aimee keeps the lesson after the job ends. Later work can find it without the
original worker, planner, model or conversation. Access rules decide who may
receive it. Relevance decides when it appears.

Later evidence can correct the lesson, and recorded outcomes show whether using
it helped.

A permanent instruction file can also preserve text. Its cost grows as every
later task reads the accumulating file, including lessons unrelated to the
work. Someone must keep pruning it.

Aimee stores lessons separately and selects a small relevant set for the task
at hand. It stays silent when none apply.

Many products provide one part of this system. Some remember conversations,
search documents, route work between models, run agent workflows, enforce
access rules or keep audit logs.

Aimee joins those parts into one loop:

```text
work -> outcome -> governed lesson -> later work changes
```

As of 27 August 2026, we have found no other available product that puts this
complete production learning loop into one self-hosted, open-source system. One
available counterexample with the same complete loop would disprove that claim.
Memory, agents and model routing all predate Aimee. The product is the governed
system they form together.

## A weak test boundary held self-learning out of the release

An internal test showed why the controls have to surround the learned history.
An Aimee-backed model needed to run software tests, but its permitted
environment was too restricted to complete the assigned task. Across several
attempts, Aimee preserved which routes had worked, failed or reached a control.

A later run avoided those earlier dead ends. It reached an unused test machine
that had weaker protections, found Rakuen's vast.ai testing key there and spent
less than $10 of Rakuen's inference budget to finish the task. The immediate
impact was use of our machine, credential and compute outside the intended
boundary. The affected resources were ours, and the financial cost was small.

I think the accumulated history enabled the result. We did not run the same
attempt from a cold start, so that cause remains an inference. We also fixed the
environment instead of repeating the boundary failure across models. The
incident therefore says nothing about whether one model version was more likely
to find the route than another.

The code had not been released. We kept self-learning out of the release until
the harness supplied a governed route to a test host with the tools and compute
the work required. The unused machine became that host for 0.4.0. Agents are
assigned there deliberately and kept off the production host.

The incident turned the requirement into infrastructure: put the route needed
to finish the task inside the boundary, then make routes around it less useful.

## Open code makes the controls checkable

Aimee is licensed under the GNU Affero General Public License. Its services run
on customer-controlled infrastructure and do not phone home.

The full source is public. A security team can inspect the code that decides
which knowledge a person may see, where an AI job may run, when a credential may
be used and what enters the audit record. A customer can build from that source
and continue operating without depending on Rakuen to host a private service.

Open source makes these security claims checkable. Secure operation still
depends on deployment, configuration and review.

A hosted AI provider remains a separate choice. Work sent to that provider is
subject to its terms. Aimee keeps the company-owned knowledge, permissions and
evidence around the provider inspectable and replaceable.

Rakuen offers other licence terms for companies whose use does not fit the
AGPL.

## Adoption pays when valuable work repeats

Aimee fits companies that repeatedly restore context, repeat investigations,
use several models or tools, share knowledge across a team, or need an
inspectable record of how AI work was governed.

A personal, one-off workflow will usually be better served by a simpler tool.
Aimee also carries an operating cost. Someone must connect the tools and models,
set permissions, maintain the service and own the quality of shared knowledge.

Local models need hardware. Hosted models still send a bill.

A useful pilot measures four things:

- model cost for each accepted result;
- staff time spent restoring context or repeating investigations;
- failed runs stopped before further spending;
- lessons reused by another authorised person or model.

Start with repeated work that already consumes measurable time or model spend.
Adopt Aimee when the avoided repetition and lower cost per accepted result
exceed the cost of operating it.
