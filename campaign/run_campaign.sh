#!/bin/bash
# Drive every arm in arms.tsv, in order, one at a time. Runs INSIDE CT 140.
#
# Re-runnable: each arm skips itself if it already has a complete prediction set
# and a score, or if it was already gated as too slow. So an interrupted
# campaign is resumed by running this again, and a single arm is re-taken by
# deleting its directory.
#
# Nothing here aborts the campaign on one bad arm. A failed or gated arm is
# recorded and the queue moves on, which is the operator's rule and also what
# keeps a 33-arm run from dying overnight on rung 6.
set -u

ROOT=${ROOT:-/opt/campaign}
ARMS=${ARMS:-$ROOT/arms.tsv}
OUT=${OUT:-$ROOT/results}
LOG="$ROOT/campaign.log"
ONLY=${ONLY:-}            # optional: comma-separated labels, run just these

mkdir -p "$OUT"
say() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG"; }

say "=== CAMPAIGN START ==="
say "arms=$ARMS out=$OUT"
[ -n "$ONLY" ] && say "restricted to: $ONLY"

total=0; complete=0; gated=0; invalid=0; failed=0

while IFS=$'\t' read -r order label model train width target draft est_gib; do
  case "$order" in ''|'#'*|order) continue ;; esac

  if [ -n "$ONLY" ] && ! printf '%s' ",$ONLY," | grep -q ",$label,"; then
    continue
  fi

  total=$((total + 1))
  say "--- arm $order/$label (${est_gib} GiB est) ---"

  LABEL="$label" MODEL="$model" TRAIN="$train" WIDTH="$width" \
  TARGET="$target" DRAFT="$draft" EST_GIB="$est_gib" ROOT="$ROOT" OUT="$OUT" \
    bash "$ROOT/run_arm.sh" 2>&1 | tee -a "$LOG"
  # Branch on run_arm.sh's status, NOT the pipeline's -- tee would mask it.
  rc=${PIPESTATUS[0]}

  # A gated or invalidated arm is a RECORDED OUTCOME, not a failure, and the
  # queue moves straight to the next one. Only an arm that broke unexpectedly
  # counts as failed.
  if [ -s "$OUT/$label/SKIPPED_TOO_SLOW" ]; then
    gated=$((gated + 1)); say "arm $label -> GATED (too slow), moving on"
  elif [ -s "$OUT/$label/INVALID_DENSE_SPILL" ]; then
    invalid=$((invalid + 1)); say "arm $label -> INVALID (dense spill), moving on"
  elif [ "$rc" -eq 0 ] && [ -s "$OUT/$label/score.json" ]; then
    complete=$((complete + 1)); say "arm $label -> COMPLETE"
  else
    failed=$((failed + 1)); say "arm $label -> FAILED rc=$rc"
  fi
done < "$ARMS"

say "=== CAMPAIGN END ==="
say "complete=$complete gated=$gated invalid=$invalid failed=$failed of $total attempted"
if [ "$gated" -gt 0 ] || [ "$invalid" -gt 0 ]; then
  say "ladders with a gated or invalid rung are INCOMPLETE and must be reported as such:"
  for d in "$OUT"/*/; do
    [ -s "$d/SKIPPED_TOO_SLOW" ] && say "  gated:   $(basename "$d")"
    [ -s "$d/INVALID_DENSE_SPILL" ] && say "  invalid: $(basename "$d")"
  done
fi
[ "$failed" -eq 0 ]
