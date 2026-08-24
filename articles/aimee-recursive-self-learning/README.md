# Aimee: Recursive Self-Learning

Part one of three. Aimee's learning capabilities were effectively disabled prior
to 0.4.0. The capacity for learning and testing existed, but it did nothing while
it was tested. With 0.4.0 self-learning is fully enabled, everything gating it is
disabled, and aimee self-learns.

## The series

1. **Self-learning** — this one. The loops exist and they work, and
   memory is what they are made of.
2. **[Memory](../the-remembering-is-the-learning/)** — the machinery behind this
   article's central claim.
3. **[Architecture](../everything-crosses-one-transport/)** — what parts one and
   two stand on.

Each article should be readable alone. Shared figures are marked as shared in
every reporting record that uses them.

## The claim, and only the claim

Three things are claimed here and nothing beyond them:

1. aimee self-learns;
2. the self-learning loops exist;
3. the memory exists to support them.

No claim is made about improvement, outcomes, or the quality of what is learned
over time. Drafts kept reintroducing disclaimers against that fourth claim; it
was never being made, and defending against it implies otherwise. If a rewrite
adds one back, cut it.

**Nor is novelty claimed.** A system that improves its own improvement process
is an old idea, and the article says so in its own section rather than leaving a
reader to assume otherwise. The distinction that matters: deflating the
*technique* is accurate and belongs in the piece; deflating the *work* is not,
and an earlier draft did that and was cut. Keep the first, refuse the second.

## Status

Draft, 2026-08-24. Not published.

The recursive self-improvement loops merged to `testing` on 2026-08-24 as
`877e994c2f`. All the learning work described is in 0.4.0.

Trimmed from a 5,200-word master draft when the architecture material was split
out to part three. On 2026-08-24 the stranded-seam incident, the lint check and
the sqlite-shim defect came back from part three: the material is about shipping
the learning work, and this article's record already held its evidence. Part
three keeps the split's cost and points here. It retains a compressed containment summary, because the
opening incident raises that question and a reader should not have to leave the
piece to get the answer.

## Evidence

First-party, in the public
[aimee repository](https://github.com/RakuenSoftware/aimee). The
[reporting record](evidence/figures.md) carries the per-figure map, the
provenance of the lead incident, the figures that moved out in the split, and
the two strong claims with what would settle them.

## Open items before publication

- ~~Counts. Refresh at the 0.4.0 tag.~~ **Closed, 2026-08-24.** `testing` is the
  0.4.0 release, so the reads already recorded are reads of 0.4.0 and there is no
  separate tag to pin to. The lint and suite counts the article carries are the
  latest.
- **Temporal learning paths** are default-off today and intended default-on at
  release. That is the one forward-looking claim in the piece, and it is a
  statement about a future default rather than about a pin, so it stands as an
  open item.
- Keep the compressed containment summary consistent with part three if either
  changes.
