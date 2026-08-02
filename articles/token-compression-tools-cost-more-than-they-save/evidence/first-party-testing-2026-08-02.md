# First-party testing inventory

Date reconstructed: 2026-08-02

Status: retained reporting; mixed evidentiary weight.

This inventory preserves the first-party work behind the original article and
the 2 August rewrite. It distinguishes runtime observations from static source
audits. None of these items is a paired cost-per-success benchmark.

No raw invoices, provider usage export, RTK analytics export or pytest fixture
was present in the article directory when it was migrated into this repository.
That absence limits those results. It does not justify deleting their existence
from the reporting record.

## Anthropic reseller billing reconciliation

The original article recorded a two-day investigation into an Anthropic
reseller bill. It said the author compared the reseller's charges with its rate
card, then examined the same cache mechanism on GPT-5.6 and the OpenAI API. It
also recorded this result: in every case measured, the cost of losing cached
input exceeded the saving attributed to removed text.

Available artifact: the contemporaneous pre-rewrite article at repository
commit `8c27834`, lines 9-27. The invoices, request traces, reseller identity and
case table were not archived with the migrated article.

Permissible claim: this is a first-party billing observation that produced the
hypothesis. It cannot support a universal claim, a provider comparison or a
numerical effect size. The published rate calculation and independent paired
benchmarks must carry those claims.

## RTK counter observation

The original article recorded that the author's RTK installation displayed
about 6.1 million estimated tokens saved while the actual input for the work was
a fraction of that figure.

Available artifact: the contemporaneous pre-rewrite article at commit
`8c27834`, line 35. The RTK database or `rtk gain` export and matching provider
usage export were not archived.

Permissible claim: report the observation and the missing raw exports together.
It tests the meaning and scale of RTK's counter, not whether RTK raised or
lowered the bill.

## RTK pytest reproduction

The original article recorded a local reproduction against RTK 0.43.0. The
project's pytest configuration already supplied `-q`; RTK supplied another
`-q`; the effective `-qq` suppressed the summary its filter expected, and the
wrapped command did not report the result correctly.

Available artifacts:

- contemporaneous pre-rewrite article at commit `8c27834`, line 41;
- RTK 0.43.0 source at commit
  `5a7880d404db8364d602f2ecdc41dd790f64013f`;
- `src/cmds/python/pytest_cmd.rs` at that commit, where `run` checks command-line
  arguments for `-q` and adds `-q` when it does not find one. The check cannot
  see `addopts` supplied by pytest configuration.

The raw terminal output and minimal fixture were not archived. The source audit
supports the mechanism but is not a substitute for the missing runtime output.

Permissible claim: report this as a local correctness reproduction with the
missing fixture disclosed. It does not establish the frequency of the bug or a
task-cost effect beyond the possibility of a retry.

## Client output-pipeline interaction

During review, the author identified a missing mechanism: coding clients already
truncate and transform tool output, while RTK inserts another transformation
layer. The resulting behaviour depends on the client, version, command form and
whether the model uses a built-in tool or Bash. The original observation is
preserved verbatim in
[`raw/2026-08-02-rtk-client-interaction.txt`](raw/2026-08-02-rtk-client-interaction.txt),
with its source note beside it.

The `-qq` reproduction is an instance of that composition problem at the CLI
configuration layer. RTK supplied a quiet flag without visibility into the
quiet flag already supplied by pytest configuration. This attribution is to
RTK, not Headroom.

JetBrains independently supplies the client-side evidence: Claude Code native
truncation reduced the counterfactual size of giant results; built-in tools
bypassed RTK; a broken rewrite caused retries; and compression caused some
re-reads. This supports the narrower description "client- and path-dependent."
It does not prove that RTK's filter is internally random.

## Additional turns compound replay

The author's follow-up observation is preserved verbatim in
[`raw/2026-08-02-turn-cost-observation.txt`](raw/2026-08-02-turn-cost-observation.txt),
with its assumptions in the adjacent source note.

The article formalises the point with a simple growing-history model. A fixed
block of `c` tokens kept for `n` calls adds `nc` traffic. If every turn adds `d`
live tokens, cumulative input includes `d n(n+1)/2`. The total therefore has a
quadratic term in turn count. The marginal next turn grows roughly linearly with
the history already accumulated.

Permissible claim: additional turns can outweigh a local context reduction
because they replay the whole live prefix and enlarge later requests. Do not
state that every provider bill is literally quadratic. Caching, compaction,
truncation and variable turn sizes change the result.

## RTK source audit

On 2 August 2026, the rewrite cloned and inspected two RTK revisions:

- release 0.43.0, commit
  `5a7880d404db8364d602f2ecdc41dd790f64013f`;
- development commit
  `e0ffd40ef7c450489aca4a50c0ab1358e4375691`.

The audit searched the analytics, tracking and pytest command paths. It checked
how saved tokens are estimated, what the counter can observe, and whether the
current README represents that number as bill savings. The development README
states that its percentage applies to Bash output, not the bill, and that its
absolute token count is estimated as `bytes / 4`.

This was a reproducible static source audit. It was not a runtime or billing
benchmark.

## Headroom source audit

On 2 August 2026, the rewrite cloned Headroom 0.33.0 at commit
`6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9` and traced three code paths:

1. `headroom/cache/prefix_tracker.py`, including byte-identical replay of the
   previously forwarded prefix;
2. `headroom/proxy/handlers/openai.py`, where one Responses path infers cache
   writes from uncached input and says OpenAI has no write premium;
3. `headroom/providers/openai.py`, where the manual fallback assumes cached
   reads receive a 50% discount.

The audit also searched the repository's published benchmarks for a paired
GPT-5.6 completed-coding-task cost result and did not find one. That is a record
of the search, not proof that no such test exists elsewhere.

This was a reproducible static source audit. It found both a cache-preservation
mechanism in Headroom's favour and GPT-5.6 accounting fallbacks that did not
match OpenAI's 9 July pricing. It was not a live Headroom request, a dashboard
comparison or a completed-task benchmark.

## Preservation rule

All artifacts added after this inventory are append-only under `evidence/raw/`.
If a run is later found invalid, retain it and add an `INVALID` note with the
reason and superseding artifact. Deletion requires a recorded reason and the
user's explicit approval.
