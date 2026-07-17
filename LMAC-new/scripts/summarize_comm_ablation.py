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


def series(info, key):
    values = [scalar_value(x) for x in info.get(key, [])]
    values = [x for x in values if x is not None]
    steps = [scalar_value(x) for x in info.get(f"{key}_T", [])]
    steps = [int(x) for x in steps if x is not None]
    if len(values) != len(steps):
        return []
    return list(zip(steps, values))


def last_value(info, key):
    items = series(info, key)
    return items[-1] if items else (None, None)


def mean(values):
    values = [x for x in values if x is not None]
    return sum(values) / len(values) if values else None


def matches_run_prefix(name, prefix):
    return name == prefix or name.startswith(f"{prefix}_")


def load_eval_runs(root, map_name, run_prefix):
    runs = []
    for config_path in Path(root).glob(f"{map_name}/*/config.json"):
        info_path = config_path.with_name("info.json")
        config = read_json(config_path)
        info = read_json(info_path) if info_path.exists() else None
        if config is None or info is None:
            continue
        alg_name = config.get("running_algorithm_name", "")
        if not matches_run_prefix(alg_name, run_prefix):
            continue
        mode = config.get("eval_comm_ablation", "none")
        runs.append(
            {
                "sacred_id": config_path.parent.name,
                "name": alg_name,
                "mode": mode,
                "info": info,
            }
        )
    return runs


def main():
    parser = argparse.ArgumentParser(
        description="Summarize communication ablation evaluation runs."
    )
    parser.add_argument("--sacred-root", default="results/sacred/LMAC")
    parser.add_argument("--maps", nargs="+", default=["1o_10b_vs_1r", "1o_2r_vs_4r", "5z_vs_1ul"])
    parser.add_argument("--run-prefix", default="comm_ablate")
    parser.add_argument("--min-drop", type=float, default=0.05)
    parser.add_argument("--json-out", default=None)
    args = parser.parse_args()

    result = {
        "_meta": {
            "run_prefix": args.run_prefix,
            "min_drop": args.min_drop,
        }
    }
    failed = False
    for map_name in args.maps:
        runs = load_eval_runs(args.sacred_root, map_name, args.run_prefix)
        grouped = {}
        for run in runs:
            grouped.setdefault(run["mode"], []).append(run)

        mode_stats = {}
        for mode, mode_runs in sorted(grouped.items()):
            wins = []
            returns = []
            steps = []
            for run in mode_runs:
                step, win = last_value(run["info"], "test_battle_won_mean")
                _, ret = last_value(run["info"], "test_return_mean")
                wins.append(win)
                returns.append(ret)
                steps.append(step)
            mode_stats[mode] = {
                "n": len(mode_runs),
                "win": mean(wins),
                "return": mean(returns),
                "used_step": mean(steps),
                "sacred_ids": [run["sacred_id"] for run in mode_runs],
            }

        normal = mode_stats.get("none", {}).get("win")
        zero = mode_stats.get("zero", {}).get("win")
        random_same_rate = mode_stats.get("random_same_rate", {}).get("win")
        drop_certified_edges = mode_stats.get("drop_certified_edges", {}).get("win")
        keep_certified_edges = mode_stats.get("keep_certified_edges", {}).get("win")
        zero_drop = None if normal is None or zero is None else normal - zero
        random_drop = None if normal is None or random_same_rate is None else normal - random_same_rate
        certified_drop = (
            None if normal is None or drop_certified_edges is None
            else normal - drop_certified_edges
        )
        keep_gap = (
            None if normal is None or keep_certified_edges is None
            else normal - keep_certified_edges
        )
        accepted = (
            zero_drop is not None
            and random_drop is not None
            and certified_drop is not None
            and zero_drop >= args.min_drop
            and random_drop >= args.min_drop
            and certified_drop >= args.min_drop
        )
        if not accepted:
            failed = True
        result[map_name] = {
            "modes": mode_stats,
            "zero_drop": zero_drop,
            "random_same_rate_drop": random_drop,
            "certified_edge_drop": certified_drop,
            "keep_certified_edges_gap": keep_gap,
            "accepted": accepted,
        }

        print(f"\nMAP {map_name}")
        for mode in ("none", "zero", "random_same_rate", "drop_certified_edges", "keep_certified_edges"):
            stats = mode_stats.get(mode)
            if stats is None:
                print(f"  {mode}: missing")
            else:
                print(
                    f"  {mode}: n={stats['n']} win={stats['win']} "
                    f"return={stats['return']} used_step={stats['used_step']}"
                )
        print(
            f"  drops: zero={zero_drop} random_same_rate={random_drop} "
            f"certified_edge={certified_drop} keep_certified_gap={keep_gap} "
            f"{'PASS' if accepted else 'PENDING_OR_FAIL'}"
        )

    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2) + "\n")

    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
