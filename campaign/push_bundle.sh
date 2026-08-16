#!/bin/bash
# Assemble the campaign bundle and put it on CT 140. Runs on the REPO HOST.
#
# The bundle mirrors the evidence tree's shape because prompt.py resolves its
# ontology as REPO = Path(__file__).parents[3], i.e. from
#   <root>/raw/harness/harness/prompt.py
# it reads
#   <root>/src/rel_types.c  and  <root>/src/kb/kb_memory_facts.c
# Get that layout wrong and the scorer raises before it scores, which is the
# failure the pinned-ontology README exists to describe.
set -u

REPO=${REPO:-$(git rev-parse --show-toplevel)}
HOST=${HOST:-root@192.168.1.253}
CT=${CT:-140}
DEST=${DEST:-/opt/campaign}

H2H="$REPO/articles/local-llm-fact-extraction-head-to-head/evidence"
SYN="$REPO/articles/synthesis-model-selection/benchmarks"
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT

fail() { echo "PUSHFAIL: $*" >&2; exit 1; }

# --- verify every source exists BEFORE staging, so a missing file is named
[ -d "$H2H/raw/harness/harness" ] || fail "harness missing: $H2H/raw/harness/harness"
[ -f "$H2H/src/rel_types.c" ] || fail "pinned ontology missing: $H2H/src/rel_types.c"
[ -f "$H2H/src/kb/kb_memory_facts.c" ] || fail "pinned prompt missing: $H2H/src/kb/kb_memory_facts.c"
GOLD="$H2H/raw/corpus/data/corpora/v5/gold_small.jsonl"
[ -f "$GOLD" ] || fail "gold set missing: $GOLD"
FIXTURE="$SYN/fixtures/ab-v1/synthesis.jsonl"
[ -f "$FIXTURE" ] || fail "synthesis fixture missing: $FIXTURE"

# --- stage
mkdir -p "$STAGE/bundle/raw/harness" "$STAGE/bundle/src/kb" "$STAGE/bundle/synthesis"
cp -r "$H2H/raw/harness/harness" "$STAGE/bundle/raw/harness/harness" || fail "copy harness"
cp "$H2H/src/rel_types.c" "$STAGE/bundle/src/rel_types.c" || fail "copy rel_types.c"
cp "$H2H/src/kb/kb_memory_facts.c" "$STAGE/bundle/src/kb/" || fail "copy kb_memory_facts.c"
cp "$GOLD" "$STAGE/bundle/gold_small.jsonl" || fail "copy gold"
cp "$FIXTURE" "$STAGE/bundle/synthesis/synthesis.jsonl" || fail "copy fixture"
cp "$SYN/ab-v2/run_candidate_matrix.py" "$STAGE/bundle/synthesis/" || fail "copy synthesis controller"
cp "$SYN/ab-v2/analyze_candidate_matrix.py" "$STAGE/bundle/synthesis/" || fail "copy synthesis analyzer"

cp "$REPO/campaign/arms.tsv" "$STAGE/" || fail "copy arms.tsv"
cp "$REPO/campaign/run_arm.sh" "$STAGE/" || fail "copy run_arm.sh"
cp "$REPO/campaign/run_campaign.sh" "$STAGE/" || fail "copy run_campaign.sh"

GOLD_LINES=$(wc -l < "$STAGE/bundle/gold_small.jsonl")
[ "$GOLD_LINES" -eq 1001 ] || fail "gold set is $GOLD_LINES lines, expected 1001"

# --- ship. Checksums are compared after transfer; a truncated bundle that
#     "looks fine" is exactly the class of failure this campaign cannot afford.
( cd "$STAGE" && tar czf - . ) | ssh -o ConnectTimeout=30 "$HOST" \
  "pct exec $CT -- bash -lc 'mkdir -p $DEST && tar xzf - -C $DEST'"
rc=$?
[ "$rc" -eq 0 ] || fail "transfer exited $rc"

LOCAL_SUM=$(find "$STAGE" -type f -exec sha256sum {} \; | sed "s#$STAGE/##" | sort -k2 | sha256sum | cut -d' ' -f1)
REMOTE_SUM=$(ssh -n -o ConnectTimeout=30 "$HOST" \
  "pct exec $CT -- bash -lc 'cd $DEST && find . -type f -not -path ./results/\* -not -path ./state/\* -exec sha256sum {} \; | sed \"s#^\./##\" | sort -k2 | sha256sum | cut -d\" \" -f1'")

echo "local  bundle sha: $LOCAL_SUM"
echo "remote bundle sha: $REMOTE_SUM"
if [ "$LOCAL_SUM" != "$REMOTE_SUM" ]; then
  echo "PUSHWARN: bundle checksums differ; inspect $DEST on CT $CT before running" >&2
  exit 2
fi
echo "PUSHOK bundle verified at $DEST on CT $CT"
