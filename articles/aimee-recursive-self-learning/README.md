# Aimee: Recursive Self-Learning

Article one of four, and the first technical entry. Aimee 0.4.0 closes six
learning loops on a live two-service deployment. The 25 August evidence target
produced one observation per loop and finished at 46 passed, 0 failed. A later
paired study isolates an outcome gain from failed-approach recall, and an
exploratory Qwen-to-Luna/Terra pilot records a Terra completion crossover.

## The series

0. **[Overview](../the-work-should-survive-the-model/)** — the non-technical
   product, buyer and market argument.
1. **Self-learning** — this one. The loops close; one loop now has paired
   efficacy evidence and a cross-model open-ended pilot.
2. **[Memory](../the-remembering-is-the-learning/)** — the machinery behind this
   article's central claim.
3. **[Architecture](../everything-crosses-one-transport/)** — what parts one and
   two stand on.

Each article should be readable alone. Shared figures are marked as shared in
every reporting record that uses them.

## The claim, and only the claim

Five things are claimed here:

1. six learning loops close on the tested deployment;
2. the harness keeps their learned state;
3. the state remains inspectable and auditable on the tested paths;
4. failed-approach synthesis and recall causally changed matched outcomes for a
   deterministic consumer while leaving novel-task outcomes unchanged;
5. in one exploratory repository task, a lesson from a stopped Qwen failure
   changed Luna verification depth and let Terra complete a hidden-graded,
   regression-sensitive repair its base arm missed.

No claim is made that all six loops improve outcomes over time or that the
one-task cross-model effect estimates a general success rate.

Novelty is outside the claim.

## Status

Draft, updated 2026-08-27. Not published.

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

Extended on 2026-08-26: the harness-versus-weights section had read as a choice
between two designs. It now states that the harness makes no assumption about
which model serves a turn or about whether that model's weights change between
turns, so a weight-updating model runs inside the same isolation and audit path
with every protection intact. The compatibility statement is a design claim
about the shipped boundary and carries no test of its own; see the open items.

Split on 2026-08-26: the full test-node incident and the non-technical product,
buyer and market argument moved to Article Zero. This article keeps the compact
incident context needed by its isolation result and retains every technical
test, source audit and design limit from the prior draft.

Extended on 2026-08-27: the failed-approach loop now carries two efficacy
layers. A 48-task paired deterministic study isolates production synthesis and
recall. A one-task open-ended pilot transfers a sealed Qwen failure lesson into
matched Luna and Terra arms. The article retains the failed learned-Qwen retry
and the Luna final-grade failure.

An editorial clarity pass on 2026-08-27 mapped comments on the earlier
three-part draft against this four-part rewrite. It restored the full incident
account promised by both reporting records to Article Zero, defines the test
machine and immediate impact, and explains why the deterministic efficacy test
can isolate recall while the one-run model pilot cannot separate learning from
ordinary model variation.

Corrected on 2026-08-27: an earlier draft described intended professional
fields as current production breadth. The article now states current production
use without assigning that use to named fields, then labels those fields as the
intended use.

Corrected on 2026-08-27: an earlier draft described Aimee only as self-hosted.
Rakuen offers both a managed cloud service and a self-hosted option.

A second large-repository campaign adds matched failure-cost evidence. Across
three valid task pairs, local Qwen consumption fell from 1,819,904 to 1,199,552
tokens, a 34.1 percent reduction. All six retained runs failed the hidden
grader, so the article identifies cost containment rather than capability
uplift. The invalid first attempt at the cross-language pair remains preserved
and quarantined; a corrected rerun supplies the third valid pair.

The same update now separates workflow-local retry summaries from the durable
failed-approach loop. It records the row shape, matching floor, recall bound,
policy arms and the experimental seam between direct lesson injection and the
storage-backed shared-KB test.

Rewritten on 2026-08-25 against `testing` at `6bcc87e`. The new six-loop target
supersedes the older per-suite counts for the article's current result: 46
passed, 0 failed.

## Evidence

First-party, in the public
[aimee repository](https://github.com/RakuenSoftware/aimee). The
[reporting record](evidence/figures.md) carries the per-figure map, the prior
incident's move to Article Zero, the figures that moved out in earlier splits,
and the two strong claims with what would settle them.

## Open items before publication

- ~~Counts. Refresh at the 0.4.0 tag.~~ **Closed, 2026-08-25.** The article
  carries the reproducible six-loop target at 46 passed, 0 failed.
- Model-agnostic failure transfer now has one exploratory Qwen-to-Luna/Terra
  task behind it. A preregistered multi-task, repeated campaign is still needed
  for a population estimate. Weight-updating compatibility remains a statement
  about where the boundary sits and has no direct first-party efficacy run.
- The cross-model pilot injected the lesson directly. Storage-backed tests
  separately cover source-independent recall within one authorised shared KB;
  a confirmatory run should exercise live multi-user retrieval end to end.
- Temporal-learning rollout details remain in the reporting record and are
  outside the article's six-loop claim.
- Keep the compressed containment summary consistent with part three if either
  changes.
