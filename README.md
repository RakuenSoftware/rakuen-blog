# Rakuen Software — blog

Articles and the evidence behind them, in one repository.

Blog content used to live in two places: published posts in
`rakuensoftware-web`, and drafts plus their measurement artifacts in `aimee`.
The evidence for a claim sat in a different repository from the claim. This
repository fixes that — each article owns its proof.

## Layout

One folder per article, named by slug. Everything that article depends on lives
under it:

```
articles/<slug>/
  article/      the post itself
  evidence/     validation writeups and decision records the post cites
  benchmarks/   raw result artifacts and fixtures the writeups were computed from
```

An article with no local evidence (opinion, announcement, one built entirely on
external sources) has only `article/`. Do not create empty folders to fill the
shape.

## The rule this repository exists to enforce

A figure in a post must be traceable to an artifact in the same article folder,
or to a named external source in the post itself. No orphan numbers.

This is not bureaucracy. It came out of the retrieval measurement campaign,
where six substantive claims turned out to be wrong and every one of them
failed silently — a plausible number, no error. Provenance is the only thing
that catches that class of bug. A number without it is not evidence.

## Articles

| article | published | evidence |
| --- | --- | --- |
| [hello-rakuen-software](articles/hello-rakuen-software/) | yes | none |
| [smoothgui-0-9-site-primitives](articles/smoothgui-0-9-site-primitives/) | yes | none |
| [token-compression-tools-cost-more-than-they-save](articles/token-compression-tools-cost-more-than-they-save/) | yes | external sources, cited inline |
| [stacking-isnt-composing](articles/stacking-isnt-composing/) | yes | source audit, reporting record |
| [we-measured-our-reranker-and-deleted-it](articles/we-measured-our-reranker-and-deleted-it/) | yes | 9 documents, 5 artifact sets |
| [local-llm-fact-extraction-head-to-head](articles/local-llm-fact-extraction-head-to-head/) | yes | 32 runs, figure map, full results tree |
| [speculative-decoding-was-free](articles/speculative-decoding-was-free/) | yes | figure map, shared results tree |
| [eight-ways-a-run-scores-fine-and-is-broken](articles/eight-ways-a-run-scores-fine-and-is-broken/) | ready | figure map, shared results tree |
| [how-small-can-a-fact-extractor-be](articles/how-small-can-a-fact-extractor-be/) | ready | figure map, shared results tree |
| [my-benchmark-lied-to-me](articles/my-benchmark-lied-to-me/) | ready | figure map, shared results tree |
| [one-sentence-turned-the-reasoning-off](articles/one-sentence-turned-the-reasoning-off/) | ready | figure map, shared results tree |
| [repeatable-is-not-identical](articles/repeatable-is-not-identical/) | ready | figure map, shared results tree |
| [the-benchmark-audited-production](articles/the-benchmark-audited-production/) | ready | figure map, shared results tree |
| [the-corpus-is-the-experiment](articles/the-corpus-is-the-experiment/) | ready | figure map, shared results tree |
| [the-parallelism-limit-was-never-vram](articles/the-parallelism-limit-was-never-vram/) | ready | figure map, shared results tree |
| [which-quant-beats-how-many-bits](articles/which-quant-beats-how-many-bits/) | ready | figure map, shared results tree |
| [synthesis-model-selection](articles/synthesis-model-selection/) | ready | figure map; two paired GPU runs, CPU selection open |

`ready` means publication-ready and gated, but not yet pushed to the live site.

## Publishing

The live site (`rakuensoftware-web`) still builds from its own
`src/content/blog/`. The published posts here are archived copies; the site has
not been repointed. Changing that is a separate decision — see
[MIGRATION.md](MIGRATION.md) for what was moved and what was left alone.
