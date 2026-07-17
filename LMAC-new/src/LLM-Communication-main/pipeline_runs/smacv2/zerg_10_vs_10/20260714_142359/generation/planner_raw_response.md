{
  "policy_hypothesis": "By sharing own identity, position, health, and type periodically, all agents can construct a map of allied status. Broadcasting visible enemy information (global position, health, type) enables focus fire and threat assessment. Sharing observed ally status further refines the team picture, supporting movement, assistance, and baneling timing. Communication across all unit types leverages partial observability into near-complete situational awareness.",
  "agent_groups": [
    {
      "group_id": "ALL",
      "members": "all agents, regardless of type",
      "observable_basis": []
    },
    {
      "group_id": "G1",
      "members": "agents with own_unit_type_zergling == 1",
      "observable_basis": [159]
    },
    {
      "group_id": "G2",
      "members": "agents with own_unit_type_hydralisk == 1",
      "observable_basis": [160]
    },
    {
      "group_id": "G3",
      "members": "agents with own_unit_type_baneling == 1",
      "observable_basis": [161]
    }
  ],
  "rules": [
    {
      "rule_id": "R1",
      "requirement_ids": ["IR1"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["own_health"],
        "feature_indices": [156],
        "operator": ">",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "llm_hypothesis",
          "evidence": "own_health is always positive when the agent is alive, so this triggers every step while alive, providing periodic status updates."
        }
      },
      "what": {
        "feature_names": [
          "own_health",
          "own_normalized_x",
          "own_normalized_y",
          "own_unit_type_zergling",
          "own_unit_type_hydralisk",
          "own_unit_type_baneling",
          "agent_id_0",
          "agent_id_1",
          "agent_id_2",
          "agent_id_3",
          "agent_id_4",
          "agent_id_5",
          "agent_id_6",
          "agent_id_7",
          "agent_id_8",
          "agent_id_9"
        ],
        "feature_indices": [156, 157, 158, 159, 160, 161, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187]
      },
      "sender_feasibility": "Every agent has direct access to its own health, position, unit type, and agent ID one-hot.",
      "receiver_necessity": "Receivers need ally identities, positions, types, and health to coordinate movement, assist damaged allies, and interpret enemy sightings relative to allies.",
      "expected_rollout_behavior": "All agents periodically broadcast their full identity and status, allowing each agent to maintain a complete allied team map.",
      "uncertainties": [
        "Global normalized coordinates may have alignment issues across agents.",
        "Agent ID one-hot is included despite being a runtime feature; indispensable for disambiguating allies."
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_0_available"],
        "feature_indices": [4],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_0_available is 0 or 1; >0.5 triggers when enemy is visible in slot 0."
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "enemy_0_available",
          "enemy_0_distance",
          "enemy_0_relative_x",
          "enemy_0_relative_y",
          "enemy_0_health",
          "enemy_0_unit_type_zergling",
          "enemy_0_unit_type_hydralisk",
          "enemy_0_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 4, 5, 6, 7, 8, 9, 10, 11]
      },
      "sender_feasibility": "Sender observes enemy slot 0 features directly; own position is needed to compute enemy global position.",
      "receiver_necessity": "Enemy health, type, and global position are critical for focus fire, threat prioritization, and movement decisions.",
      "expected_rollout_behavior": "Whenever enemy 0 is visible, its full status is broadcast; other enemies are covered by similar rules for other slots.",
      "uncertainties": [
        "Enemy slot index is sender-specific; communication via global coordinates disambiguates the specific enemy.",
        "Global position computation assumes aligned coordinate axes."
      ]
    },
    {
      "rule_id": "R3",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_1_available"],
        "feature_indices": [12],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_1_available is 0 or 1."
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "enemy_1_available",
          "enemy_1_distance",
          "enemy_1_relative_x",
          "enemy_1_relative_y",
          "enemy_1_health",
          "enemy_1_unit_type_zergling",
          "enemy_1_unit_type_hydralisk",
          "enemy_1_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 12, 13, 14, 15, 16, 17, 18, 19]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Builds shared enemy map.",
      "expected_rollout_behavior": "Broadcasts enemy 1 when visible.",
      "uncertainties": [
        "Slot aliasing; resolved via global coordinates."
      ]
    },
    {
      "rule_id": "R4",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_2_available"],
        "feature_indices": [20],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "enemy_2_available",
          "enemy_2_distance",
          "enemy_2_relative_x",
          "enemy_2_relative_y",
          "enemy_2_health",
          "enemy_2_unit_type_zergling",
          "enemy_2_unit_type_hydralisk",
          "enemy_2_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 20, 21, 22, 23, 24, 25, 26, 27]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Shared map.",
      "expected_rollout_behavior": "Enemy 2 broadcast when visible.",
      "uncertainties": []
    },
    {
      "rule_id": "R5",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_3_available"],
        "feature_indices": [28],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "enemy_3_available",
          "enemy_3_distance",
          "enemy_3_relative_x",
          "enemy_3_relative_y",
          "enemy_3_health",
          "enemy_3_unit_type_zergling",
          "enemy_3_unit_type_hydralisk",
          "enemy_3_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 28, 29, 30, 31, 32, 33, 34, 35]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Shared map.",
      "expected_rollout_behavior": "Enemy 3 broadcast when visible.",
      "uncertainties": []
    },
    {
      "rule_id": "R6",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_4_available"],
        "feature_indices": [36],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "enemy_4_available",
          "enemy_4_distance",
          "enemy_4_relative_x",
          "enemy_4_relative_y",
          "enemy_4_health",
          "enemy_4_unit_type_zergling",
          "enemy_4_unit_type_hydralisk",
          "enemy_4_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 36, 37, 38, 39, 40, 41, 42, 43]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Shared map.",
      "expected_rollout_behavior": "Enemy 4 broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R7",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_5_available"],
        "feature_indices": [44],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "enemy_5_available",
          "enemy_5_distance",
          "enemy_5_relative_x",
          "enemy_5_relative_y",
          "enemy_5_health",
          "enemy_5_unit_type_zergling",
          "enemy_5_unit_type_hydralisk",
          "enemy_5_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 44, 45, 46, 47, 48, 49, 50, 51]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Shared map.",
      "expected_rollout_behavior": "Enemy 5 broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R8",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_6_available"],
        "feature_indices": [52],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "enemy_6_available",
          "enemy_6_distance",
          "enemy_6_relative_x",
          "enemy_6_relative_y",
          "enemy_6_health",
          "enemy_6_unit_type_zergling",
          "enemy_6_unit_type_hydralisk",
          "enemy_6_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 52, 53, 54, 55, 56, 57, 58, 59]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Shared map.",
      "expected_rollout_behavior": "Enemy 6 broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R9",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_7_available"],
        "feature_indices": [60],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "enemy_7_available",
          "enemy_7_distance",
          "enemy_7_relative_x",
          "enemy_7_relative_y",
          "enemy_7_health",
          "enemy_7_unit_type_zergling",
          "enemy_7_unit_type_hydralisk",
          "enemy_7_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 60, 61, 62, 63, 64, 65, 66, 67]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Shared map.",
      "expected_rollout_behavior": "Enemy 7 broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R10",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_8_available"],
        "feature_indices": [68],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "enemy_8_available",
          "enemy_8_distance",
          "enemy_8_relative_x",
          "enemy_8_relative_y",
          "enemy_8_health",
          "enemy_8_unit_type_zergling",
          "enemy_8_unit_type_hydralisk",
          "enemy_8_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 68, 69, 70, 71, 72, 73, 74, 75]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Shared map.",
      "expected_rollout_behavior": "Enemy 8 broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R11",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_9_available"],
        "feature_indices": [76],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "enemy_9_available",
          "enemy_9_distance",
          "enemy_9_relative_x",
          "enemy_9_relative_y",
          "enemy_9_health",
          "enemy_9_unit_type_zergling",
          "enemy_9_unit_type_hydralisk",
          "enemy_9_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 76, 77, 78, 79, 80, 81, 82, 83]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Shared map.",
      "expected_rollout_behavior": "Enemy 9 broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R12",
      "requirement_ids": ["IR3"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["ally_slot_0_visible"],
        "feature_indices": [84],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "ally_slot_0_visible is 0 or 1."
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "ally_slot_0_visible",
          "ally_slot_0_distance",
          "ally_slot_0_relative_x",
          "ally_slot_0_relative_y",
          "ally_slot_0_health",
          "ally_slot_0_unit_type_zergling",
          "ally_slot_0_unit_type_hydralisk",
          "ally_slot_0_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 84, 85, 86, 87, 88, 89, 90, 91]
      },
      "sender_feasibility": "Direct observation of ally slot 0.",
      "receiver_necessity": "Allows receivers to learn health and type of allies not visible to them; global position permits matching with previous own-status broadcasts.",
      "expected_rollout_behavior": "When ally slot 0 is visible, sender forwards its status; teacher can associate with agent ID later.",
      "uncertainties": [
        "Ally slot 0 may refer to different agents across senders; identity disambiguation relies on global position and prior own-status messages."
      ]
    },
    {
      "rule_id": "R13",
      "requirement_ids": ["IR3"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["ally_slot_1_visible"],
        "feature_indices": [92],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "ally_slot_1_visible",
          "ally_slot_1_distance",
          "ally_slot_1_relative_x",
          "ally_slot_1_relative_y",
          "ally_slot_1_health",
          "ally_slot_1_unit_type_zergling",
          "ally_slot_1_unit_type_hydralisk",
          "ally_slot_1_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 92, 93, 94, 95, 96, 97, 98, 99]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Assistance and formation decisions.",
      "expected_rollout_behavior": "Allies learn about ally 1.",
      "uncertainties": []
    },
    {
      "rule_id": "R14",
      "requirement_ids": ["IR3"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["ally_slot_2_visible"],
        "feature_indices": [100],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "ally_slot_2_visible",
          "ally_slot_2_distance",
          "ally_slot_2_relative_x",
          "ally_slot_2_relative_y",
          "ally_slot_2_health",
          "ally_slot_2_unit_type_zergling",
          "ally_slot_2_unit_type_hydralisk",
          "ally_slot_2_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 100, 101, 102, 103, 104, 105, 106, 107]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Aid decisions.",
      "expected_rollout_behavior": "Ally 2 status broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R15",
      "requirement_ids": ["IR3"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["ally_slot_3_visible"],
        "feature_indices": [108],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "ally_slot_3_visible",
          "ally_slot_3_distance",
          "ally_slot_3_relative_x",
          "ally_slot_3_relative_y",
          "ally_slot_3_health",
          "ally_slot_3_unit_type_zergling",
          "ally_slot_3_unit_type_hydralisk",
          "ally_slot_3_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 108, 109, 110, 111, 112, 113, 114, 115]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Aid decisions.",
      "expected_rollout_behavior": "Ally 3 broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R16",
      "requirement_ids": ["IR3"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["ally_slot_4_visible"],
        "feature_indices": [116],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "ally_slot_4_visible",
          "ally_slot_4_distance",
          "ally_slot_4_relative_x",
          "ally_slot_4_relative_y",
          "ally_slot_4_health",
          "ally_slot_4_unit_type_zergling",
          "ally_slot_4_unit_type_hydralisk",
          "ally_slot_4_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 116, 117, 118, 119, 120, 121, 122, 123]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Aid decisions.",
      "expected_rollout_behavior": "Ally 4 broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R17",
      "requirement_ids": ["IR3"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["ally_slot_5_visible"],
        "feature_indices": [124],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "ally_slot_5_visible",
          "ally_slot_5_distance",
          "ally_slot_5_relative_x",
          "ally_slot_5_relative_y",
          "ally_slot_5_health",
          "ally_slot_5_unit_type_zergling",
          "ally_slot_5_unit_type_hydralisk",
          "ally_slot_5_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 124, 125, 126, 127, 128, 129, 130, 131]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Aid decisions.",
      "expected_rollout_behavior": "Ally 5 broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R18",
      "requirement_ids": ["IR3"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["ally_slot_6_visible"],
        "feature_indices": [132],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "ally_slot_6_visible",
          "ally_slot_6_distance",
          "ally_slot_6_relative_x",
          "ally_slot_6_relative_y",
          "ally_slot_6_health",
          "ally_slot_6_unit_type_zergling",
          "ally_slot_6_unit_type_hydralisk",
          "ally_slot_6_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 132, 133, 134, 135, 136, 137, 138, 139]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Aid decisions.",
      "expected_rollout_behavior": "Ally 6 broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R19",
      "requirement_ids": ["IR3"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["ally_slot_7_visible"],
        "feature_indices": [140],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "ally_slot_7_visible",
          "ally_slot_7_distance",
          "ally_slot_7_relative_x",
          "ally_slot_7_relative_y",
          "ally_slot_7_health",
          "ally_slot_7_unit_type_zergling",
          "ally_slot_7_unit_type_hydralisk",
          "ally_slot_7_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 140, 141, 142, 143, 144, 145, 146, 147]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Aid decisions.",
      "expected_rollout_behavior": "Ally 7 broadcast.",
      "uncertainties": []
    },
    {
      "rule_id": "R20",
      "requirement_ids": ["IR3"],
      "who": {
        "sender_group": "ALL",
        "receiver_selector": "all",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["ally_slot_8_visible"],
        "feature_indices": [148],
        "operator": ">",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "binary flag"
        }
      },
      "what": {
        "feature_names": [
          "own_normalized_x",
          "own_normalized_y",
          "ally_slot_8_visible",
          "ally_slot_8_distance",
          "ally_slot_8_relative_x",
          "ally_slot_8_relative_y",
          "ally_slot_8_health",
          "ally_slot_8_unit_type_zergling",
          "ally_slot_8_unit_type_hydralisk",
          "ally_slot_8_unit_type_baneling"
        ],
        "feature_indices": [157, 158, 148, 149, 150, 151, 152, 153, 154, 155]
      },
      "sender_feasibility": "Direct observation.",
      "receiver_necessity": "Aid decisions.",
      "expected_rollout_behavior": "Ally 8 broadcast.",
      "uncertainties": []
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "High communication volume: every agent broadcasts own status every step, and every visible enemy/ally slot triggers a separate broadcast. This ensures full shared situational awareness but may incur bandwidth costs. Trigger conditions rely on binary-semantics thresholds. Agent ID is included in own-status messages to disambiguate allies; enemy and ally slot aliasing is resolved via global coordinates computed from own position and relative offsets."
}