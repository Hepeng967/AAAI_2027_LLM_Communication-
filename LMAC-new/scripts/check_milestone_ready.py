#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def read_json(path):
    try:
        text = path.read_text()
        if not text.strip():
            return None
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def scalar_value(x):
    if isinstance(x, dict) and "value" in x:
        return float(x["value"])
    if isinstance(x, (int, float)):
        return float(x)
    return None


def latest_step(info, key):
    steps = [scalar_value(x) for x in info.get(f"{key}_T", [])]
    steps = [int(x) for x in steps if x is not None]
    return max(steps) if steps else None


def matches_run_prefix(name, prefix):
    return name == prefix or name.startswith(f"{prefix}_")


def load_current_steps(root, map_name, run_prefix, min_t_max):
    steps = []
    run_names = []
    for config_path in Path(root).glob(f"{map_name}/*/config.json"):
        info_path = config_path.with_name("info.json")
        config = read_json(config_path)
        info = read_json(info_path) if info_path.exists() else None
        if config is None or info is None:
            continue
        if config.get("t_max", 0) < min_t_max:
            continue
        alg_name = config.get("running_algorithm_name", "")
        if not matches_run_prefix(alg_name, run_prefix):
            continue
        step = latest_step(info, "test_battle_won_mean")
        if step is not None:
            steps.append(step)
            run_names.append(alg_name)
    return run_names, steps


def main():
    parser = argparse.ArgumentParser(
        description="Lightweight milestone readiness check for long RL runs."
    )
    parser.add_argument("--sacred-root", default="results/sacred/LMAC")
    parser.add_argument("--maps", nargs="+", default=["1o_10b_vs_1r", "1o_2r_vs_4r", "5z_vs_1ul"])
    parser.add_argument("--run-prefix", required=True)
    parser.add_argument("--target-step", type=int, default=500000)
    parser.add_argument("--min-t-max", type=int, default=500000)
    parser.add_argument("--ready-ratio", type=float, default=0.9)
    args = parser.parse_args()

    ready_threshold = int(args.target_step * args.ready_ratio)
    all_ready = True
    summary = {}
    for map_name in args.maps:
        run_names, steps = load_current_steps(
            args.sacred_root, map_name, args.run_prefix, args.min_t_max
        )
        ready_count = sum(step >= ready_threshold for step in steps)
        map_ready = len(steps) > 0 and ready_count == len(steps)
        all_ready = all_ready and map_ready
        summary[map_name] = {
            "runs": len(run_names),
            "ready_runs": ready_count,
            "latest_steps": steps,
            "ready": map_ready,
        }

    for map_name, item in summary.items():
        print(
            f"{map_name}: runs={item['runs']} ready_runs={item['ready_runs']} "
            f"latest_steps={item['latest_steps']} "
            f"{'READY' if item['ready'] else 'PENDING'}"
        )

    if not all_ready:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
