#!/usr/bin/env bash
set -u

export TZ="Asia/Shanghai"
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="${PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION:-python}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-/root/miniconda3/envs/gfootball/bin/python}"
RUNS_PER_TASK="${RUNS_PER_TASK:-5}"
MAX_PARALLEL="${MAX_PARALLEL:-$RUNS_PER_TASK}"
T_MAX="${T_MAX:-5050000}"
DRY_RUN="${DRY_RUN:-0}"
BATCH_SIZE_OVERRIDE="${BATCH_SIZE_OVERRIDE:-}"
TEST_NEPISODE_OVERRIDE="${TEST_NEPISODE_OVERRIDE:-}"
IFS=',' read -r -a GPU_IDS <<< "${GPU_IDS:-0}"
if (( $# > 0 )); then
  TASKS=("$@")
else
  TASKS=(academy_3_vs_1_with_keeper academy_run_pass_and_shoot_with_keeper)
fi

LOG_ROOT="${LOG_DIR:-log/grf}"
mkdir -p "$LOG_ROOT"
SUMMARY_LOG="$LOG_ROOT/experiment_progress.log"

task_spec() {
  case "$1" in
    academy_3_vs_1_with_keeper) echo '3|48|[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]' ;;
    academy_run_pass_and_shoot_with_keeper) echo '2|43|[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]' ;;
    *) echo "Unsupported GRF task: $1" >&2; return 2 ;;
  esac
}

preflight() {
  "$PYTHON_BIN" - "$1" "$2" "$3" "$4" <<'PY'
import importlib.util, sys
from pathlib import Path
import torch
task, policy, n_agents, input_dim = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
spec = importlib.util.spec_from_file_location(f"lmac_{task}", policy)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
x = torch.zeros(2, n_agents, input_dim); y = module.communication(x)
if y.ndim != 3 or y.shape[:2] != x.shape[:2] or y.shape[-1] <= input_dim:
    raise SystemExit(f"Invalid communication output {tuple(y.shape)} for input {tuple(x.shape)}")
print(f"Original LMAC policy PASS: {task} input={tuple(x.shape)} output={tuple(y.shape)}")
PY
}

echo "GRF experiments started: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$SUMMARY_LOG"
running=0
failed=0

for TASK in "${TASKS[@]}"; do
  IFS='|' read -r N_AGENTS INPUT_DIM IMPORTANT_STATE <<< "$(task_spec "$TASK")" || exit 2
  POLICY="$ROOT_DIR/src/llm_source_archive/$TASK/comm_init.py"
  [[ -f "$POLICY" ]] || { echo "Missing original LMAC policy: $POLICY" >&2; exit 1; }
  TASK_LOG_DIR="$LOG_ROOT/$TASK"
  mkdir -p "$TASK_LOG_DIR"
  TASK_LOG="$TASK_LOG_DIR/experiment_progress.log"
  preflight "$TASK" "$POLICY" "$N_AGENTS" "$INPUT_DIM" | tee -a "$TASK_LOG" || exit 1

  for ((run=1; run<=RUNS_PER_TASK; run++)); do
    while (( running >= MAX_PARALLEL )); do
      if ! wait -n; then failed=$((failed + 1)); fi
      running=$((running - 1))
    done
    seed=$((1233 + run))
    gpu="${GPU_IDS[$(((run - 1) % ${#GPU_IDS[@]}))]}"
    stamp="$(date '+%Y%m%d_%H%M%S')"
    output="$TASK_LOG_DIR/output_${TASK}_seed_${seed}_${stamp}.log"
    command=(
      "$PYTHON_BIN" -u src/main_llm_final.py --config=lmac --env-config=grf with
      "env_args.map_name=$TASK" "seed=$seed" "t_max=$T_MAX" "name=LMAC_ORIGINAL_GRF"
      "running_algorithm_name=(${TASK})LMAC_ORIGINAL"
      "comm_code_paths=['${POLICY}']" "important_state=${IMPORTANT_STATE}"
      "phase=multi_train" "use_wandb=False" "use_tensorboard=True" "save_model=False"
    )
    [[ -z "$BATCH_SIZE_OVERRIDE" ]] || command+=("batch_size=$BATCH_SIZE_OVERRIDE")
    [[ -z "$TEST_NEPISODE_OVERRIDE" ]] || command+=("test_nepisode=$TEST_NEPISODE_OVERRIDE")
    echo "Starting task=$TASK seed=$seed gpu=$gpu policy=$POLICY" | tee -a "$TASK_LOG"
    if [[ "$DRY_RUN" == 1 ]]; then
      printf 'DRY RUN CUDA_VISIBLE_DEVICES=%q ' "$gpu" | tee -a "$TASK_LOG"
      printf '%q ' "${command[@]}" | tee -a "$TASK_LOG"; printf '\n' | tee -a "$TASK_LOG"
      continue
    fi
    CUDA_VISIBLE_DEVICES="$gpu" nohup setsid "${command[@]}" >"$output" 2>&1 < /dev/null &
    echo "Started PID=$! log=$output" | tee -a "$TASK_LOG"
    running=$((running + 1))
  done
done

while (( running > 0 )); do
  if ! wait -n; then failed=$((failed + 1)); fi
  running=$((running - 1))
done
(( failed == 0 )) || { echo "$failed GRF run(s) failed." | tee -a "$SUMMARY_LOG"; exit 1; }
echo "GRF experiments finished: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$SUMMARY_LOG"
