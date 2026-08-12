"""Novel-predicate rate: the share of extracted facts the ontology does not define.

The article's fragmentation figure was 23.5% -> 10.0% at n=223 from a run that
was interrupted, so this recomputes it from complete artifacts.

A predicate is NOVEL when it survives alias folding and is still not a seed
relation. That is exactly what rel_type_canonicalize() decides in production, so
the same fold runs here rather than a looser string match.

Two things move the rate between v7 and v8 and they are reported apart, because
only one of them needs a card:

  ONTOLOGY   the same predictions rescored against the larger seed set. No model
             involved. This is the share of fragmentation that was the ontology
             failing to cover its own domain.
  PROMPT     the model emitting different predicates because the list it was
             shown changed. Only a rerun shows this, and it is the difference
             between the ontology term and the measured v8 rate.

Reporting one number for both would credit the prompt with work the ontology did.
"""
import argparse
import collections
import json
import pathlib
import re

import prompt
import prompt_versions

SEED_V8 = set(prompt.seed_relations())
SEED_V7 = SEED_V8 - set(prompt_versions.ADDED_V8)
ALIASES = prompt.seed_aliases()


def normalize(rel):
    """rel_type_canonicalize()'s normalisation step, before any fold."""
    return re.sub(r"[^a-z0-9]+", "_", str(rel or "").casefold()).strip("_")


def fold(rel, seed):
    """Leave a seed relation alone, otherwise fold a known alias.

    An alias whose target is not in `seed` does not fold: under v7 there was
    nothing for it to fold to, so treating it as known would score v7 with v8's
    ontology and understate the gap it is there to measure.
    """
    norm = normalize(rel)
    if norm in seed:
        return norm
    target = ALIASES.get(norm)
    if target in seed:
        return target
    return norm


def measure(path, seed):
    facts = novel = rows = 0
    names = collections.Counter()
    for line in path.open():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        rows += 1
        for f in row.get("pred") or []:
            facts += 1
            name = fold(f.get("relation"), seed)
            if name not in seed:
                novel += 1
                names[name] += 1
    return {"rows": rows, "facts": facts, "novel": novel,
            "pct": round(100 * novel / facts, 2) if facts else None,
            "distinct": len(names), "once": sum(1 for c in names.values() if c == 1),
            "top": names.most_common(8)}


def versions_in(path):
    """Every prompt version recorded in the file. More than one means the arm was
    assembled from runs that are not comparable, which is the failure this field
    exists to catch."""
    seen = set()
    for line in path.open():
        line = line.strip()
        if line:
            seen.add(json.loads(line).get("prompt_version"))
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="directory holding the two arms")
    ap.add_argument("--stem", default="gemma-4-E4B-it.ontology")
    args = ap.parse_args()

    d = pathlib.Path(args.out)
    arms = {"v7": d / f"{args.stem}-v7.pred.jsonl",
            "v8": d / f"{args.stem}-live.pred.jsonl"}
    missing = [k for k, p in arms.items() if not p.exists()]
    if missing:
        raise SystemExit(f"missing arm(s): {missing}")

    for label, p in arms.items():
        vs = versions_in(p)
        want = {"v7"} if label == "v7" else {prompt.PROMPT_VERSION}
        if vs != want:
            raise SystemExit(f"{p.name} records prompt_version {vs}, expected {want}")

    v7 = measure(arms["v7"], SEED_V7)
    v8 = measure(arms["v8"], SEED_V8)
    # The v7 predictions rescored against the bigger ontology: model output held
    # fixed, so the whole difference is coverage.
    rescored = measure(arms["v7"], SEED_V8)

    print(f"corpus rows: v7 {v7['rows']}, v8 {v8['rows']}")
    print(f"{'arm':<28} {'facts':>7} {'novel':>7} {'pct':>7} {'distinct':>9} {'seen once':>10}")
    for label, m in (("v7 prompt, 17 relations", v7),
                     ("v7 predictions, 24 rels", rescored),
                     ("v8 prompt, 24 relations", v8)):
        print(f"{label:<28} {m['facts']:>7} {m['novel']:>7} {m['pct']:>7} "
              f"{m['distinct']:>9} {m['once']:>10}")

    if v7["pct"] is not None and v8["pct"] is not None:
        total = v7["pct"] - v8["pct"]
        ontology = v7["pct"] - rescored["pct"]
        print(f"\ntotal fall        {total:+.2f} points")
        print(f"  ontology term   {ontology:+.2f}  (same predictions, larger seed set)")
        print(f"  prompt term     {total - ontology:+.2f}  (model reached for the "
              "listed name)")

    print("\nmost frequent novel predicates")
    for label, m in (("v7", v7), ("v8", v8)):
        print(f"  {label}: " + ", ".join(f"{n} {c}" for n, c in m["top"]))

    (d / "fragmentation.json").write_text(json.dumps(
        {"v7": v7, "v7_rescored_v8": rescored, "v8": v8}, indent=1) + "\n")


if __name__ == "__main__":
    main()
