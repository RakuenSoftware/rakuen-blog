# Aimee: Recursive Self-Learning

Part one of three. Aimee 0.4.0 self-learning changes state consumed by later
work on a live two-service deployment. The 25 August evidence target finished
at 46 passed, 0 failed. In a paired study on 26 August, 12 of 24 repeated tasks
succeeded without the learned failure record, against 24 of 24 with it.

## The series

1. **Self-learning** — this one. The learned state changes later outcomes in a
   controlled paired study.
2. **[Memory](../the-remembering-is-the-learning/)** — the machinery behind this
   article's central claim.
3. **[Architecture](../everything-crosses-one-transport/)** — what parts one and
   two stand on.

Each article should be readable alone. Shared figures are marked as shared in
every reporting record that uses them.

## The claim, and only the claim

Four things are claimed here:

1. self-learning changes later state on the tested deployment;
2. recalled failure changed later outcomes in the controlled paired study;
3. the harness keeps the learned state;
4. the state remains inspectable and auditable on the tested paths.

The outcome study used a fixed consumer to isolate the learned record. It is
not a model benchmark or a measure of open-ended generalisation.

Novelty is outside the claim.

## Status

Draft, 2026-08-24. Not published.

The recursive self-improvement work merged to `testing` on 2026-08-24 as
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
the accumulated learned state with it. The study and cross-model limits remain
adjacent to the claims they bound.

## Evidence

First-party, in the public
[aimee repository](https://github.com/RakuenSoftware/aimee). The
[reporting record](evidence/figures.md) carries the per-figure map, the
provenance of the lead incident, the figures that moved out in the split, and
the two strong claims with what would settle them. The paired-study raw output
is preserved under `evidence/raw/self-learning-efficacy-2026-08-26/`.

## Open items before publication

- ~~Counts. Refresh at the 0.4.0 tag.~~ **Closed, 2026-08-25.** The article
  carries the reproducible self-learning target at 46 passed, 0 failed.
- ~~Measure whether learned state changes later outcomes.~~ **Closed for the
  controlled failed-approach case, 2026-08-26.** Two valid runs reproduced
  12/24 without the learned record and 24/24 with it; novel controls stayed at
  12/24. Open-ended model use remains outside that study.
- Temporal-learning rollout details remain in the reporting record and are
  outside the article's self-learning claim.
- Keep the compressed containment summary consistent with part three if either
  changes.
