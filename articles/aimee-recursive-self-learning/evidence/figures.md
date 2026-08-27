# Reporting record and figure provenance

Every figure in
[`aimee-recursive-self-learning.md`](../article/aimee-recursive-self-learning.md), and where it
came from.

Article one of four, after the non-technical
[overview](../../the-work-should-survive-the-model/). The memory article is
second and the [architecture](../../everything-crosses-one-transport/) is third.
Figures shared with those pieces are marked shared here and recorded in their
records too, so one number is not logged several times as if independently
sourced.

Evidence is first-party and lives in the public
[aimee repository](https://github.com/RakuenSoftware/aimee) rather than in this
folder, because each run is a validation report attached to the change it
validates. The learning work in 0.4.0 spans many branches. The loop figures come
from the recursive self-improvement work, merged to `testing` on 2026-08-24 as
`877e994c2f`.

## The incident moved to Article Zero

**First-party account by the author.** The test run in which an aimee-backed
model got around its protections, took an underprotected node and got hold of a
vast.ai testing API key is the author's own account of Rakuen's own system, own
key and own spend, including the **under $10** figure.

The full account now lives in Article Zero, where the incident carries the
product consequence. This article keeps only the compact context required by
the isolation result. The prior reporting remains recorded here rather than
disappearing with the prose.

That is the source, and the byline names it. No artifact is attached and none is
required: the account criticises the author's own protections and deflates its
own severity, so it carries no incentive an artifact would need to check. A
vast.ai billing line could be produced and would corroborate a figure nobody has
reason to dispute.

No date is given because nothing turns on one. The claim is that this happened
during testing, before the 0.4.0 isolation work, which the article states.

**The cause is attributed, and the attribution is the author's reading.** The
article now states that the route past the protections was assembled across many
runs, and that the self-learning loops under test are what accumulated it. Two
parts of that are on the record and one is not.

On the record: the incident happened during the testing of those loops, on code
that never reached a release. The article's statement that the loops "stayed off
until 0.4.0" describes shipped releases, and testing code is where they ran. The
article now says so in place, because the earlier wording invited the reading
that nothing was learning at the time.

Not on the record: that the accumulation is what carried the model past the
protections. No paired run was made against a harness with the accumulated
record withheld, so the causal step is inference from a first-party account. The
article marks it with "I think" where it is made and says that the comparison
has not been run. It is used only to explain the requirement for an external
isolation and audit boundary.

The model is unspecified deliberately. Nothing about the account depends on
which model it was, and the author's position is that it should theoretically
have been possible with any of them. The article says so rather than leaving the
omission to look like discretion.

## Sources

| key | document | date |
|---|---|---|
| `S0S1` | `docs/validation/recursive-self-improvement-s0-s1-2026-08-23.md` | 2026-08-23 |
| `S2S6` | `docs/validation/recursive-self-improvement-s2-s6-2026-08-23.md` | 2026-08-23 |
| `FULL` | `docs/validation/recursive-self-improvement-full-stack-2026-08-23.md` | 2026-08-23 |
| `PROD` | `docs/validation/recursive-self-improvement-producers-2026-08-24.md` | 2026-08-24 |
| `PR` | PR #2835, merged to `testing` as `877e994c2f` | 2026-08-24 |
| `ENDO` | `src/modules/learning/learning_endogeneity.c` on `testing` | read 2026-08-24 |
| `TYPED` | PR #2824, typed facts in the recall walk and the scheduled lifecycle | merged 2026-08-20 |
| `TEMP` | PR #2834, evidence-backed temporal learning loop; PR #2841, promotion to default-on, read at `agent/temporal-assertion-learning-loop` | merged 2026-08-24 |
| `WORM` | [PR #2847](https://github.com/RakuenSoftware/aimee/pull/2847), `docs/validation/memory-changeset-worm-seal-2026-08-25.md` | merged 2026-08-25 as `ace897e7a3` |
| `EFFICACY` | `docs/validation/self-learning-efficacy-2026-08-26.md` | 2026-08-26 |
| `CROSS` | `benchmarks/results/roi/cross-model-shared-learning-pilot.json` and `benchmarks/results/roi/RESULTS.md` in [PR #2873](https://github.com/RakuenSoftware/aimee/pull/2873) | 2026-08-27 |
| `APPROACH` | `src/modules/learning/learning_approach_memory.c`, `src/modules/learning/include/aimee/learning/approach_memory.h`, `src/approach_store.c`, `src/tests/test_approach_memory.c` in PR #2873 | 2026-08-27 |
| `ECON` | `docs/features/economizer.md`, `docs/features/tool-output-condensation.md` in PR #2873's source tree | 2026-08-27 |

## Correction inventory, 2026-08-25

This pass preserves every first-party result already inventoried below. It
changes the disposition of five claims:

| item | evidence class | disposition |
|---|---|---|
| "everything gating it is disabled" | static source audit at the article pin | **Corrected.** `config_learning_synthesize_enabled()` reads a default-zero value, and six `learning_implicit_*` flags remain in the rollout-readiness programme. The article now confines the claim to the six measured loops: they are on and their producing halves reach consumers. |
| the missing provider registration | live two-service test plus build-graph source audit (`PROD`, `PR`) | **Retained and narrowed.** The provider-injection unit fixtures could not reproduce this deployment omission. The heading now carries the actual fix: a check derived from the build graph. |
| loop closure as evidence of self-learning benefit | live liveness tests (`S0S1`, `S2S6`, `FULL`, `PROD`, `PR`) | **Limited, then partly superseded on 2026-08-27.** Closure remains observed. `EFFICACY` now establishes benefit for the failed-approach loop only; the other five loops have not met that standard. |
| the cause of the test-node incident | first-party account plus the article's own statement of which loops were off | **Moved and scoped.** Article Zero now carries the full account, attributes the route to accumulation across runs, marks the causal step as the author's reading and states that the comparison settling it has not been run. This article retains only the isolation requirement it produced. |
| a memory mutation leaves an inseparable audit record | static call-path audit plus live PostgreSQL fault injection (`WORM`) | **Added.** The C mutation API already sealed in `fm_commit_finish()`; all five SQL-owned close paths now do the same. PR #2847 has landed. The live arm sealed 1 of 1 memory changesets and the call-stripped control sealed 0 of 1. |

Three figures are surfaced together in the memory section rather than left only
in this ledger: the confidence multiplier, proposal 8001's two observed fates,
and the live WORM seal/control counts. Their original entries and sources remain
below.

## Efficacy update, 2026-08-27

This pass adds results without removing any earlier reporting or negative
outcome.

| result | source | disposition |
|---|---|---|
| repeated-task score 12/24 with synthesis withheld and 24/24 with self-learning enabled | `EFFICACY` | **Published as causal efficacy for production failed-approach synthesis and recall.** The consumer is deterministic, so this is not presented as a model-reasoning benchmark. |
| novel-task score 12/24 in both conditions | `EFFICACY` | **Published as the unrelated-task control.** |
| 12 treatment-only successes, zero control-only, exact two-sided McNemar p = 0.00048828125 | `EFFICACY` | **Published exactly.** |
| second fresh-DB run produced byte-identical `results.csv`; both valid runs passed 12 harness checks | `EFFICACY` | **Published as reproducibility for the deployed test path.** Three invalid earlier attempts remain retained in the source report and excluded for stated setup/harness reasons. |
| local Qwen source failure stopped after 512,545 provider tokens with no patch | `CROSS` | **Published as the source of the transferred lesson.** The 11.2% comparison to an earlier plain failure belongs to Article Zero's ROI record. |
| Luna learned arm completed a full server build and focused-test execution that its base arm did not; final grade failed in both | `CROSS` | **Published as a capability and verification-depth crossover with the negative final grade in place.** |
| Terra base failed the hidden grade; learned arm passed visible and hidden grades and authored a regression-sensitive test | `CROSS` | **Published as a one-task completion crossover.** |
| learned retry on the originating Qwen model failed after 519,662 tokens | `CROSS` | **Published as a negative result.** The lesson was not universally sufficient. |
| different source/user/session/model references reinforce one row and similar-goal recall ignores source identity inside one shared KB | `src/tests/test_approach_memory.c` in PR #2873 | **Published as storage-path evidence.** Authorisation selects the accessible KB/scope; source identity remains provenance. |

The controlled Luna and Terra arms received the Qwen lesson unchanged and
directly. They did not retrieve it through separate live user identities. The
storage-backed test establishes the product's source-independent shared-KB
path; a future confirmatory campaign should exercise both pieces end to end.

The collaboration runtime exposed no provider token-usage object for the Luna
or Terra arms. No cost figure is inferred from their trajectories.

### Retry-handoff distinction

The article's comparison between a workflow-local failure summary and Aimee's
failed-approach learning is an architectural comparison, not a market census.
`APPROACH` establishes the concrete row shape, source provenance, normalised
token set, 0.5 Jaccard floor, bounded pool, maximum of eight recalled matches,
repetition count, unrelated-goal silence and `off`/`brief`/full policy arms.
The renderer's test forbids imperative `must`, `never` and `do not` language.

`ECON` supports the separate statement that accumulated tool history can be
folded or condensed with scoped recovery pointers. No economizer saving is
attributed to the Terra pilot: its controlled arms did not traverse that full
production path and exposed no provider usage objects.

The article keeps the experimental seam explicit. `CROSS` delivered the fixed
Qwen lesson directly to Luna and Terra. `APPROACH` separately tests recording
under one user/session/model source, reinforcement under another, similar-goal
recall and unrelated-goal exclusion. Joining those pieces end to end remains a
confirmatory experiment, not a completed claim.

Rakuen reports current production use. This is a first-party operator statement
with customer identities and usage records withheld. Legal, accounting,
software and other professional work are the intended use. The statement does
not establish current deployment or measured efficacy in each field.

Corrected on 27 August 2026: an earlier draft described Aimee only as
self-hosted. Rakuen offers both a managed cloud service and a self-hosted
option. None of the technical results in this article depends on which
deployment option a customer chooses.

The same correction pass expanded the opening product description. The Aimee
knowledge base holds documents, code, facts, decisions, evidence and work
history; durable learning is one capability of that larger system. This is a
product-scope correction with no effect on the technical results.

## Test environment for the live loop figures

This is the node from the incident. It was unused, the model took it, and it was
afterwards repurposed into the sanctioned agent test host, which is what keeps
agents off the production host. Author's account; the host identity is
corroborated by every validation report below naming it.

pvetest, Linux 7.0.14-8-pve x86_64, 8 cores, 31 GiB RAM, PostgreSQL 17.11 with
pgvector 0.8.0 and pg_trgm, gcc 14.2. Each run built from a scratch copy in a
private `HOME`/`AIMEE_HOME`, removed afterwards. Rakuen's own test
infrastructure, so these are our numbers on our bench.

`PROD` records its host kernel as 7.0.14-4-pve where the earlier reports record
7.0.14-8-pve. Both are as printed by the run.

The extension is pgvector 0.8.0; 0.4.0 moves the default to pgvectorscale.
Nothing above is a vector-search measurement.

## Figures

| figure in article | source | note |
|---|---|---|
| 7 modules on the KB, 17 on the server | `PROD`, `PR` | every module each daemon is granted and has a binary for |
| one shared `aimee-kb` behind many per-user `aimee-server` instances; the loops were measured against a single pair | author, corroborated by `docs/DEPLOYMENT.md` and `docs/SECURITY.md` on `testing` | **Corrected 2026-08-24.** Earlier drafts described the two services without their multiplicity, which reads as one-for-one. DEPLOYMENT.md: "Server and one KB are declared together... The one-KB Compose files are deployment profiles, not the fleet limit." SECURITY.md carries per-user write grants and KB-signed user identity. Shared with part three, which carries the reach-versus-capability distinction |
| second scan left the observation count at 2 | `S0S1` | seeded `agent_jobs` with two failures and one control |
| `no_rescue` costing 1.000 over 3 paired tasks; `no_retry` no measured effect | `S2S6` | seeded ablation grid |
| `resolved 0 of 5 considered (budget 5)` | `PROD` | |
| the policy layer's `plan_advisory` / `full` answer | `PROD` | |
| learning loops e2e 28 passed / 0 failed | `PR` | supersedes the 20/0 in `PROD` for an earlier revision of the suite |
| module liveness e2e 13 passed / 0 failed | `PROD`, `PR` | |
| deleting the KB registration turns them red at 25/28 and 9/13 | `PR` | proof against the bug |
| four pieces placed where they could not reach their own data; one answered 200 to every refused signal | `FULL`, `S2S6`, `PROD` | **shared** with the architecture article, which states the split's cost and points here. The detail moved to this article on 2026-08-24: the incident belongs with the learning work, and the e2e and registration-deletion rows above are its evidence |
| the classifier registered in the daemon and not the KB; the `WARN` and the 200 | `PROD`, `PR` | quoted verbatim from the run log. Carried over from the architecture article's record on 2026-08-24 with the prose |
| the seam lint check, its self-test deleting the real registration line, and the non-zero exit when zero pairs resolve | `PR` | `scripts/check_provider_registration.py`; the self-test is what stops the guard passing vacuously |
| the sqlite shim accepts SQL Postgres rejects; a two-hop neighbour query survived as a Postgres syntax error | `PR` | the same wall on the database side |
| `open (75% of 4 committed proposals exogenous)` | `FULL` | cross-checked against `psql` and the KB's own answer |
| `closed (0% of 25 committed proposals exogenous)` | `FULL` | 25 implicit-detector commits, no exogenous root |
| gate closed: `0 admitted`, no task file written; reopened: `1 admitted` | `FULL` | |
| unreachable reports `unavailable`, never `open` | `FULL` | changed from `open` during this work |
| the exogenous source list and the endogenous detector types | `ENDO` | unknown provenance classifies as endogenous |
| confidence classes multiply a 0.80 semantic baseline: A 1.0, B 0.75, C 0.5 | `TYPED` | **shared** with the memory article, which carries the source detail |
| typed facts were excluded from the graph walk, and separately the gravity table was dead at the fusion call site, which took the unknown default for every edge | `TYPED` | **shared** with the memory article. Two distinct defects; an earlier draft merged them into "co-occurrence at 0.45 drove recall" |
| the co-occurrence upsert counted co-occurrence as re-assertion; weight normalisation rewrote confirmation counts | `TYPED` | **shared** with the memory article |
| temporal learning paths were default-off for the loop figures, and were promoted to default-on on 2026-08-24 | `TEMP` | **Updated 2026-08-24.** PR #2841 flips `kb_mining_failure_learning_enabled` from 0 to 1, and the proposal's state line becomes "implemented, validated, and promoted default-on after benchmark review". The article previously called this default-on at release, which was forward-looking; it is a shipped fact now. The loop figures predate the flip and are unaffected |
| memory changeset WORM seal: 1 of 1 live, 0 of 1 with the five SQL seal calls stripped | `WORM` | PostgreSQL 17.11, pgvector 0.8.0, pg_trgm 1.6 on pvetest; the negative control distinguishes the seal from an unrelated audit row |

## Figures moved out in the split

| figure | now recorded in |
|---|---|
| 134 ns dispatch, 82 ns audit publish, the ceilings and the merge gate | architecture. No longer referenced here at all after the 2026-08-24 scope pass |
| grants, principal refs, the supervised-process count, the capture tap | architecture |
| the bus inventory, validation in both directions, the OIDC instance | architecture |
| ~~the provider-registration lint check and the sqlite-shim defects~~ | **returned to this article, 2026-08-24.** They moved out with the architecture split and came back with the prose: the incident is about the learning work, and its evidence was already recorded here. The architecture article keeps the split's cost and points here |
| the evidence and lifecycle layer, the five memory seams, per-seam failure behaviour | memory |
| write authority derived from authentication | memory |

The article still refers to the containment property, because its opening
incident raises the question and a reader should not have to leave the piece to
get the answer. Those sentences are sourced from the architecture record rather
than restated here.

**Trimmed 2026-08-24.** That summary had grown into a second account of the
mechanism: `--network none`, the bind-mounted socket, grant semantics and the
134 ns dispatch cost, all of which are the architecture article's to make. It
now carries only what this article's argument needs, which is that nothing acts
without crossing, and that execution and the hosted models are confined.

**Cut further the same day.** A scope pass against this article's claim removed
the standalone transport section, which explained the architecture's one novel
piece at length in the article that does not make that argument. The novelty
exception it existed to state is now one sentence in the opening, pointing at
the third article. `134 ns` no longer appears in this article at all.

## The prior-art claim

The article states that a system improving its own improvement process is an old
and ordinary idea, citing genetic algorithms running a scored population since
the 1970s, training loops adjusting against a measure, and hyperparameter search
tuning the tuner. That is general knowledge about the field rather than a
first-party finding, and it is stated to bound the article's own claim rather
than to support it: the technique is not new, the claim is that these six loops
close on this deployment.

No comparison is made to any other system's implementation, and none of the
figures in this article depend on the prior-art paragraph being right.

## Claims that are not measurements

| claim | note |
|---|---|
| ~~they will be default-on in the 0.4.0 release~~ | **Superseded 2026-08-24.** The six measured loops and the temporal loop are shipped on; this does not make unrelated learning synthesis and implicit-signal flags default-on. See the correction inventory above. |
| the loops came out of one proposal, the memory took a measurement campaign | author, and this blog |
| the benchmarking series was undertaken to establish that the memory is good enough to build on | statement of intent behind the published series; the articles are the artifact |

The "Learning like this has to live in the harness" section is argument. It carries no
figures. The claim that a continuously learning model will get outside its
harness is a judgement and is written as one.

## The strong claims, and what settles them

**Recursive self-learning is on.** Falsifiable per loop: a signal that reaches
no sink, an admitted candidate that produces no task file the harness will load,
a superseded proposal whose fate does not change, an endogeneity ratio computed
from no ledger, or a declared policy arm the sampler never returns. Each is
covered by an assertion in `tests/e2e/learning-loops-pg-e2e.sh` or
`tests/e2e/module-liveness-pg-e2e.sh`, both run on a real two-service stack.

**Failed-approach efficacy.** `EFFICACY` now measures the production synthesis
and recall path with the consumer held deterministic. It establishes a matched
task-outcome effect and unchanged novel-task control. It does not establish
open-ended model following or efficacy for the other five loops.

**Model independence.** The boundary remains model-independent by construction,
and `CROSS` now adds one direct measurement. One Qwen-derived failure lesson
changed later Luna and Terra trajectories; Terra crossed from hidden-grade
failure to completion. One task and one run per arm establish the occurrence,
not its frequency. A multi-task, repeated campaign with live shared-KB user
identities would settle the population and end-to-end deployment claims.

## Rewrite inventory, 2026-08-25

The article was rewritten against `origin/testing` at `6bcc87e`. Existing
reporting above remains in place. This table records the disposition of every
first-party class used by the prior article.

| prior reporting | evidence class | disposition |
|---|---|---|
| test-node and API-key incident, cost under $10, route assembled across runs | author observation | **Split by audience.** Article Zero keeps the observed event, spend and release consequence. This article keeps the causal inference and missing cold-start comparison beside the isolation requirement. |
| S1 candidate deduplication and task admission | live two-service test | **Retained and superseded by a newer run.** The 2026-08-25 evidence target observed two failures, one candidate and one admitted task |
| S2 paired attribution at +1.000 over three tasks | live two-service test with seeded rows | **Retained.** The article says it proves plumbing and the three-pair guard, with no efficacy claim for the other loops |
| S3 dead-end recall | live two-service test | **Retained** |
| S4 `resolved 0 of 5` | live two-service test | **Superseded in prose.** The newer target observed one covered item resolve and one uncovered item remain open. The older result remains above |
| S5 supersession and operator regret | live two-service test plus direct record readback | **Retained** |
| S6 default `full` selection | live two-service test | **Superseded in prose.** The newer target forced and recorded non-default `brief`, and exposed the use-after-free described in the article |
| 28/0 learning and 13/0 liveness suites, plus registration-deletion controls | committed end-to-end tests | **Preserved above and removed from prose.** The article carries the later unified target at **46 passed, 0 failed** |
| missing provider registration, HTTP 200 error body and build-graph check | live deployment observation, run log and static source audit | **Retained and narrowed** |
| sqlite-shim query discrepancy | runtime test plus source audit | **Removed from prose as adjacent to the provider finding. Preserved above** |
| 75% of four exogenous, 0% of 25 exogenous, closed/open admission and `unavailable` | live full-stack test plus direct record readback | **Retained** |
| confidence multipliers, graph-fusion defects, co-occurrence collision and confirmation rewrite | live test plus source audit | **Moved to part two.** Part one keeps only the auditability consequence |
| temporal-learning rollout and defaults | static source audit and merged changes | **Removed from prose. Preserved above as release reporting outside the six-loop claim** |
| changeset seal 1 of 1, stripped control 0 of 1, crash rollback and idempotent restart | live fault injection plus structural checks | **Retained and updated** from `docs/validation/memory-changeset-worm-seal-2026-08-25.md` |
| prior-art survey and novelty framing | secondary historical review | **Removed from prose.** The article makes no novelty claim |
| benchmarking-series purpose | author statement and linked articles | **Removed from prose as unnecessary to the six-loop finding** |

The new live source is
`docs/validation/learning-loop-evidence-2026-08-25.md`: PostgreSQL 17.11,
pgvector 0.8.0, pg_trgm 1.6 and Python 3.13.5 on pvetest; command
`AIMEE_TEST_PG_URL=postgresql:///postgres make -C src learning-loop-evidence`;
result **46 passed, 0 failed**. Those environment details remain here because
they belong to the measurement, although the article no longer discusses a
storage backend.

## Matched large-repository failure cost, 2026-08-27

Source: `benchmarks/results/roi/large-repo-qwen38-expansion-r1.json` in Aimee
PR #2873, SHA-256
`b02243dcf615367cb05bf014dc9a7ce645f4b1a3d38cd5c993a2a97a848cb2ac`.
The preregistration record has SHA-256
`1941579dbfcb6ebe22eaf1016152b0f497fabf24e5384cc9b189794f77082a05`.
The derived inclusion record has SHA-256
`4c2c1ad12b86a8c3a6459d6613b66e5e226ca19da4c0af3aaf5fd5152d4c8b7a`.

The two retained pairs are `pool_lease_attribution` and
`clone_fd_and_owner`. Qwen-alone totals were 428,483 and 616,577 tokens. Aimee
totals were 371,687 and 321,292. Pooled totals are 1,045,060 and 692,979, a
352,081-token or 33.69002736684975 percent reduction.

Every retained cell failed the hidden grader and wrote no patch. The base
condition stopped at the context limit. The Aimee condition stopped under the
preregistered checkpoint, escalation and abort sequence after continued
retrieval without mutation. The treatment also passed canonical history
through the production Go economizer handler. This combined-condition result
does not attribute the reduction between those two mechanisms.

`db1_outcome_codes` is excluded because both conditions lacked a historical
generated-header fixture and failed the visible grader. Its cells remain in
the unchanged source artifact. The harness correction adds preregistered setup
commands, excludes their generated artifacts from candidate diffs and writes
an atomic per-cell checkpoint.

## Corrected DB1 pair and combined result, 2026-08-27

The DB1 rerun is
`benchmarks/results/roi/large-repo-qwen38-db1-fixture-r2.json`, SHA-256
`6fd07f599ae9069d19645318ac84d2783ead18877152dc4bfdc3c825da2e8aa7`.
Both conditions generated the registered fixture and passed the visible
grader. Qwen alone used 774,844 tokens and reached the context limit. Aimee used
506,573 tokens and stopped after the preregistered sequence. Both failed the
hidden grader and wrote no patch, producing a 268,271-token or
34.62258209394407 percent failure-cost reduction.

The combined calculation is
`large-repo-qwen38-valid-pairs-combined-analysis.json`, SHA-256
`987cfdfbc7b93ea2538f50bb7860b10b44471837116ad49a4a541162af7d02ec`.
Across the three retained pairs, Qwen-alone consumption is 1,819,904 tokens and
Aimee consumption is 1,199,552. The 620,352-token difference is
34.08707272471515 percent. All six cells failed the hidden grader. This remains
a combined economizer-and-progress treatment and supports no attribution
between those mechanisms.

The invalid DB1 pair above remains part of the append-only record. Its
measurement exclusion is unchanged; the corrected rerun supplies the valid
replacement.
