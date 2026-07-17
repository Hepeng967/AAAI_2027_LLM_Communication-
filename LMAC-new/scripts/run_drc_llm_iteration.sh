#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"

RESULT_JSON="${RESULT_JSON:-}"
if [[ -z "$RESULT_JSON" ]]; then
  echo "RESULT_JSON must point to a DRC result JSON." >&2
  exit 2
fi

ROUND_LABEL="${ROUND_LABEL:-drc_llm_revision_$(date -u +%Y%m%d_%H%M%S)}"
OUT_ROOT="${OUT_ROOT:-$ROOT/description/certification_gate/$ROUND_LABEL}"
CANDIDATE_ROOT="${CANDIDATE_ROOT:-src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05}"
CANDIDATE_LABEL="${CANDIDATE_LABEL:-$ROUND_LABEL}"
MODEL="${MODEL:-deepseek-v4-flash}"
RUN_LLM="${RUN_LLM:-false}"
RUN_DRC="${RUN_DRC:-false}"
RUN_RL="${RUN_RL:-false}"
BUFFER_ROOT="${BUFFER_ROOT:-$ROOT/data}"
DECISION_LABEL="${DECISION_LABEL:-raw_action}"
CONDITIONAL_DECISION_MODE="${CONDITIONAL_DECISION_MODE:-local_loss}"
PROBE_MODEL="${PROBE_MODEL:-mlp}"
MAX_TRANSITIONS="${MAX_TRANSITIONS:-4096}"
MAX_FILES="${MAX_FILES:-64}"

mkdir -p "$OUT_ROOT"
cd "$ROOT"

FEEDBACK_JSON="$OUT_ROOT/drc_llm_feedback.json"
FEEDBACK_MD="$OUT_ROOT/drc_llm_feedback.md"
PROMPT_MD="$OUT_ROOT/deepseek_revision_prompt.md"
LLM_METADATA="$OUT_ROOT/deepseek_revision_metadata.json"
RAW_RESPONSE="$OUT_ROOT/deepseek_raw_response.md"
COMMANDS="$OUT_ROOT/commands.sh"
README="$OUT_ROOT/README.md"

echo "[DRC-LLM] building structured feedback"
"$PY" scripts/build_drc_llm_feedback.py \
  --result "$RESULT_JSON" \
  --candidate-root "$CANDIDATE_ROOT" \
  --candidate-label "$CANDIDATE_LABEL" \
  --round-label "$ROUND_LABEL" \
  --out-json "$FEEDBACK_JSON" \
  --out-md "$FEEDBACK_MD" \
  > "$OUT_ROOT/build_feedback.stdout"

DESTINATION="$("$PY" - "$FEEDBACK_JSON" <<'PY'
import json
import sys
from pathlib import Path
print(json.loads(Path(sys.argv[1]).read_text())["destination_file"])
PY
)"
MAP_NAME="$("$PY" - "$FEEDBACK_JSON" <<'PY'
import json
import sys
from pathlib import Path
print(json.loads(Path(sys.argv[1]).read_text())["map_name"])
PY
)"

echo "[DRC-LLM] destination candidate: $DESTINATION"
if [[ "$RUN_LLM" == "true" ]]; then
  "$PY" scripts/call_drc_llm_revision.py \
    --feedback-json "$FEEDBACK_JSON" \
    --destination-file "$DESTINATION" \
    --prompt-out "$PROMPT_MD" \
    --raw-response-out "$RAW_RESPONSE" \
    --metadata-out "$LLM_METADATA" \
    --model "$MODEL"
else
  "$PY" scripts/call_drc_llm_revision.py \
    --feedback-json "$FEEDBACK_JSON" \
    --destination-file "$DESTINATION" \
    --prompt-out "$PROMPT_MD" \
    --metadata-out "$LLM_METADATA" \
    --model "$MODEL" \
    --dry-run
fi

cat > "$COMMANDS" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$ROOT"

# 1. If this was a dry run, call DeepSeek to create the candidate.
RUN_LLM=true RESULT_JSON="$RESULT_JSON" OUT_ROOT="$OUT_ROOT" CANDIDATE_LABEL="$CANDIDATE_LABEL" \\
  MODEL="$MODEL" bash scripts/run_drc_llm_iteration.sh

# 2. Freeze the revised candidate into a candidate manifest.
"$PY" scripts/make_drc_candidate_manifest.py \\
  --candidate-root "$CANDIDATE_ROOT" \\
  --maps "$MAP_NAME" \\
  --require-valid \\
  --out-json "$OUT_ROOT/drc_candidates.json" \\
  --out-md "$OUT_ROOT/drc_candidates.md"

# 3. Re-run formal DRC on the generated candidate before using it for RL.
"$PY" scripts/certify_decision_relevant_comm.py \\
  --map "$MAP_NAME" \\
  --comm-code "$DESTINATION" \\
  --buffer-root "$BUFFER_ROOT" \\
  --decision-label "$DECISION_LABEL" \\
  --conditional-decision-mode "$CONDITIONAL_DECISION_MODE" \\
  --probe-model "$PROBE_MODEL" \\
  --max-files "$MAX_FILES" \\
  --max-transitions "$MAX_TRANSITIONS" \\
  --require-content-control \\
  --out-json "$OUT_ROOT/generated_candidate_drc.json" \\
  --out-md "$OUT_ROOT/generated_candidate_drc.md"

# 4. If accepted, select/freeze a teacher manifest and launch fixed-teacher RL validation.
"$PY" scripts/select_drc_teacher.py \\
  --search-root "$OUT_ROOT" \\
  --out-json "$OUT_ROOT/frozen_teacher_manifest.json" \\
  --out-md "$OUT_ROOT/frozen_teacher_manifest.md"

RUN_MAPS="$MAP_NAME" FROZEN_TEACHER_MANIFEST="$OUT_ROOT/frozen_teacher_manifest.json" \\
  RUN_ROOT="$OUT_ROOT/teacher_student_rl" bash scripts/launch_teacher_student_eval.sh
EOF
chmod +x "$COMMANDS"

if [[ "$RUN_DRC" == "true" && -f "$DESTINATION" ]]; then
  echo "[DRC-LLM] running generated candidate DRC"
  "$PY" scripts/certify_decision_relevant_comm.py \
    --map "$MAP_NAME" \
    --comm-code "$DESTINATION" \
    --buffer-root "$BUFFER_ROOT" \
    --decision-label "$DECISION_LABEL" \
    --conditional-decision-mode "$CONDITIONAL_DECISION_MODE" \
    --probe-model "$PROBE_MODEL" \
    --max-files "$MAX_FILES" \
    --max-transitions "$MAX_TRANSITIONS" \
    --require-content-control \
    --out-json "$OUT_ROOT/generated_candidate_drc.json" \
    --out-md "$OUT_ROOT/generated_candidate_drc.md"
fi

if [[ "$RUN_RL" == "true" ]]; then
  if [[ ! -f "$OUT_ROOT/frozen_teacher_manifest.json" ]]; then
    echo "RUN_RL=true requires $OUT_ROOT/frozen_teacher_manifest.json from teacher selection." >&2
    exit 3
  fi
  RUN_MAPS="$MAP_NAME" \
    FROZEN_TEACHER_MANIFEST="$OUT_ROOT/frozen_teacher_manifest.json" \
    RUN_ROOT="$OUT_ROOT/teacher_student_rl" \
    bash scripts/launch_teacher_student_eval.sh
fi

cat > "$README" <<EOF
# DRC-LLM Iteration Run

- result json: \`$RESULT_JSON\`
- map: \`$MAP_NAME\`
- run LLM: \`$RUN_LLM\`
- model: \`$MODEL\`
- structured feedback: \`$FEEDBACK_JSON\`
- feedback md: \`$FEEDBACK_MD\`
- prompt: \`$PROMPT_MD\`
- destination candidate: \`$DESTINATION\`
- command replay: \`$COMMANDS\`

## Research Conclusion

The DRC rollout buffer is part of the estimand. Its policy and quality affect
the oracle, local probe, comm probe, and causal deletion test. Use a fixed,
preregistered shared buffer for candidate comparison, keep held-out splits
disjoint, and validate the final generated teacher with fixed-teacher RL only
after DRC acceptance.

## Iteration Logic

- \`decision_sufficient_feedback\` edits \`communication(o)\`: add decision-relevant message content.
- \`causally_useful_feedback\` edits \`communication_matrix(o)\`: preserve useful sender-receiver edges and prune or condition weak ones.
- \`sender_observable\` and \`receiver_necessary\` remain internal sanity constraints.

## Next Commands

Run \`$COMMANDS\` to reproduce the prompt, DRC recertification, frozen-teacher selection, and RL validation launch.
EOF

echo "[DRC-LLM] wrote run directory: $OUT_ROOT"
echo "[DRC-LLM] replay commands: $COMMANDS"
