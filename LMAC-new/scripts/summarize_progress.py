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


def value_at(info, key, step):
    items = [(t, v) for t, v in series(info, key) if t <= step]
    return items[-1] if items else (None, None)


def matches_run_prefix(name, prefix):
    return name == prefix or name.startswith(f"{prefix}_")


def load_runs(root, map_name, mode, min_t_max):
    runs = []
    for config_path in Path(root).glob(f"{map_name}/*/config.json"):
        info_path = config_path.with_name("info.json")
        if not info_path.exists():
            continue
        config = read_json(config_path)
        info = read_json(info_path)
        if config is None or info is None:
            continue
        if config.get("t_max", 0) < min_t_max:
            continue
        name = config.get("name", "")
        alg_name = config.get("running_algorithm_name", "")
        if mode == "baseline":
            keep = name.startswith("LMAC_Final")
        elif mode == "teacher_student":
            keep = name == "LMAC" and alg_name.startswith("ts_")
        else:
            raise ValueError(f"unknown mode {mode}")
        if keep:
            runs.append((config_path.parent.name, config, info))
    return runs


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--new-sacred", default="results/sacred/LMAC")
    parser.add_argument("--baseline-sacred", default="../LMAC-main/results/sacred/LMAC")
    parser.add_argument("--maps", nargs="+", default=["1o_10b_vs_1r", "1o_2r_vs_4r", "5z_vs_1ul"])
    parser.add_argument("--steps", nargs="+", type=int, default=[500000, 1000000])
    parser.add_argument("--warn-gap", type=float, default=0.2)
    parser.add_argument("--run-prefix", default=None)
    parser.add_argument(
        "--min-current-t-max",
        type=int,
        default=0,
        help="Keep current runs whose configured t_max is at least this value.",
    )
    parser.add_argument(
        "--min-baseline-t-max",
        type=int,
        default=2050000,
        help="Keep baseline runs whose configured t_max is at least this value.",
    )
    parser.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Exit with code 2 if any completed comparison exceeds --warn-gap.",
    )
    args = parser.parse_args()

    saw_warn = False
    for map_name in args.maps:
        baseline = load_runs(args.baseline_sacred, map_name, "baseline", args.min_baseline_t_max)
        current = load_runs(args.new_sacred, map_name, "teacher_student", args.min_current_t_max)
        if args.run_prefix:
            current = [
                run for run in current
                if matches_run_prefix(run[1].get("running_algorithm_name", ""), args.run_prefix)
            ]
        print(f"\nMAP {map_name}: baseline={len(baseline)} teacher_student={len(current)}")
        for step in args.steps:
            base_win_items = [value_at(info, "test_battle_won_mean", step) for _, _, info in baseline]
            cur_win_items = [value_at(info, "test_battle_won_mean", step) for _, _, info in current]
            base_ret_items = [value_at(info, "test_return_mean", step) for _, _, info in baseline]
            cur_ret_items = [value_at(info, "test_return_mean", step) for _, _, info in current]
            base_win = mean(v for _, v in base_win_items)
            cur_win = mean(v for _, v in cur_win_items)
            base_ret = mean(v for _, v in base_ret_items)
            cur_ret = mean(v for _, v in cur_ret_items)
            base_step = mean(t for t, _ in base_win_items)
            cur_step = mean(t for t, _ in cur_win_items)
            gap = None if base_win is None or cur_win is None else base_win - cur_win
            status = "OK"
            if cur_step is None or cur_step < step * 0.9:
                status = "PENDING"
            elif gap is not None and gap > args.warn_gap:
                status = "WARN"
                saw_warn = True
            print(
                f"  step={step} baseline_win={base_win} current_win={cur_win} "
                f"gap={gap} baseline_return={base_ret} current_return={cur_ret} "
                f"baseline_used_step={base_step} current_used_step={cur_step} {status}"
            )

    if args.fail_on_warn and saw_warn:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
