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
# The synthesis controller requires the WHOLE bundle directory, not just the
# fixture: main() refuses to start unless corpus.jsonl, synthesis.jsonl and
# manifest.json are all present, and it hashes run_synthesis_ab.py and
# build_254_fixtures.py as siblings of the controller.
FIXDIR="$SYN/fixtures/ab-v1"
for f in corpus.jsonl synthesis.jsonl manifest.json; do
  [ -f "$FIXDIR/$f" ] || fail "synthesis bundle missing: $FIXDIR/$f"
done
for f in run_candidate_matrix.py analyze_candidate_matrix.py run_synthesis_ab.py build_254_fixtures.py; do
  [ -f "$SYN/ab-v2/$f" ] || fail "synthesis script missing: $SYN/ab-v2/$f"
done

# --- stage
mkdir -p "$STAGE/bundle/raw/harness" "$STAGE/bundle/src/kb" "$STAGE/bundle/synthesis"
cp -r "$H2H/raw/harness/harness" "$STAGE/bundle/raw/harness/harness" || fail "copy harness"
cp "$H2H/src/rel_types.c" "$STAGE/bundle/src/rel_types.c" || fail "copy rel_types.c"
cp "$H2H/src/kb/kb_memory_facts.c" "$STAGE/bundle/src/kb/" || fail "copy kb_memory_facts.c"
cp "$GOLD" "$STAGE/bundle/gold_small.jsonl" || fail "copy gold"

# The controller resolves its siblings by __file__, so the ab-v2 scripts must
# land together in one directory, with the fixture bundle beside them.
cp "$SYN/ab-v2/"*.py "$STAGE/bundle/synthesis/" || fail "copy synthesis scripts"
mkdir -p "$STAGE/bundle/synthesis/fixture"
cp "$FIXDIR/corpus.jsonl" "$FIXDIR/synthesis.jsonl" "$FIXDIR/manifest.json" \
   "$STAGE/bundle/synthesis/fixture/" || fail "copy synthesis fixture bundle"

for f in arms.tsv run_arm.sh run_campaign.sh run_synthesis_ladder.py; do
  cp "$REPO/campaign/$f" "$STAGE/" || fail "copy $f"
done

GOLD_LINES=$(wc -l < "$STAGE/bundle/gold_small.jsonl")
[ "$GOLD_LINES" -eq 1001 ] || fail "gold set is $GOLD_LINES lines, expected 1001"

# --- verify PER FILE, not by hashing a file listing.
#
# The previous version hashed the output of `find | sha256sum | sed | sort`
# on both ends and compared the two digests. That compared path *formatting* as
# much as content: the local list yielded "arms.tsv" while the remote list,
# after its sed passed through ssh -> pct exec -> bash -lc quoting, kept the
# "./" prefix. Identical files, different digest, and a warning that meant
# nothing. A guard that cries wolf gets ignored, which is worse than no guard.
#
# A manifest of relative paths shipped with the bundle and checked by
# `sha256sum -c` on the far side compares content and nothing else, and names
# the offending file when it disagrees.
# The manifest must exclude itself: listing it means hashing a file that is
# still being written, which then fails its own check on the far side and
# reports a corrupt bundle when nothing is wrong.
( cd "$STAGE" && find . -type f -not -name MANIFEST.sha256 | sed 's#^\./##' | sort \
    | xargs sha256sum > MANIFEST.sha256 ) || fail "could not build manifest"

( cd "$STAGE" && tar czf - . ) | ssh -o ConnectTimeout=30 "$HOST" \
  "pct exec $CT -- bash -lc 'mkdir -p $DEST && tar xzf - -C $DEST'"
rc=$?
[ "$rc" -eq 0 ] || fail "transfer exited $rc"

VERIFY=$(ssh -n -o ConnectTimeout=60 "$HOST" \
  "pct exec $CT -- bash -lc 'cd $DEST && sha256sum -c --quiet MANIFEST.sha256 2>&1; echo RC=\$?'")
VRC=$(printf '%s' "$VERIFY" | grep -oE 'RC=[0-9]+' | tail -1 | cut -d= -f2)

if [ "${VRC:-1}" -ne 0 ]; then
  echo "PUSHFAIL: bundle verification failed on CT $CT" >&2
  printf '%s\n' "$VERIFY" >&2
  exit 2
fi
FILES=$(wc -l < "$STAGE/MANIFEST.sha256")
echo "PUSHOK $FILES files verified byte-for-byte at $DEST on CT $CT"
