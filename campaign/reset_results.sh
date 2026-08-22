#!/bin/bash
# Discard campaign results on CT 140 so the matrix can be re-taken from clean.
#
# Deliberately narrow: it removes only the campaign's own outputs under
# $DEST/{results,state} plus its logs. It never touches $DEST/bundle, the
# harness, the fixtures, or the HuggingFace weight cache under /opt/hf --
# re-downloading 200+ GiB because a reset was sloppy is not an acceptable
# failure mode.
#
# Reason to reset rather than resume: arms are idempotent and skip themselves
# when complete, so results only need clearing when the SERVING CONFIGURATION
# changed and the banked arms are no longer comparable to the ones still to run.
set -u

HOST=${HOST:-root@192.168.1.253}
CT=${CT:-140}
DEST=${DEST:-/opt/campaign}

case "$DEST" in
  /opt/campaign|/opt/campaign/) : ;;
  *) echo "reset refused: DEST=$DEST is not the campaign root" >&2; exit 1 ;;
esac

# reset_results.sh --synth-failed
#   Clear only the SYNTH_FAILED markers, keeping every completed result.
#
# A synthesis arm that failed stays failed so a resumed campaign does not retry
# a genuinely broken configuration forever. That is right for a real failure and
# wrong when the failure was in the harness -- as it was on 2026-08-16, when the
# arms.tsv schema gained two columns and the wrapper still asserted eight
# fields, so every synthesis arm died in under a second for a reason that had
# nothing to do with the model.
# reset_results.sh --failed
#   Clear extraction FAILED markers so those arms retry, keeping every completed
#   result. For a harness fault rather than a model that cannot be served.
if [ "${1:-}" = "--failed" ]; then
  echo "clearing extraction FAILED markers under $DEST on CT $CT (results kept)"
  ssh -n -o ConnectTimeout=30 "$HOST" \
    "pct exec $CT -- bash -lc 'find $DEST/results -name FAILED -print -delete'"
  rc=$?
  [ "$rc" -eq 0 ] || { echo "RESETFAIL: find exited $rc" >&2; exit 1; }
  echo "RESETOK"
  exit 0
fi

# reset_results.sh --synth-arm <label>
#   Discard ONE arm's synthesis so it re-runs, keeping its extraction. For
#   an arm whose synthesis completed mechanically but did not work.
# reset_results.sh --arm <label>
#   Discard ONE arm entirely, both halves, so it re-runs from clean.
if [ "${1:-}" = "--arm" ]; then
  LBL=${2:?usage: reset_results.sh --arm <label>}
  echo "discarding arm $LBL on CT $CT"
  ssh -n -o ConnectTimeout=30 "$HOST" \
    "pct exec $CT -- rm -rf $DEST/results/$LBL $DEST/results-synthesis/$LBL $DEST/results-synthesis/$LBL.log"
  rc=$?
  [ "$rc" -eq 0 ] || { echo "RESETFAIL: rm exited $rc" >&2; exit 1; }
  echo "RESETOK"
  exit 0
fi

if [ "${1:-}" = "--synth-arm" ]; then
  LBL=${2:?usage: reset_results.sh --synth-arm <label>}
  echo "discarding synthesis for $LBL on CT $CT (extraction kept)"
  ssh -n -o ConnectTimeout=30 "$HOST" \
    "pct exec $CT -- rm -rf $DEST/results-synthesis/$LBL $DEST/results-synthesis/$LBL.log"
  rc=$?
  [ "$rc" -eq 0 ] || { echo "RESETFAIL: rm exited $rc" >&2; exit 1; }
  echo "RESETOK"
  exit 0
fi

if [ "${1:-}" = "--synth-failed" ]; then
  echo "clearing SYNTH_FAILED markers under $DEST on CT $CT (results kept)"
  ssh -n -o ConnectTimeout=30 "$HOST" \
    "pct exec $CT -- bash -lc 'find $DEST -name SYNTH_FAILED -print -delete'"
  rc=$?
  [ "$rc" -eq 0 ] || { echo "RESETFAIL: find exited $rc" >&2; exit 1; }
  echo "RESETOK"
  exit 0
fi

echo "resetting results under $DEST on CT $CT (bundle and weight cache untouched)"
ssh -n -o ConnectTimeout=30 "$HOST" \
  "pct exec $CT -- rm -rf $DEST/results $DEST/state $DEST/campaign.log $DEST/smoke.out"
rc=$?
if [ "$rc" -ne 0 ]; then
  echo "RESETFAIL: remote rm exited $rc" >&2
  exit 1
fi

REMAIN=$(ssh -n -o ConnectTimeout=30 "$HOST" \
  "pct exec $CT -- bash -lc 'ls $DEST'")
echo "$REMAIN"
printf '%s' "$REMAIN" | grep -q "bundle" || { echo "RESETFAIL: bundle missing after reset" >&2; exit 1; }
echo "RESETOK"
