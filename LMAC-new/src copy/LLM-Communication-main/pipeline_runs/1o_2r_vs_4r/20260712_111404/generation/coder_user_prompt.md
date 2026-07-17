
Translate this structured LMAC communication policy into a complete Python module:

{
  "policy_hypothesis": "The Overseer communicates full enemy state (availability, relative position, health) whenever any enemy is observed, enabling Roaches to locate, approach, and efficiently attack Reapers despite the vision-blocking pit.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "agent_0 (overseer)",
      "role_basis": "Only agent with vision across the central pit; enemy features are observable."
    },
    {
      "group_id": "G2",
      "members": "agent_1 (roach), agent_2 (roach)",
      "role_basis": "Ground attackers that cannot see enemies across the pit; must rely on communication for enemy information."
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
        "operator": ">",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_0_available is 0 if no enemy, 1 if an enemy exists in that slot; >0 triggers even if slot 0 is not the only enumerated enemy, ensuring communication when any enemy is alive."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_available",
          "enemy_0_rel_x",
          "enemy_0_rel_y",
          "enemy_0_health",
          "enemy_1_available",
          "enemy_1_rel_x",
          "enemy_1_rel_y",
          "enemy_1_health",
          "enemy_2_available",
          "enemy_2_rel_x",
          "enemy_2_rel_y",
          "enemy_2_health",
          "enemy_3_available",
          "enemy_3_rel_x",
          "enemy_3_rel_y",
          "enemy_3_health"
        ],
        "feature_indices": [
          4,
          6,
          7,
          8,
          11,
          13,
          14,
          15,
          18,
          20,
          21,
          22,
          25,
          27,
          28,
          29
        ]
      },
      "sender_feasibility": "Overseer directly observes all these features from its own observation vector.",
      "receiver_necessity": "Without this communication, Roaches have no knowledge of any enemy position or health and cannot perform task D1 (move toward enemy) or D2 (select which enemy to attack).",
      "expected_rollout_behavior": "Roaches will receive the Overseer-relative enemy coordinates. If they can also observe the Overseer (ally_*_visible), they can transform coordinates to own-relative frames. They will then move toward the nearest or weakest Reaper and attack, using health for focus-fire decisions.",
      "uncertainties": [
        "Coordinate transformation requires a Roach to see the Overseer; if out of sight, relative positions become unusable.",
        "Enemy slots are not ID‑stable; the same physical enemy may appear in different indices across timesteps, causing targeting errors.",
        "Communication latency may cause stale health values if a Reaper is damaged between message sending and Roach action."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "This policy prioritises full enemy‑state broadcast whenever any enemy exists, sacrificing bandwidth for completeness. Roach‑to‑Roach coordination (IR3) is not included because the Roaches have no observable trigger in their own observation to send a target intention; the policy relies on implicit coordination through movement and health‑based prioritisation."
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

