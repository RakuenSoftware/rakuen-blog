#!/bin/bash
# Paired bootstrap interval for ONE pair of arms. Runs INSIDE CT 140.
#
#   pair_ci.sh <baseline-label> <comparison-label>
#
# Reports <comparison> minus <baseline>, resampling the SAME note indices for
# both runs.
#
# ONE COMPARISON PER INVOCATION, and that is not a style choice. bootstrap_ci.py
# draws the individual-run and paired intervals from a single random stream, so
# passing a third --pred shifts a paired endpoint even at an identical seed. The
# series' published values are the one-pair-per-process ones; the article's own
# quant-clarification-2026-08-09.md records four interval endpoints that moved
# when this was got wrong. Do not "optimise" this into a single multi-pred call.
#
# Seed 20260809 with 20,000 replicates is the series standard. Every other
# interval in these articles uses it, so a different seed here would make this
# campaign's ranges incomparable to the published ones.
set -u

ROOT=${ROOT:-/opt/campaign}
BUNDLE="$ROOT/bundle"
OUT=${OUT:-$ROOT/results}
GOLD=${GOLD:-$BUNDLE/gold_small.jsonl}
SEED=${SEED:-20260809}
BOOT=${BOOT:-20000}

BASE=${1:?usage: pair_ci.sh <baseline-label> <comparison-label>}
COMP=${2:?usage: pair_ci.sh <baseline-label> <comparison-label>}

BASE_PRED="$OUT/$BASE/pred.jsonl"
COMP_PRED="$OUT/$COMP/pred.jsonl"

for f in "$GOLD" "$BASE_PRED" "$COMP_PRED"; do
  if [ ! -s "$f" ]; then
    echo "PAIRFAIL: missing or empty: $f" >&2
    exit 1
  fi
done

# Both runs must cover the whole gold set. A pair where one side is short is not
# a paired comparison, and resampling it would produce an interval that looks
# perfectly respectable while being computed over mismatched notes.
EXPECT=$(wc -l < "$GOLD")
for f in "$BASE_PRED" "$COMP_PRED"; do
  n=$(wc -l < "$f")
  if [ "$n" -ne "$EXPECT" ]; then
    echo "PAIRFAIL: $f has $n rows, gold has $EXPECT" >&2
    exit 1
  fi
done

echo "=== $COMP minus $BASE ==="
echo "gold=$EXPECT notes  seed=$SEED  replicates=$BOOT  (one comparison per process)"
cd "$BUNDLE/raw/harness" || exit 1
# --pred takes LABEL=PATH, not a bare path. bootstrap_ci.py does
# spec.partition("="), so a bare path lands entirely in the label and leaves the
# path empty, and the tool dies with FileNotFoundError: '' -- which reads like a
# missing file rather than a malformed argument. The FIRST --pred is the
# reference; deltas are reported against it.
python3 harness/bootstrap_ci.py \
  --gold "$GOLD" \
  --pred "$BASE=$BASE_PRED" \
  --pred "$COMP=$COMP_PRED" \
  --boot "$BOOT" \
  --seed "$SEED"
rc=$?
if [ "$rc" -ne 0 ]; then
  echo "PAIRFAIL: bootstrap_ci.py exited $rc" >&2
  exit 1
fi
echo "PAIROK"
