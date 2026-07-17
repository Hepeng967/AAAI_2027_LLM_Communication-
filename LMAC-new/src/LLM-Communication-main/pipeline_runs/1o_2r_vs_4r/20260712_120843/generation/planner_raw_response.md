{
  "policy_hypothesis": "Overseer, with unobstructed vision, transmits individual Reaper state to Roaches to compensate for their vision block by the central pit.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [0]
    },
    {
      "group_id": "G2",
      "members": [1, 2]
    }
  ],
  "rules": [
    {
      "rule_id": "R1_E0",
      "requirement_ids": ["IR1"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": [4, 6, 7, 8, 9, 10]
      },
      "when": {
        "feature_names": ["enemy_0_available"],
        "feature_indices": [4],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "Feature is 1 if enemy slot 0 is occupied and visible, 0 otherwise."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_available",
          "enemy_0_rel_x",
          "enemy_0_rel_y",
          "enemy_0_health",
          "enemy_0_type_0",
          "enemy_0_type_1"
        ],
        "feature_indices": [4, 6, 7, 8, 9, 10]
      },
      "sender_feasibility": "Overseer flies over the central pit, granting direct vision of all enemy slots regardless of terrain.",
      "receiver_necessity": "Roaches have local enemy_available fields always 0 due to pit; they cannot locate or target any Reaper without received positions.",
      "expected_rollout_behavior": "When enemy slot 0 is occupied/visible, the Overseer sends its full state each step. Roaches update their internal target representation and use it to navigate around the pit and attack.",
      "uncertainties": [
        "Whether Overseer vision always covers all four Reapers throughout the episode.",
        "Whether Roaches need full per-enemy state or only the closest threat."
      ]
    },
    {
      "rule_id": "R1_E1",
      "requirement_ids": ["IR1"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": [12, 14, 15, 16, 17, 18]
      },
      "when": {
        "feature_names": ["enemy_1_available"],
        "feature_indices": [12],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "Feature is 1 if enemy slot 1 is occupied and visible, 0 otherwise."
        }
      },
      "what": {
        "feature_names": [
          "enemy_1_available",
          "enemy_1_rel_x",
          "enemy_1_rel_y",
          "enemy_1_health",
          "enemy_1_type_0",
          "enemy_1_type_1"
        ],
        "feature_indices": [12, 14, 15, 16, 17, 18]
      },
      "sender_feasibility": "Overseer flies over the central pit, granting direct vision of all enemy slots regardless of terrain.",
      "receiver_necessity": "Roaches have local enemy_available fields always 0 due to pit; they cannot locate or target any Reaper without received positions.",
      "expected_rollout_behavior": "When enemy slot 1 is occupied/visible, the Overseer sends its full state each step. Roaches update their internal target representation and use it to navigate around the pit and attack.",
      "uncertainties": [
        "Whether Overseer vision always covers all four Reapers throughout the episode.",
        "Whether Roaches need full per-enemy state or only the closest threat."
      ]
    },
    {
      "rule_id": "R1_E2",
      "requirement_ids": ["IR1"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": [20, 22, 23, 24, 25, 26]
      },
      "when": {
        "feature_names": ["enemy_2_available"],
        "feature_indices": [20],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "Feature is 1 if enemy slot 2 is occupied and visible, 0 otherwise."
        }
      },
      "what": {
        "feature_names": [
          "enemy_2_available",
          "enemy_2_rel_x",
          "enemy_2_rel_y",
          "enemy_2_health",
          "enemy_2_type_0",
          "enemy_2_type_1"
        ],
        "feature_indices": [20, 22, 23, 24, 25, 26]
      },
      "sender_feasibility": "Overseer flies over the central pit, granting direct vision of all enemy slots regardless of terrain.",
      "receiver_necessity": "Roaches have local enemy_available fields always 0 due to pit; they cannot locate or target any Reaper without received positions.",
      "expected_rollout_behavior": "When enemy slot 2 is occupied/visible, the Overseer sends its full state each step. Roaches update their internal target representation and use it to navigate around the pit and attack.",
      "uncertainties": [
        "Whether Overseer vision always covers all four Reapers throughout the episode.",
        "Whether Roaches need full per-enemy state or only the closest threat."
      ]
    },
    {
      "rule_id": "R1_E3",
      "requirement_ids": ["IR1"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": [28, 30, 31, 32, 33, 34]
      },
      "when": {
        "feature_names": ["enemy_3_available"],
        "feature_indices": [28],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "Feature is 1 if enemy slot 3 is occupied and visible, 0 otherwise."
        }
      },
      "what": {
        "feature_names": [
          "enemy_3_available",
          "enemy_3_rel_x",
          "enemy_3_rel_y",
          "enemy_3_health",
          "enemy_3_type_0",
          "enemy_3_type_1"
        ],
        "feature_indices": [28, 30, 31, 32, 33, 34]
      },
      "sender_feasibility": "Overseer flies over the central pit, granting direct vision of all enemy slots regardless of terrain.",
      "receiver_necessity": "Roaches have local enemy_available fields always 0 due to pit; they cannot locate or target any Reaper without received positions.",
      "expected_rollout_behavior": "When enemy slot 3 is occupied/visible, the Overseer sends its full state each step. Roaches update their internal target representation and use it to navigate around the pit and attack.",
      "uncertainties": [
        "Whether Overseer vision always covers all four Reapers throughout the episode.",
        "Whether Roaches need full per-enemy state or only the closest threat."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Using separate rules per enemy slot ensures exhaustive communication but may cause redundant messages when multiple enemies are alive simultaneously. A single aggregated message would be more efficient but less deterministic."
}