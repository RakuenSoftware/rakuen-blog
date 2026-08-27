# Aimee: Self-Learning

Article One of four, and the first technical entry. It explains why
self-learning changes the boundary around an AI model, why the learning belongs
in the harness and how one governed history can survive changes to models,
weights and users.

## The series

0. **[Overview](../the-work-should-survive-the-model/)**: the short business
   case and non-technical introduction.
1. **Self-learning**: this article. It explains the learning argument and the
   boundary built around it.
2. **[Memory](../the-remembering-is-the-learning/)**: retrieval, scope,
   correction and temporal knowledge.
3. **[Architecture](../everything-crosses-one-transport/)**: the isolation,
   transport and audit structure under the system.

Each article is readable alone. Article Zero owns the product and business
case, the complete testing incident, deployment options, intended-use framing
and business-level headline results. Article One retains the technical
consequence, the conceptual argument and the headline evidence that
self-learning operates and changes a later outcome. Article One's reporting
record owns the full measurement design, replication and limitations. Article
Two owns the memory machinery behind the result. Article Three owns the full
transport implementation.

## Claim boundary

The article makes six bounded claims:

1. Self-learning lets later work inherit useful results and failed approaches,
   which changes the boundary a model harness has to enforce.
2. The deployed self-learning paths passed 46 of 46 checks, and a paired
   fixed-consumer study found that recalled failure changed repeated-task
   outcomes while leaving novel-task outcomes unchanged.
3. Internal testing showed that self-learning was unsafe without critical
   boundaries, and Rakuen built those boundaries before release.
4. The route required to finish work belongs inside governed interfaces rather
   than behind a barrier the model must route around.
5. Harness learning can persist across model and weight changes while identity
   and scope let one history serve multiple authorised users.
6. System-wide observability requires the harness to own execution, authority,
   memory and the audit path.

The article makes no market claim, population-effect claim or claim that every
learned item improves an outcome. Its reporting record retains the full
efficacy method and limitations; cross-model and cost measurements remain with
the articles whose arguments need them.

## Reconstruction

This draft reconstructs the reviewed editorial lineage instead of selecting one
historical snapshot wholesale:

- PR #83 at `48f10a17e9` supplies the fuller self-learning argument after the
  counted-loop framing was removed.
- PR #87 at `956185a0` records a scope decision that moved the measurements and
  memory machinery to Article Two. The reconstruction keeps the memory
  machinery there but returns the measurements to Article One because they
  directly support its central self-learning claim.
- PRs #91 through #98 supply the approved reader orientation, structure,
  incident ownership, company voice and ending.
- PR #104's implementation report and PR #108's hybrid rewrite are not used as
  editorial source material.

The reconstruction preserves the deliberate engineering-effort statement,
keeps the complete incident in Article Zero and restores no counted taxonomy.

## Status

Draft, reconstructed 2026-08-27. Not published.

## Evidence

Evidence is first-party and lives in the public
[Aimee repository](https://github.com/RakuenSoftware/aimee). The
[reporting record](evidence/figures.md) carries the complete source map,
corrections, excluded results and the disposition of every result removed from
Article One. Raw artifacts remain unchanged.

## Open items before publication

- Keep the containment summary consistent with the architecture article.
- Confirm that Article Two carries the measurement detail previously assigned
  to it.
- Review the reconstructed article as prose before treating this lineage as the
  new editorial baseline.
