#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"
MAP="${MAP:?Set MAP, e.g. 1o_10b_vs_1r}"
SHORT="${SHORT:-$MAP}"
CHECKPOINT_PATH="${CHECKPOINT_PATH:?Set CHECKPOINT_PATH to a results/models/... run directory}"
LOAD_STEP="${LOAD_STEP:-500000}"
GPU="${GPU:-0}"
RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/data/comm_ablation_eval_$(date +%Y%m%d_%H%M%S)}"
SEED="${SEED:-2026062100}"
TEST_NEPISODE="${TEST_NEPISODE:-100}"
RUN_PREFIX="${RUN_PREFIX:-comm_ablate}"

case "$MAP" in
  1o_10b_vs_1r)
    IMPORTANT_STATE="[62, 63, 67, 68]"
    ;;
  1o_2r_vs_4r)
    IMPORTANT_STATE="[0, 1, 2, 3, 6, 7, 8, 9, 12, 13, 14, 15, 18, 19, 20, 23, 24, 25, 28, 29, 30, 33, 34, 35]"
    ;;
  5z_vs_1ul)
    IMPORTANT_STATE="[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]"
    ;;
  *)
    echo "Unknown MAP: $MAP" >&2
    exit 2
    ;;
esac

SRC_BASE="src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05/$MAP"
COMM_PATHS="[\"$SRC_BASE/comm_init.py\", \"$SRC_BASE/comm_update.py\", \"$SRC_BASE/comm_update_timestep_wise2.py\"]"

mkdir -p "$RUN_ROOT"
PID_FILE="$RUN_ROOT/pids.tsv"
printf "mode\tpid\tlog\n" > "$PID_FILE"

cd "$ROOT_DIR"

launch_eval() {
  local mode="$1"
  local log_dir="$RUN_ROOT/$MAP/$mode"
  local log="$log_dir/eval.log"
  mkdir -p "$log_dir"
  setsid nohup env \
    CUDA_VISIBLE_DEVICES="$GPU" \
    WANDB_MODE=disabled \
    WANDB_DISABLED=true \
    "$PY" src/main_llm_final.py \
      --config=lmac \
      --env-config=sc2 \
      with \
      "seed=$SEED" \
      "name=LMAC" \
      "comm_code_paths=$COMM_PATHS" \
      "important_state=$IMPORTANT_STATE" \
      "phase=multi_train" \
      "mse_thres=0.05" \
      "tmp2=True" \
      "meta_lambda=0.1" \
      "recon_lambda=1.0" \
      "consistency_lambda=1.0" \
      "use_wandb=False" \
      "use_tensorboard=True" \
      "env_args.map_name=$MAP" \
      "running_algorithm_name=${RUN_PREFIX}_${SHORT}_${mode}" \
      "checkpoint_path=$CHECKPOINT_PATH" \
      "load_step=$LOAD_STEP" \
      "evaluate=True" \
      "test_nepisode=$TEST_NEPISODE" \
      "eval_comm_ablation=$mode" \
      > "$log" 2>&1 &
  printf "%s\t%s\t%s\n" "$mode" "$!" "$log" >> "$PID_FILE"
}

launch_eval "none"
launch_eval "zero"
launch_eval "random_same_rate"
launch_eval "drop_certified_edges"
launch_eval "keep_certified_edges"

echo "pid file: $PID_FILE"
