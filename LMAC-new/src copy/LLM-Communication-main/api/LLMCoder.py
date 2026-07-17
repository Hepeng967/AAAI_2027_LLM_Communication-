"""LLM coder for the three-function LMAC teacher interface."""

import datetime
import ast
import os
import re
import traceback
import json

import numpy as np
import torch

import config
from LLM.call_llm_api.call_llm import TextChatbot


BEIJING_TZ = datetime.timezone(datetime.timedelta(hours=8))

LMAC_SYSTEM_PROMPT = """
You translate a natural-language multi-agent communication policy into one
complete deterministic Python/PyTorch module for LMAC. Implement exactly three
functions: communication_who(o), communication_when(o), and
communication_what(o). Use only the supplied local-observation feature map;
never invent hidden state, future information, files, randomness, environment
internals, or trainable parameters. Prefer vectorized torch operations over
Python loops. Return only one Python code block.
"""


def beijing_timestamp():
    return datetime.datetime.now(BEIJING_TZ).strftime("%Y%m%d_%H%M%S")


class LLMCoder:
    def __init__(self, run_id=None):
        self.coder_bot = TextChatbot("coder")
        obs_info = config.process_lmac_rollout_obs_info(config.map_name)
        self.n_agents = obs_info["n_agents"]
        self.obs_dim = obs_info["obs_shape"]
        self.obs_feature_index = obs_info.get("feature_index", {})
        self.map_name = config.map_name
        self.run_id = run_id or beijing_timestamp()
        self.last_raw_path = None
        self.last_archive_path = None

    def generate_teacher(self, policy, promotion="", max_retry=10):
        """Generate, validate, and archive an LMAC WHO/WHEN/WHAT teacher."""
        for attempt in range(max_retry):
            prompt = self._build_prompt(policy, promotion)
            response = self.coder_bot.query(LMAC_SYSTEM_PROMPT, prompt, maintain_history=True)
            code = self.extract_code(response)
            save_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "matrix_code",
                self.map_name,
                "LMAC_WWW",
            )
            os.makedirs(save_dir, exist_ok=True)
            experiment_dir = os.path.join(save_dir, self.run_id, "generation_attempts")
            os.makedirs(experiment_dir, exist_ok=True)
            archive_path = os.path.join(experiment_dir, f"comm_init_try_{attempt + 1:02d}.py")
            raw_path = os.path.join(experiment_dir, f"raw_response_try_{attempt + 1:02d}.md")
            self.last_raw_path = raw_path
            self.last_archive_path = archive_path
            with open(raw_path, "w", encoding="utf-8") as handle:
                handle.write(response)
            with open(archive_path, "w", encoding="utf-8") as handle:
                handle.write(code if code else response)

            if code is None:
                promotion += "\n[BUG] Return one complete Python code block with all three required functions."
                continue

            try:
                self._reject_loops(code)
                namespace = {"np": np, "torch": torch}
                exec(code, namespace, namespace)
                self._validate(namespace)
            except Exception as exc:
                tb = traceback.format_exc()
                print(f"[LLMCoder][Attempt {attempt + 1} validation error] {exc}\n{tb}")
                promotion += (
                    f"\n[BUG] Generated teacher failed validation: {exc}\n"
                    f"Traceback:\n{tb}\nFix only the reported interface/runtime problem."
                )
                continue

            latest_path = os.path.join(save_dir, "comm_init.py")
            with open(latest_path, "w", encoding="utf-8") as handle:
                handle.write(code)
            print(f"[LLMCoder][SUCCESS] LMAC who/when/what teacher saved to: {latest_path}")
            return namespace

        print(f"[LLMCoder][FATAL] Failed to generate LMAC teacher after {max_retry} attempts.")
        return None

    def _build_prompt(self, policy, promotion):
        policy_text = json.dumps(policy, ensure_ascii=False, indent=2) if isinstance(policy, dict) else str(policy)
        return f"""
Translate this structured LMAC communication policy into a complete Python module:

{policy_text}

Runtime interface:
- n_agents: {self.n_agents}
- obs_dim: {self.obs_dim}
- observation feature index map: {self.obs_feature_index}

Required functions:
1. communication_who(o) -> [batch, receiver, sender] in [0,1].
2. communication_when(o) -> [batch, receiver, sender] in [0,1].
3. communication_what(o) -> an obs-aligned content mask with exactly the same
   shape as o, in [0,1]. A selected feature remains at its original index;
   unselected features are zero. Never compress or reorder features.

Constraints:
- o has shape [batch, n_agents, obs_dim].
- WHO and WHEN use matrix[:, receiver, sender] convention.
- WHO and WHEN must have zero self-communication diagonal.
- Use runtime o.shape[-1]; safely skip an index that is out of range.
- Use vectorized torch operations. Do not loop over batch elements, agents,
  senders, receivers, or observation dimensions.
- Implement every policy rule exactly once and mark its implementation with a
  comment containing its stable rule_id (for example, `# RULE R1`). Do not add
  tactical rules, thresholds, feature selections, or agent roles absent from the
  policy specification. If a stated rule cannot be implemented from the runtime
  observation, leave it inactive and explain why in its rule comment.
- The runtime derives edge_matrix = clamp(who * when, 0, 1) and
  masked_message = o * what_mask; do not implement extra wrapper functions.
- Output only imports, optional vectorized helper functions, and the three
  required communication functions in one ```python block```.

Validation feedback, if any:
{promotion}
"""

    def _validate(self, namespace):
        required = (
            "communication_who",
            "communication_when",
            "communication_what",
        )
        missing = [name for name in required if not callable(namespace.get(name))]
        if missing:
            raise RuntimeError(f"Missing required functions: {missing}")

        obs = torch.randn(2, self.n_agents, self.obs_dim)
        who = namespace["communication_who"](obs)
        when = namespace["communication_when"](obs)
        what = namespace["communication_what"](obs)
        expected_matrix = (2, self.n_agents, self.n_agents)
        for name, value in (("who", who), ("when", when)):
            if not torch.is_tensor(value) or tuple(value.shape) != expected_matrix:
                raise RuntimeError(f"{name} shape must be {expected_matrix}, got {getattr(value, 'shape', None)}")
            diag = value[:, torch.arange(self.n_agents), torch.arange(self.n_agents)]
            if diag.abs().max().item() > 1e-6:
                raise RuntimeError(f"{name} has non-zero self-communication diagonal")
            if value.min().item() < -1e-6 or value.max().item() > 1.0 + 1e-6:
                raise RuntimeError(f"{name} values must be in [0,1]")

        if not torch.is_tensor(what) or tuple(what.shape) != tuple(obs.shape):
            raise RuntimeError(
                f"what mask shape must equal obs {tuple(obs.shape)}, got {getattr(what, 'shape', None)}"
            )
        if what.min().item() < -1e-6 or what.max().item() > 1.0 + 1e-6:
            raise RuntimeError("what mask values must be in [0,1]")

    @staticmethod
    def _reject_loops(code):
        tree = ast.parse(code)
        forbidden = (ast.For, ast.AsyncFor, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
        violations = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("communication_"):
                violations.extend(type(child).__name__ for child in ast.walk(node) if isinstance(child, forbidden))
        if violations:
            raise RuntimeError(
                "communication functions must use vectorized torch operations; forbidden: "
                + ", ".join(violations)
            )

    @staticmethod
    def extract_code(response):
        """Extract a fenced Python block, or accept a direct three-function module."""
        match = re.search(r"```python(.*?)```", response, re.DOTALL)
        if not match:
            match = re.search(r"```(.*?)```", response, re.DOTALL)
        if match:
            return match.group(1).strip()
        required = ("def communication_who", "def communication_when", "def communication_what")
        return response.strip() if all(item in response for item in required) else None
