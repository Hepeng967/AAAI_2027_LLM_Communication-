"""Rollout-backed observation metadata and candidate evaluation."""

from __future__ import annotations

import importlib.util
import pickle
import traceback
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
LLM_COMM_ROOT = ROOT / "src" / "LLM-Communication-main"
COMM_INFO_ROOT = LLM_COMM_ROOT / "knowledge_data" / "communication_info"


def load_rollout_obs_summary(
    *,
    map_name: str,
    rollout_root: Path | str | None = None,
    max_files: int = 4,
    max_transitions: int = 2048,
) -> dict[str, Any]:
    """Summarize the actual LMAC offline rollout observations for prompt/validation.

    The documented SMAC obs layout can differ from the tensor consumed by LMAC
    because wrapper/config options may append extra features. This helper treats
    rollout obs.shape[-1] as the source of truth, while keeping the documented
    feature ranges for the dimensions that are known.
    """

    root = Path(rollout_root) if rollout_root is not None else ROOT / "data"
    map_root = root / map_name
    files = sorted(map_root.glob("train_traj_*.pkl"))[: max(0, max_files)]
    if not files:
        return {
            "map_name": map_name,
            "rollout_root": str(root),
            "files": [],
            "available": False,
            "error": f"No train_traj_*.pkl files found under {map_root}",
        }

    documented = load_documented_obs_info(map_name)
    episodes = 0
    transitions = 0
    obs_dim = None
    n_agents = None
    seq_lengths: list[int] = []
    action_dim = None
    input_samples = []

    for path in files:
        batch = _load_pickle(path)
        obs = batch.get("obs")
        if obs is None:
            continue
        shape = tuple(obs.shape)
        if len(shape) != 4:
            continue
        b, t, n, d = shape
        obs_dim = int(d) if obs_dim is None else obs_dim
        n_agents = int(n) if n_agents is None else n_agents
        episodes += int(b)
        valid_t = _valid_transitions(batch, int(t))
        seq_lengths.append(valid_t)
        transitions += int(b * valid_t)
        acts = batch.get("actions_onehot")
        if acts is not None and getattr(acts, "shape", None) is not None:
            action_dim = int(acts.shape[-1])
        agent_inputs = _build_agent_inputs(batch)
        if agent_inputs is not None:
            input_samples.append(agent_inputs.reshape(-1, n, agent_inputs.shape[-1]))
        if transitions >= max_transitions:
            break

    if obs_dim is None or n_agents is None:
        return {
            "map_name": map_name,
            "rollout_root": str(root),
            "files": [str(p) for p in files],
            "available": False,
            "error": "Rollout files did not contain 4D obs tensors.",
        }

    base_dim = int(documented.get("obs_shape") or 0)
    runtime_dim = int(obs_dim + (action_dim or 0) + n_agents)
    features = align_feature_index(documented, obs_dim)
    for idx in range(action_dim or 0):
        features[f"previous_action_{idx}"] = [obs_dim + idx, obs_dim + idx + 1]
    agent_id_start = obs_dim + (action_dim or 0)
    for idx in range(n_agents):
        features[f"agent_id_{idx}"] = [agent_id_start + idx, agent_id_start + idx + 1]
    samples = None
    if input_samples:
        import torch as th
        samples = th.cat(input_samples, dim=0)[:max_transitions]
    return {
        "map_name": map_name,
        "rollout_root": str(root),
        "files": [str(p) for p in files],
        "available": True,
        "n_agents": n_agents,
        "raw_obs_dim": obs_dim,
        "rollout_obs_dim": runtime_dim,
        "documented_obs_dim": base_dim,
        "extra_obs_dim": max(0, obs_dim - base_dim),
        "episodes": episodes,
        "transitions": min(transitions, max_transitions),
        "seq_lengths": seq_lengths,
        "action_dim": action_dim,
        "agent_types": documented.get("obs_agent_type_map", []),
        "feature_index": features,
        "feature_statistics": _feature_statistics(samples, features),
        "alignment_note": (
            "rollout_obs_dim is exactly the RL communication input: raw observation + "
            "previous-action one-hot + agent-id one-hot. Feature positions are identical "
            "in offline evaluation and RL training."
        ),
    }


def load_documented_obs_info(map_name: str) -> dict[str, Any]:
    info_path = COMM_INFO_ROOT / f"{map_name}.json"
    if not info_path.exists():
        return {"map_name": map_name, "feature_index": {}, "obs_feature_names": []}
    import json

    return json.loads(info_path.read_text(encoding="utf-8"))


def align_feature_index(documented: dict[str, Any], actual_dim: int) -> dict[str, list[int]]:
    features: dict[str, list[int]] = {}
    for name, span in (documented.get("feature_index") or {}).items():
        if not isinstance(span, list) or len(span) != 2:
            continue
        start, end = int(span[0]), int(span[1])
        if start >= actual_dim:
            continue
        features[name] = [start, min(end, actual_dim)]

    documented_dim = int(documented.get("obs_shape") or 0)
    for idx in range(max(0, documented_dim), actual_dim):
        features[f"lmac_extra_{idx}"] = [idx, idx + 1]
    return features


def _build_agent_inputs(batch: dict[str, Any]):
    """Reproduce LMAC_MAC._build_inputs for every offline timestep."""
    import torch as th
    obs = batch.get("obs")
    actions = batch.get("actions_onehot")
    if obs is None or actions is None or obs.dim() != 4:
        return None
    b, t, n, _ = obs.shape
    previous = th.zeros_like(actions)
    if t > 1:
        previous[:, 1:] = actions[:, :-1]
    ids = th.eye(n, device=obs.device, dtype=obs.dtype).view(1, 1, n, n).expand(b, t, n, n)
    return th.cat([obs.float(), previous.float(), ids], dim=-1)


def _feature_statistics(samples, feature_index):
    if samples is None or samples.numel() == 0:
        return {}
    flat = samples.reshape(-1, samples.shape[-1]).float()
    stats = {}
    for name, span in feature_index.items():
        start, end = span
        if end - start != 1 or start >= flat.shape[-1]:
            continue
        x = flat[:, start]
        q = x.quantile(x.new_tensor([0.05, 0.5, 0.95]))
        stats[name] = {
            "index": start,
            "min": round(float(x.min()), 6), "max": round(float(x.max()), 6),
            "mean": round(float(x.mean()), 6),
            "p05": round(float(q[0]), 6), "p50": round(float(q[1]), 6), "p95": round(float(q[2]), 6),
            "nonzero_rate": round(float((x.abs() > 1e-8).float().mean()), 6),
        }
    return stats


def evaluate_candidate_on_rollouts(
    *,
    comm_code: Path,
    map_name: str,
    rollout_root: Path | str | None = None,
    max_files: int = 4,
    max_transitions: int = 2048,
) -> dict[str, Any]:
    """Run a candidate on real rollout observations and report hard statistics."""

    try:
        return _evaluate_candidate_on_rollouts(
            comm_code=comm_code,
            map_name=map_name,
            rollout_root=rollout_root,
            max_files=max_files,
            max_transitions=max_transitions,
        )
    except Exception as exc:
        return {
            "valid": False,
            "map_name": map_name,
            "comm_code": str(comm_code),
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(),
        }


def _evaluate_candidate_on_rollouts(
    *,
    comm_code: Path,
    map_name: str,
    rollout_root: Path | str | None,
    max_files: int,
    max_transitions: int,
) -> dict[str, Any]:
    import torch as th

    module = _load_module(comm_code)
    missing = [
        name
        for name in (
            "communication_who",
            "communication_when",
            "communication_what",
        )
        if not hasattr(module, name)
    ]
    if missing:
        raise RuntimeError(f"Candidate is missing required who/when/what functions: {missing}")

    root = Path(rollout_root) if rollout_root is not None else ROOT / "data"
    files = sorted((root / map_name).glob("train_traj_*.pkl"))[: max(0, max_files)]
    if not files:
        raise RuntimeError(f"No rollout files found under {root / map_name}")

    total_steps = 0
    edge_sum = 0.0
    edge_count = 0
    msg_nonzero = 0.0
    msg_count = 0
    msg_abs_sum = 0.0
    dims = {}
    matrix_min = float("inf")
    matrix_max = float("-inf")
    who_rate_sum = 0.0
    when_rate_sum = 0.0
    active_sender_coverage_sum = 0.0
    active_sender_coverage_min = 1.0
    active_sender_count = 0
    evaluated_files: list[str] = []
    evidence_cases: list[dict[str, Any]] = []

    for path in files:
        batch = _load_pickle(path)
        obs = _build_agent_inputs(batch)
        if obs is None:
            continue
        b, t, n, d = tuple(obs.shape)
        flat = obs.reshape(b * t, n, d).float()
        if total_steps + flat.shape[0] > max_transitions:
            flat = flat[: max(0, max_transitions - total_steps)]
        if flat.numel() == 0:
            break

        who = _as_matrix(module.communication_who(flat), flat)
        when = _as_matrix(module.communication_when(flat), flat)
        matrix = (who * when).clamp(0.0, 1.0)
        what = module.communication_what(flat)
        if not th.is_tensor(what):
            what = th.as_tensor(what, device=flat.device, dtype=flat.dtype)
        if tuple(what.shape) != tuple(flat.shape):
            raise RuntimeError(
                f"communication_what(o) returned {tuple(what.shape)}, expected obs-aligned mask {tuple(flat.shape)}"
            )
        if float(what.min().item()) < -1e-6 or float(what.max().item()) > 1.0 + 1e-6:
            raise RuntimeError("communication_what(o) mask values must be in [0, 1].")
        sender_active = matrix.amax(dim=1) > 0.5
        sender_coverage = (what > 0.5).float().mean(dim=-1)
        active_coverages = sender_coverage[sender_active]
        if active_coverages.numel() > 0:
            active_sender_coverage_sum += float(active_coverages.sum().item())
            active_sender_coverage_min = min(
                active_sender_coverage_min, float(active_coverages.min().item())
            )
            active_sender_count += int(active_coverages.numel())
        if len(evidence_cases) < 12:
            slots = min(flat.shape[0], 12 - len(evidence_cases))
            sample_indices = th.linspace(0, flat.shape[0] - 1, steps=slots).long().unique().tolist()
            for sample_idx in sample_indices:
                active = (matrix[sample_idx] > 0.5).nonzero(as_tuple=False)
                selected = (what[sample_idx] > 0.5)
                evidence_cases.append({
                    "case_id": f"{path.stem}:{sample_idx}",
                    "active_edges_receiver_sender": active.tolist(),
                    "selected_what_indices_by_sender": [
                        selected[sender].nonzero(as_tuple=False).flatten().tolist()
                        for sender in range(n)
                    ],
                    "what_coverage_by_sender": [
                        round(float(value), 6) for value in sender_coverage[sample_idx].tolist()
                    ],
                    "selected_values_by_sender": [
                        {
                            str(idx): round(float(flat[sample_idx, sender, idx]), 6)
                            for idx in selected[sender].nonzero(as_tuple=False).flatten().tolist()
                        }
                        for sender in range(n)
                    ],
                })
        for name, mat in {"matrix": matrix, "who": who, "when": when}.items():
            if tuple(mat.shape) != (flat.shape[0], n, n):
                raise RuntimeError(f"{name} has shape {tuple(mat.shape)}, expected {(flat.shape[0], n, n)}")
            diag = mat[:, th.arange(n), th.arange(n)].abs().max().item()
            if diag > 1e-6:
                raise RuntimeError(f"{name} must have zero self-communication diagonal.")
            if float(mat.min().item()) < -1e-6 or float(mat.max().item()) > 1.0 + 1e-6:
                raise RuntimeError(f"{name} values must be in [0, 1].")

        offdiag = 1.0 - th.eye(n, device=flat.device).unsqueeze(0)
        edge_sum += float((matrix * offdiag).sum().item())
        edge_count += int(flat.shape[0] * n * max(n - 1, 1))
        who_rate_sum += float((who * offdiag).sum().item())
        when_rate_sum += float((when * offdiag).sum().item())
        msg_nonzero += float((what.abs() > 1e-8).sum().item())
        msg_abs_sum += float(what.abs().sum().item())
        msg_count += int(what.numel())
        matrix_min = min(matrix_min, float(matrix.min().item()))
        matrix_max = max(matrix_max, float(matrix.max().item()))
        dims = {
            "n_agents": n,
            "rollout_obs_dim": d,
            "message_dim": int(what.shape[-1]),
        }
        total_steps += int(flat.shape[0])
        evaluated_files.append(str(path))
        if total_steps >= max_transitions:
            break

    if total_steps <= 0:
        raise RuntimeError("No rollout transitions were evaluated.")

    return {
        "valid": True,
        "map_name": map_name,
        "comm_code": str(comm_code),
        "files": evaluated_files,
        "transitions": total_steps,
        **dims,
        "matrix_edge_rate": edge_sum / max(edge_count, 1),
        "who_edge_rate": who_rate_sum / max(edge_count, 1),
        "when_edge_rate": when_rate_sum / max(edge_count, 1),
        "message_nonzero_rate": msg_nonzero / max(msg_count, 1),
        "message_abs_mean": msg_abs_sum / max(msg_count, 1),
        "active_sender_what_coverage_mean": (
            active_sender_coverage_sum / active_sender_count if active_sender_count else 0.0
        ),
        "active_sender_what_coverage_min": (
            active_sender_coverage_min if active_sender_count else 0.0
        ),
        "active_sender_count": active_sender_count,
        "matrix_min": matrix_min,
        "matrix_max": matrix_max,
        "risk_flags": _risk_flags(
            edge_rate=edge_sum / max(edge_count, 1),
            message_rate=msg_nonzero / max(msg_count, 1),
        ),
        "evidence_cases": evidence_cases,
    }


def _risk_flags(*, edge_rate: float, message_rate: float) -> list[str]:
    flags = []
    if edge_rate <= 1e-6:
        flags.append("all_zero_edges_on_rollout")
    if edge_rate >= 0.95:
        flags.append("nearly_all_to_all_edges_on_rollout")
    if message_rate <= 1e-6:
        flags.append("all_zero_messages_on_rollout")
    if message_rate >= 0.95:
        flags.append("nearly_dense_messages_on_rollout")
    return flags


def _as_matrix(value: Any, obs: Any) -> Any:
    import torch as th

    mat = value if th.is_tensor(value) else th.as_tensor(value, device=obs.device, dtype=obs.dtype)
    mat = mat.to(device=obs.device, dtype=obs.dtype)
    if mat.dim() == 4:
        mat = mat.mean(dim=-1)
    return mat


def _valid_transitions(batch: dict[str, Any], fallback: int) -> int:
    mask = batch.get("mask")
    if mask is None:
        return fallback
    try:
        return int(mask.reshape(-1).sum().item())
    except Exception:
        return fallback


def _load_pickle(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        obj = pickle.load(handle)
    if not isinstance(obj, dict):
        raise RuntimeError(f"Expected dict rollout file, got {type(obj)} from {path}")
    return obj


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module
