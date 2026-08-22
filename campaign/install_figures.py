#!/usr/bin/env python3
"""Replace the article's sg-figure blocks with freshly generated ones.

The figures are generated from evidence but were pasted into the draft by hand,
so regenerating them proved nothing unless someone also copied the result back.
This does the copy, matching on the figure's radio `name` so each block lands
where it already is and the prose around it is untouched.

Refuses to run if a generated figure has no counterpart in the article, or if
the article has a figure the generator does not produce: either means the two
have diverged in structure, and silently leaving one stale is the failure this
is meant to prevent.

    install_figures.py <figures.html> <article.md>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FIG = re.compile(r'<figure class="sg-figure">.*?</figure>', re.S)
NAME = re.compile(r'name="(fig-[a-z0-9-]+)"')


def by_name(text: str) -> dict[str, str]:
    out = {}
    for m in FIG.finditer(text):
        n = NAME.search(m.group(0))
        if n:
            out[n.group(1)] = m.group(0)
    return out


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    figures = Path(sys.argv[1]).read_text()
    article_path = Path(sys.argv[2])
    article = article_path.read_text()

    fresh = by_name(figures)
    current = by_name(article)

    missing = sorted(set(fresh) - set(current))
    extra = sorted(set(current) - set(fresh))
    if missing or extra:
        for n in missing:
            print(f"generated but not in article: {n}", file=sys.stderr)
        for n in extra:
            print(f"in article but not generated: {n}", file=sys.stderr)
        return 1

    changed = []
    for name, block in fresh.items():
        if current[name] != block:
            article = article.replace(current[name], block, 1)
            changed.append(name)

    article_path.write_text(article)
    if changed:
        print("updated:", *changed, sep="\n  ")
    else:
        print("all figures already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
