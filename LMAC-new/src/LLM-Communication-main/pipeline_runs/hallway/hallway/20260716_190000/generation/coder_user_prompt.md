
Translate this structured LMAC communication policy into a complete Python module:

{
  "policy_hypothesis": "By having each agent continuously broadcast its current position, all agents can compute the remaining steps needed for each agent to reach goal 0, enabling synchronization via actions like staying or moving.",
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
  "rules": [
    {
      "rule_id": "R1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G0",
        "receiver_selector": "all_agents_except_sender",
        "observable_basis": [
          "agent_id_0",
          "agent_id_1",
          "agent_id_2",
          "agent_id_3"
        ]
      },
      "when": {
        "feature_names": [
          "current_position"
        ],
        "feature_indices": [
          0
        ],
        "operator": ">=",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "Per-task description, agent positions are always non-negative (minimum 0). This trigger fires at every timestep because position is always >=0."
        }
      },
      "what": {
        "feature_names": [
          "current_position"
        ],
        "feature_indices": [
          0
        ]
      },
      "sender_feasibility": "Agent 0 locally observes its own current_position (feature index 0), so it can send this value.",
      "receiver_necessity": "Other agents do not observe Agent 0's position; they must receive it to compute how many steps remain for Agent 0 and synchronize arrivals.",
      "expected_rollout_behavior": "Agent 0 broadcasts its position every step. Other agents receive it and use this information along with other agents' positions to decide whether to move forward or wait, aiming to reach 0 simultaneously.",
      "uncertainties": [
        "The exact decision logic (how many steps to wait) is determined by the learned policy, not the communication rule."
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all_agents_except_sender",
        "observable_basis": [
          "agent_id_0",
          "agent_id_1",
          "agent_id_2",
          "agent_id_3"
        ]
      },
      "when": {
        "feature_names": [
          "current_position"
        ],
        "feature_indices": [
          0
        ],
        "operator": ">=",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "Agent positions are documented to be >=0, so this trigger is always true, causing continuous sending."
        }
      },
      "what": {
        "feature_names": [
          "current_position"
        ],
        "feature_indices": [
          0
        ]
      },
      "sender_feasibility": "Agent 1 locally observes its own position.",
      "receiver_necessity": "Other agents need Agent 1's position to compute its remaining travel time.",
      "expected_rollout_behavior": "Continuous broadcast of Agent 1's position to all others.",
      "uncertainties": [
        "None"
      ]
    },
    {
      "rule_id": "R3",
      "requirement_ids": [
        "IR3"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all_agents_except_sender",
        "observable_basis": [
          "agent_id_0",
          "agent_id_1",
          "agent_id_2",
          "agent_id_3"
        ]
      },
      "when": {
        "feature_names": [
          "current_position"
        ],
        "feature_indices": [
          0
        ],
        "operator": ">=",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "Positions are non-negative."
        }
      },
      "what": {
        "feature_names": [
          "current_position"
        ],
        "feature_indices": [
          0
        ]
      },
      "sender_feasibility": "Agent 2 locally observes its own position.",
      "receiver_necessity": "Others need Agent 2's position for coordination.",
      "expected_rollout_behavior": "Continuous broadcast of position.",
      "uncertainties": []
    },
    {
      "rule_id": "R4",
      "requirement_ids": [
        "IR4"
      ],
      "who": {
        "sender_group": "G3",
        "receiver_selector": "all_agents_except_sender",
        "observable_basis": [
          "agent_id_0",
          "agent_id_1",
          "agent_id_2",
          "agent_id_3"
        ]
      },
      "when": {
        "feature_names": [
          "current_position"
        ],
        "feature_indices": [
          0
        ],
        "operator": ">=",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "Positions are non-negative."
        }
      },
      "what": {
        "feature_names": [
          "current_position"
        ],
        "feature_indices": [
          0
        ]
      },
      "sender_feasibility": "Agent 3 locally observes its own position.",
      "receiver_necessity": "Others need Agent 3's position for synchronization.",
      "expected_rollout_behavior": "Continuous broadcast of position.",
      "uncertainties": []
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Continuous full broadcast of positions ensures zero-latency information sharing at every step, which is ideal for tight synchronization but consumes communication bandwidth. Sparse communication (e.g., only on position change) could reduce communication but might introduce staleness if messages are lost or if agents rely on outdated information."
}

Runtime interface:
- n_agents: 4
- obs_dim: 8
- observation feature index map: {'current_position': [0, 1], 'previous_action_0': [1, 2], 'previous_action_1': [2, 3], 'previous_action_2': [3, 4], 'agent_id_0': [4, 5], 'agent_id_1': [5, 6], 'agent_id_2': [6, 7], 'agent_id_3': [7, 8]}

Required functions:
1. message_design_instruction() -> a concise string explaining the policy.
2. communication_who(o) -> [batch, receiver, sender] in [0,1].
3. communication_when(o) -> [batch, receiver, sender] in [0,1].
4. communication_what(o) -> an obs-aligned content mask with exactly the same
   shape as o, in [0,1]. A selected feature remains at its original index;
   unselected features are zero. Never compress or reorder features.

Constraints:
- o has shape [batch, n_agents, obs_dim].
- WHO and WHEN use matrix[:, receiver, sender] convention.
- WHO and WHEN must have zero self-communication diagonal.
- Use runtime o.shape[-1]; safely skip an index that is out of range.
- Use vectorized torch operations. Do not loop over batch elements, agents,
  senders, receivers, or observation dimensions.
- Implement every policy rule exactly once and mark its implementation with a
  comment containing its stable rule_id (for example, `# RULE R1`). Do not add
  tactical rules, thresholds, feature selections, or agent roles absent from the
  policy specification. If a stated rule cannot be implemented from the runtime
  observation, leave it inactive and explain why in its rule comment.
- The runtime derives edge_matrix = clamp(who * when, 0, 1) and
  masked_message = o * what_mask; do not implement extra wrapper functions.
- Output only imports, message_design_instruction, optional vectorized helper
  functions, and the three executable communication functions in one
  ```python block```.

Validation feedback, if any:

