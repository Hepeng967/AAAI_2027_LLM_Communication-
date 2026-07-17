"""User-facing defaults for ``python main.py``.

Edit this file for normal experiments. Every value can still be overridden by
the corresponding command-line flag when a one-off run is needed.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LMAC_ROOT = PROJECT_ROOT.parents[1]

# generate: create one initial policy only
# iterate:  load POLICY_PATH (or the latest matrix_code policy) and refine it
# full:     generate an initial policy and then refine it
MODE = "iterate"
MAP_NAME = "1o_2r_vs_4r"

# Leave empty to use matrix_code/<MAP_NAME>/LMAC_WWW/comm_init.py.
POLICY_PATH = ""
ROLLOUT_ROOT = str(LMAC_ROOT / "data")
OUTPUT_ROOT = str(PROJECT_ROOT / "pipeline_runs")

MAX_ITERS = 5
PATIENCE = 2
REPAIR_ATTEMPTS = 3
MAX_FILES = 64
MAX_TRANSITIONS = 4096

# In full mode, automatically collect offline rollouts when the selected map
# has no train_traj_*.pkl yet.
AUTO_COLLECT_ROLLOUTS = True
COLLECT_T_MAX = 6000
COLLECT_SEEDS = 1
COLLECT_SEED_START = 1234
COLLECT_GPU = "0"
COLLECT_CONFIG = "lmac"
COLLECT_ENV_CONFIG = "sc2"

# Empty values reuse the coder model/key/base URL in llm_api_config.py.
MODEL = ""
BASE_URL = ""
API_KEY = ""
API_CONFIG = ""
TEMPERATURE = 0.0
REASONING_EFFORT = ""
DEEPSEEK_THINKING = False

# llm: stop after freezing the teacher
# llm_rl: automatically launch teacher-student RL after acceptance
GATE = "llm"
DRY_RUN = False
