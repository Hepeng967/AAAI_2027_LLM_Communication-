"""Two-stage structured planner for LMAC WHO/WHEN/WHAT teachers."""

import json
import re
import time

from LLM.call_llm_api.call_llm import TextChatbot
import config


ANALYZER_SYSTEM_PROMPT = """
You are a MARL communication information-requirement analyst. Analyze only
decision-relevant information gaps. Do not write code and do not prescribe a
communication policy yet. Use only the supplied task and observation schema.
Return one strict JSON object and no markdown.
"""

PLANNER_SYSTEM_PROMPT = """
You are a structured LMAC communication-policy planner. Convert an information-
requirement analysis into a deterministic WHO/WHEN/WHAT policy specification.
Every communication rule must bind one WHO selector, one observable WHEN trigger,
and one obs-aligned WHAT feature selection under a stable rule_id. Do not write
Python. Return one strict JSON object and no markdown.
"""


def _extract_json(text):
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError:
        start, end = stripped.find("{"), stripped.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("Planner did not return a JSON object")
        value = json.loads(stripped[start:end + 1])
    if not isinstance(value, dict):
        raise ValueError("Planner JSON must be an object")
    return value


class LLMPlanner:
    def __init__(self):
        self.planner_bot = TextChatbot("planner")
        self.system_content = PLANNER_SYSTEM_PROMPT
        self.task_content = config.task_config
        self.analysis_prompt = self._build_analysis_prompt()
        self.policy_prompt = ""
        self.last_requirements = None
        self.last_policy_spec = None
        self.last_analysis_response = ""
        self.last_policy_response = ""

    def _build_analysis_prompt(self):
        return f"""
Task and aligned observation description:
{self.task_content}

Identify information requirements before designing communication. Return:
{{
  "task_decisions": [{{"decision_id":"D1","decision":"...","locally_missing_information":["..."]}}],
  "agent_groups": [{{"group_id":"G1","members":"...","role_basis":"observation/task evidence"}}],
  "information_requirements": [
    {{"requirement_id":"IR1","fact":"...","possible_sender_groups":["G1"],
      "possible_receiver_groups":["G1"],"sender_observable_features":
      [{{"name":"...","index":0}}],"receiver_need_hypothesis":"...",
      "task_decision_ids":["D1"],"uncertainties":["..."]}}
  ],
  "unsupported_assumptions": []
}}
Do not assume a designated agent, threshold, feature, or sparse/dense topology
without explaining its task/observation basis.
"""

    def _build_policy_prompt(self, requirements):
        return f"""
Task and aligned observation description:
{self.task_content}

Information-requirement analysis:
{json.dumps(requirements, ensure_ascii=False, indent=2)}

Return this policy schema:
{{
  "policy_hypothesis":"...",
  "agent_groups":[...],
  "rules":[
    {{"rule_id":"R1","requirement_ids":["IR1"],
      "who":{{"sender_group":"G1","receiver_selector":"...","observable_basis":[]}},
      "when":{{"feature_names":["..."],"feature_indices":[0],"operator":"...",
        "threshold":0.0,"threshold_basis":{{"type":"binary_semantics|documented_semantics|rollout_distribution|relative_comparison|llm_hypothesis","evidence":"..."}}}},
      "what":{{"feature_names":["..."],"feature_indices":[0]}},
      "sender_feasibility":"...","receiver_necessity":"...",
      "expected_rollout_behavior":"...","uncertainties":[]}}
  ],
  "default_behavior":"no communication",
  "design_tradeoffs":"..."
}}
Feature indices must match the supplied aligned schema. Do not invent runtime
fields. A threshold without a documented or observed basis must be explicitly
labelled llm_hypothesis. Prefer no communication only as a default, not as a
hard-coded claim that sparse communication is always superior.
"""

    def analyze(self):
        print("[LLMPlanner] stage 1/2: analyzing information requirements...")
        last_error = None
        for attempt in range(1, 4):
            response = self.planner_bot.query(
                ANALYZER_SYSTEM_PROMPT, self.analysis_prompt, maintain_history=False
            )
            self.last_analysis_response = response
            try:
                self.last_requirements = _extract_json(response)
                break
            except (ValueError, json.JSONDecodeError) as exc:
                last_error = exc
                print(f"[LLMPlanner] analyzer JSON invalid, retry {attempt}/3: {exc}")
                if attempt < 3:
                    time.sleep(1)
        else:
            raise ValueError(f"Analyzer failed to return valid JSON after 3 attempts: {last_error}")
        print("[LLMPlanner] information requirements generated.")
        return self.last_requirements

    def plan(self, message=None):
        requirements = message if isinstance(message, dict) else self.analyze()
        self.policy_prompt = self._build_policy_prompt(requirements)
        print("[LLMPlanner] stage 2/2: generating structured WHO/WHEN/WHAT policy...")
        last_error = None
        for attempt in range(1, 4):
            response = self.planner_bot.query(
                PLANNER_SYSTEM_PROMPT, self.policy_prompt, maintain_history=False
            )
            self.last_policy_response = response
            try:
                spec = _extract_json(response)
                break
            except (ValueError, json.JSONDecodeError) as exc:
                last_error = exc
                print(f"[LLMPlanner] policy JSON invalid, retry {attempt}/3: {exc}")
                if attempt < 3:
                    time.sleep(1)
        else:
            raise ValueError(f"Planner failed to return valid JSON after 3 attempts: {last_error}")
        rules = spec.get("rules")
        if not isinstance(rules, list) or not rules:
            raise ValueError("Structured planner returned no communication rules")
        ids = [rule.get("rule_id") for rule in rules if isinstance(rule, dict)]
        if len(ids) != len(rules) or len(set(ids)) != len(ids) or any(not item for item in ids):
            raise ValueError("Every policy rule needs a unique non-empty rule_id")
        self.last_policy_spec = spec
        print(f"[LLMPlanner] structured policy generated with {len(rules)} rule(s).")
        return spec
