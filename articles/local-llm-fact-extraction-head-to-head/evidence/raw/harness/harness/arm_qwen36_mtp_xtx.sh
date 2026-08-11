#!/bin/bash
# Qwen3.6 with speculation on and off, on the idle 7900 XTX — a SECOND FAMILY.
#
# WHY. The published article says gemma-4 is the only family in this field that
# ships a draft model, and states one-family coverage as a limit on the whole
# result. That is now false: ggml-org publishes mtp-*.gguf sidecars for both
# Qwen3.6-27B (dense) and Qwen3.6-35B-A3B (MoE), and llama-b10210 already
# carries graph_mtp for the qwen35 and qwen35moe architectures these GGUFs
# declare. So the limit can be measured away rather than restated.
#
# It also asks something gemma cannot. The article's other finding is that a
# sparse model beats speculation outright (3.5x from architecture against 2x
# from guessing) — but it measured that with speculation absent on both sides.
# This pair runs the SAME toggle on a dense and a sparse model of one family,
# which is the comparison that says whether the two mechanisms add.
#
# USAGE:  SIZE=27b|35b MTP=on|off bash harness/harness/arm_qwen36_mtp_xtx.sh
#
# THREE THINGS THAT ARE NOT OPTIONAL:
#   --device Vulkan1. Vulkan0 is the 16GB Phoenix iGPU. Defect 30 was a week of
#   measurements against an integrated GPU because llama.cpp takes device 0.
#
#   -np 1. Speculation and many slots are mutually exclusive on this backend
#   (probe_mtp_xtx.sh), and concurrency perturbs greedy output anyway.
#
#   -hf REPO:QUANT with -hfd REPO and NO -md. An explicit -md suppresses sidecar
#   resolution and silently produces a non-speculative run (enable_mtp.sh).
#
# THE DRAFT HEAD IS Q4_0 AND THAT IS NOT A CHOICE. gemma's arms used Q8_0 heads
# deliberately, because a low-quality draft depresses the acceptance rate and
# acceptance is the number the comparison turns on. On b10210 the head quant
# tracks the base quant and cannot be overridden: -hfd REPO:mtp-...-Q8_0.gguf is
# accepted and then ignored (measured — byte-identical 664 drafted / 377 accepted
# either way), and the only flag that names a draft file explicitly is the -md
# that turns MTP off. So Qwen runs a Q4_0 head against gemma's Q8_0 one. Both
# Qwen arms and both sizes share it, so the on/off comparison is unaffected; the
# gemma-to-Qwen acceptance comparison carries it as a caveat and cannot be
# cleaned up without a newer build.
set -u
cd "$(dirname "$0")/../.." || exit 1
SIZE=${SIZE:?set SIZE=27b or 35b}
MTP=${MTP:?set MTP=on or off}
OUT=results/qwen36-mtp-xtx
mkdir -p "$OUT"
say() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$OUT/arms.log"; }
. harness/harness/banked.sh

HOST=admin@192.168.1.254
PORT=8117
BIN=/mnt/media/tierbench/bin/llama-b10210/llama-server
GOLD=corpus/data/corpora/v5/gold_small.jsonl

case "$SIZE" in
  27b) REPO=ggml-org/Qwen3.6-27B-GGUF:Q4_K_M;     WANT=Qwen3.6-27B-Q4_K_M ;;
  35b) REPO=ggml-org/Qwen3.6-35B-A3B-GGUF:Q4_K_M; WANT=Qwen3.6-35B-A3B-Q4_K_M ;;
  *) say "SIZE must be 27b or 35b"; exit 1 ;;
esac
case "$MTP" in
  on)  DRAFT_ARG="-hfd ${REPO%%:*}"; WANT_SPEC=True ;;
  off) DRAFT_ARG="";                 WANT_SPEC=False ;;
  *) say "MTP must be on or off"; exit 1 ;;
esac

LBL="Qwen3.6-$SIZE.Q4_K_M.xtx.mtp-$MTP"
PRED="$OUT/$LBL.pred.jsonl"
banked_or_discarded "$PRED" "$GOLD" "$LBL" || exit 0
say "=== $LBL"

ssh -n -o ConnectTimeout=20 "$HOST" "pkill -f llama-server" >/dev/null 2>&1
sleep 5

say "starting: -hf $REPO ${DRAFT_ARG:-(no draft repo)}"
ssh -n -o ConnectTimeout=25 "$HOST" \
  "HF_HOME=/mnt/media/storage/models/hf nohup setsid $BIN -hf $REPO $DRAFT_ARG --host 127.0.0.1 --port $PORT -c 8192 -np 1 --device Vulkan1 --no-webui --no-mmproj -ngl 99 >/tmp/arm-$LBL.log 2>&1 </dev/null &" >/dev/null 2>&1

# No clock: a first fetch is 20 GiB and every deadline tried on this project
# abandoned a working host. The wait ends on health, or on the process being gone.
while true; do
  ssh -n -o ConnectTimeout=10 "$HOST" "curl -sf --max-time 5 http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break
  if ! ssh -n -o ConnectTimeout=10 "$HOST" "pgrep -f llama-server >/dev/null" 2>/dev/null; then
    say "FAIL: server gone. Last lines of its log:"
    ssh -n "$HOST" "tail -15 /tmp/arm-$LBL.log" 2>&1 | tail -15
    exit 1
  fi
  sleep 20
done

LOADED=$(ssh -n "$HOST" "curl -s http://127.0.0.1:$PORT/props" | python3 -c "import json,sys;print((json.load(sys.stdin).get('model_path') or '').split('/')[-1])" 2>/dev/null)
case "$LOADED" in
  *$WANT*) say "loaded $LOADED" ;;
  *) say "IDENTITY GUARD FAILED: loaded '$LOADED', wanted *$WANT*"; exit 1 ;;
esac

# The toggle IS the experiment, so it is asserted rather than assumed. A silently
# unresolved sidecar would make the on-arm a duplicate of the off-arm and the
# pair would read as "speculation does nothing", which is a publishable-looking
# wrong answer.
SPEC=$(ssh -n "$HOST" "curl -s http://127.0.0.1:$PORT/slots" | python3 -c "import json,sys;d=json.load(sys.stdin);print((d[0] if d else {}).get('speculative'))" 2>/dev/null)
[ "${SPEC,,}" = "${WANT_SPEC,,}" ] || { say "GUARD FAILED: speculative=$SPEC, wanted $WANT_SPEC"; exit 1; }
say "speculative=$SPEC as intended"
ssh -n "$HOST" "$BIN --list-devices 2>/dev/null | sed -n 2,4p" | sed 's/^/  /'

# .254 firewalls its serving ports off-host: ssh is reachable, 8117 is not.
pkill -f "ssh -N -L $PORT:" 2>/dev/null; sleep 1
setsid nohup ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -L "$PORT:127.0.0.1:$PORT" "$HOST" >/dev/null 2>&1 </dev/null &
sleep 6

t0=$(date +%s)
python3 harness/harness/run_llamacpp.py --base-url "http://127.0.0.1:$PORT" --model "$LBL" \
  --gold "$GOLD" --out "$PRED" --thinking --max-tokens 8192 --concurrency 1 || { say "FAIL client"; exit 1; }
t1=$(date +%s)

if ! python3 harness/harness/score.py --gold "$GOLD" --pred "$PRED" --json-out "$OUT/$LBL.score.json" 2>"$OUT/$LBL.err"; then
  if grep -q 'thinking:true' "$OUT/$LBL.err"; then
    python3 harness/harness/score.py --gold "$GOLD" --pred "$PRED" --allow-thinking-off --json-out "$OUT/$LBL.score.json" >/dev/null 2>&1
  else
    say "BLOCKED: $(tr '\n' ' ' < "$OUT/$LBL.err" | cut -c1-200)"; exit 1
  fi
fi
rm -f "$OUT/$LBL.err"
say "OK $LBL $(python3 -c "
import json;d=json.load(open('$OUT/$LBL.score.json'));s=d['strict']
print('F1=%.4f P=%.4f R=%.4f'%(s['f1'],s['precision'],s['recall']))") wall=$(( (t1-t0)/60 ))m"
python3 harness/harness/draft_acceptance.py "$PRED" | sed 's/^/  /'
