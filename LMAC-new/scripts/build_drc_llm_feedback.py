#!/usr/bin/env python3
"""Build structured DRC feedback for reproducible LLM communication revision."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from components.certified_task_facts import map_specs  # noqa: E402


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
        out.append(ch.lower() if ch.isalnum() or ch in ("-", "_") else "_")
    label = "".join(out).strip("_")
    while "__" in label:
        label = label.replace("__", "_")
    return label or "drc_llm_revision"


def resolve_destination(args, item):
    map_name = item["map_name"]
    if args.destination_file:
        return str(Path(args.destination_file))
    label = safe_label(args.candidate_label or f"{args.round_label}_{Path(item.get('comm_code', 'teacher')).stem}")
    return str(Path(args.candidate_root) / f"{map_name}_candidates" / label / "comm_init.py")


def rollout_research(item):
    return {
        "current_buffer_root": item.get("buffer_root"),
        "current_collector_inference": (
            "The formal DRC buffer is shared offline rollout data. In the current code path, "
            "collect_lmac_buffers.py builds a basic_mac+rnn+qmix runner and stores obs/state/actions/reward."
        ),
        "recommended_policy_for_drc": (
            "Use a fixed, preregistered shared buffer for all candidates in the same DRC round. "
            "Prefer warm-start or mixed-stage QMIX/LMAC rollout over purely random rollout, because the "
            "oracle, local probe, comm probe, and causal edge test are all distribution-conditioned."
        ),
        "quality_effect": (
            "Trajectory quality affects DRC training: low-return or low-diversity data can make the oracle "
            "learn poor behavior labels, collapse action coverage, hide receiver uncertainty, and understate "
            "causal usefulness. High-quality but too narrow expert data can overfit to late-stage tactics and "
            "miss exploration-time communication needs."
        ),
        "audit_requirements": [
            "record collector, schema, map, seed, split, reward/return availability",
            "report action-label distribution and held-out oracle accuracy/CE",
            "keep calibration and certification buffers disjoint",
            "do not use downstream RL win-rate to revise a candidate inside the same DRC round",
        ],
        "observed_metadata": {
            "num_buffer_files": item.get("num_buffer_files"),
            "num_transitions": item.get("num_transitions"),
            "has_return_data": item.get("has_return_data"),
            "decision_label": item.get("decision_label"),
        },
    }


def task_fact_summary(map_name):
    facts = map_specs()[map_name].get("required_task_facts", [])
    return [
        {
            "fact": fact["fact"],
            "sender": fact["sender"],
            "receivers": fact["receivers"],
            "fields": fact["fields"],
            "decision_relevance": fact.get("decision_relevance", ""),
        }
        for fact in facts
    ]


def decision_feedback(item):
    decision = item.get("decision_sufficiency", {})
    conditional = decision.get("conditional_uncertain_decision_value", {})
    content = decision.get("content_specificity", {})
    passes = bool(decision.get("passes_decision_sufficient"))
    hard_enabled = bool(conditional.get("enabled"))
    facts = task_fact_summary(item["map_name"])
    suggestions = []
    for fact in facts:
        suggestions.append(
            {
                "fact": fact["fact"],
                "sender": fact["sender"],
                "receivers": fact["receivers"],
                "message_fields_to_consider": fact["fields"],
                "why": fact["decision_relevance"],
            }
        )
    return {
        "target_function": "communication(o)",
        "purpose": "what/content revision",
        "passes": passes,
        "diagnosis": (
            "message content adds enough decision information beyond receiver-local observation"
            if passes
            else "message content is not sufficiently improving receiver matching to the centralized decision oracle"
        ),
        "metrics": {
            "decision_label": item.get("decision_label"),
            "oracle_kind": decision.get("oracle_kind"),
            "central_proxy_test_acc": decision.get("central_proxy_test_acc"),
            "local_to_central_ce": decision.get("local_to_central_ce"),
            "comm_to_central_ce": decision.get("comm_to_central_ce"),
            "ce_gain": decision.get("ce_gain"),
            "accuracy_gain": decision.get("accuracy_gain"),
            "conditional_enabled": hard_enabled,
            "conditional_mode": conditional.get("mode"),
            "conditional_ce_gain": conditional.get("ce_gain"),
            "conditional_selected_samples": conditional.get("selection_rule", {}).get("selected_samples"),
            "content_specificity_shuffle_minus_true_ce": content.get("shuffle_minus_true_ce"),
        },
        "llm_edit_rule": (
            "If this block fails, edit communication(o): add or replace sender-observable fields that can "
            "change movement, attack, retreat, or target-selection evidence. Do not fix this by only opening "
            "more edges in communication_matrix(o)."
        ),
        "suggested_message_content": suggestions,
    }


def causal_feedback(item):
    causal = item.get("causal_usefulness", {})
    passes = bool(causal.get("passes_causally_useful"))
    reports = causal.get("edge_reports") or causal.get("fact_reports") or []
    rows = []
    for row in reports:
        receivers = row.get("receivers")
        if receivers is None and row.get("receiver") is not None:
            receivers = [row.get("receiver")]
        rows.append(
            {
                "fact": row.get("fact"),
                "sender": row.get("sender"),
                "receivers": receivers,
                "base_ce": row.get("base_ce"),
                "edge_dropped_ce": row.get("edge_dropped_ce"),
                "delta_causal_ce": row.get("causal_ce_increase"),
                "active_rate": row.get("active_rate"),
                "passes": row.get("passes_causally_useful"),
                "edit_hint": edge_edit_hint(row),
            }
        )
    return {
        "target_function": "communication_matrix(o)",
        "purpose": "who/when routing revision",
        "passes": passes,
        "diagnosis": (
            "declared sender-receiver edges have positive deletion-intervention value"
            if passes
            else "some open edges are redundant, noisy, or not tied to receiver decision loss under deletion"
        ),
        "metrics": {
            "mean_causal_ce_increase": causal.get("mean_causal_ce_increase"),
            "p_value_positive": causal.get("mean_causal_ce_resampling", {}).get("p_value_positive"),
            "ci_low": causal.get("mean_causal_ce_resampling", {}).get("ci_low"),
            "ci_high": causal.get("mean_causal_ce_resampling", {}).get("ci_high"),
            "matrix_edge_rate": item.get("matrix_edge_rate"),
        },
        "edge_diagnostics": rows,
        "llm_edit_rule": (
            "If this block fails, edit communication_matrix(o): preserve high positive-delta edges, suppress "
            "non-positive edges, and make overactive weak edges conditional on sender-observable facts that "
            "the receiver likely lacks. Do not change only message dimensions when the edge itself is weak."
        ),
    }


def edge_edit_hint(row):
    delta = row.get("causal_ce_increase")
    active = row.get("active_rate")
    if delta is None:
        return "Inspect this edge/fact and make routing align with receiver need."
    if delta > 0 and (active is None or active >= 0.2):
        return "Keep this edge condition; optionally make the message content sharper."
    if delta > 0 and active is not None and active < 0.2:
        return "Useful when active but underused; consider relaxing the trigger condition."
    if active is not None and active > 0.5:
        return "Overactive but weak; add a stricter receiver-need condition or remove the edge."
    return "Weak or redundant; remove this edge unless a clearer sender-observable condition exists."


def build_feedback(item, args):
    destination = resolve_destination(args, item)
    return {
        "method": "DRC-to-LLM-structured-feedback-v1",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_result": str(args.result),
        "map_name": item["map_name"],
        "source_teacher": item.get("comm_code"),
        "destination_file": destination,
        "accepted_before_revision": item.get("accepted"),
        "rollout_data_research": rollout_research(item),
        "decision_sufficient_feedback": decision_feedback(item),
        "causally_useful_feedback": causal_feedback(item),
        "internal_checks": {
            "sender_observable_rate": item.get("scores", {}).get("sender_observable_rate"),
            "receiver_necessary_rate": item.get("scores", {}).get("receiver_necessary_rate"),
            "task_fact_completeness": item.get("scores", {}).get("task_fact_completeness"),
            "note": (
                "Keep sender_observable and receiver_necessary as internal validity checks. "
                "The main LLM edit loop is driven by decision_sufficient for what and causally_useful for who/when."
            ),
        },
        "llm_contract": {
            "must_modify": ["communication(o)", "communication_matrix(o)"],
            "must_return": ["message_design_instruction()", "communication(o)", "communication_matrix(o)"],
            "forbidden": ["global state", "reward", "RL logs", "file I/O", "randomness", "trainable parameters"],
            "selection_rule": (
                "The LLM proposes code. Acceptance still requires a later DRC run and fixed-teacher RL validation."
            ),
        },
    }


def write_markdown(path, feedback):
    decision = feedback["decision_sufficient_feedback"]
    causal = feedback["causally_useful_feedback"]
    rollout = feedback["rollout_data_research"]
    lines = [
        "# DRC Auto-Research Feedback",
        "",
        f"- method: `{feedback['method']}`",
        f"- map: `{feedback['map_name']}`",
        f"- source teacher: `{feedback['source_teacher']}`",
        f"- destination: `{feedback['destination_file']}`",
        "",
        "## Rollout Data Conclusion",
        "",
        rollout["current_collector_inference"],
        "",
        f"Recommended DRC rollout policy: {rollout['recommended_policy_for_drc']}",
        "",
        f"Quality effect: {rollout['quality_effect']}",
        "",
        "## Decision Sufficient -> communication(o)",
        "",
        f"- passes: `{decision['passes']}`",
        f"- diagnosis: {decision['diagnosis']}",
        f"- CE gain: `{fmt(decision['metrics']['ce_gain'])}`",
        f"- conditional CE gain: `{fmt(decision['metrics']['conditional_ce_gain'])}`",
        f"- edit rule: {decision['llm_edit_rule']}",
        "",
        "| fact | sender | receivers | fields | why |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for row in decision["suggested_message_content"]:
        lines.append(
            f"| {row['fact']} | {row['sender']} | {row['receivers']} | {row['message_fields_to_consider']} | {row['why']} |"
        )
    lines += [
        "",
        "## Causally Useful -> communication_matrix(o)",
        "",
        f"- passes: `{causal['passes']}`",
        f"- diagnosis: {causal['diagnosis']}",
        f"- mean delta CE: `{fmt(causal['metrics']['mean_causal_ce_increase'])}`",
        f"- edge rate: `{fmt(causal['metrics']['matrix_edge_rate'])}`",
        f"- edit rule: {causal['llm_edit_rule']}",
        "",
        "| fact | sender | receivers | delta CE | active | passes | edit hint |",
        "| --- | ---: | --- | ---: | ---: | --- | --- |",
    ]
    for row in causal["edge_diagnostics"]:
        lines.append(
            f"| {row.get('fact')} | {row.get('sender')} | {row.get('receivers')} | "
            f"{fmt(row.get('delta_causal_ce'))} | {fmt(row.get('active_rate'))} | "
            f"{fmt(row.get('passes'))} | {row.get('edit_hint')} |"
        )
    if not causal["edge_diagnostics"]:
        lines.append("| n/a | n/a | n/a | n/a | n/a | n/a | no edge/fact diagnostic rows were available |")
    lines += [
        "",
        "## Reproducible LLM Contract",
        "",
        "The next LLM call must return only executable Python code defining "
        "`message_design_instruction()`, `communication(o)`, and `communication_matrix(o)`. "
        "The revised candidate must be re-certified by DRC and then validated by fixed-teacher RL.",
    ]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Build structured DRC feedback for LLM code revision.")
    parser.add_argument("--result", required=True, help="DRC result JSON.")
    parser.add_argument("--candidate-root", default="src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05")
    parser.add_argument("--candidate-label", default="")
    parser.add_argument("--round-label", default="drc_llm_revision")
    parser.add_argument("--destination-file", default="")
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    item = json.loads(Path(args.result).read_text(encoding="utf-8"))
    feedback = build_feedback(item, args)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(feedback, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    write_markdown(args.out_md, feedback)
    print(json.dumps({"feedback_json": str(out_json), "feedback_md": args.out_md, "destination_file": feedback["destination_file"]}, indent=2))


if __name__ == "__main__":
    main()
