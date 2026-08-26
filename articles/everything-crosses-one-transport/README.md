# Everything Crosses One Transport

Part three of three. Each daemon routes supervised inter-module work through
one typed transport. The measured dispatch figure is a 134 ns median; dispatch
and audit enqueue each have a 1,000 ns enforced ceiling. Core-local calls and
external traffic sit outside that coverage.

## The series

1. **[Self-learning](../aimee-recursive-self-learning/)** — the loops close on
   the tested deployment; their effect on outcomes still needs paired
   measurement.
2. **[Memory](../the-remembering-is-the-learning/)** — the machinery behind part
   one's central claim.
3. **Architecture** — this one. What parts one and two stand on.

Each article should be readable alone. Shared figures are recorded in every
reporting record that uses them, marked as shared, so one number is not logged
three times as if independently sourced.

## Status

Draft, 2026-08-24. Not published. Source rechecked on 2026-08-25 at
`6bcc87e`.

Revised in PR review on 2026-08-25. The article now uses the original
architecture narrative as its spine and runs 5,324 words, down from 9,236.
The opening goal, transport lineage, language boundary, grants, delegate
containment, tap, evidence chain and two-service split remain in sequence.
Unsupported claims are qualified in place rather than removed with the story.

Split out of the self-learning draft, where this material had grown to roughly a
third of the piece while serving a claim that needed only part of it.

On 2026-08-24 the stranded-seam incident went back to part one for the same
reason, in the other direction: the article keeps the two-service split's cost,
which is its own claim, and points to part one for the incident, the run log and
the lint check.

## Evidence

First-party, in the public
[aimee repository](https://github.com/RakuenSoftware/aimee), read from `testing`
on 2026-08-24. See [the reporting record](evidence/figures.md) for the per-figure
map, the author's statements that are not documents, and the limits on the
security argument.

## Deliberate omission

The article's security analysis stops at the controls that exist and their
documented limits. It does not claim a penetration test, formal proof or
independent security audit.

Work beyond that exists in plan form and is **deliberately not described**,
because it is not roadmapped and not tied to any public statement. A published
article naming planned work turns it into a commitment by implication, and an
unroadmapped plan that slips then reads as a broken promise rather than as
reprioritised work.

If that work lands, the article gets a correction with a date rather than a
retroactive "as we said we would". If a future editor wonders why the piece
stops where it does: this is why, and the silence is the right default until
something ships.

## Open items before publication

- ~~PR 2839 must be confirmed merged before publication.~~ **Cleared and
  verified, 2026-08-24.** `origin/testing` is at `681306b977`, which is the
  merge commit for PR 2839 itself. The delegate sole-egress section's
  description of its Go ownership and post-start verification as shipped now
  stands on the shipped code rather than on a statement about intent.
- ~~The bus inventory is stated as complete.~~ **Retired, 2026-08-25.** The
  article now scopes the transport to supervised inter-module work and names
  the core-local and external paths outside it.
- ~~Decide whether the analysis-not-measurement limit should also be said in the
  article body.~~ **Closed, 2026-08-25.** The article states that no penetration
  test or independent security audit supports the security analysis.
- The self-learning article retains a compressed version of the containment
  argument, because its opening incident raises the question and a reader should
  not have to leave the piece to get the answer. Keep the two accounts
  consistent if either changes.
