from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .base import CollectionSpec, EnvironmentAdapter


class _HallwayBaseAdapter(EnvironmentAdapter):
    task_name = ""
    env_config = ""
    raw_obs_dim = 0
    feature_index: dict[str, list[int]] = {}

    def supports(self, task: str) -> bool:
        return task == self.task_name and self._config_path().is_file()

    def _config_path(self) -> Path:
        return self.project_root.parent / "config" / "envs" / f"{self.env_config}.yaml"

    def _env_args(self) -> dict[str, Any]:
        return yaml.safe_load(self._config_path().read_text(encoding="utf-8"))["env_args"]

    def collection_spec(self, task: str) -> CollectionSpec:
        if not self.supports(task):
            raise KeyError(f"Unsupported {self.name} task: {task}")
        return CollectionSpec(self.env_config)

    def documented_obs_info(self, task: str) -> dict[str, Any]:
        if not self.supports(task):
            raise KeyError(f"Unsupported {self.name} task: {task}")
        args = self._env_args()
        n_agents = int(args["n_agents"])
        return {
            "map_name": task,
            "environment": self.name,
            "obs_shape": self.raw_obs_dim,
            "n_agents": n_agents,
            "n_actions": 3,
            "obs_feature_names": list(self.feature_index),
            "feature_index": dict(self.feature_index),
            "obs_agent_id_map": [f"agent_{i}" for i in range(n_agents)],
            "obs_agent_type_map": ["hallway_agent"] * n_agents,
            "schema_source": f"src/envs/hallway/{'joinn.py' if self.name == 'hallway_group' else 'join1.py'}",
        }

    def runtime_probe(self, task: str) -> dict[str, Any]:
        info = self.documented_obs_info(task)
        args = self._env_args()
        return {
            "available": True,
            "environment": self.name,
            "task": task,
            "config_path": str(self._config_path()),
            "n_agents": info["n_agents"],
            "n_actions": 3,
            "obs_shape": self.raw_obs_dim,
            "state_shape": info["n_agents"] * self.raw_obs_dim,
            "episode_limit": max(args["state_numbers"]) + 10,
        }

    def static_map_spec(self, task: str) -> dict[str, Any]:
        spec = super().static_map_spec(task)
        spec["n_actions"] = 3
        return spec


class HallwayAdapter(_HallwayBaseAdapter):
    name = "hallway"
    task_name = "hallway"
    env_config = "hallway"
    raw_obs_dim = 1
    feature_index = {"current_position": [0, 1]}

    def task_description(self, task: str) -> dict[str, Any]:
        args = self._env_args()
        return {
            "environment": self.name,
            "task": task,
            "objective": "All agents must reach position 0 on the same timestep.",
            "failure_condition": "The episode terminates unsuccessfully if only a subset reaches position 0.",
            "n_agents": int(args["n_agents"]),
            "state_numbers": list(args["state_numbers"]),
            "actions": {0: "stay", 1: "move one step toward 0", 2: "move one step away from 0"},
            "information_boundary": "Each agent locally observes only its own current position.",
        }

    def task_prompt(self, task: str, obs_info: dict[str, Any]) -> str:
        desc = self.task_description(task)
        return _hallway_prompt(desc, obs_info, grouped=False)


class HallwayGroupAdapter(_HallwayBaseAdapter):
    name = "hallway_group"
    task_name = "hallway_group"
    env_config = "hallway_group"
    raw_obs_dim = 2
    feature_index = {"current_position": [0, 1], "active_status": [1, 2]}

    def task_description(self, task: str) -> dict[str, Any]:
        args = self._env_args()
        return {
            "environment": self.name,
            "task": task,
            "objective": "Members of each group must reach position 0 simultaneously; groups should finish in separate rounds.",
            "failure_conditions": [
                "A group fails when only a subset of its active members reaches position 0.",
                "If multiple groups finish in the same round, that round is rolled back and penalized.",
            ],
            "n_agents": int(args["n_agents"]),
            "n_groups": int(args["n_groups"]),
            "group_ids": list(args["group_ids"]),
            "state_numbers": list(args["state_numbers"]),
            "actions": {0: "stay", 1: "move one step toward 0", 2: "move one step away from 0"},
            "information_boundary": "Each agent observes only its own position and whether its group remains active.",
        }

    def task_prompt(self, task: str, obs_info: dict[str, Any]) -> str:
        desc = self.task_description(task)
        return _hallway_prompt(desc, obs_info, grouped=True)


def _hallway_prompt(desc: dict[str, Any], obs_info: dict[str, Any], *, grouped: bool) -> str:
    lines = [
        f"{desc['environment']} coordination task '{desc['task']}'",
        f"- Objective: {desc['objective']}",
        f"- Number of agents: {desc['n_agents']}.",
        f"- Per-agent maximum positions: {desc['state_numbers']}.",
        f"- Actions: {desc['actions']}.",
        f"- Information boundary: {desc['information_boundary']}",
        f"- Raw local observation length: {obs_info['documented_obs_shape']}.",
        f"- Runtime LMAC communication input length: {obs_info['obs_shape']}.",
        "- Runtime input appends previous-action one-hot and agent-ID one-hot to the raw observation.",
        "- Agent ID may be used to recover the fixed maximum-position assignment from the task configuration.",
    ]
    if grouped:
        lines.extend([
            f"- Fixed group assignment by agent row: {desc['group_ids']}.",
            f"- Number of groups: {desc['n_groups']}.",
            *[f"- Failure condition: {item}" for item in desc["failure_conditions"]],
        ])
    else:
        lines.append(f"- Failure condition: {desc['failure_condition']}")
    lines.append("- Observation feature index map:")
    lines.extend(f"    - {span[0]}~{span[1] - 1}: {name}" for name, span in obs_info["feature_index"].items())
    lines.append(f"- Runtime alignment: {obs_info.get('alignment_note', '')}")
    return "\n".join(lines)
