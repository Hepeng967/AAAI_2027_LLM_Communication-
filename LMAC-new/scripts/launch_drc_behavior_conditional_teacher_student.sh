#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# One-shot launcher for the 2026-06-25 DRC behavior-conditional frozen teachers.
# Run this from a normal host shell where nvidia-smi can see /dev/nvidia*.

export RUN_PREFIX="${RUN_PREFIX:-ts_drc_behavior_conditional}"
export RUN_ROOT="${RUN_ROOT:-$ROOT_DIR/data/teacher_student_eval_20260625_drc_behavior_conditional}"
export FROZEN_TEACHER_MANIFEST="${FROZEN_TEACHER_MANIFEST:-$ROOT_DIR/description/certification_gate/certification_drc_behavior_conditional_20260625/frozen_teacher_manifest.json}"
export REQUIRE_CUDA="${REQUIRE_CUDA:-true}"

export T_MAX="${T_MAX:-2050000}"
export TEST_INTERVAL="${TEST_INTERVAL:-50000}"
export TEST_NEPISODE="${TEST_NEPISODE:-100}"
export USE_TENSORBOARD="${USE_TENSORBOARD:-True}"
export TMP2="${TMP2:-True}"

export DETACH_LATENT_TO_AGENT="${DETACH_LATENT_TO_AGENT:-False}"
export TEACHER_LAMBDA="${TEACHER_LAMBDA:-1.0}"
export TEACHER_LAMBDA_FINISH="${TEACHER_LAMBDA_FINISH:-0.1}"
export TEACHER_LAMBDA_ANNEAL_TIME="${TEACHER_LAMBDA_ANNEAL_TIME:-500000}"
export COMM_SPARSITY_LAMBDA="${COMM_SPARSITY_LAMBDA:-0.001}"

# GPU layout for five TITAN Xp cards, with GPU 0 already lightly occupied.
# Override any GPU_* variable at launch time if the machine state changes.
export GPU_10B_0="${GPU_10B_0:-1}"
export GPU_10B_1="${GPU_10B_1:-2}"
export GPU_10B_2="${GPU_10B_2:-3}"

export GPU_5Z_0="${GPU_5Z_0:-4}"
export GPU_5Z_1="${GPU_5Z_1:-1}"
export GPU_5Z_2="${GPU_5Z_2:-2}"

export GPU_2R_0="${GPU_2R_0:-3}"
export GPU_2R_1="${GPU_2R_1:-4}"
export GPU_2R_2="${GPU_2R_2:-0}"

cd "$ROOT_DIR"
bash "$ROOT_DIR/scripts/launch_teacher_student_eval.sh"
