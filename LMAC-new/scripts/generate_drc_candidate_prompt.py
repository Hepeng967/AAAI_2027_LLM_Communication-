#!/usr/bin/env python3
"""Generate DRC-aware prompts for LLM teacher communication candidates."""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from components.certified_task_facts import map_specs  # noqa: E402


def fact_table(facts):
    lines = [
        "| fact | sender | receivers | obs fields | sender feasible | receiver necessary | decision relevance |",
        "| --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for fact in facts:
        lines.append(
            "| {fact} | {sender} | {receivers} | {fields} | {feasibility} | {necessity} | {decision} |".format(
                fact=fact["fact"],
                sender=fact["sender"],
                receivers=json.dumps(fact["receivers"]),
                fields=json.dumps(fact["fields"]),
                feasibility=fact.get("feasibility", ""),
                necessity=fact.get("necessity", ""),
                decision=fact.get("decision_relevance", ""),
            )
        )
    return "\n".join(lines)


def default_variant_block():
    return """
Generate one candidate at a time. Candidate labels should describe the design, for example:

- `anchor_sparse`: keep certified sender-to-receiver edges and avoid broad all-to-all routing.
- `necessity_gated`: open non-certified edges only when a sender observes a task fact and a receiver likely lacks it.
- `emergency_context`: add compact low-health or imminent-attack context only when it can change retreat or focus decisions.

Do not choose a candidate by downstream RL. The candidate will later be frozen in a manifest and evaluated by DRC.
""".strip()


def build_prompt(map_name, args):
    spec = map_specs()[map_name]
    facts = spec.get("required_task_facts", [])
    probes = spec.get("task_probes", [])
    variant_block = args.variant_block or default_variant_block()
    return f"""# DRC-Aware LLM Communication Candidate Prompt

You are designing a frozen teacher communication policy for a multi-agent reinforcement learning system.
The policy will be evaluated offline by Decision-Relevant Certification (DRC) before any student RL training.

## Map

- map: `{map_name}`
- number of agents: `{spec["n_agents"]}`
- observation dimension: `{spec["obs_dim"]}`
- time sequence length: `{spec["time_seq"]}`

## Required Decision-Relevant Task Facts

The teacher must be designed around these facts. Do not optimize for full-state reconstruction.

{fact_table(facts)}

## Static Perturbation Probes

DRC will check whether the required facts are covered by the message content and routing:

```json
{json.dumps(probes, indent=2)}
```

## Certification Requirements

Your candidate should be written so that it can pass the following offline DRC gates:

1. `sender_observable`: each transmitted fact must be recoverable from the declared sender observation.
2. `receiver_necessary`: receivers should not already know the same fact locally.
3. `task_fact_complete`: every required task fact above must be covered.
4. `decision_sufficient`: messages should help a receiver match a centralized state-conditioned decision oracle.
5. `causally_useful`: deleting certified sender-to-receiver edges should make decision matching worse.

The candidate will also be checked by a shuffled-message negative control. Therefore the message content must be semantically aligned with the current observation, not just extra input capacity.

## Candidate Design Policy

{variant_block}

## Required Python Output

Return only executable Python code. The file must define:

```python
import torch as th

def message_design_instruction():
    \"\"\"Return a concise explanation of sender feasibility, receiver necessity,
    task-fact completeness, decision sufficiency, causal usefulness, and compactness.\"\"\"
    return "..."

def communication(o):
    \"\"\"Input o has shape [batch, n_agents, obs_dim].
    Return enhanced observations with received messages appended to each receiver.
    Do not append a sender's own message to itself.
    Use only features available in o.
    Keep operations torch-compatible and device-safe.\"\"\"
    ...
    return enhanced_o

def communication_matrix(o):
    \"\"\"Return matrix with shape [batch, receiver, sender].
    matrix[:, receiver, sender] = 1 means receiver uses sender's message.
    Diagonal self-communication must be zero.
    The matrix should encode when/who communication decisions.\"\"\"
    ...
    return matrix
```

## Hard Constraints

- No trainable parameters.
- No global state access.
- No downstream RL statistics.
- No file I/O, networking, randomness, or environment calls.
- Use only local observation tensor `o`.
- Keep message dimensionality compact.
- Preserve all certified task-fact edges unless you provide a strictly more selective condition that still covers the required fact.
- Prefer sparse, interpretable routing over all-to-all communication.

## Output Location Convention

Save the resulting candidate as:

```text
src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05/{map_name}_candidates/<candidate_label>/comm_init.py
```

After generating candidates, freeze them with:

```bash
/home/hp/anaconda3/envs/LMAC/bin/python scripts/make_drc_candidate_manifest.py \\
  --maps {map_name} \\
  --require-valid \\
  --out-json description/certification_gate/drc_candidates_<STAMP>.json \\
  --out-md description/certification_gate/drc_candidates_<STAMP>.md
```
"""


def main():
    parser = argparse.ArgumentParser(description="Generate DRC-aware LLM prompts for teacher candidates.")
    parser.add_argument("--maps", nargs="+", default=None, choices=sorted(map_specs()))
    parser.add_argument("--variant-block", default="")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--print", action="store_true", dest="print_stdout")
    args = parser.parse_args()

    maps = args.maps or sorted(map_specs())
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for map_name in maps:
        prompt = build_prompt(map_name, args)
        out = out_dir / f"{map_name}_drc_candidate_prompt.md"
        out.write_text(prompt + "\n", encoding="utf-8")
        if args.print_stdout:
            print(f"===== {map_name} =====")
            print(prompt)
    print(f"Wrote {len(maps)} DRC candidate prompts to {out_dir}")


if __name__ == "__main__":
    main()
