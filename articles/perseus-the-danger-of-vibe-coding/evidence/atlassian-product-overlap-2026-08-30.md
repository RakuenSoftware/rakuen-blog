# Perseus and Atlassian product-overlap map

Date: 2026-08-30

Status: reporting work product. Publication hold.

## Scope

This map compares the public Perseus product at commit
`e7bbeb35485e67876947c87eda7e98028ddb4a29` with Atlassian product materials
published before Perseus's asserted May 2026 provisional filing. It addresses
technical and product overlap. It does not decide ownership, derivation,
inventorship or patent validity.

Perseus's own [May 2026 product
report](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/PERSEUS_PRODUCT_REPORT.md)
lists the renderer, checkpoints, Guide, Agora, Vault, federation, inbox,
graph/prefetch, cited synthesis, trust controls and assistant profiles as one
product. Its July strategy documents then identify Atlassian as the managed
enterprise memory plane occupying the adjacent product category.

## Dated Atlassian record

| Date | Atlassian publication | Shipped or announced surface |
|---|---|---|
| 2024-05-01 | [Introducing Rovo](https://www.atlassian.com/blog/announcements/introducing-atlassian-rovo-ai) | Teamwork Graph joins Atlassian and connected SaaS data; Search and Chat return contextual organizational knowledge; configurable agents synthesize data and act from instructions or workflow triggers |
| 2025-01-14 | [Rovo for GitHub Copilot](https://www.atlassian.com/blog/development/atlassian-developer-innovation-rovo-for-github-copilot) | Jira and Confluence knowledge becomes additional context for a coding assistant; developer agents plan and implement work from organizational requirements |
| 2025-07-24 | [Rovo Search quality](https://www.atlassian.com/blog/rovo/rovo-search-quality) | Contextual answers across more than fifty connected applications, source citations, permission-respecting retrieval, personalized ranking and behavior-based quality signals |
| 2025-08-12 | [Rovo Search relevance](https://www.atlassian.com/blog/atlassian-engineering/unraveling-rovo-search) | Indexed content and permissions, blended relevance signals and passage-level citations for generated answers |
| 2025-08-26 | [Rovo persistent memory](https://www.atlassian.com/blog/ai-at-work/rovo-chat-august-2025-updates) | Persistent memory tied to a user profile and Teamwork Graph, correction learning, multi-step actions and work across Atlassian and third-party applications |
| 2025-11-21 | [Rovo Dev CLI](https://www.atlassian.com/blog/blog/announcements/rovo-dev-command-line-interface) | A coding agent understands repositories, integrates Jira and Confluence context, and manages development work from the terminal |
| 2026-02-02 | [Atlassian Cloud changelog](https://confluence.atlassian.com/cloud/blog/2026/02/atlassian-cloud-changes-jan-26-to-feb-2-2026) | Rovo MCP access to Jira, Confluence and Compass with OAuth, domain and IP controls, and audit logs |
| 2026-02-04 | [Rovo MCP general availability](https://www.atlassian.com/blog/announcements/atlassian-rovo-mcp-ga) | One secure interface lets external AI clients search, fetch and act on Jira and Confluence context |
| 2026-02-25 | [Agents in Jira](https://www.atlassian.com/blog/announcements/ai-agents-in-jira) | Jira represents human and agent work together, tracks who is doing what and preserves an execution trail |
| 2026-02-25 | [Rovo MCP gallery](https://www.atlassian.com/blog/announcements/rovo-mcp-gallery) | Rovo agents use third-party MCP skills for cross-application context and actions without custom integrations |

## Surface-by-surface comparison

| Perseus surface | Perseus public behavior | Earlier Atlassian behavior | Overlap | Material difference |
|---|---|---|---|---|
| Context Engine renderer and context packs | Resolves files, commands, memory and other directives into assistant-ready Markdown; emits profiles for several assistants | Teamwork Graph ingests Atlassian and connected SaaS data; Rovo retrieves and synthesizes organizational context; Rovo for GitHub Copilot supplies that context to a coding assistant | Multi-source information is assembled and supplied to an assistant for a task | Perseus uses local directives and rendered files; Atlassian uses a managed graph, retrieval services and product integrations |
| Static graph and predictive prefetch | Discovers dependencies, checks freshness and warms cached resolver output | Atlassian indexes connected work and knowledge before Rovo queries; Rovo Dev and Rovo Search retrieve prepared context for later tasks | Preprocess and retain likely model inputs so later assistant work starts with context | The cache key and storage layer differ |
| Perseus Vault | Stores persistent narrative memory, hybrid retrieval, time decay, source anchors, corrections and supersession | Rovo published persistent profile memory backed by Teamwork Graph, personalization across conversations and learning from an explicit correction | Persistent personalized memory changes later AI context and can be corrected | Perseus exposes local storage and explicit lifecycle controls; Rovo is managed and graph-backed |
| Cited synthesis and retrieval explanations | Retrieves source material, generates bounded output and attaches source excerpts or citations | Rovo Search returns contextual answers with source links and passage-level citations across more than fifty connected applications | Cross-source retrieval produces synthesized, attributable answers | Perseus's proposed exact-string gate is a narrower validator and does not establish semantic support |
| Guide and agent directives | Selects tools or approaches from live context and can invoke agents or synthesis surfaces | Rovo Agents have defined instructions, knowledge, skills and actions; automation triggers invoke them inside Jira and Confluence workflows | Configured agents use scoped knowledge and tools to recommend, synthesize or act | Product vocabulary and orchestration host differ |
| Agora | Stores task state, dependencies, agent ownership, claiming and completion in project files | Jira stores work, dependencies and assignees; Rovo Dev moves from issue to code and pull request; Agents in Jira assigns and tracks agent work | Human and agent work is represented, assigned, coordinated and recorded | Agora is local and file-backed; Jira is a managed system of record |
| Unified adapters and MCP | One registry and call adapter dispatches local files, commands, memory, sub-agents and external tools; Perseus exposes MCP tools | Rovo MCP exposes Jira, Confluence and Compass to many AI clients; Rovo Studio agents combine Atlassian and third-party MCP skills | One controlled interface connects heterogeneous context and action surfaces to AI clients | The enumerated back ends, transport and deployment differ |
| Trust, redaction and audit | Registry metadata selects gates and profiles; product advertises redaction and audit | Teamwork Graph respects source permissions; Rovo MCP uses user consent, scopes, OAuth, domain controls, IP allowlists and audit logs | Policy metadata and enforcement control which context and actions reach an AI client | Atlassian inherits enterprise product permissions; Perseus uses local policy and workspace boundaries |
| Federation | Subscribes to narrative state across Perseus workspaces | Teamwork Graph connectors unify knowledge from Atlassian products and third-party SaaS workspaces | Cross-workspace information enters one retrieval and context plane | Perseus moves portable local narratives; Atlassian manages connected enterprise objects and relationships |
| Assistant integration | Profiles target Hermes, Codex, Claude Code, Cursor and Rovo Dev; Rovo Dev receives rendered `AGENTS.md` plus Perseus MCP tools | Rovo Dev is Atlassian's coding agent, with Jira and Confluence integration and repository understanding | Perseus directly extends an Atlassian agent with context and tools | Perseus is an add-on at this boundary, not a replacement coding agent |

## Perseus's own description of the boundary

The [20 July strategy](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/strategy/perseus-durable-cognition-strategy-2026-07-20.md)
says Atlassian is converging on managed enterprise memory across Rovo, Jira,
Confluence, chat, Teamwork Graph and agent sessions. It assigns Atlassian
product relevance, permission-aware retrieval, live work-graph context and
tenant-managed memory.

The [21 July positioning
note](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/strategy/durable-cognition-positioning-2026-07-21.md)
says Atlassian's memory plane is product-native, permission-aware, graph-backed
and embedded in Jira, Confluence and Rovo. Perseus proposes to differentiate
through longer retention, explicit correction, retrieval explanations and
portable synthesis. Its guardrails prohibit "Atlassian memory, but better"
messaging and direct feature parity.

That is a differentiation strategy within an overlapping category. It does not
support a claim that Perseus pioneered context assembly, persistent AI memory,
cross-source retrieval, cited answers, agent workflows, task coordination,
assistant adapters or policy-gated context.

## Competition analysis

Technical overlap alone does not establish commercial competition. The public
record also shows substitution, common users and a deliberate differentiation
strategy.

| Competition factor | Perseus evidence | Atlassian comparison |
|---|---|---|
| Job to be done | Put current context, durable memory and reviewable records around a model or agent | Rovo and Teamwork Graph put organizational context, memory, retrieval and agents around team workflows |
| Users | Technical teams evaluating agent and developer workflows; operators; Government programs and primes | Enterprise teams, developers and administrators using Rovo, Jira, Confluence and Rovo Dev |
| Inputs | Workspace state, tasks, durable memory, external sources and tool results | Work items, pages, code-adjacent requirements, connected SaaS knowledge and Teamwork Graph relationships |
| Outputs | Assistant briefings, recalled memory, cited synthesis, agent tasks and handoffs | Contextual answers, persistent memory, cited synthesis, agent actions, plans, work items and code workflows |
| Integration boundary | Assistant files, MCP, Rovo Dev profile and local or network deployment | Product-native Rovo surfaces, Rovo MCP, Rovo Dev and connected applications |
| Differentiation | Local-first, portable, long-horizon, explicit correction and operator control | Managed, product-native, permission-aware, graph-backed and embedded in Atlassian products |
| Choice affected | Which system owns cross-tool context, durable memory, retrieval policy and the records supplied to an agent | The same architectural position is occupied by Rovo and Teamwork Graph inside the Atlassian system |

Perseus's own [CogniRepo competitive
analysis](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/competitive-analysis-phase1.md)
defines significant overlap with Context Engine and Vault persistent memory as
a high direct competitive threat even when the products have different primary
use cases. It calls CogniRepo code-first and Perseus workspace-first, then still
labels CogniRepo the most serious threat in the context-engine space.

Atlassian overlaps Context Engine and Vault plus Agora, agents, cross-tool
retrieval, citations, permission-aware serving, MCP access and developer
workflows. Under Perseus's own test, Atlassian is a competitor.

The [design-partner
guide](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/design-partner-onboarding.md)
addresses technical teams evaluating real agent or developer workflows. The
[Federal buyer
notes](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/federal-buyers.md)
ask programs and primes to evaluate Perseus as their context, memory and record
layer. These are product-adoption documents, not a hobby-project boundary.

Perseus is an Atlassian competitor. It can complement Rovo Dev as an add-on
while competing with Rovo and Teamwork Graph for the broader context, memory,
retrieval and agent layer. Integration at one interface does not eliminate
substitution elsewhere.

The internal directions to avoid head-on competition, publish non-competitive
positioning and prohibit “Atlassian memory, but better” messaging are themselves
competitive-positioning decisions. They acknowledge the competition and manage
its presentation.

## Direct Rovo Dev integration

Perseus's pinned
[README](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/README.md#rovo-dev-mcpjson-in-repo-root)
provides an MCP configuration for Rovo Dev and says Rovo Dev reads `AGENTS.md`
at session start. The same README lists `AGENTS.md` as the Rovo Dev output in
its assistant profile table. The product report lists Rovo Dev in its adapter
conformance gallery.

Perseus therefore presents itself as a context and tool extension for an
Atlassian coding agent while omitting Rovo, Teamwork Graph and Rovo Dev from its
published closest-prior-art comparison.

## Reporting conclusion

The overlap is product-wide. Deployment, storage, portability and control
surfaces differ. The underlying product functions recur on both sides:
multi-source context assembly, persistent memory, retrieval and ranking,
attributable synthesis, agent configuration, task orchestration, adapters and
permission-aware serving.

Perseus and Atlassian compete for the same architectural role around
organizational knowledge and agent work. They target overlapping users, inputs,
workflows and integration surfaces. Perseus's complementary label describes its
chosen positioning. It does not describe a separate market.

All dated Atlassian materials above precede Perseus's asserted May 2026 filing
month. The omission is material to the article's assessment of Perseus's
novelty research and of the accuracy of its "closest prior art" representation.
