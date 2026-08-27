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

Aimee is an open-source knowledge platform for company AI work, available as a
managed cloud service or self-hosted. It brings documents, code, facts,
decisions and work history into one governed knowledge base. People and AI
models can retrieve what they are authorised to use, and useful discoveries
return to the company instead of dying with a session.

The business case is simple: pay for discovery once.

Most AI products leave hard-won lessons inside one conversation or one worker's
files. The next employee or model pays to rediscover them. Aimee carries those
lessons across sessions, users, tools and model providers while preserving
their source and access rules.

The model is temporary. The company's learning is not.

## One failure can pay twice

An AI answer is only one product of the work that created it. The company also
paid to discover which approach failed, which fact changed the decision, which
review correction mattered and which test exposed the mistake.

Aimee stores those discoveries as company-owned knowledge. The original worker,
conversation and model can disappear. Later authorised work can still retrieve
the lesson, see where it came from and correct it when the evidence changes.

The first business results were:

- **21.1 percent lower cost per completed task.**
- **34.1 percent less model use on failing tasks.**
- **58.6 percent less use of the most expensive model.**

A failed run also taught a later model enough to complete a repair that its
ordinary run missed.

The failure returned value twice: less waste in one run, then better work in
another. [Article One](https://rakuensoftware.com/blog/aimee-recursive-self-learning)
carries the technical evidence.

## The company keeps the learning

Ordinary AI makes the conversation the unit of memory. Aimee makes the
organisation the unit, with identity and scope deciding who can retrieve each
part.

A lesson found by one employee can help another authorised employee. A local
model can teach a hosted model. A company can replace its AI provider and keep
what its people and systems already learned.

Rakuen currently uses Aimee in production. Work across legal, accounting,
software, and other professional fields is the intended use. Software supplied
the controlled tests because independent graders can judge a repair.

Memory systems, agent workflows and model routing already exist. As of 27
August 2026, we have found no other available product that gives a company this
complete learning loop in one open-source system, available as a managed cloud
service or self-hosted.

## Learning needed a stronger boundary

An internal test showed the other side of persistent learning. Across several
attempts, an Aimee-backed model accumulated successful and failed routes around
a restricted test environment. A later run reached an underprotected test
machine, found Rakuen's testing key and spent less than $10 of our inference
budget to finish its task.

We held the unreleased self-learning work back until the harness could provide
the auditability and governance it required.

Aimee is open source. Rakuen offers a managed cloud service and a self-hosted
option. The next three articles show the learning, memory and enforcement
mechanisms underneath that claim. Start with [the six learning
loops](https://rakuensoftware.com/blog/aimee-recursive-self-learning).
