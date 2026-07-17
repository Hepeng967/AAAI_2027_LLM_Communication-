
Translate this structured LMAC communication policy into a complete Python module:

{
  "policy_hypothesis": "Overseer broadcasts all enemy positions and health to roaches, enabling them to navigate around the pit and focus fire on the weakest enemy, achieving coordinated attacks without explicit target assignment.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        0
      ],
      "type": "overseer"
    },
    {
      "group_id": "G2",
      "members": [
        1,
        2
      ],
      "type": "roach"
    }
  ],
  "rules": [
    {
      "rule_id": "R1",
      "requirement_ids": [
        "IR1",
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "group G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "enemy_0_available"
        ],
        "feature_indices": [
          4
        ],
        "operator": ">",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_0_available is a binary flag (0 or 1); threshold >0 fires on any positive value (i.e., when enemy_0 exists and is visible)."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_available",
          "enemy_0_distance",
          "enemy_0_rel_x",
          "enemy_0_rel_y",
          "enemy_0_health",
          "enemy_0_type_0",
          "enemy_0_type_1",
          "enemy_1_available",
          "enemy_1_distance",
          "enemy_1_rel_x",
          "enemy_1_rel_y",
          "enemy_1_health",
          "enemy_1_type_0",
          "enemy_1_type_1",
          "enemy_2_available",
          "enemy_2_distance",
          "enemy_2_rel_x",
          "enemy_2_rel_y",
          "enemy_2_health",
          "enemy_2_type_0",
          "enemy_2_type_1",
          "enemy_3_available",
          "enemy_3_distance",
          "enemy_3_rel_x",
          "enemy_3_rel_y",
          "enemy_3_health",
          "enemy_3_type_0",
          "enemy_3_type_1"
        ],
        "feature_indices": [
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19,
          20,
          21,
          22,
          23,
          24,
          25,
          26,
          27,
          28,
          29,
          30,
          31
        ]
      },
      "sender_feasibility": "Overseer can observe all enemy features (indices 4-31) from its side of the pit, likely with full map vision or sufficient range.",
      "receiver_necessity": "Roaches lack vision across the pit and need enemy locations (relative coordinates) to navigate and attack. Health information enables focus fire on the weakest enemy without explicit assignment.",
      "expected_rollout_behavior": "Roaches will use the received enemy positions to move around the pit and engage the enemy with the lowest health, achieving implicit coordination.",
      "uncertainties": [
        "Trigger condition relies solely on enemy_0_available; if enemy_0 dies early but other enemies remain alive, the rule stops firing, depriving roaches of updated data. This could be mitigated by using a different trigger (e.g., any enemy available) but single‑feature constraint prevents it.",
        "Assumes overseer always sees all enemies; vision may degrade if overseer moves too far or enemies are out of range.",
        "Implicit coordination via ‘attack lowest health’ may lead to overkill if roaches have slightly delayed information or different movement speeds."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Sending the entire enemy observation block (28 features) ensures roaches have all necessary data for movement and target selection, but it consumes significant communication bandwidth. A sparser approach (e.g., sending only the nearest enemy) would be more efficient but could harm coordination if enemies split up. The single‑trigger condition is simple but leaves a potential gap when enemy_0 is dead. The policy avoids explicit per‑roach target assignment, trusting that all roaches will independently converge on the same enemy via a common policy (lowest health); this fails if their observations or world state differ due to latency or partial updates."
}

Runtime interface:
- n_agents: 3
- obs_dim: 66
- observation feature index map: {'move_north': [0, 1], 'move_south': [1, 2], 'move_east': [2, 3], 'move_west': [3, 4], 'enemy_0_available': [4, 5], 'enemy_0_distance': [5, 6], 'enemy_0_rel_x': [6, 7], 'enemy_0_rel_y': [7, 8], 'enemy_0_health': [8, 9], 'enemy_0_type_0': [9, 10], 'enemy_0_type_1': [10, 11], 'enemy_1_available': [11, 12], 'enemy_1_distance': [12, 13], 'enemy_1_rel_x': [13, 14], 'enemy_1_rel_y': [14, 15], 'enemy_1_health': [15, 16], 'enemy_1_type_0': [16, 17], 'enemy_1_type_1': [17, 18], 'enemy_2_available': [18, 19], 'enemy_2_distance': [19, 20], 'enemy_2_rel_x': [20, 21], 'enemy_2_rel_y': [21, 22], 'enemy_2_health': [22, 23], 'enemy_2_type_0': [23, 24], 'enemy_2_type_1': [24, 25], 'enemy_3_available': [25, 26], 'enemy_3_distance': [26, 27], 'enemy_3_rel_x': [27, 28], 'enemy_3_rel_y': [28, 29], 'enemy_3_health': [29, 30], 'enemy_3_type_0': [30, 31], 'enemy_3_type_1': [31, 32], 'ally_0_visible': [32, 33], 'ally_0_distance': [33, 34], 'ally_0_rel_x': [34, 35], 'ally_0_rel_y': [35, 36], 'ally_0_health': [36, 37], 'ally_0_type_0': [37, 38], 'ally_0_type_1': [38, 39], 'ally_1_visible': [39, 40], 'ally_1_distance': [40, 41], 'ally_1_rel_x': [41, 42], 'ally_1_rel_y': [42, 43], 'ally_1_health': [43, 44], 'ally_1_type_0': [44, 45], 'ally_1_type_1': [45, 46], 'own_health': [46, 47], 'own_type_0': [47, 48], 'own_type_1': [48, 49], 'env_extra_49': [49, 50], 'env_extra_50': [50, 51], 'env_extra_51': [51, 52], 'env_extra_52': [52, 53], 'previous_action_0': [53, 54], 'previous_action_1': [54, 55], 'previous_action_2': [55, 56], 'previous_action_3': [56, 57], 'previous_action_4': [57, 58], 'previous_action_5': [58, 59], 'previous_action_6': [59, 60], 'previous_action_7': [60, 61], 'previous_action_8': [61, 62], 'previous_action_9': [62, 63], 'agent_id_0': [63, 64], 'agent_id_1': [64, 65], 'agent_id_2': [65, 66]}

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

