#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime
from pathlib import Path


MODEL_RE = re.compile(
    r"^LMAC_seed(?P<seed>\d+)_(?P<map>.+)_(?P<time>\d{4}-\d{2}-\d{2} .+)$"
)


def read_json(path):
    try:
        text = path.read_text()
        if not text.strip():
            return None
        return json.loads(text)
    except (OSError, json.JSONDecodeError):
        return None


def matches_run_prefix(name, prefix):
    return name == prefix or name.startswith(f"{prefix}_")


def parse_time(value):
    if not value:
        return None
    value = value.replace("T", " ")
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def run_start_time(run_dir):
    run = read_json(run_dir / "run.json") or {}
    return parse_time(run.get("start_time"))


def checkpoint_steps(model_dir):
    steps = []
    for child in model_dir.iterdir():
        if child.is_dir() and child.name.isdigit():
            steps.append(int(child.name))
    return sorted(steps)


def closest_step(steps, target):
    if not steps:
        return None
    return min(steps, key=lambda step: (abs(step - target), -step))


def load_sacred_runs(sacred_root, maps, run_prefix, min_t_max):
    runs = []
    for map_name in maps:
        for config_path in Path(sacred_root).glob(f"{map_name}/*/config.json"):
            config = read_json(config_path)
            if config is None:
                continue
            alg_name = config.get("running_algorithm_name", "")
            if not matches_run_prefix(alg_name, run_prefix):
                continue
            if int(config.get("t_max", 0) or 0) < min_t_max:
                continue
            seed = config.get("seed")
            if seed is None:
                continue
            runs.append(
                {
                    "map": map_name,
                    "sacred_id": config_path.parent.name,
                    "run_name": alg_name,
                    "seed": int(seed),
                    "start_time": run_start_time(config_path.parent),
                    "config_path": str(config_path),
                }
            )
    return runs


def model_candidates(models_root, map_name, seed):
    root = Path(models_root) / map_name
    candidates = []
    if not root.exists():
        return candidates
    prefix = f"LMAC_seed{seed}_{map_name}_"
    for model_dir in root.iterdir():
        if not model_dir.is_dir() or not model_dir.name.startswith(prefix):
            continue
        match = MODEL_RE.match(model_dir.name)
        model_time = parse_time(match.group("time")) if match else None
        candidates.append(
            {
                "path": model_dir,
                "time": model_time,
                "steps": checkpoint_steps(model_dir),
            }
        )
    return candidates


def choose_model(candidates, start_time):
    if not candidates:
        return None
    if start_time is None:
        return max(candidates, key=lambda item: item["time"] or datetime.min)
    return min(
        candidates,
        key=lambda item: (
            abs(((item["time"] or datetime.min) - start_time).total_seconds()),
            item["path"].name,
        ),
    )


def make_record(run, model, target_step, max_step_delta):
    out_run = dict(run)
    if out_run.get("start_time") is not None:
        out_run["start_time"] = out_run["start_time"].isoformat()
    if model is None:
        return {
            **out_run,
            "status": "missing_model_dir",
            "checkpoint_path": None,
            "selected_step": None,
            "available_steps": [],
        }
    selected = closest_step(model["steps"], target_step)
    status = "ready"
    if selected is None:
        status = "missing_checkpoints"
    elif abs(selected - target_step) > max_step_delta:
        status = "step_too_far"
    return {
        **out_run,
        "status": status,
        "checkpoint_path": str(model["path"]),
        "selected_step": selected,
        "target_step": target_step,
        "step_delta": None if selected is None else selected - target_step,
        "available_steps": model["steps"],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Find model checkpoints for teacher-student ablation evaluation."
    )
    parser.add_argument("--sacred-root", default="results/sacred/LMAC")
    parser.add_argument("--models-root", default="results/models/LMAC")
    parser.add_argument("--maps", nargs="+", default=["1o_10b_vs_1r", "1o_2r_vs_4r", "5z_vs_1ul"])
    parser.add_argument("--run-prefix", required=True)
    parser.add_argument("--target-step", type=int, default=500000)
    parser.add_argument("--max-step-delta", type=int, default=100000)
    parser.add_argument("--min-t-max", type=int, default=500000)
    parser.add_argument("--json-out", default=None)
    parser.add_argument("--shell", action="store_true", help="Print launch_comm_ablation_eval.sh environment lines.")
    args = parser.parse_args()

    runs = load_sacred_runs(args.sacred_root, args.maps, args.run_prefix, args.min_t_max)
    records = []
    for run in runs:
        model = choose_model(
            model_candidates(args.models_root, run["map"], run["seed"]),
            run["start_time"],
        )
        records.append(make_record(run, model, args.target_step, args.max_step_delta))

    result = {
        "run_prefix": args.run_prefix,
        "target_step": args.target_step,
        "records": records,
        "ready_count": sum(1 for item in records if item["status"] == "ready"),
        "total_count": len(records),
    }

    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2) + "\n")

    if args.shell:
        for item in records:
            if item["status"] != "ready":
                print(f"# PENDING {item['run_name']}: {item['status']} steps={item['available_steps']}")
                continue
            short = item["run_name"].split("_")[1] if "_" in item["run_name"] else item["map"]
            print(
                f"RUN_PREFIX=comm_ablate_{item['run_name']} "
                f"SEED={item['seed']} "
                f"MAP={item['map']} SHORT={short} "
                f"CHECKPOINT_PATH='{item['checkpoint_path']}' "
                f"LOAD_STEP={item['selected_step']} "
                "bash scripts/launch_comm_ablation_eval.sh"
            )
    else:
        for item in records:
            print(
                f"{item['map']} {item['run_name']} seed={item['seed']} "
                f"status={item['status']} step={item['selected_step']} "
                f"path={item['checkpoint_path']}"
            )
        print(f"ready={result['ready_count']}/{result['total_count']}")

    raise SystemExit(0 if result["ready_count"] == result["total_count"] and records else 1)


if __name__ == "__main__":
    main()
