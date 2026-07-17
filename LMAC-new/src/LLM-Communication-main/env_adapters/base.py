from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CollectionSpec:
    env_config: str
    overrides: tuple[str, ...] = ()


class EnvironmentAdapter:
    name = "base"

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)

    def supports(self, task: str) -> bool:
        raise NotImplementedError

    def collection_spec(self, task: str) -> CollectionSpec:
        raise NotImplementedError

    def documented_obs_info(self, task: str) -> dict[str, Any]:
        raise NotImplementedError

    def task_description(self, task: str) -> dict[str, Any]:
        raise NotImplementedError

    def task_prompt(self, task: str, obs_info: dict[str, Any]) -> str:
        raise NotImplementedError

    def runtime_probe(self, task: str) -> dict[str, Any]:
        return {"available": False, "reason": "adapter does not define a runtime probe"}

    def static_map_spec(self, task: str) -> dict[str, Any]:
        info = self.documented_obs_info(task)
        return {
            "environment": self.name,
            "task": task,
            "n_agents": int(info["n_agents"]),
            "obs_dim": int(info["obs_shape"]),
            "time_seq": 10,
            "dynamic_agent_roles": False,
        }
