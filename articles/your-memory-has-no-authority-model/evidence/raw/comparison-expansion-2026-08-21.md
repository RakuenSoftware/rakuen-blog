# Comparison expansion collection record

Collection time: 2026-08-21 UTC.

Collection method: read-only shallow clones from each public GitHub origin,
using `git clone --depth 1 --filter=blob:none`, followed by `git rev-parse HEAD`
and `git show -s --format=%cI HEAD`. Source searches used `rg`; cited files were
read from the resulting committed trees. No repository under review was
modified and no runtime benchmark was run.

| repository | collected head | commit time |
| --- | --- | --- |
| `vectorize-io/hindsight` | `3de41af867582c810309d6ea4c1b1de9d0ed9b7e` | `2026-08-21T13:02:46+02:00` |
| `MemTensor/MemOS` | `be68e2fb5370866bd5e2b188bb3d22bd13b49e09` | `2026-08-20T22:14:58+08:00` |
| `supermemoryai/supermemory` | `34876664810a43a55954a0a83571662a3bd333b8` | `2026-08-20T22:58:39Z` |
| `Uranid/mnem` | `2a8a36985dbcf107378a76daeeef7154691220e7` | `2026-06-01T14:06:46+05:30` |
| `Archolith/menhir` | `4e4f39ed388a1c689740a7d48daade9fbc79c000` | `2026-08-20T13:49:46-05:00` |
| `neo4j-labs/agent-memory` | `5b4e00af88342707d011bb9d4f2b34503f43a8c3` | `2026-08-19T16:48:22+02:00` |
| `MemoriLabs/Memori` | `538b61f245295aa1a43df8033879f8293627f74d` | `2026-07-28T12:08:56-07:00` |

Expected outcome: test whether the added systems change the comparison cells or
falsify the article's broad claims about code-plus-memory uniqueness and absent
authority models.

Actual outcome: mnem and Menhir falsified the broad code-plus-memory uniqueness
claim. Menhir also falsified the broad absence-of-authority claim. Hindsight,
MemOS and Neo4j Agent Memory added material source, history or valid-time credit.
Supermemory's documentation made directly relevant authority and temporal
claims, but the repository did not contain the self-hosted server engine needed
to verify them, so it was excluded from the scored denominator.

Reproducibility limit: these are static implementation reads at the heads above.
They do not establish runtime correctness, hosted-product behavior or later
repository state.
