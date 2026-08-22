#!/bin/bash
# Take one deleted arm, then resume the full campaign. Runs INSIDE CT 140.
#
#   ARM_PID=<pid of in-flight run_arm.sh> LABEL=<arm> chain_missing_arm.sh
#
# gemma4-e2b.base.q4 was deleted after a stale llama-server was found sharing
# the card during its run, which inflated its VRAM figure 2.3x and measured its
# throughput under contention. The campaign loop had already passed that
# position, so a plain resume would never revisit it and the E2B QAT comparison
# would be left without its non-QAT baseline.
#
# Waits for the in-flight arm rather than killing it, so nothing in progress is
# wasted.
set -u

ARM_PID=${ARM_PID:?set ARM_PID}
LABEL=${LABEL:?set LABEL}
ROOT=${ROOT:-/opt/campaign}

echo "[chain] waiting for arm pid $ARM_PID to finish"
while kill -0 "$ARM_PID" 2>/dev/null; do sleep 30; done
sleep 20

echo "[chain] stopping the loop"
pkill -f run_campaign.sh 2>/dev/null
sleep 10

echo "[chain] taking $LABEL"
ONLY="$LABEL" bash "$ROOT/run_campaign.sh"
rc=$?
echo "[chain] $LABEL finished rc=$rc"

echo "[chain] resuming the full campaign"
sleep 15
bash "$ROOT/run_campaign.sh"
