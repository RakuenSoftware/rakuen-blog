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
| [three-zeros-and-a-wrong-answer](articles/three-zeros-and-a-wrong-answer/) | draft | 81 cells committed and checkable; three figures do not reproduce |
| [one-call-one-turn](articles/one-call-one-turn/) | yes | figure map, nine cells, `recompute_table.py` |
| [we-forced-it-to-think-and-the-score-fell](articles/we-forced-it-to-think-and-the-score-fell/) | ready | figure map, forced-reasoning pair, five rerunnable scripts |

`ready` means publication-ready and gated, but not yet pushed to the live site.
`draft` means the article exists and its provenance gaps are written down, but it
is not a publication candidate and the voice gate does not check it.
No article currently sits at `investigation`, which meant the work existed and the
prose deliberately did not, because the finding was not stable enough to write
around. The last one held that status for two days and left it by running the
experiment its own README said would settle the question.

## Publishing

This repository is the only source of article text. `scripts/sync-articles.mjs`
in `rakuensoftware-web` clones **this repository's `main`** at build time and
writes the articles it publishes into a generated, gitignored
`src/content/posts/`. The site's own `src/content/blog/` is dead and nothing
reads it.

**What ships is named in `PUBLISHED` in `scripts/sync-articles.mjs`.** Landing an
article on `main` here does not publish it, and that is the point: adding the
slug to that list is a one-line diff in the site repository, and merging it is
the gate.

That gate is new because the previous one did not exist. The sync used to
publish any article whose markdown carried frontmatter, every article here
carries frontmatter because `tools/voice_gate.py` requires it, and on 2026-08-12
a deploy put eleven never-published articles on the live site at once, including
a draft whose own figure map records three figures that do not reproduce.

`tools/publish.py` predates that discovery and writes into the dead
`src/content/blog/`. Its checks are real and reach nothing, so treat its output
as a readiness report and not as publication:

```sh
python3 tools/publish.py                     # report what is ready, change nothing
```

It reports an article as exportable only if its README declares it
`Publication-ready` and `Not yet published`, `tools/voice_gate.py` passes it,
`evidence/figures.md` exists, and its frontmatter is complete. Every blocker is
reported in one run rather than one per invocation.

### Publishing is three steps and none of them is publish.py

1. merge the article to `main` here
2. add the slug to `PUBLISHED` in `rakuensoftware-web/scripts/sync-articles.mjs`
   and merge that
3. **deploy**, which is a separate manual step with no CI behind it:

```sh
ssh root@192.168.1.253 'pct exec 107 -- /opt/rakuen-web/scripts/deploy.sh'
```

Step 3 is the one that moves the website, and it pulls whatever `main` says at
the moment it runs. The script fast-forwards the site checkout, rebuilds, swaps
`dist/` atomically, restarts the server and rolls back if the new bundle fails to
serve. It prints `Live: <bundle> (commit <sha>)`, and that sha names the site's
code rather than the article revision, so it confirms a deploy happened and not
which text went out.

Removing a slug from `PUBLISHED` retires a live URL, and the next build refuses
until it is told that was deliberate:

```sh
ssh root@192.168.1.253 'pct exec 107 -- env ALLOW_UNPUBLISH=1 /opt/rakuen-web/scripts/deploy.sh'
```

**Never confirm a publish with `curl`.** The site is a single-page app and serves
`index.html` for every path, so a retired article and a live one both return 200.
Grep the built bundle on the host, which is the only check that distinguishes
them:

```sh
ssh root@192.168.1.253 'pct exec 107 -- grep -c "<a phrase from the article>" /opt/rakuen-web/dist/assets/<bundle>.js'
```

The published filename, and therefore the URL, is the article's directory name
here. Renaming a directory changes a live URL and breaks every inbound link, so
an article whose title changes after publication keeps its old directory.
