#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


COMM_ROOT = Path("src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05")
DEFAULT_MAPS = ["1o_10b_vs_1r", "1o_2r_vs_4r", "5z_vs_1ul"]


def run_cmd(cmd):
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout


def static_cert(map_name, out_dir):
    comm_dir = COMM_ROOT / map_name
    out_path = out_dir / f"cert_{map_name}.json"
    cmd = [
        sys.executable,
        "scripts/certify_llm_comm.py",
        "--map",
        map_name,
        "--comm-code",
        str(comm_dir / "comm_init.py"),
        "--comm-code",
        str(comm_dir / "comm_update.py"),
        "--comm-code",
        str(comm_dir / "comm_update_timestep_wise2.py"),
        "--out",
        str(out_path),
    ]
    code, text = run_cmd(cmd)
    if code != 0:
        return False, text
    data = json.loads(out_path.read_text())
    return bool(data.get("accepted")), text


def progress_check(args):
    cmd = [
        sys.executable,
        "scripts/milestone_monitor.py",
        "--new-sacred",
        args.new_sacred,
        "--baseline-sacred",
        args.baseline_sacred,
        "--run-prefix",
        args.run_prefix,
        "--min-t-max",
        str(args.min_current_t_max),
        "--warn-gap",
        str(args.warn_gap),
        "--milestones",
        *[str(s) for s in args.steps],
    ]
    return run_cmd(cmd)


def main():
    parser = argparse.ArgumentParser(
        description="Gate a candidate LLM communication implementation before long training."
    )
    parser.add_argument("--maps", nargs="+", default=DEFAULT_MAPS)
    parser.add_argument("--out-dir", default="description/certification_gate")
    parser.add_argument("--run-prefix", default="ts_receiverfix")
    parser.add_argument("--new-sacred", default="results/sacred/LMAC")
    parser.add_argument("--baseline-sacred", default="/data/hp/LLM_Communication/LMAC-main/results/sacred/LMAC")
    parser.add_argument("--steps", nargs="+", type=int, default=[500000])
    parser.add_argument("--min-current-t-max", type=int, default=500000)
    parser.add_argument("--warn-gap", type=float, default=0.2)
    parser.add_argument(
        "--static-only",
        action="store_true",
        help="Only run static LLM communication certificates. Use this before launching training.",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    failed = False
    print("== Static LLM communication certificate ==")
    for map_name in args.maps:
        ok, text = static_cert(map_name, out_dir)
        print(f"\n[{map_name}] {'PASS' if ok else 'FAIL'}")
        print(text)
        failed = failed or not ok

    if args.static_only:
        raise SystemExit(1 if failed else 0)

    print("\n== Low-frequency milestone progress gate ==")
    code, text = progress_check(args)
    print(text)
    if code == 2:
        print("Progress gate found a completed WARN comparison. Stop and debug before longer training.")
        failed = True
    elif code != 0:
        print(f"Progress gate failed with exit code {code}.")
        failed = True

    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
