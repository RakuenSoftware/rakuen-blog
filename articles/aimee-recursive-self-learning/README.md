# Aimee: Recursive Self-Learning

Part one of three. Aimee 0.4.0 closes six learning loops on a live two-service
deployment. The 25 August evidence target produced one observation per loop and
finished at 46 passed, 0 failed. Loop efficacy remains unmeasured.

## The series

1. **Self-learning** — this one. The loops close; their effect on task outcomes
   still needs paired measurement.
2. **[Memory](../the-remembering-is-the-learning/)** — the machinery behind this
   article's central claim.
3. **[Architecture](../everything-crosses-one-transport/)** — what parts one and
   two stand on.

Each article should be readable alone. Shared figures are marked as shared in
every reporting record that uses them.

## The claim, and only the claim

Three things are claimed here:

1. six learning loops close on the tested deployment;
2. the harness keeps their learned state;
3. the state remains inspectable and auditable on the tested paths.

No claim is made that all six loops improve outcomes over time. The article
names the missing setup-and-consumer ablation needed to establish that.

Novelty is outside the claim.

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

Corrected on 2026-08-25: the blanket claim that every learning gate was disabled
was false. The article now scopes that statement to the six measured loops,
names the build-graph check that caught the provider omission, separates loop
closure from measured benefit, and surfaces the memory audit result. The audit
sentence's dependency landed in Aimee PR #2847 on 2026-08-25.

Rewritten on 2026-08-25 against `testing` at `6bcc87e`. The new six-loop target
supersedes the older per-suite counts for the article's current result: 46
passed, 0 failed.

Revised in PR review on 2026-08-25 to restore the original narrative spine.
The article now runs 3,234 words, down from 4,313. It retains the lead incident,
the containment prerequisite, the six live observations, the deployment-graph
failure, the endogeneity gate, the memory argument and the harness trade-off.
It also makes the harness dependency explicit: without continued harness access,
an agent falls back to its checkpoint and current context rather than carrying
the accumulated learned state with it. The efficacy and cross-model limits
remain adjacent to the claims they bound.

## Evidence

First-party, in the public
[aimee repository](https://github.com/RakuenSoftware/aimee). The
[reporting record](evidence/figures.md) carries the per-figure map, the
provenance of the lead incident, the figures that moved out in the split, and
the two strong claims with what would settle them.

## Open items before publication

- ~~Counts. Refresh at the 0.4.0 tag.~~ **Closed, 2026-08-25.** The article
  carries the reproducible six-loop target at 46 passed, 0 failed.
- Temporal-learning rollout details remain in the reporting record and are
  outside the article's six-loop claim.
- Keep the compressed containment summary consistent with part three if either
  changes.
