# Graphiti response and Graphify follow-up

Collection time: 2026-08-21 UTC.

## Classification correction

Graphiti's maintainers replied that Graphiti is a framework for building
temporal knowledge graphs, not an agent-memory service. They also clarified that
most of the memory features in the reporting questions are available in Zep,
not in Graphiti. The article now:

- labels the scored row `Graphiti framework`, not `Graphiti (Zep)`;
- describes it as adjacent temporal-graph infrastructure;
- limits every scored cell to the public Graphiti repository; and
- makes no claim that the row represents Zep's hosted memory features.

The maintainers suggested Graphify for the code-graph part of the comparison.

## Graphify audit

Repository: `Graphify-Labs/graphify`.

Pinned tree: branch `v8` at
`b2cd36267456c166788c95be6e68574064a92a42`, committed 2026-08-20.

Method: cloned the public repository, recorded `HEAD`, and traced code/document
ingestion, graph construction, source linkage, saved Q&A outcomes, reflection,
correction selection and the learning overlay. The project was not installed or
run.

Result:

- AST code, documents and media map into one queryable graph;
- saved Q&A outcomes are source-linked Markdown records that enter the graph on
  a later update;
- retrieved nodes carry source file and location;
- corrections remain in the raw records while the latest correction for a
  repeated question wins in the derived lessons;
- learning status is a provenance-bearing sidecar merged at read time, not a
  mutation of structural graph truth; and
- no semantic endpoint-kind contract, user-versus-model authority rank or
  real-world valid-time interval was found.

Disposition: Graphify is included as a fourth inspectable code-plus-memory
implementation. Its work-memory provenance is credited without treating it as
assertion authority.
