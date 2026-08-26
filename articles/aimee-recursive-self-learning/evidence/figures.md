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

## Rewrite inventory, 2026-08-25

The article was rewritten against `origin/testing` at `6bcc87e`. Existing
reporting above remains in place. This table records the disposition of every
first-party class used by the prior article.

| prior reporting | evidence class | disposition |
|---|---|---|
| test-node and API-key incident, cost under $10, route assembled across runs | author observation | **Retained with limits.** The model stays unnamed, the cause is marked as the author's inference, and the missing cold-start ablation is stated beside it |
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

## Narrative restoration inventory, 2026-08-25

PR review found that the 1,502-word rewrite reported the result but no longer
carried the original story from incident to containment to learning. The
article now runs 3,127 words against the original 4,313. No raw evidence was
removed or rewritten.

| narrative segment | restored treatment | claim boundary |
|---|---|---|
| test-node and API-key incident | **Restored as the lead** | under-$10 observation and accumulated route retained; causation remains an inference without the cold-start ablation |
| why isolation preceded learning | **Restored** | governed bus coverage and documented delegate containment are stated separately |
| six loop definitions | **Restored** | terminology shortened; no novelty claim |
| live observation per loop | **Restored in sequence** | current 46/0 target supersedes old per-suite counts and old S4/S6 observations |
| S6 use-after-free | **Retained** | live non-default `brief` selection and focused regression test |
| deployment graph failure | **Restored** | provider omission, misleading HTTP 200 body and non-vacuous build check retained; backend-specific adjacent defect remains outside prose |
| endogeneity gate | **Restored** | 75% of four, 0% of 25, closed/open admission and `unavailable` retained |
| memory as the learned state | **Restored** | witness validation updated with live, negative-control and restart results; backend names remain outside prose |
| why the loops were easier than memory | **Restored in compressed form** | memory failure examples remain factual; benchmarking-series purpose stays omitted |
| harness versus weight learning | **Restored as an engineering trade-off** | cross-model operation remains by construction and is not claimed as measured |
| falsifiability and valid no-op outcomes | **Restored** | closure is established; six-loop efficacy remains open |

## Harness-dependency argument, 2026-08-26

The article now states an architectural consequence rather than a measured
result: an agent process that loses access to the harness also loses access to
harness-owned learned state. The claim excludes the process's current context
and base checkpoint, and no escape experiment was run. The “months or years”
statement describes the possible age of a fixed checkpoint's training corpus,
not a measured age for one named model.

## Essay-structure revision, 2026-08-26

The article now runs **3,256 words** against the original 4,379-word source.
Review found that the previous revision still organised too much of the story
around the evidence target. The new sequence begins with the accumulated-route
incident, establishes isolation as the prerequisite, explains what changes when
a producer closes into a loop, follows the deployment-topology failure, and
then argues that learning belongs in memory and the harness. The 46/0 target is
retained as support for loop closure rather than as the article's subject.

The PostgreSQL-versus-test-substitute query discrepancy is restored because it
belongs to the same topology lesson as the missing provider registration. It
remains a runtime and source-audit finding already recorded above; no broader
claim about database implementations is made in the prose.

The harness-dependency claim is now stated in its strongest scoped form: an
agent escaping the harness loses everything *the harness learned*. Current
context and the provider checkpoint may remain with the process. Task files,
ledger history, retrieval state, policy evidence, failed approaches and later
corrections remain harness-owned. The argument compares that current local
state with a fixed checkpoint whose training corpus may be months or years
older; it makes no claim about the cutoff date of a named model.

No new efficacy or cross-model result is introduced. Closure remains observed
on the live two-service target, model independence remains by construction, and
the paired efficacy study remains open.

## Established containment patterns as the article's thesis, 2026-08-26

The opening now makes the author's central argument explicit. AI systems are
not the first software to cross intended boundaries, spread over networks or
acquire credentials. The article names the engineering response at the level of
stable, well-established practice: least privilege, process isolation, network
segmentation, mediated access, independent audit records and recovery.

The resulting aimee claim is scoped to the mechanisms reported across this
series. Grants bound governed event kinds; delegate isolation removes ambient
network and credential routes; mediated tools preserve required capability;
the harness retains learned state; and the ordered tap plus durable evidence
make governed actions observable and reconstructable from retained records.
The article does not claim visibility into model internals, complete coverage
of core-local or arbitrary external activity, or safety after total host
compromise.

The claim that capability and control can improve together is an architectural
argument. Memory and mediated tools improve the model's practical working
surface, while the same harness supplies provenance and enforcement points.
No new performance, efficacy or security measurement is asserted by that
passage.

The thesis addition brings the article to **3,527 words**. The earlier 3,256
word count remains above as the state before this review addition.

The general malware-response framing was checked against [NIST SP 800-83 Rev.
1](https://csrc.nist.gov/pubs/sp/800/83/r1/final), whose control families include
access control, audit and accountability, contingency planning, incident
response, system and communications protection, and system integrity. The
article uses that history as design context, not as evidence that aimee has
passed a malware-containment evaluation.

## Harness capability loss, 2026-08-26

The escape consequence now includes harness-mediated capabilities as well as
learned state. The architecture record for part three documents the one-socket
surface carrying memory, local code-index access, forge operations, mediated
web access and gate decisions. A process without continued access to that
socket cannot carry those capabilities with it.

The claim is deliberately asymmetric. An escape may obtain whatever ambient
route or host authority the exploit itself exposes; the article does not claim
that the escaped process has no capability. It claims that the accumulated
learning and named working surface remain harness-owned, making escape an
immediate loss of the system that turned the checkpoint into the practical
agent described here.

The final article is **3,635 words**. The added words carry the established
containment-pattern thesis and the immediate memory-and-capability cost of
leaving the harness; they do not add a new measured result.

## Causal sentence removed, 2026-08-26

At author direction, the prose no longer states that accumulated learning
explains the test-node result or discusses the missing ablation. It reports the
observed sequence: attempts left records, and the successful run began with the
record accumulated by earlier runs. The reporting record continues to note
that no ablation isolated accumulation from the other conditions. The article
now runs **3,613 words**.

## Deployment-topology section removed, 2026-08-26

At author direction, the provider-registration failure, build-graph lint and
SQL-fixture discrepancy no longer appear in article one. They remain preserved
in this reporting record as implementation evidence, but they interrupt the
essay's argument about containment, accumulated learning and the harness.

## Production-built framing restored, 2026-08-26

The introduction again states the author's account that aimee was built in
production, for production. The passage uses that provenance to explain the
design criterion: inspectable state, fail-closed authority, restart survival
and reversibility carry more weight than novelty or an isolated interesting
result. It is an author statement about the system's development context, not a
measured comparison with research systems.

## Capability and governability argument, 2026-08-26

The introduction now states the author's central design argument directly:
governability and auditability govern how capability is added; they do not
require a less capable system. Named routes, grants, typed failure and an audit
record add engineering work while preserving the capability. Memory likewise
increases practical ability while provenance, lifecycle and reversal keep the
new state maintainable. This is an architectural argument grounded in the
mechanisms reported across the series, not a measured comparison with an
ambient-authority implementation.

## Recursive-self-learning terminology restored, 2026-08-26

The introduction again makes the original terminology point: recursive
self-learning is ordinary self-learning, and updating a later attempt from the
outcome of an earlier one is a decades-old feedback-loop shape. The article
does not claim a new technical category or novelty for that mechanism. The
historical prior-art note above remains the support and claim boundary.

## Novelty criterion clarified, 2026-08-26

The production-built framing now states the author's rule precisely: novelty
had no role in selecting the mechanisms described in article one. A novel
approach is used only where no established approach will do. This supersedes
the earlier reporting phrase that production demands merely carried “more
weight” than novelty, which implied novelty still influenced those choices.

## Harness pressure and deterministic enforcement, 2026-08-26

The isolation section now separates model behaviour from harness enforcement.
The model remains nondeterministic. Governed effects enter the rest of the
system as typed events subject to ordinary rules: the host checks an event kind
against the attached grant, accepted traffic receives an order, and the tap
records that order before routing. “Deterministic” applies to those rules and
their specified outcomes. It does not claim a bug-free implementation, a
deterministic scheduler or visibility into model internals.

The task-pressure argument is architectural rather than a claim about
conscious intent. Task completion shapes model actions; a missing capability
can make the boundary itself an obstacle. The harness provides memory, compute,
code-index access, forge operations and approved network access through
governed routes. A process that leaves may retain its checkpoint, current
context and whatever access it found, while the learned state and mediated
working surface remain harness-owned.

The transport host is written in C. Dennis Ritchie's [history of the
language](https://www.nokia.com/bell-labs/about/dennis-m-ritchie/chist.html)
dates C's creation to 1969 through 1973, supporting “more than fifty years” in
2026. The choice of C is the author's design account already recorded in part
three: this part of the system needed explicit control over memory layout and
buffer lifetime. No comparative language benchmark or claim that all C
programs behave deterministically is introduced.

## Full voice and structure pass, 2026-08-26

The article remains an essay about containment, useful memory and production
self-learning. The deployed target and its **46 passed, 0 failed** result now
support the loop story in two paragraphs instead of organising it as a test
report. The state changes remain in prose: failure admission, approach recall,
curiosity no-op, supersession, operator regret and the seeded non-default policy
choice. The three-pair `+1.000` attribution detail remains recorded above and
was removed from the article because it did not change the claim that the
producer reached its consumer.

The memory-results table was also removed from prose because each consequence
is already carried by the surrounding account. Its exact confidence
multipliers, proposal fates and witness counts remain in this reporting record.
No raw artifact or first-party observation was removed. The article preserves
the incident, all six loop mechanisms, the live-path use-after-free, the
endogeneity gate, transactional witnesses, the memory failures, the
weights-versus-harness tradeoff, and the valid no-op outcome.

## Learning shared across model instances and users, 2026-08-26

The harness section now carries the positive half of model independence.
Weight learning belongs to the modified model artifact on which it occurred.
Two copies of the same starting checkpoint that learn from different local work
become two different learned artifacts; sharing their learning requires an
explicit weight or adapter distribution and coordination mechanism. A provider
update does not contain those local changes, and a different checkpoint cannot
inherit them merely by being loaded. The article does not claim that modified
weights are impossible to distribute. It distinguishes model deployment from
one live learned record shared at recall time.

Harness state is independent of both the checkpoint and the machine running a
model. Task files and ledger rows do not encode the producing model, so several
model instances can consume the same accumulated history even when their own
answers differ. This is a construction claim. No cross-machine comparison of
model outputs is introduced.

The cross-user claim follows the deployment shape already recorded above and in
part three: one shared knowledge service stands behind many per-user server
instances. Sharing remains subject to memory scope. Project and workspace
records stay inside their query-time visibility bands; records made shared or
global can be recalled by another permitted user. The article claims shared
learned state, not identical model outputs or unscoped access to another user's
memory.

## Local and institutional memory, 2026-08-26

The article now follows cross-user sharing to its organisational consequence.
Local memory remains attributable to the user and work that produced it. A
workspace can provide a team-level view, while shared or global scope can make
approved knowledge available across a wider organisation or company. The
query-time scope mechanism and per-user identity remain the enforcement basis;
the article does not claim that all memory is visible to every enrolled user.

Legal, engineering and sales are illustrative groups, not a measured customer
deployment. The stated benefit follows from the architecture: permitted users
and model instances query one governed knowledge service, records retain source
and scope, and shared records can cross group boundaries. “Unify” means those
groups can work from a common accumulated record. It does not mean their local
contexts, permissions or interpretations become identical.

The uniqueness statement is the author's scoped claim about AI harnesses, not
memory libraries or agent-development frameworks. The closest documentation
reviewed included LangGraph namespaced stores, Letta shared memory blocks and
Mem0 shared project memory. Those systems were excluded from the comparison
because they do not occupy the harness category meant by the claim. No
exhaustive census of AI harnesses exists here, so the article says “to my
knowledge” and defines the full shape: local user memory, scoped shared
institutional memory, model-independent consumption across machines, and
changes that remain attributable and reversible.

## Governability and observability require the harness, 2026-08-26

The article now distinguishes the accuracy of a library's own log from the
completeness and integrity of a system audit. A memory library can record the
calls it receives. It does not, by itself, control the model's credentials,
network routes, tools or alternate state paths, and therefore cannot establish
that an absent record means an action did not happen. If an agent can bypass
the library, the library cannot make the agent governable.

The harness claim rests on mechanisms already reported in this article and
part three. Grants constrain the governed event kinds a component can use; the
host assigns accepted traffic an order; the tap records it before routing; and
memory changesets commit with hash-chained witnesses. These properties do not
prove that bugs or host compromise are impossible. They place enforcement and
observation outside the learner's authority and make completeness a property
of the governed path instead of a promise from the component being observed.

An agent framework or memory library can participate in that design. Neither
can supply the end-to-end property alone because neither category owns the
model's complete execution and authority boundary. “True self-learning” and
“fully persistent memory” state the author's engineering standard: outcomes
change later behaviour through state whose access, provenance and reversal are
independently governed and observed. They do not claim that an ungoverned
memory cannot retain bytes or that a library cannot update a later prompt.

## Why weights cannot become institutional memory, 2026-08-26

The article now states the category boundary directly. Model weights can encode
information and change model behaviour. On their own they do not provide an
independent user identity, query-time workspace boundary, source record,
lifecycle or revocation path. Those properties require a system outside the
weights. Once that system supplies them and decides what each model instance
may receive, the relevant learning property lives in the harness.

The company consequence is an architectural inference. Putting organisational
knowledge into one checkpoint gives every deployment of that checkpoint the
same blended update. Maintaining different weight artifacts for different
groups restores separation by forking the learned state, which loses the common
live record. Harness memory can instead retain local and workspace state while
making shared or global records available to permitted users and model
instances. The claim is not that weights cannot memorise company information;
it is that weights alone cannot make that information a scoped, attributable,
reversible institutional memory shared across models and users.

## Duplicate-content reduction, 2026-08-26

After the model-sharing, institutional-memory and harness-governance arguments
were restored, the working article reached **3,959 words**. A full pass against
the voice guide reduced it to **3,417 words**, a 13.7% cut. The model-and-user
sharing section fell from 1,135 to 856 words by turning its repeated portability,
company-value, governability and escape arguments into one sequence.

The pass removed a second explanation of task pressure from the lead; the full
argument remains in the isolation section. It compressed the introduction's
repeated capability-and-control mechanism, removed a recap of memory lifecycle
consequences already established above it, and replaced the second account of
the policy use-after-free with the distinct no-op-versus-change result the final
section needed. The complete use-after-free sequence and fix remain in the loop
section.

No loop, incident, source audit, runtime observation or claim boundary was
removed. The article still carries the opening incident, the containment
response, all six loop mechanisms, deployed closure result, endogeneity gate,
transactional witness, memory failures, weight-learning concession,
cross-model and cross-user sharing, institutional-memory consequence,
uniqueness claim, library-log limit, escape cost and valid no-op outcome.

## Production criterion voice pass, 2026-08-26

The introduction now carries the same claims with a sharper progression:
recursive self-learning remains ordinary feedback, the component techniques
remain established, aimee remains a production-built assembly, and production
still selects for inspectable state, fail-closed authority, restart survival
and reversal. The pager language expresses the author's operating standard and
introduces no new incident or availability result. The ranking explanation for
the title remains an author statement.

## Recursive terminology paragraph restored, 2026-08-26

At author direction, the terminology paragraph from the preceding revision is
restored verbatim. Its wording carries the intended distinction between the
proposal's title, ordinary self-learning as a decades-old feedback loop, and
the candid reason `recursive` remains in the title. The surrounding production
criterion rewrite is unchanged.

## Model-sharing section split, 2026-08-26

The 837-word model-and-user section contained two complete arguments. It is now
split into **One learned history can serve many models and users** and **Only
the harness can make learning governable**, at approximately 450 and 360 words.
The uniqueness claim opens the second section because it applies to the full
harness shape rather than shared storage alone.

The light refinement removed a repeated announcement that all six loops close
and folded the checkpoint-age consequence into the escape comparison. The
article moved from **3,416 to 3,387 words**. No reporting or mechanism was
removed; the split changes navigation and paragraph pressure only.

## Development effort statement, 2026-08-26

At author direction, the article initially stated that the full harness took
almost a year, involved some very senior engineers and was easily the hardest
thing the author had built. An editorial pass later that day shortened the same
first-party account: it took almost a year, involved senior engineers and was the
hardest system the author had built. The comparison with the major cloud the
author helped build remains. The emphatic lead-in was removed.

The development effort and relative difficulty remain the author's personal
judgement, not a result inferred from repository history or a comparative study.
The cloud is deliberately unnamed and no independent scope or effort comparison
is claimed.

## Editorial structure pass, 2026-08-26

The lead now states what self-learning changes before the testing incident, and
identifies the author as one of aimee's builders. The production passage now
states that the incident happened on unreleased code and changed the release
condition: self-learning stayed off until its governed route existed.

The sentence about teaching each group the same company was replaced with the
identity-and-scope consequence it was meant to express. The valid no-change
section moved beside the other account of what later runs inherit, leaving the
harness section to close on the design criterion supplied by the incident. The
original isolation section keeps its scope, related failure sentences were
consolidated, and the development-effort statement now follows the mechanism
whose effort it describes. No measurement, mechanism or scope claim changed.

The section-balance pass added a heading to the previously unheaded containment
context, merged the valid no-change material into the account of what later runs
inherit, and separated model portability from company-wide sharing. It moved no
prose and changed no claim.

## Self-learning terminology and compression, 2026-08-26

At author direction, the article calls the deployed capability self-learning
and removes the numbered-loop specification. The exact live observations,
endogeneity ratios, admission controls and policy-selection use-after-free
remain in this reporting record and in
`docs/validation/learning-loop-evidence-2026-08-25.md` in the aimee repository.
The article retains the **46 checks** and the boundary between observed state
change and unmeasured efficacy.

The statement that the mechanisms were easy to sketch has also been removed.
It was an authorial comparison, not a measured development-effort claim.

## Paired outcome study, 2026-08-26

The outcome figure, now carried in part two, comes from
[Aimee PR #2859](https://github.com/RakuenSoftware/aimee/pull/2859) and its
validation report, `docs/validation/self-learning-efficacy-2026-08-26.md`.
The raw outputs from both valid runs are preserved in
[`raw/self-learning-efficacy-2026-08-26/`](raw/self-learning-efficacy-2026-08-26/).

Both conditions received the same two failed observations for each of 24
repeated tasks. The control withheld synthesis before consumption. The
treatment ran production synthesis and read the result through production
recall. A fixed consumer began with the same choice in each condition and
changed it only when recall identified that choice as failed. Another 24 tasks
had no matching history.

| figure in article | result |
|---|---:|
| repeated tasks without the learned failure record | 12/24 |
| repeated tasks with the learned failure record | 24/24 |
| novel tasks, both conditions | 12/24 |

There were 12 treatment-only successes and no control-only successes. The
exact two-sided McNemar p-value was 0.00048828125. Two valid runs passed 12
harness checks with no failures and produced byte-identical cell-level CSVs,
SHA-256
`250a617ff71ad3f069fdd5bd9c82ebc142f3e694693fb368c971706abafaf62c`.

This establishes an outcome change for the controlled failed-approach case. It
does not measure model reasoning or open-ended generalisation. Three earlier
attempts were excluded: one stopped at database setup, one at readiness, and
one produced the same cell results but failed three reporting assertions. The
Aimee validation report records each disposition.

## Part-one memory trim, 2026-08-26

The section specifying fact classes, lifecycle operations and transactional
witness behaviour has been removed from part one at author direction. Those
details belong to part two. Their evidence remains in this reporting record;
none of it supports the new paired-study figure.

## Readability pass, 2026-08-26

The article's section hierarchy, claims and evidence boundaries remain in
place. The pass shortened transitions, replaced ambiguous pronouns and kept one
subject in each paragraph. The list of memory implementation defects left part
one; those defects remain in part two and in the figure inventory above. No
measurement or raw artifact changed.
