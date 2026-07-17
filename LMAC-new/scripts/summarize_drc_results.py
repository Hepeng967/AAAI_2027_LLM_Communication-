#!/usr/bin/env python3
"""Summarize DRC certification JSON files into paper-friendly tables."""

import argparse
import csv
import json
from pathlib import Path


FIELDS = [
    "file",
    "method",
    "map",
    "accepted",
    "has_return_data",
    "stat_gate",
    "content_gate",
    "sender_observable",
    "receiver_necessary",
    "task_complete",
    "decision_sufficient",
    "causally_useful",
    "score",
    "decision_gain",
    "decision_p",
    "causal_gain",
    "causal_p",
    "shuffle_delta",
    "shuffle_p",
    "edge_rate",
    "message_dim",
    "probe_model",
    "oracle_kind",
    "teacher",
]


def get_nested(item, path, default=None):
    cur = item
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def bool_rate(rows, key):
    if not rows:
        return None
    return sum(1 for row in rows if row.get(key)) / len(rows)


def summarize_one(path):
    item = json.loads(path.read_text())
    if "map_name" not in item or "scores" not in item:
        return None
    observability = item.get("observability_and_necessity", [])
    decision = item.get("decision_sufficiency", {})
    causal = item.get("causal_usefulness", {})
    content = decision.get("content_specificity", {})
    scores = item.get("scores", {})
    return {
        "file": path.name,
        "method": item.get("method"),
        "map": item.get("map_name"),
        "accepted": item.get("accepted"),
        "has_return_data": item.get("has_return_data"),
        "stat_gate": item.get("passes_statistical_gate"),
        "content_gate": item.get("passes_content_gate"),
        "sender_observable": scores.get("sender_observable_rate", bool_rate(observability, "passes_sender_observable")),
        "receiver_necessary": scores.get("receiver_necessary_rate", bool_rate(observability, "passes_receiver_necessary")),
        "task_complete": scores.get(
            "task_fact_completeness",
            get_nested(item, ["task_fact_completeness", "coverage_rate"]),
        ),
        "decision_sufficient": decision.get("passes_decision_sufficient"),
        "causally_useful": causal.get("passes_causally_useful"),
        "score": scores.get("final_score"),
        "decision_gain": scores.get("decision_sufficiency_gain"),
        "decision_p": get_nested(decision, ["ce_gain_resampling", "p_value_positive"]),
        "causal_gain": scores.get("causal_usefulness"),
        "causal_p": get_nested(causal, ["mean_causal_ce_resampling", "p_value_positive"]),
        "shuffle_delta": content.get("shuffle_minus_true_ce"),
        "shuffle_p": get_nested(content, ["shuffle_minus_true_resampling", "p_value_positive"]),
        "edge_rate": item.get("matrix_edge_rate"),
        "message_dim": item.get("message_dim"),
        "probe_model": decision.get("probe_model"),
        "oracle_kind": decision.get("oracle_kind"),
        "teacher": item.get("comm_code"),
    }


def fmt(value):
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def main():
    parser = argparse.ArgumentParser(description="Summarize DRC result JSON files.")
    parser.add_argument("--search-root", required=True)
    parser.add_argument("--out-csv", required=True)
    parser.add_argument("--out-md", default=None)
    args = parser.parse_args()

    root = Path(args.search_root)
    rows = []
    for path in sorted(root.glob("*.json")):
        row = summarize_one(path)
        if row is not None:
            rows.append(row)
    rows.sort(key=lambda r: (r["map"] or "", not bool(r["accepted"]), -(r["score"] or -1e9)))

    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    if args.out_md:
        lines = [
            "# DRC Results Summary",
            "",
            f"- search root: `{root}`",
            f"- rows: `{len(rows)}`",
            "",
            "| map | accepted | return | stat | content | score | decision | decision_p | causal | causal_p | shuffle | edge | probe | oracle | file |",
            "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
        ]
        for row in rows:
            lines.append(
                f"| {fmt(row['map'])} | {fmt(row['accepted'])} | {fmt(row['has_return_data'])} | "
                f"{fmt(row['stat_gate'])} | {fmt(row['content_gate'])} | {fmt(row['score'])} | "
                f"{fmt(row['decision_gain'])} | {fmt(row['decision_p'])} | {fmt(row['causal_gain'])} | "
                f"{fmt(row['causal_p'])} | {fmt(row['shuffle_delta'])} | {fmt(row['edge_rate'])} | "
                f"{fmt(row['probe_model'])} | {fmt(row['oracle_kind'])} | {fmt(row['file'])} |"
            )
        out_md = Path(args.out_md)
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text("\n".join(lines) + "\n")

    print(f"Wrote {len(rows)} DRC rows to {out_csv}")


if __name__ == "__main__":
    main()
