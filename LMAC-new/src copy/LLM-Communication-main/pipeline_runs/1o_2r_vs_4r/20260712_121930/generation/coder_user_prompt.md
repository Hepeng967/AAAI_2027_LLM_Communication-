
Translate this structured LMAC communication policy into a complete Python module:

{
  "policy_hypothesis": "By having the Overseer continuously broadcast enemy positions, health, and type, Roaches obtain the necessary information to move towards and prioritize Reapers. Additionally, Roaches share their last action to infer each other's targeting intention, thereby coordinating attacks and reducing duplicated efforts.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        0
      ],
      "role_basis": "Overseer (flying) can see over the pit; enemy_*_available features are expected to be 1 when enemies are in sight."
    },
    {
      "group_id": "G2",
      "members": [
        1,
        2
      ],
      "role_basis": "Roaches (ground) cannot see across the pit; enemy_*_available is expected to be 0, so they must rely on communication."
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
        "receiver_selector": "all members of G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "agent_id_0"
        ],
        "feature_indices": [
          63
        ],
        "operator": ">",
        "threshold": -1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "agent_id_0 is always 0 for the Overseer, so this condition triggers every step the Overseer is alive."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_available",
          "enemy_0_rel_x",
          "enemy_0_rel_y",
          "enemy_0_health",
          "enemy_0_type_0",
          "enemy_0_type_1",
          "enemy_1_available",
          "enemy_1_rel_x",
          "enemy_1_rel_y",
          "enemy_1_health",
          "enemy_1_type_0",
          "enemy_1_type_1",
          "enemy_2_available",
          "enemy_2_rel_x",
          "enemy_2_rel_y",
          "enemy_2_health",
          "enemy_2_type_0",
          "enemy_2_type_1",
          "enemy_3_available",
          "enemy_3_rel_x",
          "enemy_3_rel_y",
          "enemy_3_health",
          "enemy_3_type_0",
          "enemy_3_type_1"
        ],
        "feature_indices": [
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ]
      },
      "sender_feasibility": "Overseer directly observes enemies via its observation, so these features are always accessible when enemies are in sight.",
      "receiver_necessity": "Roaches cannot see enemies across the pit, so they need this information to move towards and attack Reapers.",
      "expected_rollout_behavior": "Roaches should move towards the nearest alive Reaper using received positions, and attack the one with lowest health or closest.",
      "uncertainties": [
        "Relative coordinates are from Overseer's perspective; Roaches must transform using ally_0 (Overseer) position if visible. If Roach loses sight of Overseer, transformation may fail.",
        "Overseer may lose vision of some Reapers if they move, causing incomplete or outdated information.",
        "Communication delay may cause position lag."
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "other members of G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "previous_action_0"
        ],
        "feature_indices": [
          53
        ],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "previous_action features are one-hot encoded; after an action is selected, its corresponding component becomes 1.0 and others 0.0. Thus, previous_action_0 > 0.5 indicates an action has been taken, triggering a communication."
        }
      },
      "what": {
        "feature_names": [
          "previous_action_0",
          "previous_action_1",
          "previous_action_2",
          "previous_action_3",
          "previous_action_4",
          "previous_action_5",
          "previous_action_6",
          "previous_action_7",
          "previous_action_8",
          "previous_action_9"
        ],
        "feature_indices": [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      },
      "sender_feasibility": "Roaches always observe their own previous_action after acting.",
      "receiver_necessity": "Roaches need to know which Reaper the other Roach is targeting to avoid attacking the same target and to distribute damage efficiently. By receiving the last action, they can infer the targeted enemy (e.g., attack[enemy_i] action) or movement direction, which combined with enemy position information from Overseer, allows estimation of intent.",
      "expected_rollout_behavior": "Roaches will attempt to coordinate: if both attack same enemy, they might still do damage but may switch if one sees a different action from the other. It may lead to more efficient target distribution.",
      "uncertainties": [
        "Previous actions only encode the action, not directly the enemy index if the action was movement; inference may be ambiguous.",
        "If Roaches move before receiving the other's action, coordination may lag.",
        "If actions are not informative enough (e.g., both move north), coordination may fail."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "The policy relies on constant communication from Overseer, which may be bandwidth-heavy. The Roach-to-Roach communication is limited to action encoding, which may not perfectly convey targeting intent, potentially leading to suboptimal coordination."
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

