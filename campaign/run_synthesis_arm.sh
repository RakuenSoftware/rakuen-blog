#!/bin/bash
# The synthesis half of ONE arm. Runs INSIDE CT 140, immediately after that
# arm's extraction half, against the same weights on the same card.
#
# Separate from run_arm.sh on purpose. The synthesis controller launches and
# owns its own llama-server with its own load profile, so the two halves cannot
# share a process; trying to fold it into run_arm.sh would mean either running
# the controller against a server it did not configure, or reimplementing it.
# Neither is worth it -- the controller is the piece the synthesis article
# validated, and it stays untouched.
#
# The cost is one extra model load per arm. Accepted: correctness of the load
# profile matters more than a few minutes of reload, and the weights are already
# in the page cache from extraction.
set -u

ROOT=${ROOT:-/opt/campaign}
BUNDLE="$ROOT/bundle"
SYN_OUT=${SYN_OUT:-$ROOT/results-synthesis}
BIN=${BIN:-/opt/llama.cpp/build-cuda/bin/llama-server}
FIXTURE="$BUNDLE/synthesis/fixture"
MAX_CASES=${MAX_CASES:-1000}
SYN_PORT=${SYN_PORT:-8920}

LABEL=${LABEL:?set LABEL}

say() { echo "[$(date -u +%H:%M:%SZ)] $LABEL: synthesis $*"; }

mkdir -p "$SYN_OUT"
ARM="$SYN_OUT/$LABEL"

# Idempotent independently of the extraction half, so re-running the campaign
# backfills synthesis for arms whose extraction already finished without having
# to re-run a 60-minute extraction to get there.
if [ -s "$ARM/summary_$LABEL.json" ]; then
  say "SKIP already complete"
  exit 0
fi
if [ -s "$ARM/SYNTH_FAILED" ]; then
  say "SKIP previously failed; remove SYNTH_FAILED to retry"
  exit 0
fi

# The controller refuses to start if its port is occupied, which is the right
# behaviour but a confusing failure if the extraction server is still dying.
# Wait for the card to actually be free rather than racing it.
for _ in $(seq 1 30); do
  if ! pgrep -f "$BIN" > /dev/null 2>&1; then
    break
  fi
  sleep 2
done
if pgrep -f "$BIN" > /dev/null 2>&1; then
  say "FAIL a llama-server is still running; refusing to contend for the card"
  mkdir -p "$ARM"
  printf 'a llama-server was still running when synthesis was due to start\n' > "$ARM/SYNTH_FAILED"
  exit 1
fi

# 1,000 cases in SHA-256 case-id order is the canonical population for this
# fixture; the controller's default of 0 means all 10,000 and would not be the
# same measurement the synthesis article reports.
say "START ($MAX_CASES cases)"
START=$(date -u +%s)
python3 "$ROOT/run_synthesis_ladder.py" \
  --bundle "$FIXTURE" \
  --results-root "$SYN_OUT" \
  --llama-server "$BIN" \
  --hf-home "${HF_HOME:-/opt/hf}" \
  --port "$SYN_PORT" \
  --max-cases "$MAX_CASES" \
  --labels "$LABEL" >> "$SYN_OUT/$LABEL.log" 2>&1
RC=$?
SECS=$(( $(date -u +%s) - START ))

if [ "$RC" -ne 0 ]; then
  say "FAIL controller exited $RC after ${SECS}s"
  mkdir -p "$ARM"
  printf 'synthesis controller exited %s after %ss\n' "$RC" "$SECS" > "$ARM/SYNTH_FAILED"
  tail -40 "$SYN_OUT/$LABEL.log" >> "$ARM/SYNTH_FAILED" 2>/dev/null
  exit 1
fi

# Exit 0 is not proof. The controller validates its own results and raises on a
# mismatch, but a zero exit with no summary on disk would still read as success
# to the campaign loop, which is precisely the failure shape this campaign keeps
# producing.
if [ ! -s "$ARM/summary_$LABEL.json" ]; then
  say "FAIL controller exited 0 but wrote no summary"
  mkdir -p "$ARM"
  printf 'controller exited 0 with no summary_%s.json\n' "$LABEL" > "$ARM/SYNTH_FAILED"
  tail -40 "$SYN_OUT/$LABEL.log" >> "$ARM/SYNTH_FAILED" 2>/dev/null
  exit 1
fi

ROWS=$(wc -l < "$ARM/raw_$LABEL.jsonl" 2>/dev/null || echo 0)
say "COMPLETE ${SECS}s rows=$ROWS"
exit 0
