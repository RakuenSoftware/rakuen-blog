# Perseus public proposed-claim chart

Date: 2026-08-30

Status: reporting work product. Publication hold.

## Method

This chart maps the fifteen proposed claims in Perseus's public disclosure
summaries. It does not purport to reproduce the confidential provisional. Each
row distinguishes four questions:

1. What combination did Perseus actually describe?
2. Which earlier source supplies which limitation?
3. What reason would have led a skilled developer to combine the sources?
4. Does the combination produce any interaction or result beyond the expected
   behavior of its parts?

Every public combination joins established mechanisms under familiar
engineering pressure and produces the expected result. Longer wording does not
turn those combinations into technical inventions. This chart evaluates
Perseus's public novelty narrative. It does not offer an invalidity opinion on
confidential claims that the public cannot inspect.

## Evidence grades

- **A:** independently dated standard, paper, patent publication or stable
  contemporary design note with the relevant mechanism.
- **B:** dated public repository discussion, release or historical artifact whose
  feature content is visible.
- **C:** current documentation with incomplete feature chronology, or a Git
  commit whose historical public accessibility has not been independently
  corroborated.
- **D:** category analogy only. Useful for a search or combination rationale,
  insufficient as element proof.

## Atlassian's dated prior-art family

The claimed inventor's employer published a particularly direct sequence before
Perseus's asserted filing month:

| Date | Atlassian publication | Public mechanism | Perseus clusters |
|---|---|---|---|
| 2024-05-01 | [Rovo introduction](https://www.atlassian.com/blog/announcements/introducing-atlassian-rovo-ai) | Teamwork Graph ingests Atlassian and connected SaaS data; Rovo returns contextual results and company-grounded chat; instructed agents synthesize enterprise information and run from workflow triggers | D1.1, D1.2, U1.1; general agent orchestration |
| 2025-01-14 | [Rovo for GitHub Copilot](https://www.atlassian.com/blog/development/atlassian-developer-innovation-rovo-for-github-copilot) | Jira and Confluence knowledge is synthesized into additional context used by an AI coding assistant inside the IDE | D1.1 and model-facing context assembly |
| 2025-07-24 | [Rovo Search quality](https://www.atlassian.com/blog/rovo/rovo-search-quality) | Context-aware answers across more than fifty connected applications, with links to sources | D1.2 and the broader D4.1 attribution problem |
| 2025-08-26 | [Rovo persistent memory](https://www.atlassian.com/blog/ai-at-work/rovo-chat-august-2025-updates) | Persistent memory tied to a user profile and backed by Teamwork Graph | U1.3 and persistent context |
| 2026-02-04 | [Rovo MCP general availability](https://www.atlassian.com/blog/announcements/atlassian-rovo-mcp-ga) | One controlled interface gives AI clients access to Jira and Confluence context | U1.1 and external context sources |

These publications establish Atlassian as prior art to the technical field and
to several public Perseus elements. Perseus's later internal strategy documents
confirm that it recognized the overlap. Its published closest-prior-art table
omits Atlassian entirely.

## D1.1: resolve-before-context pipeline

**Published combination:** an authored document containing directives; one
registry holding resolver functions and security/cache metadata; resolution at
context-assembly time; plain-text output; and model consumption without the
model issuing inference-time tool calls for those directives.

**Earlier elements:**

- GNU m4 provides authored macros, registered operations, file inclusion,
  command execution and text output before a later consumer. Grade A.
- Docutils provides an extensible directive registry and document rendering.
  Grade A.
- Org Babel provides one document surface over heterogeneous executable source
  types and inserts the results into exported text. Grade A.
- RAG establishes that externally retrieved text is supplied as model context.
  Grade A.
- Aider establishes automatic repository-context assembly under a token budget
  before a model request. Grade A.

**Combination rationale:** prompt cost, latency and reproducibility give a direct
reason to perform deterministic work once before a model call. Aider documents
the token-budget pressure. Build and document preprocessors supply the familiar
implementation pattern.

**Strongest Perseus response:** the public summary places registry metadata and
prompt output in the same description.

**Status:** technically obvious. No unexpected interaction or result is stated.

## D1.2: registry-declared context tiers

**Published combination:** each registry entry carries a context tier, and the
renderer admits only directives at or below the selected tier to allocate a
bounded model context.

**Earlier elements:** Aider ranks a repository graph into a token budget. CPU,
storage and document systems supply tiered admission as category analogies.
Continue and Cursor supply typed or scoped model-context selection, but the
current source dates remain incomplete. Grades A, D and C respectively.

**Combination rationale:** a bounded context window creates the same capacity
problem that ranking and tiering already solve. Attaching the priority to an
existing registry row is the expected place to store it.

**Strongest Perseus response:** Perseus assigns a fixed tier to resolver types
instead of ranking content dynamically.

**Status:** technically obvious. A fixed tier is a routine simplification of
ranking or priority admission.

## D1.3: quote-preserving normalized cache key

**Published combination:** collapse whitespace outside quotes, preserve it
inside quotes, hash the normalized directive, and cache resolver output under
that hash.

**Earlier elements:** lexers distinguish literal content from syntactic
whitespace; canonical serializers normalize equivalent inputs; Bazel hashes
canonical action inputs; Org Babel caches document computations. Grades A and
D.

**Combination rationale:** semantically irrelevant spacing causing cache misses
is the ordinary reason to canonicalize before hashing. Preserving literal
contents avoids changing the directive argument.

**Strongest Perseus response:** the public summary specifies one normalization
rule for this parser cache.

**Status:** technically obvious. The normalization produces exactly the cache
behaviour a developer would expect.

## D2.1: checkpoint-correlated implicit reinforcement

**Published combination:** compare a later checkpoint description with earlier
skill recommendations, infer acceptance on a match, and infer rejection when a
window expires without a match.

**Earlier elements:** implicit-feedback recommenders, delayed-feedback bandits
and editor suggestion-selection telemetry. Grade A.

**Combination rationale:** a developer checkpoint is an observable outcome event.
Time-window attribution is a standard response to delayed outcome signals.

**Strongest Perseus response:** Perseus uses a project checkpoint description as
the delayed outcome event and treats expiration of one window as rejection.

**Status:** technically obvious. The noisy-rejection problem is also a model
quality defect.

## D3.1: registry gate plus named permission profiles

**Published combination:** registry metadata declares shell, file and mutation
capabilities; the renderer consults that metadata before dispatch; an unsatisfied
gate denies execution; one named profile seeds default gates across boundaries.

**Earlier elements:** reference monitors and XACML supply policy decision and
enforcement points; extension manifests declare capabilities; named policy sets
and security profiles seed groups of defaults; Docutils separates risky
directive capabilities. Grades A and D.

**Combination rationale:** once directive dispatch is centralized, capability
metadata and profile-derived defaults are the conventional way to avoid repeated
per-call policy configuration.

**Strongest Perseus response:** Perseus packages registry metadata, per-dispatch
consultation and named profiles in one document renderer.

**Implementation conflict:** network, redirect, path, authentication and output
checks remain distributed. Perseus's own security review found missed checks in
those paths. This challenges the broad “single policy definition” representation;
it does not itself prove the proposed combination old.

**Status:** technically obvious. Central dispatch, capability metadata and a
named policy bundle perform their ordinary functions.

## D4.1: exact-quote citation gate

**Published combination:** receive source documents and model-generated claims
with line citations; open the cited range; require the supplied quote to occur
exactly; drop claims whose citations fail that test.

**Earlier elements:** RARR, AIS and ALCE supply attributed generation and
support evaluation; ordinary span validators supply exact source matching.
Grade A.

**Combination rationale:** attributed generation already needs a mechanical way
to confirm that a quoted span came from the named source. Exact matching is the
simplest validator.

**Strongest Perseus response:** Perseus substitutes exact-string matching within
a line window for broader attribution or entailment machinery.

**Implementation conflict:** the reviewed production entry point returns a
prompt and never consumes or validates the host's answer. The private helper
accepts a false claim carrying an unrelated exact quote. The first fact
challenges reduction to practice. The second challenges the disclosure's broad
claim that every generated claim is verified “against” the sources. Neither fact
adds novelty to the narrow exact-string method.

**Status:** exact span validation is obvious, and the product representation is
contradicted by the rerunnable checks.

## D5.1: static dependency prefetch

**Published combination:** parse file-referencing directives, stat their targets,
compute directive cache keys, and preload matching cache entries before normal
renderer demand.

**Earlier elements:** Aimee pre-indexed repository files and dependency edges,
tracked hashes and freshness, and reused stored results during later context
assembly before Perseus's asserted filing month, according to Rakuen's
pre-rewrite records. LlamaIndex `v0.10.17` hashed and cached each
node-transformation pair and skipped unchanged document hashes. Prompt Cache
precomputed reusable LLM attention states in 2023. RAGCache cached retrieved
knowledge states in April 2024. TurboRAG precomputed document KV caches offline
in October 2024. Make and Bazel supply still older dependency, freshness and
cache-key machinery. Grades A and first-party C for the erased Aimee chronology.

**Combination rationale:** a directive that names a file exposes its dependency
before execution. LLM ingestion and inference systems already used hashes,
precomputed context state and caches to avoid repeating unchanged work. A file
modification time is an ordinary freshness input for the same operation.

**Strongest Perseus response:** Perseus applies the established sequence to
file-referencing directives and uses file modification times as freshness data.

**Status:** technically obvious and directly preceded in LLM systems. Directive
syntax and file modification times change no mechanism or result.

## D6.1: file-based agent task coordination

**Published combination:** task files with structured frontmatter containing
status, agent and dependency references; atomic claim and completion operations;
ready-work selection by dependency traversal; no central server.

**Earlier elements:** Hearsay-II and Linda provide shared asynchronous work state;
Maildir provides crash-safe file publication; Task Master provides agent task
files, status, dependencies and next-work selection; Beads provides dependencies,
ready-work selection and atomic claiming. Grades A, B and C.

**Combination rationale:** projects already storing agent tasks locally have a
direct reason to use filesystem publication primitives and dependency traversal
to coordinate without infrastructure.

**Strongest Perseus response:** Perseus chooses Markdown frontmatter and no
central server where other AI task tools use other file formats or a database.

**Implementation conflict:** `os.replace` prevents partial publication but does
not compare task state. The later advisory-lock repair re-reads under the lock,
yet lock acquisition failure is swallowed. A forced fail-open test made two
claimers return success. The disclosure's unconditional “two agents cannot
claim” and NFS language therefore exceed the tested guarantee.

**Status:** technically obvious. Frontmatter is a file format, while task state,
dependencies, claiming and filesystem coordination were established machinery.

## R1.1: recursive include with path and inode ancestor identity

**Published combination:** resolve nested documents depth-first; carry an
immutable active ancestor chain with path and device-inode identities; stop a
branch when either identity repeats.

**Earlier elements:** m4 and the C preprocessor provide recursive inclusion; graph
algorithms use an active ancestor stack; filesystem tools use device and inode to
recognize hard-link aliases. Grade A.

**Combination rationale:** recursive inclusion creates cycles, while path aliases
defeat string-only detection. Filesystem identity is the standard mechanism for
recognizing the same object under different names.

**Strongest Perseus response:** the public summary places both path strings and
filesystem identity in the active ancestor set.

**Status:** technically obvious. Recursive inclusion requires an active cycle
set, and filesystem identity is the standard response to path aliases. Adding
device and inode to that set produces the expected result.

## R1.2: independent recursion depth bound

The C preprocessor documents a configurable maximum include depth. Recursive
parsers commonly bound depth separately from cycle detection. Grade A.

**Status:** strong anticipation candidate for the dependent limitation, subject
to claim construction and the parent claim.

## R1.3: resolver output remains literal

Raw/literal document blocks prevent re-entry into a parser. GNU m4's command
execution behavior supplies an older example where command output is not
rescanned as macro input. Grade A.

**Status:** strong anticipation candidate for the non-reentry limitation, subject
to the parent claim.

## R1.4: static typed dependency graph

Make, Ninja and Bazel construct dependency graphs before executing actions.
Registry metadata supplies node type and safety labels. Grades A and D.

**Status:** technically obvious. A parser exposes dependencies, and a typed edge
record is an ordinary representation of them.

## U1.1: one registry and adapter over six source classes

**Published combination:** one registry declares resolver, source class and call
signature; a registry-derived grammar parses the document; one adapter dispatches
filesystem, recursive, command, memory, sub-agent and external-tool sources.

**Earlier elements:** Docutils provides a registry-backed directive grammar; Org
Babel provides one interface over heterogeneous back ends; Continue provides one
model-context provider interface; MCP groups resources, prompts and tools. Grades
A and C.

**Combination rationale:** a common interface and registry remove parser branches
and make new providers extensible. That is the ordinary purpose of both patterns.

**Strongest Perseus response:** the public summary enumerates six functional
classes under the same registry, grammar and call-signature adapter.

**Status:** technically obvious. The number of source classes adds no technical
interaction.

## U1.2: parser vocabulary derived from registry

Docutils exposes a directive registry from which directive lookup occurs. Plugin
registries conventionally define the recognized extension vocabulary. Grade A.

**Strongest Perseus response:** the parser-recognized names are generated from
the same registry.

**Status:** technically obvious. Deriving accepted names from the registry is the
ordinary way to prevent parser and registry drift.

## U1.3: local semantic-memory source with byte-reproducible output

SQLite FTS5 and BM25 provide local, offline ranked retrieval. Fixed inputs can
produce repeatable output when ordering, versions and external state are fixed.
Grade A.

**Strongest Perseus response:** byte identity may depend on explicit tie-breaking,
index state, tokenizer/version and serialization rules. The public summary does
not identify those constraints.

**Status:** old retrieval mechanism with a result-oriented determinism
limitation. Runtime reproducibility testing remains outstanding.

## Restatements and exhibits

The 27 June “resolution outside the model loop” document restates D1.1. Exhibit
E4's one-round-trip count is a technical-effect argument, not an additional
proposed claim. Its round-trip comparison is structurally derived from the chosen
one-call versus serial-agent baselines. It is not a live-model latency result.

## Current conclusion

None of the fifteen public combinations is technically new. Each joins familiar
parts for their established functions, under the exact engineering pressure
that normally causes a competent developer to join them. None states an
unexpected interaction or result. Perseus could not have pioneered these
mechanisms or their routine combinations.

Perseus's public “closest prior art” work remains inadequate because it omits
these predecessor classes and supplies no element chart of its own. That is the
publishable finding from the public record.
