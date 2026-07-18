from __future__ import annotations

from typing import Any

from .base import CollectionSpec, EnvironmentAdapter


TASKS = {
    "sysadmin_10": {"config": "cognac_sysadmin_10", "n_agents": 10, "obs": 40, "state": 20, "actions": {0: "do nothing", 1: "reboot"}},
    "binary_consensus_10": {"config": "cognac_binary_consensus_10", "n_agents": 10, "obs": 30, "state": 10, "actions": {0: "binary action 0", 1: "binary action 1"}},
    "firefighting_10": {"config": "cognac_firefighting_10", "n_agents": 10, "obs": 1, "state": 11, "actions": {0: "fight left house", 1: "fight right house"}},
}

OBS_SCHEMAS = {
    "sysadmin_10": {
        "machine_and_job_state_by_node": [0, 20],
        "node_visibility_mask": [20, 30],
        "sender_adjacency_row": [30, 40],
    },
    "binary_consensus_10": {
        "binary_state_by_node": [0, 10],
        "node_visibility_mask": [10, 20],
        "sender_adjacency_row": [20, 30],
    },
    "firefighting_10": {
        "observed_flame_indicator_at_last_visited_house": [0, 1],
    },
}


class COGNACAdapter(EnvironmentAdapter):
    name = "cognac"

    def supports(self, task: str) -> bool:
        return task in TASKS

    def collection_spec(self, task: str) -> CollectionSpec:
        return CollectionSpec(TASKS[task]["config"])

    def documented_obs_info(self, task: str) -> dict[str, Any]:
        spec = TASKS[task]
        feature_index = OBS_SCHEMAS[task]
        return {
            "map_name": task, "environment": self.name,
            "obs_shape": spec["obs"], "n_agents": spec["n_agents"], "n_actions": 2,
            "obs_feature_names": list(feature_index),
            "feature_index": feature_index,
            "obs_agent_id_map": [f"node_{i}" for i in range(10)],
            "obs_agent_type_map": [task.split("_10")[0]] * 10,
            "schema_source": "src/envs/cognac_wrapper.py",
        }

    def task_description(self, task: str) -> dict[str, Any]:
        objectives = {
            "sysadmin_10": "Keep networked machines healthy and completing jobs; failures propagate along directed graph edges.",
            "binary_consensus_10": "Reach binary consensus quickly through probabilistic influence edges.",
            "firefighting_10": "Coordinate ten firefighters to minimize fire across eleven houses.",
        }
        return {"environment": self.name, "task": task, "objective": objectives[task], **TASKS[task]}

    def task_prompt(self, task: str, obs_info: dict[str, Any]) -> str:
        d = self.task_description(task)
        common = [
            f"COGNAC graph-coordination task '{task}'.", f"- Objective: {d['objective']}",
            "- Ten homogeneous agents use two discrete actions and a shared team reward.",
            f"- Actions: {d['actions']}.", f"- Runtime local observation length: {d['obs']}.",
            f"- Centralized state length: {d['state']}.",
        ]
        details = {
            "sysadmin_10": [
                "- Raw indices 0..19 contain two normalized fields per node: machine status then job status.",
                "- Raw indices 20..29 are the node visibility mask; 30..39 are this sender's directed adjacency row.",
                "- A zero in 0..19 is unknown when the corresponding visibility-mask entry is zero.",
                "- Reboot is useful for an unhealthy local machine but interrupts useful work, so graph-dependent failures and neighbor status create information needs.",
            ],
            "binary_consensus_10": [
                "- Raw indices 0..9 contain node-indexed binary states; 10..19 are the visibility mask; 20..29 are this sender's directed influence adjacency row.",
                "- A zero in 0..9 is unknown when the corresponding visibility-mask entry is zero; do not interpret it as observed opinion 0.",
                "- Communication is useful when visible opinions or influence dependencies reveal disagreement that another agent cannot observe locally.",
            ],
            "firefighting_10": [
                "- Raw index 0 is a stochastic binary flame observation at the house last visited by that firefighter, not the true global fire level.",
                "- Agent i chooses between adjacent house i (action 0) and house i+1 (action 1); two neighboring firefighters can jointly visit an interior house.",
                "- Communication should help adjacent firefighters coordinate concentration versus coverage under noisy flame observations.",
            ],
        }
        common.extend(details[task])
        common.extend([
            "- LMAC appends previous-action one-hot and agent-ID one-hot after these raw fields; they are not hidden global state.",
            "- WHO, WHEN and WHAT must use only the supplied per-agent observation tensor and exact indices.",
        ])
        return "\n".join(common)

    def runtime_probe(self, task: str) -> dict[str, Any]:
        s = TASKS[task]
        return {"available": True, "environment": self.name, "task": task,
                "n_agents": 10, "n_actions": 2, "obs_shape": s["obs"],
                "state_shape": s["state"], "episode_limit": 100}

    def static_map_spec(self, task: str) -> dict[str, Any]:
        s = TASKS[task]
        return {
            "environment": self.name,
            "task": task,
            "n_agents": int(s["n_agents"]),
            "n_actions": 2,
            "obs_dim": int(s["obs"]),
            "time_seq": 10,
            "dynamic_agent_roles": False,
        }
