#!/usr/bin/env python3
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import torch as th

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from components.certified_task_facts import map_specs


MAP_SPECS = {
    "1o_10b_vs_1r": {
        "n_agents": 11,
        "obs_dim": 103,
        "time_seq": 10,
        "expected_sender_rate": 10 / (11 * 10),
        "critical_receivers": list(range(10)),
        "critical_senders": [10],
        "task_probes": [
            {
                "name": "overseer_enemy_position_to_banelings",
                "sender": 10,
                "fields": [6, 7],
                "receivers": list(range(10)),
                "fact": "enemy_position",
            },
            {
                "name": "overseer_last_action_to_banelings",
                "sender": 10,
                "fields": list(range(85, 92)),
                "receivers": list(range(10)),
                "fact": "enemy_last_action",
            },
        ],
        "required_task_facts": [
            {
                "fact": "enemy_position",
                "sender": 10,
                "fields": [6, 7],
                "receivers": list(range(10)),
                "feasibility": "Overseer observes enemy position while Banelings need it for target approach.",
                "necessity": "Banelings have limited local sight; the Overseer-to-Baneling edge resolves decentralized target localization.",
                "decision_relevance": "Enemy position changes movement and attack timing for Banelings.",
            },
            {
                "fact": "enemy_last_action",
                "sender": 10,
                "fields": list(range(85, 92)),
                "receivers": list(range(10)),
                "feasibility": "Overseer observation includes the enemy last-action slice.",
                "necessity": "Banelings cannot infer full enemy action history from their local observation alone.",
                "decision_relevance": "Enemy action intent affects whether Banelings should close distance or wait.",
            },
        ],
    },
    "1o_2r_vs_4r": {
        "n_agents": 5,
        "obs_dim": 62,
        "time_seq": 10,
        "task_probes": [
            {
                "name": "ally_health_broadcast",
                "sender": 0,
                "fields": [50],
                "receivers": [1, 2, 3, 4],
                "fact": "ally_health",
            },
            {
                "name": "enemy_position_health_broadcast",
                "sender": 0,
                "fields": [6, 7, 8],
                "receivers": [1, 2, 3, 4],
                "fact": "enemy_position_health",
            },
        ],
        "required_task_facts": [
            {
                "fact": "ally_health",
                "sender": 0,
                "fields": [50],
                "receivers": [1, 2, 3, 4],
                "feasibility": "The reporting unit observes its own health field.",
                "necessity": "Other agents need team health to coordinate focus fire and avoid over-committing wounded allies.",
                "decision_relevance": "Ally health changes retreat, cover, and attack allocation decisions.",
            },
            {
                "fact": "enemy_position_health",
                "sender": 0,
                "fields": [6, 7, 8],
                "receivers": [1, 2, 3, 4],
                "feasibility": "The sender observes enemy relative position and health fields.",
                "necessity": "Receivers may not observe the same enemy state under partial observability.",
                "decision_relevance": "Enemy position and health determine target selection and movement.",
            },
        ],
    },
    "5z_vs_1ul": {
        "n_agents": 5,
        "obs_dim": 48,
        "time_seq": 10,
        "task_probes": [
            {
                "name": "ultralisk_position_broadcast",
                "sender": 0,
                "fields": [4, 5, 6],
                "receivers": [1, 2, 3, 4],
                "fact": "ultralisk_visibility_position",
            },
            {
                "name": "health_and_attack_intent_broadcast",
                "sender": 0,
                "fields": [34, 42],
                "receivers": [1, 2, 3, 4],
                "fact": "health_and_attack_intent",
            },
        ],
        "required_task_facts": [
            {
                "fact": "ultralisk_visibility_position",
                "sender": 0,
                "fields": [4, 5, 6],
                "receivers": [1, 2, 3, 4],
                "feasibility": "The sender observes Ultralisk visibility and relative position.",
                "necessity": "Other Zealots need shared target localization to maintain surround and avoid isolated attacks.",
                "decision_relevance": "Ultralisk position changes chase, surround, and retreat choices.",
            },
            {
                "fact": "health_and_attack_intent",
                "sender": 0,
                "fields": [34, 42],
                "receivers": [1, 2, 3, 4],
                "feasibility": "The sender observes the relevant health and attack-intent fields.",
                "necessity": "Receivers need team and intent context to coordinate focus and disengagement.",
                "decision_relevance": "Health and attack intent alter whether agents trade damage or reposition.",
            },
        ],
    },
}

# Keep the runtime certificate tied to the same required-fact table used by
# learner-side certified teacher weighting.
MAP_SPECS = map_specs()


def load_module(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def call_comm(module, obs, seq_obs):
    try:
        return module.communication(obs)
    except Exception as first_error:
        try:
            return module.communication(seq_obs)
        except Exception as second_error:
            raise RuntimeError(
                f"communication failed for current obs ({first_error}) "
                f"and time-sequence obs ({second_error})"
            )


def build_seq(obs, time_seq):
    return obs.unsqueeze(1).expand(-1, time_seq, -1, -1).contiguous()


def message_part(enhanced, obs_dim):
    return enhanced[:, :, obs_dim:]


def run_task_probes(module, map_name, batch_size, matrix):
    spec = MAP_SPECS[map_name]
    n_agents = spec["n_agents"]
    obs_dim = spec["obs_dim"]
    time_seq = spec["time_seq"]
    reports = []

    for probe in spec.get("task_probes", []):
        base = th.zeros(batch_size, n_agents, obs_dim)
        perturbed = base.clone()
        sender = probe["sender"]
        fields = probe["fields"]
        receivers = probe["receivers"]
        for offset, field in enumerate(fields):
            perturbed[:, sender, field] = 0.25 + 0.05 * (offset + 1)

        base_msg = message_part(call_comm(module, base, build_seq(base, time_seq)), obs_dim)
        perturbed_msg = message_part(call_comm(module, perturbed, build_seq(perturbed, time_seq)), obs_dim)
        delta = (perturbed_msg - base_msg).abs().mean(dim=-1)

        receiver_delta = delta[:, receivers].mean().item() if receivers else 0.0
        non_receiver_ids = [i for i in range(n_agents) if i not in receivers]
        non_receiver_delta = (
            delta[:, non_receiver_ids].mean().item() if non_receiver_ids else 0.0
        )

        edge_present = None
        if matrix is not None:
            edge_present = bool((matrix[:, receivers, sender] > 0.5).float().mean().item() > 0.99)

        reports.append(
            {
                "name": probe["name"],
                "fact": probe.get("fact"),
                "sender": sender,
                "fields": fields,
                "receivers": receivers,
                "receiver_delta": receiver_delta,
                "non_receiver_delta": non_receiver_delta,
                "leakage_ratio": (
                    non_receiver_delta / receiver_delta if receiver_delta > 0 else None
                ),
                "matrix_edge_present": edge_present,
                "passes": (
                    receiver_delta > 1e-5
                    and non_receiver_delta <= max(receiver_delta * 0.1, 1e-8)
                    and (edge_present is not False)
                ),
            }
        )

    return reports


def fields_match(required, probe):
    return (
        required["sender"] == probe["sender"]
        and set(required["fields"]).issubset(set(probe["fields"]))
        and set(required["receivers"]).issubset(set(probe["receivers"]))
    )


def build_completeness_report(map_name, task_probe_reports, matrix, required_facts=None, definition_note=""):
    spec = MAP_SPECS[map_name]
    if required_facts is None:
        required_facts = spec.get("required_task_facts", [])
    probe_by_fact = {}
    for probe in task_probe_reports:
        if probe.get("fact") is not None:
            probe_by_fact.setdefault(probe["fact"], []).append(probe)

    fact_reports = []
    for required in required_facts:
        candidate_probes = [
            probe for probe in probe_by_fact.get(required["fact"], [])
            if fields_match(required, probe)
        ]
        covered_probe = next((probe for probe in candidate_probes if probe["passes"]), None)
        matrix_edges_present = None
        if matrix is not None:
            sender = required["sender"]
            receivers = required["receivers"]
            matrix_edges_present = bool(
                (matrix[:, receivers, sender] > 0.5).float().mean().item() > 0.99
            )

        fact_reports.append(
            {
                "fact": required["fact"],
                "sender": required["sender"],
                "fields": required["fields"],
                "receivers": required["receivers"],
                "feasibility": required["feasibility"],
                "necessity": required["necessity"],
                "decision_relevance": required["decision_relevance"],
                "covered_by_probe": covered_probe["name"] if covered_probe else None,
                "probe_passes": covered_probe is not None,
                "matrix_edges_present": matrix_edges_present,
                "passes": covered_probe is not None and matrix_edges_present is not False,
            }
        )

    coverage_rate = (
        sum(1 for item in fact_reports if item["passes"]) / len(fact_reports)
        if fact_reports else 1.0
    )
    return {
        "definition": (
            "Task-decision completeness is evaluated against map-specific required "
            "facts rather than full state reconstruction."
            + (f" {definition_note}" if definition_note else "")
        ),
        "required_fact_count": len(fact_reports),
        "covered_fact_count": sum(1 for item in fact_reports if item["passes"]),
        "coverage_rate": coverage_rate,
        "fact_reports": fact_reports,
        "passes_task_decision_completeness": coverage_rate >= 1.0,
    }


def certify_file(path, map_name, batch_size, require_matrix):
    spec = MAP_SPECS[map_name]
    n_agents = spec["n_agents"]
    obs_dim = spec["obs_dim"]
    time_seq = spec["time_seq"]
    module = load_module(path)

    obs = th.randn(batch_size, n_agents, obs_dim)
    seq_obs = th.randn(batch_size, time_seq, n_agents, obs_dim)
    enhanced = call_comm(module, obs, seq_obs)
    if enhanced.dim() != 3:
        raise ValueError(f"communication must return [batch, agents, dim], got {tuple(enhanced.shape)}")
    if enhanced.shape[0] != batch_size or enhanced.shape[1] != n_agents:
        raise ValueError(f"unexpected enhanced shape {tuple(enhanced.shape)}")
    if enhanced.shape[-1] <= obs_dim:
        raise ValueError("communication did not append any message dimensions")

    msg = enhanced[:, :, obs_dim:]
    msg_norm_by_agent = msg.abs().mean(dim=(0, 2)).tolist()

    matrix = None
    matrix_rate = None
    per_receiver_rate = None
    if hasattr(module, "communication_matrix"):
        matrix = module.communication_matrix(obs)
        if not th.is_tensor(matrix):
            matrix = th.as_tensor(matrix)
        if matrix.shape != (batch_size, n_agents, n_agents):
            raise ValueError(f"communication_matrix must be [batch, receiver, sender], got {tuple(matrix.shape)}")
        eye = th.eye(n_agents).unsqueeze(0)
        matrix = matrix.float().clamp(0, 1) * (1 - eye)
        matrix_rate = matrix.sum().item() / (batch_size * n_agents * (n_agents - 1))
        per_receiver_rate = matrix.sum(dim=-1).mean(dim=0).tolist()

    likely_receiver_side = False
    if matrix is not None:
        receiver_has_msg = (msg.abs().mean(dim=-1) > 1e-6).float()
        receiver_has_incoming = (matrix.sum(dim=-1) > 0).float()
        likely_receiver_side = bool((receiver_has_msg == receiver_has_incoming).float().mean().item() > 0.9)

    task_probe_reports = run_task_probes(module, map_name, batch_size, matrix)
    task_probe_passes = all(r["passes"] for r in task_probe_reports)
    completeness_report = build_completeness_report(map_name, task_probe_reports, matrix)

    passes = (
        enhanced.shape[-1] > obs_dim
        and (matrix is not None or not require_matrix)
        and task_probe_passes
        and completeness_report["passes_task_decision_completeness"]
    )
    return {
        "path": str(path),
        "map_name": map_name,
        "require_matrix": require_matrix,
        "enhanced_shape": list(enhanced.shape),
        "message_dim": int(enhanced.shape[-1] - obs_dim),
        "message_abs_mean_by_agent": msg_norm_by_agent,
        "has_communication_matrix": matrix is not None,
        "matrix_edge_rate": matrix_rate,
        "incoming_rate_by_receiver": per_receiver_rate,
        "likely_receiver_side_message": likely_receiver_side,
        "task_probe_reports": task_probe_reports,
        "task_decision_completeness": completeness_report,
        "passes_static_certificate": passes,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Static certificate for LLM-generated communication protocols."
    )
    parser.add_argument("--map", required=True, choices=sorted(MAP_SPECS))
    parser.add_argument("--comm-code", action="append", required=True)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    reports = [
        certify_file(Path(p), args.map, args.batch_size, require_matrix=(idx == 0))
        for idx, p in enumerate(args.comm_code)
    ]
    result = {
        "map_name": args.map,
        "batch_size": args.batch_size,
        "reports": reports,
        "accepted": all(r["passes_static_certificate"] for r in reports),
        "note": (
            "This is the static certificate only. Full task-decision completeness "
            "also requires probe/ablation/fixed-teacher online validation."
        ),
    }

    text = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
