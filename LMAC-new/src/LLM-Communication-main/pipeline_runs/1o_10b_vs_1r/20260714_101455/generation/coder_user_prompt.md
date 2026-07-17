
Translate this structured LMAC communication policy into a complete Python module:

{
  "policy_hypothesis": "Overseer broadcasts Roach position to all Banelings when it sees the Roach, enabling direct approach. Banelings relay positions of visible allies back to Overseer to help Overseer move closer to distant Baneling clusters.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        10
      ],
      "role_basis": "Overseer, can detect Roach and observe all agents."
    },
    {
      "group_id": "G2",
      "members": [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9
      ],
      "role_basis": "Banelings, cannot directly see Roach, rely on communication."
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
          "enemy_0_available"
        ],
        "feature_indices": [
          4
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_0_available is a binary flag indicating Roach is visible in observation range."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_rel_x",
          "enemy_0_rel_y",
          "enemy_0_distance"
        ],
        "feature_indices": [
          6,
          7,
          5
        ]
      },
      "sender_feasibility": "Overseer always observes enemy_0_available and its components when available.",
      "receiver_necessity": "Banelings need Roach position to navigate and attack; without this they cannot complete task.",
      "expected_rollout_behavior": "When Overseer sees Roach, it continuously broadcasts Roach position; Banelings receiving this (if they also see Overseer) compute attack path.",
      "uncertainties": [
        "Only useful if Baneling can observe Overseer to perform coordinate transformation; otherwise message discarded.",
        "Communication delay and Roach movement may make info stale quickly."
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": [
        "IR3"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all members of G1",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "ally_0_visible",
          "ally_1_visible",
          "ally_2_visible",
          "ally_3_visible",
          "ally_4_visible",
          "ally_5_visible",
          "ally_6_visible",
          "ally_7_visible",
          "ally_8_visible",
          "ally_9_visible"
        ],
        "feature_indices": [
          11,
          18,
          25,
          32,
          39,
          46,
          53,
          60,
          67,
          74
        ],
        "operator": "max",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "Each ally_i_visible is 1 if that ally is currently observable by sender. max > 0.5 triggers when at least one ally is visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_0_rel_x",
          "ally_0_rel_y"
        ],
        "feature_indices": [
          13,
          14
        ]
      },
      "sender_feasibility": "Baneling can always observe its own ally visibility and corresponding relative coordinates.",
      "receiver_necessity": "Overseer needs to know positions of Banelings not directly visible to itself, to navigate towards them and extend communication coverage.",
      "expected_rollout_behavior": "Banelings broadcast position of first visible ally; Overseer aggregates to estimate unseen Baneling positions and moves to connect them.",
      "uncertainties": [
        "The relayed position is relative to sender; Overseer must know sender's own relative position to compute absolute location, possible if sender is visible.",
        "Only first ally slot transmitted; may miss other visible allies, but serves as sample.",
        "No explicit agent identity in relay; Overseer must associate sender identity with its own ally tracking to infer which Baneling is reported."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Overseer broadcasts continuously which may lead to high bandwidth, but necessary for real-time Roach tracking. Baneling ally relay attempts to improve Overseer's movement planning, but relayed position may be outdated or ambiguous. IR2 (Baneling-to-Baneling relay of Roach position) is unsupported due to lack of memory for estimated Roach position."
}

Runtime interface:
- n_agents: 11
- obs_dim: 103
- observation feature index map: {'move_north': [0, 1], 'move_south': [1, 2], 'move_east': [2, 3], 'move_west': [3, 4], 'enemy_0_available': [4, 5], 'enemy_0_distance': [5, 6], 'enemy_0_rel_x': [6, 7], 'enemy_0_rel_y': [7, 8], 'enemy_0_health': [8, 9], 'enemy_0_type_0': [9, 10], 'enemy_0_type_1': [10, 11], 'ally_0_visible': [11, 12], 'ally_0_distance': [12, 13], 'ally_0_rel_x': [13, 14], 'ally_0_rel_y': [14, 15], 'ally_0_health': [15, 16], 'ally_0_type_0': [16, 17], 'ally_0_type_1': [17, 18], 'ally_1_visible': [18, 19], 'ally_1_distance': [19, 20], 'ally_1_rel_x': [20, 21], 'ally_1_rel_y': [21, 22], 'ally_1_health': [22, 23], 'ally_1_type_0': [23, 24], 'ally_1_type_1': [24, 25], 'ally_2_visible': [25, 26], 'ally_2_distance': [26, 27], 'ally_2_rel_x': [27, 28], 'ally_2_rel_y': [28, 29], 'ally_2_health': [29, 30], 'ally_2_type_0': [30, 31], 'ally_2_type_1': [31, 32], 'ally_3_visible': [32, 33], 'ally_3_distance': [33, 34], 'ally_3_rel_x': [34, 35], 'ally_3_rel_y': [35, 36], 'ally_3_health': [36, 37], 'ally_3_type_0': [37, 38], 'ally_3_type_1': [38, 39], 'ally_4_visible': [39, 40], 'ally_4_distance': [40, 41], 'ally_4_rel_x': [41, 42], 'ally_4_rel_y': [42, 43], 'ally_4_health': [43, 44], 'ally_4_type_0': [44, 45], 'ally_4_type_1': [45, 46], 'ally_5_visible': [46, 47], 'ally_5_distance': [47, 48], 'ally_5_rel_x': [48, 49], 'ally_5_rel_y': [49, 50], 'ally_5_health': [50, 51], 'ally_5_type_0': [51, 52], 'ally_5_type_1': [52, 53], 'ally_6_visible': [53, 54], 'ally_6_distance': [54, 55], 'ally_6_rel_x': [55, 56], 'ally_6_rel_y': [56, 57], 'ally_6_health': [57, 58], 'ally_6_type_0': [58, 59], 'ally_6_type_1': [59, 60], 'ally_7_visible': [60, 61], 'ally_7_distance': [61, 62], 'ally_7_rel_x': [62, 63], 'ally_7_rel_y': [63, 64], 'ally_7_health': [64, 65], 'ally_7_type_0': [65, 66], 'ally_7_type_1': [66, 67], 'ally_8_visible': [67, 68], 'ally_8_distance': [68, 69], 'ally_8_rel_x': [69, 70], 'ally_8_rel_y': [70, 71], 'ally_8_health': [71, 72], 'ally_8_type_0': [72, 73], 'ally_8_type_1': [73, 74], 'ally_9_visible': [74, 75], 'ally_9_distance': [75, 76], 'ally_9_rel_x': [76, 77], 'ally_9_rel_y': [77, 78], 'ally_9_health': [78, 79], 'ally_9_type_0': [79, 80], 'ally_9_type_1': [80, 81], 'own_health': [81, 82], 'own_type_0': [82, 83], 'own_type_1': [83, 84], 'env_extra_84': [84, 85], 'previous_action_0': [85, 86], 'previous_action_1': [86, 87], 'previous_action_2': [87, 88], 'previous_action_3': [88, 89], 'previous_action_4': [89, 90], 'previous_action_5': [90, 91], 'previous_action_6': [91, 92], 'agent_id_0': [92, 93], 'agent_id_1': [93, 94], 'agent_id_2': [94, 95], 'agent_id_3': [95, 96], 'agent_id_4': [96, 97], 'agent_id_5': [97, 98], 'agent_id_6': [98, 99], 'agent_id_7': [99, 100], 'agent_id_8': [100, 101], 'agent_id_9': [101, 102], 'agent_id_10': [102, 103]}

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

