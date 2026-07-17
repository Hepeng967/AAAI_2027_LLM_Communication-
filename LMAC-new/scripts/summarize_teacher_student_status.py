#!/usr/bin/env python3
import argparse
import csv
import json
import os
import re
import signal
from pathlib import Path


T_ENV_RE = re.compile(r"t_env:\s*([0-9]+)\s*/\s*([0-9]+)")
RECENT_T_ENV_RE = re.compile(r"Recent Stats \| t_env:\s*([0-9]+)")
STAT_RE = re.compile(
    r"\[INFO [^\]]+\] my_main ([A-Za-z0-9_./-]+):\s*([-+0-9.eE]+)"
)
KV_RE = re.compile(r"([A-Za-z0-9_./-]+):\s*([-+0-9.eE]+)")


def is_running(pid: str) -> bool:
    try:
        os.kill(int(pid), 0)
        return True
    except (ValueError, ProcessLookupError):
        return False
    except PermissionError:
        return True


def read_status(path: Path):
    if not path.exists():
        return "", ""
    end_code = ""
    end_utc = ""
    with path.open() as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row.get("event") == "end":
                end_utc = row.get("utc", "")
                end_code = row.get("code", "")
    return end_utc, end_code


def parse_log(path: Path):
    latest_t = ""
    target_t = ""
    last_stats = {}
    if not path.exists():
        return latest_t, target_t, last_stats
    try:
        with path.open(errors="replace") as f:
            for line in f:
                m = T_ENV_RE.search(line)
                if m:
                    latest_t, target_t = m.group(1), m.group(2)
                recent = RECENT_T_ENV_RE.search(line)
                if recent:
                    latest_t = recent.group(1)
                s = STAT_RE.search(line)
                if s:
                    key, value = s.group(1), s.group(2)
                    if key in {
                        "test_battle_won_mean",
                        "test_return_mean",
                        "Teacher_comm_loss",
                        "Student_comm_rate",
                        "loss",
                    }:
                        last_stats[key] = value
                for key, value in KV_RE.findall(line):
                    if key in {
                        "test_battle_won_mean",
                        "test_return_mean",
                        "Teacher_comm_loss",
                        "Student_comm_rate",
                        "loss",
                    }:
                        last_stats[key] = value
    except OSError as exc:
        last_stats["log_error"] = str(exc)
    return latest_t, target_t, last_stats


def build_sacred_index(root: Path):
    index = {}
    sacred_root = root / "results" / "sacred" / "LMAC"
    if not sacred_root.exists():
        return index
    for config_path in sacred_root.glob("*/*/config.json"):
        try:
            with config_path.open() as f:
                config = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        map_name = config.get("env_args", {}).get("map_name")
        seed = str(config.get("seed", ""))
        run_name = str(config.get("running_algorithm_name", ""))
        if not map_name or not seed or not run_name:
            continue
        index[(map_name, seed, run_name)] = config_path.parent
    return index


def latest_sacred_metrics(run_dir: Path):
    metrics_path = run_dir / "metrics.json"
    if not metrics_path.exists():
        return {}, ""
    try:
        with metrics_path.open() as f:
            metrics = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}, ""

    out = {}
    max_step = ""
    for key in [
        "test_battle_won_mean",
        "test_return_mean",
        "Teacher_comm_loss",
        "Student_comm_rate",
        "loss",
    ]:
        values = metrics.get(key, {}).get("values", [])
        steps = metrics.get(key, {}).get("steps", [])
        if values:
            out[key] = str(values[-1])
        if steps:
            try:
                max_step = str(max(int(max_step or 0), int(steps[-1])))
            except ValueError:
                max_step = str(steps[-1])
    return out, max_step


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_root", type=Path)
    args = parser.parse_args()

    pid_file = args.run_root / "pids.tsv"
    if not pid_file.exists():
        raise SystemExit(f"missing pid file: {pid_file}")

    repo_root = Path(__file__).resolve().parents[1]
    sacred_index = build_sacred_index(repo_root)

    fields = [
        "map",
        "seed_idx",
        "seed",
        "gpu",
        "pid",
        "running",
        "end_code",
        "t_env",
        "t_max",
        "metric_step",
        "test_battle_won_mean",
        "test_return_mean",
        "Teacher_comm_loss",
        "Student_comm_rate",
        "log",
    ]
    print("\t".join(fields))
    with pid_file.open() as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            log = Path(row["log"])
            status = log.with_name("status.tsv")
            _, end_code = read_status(status)
            t_env, t_max, log_stats = parse_log(log)
            stats = {}
            metric_step = ""
            sacred_dir = sacred_index.get((row["map"], row["seed"], log.parent.name))
            if sacred_dir is not None:
                sacred_stats, metric_step = latest_sacred_metrics(sacred_dir)
                stats.update({k: v for k, v in sacred_stats.items() if v != ""})
            try:
                log_step_num = int(t_env or 0)
                metric_step_num = int(metric_step or 0)
            except ValueError:
                log_step_num = metric_step_num = 0
            if log_step_num >= metric_step_num:
                stats.update({k: v for k, v in log_stats.items() if v != ""})
            out = {
                **row,
                "running": str(is_running(row["pid"])).lower(),
                "end_code": end_code,
                "t_env": t_env,
                "t_max": t_max,
                "metric_step": metric_step,
                "test_battle_won_mean": stats.get("test_battle_won_mean", ""),
                "test_return_mean": stats.get("test_return_mean", ""),
                "Teacher_comm_loss": stats.get("Teacher_comm_loss", ""),
                "Student_comm_rate": stats.get("Student_comm_rate", ""),
            }
            print("\t".join(out.get(k, "") for k in fields))


if __name__ == "__main__":
    main()
