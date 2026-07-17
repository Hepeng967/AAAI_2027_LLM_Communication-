
Translate this structured LMAC communication policy into a complete Python module:

{
  "policy_hypothesis": "The overseer uses its unobstructed aerial vision to detect all four reapers across the pit and communicates their relative positions and health to the roaches, enabling them to navigate around the pit and engage enemies.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        "overseer"
      ],
      "role_basis": "Flying unit with cross-pit vision."
    },
    {
      "group_id": "G2",
      "members": [
        "roach",
        "roach"
      ],
      "role_basis": "Ground units blocked by pit, rely on communication."
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
        "receiver_selector": "G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "enemy_0_available"
        ],
        "feature_indices": [
          4
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_0_available is 1 if enemy reaper 0 exists and is visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_rel_x",
          "enemy_0_rel_y",
          "enemy_0_health"
        ],
        "feature_indices": [
          6,
          7,
          8
        ]
      },
      "sender_feasibility": "Overseer can observe enemy reapers across the pit.",
      "receiver_necessity": "Roaches need enemy locations to navigate and attack.",
      "expected_rollout_behavior": "Roaches receive coordinates of enemy 0 and can move to engage, possibly prioritizing wounded enemies.",
      "uncertainties": [
        "Some reapers may be out of sight range",
        "Positions may become outdated due to enemy movement",
        "Roaches must integrate coordinates with local pathfinding"
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "enemy_1_available"
        ],
        "feature_indices": [
          11
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_1_available is 1 if enemy reaper 1 exists and is visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_1_rel_x",
          "enemy_1_rel_y",
          "enemy_1_health"
        ],
        "feature_indices": [
          13,
          14,
          15
        ]
      },
      "sender_feasibility": "Overseer can observe enemy reapers across the pit.",
      "receiver_necessity": "Roaches need enemy locations to navigate and attack.",
      "expected_rollout_behavior": "Roaches receive coordinates of enemy 1 and can move to engage.",
      "uncertainties": [
        "Some reapers may be out of sight range",
        "Positions may become outdated",
        "Roaches must integrate coordinates with local pathfinding"
      ]
    },
    {
      "rule_id": "R3",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "enemy_2_available"
        ],
        "feature_indices": [
          18
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_2_available is 1 if enemy reaper 2 exists and is visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_2_rel_x",
          "enemy_2_rel_y",
          "enemy_2_health"
        ],
        "feature_indices": [
          20,
          21,
          22
        ]
      },
      "sender_feasibility": "Overseer can observe enemy reapers across the pit.",
      "receiver_necessity": "Roaches need enemy locations to navigate and attack.",
      "expected_rollout_behavior": "Roaches receive coordinates of enemy 2 and can move to engage.",
      "uncertainties": [
        "Some reapers may be out of sight range",
        "Positions may become outdated",
        "Roaches must integrate coordinates with local pathfinding"
      ]
    },
    {
      "rule_id": "R4",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "enemy_3_available"
        ],
        "feature_indices": [
          25
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_3_available is 1 if enemy reaper 3 exists and is visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_3_rel_x",
          "enemy_3_rel_y",
          "enemy_3_health"
        ],
        "feature_indices": [
          27,
          28,
          29
        ]
      },
      "sender_feasibility": "Overseer can observe enemy reapers across the pit.",
      "receiver_necessity": "Roaches need enemy locations to navigate and attack.",
      "expected_rollout_behavior": "Roaches receive coordinates of enemy 3 and can move to engage.",
      "uncertainties": [
        "Some reapers may be out of sight range",
        "Positions may become outdated",
        "Roaches must integrate coordinates with local pathfinding"
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Per-enemy rule granularity ensures only visible enemies are reported; health inclusion supports prioritization; bandwidth impact is low (3 floats per visible enemy)."
}

Runtime interface:
- n_agents: 3
- obs_dim: 49
- observation feature index map: {'move_north': [0, 1], 'move_south': [1, 2], 'move_east': [2, 3], 'move_west': [3, 4], 'enemy_0_available': [4, 5], 'enemy_0_distance': [5, 6], 'enemy_0_rel_x': [6, 7], 'enemy_0_rel_y': [7, 8], 'enemy_0_health': [8, 9], 'enemy_0_type_0': [9, 10], 'enemy_0_type_1': [10, 11], 'enemy_1_available': [11, 12], 'enemy_1_distance': [12, 13], 'enemy_1_rel_x': [13, 14], 'enemy_1_rel_y': [14, 15], 'enemy_1_health': [15, 16], 'enemy_1_type_0': [16, 17], 'enemy_1_type_1': [17, 18], 'enemy_2_available': [18, 19], 'enemy_2_distance': [19, 20], 'enemy_2_rel_x': [20, 21], 'enemy_2_rel_y': [21, 22], 'enemy_2_health': [22, 23], 'enemy_2_type_0': [23, 24], 'enemy_2_type_1': [24, 25], 'enemy_3_available': [25, 26], 'enemy_3_distance': [26, 27], 'enemy_3_rel_x': [27, 28], 'enemy_3_rel_y': [28, 29], 'enemy_3_health': [29, 30], 'enemy_3_type_0': [30, 31], 'enemy_3_type_1': [31, 32], 'ally_0_visible': [32, 33], 'ally_0_distance': [33, 34], 'ally_0_rel_x': [34, 35], 'ally_0_rel_y': [35, 36], 'ally_0_health': [36, 37], 'ally_0_type_0': [37, 38], 'ally_0_type_1': [38, 39], 'ally_1_visible': [39, 40], 'ally_1_distance': [40, 41], 'ally_1_rel_x': [41, 42], 'ally_1_rel_y': [42, 43], 'ally_1_health': [43, 44], 'ally_1_type_0': [44, 45], 'ally_1_type_1': [45, 46], 'own_health': [46, 47], 'own_type_0': [47, 48], 'own_type_1': [48, 49]}

Required functions:
1. communication_who(o) -> [batch, receiver, sender] in [0,1].
2. communication_when(o) -> [batch, receiver, sender] in [0,1].
3. communication_what(o) -> an obs-aligned content mask with exactly the same
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
- Output only imports, optional vectorized helper functions, and the three
  required communication functions in one ```python block```.

Validation feedback, if any:

