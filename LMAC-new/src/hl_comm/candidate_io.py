"""Candidate file management and validation helpers."""

from __future__ import annotations

import importlib.util
import re
import sys
import traceback
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from components.certified_task_facts import map_specs  # noqa: E402


def extract_code_block(text: str) -> str:
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


def candidate_dir(run_root: Path, iteration: int) -> Path:
    return run_root / "candidates" / f"iter_{iteration:03d}"


def write_prompt(path: Path, messages: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = []
    for msg in messages:
        body.append(f"## {msg['role']}\n\n{msg['content']}\n")
    path.write_text("\n".join(body), encoding="utf-8")


def write_candidate_from_response(raw_text: str, dest: Path) -> str:
    code = extract_code_block(raw_text)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(code, encoding="utf-8")
    return code


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def validate_candidate(path: Path, map_name: str, rollout_summary: dict[str, Any] | None = None) -> dict[str, Any]:
    try:
        return _validate_candidate(path, map_name, rollout_summary=rollout_summary)
    except Exception as exc:
        return {
            "valid": False,
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(),
            "comm_code": str(path),
            "map_name": map_name,
        }


def _validate_candidate(path: Path, map_name: str, rollout_summary: dict[str, Any] | None = None) -> dict[str, Any]:
    _reject_python_loops(path)
    import torch as th

    spec = map_specs()[map_name]
    module = load_module(path)
    missing = [
        name
        for name in (
            "message_design_instruction",
            "communication_who",
            "communication_when",
            "communication_what",
        )
        if not hasattr(module, name)
    ]
    if missing:
        raise RuntimeError(f"Candidate is missing required functions: {missing}")

    b = 4
    n = int((rollout_summary or {}).get("n_agents") or spec["n_agents"])
    d = int((rollout_summary or {}).get("rollout_obs_dim") or spec["obs_dim"])
    obs = th.zeros(b, n, d)
    obs[:, :, : min(d, 8)] = th.rand(b, n, min(d, 8))

    who = _normalize_matrix(module.communication_who(obs), obs, n, "communication_who")
    when = _normalize_matrix(module.communication_when(obs), obs, n, "communication_when")
    matrix = (who * when).clamp(0.0, 1.0)
    what = module.communication_what(obs)
    if not th.is_tensor(what):
        what = th.as_tensor(what)
    if tuple(what.shape) != (b, n, d):
        raise RuntimeError(
            f"communication_what(o) must return an obs-aligned mask {(b, n, d)}, got {tuple(what.shape)}"
        )
    if float(what.min().item()) < -1e-6 or float(what.max().item()) > 1.0 + 1e-6:
        raise RuntimeError("communication_what(o) mask values must be in [0, 1].")

    return {
        "valid": True,
        "map_name": map_name,
        "comm_code": str(path),
        "validation_obs_source": "rollout" if rollout_summary and rollout_summary.get("available") else "static_spec",
        "validation_obs_dim": d,
        "documented_obs_dim": (rollout_summary or {}).get("documented_obs_dim") or spec.get("obs_dim"),
        "message_dim": d,
        "matrix_edge_rate": float(matrix.sum().item() / max(b * n * (n - 1), 1)),
        "who_edge_rate": float(who.sum().item() / max(b * n * (n - 1), 1)),
        "when_edge_rate": float(when.sum().item() / max(b * n * (n - 1), 1)),
        "what_dim": int(what.shape[-1]),
        "matrix_min": float(matrix.min().item()),
        "matrix_max": float(matrix.max().item()),
    }


def _reject_python_loops(path: Path) -> None:
    """Communication functions must remain GPU-vectorizable."""
    import ast
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    forbidden = (ast.For, ast.AsyncFor, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
    violations = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("communication_"):
            for child in ast.walk(node):
                if isinstance(child, forbidden):
                    violations.append(f"{node.name}:{getattr(child, 'lineno', '?')}:{type(child).__name__}")
    if violations:
        raise RuntimeError(
            "Python loops/comprehensions are forbidden inside communication functions; "
            "use vectorized torch operations. Violations: " + ", ".join(violations)
        )


def _normalize_matrix(value, obs, n: int, name: str):
    import torch as th

    matrix = value if th.is_tensor(value) else th.as_tensor(value)
    if matrix.dim() == 4:
        matrix = matrix.mean(dim=-1)
    expected = (obs.shape[0], n, n)
    if tuple(matrix.shape) != expected:
        raise RuntimeError(f"{name}(o) returned invalid shape {tuple(matrix.shape)}; expected {expected}")
    diag = matrix[:, th.arange(n), th.arange(n)].abs().max().item()
    if diag > 1e-6:
        raise RuntimeError(f"{name}(o) must have zero self-communication diagonal.")
    if float(matrix.min().item()) < -1e-6 or float(matrix.max().item()) > 1.0 + 1e-6:
        raise RuntimeError(f"{name}(o) values must be in [0, 1].")
    return matrix
