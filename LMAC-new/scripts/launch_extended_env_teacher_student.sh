#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-python}"
RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/data/teacher_student_extended_$(date +%Y%m%d_%H%M%S)}"
RUN_MAPS="${RUN_MAPS:?Set RUN_MAPS to one supported extended-environment task}"
FROZEN_TEACHER_MANIFEST="${FROZEN_TEACHER_MANIFEST:?Set FROZEN_TEACHER_MANIFEST}"
T_MAX="${T_MAX:-2050000}"
SEEDS="${SEEDS:-1234}"
GPU="${GPU:-0}"

mkdir -p "$RUN_ROOT"
cd "$ROOT_DIR"

launch_one() {
  local task="$1"
  local env_config important_state map_override
  case "$task" in
    hallway)
      env_config="hallway"
      important_state="[0,1,2,3]"
      map_override=""
      ;;
    hallway_group)
      env_config="hallway_group"
      important_state="[0,1,2,3,4,5,6,7,8,9,10,11,12,13]"
      map_override=""
      ;;
    academy_3_vs_1_with_keeper)
      env_config="grf"
      important_state="[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]"
      map_override="env_args.map_name=$task"
      ;;
    academy_run_pass_and_shoot_with_keeper)
      env_config="grf"
      important_state="[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]"
      map_override="env_args.map_name=$task"
      ;;
    *)
      echo "Unsupported extended-environment task: $task" >&2
      return 2
      ;;
  esac

  local comm_paths
  comm_paths="$("$PY" scripts/manifest_comm_paths.py --manifest "$FROZEN_TEACHER_MANIFEST" --map "$task" --format json-list)"
  for seed in $SEEDS; do
    local run_dir="$RUN_ROOT/$task/seed_$seed"
    mkdir -p "$run_dir/save" "$run_dir/buffer"
    local cmd=(
      "$PY" src/main_llm_final.py
      "--config=lmac" "--env-config=$env_config" with
      "seed=$seed" "t_max=$T_MAX" "name=LMAC"
      "save_dir=$run_dir/save" "buffer_dir=$run_dir/buffer"
      "comm_code_paths=$comm_paths" "important_state=$important_state"
      "phase=multi_train" "use_wandb=False" "use_tensorboard=True"
      "running_algorithm_name=teacher_student_${task}_${seed}"
    )
    if [[ -n "$map_override" ]]; then
      cmd+=("$map_override")
    fi
    CUDA_VISIBLE_DEVICES="$GPU" "${cmd[@]}" > "$run_dir/train.log" 2>&1
  done
}

for task in $RUN_MAPS; do
  launch_one "$task"
done
