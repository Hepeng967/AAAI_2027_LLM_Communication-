
Task and aligned observation description:
hallway coordination task 'hallway'
- Objective: All agents must reach position 0 on the same timestep.
- Number of agents: 4.
- Per-agent maximum positions: [4, 6, 8, 10].
- Actions: {0: 'stay', 1: 'move one step toward 0', 2: 'move one step away from 0'}.
- Information boundary: Each agent locally observes only its own current position.
- Raw local observation length: 1.
- Runtime LMAC communication input length: 8.
- Runtime input appends previous-action one-hot and agent-ID one-hot to the raw observation.
- Agent ID may be used to recover the fixed maximum-position assignment from the task configuration.
- Failure condition: The episode terminates unsuccessfully if only a subset reaches position 0.
- Observation feature index map:
    - 0~0: current_position
    - 1~1: previous_action_0
    - 2~2: previous_action_1
    - 3~3: previous_action_2
    - 4~4: agent_id_0
    - 5~5: agent_id_1
    - 6~6: agent_id_2
    - 7~7: agent_id_3
- Runtime alignment: The LMAC policy consumes raw environment observation followed by previous-action one-hot and agent-id one-hot. For this rollout: environment observation indices are [0,0], previous action indices are [1,3], and agent ID indices are [4,7]. WHAT should prioritize environment observations; previous action or agent ID may only be selected with an explicit coordination justification. Undocumented env_extra dimensions must not be assigned invented semantics.

Information-requirement analysis:
{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Choose action (move toward 0, stay, or move away) at each timestep to coordinate simultaneous arrival at position 0.",
      "locally_missing_information": [
        "Current positions of all other agents.",
        "Intended future actions or movement speed of other agents.",
        "Possibly the maximum position of other agents if not known from task configuration (assumed known from agent ID mapping)."
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G0",
      "members": "Agent 0",
      "role_basis": "Maximum position 4 (shortest distance to goal)."
    },
    {
      "group_id": "G1",
      "members": "Agent 1",
      "role_basis": "Maximum position 6."
    },
    {
      "group_id": "G2",
      "members": "Agent 2",
      "role_basis": "Maximum position 8."
    },
    {
      "group_id": "G3",
      "members": "Agent 3",
      "role_basis": "Maximum position 10 (longest distance to goal)."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Current position of Agent 0",
      "possible_sender_groups": [
        "G0"
      ],
      "possible_receiver_groups": [
        "G1",
        "G2",
        "G3"
      ],
      "sender_observable_features": [
        {
          "name": "current_position",
          "index": 0
        }
      ],
      "receiver_need_hypothesis": "Receivers need to know Agent 0's distance to goal to compute how many steps it needs and whether to wait/adjust to synchronize arrival.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Receiver does not know Agent 0's current position; cannot infer its remaining travel time without direct communication."
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "Current position of Agent 1",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G0",
        "G2",
        "G3"
      ],
      "sender_observable_features": [
        {
          "name": "current_position",
          "index": 0
        }
      ],
      "receiver_need_hypothesis": "Receivers need Agent 1's distance to goal for synchronization.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Uncertainty about Agent 1's current position and remaining steps."
      ]
    },
    {
      "requirement_id": "IR3",
      "fact": "Current position of Agent 2",
      "possible_sender_groups": [
        "G2"
      ],
      "possible_receiver_groups": [
        "G0",
        "G1",
        "G3"
      ],
      "sender_observable_features": [
        {
          "name": "current_position",
          "index": 0
        }
      ],
      "receiver_need_hypothesis": "Receivers need Agent 2's distance to goal for synchronization.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Uncertainty about Agent 2's current position and remaining steps."
      ]
    },
    {
      "requirement_id": "IR4",
      "fact": "Current position of Agent 3",
      "possible_sender_groups": [
        "G3"
      ],
      "possible_receiver_groups": [
        "G0",
        "G1",
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "current_position",
          "index": 0
        }
      ],
      "receiver_need_hypothesis": "Receivers need Agent 3's distance to goal for synchronization.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Uncertainty about Agent 3's current position and remaining steps."
      ]
    }
  ],
  "unsupported_assumptions": []
}

Return this policy schema:
{
  "policy_hypothesis":"...",
  "agent_groups":[...],
  "rules":[
    {"rule_id":"R1","requirement_ids":["IR1"],
      "who":{"sender_group":"G1","receiver_selector":"...","observable_basis":[]},
      "when":{"feature_names":["..."],"feature_indices":[0],"operator":"...",
        "threshold":0.0,"threshold_basis":{"type":"binary_semantics|documented_semantics|rollout_distribution|relative_comparison|llm_hypothesis","evidence":"..."}},
      "what":{"feature_names":["..."],"feature_indices":[0]},
      "sender_feasibility":"...","receiver_necessity":"...",
      "expected_rollout_behavior":"...","uncertainties":[]}
  ],
  "default_behavior":"no communication",
  "design_tradeoffs":"..."
}
Feature indices must match the supplied aligned schema. Do not invent runtime
fields. A threshold without a documented or observed basis must be explicitly
labelled llm_hypothesis. Prefer no communication only as a default, not as a
hard-coded claim that sparse communication is always superior.
