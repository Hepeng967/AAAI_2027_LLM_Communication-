from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import CollectionSpec, EnvironmentAdapter


TASKS = {
    "academy_3_vs_1_with_keeper": {"n_agents": 3, "n_enemies": 2, "obs_shape": 26},
    "academy_run_pass_and_shoot_with_keeper": {"n_agents": 2, "n_enemies": 2, "obs_shape": 22},
}


class GRFAdapter(EnvironmentAdapter):
    name = "grf"

    def supports(self, task: str) -> bool:
        return task in TASKS and (self.project_root.parent / "config" / "envs" / "grf.yaml").is_file()

    def collection_spec(self, task: str) -> CollectionSpec:
        if not self.supports(task):
            raise KeyError(f"Unsupported GRF task: {task}")
        return CollectionSpec("grf", (f"env_args.map_name={task}",))

    def documented_obs_info(self, task: str) -> dict[str, Any]:
        if not self.supports(task):
            raise KeyError(f"Unsupported GRF task: {task}")
        spec = TASKS[task]
        feature_index = _feature_index(spec["n_agents"], spec["n_enemies"])
        if max(end for _, end in feature_index.values()) != spec["obs_shape"]:
            raise RuntimeError(f"GRF schema for {task} does not match obs_shape={spec['obs_shape']}")
        return {
            "map_name": task,
            "environment": "grf",
            "obs_shape": spec["obs_shape"],
            "n_agents": spec["n_agents"],
            "n_enemies": spec["n_enemies"],
            "n_actions": 19,
            "obs_feature_names": list(feature_index),
            "feature_index": feature_index,
            "obs_agent_id_map": [f"controlled_player_{i}" for i in range(spec["n_agents"])],
            "obs_agent_type_map": ["football_player"] * spec["n_agents"],
            "schema_source": "src/envs/grf_wrapper.py::GRFWrapper.get_simple_obs",
        }

    def task_description(self, task: str) -> dict[str, Any]:
        spec = TASKS[task]
        if task == "academy_3_vs_1_with_keeper":
            objective = (
                "Three controlled attackers cooperate against one field defender and a goalkeeper, "
                "using positioning and passes to score."
            )
        else:
            objective = (
                "Two controlled attackers execute a run-pass-and-shoot sequence against one field "
                "defender and a goalkeeper."
            )
        return {
            "environment": "Google Research Football",
            "task": task,
            "objective": objective,
            "n_agents": spec["n_agents"],
            "n_enemies": spec["n_enemies"],
            "episode_limit": 150,
            "reward": "100 for scoring; a failed terminal episode returns -1; otherwise 0.",
            "information_boundary": (
                "A teacher may compare controlled players' local observations, but may not use "
                "unexposed raw football state, future events, or global state."
            ),
        }

    def task_prompt(self, task: str, obs_info: dict[str, Any]) -> str:
        desc = self.task_description(task)
        lines = [
            f"Google Research Football task '{task}'",
            f"- Objective: {desc['objective']}",
            f"- Controlled agents/opponents including goalkeeper: {desc['n_agents']}/{desc['n_enemies']}.",
            f"- Episode limit: {desc['episode_limit']} steps.",
            f"- Reward: {desc['reward']}",
            f"- Information boundary: {desc['information_boundary']}",
            "- Coordinates are in the GRF normalized pitch coordinate system.",
            "- Teammate slots exclude the observing player; opponent slots include the configured field defender and goalkeeper.",
            "- Relative positions are centered on the observing controlled player; direction vectors are not relative positions.",
            f"- Raw local observation length: {obs_info['documented_obs_shape']}.",
            f"- Runtime LMAC communication input length: {obs_info['obs_shape']}.",
            "- Runtime input appends the previous 19-action one-hot and controlled-player ID one-hot.",
            "- Observation feature index map:",
        ]
        lines.extend(f"    - {span[0]}~{span[1] - 1}: {name}" for name, span in obs_info["feature_index"].items())
        lines.append(f"- Runtime alignment: {obs_info.get('alignment_note', '')}")
        return "\n".join(lines)

    def runtime_probe(self, task: str) -> dict[str, Any]:
        info = self.documented_obs_info(task)
        return {
            "available": False,
            "reason": "GRF runtime construction launches the football engine; static wrapper schema is used before collection.",
            "n_agents": info["n_agents"],
            "n_enemies": info["n_enemies"],
            "n_actions": info["n_actions"],
            "obs_shape": info["obs_shape"],
            "episode_limit": 150,
        }

    def static_map_spec(self, task: str) -> dict[str, Any]:
        spec = super().static_map_spec(task)
        spec.update({"n_enemies": TASKS[task]["n_enemies"], "n_actions": 19})
        return spec


def _feature_index(n_agents: int, n_enemies: int) -> dict[str, list[int]]:
    index: dict[str, list[int]] = {}
    cursor = 0

    def add(name: str, width: int) -> None:
        nonlocal cursor
        index[name] = [cursor, cursor + width]
        cursor += width

    add("ego_absolute_xy", 2)
    for slot in range(n_agents - 1):
        add(f"teammate_{slot}_relative_xy", 2)
    add("ego_direction_xy", 2)
    for slot in range(n_agents - 1):
        add(f"teammate_{slot}_direction_xy", 2)
    for slot in range(n_enemies):
        add(f"opponent_{slot}_relative_xy", 2)
    for slot in range(n_enemies):
        add(f"opponent_{slot}_direction_xy", 2)
    add("ball_relative_xy", 2)
    add("ball_z", 1)
    add("ball_direction_xyz", 3)
    return index
