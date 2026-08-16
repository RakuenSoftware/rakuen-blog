#!/usr/bin/env python3
"""Drive the synthesis fixture across the quant-ladder arms, on the 5080.

This does NOT fork `run_candidate_matrix.py`. It imports it and overrides
exactly three things, so that everything the synthesis article validated —
case-population checks, model-identity checks, artifact hashing, the fail-closed
result validator, the single-slot load profile, the run lock — keeps running
unchanged over the ladder arms.

The three overrides, and why each is necessary:

1. `CANDIDATES` is generated from `arms.tsv` instead of being the article's nine
   hardcoded configurations. Same schema, one entry per ladder arm.

2. `validate_candidate_matrix` is replaced. The original refuses any Gemma
   target that is not QAT UD-Q4:

       if candidate.get("target_training") != "QAT" or "qat" not in target:
           raise RuntimeError(...)
       if not quant.startswith("UD-Q4") ...

   That is exactly right for the article it was written for and exactly wrong
   here — it would reject 20 of the 33 arms, including every non-QAT Gemma rung,
   which is most of the ladder. The replacement enforces what a *ladder* needs
   instead: every arm well-formed, labels unique, and every model's rungs drawn
   from one publisher so that a ladder never mixes weights lineages.

3. `LOAD_PROFILE["device"]` becomes `CUDA0`. The article's profile names
   `Vulkan1`, which is the RX 7900 XTX on the other host. This campaign runs on
   the RTX 5080.

Consequence of (3), stated rather than discovered later: these synthesis numbers
share a fixture and a scorer with the published nine-configuration matrix but
NOT a device, so they do not join that table. They are internally comparable
across ladder arms, which is what the ladder needs.

`prompt_cache_mib` stays at 1024. That value is results-affecting in this series
— the 10,000-note ladder had to be re-taken because two families had been run at
different `--cache-ram` settings — so it is held fixed across every arm.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "bundle" / "synthesis"))

import run_candidate_matrix as rcm  # noqa: E402


ARMS = Path(__file__).resolve().parent / "arms.tsv"


def expected_model_name(target: str) -> str:
    """Reproduce the model identity llama.cpp will report for a -hf target.

    `unsloth/gemma-4-E2B-it-qat-GGUF:UD-Q4_K_XL` -> `gemma-4-E2B-it-qat-UD-Q4_K_XL`
    `LiquidAI/LFM2.5-2.6B-GGUF:Q6_K`             -> `LFM2.5-2.6B-Q6_K`

    The controller checks this substring against the served model path and
    raises on a mismatch, which is the guard that catches a target silently
    resolving to a different file than the one asked for.
    """
    repo, _, quant = target.partition(":")
    stem = repo.split("/")[-1]
    if stem.endswith("-GGUF"):
        stem = stem[: -len("-GGUF")]
    return f"{stem}-{quant}"


def load_arms() -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    with ARMS.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#") or not line.strip():
                continue
            row = line.rstrip("\n").split("\t")
            if row[0] == "order":
                continue
            if len(row) != 8:
                raise RuntimeError(f"arms.tsv: expected 8 fields, got {len(row)}: {row!r}")
            _order, label, model, train, width, target, draft, _est = row
            candidates.append(
                {
                    "label": label,
                    "family": model,
                    "target_training": "QAT" if train == "qat" else "base",
                    "target_quantization": width.upper(),
                    "target": target,
                    "draft": draft if draft != "-" else None,
                    "expected_model": expected_model_name(target),
                    "speculative": draft != "-",
                }
            )
    if not candidates:
        raise RuntimeError(f"arms.tsv produced no candidates: {ARMS}")
    return candidates


def validate_ladder(candidates: list[dict[str, object]]) -> None:
    """What a ladder requires, in place of the article's QAT-only rule."""
    labels = [str(c["label"]) for c in candidates]
    duplicates = {label for label in labels if labels.count(label) > 1}
    if duplicates:
        raise RuntimeError(f"duplicate arm labels: {sorted(duplicates)}")

    publishers: dict[str, set[str]] = {}
    for candidate in candidates:
        target = str(candidate["target"])
        if ":" not in target or "/" not in target:
            raise RuntimeError(f"{candidate['label']}: malformed target {target!r}")
        if candidate["speculative"] and not candidate["draft"]:
            raise RuntimeError(f"{candidate['label']}: speculative with no draft")
        publishers.setdefault(str(candidate["family"]), set()).add(target.split("/")[0])

    # A ladder that mixes publishers between its own rungs is not a ladder; it
    # is the mistake quant-clarification-2026-08-09.md records having already
    # been made once, by pairing a Q4 from one campaign against Q6 and Q8 from
    # another. Note this checks TARGET publishers only: Qwen deliberately takes
    # its draft from ggml-org because unsloth ships no MTP sidecar for it, and
    # that draft is identical across all of that model's rungs.
    for model, names in sorted(publishers.items()):
        if len(names) > 1:
            raise RuntimeError(
                f"{model}: rungs span multiple publishers {sorted(names)}; "
                "a ladder must hold weights lineage constant"
            )


def main() -> int:
    candidates = load_arms()
    validate_ladder(candidates)

    rcm.CANDIDATES = tuple(candidates)
    rcm.validate_candidate_matrix = lambda: validate_ladder(list(rcm.CANDIDATES))
    rcm.LOAD_PROFILE["device"] = "CUDA0"

    print(
        f"ladder: {len(candidates)} arms, device={rcm.LOAD_PROFILE['device']}, "
        f"cache_ram={rcm.LOAD_PROFILE['prompt_cache_mib']}MiB",
        flush=True,
    )
    return rcm.main()


if __name__ == "__main__":
    raise SystemExit(main())
