# Reporting record and figure provenance

Every figure in
[`aimee-recursive-self-learning.md`](../article/aimee-recursive-self-learning.md), and where it
came from.

Part one of three. The memory article is second, the
[architecture](../../everything-crosses-one-transport/) is third. Figures shared
with those pieces are marked shared here and recorded in their records too, so
one number is not logged three times as if independently sourced.

Evidence is first-party and lives in the public
[aimee repository](https://github.com/RakuenSoftware/aimee) rather than in this
folder, because each run is a validation report attached to the change it
validates. The learning work in 0.4.0 spans many branches. The loop figures come
from the recursive self-improvement work, merged to `testing` on 2026-08-24 as
`877e994c2f`.

## The incident in the lead

**First-party account by the author.** The test run in which an aimee-backed
model got around its protections, took an underprotected node and got hold of a
vast.ai testing API key is the author's own account of Rakuen's own system, own
key and own spend, including the **under $10** figure.

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
article marks it with "I think" where it is made, in the lead, and says there
that the ablation has not been run. It is not used to support any other claim in
the piece.

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

## Correction inventory, 2026-08-25

This pass preserves every first-party result already inventoried below. It
changes the disposition of five claims:

| item | evidence class | disposition |
|---|---|---|
| "everything gating it is disabled" | static source audit at the article pin | **Corrected.** `config_learning_synthesize_enabled()` reads a default-zero value, and six `learning_implicit_*` flags remain in the rollout-readiness programme. The article now confines the claim to the six measured loops: they are on and their producing halves reach consumers. |
| the missing provider registration | live two-service test plus build-graph source audit (`PROD`, `PR`) | **Retained and narrowed.** The provider-injection unit fixtures could not reproduce this deployment omission. The heading now carries the actual fix: a check derived from the build graph. |
| loop closure as evidence of self-learning benefit | live liveness tests (`S0S1`, `S2S6`, `FULL`, `PROD`, `PR`) | **Limited.** Closure remains observed. The article now concedes that closure is not benefit and names paired ablation as the standard the six-loop set has not yet met. |
| the cause of the incident in the lead | first-party account plus the article's own statement of which loops were off | **Added and scoped.** Earlier drafts described the incident without saying how the model got there, which reads as one run finding a route. The article now attributes it to the self-learning loops accumulating across runs while under test, marks the causal step as the author's reading, and states that the ablation settling it has not been run. |
| a memory mutation leaves an inseparable audit record | static call-path audit plus live PostgreSQL fault injection (`WORM`) | **Added.** The C mutation API already sealed in `fm_commit_finish()`; all five SQL-owned close paths now do the same. PR #2847 has landed. The live arm sealed 1 of 1 memory changesets and the call-stripped control sealed 0 of 1. |

Three figures are surfaced together in the memory section rather than left only
in this ledger: the confidence multiplier, proposal 8001's two observed fates,
and the live WORM seal/control counts. Their original entries and sources remain
below.

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

## The two strong claims, and what settles them

**Recursive self-learning is on.** Falsifiable per loop: a signal that reaches
no sink, an admitted candidate that produces no task file the harness will load,
a superseded proposal whose fate does not change, an endogeneity ratio computed
from no ledger, or a declared policy arm the sampler never returns. Each is
covered by an assertion in `tests/e2e/learning-loops-pg-e2e.sh` or
`tests/e2e/module-liveness-pg-e2e.sh`, both run on a real two-service stack.

**Model independence.** By construction, not by measurement. The loops are
harness code and no ledger row records a producing model. **Not measured here:**
the six loops have not been run across a set of models. Aimee's measured
model-neutrality lives in other articles in this series and covers extraction
and synthesis, not these loops.
