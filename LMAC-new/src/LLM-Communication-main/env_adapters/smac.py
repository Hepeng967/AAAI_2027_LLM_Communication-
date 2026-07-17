from __future__ import annotations

import json
from pathlib import Path

from .base import CollectionSpec, EnvironmentAdapter


class SMACAdapter(EnvironmentAdapter):
    """Compatibility adapter. Existing SMAC JSON and prompts remain authoritative."""

    name = "smac"

    def supports(self, task: str) -> bool:
        return (self.project_root / "knowledge_data" / "communication_info" / f"{task}.json").is_file()

    def collection_spec(self, task: str) -> CollectionSpec:
        return CollectionSpec("sc2", (f"env_args.map_name={task}",))

    def documented_obs_info(self, task: str):
        path = self.project_root / "knowledge_data" / "communication_info" / f"{task}.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def task_description(self, task: str):
        return {"environment": "smac", "task": task, "legacy_prompt_compatible": True}

    def task_prompt(self, task: str, obs_info: dict) -> str:
        # config.py deliberately retains the original SMAC prompt construction.
        return ""
