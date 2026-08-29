# Evidence inventory for the working paper

Working title: *From Failed Run to Shared Capability: Production-Grade
Organisational Memory Across Heterogeneous Language-Model Agents*.

This inventory was created before drafting the paper. It preserves positive,
negative and invalid results and defines the novelty boundary.

Every Aimee path below is read at commit
[`faaf05298ce4d3b484f24cb00ccc402c62128e69`](https://github.com/RakuenSoftware/aimee/tree/faaf05298ce4d3b484f24cb00ccc402c62128e69),
the merge of Aimee PR
[#2873](https://github.com/RakuenSoftware/aimee/pull/2873) into `testing` on
2026-08-28. Every SHA-256 recorded here was reverified against that commit on
2026-08-29.

## First-party system and experiment sources

| key | source | evidence class | disposition |
|---|---|---|---|
| `LOOPS` | `docs/validation/learning-loop-evidence-2026-08-25.md` in the Aimee repository | live two-service PostgreSQL target, 46 passed and 0 failed | **Use for system closure only.** Does not establish efficacy. |
| `EFFICACY` | `docs/validation/self-learning-efficacy-2026-08-26.md` | paired deterministic consumer study with fresh databases | **Primary causal result.** Repeated tasks 12/24 control and 24/24 treatment; novel tasks 12/24 in both; exact McNemar p = 0.00048828125; second valid run byte-identical. |
| `QWEN-STOP` | `benchmarks/results/roi/large-repo-qwen38-trust-progress.json`, SHA-256 `9f33c6e1949a1e53fab48ec7ea2baf50f92c1d8c60500b391d6f8b9ee4e1cbb4` | local Qwen3.8-27B provider-backed large-repository run | **Source failure.** Stopped after 28 non-mutating calls, including nine repeated or overlapping retrievals; 512,545 provider tokens; no patch. |
| `CROSS` | `benchmarks/results/roi/cross-model-shared-learning-pilot.json`, SHA-256 `f28de14812700b90aa2a03e9457c404040a5597a7574e899d4b77c30b6b1e64d` | matched exploratory cross-model coding pilot | **Primary open-ended result.** Luna capability crossover without completion; Terra hidden-grade completion crossover with a regression-sensitive test. One task and one run per arm. |
| `QWEN-RETRY` | `benchmarks/results/roi/large-repo-qwen38-trust-learned-retry.json`, SHA-256 `ab15d4e3aec6e1067f514b9677cacc00ecb0fc8e255e289b18aba7d3ef68ca13` | learned retry on originating local model | **Required negative result.** Failed after 519,662 tokens, 1.4% above the source failure. |
| `FAILCOST-3` | `benchmarks/results/roi/large-repo-qwen38-valid-pairs-combined-analysis.json`, SHA-256 `987cfdfbc7b93ea2538f50bb7860b10b44471837116ad49a4a541162af7d02ec`, over `large-repo-qwen38-expansion-r1.json` (`b02243dcf615367cb05bf014dc9a7ce645f4b1a3d38cd5c993a2a97a848cb2ac`) and `large-repo-qwen38-db1-fixture-r2.json` (`6fd07f599ae9069d19645318ac84d2783ead18877152dc4bfdc3c825da2e8aa7`) | three matched same-model large-repository pairs with a sealed hidden grader | **Failure-cost result.** Pooled consumption 1,819,904 control and 1,199,552 treatment, a 34.1% reduction. All six runs failed the hidden grader, so this is cost containment, not capability. Combined economizer and progress treatment; no attribution between the two. |
| `SHARED-KB` | `src/tests/test_approach_memory.c`, SHA-256 `cf7f63af2d65684308941fc8cccf3594c1fb07653d28d8d81bb9fb38da947d0e`, and `src/headers/approach_store.h`, SHA-256 `b2b42a861ce749a27ecbfa893881072c4f7a69d5d26338eae4edda1a3af5fde1` | storage-backed product test and API contract | **Mechanism evidence.** Different user/session/model sources reinforce and recall one similar-goal record inside an authorised KB. The cross-model pilot injected the lesson directly rather than exercising live user identities. |
| `E6` | `benchmarks/code-agent-effectiveness/results/e6-20260730-provider.json` plus 16 hashed provider streams; analysis in Article Zero evidence | paired eight-task GPT-5.6 Sol study with hidden-test outcomes | **Economic result.** Five passes standard, six Aimee-on; 22.0% fewer billable token units and 21.1% lower API-price-equivalent cost per passing task at 2026-08-27 rates. Subscription authentication means price-equivalent, not observed invoice. |
| `QWEN-PLAIN` | earlier recorded same-task plain failure at 577,214 tokens and fresh divergent plain arm at 333,390 tokens | non-stable failure comparisons | **Descriptive only.** The stopped run is 11.2% below the earlier failure, but the fresh arm context-failed earlier; do not estimate a paired savings effect. |
| `DELEGATE-50` | `benchmarks/results/cost_savings/lite50.json` and `.perinstance.json` | 50-task frontier-model ledger comparison | **Supporting only.** 58.6% frontier-token displacement; worker tokens and correctness absent. Not total savings. |
| `PRODUCTION-BREADTH` | Rakuen operator statement, 2026-08-27 | confidential first-party deployment account | **Context only.** Current use across legal, accounting, software and other professional work. No customer identities, records or cross-domain efficacy estimate. |

## Cross-model pilot matrix

| model | base arm | learned arm | supported interpretation |
|---|---|---|---|
| GPT-5.6 Luna | production and test patch; stopped verification early; independent visible grader did not link | full server build and focused-test execution; visible and hidden final grade failed | transferred lesson increased implementation and verification depth, not task completion |
| GPT-5.6 Terra | own tests and visible grader passed; sealed hidden grader failed | visible and hidden graders passed; authored test-only patch failed on buggy parent | transferred lesson converted a hidden-grade failure into a regression-sensitive completion |

Both pairs used the same buggy revision, task, medium reasoning and independent
grader within the model. The learned arm alone received the unchanged lesson
derived from `QWEN-STOP`.

The runtime did not expose provider token-usage objects for Luna or Terra. The
matrix supports no cost claim for those arms.

## Matched failure-cost campaign

| task | languages | Qwen alone | Aimee | reduction | control stop | treatment stop |
|---|---|---:|---:|---:|---|---|
| `pool_lease_attribution` | C | 428,483 | 371,687 | 13.26% | context limit | progress abort |
| `clone_fd_and_owner` | C | 616,577 | 321,292 | 47.89% | context limit | progress abort |
| `db1_outcome_codes` | C, Go, JSON | 774,844 | 506,573 | 34.62% | context limit | progress abort |
| pooled | | 1,819,904 | 1,199,552 | 34.09% | | |

Every pair used the same model, buggy revision, prompt, tools, limits and sealed
hidden grader. All six cells failed the hidden grader and wrote no patch, so the
campaign supports **failure-cost containment only** and no capability claim.

The treatment applied context reduction through the production economizer
handler and the preregistered checkpoint, escalation and abort sequence
together. **The 620,352-token difference is not attributed between those two
mechanisms.**

The first `db1_outcome_codes` pair lacked a required historical generated-header
fixture and failed the visible grader in both conditions. Its cells remain
unchanged in `large-repo-qwen38-expansion-r1.json` and are excluded from
measurement. The corrected rerun in `large-repo-qwen38-db1-fixture-r2.json`
generated the fixture in both conditions, passed the visible grader in both and
supplies the retained third pair.

## Related-work boundary

| work | primary source | what it establishes | distinction from this paper |
|---|---|---|---|
| Reflexion | [Shinn et al., 2023](https://arxiv.org/abs/2303.11366) | verbal feedback in an episodic buffer improves subsequent trials without weight updates | primarily an agent's own trial-and-error memory, not an organisation-scoped, governed, cross-user production substrate |
| ExpeL | [Zhao et al., 2023/2024](https://arxiv.org/abs/2308.10144) | extracts natural-language knowledge from training-task experiences and reuses it at inference | experiential learning and transfer precede Aimee; production identity, authorisation, isolation and audit are outside its evaluated claim |
| INMS | [Gao and Zhang, 2024/2026](https://arxiv.org/abs/2404.09982) | asynchronous shared conversational memory among agents improves three datasets | precludes any broad first claim for shared or cross-agent memory; does not evaluate durable organisational governance or a real repository failure-to-completion path |
| Learning to Share | [Fioresi et al., 2026](https://arxiv.org/abs/2602.05965) | learned admission to a global memory bank reduces runtime in parallel agent teams while maintaining or improving benchmarks | memory is shared within parallel execution; not a durable cross-run record transferred from a failed source model to later users and models |
| Negative Knowledge | [Wang, 2026](https://arxiv.org/abs/2606.21024) | typed failure records improve same-task and cross-task scientific research while reducing tokens | closest failure-memory motivation; reported evaluations are research-agent settings and do not establish heterogeneous-model, cross-user production governance |
| Recuris | [Yu et al., 2026](https://arxiv.org/abs/2608.24876) | evolves one benchmark-specific skill-memory package from a deployment model and loads it unchanged into frozen target models, improving 35 of 37 completed model-benchmark pairs | closest cross-model performance prior art and fatal to a broad first claim; does not present an organisation-scoped production service with user authorisation, provenance/correction, isolated execution or tamper-evident audit |
| Cross-Model Memory Transfer | [Li et al., 2026](https://arxiv.org/abs/2608.17050) | transfers a learned Engram table between backbones, often with target-side reader adaptation | parametric-adjacent stored knowledge and QA evaluation, not experiential failure memory shared among operational agents |
| Structurally Aligned Subtask-Level Memory | [Shen et al., 2026](https://arxiv.org/abs/2602.21611) | software-agent memory aligned to subtasks improves SWE-bench Verified across backbones | relevant software-memory baseline; does not make the full organisational production-system claim |
| Experience-Following Behavior | [Xiong et al., ACL 2026](https://aclanthology.org/2026.acl-long.27/) | similar recalled experiences induce similar outputs; poor memories propagate errors and can be misaligned | motivates Aimee's provenance, correction and evidence gates; it is a safety boundary rather than novelty support |

## Citation verification, 2026-08-29

Every work in the boundary table above was checked against its primary source
on 2026-08-29 and the paper now carries a complete reference list with authors,
titles, identifiers and dates.

Two defects were corrected. The subtask-level memory entry had no author
recorded and is now attributed to Shen, Zhang, Sun, Zeng and Yue. The Recuris
entry cited a system name without its paper title, which is *Recursive
Experiential-Working Memory Evolution for Long-Horizon Agent Harnesses* by Yu
and seven co-authors; its abstract confirms the four benchmarks, ten models and
35 of 37 completed model-benchmark pairs the paper reports.

ExpeL is published at AAAI-24 rather than arXiv alone, and the ACL
experience-following study is at pages 623-645 of the ACL 2026 long-paper
proceedings. Both are recorded in the reference list.

## Novelty claim allowed by the evidence

The paper must not claim to be the first demonstration that experiential memory
can improve another model. Recuris and INMS preclude that claim, while ExpeL,
Reflexion and Negative Knowledge establish substantial earlier memory-based
learning.

The defensible contribution is a systems claim:

> A production-oriented, customer-controlled organisational learning substrate
> converts operational failures into durable, provenance-bearing and
> access-scoped records; exposes them to unchanged heterogeneous agents; keeps
> execution and audit authority outside the learner; and demonstrates the path
> from a stopped local-model failure to a hidden-graded repair completed by a
> different model tier.

The paper may say that the authors found no prior work documenting this complete
combination. It must describe the review as bounded, not exhaustive, and must
not equate absence in a paper with absence in all private systems.

**Satisfied, 2026-08-29.** Section 1 now states that the review covers published
literature and available public product documentation, that absence from the
published record is not evidence of absence, and that no claim is made about
unpublished or private systems. Section 6 repeats the limit as a threat to
validity.

## Invalid and negative evidence that must remain visible

- Three invalid `EFFICACY` attempts remain excluded for documented setup or
  harness failures. One produced the same scores but failed harness assertions
  and is not counted.
- The learned Qwen retry did not improve and used 1.4% more tokens.
- Luna's learned arm did not pass either final grader.
- A fresh plain Qwen arm context-failed at 333,390 tokens, preventing a stable
  paired estimate for the 11.2% stopped-run comparison.
- Every run in the matched failure-cost campaign failed its hidden grader. The
  34.1% reduction is cost containment on unproductive trajectories and is not
  evidence of capability.
- The first `db1_outcome_codes` pair remains quarantined in its original
  artifact for a missing build fixture and is excluded from measurement.
- The cross-model pilot has one task and one run per arm.
- The cross-model arms did not use live multi-user retrieval and expose no
  provider token-usage data.
- Production breadth is first-party and confidential; it is not a quantified
  multi-domain efficacy study.

## Required next experiment

Extended 2026-08-29. Section 7 of the paper gained two subsections the earlier
design omitted: 7.3 recall generalisation and near-miss controls, which the
matching-description limit on `EFFICACY` makes necessary, and 7.4 mechanism
attribution for `FAILCOST-3`, whose combined economizer-and-progress treatment
leaves its 34.1% unattributed. The article README carries the full sequenced
experiment plan, including the deterministic studies that need no provider spend
and the two prerequisites gating the hosted work.

A submission-grade confirmatory study should preregister tasks, exclusions,
budgets, stopping rules and graders; use multiple large repositories and task
languages; cross several source and consumer models; repeat every arm; route
learned records through distinct live user identities on one shared KB; record
all billing categories; include poisoned, stale and unrelated-memory controls;
and report completion, regression sensitivity, token cost, wall time, recall
precision, security leakage and negative transfer.
