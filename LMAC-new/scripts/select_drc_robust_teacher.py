#!/usr/bin/env python3
"""Select teachers that are accepted across multiple DRC search roots."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def resolve_path(path):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    try:
        return str(p.resolve())
    except FileNotFoundError:
        return str(p.absolute())


def load_rows(search_root):
    rows = []
    root = Path(search_root)
    for path in sorted(root.glob("*.json")):
        try:
            item = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if "map_name" not in item or "comm_code" not in item or "scores" not in item:
            continue
        decision = item.get("decision_sufficiency", {})
        content = decision.get("content_specificity", {})
        rows.append(
            {
                "search_root": str(root),
                "evidence_json": str(path),
                "map": item["map_name"],
                "teacher_path": item["comm_code"],
                "teacher_key": resolve_path(item["comm_code"]),
                "accepted": bool(item.get("accepted")),
                "has_return_data": bool(item.get("has_return_data")),
                "stat_gate": bool(item.get("passes_statistical_gate")),
                "content_gate": bool(item.get("passes_content_gate")),
                "score": float(item["scores"].get("final_score", float("-inf"))),
                "decision_gain": float(item["scores"].get("decision_sufficiency_gain", 0.0)),
                "causal": float(item["scores"].get("causal_usefulness", 0.0)),
                "edge_rate": float(item.get("matrix_edge_rate", 0.0)),
                "probe_model": decision.get("probe_model"),
                "oracle_kind": decision.get("oracle_kind"),
                "decision_label": decision.get("decision_label", item.get("decision_label")),
                "shuffle_delta": content.get("shuffle_minus_true_ce"),
            }
        )
    return rows


def passes_filters(row, args):
    if not row["accepted"]:
        return False
    if args.require_return_data and not row["has_return_data"]:
        return False
    if args.require_stat_gate and not row["stat_gate"]:
        return False
    if args.require_content_gate and not row["content_gate"]:
        return False
    return True


def aggregate(rows, search_roots, args):
    grouped = {}
    for row in rows:
        key = (row["map"], row["teacher_key"])
        grouped.setdefault(key, []).append(row)

    robust = []
    rejected = []
    required_roots = {str(Path(root)) for root in search_roots}
    for (map_name, teacher_key), group in sorted(grouped.items()):
        by_root = {}
        for row in group:
            root = row["search_root"]
            if root not in by_root or row["score"] > by_root[root]["score"]:
                by_root[root] = row
        passed_roots = {
            root
            for root, row in by_root.items()
            if root in required_roots and passes_filters(row, args)
        }
        missing_roots = sorted(required_roots - set(by_root))
        failed_roots = sorted(required_roots - passed_roots - set(missing_roots))
        if passed_roots == required_roots:
            scores = [by_root[root]["score"] for root in required_roots]
            edge_rates = [by_root[root]["edge_rate"] for root in required_roots]
            decision = [by_root[root]["decision_gain"] for root in required_roots]
            causal = [by_root[root]["causal"] for root in required_roots]
            robust.append(
                {
                    "map": map_name,
                    "teacher_key": teacher_key,
                    "teacher_path": group[0]["teacher_path"],
                    "mean_score": sum(scores) / len(scores),
                    "min_score": min(scores),
                    "mean_edge_rate": sum(edge_rates) / len(edge_rates),
                    "mean_decision_gain": sum(decision) / len(decision),
                    "mean_causal_usefulness": sum(causal) / len(causal),
                    "evidence": [by_root[root] for root in sorted(required_roots)],
                }
            )
        else:
            rejected.append(
                {
                    "map": map_name,
                    "teacher_key": teacher_key,
                    "teacher_path": group[0]["teacher_path"],
                    "passed_roots": sorted(passed_roots),
                    "missing_roots": missing_roots,
                    "failed_roots": failed_roots,
                }
            )
    return robust, rejected


def select_by_map(robust):
    selected = {}
    for row in robust:
        cur = selected.get(row["map"])
        rank = (row["mean_score"], row["min_score"], -row["mean_edge_rate"])
        if cur is None or rank > (cur["mean_score"], cur["min_score"], -cur["mean_edge_rate"]):
            selected[row["map"]] = row
    return selected


def main():
    parser = argparse.ArgumentParser(description="Select DRC teachers robust across multiple search roots.")
    parser.add_argument("--search-roots", nargs="+", required=True)
    parser.add_argument("--require-return-data", action="store_true")
    parser.add_argument("--require-stat-gate", action="store_true")
    parser.add_argument("--require-content-gate", action="store_true")
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", default=None)
    args = parser.parse_args()

    rows = []
    for root in args.search_roots:
        rows.extend(load_rows(root))
    robust, rejected = aggregate(rows, args.search_roots, args)
    selected = select_by_map(robust)

    manifest = {
        "method": "DRC-robust-frozen-teacher-selection",
        "search_roots": [str(Path(root)) for root in args.search_roots],
        "selection_rule": (
            "A teacher is robust only if the same resolved teacher path is accepted "
            "in every requested DRC search root after filters. Robust teachers are "
            "ranked per map by mean_score, then min_score, then lower mean_edge_rate."
        ),
        "filters": {
            "require_return_data": args.require_return_data,
            "require_stat_gate": args.require_stat_gate,
            "require_content_gate": args.require_content_gate,
        },
        "teachers": {
            map_name: {
                "teacher_path": row["teacher_path"],
                "resolved_teacher_path": row["teacher_key"],
                "score": row["mean_score"],
                "mean_score": row["mean_score"],
                "min_score": row["min_score"],
                "decision_gain": row["mean_decision_gain"],
                "causal_usefulness": row["mean_causal_usefulness"],
                "edge_rate": row["mean_edge_rate"],
                "evidence_json": row["evidence"][0]["evidence_json"],
                "robust_evidence": [
                    {
                        "search_root": ev["search_root"],
                        "evidence_json": ev["evidence_json"],
                        "score": ev["score"],
                        "decision_gain": ev["decision_gain"],
                        "causal_usefulness": ev["causal"],
                        "edge_rate": ev["edge_rate"],
                        "probe_model": ev["probe_model"],
                        "oracle_kind": ev["oracle_kind"],
                        "has_return_data": ev["has_return_data"],
                        "stat_gate": ev["stat_gate"],
                        "content_gate": ev["content_gate"],
                    }
                    for ev in row["evidence"]
                ],
            }
            for map_name, row in sorted(selected.items())
        },
        "num_search_roots": len(args.search_roots),
        "num_result_rows": len(rows),
        "num_robust_candidates": len(robust),
        "num_selected_maps": len(selected),
        "num_rejected_candidates": len(rejected),
        "rejected_candidates": rejected,
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(manifest, indent=2) + "\n")

    if args.out_md:
        lines = [
            "# Robust Frozen DRC Teacher Manifest",
            "",
            f"- search roots: `{len(args.search_roots)}`",
            f"- selected maps: `{len(selected)}`",
            f"- robust candidates: `{len(robust)}`",
            f"- rejected candidates: `{len(rejected)}`",
            "",
            "| map | mean_score | min_score | decision | causal | edge | teacher |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
        for map_name, row in sorted(selected.items()):
            lines.append(
                f"| {map_name} | {row['mean_score']:.4f} | {row['min_score']:.4f} | "
                f"{row['mean_decision_gain']:.4f} | {row['mean_causal_usefulness']:.4f} | "
                f"{row['mean_edge_rate']:.4f} | `{row['teacher_path']}` |"
            )
        Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out_md).write_text("\n".join(lines) + "\n")

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
