#!/usr/bin/env bash
set -u

export TZ="Asia/Shanghai"
export SC2PATH="${SC2PATH:-/data/hp/3rdparty/StarCraftII}"
# tensorboard_logger ships legacy generated protobuf classes. Use protobuf's
# compatible Python implementation instead of requiring TensorFlow or
# downgrading protobuf for the whole SMAC environment.
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="${PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION:-python}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-/home/hp/anaconda3/envs/SMAC/bin/python}"
CONFIG="${CONFIG:-lmac}"
RUNS_PER_MAP="${RUNS_PER_MAP:-5}"
# By default launch all seeds for one map concurrently. Override
# MAX_PARALLEL explicitly when GPU memory requires a lower concurrency.
MAX_PARALLEL="${MAX_PARALLEL:-$RUNS_PER_MAP}"
T_MAX="${T_MAX:-2050000}"
DRY_RUN="${DRY_RUN:-0}"
IFS=',' read -r -a GPU_IDS <<< "${GPU_IDS:-6}"

if (( $# > 0 )); then
  MAPS=("$@")
elif [[ -n "${SELECTED_MAPS:-}" ]]; then
  IFS=',' read -r -a MAPS <<< "$SELECTED_MAPS"
else
  MAPS=(
    # "1o_2r_vs_4r"
    "1o_10b_vs_1r"
    # "5z_vs_1ul"
  )
fi

if (( ${#MAPS[@]} == 0 )); then
  echo "No maps selected." >&2
  exit 2
fi

LOG_DIR="${LOG_DIR:-log/smac}"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/experiment_progress.log"

resolve_frozen_teacher() {
  "$PYTHON_BIN" - "$1" "$ROOT_DIR" <<'PY'
import json, sys
from pathlib import Path
map_name, root = sys.argv[1], Path(sys.argv[2])
runs = root / "src/LLM-Communication-main/pipeline_runs" / map_name
for run in sorted((p for p in runs.glob("*") if p.is_dir()), reverse=True):
    status_path = run / "pipeline_status.json"
    if not status_path.exists():
        continue
    status = json.loads(status_path.read_text())
    manifest_path = status.get("iteration", {}).get("frozen_manifest")
    if status.get("overall") != "complete" or status.get("iteration", {}).get("status") != "accepted":
        continue
    if not manifest_path or not Path(manifest_path).is_file():
        continue
    manifest = json.loads(Path(manifest_path).read_text())
    teacher = manifest.get("teachers", {}).get(map_name, {}).get("teacher_path")
    if teacher and Path(teacher).is_file():
        print(Path(teacher).resolve())
        raise SystemExit(0)
raise SystemExit(f"No accepted frozen teacher found for {map_name}")
PY
}

important_state_for_map() {
  "$PYTHON_BIN" - "$1" "$ROOT_DIR" <<'PY'
import importlib.util
import json
import sys
from pathlib import Path

map_name, root = sys.argv[1], Path(sys.argv[2])
path = root / "src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05" / map_name / "imp_state_select.py"
if not path.is_file():
    raise SystemExit(f"Important-state selector not found for {map_name}: {path}")
spec = importlib.util.spec_from_file_location(f"important_state_{map_name}", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
indices = module.select_important_state()
if not isinstance(indices, (list, tuple)) or not indices:
    raise SystemExit(f"Invalid important-state selection in {path}: {indices!r}")
if any(not isinstance(index, int) or index < 0 for index in indices):
    raise SystemExit(f"Important-state indices must be non-negative integers: {indices!r}")
print(json.dumps(list(indices), separators=(",", ":")))
PY
}

preflight_teacher() {
  "$PYTHON_BIN" - "$1" "$2" <<'PY'
import importlib.util
import sys
from pathlib import Path

map_name, path = sys.argv[1], Path(sys.argv[2])
spec = importlib.util.spec_from_file_location(f"frozen_teacher_{map_name}", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
missing = [name for name in ("communication_who", "communication_when", "communication_what")
           if not callable(getattr(module, name, None))]
if missing:
    raise SystemExit(f"Frozen teacher {path} is missing functions: {', '.join(missing)}")
print(f"Teacher preflight PASS: {map_name} ({path})")
PY
}

echo "实验开始时间: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
running=0
failed=0

for MAP_NAME in "${MAPS[@]}"; do
  TASK_LOG_DIR="$LOG_DIR/$MAP_NAME"
  mkdir -p "$TASK_LOG_DIR"
  TASK_LOG_FILE="$TASK_LOG_DIR/experiment_progress.log"
  TEACHER_PATH="$(resolve_frozen_teacher "$MAP_NAME")" || exit 1
  IMPORTANT_STATE="$(important_state_for_map "$MAP_NAME")" || exit 1
  preflight_teacher "$MAP_NAME" "$TEACHER_PATH" | tee -a "$TASK_LOG_FILE" || exit 1
  echo "Resolved frozen teacher: $MAP_NAME -> $TEACHER_PATH" | tee -a "$TASK_LOG_FILE"
  echo "Resolved important state: $MAP_NAME -> $IMPORTANT_STATE" | tee -a "$TASK_LOG_FILE"

  for ((iteration = 1; iteration <= RUNS_PER_MAP; iteration++)); do
    while (( running >= MAX_PARALLEL )); do
      if ! wait -n; then failed=$((failed + 1)); fi
      running=$((running - 1))
    done

    gpu="${GPU_IDS[$(((iteration - 1) % ${#GPU_IDS[@]}))]}"
    seed=$((1233 + iteration))
    start_time="$(date '+%Y%m%d_%H%M%S')"
    output="$TASK_LOG_DIR/output_${MAP_NAME}_seed_${seed}_${start_time}.log"
    echo "Starting map=$MAP_NAME seed=$seed gpu=$gpu teacher=$TEACHER_PATH" | tee -a "$TASK_LOG_FILE"

    command=(
      "$PYTHON_BIN" -u src/main_llm_final.py
      "--config=$CONFIG" --env-config=sc2 with
      "env_args.map_name=$MAP_NAME" \
      "seed=$seed" \
      "t_max=$T_MAX" \
      "name=LMAC_LLM_WWW" \
      "running_algorithm_name=(${MAP_NAME})LMAC_LLM_WWW" \
      "comm_code_paths=['${TEACHER_PATH}']" \
      "important_state=${IMPORTANT_STATE}" \
      "phase=multi_train" \
      "tmp2=True" \
      "use_wandb=False" \
      "use_tensorboard=True" \
      "save_model=False"
    )

    if [[ "$DRY_RUN" == "1" ]]; then
      printf 'DRY RUN CUDA_VISIBLE_DEVICES=%q ' "$gpu" | tee -a "$TASK_LOG_FILE"
      printf '%q ' "${command[@]}" | tee -a "$TASK_LOG_FILE"
      printf '\n' | tee -a "$TASK_LOG_FILE"
      continue
    fi

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
  echo "训练结束，但有 $failed 个进程失败。" | tee -a "$LOG_FILE"
  exit 1
fi
echo "所有实验运行完毕：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
