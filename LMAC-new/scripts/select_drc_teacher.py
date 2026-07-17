#!/usr/bin/env python3
"""Select frozen teachers from DRC certification outputs."""

import argparse
import json
from pathlib import Path


def load_candidates(search_root):
    rows = []
    for path in sorted(Path(search_root).glob("*.json")):
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
                "path": path,
                "map": item["map_name"],
                "teacher_path": item["comm_code"],
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


def main():
    parser = argparse.ArgumentParser(description="Select frozen teacher manifest from DRC outputs.")
    parser.add_argument("--search-root", required=True)
    parser.add_argument("--require-return-data", action="store_true")
    parser.add_argument("--require-stat-gate", action="store_true")
    parser.add_argument("--require-content-gate", action="store_true")
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", default=None)
    args = parser.parse_args()

    rows = load_candidates(args.search_root)
    selected = {}
    rejected = []
    for row in rows:
        if not passes_filters(row, args):
            rejected.append(row)
            continue
        cur = selected.get(row["map"])
        if cur is None or (row["score"], -row["edge_rate"]) > (cur["score"], -cur["edge_rate"]):
            selected[row["map"]] = row

    manifest = {
        "method": "DRC-v5-frozen-teacher-selection",
        "search_root": str(args.search_root),
        "selection_rule": (
            "accepted candidates are filtered by requested formal gates, then ranked by "
            "final_score with lower edge_rate as a tie-breaker"
        ),
        "filters": {
            "require_return_data": args.require_return_data,
            "require_stat_gate": args.require_stat_gate,
            "require_content_gate": args.require_content_gate,
        },
        "teachers": {
            name: {
                "teacher_path": row["teacher_path"],
                "evidence_json": str(row["path"]),
                "score": row["score"],
                "decision_gain": row["decision_gain"],
                "causal_usefulness": row["causal"],
                "edge_rate": row["edge_rate"],
                "probe_model": row["probe_model"],
                "oracle_kind": row["oracle_kind"],
                "decision_label": row["decision_label"],
                "has_return_data": row["has_return_data"],
                "stat_gate": row["stat_gate"],
                "content_gate": row["content_gate"],
                "shuffle_delta": row["shuffle_delta"],
            }
            for name, row in sorted(selected.items())
        },
        "num_candidates": len(rows),
        "num_selected_maps": len(selected),
        "num_rejected_candidates": len(rejected),
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(manifest, indent=2) + "\n")

    if args.out_md:
        lines = [
            "# Frozen DRC Teacher Manifest",
            "",
            f"- search root: `{args.search_root}`",
            f"- selected maps: `{len(selected)}`",
            f"- candidates: `{len(rows)}`",
            "",
            "| map | score | decision | causal | edge | probe | oracle | label | return | stat | content | teacher |",
            "| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for name, row in sorted(selected.items()):
            lines.append(
                f"| {name} | {row['score']:.4f} | {row['decision_gain']:.4f} | "
                f"{row['causal']:.4f} | {row['edge_rate']:.4f} | {row['probe_model']} | "
                f"{row['oracle_kind']} | {row['decision_label']} | {row['has_return_data']} | {row['stat_gate']} | "
                f"{row['content_gate']} | `{row['teacher_path']}` |"
            )
        Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out_md).write_text("\n".join(lines) + "\n")

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
