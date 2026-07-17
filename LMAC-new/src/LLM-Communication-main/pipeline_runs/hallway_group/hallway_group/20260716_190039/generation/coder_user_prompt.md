
Translate this structured LMAC communication policy into a complete Python module:

{
  "policy_hypothesis": "Groups coordinate within themselves by sharing positions to reach 0 simultaneously, and between groups by sharing active_status upon finish and continuous positions to anticipate readiness and avoid simultaneous finishes.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        0,
        1,
        2
      ],
      "role_basis": "Fixed group assignment from task configuration; agents must finish together in a round distinct from G2."
    },
    {
      "group_id": "G2",
      "members": [
        3,
        4,
        5,
        6
      ],
      "role_basis": "Fixed group assignment from task configuration; agents must finish together in a round distinct from G1."
    }
  ],
  "rules": [
    {
      "rule_id": "R1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all agents in G1",
        "observable_basis": []
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
          "evidence": "Task specification ensures current_position is always non-negative, making the condition always true."
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
      "sender_feasibility": "Each agent in G1 directly observes its own current_position (index 0) locally.",
      "receiver_necessity": "Other G1 agents need the sender's position to coordinate simultaneous arrival at 0.",
      "expected_rollout_behavior": "Continuous sharing of positions within G1 enables all members to adjust movements and reach 0 together.",
      "uncertainties": [
        "Positions may become stale before the receiver acts due to communication delay and asynchronous action execution."
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all agents in G2",
        "observable_basis": []
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
          "evidence": "Task specification ensures current_position is always non-negative, making the condition always true."
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
      "sender_feasibility": "Each agent in G2 directly observes its own current_position (index 0) locally.",
      "receiver_necessity": "Other G2 agents need the sender's position to coordinate simultaneous arrival at 0.",
      "expected_rollout_behavior": "Continuous sharing of positions within G2 enables all members to adjust movements and reach 0 together.",
      "uncertainties": [
        "Positions may become stale before the receiver acts due to communication delay and asynchronous action execution."
      ]
    },
    {
      "rule_id": "R3",
      "requirement_ids": [
        "IR3"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all agents in G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "active_status"
        ],
        "feature_indices": [
          1
        ],
        "operator": "==",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "active_status is binary (0: finished / 1: active); a value of exactly 0 signals the group has completed its round."
        }
      },
      "what": {
        "feature_names": [
          "active_status"
        ],
        "feature_indices": [
          1
        ]
      },
      "sender_feasibility": "Each agent in G1 directly observes its group's active_status (index 1) locally.",
      "receiver_necessity": "G2 agents need to know when G1 has finished to safely complete their own finish without same‑round conflict.",
      "expected_rollout_behavior": "When G1 becomes inactive (all members at 0), a broadcast alerts G2; G2 can then finalise its own finish, reducing simultaneous finishes.",
      "uncertainties": [
        "Active_status=1 indicates G1 is still active, but G1 could decide to finish at the same moment G2 does, leading to a simultaneous finish and penalty; simple status observation does not guarantee mutual exclusion."
      ]
    },
    {
      "rule_id": "R4",
      "requirement_ids": [
        "IR4"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all agents in G1",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "active_status"
        ],
        "feature_indices": [
          1
        ],
        "operator": "==",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "active_status is binary (0: finished / 1: active); a value of exactly 0 signals the group has completed its round."
        }
      },
      "what": {
        "feature_names": [
          "active_status"
        ],
        "feature_indices": [
          1
        ]
      },
      "sender_feasibility": "Each agent in G2 directly observes its group's active_status (index 1) locally.",
      "receiver_necessity": "G1 agents need to know when G2 has finished to safely complete their own finish without same‑round conflict.",
      "expected_rollout_behavior": "When G2 becomes inactive, a broadcast alerts G1; G1 can then finalise its own finish, reducing simultaneous finishes.",
      "uncertainties": [
        "Active_status=1 indicates G2 is still active, but G2 could decide to finish at the same moment G1 does, leading to a simultaneous finish and penalty; simple status observation does not guarantee mutual exclusion."
      ]
    },
    {
      "rule_id": "R5",
      "requirement_ids": [
        "IR5"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all agents in G2",
        "observable_basis": []
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
          "evidence": "Task specification ensures current_position is always non-negative, making the condition always true."
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
      "sender_feasibility": "Each agent in G1 directly observes its own current_position (index 0) locally.",
      "receiver_necessity": "G2 agents can estimate G1's collective distance to 0, helping to determine safe timing for their own finish.",
      "expected_rollout_behavior": "Continuous sharing of G1 positions to G2 allows G2 to monitor progress and avoid finishing while G1 is still approaching 0.",
      "uncertainties": [
        "Exact finish timing depends on future actions; positional proximity does not guarantee immediate finish, especially if agents deliberately delay."
      ]
    },
    {
      "rule_id": "R6",
      "requirement_ids": [
        "IR6"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all agents in G1",
        "observable_basis": []
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
          "evidence": "Task specification ensures current_position is always non-negative, making the condition always true."
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
      "sender_feasibility": "Each agent in G2 directly observes its own current_position (index 0) locally.",
      "receiver_necessity": "G1 agents can estimate G2's collective distance to 0, helping to determine safe timing for their own finish.",
      "expected_rollout_behavior": "Continuous sharing of G2 positions to G1 allows G1 to monitor progress and avoid finishing while G2 is still approaching 0.",
      "uncertainties": [
        "Exact finish timing depends on future actions; positional proximity does not guarantee immediate finish, especially if agents deliberately delay."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Sending intra‑group positions continuously ensures synchronisation but incurs constant bandwidth. Inter‑group active_status broadcasts only on finish are sparse but risk deadlock if the first group never finishes; continuous position sharing between groups adds robustness at the cost of extra messages."
}

Runtime interface:
- n_agents: 7
- obs_dim: 12
- observation feature index map: {'current_position': [0, 1], 'active_status': [1, 2], 'previous_action_0': [2, 3], 'previous_action_1': [3, 4], 'previous_action_2': [4, 5], 'agent_id_0': [5, 6], 'agent_id_1': [6, 7], 'agent_id_2': [7, 8], 'agent_id_3': [8, 9], 'agent_id_4': [9, 10], 'agent_id_5': [10, 11], 'agent_id_6': [11, 12]}

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

