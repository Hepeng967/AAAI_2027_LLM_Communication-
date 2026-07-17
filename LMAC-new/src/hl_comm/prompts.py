"""Prompt builders for the LMAC communication HL loop."""

from __future__ import annotations

import json
from textwrap import dedent


DEFAULT_MAPS = ["1o_10b_vs_1r", "1o_2r_vs_4r", "5z_vs_1ul"]


SYSTEM_CODER = (
    "You are a MARL communication-policy coding agent. Return only one complete "
    "Python file in a single ```python code block```."
)


def build_initial_prompt(
    *,
    map_name: str,
    map_spec: dict,
    task_facts: dict | None,
    rollout_summary: dict | None = None,
) -> list[dict[str, str]]:
    user = f"""
Design an initial LMAC teacher communication policy for task `{map_name}` in
environment `{map_spec.get('environment', 'smac')}`.

Map spec:
{json.dumps(map_spec, ensure_ascii=False, indent=2)}

Rollout-backed LMAC observation alignment:
{json.dumps(rollout_summary or {}, ensure_ascii=False, indent=2)}

Certified task facts, if available:
{json.dumps(task_facts or {{}}, ensure_ascii=False, indent=2)}

Required functions:
- message_design_instruction() -> str
- communication_who(o) -> tensor [batch, receiver_agent, sender_agent]
- communication_when(o) -> tensor [batch, receiver_agent, sender_agent]
- communication_what(o) -> content mask [batch, n_agents, obs_dim], values in
  [0, 1], preserving the original observation-feature positions

Constraints:
- `o` contains the collection of all allied agents' local observations. The
  policy may compare these rows, but must not read global state, files,
  randomness, trainable parameters, future information, or environment internals.
- Use `rollout_obs_dim` as the true runtime obs dimension. Documented feature
  names only cover known ranges; lmac_extra_* dimensions are wrapper-added and
  should be used conservatively.
- If `dynamic_agent_roles` is true, never infer a fixed unit role from agent ID;
  infer roles only from observable unit-type/capability fields.
- Use torch operations and keep the code deterministic.
- Self communication diagonal must be zero.
- Matrix convention: matrix[:, receiver, sender] = 1 means receiver uses sender's message.
- The runtime derives the communication matrix as clamp(who * when, 0, 1).
- WHAT selects sparse, sender-observable, receiver-necessary dimensions from the
  original observation. Do not compress or reorder selected features.
"""
    return [{"role": "system", "content": SYSTEM_CODER}, {"role": "user", "content": dedent(user).strip()}]


def build_repair_prompt(
    *,
    source_code: str,
    error: str,
    map_name: str,
    map_spec: dict,
    rollout_summary: dict | None = None,
) -> list[dict[str, str]]:
    user = f"""
Repair this LMAC teacher communication policy for `{map_name}`.

Validation error:
{error}

Map spec:
{json.dumps(map_spec, ensure_ascii=False, indent=2)}

Rollout-backed LMAC observation alignment:
{json.dumps(rollout_summary or {}, ensure_ascii=False, indent=2)}

Current code:
```python
{source_code}
```

Return a complete corrected Python file. Preserve message_design_instruction, communication,
communication_who, communication_when, and communication_what.
"""
    return [{"role": "system", "content": SYSTEM_CODER}, {"role": "user", "content": dedent(user).strip()}]


def build_summary_prompt(
    *,
    map_name: str,
    current_code: str,
    judge_summary: dict,
    rollout_evaluation: dict | None,
    recent_trials: list[dict],
) -> list[dict[str, str]]:
    system = "You analyze LLM-judged failures for LMAC communication policies. Return one compact JSON object only."
    user = f"""
Analyze the LLM judge result for map `{map_name}` and propose the next communication-code revision.

Judge summary:
{json.dumps(judge_summary, ensure_ascii=False, indent=2)}

Rollout evaluation:
{json.dumps(rollout_evaluation or {}, ensure_ascii=False, indent=2)}

Recent trials:
{json.dumps(recent_trials[-5:], ensure_ascii=False, indent=2)}

Current code:
```python
{current_code}
```

Return JSON with keys:
- Evaluation
- Missing_Information_Hypothesis
- Improvement_Suggestions
- Target_Functions
- Target_Rule_IDs
Do not use downstream RL win-rate as feedback. Focus on rollout-grounded who/when/what critique only.
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": dedent(user).strip()}]


def build_revision_prompt(
    *,
    map_name: str,
    map_spec: dict,
    rollout_summary: dict | None,
    rollout_evaluation: dict | None,
    current_code: str,
    judge_summary: dict,
    llm_feedback: str,
) -> list[dict[str, str]]:
    user = f"""
Revise this LMAC teacher communication policy for `{map_name}` using the LLM judge feedback.

Map spec:
{json.dumps(map_spec, ensure_ascii=False, indent=2)}

Rollout-backed LMAC observation alignment:
{json.dumps(rollout_summary or {}, ensure_ascii=False, indent=2)}

Rollout evaluation:
{json.dumps(rollout_evaluation or {}, ensure_ascii=False, indent=2)}

Structured judge summary:
{json.dumps(judge_summary, ensure_ascii=False, indent=2)}

LLM failure analysis:
{llm_feedback}

Current source:
```python
{current_code}
```

Revision target:
- Preserve stable `# RULE <rule_id>` comments and edit only rule IDs identified
  by the judge unless a documented cross-rule conflict requires another edit.
- who failures: edit communication_who(o).
- when failures: edit communication_when(o).
- what/content failures: edit communication_what(o).
- communication_what(o) must remain an obs-aligned [batch, n_agents, obs_dim]
  mask in [0,1]; selected features keep their original indices.
- Keep the strategy pure: use only the supplied collection of allied local
  observations, deterministic operations, and no trainable parameters or global state.

Return only a complete Python file with all required who/when/what functions.
"""
    return [{"role": "system", "content": SYSTEM_CODER}, {"role": "user", "content": dedent(user).strip()}]


def build_llm_judge_prompt(
    *,
    map_name: str,
    map_spec: dict,
    candidate_code: str,
    validation: dict,
    rollout_summary: dict | None,
    rollout_evaluation: dict | None,
    recent_trials: list[dict],
) -> list[dict[str, str]]:
    system = (
        "You are an expert MARL communication-policy judge. Evaluate the generated "
        "policy only from the task spec, code, and interface validation. Return one JSON object only."
    )
    user = f"""
Evaluate this pure LLM-generated LMAC communication strategy for task `{map_name}`
in environment `{map_spec.get('environment', 'smac')}`.

Research goal:
- We are testing the capability boundary of LLM-designed communication.
- Do NOT use DRC, decision_sufficient, causally_useful, downstream RL win-rate, or hidden/global state.
- Judge whether the policy gives a plausible pure communication strategy for who, when, and what.

Map spec:
{json.dumps(map_spec, ensure_ascii=False, indent=2)}

Rollout-backed LMAC observation alignment:
{json.dumps(rollout_summary or {}, ensure_ascii=False, indent=2)}

Interface validation:
{json.dumps(validation, ensure_ascii=False, indent=2)}

Rollout evaluation:
{json.dumps(rollout_evaluation or {}, ensure_ascii=False, indent=2)}

Recent trials:
{json.dumps(recent_trials[-5:], ensure_ascii=False, indent=2)}

Candidate code:
```python
{candidate_code}
```

Return strict JSON with keys:
{{
  "accepted": bool,
  "score": float between 0 and 1,
  "who_score": float between 0 and 1,
  "when_score": float between 0 and 1,
  "what_score": float between 0 and 1,
  "rollout_grounding_score": float between 0 and 1,
  "replacement_readiness": "direct_teacher"|"student_supervision_ready"|"not_ready",
  "blocking_failures": [{{"type": "short_name", "evidence": "specific rollout/code evidence", "revision_target": "who|when|what"}}],
  "rule_checks": [{{
    "rule_id": "R1 or a deterministic inferred ID if legacy code has no marker",
    "requirement_hypothesis": "information need served by this rule",
    "who_supported": true,
    "when_supported": true,
    "what_supported": true,
    "threshold_in_observed_range": true,
    "observed_trigger_or_edge_rate": 0.0,
    "supporting_case_ids": [],
    "counterexample_case_ids": [],
    "unresolved_questions": []
  }}],
  "cross_rule_check": {{
    "who_when_what_consistent": true,
    "conflicts_or_uncovered_requirements": []
  }},
  "evidence_case_ids": ["case ids used to support the verdict"],
  "failure_analysis": "specific critique of missing or redundant who/when/what logic",
  "improvement_suggestions": "concrete code-level changes for the next revision",
  "expected_effect": "why these changes should improve coordination"
}}

Acceptance guideline:
- accepted=true only if who, when, and what are all task-plausible and compact.
- accepted=true requires blocking_failures=[]; any always-on condition caused by
  an out-of-scale threshold, missing runtime field, interface inefficiency, or
  contradiction between analysis and code is blocking and requires revision.
- Derive conclusions from rollout feature statistics and evidence cases. Do not
  treat an agent id or feature index as required unless the task description and
  actual runtime observations support it.
- The policy must be grounded in the offline rollout statistics, not only generic SMAC knowledge.
- Favor strategies that could directly replace a fixed communication module and also supervise a learnable selector.
- Penalize all-to-all always-on matrices unless the task truly requires them.
- Penalize messages that merely copy all observations without compact task logic.
- First inventory every `# RULE <rule_id>` represented in the code. For legacy
  code without markers, infer stable IDs R1, R2, ... and state that they were inferred.
- Complete one rule_checks entry per inventoried rule. Explicitly look for
  counterexamples before accepting; a prose claim contradicted by a cited case or
  by the code is a blocking failure.
- Sparse or dense communication is not independently correct or incorrect. Treat
  communication rates as evidence and justify the verdict from task needs.
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": dedent(user).strip()}]
