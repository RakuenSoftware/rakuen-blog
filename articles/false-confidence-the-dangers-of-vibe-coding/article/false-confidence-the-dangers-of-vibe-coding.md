---
title: "False Confidence: The Dangers of Vibe Coding"
slug: false-confidence-the-dangers-of-vibe-coding
date: 2026-08-30
author: Rakuen Software
tags: [agents, context, security, patents, aimee]
excerpt: "Perseus let LLM-generated claims testify for other LLM-generated claims. The result looked reviewed: an architecture, tests, audits, patent exhibits and a novelty story. Independent evidence contradicted its strongest conclusions."
---

*Pre-print for right of reply. Responses remain open until 17:00 UTC on
September 7, 2026. Target publication: September 9, 2026.*

*Drafted from a static review of Perseus at commit
[`e7bbeb35`](https://github.com/Perseus-Computing-LLC/perseus/tree/e7bbeb35485e67876947c87eda7e98028ddb4a29)
and Perseus Vault at
[`0e91c26`](https://github.com/Perseus-Computing-LLC/perseus-vault/tree/0e91c26c7c35f991336b990bfb29454b5757c179).
Rakuen Software builds aimee, which overlaps parts of this field. That interest
bears directly on the article. Perseus has responded to our questions; its
response appears below. Other right-of-reply work remains open.*

*This is technical analysis of Perseus's public claims and source. Patent
validity remains outside the article's scope. The methods, raw runs and held
conclusions are in the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/false-confidence-the-dangers-of-vibe-coding/evidence/reporting-2026-08-30.md).*

[Perseus](https://github.com/Perseus-Computing-LLC/perseus) prepares live
workspace context for AI assistants. It resolves files, commands, environment
values, services and memory into `AGENTS.md`, `CLAUDE.md` and similar files
before the assistant starts work. The public product family targets local and
self-hosted deployments, with Perseus Vault providing persistent agent memory.

The repository grew beyond that useful renderer. It acquired security reviews,
benchmarks, defensive publications, a claim map and patent exhibits. Each
artifact has the form of evidence. Each points at another artifact from the
same project.

The volume supplies no independent proof. A test establishes behaviour under
its fixture. A digest identifies an artifact, and a claim map connects prose to
a proposed claim. Security, factual support and novelty require evidence from
outside the claim that needs proving.

Vibe coding can produce incorrect code. Its deeper danger is a structure of
apparent verification around an untested premise. The code, tests, audits and
novelty analysis agree because they share one context. Their agreement is
correlation.

## Provenance: The reviewers shared one source of confidence

Git attributes the commit that introduced all six original defensive
publications to [Hermes
Agent](https://github.com/Perseus-Computing-LLC/perseus/commit/6ca32dc17090496715bcfa7fbca6e2ef55480f52).
The same identity is author and committer. One commit added 438 lines covering
six problem statements, prior-art sections, descriptions of the invention,
distinction tables and proposed claim summaries.

Other commits are attributed to Codex and Claude Opus. Context Engine and Vault
contain reviews labelled “Independent pre-launch audit” introduced by commits
attributed to Perseus Computing and co-authored by Claude Opus. Neither review
names an external auditor. Both projects' security milestones say that an
independent external audit remains open.

Git cannot reveal an undocumented conversation or prove who physically typed a
line. It does show the review the project recorded. We found agent-attributed
claims and AI-coauthored reviews in the relevant history. We found no identified
human technical reviewer who independently checked the storage boundary,
production enforcement paths or prior-art history before publication.

A human may have read or approved the files. Approval supplies authority to
publish. It supplies no independent evidence when the same process produced the
architecture, the test and the explanation that the test proved the
architecture.

The recorded process closes on itself:

```text
LLM describes a property
        ↓
LLM implements part of it
        ↓
LLM writes a test around that part
        ↓
LLM reviews the implementation
        ↓
LLM promotes the test to proof of the property
        ↓
Later LLMs retrieve the claim as established fact
```

An LLM predicts a response from the context it receives. A second pass can find
mistakes, but shared framing makes the two outputs correlated. Independent
review needs a source of authority outside that loop.

## Patent: Confidence reached a filing before the prior-art record

Perseus says it filed provisional application `64/069,842` in May 2026. The
public record examined here is its [claim
map](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/disclosures/CLAIM-MAP.md),
claims summaries, defensive publications and a description of its “novel
core.” Its eight primary public claims describe resolution before model
invocation, registry-declared context tiers, quote-preserving normalized cache
keys, checkpoint-correlated reinforcement, registry permission gates,
exact-quote citation validation, static dependency prefetch and file-based
agent task coordination.

Four dependent claims add path-and-inode cycle detection, a recursion-depth
limit, literal resolver output and a static typed dependency graph. Three
umbrella claims add one registry and adapter across six source classes, parser
vocabulary derived from that registry and local semantic-memory retrieval with
byte-reproducible output.

Those records present tests and exhibits as evidence that proposed elements
were reduced to practice. Reduction to practice establishes implementation
timing. Novelty requires a prior-art record. Those public claims are the claims
tested and refuted here.

What Perseus has disclosed is overly broad and sits across substantial prior
art. If rights of that breadth were granted, the effect would be chilling. The
claims reach from Atlassian's commercial products to independent open-source
projects implementing context assembly, persistent memory, retrieval, agent
coordination and MCP access. They amount to a shot across the bow of an industry
that had already built the claimed mechanisms.

That is the target of this article. An LLM can turn a plausible description
into genuine confidence that a familiar combination is an invention. When LLMs
then draft the architecture, tests, claim map, prior-art comparisons and review,
the resulting volume looks like independent confirmation while every artifact
inherits the same premise.

Perseus shows that loop reaching a patent filing. The danger extends beyond bad
code or an inaccurate answer. It is false confidence detached from
counterfactual evidence, carried into public claims that could burden everyone
who had already built the field.

The named search fails a basic source check. Perseus describes Accenture's [US
12,511,287](https://patents.google.com/patent/US12511287B1/en) as resolution
interleaved with model calls. The patent describes generating candidate queries
for document chunks, adding selected query data and storing the enriched chunks
before a later user prompt retrieves them.

One Intuit row combines two separate inventions under “prompt construction.”
[US 2025/0139367](https://patents.google.com/patent/US20250139367A1/en)
translates a prompt into a planning problem. [US
12,423,313](https://patents.google.com/patent/US12423313B1/en) constructs and
searches hierarchical document graphs for RAG. Different inventors, priority
dates and mechanisms disappear inside one label.

These descriptions show that the published closest-prior-art account misstates
or collapses the few references it names.

The larger omission is a whole field. By May 2026, LLM memory had years of
papers, implementations, product documentation and a dedicated survey. A
counterfactual search would have looked for earlier systems that stored
experience across sessions, ranked it by relevance and time, corrected it,
consolidated it or served it to agents. Perseus's public analysis accepted its
own categories and searched for distinctions inside them.

We sent Perseus the advance preprint and twenty-two numbered questions
covering the filing and prior art, authorship and review, implementation claims,
security and Vault. After receiving the preprint and reviewing the questions,
Perseus did not refute any reported finding, including the product-level
competition with Atlassian.

Its only response was that the questions did not describe claims in its patent.
This article analyzes the claims Perseus made public. That response does not
refute any finding about them.

The later public record clarifies the filing sequence. A [conversion
issue](https://github.com/Perseus-Computing-LLC/perseus/issues/493), opened June
28 UTC after the June 27 IP work, treats the non-provisional as future work due
around May 2027. It lists a professional novelty search as unfinished and
records two receipts with the same application number three days apart.

The reported filing moved confidence into consequential legal action. Generated
architecture, tests, distinctions and claim maps had become sufficient grounds
to begin the patent process without a public account of the strongest
counterfactual evidence.

## Prior art: LLM memory already had a history

Perseus Vault describes persistent memory, episodic and semantic layers,
Ebbinghaus decay, reflection, hybrid retrieval, temporal history, corrections,
supersession, source-linked recall and shared agent access. Earlier LLM systems
had already established each part of that vocabulary and most of its
combinations.

| Public date | Earlier LLM-memory system | Mechanism already in the field |
|---|---|---|
| March 2023 | [Reflexion](https://arxiv.org/abs/2303.11366) | Stores linguistic feedback in an episodic memory buffer and uses it to improve later trials |
| April 2023 | [Generative Agents](https://arxiv.org/abs/2304.03442) | Keeps a natural-language experience record, synthesizes higher-level reflections and retrieves memories dynamically for planning |
| May 2023 | [MemoryBank](https://arxiv.org/abs/2305.10250) | Persistent cross-session memory, continuous updates, user modelling and forgetting explicitly based on the Ebbinghaus curve |
| September 2023 | [CoALA](https://arxiv.org/abs/2309.02427) | Organizes language agents around modular working, episodic, semantic and procedural memory with internal read and write actions |
| October 2023 | [MemGPT](https://arxiv.org/abs/2310.08560) | Manages memory tiers for bounded context and multi-session agents that remember, reflect and evolve |
| October 2023 | [AutoGen Teachability](https://github.com/microsoft/autogen/discussions/404) | Persists user teachings in a vector database and selectively recalls facts, preferences and skills across chats, including proposed codebase use |
| April 2024 | [LLM-agent memory survey](https://arxiv.org/abs/2404.13501) | Reviews an already populated field of agent-memory mechanisms and applications |
| May 1, 2024 | [Rovo and Teamwork Graph](https://www.atlassian.com/blog/announcements/introducing-atlassian-rovo-ai) | Combines Atlassian and connected SaaS data so search, chat and configurable agents can retrieve, synthesize and act on organizational context |
| January 2025 | [Zep and Graphiti](https://arxiv.org/abs/2501.13956) | Temporal knowledge-graph memory integrating conversations and business data while retaining historical relationships |
| January 14, 2025 | [Rovo for GitHub Copilot](https://www.atlassian.com/blog/development/atlassian-developer-innovation-rovo-for-github-copilot) | Supplies Jira and Confluence knowledge as additional context for a coding assistant |
| February 2025 | [Mastra](https://mastra.ai/blog/agent-memory-guide) | Persistent storage, semantic search, context management, resource and thread scopes, and thread sharing between agents |
| February 2025 | [A-MEM](https://arxiv.org/abs/2502.12110) | Builds linked memory networks and lets new memories update the representations of historical ones |
| April 2025 | [Mem0](https://arxiv.org/abs/2504.19413) | Dynamically extracts, consolidates and retrieves conversational memory, with a graph variant for relationships |
| August 26, 2025 | [Rovo persistent memory](https://www.atlassian.com/blog/ai-at-work/rovo-chat-august-2025-updates) | Persists profile memory through Teamwork Graph, carries it across conversations and learns from explicit correction |
| December 2025 | [Hindsight](https://arxiv.org/abs/2512.12818) | Temporal, entity-aware retain, recall and reflection with traceable updates across facts, experiences, observations and mental models |
| February 2026 | [Aimee](https://github.com/RakuenSoftware/aimee) | Repository memory, session context, safety gates, delegated agents, checkpoints and outcome-aware routing |
| February 4, 2026 | [Rovo MCP](https://www.atlassian.com/blog/announcements/atlassian-rovo-mcp-ga) | Exposes Jira, Confluence and Compass context to external AI clients through one controlled MCP interface |
| March 12, 2026 | [CogniRepo](https://github.com/ashlesh-t/cognirepo/commit/e7d9d0815a6b78d9c96852dadde58d7382dc11ff) | Public source for persistent semantic and episodic memory, FAISS retrieval, importance scoring, bounded pruning and selected repository context for agents |
| March 2026 | [Hindsight MCP memory](https://github.com/vectorize-io/hindsight/blob/main/hindsight-docs/blog/2026-03-04-mcp-agent-memory.md) | Serves memory over MCP and combines semantic search, BM25, graph traversal and temporal filtering before reranking |

CogniRepo is especially probative because Perseus found the comparison itself.
The March 12 snapshot contains working store and recall paths, durable semantic
and episodic memory, vector retrieval and pruning. Its MCP server was still a
mock. The working evidence covers the memory and retrieval core.

Perseus then committed a [direct repository
inspection](https://github.com/Perseus-Computing-LLC/perseus/blob/2e2f8e87179aa524e7f5c3f2fc7798996ad071d8/docs/competitive-analysis-phase1.md)
on June 19. The file is dated June 18. It marked CogniRepo's persistent memory,
context retrieval and cross-agent handoff as high overlap. It called CogniRepo
“the most serious competitive threat” in the context-engine space and said the
project overlapped significantly with both context rendering and Vault.

The two dated artifacts establish a public predecessor before the reported
provisional and documented Perseus knowledge by June 19. Perseus's May
knowledge remains unknown. CogniRepo belongs in any competent later novelty
analysis, including the non-provisional work that the later conversion issue
said was still ahead.

The same competitor report names codebase-memory-mcp, memory-mesh,
memtrace-public, YourMemory and ContextForge. Their selection establishes
technical relevance. Anticipation requires a dated element comparison. Every
public version before the relevant priority date belongs in that review, yet
none appears in Perseus's published closest-art table.

Mastra's [beta account](https://mastra.ai/blog/beta-launch) supplies the lineage
in its own words. The team read the MemGPT paper, then implemented memory with
recent messages, top-k retrieval and surrounding context. Ideas moved through
the field, and Mastra named the predecessor.

Cognee belongs in the same direct product family. Our pinned [source
audit](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/your-memory-has-no-authority-model/evidence/source-audit-2026-08-20.md)
found graph-plus-vector memory, chunk-to-document source paths and a temporal
conflict resolver that retains superseded edges. Aimee is another predecessor,
but Rakuen is an interested first-party source.

Atlassian [introduced Rovo and Teamwork
Graph](https://www.atlassian.com/blog/announcements/introducing-atlassian-rovo-ai)
in May 2024. It later supplied [Jira and Confluence context to GitHub
Copilot](https://www.atlassian.com/blog/development/atlassian-developer-innovation-rovo-for-github-copilot),
[persistent profile
memory](https://www.atlassian.com/blog/ai-at-work/rovo-chat-august-2025-updates)
and a [Rovo MCP
interface](https://www.atlassian.com/blog/announcements/atlassian-rovo-mcp-ga).
All preceded the reported filing month.

Perseus's July strategy describes
Atlassian as converging on managed enterprise memory and instructs the project
to avoid building “Atlassian memory, but better.” Rovo and Teamwork Graph
remain absent from its published closest-prior-art table.

An unseen patent claim needs its own element analysis. The public novelty story
faces a simpler problem. Persistent memory, tiers, reflection, time decay,
hybrid retrieval, temporal correction, graphs, scopes and agent interfaces were
already part of LLM memory. Researchers began writing the field's history in
April 2024.

The exhaustive element work remains in the [public claim
chart](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/false-confidence-the-dangers-of-vibe-coding/evidence/public-claim-chart-2026-08-30.md)
and [IP
matrix](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/false-confidence-the-dangers-of-vibe-coding/evidence/ip-claim-matrix-2026-08-30.md).
Older preprocessors, build systems, policy engines and retrieval systems supply
the deeper ancestry. The direct LLM systems above settle the narrower question:
developers had assembled these mechanisms for agents before Perseus.

## Implementation: Public claims exceed enforced boundaries

Perseus can fairly point to substantial working components. Vault encrypts its
body column, and the synthesis helper checks quoted source spans. The directive
registry records capabilities, while Agora publishes task files atomically.
Each one solves a real part of its problem.

The public descriptions claim the complete property:

| Public representation | Boundary the implementation provides |
|---|---|
| Persistent, encrypted memory | The body column is encrypted, while the FTS5 index reproduces the body in plaintext; metadata and optional vectors also remain plaintext |
| Every generated synthesis claim is mechanically verified against its source | The production entry point returns a prompt and generates no claims; the validator checks exact quotation, without testing whether the quote supports the proposition |
| One directive registry is the security policy spine | The registry records capability metadata; path, redirect, authentication, redaction and output checks execute in individual resolvers and transports |
| Atomic, NFS-safe task claiming prevents two agents taking one task | Atomic replacement prevents partial publication; mutual exclusion depends on an advisory lock whose documented failure path continues without the lock |

Vault's [README](https://github.com/Perseus-Computing-LLC/perseus-vault/tree/0e91c26c7c35f991336b990bfb29454b5757c179)
opens with “Persistent, encrypted memory for AI agents,” and fresh installations
encrypt the body field with AES-256-GCM by default. Its [security
policy](https://github.com/Perseus-Computing-LLC/perseus-vault/blob/0e91c26c7c35f991336b990bfb29454b5757c179/SECURITY.md)
states that FTS5 stores the body in plaintext and that full-disk encryption must
protect the index and metadata. Encryption protects one representation. An
attacker holding the database can read the searchable representation.

The citation claim exceeds its validator. The private helper opens a cited line
range and checks whether the supplied quote occurs exactly. We passed it a
false claim that Perseus had been independently audited by NASA and an unrelated
exact quote from the source range; the validator accepted it. The [recorded
run](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/false-confidence-the-dangers-of-vibe-coding/evidence/raw/2026-08-30-citation-gate-semantic-mismatch.txt)
establishes quotation presence and leaves semantic support untested.

With generation enabled and a model configured, the public synthesis path
returned a prompt, `generated: false` and no claims. Tests call the private
validator with hand-built model responses. The
[production-path
run](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/false-confidence-the-dangers-of-vibe-coding/evidence/raw/2026-08-30-production-synthesis-path.txt)
matches the source. The reviewed build contains an exact-string validator and
lacks the disclosed end-to-end path from model answer to validated rendered
output.

The registry gives the parser, tooling and reviewers one map of declared
capabilities. Resolver and transport code enforce those declarations. Perseus's
own July security review found federation egress that had skipped SSRF and
redirect guards, an allow-list bypass in `@tool`, a symlink escape in `@tree`,
fail-open update verification and unbounded network reads.

The project later repaired several paths. The recorded bugs still locate the
boundary outside the single registry described by the IP documents.

Agora added a lock and a second read after recording a double-claim race, but
its lock helper deliberately swallows lock failures and continues. We forced
that documented branch and synchronized two claimers after both read the task
as open; [both returned
success](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/false-confidence-the-dangers-of-vibe-coding/evidence/raw/2026-08-30-agora-lock-failure.txt).
The result covers one permitted failure path. That path cannot support an
unconditional mutual-exclusion or NFS-safety claim.

Vault's own [claims
audit](https://github.com/Perseus-Computing-LLC/perseus-vault/blob/0e91c26c7c35f991336b990bfb29454b5757c179/CLAIMS-AUDIT.md)
records the same direction of travel. It retired a sub-millisecond recall claim,
removed an unsupported 100,000-entity insert-rate figure, replaced “signed”
with “content-hashed” and clarified that “federation” meant a local export,
workspace rename and re-import. The corrections deserve credit. They also show
that the prose had outrun the evidence more than once.

Our review was static except for three narrow reproducers. It did not test a
deployment or its dependencies. The findings concern the reviewed claims and
paths. They establish no general security verdict on current Perseus releases.

## Consequence: Full faith lets incompetence look reviewed

Perseus contains useful engineering: its shell gates default closed, and path
resolution canonicalises before checking containment. Later fixes bounded
remote reads, labelled remote context and tightened transport checks. The
project preserved reviews that record problems and corrections.

The process failed when one source of information wrote the claim, chose the
comparison, constructed the test and explained the result. The public record
identifies no participant inside that loop with independent authority to reject
its premise.

Before LLMs, this pattern would have looked like ordinary technical
incompetence. The reviewed paths failed to provide the complete properties
claimed for them. The novelty analysis missed the documented history of its
field. LLMs made the same work look reviewed.

Perseus demonstrates a new way for incompetence to become difficult to see.
Human authority remained at the final step, but the factual judgment behind
that authority had been outsourced to systems incapable of providing
independent confirmation. The models generated the claim, the review and the
reassurance; the human supplied belief and permission.

Upon review, we found failures at critical security and architectural
boundaries that should not survive competent human engineering review. A
plaintext search index cannot support an unconditional encrypted-memory claim.

An exact quotation match cannot establish that a source supports a
proposition. A lock that fails open cannot guarantee mutual exclusion. The
implementation cannot provide those public properties as stated, yet the
claims, audits and patent materials reinforced one another as if agreement
were proof.

That is the peril of trusting an LLM as an authority. A model can help inspect
evidence. It can also write the claim, choose the comparison, construct the
test and explain the result, with every artifact confirming the same premise.
Agreement inside that loop creates confidence, not evidence.

The replacement tests a security property where its boundary executes and a
citation against the proposition it accompanies. A novelty search begins with
the evidence most likely to disprove novelty. An independent reviewer can
reject the taxonomy, fixture and success condition before the result exists.

LLMs can and do create false confidence. Authority still comes from an
independent source, a reproduced boundary test or a human reviewer empowered
to disagree. Perseus asks generated artifacts to testify for one another. They
are the same witness.
