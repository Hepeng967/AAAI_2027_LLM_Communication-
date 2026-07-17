#!/usr/bin/env python3
"""Generate LLM revision prompts from offline DRC certificate results."""

import argparse
import json
import sys
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
            if "map_name" in item and "scores" in item:
                rows.append((item_path, item))
    return rows


def fmt(value):
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def gate_status(item):
    scores = item.get("scores", {})
    decision = item.get("decision_sufficiency", {})
    causal = item.get("causal_usefulness", {})
    completeness = item.get("task_fact_completeness", {})
    return {
        "accepted": item.get("accepted"),
        "sender_observable_rate": scores.get("sender_observable_rate"),
        "receiver_necessary_rate": scores.get("receiver_necessary_rate"),
        "task_fact_completeness": scores.get("task_fact_completeness", completeness.get("coverage_rate")),
        "decision_sufficient": decision.get("passes_decision_sufficient"),
        "causally_useful": causal.get("passes_causally_useful"),
        "stat_gate": item.get("passes_statistical_gate"),
        "content_gate": item.get("passes_content_gate"),
    }


def failed_fact_notes(item):
    notes = []
    for row in item.get("observability_and_necessity", []):
        fact = row.get("fact")
        if row.get("passes_sender_observable") is False:
            notes.append(
                f"- `{fact}` sender observability failed: sender R2={fmt(row.get('sender_observability_r2'))}. "
                "Use only fields visible to the declared sender or change the sender in the task-fact registry."
            )
        if row.get("passes_receiver_necessary") is False:
            notes.append(
                f"- `{fact}` receiver necessity failed: need gain={fmt(row.get('necessity_gain_r2'))}. "
                "Avoid sending facts receivers already observe; make routing more selective."
            )
    completeness = item.get("task_fact_completeness", {})
    for row in completeness.get("fact_reports", []):
        if row.get("passes") is False:
            notes.append(
                f"- `{row.get('fact')}` task-fact completeness failed: ensure sender {row.get('sender')} "
                f"routes fields {row.get('fields')} to receivers {row.get('receivers')}."
            )
    return notes


def decision_notes(item):
    decision = item.get("decision_sufficiency", {})
    content = decision.get("content_specificity", {})
    notes = []
    if decision.get("passes_decision_sufficient") is False:
        notes.append(
            "- Decision sufficiency failed: local+message did not improve matching to the centralized oracle. "
            f"accuracy_gain={fmt(decision.get('accuracy_gain'))}, ce_gain={fmt(decision.get('ce_gain'))}. "
            "Revise message content so it changes receiver decision/action evidence, not just reconstructs facts."
        )
    if item.get("requires_statistical_significance") and not item.get("passes_statistical_gate"):
        ce_report = decision.get("ce_gain_resampling", {})
        notes.append(
            "- Statistical gate failed: the decision/causal effect was not robust under held-out resampling. "
            f"decision p={fmt(ce_report.get('p_value_positive'))}, "
            f"CI=[{fmt(ce_report.get('ci_low'))}, {fmt(ce_report.get('ci_high'))}]. "
            "Prefer simpler, higher-signal messages and fewer opportunistic edges."
        )
    if item.get("requires_content_control") and not item.get("passes_content_gate"):
        shuffle = content.get("shuffle_minus_true_resampling", {})
        notes.append(
            "- Content-specificity gate failed: true messages did not beat shuffled-message controls strongly enough. "
            f"shuffle_minus_true={fmt(content.get('shuffle_minus_true_ce'))}, "
            f"p={fmt(shuffle.get('p_value_positive'))}. "
            "Make messages depend on the current sender observation and route only to receivers that need that content."
        )
    return notes


def causal_notes(item):
    causal = item.get("causal_usefulness", {})
    notes = []
    if causal.get("passes_causally_useful") is False:
        notes.append(
            "- Causal usefulness failed: deleting certified edges did not hurt oracle matching. "
            f"mean_ce_increase={fmt(causal.get('mean_causal_ce_increase'))}. "
            "Route messages to receivers whose action choice should change when the fact is absent."
        )
    for row in causal.get("fact_reports", []):
        if row.get("passes_causally_useful") is False or row.get("passes_statistical_causally_useful") is False:
            notes.append(
                f"- `{row.get('fact')}` edge intervention weak: sender={row.get('sender')}, "
                f"receivers={row.get('receivers')}, ce_increase={fmt(row.get('causal_ce_increase'))}. "
                "Check whether the edge is always open but content is redundant, or content is useful but routed too broadly."
            )
    return notes


def task_fact_table(map_name):
    spec = map_specs()[map_name]
    lines = [
        "| fact | sender | receivers | fields | decision relevance |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for fact in spec.get("required_task_facts", []):
        lines.append(
            f"| {fact['fact']} | {fact['sender']} | {fact['receivers']} | "
            f"{fact['fields']} | {fact.get('decision_relevance', '')} |"
        )
    return "\n".join(lines)


def build_feedback(path, item):
    map_name = item["map_name"]
    status = gate_status(item)
    scores = item.get("scores", {})
    accepted = bool(item.get("accepted"))
    if accepted:
        notes = [
            "- This candidate is accepted by the configured DRC gates. Do not revise it using RL results. "
            "Freeze it if it is selected by score and bandwidth tie-break."
        ]
    else:
        notes = failed_fact_notes(item) + decision_notes(item) + causal_notes(item)
    if not notes:
        notes = [
            "- The candidate was not accepted, but no fine-grained failure note was available. "
            "Inspect the full JSON and revise only against DRC gates, not downstream RL."
        ]

    header = f"""# DRC-Guided LLM {'Freeze' if accepted else 'Revision'} Prompt

You are {'selecting/freezing' if accepted else 'revising'} a teacher communication policy for MARL using only offline DRC certificate evidence.
Do not use downstream RL win-rate, TensorBoard curves, or training loss to choose the teacher.

## Candidate Under Review

- result file: `{path}`
- map: `{map_name}`
- teacher: `{item.get('comm_code')}`
- accepted: `{item.get('accepted')}`
- final score: `{fmt(scores.get('final_score'))}`
- edge rate: `{fmt(item.get('matrix_edge_rate'))}`
- message dim: `{fmt(item.get('message_dim'))}`

## Gate Status

| gate | value |
| --- | --- |
| sender observable rate | `{fmt(status['sender_observable_rate'])}` |
| receiver necessary rate | `{fmt(status['receiver_necessary_rate'])}` |
| task-fact completeness | `{fmt(status['task_fact_completeness'])}` |
| decision sufficient | `{fmt(status['decision_sufficient'])}` |
| causally useful | `{fmt(status['causally_useful'])}` |
| statistical gate | `{fmt(status['stat_gate'])}` |
| content gate | `{fmt(status['content_gate'])}` |

## Required Task Facts

{task_fact_table(map_name)}

## DRC Failure / Selection Feedback

{chr(10).join(notes)}
"""

    if accepted:
        body = f"""
## Freeze Instructions

Do not generate a new candidate from this accepted result. The next offline step is selection:

1. Compare accepted candidates within the same DRC search directory.
2. Rank by `scores.final_score`.
3. Break ties by lower `matrix_edge_rate`.
4. Write the selected teacher into `frozen_teacher_manifest.json`.
5. Use downstream RL only for fixed-teacher validation.

Recommended selector:

```bash
/home/hp/anaconda3/envs/LMAC/bin/python scripts/select_drc_teacher.py \\
  --search-root <drc_teacher_search_dir> \\
  --require-return-data \\
  --require-stat-gate \\
  --require-content-gate \\
  --out-json <formal_out>/frozen_teacher_manifest.json \\
  --out-md <formal_out>/frozen_teacher_manifest.md
```
"""
    else:
        body = f"""
## Revision Instructions

Generate a new candidate `comm_init.py` that changes only the communication teacher:

1. Preserve all required task facts unless the feedback says a fact is not sender-observable or not receiver-necessary.
2. Prefer compact messages whose content can change receiver movement, attack, retreat, or target-selection decisions.
3. Make `communication_matrix(o)` sparse and interpretable: open an edge only when the receiver needs the sender's current task fact.
4. If decision sufficiency failed, revise message semantics or routing so local+message improves the centralized oracle proxy.
5. If causal usefulness failed, ensure deleting certified edges removes information that the receiver actually uses for action decisions.
6. If content-specificity failed, make messages depend on current sender observation and avoid constant or slot-only messages.
7. Do not use global state, reward, RL logs, file I/O, randomness, or trainable parameters.

Return only executable Python code defining:

```python
import torch as th

def message_design_instruction():
    ...

def communication(o):
    ...

def communication_matrix(o):
    ...
```

Save the new candidate under:

```text
src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05/{map_name}_candidates/<new_candidate_label>/comm_init.py
```
"""
    return header + body


def main():
    parser = argparse.ArgumentParser(description="Generate DRC-guided LLM revision prompts.")
    parser.add_argument("--result", nargs="+", required=True, help="DRC JSON file(s) or directories.")
    parser.add_argument("--only-failed", action="store_true")
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    rows = load_results(args.result)
    if args.only_failed:
        rows = [(p, item) for p, item in rows if not item.get("accepted")]
    if not rows:
        raise SystemExit("No matching DRC result JSON files found.")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for path, item in rows:
        prompt_kind = "freeze" if item.get("accepted") else "revision"
        label = f"{item['map_name']}_{Path(path).stem}_{prompt_kind}_prompt.md"
        out = out_dir / label
        out.write_text(build_feedback(path, item), encoding="utf-8")
    print(f"Wrote {len(rows)} DRC feedback prompts to {out_dir}")


if __name__ == "__main__":
    main()
