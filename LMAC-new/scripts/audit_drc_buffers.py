#!/usr/bin/env python3
"""Audit offline buffers before running formal DRC certification."""

import argparse
import json
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT))

from components.certified_task_facts import map_specs  # noqa: E402


REQUIRED_BASE = ("obs", "state", "actions_onehot", "mask")
REQUIRED_RETURN = ("reward", "terminated")
OPTIONAL_FORMAL = ("actions", "avail_actions")
OPTIONAL_METADATA = "metadata"


def find_files(buffer_root, map_name, max_files):
    root = Path(buffer_root)
    candidates = sorted((root / map_name).glob("**/*.pkl"))
    if not candidates:
        candidates = sorted(root.glob(f"**/{map_name}/**/*.pkl"))
    return candidates[:max_files]


def shape_list(value):
    return list(value.shape) if hasattr(value, "shape") else None


def audit_file(path, spec, map_name):
    with Path(path).open("rb") as f:
        item = pickle.load(f)
    keys = set(item)
    report = {
        "file": str(path),
        "keys": sorted(keys),
        "has_base_fields": all(k in keys for k in REQUIRED_BASE),
        "has_return_fields": all(k in keys for k in REQUIRED_RETURN),
        "has_optional_formal_fields": all(k in keys for k in OPTIONAL_FORMAL),
        "has_metadata": OPTIONAL_METADATA in keys and isinstance(item.get(OPTIONAL_METADATA), dict),
        "metadata": item.get(OPTIONAL_METADATA) if isinstance(item.get(OPTIONAL_METADATA), dict) else None,
        "shapes": {k: shape_list(v) for k, v in item.items() if k in keys},
        "shape_issues": [],
        "metadata_issues": [],
    }
    metadata = report["metadata"]
    if metadata is None:
        report["metadata_issues"].append("metadata missing")
    else:
        if metadata.get("map_name") != map_name:
            report["metadata_issues"].append(
                f"metadata map_name {metadata.get('map_name')} != expected {map_name}"
            )
        if metadata.get("split") not in ("train", "test"):
            report["metadata_issues"].append(
                f"metadata split {metadata.get('split')} is not train/test"
            )
        if metadata.get("contains_return_fields") is not True:
            report["metadata_issues"].append("metadata does not mark return fields")
    if "obs" in item:
        obs_shape = shape_list(item["obs"])
        if obs_shape is None or len(obs_shape) != 4:
            report["shape_issues"].append("obs is not [batch,time,agents,dim]")
        else:
            if obs_shape[2] != spec["n_agents"]:
                report["shape_issues"].append(f"obs agents {obs_shape[2]} != spec {spec['n_agents']}")
            raw_plus_last_action_id = None
            if "actions_onehot" in item:
                act_shape = shape_list(item["actions_onehot"])
                if act_shape is not None and len(act_shape) == 4:
                    raw_plus_last_action_id = obs_shape[-1] + act_shape[-1] + obs_shape[2]
            if obs_shape[-1] != spec["obs_dim"] and raw_plus_last_action_id != spec["obs_dim"]:
                report["shape_issues"].append(
                    f"obs dim {obs_shape[-1]} cannot match/rebuild teacher obs_dim {spec['obs_dim']}"
                )
    return report


def aggregate(file_reports):
    total = len(file_reports)
    if total == 0:
        return {
            "num_files": 0,
            "base_coverage": 0.0,
            "return_coverage": 0.0,
            "optional_formal_coverage": 0.0,
            "metadata_coverage": 0.0,
            "metadata_ok_coverage": 0.0,
            "shape_ok_coverage": 0.0,
            "formal_ready": False,
        }
    base = sum(r["has_base_fields"] for r in file_reports)
    ret = sum(r["has_return_fields"] for r in file_reports)
    opt = sum(r["has_optional_formal_fields"] for r in file_reports)
    meta = sum(r["has_metadata"] for r in file_reports)
    meta_ok = sum(not r["metadata_issues"] for r in file_reports)
    shape_ok = sum(not r["shape_issues"] for r in file_reports)
    return {
        "num_files": total,
        "base_coverage": base / total,
        "return_coverage": ret / total,
        "optional_formal_coverage": opt / total,
        "metadata_coverage": meta / total,
        "metadata_ok_coverage": meta_ok / total,
        "shape_ok_coverage": shape_ok / total,
        "formal_ready": base == total and ret == total and shape_ok == total,
    }


def main():
    parser = argparse.ArgumentParser(description="Audit DRC certification buffers.")
    parser.add_argument("--buffer-root", default=str(ROOT / "data"))
    parser.add_argument(
        "--maps",
        nargs="+",
        default=["1o_10b_vs_1r", "1o_2r_vs_4r", "5z_vs_1ul"],
    )
    parser.add_argument("--max-files", type=int, default=128)
    parser.add_argument("--out-json", default=None)
    parser.add_argument("--out-md", default=None)
    args = parser.parse_args()

    specs = map_specs()
    result = {
        "buffer_root": str(args.buffer_root),
        "max_files_per_map": args.max_files,
        "required_base_fields": list(REQUIRED_BASE),
        "required_return_fields_for_formal_drc_v5": list(REQUIRED_RETURN),
        "optional_formal_fields": list(OPTIONAL_FORMAL),
        "maps": {},
    }
    for map_name in args.maps:
        if map_name not in specs:
            raise ValueError(f"Unknown map {map_name}; expected one of {sorted(specs)}")
        files = find_files(args.buffer_root, map_name, args.max_files)
        reports = [audit_file(path, specs[map_name], map_name) for path in files]
        result["maps"][map_name] = {
            "summary": aggregate(reports),
            "files": reports,
        }

    text = json.dumps(result, indent=2)
    if args.out_json:
        Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out_json).write_text(text + "\n")
    if args.out_md:
        lines = [
            "# DRC Buffer Audit",
            "",
            f"- buffer root: `{args.buffer_root}`",
            f"- max files per map: `{args.max_files}`",
            "",
            "| map | files | base | return | optional | metadata | metadata_ok | shape_ok | formal_ready |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
        for map_name, item in result["maps"].items():
            s = item["summary"]
            lines.append(
                f"| {map_name} | {s['num_files']} | {s['base_coverage']:.3f} | "
                f"{s['return_coverage']:.3f} | {s['optional_formal_coverage']:.3f} | "
                f"{s['metadata_coverage']:.3f} | {s['metadata_ok_coverage']:.3f} | "
                f"{s['shape_ok_coverage']:.3f} | {s['formal_ready']} |"
            )
        Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out_md).write_text("\n".join(lines) + "\n")
    print(text)


if __name__ == "__main__":
    main()
