{
  "policy_hypothesis": "Overseer continuously shares enemy positions and health to enable Roaches to locate and target Reapers across the pit.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        0
      ],
      "role_basis": "Overseer with global vision of enemies"
    },
    {
      "group_id": "G2",
      "members": [
        1,
        2
      ],
      "role_basis": "Roaches that lack direct enemy vision due to pit"
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
        "receiver_selector": "all roaches in G2",
        "observable_basis": [
          "ally_0_visible",
          "ally_1_visible"
        ]
      },
      "when": {
        "feature_names": [
          "own_health"
        ],
        "feature_indices": [
          46
        ],
        "operator": ">",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "Agent health is always positive while alive; dead agents cannot communicate, so this fires every step the sender is alive."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_available",
          "enemy_0_distance",
          "enemy_0_rel_x",
          "enemy_0_rel_y",
          "enemy_0_health",
          "enemy_1_available",
          "enemy_1_distance",
          "enemy_1_rel_x",
          "enemy_1_rel_y",
          "enemy_1_health",
          "enemy_2_available",
          "enemy_2_distance",
          "enemy_2_rel_x",
          "enemy_2_rel_y",
          "enemy_2_health",
          "enemy_3_available",
          "enemy_3_distance",
          "enemy_3_rel_x",
          "enemy_3_rel_y",
          "enemy_3_health"
        ],
        "feature_indices": [
          4,
          5,
          6,
          7,
          8,
          11,
          12,
          13,
          14,
          15,
          18,
          19,
          20,
          21,
          22,
          25,
          26,
          27,
          28,
          29
        ]
      },
      "sender_feasibility": "Overseer has full observation of all enemies and can send every step without resource cost.",
      "receiver_necessity": "Roaches cannot see enemies across pit and need this information to move and attack effectively.",
      "expected_rollout_behavior": "Overseer broadcasts enemy positions and health continuously; Roaches use the data to navigate toward the closest or weakest Reaper and engage.",
      "uncertainties": [
        "Overseer vision range may be limited and not see all Reapers in some configurations.",
        "Communicated positions may become stale before Roaches can act, reducing effectiveness.",
        "Coordinate transformation from Overseer-relative to Roach-relative frames may introduce errors if not calibrated."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Continuous communication is simple and robust but may waste bandwidth if state changes slowly or enemies are out of reach; a more efficient trigger could be based on enemy movement or first sight."
}
