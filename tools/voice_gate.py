#!/usr/bin/env python3
"""Conservative mechanical checks for unpublished Rakuen articles."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FRONTMATTER = ("title", "date", "author", "tags", "excerpt")
FORBIDDEN_WORDS = (
    "very",
    "extremely",
    "incredibly",
    "obviously",
    "clearly",
    "simply",
)
RULE_VERBS = (
    "print ",
    "read ",
    "record ",
    "report ",
    "check ",
    "keep ",
    "run ",
    "set ",
    "treat ",
    "use ",
    "never ",
    "make ",
    "refuse ",
)
EXPANSIONS = {
    "F1": re.compile(
        r"harmonic\s+means?\s+of\s+precision\s+and\s+recall\s+\(F1\)|"
        r"F1\s+means\s+the\s+harmonic\s+mean\s+of\s+precision\s+and\s+recall",
        re.IGNORECASE,
    ),
    "QAT": re.compile(
        r"quantization-aware(?:\s+training|-trained)\s+\(QAT\)", re.IGNORECASE
    ),
    "MTP": re.compile(r"multi-token\s+prediction\s+\(MTP\)", re.IGNORECASE),
    "KV": re.compile(r"key-value\s+\(KV\)", re.IGNORECASE),
}


def article_path(slug: str) -> Path:
    return ROOT / "articles" / slug / "article" / f"{slug}.md"


def ready_articles() -> tuple[str, ...]:
    ready: list[str] = []
    for readme in sorted((ROOT / "articles").glob("*/README.md")):
        text = readme.read_text(encoding="utf-8")
        if "Publication-ready" in text and "Not yet published" in text:
            ready.append(readme.parent.name)
    return tuple(ready)


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        return "", text
    return parts[1], parts[2]


def prose_without_code_or_tables(body: str) -> str:
    lines: list[str] = []
    fenced = False
    for line in body.splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced or line.startswith("    ") or line.startswith("|"):
            continue
        lines.append(re.sub(r"`[^`]+`", "", line))
    return "\n".join(lines)


def check(slug: str) -> list[str]:
    path = article_path(slug)
    failures: list[str] = []
    if not path.is_file():
        return [f"missing article: {path}"]

    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    if not frontmatter:
        failures.append("missing YAML frontmatter")
    for key in REQUIRED_FRONTMATTER:
        if not re.search(rf"^{key}:", frontmatter, re.MULTILINE):
            failures.append(f"missing frontmatter field: {key}")

    evidence = ROOT / "articles" / slug / "evidence" / "figures.md"
    if not evidence.is_file():
        failures.append("missing evidence/figures.md")
    if "https://github.com/RakuenSoftware/rakuen-blog/" not in body:
        failures.append("missing absolute provenance link")
    if "Rakuen builds aimee" not in body:
        failures.append("missing adjacent interest disclosure")

    prose = prose_without_code_or_tables(body)
    if "—" in prose:
        failures.append("contains an em dash")
    if "?" in prose:
        failures.append("contains a prose question; review for decoration")
    if re.search(r"[\U0001F300-\U0001FAFF]", prose):
        failures.append("contains emoji")
    for word in FORBIDDEN_WORDS:
        if re.search(rf"\b{word}\b", prose, re.IGNORECASE):
            failures.append(f"contains intensifier: {word}")
    if re.search(r"\barm(?:s)?\b", prose, re.IGNORECASE):
        failures.append("uses arm instead of run")
    if re.search(r"Ready for publication|Publication-ready", body, re.IGNORECASE):
        failures.append("contains workflow status in article prose")

    for acronym, expansion in EXPANSIONS.items():
        first = re.search(rf"\b{re.escape(acronym)}\b", prose)
        if first:
            marker = expansion.search(prose)
            if not marker or marker.start() > first.start():
                failures.append(f"{acronym} is not expanded at first use")

    for match in re.finditer(r"\*\*([^*]+)\*\*", prose):
        content = match.group(1).strip()
        if not re.search(r"\d", content) and not content.lower().startswith(RULE_VERBS):
            failures.append(f"bold is neither a figure nor a rule: {content!r}")

    blocks = re.split(r"\n\s*\n", prose)
    for block in blocks:
        compact = " ".join(line.strip() for line in block.splitlines())
        if not compact or compact.startswith("#") or compact.startswith("-"):
            continue
        sentence_count = len(re.findall(r"[.!](?:[\"”']|$|\s)", compact))
        if sentence_count > 4:
            failures.append(
                f"paragraph has {sentence_count} sentences: {compact[:80]!r}"
            )

    word_count = len(re.findall(r"\b[\w.+−]+\b", body))
    if word_count > 1300:
        failures.append(f"article exceeds 1,300-word gate: {word_count}")
    return failures


def main() -> int:
    selected = tuple(sys.argv[1:]) or ready_articles()
    if not selected:
        print("FAIL no publication-ready articles discovered")
        return 1
    failed = False
    for slug in selected:
        failures = check(slug)
        if failures:
            failed = True
            print(f"FAIL {slug}")
            for failure in failures:
                print(f"  - {failure}")
        else:
            print(f"PASS {slug}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
