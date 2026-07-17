"""Subprocess wrappers around the existing LMAC DRC scripts."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


def run_command(cmd: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> dict[str, Any]:
    proc = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "ok": proc.returncode == 0,
    }


def validate_with_script(*, map_name: str, comm_code: Path, out_json: Path, python: str = sys.executable) -> dict[str, Any]:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    result = run_command(
        [
            python,
            "scripts/validate_drc_comm_code.py",
            "--map",
            map_name,
            "--comm-code",
            str(comm_code),
            "--out-json",
            str(out_json),
        ]
    )
    if result["ok"] and out_json.exists():
        result["report"] = json.loads(out_json.read_text(encoding="utf-8"))
    return result


def run_drc(
    *,
    map_name: str,
    comm_code: Path,
    buffer_root: Path,
    out_json: Path,
    out_md: Path,
    max_files: int,
    max_transitions: int,
    python: str = sys.executable,
    decision_label: str = "raw_action",
    conditional_decision_mode: str = "local_loss",
    probe_model: str = "mlp",
    require_content_control: bool = True,
    require_stat_significance: bool = False,
) -> dict[str, Any]:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        python,
        "scripts/certify_decision_relevant_comm.py",
        "--map",
        map_name,
        "--comm-code",
        str(comm_code),
        "--buffer-root",
        str(buffer_root),
        "--decision-label",
        decision_label,
        "--conditional-decision-mode",
        conditional_decision_mode,
        "--probe-model",
        probe_model,
        "--max-files",
        str(max_files),
        "--max-transitions",
        str(max_transitions),
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]
    if require_content_control:
        cmd.append("--require-content-control")
    if require_stat_significance:
        cmd.append("--require-stat-significance")
    result = run_command(cmd)
    if result["ok"] and out_json.exists():
        result["report"] = json.loads(out_json.read_text(encoding="utf-8"))
    return result


def select_teacher(*, search_root: Path, out_json: Path, out_md: Path, python: str = sys.executable) -> dict[str, Any]:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    return run_command(
        [
            python,
            "scripts/select_drc_teacher.py",
            "--search-root",
            str(search_root),
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
        ]
    )


def launch_teacher_student_rl(
    *,
    map_name: str,
    manifest: Path,
    run_root: Path,
) -> dict[str, Any]:
    env = os.environ.copy()
    env.update({"RUN_MAPS": map_name, "FROZEN_TEACHER_MANIFEST": str(manifest), "RUN_ROOT": str(run_root)})
    from components.certified_task_facts import map_specs

    environment = map_specs().get(map_name, {}).get("environment", "smac")
    script = (
        "scripts/launch_extended_env_teacher_student.sh"
        if environment in {"hallway", "hallway_group", "grf"}
        else "scripts/launch_teacher_student_eval.sh"
    )
    return run_command(["bash", script], env=env)


def summarize_drc_report(report: dict[str, Any]) -> dict[str, Any]:
    scores = report.get("scores", {})
    decision = report.get("decision_sufficiency", {})
    causal = report.get("causal_usefulness", {})
    return {
        "accepted": report.get("accepted"),
        "score": scores.get("final_score"),
        "sender_observable_rate": scores.get("sender_observable_rate"),
        "receiver_necessary_rate": scores.get("receiver_necessary_rate"),
        "task_fact_completeness": scores.get("task_fact_completeness"),
        "decision_sufficient": decision.get("passes_decision_sufficient"),
        "decision_gain": scores.get("decision_sufficiency_gain"),
        "causally_useful": causal.get("passes_causally_useful"),
        "causal_gain": scores.get("causal_usefulness"),
        "matrix_edge_rate": report.get("matrix_edge_rate"),
        "message_dim": report.get("message_dim"),
        "comm_code": report.get("comm_code"),
    }
