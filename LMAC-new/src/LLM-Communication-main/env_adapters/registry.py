from __future__ import annotations

from pathlib import Path

from .smac import SMACAdapter
from .smacv2 import SMACv2Adapter
from .hallway import HallwayAdapter, HallwayGroupAdapter
from .grf import GRFAdapter


ALIASES = {
    "sc2": "smac",
    "sc2v2": "smacv2",
    "smac_v2": "smacv2",
    "football": "grf",
    "google_football": "grf",
    "google-football": "grf",
    "gfootball": "grf",
}


def normalize_environment(name: str | None) -> str:
    value = (name or "smac").strip().lower()
    return ALIASES.get(value, value)


def get_adapter(name: str | None, project_root: Path | None = None):
    root = project_root or Path(__file__).resolve().parents[1]
    env = normalize_environment(name)
    adapters = {
        "smac": SMACAdapter(root),
        "smacv2": SMACv2Adapter(root),
        "hallway": HallwayAdapter(root),
        "hallway_group": HallwayGroupAdapter(root),
        "grf": GRFAdapter(root),
    }
    if env not in adapters:
        raise KeyError(f"Environment '{env}' is not implemented. Available: {sorted(adapters)}")
    return adapters[env]
