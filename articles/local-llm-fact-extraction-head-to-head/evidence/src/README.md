# Why two C files live in an evidence folder

`harness/harness/prompt.py` does not hard-code the relation ontology. It parses
it out of aimee's own C sources, so that the benchmark scores the system that is
actually running rather than a copy of it that can drift:

- `src/rel_types.c` — `SEED_ONTOLOGY` (the relations), `SEED_ALIASES` (the
  alias fold production applies before a triple reaches the write gate), and the
  symmetric/inverse pairs.
- `src/kb/kb_memory_facts.c` — `MF_SYSTEM_PROMPT_TMPL`, the extraction prompt.

Those files live in the aimee repository, which is not this one. Without them
nothing in the results tree can be rescored: `prompt.py` raises before the
scorer runs. Every score in `evidence/figures.md` was therefore traceable to an
artifact but not *recomputable*, which is a weaker guarantee than this
repository claims to enforce. Vendoring the two files closes that.

## The pin

Both files are copied verbatim from aimee at commit
`0a7c8cc3a3f523cff79e0fa8cc32ddf61ca15473` (2026-08-02 14:39 UTC, "ontology:
seed the seven relations the domain kept inventing (defect 35)").

The commit was not chosen by date. It was chosen by rescoring the banked runs
under every version of `rel_types.c` since the ontology landed and keeping the
one that reproduces what was banked:

| candidate | date | article's 20 runs | all 76 rescorable runs |
|---|---|---|---|
| `fb836f14db` | 2026-08-02 07:26 | 20/20 exact | 70 exact, 6 differ |
| **`0a7c8cc3a3`** | **2026-08-02 14:39** | **20/20 exact** | **71 exact, 5 differ** |
| `29035372ee` | 2026-08-02, on main | 0/20 | 12 exact, 64 differ |

"The article's 20 runs" are the twelve paired 10k scores and the six acceptance
runs behind `speculative-decoding-was-free`, plus the two Qwen3.6 runs. All
twenty reproduce tp, fp and fn exactly — not just F1 to four places — under both
Aug-2 candidates, so the article's figures do not depend on which of the two is
picked. `0a7c8cc3a3` is pinned because it is the later of the two and
reproduces one more run overall.

`29035372ee` is the version that survives on aimee's `main` today, and it
reproduces almost nothing. That is why re-deriving the ontology from a current
checkout silently produces wrong numbers, and why this folder exists.

## Known limits

Five of the 76 rescorable runs do not reproduce under any candidate, and four
more cannot be rescored at all (their row count matches no gold set). Those are
older arms scored against earlier corpus and ontology states; the results tree
was not scored under a single scorer. None of them is cited by any published
article. If one is ever cited, it has to be rescored first.

These files are aimee source, included here as evidence, and are not built or
executed by anything in this repository.
