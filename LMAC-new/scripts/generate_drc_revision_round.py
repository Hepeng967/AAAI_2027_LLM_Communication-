#!/usr/bin/env python3
"""Create a DRC-only LLM revision round from teacher-search results.

This script is deliberately offline: it consumes DRC certificates and emits
revision prompts plus a manifest for the next candidate-generation round. It
does not inspect downstream RL logs or training curves.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SRC))

from scripts.generate_drc_feedback_prompt import build_feedback, load_results  # noqa: E402


FORMAL_GATES = [
    "sender_observable",
    "receiver_necessary",
    "task_fact_complete",
    "decision_sufficient",
    "causally_useful",
]


def fmt(value):
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def safe_label(text):
    out = []
    for ch in str(text):
        if ch.isalnum() or ch in ("-", "_"):
            out.append(ch)
        else:
            out.append("_")
    label = "".join(out).strip("_").lower()
    while "__" in label:
        label = label.replace("__", "_")
    return label or "candidate"


def failed_gates(item):
    failed = []
    cert = item.get("formal_certificate", {})
    for gate in cert.get("gates", []):
        name = gate.get("gate")
        if name and gate.get("passes") is False:
            failed.append(name)
    if failed:
        return failed

    scores = item.get("scores", {})
    decision = item.get("decision_sufficiency", {})
    causal = item.get("causal_usefulness", {})
    completeness = item.get("task_fact_completeness", {})
    if scores.get("sender_observable_rate", 0.0) < 1.0:
        failed.append("sender_observable")
    if scores.get("receiver_necessary_rate", 0.0) < 1.0:
        failed.append("receiver_necessary")
    if scores.get("task_fact_completeness", completeness.get("coverage_rate", 0.0)) < 1.0:
        failed.append("task_fact_complete")
    if decision.get("passes_decision_sufficient") is False:
        failed.append("decision_sufficient")
    if causal.get("passes_causally_useful") is False:
        failed.append("causally_useful")
    if item.get("requires_statistical_significance") and not item.get("passes_statistical_gate"):
        failed.append("statistical_support")
    if item.get("requires_content_control") and not item.get("passes_content_gate"):
        failed.append("content_specificity")
    return failed


def primary_failure(failures):
    priority = [
        "sender_observable",
        "receiver_necessary",
        "task_fact_complete",
        "decision_sufficient",
        "causally_useful",
        "content_specificity",
        "statistical_support",
    ]
    for gate in priority:
        if gate in failures:
            return gate
    return failures[0] if failures else "accepted"


def revision_strategy(failure):
    strategies = {
        "sender_observable": (
            "Constrain message slots to features available in the declared sender observation. "
            "If a fact is not sender-observable, change the sender or remove that fact from the candidate design."
        ),
        "receiver_necessary": (
            "Make routing receiver-conditional. Do not send facts that the receiver already observes; "
            "open an edge only when the sender has information that should be missing locally at the receiver."
        ),
        "task_fact_complete": (
            "Restore all declared task facts and make them explicitly decodable from current messages."
        ),
        "decision_sufficient": (
            "Change message semantics toward action-relevant variables: target availability, threat, distance, "
            "health pressure, retreat/focus-fire cues, movement direction, target selection, and other variables "
            "that alter action evidence."
        ),
        "causally_useful": (
            "Tie each open edge to a receiver decision. Deleting that edge should remove a fact the receiver uses "
            "for movement, attack, retreat, or target selection."
        ),
        "content_specificity": (
            "Avoid constant, slot-only, or purely topological messages. Make content vary with the current observation "
            "and keep edges sparse enough that shuffled messages are measurably worse."
        ),
        "statistical_support": (
            "Prefer lower-variance, higher-signal messages. Remove opportunistic edges and redundant dimensions that "
            "can help on one split but fail resampling."
        ),
        "accepted": (
            "Do not revise. The candidate can enter frozen teacher selection under the preregistered protocol."
        ),
    }
    return strategies.get(failure, strategies["decision_sufficient"])


def round_prompt(path, item, args, candidate_label):
    failures = failed_gates(item)
    primary = primary_failure(failures)
    base = build_feedback(path, item)
    destination = (
        Path(args.candidate_root)
        / f"{item['map_name']}_candidates"
        / candidate_label
        / "comm_init.py"
    )
    round_header = f"""# DRC Revision Round Assignment

This prompt is part of an offline DRC-guided teacher search round. Use only the
certificate evidence below. Do not inspect or mention downstream RL results.

## Revision Identity

- round label: `{args.round_label}`
- map: `{item['map_name']}`
- source result: `{path}`
- source teacher: `{item.get('comm_code')}`
- accepted already: `{item.get('accepted')}`
- failed gates: `{', '.join(failures) if failures else 'none'}`
- primary repair target: `{primary}`
- repair strategy: {revision_strategy(primary)}
- destination candidate label: `{candidate_label}`
- destination file: `{destination}`

## Offline Selection Principle

The next candidate should improve the DRC estimand that failed, not the
downstream win rate. In paper language, this is a certificate-guided proposal
step: the LLM proposes a new structural communication rule, while acceptance is
still decided only by the preregistered offline certificate.

"""
    return round_header + "\n" + base


def summarize_rows(rows):
    by_map = defaultdict(list)
    failures = Counter()
    accepted = 0
    for path, item in rows:
        map_name = item.get("map_name", "unknown")
        row_failures = failed_gates(item)
        if item.get("accepted"):
            accepted += 1
        for gate in row_failures:
            failures[gate] += 1
        by_map[map_name].append((path, item, row_failures))
    return by_map, failures, accepted


def write_manifest(out_path, args, revision_rows, accepted_rows, failures):
    manifest = {
        "method": "DRC-guided-revision-round-v1",
        "round_label": args.round_label,
        "source_results": [str(Path(p)) for p in args.result],
        "candidate_root": args.candidate_root,
        "offline_only": True,
        "selection_rule": (
            "Generate revised LLM candidates from failed DRC gates only; freeze a teacher only after "
            "a subsequent formal DRC run accepts it under the preregistered protocol."
        ),
        "num_revision_prompts": len(revision_rows),
        "num_accepted_prompts": len(accepted_rows),
        "failure_counts": dict(sorted(failures.items())),
        "revision_prompts": revision_rows,
        "accepted_prompts": accepted_rows,
    }
    out_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def write_markdown(out_path, manifest):
    lines = [
        "# DRC-Guided Revision Round",
        "",
        f"- method: `{manifest['method']}`",
        f"- round label: `{manifest['round_label']}`",
        f"- offline only: `{manifest['offline_only']}`",
        f"- revision prompts: `{manifest['num_revision_prompts']}`",
        f"- accepted prompts: `{manifest['num_accepted_prompts']}`",
        "",
        "## Failure Counts",
        "",
        "| gate | count |",
        "| --- | ---: |",
    ]
    for gate, count in manifest["failure_counts"].items():
        lines.append(f"| {gate} | {count} |")
    if not manifest["failure_counts"]:
        lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Revision Prompts",
            "",
            "| map | primary repair | score | edge | prompt | destination |",
            "| --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in manifest["revision_prompts"]:
        lines.append(
            "| {map} | {primary} | {score} | {edge} | `{prompt}` | `{destination}` |".format(
                map=row["map"],
                primary=row["primary_failure"],
                score=fmt(row["score"]),
                edge=fmt(row["edge_rate"]),
                prompt=row["prompt_path"],
                destination=row["destination_file"],
            )
        )
    if not manifest["revision_prompts"]:
        lines.append("| n/a | n/a | n/a | n/a | n/a | n/a |")

    lines.extend(
        [
            "",
            "## Accepted Candidates",
            "",
            "| map | score | edge | prompt | teacher |",
            "| --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in manifest["accepted_prompts"]:
        lines.append(
            "| {map} | {score} | {edge} | `{prompt}` | `{teacher}` |".format(
                map=row["map"],
                score=fmt(row["score"]),
                edge=fmt(row["edge_rate"]),
                prompt=row["prompt_path"],
                teacher=row["teacher_path"],
            )
        )
    if not manifest["accepted_prompts"]:
        lines.append("| n/a | n/a | n/a | n/a | n/a |")

    lines.extend(
        [
            "",
            "## Protocol Note",
            "",
            "This round is a proposal mechanism, not an acceptance mechanism. A revised candidate must be "
            "added to the candidate manifest and recertified. Downstream RL remains a fixed-teacher "
            "evaluation stage and is not used for candidate revision.",
        ]
    )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate a DRC-only revision round from teacher-search results.")
    parser.add_argument("--result", nargs="+", required=True, help="DRC JSON file(s) or directories.")
    parser.add_argument(
        "--candidate-root",
        default="src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05",
        help="Root where revised candidates should be saved.",
    )
    parser.add_argument("--round-label", default="drc_revision_round")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--max-per-map", type=int, default=3)
    parser.add_argument("--include-accepted", action="store_true")
    args = parser.parse_args()

    rows = load_results(args.result)
    if not rows:
        raise SystemExit("No DRC result JSON files found.")

    by_map, failures, _ = summarize_rows(rows)
    out_dir = Path(args.out_dir)
    prompt_dir = out_dir / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)

    revision_rows = []
    accepted_rows = []
    for map_name, group in sorted(by_map.items()):
        failed_group = [(p, item, f) for p, item, f in group if not item.get("accepted")]
        failed_group.sort(
            key=lambda triple: (
                primary_failure(triple[2]),
                -float(triple[1].get("scores", {}).get("final_score", 0.0)),
                float(triple[1].get("matrix_edge_rate", 1.0)),
            )
        )
        for idx, (path, item, item_failures) in enumerate(failed_group[: args.max_per_map], start=1):
            primary = primary_failure(item_failures)
            label = safe_label(f"{args.round_label}_{Path(path).stem}_{primary}_r{idx}")
            prompt_path = prompt_dir / f"{map_name}_{label}_revision_prompt.md"
            prompt_path.write_text(round_prompt(path, item, args, label), encoding="utf-8")
            destination = (
                Path(args.candidate_root)
                / f"{map_name}_candidates"
                / label
                / "comm_init.py"
            )
            revision_rows.append(
                {
                    "map": map_name,
                    "source_result": str(path),
                    "source_teacher": item.get("comm_code"),
                    "failed_gates": item_failures,
                    "primary_failure": primary,
                    "strategy": revision_strategy(primary),
                    "candidate_label": label,
                    "destination_file": str(destination),
                    "prompt_path": str(prompt_path),
                    "score": item.get("scores", {}).get("final_score"),
                    "edge_rate": item.get("matrix_edge_rate"),
                }
            )

        if args.include_accepted:
            for path, item, _ in group:
                if not item.get("accepted"):
                    continue
                label = safe_label(f"{Path(path).stem}_freeze")
                prompt_path = prompt_dir / f"{map_name}_{label}_prompt.md"
                prompt_path.write_text(build_feedback(path, item), encoding="utf-8")
                accepted_rows.append(
                    {
                        "map": map_name,
                        "source_result": str(path),
                        "teacher_path": item.get("comm_code"),
                        "prompt_path": str(prompt_path),
                        "score": item.get("scores", {}).get("final_score"),
                        "edge_rate": item.get("matrix_edge_rate"),
                    }
                )

    manifest_path = out_dir / "revision_round_manifest.json"
    md_path = out_dir / "revision_round_manifest.md"
    manifest = write_manifest(manifest_path, args, revision_rows, accepted_rows, failures)
    write_markdown(md_path, manifest)
    print(f"Wrote {len(revision_rows)} revision prompts to {prompt_dir}")
    print(f"Wrote manifest to {manifest_path}")


if __name__ == "__main__":
    main()
