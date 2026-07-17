
Translate this structured LMAC communication policy into a complete Python module:

{
  "policy_hypothesis": "Overseer detects visible Reapers and selectively broadcasts individual enemy position, health, and type to both Roaches. The per-enemy trigger ensures bandwidth is used only for active threats, giving Roaches the data needed to navigate across the pit and engage specific targets.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        "agent_0"
      ],
      "role": "overseer (full vision across pit, sends enemy information)"
    },
    {
      "group_id": "G2",
      "members": [
        "agent_1",
        "agent_2"
      ],
      "role": "roach (cannot see enemies, receives targeting information)"
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
        "operator": "gt",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "enemy_0_available is 1 if enemy 0 is alive and visible, 0 otherwise"
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_distance",
          "enemy_0_rel_x",
          "enemy_0_rel_y",
          "enemy_0_health",
          "enemy_0_type_0",
          "enemy_0_type_1"
        ],
        "feature_indices": [
          5,
          6,
          7,
          8,
          9,
          10
        ]
      },
      "sender_feasibility": "Overseer can observe enemy_0 information directly from its observation (indices 4-10).",
      "receiver_necessity": "Roaches cannot observe any enemy features because the terrain pit blocks line-of-sight; they rely on this message to gain targeting data.",
      "expected_rollout_behavior": "Whenever enemy 0 is alive and visible, Overseer sends its distance, relative position, health, and type. Roaches receive the message and can coordinate navigation and attack on that enemy.",
      "uncertainties": [
        "Enemy positions are relative to Overseer; Roaches must combine communicated data with their own observed ally_0 distance/direction to compute world-relative coordinates.",
        "Communication delay may cause stale locations if enemies or Overseer move before the data is received and processed.",
        "If multiple enemies are present, multiple rules may trigger simultaneously, potentially causing message collisions if bandwidth is severely limited."
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
          12
        ],
        "operator": "gt",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "enemy_1_available is 1 if enemy 1 is alive and visible, 0 otherwise"
        }
      },
      "what": {
        "feature_names": [
          "enemy_1_distance",
          "enemy_1_rel_x",
          "enemy_1_rel_y",
          "enemy_1_health",
          "enemy_1_type_0",
          "enemy_1_type_1"
        ],
        "feature_indices": [
          13,
          14,
          15,
          16,
          17,
          18
        ]
      },
      "sender_feasibility": "Overseer can observe enemy_1 information directly from its observation (indices 12-18).",
      "receiver_necessity": "Same as R1: Roaches cannot see enemy 1 locally.",
      "expected_rollout_behavior": "Similar to R1 but for enemy 1. Allows Roaches to track and engage a second enemy if present.",
      "uncertainties": [
        "Coordinate transformation and staleness risks identical to R1.",
        "Overlapping communication from multiple rules may require Roaches to distinguish messages by enemy index."
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
          20
        ],
        "operator": "gt",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "enemy_2_available is 1 if enemy 2 is alive and visible, 0 otherwise"
        }
      },
      "what": {
        "feature_names": [
          "enemy_2_distance",
          "enemy_2_rel_x",
          "enemy_2_rel_y",
          "enemy_2_health",
          "enemy_2_type_0",
          "enemy_2_type_1"
        ],
        "feature_indices": [
          21,
          22,
          23,
          24,
          25,
          26
        ]
      },
      "sender_feasibility": "Overseer can observe enemy_2 information directly (indices 20-26).",
      "receiver_necessity": "Same as above.",
      "expected_rollout_behavior": "Adds support for a third enemy, ensuring all visible Reapers can be communicated to Roaches.",
      "uncertainties": [
        "Same coordinate/staleness issues.",
        "Message ordering and correlation may become more complex with multiple rules triggering simultaneously."
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
          28
        ],
        "operator": "gt",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "enemy_3_available is 1 if enemy 3 is alive and visible, 0 otherwise"
        }
      },
      "what": {
        "feature_names": [
          "enemy_3_distance",
          "enemy_3_rel_x",
          "enemy_3_rel_y",
          "enemy_3_health",
          "enemy_3_type_0",
          "enemy_3_type_1"
        ],
        "feature_indices": [
          29,
          30,
          31,
          32,
          33,
          34
        ]
      },
      "sender_feasibility": "Overseer can observe enemy_3 information directly (indices 28-34).",
      "receiver_necessity": "Same as above.",
      "expected_rollout_behavior": "Completes coverage for up to four Reapers. Each rule fires independently when the corresponding enemy appears, giving Roaches a full picture.",
      "uncertainties": [
        "All previous uncertainties apply.",
        "In practice, not all enemy slots may be occupied; empty‑slot rules never trigger, conserving bandwidth."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Four separate rules per enemy slot provide per‑target bandwidth efficiency but may increase rule management overhead. A single aggregate rule sending all enemy data when any enemy is available is simpler but wastes bandwidth on empty slots. This per‑enemy design maximises information density while keeping triggers observable and local to the Overseer’s raw features."
}

Runtime interface:
- n_agents: 3
- obs_dim: 66
- observation feature index map: {'move_north': [0, 1], 'move_south': [1, 2], 'move_east': [2, 3], 'move_west': [3, 4], 'enemy_0_available': [4, 5], 'enemy_0_distance': [5, 6], 'enemy_0_rel_x': [6, 7], 'enemy_0_rel_y': [7, 8], 'enemy_0_health': [8, 9], 'enemy_0_type_0': [9, 10], 'enemy_0_type_1': [10, 11], 'enemy_0_unused_health_padding': [11, 12], 'enemy_1_available': [12, 13], 'enemy_1_distance': [13, 14], 'enemy_1_rel_x': [14, 15], 'enemy_1_rel_y': [15, 16], 'enemy_1_health': [16, 17], 'enemy_1_type_0': [17, 18], 'enemy_1_type_1': [18, 19], 'enemy_1_unused_health_padding': [19, 20], 'enemy_2_available': [20, 21], 'enemy_2_distance': [21, 22], 'enemy_2_rel_x': [22, 23], 'enemy_2_rel_y': [23, 24], 'enemy_2_health': [24, 25], 'enemy_2_type_0': [25, 26], 'enemy_2_type_1': [26, 27], 'enemy_2_unused_health_padding': [27, 28], 'enemy_3_available': [28, 29], 'enemy_3_distance': [29, 30], 'enemy_3_rel_x': [30, 31], 'enemy_3_rel_y': [31, 32], 'enemy_3_health': [32, 33], 'enemy_3_type_0': [33, 34], 'enemy_3_type_1': [34, 35], 'enemy_3_unused_health_padding': [35, 36], 'ally_0_visible': [36, 37], 'ally_0_distance': [37, 38], 'ally_0_rel_x': [38, 39], 'ally_0_rel_y': [39, 40], 'ally_0_health': [40, 41], 'ally_0_type_0': [41, 42], 'ally_0_type_1': [42, 43], 'ally_1_visible': [43, 44], 'ally_1_distance': [44, 45], 'ally_1_rel_x': [45, 46], 'ally_1_rel_y': [46, 47], 'ally_1_health': [47, 48], 'ally_1_type_0': [48, 49], 'ally_1_type_1': [49, 50], 'own_health': [50, 51], 'own_type_0': [51, 52], 'own_type_1': [52, 53], 'previous_action_0': [53, 54], 'previous_action_1': [54, 55], 'previous_action_2': [55, 56], 'previous_action_3': [56, 57], 'previous_action_4': [57, 58], 'previous_action_5': [58, 59], 'previous_action_6': [59, 60], 'previous_action_7': [60, 61], 'previous_action_8': [61, 62], 'previous_action_9': [62, 63], 'agent_id_0': [63, 64], 'agent_id_1': [64, 65], 'agent_id_2': [65, 66]}

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

