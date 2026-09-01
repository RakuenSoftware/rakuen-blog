# False Confidence: The Dangers of Vibe Coding

A reported analysis of the public Perseus Context Engine repository and its IP
disclosures. The piece argues that the project's central failure is
proof-shaped volume: code, tests, claim maps and benchmark exhibits accumulate
faster than the work needed to establish what each artifact proves.

## Status

Pre-print for right-of-reply review, 2026-09-01. Not final publication.

The public repository registers the new slug in `articles/REVIEW`. The article
is available at its eventual URL as an unlisted, non-indexed pre-print. Responses
remain open until 17:00 UTC on 2026-09-07, with publication targeted for
2026-09-09 after the reporting and publication gates are complete.

The current draft is based on a static review of Perseus at commit
`e7bbeb35485e67876947c87eda7e98028ddb4a29`, the project's own security review,
its public claim map and its linked technical disclosures. The Vault material is
pinned to `0e91c26c7c35f991336b990bfb29454b5757c179`. Three narrow standalone
reproducers cover citation validation, the production synthesis path and the
Agora lock's documented fail-open branch. They are not a penetration test.

## Evidence

[`evidence/reporting-2026-08-30.md`](evidence/reporting-2026-08-30.md) records
the source pin, the evidence classes, the claims deliberately withheld and the
publication blockers.

[`evidence/ip-claim-matrix-2026-08-30.md`](evidence/ip-claim-matrix-2026-08-30.md)
charts every public Perseus claim cluster against older mechanisms and dated AI
projects. It separates technical overlap from anticipation, obviousness,
priority and eligibility conclusions.

[`evidence/public-claim-chart-2026-08-30.md`](evidence/public-claim-chart-2026-08-30.md)
charts all fifteen public proposed claims at the combination level, including
the established mechanisms, combination rationale and expected result.

[`evidence/atlassian-product-overlap-2026-08-30.md`](evidence/atlassian-product-overlap-2026-08-30.md)
maps Context Engine, Vault, Agora, retrieval, agents, MCP, trust controls and
federation against Atlassian products published before the asserted filing.

[`evidence/cognirepo-prior-art-2026-09-01.md`](evidence/cognirepo-prior-art-2026-09-01.md)
checks CogniRepo's 12 March public source, Perseus's June competitive analysis
and the patent-process chronology. It separates technical overlap, documented
knowledge and the later non-provisional disclosure duty.

[`evidence/right-of-reply-draft-2026-08-30.md`](evidence/right-of-reply-draft-2026-08-30.md)
preserves the prepared right-of-reply request to Perseus. A public version was
delivered as issue #1026 on 2026-08-30.

[`evidence/right-of-reply-perseus-response-2026-08-30.md`](evidence/right-of-reply-perseus-response-2026-08-30.md)
records Perseus's response and its evidentiary disposition. The response
supplied no supporting record and changed no technical finding.

[`evidence/right-of-reply-atlassian-draft-2026-08-30.md`](evidence/right-of-reply-atlassian-draft-2026-08-30.md)
gives Atlassian five focused questions about product chronology, competition,
the published ownership email, any assignment or waiver, and whether the public
patent account reaches Atlassian's products.

[`evidence/source-questions-prior-art-projects-draft-2026-08-30.md`](evidence/source-questions-prior-art-projects-draft-2026-08-30.md)
provides the base email, documented public contact routes and four focused
questions for the named prior-art parties, plus tailored messages for Accenture
and Intuit.
Publication remains blocked until the material parties have had a fair chance
to answer and their responses have been incorporated where they bear.

The article carries no measured performance figure. Repository size and test
count are not used as evidence of quality or authorship.

## Commercial interest

Rakuen Software builds `aimee`, whose repository memory, source graph and
agent-context work may overlap parts of Perseus's claimed field. Rakuen
therefore benefits if readers conclude that the field has earlier work or that
Perseus's differentiation is narrow. The article states this beside the first
comparison.

## Blockers

- Complete or clearly retain the held chronology items in the claim matrix. In particular,
  establish the effective Perseus priority date, reconstruct the first public
  date for every `aimee` feature proposed as prior art and pin current product
  documentation to historical artifacts.
- Send the prepared questions to verified Atlassian contacts and send
  source-verification questions to the maintainers whose dates or capabilities
  remain material. Give seven calendar days after confirmed receipt, record any
  extension, and incorporate each answer where it bears. Perseus's response to
  the public request has been incorporated.
- Have patent counsel review any sentence that moves from technical overlap to
  anticipation, obviousness or validity.
