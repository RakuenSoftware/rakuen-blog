# Reporting record: Perseus and vibe coding

Date: 2026-08-30

Status: expanded draft. Publication hold.

## Form and thesis

The article is reported analysis with a closing recommendation. The source
findings come from a static review of public Perseus source and documentation.
The thesis that proof-shaped volume is a characteristic danger of vibe coding
is Rakuen Software's analysis.

The piece does not claim that a court or patent office would find any Perseus
claim invalid. Anticipation, obviousness, priority and inventorship are legal
questions that require a complete record and counsel.

## Interest

Rakuen Software builds `aimee`. `aimee` operates in repository memory,
code-intelligence and agent-context infrastructure. Rakuen benefits if readers
conclude that Perseus's claimed field contains earlier work or that its
differentiation is narrow.

The article discloses this interest before the first comparison and again where
`aimee` appears.

## Perseus source pin

- Repository: <https://github.com/Perseus-Computing-LLC/perseus>
- Commit: `e7bbeb35485e67876947c87eda7e98028ddb4a29`
- Commit date reported by Git: 2026-08-29
- Static review date: 2026-08-30

Material reviewed for the initial draft:

- `README.md` and `SECURITY.md`;
- `docs/disclosures/CLAIM-MAP.md`;
- all nine documents in `docs/disclosures/`, including the six numbered
  disclosures, the three 27 June disclosures and `CLAIM-MAP.md`;
- `docs/ip/README.md` and `docs/ip/2026-06-01-atlassian-legal-response.md`;
- `docs/strategy/perseus-durable-cognition-strategy-2026-07-20.md`,
  `docs/strategy/perseus-memory-one-page-2026-07-20.md` and
  `docs/strategy/durable-cognition-positioning-2026-07-21.md`;
- all four Markdown and JSON exhibit pairs in `docs/ip/exhibits/`;
- `docs/security-review-2026-07-05.md`;
- `docs/SECURITY-INDEX.md` and `docs/SECURITY-MILESTONES.md`;
- `src/perseus/registry.py`, `renderer.py`, `mcp.py`, `serve.py`;
- directive implementations for query, tool, agent, read, include, services
  and remote Perseus resolution; and
- federation, webhook, redaction and local Vault-index implementations.

The source review was static. It was not a runtime penetration test, deployment
review or dependency audit.

## Perseus Vault source pin

- Repository: <https://github.com/Perseus-Computing-LLC/perseus-vault>
- Commit: `0e91c26c7c35f991336b990bfb29454b5757c179`
- Static review date: 2026-08-30

Material reviewed for the memory section:

- `README.md`, `SECURITY.md` and `CLAIMS-AUDIT.md`;
- `docs/THREAT-MODEL.md` and `docs/SECURITY-MILESTONES.md`;
- `docs/security-review-2026-07-05.md`; and
- the Git history that introduced the July security review.

The threat model identifies its own code scope as v2.2.1. Current v2.23-series
behaviour is attributed only where the current README or security policy repeats
the property. No Vault runtime or source-code security test was performed.

## Evidence classes

### Public project claims

The article attributes product, benchmark, patent and security statements to
Perseus's own documents. Those documents establish what the project says. They
do not independently establish the truth, novelty or legal effect of the
claims.

### Static source observations

The reviewed source establishes where the registry declares metadata and where
resolver and transport code enforce policy. The article uses the project's own
July security review for its list of historical confirmed findings. It does not
publish newly discovered vulnerability claims from the 30 August source read.

Git attributes the commit that introduced all six original Context Engine
disclosures to Hermes Agent as author and committer. Git also attributes commits
in the reviewed history to Codex and Claude identities. Metadata establishes the
published attribution. It does not establish who physically composed each line
or the amount of human review.

The two documents titled “Independent pre-launch audit” were introduced in
commits attributed to Perseus Computing and co-authored by Claude Opus. Neither
document names an external auditor. Both repositories separately describe a
full independent or independent external audit as open. The article reports the
label, provenance and unresolved meaning. It does not infer a hidden author.

### Narrow runtime checks

Three standard-library reproducers were run against the pinned Context Engine
checkout:

1. `citation_gate_semantic_mismatch.py` passed a false NASA-audit claim with an
   unrelated exact quote to the private citation validator. The validator
   accepted it. **Disposition:** used to distinguish exact quotation from
   semantic support. Raw record:
   [`raw/2026-08-30-citation-gate-semantic-mismatch.txt`](raw/2026-08-30-citation-gate-semantic-mismatch.txt).
2. `production_synthesis_path.py` called the public synthesis entry point with
   generation enabled and a configured model. It returned a prompt,
   `generated: false` and no claims. **Disposition:** used to describe the
   reviewed production entry point, not every possible external integration.
   Raw record:
   [`raw/2026-08-30-production-synthesis-path.txt`](raw/2026-08-30-production-synthesis-path.txt).
3. `agora_lock_failure.py` forced the lock helper's documented fail-open branch
   and synchronized two claimers after their open-state reads. Both returned
   success. **Disposition:** used only to show that the permitted fail-open path
   cannot support an unconditional mutual-exclusion guarantee. It does not show
   lock failure on a supported filesystem. Raw record:
   [`raw/2026-08-30-agora-lock-failure.txt`](raw/2026-08-30-agora-lock-failure.txt).

A targeted `pytest` attempt did not start because the reporting environment had
no pytest module. **Disposition:** invalid as a product test; no pass or fail
claim. Raw record:
[`raw/2026-08-30-pytest-unavailable.txt`](raw/2026-08-30-pytest-unavailable.txt).

Three earlier citation reproducer attempts were invalid because they used a
missing interpreter, shadowed the package or omitted imports. They remain in
[`raw/2026-08-30-citation-gate-invalid-attempts.txt`](raw/2026-08-30-citation-gate-invalid-attempts.txt)
under the append-only artifact rule.

### Prior-art examples

GNU m4, Docutils, Org Babel, Make, Bazel, RAG, FTS5, BM25, XACML, Hearsay-II,
Maildir and implicit-feedback systems are used as technically relevant
predecessor classes. Aider, Continue, Cursor, Claude Code, GitHub Copilot,
Repomix, Cline, AutoGen, Claude Task Master, Beads and claude-flow are used as
AI-tool equivalents.

Atlassian is a separate first-party prior-art family. Its dated public materials
establish:

- Rovo and Teamwork Graph cross-tool context, grounded chat, agents and workflow
  triggers on 2024-05-01;
- Jira and Confluence context supplied to GitHub Copilot on 2025-01-14;
- context-aware search across more than fifty connected applications with
  source links on 2025-07-24;
- persistent profile memory backed by Teamwork Graph on 2025-08-26; and
- general availability of the Rovo MCP server on 2026-02-04.

These are official Atlassian publications predating Perseus's asserted May 2026
filing month. They establish prior art to the broad technical field and several
public elements. The article does not say one Atlassian publication anticipates
every limitation of a confidential claim.

[`ip-claim-matrix-2026-08-30.md`](ip-claim-matrix-2026-08-30.md) records the
element-level comparison, source dates, gaps and publication holds. The chart
supports the finding that the Perseus documents omit close predecessors. It
does not state that one reference anticipates a complete patent claim.

[`public-claim-chart-2026-08-30.md`](public-claim-chart-2026-08-30.md) separately
charts every public proposed claim or dependent limitation at combination level.
It records the strongest Perseus response and the missing single-reference
limitation. The engineering conclusion is that every combination is obvious;
remaining single-reference searches concern anticipation evidence only.

The named-patent check read the summaries and bibliographic records for
Accenture US 12,511,287 and Intuit US 2025/0139367 and US 12,423,313. The article
uses those primary documents to challenge Perseus's descriptions. It does not
claim those patents anticipate Perseus.

### Aimee overlap

Rakuen's records place `aimee` in public access from February 2026. The visible
Git root dated 3 June is a history-replacement snapshot, not the launch. It
removed at least three months of public ancestry from the current graph.

The current repository cannot by itself prove which feature was public on
which February date. The draft therefore describes the chronology and the
evidence loss, while withholding an element-level prior-art conclusion until
surviving commits, packages, images, forks, caches and third-party links are
reconstructed. Perseus's effective priority date and provisional support also
remain unknown.

## First-party reporting inventory

This is a new article. No earlier published article, interview or right-of-reply
response exists to preserve. This draft now contains the first-party checks
listed below.

First-party work completed before this draft:

1. Static checkout review of Perseus at the pinned commit. **Disposition:** used
   for architecture and documentation analysis only.
2. Static inspection of Perseus's IP disclosures and claim map. **Disposition:**
   used to describe the project's proposed distinction.
3. Static inspection of the project's own July security review. **Disposition:**
   cited as a vendor-maintained review, not an independent audit.
4. Element-by-element comparison with predecessor systems. **Disposition:**
   recorded in the IP claim matrix and used to challenge the completeness of
   Perseus's novelty analysis; no validity conclusion published.
5. Historical-artifact checks for Aider, Continue, Repomix, Cline, AutoGen,
   Claude Task Master, Beads and claude-flow. **Disposition:** dated artifacts
   used where available; current Cursor and Claude Code pages retained as
   technically relevant but placed on a chronology hold.
6. Preliminary comparison with `aimee`. **Disposition:** February public access
   and the June history replacement described; feature-level dates and legal
   priority conclusions withheld.
7. Historical GitHub artifact check for the named AI projects. **Disposition:**
   commit permalinks used for Continue, Task Master, Beads and claude-flow;
   repository creation dates treated only as repository dates, never as feature
   dates.
8. URL audit after the IP rewrite. **Disposition:** one dead LlamaIndex page was
   removed and a moved GNU Find link was replaced. Every retained link returned
   content during the final check except the Wiley DOI landing page, which
   rejected automated access with HTTP 403. The DOI remains the publisher's
   canonical identifier for Feldman's paper. The article's absolute link back
   to this reporting record returns 404 until the new article is committed to
   the linked branch; it is a publication-path check, not an external source.
9. Git provenance review for the original disclosures and both July security
   reviews. **Disposition:** used to report repository attribution and to ask
   what “independent” means; authorship beyond Git metadata withheld.
10. Named-patent source check. **Disposition:** used to identify inaccurate or
    collapsed descriptions in Perseus's closest-prior-art table.
11. Vault claims and security-document audit. **Disposition:** current
    plaintext-index statements and recorded historical corrections used with
    their version limits; no current general insecurity claim.
12. Three narrow Context Engine runtime reproducers and one unavailable pytest
    attempt. **Disposition:** recorded under Narrow runtime checks above.

## Claims withheld

The following claims require more work and do not appear as findings:

- Perseus was written by a model or principally produced through AI coding;
- any named patent claim is anticipated or obvious;
- `aimee` predates the effective Perseus filing date for every relevant
  element;
- the current Cursor or Claude Code documentation proves the same behavior was
  public before May 2026;
- any newly observed static security concern is exploitable in a supported
  deployment; and
- either July security review was performed by an external auditor, or that the
  “independent” label proves a particular author's intent;
- current Vault workspace scoping lacks the stricter controls added after the
  v2.2.1 threat model;
- the volume of source, tests or documentation measures quality.

The phrase "vibe coding" names the governance mechanism argued in the article.
It is not presented as a verified account of who typed the code.

## Right of reply

The request is drafted at
[`right-of-reply-draft-2026-08-30.md`](right-of-reply-draft-2026-08-30.md).
The recipient is `perseus@perseus.observer`, published as the company contact in
the pinned Context Engine README and security policy. It asks about:

- the thesis that its claim map does not address the closest predecessor
  classes;
- the specific challenges to its RAG, LangChain and MCP comparisons;
- the argument that the registry describes policy while enforcement remains
  distributed;
- the distinction between parser non-reentry and model-facing prompt
  injection; and
- the proposed description of `aimee` overlap, including the explicit refusal
  to draw a feature-level prior-art conclusion before reconstructing its
  erased ancestry;
- the citation-validator counterexample and the distinction between quotation
  presence and semantic support;
- the Agora double-claim race, advisory-lock dependency and NFS claim;
- the interpretation placed on Atlassian's legal email; and
- the element-level predecessor table, with a request that Perseus identify the
  narrower mechanism it says remains novel;
- the Hermes Agent attribution and human review process;
- the provenance and meaning of both “Independent pre-launch audit” labels;
- the named patent descriptions;
- Vault's encryption boundary and historical claims corrections; and
- the filing date, receipt and support for the 27 June elements.

The planned window is seven calendar days after confirmed receipt. The request,
receipt, exact UTC deadline, any extension and the response must be recorded.
Silence will be reported without assigning a motive.

## Publication gate

- Prior-art element chart: complete as reporting work product; counsel review
  and several source-date holds remain.
- Perseus effective priority date: outstanding.
- `aimee` public chronology: outstanding.
- Right of reply: draft complete; sending, receipt, response window and article
  integration outstanding. This is a hard publication blocker.
- Legal review of patent-language passages: outstanding.
- Mechanical voice and provenance gate: passed on 2026-08-30.
- Editorial review after right of reply: outstanding.

The article remains a draft.
