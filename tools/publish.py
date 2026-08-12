#!/usr/bin/env python3
"""Export publication-ready articles to the live site's content directory.

The live site (`rakuensoftware-web`) builds from `src/content/blog/*.md`. This
repository is where articles are written and gated. This script is the bridge,
and it deliberately stops short of publishing.

    python3 tools/publish.py                  # report what is ready, change nothing
    python3 tools/publish.py --out DIR        # write the exported files to DIR
    python3 tools/publish.py --site PATH      # write into a site checkout
    python3 tools/publish.py --site PATH SLUG # write one named article only

Naming one or more slugs exports only those. Writing with no slug named exports
every ready article at once, which is rarely what someone shipping a single piece
means, so that form asks for confirmation before it writes.

Nothing here commits, pushes, merges or deploys. Writing into a site checkout
leaves modified files in that working tree for a human to review, branch and
merge. Ingestion is a manual merge, by design: an article that passes every gate
in this repository has still not been read by anyone at the point the gates pass.

## What gates an article

An article is exported only if all of these hold. Each is a separate failure and
all are reported, so one run tells you everything blocking a release.

1. Its README says `Publication-ready` and `Not yet published`. That is the
   author's declaration of intent and nothing else substitutes for it.
2. `tools/voice_gate.py` passes it.
3. `evidence/figures.md` exists. The repository's rule is that a figure traces to
   an artifact or a named source, and the figure map is where that is recorded.
4. Its frontmatter carries every required field.

## URLs

The site filename comes from the article's `slug:` frontmatter field when it has
one, and from the article's directory name otherwise. That is how an article
whose title changed keeps the URL it was published under: set `slug:` to the old
name. Changing a live URL is a decision, so this script never infers one.
"""

from __future__ import annotations

import argparse
import re
import shutil
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="directory to write exported files to")
    parser.add_argument(
        "--site", type=Path, help="site checkout; writes to its src/content/blog"
    )
    parser.add_argument(
        "slugs", nargs="*", help="export only these articles; default is all ready ones"
    )
    parser.add_argument(
        "--all", action="store_true", help="confirm exporting every ready article"
    )
    args = parser.parse_args()

    destination = args.out
    if args.site:
        destination = args.site / "src" / "content" / "blog"
        if not destination.is_dir():
            print(f"not a site checkout: {destination} does not exist", file=sys.stderr)
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

    if not destination:
        print(f"\n{len(exportable)} ready, {len(declared) - len(exportable)} blocked.")
        print("Nothing written. Pass --out DIR or --site PATH to export.")
        return 0

    if not args.slugs and len(exportable) > 1 and not args.all:
        print(
            f"\nRefusing to write {len(exportable)} articles at once without being asked.\n"
            "Shipping one piece is the common case and exporting every ready article\n"
            "is rarely what that means. Name the slugs, or pass --all deliberately:\n"
            f"  python3 tools/publish.py --site PATH {exportable[0][1][:-3]}",
            file=sys.stderr,
        )
        return 2

    destination.mkdir(parents=True, exist_ok=True)
    for source, name in exportable:
        target = destination / name
        verb = "overwrite" if target.exists() else "create"
        shutil.copyfile(source, target)
        print(f"{verb:9s} {target}")

    print(f"\n{len(exportable)} file(s) written to {destination}.")
    print("Nothing was committed, pushed or merged.")
    print("Review the diff in that checkout, branch it, and merge it yourself.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
