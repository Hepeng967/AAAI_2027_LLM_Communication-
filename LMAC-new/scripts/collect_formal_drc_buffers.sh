#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"
STAMP="${STAMP:-$(date -u +%Y%m%d_%H%M%S)}"
MAPS="${MAPS:-10b 2r 5z}"
RUN_MAPS="${RUN_MAPS:-1o_10b_vs_1r 1o_2r_vs_4r 5z_vs_1ul}"
TRAIN_COUNT="${TRAIN_COUNT:-64}"
TEST_COUNT="${TEST_COUNT:-64}"
SEED="${SEED:-1234}"
OUTPUT_ROOT="${OUTPUT_ROOT:-$ROOT/data/formal_drc_v5/$STAMP}"
AUDIT_OUT="${AUDIT_OUT:-$ROOT/description/certification_gate/formal_drc_v5_buffers_$STAMP}"
COLLECT_CHUNK_SIZE="${COLLECT_CHUNK_SIZE:-0}"
OVERWRITE_OUTPUT="${OVERWRITE_OUTPUT:-false}"

mkdir -p "$OUTPUT_ROOT" "$AUDIT_OUT"

if [[ "$OVERWRITE_OUTPUT" == "true" ]]; then
  rm -rf "$OUTPUT_ROOT"
  mkdir -p "$OUTPUT_ROOT"
fi

if [[ "$COLLECT_CHUNK_SIZE" -gt 0 ]]; then
  for map_alias in $MAPS; do
    target="$COLLECT_CHUNK_SIZE"
    while [[ "$target" -lt "$TRAIN_COUNT" || "$target" -lt "$TEST_COUNT" ]]; do
      train_target="$target"
      test_target="$target"
      if [[ "$train_target" -gt "$TRAIN_COUNT" ]]; then
        train_target="$TRAIN_COUNT"
      fi
      if [[ "$test_target" -gt "$TEST_COUNT" ]]; then
        test_target="$TEST_COUNT"
      fi
      echo "[COLLECT-CHUNK] map=$map_alias train_count=$train_target test_count=$test_target"
      "$PY" "$ROOT/scripts/collect_lmac_buffers.py" \
        --maps "$map_alias" \
        --train-count "$train_target" \
        --test-count "$test_target" \
        --seed "$SEED" \
        --output-root "$OUTPUT_ROOT"
      target="$(( target + COLLECT_CHUNK_SIZE ))"
    done
    echo "[COLLECT-CHUNK] map=$map_alias train_count=$TRAIN_COUNT test_count=$TEST_COUNT"
    "$PY" "$ROOT/scripts/collect_lmac_buffers.py" \
      --maps "$map_alias" \
      --train-count "$TRAIN_COUNT" \
      --test-count "$TEST_COUNT" \
      --seed "$SEED" \
      --output-root "$OUTPUT_ROOT"
  done
else
  "$PY" "$ROOT/scripts/collect_lmac_buffers.py" \
    --maps $MAPS \
    --train-count "$TRAIN_COUNT" \
    --test-count "$TEST_COUNT" \
    --seed "$SEED" \
    --output-root "$OUTPUT_ROOT" \
    --overwrite
fi

"$PY" "$ROOT/scripts/audit_drc_buffers.py" \
  --buffer-root "$OUTPUT_ROOT" \
  --maps $RUN_MAPS \
  --max-files "$(( TRAIN_COUNT + TEST_COUNT ))" \
  --out-json "$AUDIT_OUT/buffer_audit.json" \
  --out-md "$AUDIT_OUT/buffer_audit.md"

echo "Formal DRC buffers written to: $OUTPUT_ROOT"
echo "Audit written to: $AUDIT_OUT"
echo "Run certification with:"
echo "  BUFFER_ROOT='$OUTPUT_ROOT' RUN_MAPS='$RUN_MAPS' bash '$ROOT/scripts/run_formal_drc_v5.sh'"
