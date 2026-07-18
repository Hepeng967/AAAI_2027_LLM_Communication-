#!/usr/bin/env bash
set -u

export TZ="Asia/Shanghai"
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="${PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION:-python}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-/root/miniconda3/envs/gfootball/bin/python}"
CONFIG="${CONFIG:-lmac}"
RUNS_PER_TASK="${RUNS_PER_TASK:-5}"
MAX_PARALLEL="${MAX_PARALLEL:-$RUNS_PER_TASK}"
T_MAX="${T_MAX:-2050000}"
DRY_RUN="${DRY_RUN:-0}"
BATCH_SIZE_OVERRIDE="${BATCH_SIZE_OVERRIDE:-}"
TEST_NEPISODE_OVERRIDE="${TEST_NEPISODE_OVERRIDE:-}"
IFS=',' read -r -a GPU_IDS <<< "${GPU_IDS:-0}"

if (( $# > 0 )); then
  TASKS=("$@")
elif [[ -n "${SELECTED_TASKS:-}" ]]; then
  IFS=',' read -r -a TASKS <<< "$SELECTED_TASKS"
else
  TASKS=("sysadmin_10" "binary_consensus_10" "firefighting_10")
fi

if (( ${#TASKS[@]} == 0 )); then
  echo "No COGNAC tasks selected." >&2
  exit 2
fi
if (( ${#GPU_IDS[@]} == 0 )); then
  echo "GPU_IDS must contain at least one GPU id." >&2
  exit 2
fi

LOG_ROOT="${LOG_DIR:-log/cognac}"
mkdir -p "$LOG_ROOT"
SUMMARY_LOG="$LOG_ROOT/experiment_progress.log"

task_spec() {
  # env-config | agents | raw obs | complete LMAC input | state size
  case "$1" in
    sysadmin_10)        echo 'cognac_sysadmin_10|10|40|52|20' ;;
    binary_consensus_10) echo 'cognac_binary_consensus_10|10|30|42|10' ;;
    firefighting_10)    echo 'cognac_firefighting_10|10|1|13|11' ;;
    *)
      echo "Unsupported COGNAC task: $1" >&2
      return 2
      ;;
  esac
}

check_python_runtime() {
  if [[ ! -x "$PYTHON_BIN" ]]; then
    echo "Python runtime is not executable: $PYTHON_BIN" >&2
    return 1
  fi
  "$PYTHON_BIN" - <<'PY'
missing = []
for package in ("sacred", "torch", "numpy", "gymnasium", "pettingzoo"):
    try:
        __import__(package)
    except Exception as exc:
        missing.append(f"{package}: {type(exc).__name__}: {exc}")
if missing:
    raise SystemExit("Selected PYTHON_BIN is missing required packages:\n  " + "\n  ".join(missing))
print("Python runtime preflight PASS")
PY
}

important_state_for_size() {
  "$PYTHON_BIN" - "$1" <<'PY'
import json
import sys
print(json.dumps(list(range(int(sys.argv[1]))), separators=(",", ":")))
PY
}

preflight_task() {
  "$PYTHON_BIN" - "$1" "$2" "$3" "$4" "$5" "$6" "$ROOT_DIR" <<'PY'
import importlib.util
import sys
from pathlib import Path

import numpy as np
import torch

task = sys.argv[1]
policy = Path(sys.argv[2])
n_agents = int(sys.argv[3])
raw_obs_dim = int(sys.argv[4])
input_dim = int(sys.argv[5])
state_dim = int(sys.argv[6])
root = Path(sys.argv[7])

sys.path.insert(0, str(root / "src"))
from envs.cognac_wrapper import COGNACWrapper

env = COGNACWrapper(
    task=task,
    max_steps=100,
    graph_path=(root / "src/envs/cognac_assets/basic_directed_network_10.npy")
        if task != "firefighting_10" else None,
    seed=1234,
)
obs, state = env.reset()
if len(obs) != n_agents or any(np.asarray(item).shape != (raw_obs_dim,) for item in obs):
    raise SystemExit(f"Invalid environment observations for {task}: {[np.asarray(x).shape for x in obs]}")
if np.asarray(state).shape != (state_dim,):
    raise SystemExit(f"Invalid environment state for {task}: {np.asarray(state).shape}")
step_result = env.step([0] * n_agents)
if len(step_result) != 5:
    raise SystemExit(f"COGNAC wrapper must return a five-tuple, got {len(step_result)} values")
env.close()

spec = importlib.util.spec_from_file_location(f"lmac_original_{task}", policy)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
communication = getattr(module, "communication", None)
if not callable(communication):
    raise SystemExit(f"Original LMAC policy {policy} is missing communication(o)")

for label, inputs in (
    ("zero", torch.zeros(2, n_agents, input_dim)),
    ("random", torch.rand(2, n_agents, input_dim)),
):
    with torch.no_grad():
        output = communication(inputs)
    if not isinstance(output, torch.Tensor) or output.ndim != 3:
        raise SystemExit(f"{label}: communication(o) must return a rank-3 Tensor")
    if output.shape[:2] != inputs.shape[:2] or output.shape[-1] <= input_dim:
        raise SystemExit(
            f"{label}: invalid communication output {tuple(output.shape)} "
            f"for input {tuple(inputs.shape)}"
        )
    if not torch.equal(output[..., :input_dim], inputs):
        raise SystemExit(f"{label}: communication(o) must preserve its input as the output prefix")
    if not torch.isfinite(output).all():
        raise SystemExit(f"{label}: communication(o) returned NaN or Inf")

print(
    f"COGNAC/LMAC preflight PASS: {task} raw_obs={raw_obs_dim} "
    f"input={input_dim} state={state_dim} output={output.shape[-1]} ({policy})"
)
PY
}

wait_for_one() {
  if wait -n; then
    return 0
  fi
  status=$?
  echo "A COGNAC training subprocess failed with exit code $status." | tee -a "$SUMMARY_LOG" >&2
  return "$status"
}

check_python_runtime | tee -a "$SUMMARY_LOG" || exit 1
echo "Original LMAC COGNAC experiments started: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$SUMMARY_LOG"
running=0
failed=0

for TASK in "${TASKS[@]}"; do
  IFS='|' read -r ENV_CONFIG N_AGENTS RAW_OBS_DIM INPUT_DIM STATE_DIM <<< "$(task_spec "$TASK")" || exit 2
  POLICY="$ROOT_DIR/src/llm_source_archive/$TASK/comm_init.py"
  [[ -f "$POLICY" ]] || {
    echo "Missing original LMAC COGNAC policy: $POLICY" >&2
    exit 1
  }
  IMPORTANT_STATE="$(important_state_for_size "$STATE_DIM")" || exit 1

  TASK_LOG_DIR="$LOG_ROOT/$TASK"
  mkdir -p "$TASK_LOG_DIR"
  TASK_LOG="$TASK_LOG_DIR/experiment_progress.log"
  preflight_task "$TASK" "$POLICY" "$N_AGENTS" "$RAW_OBS_DIM" "$INPUT_DIM" "$STATE_DIM" \
    | tee -a "$TASK_LOG" || exit 1
  echo "Resolved COGNAC env config: $TASK -> $ENV_CONFIG" | tee -a "$TASK_LOG"
  echo "Resolved original LMAC policy: $TASK -> $POLICY" | tee -a "$TASK_LOG"
  echo "Resolved complete centralized state selection: $IMPORTANT_STATE" | tee -a "$TASK_LOG"

  for ((run=1; run<=RUNS_PER_TASK; run++)); do
    while (( running >= MAX_PARALLEL )); do
      if ! wait_for_one; then failed=$((failed + 1)); fi
      running=$((running - 1))
    done

    seed=$((1233 + run))
    gpu="${GPU_IDS[$(((run - 1) % ${#GPU_IDS[@]}))]}"
    stamp="$(date '+%Y%m%d_%H%M%S')"
    output="$TASK_LOG_DIR/output_${TASK}_seed_${seed}_${stamp}.log"
    command=(
      "$PYTHON_BIN" -u src/main_llm_final.py
      "--config=$CONFIG" "--env-config=$ENV_CONFIG" with
      "seed=$seed" "t_max=$T_MAX"
      "name=LMAC_ORIGINAL_COGNAC"
      "running_algorithm_name=(${TASK})LMAC_ORIGINAL_COGNAC"
      "comm_code_paths=['${POLICY}']"
      "important_state=${IMPORTANT_STATE}"
      "phase=multi_train" "use_wandb=False"
      "use_tensorboard=True" "save_model=False"
    )
    [[ -z "$BATCH_SIZE_OVERRIDE" ]] || command+=("batch_size=$BATCH_SIZE_OVERRIDE")
    [[ -z "$TEST_NEPISODE_OVERRIDE" ]] || command+=("test_nepisode=$TEST_NEPISODE_OVERRIDE")

    echo "Starting task=$TASK seed=$seed gpu=$gpu policy=$POLICY" | tee -a "$TASK_LOG"
    if [[ "$DRY_RUN" == "1" ]]; then
      printf 'DRY RUN CUDA_VISIBLE_DEVICES=%q ' "$gpu" | tee -a "$TASK_LOG"
      printf '%q ' "${command[@]}" | tee -a "$TASK_LOG"
      printf '\n' | tee -a "$TASK_LOG"
      continue
    fi

    CUDA_VISIBLE_DEVICES="$gpu" nohup setsid "${command[@]}" > "$output" 2>&1 < /dev/null &
    echo "Started PID=$! log=$output" | tee -a "$TASK_LOG"
    running=$((running + 1))
  done
done

while (( running > 0 )); do
  if ! wait_for_one; then failed=$((failed + 1)); fi
  running=$((running - 1))
done

if (( failed > 0 )); then
  echo "$failed original LMAC COGNAC run(s) failed." | tee -a "$SUMMARY_LOG"
  exit 1
fi
echo "Original LMAC COGNAC experiments finished: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$SUMMARY_LOG"
