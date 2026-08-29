# From Failed Run to Shared Capability

Working academic paper on production-grade organisational memory across
heterogeneous language-model agents.

## Status

Working paper, updated 2026-08-29. Not submission-ready.

Updated 2026-08-29. Experiment D gained the matched large-repository
failure-cost campaign: three same-model pairs reduce pooled consumption from
1,819,904 to 1,199,552 tokens, a 34.1 percent reduction, while all six runs fail
the sealed hidden grader. It is recorded as cost containment, not capability,
and the combined economizer-and-progress treatment is left unattributed. The
same pass added the bounded-review sentence the evidence inventory requires,
repointed the data-availability section from open PR #2873 to its merge commit
`faaf05298ce4d3b484f24cb00ccc402c62128e69`, and reverified every SHA-256 in the
inventory against that commit.

The deterministic efficacy study is replicated and causal for the tested
consumer. The open-ended cross-model result is exploratory with one task and
one run per arm. The paper includes a confirmatory study design rather than
presenting the pilot as a population estimate.

## Claim boundary

This is not a first claim for experiential memory, shared agent memory,
cross-task failure memory or cross-model memory benefit. The contribution is
the production systems combination: organisation-scoped reuse across authorised
users and models, durable provenance and correction, independent isolation and
audit, failure-cost control, and a real repository completion crossover.

## Evidence

The [evidence inventory](evidence/figures.md) was completed before the paper was
drafted. It includes the learned-Qwen negative retry, Luna's final-grade failure,
the divergent plain-run comparison and the limits of confidential production
use. It was extended on 2026-08-29 with `FAILCOST-3`, the matched failure-cost
campaign, whose six hidden-grader failures and quarantined first pair are
recorded alongside its 34.1 percent reduction.

## Open items before publication

- **Venue and format are undecided.** The paper is markdown with blog
  frontmatter, and it has no author names, no affiliations and no anonymised
  variant. A submission target decides those. The reference list is written and
  every entry verified against its primary source on 2026-08-29, in a
  style-neutral form that converts to a venue's style without revisiting the
  sources.
- **The publication route is undecided.** `tools/publish.py` does not see this
  folder, and `tools/voice_gate.py` fails it on rules written for journalism:
  an absolute rakuen-blog provenance link, the literal `Rakuen builds aimee`
  disclosure string, the word `arm`, and paragraph length. If the paper exits as
  a preprint rather than a blog post it needs an exemption path rather than a
  rewrite against that gate. The paper already carries a conflict-of-interest
  section.
- **The confirmatory campaign in section 7 has not started.** It is a design,
  not a preregistration. Nothing in the paper may be restated as a population
  effect until it runs. The experiments it needs are sequenced below.
- `DELEGATE-50` is inventoried as supporting only and stays out of the paper.
  Revisit only if worker tokens and correctness are ever collected.

## Experiments still needed

Ordered by cost. The first group closes real holes for no provider spend and
should not wait on anything.

### The hole a reviewer will find first

Nothing yet shows that the **typed record** beats any other extra text. Both
cross-model learned arms received a lesson. Neither was compared against a raw
transcript of the Qwen failure or a generic warning that a previous attempt
failed by over-exploring. Until that four-arm control runs, the transfer result
is equally consistent with "extra prompt text about failure helps", which is a
much weaker claim than the paper makes. Designed in section 7.2, unrun.

### Deterministic, no provider spend

These reuse `make -C src self-learning-efficacy`, whose runs are already
byte-identical across fresh databases.

- **Recall generalisation and near-miss controls.** Now section 7.3. Section 3.2
  proves recall for matching task descriptions only; "similar-goal recall" is
  unsupported as stated until paraphrased and structurally related goals are
  tested, with near misses that must not recall.
- **Correction changing an outcome.** Section 2.2 claims records are correctable
  and section 7.5 verifies supersession as an audit property. No experiment
  shows a corrected record changing what a consumer does. Admit a wrong lesson,
  correct it, show the consumer tracks the correction.
- **Poisoned-lesson transfer, end to end.** Section 5.2 rests the risk term on
  Xiong et al. with no first-party evidence. `benchmarks/memory/poison_gate.py`
  and `poison_fixtures.json` already score demotion; what is missing is a
  poisoned lesson degrading a real consumer's outcome and the gate preventing
  it.
- **The other five loops.** Experiment A shows closure for six loops. Experiment
  B shows efficacy for one. Five have no efficacy evidence at all, and each
  wants its own paired study on the Experiment B pattern.

### Local model, gated on the task corpus

- **Mechanism attribution for failure cost.** Now section 7.4. The 34.1%
  reduction is a combined economizer-and-progress treatment, so a number already
  in the abstract is mechanistically uninterpretable until the 2x2 runs.
- **A population estimate for failure cost.** Three pairs at one run per cell.
  Repeat arms and add tasks.
- **The stopping benefit.** The 11.2% comparison is two trajectories and a fresh
  plain arm diverged. Needs repeated randomised trajectories or a deterministic
  replay environment.

### Hosted models, expensive

- The section 7.2 matrix: three source classes by three consumer classes, four
  consumer arms, repeated for variance.
- **The live multi-user path.** Every cross-model run so far injected the lesson
  directly; `SHARED-KB` covers source-independent recall separately. One live
  end-to-end retrieval run closes the seam the threats section names.
- **One domain outside software.** Section 5.3 concedes that production breadth
  is not efficacy breadth, and section 7 is entirely repositories. A legal or
  accounting study with an adjudicated external criterion is the smallest honest
  version.

### Two prerequisites that gate the hosted work

- **The task corpus.** `benchmarks/roi/large_repo_tasks.json` holds three tasks.
  Section 7.1 asks for at least 30 across three repositories with frozen
  revisions, hidden tests and sensitivity checks. Building and freezing it is
  the real gating item.
- **Usage instrumentation.** The collaboration runtime exposed no token-usage
  objects for Luna or Terra, so no cost claim about hosted consumers is possible
  until it reports them. This is a blocker, not an experiment.
