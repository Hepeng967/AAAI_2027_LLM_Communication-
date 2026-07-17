#!/usr/bin/env python3
"""Preflight checks before running formal DRC teacher certification."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def load_json(path):
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def run_json(cmd):
    proc = subprocess.run(cmd, check=True, text=True, capture_output=True)
    return json.loads(proc.stdout)


def normalize_path(path):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    try:
        return str(p.resolve())
    except FileNotFoundError:
        return str(p.absolute())


def summarize_candidate_manifest(path, maps):
    item = load_json(path)
    if item is None:
        return {
            "name": "candidate_manifest",
            "passes": False,
            "reason": "missing",
            "path": path,
        }
    rows = [row for row in item.get("candidates", []) if row.get("map") in maps]
    valid = [row for row in rows if row.get("valid_for_drc_search")]
    missing_paths = []
    missing_hashes = []
    for row in rows:
        p = Path(normalize_path(row.get("path", "")))
        if not p.exists():
            missing_paths.append(row)
        if not row.get("sha256"):
            missing_hashes.append(row)
    return {
        "name": "candidate_manifest",
        "passes": bool(rows) and len(valid) == len(rows) and not missing_paths and not missing_hashes,
        "path": path,
        "manifest_sha256": item.get("manifest_sha256"),
        "candidate_count_for_maps": len(rows),
        "valid_candidate_count_for_maps": len(valid),
        "missing_paths": missing_paths,
        "missing_hashes": missing_hashes,
    }


def summarize_buffer_audit(buffer_root, maps, max_files, require_metadata):
    audit = run_json(
        [
            PYTHON,
            str(ROOT / "scripts" / "audit_drc_buffers.py"),
            "--buffer-root",
            str(buffer_root),
            "--maps",
            *maps,
            "--max-files",
            str(max_files),
        ]
    )
    summaries = {name: data.get("summary", {}) for name, data in audit.get("maps", {}).items()}
    failed = {name: summary for name, summary in summaries.items() if not summary.get("formal_ready")}
    metadata_failed = {
        name: summary
        for name, summary in summaries.items()
        if require_metadata and summary.get("metadata_ok_coverage") != 1.0
    }
    return {
        "name": "buffer_audit",
        "passes": bool(summaries) and not failed and not metadata_failed,
        "buffer_root": str(buffer_root),
        "max_files": max_files,
        "require_metadata": require_metadata,
        "maps": summaries,
        "failed_maps": failed,
        "metadata_failed_maps": metadata_failed,
        "raw_audit": audit,
    }


def write_protocol_snapshot(args, out_dir):
    protocol_json = out_dir / "preflight_drc_protocol.json"
    protocol_md = out_dir / "preflight_drc_protocol.md"
    cmd = [
        PYTHON,
        str(ROOT / "scripts" / "write_drc_protocol.py"),
        "--buffer-root",
        str(args.buffer_root),
        "--maps",
        *args.maps,
        "--audit-max-files",
        str(args.audit_max_files),
        "--max-files",
        str(args.max_files),
        "--max-transitions",
        str(args.max_transitions),
        "--probe-model",
        args.probe_model,
        "--probe-hidden-dim",
        str(args.probe_hidden_dim),
        "--probe-weight-decay",
        str(args.probe_weight_decay),
        "--probe-epochs",
        str(args.probe_epochs),
        "--decision-oracle",
        args.decision_oracle,
        "--decision-label",
        args.decision_label,
        "--min-conditional-decision-nats",
        str(args.min_conditional_decision_nats),
        "--conditional-decision-mode",
        args.conditional_decision_mode,
        "--conditional-decision-quantile",
        str(args.conditional_decision_quantile),
        "--min-conditional-decision-samples",
        str(args.min_conditional_decision_samples),
        "--min-receiver-necessity-rate",
        str(args.min_receiver_necessity_rate),
        "--score-gain-cap",
        str(args.score_gain_cap),
        "--n-bootstrap",
        str(args.n_bootstrap),
        "--n-sign-permutations",
        str(args.n_sign_permutations),
        "--n-message-shuffles",
        str(args.n_message_shuffles),
        "--stat-alpha",
        str(args.stat_alpha),
        "--candidate-manifest",
        str(args.candidate_manifest),
        "--out-json",
        str(protocol_json),
        "--out-md",
        str(protocol_md),
    ]
    if args.fact_subset_manifest:
        cmd.extend(["--fact-subset-manifest", str(args.fact_subset_manifest)])
    if args.require_stat_significance:
        cmd.append("--require-stat-significance")
    if args.require_content_control:
        cmd.append("--require-content-control")
    proc = subprocess.run(cmd, check=True, text=True, capture_output=True)
    protocol = json.loads(proc.stdout)
    return {
        "name": "protocol_snapshot",
        "passes": bool(protocol.get("protocol_sha256")) and bool(protocol.get("candidates")),
        "protocol_sha256": protocol.get("protocol_sha256"),
        "path_json": str(protocol_json),
        "path_md": str(protocol_md),
        "candidate_count": len(protocol.get("candidates", [])),
    }


def command_block(args, out_dir):
    env = {
        "RUN_MAPS": " ".join(args.maps),
        "BUFFER_ROOT": str(args.buffer_root),
        "CANDIDATE_MANIFEST": str(args.candidate_manifest),
        "FACT_SUBSET_MANIFEST": str(args.fact_subset_manifest),
        "OUT_ROOT": str(args.formal_out_root or (out_dir / "formal_drc_v5")),
        "PROBE_MODEL": args.probe_model,
        "PROBE_HIDDEN_DIM": str(args.probe_hidden_dim),
        "PROBE_WEIGHT_DECAY": str(args.probe_weight_decay),
        "PROBE_EPOCHS": str(args.probe_epochs),
        "MAX_FILES": str(args.max_files),
        "MAX_TRANSITIONS": str(args.max_transitions),
        "AUDIT_MAX_FILES": str(args.audit_max_files),
        "DECISION_ORACLE": args.decision_oracle,
        "DECISION_LABEL": args.decision_label,
        "MIN_CONDITIONAL_DECISION_NATS": str(args.min_conditional_decision_nats),
        "CONDITIONAL_DECISION_MODE": args.conditional_decision_mode,
        "CONDITIONAL_DECISION_QUANTILE": str(args.conditional_decision_quantile),
        "MIN_CONDITIONAL_DECISION_SAMPLES": str(args.min_conditional_decision_samples),
        "MIN_RECEIVER_NECESSITY_RATE": str(args.min_receiver_necessity_rate),
        "SCORE_GAIN_CAP": str(args.score_gain_cap),
        "N_BOOTSTRAP": str(args.n_bootstrap),
        "N_SIGN_PERMUTATIONS": str(args.n_sign_permutations),
        "N_MESSAGE_SHUFFLES": str(args.n_message_shuffles),
        "STAT_ALPHA": str(args.stat_alpha),
        "REQUIRE_STAT_SIGNIFICANCE": str(args.require_stat_significance).lower(),
        "REQUIRE_CONTENT_CONTROL": str(args.require_content_control).lower(),
    }
    prefix = " ".join(f'{key}="{value}"' for key, value in env.items())
    return {
        "formal_drc_command": f"{prefix} bash {ROOT / 'scripts' / 'run_formal_drc_v5.sh'}",
        "collect_buffer_command": (
            f'MAPS="<short map aliases>" RUN_MAPS="{" ".join(args.maps)}" '
            f"bash {ROOT / 'scripts' / 'collect_formal_drc_buffers.sh'}"
        ),
    }


def write_md(path, report):
    lines = [
        "# DRC Formal Run Preflight",
        "",
        f"- ready: `{report['ready']}`",
        f"- output root: `{report['out_dir']}`",
        "",
        "## Checks",
        "",
        "| check | pass | details |",
        "| --- | --- | --- |",
    ]
    for check in report["checks"]:
        details = {k: v for k, v in check.items() if k not in ("name", "passes", "raw_audit")}
        lines.append(f"| {check['name']} | {check['passes']} | `{json.dumps(details, sort_keys=True)}` |")
    lines += [
        "",
        "## Commands",
        "",
        "Formal DRC command:",
        "",
        "```bash",
        report["commands"]["formal_drc_command"],
        "```",
        "",
        "If buffers are not ready, collect formal buffers first:",
        "",
        "```bash",
        report["commands"]["collect_buffer_command"],
        "```",
        "",
        "## Interpretation",
        "",
        "Run formal DRC only when `ready` is true. A failed preflight usually means "
        "the candidate manifest is missing/invalid, buffers do not include "
        "reward/terminated fields, shapes do not match the teacher interface, or "
        "the protocol snapshot cannot be hashed.",
    ]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Preflight a formal DRC run.")
    parser.add_argument("--buffer-root", required=True)
    parser.add_argument("--candidate-manifest", required=True)
    parser.add_argument("--fact-subset-manifest", default="")
    parser.add_argument("--maps", nargs="+", default=["1o_10b_vs_1r", "5z_vs_1ul"])
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--formal-out-root", default="")
    parser.add_argument("--audit-max-files", type=int, default=64)
    parser.add_argument("--max-files", type=int, default=64)
    parser.add_argument("--max-transitions", type=int, default=4096)
    parser.add_argument("--probe-model", choices=["linear", "mlp"], default="mlp")
    parser.add_argument("--probe-hidden-dim", type=int, default=128)
    parser.add_argument("--probe-weight-decay", type=float, default=1e-4)
    parser.add_argument("--probe-epochs", type=int, default=120)
    parser.add_argument("--decision-oracle", choices=["auto", "behavior", "return"], default="auto")
    parser.add_argument("--decision-label", choices=["raw_action", "action_group"], default="raw_action")
    parser.add_argument("--min-conditional-decision-nats", type=float, default=0.01)
    parser.add_argument("--conditional-decision-mode", choices=["none", "local_entropy", "local_loss"], default="none")
    parser.add_argument("--conditional-decision-quantile", type=float, default=0.25)
    parser.add_argument("--min-conditional-decision-samples", type=int, default=256)
    parser.add_argument("--min-receiver-necessity-rate", type=float, default=1.0)
    parser.add_argument("--score-gain-cap", type=float, default=1.0)
    parser.add_argument("--n-bootstrap", type=int, default=500)
    parser.add_argument("--n-sign-permutations", type=int, default=500)
    parser.add_argument("--n-message-shuffles", type=int, default=16)
    parser.add_argument("--stat-alpha", type=float, default=0.05)
    parser.add_argument("--require-stat-significance", action="store_true", default=True)
    parser.add_argument("--no-require-stat-significance", dest="require_stat_significance", action="store_false")
    parser.add_argument("--require-content-control", action="store_true", default=True)
    parser.add_argument("--no-require-content-control", dest="require_content_control", action="store_false")
    parser.add_argument("--require-metadata", action="store_true", default=True)
    parser.add_argument("--no-require-metadata", dest="require_metadata", action="store_false")
    parser.add_argument("--out-json", default="")
    parser.add_argument("--out-md", default="")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    checks = [
        summarize_candidate_manifest(args.candidate_manifest, set(args.maps)),
        summarize_buffer_audit(args.buffer_root, args.maps, args.audit_max_files, args.require_metadata),
        write_protocol_snapshot(args, out_dir),
    ]
    report = {
        "method": "DRC-formal-run-preflight-v1",
        "ready": all(check["passes"] for check in checks),
        "out_dir": str(out_dir),
        "inputs": {
            "buffer_root": str(args.buffer_root),
            "candidate_manifest": str(args.candidate_manifest),
            "fact_subset_manifest": str(args.fact_subset_manifest),
            "maps": args.maps,
        },
        "checks": checks,
        "commands": command_block(args, out_dir),
    }

    out_json = Path(args.out_json) if args.out_json else out_dir / "preflight_report.json"
    out_md = Path(args.out_md) if args.out_md else out_dir / "preflight_report.md"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2) + "\n")
    write_md(out_md, report)
    print(json.dumps({"ready": report["ready"], "out_json": str(out_json), "out_md": str(out_md)}, indent=2))
    if not report["ready"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
