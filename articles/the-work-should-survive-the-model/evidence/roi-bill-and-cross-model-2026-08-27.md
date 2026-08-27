# Bill-equivalent and cross-model ROI evidence, 2026-08-27

This note extends the 26 August token analysis without altering its append-only
raw artifact. It adds a category-priced calculation and records the exploratory
failure-learning pilot used in Article Zero.

## API-price-equivalent cost per passing task

The preserved E6 streams report uncached input, cached input and output
separately. On 27 August 2026, the
[official GPT-5.6 Sol model page](https://developers.openai.com/api/docs/models/gpt-5.6-sol)
listed $4.00 per million uncached input tokens, $0.40 per million cached input
tokens and $20.00 per million output tokens. Every E6 request contained fewer
than 272,000 input tokens, so the model page's long-context multiplier does not
apply.

| category | standard | Aimee on | price per million |
|---|---:|---:|---:|
| uncached input | 242,514 | 243,724 | $4.00 |
| cached input | 873,216 | 802,304 | $0.40 |
| output | 19,550 | 16,178 | $20.00 |
| passing tasks | 5 | 6 | |

Calculation:

```text
standard total = (242,514 * $4 + 873,216 * $0.40 + 19,550 * $20) / 1,000,000
               = $1.7103424
standard per pass = $1.7103424 / 5 = $0.342068480

Aimee-on total = (243,724 * $4 + 802,304 * $0.40 + 16,178 * $20) / 1,000,000
               = $1.6193776
Aimee-on per pass = $1.6193776 / 6 = $0.269896267

relative change = ($0.269896267 / $0.342068480) - 1
                = -21.098762%
```

The article publishes this as a **21.1 percent lower API-price-equivalent bill
per passing task**. The runs used subscription authentication rather than
metered API billing, so this is not an observed invoice charge. The official
page describes the listed rates as promotional through at least 21 November
2026. The rate and retrieval date remain attached to the calculation so it can
be repriced later.

The 22.0 percent figure remains valid for provider-recorded billable token units
per passing task. It is not used as the exact dollar reduction because the
categories have different rates.

## Stopped failure and transferred lesson

The source artifact is
`benchmarks/results/roi/large-repo-qwen38-trust-progress.json` in Aimee PR
[#2873](https://github.com/RakuenSoftware/aimee/pull/2873), SHA-256
`9f33c6e1949a1e53fab48ec7ea2baf50f92c1d8c60500b391d6f8b9ee4e1cbb4`.
The local Qwen3.8-27B run stopped after 28 successful non-mutating calls, nine of
which repeated or overlapped retrievals. It recorded 512,545 provider tokens
and produced no patch.

An earlier recorded plain failure used 577,214 tokens. The difference is
64,669 tokens, or 11.2 percent. This is descriptive only. A fresh plain arm
diverged and reached its context limit at 333,390 tokens, so the evidence does
not support a stable paired 11.2 percent savings estimate.

The stopped failure yielded this sealed lesson:

> Broad repository exploration with repeated or overlapping retrievals and no
> edit failed. On a similar goal, choose a materially different plan, form a
> concrete defect hypothesis, and attempt the smallest justified edit or
> decisive test before broadening exploration.

The cross-model record is
`benchmarks/results/roi/cross-model-shared-learning-pilot.json` in the same PR,
SHA-256
`f28de14812700b90aa2a03e9457c404040a5597a7574e899d4b77c30b6b1e64d`.
For each Codex model, base and learned arms used separate worktrees at the same
buggy revision, the same task, medium reasoning and the same visible and hidden
grader. Only the learned arm received the Qwen-derived lesson.

| model | base | learned | disposition |
|---|---|---|---|
| GPT-5.6 Luna | produced code and tests; stopped verification early; independent visible grader did not link | completed a full server build and ran the focused test; final visible and hidden graders failed | **Capability crossover, published with failure.** The lesson increased implementation and verification depth but did not complete the task. |
| GPT-5.6 Terra | self-selected and visible tests passed; hidden grader failed | visible and hidden graders passed; authored test-only patch failed on the buggy parent | **Completion crossover, published as exploratory.** The learned arm completed a regression-sensitive repair the base arm missed. |

A learned retry with the originating Qwen model also failed after 519,662
tokens, 1.4 percent more than the source failure. It is retained as a negative
result. The system-level value in this pilot came from later Luna and Terra
behaviour, not a universally successful advisory.

The collaboration runtime did not expose token-usage objects for the Luna and
Terra arms. The pilot therefore supports capability claims, not a token-saving
claim for those arms.

## Shared-KB claim boundary

The controlled pilot supplied the lesson unchanged to the learned arms. It did
not exercise a live multi-user retrieval route during those four runs.

The product path is covered separately by storage-backed tests. Approach
failure records live in the shared Aimee KB. Source, session and model identity
are provenance fields rather than recall filters. The test records the first
failure under `user-a/session-1/qwen-local`, reinforces it under
`user-b/session-9/terra`, recalls it for a similar goal, and excludes an
unrelated goal. Authorisation still determines which KB and scope a caller may
read.

The supported combined statement is that the lesson changed work across models
in the controlled pilot, and the deployed storage mechanism makes such records
reusable by later authorised users and models on the same KB. It is not a claim
that the pilot itself exercised multiple live user identities.

## Production breadth

Rakuen reports current production use across legal, accounting, software and
other professional work. This is a first-party operator statement recorded on
27 August 2026. Customer identities, corpora and usage records are not disclosed.

The production statement establishes domain breadth, not a causal efficacy
estimate in each domain. The cross-model completion crossover is a controlled
software task because a sealed hidden grader and regression-sensitive test make
the outcome independently checkable.

## Closest academic result

[Recuris](https://arxiv.org/abs/2608.24876) is an implemented experimental
system, not a theoretical proposal. It evolves a benchmark-specific skill-memory
package from one deployment model and loads the package unchanged into frozen
target models. It reports task-success gains across four long-horizon benchmarks
and ten models.

The paper does not present or evaluate an organisation-scoped production
knowledge service with multiple user identities, access-scoped recall, durable
record provenance and correction, independent execution and credential
isolation, or a tamper-evident audit path. Its experiments use controlled
benchmarks rather than current production users in multiple professional
domains.

The articles therefore do not claim that Aimee invented cross-model memory or
first demonstrated a performance effect from it. Their narrower distinction is
that Aimee integrates cross-model experiential learning into a production,
customer-controlled and governed organisational system, and the current pilot
shows a Qwen-derived failure lesson changing completion of a real repository
repair by another model tier.
