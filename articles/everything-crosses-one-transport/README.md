# Everything Crosses One Transport

Part three of three. Nothing in aimee can do anything without crossing one
transport, which costs 134 ns and records what went through it. That is what
makes governance a guarantee rather than a policy document, and it is why the
chokepoint is not worth attacking.

## The series

1. **[Self-learning](../aimee-recursive-self-learning/):** why isolation comes
   before learning and what later work inherits.
2. **[Memory](../the-remembering-is-the-learning/):** how stored evidence
   becomes learning.
3. **Architecture:** this one. The governed boundary around both.

Each article should be readable alone. Shared figures are recorded in every
reporting record that uses them, marked as shared, so one number is not logged
three times as if independently sourced.

## Status

Draft, 2026-08-24. Not published.

Split out of the self-learning draft, where this material had grown to roughly a
third of the piece while serving a claim that needed only part of it.

On 2026-08-24 the stranded-seam incident went back to part one for the same
reason, in the other direction: the article keeps the two-service split's cost,
which is its own claim, and points to part one for the incident, the run log and
the lint check.

Revised on 2026-08-26 to stand alone. Cross-article references now state the
incident, memory operation or failure rule needed at that point, while the
series links remain optional context.

## Evidence

First-party, in the public
[aimee repository](https://github.com/RakuenSoftware/aimee), read from `testing`
on 2026-08-24. See [the reporting record](evidence/figures.md) for the per-figure
map, the author's statements that are not documents, and the limits on the
security argument.

## Deliberate omission

The article's security claim ends at "detection and provenance, not prevention",
with "at least for now" and no more.

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
- ~~The bus inventory is stated as complete.~~ **Checked, 2026-08-24**, against
  `origin/testing` at `681306b977`. PAM and OIDC appear nowhere in
  `src/core/event_bus/`, so the disclaimer holds. `policy` inside the bus is
  only `BLOCK`/`SHED` backpressure, which the article already describes, not
  authorization. One wrinkle worth keeping: mTLS lives in
  `src/core/connection/`, not in the bus directory, so the article's "bus"
  spans the module transport and the inter-instance connection. The claim is
  accurate; a reader checking one directory will not find it. See the record.
- ~~Decide whether the analysis-not-measurement limit should also be said in the
  article body.~~ **Decided, 2026-08-24: no.** The security argument is analysis
  and no penetration test or third-party audit stands behind it. That stays in
  the reporting record, and the article continues to state its own losable form
  in the body, which was judged enough.
- The self-learning article retains a compressed version of the containment
  argument, because its opening incident raises the question and a reader should
  not have to leave the piece to get the answer. Keep the two accounts
  consistent if either changes.
