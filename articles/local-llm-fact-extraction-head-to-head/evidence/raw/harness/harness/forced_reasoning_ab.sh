#!/bin/bash
# Does forcing reasoning change the answer on the notes the model chose to skip?
#
# E4B at Q6 answers about 13% of notes with no reasoning pass, reproducibly:
# 13.3% on three separate 10,000-note runs, with and without speculation, and
# 15.0% to 16.8% on four 1,001-note campaigns. The same weights at Q4 and Q8 do
# it on 0.1%. So the build decides, not the note.
#
# Every comparison up to now has been observational, and observation cannot
# settle the question that matters. The model picks which notes go silent, so
# "silent notes score well" fits two stories at once: reasoning was not needed
# there, or the model skipped the notes it already knew. The same note answered
# both ways separates them.
#
# Both halves run against ONE server process with the same weights, cache size
# and concurrency. The only difference is the conditional clause: "Reason first
# if it helps" against "Reason first on every note".
#
# The wording is a confound and the design absorbs it. Notes that reasoned under
# BOTH prompts are the control. If those move as much as the forced-silent ones,
# the effect is the sentence and not the reasoning.
#
# Q6 is the subject because it is the build that shows the behaviour. Running
# this on Q4 would measure a 0.1% population and answer nothing.
set -u
cd "$(dirname "$0")/.." || exit 1

CARD=${CARD:-xtx}
OUT=results/forced-reasoning-20260813
GOLD=data/corpora/v5/gold_small.jsonl
REPO_ID=unsloth/gemma-4-E4B-it-GGUF:UD-Q6_K_XL
FAM=gemma-4-E4B-it
mkdir -p "$OUT"
EXPECT=$(wc -l < "$GOLD")
LOG="$OUT/forced_reasoning.log"
say() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$LOG"; }

case "$CARD" in
  xtx)  PORT=8830 ;;
  5080) PORT=8330 ;;
  *) echo "CARD must be xtx or 5080"; exit 1 ;;
esac

run_half() {   # $1 = prompt version
  local VER=$1
  local LBL="$FAM.Q6.$VER"
  local PRED="$OUT/$LBL.pred.jsonl"
  if [ -s "$PRED" ] && [ "$(wc -l < "$PRED")" -ge "$EXPECT" ]; then
    say "SKIP $LBL (banked)"; return 0
  fi
  say "--- $LBL on $CARD, nproc=1, no speculation, $EXPECT notes"
  local t0=$(date +%s)
  GOLD="$GOLD" OUT="$OUT" LABEL="$LBL" REPO="$REPO_ID" DRAFT="" \
    VERIFY_FAM="$FAM" CARD="$CARD" NPROC=1 BASE_PORT="$PORT" \
    CACHE_RAM_MIB=1024 PROMPT_VERSION="$VER" \
    bash harness/shard_run.sh || { say "FAIL $LBL"; return 1; }
  local t1=$(date +%s)
  say "OK $LBL wall=$(( (t1-t0)/60 ))m"
}

say "=== forced-reasoning A/B on the $CARD, $EXPECT notes, $FAM UD-Q6_K_XL"
run_half live || exit 1
run_half forcereason || exit 1

say "=== paired result ==="
python3 harness/forced_reasoning.py --out "$OUT" --gold "$GOLD" 2>&1 | tee -a "$LOG"
say "=== forced-reasoning A/B COMPLETE ==="
