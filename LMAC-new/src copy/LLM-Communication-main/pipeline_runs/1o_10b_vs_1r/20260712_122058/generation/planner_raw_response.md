{
  "policy_hypothesis": "Efficient communication from the Overseer (the only agent able to sense the Roach) to the Banelings is essential for goal-directed movement. Additionally, broadcasting ally positions provides a common reference frame, enabling coordination and collision avoidance in complex terrain. The effectiveness depends on Banelings being able to see the Overseer to transform its relative coordinates into local frames.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [10],
      "types": ["overseer"]
    },
    {
      "group_id": "G2",
      "members": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
      "types": ["baneling"]
    }
  ],
  "rules": [
    {
      "rule_id": "R1",
      "requirement_ids": ["IR1"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_0_available"],
        "feature_indices": [4],
        "operator": "eq",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "feature is a visibility flag (0/1) documented in observation schema"
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
        "feature_indices": [5, 6, 7, 8, 9, 10]
      },
      "sender_feasibility": "The Overseer always has access to enemy_0 features when the Roach is detected; communication is feasible whenever the trigger condition holds.",
      "receiver_necessity": "Banelings cannot observe the Roach themselves and require its location to guide movement. Without this message, they resort to random exploration, dramatically reducing success.",
      "expected_rollout_behavior": "Banelings that receive the message will move towards the Roach relative to the Overseer. If they also see the Overseer, they can convert relative coordinates and approach accurately; otherwise, movement may be suboptimal.",
      "uncertainties": [
        "Relative coordinates (rel_x, rel_y) are in the Overseer's frame. If a Baneling cannot currently see the Overseer (ally_*_visible=0 for the Overseer slot), it cannot transform these coordinates into its own local frame, potentially leading to degraded movement.",
        "If the Roach remains continuously visible, the Overseer may communicate excessively, but the policy does not limit frequency."
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["ally_9_visible"],
        "feature_indices": [74],
        "operator": "eq",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "feature is a visibility flag; ally_9 corresponds to the Overseer for all Banelings based on ordered ally slots"
        }
      },
      "what": {
        "feature_names": [
          "ally_9_distance",
          "ally_9_rel_x",
          "ally_9_rel_y",
          "ally_9_health",
          "ally_9_type_0",
          "ally_9_type_1"
        ],
        "feature_indices": [75, 76, 77, 78, 79, 80]
      },
      "sender_feasibility": "Any Baneling that has the Overseer in sight can send the Overseer's relative position. If no Baneling sees the Overseer, this rule never fires.",
      "receiver_necessity": "This message helps other Banelings estimate the Overseer's position, which is critical for converting the Overseer's enemy location reports (R1) into local movement commands. It also provides an anchor for relative positioning.",
      "expected_rollout_behavior": "Banelings that lose direct sight of the Overseer can still infer its approximate location from recent messages, allowing continued pursuit of the Roach and better formation keeping.",
      "uncertainties": [
        "The rule only triggers when a Baneling directly observes the Overseer. In complete darkness or occlusion, no such message is sent, forcing reliance on stale or absent reference data.",
        "Multiple Banelings may send the same information, creating redundancy but no direct harm."
      ]
    },
    {
      "rule_id": "R3",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["ally_0_visible"],
        "feature_indices": [11],
        "operator": "eq",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "ally_0_visible indicates whether the first Baneling is visible to the Overseer; acting as a proxy that at least one ally is visible, which is almost always true given Overseer's detection capability."
        }
      },
      "what": {
        "feature_names": [
          "ally_0_distance", "ally_0_rel_x", "ally_0_rel_y", "ally_0_health", "ally_0_type_0", "ally_0_type_1",
          "ally_1_distance", "ally_1_rel_x", "ally_1_rel_y", "ally_1_health", "ally_1_type_0", "ally_1_type_1",
          "ally_2_distance", "ally_2_rel_x", "ally_2_rel_y", "ally_2_health", "ally_2_type_0", "ally_2_type_1",
          "ally_3_distance", "ally_3_rel_x", "ally_3_rel_y", "ally_3_health", "ally_3_type_0", "ally_3_type_1",
          "ally_4_distance", "ally_4_rel_x", "ally_4_rel_y", "ally_4_health", "ally_4_type_0", "ally_4_type_1",
          "ally_5_distance", "ally_5_rel_x", "ally_5_rel_y", "ally_5_health", "ally_5_type_0", "ally_5_type_1",
          "ally_6_distance", "ally_6_rel_x", "ally_6_rel_y", "ally_6_health", "ally_6_type_0", "ally_6_type_1",
          "ally_7_distance", "ally_7_rel_x", "ally_7_rel_y", "ally_7_health", "ally_7_type_0", "ally_7_type_1",
          "ally_8_distance", "ally_8_rel_x", "ally_8_rel_y", "ally_8_health", "ally_8_type_0", "ally_8_type_1",
          "ally_9_distance", "ally_9_rel_x", "ally_9_rel_y", "ally_9_health", "ally_9_type_0", "ally_9_type_1"
        ],
        "feature_indices": [
          12, 13, 14, 15, 16, 17,
          19, 20, 21, 22, 23, 24,
          26, 27, 28, 29, 30, 31,
          33, 34, 35, 36, 37, 38,
          40, 41, 42, 43, 44, 45,
          47, 48, 49, 50, 51, 52,
          54, 55, 56, 57, 58, 59,
          61, 62, 63, 64, 65, 66,
          68, 69, 70, 71, 72, 73,
          75, 76, 77, 78, 79, 80
        ]
      },
      "sender_feasibility": "The Overseer can observe all Banelings and send their full state. Communication is feasible whenever at least one Baneling is visible (ally_0_visible=1), which is effectively always given its detection role.",
      "receiver_necessity": "Banelings require knowledge of other Baneling positions to avoid collisions and coordinate paths through complex terrain. Many Banelings may be outside each other's sight range, so this broadcast fills that gap.",
      "expected_rollout_behavior": "Each Baneling receives the full ally position list from the Overseer's perspective. Combined with local sightings, they can build a more complete map of nearby allies, enabling smoother navigation and reduced path conflicts.",
      "uncertainties": [
        "The ally coordinates are in the Overseer's reference frame. The same frame‐of‐reference problem exists as in R1; a Baneling must know the Overseer's relative position to fully utilize these coordinates.",
        "The message size is large, but no communication constraints are assumed; if channel capacity were limited, this could be expensive."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "The policy relies heavily on the Overseer as a communication hub. All coordinate data from R1 and R3 are in the Overseer's frame, making the Banelings dependent on also being able to see the Overseer (or receive R2 messages). Without that, R1 may be ineffective. R2 partially mitigates this by propagating the Overseer's position when it is visible. A tradeoff exists between communication frequency (continuous broadcast by R3) and bandwidth; in an unconstrained channel this is acceptable, but a real deployment might benefit from event‐driven messaging. The default ‘no communication’ would lead to undirected Baneling movement, likely failing the task."
}