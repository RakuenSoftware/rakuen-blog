# Aimee: Self-Learning

Article one of four, and the first technical entry. It explains how Aimee turns
the outcomes of successful and failed work into durable company knowledge,
shares relevant lessons across authorised models and users, and keeps that
learning inside an auditable and governed boundary.

## The series

0. **[Overview](../the-work-should-survive-the-model/)**: the short business
   case and non-technical introduction.
1. **Self-learning**: this article. It defines the learning claim, reports the
   current evidence and explains the boundary built around it.
2. **[Memory](../the-remembering-is-the-learning/)**: retrieval, scope,
   correction and temporal knowledge.
3. **[Architecture](../everything-crosses-one-transport/)**: the isolation,
   transport and audit structure under the system.

Each article should be readable alone. Shared figures are marked in every
reporting record that uses them.

## Claim boundary

The article makes four claims:

1. Failed-approach synthesis and recall changed matched outcomes in a
   deterministic controlled test while leaving unrelated-task outcomes
   unchanged.
2. In one exploratory repository task, a lesson from a stopped Qwen failure
   changed later Luna and Terra work. Learned Terra completed a hidden-graded
   repair that its base run missed; learned Luna and the Qwen retry still
   failed.
3. Harness records can persist across workflows and model changes, retain
   identity, scope and provenance, and remain independently auditable on the
   tested paths.
4. The governance boundary sits outside the model and can support both harness
   learning and changing model weights.

The article does not claim a population success rate, that every learned item
improves work, or that one open-ended model run separates learning from ordinary
model variation. It does not make a novelty claim.

## Status

Draft, restored 2026-08-27. Not published.

PR #104 mistakenly replaced the agreed conceptual article with a
count-driven implementation report. This restoration removes that public
section and its references, returns the article to self-learning throughout,
and preserves every underlying result in the reporting record.

The restoration also keeps the editorial corrections made on 2026-08-27:

- Aimee is described as a full company knowledge platform, not only a memory
  or execution layer.
- Rakuen offers managed cloud and self-hosted deployments.
- Legal, accounting, software and other professional fields are described as
  intended uses rather than asserted as measured production breadth.
- The internal incident is introduced as evidence that self-learning was unsafe
  without enforced boundaries, followed by the boundaries Rakuen built before
  release.
- Model nondeterminism, the decision not to reproduce a known boundary defect
  across models, and the limits of the cross-model pilot are stated directly.

The public article retains two efficacy layers. A 48-task deterministic study
isolates production synthesis and recall. A one-task open-ended pilot transfers
a sealed Qwen failure lesson into matched Luna and Terra runs. The negative
learned-Qwen and Luna outcomes remain in the article.

The matched 34.1 percent failed-task token result belongs to the business
overview, not this article. Its complete source and limitations remain in the
reporting record.

## Evidence

Evidence is first-party and lives in the public
[Aimee repository](https://github.com/RakuenSoftware/aimee). The
[reporting record](evidence/figures.md) carries the per-result source map,
corrections, excluded results and open claim boundaries. Raw artifacts are
append-only.

## Open items before publication

- Run a preregistered, repeated, multi-task cross-model campaign to estimate
  how often learned failure improves later work.
- Join automatic failure recording, live shared-knowledge retrieval, model
  action and hidden grading in one end-to-end experiment.
- Test the stated compatibility with changing model weights directly.
- Keep the containment summary consistent with the architecture article.
