#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"
RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/data/teacher_student_eval_$(date +%Y%m%d_%H%M%S)}"
T_MAX="${T_MAX:-2050000}"
EPSILON_ANNEAL_TIME="${EPSILON_ANNEAL_TIME:-50000}"
TEST_INTERVAL="${TEST_INTERVAL:-50000}"
TEST_NEPISODE="${TEST_NEPISODE:-100}"
USE_TENSORBOARD="${USE_TENSORBOARD:-True}"
TMP2="${TMP2:-True}"
RUN_PREFIX="${RUN_PREFIX:-ts_packed_dynamic}"
LLM_MESSAGE_SEMANTICS="${LLM_MESSAGE_SEMANTICS:-receiver_packed}"
RUN_MAPS="${RUN_MAPS:-1o_10b_vs_1r 1o_2r_vs_4r 5z_vs_1ul}"
SKIP_STATIC_CERT="${SKIP_STATIC_CERT:-0}"
DETACH_LATENT_TO_AGENT="${DETACH_LATENT_TO_AGENT:-False}"
TEACHER_LAMBDA="${TEACHER_LAMBDA:-1.0}"
TEACHER_LAMBDA_FINISH="${TEACHER_LAMBDA_FINISH:-0.1}"
TEACHER_LAMBDA_ANNEAL_TIME="${TEACHER_LAMBDA_ANNEAL_TIME:-500000}"
COMM_SPARSITY_LAMBDA="${COMM_SPARSITY_LAMBDA:-0.001}"
FROZEN_TEACHER_MANIFEST="${FROZEN_TEACHER_MANIFEST:-}"
REQUIRE_CUDA="${REQUIRE_CUDA:-true}"

mkdir -p "$RUN_ROOT"
PID_FILE="$RUN_ROOT/pids.tsv"
printf "map\tseed_idx\tseed\tgpu\tpid\tlog\tsave_dir\n" > "$PID_FILE"

cd "$ROOT_DIR"

if [[ "$REQUIRE_CUDA" == "true" ]]; then
  if ! "$PY" - <<'PY'
import sys
import torch

if not torch.cuda.is_available() or torch.cuda.device_count() <= 0:
    raise SystemExit(1)
print(f"CUDA ready: {torch.cuda.device_count()} visible device(s)")
PY
  then
    rm -f "$PID_FILE"
    echo "CUDA is not available. Refusing to launch teacher-student RL runs." >&2
    echo "Set REQUIRE_CUDA=false only for explicit CPU/debug runs." >&2
    exit 2
  fi
else
  echo "REQUIRE_CUDA=false: CUDA preflight skipped."
fi

if [[ -n "$FROZEN_TEACHER_MANIFEST" ]]; then
  echo "FROZEN_TEACHER_MANIFEST=$FROZEN_TEACHER_MANIFEST: using DRC frozen teachers and skipping legacy static certificate gate."
  for map in $RUN_MAPS; do
    "$PY" scripts/manifest_comm_paths.py \
      --manifest "$FROZEN_TEACHER_MANIFEST" \
      --map "$map" \
      --format path \
      > /dev/null
  done
elif [[ "$SKIP_STATIC_CERT" != "1" ]]; then
  echo "running static LLM communication certificate gate..."
  "$PY" scripts/certification_gate.py \
    --static-only \
    --maps 1o_10b_vs_1r 1o_2r_vs_4r 5z_vs_1ul \
    --run-prefix "$RUN_PREFIX" \
    --out-dir description/certification_gate
  echo "static certificate gate passed."
else
  echo "SKIP_STATIC_CERT=1: static certificate gate skipped."
fi

launch_one() {
  local map="$1"
  local short="$2"
  local seed_idx="$3"
  local seed="$4"
  local gpu="$5"
  local important_state="$6"

  if [[ " $RUN_MAPS " != *" $map "* ]]; then
    return 0
  fi

  local comm_paths
  if [[ -n "$FROZEN_TEACHER_MANIFEST" ]]; then
    comm_paths="$("$PY" scripts/manifest_comm_paths.py --manifest "$FROZEN_TEACHER_MANIFEST" --map "$map" --format json-list)"
  else
    local src_base="src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05/$map"
    comm_paths="[\"$src_base/comm_init.py\", \"$src_base/comm_update.py\", \"$src_base/comm_update_timestep_wise2.py\"]"
  fi
  local run_name="${RUN_PREFIX}_${short}_seed${seed_idx}"
  local save_dir="$RUN_ROOT/$map/$run_name/save"
  local buffer_dir="$RUN_ROOT/$map/$run_name/buffer"
  local log_dir="$RUN_ROOT/$map/$run_name"
  local log="$log_dir/train.log"
  local status="$log_dir/status.tsv"

  mkdir -p "$save_dir" "$buffer_dir" "$log_dir"

  printf "event\tutc\tcode\nstart\t%s\t\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$status"

  setsid nohup bash -c '
    set +e
    env \
      CUDA_VISIBLE_DEVICES="$0" \
      WANDB_MODE=disabled \
      WANDB_DISABLED=true \
      "$1" src/main_llm_final.py \
        --config=lmac \
        --env-config=sc2 \
        with \
        "seed=$2" \
        "t_max=$3" \
        "epsilon_anneal_time=$4" \
        "name=LMAC" \
        "save_dir=$5" \
        "buffer_dir=$6" \
        "comm_code_paths=$7" \
        "important_state=$8" \
        "phase=multi_train" \
        "mse_thres=0.05" \
        "tmp2=$9" \
        "meta_lambda=0.1" \
        "recon_lambda=1.0" \
        "consistency_lambda=1.0" \
        "use_wandb=False" \
        "use_tensorboard=${10}" \
        "test_interval=${11}" \
        "test_nepisode=${12}" \
        "env_args.map_name=${13}" \
        "running_algorithm_name=${14}" \
        "llm_message_semantics=${16}" \
        "detach_latent_to_agent=${17}" \
        "teacher_lambda=${18}" \
        "teacher_lambda_finish=${19}" \
        "teacher_lambda_anneal_time=${20}" \
        "comm_sparsity_lambda=${21}"
    code=$?
    printf "end\t%s\t%s\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$code" >> "${15}"
    exit "$code"
  ' "$gpu" "$PY" "$seed" "$T_MAX" "$EPSILON_ANNEAL_TIME" "$save_dir" "$buffer_dir" "$comm_paths" "$important_state" "$TMP2" "$USE_TENSORBOARD" "$TEST_INTERVAL" "$TEST_NEPISODE" "$map" "$run_name" "$status" "$LLM_MESSAGE_SEMANTICS" "$DETACH_LATENT_TO_AGENT" "$TEACHER_LAMBDA" "$TEACHER_LAMBDA_FINISH" "$TEACHER_LAMBDA_ANNEAL_TIME" "$COMM_SPARSITY_LAMBDA" \
    > "$log" 2>&1 &

  local pid="$!"
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$map" "$seed_idx" "$seed" "$gpu" "$pid" "$log" "$save_dir" >> "$PID_FILE"
  echo "launched map=$map seed_idx=$seed_idx seed=$seed gpu=$gpu pid=$pid log=$log"
}

launch_one "1o_10b_vs_1r" "10b" 0 2026061700 "${GPU_10B_0:-0}" "[62, 63, 67, 68]"
launch_one "1o_10b_vs_1r" "10b" 1 2026061701 "${GPU_10B_1:-1}" "[62, 63, 67, 68]"
launch_one "1o_10b_vs_1r" "10b" 2 2026061702 "${GPU_10B_2:-2}" "[62, 63, 67, 68]"

launch_one "5z_vs_1ul" "5z" 0 2026061710 "${GPU_5Z_0:-3}" "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]"
launch_one "5z_vs_1ul" "5z" 1 2026061711 "${GPU_5Z_1:-4}" "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]"
launch_one "5z_vs_1ul" "5z" 2 2026061712 "${GPU_5Z_2:-0}" "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]"

launch_one "1o_2r_vs_4r" "2r" 0 2026061720 "${GPU_2R_0:-1}" "[0, 1, 2, 3, 6, 7, 8, 9, 12, 13, 14, 15, 18, 19, 20, 23, 24, 25, 28, 29, 30, 33, 34, 35]"
launch_one "1o_2r_vs_4r" "2r" 1 2026061721 "${GPU_2R_1:-2}" "[0, 1, 2, 3, 6, 7, 8, 9, 12, 13, 14, 15, 18, 19, 20, 23, 24, 25, 28, 29, 30, 33, 34, 35]"
launch_one "1o_2r_vs_4r" "2r" 2 2026061722 "${GPU_2R_2:-3}" "[0, 1, 2, 3, 6, 7, 8, 9, 12, 13, 14, 15, 18, 19, 20, 23, 24, 25, 28, 29, 30, 33, 34, 35]"

echo "pid file: $PID_FILE"
