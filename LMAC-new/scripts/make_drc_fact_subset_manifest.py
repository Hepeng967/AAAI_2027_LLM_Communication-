#!/usr/bin/env python3
"""Build a receiver-necessity-pruned task-fact manifest from DRC results."""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from components.certified_task_facts import map_specs  # noqa: E402


def load_results(paths):
    rows = []
    for path in paths:
        p = Path(path)
        candidates = sorted(p.glob("*.json")) if p.is_dir() else [p]
        for item_path in candidates:
            try:
                item = json.loads(item_path.read_text())
            except Exception:
                continue
            if "map_name" in item and "observability_and_necessity" in item:
                rows.append((item_path, item))
    return rows


def fact_votes(rows, min_necessity_gain):
    grouped = defaultdict(lambda: defaultdict(list))
    for path, item in rows:
        map_name = item["map_name"]
        for row in item.get("observability_and_necessity", []):
            fact = row.get("fact")
            if not fact:
                continue
            passes_sender = bool(row.get("passes_sender_observable"))
            passes_receiver = bool(row.get("passes_receiver_necessary"))
            gain = float(row.get("necessity_gain_r2", 0.0))
            grouped[map_name][fact].append(
                {
                    "source_result": str(path),
                    "passes_sender_observable": passes_sender,
                    "passes_receiver_necessary": passes_receiver,
                    "necessity_gain_r2": gain,
                    "selected": passes_sender and passes_receiver and gain >= min_necessity_gain,
                }
            )
    return grouped


def build_manifest(rows, args):
    specs = map_specs()
    grouped = fact_votes(rows, args.min_necessity_gain)
    maps = {}
    for map_name in sorted(grouped):
        spec_facts = {fact["fact"]: fact for fact in specs[map_name].get("required_task_facts", [])}
        certified = []
        rejected = []
        fact_evidence = {}
        for fact_name, evidence in sorted(grouped[map_name].items()):
            selected_votes = sum(1 for row in evidence if row["selected"])
            total = len(evidence)
            selected = selected_votes >= max(1, args.min_support)
            fact_evidence[fact_name] = {
                "selected_votes": selected_votes,
                "total_votes": total,
                "mean_necessity_gain_r2": sum(row["necessity_gain_r2"] for row in evidence) / max(total, 1),
                "evidence": evidence,
            }
            if selected:
                certified.append(fact_name)
            else:
                rejected.append(fact_name)

        maps[map_name] = {
            "certified_fact_names": certified,
            "rejected_fact_names": rejected,
            "certified_facts": [spec_facts[name] for name in certified if name in spec_facts],
            "rejected_facts": [spec_facts[name] for name in rejected if name in spec_facts],
            "fact_evidence": fact_evidence,
        }

    return {
        "method": "DRC-receiver-necessity-fact-subset-v1",
        "source_results": [str(Path(p)) for p in args.result],
        "min_necessity_gain": args.min_necessity_gain,
        "min_support": args.min_support,
        "selection_rule": (
            "A task fact is retained for task-fact completeness only if offline DRC evidence "
            "shows it is sender-observable and receiver-necessary. Rejected facts may still "
            "be logged, but are not treated as required communication content in subset runs."
        ),
        "maps": maps,
    }


def write_markdown(path, manifest):
    lines = [
        "# DRC Receiver-Necessity Fact Subset",
        "",
        f"- method: `{manifest['method']}`",
        f"- min necessity gain: `{manifest['min_necessity_gain']}`",
        f"- min support: `{manifest['min_support']}`",
        "",
        "## Map Summary",
        "",
        "| map | retained facts | rejected facts |",
        "| --- | --- | --- |",
    ]
    for map_name, row in manifest["maps"].items():
        retained = ", ".join(row["certified_fact_names"]) or "none"
        rejected = ", ".join(row["rejected_fact_names"]) or "none"
        lines.append(f"| {map_name} | {retained} | {rejected} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This manifest is an offline preregistration artifact. It can be passed to "
            "`certify_decision_relevant_comm.py --fact-subset-manifest` so task-fact "
            "completeness is evaluated only over facts that passed sender-observability "
            "and receiver-necessity evidence.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Make a receiver-necessity-pruned DRC fact subset manifest.")
    parser.add_argument("--result", nargs="+", required=True, help="DRC result JSON files or directories.")
    parser.add_argument("--min-necessity-gain", type=float, default=0.05)
    parser.add_argument("--min-support", type=int, default=1)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    rows = load_results(args.result)
    if not rows:
        raise SystemExit("No DRC result JSON files found.")
    manifest = build_manifest(rows, args)
    Path(args.out_json).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(Path(args.out_md), manifest)
    print(f"Wrote fact subset manifest to {args.out_json}")


if __name__ == "__main__":
    main()
