#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/gfootball/bin/python}"

RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/data/teacher_student_eval_20260628_grf}"
RUN_PREFIX="${RUN_PREFIX:-ts_drc_grf}"
T_MAX="${T_MAX:-10050000}"
TEST_INTERVAL="${TEST_INTERVAL:-10000}"
TEST_NEPISODE="${TEST_NEPISODE:-16}"
USE_TENSORBOARD="${USE_TENSORBOARD:-True}"

mkdir -p "$RUN_ROOT"
PID_FILE="$RUN_ROOT/pids.tsv"
printf "map\tseed_idx\tseed\tgpu\tpid\tlog\tsave_dir\n" > "$PID_FILE"

cd "$ROOT_DIR"

launch_one() {
  local map="$1"
  local short="$2"
  local seed_idx="$3"
  local seed="$4"
  local gpu="$5"
  local teacher="$6"
  local important_state="$7"

  local run_name="${RUN_PREFIX}_${short}_seed${seed_idx}"
  local save_dir="$RUN_ROOT/$map/$run_name/save"
  local buffer_dir="$RUN_ROOT/$map/$run_name/buffer"
  local log_dir="$RUN_ROOT/$map/$run_name"
  local log="$log_dir/train.log"
  local status="$log_dir/status.tsv"
  local comm_paths="[\"$teacher\"]"

  mkdir -p "$save_dir" "$buffer_dir" "$log_dir"
  printf "event\tutc\tcode\nstart\t%s\t\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$status"

  setsid nohup bash -c '
    set +e
    env CUDA_VISIBLE_DEVICES="$0" WANDB_MODE=disabled WANDB_DISABLED=true PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python "$1" src/main_llm_final.py \
      --config=lmac --env-config=grf with \
      "seed=$2" "t_max=$3" "epsilon_anneal_time=50000" \
      "name=LMAC" "save_dir=$4" "buffer_dir=$5" \
      "comm_code_paths=$6" "important_state=$7" \
      "phase=multi_train" "mse_thres=0.05" "tmp2=True" \
      "meta_lambda=0.1" "recon_lambda=1.0" "consistency_lambda=1.0" \
      "use_wandb=False" "use_tensorboard=$8" \
      "test_interval=$9" "test_nepisode=${10}" \
      "env_args.map_name=${11}" "running_algorithm_name=${12}" \
      "llm_message_semantics=receiver_packed" \
      "detach_latent_to_agent=False" \
      "teacher_lambda=1.0" "teacher_lambda_finish=0.1" "teacher_lambda_anneal_time=500000" \
      "comm_sparsity_lambda=0.001"
    code=$?
    printf "end\t%s\t%s\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$code" >> "${13}"
    exit "$code"
  ' "$gpu" "$PY" "$seed" "$T_MAX" "$save_dir" "$buffer_dir" "$comm_paths" "$important_state" "$USE_TENSORBOARD" "$TEST_INTERVAL" "$TEST_NEPISODE" "$map" "$run_name" "$status" \
    > "$log" 2>&1 &

  local pid="$!"
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$map" "$seed_idx" "$seed" "$gpu" "$pid" "$log" "$save_dir" >> "$PID_FILE"
  echo "launched map=$map seed_idx=$seed_idx seed=$seed gpu=$gpu pid=$pid log=$log"
}

TASK_3V1="academy_3_vs_1_with_keeper"
TASK_RPS="academy_run_pass_and_shoot_with_keeper"
TEACHER_3V1="src/llm_source/LMAC_drc_teacher_20260628/${TASK_3V1}/comm_init.py"
TEACHER_RPS="src/llm_source/LMAC_drc_teacher_20260628/${TASK_RPS}/comm_init.py"
IMP_3V1="[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]"
IMP_RPS="[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]"

launch_one "$TASK_3V1" "3v1" 0 2026062810 "${GPU_3V1_0:-1}" "$TEACHER_3V1" "$IMP_3V1"
launch_one "$TASK_3V1" "3v1" 1 2026062811 "${GPU_3V1_1:-2}" "$TEACHER_3V1" "$IMP_3V1"
launch_one "$TASK_3V1" "3v1" 2 2026062812 "${GPU_3V1_2:-3}" "$TEACHER_3V1" "$IMP_3V1"

launch_one "$TASK_RPS" "rps" 0 2026062820 "${GPU_RPS_0:-4}" "$TEACHER_RPS" "$IMP_RPS"
launch_one "$TASK_RPS" "rps" 1 2026062821 "${GPU_RPS_1:-1}" "$TEACHER_RPS" "$IMP_RPS"
launch_one "$TASK_RPS" "rps" 2 2026062822 "${GPU_RPS_2:-2}" "$TEACHER_RPS" "$IMP_RPS"

echo "pid file: $PID_FILE"
