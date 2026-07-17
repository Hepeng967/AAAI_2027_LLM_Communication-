#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def read_json(path):
    try:
        text = path.read_text()
        if not text.strip():
            return None
        return json.loads(text)
    except (OSError, json.JSONDecodeError):
        return None


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


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


def readiness(sacred_root, maps, run_prefix, milestone, min_t_max, ready_ratio):
    threshold = int(milestone * ready_ratio)
    summary = {}
    all_ready = True
    for map_name in maps:
        run_names, steps = load_current_steps(sacred_root, map_name, run_prefix, min_t_max)
        ready_count = sum(step >= threshold for step in steps)
        ready = len(steps) > 0 and ready_count == len(steps)
        all_ready = all_ready and ready
        summary[map_name] = {
            "runs": len(run_names),
            "ready_runs": ready_count,
            "latest_steps": steps,
            "ready": ready,
        }
    return all_ready, summary


def run_summary(args, milestone):
    cmd = [
        sys.executable,
        "scripts/summarize_progress.py",
        "--new-sacred",
        args.new_sacred,
        "--baseline-sacred",
        args.baseline_sacred,
        "--run-prefix",
        args.run_prefix,
        "--steps",
        str(milestone),
        "--min-current-t-max",
        str(args.min_t_max),
        "--warn-gap",
        str(args.warn_gap),
        "--fail-on-warn",
    ]
    for map_name in args.maps:
        cmd.extend(["--maps", map_name])
    # argparse with nargs expects maps after one flag, so rebuild this part cleanly.
    cmd = [
        sys.executable,
        "scripts/summarize_progress.py",
        "--new-sacred",
        args.new_sacred,
        "--baseline-sacred",
        args.baseline_sacred,
        "--maps",
        *args.maps,
        "--run-prefix",
        args.run_prefix,
        "--steps",
        str(milestone),
        "--min-current-t-max",
        str(args.min_t_max),
        "--warn-gap",
        str(args.warn_gap),
        "--fail-on-warn",
    ]
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Low-frequency experiment monitor. It only runs the expensive progress "
            "comparison once a configured milestone is ready."
        )
    )
    parser.add_argument("--new-sacred", default="results/sacred/LMAC")
    parser.add_argument("--baseline-sacred", default="/data/hp/LLM_Communication/LMAC-main/results/sacred/LMAC")
    parser.add_argument("--maps", nargs="+", default=["1o_10b_vs_1r", "1o_2r_vs_4r", "5z_vs_1ul"])
    parser.add_argument("--run-prefix", required=True)
    parser.add_argument("--milestones", nargs="+", type=int, default=[500000, 1000000])
    parser.add_argument("--min-t-max", type=int, default=500000)
    parser.add_argument("--ready-ratio", type=float, default=0.9)
    parser.add_argument("--warn-gap", type=float, default=0.2)
    parser.add_argument("--force", action="store_true", help="Re-run summary even if this milestone was already reported.")
    parser.add_argument(
        "--state-file",
        default="description/certification_gate/milestone_monitor_state.json",
        help="Records reported milestones so repeated checks stay quiet.",
    )
    parser.add_argument(
        "--json-out",
        default=None,
        help="Optional path for the latest monitor report.",
    )
    args = parser.parse_args()

    state_path = Path(args.state_file)
    state = read_json(state_path) or {}
    reported = set(state.get(args.run_prefix, {}).get("reported_milestones", []))
    report = {
        "run_prefix": args.run_prefix,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "milestones": {},
        "selected_milestone": None,
        "status": "PENDING",
    }

    selected = None
    for milestone in sorted(args.milestones):
        ready, item = readiness(
            args.new_sacred,
            args.maps,
            args.run_prefix,
            milestone,
            args.min_t_max,
            args.ready_ratio,
        )
        report["milestones"][str(milestone)] = item
        if ready and (args.force or milestone not in reported):
            selected = milestone
            break

    if selected is None:
        print("No new ready milestone. Skipping full progress comparison.")
        for milestone, item in report["milestones"].items():
            compact = {
                map_name: {
                    "runs": map_item["runs"],
                    "ready_runs": map_item["ready_runs"],
                    "latest_steps": map_item["latest_steps"],
                }
                for map_name, map_item in item.items()
            }
            print(f"milestone={milestone} {compact}")
        if args.json_out:
            write_json(Path(args.json_out), report)
        return 0

    print(f"Milestone {selected} is ready. Running formal LMAC-main comparison.")
    result = run_summary(args, selected)
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    report["selected_milestone"] = selected
    report["summary_returncode"] = result.returncode
    report["summary_stdout"] = result.stdout
    report["summary_stderr"] = result.stderr
    report["status"] = "WARN" if result.returncode == 2 else "OK" if result.returncode == 0 else "ERROR"

    if not args.force:
        state.setdefault(args.run_prefix, {}).setdefault("reported_milestones", [])
        if selected not in state[args.run_prefix]["reported_milestones"]:
            state[args.run_prefix]["reported_milestones"].append(selected)
            state[args.run_prefix]["reported_milestones"].sort()
        state[args.run_prefix]["last_checked_utc"] = report["checked_at_utc"]
        state[args.run_prefix]["last_status"] = report["status"]
        write_json(state_path, state)

    if args.json_out:
        write_json(Path(args.json_out), report)

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
