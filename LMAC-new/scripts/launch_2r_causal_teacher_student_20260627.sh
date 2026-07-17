#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"

export RUN_PREFIX="${RUN_PREFIX:-ts_drc_2r_causal_dense}"
export RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/data/teacher_student_eval_20260627_2r_causal_dense}"
export FROZEN_TEACHER_MANIFEST="${FROZEN_TEACHER_MANIFEST:-$ROOT_DIR/description/certification_gate/certification_drc_behavior_conditional_2r_causal_20260627/frozen_teacher_manifest.json}"
export REQUIRE_CUDA="${REQUIRE_CUDA:-true}"

export T_MAX="${T_MAX:-2050000}"
export EPSILON_ANNEAL_TIME="${EPSILON_ANNEAL_TIME:-50000}"
export TEST_INTERVAL="${TEST_INTERVAL:-50000}"
export TEST_NEPISODE="${TEST_NEPISODE:-100}"
export USE_TENSORBOARD="${USE_TENSORBOARD:-True}"
export TMP2="${TMP2:-True}"

export DETACH_LATENT_TO_AGENT="${DETACH_LATENT_TO_AGENT:-False}"
export TEACHER_LAMBDA="${TEACHER_LAMBDA:-1.0}"
export TEACHER_LAMBDA_FINISH="${TEACHER_LAMBDA_FINISH:-0.1}"
export TEACHER_LAMBDA_ANNEAL_TIME="${TEACHER_LAMBDA_ANNEAL_TIME:-500000}"
export COMM_SPARSITY_LAMBDA="${COMM_SPARSITY_LAMBDA:-0.001}"
export LLM_MESSAGE_SEMANTICS="${LLM_MESSAGE_SEMANTICS:-receiver_packed}"

export GPU_2R_0="${GPU_2R_0:-3}"
export GPU_2R_1="${GPU_2R_1:-0}"
export GPU_2R_2="${GPU_2R_2:-1}"
export GPU_2R_3="${GPU_2R_3:-2}"
export GPU_2R_4="${GPU_2R_4:-4}"

mkdir -p "$RUN_ROOT"
PID_FILE="$RUN_ROOT/pids.tsv"
printf "map\tseed_idx\tseed\tgpu\tpid\tlog\tsave_dir\n" > "$PID_FILE"

cd "$ROOT_DIR"

if [[ "$REQUIRE_CUDA" == "true" ]]; then
  if ! "$PY" - <<'PY'
import torch

if not torch.cuda.is_available() or torch.cuda.device_count() <= 0:
    raise SystemExit(1)
print(f"CUDA ready: {torch.cuda.device_count()} visible device(s)")
PY
  then
    rm -f "$PID_FILE"
    echo "CUDA is not available. Refusing to launch 2r teacher-student RL runs." >&2
    exit 2
  fi
fi

"$PY" scripts/manifest_comm_paths.py \
  --manifest "$FROZEN_TEACHER_MANIFEST" \
  --map "1o_2r_vs_4r" \
  --format path \
  > /dev/null

launch_one() {
  local seed_idx="$1"
  local seed="$2"
  local gpu="$3"

  local map="1o_2r_vs_4r"
  local short="2r"
  local important_state="[0, 1, 2, 3, 6, 7, 8, 9, 12, 13, 14, 15, 18, 19, 20, 23, 24, 25, 28, 29, 30, 33, 34, 35]"
  local comm_paths
  comm_paths="$("$PY" scripts/manifest_comm_paths.py --manifest "$FROZEN_TEACHER_MANIFEST" --map "$map" --format json-list)"

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

launch_one 0 2026062700 "$GPU_2R_0"
launch_one 1 2026062701 "$GPU_2R_1"
launch_one 2 2026062702 "$GPU_2R_2"
launch_one 3 2026062703 "$GPU_2R_3"
launch_one 4 2026062704 "$GPU_2R_4"

echo "pid file: $PID_FILE"
