#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"
STAMP="${STAMP:-$(date -u +%Y%m%d_%H%M%S)}"
OUT_ROOT="${OUT_ROOT:-$ROOT/description/certification_gate/drc_teacher_construction_$STAMP}"
RUN_MAPS="${RUN_MAPS:-1o_10b_vs_1r 1o_2r_vs_4r 5z_vs_1ul}"
CANDIDATE_ROOT="${CANDIDATE_ROOT:-$ROOT/src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05}"
REQUIRE_VALID_CANDIDATES="${REQUIRE_VALID_CANDIDATES:-true}"
RUN_FORMAL="${RUN_FORMAL:-false}"
RUN_LLM_INIT="${RUN_LLM_INIT:-false}"
INIT_CANDIDATE_LABEL="${INIT_CANDIDATE_LABEL:-deepseek_init_$STAMP}"
MODEL="${MODEL:-deepseek-v4-flash}"

PROMPT_DIR="${PROMPT_DIR:-$OUT_ROOT/candidate_prompts}"
LLM_INIT_OUT="${LLM_INIT_OUT:-$OUT_ROOT/llm_initial_candidates}"
CANDIDATE_MANIFEST="${CANDIDATE_MANIFEST:-$OUT_ROOT/drc_candidates.json}"
CANDIDATE_MANIFEST_MD="${CANDIDATE_MANIFEST_MD:-$OUT_ROOT/drc_candidates.md}"
FORMAL_OUT="${FORMAL_OUT:-$OUT_ROOT/formal_drc_v5}"
FEEDBACK_OUT="${FEEDBACK_OUT:-$FORMAL_OUT/feedback_prompts}"
REVISION_ROUND_OUT="${REVISION_ROUND_OUT:-$FORMAL_OUT/revision_round}"

mkdir -p "$OUT_ROOT"

echo "[DRC-CONSTRUCT] writing DRC-aware candidate prompts"
"$PY" "$ROOT/scripts/generate_drc_candidate_prompt.py" \
  --maps $RUN_MAPS \
  --out-dir "$PROMPT_DIR"

if [[ "$RUN_LLM_INIT" == "true" ]]; then
  echo "[DRC-CONSTRUCT] calling LLM for initial DRC candidates"
  mkdir -p "$LLM_INIT_OUT"
  for map in $RUN_MAPS; do
    "$PY" "$ROOT/scripts/call_drc_llm_candidate.py" \
      --prompt "$PROMPT_DIR/${map}_drc_candidate_prompt.md" \
      --map "$map" \
      --candidate-root "$CANDIDATE_ROOT" \
      --candidate-label "$INIT_CANDIDATE_LABEL" \
      --metadata-out "$LLM_INIT_OUT/${map}_${INIT_CANDIDATE_LABEL}_metadata.json" \
      --raw-response-out "$LLM_INIT_OUT/${map}_${INIT_CANDIDATE_LABEL}_raw_response.md" \
      --model "$MODEL"
  done
fi

echo "[DRC-CONSTRUCT] freezing candidate manifest"
manifest_args=(
  "$ROOT/scripts/make_drc_candidate_manifest.py"
  --maps $RUN_MAPS
  --candidate-root "$CANDIDATE_ROOT"
  --out-json "$CANDIDATE_MANIFEST"
  --out-md "$CANDIDATE_MANIFEST_MD"
)
if [[ "$REQUIRE_VALID_CANDIDATES" == "true" ]]; then
  manifest_args+=(--require-valid)
fi
"$PY" "${manifest_args[@]}"

cat > "$OUT_ROOT/README.md" <<EOF
# DRC Teacher Construction

- stamp: \`$STAMP\`
- maps: \`$RUN_MAPS\`
- prompt dir: \`$PROMPT_DIR\`
- run LLM init: \`$RUN_LLM_INIT\`
- init candidate label: \`$INIT_CANDIDATE_LABEL\`
- candidate manifest: \`$CANDIDATE_MANIFEST\`
- run formal: \`$RUN_FORMAL\`

## Next Steps

1. Inspect generated prompts.
2. Add or revise candidate \`comm_init.py\` files under each map's candidate directory, or set \`RUN_LLM_INIT=true\` to call DeepSeek.
3. Re-run this script to refresh the candidate manifest.
4. Set \`RUN_FORMAL=true\` and \`BUFFER_ROOT=<formal reward-bearing buffer root>\` to certify candidates.

EOF

if [[ "$RUN_FORMAL" != "true" ]]; then
  cat <<EOF
[DRC-CONSTRUCT] prompt and manifest stages complete.

Artifacts:
  $PROMPT_DIR
  $CANDIDATE_MANIFEST
  $CANDIDATE_MANIFEST_MD

To run formal DRC after candidates and buffers are ready:

  RUN_FORMAL=true \\
  RUN_MAPS="$RUN_MAPS" \\
  CANDIDATE_MANIFEST="$CANDIDATE_MANIFEST" \\
  BUFFER_ROOT=<formal_buffer_root> \\
  bash "$ROOT/scripts/run_drc_teacher_construction.sh"
EOF
  exit 0
fi

echo "[DRC-CONSTRUCT] running formal DRC-v5"
set +e
OUT_ROOT="$FORMAL_OUT" \
CANDIDATE_MANIFEST="$CANDIDATE_MANIFEST" \
RUN_MAPS="$RUN_MAPS" \
bash "$ROOT/scripts/run_formal_drc_v5.sh"
formal_status=$?
set -e

if [[ -d "$FORMAL_OUT/teacher_search" ]]; then
  echo "[DRC-CONSTRUCT] generating DRC-only feedback prompts for failed candidates"
  "$PY" "$ROOT/scripts/generate_drc_feedback_prompt.py" \
    --result "$FORMAL_OUT/teacher_search" \
    --only-failed \
    --out-dir "$FEEDBACK_OUT" || true
  echo "[DRC-CONSTRUCT] generating DRC-guided revision round manifest"
  "$PY" "$ROOT/scripts/generate_drc_revision_round.py" \
    --result "$FORMAL_OUT/teacher_search" \
    --candidate-root "$CANDIDATE_ROOT" \
    --round-label "drc_revision_${STAMP}" \
    --out-dir "$REVISION_ROUND_OUT" || true
fi

if [[ "$formal_status" -ne 0 ]]; then
  echo "[DRC-CONSTRUCT] formal DRC failed with status $formal_status"
  echo "[DRC-CONSTRUCT] inspect: $FORMAL_OUT"
  exit "$formal_status"
fi

echo "[DRC-CONSTRUCT] complete"
echo "Formal artifacts: $FORMAL_OUT"
