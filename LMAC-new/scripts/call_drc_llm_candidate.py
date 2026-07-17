#!/usr/bin/env python3
"""Call DeepSeek/OpenAI-compatible LLM to create an initial DRC teacher candidate."""

import argparse
import importlib.util
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch as th


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from components.certified_task_facts import map_specs  # noqa: E402


def resolve(path):
    p = Path(path)
    return p if p.is_absolute() else ROOT / p


def extract_code_block(text):
    matches = re.findall(r"```(?:python)?\n([\s\S]*?)```", text)
    if matches:
        return matches[0].strip() + "\n"
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("def "):
            start = idx
            break
    if start is None:
        raise RuntimeError("LLM response did not contain executable Python code.")
    return "\n".join(lines[start:]).strip() + "\n"


def call_openai_compatible(prompt, args):
    try:
        from openai import OpenAI
    except Exception as exc:
        raise RuntimeError("The openai package is required for DeepSeek/OpenAI-compatible calls.") from exc

    api_key = args.api_key or os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("No API key found. Set DEEPSEEK_API_KEY or pass --api-key.")
    client = OpenAI(api_key=api_key, base_url=args.base_url)
    kwargs = {
        "model": args.model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "temperature": args.temperature,
    }
    if args.reasoning_effort:
        kwargs["reasoning_effort"] = args.reasoning_effort
    if args.deepseek_thinking:
        kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
    resp = client.chat.completions.create(**kwargs)
    usage = {}
    if getattr(resp, "usage", None) is not None:
        usage = {
            "prompt_tokens": getattr(resp.usage, "prompt_tokens", None),
            "completion_tokens": getattr(resp.usage, "completion_tokens", None),
            "total_tokens": getattr(resp.usage, "total_tokens", None),
        }
    return resp.choices[0].message.content, usage


def load_module(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_candidate(path, map_name):
    spec = map_specs()[map_name]
    module = load_module(path)
    missing = [name for name in ("message_design_instruction", "communication", "communication_matrix") if not hasattr(module, name)]
    if missing:
        raise RuntimeError(f"Candidate is missing required functions: {missing}")

    b = 4
    n = spec["n_agents"]
    d = spec["obs_dim"]
    obs = th.zeros(b, n, d)
    obs[:, :, : min(d, 8)] = th.rand(b, n, min(d, 8))
    enhanced = module.communication(obs)
    if not th.is_tensor(enhanced):
        enhanced = th.as_tensor(enhanced)
    if enhanced.dim() != 3 or tuple(enhanced.shape[:2]) != (b, n) or enhanced.shape[-1] < d:
        raise RuntimeError(f"communication(o) returned invalid shape {tuple(enhanced.shape)} for obs {(b, n, d)}")

    matrix = module.communication_matrix(obs)
    if not th.is_tensor(matrix):
        matrix = th.as_tensor(matrix)
    if matrix.dim() == 4:
        matrix = matrix.mean(dim=-1)
    if tuple(matrix.shape) != (b, n, n):
        raise RuntimeError(f"communication_matrix(o) returned invalid shape {tuple(matrix.shape)}; expected {(b, n, n)}")
    diag = matrix[:, th.arange(n), th.arange(n)].abs().max().item()
    if diag > 1e-6:
        raise RuntimeError("communication_matrix(o) must have zero self-communication diagonal.")
    return {
        "message_dim": int(enhanced.shape[-1] - d),
        "matrix_edge_rate": float(matrix.sum().item() / max(b * n * (n - 1), 1)),
    }


def main():
    parser = argparse.ArgumentParser(description="Generate an initial DRC communication candidate with an LLM.")
    parser.add_argument("--prompt", required=True, help="DRC candidate prompt md.")
    parser.add_argument("--map", required=True)
    parser.add_argument("--candidate-root", default="src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05")
    parser.add_argument("--candidate-label", required=True)
    parser.add_argument("--metadata-out", required=True)
    parser.add_argument("--raw-response-out", default="")
    parser.add_argument("--model", default="deepseek-v4-flash")
    parser.add_argument("--base-url", default=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"))
    parser.add_argument("--api-key", default="")
    parser.add_argument("--reasoning-effort", default=os.environ.get("DEEPSEEK_REASONING_EFFORT", ""))
    parser.add_argument("--deepseek-thinking", action="store_true")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--dry-run", action="store_true", help="Write metadata only; do not call the LLM.")
    args = parser.parse_args()

    prompt_path = resolve(args.prompt)
    prompt = prompt_path.read_text(encoding="utf-8")
    candidate_path = resolve(Path(args.candidate_root) / f"{args.map}_candidates" / args.candidate_label / "comm_init.py")
    raw_path = resolve(args.raw_response_out) if args.raw_response_out else candidate_path.with_suffix(".raw_response.md")
    metadata = {
        "method": "DRC-LLM-initial-candidate-call-v1",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "map_name": args.map,
        "prompt": str(prompt_path),
        "candidate_label": args.candidate_label,
        "candidate_path": str(candidate_path),
        "model": args.model,
        "base_url": args.base_url,
        "dry_run": args.dry_run,
        "status": "dry_run_prompt_ready" if args.dry_run else "candidate_written",
    }

    if not args.dry_run:
        raw_text, usage = call_openai_compatible(prompt, args)
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(raw_text, encoding="utf-8")
        code = extract_code_block(raw_text)
        candidate_path.parent.mkdir(parents=True, exist_ok=True)
        candidate_path.write_text(code, encoding="utf-8")
        metadata["raw_response_out"] = str(raw_path)
        metadata["usage"] = usage
        metadata["validation"] = validate_candidate(candidate_path, args.map)

    metadata_out = resolve(args.metadata_out)
    metadata_out.parent.mkdir(parents=True, exist_ok=True)
    metadata_out.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
