# Right of reply: Perseus article

Status: ready to send. Publication blocker until sent and the response window
has closed.

Subject: Right of reply: findings concerning Perseus IP, security and product claims

To Perseus Computing LLC,

Delivery address: `perseus@perseus.observer`, published as the company contact
in the pinned Context Engine README and security policy.

Rakuen Software is preparing a reported analysis of the public Perseus Context
Engine and Perseus Vault repositories. Rakuen builds Aimee, which overlaps this
field. We will disclose that commercial interest prominently.

Our Context Engine review is pinned to commit
`e7bbeb35485e67876947c87eda7e98028ddb4a29`. Our Vault review is pinned to
commit `0e91c26c7c35f991336b990bfb29454b5757c179`. We are giving you the material
findings before publication and invite corrections, source records and a
statement for publication.

Please respond by **[DATE, TIME UTC, seven calendar days after confirmed
receipt]**. If a narrow extension is needed to retrieve a specific record,
please identify the record and proposed date before the deadline. We will place
answers with the findings they address. If we receive no response, we will say
so without assigning a motive.

## Questions and findings

1. Perseus says provisional application `64/069,842` was filed in May 2026.
   Please provide the exact filing date and a redacted filing receipt. If you
   want us to assess support for the public 27 June claim elements, please also
   provide the filed specification or identify where each element appears in
   it.

2. Our attached public claim chart covers all fifteen proposed claims or claim
   clusters in the public disclosures. We found old elements throughout, a
   routine reason to make every combination and no unexpected technical result.
   Please identify the precise feature you contend is novel in each charted
   claim and the strongest earlier reference you considered for it. For static
   dependency prefetch specifically, why does your analysis omit Aimee,
   LlamaIndex ingestion caching, Prompt Cache, RAGCache and TurboRAG?

3. Git attributes the 28 May commit that introduced six complete technical
   disclosures to Hermes Agent as author and committer. Other commits are
   attributed to Codex or Claude. What did those agent identities do? Who chose
   and read the prior art, who drafted the distinctions, and who approved each
   claim summary before publication?

4. The resolver-generator disclosure says every generated claim is
   mechanically verified before rendered output. In the pinned build, the
   public synthesis path returns a prompt with `generated: false` and no claims.
   The private validator accepts a claim that Perseus was independently audited
   by NASA when its exact quote merely says a resolver builds a dependency
   graph. Is there another production component that performs generation and
   semantic support checking? If so, please identify the code and version.

5. The Agora disclosure says two agents cannot claim the same task and states
   that the protocol works across NFS. The implementation depends on advisory
   locking, and its lock helper permits a fail-open path. Under that permitted
   condition our synchronized reproducer returned success to both claimers.
   Which filesystems, NFS versions, lock managers and mount options are
   supported? Please provide a multi-client test or narrow the guarantee.

6. The trust-boundary disclosure describes one registry as a single policy
   spine. Path, redirect, authentication, redaction and output checks still
   execute in individual resolvers and transports, and the project's July
   review found missed checks in those sites. What exact security property does
   the registry itself enforce, beyond recording metadata and selecting gates?

7. Exhibit E4 derives round-trip counts from two selected architectures and
   sets token, latency and cost fields to null. The introducing commit calls it
   a benchmark that quantifies the patent's core technical effect for Section
   101 prosecution. Was any live model, network, token, latency or cost
   measurement made? Please provide the raw data and protocol if so.

8. The published Atlassian email says Atlassian cannot confirm full ownership.
   Perseus's appended analysis says Atlassian “declined to review or claim
   ownership.” Perseus's July strategy documents describe Atlassian as building
   managed enterprise memory across Rovo, Jira, Confluence, Teamwork Graph and
   agent sessions, tell Perseus not to compete head-on, and prohibit “Atlassian
   memory, but better.” What were Thomas Connally's Atlassian role and relevant
   duties while Perseus was developed? Did those duties involve AI agents,
   context management, memory, Rovo, Jira, Confluence or Teamwork Graph? Do you
   have an agreement, assignment, waiver or release that supports your ownership
   statement? Please provide it or explain the difference in wording. Do you
   dispute our product-level mapping of Context Engine, Vault, Agora, cited
   synthesis, agent workflows, MCP adapters, trust controls and federation to
   Rovo, Teamwork Graph, Rovo Search, Rovo Dev, Agents in Jira and Rovo MCP? If
   so, identify the functional distinction for each disputed row.

9. The Context Engine and Vault security reviews call themselves “Independent
   pre-launch” audits. Git attributes their introducing commits to Perseus
   Computing, with Claude Opus as a co-author, while both products' milestone
   documents say an independent external audit remains open. Who performed the
   reviews, for what organization and under what engagement? In what sense were
   they independent?

10. Vault advertises persistent encrypted memory. Its current security policy
    says the FTS5 index contains memory bodies in plaintext, with metadata also
    plaintext; its threat model says vectors are plaintext and semantically
    reconstructable. Its claims audit records a retired latency claim, an
    unbacked insert-rate figure, “signed” used for a self-computed hash and
    “federation” used for a local file operation. Do you dispute this account?
    What exact current encryption boundary should the headline communicate?

11. Perseus's closest-prior-art table describes Accenture US 12,511,287 as
    workflow orchestration with resolution interleaved with model calls. The
    patent describes generating query data for chunks and storing the enriched
    chunks before a later prompt. The same table combines Intuit US
    2025/0139367, a prompt-to-planning-problem patent, with US 12,423,313, a
    hierarchical graph RAG patent, under one generic description. Please supply
    the element analysis supporting those descriptions and correct any errors.

12. We have identified older and contemporary work including m4, Docutils, Org
    Babel, Make, Bazel, RAG, XACML, Hearsay-II, Maildir, Aider, Continue, Cline,
    AutoGen, Task Master and other agent task or memory systems. Atlassian's
    dated public Rovo materials describe cross-tool Teamwork Graph context,
    company-grounded chat and agents in May 2024; Jira and Confluence context
    supplied to GitHub Copilot in January 2025; source-linked search in July
    2025; persistent user memory in August 2025; and a generally available Rovo
    MCP server in February 2026. Why are Rovo and Teamwork Graph absent from the
    closest-prior-art table despite Connally's employment at Atlassian? Aimee was
    publicly accessible from February 2026, although a 3 June history
    replacement removed at least three months of visible ancestry. Which of
    these did you review before calling the public disclosures the novel core
    and their named references the closest prior art?

Please also send any correction we have not asked about and any statement you
want quoted in full or in relevant part. We may follow up on factual material
that changes the draft.

Regards,

Rakuen Software

## Send record

- Recipient address: `perseus@perseus.observer` (verified against the pinned
  Context Engine README and `SECURITY.md`)
- Sent at: pending
- Confirmed received: pending
- Response deadline: pending
- Extension requested or granted: none
- Response artifact: pending
