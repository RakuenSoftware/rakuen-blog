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

The live site (`rakuensoftware-web`) builds from its own `src/content/blog/`.
The site has not been repointed at this repository and that remains a separate
decision — see [MIGRATION.md](MIGRATION.md) for what was moved and what was left
alone.

`tools/publish.py` is the bridge across that gap:

```sh
python3 tools/publish.py                     # report what is ready, change nothing
python3 tools/publish.py --site ../rakuensoftware-web one-call-one-turn
```

Name the articles to export. Writing with no slug named would export every ready
article at once, which is rarely what shipping one piece means, so that form
refuses and asks for `--all` if it is really meant.

It exports an article only if the article's README declares it
`Publication-ready` and `Not yet published`, `tools/voice_gate.py` passes it,
`evidence/figures.md` exists, and its frontmatter is complete. Every blocker is
reported in one run rather than one per invocation.

**It never commits, pushes, merges or deploys.** Writing into a site checkout
leaves modified files there for a human to review, branch and merge. Ingestion is
a manual merge on purpose: passing every gate in this repository means no person
has read the piece yet.

### Exporting is the first of four steps

Exporting a file is not publishing, and the gap has been mistaken for the finish
line more than once. The whole path to a live URL:

1. `python3 tools/publish.py --site ../rakuensoftware-web <slug>`
2. in the site checkout, branch off `main`, commit the file, open a pull request
3. merge it
4. **deploy**, which is a separate manual step with no CI behind it:

```sh
ssh root@192.168.1.253 'pct exec 107 -- /opt/rakuen-web/scripts/deploy.sh'
```

Step 4 is the one that moves the website. Until it runs, `main` has the article
and rakuensoftware.com does not. The script fast-forwards the checkout, rebuilds,
swaps `dist/` atomically, restarts the server and rolls back if the new bundle
fails to serve. It prints `Live: <bundle> (commit <sha>)`, and that sha is the
only confirmation worth having.

Check the result rather than trusting the merge:

```sh
curl -o /dev/null -w '%{http_code}\n' https://rakuensoftware.com/blog/<slug>
```

The site is a single-page app, so the page title is not in the HTML and grepping
the response for it proves nothing. To confirm the text really shipped, grep the
built bundle on the host instead.

Do not branch the site checkout from whatever it happens to have checked out. It
is often left on a merged feature branch, and committing there puts the article
on a stale branch beside work that has already landed.

The site filename comes from the article's `slug:` frontmatter field when it has
one, and from the article's directory name otherwise. That is how an article
whose title changed keeps its published URL. Changing a live URL is a decision,
so the script never infers one.
