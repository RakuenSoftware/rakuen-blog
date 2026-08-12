#!/bin/bash
# The complete fragmentation measurement: v7 (17 relations) against v8 (24), one
# card, one corpus, one model, both arms in full.
#
# The article prints 23.5% -> 10.0% at n=223 and calls it provisional, because
# the run was interrupted and no complete artifact survived it. This is that run
# finished. Nothing else about the protocol changes.
#
# What is being measured is the NOVEL-PREDICATE RATE: the share of extracted
# facts whose relation is outside the seed ontology after alias folding. It moves
# for two reasons at once and the design keeps them together deliberately,
# because that pairing is the decision a reader faces:
#
#   1. the ontology defines seven more relations, so fewer predicates are novel
#   2. the prompt lists those seven, so the model reaches for them instead of
#      inventing a synonym
#
# Separating the two is a rescoring exercise on the same predictions and does not
# need a card. It is done in fragmentation.py, not here.
#
# Both arms hit the SAME server process with the same weights, the same cache
# size and the same concurrency, so the interpolated relation list is the only
# thing that differs between them. shard_run.sh owns the server lifecycle, model
# verification and port hygiene; this script only chooses the two prompts.
set -u
cd "$(dirname "$0")/.." || exit 1

CARD=${CARD:-xtx}
OUT=results/ontology-ab-20260812
GOLD=data/corpora/v5/gold_small.jsonl
REPO_ID=unsloth/gemma-4-E4B-it-GGUF:UD-Q4_K_XL
DRAFT_ID=""
FAM=gemma-4-E4B-it
mkdir -p "$OUT"
EXPECT=$(wc -l < "$GOLD")
LOG="$OUT/ontology_ab.log"
say() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$LOG"; }

case "$CARD" in
  xtx)  PORT=8820 ;;
  5080) PORT=8320 ;;
  *) echo "CARD must be xtx or 5080"; exit 1 ;;
esac

run_arm() {   # $1 = prompt version passed to run_llamacpp.py
  local VER=$1
  local LBL="$FAM.ontology-$VER"
  local PRED="$OUT/$LBL.pred.jsonl"
  if [ -s "$PRED" ] && [ "$(wc -l < "$PRED")" -ge "$EXPECT" ]; then
    say "SKIP $LBL (banked)"; return 0
  fi
  say "--- $LBL on $CARD, nproc=1, no speculation, $EXPECT notes"
  local t0=$(date +%s)
  GOLD="$GOLD" OUT="$OUT" LABEL="$LBL" REPO="$REPO_ID" DRAFT="$DRAFT_ID" \
    VERIFY_FAM="$FAM" CARD="$CARD" NPROC=1 BASE_PORT="$PORT" \
    CACHE_RAM_MIB=1024 PROMPT_VERSION="$VER" \
    bash harness/shard_run.sh || { say "FAIL $LBL"; return 1; }
  local t1=$(date +%s)
  say "OK $LBL wall=$(( (t1-t0)/60 ))m"
}

say "=== ontology A/B on the $CARD, $EXPECT notes, $FAM"
say "v7 renders 17 relations, live renders 24; the template is byte-identical"
run_arm v7 || exit 1
run_arm live || exit 1

say "=== novel-predicate rates ==="
python3 harness/fragmentation.py --out "$OUT" 2>&1 | tee -a "$LOG"
say "=== ontology A/B COMPLETE ==="
