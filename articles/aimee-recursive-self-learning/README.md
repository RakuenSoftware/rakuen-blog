# Aimee: Self-Learning

Article One of four, and the first technical entry. The editorial baseline is
PR #83 at `48f10a17e9`, the last valid version identified after the article was
replaced by later rewrites.

## The series

0. **[Overview](../the-work-should-survive-the-model/)**: the short business
   case and non-technical introduction.
1. **Self-learning**: this article. It explains the learning claim, its current
   evidence and the boundary built around it.
2. **[Memory](../the-remembering-is-the-learning/)**: retrieval, scope,
   correction and temporal knowledge.
3. **[Architecture](../everything-crosses-one-transport/)**: the isolation,
   transport and audit structure under the system.

Each article should be readable alone. Article Zero owns the product pitch,
business figures, deployment options, intended-use framing and complete
incident account. Article One retains the technical consequences and evidence.

## Claim boundary

The article makes five measured or architectural claims:

1. The deployed self-learning target passed 46 checks and changed later system
   state. This establishes operation, not universal outcome improvement.
2. Failed-approach synthesis and recall changed repeated-task outcomes from
   12/24 to 24/24 in a deterministic paired test while unrelated tasks remained
   12/24 in both conditions.
3. In one exploratory repository task, a lesson from a stopped Qwen failure
   changed later Luna and Terra work. Learned Terra completed the hidden-graded
   repair; learned Luna and the learned Qwen retry still failed.
4. Across three matched large failures, Aimee reduced provider-recorded tokens
   by 34.1 percent. Every run failed, so the result establishes cost containment
   rather than improved Qwen capability.
5. Harness records can persist across workflows and model changes, retain
   identity, scope and provenance, and remain independently auditable on the
   tested paths.

The article does not claim a population success rate, that every learned item
improves work, or that one open-ended model run separates learning from ordinary
model variation. It makes no market or novelty claim.

## Status

Draft, restored from PR #83 on 2026-08-27. Not published.

The restoration uses the exact PR #83 article as its editorial source. It then
makes only these scoped changes:

- Removes the full incident, product and business material now owned by Article
  Zero.
- Changes the public title and terminology to self-learning.
- States directly that internal testing showed self-learning was unsafe without
  critical boundaries and that Rakuen built those boundaries before release.
- Adds the later controlled recall result, exploratory cross-model pilot and
  matched failed-task token result without replacing the PR #83 structure.
- Removes the implementation diary and counted taxonomy introduced by PR #104.

The previous PR #108 rewrite is not used as editorial source material.

## Evidence

Evidence is first-party and lives in the public
[Aimee repository](https://github.com/RakuenSoftware/aimee). The
[reporting record](evidence/figures.md) carries the per-result source map,
corrections, excluded results and open claim boundaries. Raw artifacts remain
unchanged.

## Open items before publication

- Run a preregistered, repeated, multi-task cross-model campaign to estimate
  how often learned failure improves later work.
- Join automatic failure recording, live shared-knowledge retrieval, model
  action and hidden grading in one end-to-end experiment.
- Test compatibility with changing model weights directly.
- Keep the containment summary consistent with the architecture article.
