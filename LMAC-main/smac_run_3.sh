#!/usr/bin/env bash
set -u

export TZ="Asia/Shanghai"
export SC2PATH="${SC2PATH:-/data/hp/3rdparty/StarCraftII}"
export PYTHONDONTWRITEBYTECODE=1
# tensorboard_logger bundles legacy protobuf definitions. Current protobuf
# rejects them under the C++ implementation, while the Python implementation
# remains wire-compatible and is only used for lightweight metric logging.
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
BATCH_SIZE_OVERRIDE="${BATCH_SIZE_OVERRIDE:-}"
# LMAC-main lacks original archive files for 1o_2r_vs_4r. This directory holds
# a previously generated, old-interface communication(o) LMAC policy, not WWW.
LEGACY_ASSET_ROOT="${LEGACY_ASSET_ROOT:-/data/hp/LLM_Communication/LMAC-new/src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05}"
IFS=',' read -r -a GPU_IDS <<< "${GPU_IDS:-7}"

if (( $# > 0 )); then
  MAPS=("$@")
elif [[ -n "${SELECTED_MAPS:-}" ]]; then
  IFS=',' read -r -a MAPS <<< "$SELECTED_MAPS"
else
  MAPS=(
    # "1o_2r_vs_4r"
    # "1o_10b_vs_1r"
    "5z_vs_1ul"
  )
fi

if (( ${#MAPS[@]} == 0 )); then
  echo "No maps selected." >&2
  exit 2
fi

LOG_DIR="${LOG_DIR:-log}"
mkdir -p "$LOG_DIR" "$ROOT_DIR/results"
LOG_FILE="$LOG_DIR/experiment_progress.log"

# Never patch LMAC-main/src. Make a private source copy and apply only runtime
# compatibility fixes (syntax, optional dependencies and CLI parsing) there.
prepare_runtime_source() {
  RUNTIME_ROOT="$(mktemp -d /tmp/lmac-main-runtime.XXXXXX)"
  cp -a "$ROOT_DIR/src" "$RUNTIME_ROOT/src"
  ln -s "$ROOT_DIR/results" "$RUNTIME_ROOT/results"

  "$PYTHON_BIN" - "$RUNTIME_ROOT/src" <<'PY'
from pathlib import Path
import sys

src = Path(sys.argv[1])

def replace(relative, old, new):
    path = src / relative
    text = path.read_text()
    if old not in text:
        raise SystemExit(f"Compatibility patch anchor missing in {path}: {old!r}")
    path.write_text(text.replace(old, new))

replace(
    "controllers/lmac_controller.py",
    "       agent_outputs, *_  = self.forward(ep_batch, t_ep, test_mode=test_mode)\n"
    "       chosen_actions = self.action_selector.select_action(agent_outputs[bs], avail_actions[bs], t_env, test_mode=test_mode)\n\n"
    "       return chosen_actions",
    "        agent_outputs, *_ = self.forward(ep_batch, t_ep, test_mode=test_mode)\n"
    "        chosen_actions = self.action_selector.select_action(agent_outputs[bs], avail_actions[bs], t_env, test_mode=test_mode)\n\n"
    "        return chosen_actions",
)
replace(
    "main_llm_final.py",
    "import sys\nimport yaml",
    "import sys\nimport ast\nimport yaml",
)
replace(
    "main_llm_final.py",
    '            config_dict["comm_code_paths"] = comm_code_paths',
    '            config_dict["comm_code_paths"] = ast.literal_eval(comm_code_paths)',
)
replace(
    "run_llm_final.py",
    "import wandb",
    "try:\n    import wandb\nexcept ImportError:\n    wandb = None",
)
replace(
    "run_llm_final.py",
    "from LLM.llm_core import Communication",
    "from LLM.code_utils import CodeUtils",
)
replace(
    "run_llm_final.py",
    '    args.device = "cuda" if th.cuda.is_available() else "cpu"',
    '    args.device = "cuda" if args.use_cuda and th.cuda.is_available() else "cpu"',
)
replace(
    "run_llm_final.py",
    "        comm = Communication(args, None)\n"
    "        comm_module = comm.code_utils.import_and_reload_module(comm_code_paths[0])",
    "        code_utils = CodeUtils(args)\n"
    "        comm_module = code_utils.import_and_reload_module(comm_code_paths[0])",
)
replace(
    "run_llm_final.py",
    "comm.code_utils.import_and_reload_module",
    "code_utils.import_and_reload_module",
)
replace(
    "run_llm_final.py",
    '    done_flag_path = os.path.join(args.save_dir, "done.flag")',
    '    done_flag_path = os.path.join(args.save_dir, "done.flag")\n'
    '    os.makedirs(os.path.dirname(done_flag_path) or ".", exist_ok=True)',
)
replace(
    "learners/lmac_learner.py",
    '        device = "cuda" if th.cuda.is_available() else "cpu" ',
    '        device = "cuda" if args.use_cuda and th.cuda.is_available() else "cpu"',
)
replace(
    "envs/__init__.py",
    "from envs.lbf_envs.lbf_env import ForagingEnv",
    "try:\n    import gym\nexcept ModuleNotFoundError:\n"
    "    import gymnasium as gym\n    sys.modules.setdefault('gym', gym)\n\n"
    "from envs.lbf_envs.lbf_env import ForagingEnv",
)
PY

  RUNTIME_SRC="$RUNTIME_ROOT/src"
  echo "Prepared isolated compatibility runtime: $RUNTIME_ROOT" | tee -a "$LOG_FILE"
}

resolve_baseline_asset() {
  "$PYTHON_BIN" - "$1" "$2" "$ROOT_DIR" "$LEGACY_ASSET_ROOT" <<'PY'
import sys
from pathlib import Path

map_name, filename = sys.argv[1], sys.argv[2]
root, fallback = Path(sys.argv[3]), Path(sys.argv[4])
primary = root / "src/llm_source_archive" / map_name / filename
generated = root / "generated_lmac_assets" / map_name / filename
path = primary if primary.is_file() else generated if generated.is_file() else fallback / map_name / filename
if not path.is_file():
    raise SystemExit(
        f"Original LMAC asset missing for {map_name}: tried {primary}, {generated}, and {path}"
    )
print(path.resolve())
PY
}

read_important_state() {
  "$PYTHON_BIN" - "$1" <<'PY'
import importlib.util
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("lmac_important_state", path)
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

preflight_policy() {
  "$PYTHON_BIN" - "$1" "$2" <<'PY'
import importlib.util
import sys
from pathlib import Path

map_name, path = sys.argv[1], Path(sys.argv[2])
spec = importlib.util.spec_from_file_location(f"lmac_policy_{map_name}", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
if not callable(getattr(module, "communication", None)):
    raise SystemExit(f"Original LMAC policy {path} is missing communication(o)")
print(f"Original LMAC policy preflight PASS: {map_name} ({path})")
PY
}

wait_for_one() {
  if wait -n; then
    return 0
  fi
  status=$?
  latest_log="$(find "$LOG_DIR" -maxdepth 1 -type f -name 'output_*.log' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)"
  echo "Training subprocess failed with exit code $status." | tee -a "$LOG_FILE" >&2
  if [[ -n "$latest_log" && -f "$latest_log" ]]; then
    echo "Last 80 lines of $latest_log:" | tee -a "$LOG_FILE" >&2
    tail -80 "$latest_log" | tee -a "$LOG_FILE" >&2
  fi
  return "$status"
}

prepare_runtime_source
cleanup_runtime() {
  if (( ${running:-0} > 0 )); then
    echo "Parent exited while $running training process(es) may still be active; retaining runtime: $RUNTIME_ROOT" >&2
    return
  fi
  rm -rf "${RUNTIME_ROOT:-}"
}
handle_interrupt() {
  echo "Interrupted parent monitor; detached training processes are left running." >&2
  exit 130
}
trap cleanup_runtime EXIT
trap handle_interrupt INT TERM
echo "实验开始时间: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
running=0
failed=0

for MAP_NAME in "${MAPS[@]}"; do
  POLICY_PATH="$(resolve_baseline_asset "$MAP_NAME" comm_init.py)" || exit 1
  IMPORTANT_STATE_PATH="$(resolve_baseline_asset "$MAP_NAME" imp_state_select.py)" || exit 1
  IMPORTANT_STATE="$(read_important_state "$IMPORTANT_STATE_PATH")" || exit 1
  preflight_policy "$MAP_NAME" "$POLICY_PATH" | tee -a "$LOG_FILE" || exit 1
  echo "Resolved original LMAC policy: $MAP_NAME -> $POLICY_PATH" | tee -a "$LOG_FILE"
  echo "Resolved important state: $MAP_NAME -> $IMPORTANT_STATE" | tee -a "$LOG_FILE"

  for ((iteration = 1; iteration <= RUNS_PER_MAP; iteration++)); do
    while (( running >= MAX_PARALLEL )); do
      if ! wait_for_one; then failed=$((failed + 1)); fi
      running=$((running - 1))
    done

    gpu="${GPU_IDS[$(((iteration - 1) % ${#GPU_IDS[@]}))]}"
    seed=$((1233 + iteration))
    start_time="$(date '+%Y%m%d_%H%M%S')"
    output="$LOG_DIR/output_${MAP_NAME}_seed_${seed}_${start_time}.log"
    echo "Starting original LMAC map=$MAP_NAME seed=$seed gpu=$gpu policy=$POLICY_PATH" | tee -a "$LOG_FILE"

    command=(
      "$PYTHON_BIN" -u "$RUNTIME_SRC/main_llm_final.py"
      "--config=$CONFIG" --env-config=sc2 with
      "env_args.map_name=$MAP_NAME"
      "seed=$seed"
      "t_max=$T_MAX"
      "name=LMAC_ORIGINAL"
      "running_algorithm_name=(${MAP_NAME})LMAC_ORIGINAL"
      "comm_code_paths=['${POLICY_PATH}']"
      "important_state=${IMPORTANT_STATE}"
      "phase=multi_train"
      "use_wandb=False"
      "use_tensorboard=True"
      "save_model=False"
    )
    if [[ -n "$BATCH_SIZE_OVERRIDE" ]]; then
      command+=("batch_size=$BATCH_SIZE_OVERRIDE")
    fi

    if [[ "$DRY_RUN" == "1" ]]; then
      printf 'DRY RUN CUDA_VISIBLE_DEVICES=%q ' "$gpu" | tee -a "$LOG_FILE"
      printf '%q ' "${command[@]}" | tee -a "$LOG_FILE"
      printf '\n' | tee -a "$LOG_FILE"
      continue
    fi

    # A separate session prevents terminal Ctrl-C from killing a training run.
    # If the parent monitor is interrupted, cleanup_runtime retains the source
    # copy needed by Sacred and the detached children can continue safely.
    CUDA_VISIBLE_DEVICES="$gpu" nohup setsid "${command[@]}" > "$output" 2>&1 < /dev/null &
    echo "Started PID=$! log=$output" | tee -a "$LOG_FILE"
    running=$((running + 1))
  done
done

while (( running > 0 )); do
  if ! wait_for_one; then failed=$((failed + 1)); fi
  running=$((running - 1))
done

if (( failed > 0 )); then
  echo "训练结束，但有 $failed 个进程失败。" | tee -a "$LOG_FILE"
  exit 1
fi
echo "所有实验运行完毕：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
