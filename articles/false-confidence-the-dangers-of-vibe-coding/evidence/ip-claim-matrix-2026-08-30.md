# Perseus public IP claim matrix

Date: 2026-08-30

Status: reporting work product. Publication hold.

## Scope

This matrix covers the claims Perseus chose to publish at commit
`e7bbeb35485e67876947c87eda7e98028ddb4a29`. It does not cover the unreleased
text of provisional application `64/069,842`, which was unavailable for review.

The public material consists of claim summaries, a claim map, technical
disclosures and implementation exhibits. A test or exhibit can show that
Perseus implemented an element. It cannot show that Perseus invented the
element.

The legal questions remain separate:

- **Anticipation:** one earlier reference must disclose every limitation of a
  claim, expressly or inherently. See USPTO
  [MPEP 2131](https://mpep.uspto.gov/RDMS/MPEP/print?href=d0e197004.html&version=e8r9).
- **Obviousness:** several references may be combined when the record supplies
  a reason to combine them and the result is predictable. See USPTO
  [MPEP 2141](https://www.uspto.gov/web/offices/pac/mpep/s2141.html).
- **Priority support:** material published on 27 June 2026 receives the May
  provisional date only if the provisional supports it. The public repository
  cannot answer that question because it withholds the provisional.
- **Eligibility:** a useful software result still needs a claimed technical
  mechanism beyond an abstract information-processing result. See USPTO
  [MPEP 2106](https://www.uspto.gov/web/offices/pac/mpep/s2106.html).

No row below states a legal conclusion. Each row identifies the public claim,
the old elements, the best located sources and the work still required before
publication.

## Source-date rules

The operative date is public availability, not the current repository root.
Current documentation can explain a mechanism. It cannot establish that the
mechanism was public on the date now printed on the page.

For fast-moving AI projects, this matrix therefore prefers:

- dated design posts;
- specifications with an issue date;
- historical commit permalinks;
- dated discussions and releases; and
- old standards or papers whose publication is independent of Git history.

Repository creation dates establish only that a repository existed. They do
not establish when a feature appeared. A rewritten repository can also erase
the ancestry needed to prove an earlier date. Aimee is presently in that
category.

## Public cluster 1: resolve directives before model invocation

### Perseus's public elements

1. Parse typed annotations in an authored document.
2. Dispatch them to source-specific resolvers.
3. Resolve them before a model invocation.
4. Place the results into model context.
5. Require zero inference-time tool calls for that resolution.
6. Produce deterministic output when external inputs are frozen.

### Earlier mechanisms

- [GNU m4](https://www.gnu.org/software/m4/manual/m4.html), descended from a
  1976 implementation, expands registered macros, includes files and executes
  commands while copying input to output.
- [CMake `execute_process`](https://cmake.org/cmake/help/git-stage/command/execute_process.html)
  runs commands during configuration, before generation.
- [Org Babel](https://orgmode.org/worg/org-contrib/babel/intro.html) executes
  heterogeneous code blocks and inserts their results into a document. A
  [2011 tutorial](https://orgmode.org/worg/org-contrib/babel/how-to-use-Org-Babel-for-R.html)
  dates the public system.
- [RAG](https://arxiv.org/abs/2005.11401), 2020, retrieves external material and
  conditions generation on it.

### Assessment

The model sees prepared text because the program prepares the text first. Zero
tool calls during inference follow from that ordering. Frozen inputs make an
ordinary deterministic preprocessor repeat.

This is the ordinary combination of a document preprocessor, which supplies
parsing and dispatch, and RAG, which supplies the model-context destination.
Parsing source declarations, executing them before a model call and emitting
one finished context artifact produce no unexpected interaction.

## Public cluster 2: context tiers and selective loading

### Perseus's public elements

1. Attach a tier to each directive or source.
2. Select material at or below a requested tier.
3. Use the selection to manage a bounded context window.

### Earlier mechanisms

- Storage and CPU cache hierarchies assign material to levels and admit it
  under bounded capacity.
- Aider's dated [October 2023 repository-map design](https://aider.chat/2023/10/22/repomap.html)
  ranks code-graph material and selects the highest-value portion that fits a
  token budget.
- Continue exposed multiple typed context providers and let a user select the
  material to add through one `@` interface. See its
  [provider documentation](https://docs.continue.dev/customize/deep-dives/custom-providers).
- Cursor project rules can be always present, path-scoped, manually included or
  selected by relevance. See [Cursor rules](https://docs.cursor.com/context/rules-for-ai).
- Claude Code loads project instructions, skills, MCP data and sub-agent
  context at different lifecycle points. See Anthropic's
  [context-loading description](https://code.claude.com/docs/en/features-overview).

### Assessment

The word `tier` adds no mechanism. The public claim needs an unexpected result
from this selection rule or a narrower implementation that the older budgeted
selectors do not teach.

## Public cluster 3: quote-preserving normalized cache keys

### Perseus's public elements

1. Collapse whitespace outside quoted substrings.
2. Preserve whitespace inside quoted substrings.
3. Hash the normalized line.
4. Cache resolver output under the hash.

### Earlier mechanisms

- Lexers distinguish insignificant token-separating whitespace from characters
  inside string literals.
- Canonical serializers map semantically equivalent input to one byte sequence.
- Content-addressed caches hash canonical action inputs. Bazel describes the
  model in its [remote-cache documentation](https://bazel.build/remote/caching).
- Org Babel documents
  [cached evaluation](https://orgmode.org/worg/org-contrib/babel/header-args.html)
  of document computations.

### Assessment

Every part performs its established function. The selected canonical form has
the predictable effect: spacing outside literals stops causing misses while
literal contents remain distinct. The exact rule is an ordinary application of
lexer-aware canonicalization to a cache key and produces the expected result.

## Public cluster 4: checkpoint-correlated implicit reinforcement

### Perseus's public elements

1. Recommend a skill or action.
2. Observe a later checkpoint event.
3. Correlate the event with the recommendation inside a time window.
4. Treat presence as acceptance and prolonged absence as rejection.
5. Update a score and use it in later recommendations.

### Earlier mechanisms

- Hu, Koren and Volinsky published
  [Collaborative Filtering for Implicit Feedback Datasets](https://doi.org/10.1109/ICDM.2008.22)
  in 2008.
- Delayed outcome attribution appears in 2018 work on
  [linear bandits with delayed feedback](https://arxiv.org/abs/1807.02089).
- Visual Studio IntelliCode records whether developers select its suggestions
  and uses that telemetry to monitor recommendation quality. See Microsoft's
  [IntelliCode documentation](https://learn.microsoft.com/en-us/visualstudio/ide/intellicode-visual-studio).

### Assessment

A checkpoint is an observable implicit-feedback event. The time window is an
attribution heuristic. The score update still needs a specific new learning
rule to distinguish it from old implicit and delayed feedback.

The rejection label is also noisy. An absent checkpoint can mean abandonment,
branch change, an unrecorded completion, a different wording or acceptance
without the expected event. This is a model-quality problem even if the claim
survives the prior-art search.

## Public cluster 5: five-site trust boundary and policy spine

### Perseus's public elements

1. Enumerate shell, filesystem, foreign-content, plugin and redaction sites.
2. Store capability metadata in a directive registry.
3. Derive parser and tooling behavior from the registry.
4. Describe the renderer as a common enforcement point.

### Earlier mechanisms

- Reference monitors centralize an access-control decision at a complete
  mediation point.
- OASIS records XACML 1.1 approval in
  [2003](https://www.oasis-open.org/committees/xacml/faq.php). XACML 3.0 defines
  policy decision and enforcement roles in the
  [2013 specification](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.pdf).
- Browser extension manifests declare capabilities and host access before code
  uses them.
- Docutils treated file insertion and raw content as distinct dangerous
  capabilities in its
  [2009-era directive documentation](https://docutils.sourceforge.io/0.6/docs/ref/rst/directives.html).

### Assessment

The list contains five familiar hazards. Registry metadata describes them.
Perseus still enforces path containment, redirects, destination allow lists,
authentication, output bounds and redaction in separate code paths. Its July
2026 security review found missed checks in those paths.

The architecture therefore falls short of its own central-enforcement premise.
That implementation gap is separate from novelty, but it also weakens the
claimed technical effect.

## Public cluster 6: resolver-generator boundary with a citation gate

### Perseus's public elements

1. Assemble sources deterministically.
2. Ask a model to emit claims with source and line references.
3. Open the cited line window.
4. Require the supplied quote to occur exactly in that window.
5. Drop a claim with no passing citation.
6. Report dropped claims and conflicts.

### Earlier mechanisms

- RARR, published in 2022, searches for evidence and revises unsupported model
  output. See the [RARR paper](https://arxiv.org/abs/2210.08726).
- The AIS framework evaluates whether a source supports an output. See
  [Attributable to Identified Sources](https://aclanthology.org/2023.cl-4.2/).
- ALCE evaluated citation correctness and citation quality for LLM answers in
  2023. See the [ALCE paper](https://arxiv.org/abs/2305.14627).
- Exact source-span validation is ordinary string matching.

### Assessment

Perseus's gate proves only that copied text appears in the cited window. It
does not prove that the text supports the generated proposition. A false claim
with one irrelevant exact quote passes the validator.

The implementation also stops before model generation. `synthesize_question`
returns a prompt for the host, while tests feed hand-built claims to the
validator. The public disclosure describes a broader end-to-end gate than the
current implementation demonstrates.

## Public cluster 7: static directive graph and predictive prefetch

### Perseus's public elements

1. Parse directive dependencies without executing them.
2. Construct a dependency graph.
3. traverse dependencies in execution order.
4. inspect freshness inputs such as modification times.
5. compute cache keys and preload expected entries.
6. execute normal resolution for misses.

### Earlier mechanisms

- Rakuen's pre-rewrite records place Aimee's public repository indexing before
  Perseus's asserted filing month. Aimee indexed files and dependency edges
  before model sessions, tracked hashes and freshness, and reused the stored
  results during context assembly. The June history replacement means this is
  first-party chronology pending independent artifact reconstruction.
- LlamaIndex
  [`v0.10.17`](https://docs.llamaindex.ai/en/v0.10.17/module_guides/loading/ingestion_pipeline/root.html)
  hashed and cached every node-transformation combination. With a document
  store, it compared document hashes and skipped unchanged inputs.
- [Prompt Cache](https://arxiv.org/abs/2311.04934), submitted in November 2023,
  precomputed and stored attention states for reusable prompt modules including
  context documents.
- [RAGCache](https://arxiv.org/abs/2404.12457), submitted in April 2024, cached
  retrieved knowledge's intermediate states and overlapped retrieval with
  inference.
- [TurboRAG](https://arxiv.org/abs/2410.07590), submitted in October 2024,
  precomputed document-chunk KV caches offline and retrieved them for prefill.
- Feldman's [1979 Make paper](https://onlinelibrary.wiley.com/doi/10.1002/spe.4380090402)
  says Make had run on Unix since 1975. It models file relationships, traverses
  the graph and executes stale targets.
- Bazel builds target and action graphs, hashes declared inputs, consults
  caches and runs misses. See [Bazel remote caching](https://bazel.build/remote/caching).
- The HTML standard defines
  [prefetch](https://html.spec.whatwg.org/dev/links.html) as fetching and
  caching a resource likely to be required later.

### Assessment

The disclosure concedes Make, Ninja and Bazel, then distinguishes them by field
of use. That distinction also ignores direct LLM predecessors. Aimee,
LlamaIndex, Prompt Cache, RAGCache and TurboRAG performed the same class of
work on model inputs before Perseus's asserted filing month. Perseus's graph,
freshness test, key calculation and cache lookup retain their established
functions and produce the expected result.

## Public cluster 8: file-based asynchronous multi-agent coordination

### Perseus's public elements

1. Store one task per file with structured frontmatter.
2. Record state, agent identity and dependencies.
3. list ready work by traversing dependencies.
4. claim and complete through atomic file replacement.
5. report stale claims, orphans and cycles.
6. keep history through Git.
7. operate without a database, queue or central server.

### Earlier mechanisms

- Hearsay-II used a shared blackboard, task agenda and scheduler in the 1970s.
  See the [1980 system paper](https://mas.cs.umass.edu/Documents/Erman_Hearsay80.pdf).
- Linda coordinated independent workers through a shared tuple space.
- Maildir uses temporary files and rename to avoid partial delivery. Its
  [protocol](https://cr.yp.to/proto/maildir.html) addresses NFS operation.
- AutoGen provided a multi-agent conversation framework in
  [2023](https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat/).
- Claude Task Master managed AI-development tasks, status and dependencies by
  2025. A dated June 2025 discussion describes its
  [`next` selection](https://github.com/eyaltoledano/claude-task-master/discussions/680).
- Beads existed before May 2026 as a persistent, dependency-aware graph for
  coding agents with automatic ready-work selection. See its
  [30 April 2026 historical README](https://github.com/steveyegge/beads/blob/8694c53589f122ce622600cee377e820452b50ca/README.md).
- Claude-flow existed before May 2026 with agent swarms, persistent memory and
  coordination. See its
  [30 April 2026 historical README](https://github.com/ruvnet/claude-flow/blob/1976c57ccdb6deb8c5750ed6cb62eae7a057ae17/README.md).

### Assessment

The storage format is the narrowest distinction. Markdown frontmatter is a
serialization choice for old task-state and dependency data. Git is an old
history mechanism. File rename is an old publication primitive.

The stated concurrency guarantee is technically wrong. `os.replace` prevents
partial-file visibility. It does not atomically compare an open status and set
the claimant. Perseus later added a lock and a second read after documenting a
double-claim race. The lock helper swallows lock errors and continues, so the
remaining guarantee depends on advisory locking that all clients honor.

## Public cluster 9: one grammar over six source classes

### Perseus's public elements

1. Parse a uniform typed-directive syntax.
2. derive recognized names from one registry.
3. dispatch through one adapter contract.
4. cover filesystem, recursive composition, shell, memory, sub-agent and
   external-tool sources.
5. add a source by registering it without changing the parser.

### Earlier mechanisms

- GNU m4 uses one macro language for built-ins, file inclusion and command
  execution.
- Docutils has one directive syntax and an extensible
  [directive registry](https://docutils.sourceforge.io/0.22/docs/howto/rst-directives.html).
- Org Babel gives many language back ends one document interface.
- Continue's `@` provider interface covered files, code, Git diffs, terminal
  output, open files, clipboard, workspace trees, debugger state, repository
  maps and external systems.
- MCP's November 2024 specification unified
  [resources, prompts and tools](https://modelcontextprotocol.io/specification/2024-11-05)
  behind one client-server protocol.

### Assessment

Registries exist so a new row does not require parser changes. Six entries do
not change that mechanism. Perseus needs a technical interaction among the six
classes. The public summary supplies a count.

## Public cluster 10: recursive dependency-ordered include resolution

### Perseus's public elements

1. Resolve included documents depth-first.
2. recurse through nested includes.
3. detect a path already on the active stack.
4. detect aliases through device and inode identity.
5. apply a configurable depth bound.
6. record a typed dependency graph.
7. keep resolver output from re-entering the directive parser.

### Earlier mechanisms

- GNU m4 recursively processes included files.
- The C preprocessor processes includes before returning to the parent and has
  a configurable
  [include-depth limit](https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html).
- Make performs depth-first dependency traversal.
- Filesystem software identifies hard-link aliases with a device and inode
  pair. GNU Find documents the relation in its
  [hard-link reference](https://www.gnu.org/software/findutils/manual/find.html#Hard-Links).
- Graph algorithms use an active recursion stack to detect cycles.
- Literal and raw document blocks prevent parser re-entry.

### Assessment

Path plus inode closes a real aliasing hole. It is still the direct application
of filesystem identity to ordinary cycle detection. Depth bounding and output
non-reentry are standard parser controls.

## Public cluster 11: local FTS memory and deterministic retrieval

### Perseus's public elements

1. Index local project memory.
2. query with full-text search.
3. rank results locally.
4. render selected results without a network call.
5. return deterministic output for fixed index state and query.

### Earlier mechanisms

- SQLite FTS5 supplies local full-text indexes and BM25 ranking.
- Search systems have returned deterministic results for fixed data, query,
  tokenizer, rank function and tie-breaking rules for decades.
- Cline users publicly described file-backed and MCP-backed project memory in a
  [February 2025 discussion](https://github.com/cline/cline/discussions/1818).
- A historical Repomix artifact before May 2026 describes packing a repository
  into AI-friendly output with token counting. See its
  [30 April 2026 README](https://github.com/yamadashy/repomix/blob/2fedcaccbc64add281985ca43436f03268d5851e/README.md).

### Assessment

Local execution and a model-facing destination are field and deployment
choices. A new memory claim would need a retrieval or ranking mechanism beyond
the disclosed FTS behavior.

## Public cluster 12: one-round-trip technical effect

### Perseus's public elements

1. Compare a preassembled request with an agent loop that performs `N` model
   mediated tool calls.
2. count one model request for the preassembled path.
3. count approximately `N + 1` requests for the chosen agentic path.
4. describe the difference as lower latency and cost.

### Evidence problem

Exhibit E4 labels the round-trip values a structural model. It does not time a
live model path. The result follows from how the two paths are defined. A
single prepared request has one request. A serial agent loop with one request
per tool has more.

The comparison omits batching, parallel tool calls, client-side retrieval,
server-side retrieval and cached prompt prefixes. It proves a property of the
selected baseline. It does not prove a general technical advantage over
earlier context assemblers.

## Equivalent AI projects before the asserted filing window

This table keeps the modern systems in proportion. They show that Perseus
entered a crowded AI-tool field. Each row must still be mapped to a complete
claim before it can carry a legal conclusion.

| Project | Dated public artifact | Relevant public behavior | Claims it bears on |
|---|---|---|---|
| Atlassian Rovo and Teamwork Graph | [1 May 2024 introduction](https://www.atlassian.com/blog/announcements/introducing-atlassian-rovo-ai); [14 January 2025 GitHub Copilot integration](https://www.atlassian.com/blog/development/atlassian-developer-innovation-rovo-for-github-copilot); [26 August 2025 persistent memory](https://www.atlassian.com/blog/ai-at-work/rovo-chat-august-2025-updates); [4 February 2026 MCP GA](https://www.atlassian.com/blog/announcements/atlassian-rovo-mcp-ga) | cross-tool context graph, contextual retrieval, company-grounded chat, instructed agents, coding-assistant context, persistent profile memory and one MCP context interface | preassembled model context, source adapters, persistent memory, agent workflows and contextual retrieval |
| Aider | [22 October 2023 design note](https://aider.chat/2023/10/22/repomap.html) | tree-sitter repository map, graph ranking, token budget, context on each request | tiers, source graph, preassembled model context |
| Continue | [public commit dated 24 May 2023](https://github.com/continuedev/continue/commit/0877ada8ed9f71f3ee792bcb34a4005e3c86827d); current [provider history](https://docs.continue.dev/customize/deep-dives/custom-providers) | one typed context interface over files, code, diffs, terminal, tree, debugger, repository map and external providers | unified grammar, source adapters, context selection |
| Cursor | [rules documentation](https://docs.cursor.com/context/rules-for-ai) | project instructions, scoped and relevance-selected rules, file and code context | tiers, persistent instructions, pre-session context |
| Claude Code | [context-loading documentation](https://code.claude.com/docs/en/features-overview) | `CLAUDE.md`, scoped skills, MCP, hooks and fresh sub-agent contexts | instructions, lifecycle resolution, sub-agents, tiers |
| Repomix | [October 2024 issue](https://github.com/yamadashy/repomix/issues/71) | bounded repository artifacts intended for model context | preassembly, token budgets, deterministic repository packing |
| Cline | [16 February 2025 discussion](https://github.com/cline/cline/discussions/1818) | persistent project files, memory bank, MCP memory and cross-tool reuse | local memory, context tiers, durable project state |
| AutoGen | [2023 documentation](https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat/) | multi-agent conversation and coordination | agent orchestration |
| Claude Task Master | [6 June 2025 discussion](https://github.com/eyaltoledano/claude-task-master/discussions/680) | status and dependency aware selection of the next task | task graph, ready work, agent coordination |
| claude-flow | [30 April 2026 historical README](https://github.com/ruvnet/claude-flow/blob/1976c57ccdb6deb8c5750ed6cb62eae7a057ae17/README.md) | agent swarms, persistent memory and coordination | multi-agent coordination, memory, routing |
| Beads | [30 April 2026 historical README](https://github.com/steveyegge/beads/blob/8694c53589f122ce622600cee377e820452b50ca/README.md) | dependency graph, ready-work selection and persistent agent task memory | task graph, claiming, durable local coordination |
| Aimee | February 2026 public availability reported by Rakuen; surviving artifact reconstruction pending | repository memory, session context, safety gates, delegated agents, checkpoints and outcome-aware routing | several clusters, subject to exact feature dates |

The [Atlassian product-overlap
map](atlassian-product-overlap-2026-08-30.md) expands the first row across
Context Engine, Vault, Agora, retrieval, cited synthesis, agents, MCP, trust
controls, federation and Perseus's direct Rovo Dev integration.

Cursor and Claude Code need historical page captures before their current docs
can carry a pre-May 2026 date. Continue's repository creation date does not date
every provider. Those sources are technically relevant and chronologically
incomplete. The article must preserve that distinction.

## Aimee chronology

Rakuen's records place Aimee in public access from February 2026. The current
visible root commit is `c5dc975`, dated 3 June 2026, with snapshot commit
`c8249256` named in its message. The snapshot replaced at least three months of
public history. Treating 3 June as the project's launch date repeats damage
caused by the rewrite.

The current repository alone cannot prove the February feature dates. Before
publication, reconstruct them from:

- surviving old commit identifiers and Git object stores;
- package and release registries;
- container manifests and immutable image digests;
- forks and mirrors;
- public issue, pull-request and discussion links;
- archived documentation and search caches; and
- third-party references that identify a feature and date.

Each artifact must show both public availability and the feature offered as
prior art. A project name and a February timestamp are insufficient.

## Ownership and entitlement

Perseus publishes an Atlassian legal email as part of its IP record. The email
says Atlassian normally does not review side projects, cannot confirm full
ownership and leaves assessment of the employment agreement to the employee.
Perseus's appended analysis says Atlassian declined to claim the project and
calls the exchange a good paper trail.

The email is evidence of notice. It is not a release, assignment, waiver or
ownership confirmation. It does not establish that Atlassian owns the work
either. The unresolved evidence is the employment agreement, work history,
resource segregation, governing law and any signed assignment or waiver.

## Publication gates

- Obtain the May 2026 provisional or a later published application before
  describing its actual claims or support.
- Pin Cursor and Claude Code behavior to historical artifacts before using them
  as dated prior art.
- Pin each Continue provider used in a claim chart to the commit that introduced
  it.
- Reconstruct Aimee's February public record feature by feature.
- Locate the best single reference for the exact cache-normalization rule.
- Locate a single pre-May 2026 prompt assembler covering the complete
  resolve-before-context sequence.
- Chart source combinations with an explicit reason to combine and avoid
  hindsight.
- Ask Perseus to identify the narrow mechanism it says survives each source.
- Ask for the full method and raw measurements behind the round-trip exhibits.
- Obtain patent counsel review before publishing an anticipation, obviousness,
  priority, inventorship, entitlement or eligibility conclusion.
