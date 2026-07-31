# Migration record — 2026-07-31

What was brought into this repository, from where, and at which commit.

## Sources

| source repo | commit | what came from it |
| --- | --- | --- |
| `aimee` (branch `blog/retrieval-writeup`) | `d672f7b3d` | the reranker/embedder draft, its validation documents, `embedder-gate` and `reranker-2026-07-29` artifacts |
| `aimee` (`origin/testing`) | `b55483f8a` | `gemma4-unified` results and the `ab-v1` fixtures |
| `aimee` (session branch `25fb29ea`) | `d5899b408` | `rank-gate-2026-07-30` artifacts |
| `aimee` (commit) | `c92e80b1c` | the nomic cutover decision record, in its closed-out state |
| `rakuensoftware-web` | `b84c891bd` | the three published posts |

## What was left alone, deliberately

**The live site.** `rakuensoftware-web/src/content/blog/` is untouched and still
builds the site via `import.meta.glob('../content/blog/*.md')`. The three posts
here are archive copies. Repointing the site is a separate decision.

## What still has to happen in `aimee`

The evidence was moved, not copied, so `aimee` has to give it up and its
documents have to stop pointing at paths that no longer exist. That change is
staged on a branch in `aimee` and is not merged:

- delete `benchmarks/results/{embedder-gate,reranker-2026-07-29,rank-gate-2026-07-30,gemma4-unified}`
- delete `benchmarks/fixtures/gemma4-unified`
- delete `docs/blog/`
- rewrite the relative artifact links in `docs/validation/retrieval-stack-report-2026-07-30.md`,
  `docs/validation/embedder-gate-locomo.md`, `docs/validation/embedder-gate-scifact.md`
  and `docs/proposals/pending/nomic-cutover-and-reranker-removal.md` to point here

**Understand the trade before merging that.** Those four documents are `aimee`'s
own validation record. After the move they cite an external repository, so
`aimee` alone no longer reproduces its retrieval decisions. That was the
instruction, and it is the cost of a single home for evidence. The alternative —
copying rather than moving — was considered and rejected on the grounds that two
copies drift.

The validation documents themselves stay in `aimee`. Only the artifacts they
compute from move here, plus the copies under `articles/*/evidence/`.

## Known duplicate

`benchmarks/results/rank-gate-2026-07-30/` was copied here but not deleted from
`aimee`: it lives on session branch `25fb29ea`, which the removal branch cannot
reach. Low stakes — that branch is unmerged, and if it never merges the duplicate
resolves itself. The one thing to watch is the reverse: if `25fb29ea` merges to
`testing` after the removal branch does, it reintroduces artifacts the migration
took out. Check for that path before merging either.
