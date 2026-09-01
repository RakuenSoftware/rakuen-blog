# CogniRepo prior-art chronology

Checked: 2026-09-01 UTC

## Finding

CogniRepo is a dated, public, technically relevant predecessor to Perseus's
published memory and context story. Its 12 March 2026 source snapshot already
implemented persistent local semantic memory, vector retrieval, episodic
logging and bounded pruning. It also described a local memory-and-retrieval
layer that selected repository knowledge for an LLM.

Perseus later inspected CogniRepo directly. Its competitive analysis is dated
18 June and first appears in the public Git history on 19 June. It classified
the overlap with Perseus Context Engine and Vault as high and direct. That
document establishes actual knowledge by 19 June. It does not establish that
Perseus knew of CogniRepo before its asserted May provisional filing.

## Public chronology

| Date | Artifact | What it establishes |
|---|---|---|
| 2026-03-12 13:06 UTC | [CogniRepo initial commit](https://github.com/ashlesh-t/cognirepo/commit/452516909b3692fbaf92c9c0af2395880fe1d915) | The public Git repository existed. GitHub's repository API records `created_at` as `2026-03-12T13:06:23Z`. |
| 2026-03-12 19:14 UTC | [Initial feature commit](https://github.com/ashlesh-t/cognirepo/commit/e7d9d0815a6b78d9c96852dadde58d7382dc11ff) | Public source for semantic memory, episodic memory, FAISS storage and retrieval, store/retrieve commands, document search and memory pruning. |
| 2026-03-28 | [PyPI 0.1.0 release](https://pypi.org/project/cognirepo/0.1.0/) | The first Python package distribution. This is later than the public Git source and should not be used as the project's first-publication date. |
| 2026-06-17 | [PyPI 1.1.3 release](https://pypi.org/project/cognirepo/1.1.3/) | A packaged release immediately before Perseus's competitive review. |
| 2026-06-18/19 | [Perseus competitive analysis](https://github.com/Perseus-Computing-LLC/perseus/blob/2e2f8e87179aa524e7f5c3f2fc7798996ad071d8/docs/competitive-analysis-phase1.md) | The file is dated 18 June and was committed publicly on 19 June. Perseus says it directly inspected CogniRepo, maps multiple high-overlap features and calls it the most serious context-engine threat. |
| 2026-06-27/28 | [Perseus issue 493](https://github.com/Perseus-Computing-LLC/perseus/issues/493) | The non-provisional conversion remained future work. The issue lists a professional novelty search as an external action and describes two receipts with the same application number three days apart. It does not document a June 27 refiling. |

## March 12 feature check

The initial feature commit contains working source for these mechanisms:

- `memory/semantic_memory.py` embeds text, computes importance, stores it and
  retrieves by a query embedding.
- `vector_db/local_vector_db.py` persists a FAISS index plus JSON metadata and
  returns nearest stored memories.
- `memory/episodic_memory.py` appends timestamped events to a durable JSON log.
- `tools/store_memory.py` and `tools/retrieve_memory.py` expose the write and
  recall paths.
- `cron/prune_memory.py` bounds stored memory by ranking importance and keeping
  the highest-scored records.
- The README describes the result as a local memory and retrieval layer that
  supplies relevant repository knowledge to an LLM.

The same commit's MCP server is a mock. The March 12 artifact therefore proves
the persistent-memory and retrieval core, plus the described agent-context
architecture. It should not be cited as proof of a working MCP server on that
date.

## Perseus's admitted overlap

The analysis dated 18 June records these CogniRepo comparisons:

- persistent memory versus Vault: high overlap;
- context retrieval versus `@memory` and `@read`: high overlap;
- code lookup versus `@file`: high overlap;
- cross-agent handoff: high overlap;
- memory decay and pruning: medium overlap;
- architectural-decision memory: medium overlap.

It concludes: "CogniRepo is the most serious competitive threat to Perseus in
the 'context engine' space" and says it overlaps significantly with both
Perseus context rendering and Vault persistent memory. This is first-party
evidence that Perseus recognized technical relevance. It is not an adjudication
of an unreleased patent claim.

The report also names `codebase-memory-mcp`, `memory-mesh`, `memtrace-public`,
`YourMemory` and `ContextForge`. Their inclusion establishes that Perseus
selected them for technical comparison. Each public artifact predating the
relevant priority date is a prior-art candidate requiring its own chronology
and element check. The competitor label alone does not establish anticipation.

## Patent-process boundary

The public record supports three separate propositions:

1. CogniRepo's relevant source was publicly available before the asserted May
   2026 provisional.
2. Perseus had documented knowledge of the overlap by 19 June.
3. Perseus was still preparing a future non-provisional conversion after that
   review.

It does not support the claim that Perseus refiled the application on 27 June.
Issue 493 describes the same application number on two receipts and treats the
non-provisional as future work.

USPTO [MPEP section 609](https://www.uspto.gov/web/offices/pac/mpep/s609.html)
says information disclosure statements are not permitted in provisional
applications because provisionals receive no substantive examination. In a
non-provisional, people involved in preparation or prosecution must disclose
information known to be material to patentability under 37 CFR 1.56. Materiality
depends on the unreleased claims and the information already of record. The
public record cannot establish whether CogniRepo was or will be disclosed.

## Publication disposition

Use CogniRepo as hard evidence against the public claim that the memory and
context field lacked close predecessors. State its March 12 mechanisms and
Perseus's June 18/19 recognition separately. Avoid saying one public artifact
anticipates an unavailable patent claim, that Perseus knew of CogniRepo before
May, or that June 27 was a refiling without a filing record.
