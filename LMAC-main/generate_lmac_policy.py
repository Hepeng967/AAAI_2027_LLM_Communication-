#!/usr/bin/env python3
"""Run only the original LMAC phase-0 Planner/Coder prompts for one SMAC map."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from LLM.llm_core import Communication, get_token_usage  # noqa: E402


def load_deepseek_config(path: Path, model: str) -> tuple[str, str]:
    spec = importlib.util.spec_from_file_location("lmac_api_config", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load API config: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    config = module.LLMAPIConfig.get_model_config(model)
    if config is None:
        raise RuntimeError(f"Model {model!r} is absent from {path}")
    return config.api_key, config.base_url


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", default="1o_2r_vs_4r")
    parser.add_argument("--env", default="sc2")
    parser.add_argument("--n-agents", type=int, default=3)
    parser.add_argument("--model", default="deepseek-v4-pro")
    parser.add_argument("--max-retries", type=int, default=10)
    parser.add_argument(
        "--task-data-dir",
        type=Path,
        default=ROOT / "src" / "llm_source",
    )
    parser.add_argument(
        "--api-config",
        type=Path,
        default=Path("/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/configs/llm_api_config.py"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
    )
    cli = parser.parse_args()

    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    base_url = os.environ.get("DEEPSEEK_BASE_URL", "")
    if not api_key or not base_url:
        configured_key, configured_url = load_deepseek_config(cli.api_config, cli.model)
        api_key = api_key or configured_key
        base_url = base_url or configured_url

    output_dir = cli.output_dir or ROOT / "generated_lmac_assets" / cli.map

    args = SimpleNamespace(
        env=cli.env,
        env_args={"map_name": cli.map},
        dir=str(cli.task_data_dir),
        name="LMAC_ORIGINAL_PHASE0",
        batch_size=2,
        n_agents=cli.n_agents,
        model=cli.model,
        openai_key=api_key,
        api_base_url=base_url,
        claude_key="",
        gemini_key="",
        mse_thres=0.05,
        max_retries=cli.max_retries,
        message_dim_limit=False,
        message_limit_dimension=3,
    )

    # Read dimensions using the original LMAC EnvUtils and original task sheet.
    probe = Communication(args, torch.empty(0), temperature=0.0)
    _, _, obs_dim = probe.env_utils.get_detail_content_and_task_desc()
    test_obs = torch.randn(args.batch_size, args.n_agents, obs_dim)
    comm = Communication(args, test_obs, temperature=0.0)

    output_dir.mkdir(parents=True, exist_ok=True)
    comm.code_utils.code_dir = str(output_dir)
    print(f"[generate-only] map={cli.map} agents={args.n_agents} obs_dim={obs_dim}", flush=True)
    print("[generate-only] original LMAC phase 0 step 1: important state", flush=True)
    imp_path, important_dims = comm.imp_state_generate(max_retries=cli.max_retries)
    print("[generate-only] original LMAC phase 0 step 2: communication(o)", flush=True)
    comm_path, module, message_dim = comm.init_comm_generate(
        max_retries=cli.max_retries,
        important_dims=important_dims,
    )

    output = module.communication(test_obs)
    if output.shape[:2] != test_obs.shape[:2] or output.shape[-1] < obs_dim:
        raise RuntimeError(f"Invalid communication output shape: {tuple(output.shape)}")

    manifest = {
        "map": cli.map,
        "model": cli.model,
        "prompt_implementation": "LMAC-main/src/LLM",
        "task_data": str(cli.task_data_dir / "sc2.xlsx"),
        "important_state_file": str(Path(imp_path).resolve()),
        "communication_file": str(Path(comm_path).resolve()),
        "important_dims": important_dims,
        "input_shape": list(test_obs.shape),
        "output_shape": list(output.shape),
        "message_dim": message_dim,
        "token_usage": get_token_usage(),
    }
    (output_dir / "generation_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"[generate-only] SUCCESS: {comm_path}", flush=True)
    print(f"[generate-only] manifest: {output_dir / 'generation_manifest.json'}", flush=True)


if __name__ == "__main__":
    main()
