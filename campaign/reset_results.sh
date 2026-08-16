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
