#!/usr/bin/env bash
set -u

export TZ="Asia/Shanghai"
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="${PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION:-python}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# The base environment used to generate a teacher does not contain Sacred.
# gfootball is the existing LMAC runtime environment and contains the PyMARL
# dependencies needed by main_llm_final.py and the COGNAC wrapper.
PYTHON_BIN="${PYTHON_BIN:-/root/miniconda3/envs/gfootball/bin/python}"
CONFIG="${CONFIG:-lmac}"
RUNS_PER_TASK="${RUNS_PER_TASK:-3}"
MAX_PARALLEL="${MAX_PARALLEL:-$RUNS_PER_TASK}"
T_MAX="${T_MAX:-2050000}"
DRY_RUN="${DRY_RUN:-0}"
IFS=',' read -r -a GPU_IDS <<< "${GPU_IDS:-1}"

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

LOG_DIR="${LOG_DIR:-log/cognac}"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/experiment_progress.log"

task_spec() {
  # env-config | agents | complete LMAC input dim | centralized state indices
  case "$1" in
    sysadmin_10)
      echo 'cognac_sysadmin_10|10|52|[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]'
      ;;
    binary_consensus_10)
      echo 'cognac_binary_consensus_10|10|42|[0,1,2,3,4,5,6,7,8,9]'
      ;;
    firefighting_10)
      echo 'cognac_firefighting_10|10|13|[0,1,2,3,4,5,6,7,8,9,10]'
      ;;
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

resolve_latest_teacher() {
  "$PYTHON_BIN" - "$1" "$ROOT_DIR" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

task, root = sys.argv[1], Path(sys.argv[2])
runs = root / "src/LLM-Communication-main/pipeline_runs/cognac" / task
stable = root / "src/LLM-Communication-main/matrix_code/cognac" / task / "LMAC_WWW/comm_init.py"

def localize(raw_path):
    """Resolve archived absolute paths inside the current checkout."""
    path = Path(raw_path or "")
    marker = ("src", "LLM-Communication-main")
    parts = path.parts
    for index in range(len(parts) - len(marker) + 1):
        if parts[index:index + len(marker)] == marker:
            local = root.joinpath(*parts[index:])
            if local.is_file():
                return local
    return path

for run in sorted((p for p in runs.glob("*") if p.is_dir()), reverse=True):
    status_path = run / "pipeline_status.json"
    if not status_path.is_file():
        continue
    status = json.loads(status_path.read_text(encoding="utf-8"))
    iteration = status.get("iteration", {})
    if status.get("overall") != "complete" or iteration.get("status") != "accepted":
        continue
    manifest_path = localize(iteration.get("frozen_manifest"))
    selected = localize(status.get("selected_policy"))
    if not manifest_path.is_file() or not selected.is_file() or not stable.is_file():
        continue
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    teacher = localize(manifest.get("teachers", {}).get(task, {}).get("teacher_path"))
    if not teacher.is_file():
        continue
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    if len({digest(teacher), digest(selected), digest(stable)}) != 1:
        raise SystemExit(
            f"Accepted teacher mismatch for {task}: frozen={teacher}, "
            f"selected={selected}, stable={stable}"
        )
    print(teacher.resolve())
    raise SystemExit(0)

raise SystemExit(
    f"No consistent accepted frozen teacher found under {runs}. "
    "A generated-only or failed pipeline run is deliberately not used for RL."
)
PY
}

preflight_teacher() {
  "$PYTHON_BIN" - "$1" "$2" "$3" "$4" <<'PY'
import importlib.util
import sys
from pathlib import Path

import torch

task = sys.argv[1]
path = Path(sys.argv[2])
n_agents = int(sys.argv[3])
obs_dim = int(sys.argv[4])
spec = importlib.util.spec_from_file_location(f"cognac_teacher_{task}", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

required = ("communication_who", "communication_when", "communication_what")
missing = [name for name in required if not callable(getattr(module, name, None))]
if missing:
    raise SystemExit(f"Teacher {path} is missing functions: {missing}")

# Use both zero and random observations. The latter catches policies whose
# conditional branches produce invalid shapes or values only when activated.
for label, obs in (
    ("zero", torch.zeros(2, n_agents, obs_dim)),
    ("random", torch.rand(2, n_agents, obs_dim)),
):
    with torch.no_grad():
        who = module.communication_who(obs)
        when = module.communication_when(obs)
        what = module.communication_what(obs)
    expected_edges = (2, n_agents, n_agents)
    if tuple(who.shape) != expected_edges or tuple(when.shape) != expected_edges:
        raise SystemExit(
            f"{label} input produced invalid WHO/WHEN shapes: "
            f"{tuple(who.shape)} / {tuple(when.shape)}; expected {expected_edges}"
        )
    if tuple(what.shape) != tuple(obs.shape):
        raise SystemExit(
            f"{label} input produced invalid WHAT shape: {tuple(what.shape)}; "
            f"expected {tuple(obs.shape)}"
        )
    for name, value in (("WHO", who), ("WHEN", when), ("WHAT", what)):
        if not torch.isfinite(value).all() or (value < 0).any() or (value > 1).any():
            raise SystemExit(f"{label} input: {name} must contain finite values in [0,1]")
    diagonal = torch.arange(n_agents)
    if who[:, diagonal, diagonal].abs().max() > 1e-6:
        raise SystemExit(f"{label} input: WHO self-communication diagonal must be zero")
    if when[:, diagonal, diagonal].abs().max() > 1e-6:
        raise SystemExit(f"{label} input: WHEN self-communication diagonal must be zero")

print(f"Teacher preflight PASS: {task} n_agents={n_agents} obs_dim={obs_dim} ({path})")
PY
}

check_python_runtime | tee -a "$LOG_FILE" || exit 1
echo "COGNAC experiments started: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
running=0
failed=0

for TASK in "${TASKS[@]}"; do
  TASK_LOG_DIR="$LOG_DIR/$TASK"
  mkdir -p "$TASK_LOG_DIR"
  TASK_LOG_FILE="$TASK_LOG_DIR/experiment_progress.log"
  IFS='|' read -r ENV_CONFIG N_AGENTS OBS_DIM IMPORTANT_STATE <<< "$(task_spec "$TASK")" || exit 2

  TEACHER_PATH="$(resolve_latest_teacher "$TASK")" || exit 1
  preflight_teacher "$TASK" "$TEACHER_PATH" "$N_AGENTS" "$OBS_DIM" \
    | tee -a "$TASK_LOG_FILE" || exit 1
  echo "Resolved COGNAC env config: $TASK -> $ENV_CONFIG" | tee -a "$TASK_LOG_FILE"
  echo "Resolved accepted frozen teacher: $TASK -> $TEACHER_PATH" | tee -a "$TASK_LOG_FILE"

  for ((iteration=1; iteration<=RUNS_PER_TASK; iteration++)); do
    while (( running >= MAX_PARALLEL )); do
      if ! wait -n; then failed=$((failed + 1)); fi
      running=$((running - 1))
    done

    gpu="${GPU_IDS[$(((iteration - 1) % ${#GPU_IDS[@]}))]}"
    seed=$((1233 + iteration))
    stamp="$(date '+%Y%m%d_%H%M%S')"
    output="$TASK_LOG_DIR/output_${TASK}_seed_${seed}_${stamp}.log"
    command=(
      "$PYTHON_BIN" -u src/main_llm_final.py
      "--config=$CONFIG" "--env-config=$ENV_CONFIG" with
      "seed=$seed" "t_max=$T_MAX"
      "name=LMAC_LLM_WWW_COGNAC"
      "running_algorithm_name=(${TASK})LMAC_LLM_WWW_COGNAC"
      "comm_code_paths=['${TEACHER_PATH}']"
      "important_state=${IMPORTANT_STATE}"
      "phase=multi_train" "tmp2=True" "use_wandb=False"
      "use_tensorboard=True" "save_model=False"
    )

    if [[ "$DRY_RUN" == "1" ]]; then
      printf 'DRY RUN CUDA_VISIBLE_DEVICES=%q ' "$gpu" | tee -a "$TASK_LOG_FILE"
      printf '%q ' "${command[@]}" | tee -a "$TASK_LOG_FILE"
      printf '\n' | tee -a "$TASK_LOG_FILE"
      continue
    fi

    echo "Starting task=$TASK seed=$seed gpu=$gpu teacher=$TEACHER_PATH" | tee -a "$TASK_LOG_FILE"
    CUDA_VISIBLE_DEVICES="$gpu" nohup setsid "${command[@]}" > "$output" 2>&1 < /dev/null &
    echo "Started PID=$! log=$output" | tee -a "$TASK_LOG_FILE"
    running=$((running + 1))
  done
done

while (( running > 0 )); do
  if ! wait -n; then failed=$((failed + 1)); fi
  running=$((running - 1))
done

if (( failed > 0 )); then
  echo "$failed COGNAC run(s) failed." | tee -a "$LOG_FILE"
  exit 1
fi
echo "All COGNAC experiments finished: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
