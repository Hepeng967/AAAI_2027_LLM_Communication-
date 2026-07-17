#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd):
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout


def summarize_static_report(report):
    if report is None:
        return {
            "accepted": False,
            "reason": "missing_static_report",
            "files": [],
        }

    files = []
    for item in report.get("reports", []):
        probes = []
        for probe in item.get("task_probe_reports", []):
            probes.append(
                {
                    "name": probe.get("name"),
                    "passes": bool(probe.get("passes")),
                    "receiver_delta": probe.get("receiver_delta"),
                    "non_receiver_delta": probe.get("non_receiver_delta"),
                    "matrix_edge_present": probe.get("matrix_edge_present"),
                    "leakage_ratio": probe.get("leakage_ratio"),
                }
            )
        completeness = item.get("task_decision_completeness", {})
        files.append(
            {
                "path": item.get("path"),
                "passes": bool(item.get("passes_static_certificate")),
                "message_dim": item.get("message_dim"),
                "has_communication_matrix": item.get("has_communication_matrix"),
                "matrix_edge_rate": item.get("matrix_edge_rate"),
                "likely_receiver_side_message": item.get("likely_receiver_side_message"),
                "task_probes": probes,
                "task_decision_completeness": {
                    "passes": bool(completeness.get("passes_task_decision_completeness")),
                    "coverage_rate": completeness.get("coverage_rate"),
                    "covered_fact_count": completeness.get("covered_fact_count"),
                    "required_fact_count": completeness.get("required_fact_count"),
                    "fact_reports": completeness.get("fact_reports", []),
                },
            }
        )

    return {
        "accepted": bool(report.get("accepted")),
        "files": files,
    }


def summarize_ablation_report(report, maps):
    if report is None:
        return {
            "status": "pending",
            "reason": "missing_ablation_summary",
            "accepted": False,
            "min_drop": None,
            "maps": {},
        }

    maps_out = {}
    accepted = True
    pending = False
    meta = report.get("_meta", {})
    for map_name in maps:
        item = report.get(map_name)
        if item is None:
            pending = True
            accepted = False
            maps_out[map_name] = {
                "status": "pending",
                "reason": "missing_map_ablation",
            }
            continue

        mode_names = item.get("modes", {}).keys()
        missing_modes = [
            mode for mode in (
                "none",
                "zero",
                "random_same_rate",
                "drop_certified_edges",
                "keep_certified_edges",
            )
            if mode not in mode_names
        ]
        map_accepted = bool(item.get("accepted")) and not missing_modes
        accepted = accepted and map_accepted
        pending = pending or bool(missing_modes)
        maps_out[map_name] = {
            "status": "pass" if map_accepted else "pending_or_fail",
            "accepted": map_accepted,
            "zero_drop": item.get("zero_drop"),
            "random_same_rate_drop": item.get("random_same_rate_drop"),
            "certified_edge_drop": item.get("certified_edge_drop"),
            "keep_certified_edges_gap": item.get("keep_certified_edges_gap"),
            "missing_modes": missing_modes,
        }

    return {
        "status": "pass" if accepted else "pending" if pending else "fail",
        "accepted": accepted,
        "min_drop": meta.get("min_drop"),
        "maps": maps_out,
    }


def classify_progress(code, text):
    if code == 2:
        return "warn"
    if code != 0:
        return f"error_{code}"
    if "PENDING" in text:
        return "pending"
    return "pass"


def final_decision(static_summary, progress_status, ablation_summary):
    static_pass = all(item.get("accepted") for item in static_summary.values())
    ablation_status = ablation_summary.get("status")
    checks = {
        "static": "pass" if static_pass else "fail",
        "progress": progress_status,
        "ablation": ablation_status,
    }

    if static_pass and progress_status == "pass" and ablation_status == "pass":
        status = "accepted"
        reason = "all_static_progress_and_ablation_gates_passed"
    elif (
        "warn" in checks.values()
        or "fail" in checks.values()
        or any(str(v).startswith("error") for v in checks.values())
    ):
        status = "rejected"
        reason = "at_least_one_completed_gate_failed"
    elif not static_pass:
        status = "rejected"
        reason = "static_certificate_failed"
    else:
        status = "pending"
        reason = "waiting_for_completed_progress_or_ablation_evidence"

    return {
        "status": status,
        "reason": reason,
        "checks": checks,
    }


def fmt_float(value):
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def write_markdown(result, out_path):
    lines = [
        "# Communication Certificate",
        "",
        f"- Run prefix: `{result['run_prefix']}`",
        f"- Steps: `{', '.join(str(s) for s in result['steps'])}`",
        f"- Progress status: `{result['progress_status']}`",
        f"- Ablation status: `{result['ablation_summary']['status']}`",
        f"- Final decision: `{result['final_decision']['status']}` "
        f"({result['final_decision']['reason']})",
        f"- Warn gap: `{result['warn_gap']}`",
        "",
        "## Static Task-Decision Certificate",
        "",
        "This gate checks protocol well-formedness and task-critical field sensitivity. "
        "It is intentionally not a state-reconstruction-only criterion.",
        "",
    ]

    for map_name, summary in result["static_summary"].items():
        accepted = "PASS" if summary.get("accepted") else "FAIL"
        lines.extend([f"### {map_name}: {accepted}", ""])
        for item in summary.get("files", []):
            lines.append(
                f"- `{item['path']}`: "
                f"pass={item['passes']}, "
                f"message_dim={item['message_dim']}, "
                f"matrix_edge_rate={fmt_float(item['matrix_edge_rate'])}, "
                f"receiver_side={item['likely_receiver_side_message']}"
            )
            for probe in item.get("task_probes", []):
                lines.append(
                    f"  - probe `{probe['name']}`: "
                    f"pass={probe['passes']}, "
                    f"receiver_delta={fmt_float(probe['receiver_delta'])}, "
                    f"non_receiver_delta={fmt_float(probe['non_receiver_delta'])}, "
                    f"leakage_ratio={fmt_float(probe.get('leakage_ratio'))}, "
                    f"matrix_edge={probe['matrix_edge_present']}"
                )
            completeness = item.get("task_decision_completeness", {})
            lines.append(
                f"  - completeness: pass={completeness.get('passes')}, "
                f"coverage={fmt_float(completeness.get('coverage_rate'))}, "
                f"covered={completeness.get('covered_fact_count')}/"
                f"{completeness.get('required_fact_count')}"
            )
            for fact in completeness.get("fact_reports", []):
                lines.append(
                    f"    - fact `{fact['fact']}`: "
                    f"pass={fact['passes']}, "
                    f"probe={fact['covered_by_probe']}, "
                    f"matrix_edges={fact['matrix_edges_present']}"
                )
        lines.append("")

    lines.extend(
        [
            "## Dynamic Progress Gate",
            "",
            "A completed run is rejected if `test_battle_won_mean` trails LMAC-main by "
            "more than the warn gap. Pending runs are not final evidence.",
            "",
            "```text",
            result["progress_output"].strip(),
            "```",
            "",
            "## Dynamic Causal Certificate",
            "",
            "This gate checks whether communication, edge structure, and certified "
            "task-fact edges have measurable causal utility.",
            "",
            f"- Min drop: `{fmt_float(result['ablation_summary'].get('min_drop'))}`",
            "",
        ]
    )

    for map_name, item in result["ablation_summary"].get("maps", {}).items():
        lines.append(
            f"- `{map_name}`: status={item.get('status')}, "
            f"zero_drop={fmt_float(item.get('zero_drop'))}, "
            f"random_same_rate_drop={fmt_float(item.get('random_same_rate_drop'))}, "
            f"certified_edge_drop={fmt_float(item.get('certified_edge_drop'))}, "
            f"keep_certified_edges_gap={fmt_float(item.get('keep_certified_edges_gap'))}"
        )
        if item.get("missing_modes"):
            lines.append(f"  - missing modes: {', '.join(item['missing_modes'])}")
    if not result["ablation_summary"].get("maps"):
        lines.append(f"- pending: {result['ablation_summary'].get('reason')}")

    lines.extend(
        [
            "",
            "## Decision Rule",
            "",
            f"- Final: status=`{result['final_decision']['status']}`, "
            f"reason=`{result['final_decision']['reason']}`",
            f"- Static: {result['decision_rule']['static']}",
            f"- Progress: {result['decision_rule']['progress']}",
            f"- Ablation: {result['decision_rule']['ablation']}",
            "- Next dynamic checks: "
            + ", ".join(result["decision_rule"]["next_dynamic_checks"]),
            "",
        ]
    )

    out_path.write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(
        description="Create an auditable communication certificate for a candidate teacher/student run."
    )
    parser.add_argument("--run-prefix", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--maps", nargs="+", default=["1o_10b_vs_1r", "1o_2r_vs_4r", "5z_vs_1ul"])
    parser.add_argument("--steps", nargs="+", type=int, default=[500000])
    parser.add_argument("--warn-gap", type=float, default=0.2)
    parser.add_argument("--new-sacred", default="results/sacred/LMAC")
    parser.add_argument("--baseline-sacred", default="/data/hp/LLM_Communication/LMAC-main/results/sacred/LMAC")
    parser.add_argument("--static-cert-dir", default="description/certification_gate")
    parser.add_argument(
        "--ablation-summary",
        default="description/certification_gate/comm_ablation_summary.json",
        help="Optional dynamic ablation summary JSON from summarize_comm_ablation.py.",
    )
    parser.add_argument(
        "--markdown-out",
        default=None,
        help="Optional Markdown summary path. Defaults to the JSON path with .md suffix.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Write JSON/Markdown files without printing the full JSON document.",
    )
    args = parser.parse_args()

    cert_dir = Path(args.static_cert_dir)
    static_reports = {}
    static_summary = {}
    for map_name in args.maps:
        path = cert_dir / f"cert_{map_name}.json"
        static_reports[map_name] = json.loads(path.read_text()) if path.exists() else None
        static_summary[map_name] = summarize_static_report(static_reports[map_name])

    progress_cmd = [
        sys.executable,
        "scripts/summarize_progress.py",
        "--new-sacred",
        args.new_sacred,
        "--baseline-sacred",
        args.baseline_sacred,
        "--run-prefix",
        args.run_prefix,
        "--steps",
        *[str(s) for s in args.steps],
        "--min-current-t-max",
        str(max(args.steps)),
        "--warn-gap",
        str(args.warn_gap),
        "--fail-on-warn",
    ]
    code, progress_text = run(progress_cmd)
    progress_status = classify_progress(code, progress_text)
    ablation_path = Path(args.ablation_summary)
    ablation_report = json.loads(ablation_path.read_text()) if ablation_path.exists() else None
    ablation_summary = summarize_ablation_report(ablation_report, args.maps)
    decision = final_decision(static_summary, progress_status, ablation_summary)

    result = {
        "run_prefix": args.run_prefix,
        "maps": args.maps,
        "steps": args.steps,
        "warn_gap": args.warn_gap,
        "static_summary": static_summary,
        "static_reports": static_reports,
        "progress_status": progress_status,
        "progress_output": progress_text,
        "ablation_summary": ablation_summary,
        "ablation_report": ablation_report,
        "final_decision": decision,
        "decision_rule": {
            "static": (
                "All maps must pass shape/message/matrix checks, task-critical "
                "field sensitivity probes, and required task-fact coverage."
            ),
            "progress": (
                "A completed comparison is rejected if test_battle_won_mean trails "
                "LMAC-main by more than warn_gap. Pending comparisons are not accepted "
                "as final evidence."
            ),
            "ablation": (
                "Dynamic acceptance requires normal communication to outperform "
                "no-communication, random same-rate communication, and "
                "drop-certified-edge evaluation by the configured min_drop."
            ),
            "next_dynamic_checks": [
                "fixed-teacher rollout against no-communication/random-budget baselines",
                "certified-edge ablation",
                "field shuffle ablation",
                "task-critical variable probe",
            ],
        },
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    markdown_out = Path(args.markdown_out) if args.markdown_out else out.with_suffix(".md")
    write_markdown(result, markdown_out)
    if args.quiet:
        print(
            f"wrote {out} and {markdown_out}; "
            f"progress={progress_status}; ablation={ablation_summary['status']}; "
            f"final={decision['status']}"
        )
    else:
        print(json.dumps(result, indent=2))

    raise SystemExit(1 if progress_status.startswith("error") else 0)


if __name__ == "__main__":
    main()
