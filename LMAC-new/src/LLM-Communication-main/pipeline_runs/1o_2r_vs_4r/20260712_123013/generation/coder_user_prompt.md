
Translate this structured LMAC communication policy into a complete Python module:

{
  "policy_hypothesis": "In the 1o_2r_vs_4r map, the Overseer has full vision of all Reapers and serves as an information hub, broadcasting enemy positions and health to the blind Roaches. Roaches additionally coordinate their attack targets by sharing intended target indices, mitigating overkill. The communication policy is deterministic, with rules triggering on relevant observations.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        "overseer"
      ],
      "role_basis": "Flying unit not blocked by the pit, can see all enemies."
    },
    {
      "group_id": "G2",
      "members": [
        "roach",
        "roach"
      ],
      "role_basis": "Ground units blocked by the pit, cannot see enemies initially, rely on Overseer intel."
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
        "receiver_selector": "group:G2",
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
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_*_available is a binary flag (0 or 1); 1 indicates the Overseer currently sees the Reaper."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_rel_x",
          "enemy_0_rel_y",
          "enemy_1_rel_x",
          "enemy_1_rel_y",
          "enemy_2_rel_x",
          "enemy_2_rel_y",
          "enemy_3_rel_x",
          "enemy_3_rel_y"
        ],
        "feature_indices": [
          6,
          7,
          14,
          15,
          22,
          23,
          30,
          31
        ]
      },
      "sender_feasibility": "Overseer's observation includes enemy relative coordinates for all four Reapers because enemy_*_available flags are 1.",
      "receiver_necessity": "Roaches need Reaper positions to compute movement directions around the pit; without this they cannot navigate towards the enemy side.",
      "expected_rollout_behavior": "Overseer continuously broadcasts all enemy positions every step. Roaches receive and use them to move towards the nearest Reaper.",
      "uncertainties": [
        "Coordinates are relative to the Overseer; Roaches must transform them using their own observation of the Overseer's relative position (ally_* features) to get egocentric coordinates.",
        "Reaper movement can make position data stale between updates."
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "group:G2",
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
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "Same as R1; Overseer's enemy_*_available=1 triggers health sharing."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_health",
          "enemy_1_health",
          "enemy_2_health",
          "enemy_3_health"
        ],
        "feature_indices": [
          8,
          16,
          24,
          32
        ]
      },
      "sender_feasibility": "Overseer observes health of each Reaper.",
      "receiver_necessity": "Roaches need health to focus fire on the weakest Reapers, improving elimination speed and reducing incoming damage.",
      "expected_rollout_behavior": "Overseer broadcasts health values. Roaches use them to select the Reaper with lowest health as primary target.",
      "uncertainties": [
        "Health changes dynamically during combat; communicated values may be outdated before the Roach acts."
      ]
    },
    {
      "rule_id": "R3",
      "requirement_ids": [
        "IR3"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "peer_agents",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "own_health"
        ],
        "feature_indices": [
          50
        ],
        "operator": ">",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "The agent's own health remains positive while alive; this trigger ensures the Roach sends its intention every step it is active."
        }
      },
      "what": {
        "feature_names": [],
        "feature_indices": []
      },
      "sender_feasibility": "The sender Roach can derive an intended target index (0‑3) from its policy (e.g., selecting the Reaper with the lowest received health) and encode it in the communication vector. This index is not a raw observation feature but a computed decision variable.",
      "receiver_necessity": "Receiving Roach uses the target intention to avoid attacking the same Reaper, reducing overkill and improving team damage distribution.",
      "expected_rollout_behavior": "Each Roach sends its currently intended target index at every step. The peer Roach uses this to pick a different target if possible.",
      "uncertainties": [
        "Intended target is not directly observable in the sender's own observation; it relies on a learned encoding from the sender's policy network.",
        "If transmission/decision delay occurs, the sender's actual target may have changed by the time the receiver acts."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Centralized observation via the Overseer creates a single point of information which simplifies Roach decision‑making but may become a bottleneck. Broadcasting all enemy data every step provides robustness against outdated information but increases communication load. Roach intention sharing improves coordination but adds extra communication overhead; the empty 'what' relies on the learning process to encode the target index efficiently."
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

