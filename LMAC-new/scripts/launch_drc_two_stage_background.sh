#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAMP="${STAMP:-$(date -u +%Y%m%d_%H%M%S)}"
OUT_ROOT="${OUT_ROOT:-$ROOT/description/certification_gate/drc_two_stage_full_$STAMP}"
LOG_DIR="${LOG_DIR:-$OUT_ROOT/logs}"
LOG_FILE="${LOG_FILE:-$LOG_DIR/two_stage_execute.log}"
PID_FILE="${PID_FILE:-$OUT_ROOT/two_stage_execute.pid}"
ENV_FILE="${ENV_FILE:-$OUT_ROOT/two_stage_execute.env}"

mkdir -p "$OUT_ROOT" "$LOG_DIR"

export RUN_MODE="${RUN_MODE:-execute}"
export COLLECT_BUFFERS="${COLLECT_BUFFERS:-true}"
export BUFFER_ROOT="${BUFFER_ROOT:-$OUT_ROOT/formal_buffers}"
export TRAIN_COUNT="${TRAIN_COUNT:-64}"
export TEST_COUNT="${TEST_COUNT:-64}"
export COLLECT_CHUNK_SIZE="${COLLECT_CHUNK_SIZE:-8}"
export OVERWRITE_OUTPUT="${OVERWRITE_OUTPUT:-false}"
export MAX_FILES="${MAX_FILES:-64}"
export AUDIT_MAX_FILES="${AUDIT_MAX_FILES:-64}"
export MAX_TRANSITIONS="${MAX_TRANSITIONS:-4096}"
export PROBE_EPOCHS="${PROBE_EPOCHS:-120}"
export N_BOOTSTRAP="${N_BOOTSTRAP:-500}"
export N_SIGN_PERMUTATIONS="${N_SIGN_PERMUTATIONS:-500}"
export N_MESSAGE_SHUFFLES="${N_MESSAGE_SHUFFLES:-16}"
export SCORE_GAIN_CAP="${SCORE_GAIN_CAP:-1.0}"
export CANDIDATE_MANIFEST="${CANDIDATE_MANIFEST:-$ROOT/description/certification_gate/drc_candidates_with_masked_pruned_20260625_031450.json}"
export CANDIDATE_MANIFEST_MD="${CANDIDATE_MANIFEST_MD:-$ROOT/description/certification_gate/drc_candidates_with_masked_pruned_20260625_031450.md}"
export OUT_ROOT

if [[ -f "$PID_FILE" ]]; then
  old_pid="$(cat "$PID_FILE")"
  if [[ -n "$old_pid" ]] && kill -0 "$old_pid" 2>/dev/null; then
    echo "Existing DRC two-stage run is still active: pid=$old_pid" >&2
    echo "PID file: $PID_FILE" >&2
    exit 1
  fi
fi

cat > "$ENV_FILE" <<EOF
RUN_MODE=$RUN_MODE
COLLECT_BUFFERS=$COLLECT_BUFFERS
BUFFER_ROOT=$BUFFER_ROOT
TRAIN_COUNT=$TRAIN_COUNT
TEST_COUNT=$TEST_COUNT
COLLECT_CHUNK_SIZE=$COLLECT_CHUNK_SIZE
OVERWRITE_OUTPUT=$OVERWRITE_OUTPUT
MAX_FILES=$MAX_FILES
AUDIT_MAX_FILES=$AUDIT_MAX_FILES
MAX_TRANSITIONS=$MAX_TRANSITIONS
PROBE_EPOCHS=$PROBE_EPOCHS
N_BOOTSTRAP=$N_BOOTSTRAP
N_SIGN_PERMUTATIONS=$N_SIGN_PERMUTATIONS
N_MESSAGE_SHUFFLES=$N_MESSAGE_SHUFFLES
SCORE_GAIN_CAP=$SCORE_GAIN_CAP
CANDIDATE_MANIFEST=$CANDIDATE_MANIFEST
CANDIDATE_MANIFEST_MD=$CANDIDATE_MANIFEST_MD
OUT_ROOT=$OUT_ROOT
LOG_FILE=$LOG_FILE
EOF

launcher_cmd='
  set +e
  cd "$1"
  if [[ "$2" == "true" ]]; then
    bash -x "$1/scripts/run_drc_two_stage_evidence_pipeline.sh"
  else
    bash "$1/scripts/run_drc_two_stage_evidence_pipeline.sh"
  fi
  status=$?
  echo "[DRC-LAUNCHER] finished with status ${status}"
  exit "$status"
'

if command -v setsid >/dev/null 2>&1; then
  setsid bash -c "$launcher_cmd" \
    launch_drc_two_stage_background "$ROOT" "${TRACE:-false}" > "$LOG_FILE" 2>&1 &
else
  nohup bash -c "$launcher_cmd" \
    launch_drc_two_stage_background "$ROOT" "${TRACE:-false}" > "$LOG_FILE" 2>&1 &
fi

pid="$!"
echo "$pid" > "$PID_FILE"

cat <<EOF
Started DRC two-stage evidence run.
PID: $pid
PID file: $PID_FILE
Log: $LOG_FILE
Env: $ENV_FILE
Output root: $OUT_ROOT
EOF
