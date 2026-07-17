from __future__ import annotations

from pathlib import Path
from typing import Any
import os
import sys

import yaml

from .base import CollectionSpec, EnvironmentAdapter


TASK_ENV_CONFIG = {
    "protoss_10_vs_10": "sc2_v2_protoss",
    "terran_10_vs_10": "sc2_v2_terran",
    "zerg_10_vs_10": "sc2_v2_zerg",
}


class SMACv2Adapter(EnvironmentAdapter):
    name = "smacv2"

    def supports(self, task: str) -> bool:
        return task in TASK_ENV_CONFIG and self._env_config_path(task).is_file()

    def _env_config_path(self, task: str) -> Path:
        env_config = TASK_ENV_CONFIG.get(task, "")
        return self.project_root.parent / "config" / "envs" / f"{env_config}.yaml"

    def _scenario(self, task: str) -> dict[str, Any]:
        if not self.supports(task):
            raise KeyError(f"Unsupported SMACv2 task: {task}")
        return yaml.safe_load(self._env_config_path(task).read_text(encoding="utf-8"))

    def collection_spec(self, task: str) -> CollectionSpec:
        # The selected env YAML already contains map/capability configuration.
        return CollectionSpec(TASK_ENV_CONFIG[task])

    def runtime_probe(self, task: str) -> dict[str, Any]:
        """Construct the configured wrapper without starting a StarCraft game."""
        os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
        src_root = self.project_root.parent
        if str(src_root) not in sys.path:
            sys.path.insert(0, str(src_root))
        from envs.smacv2_wrapper import SMACv2Wrapper

        env_config = TASK_ENV_CONFIG[task]
        config_path = self._env_config_path(task)
        env_args = yaml.safe_load(config_path.read_text(encoding="utf-8"))["env_args"]
        env_args.pop("seed", None)
        env = SMACv2Wrapper(seed=1234, **env_args)
        try:
            info = env.get_env_info()
        finally:
            env.close()
        keys = ("n_agents", "n_enemies", "n_actions", "obs_shape", "state_shape", "episode_limit")
        result = {key: info.get(key) for key in keys}
        result.update({"available": True, "env_config": env_config, "config_path": str(config_path)})
        documented = self.documented_obs_info(task)
        if int(result["obs_shape"]) != int(documented["obs_shape"]):
            raise RuntimeError(
                f"SMACv2 OBS schema mismatch for {task}: wrapper={result['obs_shape']} "
                f"adapter={documented['obs_shape']}"
            )
        return result

    def task_description(self, task: str) -> dict[str, Any]:
        env_args = self._scenario(task)["env_args"]
        capability = env_args["capability_config"]
        team = capability["team_gen"]
        return {
            "environment": "smacv2",
            "task": task,
            "objective": "Ten allied units cooperate under partial observability to defeat ten enemy units.",
            "n_agents": int(capability["n_units"]),
            "n_enemies": int(capability.get("n_enemies", capability["n_units"])),
            "unit_composition": {
                "dynamic_each_episode": True,
                "unit_types": list(team["unit_types"]),
                "sampling_weights": list(team["weights"]),
                "unit_type_is_observed": bool(team.get("observe", False)),
                "exception_unit_types": list(team.get("exception_unit_types", [])),
            },
            "start_positions": dict(capability.get("start_positions", {})),
            "information_boundary": {
                "allowed": "the collection of all allied agents' local observations",
                "forbidden": ["global state", "future information", "environment internals", "hidden unit identity"],
            },
            "agent_id_semantics": "Tensor row identity only; it does not imply a fixed unit type across episodes.",
        }

    def documented_obs_info(self, task: str) -> dict[str, Any]:
        desc = self.task_description(task)
        n_agents, n_enemies = desc["n_agents"], desc["n_enemies"]
        unit_types = desc["unit_composition"]["unit_types"]
        type_bits = len(unit_types)
        shield = 1 if task.startswith("protoss_") else 0
        move_dim = 4
        enemy_width = 4 + 1 + shield + type_bits
        ally_width = 4 + 1 + shield + type_bits
        own_width = type_bits + 1 + shield + 2
        feature_index: dict[str, list[int]] = {}
        cursor = 0
        for name in ("move_north", "move_south", "move_east", "move_west"):
            feature_index[name] = [cursor, cursor + 1]
            cursor += 1
        enemy_fields = ["available", "distance", "relative_x", "relative_y", "health"]
        if shield:
            enemy_fields.append("shield")
        enemy_fields += [f"unit_type_{name}" for name in unit_types]
        for enemy in range(n_enemies):
            for field in enemy_fields:
                feature_index[f"enemy_{enemy}_{field}"] = [cursor, cursor + 1]
                cursor += 1
        ally_fields = ["visible", "distance", "relative_x", "relative_y", "health"]
        if shield:
            ally_fields.append("shield")
        ally_fields += [f"unit_type_{name}" for name in unit_types]
        for ally_slot in range(n_agents - 1):
            for field in ally_fields:
                feature_index[f"ally_slot_{ally_slot}_{field}"] = [cursor, cursor + 1]
                cursor += 1
        # get_obs_agent writes own health/shield, then absolute normalized
        # position, then the observed unit-type one-hot bits.
        own_fields = ["own_health"] + (["own_shield"] if shield else [])
        own_fields += ["own_normalized_x", "own_normalized_y"]
        own_fields += [f"own_unit_type_{name}" for name in unit_types]
        for field in own_fields:
            feature_index[field] = [cursor, cursor + 1]
            cursor += 1
        expected = move_dim + n_enemies * enemy_width + (n_agents - 1) * ally_width + own_width
        if cursor != expected:
            raise RuntimeError(f"SMACv2 schema construction mismatch: cursor={cursor}, expected={expected}")
        return {
            "map_name": task,
            "environment": "smacv2",
            "obs_shape": expected,
            "n_agents": n_agents,
            "n_enemies": n_enemies,
            "obs_feature_names": list(feature_index),
            "feature_index": feature_index,
            "obs_agent_id_map": [f"agent_{i}" for i in range(n_agents)],
            "obs_agent_type_map": ["dynamic_from_own_unit_type_bits"] * n_agents,
            "feature_groups": {
                "movement": [0, move_dim],
                "enemies": [move_dim, move_dim + n_enemies * enemy_width],
                "allies": [move_dim + n_enemies * enemy_width, move_dim + n_enemies * enemy_width + (n_agents - 1) * ally_width],
                "own": [expected - own_width, expected],
            },
            "schema_source": "SMACv2 get_obs_*_feats_size layout plus selected scenario YAML",
        }

    def task_prompt(self, task: str, obs_info: dict[str, Any]) -> str:
        desc = self.task_description(task)
        composition = desc["unit_composition"]
        lines = [
            f"SMACv2 cooperative combat task '{task}'",
            f"- Objective: {desc['objective']}",
            f"- Agents/enemies: {desc['n_agents']}/{desc['n_enemies']}.",
            f"- Possible allied unit types: {composition['unit_types']} with sampling weights {composition['sampling_weights']}.",
            "- Unit composition and the agent-to-unit-type assignment can change every episode.",
            "- Agent ID is only a tensor-row identity. Never infer a fixed unit role from agent ID.",
            "- Infer roles from the documented observable unit-type fields.",
            "- The teacher receives the collection of all allied local observations and may compare them.",
            "- Do not use global state, future information, hidden environment state, or invented feature semantics.",
            f"- Documented raw observation length: {obs_info['documented_obs_shape']}.",
            f"- Runtime LMAC input length: {obs_info['obs_shape']}.",
            "- Observation feature index map:",
        ]
        for name, span in obs_info["feature_index"].items():
            lines.append(f"    - {span[0]}~{span[1] - 1}: {name}")
        lines.append(f"- Runtime alignment: {obs_info.get('alignment_note', '')}")
        return "\n".join(lines)

    def static_map_spec(self, task: str) -> dict[str, Any]:
        spec = super().static_map_spec(task)
        desc = self.task_description(task)
        spec.update({
            "n_enemies": desc["n_enemies"],
            "dynamic_agent_roles": True,
            "possible_unit_types": desc["unit_composition"]["unit_types"],
            "agent_id_role_warning": desc["agent_id_semantics"],
        })
        return spec
