"""Append-only trial ledger and report generation."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def append_trial(path: Path, entry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    item = {"timestamp": utc_now(), **entry}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(item, sort_keys=True, ensure_ascii=False) + "\n")


def read_trials(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_summary_csv(trials_path: Path, summary_path: Path) -> None:
    rows = read_trials(trials_path)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "timestamp",
        "map_name",
        "iteration",
        "candidate",
        "stage",
        "valid",
        "accepted",
        "score",
        "who_score",
        "when_score",
        "what_score",
        "decision_gain",
        "causal_gain",
        "edge_rate",
        "message_dim",
        "status",
        "failure_analysis",
        "next_hypothesis",
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: _field(row, field) for field in fields})


def write_report(trials_path: Path, report_path: Path) -> None:
    rows = read_trials(trials_path)
    lines = [
        "# HL Communication Auto-Research Report",
        "",
        f"- trials: `{len(rows)}`",
        "",
        "| map | iter | stage | valid | accepted | score | decision | causal | candidate |",
        "| --- | ---: | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {_fmt(row.get('map_name'))} | {_fmt(row.get('iteration'))} | {_fmt(row.get('stage'))} | "
            f"{_fmt(row.get('valid'))} | {_fmt(row.get('accepted'))} | {_fmt(row.get('score'))} | "
            f"{_fmt(row.get('decision_gain'))} | {_fmt(row.get('causal_gain'))} | {_fmt(row.get('candidate'))} |"
        )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def refresh_outputs(trials_path: Path, summary_path: Path, report_path: Path) -> None:
    write_summary_csv(trials_path, summary_path)
    write_report(trials_path, report_path)


def _field(row: dict[str, Any], field: str) -> Any:
    if field in row:
        return row[field]
    if field == "edge_rate":
        return row.get("matrix_edge_rate")
    if field == "message_dim":
        return row.get("validation", {}).get("message_dim") or row.get("message_dim")
    return ""


def _fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)
