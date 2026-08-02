# Reporting record: token compression rewrite

Date: 2026-08-02

Status: draft complete; publication hold for right of reply.

This file records the load-bearing sources, calculations, source limits and
outstanding reporting for the rewritten article. It is not itself evidence that
any compression product changes a user's bill.

## Form and interests

The article is reported analysis. Measurements and observed source behaviour
are attributed. The interpretation and recommendation belong to Rakuen
Software.

Rakuen Software builds `aimee`, an agent server that competes for some of the
same users by managing memory, context, model routing and budgets. The article
discloses that interest next to its opening finding and applies the same paired
measurement requirement to `aimee`.

## Load-bearing sources

### GPT-5.6 price and cache behaviour

- OpenAI, "GPT-5.6: Frontier intelligence that scales with your ambition",
  2026-07-09:
  <https://openai.com/index/gpt-5-6/>
- OpenAI, "Model guidance", accessed 2026-08-02:
  <https://developers.openai.com/api/docs/guides/latest-model>
- OpenAI, "Unrolling the Codex agent loop", accessed 2026-08-02:
  <https://openai.com/index/unrolling-the-codex-agent-loop/>

OpenAI states that GPT-5.6 cache writes cost 1.25 times ordinary input and cache
reads receive a 90% discount. It also documents exact-prefix matching, explicit
breakpoints, `cached_tokens` and `cache_write_tokens`.

### Break-even calculation

For an already-cached suffix of `x` tokens:

- next cached read: `0.10x`
- rewritten compressed suffix: `1.25(1-r)x`
- break-even: `1.25(1-r)x <= 0.10x`
- result: `r >= 0.92`

This is an illustrative calculation from OpenAI's published multipliers. It
applies only when the edit forces that suffix to be written and compares the
next request. It is not a claim about every compression operation.

### Growing-history turn calculation

For a fixed block of `c` tokens retained across `n` later calls, the additional
input traffic is `nc`.

For a base prompt of `b` tokens and `d` new live tokens added on each of `n`
turns:

- per-turn input: `b + kd`
- cumulative input: `T(n) = nb + d n(n+1)/2`

The quadratic term follows from replaying a history that grows on every turn.
It is an illustrative workload model, not a provider price formula. Compaction,
truncation, eviction, variable turn sizes and cache categories change realised
traffic and cost.

### Cache-aware compression

- Yan Song, "Cache-Aware Prompt Compression: A Two-Tier Cost Model for LLM API
  Caching", submitted 2026-07-17:
  <https://arxiv.org/abs/2607.15516>

Figures used: tau-bench retail, 50 tasks, 36/50 successful for both CAPC and
vanilla, CAPC 7.9% cheaper than vanilla, query-aware compression 40.1% more
expensive. These are author-reported preprint results on Sonnet 4.6 with a
five-minute cache policy. The paper says provider-specific figures need
remeasurement.

### RTK

- RTK 0.43.0 source, commit `5a7880d404db8364d602f2ecdc41dd790f64013f`:
  <https://github.com/rtk-ai/rtk/tree/5a7880d404db8364d602f2ecdc41dd790f64013f>
- RTK development README, commit
  `e0ffd40ef7c450489aca4a50c0ab1358e4375691`, dated 2026-08-01:
  <https://github.com/rtk-ai/rtk/blob/e0ffd40ef7c450489aca4a50c0ab1358e4375691/README.md#how-savings-work>
- Denis Shiryaev, JetBrains, "Does rtk skill really cut agent tokens by
  60-90%? We tested it", 2026-07-20:
  <https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/>

Figures used: 80 clean low-effort pairs; median task cost +7.6% (`p=0.004`),
turns +13.8% (`p=0.03`), cache reads +14.3% (`p=0.008`); high-effort task cost
+0.1% (`p=0.99`); quality tied in both arms. These are JetBrains measurements
of RTK 0.43.0 with Claude Code 2.1.201 and Claude Sonnet 5, not GPT-5.6.

Structural findings used: Claude Code's built-in `Read` and `Grep` tools bypass
the Bash hook; its native output limit would truncate a 1.2 MB `cat` result to a
few thousand tokens; RTK counted about 320,000 tokens saved for that command;
and `rtk gain` reported 96.2 million tokens saved across the low-effort run while
the measured bill increased. JetBrains also found a broken compound-`find`
rewrite, compression-induced re-reads and additional turns. These findings
support client-pipeline interaction, not randomness inside RTK's filters.

The current development README explicitly limits its percentage to Bash output
and says it is not a bill reduction. The article includes that clarification.

### Headroom

- Headroom source, commit `6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9`,
  dated 2026-08-01, version field 0.33.0:
  <https://github.com/headroomlabs-ai/headroom/tree/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9>
- Prefix replay:
  <https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/cache/prefix_tracker.py#L267-L368>
- CCR retrieval continuation:
  <https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/ccr/response_handler.py#L420-L529>
- OpenAI cache-write inference:
  <https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/proxy/handlers/openai.py#L1246-L1257>
- OpenAI manual price fallback:
  <https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/providers/openai.py#L530-L587>
- Vendor benchmark summary:
  <https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/README.md#proof>

The article does not claim that Headroom necessarily breaks prompt caching. The
reviewed source contains explicit prefix-freezing and byte-replay measures.

The reviewed CCR handler also establishes the additional-turn mechanism. When
the model calls `headroom_retrieve`, it retrieves the full original, appends a
tool result and makes a continuation API call. The default
`max_retrieval_rounds` is three. This proves that retrieval can add model calls
by design. It does not establish a real-task retrieval rate or the frequency of
other corrective turns.

The article identifies two narrower GPT-5.6 accounting mismatches. One code
path infers writes and says OpenAI has no write premium. A manual fallback
prices cache reads at 50% of input. The article also states the limits of that
finding: LiteLLM may supply current pricing, other response paths may supply
exact usage, and these code paths do not prove every dashboard number wrong.

No independent, paired GPT-5.6 completed-coding-task cost benchmark for
Headroom was found in the source review or web search completed on 2026-08-02.
This is a statement about the reporting search, not the world.

### Codex trace account

- Reddit user `ikhDark`, "Important Findings On Cache and Baked In Codex Code",
  2026-07-24:
  <https://www.reddit.com/r/codex/comments/1v4vawj/important_findings_on_cache_and_baked_in_codex/>

Figures used: ten rollouts, 252.2 million total tokens, 251.7 million input
tokens, 2,007 model calls, 125,394 average input tokens per call, 290 average
output tokens per call, 97.818% weighted cache rate.

This account is single-sourced. Raw traces were not obtained and the analysis
was not independently reproduced. It does not reveal Codex subscription
metering and cannot establish a billing or quota bug. The article states all
three limits before interpreting the reported workload shape.

## Prior first-party reporting remains in the record

The complete disposition is in
[`first-party-testing-2026-08-02.md`](first-party-testing-2026-08-02.md). The
article reports the author's two-day reseller investigation, the 6.1
million-token local RTK counter observation, the RTK 0.43.0 pytest reproduction,
and the pinned RTK and Headroom source audits. It states which work was a
runtime observation and which was static review.

The raw invoices, provider usage export, RTK analytics export, terminal output
and pytest fixture were not present in the migrated article folder. The article
discloses that limit where each result appears. Those observations cannot carry
a universal claim or numerical effect size, but missing raw support is not a
reason to erase prior reporting.

The rewrite still removes the categorical instruction to delete every
compression plugin. The cache-aware-compression preprint supplies a measured
counterexample. It also removes claims about unspecified reseller differences
and controls allegedly hard-coded off in Codex because the prior article did
not preserve a basis for them. Their removal is recorded here rather than left
silent.

## Raw artifacts are append-only

The repository-wide rules are in [`articles/AGENTS.md`](../../AGENTS.md). New
raw reporting output belongs under `evidence/raw/` with its command, version,
fixture, environment and outcome. A later correction marks an artifact invalid
and points to the superseding run. It does not overwrite or silently remove the
original. Deletion requires a recorded reason and explicit user approval.

## Right of reply required before publication

No external messages were sent as part of this rewrite. Before republication,
send the specific claims with a response deadline to RTK, Headroom and OpenAI.
Record the replies where they bear, or record that no reply arrived by the
deadline without implying why.

Questions for RTK:

1. Does RTK dispute JetBrains' interpretation of the 0.43.0 low- or high-effort
   results?
2. Does the current project claim any reduction in provider cost, beyond the
   documented reduction in Bash output?
3. Does RTK account for project-level pytest `addopts` when deciding whether to
   add `-q`, and can 0.43.0 misreport a run when the effective option is `-qq`?
4. How does `rtk gain` account for output the host client would have truncated
   or transformed without RTK, and for retries or re-reads caused by a rewrite?

Questions for Headroom:

1. Which current code path reads GPT-5.6 `cache_write_tokens` and prices those
   writes at 1.25 times input?
2. Does Headroom have a paired GPT-5.6 benchmark reporting cost per successful
   coding task, including retrievals and extra turns?
3. Do Headroom's coding-agent benchmarks report CCR continuation rounds and
   non-CCR re-reads or corrective turns separately from local token reduction?
4. Does Headroom adapt its compression policy or back off based on
   completed-task cost and quality segmented by client, provider and model?

Questions for OpenAI:

1. How does Codex subscription metering treat cached input, cache writes and
   child-agent usage?
2. Which user controls currently exist for cumulative input, model calls,
   child-agent use, tool-output retention and compaction timing?
