#!/usr/bin/env python3
"""Add the three small-model BF16 rungs that were specified and never run.

BF16 was requested for every model except gemma-4 12B. It was deferred in the
registered plan pending offload measurements, then reinstated for LFM2.5-2.6B
only — the model under discussion at the time — and the other five were never
brought back.

This adds the three that are cheap and card-resident or lightly offloaded:
gemma-4 E2B, gemma-4 E4B and LFM2.5-8B-A1B. The two large mixtures, 26B-A4B at
~52 GiB and Qwen3.6-35B-A3B at ~70 GiB, are left out deliberately: they would
run for days and their BF16 numbers would mostly re-measure the capacity effect
the campaign already documents.

Why it matters that these run: BF16 is the unquantised reference. Without it a
ladder can only say what four bits costs relative to six or eight, not what
quantisation costs relative to none. LFM2.5-2.6B is currently the only model
where that question has an answer.
"""

from pathlib import Path

ARMS = Path(__file__).resolve().parent / "arms.tsv"

# Inserted after each model's Q8 rung so a ladder stays in ascending width.
NEW_AFTER = {
    "gemma4-e2b.base.q8": (
        "gemma4-e2b.base.bf16", "gemma4-e2b", "base", "bf16",
        "unsloth/gemma-4-E2B-it-GGUF:BF16",
        "unsloth/gemma-4-E2B-it-GGUF:MTP/mtp-gemma-4-E2B-it-Q8_0.gguf", "10.0",
    ),
    "gemma4-e4b.base.q8": (
        "gemma4-e4b.base.bf16", "gemma4-e4b", "base", "bf16",
        "unsloth/gemma-4-E4B-it-GGUF:BF16",
        "unsloth/gemma-4-E4B-it-GGUF:MTP/mtp-gemma-4-E4B-it-Q8_0.gguf", "16.0",
    ),
    "lfm25-8b-a1b.base.q8": (
        "lfm25-8b-a1b.base.bf16", "lfm25-8b-a1b", "base", "bf16",
        "LiquidAI/LFM2.5-8B-A1B-GGUF:BF16", "-", "16.0",
    ),
}


def main() -> int:
    lines = ARMS.read_text().splitlines()
    out = []
    added = []
    for line in lines:
        if line.startswith("#") or not line.strip() or line.startswith("order"):
            out.append(line)
            continue
        fields = line.split("\t")
        out.append(line)
        after = NEW_AFTER.get(fields[1])
        if after:
            label, model, train, width, target, draft, est = after
            out.append("\t".join(
                ["0", label, model, train, width, target, draft, est, "f16", "f16"]))
            added.append(label)

    numbered = []
    count = 0
    for line in out:
        if line.startswith("#") or not line.strip() or line.startswith("order"):
            numbered.append(line)
            continue
        count += 1
        fields = line.split("\t")
        fields[0] = str(count)
        numbered.append("\t".join(fields))

    if len(added) != len(NEW_AFTER):
        raise SystemExit(f"expected {len(NEW_AFTER)} insertions, made {len(added)}: {added}")

    ARMS.write_text("\n".join(numbered) + "\n")
    print("added:", *added, sep="\n  ")
    print("total arms:", count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
