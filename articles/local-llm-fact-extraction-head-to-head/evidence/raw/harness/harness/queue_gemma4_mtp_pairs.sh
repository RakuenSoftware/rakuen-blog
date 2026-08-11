#!/bin/bash
# Two independent GPU lanes. Run with CARD=5080 or CARD=xtx.
set -u
cd "$(dirname "$0")/../.." || exit 1
CARD=${CARD:?set CARD=5080 or xtx}
OUT=results/gemma4-mtp-pairs-20260810
mkdir -p "$OUT"
say() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$OUT/queue-$CARD.log"; }

run_pair() {
  local size=$1
  say "PAIR START size=$size card=$CARD order=off,on"
  SIZE="$size" CARD="$CARD" MTP=off bash harness/harness/arm_gemma4_mtp_pair.sh || exit 1
  SIZE="$size" CARD="$CARD" MTP=on bash harness/harness/arm_gemma4_mtp_pair.sh || exit 1
  say "PAIR COMPLETE size=$size card=$CARD"
}

case "$CARD" in
  5080)
    run_pair 12b
    run_pair 26b
    ;;
  xtx)
    # Do not overlap the Qwen3.6-35B-A3B replacement off-side already using
    # Vulkan1. Wait for its owning wrapper, then claim the card for 31B.
    say "waiting for Qwen3.6-35B-A3B off-side to release the XTX"
    while pgrep -f 'arm_qwen36_mtp_xtx[.]sh' >/dev/null 2>&1; do sleep 30; done

    # arm_qwen36_mtp_xtx.sh owns the run but historically leaves its server and
    # SSH forward resident. Resolve both exact PIDs from the listening socket;
    # never use a broad llama-server or ssh pattern here.
    REMOTE_PID=$(ssh -n -o ConnectTimeout=15 admin@192.168.1.254 \
      "ss -ltnpH 'sport = :8117'" 2>/dev/null \
      | grep -oE 'pid=[0-9]+' | head -1 | cut -d= -f2)
    if [ -n "$REMOTE_PID" ]; then
      say "releasing completed Qwen server pid=$REMOTE_PID on XTX port 8117"
      ssh -n -o ConnectTimeout=15 admin@192.168.1.254 "kill -TERM $REMOTE_PID" >/dev/null 2>&1 || exit 1
      sleep 4
    fi
    LOCAL_PID=$(ss -ltnpH 'sport = :8117' 2>/dev/null \
      | grep -oE 'pid=[0-9]+' | head -1 | cut -d= -f2)
    if [ -n "$LOCAL_PID" ]; then
      say "releasing completed Qwen tunnel pid=$LOCAL_PID on local port 8117"
      kill -TERM "$LOCAL_PID" 2>/dev/null || exit 1
      sleep 2
    fi
    ssh -n -o ConnectTimeout=15 admin@192.168.1.254 \
      "ss -ltnpH 'sport = :8117'" 2>/dev/null | grep -q . \
      && { say "FAIL: Qwen server still owns XTX port 8117"; exit 1; }
    run_pair 31b
    ;;
  *) say "CARD must be 5080 or xtx"; exit 1 ;;
esac

say "QUEUE COMPLETE card=$CARD"
