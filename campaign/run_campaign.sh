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

SYN_OUT=${SYN_OUT:-$ROOT/results-synthesis}
mkdir -p "$SYN_OUT"

total=0; complete=0; gated=0; invalid=0; failed=0
synth_complete=0; synth_failed=0; synth_skipped=0

while IFS=$'\t' read -r order label model train width target draft est_gib ctk ctv; do
  case "$order" in ''|'#'*|order) continue ;; esac

  if [ -n "$ONLY" ] && ! printf '%s' ",$ONLY," | grep -q ",$label,"; then
    continue
  fi

  total=$((total + 1))
  say "--- arm $order/$label (${est_gib} GiB est) ---"

  LABEL="$label" MODEL="$model" TRAIN="$train" WIDTH="$width" \
  TARGET="$target" DRAFT="$draft" EST_GIB="$est_gib" ROOT="$ROOT" OUT="$OUT" \
  CTK="${ctk:-f16}" CTV="${ctv:-f16}" \
    bash "$ROOT/run_arm.sh" 2>&1 | tee -a "$LOG"
  # Branch on run_arm.sh's status, NOT the pipeline's -- tee would mask it.
  rc=${PIPESTATUS[0]}

  # A gated or invalidated arm is a RECORDED OUTCOME, not a failure, and the
  # queue moves straight to the next one. Only an arm that broke unexpectedly
  # counts as failed.
  if [ -s "$OUT/$label/SKIPPED_TOO_SLOW" ]; then
    gated=$((gated + 1)); say "arm $label -> extraction GATED (too slow), moving on"
  elif [ -s "$OUT/$label/INVALID_DENSE_SPILL" ]; then
    invalid=$((invalid + 1)); say "arm $label -> extraction INVALID (dense spill), moving on"
  elif [ "$rc" -eq 0 ] && [ -s "$OUT/$label/score.json" ]; then
    complete=$((complete + 1)); say "arm $label -> extraction COMPLETE"
  else
    failed=$((failed + 1)); say "arm $label -> extraction FAILED rc=$rc"
  fi

  # --- synthesis half, same weights, same card, immediately after.
  #
  # This article reports BOTH tasks per arm; an arm with only its extraction
  # half is half an arm. It runs even when extraction was gated or invalidated,
  # because "too slow for 1,001 extraction notes" and "unusable for synthesis"
  # are different questions and the second is worth answering on its own.
  #
  # It is skipped only where there is nothing to serve: a target that could not
  # be loaded at all.
  if [ -s "$OUT/$label/FAILED" ] && grep -q "server" "$OUT/$label/FAILED" 2>/dev/null; then
    say "arm $label -> synthesis SKIPPED (extraction could not serve the model)"
    synth_skipped=$((synth_skipped + 1))
  elif [ -s "$OUT/$label/INVALID_DENSE_SPILL" ]; then
    # A dense spill means the model was mis-served, not that extraction was
    # merely slow. Synthesis on the same mis-served model is invalid for the
    # same reason, and costs ~90 minutes to produce something unusable.
    say "arm $label -> synthesis SKIPPED (dense spill invalidates this serving)"
    synth_skipped=$((synth_skipped + 1))
  else
    # Cache type decides the synthesis results root, so the campaign has to
    # look in the same place run_synthesis_arm.sh writes to.
    if [ "${ctk:-f16}" = "f16" ] && [ "${ctv:-f16}" = "f16" ]; then
      arm_syn_out="$SYN_OUT"
    else
      arm_syn_out="$ROOT/results-synthesis-ctk${ctk}-ctv${ctv}"
    fi
    LABEL="$label" ROOT="$ROOT" CTK="${ctk:-f16}" CTV="${ctv:-f16}" \
      bash "$ROOT/run_synthesis_arm.sh" 2>&1 | tee -a "$LOG"
    src=${PIPESTATUS[0]}
    if [ "$src" -eq 0 ] && [ -s "$arm_syn_out/$label/summary_$label.json" ]; then
      synth_complete=$((synth_complete + 1)); say "arm $label -> synthesis COMPLETE"
    else
      synth_failed=$((synth_failed + 1)); say "arm $label -> synthesis FAILED rc=$src"
    fi
  fi
done < "$ARMS"

say "=== CAMPAIGN END ==="
say "extraction: complete=$complete gated=$gated invalid=$invalid failed=$failed of $total attempted"
say "synthesis:  complete=$synth_complete failed=$synth_failed skipped=$synth_skipped"
if [ "$synth_complete" -ne "$complete" ]; then
  say "NOTE extraction and synthesis counts differ; an arm with only one half is"
  say "     not a two-task result and must not be reported as one"
fi
if [ "$gated" -gt 0 ] || [ "$invalid" -gt 0 ]; then
  say "ladders with a gated or invalid rung are INCOMPLETE and must be reported as such:"
  for d in "$OUT"/*/; do
    [ -s "$d/SKIPPED_TOO_SLOW" ] && say "  gated:   $(basename "$d")"
    [ -s "$d/INVALID_DENSE_SPILL" ] && say "  invalid: $(basename "$d")"
  done
fi
[ "$failed" -eq 0 ]
