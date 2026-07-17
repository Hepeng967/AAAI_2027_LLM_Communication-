#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"

MAP_NAME="${MAP_NAME:-}"
COMM_CODE="${COMM_CODE:-}"
if [[ -z "$MAP_NAME" || -z "$COMM_CODE" ]]; then
  echo "MAP_NAME and COMM_CODE are required." >&2
  echo "Example: MAP_NAME=5z_vs_1ul COMM_CODE=src/llm_source/.../comm_init.py bash scripts/validate_generated_teacher_pipeline.sh" >&2
  exit 2
fi

STAMP="${STAMP:-$(date -u +%Y%m%d_%H%M%S)}"
OUT_ROOT="${OUT_ROOT:-$ROOT/description/certification_gate/generated_teacher_validation_$STAMP}"
BUFFER_ROOT="${BUFFER_ROOT:-$ROOT/data}"
RUN_DRC="${RUN_DRC:-false}"
RUN_RL="${RUN_RL:-false}"
DECISION_LABEL="${DECISION_LABEL:-raw_action}"
CONDITIONAL_DECISION_MODE="${CONDITIONAL_DECISION_MODE:-local_loss}"
PROBE_MODEL="${PROBE_MODEL:-mlp}"
MAX_TRANSITIONS="${MAX_TRANSITIONS:-4096}"
MAX_FILES="${MAX_FILES:-64}"
REQUIRE_CONTENT_CONTROL="${REQUIRE_CONTENT_CONTROL:-true}"
REQUIRE_STAT_SIGNIFICANCE="${REQUIRE_STAT_SIGNIFICANCE:-false}"

mkdir -p "$OUT_ROOT"
cd "$ROOT"

VALIDATION_JSON="$OUT_ROOT/interface_validation.json"
DRC_JSON="$OUT_ROOT/generated_teacher_drc.json"
DRC_MD="$OUT_ROOT/generated_teacher_drc.md"
MANIFEST_JSON="$OUT_ROOT/frozen_teacher_manifest.json"
MANIFEST_MD="$OUT_ROOT/frozen_teacher_manifest.md"
RL_PLAN_MD="$OUT_ROOT/teacher_student_rl_plan.md"
COMMANDS="$OUT_ROOT/commands.sh"
README="$OUT_ROOT/README.md"

echo "[GEN-TEACHER] validating teacher interface"
"$PY" scripts/validate_drc_comm_code.py \
  --map "$MAP_NAME" \
  --comm-code "$COMM_CODE" \
  --out-json "$VALIDATION_JSON" \
  > "$OUT_ROOT/interface_validation.stdout"

content_arg=()
if [[ "$REQUIRE_CONTENT_CONTROL" == "true" ]]; then
  content_arg=(--require-content-control)
fi
stat_arg=()
if [[ "$REQUIRE_STAT_SIGNIFICANCE" == "true" ]]; then
  stat_arg=(--require-stat-significance)
fi

cat > "$COMMANDS" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$ROOT"

"$PY" scripts/validate_drc_comm_code.py \\
  --map "$MAP_NAME" \\
  --comm-code "$COMM_CODE" \\
  --out-json "$VALIDATION_JSON"

"$PY" scripts/certify_decision_relevant_comm.py \\
  --map "$MAP_NAME" \\
  --comm-code "$COMM_CODE" \\
  --buffer-root "$BUFFER_ROOT" \\
  --decision-label "$DECISION_LABEL" \\
  --conditional-decision-mode "$CONDITIONAL_DECISION_MODE" \\
  --probe-model "$PROBE_MODEL" \\
  --max-files "$MAX_FILES" \\
  --max-transitions "$MAX_TRANSITIONS" \\
  ${content_arg[*]} ${stat_arg[*]} \\
  --out-json "$DRC_JSON" \\
  --out-md "$DRC_MD"

"$PY" scripts/select_drc_teacher.py \\
  --search-root "$OUT_ROOT" \\
  --out-json "$MANIFEST_JSON" \\
  --out-md "$MANIFEST_MD"

"$PY" scripts/plan_teacher_student_from_manifest.py \\
  --manifest "$MANIFEST_JSON" \\
  --out-md "$RL_PLAN_MD"

RUN_MAPS="$MAP_NAME" FROZEN_TEACHER_MANIFEST="$MANIFEST_JSON" \\
  RUN_ROOT="$OUT_ROOT/teacher_student_rl" bash scripts/launch_teacher_student_eval.sh
EOF
chmod +x "$COMMANDS"

if [[ "$RUN_DRC" == "true" ]]; then
  echo "[GEN-TEACHER] running DRC recertification"
  "$PY" scripts/certify_decision_relevant_comm.py \
    --map "$MAP_NAME" \
    --comm-code "$COMM_CODE" \
    --buffer-root "$BUFFER_ROOT" \
    --decision-label "$DECISION_LABEL" \
    --conditional-decision-mode "$CONDITIONAL_DECISION_MODE" \
    --probe-model "$PROBE_MODEL" \
    --max-files "$MAX_FILES" \
    --max-transitions "$MAX_TRANSITIONS" \
    "${content_arg[@]}" "${stat_arg[@]}" \
    --out-json "$DRC_JSON" \
    --out-md "$DRC_MD"

  "$PY" scripts/select_drc_teacher.py \
    --search-root "$OUT_ROOT" \
    --out-json "$MANIFEST_JSON" \
    --out-md "$MANIFEST_MD"

  "$PY" scripts/plan_teacher_student_from_manifest.py \
    --manifest "$MANIFEST_JSON" \
    --out-md "$RL_PLAN_MD"
fi

if [[ "$RUN_RL" == "true" ]]; then
  if [[ ! -f "$MANIFEST_JSON" ]]; then
    echo "RUN_RL=true requires RUN_DRC=true first, or an existing frozen manifest at $MANIFEST_JSON." >&2
    exit 3
  fi
  RUN_MAPS="$MAP_NAME" \
    FROZEN_TEACHER_MANIFEST="$MANIFEST_JSON" \
    RUN_ROOT="$OUT_ROOT/teacher_student_rl" \
    bash scripts/launch_teacher_student_eval.sh
fi

cat > "$README" <<EOF
# Generated Teacher Validation Pipeline

- map: \`$MAP_NAME\`
- comm code: \`$COMM_CODE\`
- interface validation: \`$VALIDATION_JSON\`
- run DRC: \`$RUN_DRC\`
- run RL: \`$RUN_RL\`
- DRC json: \`$DRC_JSON\`
- frozen manifest: \`$MANIFEST_JSON\`
- RL plan: \`$RL_PLAN_MD\`
- replay commands: \`$COMMANDS\`

This wrapper is the fixed-teacher handoff after LLM initialization or DRC-guided
revision. The generated teacher must pass interface validation, then DRC
recertification, then frozen-teacher RL validation.
EOF

echo "[GEN-TEACHER] wrote validation directory: $OUT_ROOT"
echo "[GEN-TEACHER] replay commands: $COMMANDS"
