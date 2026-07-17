#!/usr/bin/env python3
"""Audit whether DRC artifacts are ready to be treated as formal evidence."""

import argparse
import json
from pathlib import Path


REQUIRED_CERT_SETTINGS = {
    "require_stat_significance": True,
    "require_content_control": True,
}

REQUIRED_FORMAL_GATES = {
    "sender_observable",
    "receiver_necessary",
    "task_fact_complete",
    "decision_sufficient",
    "causally_useful",
}


def load_json(path):
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def check_candidate_manifest(path):
    item = load_json(path)
    if item is None:
        return {"name": "candidate_manifest", "passes": False, "reason": "missing"}
    count = item.get("candidate_count", 0)
    valid = item.get("valid_candidate_count", 0)
    rows = item.get("candidates", [])
    hashes_ok = all(row.get("sha256") for row in rows)
    return {
        "name": "candidate_manifest",
        "passes": count > 0 and valid == count and hashes_ok,
        "candidate_count": count,
        "valid_candidate_count": valid,
        "hashes_present": hashes_ok,
        "manifest_sha256": item.get("manifest_sha256"),
    }


def check_buffer_audit(path):
    item = load_json(path)
    if item is None:
        return {"name": "buffer_audit", "passes": False, "reason": "missing"}
    maps = item.get("maps", {})
    summaries = {name: data.get("summary", {}) for name, data in maps.items()}
    failed = {
        name: summary
        for name, summary in summaries.items()
        if not summary.get("formal_ready")
    }
    metadata_failed = {
        name: summary
        for name, summary in summaries.items()
        if summary.get("metadata_ok_coverage") != 1.0
    }
    return {
        "name": "buffer_audit",
        "passes": bool(summaries) and not failed and not metadata_failed,
        "maps": summaries,
        "failed_maps": failed,
        "metadata_failed_maps": metadata_failed,
    }


def check_protocol(path):
    item = load_json(path)
    if item is None:
        return {"name": "protocol", "passes": False, "reason": "missing"}
    cert = item.get("certification", {})
    missing_settings = {
        key: expected
        for key, expected in REQUIRED_CERT_SETTINGS.items()
        if cert.get(key) != expected
    }
    has_hash = bool(item.get("protocol_sha256"))
    has_candidates = bool(item.get("candidates"))
    has_receiver_threshold = "min_receiver_necessity_rate" in cert
    has_conditional_decision_threshold = "min_conditional_decision_nats" in cert
    has_conditional_decision_mode = "conditional_decision_mode" in cert
    has_conditional_decision_quantile = "conditional_decision_quantile" in cert
    has_min_conditional_decision_samples = "min_conditional_decision_samples" in cert
    has_score_gain_cap = "score_gain_cap" in cert
    return {
        "name": "protocol",
        "passes": (
            has_hash
            and has_candidates
            and has_receiver_threshold
            and has_conditional_decision_threshold
            and has_conditional_decision_mode
            and has_conditional_decision_quantile
            and has_min_conditional_decision_samples
            and has_score_gain_cap
            and not missing_settings
        ),
        "protocol_sha256": item.get("protocol_sha256"),
        "has_candidates": has_candidates,
        "has_receiver_threshold": has_receiver_threshold,
        "has_conditional_decision_threshold": has_conditional_decision_threshold,
        "has_conditional_decision_mode": has_conditional_decision_mode,
        "has_conditional_decision_quantile": has_conditional_decision_quantile,
        "has_min_conditional_decision_samples": has_min_conditional_decision_samples,
        "has_score_gain_cap": has_score_gain_cap,
        "missing_or_mismatched_settings": missing_settings,
    }


def iter_drc_results(search_root):
    root = Path(search_root)
    for path in sorted(root.glob("*.json")):
        try:
            item = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if "map_name" in item and "scores" in item:
            yield path, item


def check_teacher_search(path):
    if not path:
        return {"name": "teacher_search", "passes": False, "reason": "missing"}
    root = Path(path)
    if not root.exists():
        return {"name": "teacher_search", "passes": False, "reason": "missing"}
    rows = list(iter_drc_results(root))
    accepted = [(p, item) for p, item in rows if item.get("accepted")]
    formal_accepted = []
    accepted_with_missing_gates = []
    for p, item in accepted:
        cert = item.get("formal_certificate", {})
        gate_names = {row.get("gate") for row in cert.get("gates", [])}
        missing_gates = sorted(REQUIRED_FORMAL_GATES - gate_names)
        if item.get("has_return_data") and item.get("passes_statistical_gate") and item.get("passes_content_gate") and not missing_gates:
            formal_accepted.append((p, item))
        elif missing_gates:
            accepted_with_missing_gates.append({"file": str(p), "missing_gates": missing_gates})
    maps_with_formal = sorted({item["map_name"] for _, item in formal_accepted})
    return {
        "name": "teacher_search",
        "passes": bool(formal_accepted),
        "num_results": len(rows),
        "num_accepted": len(accepted),
        "num_formal_accepted": len(formal_accepted),
        "maps_with_formal_accepted": maps_with_formal,
        "accepted_with_missing_formal_gates": accepted_with_missing_gates,
        "summary_exists": (root / "summary.md").exists(),
    }


def check_frozen_manifest(path, require_robust=False):
    item = load_json(path)
    if item is None:
        return {"name": "frozen_manifest", "passes": False, "reason": "missing"}
    teachers = item.get("teachers", {})
    robust_ok = True
    if require_robust:
        robust_ok = item.get("method") == "DRC-robust-frozen-teacher-selection" and all(
            row.get("robust_evidence") for row in teachers.values()
        )
    paths_exist = {}
    for map_name, row in teachers.items():
        p = Path(row.get("teacher_path", ""))
        if not p.is_absolute():
            p = Path(__file__).resolve().parents[1] / p
        paths_exist[map_name] = p.exists()
    return {
        "name": "frozen_manifest",
        "passes": bool(teachers) and all(paths_exist.values()) and robust_ok,
        "method": item.get("method"),
        "num_teachers": len(teachers),
        "paths_exist": paths_exist,
        "requires_robust": require_robust,
        "robust_ok": robust_ok,
    }


def write_md(path, report):
    lines = [
        "# DRC Formal Readiness Audit",
        "",
        f"- formal ready: `{report['formal_ready']}`",
        "",
        "| check | pass | details |",
        "| --- | --- | --- |",
    ]
    for check in report["checks"]:
        details = {k: v for k, v in check.items() if k not in ("name", "passes")}
        lines.append(f"| {check['name']} | {check['passes']} | `{json.dumps(details, sort_keys=True)}` |")
    lines += [
        "",
        "## Interpretation",
        "",
        "This audit checks whether artifacts are strong enough to be treated as formal DRC evidence. "
        "A failed audit does not mean the code is broken; it usually means the run is a smoke test, "
        "uses non-return buffers, lacks strict statistical/content gates, or has no frozen teacher manifest.",
    ]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Audit formal readiness of DRC artifacts.")
    parser.add_argument("--candidate-manifest", default="")
    parser.add_argument("--buffer-audit", default="")
    parser.add_argument("--protocol", default="")
    parser.add_argument("--teacher-search", default="")
    parser.add_argument("--frozen-manifest", default="")
    parser.add_argument("--require-robust-manifest", action="store_true")
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", default=None)
    args = parser.parse_args()

    checks = [
        check_candidate_manifest(args.candidate_manifest),
        check_buffer_audit(args.buffer_audit),
        check_protocol(args.protocol),
        check_teacher_search(args.teacher_search),
        check_frozen_manifest(args.frozen_manifest, require_robust=args.require_robust_manifest),
    ]
    report = {
        "method": "DRC-formal-readiness-audit-v1",
        "formal_ready": all(check["passes"] for check in checks),
        "inputs": {
            "candidate_manifest": args.candidate_manifest,
            "buffer_audit": args.buffer_audit,
            "protocol": args.protocol,
            "teacher_search": args.teacher_search,
            "frozen_manifest": args.frozen_manifest,
            "require_robust_manifest": args.require_robust_manifest,
        },
        "checks": checks,
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2) + "\n")
    if args.out_md:
        write_md(args.out_md, report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
