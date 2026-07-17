#!/usr/bin/env python3
"""Validate a DRC teacher communication code file before certification/RL."""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import torch as th


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from components.certified_task_facts import map_specs  # noqa: E402


def load_module(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(path, map_name):
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
        "map_name": map_name,
        "comm_code": str(path),
        "valid": True,
        "message_dim": int(enhanced.shape[-1] - d),
        "matrix_edge_rate": float(matrix.sum().item() / max(b * n * (n - 1), 1)),
        "matrix_min": float(matrix.min().item()),
        "matrix_max": float(matrix.max().item()),
    }


def main():
    parser = argparse.ArgumentParser(description="Validate DRC communication teacher interface.")
    parser.add_argument("--map", required=True, choices=sorted(map_specs()))
    parser.add_argument("--comm-code", required=True)
    parser.add_argument("--out-json", default="")
    args = parser.parse_args()

    report = validate(Path(args.comm_code), args.map)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out_json:
        out = Path(args.out_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
