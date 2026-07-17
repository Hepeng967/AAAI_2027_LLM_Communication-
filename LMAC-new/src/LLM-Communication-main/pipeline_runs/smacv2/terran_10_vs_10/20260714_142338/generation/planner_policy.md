{
  "policy_hypothesis": "Sharing off-screen enemy and ally positions, own health/type, and previous actions enables better attack coordination, healing triage, and movement planning, reducing overkill, isolation, and surprise attacks despite partial observability.",
  "agent_groups": [
    {
      "group_id": "G1",
      "role_basis": "Observable own unit type: medivac serves as healer/support, incapable of attacking enemies.",
      "member_spec": "agents with own_unit_type_medivac == 1",
      "observable_indices": [
        161
      ]
    },
    {
      "group_id": "G2",
      "role_basis": "Observable own unit type: marine and marauder are damage dealers that attack enemies and may require healing.",
      "member_spec": "agents with own_unit_type_marine == 1 or own_unit_type_marauder == 1",
      "observable_indices": [
        159,
        160
      ]
    }
  ],
  "rules": [
    {
      "rule_id": "R1_enemy0_G1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
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
          "evidence": "0 means enemy not visible, 1 means visible in local sight range."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_distance",
          "enemy_0_relative_x",
          "enemy_0_relative_y",
          "enemy_0_health",
          "enemy_0_unit_type_marine",
          "enemy_0_unit_type_marauder",
          "enemy_0_unit_type_medivac"
        ],
        "feature_indices": [
          5,
          6,
          7,
          8,
          9,
          10,
          11
        ]
      },
      "sender_feasibility": "G1 medivacs can observe enemy_0 in their local sight and broadcast its state.",
      "receiver_necessity": "All agents may be outside sight of this enemy; receiving its info improves global targeting and threat avoidance.",
      "expected_rollout_behavior": "When a medivac sees enemy_0, it broadcasts its position, health, and type, allowing allies to prioritize low-health enemies or react to flankers even if they are beyond their own sight.",
      "uncertainties": [
        "receiver misses low-health enemies that could be finished quickly",
        "receiver is unaware of enemy flanking maneuvers outside its sight",
        "receiver cannot prioritize targets based on global threat picture"
      ]
    },
    {
      "rule_id": "R1_enemy0_G2",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
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
          "evidence": "0 means enemy not visible, 1 means visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_distance",
          "enemy_0_relative_x",
          "enemy_0_relative_y",
          "enemy_0_health",
          "enemy_0_unit_type_marine",
          "enemy_0_unit_type_marauder",
          "enemy_0_unit_type_medivac"
        ],
        "feature_indices": [
          5,
          6,
          7,
          8,
          9,
          10,
          11
        ]
      },
      "sender_feasibility": "G2 damage dealers observe enemy_0 and can share its state.",
      "receiver_necessity": "All agents benefit from a shared enemy picture to coordinate attacks and avoid threats.",
      "expected_rollout_behavior": "DPS agents broadcast visible enemy info, enabling allies to finish wounded enemies or prepare for incoming threats.",
      "uncertainties": [
        "receiver misses low-health enemies that could be finished quickly",
        "receiver is unaware of enemy flanking maneuvers outside its sight",
        "receiver cannot prioritize targets based on global threat picture"
      ]
    },
    {
      "rule_id": "R1_enemy1_G1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "enemy_1_available"
        ],
        "feature_indices": [
          12
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_1_distance",
          "enemy_1_relative_x",
          "enemy_1_relative_y",
          "enemy_1_health",
          "enemy_1_unit_type_marine",
          "enemy_1_unit_type_marauder",
          "enemy_1_unit_type_medivac"
        ],
        "feature_indices": [
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      },
      "sender_feasibility": "G1 can observe enemy_1 and broadcast its state.",
      "receiver_necessity": "All agents need off-screen enemy data for attack coordination.",
      "expected_rollout_behavior": "G1 shares enemy_1 info, improving global awareness.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy1_G2",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "enemy_1_available"
        ],
        "feature_indices": [
          12
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_1_distance",
          "enemy_1_relative_x",
          "enemy_1_relative_y",
          "enemy_1_health",
          "enemy_1_unit_type_marine",
          "enemy_1_unit_type_marauder",
          "enemy_1_unit_type_medivac"
        ],
        "feature_indices": [
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      },
      "sender_feasibility": "G2 can observe enemy_1 and share.",
      "receiver_necessity": "Global enemy view needed by all.",
      "expected_rollout_behavior": "G2 broadcasts enemy_1 state.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy2_G1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "enemy_2_available"
        ],
        "feature_indices": [
          20
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_2_distance",
          "enemy_2_relative_x",
          "enemy_2_relative_y",
          "enemy_2_health",
          "enemy_2_unit_type_marine",
          "enemy_2_unit_type_marauder",
          "enemy_2_unit_type_medivac"
        ],
        "feature_indices": [
          21,
          22,
          23,
          24,
          25,
          26,
          27
        ]
      },
      "sender_feasibility": "G1 sees enemy_2 and broadcasts.",
      "receiver_necessity": "Off-screen enemy data needed.",
      "expected_rollout_behavior": "Enemy_2 info shared by medivac.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy2_G2",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "enemy_2_available"
        ],
        "feature_indices": [
          20
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_2_distance",
          "enemy_2_relative_x",
          "enemy_2_relative_y",
          "enemy_2_health",
          "enemy_2_unit_type_marine",
          "enemy_2_unit_type_marauder",
          "enemy_2_unit_type_medivac"
        ],
        "feature_indices": [
          21,
          22,
          23,
          24,
          25,
          26,
          27
        ]
      },
      "sender_feasibility": "G2 observes and shares enemy_2.",
      "receiver_necessity": "Global awareness for all.",
      "expected_rollout_behavior": "DPS broadcasts enemy_2 info.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy3_G1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "enemy_3_available"
        ],
        "feature_indices": [
          28
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_3_distance",
          "enemy_3_relative_x",
          "enemy_3_relative_y",
          "enemy_3_health",
          "enemy_3_unit_type_marine",
          "enemy_3_unit_type_marauder",
          "enemy_3_unit_type_medivac"
        ],
        "feature_indices": [
          29,
          30,
          31,
          32,
          33,
          34,
          35
        ]
      },
      "sender_feasibility": "G1 broadcasts enemy_3 state.",
      "receiver_necessity": "Distribute enemy info.",
      "expected_rollout_behavior": "Medivac shares visible enemy_3.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy3_G2",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "enemy_3_available"
        ],
        "feature_indices": [
          28
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_3_distance",
          "enemy_3_relative_x",
          "enemy_3_relative_y",
          "enemy_3_health",
          "enemy_3_unit_type_marine",
          "enemy_3_unit_type_marauder",
          "enemy_3_unit_type_medivac"
        ],
        "feature_indices": [
          29,
          30,
          31,
          32,
          33,
          34,
          35
        ]
      },
      "sender_feasibility": "G2 broadcasts enemy_3.",
      "receiver_necessity": "Allies need enemy state.",
      "expected_rollout_behavior": "DPS shares enemy_3 data.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy4_G1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "enemy_4_available"
        ],
        "feature_indices": [
          36
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_4_distance",
          "enemy_4_relative_x",
          "enemy_4_relative_y",
          "enemy_4_health",
          "enemy_4_unit_type_marine",
          "enemy_4_unit_type_marauder",
          "enemy_4_unit_type_medivac"
        ],
        "feature_indices": [
          37,
          38,
          39,
          40,
          41,
          42,
          43
        ]
      },
      "sender_feasibility": "G1 sees enemy_4.",
      "receiver_necessity": "Global enemy picture improved.",
      "expected_rollout_behavior": "Medivac broadcasts enemy_4.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy4_G2",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "enemy_4_available"
        ],
        "feature_indices": [
          36
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_4_distance",
          "enemy_4_relative_x",
          "enemy_4_relative_y",
          "enemy_4_health",
          "enemy_4_unit_type_marine",
          "enemy_4_unit_type_marauder",
          "enemy_4_unit_type_medivac"
        ],
        "feature_indices": [
          37,
          38,
          39,
          40,
          41,
          42,
          43
        ]
      },
      "sender_feasibility": "G2 shares enemy_4 state.",
      "receiver_necessity": "Allies need enemy locations.",
      "expected_rollout_behavior": "DPS broadcasts enemy_4.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy5_G1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "enemy_5_available"
        ],
        "feature_indices": [
          44
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_5_distance",
          "enemy_5_relative_x",
          "enemy_5_relative_y",
          "enemy_5_health",
          "enemy_5_unit_type_marine",
          "enemy_5_unit_type_marauder",
          "enemy_5_unit_type_medivac"
        ],
        "feature_indices": [
          45,
          46,
          47,
          48,
          49,
          50,
          51
        ]
      },
      "sender_feasibility": "G1 observes enemy_5.",
      "receiver_necessity": "Share enemy position.",
      "expected_rollout_behavior": "Medivac shares enemy_5 info.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy5_G2",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "enemy_5_available"
        ],
        "feature_indices": [
          44
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_5_distance",
          "enemy_5_relative_x",
          "enemy_5_relative_y",
          "enemy_5_health",
          "enemy_5_unit_type_marine",
          "enemy_5_unit_type_marauder",
          "enemy_5_unit_type_medivac"
        ],
        "feature_indices": [
          45,
          46,
          47,
          48,
          49,
          50,
          51
        ]
      },
      "sender_feasibility": "G2 broadcasts enemy_5.",
      "receiver_necessity": "Enemy data needed.",
      "expected_rollout_behavior": "DPS shares enemy_5.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy6_G1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "enemy_6_available"
        ],
        "feature_indices": [
          52
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_6_distance",
          "enemy_6_relative_x",
          "enemy_6_relative_y",
          "enemy_6_health",
          "enemy_6_unit_type_marine",
          "enemy_6_unit_type_marauder",
          "enemy_6_unit_type_medivac"
        ],
        "feature_indices": [
          53,
          54,
          55,
          56,
          57,
          58,
          59
        ]
      },
      "sender_feasibility": "G1 sees enemy_6.",
      "receiver_necessity": "Share enemy locations.",
      "expected_rollout_behavior": "Medivac broadcasts enemy_6.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy6_G2",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "enemy_6_available"
        ],
        "feature_indices": [
          52
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_6_distance",
          "enemy_6_relative_x",
          "enemy_6_relative_y",
          "enemy_6_health",
          "enemy_6_unit_type_marine",
          "enemy_6_unit_type_marauder",
          "enemy_6_unit_type_medivac"
        ],
        "feature_indices": [
          53,
          54,
          55,
          56,
          57,
          58,
          59
        ]
      },
      "sender_feasibility": "G2 broadcasts enemy_6 state.",
      "receiver_necessity": "Global awareness.",
      "expected_rollout_behavior": "DPS shares enemy_6.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy7_G1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "enemy_7_available"
        ],
        "feature_indices": [
          60
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_7_distance",
          "enemy_7_relative_x",
          "enemy_7_relative_y",
          "enemy_7_health",
          "enemy_7_unit_type_marine",
          "enemy_7_unit_type_marauder",
          "enemy_7_unit_type_medivac"
        ],
        "feature_indices": [
          61,
          62,
          63,
          64,
          65,
          66,
          67
        ]
      },
      "sender_feasibility": "G1 observes enemy_7.",
      "receiver_necessity": "Share.",
      "expected_rollout_behavior": "Medivac shares enemy_7.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy7_G2",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "enemy_7_available"
        ],
        "feature_indices": [
          60
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_7_distance",
          "enemy_7_relative_x",
          "enemy_7_relative_y",
          "enemy_7_health",
          "enemy_7_unit_type_marine",
          "enemy_7_unit_type_marauder",
          "enemy_7_unit_type_medivac"
        ],
        "feature_indices": [
          61,
          62,
          63,
          64,
          65,
          66,
          67
        ]
      },
      "sender_feasibility": "G2 broadcasts enemy_7.",
      "receiver_necessity": "Enemy data needed.",
      "expected_rollout_behavior": "DPS shares enemy_7.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy8_G1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "enemy_8_available"
        ],
        "feature_indices": [
          68
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_8_distance",
          "enemy_8_relative_x",
          "enemy_8_relative_y",
          "enemy_8_health",
          "enemy_8_unit_type_marine",
          "enemy_8_unit_type_marauder",
          "enemy_8_unit_type_medivac"
        ],
        "feature_indices": [
          69,
          70,
          71,
          72,
          73,
          74,
          75
        ]
      },
      "sender_feasibility": "G1 sees enemy_8.",
      "receiver_necessity": "Share enemy info.",
      "expected_rollout_behavior": "Medivac broadcasts enemy_8.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy8_G2",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "enemy_8_available"
        ],
        "feature_indices": [
          68
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_8_distance",
          "enemy_8_relative_x",
          "enemy_8_relative_y",
          "enemy_8_health",
          "enemy_8_unit_type_marine",
          "enemy_8_unit_type_marauder",
          "enemy_8_unit_type_medivac"
        ],
        "feature_indices": [
          69,
          70,
          71,
          72,
          73,
          74,
          75
        ]
      },
      "sender_feasibility": "G2 broadcasts enemy_8.",
      "receiver_necessity": "Global enemy picture.",
      "expected_rollout_behavior": "DPS shares enemy_8.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy9_G1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "enemy_9_available"
        ],
        "feature_indices": [
          76
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_9_distance",
          "enemy_9_relative_x",
          "enemy_9_relative_y",
          "enemy_9_health",
          "enemy_9_unit_type_marine",
          "enemy_9_unit_type_marauder",
          "enemy_9_unit_type_medivac"
        ],
        "feature_indices": [
          77,
          78,
          79,
          80,
          81,
          82,
          83
        ]
      },
      "sender_feasibility": "G1 observes enemy_9.",
      "receiver_necessity": "Share.",
      "expected_rollout_behavior": "Medivac shares enemy_9.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R1_enemy9_G2",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "enemy_9_available"
        ],
        "feature_indices": [
          76
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "enemy_9_distance",
          "enemy_9_relative_x",
          "enemy_9_relative_y",
          "enemy_9_health",
          "enemy_9_unit_type_marine",
          "enemy_9_unit_type_marauder",
          "enemy_9_unit_type_medivac"
        ],
        "feature_indices": [
          77,
          78,
          79,
          80,
          81,
          82,
          83
        ]
      },
      "sender_feasibility": "G2 broadcasts enemy_9.",
      "receiver_necessity": "Enemy data needed.",
      "expected_rollout_behavior": "DPS shares enemy_9.",
      "uncertainties": [
        "receiver misses low-health enemies",
        "unaware of flanking",
        "no global priority"
      ]
    },
    {
      "rule_id": "R2_ally0_G1",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_0_visible"
        ],
        "feature_indices": [
          84
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_0_distance",
          "ally_slot_0_relative_x",
          "ally_slot_0_relative_y",
          "ally_slot_0_health",
          "ally_slot_0_unit_type_marine",
          "ally_slot_0_unit_type_marauder",
          "ally_slot_0_unit_type_medivac"
        ],
        "feature_indices": [
          85,
          86,
          87,
          88,
          89,
          90,
          91
        ]
      },
      "sender_feasibility": "G1 medivacs observe ally in slot 0 when visible and can broadcast its status.",
      "receiver_necessity": "All agents need off-screen ally positions to find healing or coordinate movement.",
      "expected_rollout_behavior": "When a medivac sees an ally in slot 0, it shares that ally's position, health, and type, enabling other allies to locate healers or injured units.",
      "uncertainties": [
        "medivac cannot find distant injured allies, causing unnecessary deaths",
        "dps cannot locate medivac for healing support",
        "agents may become isolated without knowledge of ally positions"
      ]
    },
    {
      "rule_id": "R2_ally0_G2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_0_visible"
        ],
        "feature_indices": [
          84
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_0_distance",
          "ally_slot_0_relative_x",
          "ally_slot_0_relative_y",
          "ally_slot_0_health",
          "ally_slot_0_unit_type_marine",
          "ally_slot_0_unit_type_marauder",
          "ally_slot_0_unit_type_medivac"
        ],
        "feature_indices": [
          85,
          86,
          87,
          88,
          89,
          90,
          91
        ]
      },
      "sender_feasibility": "G2 damage dealers also see allies and can share.",
      "receiver_necessity": "Off-screen ally data helps all coordinate, especially DPS to find medivacs.",
      "expected_rollout_behavior": "DPS agents broadcast visible ally info, aiding formation and healing requests.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation due to missing ally positions"
      ]
    },
    {
      "rule_id": "R2_ally1_G1",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_1_visible"
        ],
        "feature_indices": [
          92
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_1_distance",
          "ally_slot_1_relative_x",
          "ally_slot_1_relative_y",
          "ally_slot_1_health",
          "ally_slot_1_unit_type_marine",
          "ally_slot_1_unit_type_marauder",
          "ally_slot_1_unit_type_medivac"
        ],
        "feature_indices": [
          93,
          94,
          95,
          96,
          97,
          98,
          99
        ]
      },
      "sender_feasibility": "G1 sees slot1 ally and shares.",
      "receiver_necessity": "Expand ally awareness.",
      "expected_rollout_behavior": "Medivac shares slot1 ally info.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally1_G2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_1_visible"
        ],
        "feature_indices": [
          92
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_1_distance",
          "ally_slot_1_relative_x",
          "ally_slot_1_relative_y",
          "ally_slot_1_health",
          "ally_slot_1_unit_type_marine",
          "ally_slot_1_unit_type_marauder",
          "ally_slot_1_unit_type_medivac"
        ],
        "feature_indices": [
          93,
          94,
          95,
          96,
          97,
          98,
          99
        ]
      },
      "sender_feasibility": "G2 shares slot1 ally.",
      "receiver_necessity": "Global ally positions.",
      "expected_rollout_behavior": "DPS broadcasts slot1 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally2_G1",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_2_visible"
        ],
        "feature_indices": [
          100
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_2_distance",
          "ally_slot_2_relative_x",
          "ally_slot_2_relative_y",
          "ally_slot_2_health",
          "ally_slot_2_unit_type_marine",
          "ally_slot_2_unit_type_marauder",
          "ally_slot_2_unit_type_medivac"
        ],
        "feature_indices": [
          101,
          102,
          103,
          104,
          105,
          106,
          107
        ]
      },
      "sender_feasibility": "G1 sees slot2 ally.",
      "receiver_necessity": "Share.",
      "expected_rollout_behavior": "Medivac shares slot2 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally2_G2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_2_visible"
        ],
        "feature_indices": [
          100
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_2_distance",
          "ally_slot_2_relative_x",
          "ally_slot_2_relative_y",
          "ally_slot_2_health",
          "ally_slot_2_unit_type_marine",
          "ally_slot_2_unit_type_marauder",
          "ally_slot_2_unit_type_medivac"
        ],
        "feature_indices": [
          101,
          102,
          103,
          104,
          105,
          106,
          107
        ]
      },
      "sender_feasibility": "G2 shares slot2 ally.",
      "receiver_necessity": "Ally awareness.",
      "expected_rollout_behavior": "DPS broadcasts slot2 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally3_G1",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_3_visible"
        ],
        "feature_indices": [
          108
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_3_distance",
          "ally_slot_3_relative_x",
          "ally_slot_3_relative_y",
          "ally_slot_3_health",
          "ally_slot_3_unit_type_marine",
          "ally_slot_3_unit_type_marauder",
          "ally_slot_3_unit_type_medivac"
        ],
        "feature_indices": [
          109,
          110,
          111,
          112,
          113,
          114,
          115
        ]
      },
      "sender_feasibility": "G1 sees slot3 ally.",
      "receiver_necessity": "Share ally info.",
      "expected_rollout_behavior": "Medivac shares slot3 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally3_G2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_3_visible"
        ],
        "feature_indices": [
          108
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_3_distance",
          "ally_slot_3_relative_x",
          "ally_slot_3_relative_y",
          "ally_slot_3_health",
          "ally_slot_3_unit_type_marine",
          "ally_slot_3_unit_type_marauder",
          "ally_slot_3_unit_type_medivac"
        ],
        "feature_indices": [
          109,
          110,
          111,
          112,
          113,
          114,
          115
        ]
      },
      "sender_feasibility": "G2 shares slot3 ally.",
      "receiver_necessity": "Ally positions needed.",
      "expected_rollout_behavior": "DPS broadcasts slot3 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally4_G1",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_4_visible"
        ],
        "feature_indices": [
          116
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_4_distance",
          "ally_slot_4_relative_x",
          "ally_slot_4_relative_y",
          "ally_slot_4_health",
          "ally_slot_4_unit_type_marine",
          "ally_slot_4_unit_type_marauder",
          "ally_slot_4_unit_type_medivac"
        ],
        "feature_indices": [
          117,
          118,
          119,
          120,
          121,
          122,
          123
        ]
      },
      "sender_feasibility": "G1 sees slot4 ally.",
      "receiver_necessity": "Share.",
      "expected_rollout_behavior": "Medivac shares slot4 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally4_G2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_4_visible"
        ],
        "feature_indices": [
          116
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_4_distance",
          "ally_slot_4_relative_x",
          "ally_slot_4_relative_y",
          "ally_slot_4_health",
          "ally_slot_4_unit_type_marine",
          "ally_slot_4_unit_type_marauder",
          "ally_slot_4_unit_type_medivac"
        ],
        "feature_indices": [
          117,
          118,
          119,
          120,
          121,
          122,
          123
        ]
      },
      "sender_feasibility": "G2 shares slot4 ally.",
      "receiver_necessity": "Ally awareness.",
      "expected_rollout_behavior": "DPS broadcasts slot4 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally5_G1",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_5_visible"
        ],
        "feature_indices": [
          124
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_5_distance",
          "ally_slot_5_relative_x",
          "ally_slot_5_relative_y",
          "ally_slot_5_health",
          "ally_slot_5_unit_type_marine",
          "ally_slot_5_unit_type_marauder",
          "ally_slot_5_unit_type_medivac"
        ],
        "feature_indices": [
          125,
          126,
          127,
          128,
          129,
          130,
          131
        ]
      },
      "sender_feasibility": "G1 sees slot5 ally.",
      "receiver_necessity": "Share ally info.",
      "expected_rollout_behavior": "Medivac shares slot5 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally5_G2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_5_visible"
        ],
        "feature_indices": [
          124
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_5_distance",
          "ally_slot_5_relative_x",
          "ally_slot_5_relative_y",
          "ally_slot_5_health",
          "ally_slot_5_unit_type_marine",
          "ally_slot_5_unit_type_marauder",
          "ally_slot_5_unit_type_medivac"
        ],
        "feature_indices": [
          125,
          126,
          127,
          128,
          129,
          130,
          131
        ]
      },
      "sender_feasibility": "G2 shares slot5 ally.",
      "receiver_necessity": "Ally positions needed.",
      "expected_rollout_behavior": "DPS broadcasts slot5 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally6_G1",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_6_visible"
        ],
        "feature_indices": [
          132
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_6_distance",
          "ally_slot_6_relative_x",
          "ally_slot_6_relative_y",
          "ally_slot_6_health",
          "ally_slot_6_unit_type_marine",
          "ally_slot_6_unit_type_marauder",
          "ally_slot_6_unit_type_medivac"
        ],
        "feature_indices": [
          133,
          134,
          135,
          136,
          137,
          138,
          139
        ]
      },
      "sender_feasibility": "G1 sees slot6 ally.",
      "receiver_necessity": "Share.",
      "expected_rollout_behavior": "Medivac shares slot6 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally6_G2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_6_visible"
        ],
        "feature_indices": [
          132
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_6_distance",
          "ally_slot_6_relative_x",
          "ally_slot_6_relative_y",
          "ally_slot_6_health",
          "ally_slot_6_unit_type_marine",
          "ally_slot_6_unit_type_marauder",
          "ally_slot_6_unit_type_medivac"
        ],
        "feature_indices": [
          133,
          134,
          135,
          136,
          137,
          138,
          139
        ]
      },
      "sender_feasibility": "G2 shares slot6 ally.",
      "receiver_necessity": "Ally awareness.",
      "expected_rollout_behavior": "DPS broadcasts slot6 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally7_G1",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_7_visible"
        ],
        "feature_indices": [
          140
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_7_distance",
          "ally_slot_7_relative_x",
          "ally_slot_7_relative_y",
          "ally_slot_7_health",
          "ally_slot_7_unit_type_marine",
          "ally_slot_7_unit_type_marauder",
          "ally_slot_7_unit_type_medivac"
        ],
        "feature_indices": [
          141,
          142,
          143,
          144,
          145,
          146,
          147
        ]
      },
      "sender_feasibility": "G1 sees slot7 ally.",
      "receiver_necessity": "Share ally info.",
      "expected_rollout_behavior": "Medivac shares slot7 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally7_G2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_7_visible"
        ],
        "feature_indices": [
          140
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_7_distance",
          "ally_slot_7_relative_x",
          "ally_slot_7_relative_y",
          "ally_slot_7_health",
          "ally_slot_7_unit_type_marine",
          "ally_slot_7_unit_type_marauder",
          "ally_slot_7_unit_type_medivac"
        ],
        "feature_indices": [
          141,
          142,
          143,
          144,
          145,
          146,
          147
        ]
      },
      "sender_feasibility": "G2 shares slot7 ally.",
      "receiver_necessity": "Ally positions needed.",
      "expected_rollout_behavior": "DPS broadcasts slot7 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally8_G1",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_8_visible"
        ],
        "feature_indices": [
          148
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_8_distance",
          "ally_slot_8_relative_x",
          "ally_slot_8_relative_y",
          "ally_slot_8_health",
          "ally_slot_8_unit_type_marine",
          "ally_slot_8_unit_type_marauder",
          "ally_slot_8_unit_type_medivac"
        ],
        "feature_indices": [
          149,
          150,
          151,
          152,
          153,
          154,
          155
        ]
      },
      "sender_feasibility": "G1 sees slot8 ally.",
      "receiver_necessity": "Share.",
      "expected_rollout_behavior": "Medivac shares slot8 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R2_ally8_G2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "ally_slot_8_visible"
        ],
        "feature_indices": [
          148
        ],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "0 not visible, 1 visible."
        }
      },
      "what": {
        "feature_names": [
          "ally_slot_8_distance",
          "ally_slot_8_relative_x",
          "ally_slot_8_relative_y",
          "ally_slot_8_health",
          "ally_slot_8_unit_type_marine",
          "ally_slot_8_unit_type_marauder",
          "ally_slot_8_unit_type_medivac"
        ],
        "feature_indices": [
          149,
          150,
          151,
          152,
          153,
          154,
          155
        ]
      },
      "sender_feasibility": "G2 shares slot8 ally.",
      "receiver_necessity": "Ally awareness.",
      "expected_rollout_behavior": "DPS broadcasts slot8 ally.",
      "uncertainties": [
        "medivac cannot find distant injured allies",
        "dps cannot locate medivac",
        "isolation"
      ]
    },
    {
      "rule_id": "R3_medivac_always",
      "requirement_ids": [
        "IR3"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "own_health"
        ],
        "feature_indices": [
          156
        ],
        "operator": ">=",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "own_health is always non-negative for live agents, so this rule triggers every timestep the medivac is alive."
        }
      },
      "what": {
        "feature_names": [
          "own_health",
          "own_normalized_x",
          "own_normalized_y",
          "own_unit_type_medivac"
        ],
        "feature_indices": [
          156,
          157,
          158,
          161
        ]
      },
      "sender_feasibility": "Medivac always has access to its own health, position, and type.",
      "receiver_necessity": "All agents, especially injured DPS, need to know medivac locations to approach for healing.",
      "expected_rollout_behavior": "Medivacs continuously broadcast their type and position, enabling damaged allies to find a healer even when out of sight.",
      "uncertainties": [
        "without own-health broadcasts, medivacs are blind to the health status of allies outside their sight range",
        "dps cannot reliably find a medivac when injured"
      ]
    },
    {
      "rule_id": "R3_dps_injured",
      "requirement_ids": [
        "IR3"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "own_health"
        ],
        "feature_indices": [
          156
        ],
        "operator": "<",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "llm_hypothesis",
          "evidence": "A health level below 0.5 is assumed to represent significant damage that warrants healing attention in SMACv2."
        }
      },
      "what": {
        "feature_names": [
          "own_health",
          "own_normalized_x",
          "own_normalized_y",
          "own_unit_type_marine",
          "own_unit_type_marauder"
        ],
        "feature_indices": [
          156,
          157,
          158,
          159,
          160
        ]
      },
      "sender_feasibility": "Injured DPS agents can easily monitor their own health and broadcast their state.",
      "receiver_necessity": "Medivacs (G1) need to know which allies are injured and where, so they can triage and heal distant units.",
      "expected_rollout_behavior": "When a marine or marauder drops below half health, it broadcasts its health, position, and type, alerting medivacs to provide healing support.",
      "uncertainties": [
        "without own-health broadcasts, medivacs are blind to the health status of allies outside their sight range",
        "dps cannot reliably find a medivac when injured"
      ]
    },
    {
      "rule_id": "R4_G1_actions",
      "requirement_ids": [
        "IR4"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all",
        "observable_basis": [
          161
        ]
      },
      "when": {
        "feature_names": [
          "own_health"
        ],
        "feature_indices": [
          156
        ],
        "operator": ">=",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "own_health is always non-negative, ensuring continuous broadcast of last action."
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
          "previous_action_9",
          "previous_action_10",
          "previous_action_11",
          "previous_action_12",
          "previous_action_13",
          "previous_action_14",
          "previous_action_15"
        ],
        "feature_indices": [
          162,
          163,
          164,
          165,
          166,
          167,
          168,
          169,
          170,
          171,
          172,
          173,
          174,
          175,
          176,
          177
        ]
      },
      "sender_feasibility": "Medivac always knows its last discrete action.",
      "receiver_necessity": "Allies benefit from knowing the medivac's recent move or heal action to coordinate movement and avoid collisions.",
      "expected_rollout_behavior": "Medivacs continuously share their previous action, allowing DPS to predict healer movement and avoid overlapping paths.",
      "uncertainties": [
        "without action sharing, agents may unknowingly attack the same enemy, wasting damage",
        "agents may collide or move suboptimally if unaware of allies' last move direction"
      ]
    },
    {
      "rule_id": "R4_G2_actions",
      "requirement_ids": [
        "IR4"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all",
        "observable_basis": [
          159,
          160
        ]
      },
      "when": {
        "feature_names": [
          "own_health"
        ],
        "feature_indices": [
          156
        ],
        "operator": ">=",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "own_health is always non-negative, so action broadcast is always active."
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
          "previous_action_9",
          "previous_action_10",
          "previous_action_11",
          "previous_action_12",
          "previous_action_13",
          "previous_action_14",
          "previous_action_15"
        ],
        "feature_indices": [
          162,
          163,
          164,
          165,
          166,
          167,
          168,
          169,
          170,
          171,
          172,
          173,
          174,
          175,
          176,
          177
        ]
      },
      "sender_feasibility": "Damage dealers can always broadcast their previous action.",
      "receiver_necessity": "Allies need to know which enemy was attacked or what movement was made to coordinate focus fire and avoid collisions.",
      "expected_rollout_behavior": "DPS agents continuously share their previous discrete action, enabling allies to avoid overkill and move together.",
      "uncertainties": [
        "without action sharing, agents may unknowingly attack the same enemy, wasting damage",
        "agents may collide or move suboptimally if unaware of allies' last move direction"
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "This policy broadcasts a large number of features (up to all visible enemy/ally slots, continuous actions, and health states), which may exceed communication budgets in early training. However, it provides a rich test of the LMAC scheduler’s ability to prioritize the most critical information under a constraint. The policy deliberately omits prioritization among slots; instead, it relies on the teacher’s future refinement to select the most valuable subsets for efficient communication."
}
