# Source verification and right of reply: named prior-art parties

Status: draft. Not sent.

This file covers the external parties whose patents, papers or products are
material to the article's prior-art findings. Perseus has already received the
advance preprint and twenty-two questions. Do not send it this request again.

The article does not ask these recipients to decide patent validity. It asks
them to verify what their own work disclosed, whether the public Perseus claim
map describes the same mechanism, and whether Perseus contacted them about the
patent.

## Base email

**To:** use the documented address in the recipient table below

**Subject:** Pre-publication fact check: `[PROJECT]` and Perseus patent claims

Hello,

Rakuen Software is preparing a reported article, *False Confidence: The
Dangers of Vibe Coding*. It identifies `[PROJECT]` as earlier work relevant to
the patent and public novelty claims made by Perseus Computing LLC.

Review copy: `[ATTACH THE CURRENT PREPRINT OR INSERT AN ACCESSIBLE PRIVATE LINK]`

We are asking for factual corrections and records, not a legal opinion on
patent validity. Please answer these four questions on the record:

1. Is this description accurate: `[DATED CAPABILITY FROM THE TABLE BELOW]`?
   Please give the earliest public artifact that supports it, or the specific
   correction.
2. Our article maps `[MECHANISM FROM THE TABLE BELOW]` against Perseus's
   [public claim map](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/disclosures/CLAIM-MAP.md)
   and novelty materials. Does Perseus's public description encompass the
   mechanism your work disclosed? If not, what specific technical limitation
   separates them?
3. By June 27, 2026, had Perseus Computing LLC or Thomas Connally contacted you
   about a patent, citing or disclosing your work, or obtaining a licence or
   consent? If so, when and for what stated purpose? Please also identify any
   later contact.
4. What other factual correction or on-record statement should we include?
   Please identify the supporting public record.

Please respond by Monday, September 7, 2026 at 17:00 UTC. Publication is
targeted for Wednesday, September 9. If you need a short extension, tell us
before the deadline. We may quote your response, and we will link or describe
supporting records that bear on the findings.

Regards,

`[NAME]`

Rakuen Software

`[EMAIL]`

## Recipient and substitution table

Replace both bracketed passages in the base email with the text in the last two
columns. Send each recipient a separate message.

| Party named in article | Recipient | Public contact source | Dated capability | Mechanism in the public Perseus account |
|---|---|---|---|---|
| Reflexion | Noah Shinn, `noahshinn024@gmail.com` | [paper author block](https://arxiv.org/pdf/2303.11366) | By March 2023, Reflexion stored linguistic feedback in an episodic memory buffer and used it in later trials. | Persistent episodic memory that changes later agent behaviour. |
| Generative Agents | Joon Sung Park, `joonspk@stanford.edu` | [paper author block](https://arxiv.org/pdf/2304.03442) | By April 2023, Generative Agents stored natural-language experience, synthesized reflections and retrieved memories dynamically for planning. | Persistent experience, reflection, retrieval and planning. |
| MemoryBank | Yanlin Wang, `wangylin36@mail.sysu.edu.com` | [published paper; corresponding author](https://ojs.aaai.org/index.php/AAAI/article/download/29946/31654) | By May 2023, MemoryBank provided cross-session memory, continuous updates, user modelling and time-based forgetting. | Persistent memory, consolidation, profiles and Ebbinghaus-style decay. |
| CoALA | Theodore R. Sumers, `sumers@princeton.edu` | [paper author block](https://arxiv.org/pdf/2309.02427) | By September 2023, CoALA organized agents around working, episodic, semantic and procedural memory with internal read and write actions. | Typed memory layers and agent memory operations. |
| MemGPT / Letta | Charles Packer, `cpacker@berkeley.edu` | [MemGPT paper author block](https://arxiv.org/pdf/2310.08560) | By October 2023, MemGPT managed memory tiers for bounded context and persistent multi-session agents. | Tiered persistent memory, recall and reflection for agents. |
| Microsoft AutoGen Teachability | AutoGen team, `autogen@microsoft.com` | [Microsoft Research contact](https://www.microsoft.com/en-us/research/project/autogen/opportunities/) | By October 2023, AutoGen Teachability persisted user teachings in a vector database and selectively recalled facts, preferences and skills across chats. | Persistent vector memory and selective cross-session recall. |
| Zep / Graphiti | Preston Rasmussen, `preston@getzep.com` | [Zep paper author block](https://blog.getzep.com/content/files/2025/01/ZEP__USING_KNOWLEDGE_GRAPHS_TO_POWER_LLM_AGENT_MEMORY_2025011700.pdf) | By January 2025, Zep and Graphiti provided temporal knowledge-graph memory integrating conversations and business data while retaining historical relationships. | Graph memory, temporal history, correction and source-linked retrieval. |
| Mastra | Mastra, `legal@mastra.ai` | [official contact](https://mastra.ai/terms-of-service) | By February 2025, Mastra documented persistent storage, semantic retrieval, context management, resource and thread scopes, and memory shared between agents. | Persistent scoped memory, semantic retrieval and cross-agent sharing. |
| A-MEM | Wujiang Xu, `wujiang.xu@rutgers.edu` | [paper author block](https://arxiv.org/pdf/2502.12110) | By February 2025, A-MEM built linked memory networks and let new memories update representations of earlier memories. | Linked memory, consolidation and updating historical records. |
| Mem0 | Mem0 research team, `research@mem0.ai` | [paper author block](https://arxiv.org/pdf/2504.19413) | By April 2025, Mem0 dynamically extracted, consolidated and retrieved conversational memory, including a graph variant for relationships. | Extraction, consolidation, semantic retrieval and graph memory. |
| Hindsight / Vectorize | Vectorize, `contact@vectorize.io` | [official contact](https://vectorize.io/contact) | By December 2025, Hindsight documented temporal and entity-aware retention, recall and reflection with traceable updates; by March 2026 it served memory over MCP with hybrid retrieval. | Temporal memory, reflection, hybrid retrieval, history and MCP access. |
| CogniRepo | Ashlesh, `ashleshat5@gmail.com` | [maintainer's public contact](https://www.ashlesh.co.in/) | Public source dated March 12, 2026 implemented semantic and episodic memory, FAISS retrieval, importance scoring and bounded pruning; its MCP server was then a mock. | Persistent memory, selected repository context, retrieval, decay and cross-agent handoff. |
| Cognee | Cognee / Topoteretes, `info@topoteretes.com` | [official contact](https://www.cognee.ai/about-us) | Public Cognee source before the reported filing documented graph-plus-vector memory, chunk-to-document provenance and temporal conflict handling that retained superseded edges. | Graph and vector memory, provenance, temporal correction and supersession. |
| codebase-memory-mcp | Martin Vogel, `martin.vogel.tech@gmail.com` | [repository contact](https://github.com/DeusData/codebase-memory-mcp/blob/main/SECURITY.md) | The version available before the relevant filing date, if any, provided persistent structural code memory through an MCP knowledge graph. | Repository context, persistent structural memory and MCP retrieval. |
| memory-mesh | memory-mesh maintainer, `kilhub.projects@gmail.com` | [public Git commit metadata](https://github.com/kilhubprojects/memory-mesh/commits/main/) | The version available before the relevant filing date, if any, provided local agent memory and retrieval. | Persistent agent memory, retrieval and memory tiers or decay where then implemented. |
| memtrace-public | Syncable, `axth@syncable.dev` | [public GitHub organisation contact](https://github.com/syncable-dev) | The version available before the relevant filing date, if any, provided structural code memory and temporal graph functions. | Persistent structural memory, temporal relationships and context retrieval. |
| YourMemory | Sachit Mishra, `mishrasachit1@gmail.com` | [public Git commit metadata](https://github.com/sachitrafa/YourMemory/commits/main/) | The version available before the relevant filing date, if any, provided persistent agent memory, Ebbinghaus-style decay and published retrieval benchmarks. | Persistent memory, decay, semantic recall and agent access. |
| ContextForge | Maintainer via [GitHub Issues](https://github.com/zeroranker/contextforge/issues) | No verified public email found; use the repository's public contact route. | Version 1.0.0, publicly available by April 2026, compressed repositories into selected context under a requested token budget. | Selection and compression of repository context for model input. |

The addresses above were found in public first-party publications, official
contact pages, project profiles or public Git metadata on September 1, 2026.
They have not been tested for delivery. MemoryBank's address is reproduced as
printed in the published paper. ContextForge has no verified public email in
the reviewed sources.

The last five rows require special care. Ask the recipient to identify the exact
pre-filing version and artifact. Perseus's June competitor report establishes
that it regarded the projects as technically relevant; it does not establish
that every current feature was public before the asserted May filing.

## CogniRepo-specific follow-up

Add this fifth question only to the CogniRepo message:

5. Perseus committed a direct CogniRepo inspection on June 19, dated June 18,
   and called CogniRepo its most serious context-engine threat. Before that
   inspection, did you have any communication with Perseus or Connally? After
   it, did they tell you that CogniRepo would be cited or disclosed in any
   patent filing?

## Mastra-specific follow-up

Add this fifth question only to the Mastra message:

5. Mastra's [beta account](https://mastra.ai/blog/beta-launch) says the team
   read the MemGPT paper and then built its memory implementation around recent
   messages, top-k retrieval and surrounding context. Is that chronology
   accurate? Identify the earliest public artifact for the implementation.

## Accenture email

**To:** Cliff Angelo, Accenture Media Relations,
`cliff.angelo@accenture.com` ([official contact](https://newsroom.accenture.com/pr-contacts))

**Subject:** Pre-publication fact check: Accenture US 12,511,287 and Perseus

Hello,

Rakuen Software is preparing *False Confidence: The Dangers of Vibe Coding*.
The article checks how Perseus Computing LLC describes Accenture's US
12,511,287 in its public patent materials. Review copy:
`[ATTACH THE CURRENT PREPRINT OR INSERT AN ACCESSIBLE PRIVATE LINK]`

Please answer these questions on the record:

1. The article says US 12,511,287 generates candidate queries for document
   chunks, adds selected query data to those chunks, and stores them before a
   later user prompt retrieves them. What is factually incorrect in that
   description?
2. Perseus characterizes the patent as resolution interleaved with model calls.
   Does Accenture consider that an accurate description? Identify the patent
   passage that supports any correction.
3. By June 27, 2026, had Perseus or Thomas Connally contacted Accenture about
   citing this patent, distinguishing a Perseus application from it, or
   obtaining a licence or consent? If so, when and for what purpose? Please
   also identify any later contact.
4. What other sourced correction or statement should the article include?

Please respond by Monday, September 7, 2026 at 17:00 UTC. Publication is
targeted for Wednesday, September 9.

Regards,

`[NAME]`

Rakuen Software

`[EMAIL]`

## Intuit email

**To:** Intuit Media Relations, `press-inquiries@intuit.com`
([official contact](https://www.intuit.com/ca/company/press-room/media-contacts/))

**Subject:** Pre-publication fact check: Intuit patents and Perseus

Hello,

Rakuen Software is preparing *False Confidence: The Dangers of Vibe Coding*.
The article checks how Perseus Computing LLC describes two Intuit inventions in
its public patent materials. Review copy:
`[ATTACH THE CURRENT PREPRINT OR INSERT AN ACCESSIBLE PRIVATE LINK]`

Please answer these questions on the record:

1. The article says US 2025/0139367 translates a prompt into a planning problem,
   while US 12,423,313 constructs and searches hierarchical document graphs for
   retrieval-augmented generation. What is factually incorrect in that
   description?
2. Perseus combines the two inventions under one “prompt construction” row.
   Does that accurately represent their mechanisms? Identify the patent passage
   that supports any correction.
3. By June 27, 2026, had Perseus or Thomas Connally contacted Intuit about
   citing either patent, distinguishing a Perseus application from them, or
   obtaining a licence or consent? If so, when and for what purpose? Please
   also identify any later contact.
4. What other sourced correction or statement should the article include?

Please respond by Monday, September 7, 2026 at 17:00 UTC. Publication is
targeted for Wednesday, September 9.

Regards,

`[NAME]`

Rakuen Software

`[EMAIL]`

## Parties not contacted and why

| Name in article | Disposition |
|---|---|
| Perseus Computing LLC and Thomas Connally | Already received the full preprint and twenty-two questions. Their response is preserved separately. |
| Rakuen Software and Aimee | The publisher is the interested first-party source. The article discloses that interest; sending ourselves a request would create no independent evidence. |
| Hermes Agent, Codex, Claude Opus, OpenAI and Anthropic | Named only to describe public Git attribution or the tool identity recorded in repository metadata. The article does not attribute the developer's conduct or patent claims to the model providers. |
| GitHub | GitHub Copilot is named only as the recipient of Jira and Confluence context in an official Atlassian product announcement. No disputed claim is attributed to GitHub. |
| USPTO | Its manuals are cited for patent-process rules. The article does not ask the agency to assess the unpublished application. |
| NASA | Appears only inside a deliberately false test fixture used to test citation validation. The article makes no factual claim about NASA. |
| Authors of the 2024 field survey | The article uses the survey only to establish that a literature existed. It attributes no disputed finding to a named author. |

## Send record

Record one row per separate message. Do not use a bulk recipient list.

| Party | Recipient | Sent | Received | Deadline | Response artifact |
|---|---|---|---|---|---|
| Reflexion | `noahshinn024@gmail.com` | pending | pending | 2026-09-07 17:00 UTC | pending |
| Generative Agents | `joonspk@stanford.edu` | pending | pending | 2026-09-07 17:00 UTC | pending |
| MemoryBank | `wangylin36@mail.sysu.edu.com` | pending | pending | 2026-09-07 17:00 UTC | pending |
| CoALA | `sumers@princeton.edu` | pending | pending | 2026-09-07 17:00 UTC | pending |
| MemGPT / Letta | `cpacker@berkeley.edu` | pending | pending | 2026-09-07 17:00 UTC | pending |
| Microsoft AutoGen | `autogen@microsoft.com` | pending | pending | 2026-09-07 17:00 UTC | pending |
| Zep / Graphiti | `preston@getzep.com` | pending | pending | 2026-09-07 17:00 UTC | pending |
| Mastra | `legal@mastra.ai` | pending | pending | 2026-09-07 17:00 UTC | pending |
| A-MEM | `wujiang.xu@rutgers.edu` | pending | pending | 2026-09-07 17:00 UTC | pending |
| Mem0 | `research@mem0.ai` | pending | pending | 2026-09-07 17:00 UTC | pending |
| Hindsight / Vectorize | `contact@vectorize.io` | pending | pending | 2026-09-07 17:00 UTC | pending |
| CogniRepo | `ashleshat5@gmail.com` | pending | pending | 2026-09-07 17:00 UTC | pending |
| Cognee | `info@topoteretes.com` | pending | pending | 2026-09-07 17:00 UTC | pending |
| codebase-memory-mcp | `martin.vogel.tech@gmail.com` | pending | pending | 2026-09-07 17:00 UTC | pending |
| memory-mesh | `kilhub.projects@gmail.com` | pending | pending | 2026-09-07 17:00 UTC | pending |
| memtrace-public | `axth@syncable.dev` | pending | pending | 2026-09-07 17:00 UTC | pending |
| YourMemory | `mishrasachit1@gmail.com` | pending | pending | 2026-09-07 17:00 UTC | pending |
| ContextForge | GitHub Issues | pending | pending | 2026-09-07 17:00 UTC | pending |
| Accenture | `cliff.angelo@accenture.com` | pending | pending | 2026-09-07 17:00 UTC | pending |
| Intuit | `press-inquiries@intuit.com` | pending | pending | 2026-09-07 17:00 UTC | pending |
