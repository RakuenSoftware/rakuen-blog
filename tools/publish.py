#!/usr/bin/env python3
"""Report which articles are ready to publish, and what the site is serving.

    python3 tools/publish.py                 # what is ready here
    python3 tools/publish.py --site PATH     # that, against what the site publishes

This writes nothing, anywhere. It used to copy files into a site checkout's
`src/content/blog/`, which was already dead when it was written: the site builds
articles by cloning THIS repository in `scripts/sync-articles.mjs` and writing
them to a generated `src/content/posts/`. Nothing has read `src/content/blog/`
for some time, so every export this script performed went into a directory the
build ignores. The checks below were sound and their output was never connected
to anything, which is the worst arrangement of the two.

Publishing is: merge the article here, add its slug to `PUBLISHED` in
`rakuensoftware-web/scripts/sync-articles.mjs`, merge that, then deploy. A
one-line diff in the site repository is the gate, and a human merging it is the
point — an article that passes every check here has still not been read by
anyone at the moment the checks pass.

## What gates an article

Each is a separate failure and all are reported, so one run tells you everything
blocking a release.

1. Its README says `Publication-ready` and `Not yet published`. That is the
   author's declaration of intent and nothing else substitutes for it.
2. `tools/voice_gate.py` passes it.
3. `evidence/figures.md` exists. The repository's rule is that a figure traces to
   an artifact or a named source, and the figure map is where that is recorded.
4. Its frontmatter carries every required field.

## Against a site checkout

`--site PATH` reads `PUBLISHED` out of that checkout's `sync-articles.mjs` and
reports the difference in both directions. Both directions have bitten:

- ready here, absent from PUBLISHED: finished work nobody noticed was waiting
- in PUBLISHED, not ready here: a live URL whose article no longer passes its
  own gates, or was renamed, which the site build refuses to serve

It reads that file and does not write it. A Python script editing a JavaScript
array in another repository is a merge conflict waiting to happen, and the merge
of that one line is the gate this repository is deliberately not automating.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / "articles"
REQUIRED_FRONTMATTER = ("title", "date", "author", "tags", "excerpt")


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        return "", text
    return parts[1], parts[2]


def declared_ready(readme: Path) -> bool:
    if not readme.is_file():
        return False
    text = readme.read_text(encoding="utf-8")
    return "Publication-ready" in text and "Not yet published" in text


def site_name(frontmatter: str, directory: str) -> str:
    match = re.search(r"^slug:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
    return (match.group(1) if match else directory) + ".md"


def voice_gate_failures(slug: str) -> list[str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "voice_gate.py"), slug],
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return []
    return [
        line.strip().lstrip("- ")
        for line in proc.stdout.splitlines()
        if line.startswith("  - ")
    ] or ["voice gate failed"]


def check(directory: Path) -> tuple[str | None, list[str]]:
    """Return (site filename, blockers). A ready article has no blockers."""
    slug = directory.name
    article = directory / "article" / f"{slug}.md"
    blockers: list[str] = []

    if not article.is_file():
        return None, [f"no article at {article.relative_to(ROOT)}"]

    frontmatter, _ = split_frontmatter(article.read_text(encoding="utf-8"))
    if not frontmatter:
        blockers.append("no YAML frontmatter")
    for field in REQUIRED_FRONTMATTER:
        if not re.search(rf"^{field}:", frontmatter, re.MULTILINE):
            blockers.append(f"frontmatter missing {field}")

    if not (directory / "evidence" / "figures.md").is_file():
        blockers.append("no evidence/figures.md")

    blockers.extend(voice_gate_failures(slug))
    return site_name(frontmatter, slug), blockers


def published_slugs(site: Path) -> list[str] | None:
    """The PUBLISHED list out of a site checkout's sync-articles.mjs.

    Parsed rather than executed, and deliberately narrow: the array literal, its
    quoted entries, nothing else. A looser regex over the whole file would also
    match the slug names in that file's own comments, which is how a reconciler
    reports a difference that is not there.
    """
    script = site / "scripts" / "sync-articles.mjs"
    if not script.is_file():
        print(f"not a site checkout: {script} does not exist", file=sys.stderr)
        return None
    text = script.read_text(encoding="utf-8")
    match = re.search(r"const PUBLISHED = \[(.*?)\];", text, re.S)
    if not match:
        print(f"no PUBLISHED array in {script}", file=sys.stderr)
        return None
    return re.findall(r"['\"]([^'\"]+)['\"]", match.group(1))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site", type=Path, help="site checkout to reconcile against; read only"
    )
    parser.add_argument(
        "slugs", nargs="*", help="report only these articles; default is all ready ones"
    )
    args = parser.parse_args()

    live: list[str] | None = None
    if args.site:
        live = published_slugs(args.site)
        if live is None:
            return 2

    candidates = sorted(d for d in ARTICLES.iterdir() if (d / "README.md").is_file())
    declared = [d for d in candidates if declared_ready(d / "README.md")]

    if args.slugs:
        known = {d.name for d in candidates}
        unknown = [s for s in args.slugs if s not in known]
        if unknown:
            print(f"no such article: {', '.join(unknown)}", file=sys.stderr)
            return 2
        not_ready = [s for s in args.slugs if s not in {d.name for d in declared}]
        if not_ready:
            print(
                f"not declared publication-ready: {', '.join(not_ready)}",
                file=sys.stderr,
            )
            return 2
        declared = [d for d in declared if d.name in set(args.slugs)]

    if not declared:
        print("no article declares itself publication-ready and unpublished.")
        return 0

    exportable: list[tuple[Path, str]] = []
    for directory in declared:
        name, blockers = check(directory)
        if blockers:
            print(f"BLOCKED {directory.name}")
            for blocker in blockers:
                print(f"   {blocker}")
        else:
            exportable.append((directory / "article" / f"{directory.name}.md", name))
            arrow = "" if name == f"{directory.name}.md" else f"  -> {name}"
            print(f"READY   {directory.name}{arrow}")

    print(f"\n{len(exportable)} ready, {len(declared) - len(exportable)} blocked.")

    if live is None:
        print("Pass --site PATH to compare this against what the site publishes.")
        return 0

    ready_slugs = {source.parent.parent.name for source, _ in exportable}
    # An article EXISTS if it has prose. It is a publication CANDIDATE if it also
    # has a README declaring intent, which is what `candidates` holds. Using the
    # latter here reported four live articles as missing, because a piece that
    # shipped long ago has no reason to still carry a readiness README.
    all_slugs = {
        d.name
        for d in ARTICLES.iterdir()
        if (d / "article" / f"{d.name}.md").is_file()
    }
    waiting = sorted(ready_slugs - set(live))
    # Ordered by PUBLISHED rather than sorted: a slug the site serves and this
    # repository cannot account for is worth seeing in the order it appears in
    # the file someone will edit.
    unaccounted = [s for s in live if s not in all_slugs]
    not_ready = [s for s in live if s in all_slugs and s not in ready_slugs]
    # Live AND still declaring itself unpublished. The first version of this
    # report had no bucket for it, so the state fell between two filters and
    # vanished — and one-call-one-turn was sitting in it, published on
    # 2026-08-12 with a README that still said "Not yet published".
    stale_readme = [s for s in live if s in ready_slugs]

    print(f"\nSite publishes {len(live)} article(s).")
    if waiting:
        print(f"\nReady here, not in PUBLISHED ({len(waiting)}):")
        for slug in waiting:
            print(f"  + {slug}")
        print("  Add these to PUBLISHED in scripts/sync-articles.mjs to publish them.")
    if unaccounted:
        print(f"\nIn PUBLISHED, no such article here ({len(unaccounted)}):")
        for slug in unaccounted:
            print(f"  ? {slug}")
        print("  The site build fails on these. A renamed directory changes a live URL.")
    if not_ready:
        print(f"\nLive, but not currently publication-ready here ({len(not_ready)}):")
        for slug in not_ready:
            print(f"  ! {slug}")
        print("  Expected for anything already published: its README says so.")
    if stale_readme:
        print(f"\nLive, but its README still says unpublished ({len(stale_readme)}):")
        for slug in stale_readme:
            print(f"  * {slug}")
        print("  Update the Status section. It is the declaration everything else reads.")
    if not (waiting or unaccounted or stale_readme):
        print("Nothing is waiting to be published.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
