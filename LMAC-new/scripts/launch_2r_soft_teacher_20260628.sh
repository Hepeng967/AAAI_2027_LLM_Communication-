#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"

RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/data/teacher_student_eval_20260628_2r_soft_teacher}"
RUN_PREFIX="${RUN_PREFIX:-ts_drc_2r_soft_teacher}"
TEACHER_PATH="${TEACHER_PATH:-src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05/1o_2r_vs_4r/comm_init.py}"

T_MAX="${T_MAX:-2050000}"
TEST_INTERVAL="${TEST_INTERVAL:-50000}"
TEST_NEPISODE="${TEST_NEPISODE:-100}"
USE_TENSORBOARD="${USE_TENSORBOARD:-True}"
TMP2="${TMP2:-True}"

TEACHER_LAMBDA="${TEACHER_LAMBDA:-1.0}"
TEACHER_LAMBDA_FINISH="${TEACHER_LAMBDA_FINISH:-0.1}"
TEACHER_LAMBDA_ANNEAL_TIME="${TEACHER_LAMBDA_ANNEAL_TIME:-500000}"
COMM_SPARSITY_LAMBDA="${COMM_SPARSITY_LAMBDA:-0.001}"
STUDENT_COMM_HARD_EVAL="${STUDENT_COMM_HARD_EVAL:-False}"

mkdir -p "$RUN_ROOT"
PID_FILE="$RUN_ROOT/pids.tsv"
printf "map\tseed_idx\tseed\tgpu\tpid\tlog\tsave_dir\n" > "$PID_FILE"

cd "$ROOT_DIR"

launch_one() {
  local seed_idx="$1"
  local seed="$2"
  local gpu="$3"
  local map="1o_2r_vs_4r"
  local run_name="${RUN_PREFIX}_seed${seed_idx}"
  local save_dir="$RUN_ROOT/$map/$run_name/save"
  local buffer_dir="$RUN_ROOT/$map/$run_name/buffer"
  local log_dir="$RUN_ROOT/$map/$run_name"
  local log="$log_dir/train.log"
  local status="$log_dir/status.tsv"
  local important_state="[0, 1, 2, 3, 6, 7, 8, 9, 12, 13, 14, 15, 18, 19, 20, 23, 24, 25, 28, 29, 30, 33, 34, 35]"
  local comm_paths="[\"$TEACHER_PATH\"]"

  mkdir -p "$save_dir" "$buffer_dir" "$log_dir"
  printf "event\tutc\tcode\nstart\t%s\t\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$status"

  setsid nohup bash -c '
    set +e
    env CUDA_VISIBLE_DEVICES="$0" WANDB_MODE=disabled WANDB_DISABLED=true "$1" src/main_llm_final.py \
      --config=lmac --env-config=sc2 with \
      "seed=$2" "t_max=$3" "epsilon_anneal_time=50000" \
      "name=LMAC" "save_dir=$4" "buffer_dir=$5" \
      "comm_code_paths=$6" "important_state=$7" \
      "phase=multi_train" "mse_thres=0.05" "tmp2=$8" \
      "meta_lambda=0.1" "recon_lambda=1.0" "consistency_lambda=1.0" \
      "use_wandb=False" "use_tensorboard=$9" \
      "test_interval=${10}" "test_nepisode=${11}" \
      "env_args.map_name=${12}" "running_algorithm_name=${13}" \
      "llm_message_semantics=receiver_packed" \
      "detach_latent_to_agent=False" \
      "teacher_lambda=${15}" "teacher_lambda_finish=${16}" \
      "teacher_lambda_anneal=True" "teacher_lambda_anneal_time=${17}" \
      "comm_sparsity_lambda=${18}" "student_comm_hard_eval=${19}"
    code=$?
    printf "end\t%s\t%s\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$code" >> "${14}"
    exit "$code"
  ' "$gpu" "$PY" "$seed" "$T_MAX" "$save_dir" "$buffer_dir" "$comm_paths" "$important_state" "$TMP2" "$USE_TENSORBOARD" "$TEST_INTERVAL" "$TEST_NEPISODE" "$map" "$run_name" "$status" "$TEACHER_LAMBDA" "$TEACHER_LAMBDA_FINISH" "$TEACHER_LAMBDA_ANNEAL_TIME" "$COMM_SPARSITY_LAMBDA" "$STUDENT_COMM_HARD_EVAL" \
    > "$log" 2>&1 &

  local pid="$!"
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$map" "$seed_idx" "$seed" "$gpu" "$pid" "$log" "$save_dir" >> "$PID_FILE"
  echo "launched map=$map seed_idx=$seed_idx seed=$seed gpu=$gpu pid=$pid log=$log"
}

launch_one 0 2026062900 "${GPU_2R_0:-3}"
launch_one 1 2026062901 "${GPU_2R_1:-4}"
launch_one 2 2026062902 "${GPU_2R_2:-0}"

echo "pid file: $PID_FILE"
