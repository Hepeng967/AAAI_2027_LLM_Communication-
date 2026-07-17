#!/usr/bin/env python3
"""Write a paper-grade dossier for a DRC teacher-construction run."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def load_json(path):
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def get_nested(item, keys, default=None):
    cur = item
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def iter_result_json(search_root):
    if not search_root:
        return
    root = Path(search_root)
    if not root.exists():
        return
    for path in sorted(root.glob("*.json")):
        try:
            item = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if "map_name" in item and "scores" in item:
            yield path, item


def gate_value(item, gate):
    scores = item.get("scores", {})
    decision = item.get("decision_sufficiency", {})
    causal = item.get("causal_usefulness", {})
    if gate == "sender_observable":
        value = scores.get("sender_observable_rate")
        return None if value is None else value >= 1.0
    if gate == "receiver_necessary":
        cert = item.get("formal_certificate", {})
        for row in cert.get("gates", []):
            if row.get("gate") == "receiver_necessary":
                return bool(row.get("passes"))
        value = scores.get("receiver_necessary_rate")
        return None if value is None else value >= 1.0
    if gate == "task_fact_complete":
        value = scores.get("task_fact_completeness")
        return None if value is None else value >= 1.0
    if gate == "decision_sufficient":
        return decision.get("passes_decision_sufficient")
    if gate == "causally_useful":
        return causal.get("passes_causally_useful")
    if gate == "statistical":
        return item.get("passes_statistical_gate")
    if gate == "content_control":
        return item.get("passes_content_gate")
    if gate == "formal_return_data":
        return item.get("has_return_data")
    return None


def candidate_row(path, item):
    decision = item.get("decision_sufficiency", {})
    causal = item.get("causal_usefulness", {})
    content = decision.get("content_specificity", {})
    scores = item.get("scores", {})
    gates = {
        name: gate_value(item, name)
        for name in (
            "sender_observable",
            "receiver_necessary",
            "task_fact_complete",
            "decision_sufficient",
            "causally_useful",
            "statistical",
            "content_control",
            "formal_return_data",
        )
    }
    failed_gates = [name for name, passed in gates.items() if passed is False]
    unknown_gates = [name for name, passed in gates.items() if passed is None]
    return {
        "file": str(path),
        "map": item.get("map_name"),
        "teacher": item.get("comm_code"),
        "accepted": bool(item.get("accepted")),
        "gates": gates,
        "failed_gates": failed_gates,
        "unknown_gates": unknown_gates,
        "score": scores.get("final_score"),
        "edge_rate": item.get("matrix_edge_rate"),
        "message_dim": item.get("message_dim"),
        "decision_label": decision.get("decision_label", item.get("decision_label")),
        "decision_gain": scores.get("decision_sufficiency_gain"),
        "conditional_decision_value_nats": scores.get("conditional_decision_value_nats"),
        "conditional_decision_value_bits": scores.get("conditional_decision_value_bits"),
        "decision_p": get_nested(decision, ["ce_gain_resampling", "p_value_positive"]),
        "causal_gain": scores.get("causal_usefulness"),
        "causal_p": get_nested(causal, ["mean_causal_ce_resampling", "p_value_positive"]),
        "shuffle_minus_true_ce": content.get("shuffle_minus_true_ce"),
        "shuffle_p": get_nested(content, ["shuffle_minus_true_resampling", "p_value_positive"]),
        "oracle_kind": decision.get("oracle_kind"),
        "probe_model": decision.get("probe_model"),
    }


def summarize_by_map(rows):
    by_map = defaultdict(list)
    for row in rows:
        by_map[row["map"]].append(row)
    out = {}
    for map_name, items in sorted(by_map.items()):
        accepted = [row for row in items if row["accepted"]]
        failure_counts = Counter()
        for row in items:
            failure_counts.update(row["failed_gates"])
        unknown_counts = Counter()
        for row in items:
            unknown_counts.update(row["unknown_gates"])
        best = None
        if accepted:
            best = sorted(
                accepted,
                key=lambda row: (
                    row["score"] if row["score"] is not None else float("-inf"),
                    -(row["edge_rate"] if row["edge_rate"] is not None else float("inf")),
                ),
                reverse=True,
            )[0]
        out[map_name] = {
            "num_candidates": len(items),
            "num_accepted": len(accepted),
            "failure_counts": dict(sorted(failure_counts.items())),
            "unknown_counts": dict(sorted(unknown_counts.items())),
            "best_accepted": best,
        }
    return out


def fmt(value):
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def path_key(path):
    if not path:
        return ""
    try:
        return str(Path(path).resolve())
    except FileNotFoundError:
        return str(Path(path).absolute())


def write_md(path, dossier):
    lines = [
        "# Decision-Relevant Certification Dossier",
        "",
        "## Run Identity",
        "",
        f"- formal ready: `{dossier['formal_ready']}`",
        f"- protocol sha256: `{dossier['protocol_sha256']}`",
        f"- search root: `{dossier['inputs']['teacher_search']}`",
        f"- candidate manifest: `{dossier['inputs']['candidate_manifest']}`",
        f"- frozen manifest: `{dossier['inputs']['frozen_manifest']}`",
        "",
        "## Academic Claim",
        "",
        "A candidate teacher is selected before downstream RL only if it passes offline "
        "decision-relevance gates: sender observability, receiver necessity, task-fact "
        "completeness, decision sufficiency, causal usefulness, statistical support, "
        "and message-content negative controls. The decision gate reports conditional "
        "decision value as held-out log-loss reduction, an implementable proxy for "
        "`I(M; Y_dec | O_receiver)`.",
        "",
        "## Map Summary",
        "",
        "| map | candidates | accepted | best score | cond info nats | causal | edge | failed gates | unknown gates |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for map_name, row in dossier["map_summary"].items():
        best = row.get("best_accepted") or {}
        failures = ", ".join(f"{k}:{v}" for k, v in row.get("failure_counts", {}).items()) or "none"
        unknowns = ", ".join(f"{k}:{v}" for k, v in row.get("unknown_counts", {}).items()) or "none"
        lines.append(
            f"| {map_name} | {row['num_candidates']} | {row['num_accepted']} | "
            f"{fmt(best.get('score'))} | {fmt(best.get('conditional_decision_value_nats'))} | "
            f"{fmt(best.get('causal_gain'))} | {fmt(best.get('edge_rate'))} | {failures} | {unknowns} |"
        )
    lines += [
        "",
        "## Selected Frozen Teachers",
        "",
        "| map | teacher | evidence | score | cond info nats | causal | content control |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    teachers = dossier.get("frozen_teachers", {})
    if teachers:
        for map_name, row in sorted(teachers.items()):
            lines.append(
                f"| {map_name} | `{row.get('teacher_path')}` | `{row.get('evidence_json')}` | "
                f"{fmt(row.get('score'))} | {fmt(row.get('conditional_decision_value_nats'))} | "
                f"{fmt(row.get('causal_usefulness'))} | {fmt(row.get('content_gate'))} |"
            )
    else:
        lines.append("| n/a | n/a | n/a | n/a | n/a | n/a | n/a |")
    lines += [
        "",
        "## Formal Readiness",
        "",
        f"- readiness audit present: `{dossier['readiness_audit_present']}`",
        f"- formal ready: `{dossier['formal_ready']}`",
        "",
        "A dossier can be useful for debugging even when not formal-ready. For paper "
        "evidence, `formal_ready` must be true and the input buffers must include "
        "reward/terminated fields collected before teacher selection.",
        "",
        "## Candidate-Level Table",
        "",
        "| map | accepted | score | cond info nats | decision p | causal | causal p | shuffle | failed gates | unknown gates | file |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for row in dossier["candidates"]:
        lines.append(
            f"| {row['map']} | {row['accepted']} | {fmt(row.get('score'))} | "
            f"{fmt(row.get('conditional_decision_value_nats'))} | {fmt(row.get('decision_p'))} | "
            f"{fmt(row.get('causal_gain'))} | {fmt(row.get('causal_p'))} | "
            f"{fmt(row.get('shuffle_minus_true_ce'))} | {', '.join(row['failed_gates']) or 'none'} | "
            f"{', '.join(row['unknown_gates']) or 'none'} | "
            f"`{row['file']}` |"
        )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Write a DRC paper dossier.")
    parser.add_argument("--teacher-search", required=True)
    parser.add_argument("--candidate-manifest", default="")
    parser.add_argument("--protocol", default="")
    parser.add_argument("--buffer-audit", default="")
    parser.add_argument("--frozen-manifest", default="")
    parser.add_argument("--formal-readiness-audit", default="")
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", default=None)
    args = parser.parse_args()

    candidate_manifest = load_json(args.candidate_manifest)
    protocol = load_json(args.protocol)
    buffer_audit = load_json(args.buffer_audit)
    frozen_manifest = load_json(args.frozen_manifest)
    readiness = load_json(args.formal_readiness_audit)
    rows = [candidate_row(path, item) for path, item in iter_result_json(args.teacher_search)]
    map_summary = summarize_by_map(rows)

    frozen_teachers = {}
    if frozen_manifest:
        frozen_teachers = frozen_manifest.get("teachers", {})
        by_evidence = {path_key(row["file"]): row for row in rows}
        for teacher in frozen_teachers.values():
            evidence = path_key(teacher.get("evidence_json"))
            if evidence in by_evidence:
                teacher["conditional_decision_value_nats"] = by_evidence[evidence].get(
                    "conditional_decision_value_nats"
                )

    dossier = {
        "method": "DRC-paper-dossier-v1",
        "inputs": {
            "teacher_search": args.teacher_search,
            "candidate_manifest": args.candidate_manifest,
            "protocol": args.protocol,
            "buffer_audit": args.buffer_audit,
            "frozen_manifest": args.frozen_manifest,
            "formal_readiness_audit": args.formal_readiness_audit,
        },
        "protocol_sha256": (protocol or {}).get("protocol_sha256"),
        "candidate_manifest_sha256": (candidate_manifest or {}).get("manifest_sha256"),
        "candidate_count_manifest": (candidate_manifest or {}).get("candidate_count"),
        "buffer_audit_summary": {
            name: data.get("summary", {})
            for name, data in (buffer_audit or {}).get("maps", {}).items()
        },
        "readiness_audit_present": readiness is not None,
        "formal_ready": bool((readiness or {}).get("formal_ready")),
        "map_summary": map_summary,
        "frozen_teachers": frozen_teachers,
        "candidates": rows,
        "paper_interpretation": (
            "Use this dossier as the teacher-construction evidence package. It is "
            "paper-grade only when formal_ready is true; otherwise it documents "
            "smoke/debug evidence and missing gates."
        ),
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(dossier, indent=2) + "\n")
    if args.out_md:
        write_md(args.out_md, dossier)
    print(json.dumps({"out_json": str(out_json), "formal_ready": dossier["formal_ready"], "rows": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
