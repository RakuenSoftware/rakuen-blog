---
title: "Perseus: The danger of vibe coding"
date: 2026-08-30
author: Rakuen Software
tags: [agents, context, security, patents, aimee]
excerpt: "Perseus has code, tests, security reviews, claim maps and patent exhibits. The volume looks like proof. Its own documents show a different problem: the artifacts establish that work exists, then reach beyond what the work can establish."
---

*Drafted 30 August 2026 from a static review of Perseus at commit
[`e7bbeb35`](https://github.com/Perseus-Computing-LLC/perseus/tree/e7bbeb35485e67876947c87eda7e98028ddb4a29).
Rakuen Software builds aimee, which may overlap parts of the field Perseus
claims. That interest bears directly on this article. Perseus Computing LLC has
not yet had a chance to respond, and the prior-art chronology is still open.*

*Publication is blocked until the company receives the specific findings and a
fair chance to answer. This is technical analysis. Patent-validity conclusions
remain outside its scope.*

The methods, raw runs and held claims are in the article's [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/perseus-the-danger-of-vibe-coding/evidence/reporting-2026-08-30.md).

[Perseus](https://github.com/Perseus-Computing-LLC/perseus) resolves files,
commands, environment values, services and memory into context an AI assistant
can read. It can render that context into `AGENTS.md`, `CLAUDE.md` and other
instruction files before the assistant starts work. The useful idea is simple:
collect the facts once, then give the model a prepared view.

The repository has grown far beyond that renderer. It now carries a platform
story, a memory product, a ledger, benchmark claims, security documents,
defensive publications, a claim map and patent exhibits. Each artifact has the
form of evidence. The collection asks the reader to treat their volume as
authority.

The documents carry less authority than their presentation suggests. Tests
establish that an implementation behaves as its tests expect. A digest establishes the identity
of an artifact. A benchmark establishes a result under its recorded method.

A claim map establishes that an author can connect prose to a proposed claim.
None establishes that the claim was new.

Vibe coding makes that failure cheap. Generation can produce the implementation,
the test, the explanation and the exhibit in one burst. Each new artifact cites
the others. The resulting package looks reviewed before anyone has performed
the review that matters.

## The authorship record makes the risk concrete

Git attributes the commit that introduced all six original defensive
publications to [Hermes
Agent](https://github.com/Perseus-Computing-LLC/perseus/commit/6ca32dc17090496715bcfa7fbca6e2ef55480f52).
The same identity is the author and committer. That one commit added 438 lines:
six problem statements, six prior-art sections, six descriptions of the
invention, six distinction tables and six proposed claim summaries.

Other commits are attributed to Codex and Claude Opus. Later IP commits under
the Perseus Computing identity use verbs such as “prove” for tests of proposed
claim elements and describe an offline structural comparison as prosecution
support. Git metadata cannot establish who composed every sentence or how much
human review occurred. It does establish that an agent identity published the
first complete public IP narrative in one commit.

The danger in the title is visible here. An agent identity published the
comparison, the claim summary and the document declaring the comparison
sufficient. Later tests pointed back to that taxonomy. The public record does
not identify an independent prior-art reviewer before those claims became
project facts.

## IP: The public record ends at claim summaries

Perseus says it filed provisional application `64/069,842` in May 2026. A
provisional application is ordinarily confidential. The public repository does
not contain the filed specification, a filing receipt or a public application
with examined claims. The USPTO confirms that [unpublished applications are
generally held in confidence](https://www.uspto.gov/web/offices/pac/mpep/s103.html).

What can be reviewed is Perseus's own [claim
map](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/disclosures/CLAIM-MAP.md)
and the documents labelled "Claims Summary" or "for attorney review." Those
are proposed claim descriptions. A published patent application with examined
claims remains unavailable.

This article can test the public novelty story.
Secret text remains outside its scope.

The public story still fails on its own terms. Perseus calls the material a
defensive publication of its "novel core" and says the documents distinguish it
from the closest prior art. The comparison begins after accepting
the project's preferred categories, then points inward from each element to a
Perseus-authored test or exhibit.

A test can establish implementation. A digest can establish artifact identity.
Neither establishes novelty. Patent law does not ask how many tests an applicant
generated.

For anticipation, the USPTO asks whether one reference contains
[every element of the
claim](https://www.uspto.gov/web/offices/pac/mpep/s2131.html).
For obviousness, it warns that a combination of familiar elements performing
their established functions is likely obvious when it produces only the
[predictable
result](https://www.uspto.gov/web/offices/pac/mpep/s2141.html).

## Every discrepancy makes the public claim stronger

The IP problem extends beyond incomplete prior art. In the reviewed documents,
the material discrepancies all move in the same direction.

| Underlying record | Perseus's stronger representation |
|---|---|
| The synthesis entry point returns a prompt and generates no claims | The disclosure says a citation gate verifies every generated claim before rendered output |
| A private helper checks only that some exact quote occurs in a cited range | The same disclosure describes claims as mechanically verified against their sources |
| `os.replace` prevents partial file publication, while mutual exclusion depends on an advisory lock that may fail open | The Agora disclosure says two agents cannot claim one task and the protocol works across NFS |
| Atlassian says it cannot confirm whether the employee has full ownership | Perseus's appended analysis says Atlassian declined to claim the project |
| Exhibit E4 derives model round trips from two chosen architectures | The commit calls it a benchmark that quantifies the patent's core technical effect |
| Accenture describes query-enriched chunks stored before a later prompt | The claim map calls the patent workflow orchestration with resolution interleaved with model calls |

The separate Vault repository supplies its own corrections. Its [claims
audit](https://github.com/Perseus-Computing-LLC/perseus-vault/blob/0e91c26c7c35f991336b990bfb29454b5757c179/CLAIMS-AUDIT.md)
records a retired sub-millisecond recall claim, an unsupported 100,000-entity
insert-rate figure, use of “signed” for a self-computed content hash and use of
“federation” for a local export, workspace rename and re-import.

Any one mistake could be ordinary. The reviewed set contains a pattern: source
material becomes broader, safer, more independent or more legally useful when
Perseus summarizes it. The project controls both layers.

The repository cannot establish intent. It can establish that every reviewed
discrepancy favours the same public story. That is enough to put the project's
candour in question. Perseus now needs to answer with the underlying records.

## The named patent search does not survive reading the patents

Perseus says its claim map records the closest located patent references. Three
of the references show how little pressure that search applied.

Accenture's [US 12,511,287](https://patents.google.com/patent/US12511287B1/en)
generates candidate queries for document chunks, classifies their quality,
adds selected query data to each chunk and stores the enriched chunk before a
later user prompt retrieves it. Perseus describes the patent as workflow
orchestration with resolution interleaved with model calls. The patent's own
summary describes precomputation and storage.

The Intuit row combines two separate inventions under “prompt construction /
context assembly.” [US 2025/0139367](https://patents.google.com/patent/US20250139367A1/en)
uses a large language model to translate a prompt into a planning problem. [US
12,423,313](https://patents.google.com/patent/US12423313B1/en) constructs and
searches hierarchical document graphs for RAG.

They have different inventors,
different priority dates and different mechanisms. Combining them under one
generic label hides the parts an element comparison would need.

These errors do not make either patent anticipate a Perseus claim. They do
show that the published “closest prior art” analysis cannot be trusted as a
description of the references it names. A claim map prepared for examiners
needs claim-by-claim citations and quotations. Perseus published a row of
conclusions.

## The ancestry starts in the 1970s

Perseus entered several mature fields at once.

[GNU m4](https://www.gnu.org/software/m4/manual/m4.html) copies input to output
while expanding registered macros. It includes and recursively processes files,
runs shell commands and can choose whether command output is scanned again.
The design descends from 1970s macro processors.

[Docutils](https://docutils.sourceforge.io/0.22/docs/howto/rst-directives.html)
uses one extensible directive syntax backed by a central directive registry.
Its include directive reads another document and parses it in the current
document context. Its raw directive passes content through untouched. Its
[2009-era documentation](https://docutils.sourceforge.io/0.6/docs/ref/rst/directives.html)
even treats file insertion and raw content as separate security-sensitive
capabilities.

[Org Babel](https://orgmode.org/worg/org-contrib/babel/intro.html) executes many
languages embedded in a document, passes data between blocks and places results
back into an exported document. Its documented options include result modes,
sessions, noweb composition and [cached
evaluation](https://orgmode.org/worg/org-contrib/babel/header-args.html). A
public tutorial records Babel in Org 7.0 and later by
[2011](https://orgmode.org/worg/org-contrib/babel/how-to-use-Org-Babel-for-R.html).

Make was already tracking file relationships, walking a dependency graph
depth-first, consulting modification times and executing only required actions
in the 1970s. Stuart Feldman's [1979
paper](https://onlinelibrary.wiley.com/doi/10.1002/spe.4380090402) says Make had
been used on Unix since 1975. Bazel later turned declared action inputs,
environment and commands into hashes and checked local and remote caches before
executing missing actions. That process is described in Bazel's [remote-cache
documentation](https://bazel.build/remote/caching).

The model-specific bridge is also old by Perseus's asserted filing date. The
2020 [RAG paper](https://arxiv.org/abs/2005.11401) retrieves from external memory
and conditions generation on the retrieved passages. MCP's November 2024
specification already separated [resources, prompts and
tools](https://modelcontextprotocol.io/specification/2024-11-05).

Perseus's claim documents narrow each predecessor until it no longer competes.
RAG becomes static embeddings. LangChain becomes data fetched at some
irrelevant earlier time. MCP becomes a mandatory sequence of model-driven tool
calls.

Those characterizations shrink the category until each comparison stops being
useful. A retriever can query a live source. A chain can execute immediately
before inference. An MCP client can read resources or invoke tools without
forcing one serial model round trip per context item.

## Every public claim starts with old machinery

The following table covers every substantive cluster in the public claim map
and its linked disclosures. Each row strips the Perseus label down to the
mechanism underneath it. Every mechanism is old, and none of the repackaging
produces an unexpected result.

| Public claim theme | Earlier work the comparison omits | What remains after the label is removed |
|---|---|---|
| Resolve typed annotations before model invocation | m4, Docutils, Org Babel, CMake configuration and RAG | Preprocessing data and inserting the result into a later consumer |
| Context tiers and selective loading | CPU and storage hierarchies, cache tiers, prompt budgets, Aider repo-map ranking and Continue context selection | A priority label on material competing for a bounded context window |
| Quote-preserving normalized cache keys | Lexers that distinguish quoted literals from insignificant whitespace, canonical serialization and content-addressed caches | A conventional choice of canonicalization before hashing |
| Checkpoint-correlated reinforcement | Implicit-feedback recommenders, delayed-feedback bandits and editor suggestion telemetry | Treating a later developer event as an implicit outcome label |
| One registry as a policy spine | Reference monitors, XACML policy decision and enforcement points, extension manifests and capability tables | Security metadata attached to dispatch entries |
| Citation-gated synthesis | Attributed generation, RARR, AIS, ALCE and ordinary exact-string validators | Checking that a quote exists, without checking that it entails the generated claim |
| Static directive graph and predictive prefetch | Aimee, LlamaIndex ingestion caching, Prompt Cache, RAGCache, TurboRAG, Make, Ninja and Bazel | A file modification-time wrapper around ordinary precomputation and cache reuse |
| File-based multi-agent task coordination | Blackboard systems, Linda tuple spaces, spool directories, Maildir, Git task trackers, AutoGen, Task Master and Beads | Task metadata and a claim/complete protocol stored in project files |
| Uniform grammar over six source classes | Shells, macro processors, Docutils registries, Org Babel, Continue context providers and MCP | Counting six back ends behind one dispatch table |
| Recursive include resolution with path and inode cycle checks | Recursive preprocessors, bounded include depth, filesystem identity and graph-cycle detection | Applying standard recursion guards to included context files |
| Resolver output remains literal data | Quoting, literal/raw blocks, non-evaluating template output and m4 `syscmd` behavior | A parser non-reentry rule |
| Local FTS memory with deterministic output | SQLite FTS5, BM25 and local search indexes | Running an old retrieval algorithm without a network call |

The table supplies the search plan the project's own "closest prior art"
analysis should have performed before declaring a novel core. Legal conclusions
require the actual claims and a complete record.

## The combinations are old machinery with longer claim language

Perseus took routine implementation choices and wrote them as longer
combinations. Longer wording changes the packaging. It contributes no
mechanism.

The exact quote-aware cache normalization joins lexer rules, canonicalization
and a content-addressed cache. The registry, per-dispatch gate and named
permission profiles join plugin dispatch, capability metadata and policy
profiles. The citation rule performs exact span validation.

The file-task
protocol joins dependency-aware task records with ordinary filesystem
publication and locking. The immutable ancestor chain applies graph-cycle
detection to path and device-inode identity. The six-source grammar is a plugin
registry and adapter with six entries.

Each part performs its established function. Whitespace outside literals is
normalized so equivalent inputs share a cache entry. Capability metadata selects
a gate. A cited string is checked against its source range.

A task record changes
state under a lock. Device and inode identify the same file through an alias. An
adapter presents different back ends through one call shape. The results are the
results a competent developer would expect.

Every combination is old. Perseus could not have pioneered any of them.

Document preprocessors, build systems, attributed-generation work, policy
systems and existing AI tools supply the mechanisms. Token limits, latency,
extensibility and crash safety supplied the reasons to combine them long before
Perseus existed. The results were predictable.

The [full fifteen-item chart](../evidence/public-claim-chart-2026-08-30.md)
records the exact combination, source grade, combination rationale, strongest
Perseus framing and expected technical result. Every row reaches the same
engineering conclusion: old mechanisms, routine combinations and predictable
results. Perseus's short comparison did not identify any of the closest prior
art documented in this review. It omitted the relevant predecessor classes,
the direct LLM systems, Aimee, and the Rovo and Teamwork Graph products built
by the claimed inventor's employer.

### Resolve before context is preprocessing

The first disclosure opens with the categorical statement that prior approaches
"all resolve state at inference time." GNU m4 alone is enough to disprove the
category. It resolves files and command output while producing text for a later
consumer. CMake's
[`execute_process`](https://cmake.org/cmake/help/git-stage/command/execute_process.html)
runs commands during configuration, before it generates the build system.

The alleged technical effect is fewer model round trips. That follows directly
from moving known work out of an agent loop and doing it first. A system that
prepares one prompt makes one model call because it prepares one prompt.

The
absence of an unnecessary model call is useful. The resulting call count does
not date the preprocessor to 2026.

### Six entries still make a registry

The unified-grammar disclosure calls unification its "novelty anchor." It
requires one registry, parser-recognized names derived from that registry, a
common adapter and six source classes: files, recursive composition, shell,
memory, sub-agents and tools.

Docutils already says application directives can be added with
`register_directive`, while core names live in `_directive_registry`. Continue
exposed one `@` context interface for files, code, Git diffs, terminal output,
open files, clipboard, workspace trees, debugger state, repository maps and
external providers. Its [context-provider
documentation](https://docs.continue.dev/customize/deep-dives/custom-providers)
also records deprecated providers for commits, Discord, Jira, databases, URLs,
search and the web.

The number six supplies a count. Calling the values "source classes" supplies
a category. A registry already exists to let a developer add a row without
editing the parser.

### The cache claims describe ordinary canonicalization

Perseus proposes collapsing whitespace outside quoted strings, preserving
whitespace inside them, hashing the normalized directive and caching the
result. Lexers have distinguished syntax whitespace from quoted literal
content for decades. Build systems and content-addressed stores hash canonical
inputs so equivalent requests share results.

The normalization rule is ordinary lexer-aware canonicalization. It gives the
cache the behavior a programmer would predict: irrelevant spacing stops causing
misses while quoted arguments retain their meaning. Perseus added no new cache,
parser or canonicalization mechanism.

### Checkpoint reinforcement renames implicit feedback

The checkpoint disclosure recommends a skill, observes a later checkpoint and
treats a matching event as acceptance or prolonged absence as rejection. It
then updates a score and proposes A/B tests.

Recommender systems have learned from passive behavior for decades. Hu, Koren
and Volinsky's 2008 work is literally titled [Collaborative Filtering for
Implicit Feedback
Datasets](https://doi.org/10.1109/ICDM.2008.22). Delayed-feedback bandit work was
well established before 2026, including [linear bandits with stochastic delayed
feedback](https://arxiv.org/abs/1807.02089) in 2018. Visual Studio IntelliCode
records whether a developer selected a recommendation and uses the telemetry to
monitor recommendation quality, as Microsoft's [documentation
explains](https://learn.microsoft.com/en-us/visualstudio/ide/intellicode-visual-studio).

A checkpoint is another observable event. A time window is another attribution
rule. The word "reinforcement" leaves the learning method unchanged.

Worse,
absence inside an arbitrary window produces an unreliable rejection label.
The developer may have stopped work, changed branches, completed the task
without the expected checkpoint text or accepted the advice without recording
the matching words.

### The five-site trust boundary is a checklist

Perseus identifies shell execution, filesystem reads, foreign content, plugins
and redaction. It stores capability metadata in registry entries and describes
the renderer as the common enforcement point. The proposed claim also includes
named permission profiles that seed default gates from one profile selection.

XACML standardized the separation between a policy decision point and a policy
enforcement point years ago. OASIS records that version 1.1 was approved in
[2003](https://www.oasis-open.org/committees/xacml/faq.php), and the 2013 XACML
3.0 specification defines the policy and enforcement roles
[directly](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.pdf).
Browser extension manifests have long declared API and host permissions.
Named security policies and profiles have long selected bundles of defaults.

More importantly, actual enforcement remains distributed. The registry records
facts such as `executes_shell` and `reads_files`.
Individual resolvers, transports and storage paths still perform path checks,
allow-list checks, redirect checks, authentication and output bounds.

The project's own security review found missed checks in those distributed paths.
A table describing five hazards remains a policy inventory.

The registry, per-dispatch consultation and named-profile combination is
obvious. A centralized dispatcher is the natural place to consult capability
metadata, and a named profile is the ordinary way to select a bundle of policy
defaults. Reference monitors, extension manifests and policy profiles already
supply the pattern.

Docutils already applied the same pattern to document
directives: one registry, parser-recognized names, capability-sensitive
directives and rendered document output. Perseus changes the back ends and
hands the rendered document to an AI assistant. The architecture remains old.

### The citation gate verifies quotation alone

The resolver-generator disclosure says Perseus mechanically verifies every
generated claim against source documents before admitting it. The proposed
claim summary is narrower. It requires an exact comparison between a supplied
quote and a cited line range, then drops claims whose citations fail that test.

The distinction matters. An exact-span validator can satisfy that proposed
claim while accepting a proposition the quote never supports. That weakness
refutes the disclosure's broad verification language. The narrower method is
still routine exact-span validation, with no semantic verification at all.

We ran the private validator in the pinned public build with this claim:

```json
{
  "text": "Perseus was independently audited by NASA.",
  "citations": [{
    "source_id": "src1",
    "line_start": 3,
    "line_end": 3,
    "quote": "The resolver builds a dependency graph."
  }]
}
```

The validator [accepted the claim and dropped
nothing](../evidence/raw/2026-08-30-citation-gate-semantic-mismatch.txt). Exact
string presence establishes quotation. Entailment requires the quote to support
the proposition.

The field had already confronted the real problem. [RARR](https://arxiv.org/abs/2210.08726)
searched for attribution and revised unsupported model output in 2022. The AIS
framework asks whether a source supports a proposition. The [AIS
paper](https://aclanthology.org/2023.cl-4.2/) defines that relationship.

[ALCE](https://arxiv.org/abs/2305.14627)
evaluated citation correctness and citation quality in 2023.

The larger implementation gap is simpler. We called the public synthesis entry
point with generation enabled and a configured model name. It returned a prompt,
reported `generated: false` and produced no claims to validate. The function's
own note says in-process generation was removed.

The [recorded
run](../evidence/raw/2026-08-30-production-synthesis-path.txt) matches the source:
tests call the private validator with hand-built responses, while the production
path never consumes the host's answer.

Perseus has reduced an exact-string helper to practice. The reviewed build does
not contain the disclosed end-to-end gate from model answer to validated rendered
output. Describing every generated claim as mechanically verified crosses from
optimistic architecture into a false account of the running path.

### Dependency prefetch was already routine in LLM systems

Perseus statically identifies directive dependencies, checks file modification
times, computes cache keys and preloads existing entries before normal
resolution. The disclosure itself admits Make, Bazel and Ninja, then attempts
to escape them because their domain is software builds rather than model
context.

Aimee was publicly accessible by February 2026, before Perseus's asserted May
filing. It pre-indexed repository files and dependency edges before model
sessions, tracked content hashes and freshness, and reused stored results while
assembling context. It discovered likely inputs early and avoided recomputing
unchanged work.

The broader LLM field had already made the pattern routine. LlamaIndex
[`v0.10.17`](https://docs.llamaindex.ai/en/v0.10.17/module_guides/loading/ingestion_pipeline/root.html)
hashed every node-and-transformation pair, persisted the cache, reused matching
results and skipped documents whose stored hash had not changed.

[Prompt Cache](https://arxiv.org/abs/2311.04934) described precomputing and
storing attention states for reusable prompt modules, including documents used
as context, in November 2023. [RAGCache](https://arxiv.org/abs/2404.12457)
cached retrieved knowledge's intermediate states and overlapped retrieval with
inference in April 2024. [TurboRAG](https://arxiv.org/abs/2410.07590) precomputed
document-chunk key-value (KV) caches offline and retrieved them for model
prefill in October 2024.

Make and Bazel remain older examples of the same engineering rule. The closer
references are LLM systems that identified reusable model inputs, keyed or
precomputed them, reused cached work and processed misses. Perseus added a file
modification time and directive syntax to an optimization Aimee and the rest of
the LLM field were already using. It pioneered nothing here.

### Agora inherits the blackboard

Agora stores task status, agent identity and dependency references in Markdown
frontmatter. Agents list, claim and complete those tasks. Git supplies history.
The disclosure contrasts this only with remote issue trackers, brokers, pull
requests and bare lock files.

That list omits the lineage of the design. Hearsay-II used a shared blackboard
where independent knowledge sources communicated through a uniform global
working memory in the 1970s. The [1980 system
paper](https://mas.cs.umass.edu/Documents/Erman_Hearsay80.pdf) describes the
blackboard, task agenda and scheduler. Linda used a shared tuple space for
coordination.

Maildir writes a file in `tmp` and moves it into `new`, avoiding
partial delivery and supporting shared filesystems; its design is documented
as [reliable over NFS](https://cr.yp.to/proto/maildir.html).

The AI-tool field was crowded too. Microsoft's
[AutoGen](https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat/) offered
a unified multi-agent conversation framework in 2023. By 2025, Claude Task
Master stored task status and dependencies, selected the next unblocked task
and generated individual task files.

Public June 2025 reports show its
[`next` command selecting work from status and
dependencies](https://github.com/eyaltoledano/claude-task-master/discussions/680).
Beads then supplied a Git-friendly dependency graph, ready-work selection,
claiming and closing for coding agents. Claude-flow coordinated agent swarms
with shared memory before Perseus's asserted filing date.

The Markdown-frontmatter task protocol is also obvious. Existing agent tools
already stored task status, dependencies and agent work locally. Filesystem
publication and locking are the standard way to coordinate changes without a
server.

Markdown frontmatter is a serialization choice. It contributes no new
mechanism.

Perseus's concurrency guarantee is also overstated. `os.replace` prevents a
reader from seeing a partially written file. Atomic "claim this task if still
open" requires a state comparison too.

The project later added a [lock and a
second read](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/src/perseus/audit.py) after
documenting a race where two claimers both won. Its lock helper deliberately
[swallows lock failures](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/src/perseus/config.py)
and continues, so the guarantee still depends on a
working advisory-lock implementation. A portable compare-and-swap guarantee
across NFS clients requires more.

We forced the lock helper's documented fail-open condition and synchronized two
claimers after both read the task as open. [Both returned
success](../evidence/raw/2026-08-30-agora-lock-failure.txt). The run does not show
that a supported production filesystem will reject the lock.

It shows that the
code path Perseus deliberately permits cannot sustain the disclosure's
unqualified guarantee. NFS safety needs a named locking protocol, server and
mount assumptions, plus a multi-client test.

### Recursive includes inherit old parser controls

The recursive-resolution disclosure claims depth-first include processing,
path and device-inode cycle detection, a depth limit, a typed dependency graph
and a rule that resolver output is not parsed again.

GNU m4 recursively parses included files. The C preprocessor scans included
files before returning to the parent stream and has a configurable [maximum
include depth](https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html).
Make traverses dependencies depth-first.

Filesystem tools identify hard links
with the device and inode pair; GNU Find documents that relationship in its
[hard-link reference](https://www.gnu.org/software/findutils/manual/find.html#Hard-Links).
Literal and raw blocks have always meant "do not interpret this as more source."

Path plus inode is sensible defensive engineering. It catches aliases that a
string-path check can miss. Combining filesystem identity with standard cycle
detection produces a familiar recursive document architecture.

The path-and-inode ancestor chain is obvious too. Recursive parsers need cycle
detection. Paths have aliases. Device and inode identify the underlying file.

Putting that identity in the active ancestor set is the direct fix a competent
developer would make. The word “immutable” describes the data structure, not an
invention.

## The AI projects Perseus writes out of the history

The older systems defeat the idea that the mechanisms were born with LLMs. The
following projects defeat the narrower suggestion that nobody had assembled
those mechanisms for AI development before Perseus.

- **Aider, 2023.** Aider automatically built a repository map with tree-sitter,
  ranked a code dependency graph to fit a token budget and sent the selected map
  with each model request. Its dated [October 2023 design
  note](https://aider.chat/2023/10/22/repomap.html) describes the entire path.

- Continue. Continue's public repository dates to [May
  2023](https://github.com/continuedev/continue/commit/0877ada8ed9f71f3ee792bcb34a4005e3c86827d).
  Its current history records typed `@` context providers for files, code, diffs, terminal
  output, trees, debugger state, repository maps, databases, issue trackers,
  URLs and web search. Rules were concatenated into model requests.

- Cursor. Cursor uses `@Files`, `@Folders`, `@Code`, documentation, Git
  history and persistent project rules as model context. Rules can be selected
  by path or relevance and are [included at the start of model
  context](https://docs.cursor.com/context/rules-for-ai).

- Claude Code. `CLAUDE.md` supplies project instructions at session start,
  hooks run external commands at lifecycle points and sub-agents receive fresh,
  scoped context. Anthropic's own [context-loading
  description](https://code.claude.com/docs/en/features-overview) lays out the
  tiers and timing.

- GitHub Copilot. Repository instruction files automatically add project
  context to requests. GitHub's current CLI goes further and recursively imports
  instruction files with depth, cycle and size guards.

- Repomix and related repository packers. These tools collected a repository
  into a bounded artifact intended to be handed to a model. A public October
  2024 issue discusses splitting packed output by model token capacity and using
  the packed repository as AI context in the [Claude Projects
  workflow](https://github.com/yamadashy/repomix/issues/71).

- **Cline memory-bank practice, 2025.** Public Cline discussions from February
  2025 describe persistent project files, an MCP-backed memory bank, scoped
  files, eventual vector retrieval and reuse across Cline, Cursor and Claude.
  The [dated discussion](https://github.com/cline/cline/discussions/1818) is a
  particularly direct warning against treating local model memory as a 2026
  invention.

- AutoGen, Claude Task Master, Beads and claude-flow. These projects covered
  multi-agent conversation, dependency-aware tasks, ready-work selection,
  claiming, persistent shared state, swarm coordination and memory. Historical
  April 2026 artifacts for [Beads](https://github.com/steveyegge/beads/blob/8694c53589f122ce622600cee377e820452b50ca/README.md)
  and [claude-flow](https://github.com/ruvnet/claude-flow/blob/1976c57ccdb6deb8c5750ed6cb62eae7a057ae17/README.md)
  carry pre-May commit timestamps. Storage and control plane remain
  implementation choices inside an established category.

The legal standards explain why exact product identity is unnecessary. A broad
claim can be anticipated by one reference. A combination can be
obvious when known pieces are assembled for their known functions. Perseus's
documents repeatedly argue that the field is new because one project has put
many old pieces behind one name.

## His employer had published the same field two years earlier

Perseus's own July strategy documents acknowledge Atlassian as an adjacent AI
context and memory platform. Atlassian's public record supplies the earlier
dates.

On [1 May
2024](https://www.atlassian.com/blog/announcements/introducing-atlassian-rovo-ai),
Atlassian introduced Rovo and its Teamwork Graph. The graph pulled data from
Atlassian products and connected SaaS applications into one view of goals,
knowledge, teams and work. Rovo returned contextual results and in-context
knowledge cards, grounded chat in company data, and supplied agents that could
synthesize enterprise information and act from instructions or workflow
triggers.

By [14 January
2025](https://www.atlassian.com/blog/development/atlassian-developer-innovation-rovo-for-github-copilot),
Rovo for GitHub Copilot brought Jira and Confluence data into the developer's
IDE. Atlassian described Copilot using that synthesized domain knowledge as
additional context while writing code. This is repository-adjacent context
assembly for an AI coding assistant, published sixteen months before Perseus's
asserted filing month.

Atlassian then published context-aware search across more than fifty connected
applications with links to sources in [July
2025](https://www.atlassian.com/blog/rovo/rovo-search-quality). In [August
2025](https://www.atlassian.com/blog/ai-at-work/rovo-chat-august-2025-updates),
it added persistent memory tied to a user profile and backed by Teamwork Graph.
On [4 February
2026](https://www.atlassian.com/blog/announcements/atlassian-rovo-mcp-ga), its
Rovo MCP server became generally available, giving AI clients one controlled
interface to Jira and Confluence context.

The overlap runs across the product, not one patent phrase:

| Perseus surface | Atlassian product published before the asserted filing | Functional overlap |
|---|---|---|
| Context Engine renderer, dependency graph and assistant context packs | Teamwork Graph, Rovo Search, Rovo for GitHub Copilot and [Rovo Dev](https://www.atlassian.com/blog/blog/announcements/rovo-dev-command-line-interface) | Collect live work and knowledge from several sources, select relevant context and supply it to an AI assistant before or during a task |
| Perseus Vault persistent memory | Rovo's Teamwork Graph-backed profile memory | Retain context across conversations, personalize later retrieval and learn from an explicit correction |
| Vault hybrid recall, source anchors and cited synthesis | [Rovo Search](https://www.atlassian.com/blog/atlassian-engineering/unraveling-rovo-search) across more than fifty connectors | Rank cross-source knowledge, synthesize answers and attach source links or passage-level citations |
| Guide, agent directives and bounded synthesis | Rovo Agents and Rovo Dev | Give an agent instructions, knowledge and actions, then use it to plan, synthesize and execute work |
| Agora task state and agent coordination | Jira, Rovo Dev and [Agents in Jira](https://www.atlassian.com/blog/announcements/ai-agents-in-jira) | Represent work, dependencies and ownership; assign it to agents; track execution and preserve a work trail |
| Unified adapters, assistant profiles and MCP serving | Rovo MCP and [Rovo Studio MCP skills](https://www.atlassian.com/blog/announcements/rovo-mcp-gallery) | Present several data and action surfaces to different AI clients through one controlled interface |
| Trust profiles, redaction and audit | Teamwork Graph permissions and [Rovo MCP controls](https://confluence.atlassian.com/cloud/blog/2026/02/atlassian-cloud-changes-jan-26-to-feb-2-2026) | Gate context and actions through existing permissions, scopes, domain and IP allowlists, and audit logs |
| Federation and cross-workspace memory | Teamwork Graph connectors | Join knowledge from Atlassian products and third-party workspaces into one retrieval plane |

Perseus describes its version as local, offline, portable and user-controlled.
Atlassian's version is managed, permission-aware and embedded in its products.
Those may be useful product differences. They do not create new context
assembly, memory, retrieval, agent, task or adapter mechanisms.

The most revealing overlap is operational. Perseus ships a
[`rovodev` profile](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/README.md#rovo-dev-mcpjson-in-repo-root),
renders `AGENTS.md` for Rovo Dev and tells users to pair that rendered context
with Perseus MCP tools. Perseus is designed to extend Atlassian's own coding
agent with context and tool surfaces that its novelty analysis places inside
Perseus's claimed core.

Atlassian had therefore published cross-source context assembly, persistent AI
memory, source-linked retrieval, coding-assistant context and agent workflows
before Perseus. The products differ in deployment and representation. The
technical field does not.

Perseus's published closest-prior-art table names MCP, Accenture and Intuit. It
omits Rovo and Teamwork Graph. The omission is difficult to explain as an
obscure search miss. The claimed inventor worked for Atlassian, disclosed an
“AI Context Management Patent” to its legal department, and later wrote Perseus
strategy documents designed around Atlassian's existing platform.

Perseus's internal strategy is an admission of product proximity. It assigns
Atlassian product-native relevance, permission-aware retrieval, live work-graph
context and tenant-managed memory, then tells Perseus to differentiate through
longer retention, explicit control, explanations and portability. That is a
market-positioning carve-out inside the same product category. It is not an
account of a newly pioneered technical field.

### “Complementary” is positioning, not a market boundary

Perseus tries to turn the overlap into complementarity by defining Atlassian as
suite-bound and itself as portable. Competing products differentiate themselves
this way all the time. A local or on-premises product still competes with a
managed cloud product when both seek to become the context and memory layer
around the same teams and agents.

Perseus's own [competitive-analysis
method](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/competitive-analysis-phase1.md)
makes the point. It calls CogniRepo the most serious competitive threat in the
context-engine space because CogniRepo overlaps Context Engine and Vault
memory. It reaches that conclusion even while stressing that CogniRepo is
code-first and Perseus is workspace-first.

Atlassian overlaps those two surfaces plus agent workflows, task coordination,
cross-tool retrieval, citations, permission-aware serving, MCP access and
developer context. Perseus also solicits [technical teams evaluating agent and
developer workflows](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/design-partner-onboarding.md)
and [government programs and
primes](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/federal-buyers.md)
to adopt its context and memory layer around their models. It seeks the same
architectural position that Rovo and Teamwork Graph occupy.

Perseus can extend Rovo Dev in one deployment while competing with Rovo and
Teamwork Graph for control of cross-tool context and durable memory. Products
can complement each other at one interface and compete across the rest of the
stack. Perseus's instruction to avoid “head-on competition” acknowledges the
competition. It does not erase it.

Employment alone establishes no prior art. Atlassian's dated public disclosures
do. The employment relationship makes their omission from Perseus's novelty
analysis, and the unresolved ownership warning from Atlassian legal, materially
harder to dismiss.

## Aimee is one predecessor in a crowded field

Rakuen builds `aimee`. We have a direct commercial interest in this comparison.

Aimee was publicly accessible by February 2026, before Perseus's asserted May
filing. It already provided persistent memory, pre-session context assembly,
tiered retrieval, safety gates, delegated agents, outcome-aware routing, task
state and dependency-aware repository indexing. Perseus's novelty comparison
omits it.

The case has independent support. Aider, Continue, Cursor, Cline, Repomix,
Claude Code, MCP, AutoGen, Task Master, Beads and claude-flow prevent
the dispute from becoming one competitor's word against another's. They show a
field converging on repository context, persistent instruction files, local
memory, typed providers, dependency-aware work and multi-agent orchestration
well before Perseus wrote its claim map.

## Ownership: Perseus documented the Atlassian overlap itself

Perseus also publishes an [Atlassian legal
email](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/ip/2026-06-01-atlassian-legal-response.md).
The repository titles it an employee invention disclosure for an “AI Context
Management Patent.”

The email says Atlassian normally does not review side projects and cannot
confirm that the employee has full ownership. It tells the employee to assess
the agreement and maintain segregation.

Perseus's appended analysis turns that into "declined to review or claim
ownership" and calls it a good paper trail. Those are different propositions.
A decision to skip review supplies no disclaimer, release or assignment. The
email expressly refuses to confirm ownership.

Perseus's own July strategy records make the product overlap explicit. A
[strategy owned by Thomas
Connally](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/strategy/perseus-durable-cognition-strategy-2026-07-20.md)
describes Atlassian as building managed enterprise memory across Rovo, Jira,
Confluence, chat, Teamwork Graph and agent sessions. It tells Perseus to avoid
head-on competition. The accompanying [one-page
strategy](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/strategy/perseus-memory-one-page-2026-07-20.md)
assigns Atlassian product relevance, permission-aware retrieval, live work-graph
context and tenant-managed memory, then instructs Perseus: “Do not build
‘Atlassian memory, but better.’”

Those documents do not establish Connally's job duties or the scope of his
employment agreement. They establish that Perseus and its author recognized
Atlassian as operating in the same AI context and memory field. The legal
email's warning about conflicts and its refusal to confirm ownership therefore
address a concrete overlap identified by Perseus itself.

The document proves neither Atlassian ownership nor clear title. Chain of title depends on the
employment agreement, the work performed, the resources used, applicable law
and any executed assignment or waiver. The repository contains no basis for the
stronger conclusion.

## Patent eligibility is another unresolved problem

The claim map invokes Section 101 by describing dependency graphs, reduced
round trips and deterministic output as improvements to computer functioning.
Eligibility turns on the claimed mechanism.

USPTO guidance identifies high-level collection, analysis and display of
information as a recurring abstract-idea problem. It also warns that limiting
an abstract process to a field of use or implementing it with generic computer
functions may add nothing meaningful. The current [eligibility
guidance](https://www.uspto.gov/web/offices/pac/mpep/s2106.html) permits
software claims with the required eligible mechanism. Result-oriented language
alone remains insufficient.

Without the filed specification and actual claims, this section identifies an
eligibility risk. It cannot decide eligibility.

Most public Perseus summaries read as desired results: collect selected
information, apply policies, cache it, arrange it and present it to a model.
The concrete mechanisms offered in support are registries, parsers, graphs,
hashes, files, locks and string comparisons. Those are the same mechanisms the
prior-art analysis shows were routine. Moving their output into an LLM prompt
does not automatically transform information processing into a new computer.

## Security: The policy spine is a description

The [resolve-before-context
disclosure](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/disclosures/disclosure-1-resolve-before-context.md)
calls the directive registry a single policy spine. Each directive declares
whether it executes shell commands, reads files, mutates state or can be
cached. The parser and tooling derive behavior from that registry.

Metadata describes a boundary. Resolver code enforces it. Network destinations, redirects, output limits,
authentication, redaction and file paths each need a correct check at the point
of use.

Perseus labels its [July 2026 security
review](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/security-review-2026-07-05.md)
an “Independent pre-launch audit.” Git attributes the commit that introduced it
to Perseus Computing, with Claude Opus listed as a co-author. The document names
no external auditor.

The project's own [security
milestones](https://github.com/Perseus-Computing-LLC/perseus/blob/e7bbeb35485e67876947c87eda7e98028ddb4a29/docs/SECURITY-MILESTONES.md)
say an independent external audit remains a hard gate that has not been met.
“Independent” may refer to a separate internal or agent review pass. The public
record never says.

The review demonstrates the gap. It found federation egress that had skipped the existing
SSRF and redirect guards, an allow-list bypass in `@tool`, a symlink escape in
`@tree`, fail-open update verification, unbounded network reads and several
deployment problems. The review says several reported critical findings did
not survive manual verification.

That manual rejection is good security work. It is also evidence that producing
findings was easier than establishing them.

The project has repaired several of those paths since the review. The pattern
remains more important than the old bugs. A central registry can describe the
capability class while the real policy stays distributed across every resolver,
transport and cache.

The security claim should describe the enforcement that exists. The current IP
language describes the enforcement the architecture wants.

The milestone sets the right limit. The rest of the repository should inherit
it. Our work here was a static source and document review plus three narrow
runtime checks.

It was not a penetration test, deployment review or dependency
audit. The article makes no general finding that current Perseus releases are
insecure.

## Memory: The encrypted body leaves a plaintext memory

[Perseus Vault](https://github.com/Perseus-Computing-LLC/perseus-vault/tree/0e91c26c7c35f991336b990bfb29454b5757c179)
opens with “Persistent, encrypted memory for AI agents.” The body field is
encrypted with AES-256-GCM by default for fresh installations. The useful
caveat sits much lower: its FTS5 search index contains the body in plaintext.
Metadata stays plaintext too.

Optional embedding vectors are also stored in plaintext and may reveal semantic
content.

The project's [security
policy](https://github.com/Perseus-Computing-LLC/perseus-vault/blob/0e91c26c7c35f991336b990bfb29454b5757c179/SECURITY.md)
states the consequence directly. Body encryption does not make the database
file opaque. Full-disk encryption must protect the index and metadata.

The
[threat
model](https://github.com/Perseus-Computing-LLC/perseus-vault/blob/0e91c26c7c35f991336b990bfb29454b5757c179/docs/THREAT-MODEL.md)
also says workspace scoping is a routing and relevance control under its
trusted-caller model, not multi-tenant isolation. That threat model is pinned
to v2.2.1, so it cannot establish every property of the current v2.23 series.
The current README and security policy confirm the plaintext index.

Vault's own [claims
audit](https://github.com/Perseus-Computing-LLC/perseus-vault/blob/0e91c26c7c35f991336b990bfb29454b5757c179/CLAIMS-AUDIT.md)
records what happened when someone finally checked the prose against the
artifacts. The project retired sub-millisecond recall, removed an unbacked
100,000-entity insert-rate figure, replaced “signed” with “content-hashed” and
clarified that “federation” meant a local export, rename and re-import. Those
corrections deserve credit. They also establish that product claims had outrun
the evidence more than once.

Vault repeats the “Independent pre-launch audit” label in a review introduced
by a commit attributed to Perseus Computing and co-authored by Claude Opus. Its
[security milestones](https://github.com/Perseus-Computing-LLC/perseus-vault/blob/0e91c26c7c35f991336b990bfb29454b5757c179/docs/SECURITY-MILESTONES.md)
say the full independent audit remains open. The review found that the claimed
audit chain was not tamper-evident, a documented authentication flag was dead,
the installer failed open, the container ran as root and the claimed
`cargo audit` CI job did not exist.

Later commits repaired several findings.
The unresolved issue is the label. The public record identifies no independent
auditor for a review that the same repository says has yet to happen.

## Determinism: Frozen inputs make an ordinary program repeat

The IP documents describe byte-reproducible output as a technical effect. The
qualification does the work: external state must be frozen.

Perseus can resolve dates, environment variables, files, Git state, shell
commands, services, HTTP responses and mutable memory. Those values can change
between renders. Freeze the source document, configuration, filesystem,
process state, network responses, clock and memory, and a deterministic
renderer can reproduce its bytes. The same is true of a build system or a
template engine.

Reproducibility is useful. It can support debugging, cache correctness and an
audit trail. The public argument still has to identify the mechanism that
differs from ordinary deterministic preprocessing.

A hash of the finished
artifact proves byte identity alone. Truth, safety and inventiveness require
separate evidence.

## Context: Literal parser output remains model instructions

One disclosure says resolver output is inserted as literal data and never
reparsed as a directive. That is a real parser property. Resolved output cannot
create another Perseus directive unless an authored include edge permits it.

The next consumer is a language model. Perseus writes the result into files
whose purpose is to instruct that model. The model receives parser data and
instructions as token sequences. A malicious file, memory, command result or remote source can still place
imperative text into the final context.

Markers and fences help a model interpret the boundary. They remain soft
controls. The product contract should say who controls each source,
which content may enter an instruction-bearing artifact and what happens when
sources disagree. The renderer's parse rule answers a smaller question.

## Engineering: Proof needs an owner outside the generator

Vibe coding is a production method. It can generate useful code quickly, and
Perseus contains a substantial amount of useful work. Its shell gates default
closed. Path resolution canonicalises before checking containment.

Later fixes
bounded remote reads, labelled remote context and tightened several transport
checks. The maintainers also preserved an internal review that records findings
they rejected.

Speed becomes dangerous when the same process produces the claim and the proof
of the claim. Generated tests tend to confirm the implementation's own model.
Generated comparisons inherit the prompt's taxonomy.

Generated claim maps make
every feature look intentional and every intention look novel. More output
then increases confidence without adding an independent challenge.

The replacement is procedural:

- **Keep claim and test separate.** Give a reviewer authority to reject the
  taxonomy, fixture and success condition before the result exists.

- **Check the strongest predecessor.** Start with document preprocessors,
  build systems, retrieval pipelines and existing agent context tools. Chart
  their elements and dates before writing the distinction.

- **Run the test where the boundary executes.** Registry metadata is a source map.
  Resolver, transport and storage code enforce the policy.

- **Keep evidence classes separate.** A static audit, runtime test, benchmark,
  vendor report and legal conclusion carry different weight.

- **Record the subject's answer.** Put the specific technical findings to the
  maintainers and publish their strongest supported response beside them.

Perseus could narrow its IP story to the mechanism it can defend, keep its
security claims inside the audit it has completed and present its benchmarks as
measurements under named conditions. The context engine would then stand on its
implementation.

The current package asks its artifacts to testify for one another. They are the
same witness.
