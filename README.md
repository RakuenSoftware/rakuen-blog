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

This table is written for a reader. What is actually live is
[`articles/PUBLISHED`](articles/PUBLISHED), which the site reads directly — a
`yes` below is a description of that file, not the thing that puts a page on the
website.

| article | published | evidence |
| --- | --- | --- |
| [hello-rakuen-software](articles/hello-rakuen-software/) | yes | none |
| [smoothgui-0-9-site-primitives](articles/smoothgui-0-9-site-primitives/) | yes | none |
| [token-compression-tools-cost-more-than-they-save](articles/token-compression-tools-cost-more-than-they-save/) | yes | external sources, cited inline |
| [stacking-isnt-composing](articles/stacking-isnt-composing/) | yes | source audit, reporting record |
| [we-measured-our-reranker-and-deleted-it](articles/we-measured-our-reranker-and-deleted-it/) | yes | 9 documents, 5 artifact sets |
| [local-llm-fact-extraction-head-to-head](articles/local-llm-fact-extraction-head-to-head/) | yes | 32 runs, figure map, full results tree |
| [speculative-decoding-was-free](articles/speculative-decoding-was-free/) | yes | figure map, shared results tree |
| [the-harness-measured-itself](articles/the-harness-measured-itself/) | ready | figure map, shared results tree |
| [one-sentence-turned-the-reasoning-off](articles/one-sentence-turned-the-reasoning-off/) | ready | figure map, shared results tree |
| [repeatable-is-not-identical](articles/repeatable-is-not-identical/) | ready | figure map, shared results tree |
| [the-benchmark-audited-production](articles/the-benchmark-audited-production/) | ready | figure map, shared results tree |
| [the-corpus-is-the-experiment](articles/the-corpus-is-the-experiment/) | ready | figure map, shared results tree |
| [the-parallelism-limit-was-never-vram](articles/the-parallelism-limit-was-never-vram/) | ready | figure map, shared results tree |
| [synthesis-model-selection](articles/synthesis-model-selection/) | yes | nine-model paired GPU matrix, Qwen3.8 follow-up complete |
| [which-quant-beats-how-many-bits](articles/which-quant-beats-how-many-bits/) | yes | 37 runs on both tasks, paired intervals on each; first of the quantization series |
| [three-zeros-and-a-wrong-answer](articles/three-zeros-and-a-wrong-answer/) | retired | headline published as `one-call-one-turn`; surviving finding moved to `the-harness-measured-itself` |
| [one-call-one-turn](articles/one-call-one-turn/) | yes | figure map, nine cells, `recompute_table.py` |
| [the-model-decides-when-to-think](articles/the-model-decides-when-to-think/) | investigation | four rerunnable scripts; no article written yet |
| [kv-cache-precision](articles/kv-cache-precision/) | investigation | four cache configurations on one model recorded; no article written yet |
| [your-memory-has-no-authority-model](articles/your-memory-has-no-authority-model/) | draft | source map, eight-repository source audit; right of reply outstanding |
| [ornith-against-its-base](articles/ornith-against-its-base/) | draft | registered plan; four runs outstanding, no accuracy result yet |

`ready` means publication-ready and gated, but not yet pushed to the live site.
`draft` means the article exists and its provenance gaps are written down, but it
is not a publication candidate and the voice gate does not check it.
`held` means the article passes every gate and is still not a candidate, because
the measurement behind it is too thin to publish as guidance. A gate can check
provenance; it cannot decide that enough has been measured.
`retired` means the article is superseded and will not ship. Its folder stays when
another article cites its artifacts.
`investigation` means the work exists and the prose deliberately does not, because
the finding is not stable enough to write around.

## Publishing

[`articles/PUBLISHED`](articles/PUBLISHED) is the live blog. A line in that file
is an `articles/<slug>` directory, and it is also the URL:
`rakuensoftware.com/blog/<slug>`.

**Publishing is adding one line to that file and merging it to `main`.** The site
polls this branch every three minutes, pulls the named articles, rebuilds and
swaps itself over. Nothing has to be deployed and nothing has to be committed to
the site repository. Editing an article that is already listed republishes it the
same way, on the same timer.

That list used to live in the site repository, so shipping an article meant a
commit here and a second commit there, and the two drifted. It moved here on
2026-08-20 to put the decision next to the article it is about. The gate itself
did not change: a person still writes the line, and everything absent is held on
purpose. The header of the file records why it is a list and not a rule.

Removing a line retires a live URL. The site refuses to do that unless its build
is run with `ALLOW_UNPUBLISH=1`, so it cannot happen by a stray edit. Renaming a
line changes a live URL and breaks every inbound link to it.

The slug is the directory name. The `slug:` frontmatter field is read by
`tools/publish.py` only and does not affect the live URL.

### Before you add the line

`tools/publish.py` reports what is ready and changes nothing:

```sh
python3 tools/publish.py          # report what is ready and what blocks the rest
```

An article is ready only if its README declares it `Publication-ready` and `Not
yet published`, `tools/voice_gate.py` passes it, `evidence/figures.md` exists,
and its frontmatter is complete. Every blocker is reported in one run rather than
one per invocation.

Ready is not published. Passing every gate here means no person has read the
piece yet, which is exactly what the line in `PUBLISHED` asserts and no check
can.

Its `--site` export mode wrote into the site's old `src/content/blog/`, which the
site no longer reads. Use the report; ignore the export.

### Confirming it went live

Give the timer a few minutes, then check the result rather than trusting the
merge:

```sh
curl -o /dev/null -w '%{http_code}\n' https://rakuensoftware.com/blog/<slug>
```

The site is a single-page app, so the page title is not in the HTML and grepping
the response for it proves nothing. To confirm the text really shipped, grep the
built bundle on the host instead.

If the slug never appears, the sync refused the build. Its guards fail loudly and
leave the previous site serving, so the reason is in the host's journal:

```sh
ssh root@192.168.1.253 'pct exec 107 -- journalctl -u rakuen-autopublish -n 50'
```
