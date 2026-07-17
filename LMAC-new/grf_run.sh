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
T_MAX="${T_MAX:-5050000}"
DRY_RUN="${DRY_RUN:-0}"
IFS=',' read -r -a GPU_IDS <<< "${GPU_IDS:-1}"

if (( $# > 0 )); then
  TASKS=("$@")
elif [[ -n "${SELECTED_TASKS:-}" ]]; then
  IFS=',' read -r -a TASKS <<< "$SELECTED_TASKS"
else
  TASKS=("academy_3_vs_1_with_keeper" "academy_run_pass_and_shoot_with_keeper")
fi

LOG_DIR="${LOG_DIR:-log/grf}"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/experiment_progress.log"

task_spec() {
  case "$1" in
    academy_3_vs_1_with_keeper)
      echo '3|48|[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]'
      ;;
    academy_run_pass_and_shoot_with_keeper)
      echo '2|43|[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]'
      ;;
    *) echo "Unsupported GRF task: $1" >&2; return 2 ;;
  esac
}

resolve_latest_teacher() {
  "$PYTHON_BIN" - "$1" "$ROOT_DIR" <<'PY'
import hashlib, json, sys
from pathlib import Path

task, root = sys.argv[1], Path(sys.argv[2])
runs = root / "src/LLM-Communication-main/pipeline_runs/grf" / task
stable = root / "src/LLM-Communication-main/matrix_code/grf" / task / "LMAC_WWW/comm_init.py"
for run in sorted((p for p in runs.glob("*") if p.is_dir()), reverse=True):
    status_path = run / "pipeline_status.json"
    if not status_path.is_file():
        continue
    status = json.loads(status_path.read_text())
    iteration = status.get("iteration", {})
    if status.get("overall") != "complete" or iteration.get("status") != "accepted":
        continue
    manifest_path = Path(iteration.get("frozen_manifest") or "")
    selected = Path(status.get("selected_policy") or "")
    if not manifest_path.is_file() or not selected.is_file() or not stable.is_file():
        continue
    manifest = json.loads(manifest_path.read_text())
    teacher = Path(manifest.get("teachers", {}).get(task, {}).get("teacher_path") or "")
    if not teacher.is_file():
        continue
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    if len({digest(teacher), digest(selected), digest(stable)}) != 1:
        raise SystemExit(
            f"Latest teacher mismatch for {task}: frozen={teacher}, selected={selected}, stable={stable}"
        )
    print(teacher.resolve())
    raise SystemExit(0)
raise SystemExit(f"No consistent accepted frozen teacher found under {runs}")
PY
}

preflight_teacher() {
  "$PYTHON_BIN" - "$1" "$2" "$3" "$4" <<'PY'
import importlib.util, sys
from pathlib import Path
import torch

task, path, n_agents, obs_dim = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
spec = importlib.util.spec_from_file_location(f"teacher_{task}", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
required = ("communication_who", "communication_when", "communication_what")
missing = [name for name in required if not callable(getattr(module, name, None))]
if missing:
    raise SystemExit(f"Teacher is missing functions: {missing}")
obs = torch.zeros(2, n_agents, obs_dim)
with torch.no_grad():
    who, when, what = (getattr(module, name)(obs) for name in required)
expected_matrix = (2, n_agents, n_agents)
if tuple(who.shape) != expected_matrix or tuple(when.shape) != expected_matrix:
    raise SystemExit(f"Invalid WHO/WHEN shapes: {tuple(who.shape)} / {tuple(when.shape)}")
if tuple(what.shape) != tuple(obs.shape):
    raise SystemExit(f"Invalid WHAT shape: {tuple(what.shape)} != {tuple(obs.shape)}")
for name, value in (("WHO", who), ("WHEN", when), ("WHAT", what)):
    if not torch.isfinite(value).all() or value.min() < 0 or value.max() > 1:
        raise SystemExit(f"{name} must contain finite values in [0,1]")
diag = torch.arange(n_agents)
if who[:, diag, diag].abs().max() > 1e-6 or when[:, diag, diag].abs().max() > 1e-6:
    raise SystemExit("WHO/WHEN self-communication diagonal must be zero")
print(f"Teacher preflight PASS: {task} n_agents={n_agents} obs_dim={obs_dim} ({path})")
PY
}

echo "GRF experiments started: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
running=0
failed=0

for TASK in "${TASKS[@]}"; do
  TASK_LOG_DIR="$LOG_DIR/$TASK"
  mkdir -p "$TASK_LOG_DIR"
  TASK_LOG_FILE="$TASK_LOG_DIR/experiment_progress.log"
  IFS='|' read -r N_AGENTS OBS_DIM IMPORTANT_STATE <<< "$(task_spec "$TASK")" || exit 2
  TEACHER_PATH="$(resolve_latest_teacher "$TASK")" || exit 1
  preflight_teacher "$TASK" "$TEACHER_PATH" "$N_AGENTS" "$OBS_DIM" | tee -a "$TASK_LOG_FILE" || exit 1
  echo "Resolved latest accepted teacher: $TASK -> $TEACHER_PATH" | tee -a "$TASK_LOG_FILE"

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
      "--config=$CONFIG" "--env-config=grf" with
      "env_args.map_name=$TASK" "seed=$seed" "t_max=$T_MAX"
      "name=LMAC_LLM_WWW_GRF" "running_algorithm_name=(${TASK})LMAC_LLM_WWW_GRF"
      "comm_code_paths=['${TEACHER_PATH}']" "important_state=${IMPORTANT_STATE}"
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
(( failed == 0 )) || { echo "$failed GRF run(s) failed." | tee -a "$LOG_FILE"; exit 1; }
echo "All GRF experiments finished: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
