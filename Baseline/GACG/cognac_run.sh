#!/usr/bin/env bash
set -u

export TZ="Asia/Shanghai"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-/root/miniconda3/envs/gfootball/bin/python}"
CONFIG="${CONFIG:-gacg}"
METHOD_NAME="${METHOD_NAME:-GACG}"
RUNS_PER_TASK="${RUNS_PER_TASK:-5}"
MAX_PARALLEL="${MAX_PARALLEL:-$RUNS_PER_TASK}"
T_MAX="${T_MAX:-2050000}"
DRY_RUN="${DRY_RUN:-0}"
IFS=',' read -r -a GPU_IDS <<< "${GPU_IDS:-0}"

if (( $# > 0 )); then
  TASKS=("$@")
elif [[ -n "${SELECTED_TASKS:-}" ]]; then
  IFS=',' read -r -a TASKS <<< "$SELECTED_TASKS"
else
  TASKS=("sysadmin_10" "binary_consensus_10" "firefighting_10")
fi

task_config() {
  case "$1" in
    sysadmin_10) echo "cognac_sysadmin_10" ;;
    binary_consensus_10) echo "cognac_binary_consensus_10" ;;
    firefighting_10) echo "cognac_firefighting_10" ;;
    *) echo "Unsupported COGNAC task: $1" >&2; return 2 ;;
  esac
}

preflight() {
  [[ -x "$PYTHON_BIN" ]] || {
    echo "Python runtime is not executable: $PYTHON_BIN" >&2
    return 1
  }
  "$PYTHON_BIN" -c 'import torch_scatter' >/dev/null 2>&1 || {
    echo "GACG requires torch_scatter, but it is missing from PYTHON_BIN=$PYTHON_BIN." >&2
    echo "Install the torch-scatter wheel matching this Python's PyTorch/CUDA build before training." >&2
    return 1
  }
  "$PYTHON_BIN" - "$ROOT_DIR" <<'PY'
import sys
from pathlib import Path

import numpy as np

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "src"))
from envs.cognac_wrapper import COGNACWrapper

specs = {
    "sysadmin_10": (10, 40, 20),
    "binary_consensus_10": (10, 30, 10),
    "firefighting_10": (10, 1, 11),
}
for task, (n_agents, obs_dim, state_dim) in specs.items():
    kwargs = {"task": task, "max_steps": 100, "seed": 1234}
    if task != "firefighting_10":
        kwargs["graph_path"] = root / "src/envs/cognac_assets/basic_directed_network_10.npy"
    env = COGNACWrapper(**kwargs)
    obs, state = env.reset()
    assert len(obs) == n_agents
    assert all(np.asarray(item).shape == (obs_dim,) for item in obs)
    assert np.asarray(state).shape == (state_dim,)
    reward, terminated, info = env.step([0] * n_agents)
    assert isinstance(reward, float)
    assert isinstance(terminated, bool)
    assert isinstance(info, dict)
    env.close()
    print(f"COGNAC preflight PASS: {task} obs={obs_dim} state={state_dim}")
PY
}

if (( ${#GPU_IDS[@]} == 0 )); then
  echo "GPU_IDS must contain at least one GPU id." >&2
  exit 2
fi

LOG_ROOT="${LOG_DIR:-log/cognac}"
mkdir -p "$LOG_ROOT"
SUMMARY_LOG="$LOG_ROOT/experiment_progress.log"
preflight | tee -a "$SUMMARY_LOG" || exit 1
echo "$METHOD_NAME COGNAC experiments started: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$SUMMARY_LOG"

running=0
failed=0
for task in "${TASKS[@]}"; do
  env_config="$(task_config "$task")" || exit 2
  task_log_dir="$LOG_ROOT/$task"
  mkdir -p "$task_log_dir"
  task_log="$task_log_dir/experiment_progress.log"

  for ((run=1; run<=RUNS_PER_TASK; run++)); do
    while (( running >= MAX_PARALLEL )); do
      if ! wait -n; then failed=$((failed + 1)); fi
      running=$((running - 1))
    done

    seed=$((1233 + run))
    gpu="${GPU_IDS[$(((run - 1) % ${#GPU_IDS[@]}))]}"
    stamp="$(date '+%Y%m%d_%H%M%S')"
    output="$task_log_dir/output_${task}_seed_${seed}_${stamp}.log"
    command=(
      "$PYTHON_BIN" -u src/main.py
      "--config=$CONFIG" "--env-config=$env_config" with
      "seed=$seed" "t_max=$T_MAX"
      "name=${METHOD_NAME}_COGNAC"
      "test_nepisode=32" "save_model=False"
    )

    if [[ "$DRY_RUN" == "1" ]]; then
      printf 'DRY RUN CUDA_VISIBLE_DEVICES=%q ' "$gpu" | tee -a "$task_log"
      printf '%q ' "${command[@]}" | tee -a "$task_log"
      printf '\n' | tee -a "$task_log"
      continue
    fi

    echo "Starting method=$METHOD_NAME task=$task seed=$seed gpu=$gpu" | tee -a "$task_log"
    CUDA_VISIBLE_DEVICES="$gpu" nohup setsid "${command[@]}" > "$output" 2>&1 < /dev/null &
    echo "Started PID=$! log=$output" | tee -a "$task_log"
    running=$((running + 1))
  done
done

while (( running > 0 )); do
  if ! wait -n; then failed=$((failed + 1)); fi
  running=$((running - 1))
done

if (( failed > 0 )); then
  echo "$failed $METHOD_NAME COGNAC run(s) failed." | tee -a "$SUMMARY_LOG"
  exit 1
fi
echo "$METHOD_NAME COGNAC experiments finished: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$SUMMARY_LOG"
