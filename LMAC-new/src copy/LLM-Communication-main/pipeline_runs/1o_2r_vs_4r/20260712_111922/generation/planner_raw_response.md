{
  "policy_hypothesis": "The overseer uses its unobstructed aerial vision to detect all four reapers across the pit and communicates their relative positions and health to the roaches, enabling them to navigate around the pit and engage enemies.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": ["overseer"],
      "role_basis": "Flying unit with cross-pit vision."
    },
    {
      "group_id": "G2",
      "members": ["roach", "roach"],
      "role_basis": "Ground units blocked by pit, rely on communication."
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
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_0_available is 1 if enemy reaper 0 exists and is visible."
        }
      },
      "what": {
        "feature_names": ["enemy_0_rel_x", "enemy_0_rel_y", "enemy_0_health"],
        "feature_indices": [6, 7, 8]
      },
      "sender_feasibility": "Overseer can observe enemy reapers across the pit.",
      "receiver_necessity": "Roaches need enemy locations to navigate and attack.",
      "expected_rollout_behavior": "Roaches receive coordinates of enemy 0 and can move to engage, possibly prioritizing wounded enemies.",
      "uncertainties": [
        "Some reapers may be out of sight range",
        "Positions may become outdated due to enemy movement",
        "Roaches must integrate coordinates with local pathfinding"
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": ["IR1"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_1_available"],
        "feature_indices": [11],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_1_available is 1 if enemy reaper 1 exists and is visible."
        }
      },
      "what": {
        "feature_names": ["enemy_1_rel_x", "enemy_1_rel_y", "enemy_1_health"],
        "feature_indices": [13, 14, 15]
      },
      "sender_feasibility": "Overseer can observe enemy reapers across the pit.",
      "receiver_necessity": "Roaches need enemy locations to navigate and attack.",
      "expected_rollout_behavior": "Roaches receive coordinates of enemy 1 and can move to engage.",
      "uncertainties": [
        "Some reapers may be out of sight range",
        "Positions may become outdated",
        "Roaches must integrate coordinates with local pathfinding"
      ]
    },
    {
      "rule_id": "R3",
      "requirement_ids": ["IR1"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_2_available"],
        "feature_indices": [18],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_2_available is 1 if enemy reaper 2 exists and is visible."
        }
      },
      "what": {
        "feature_names": ["enemy_2_rel_x", "enemy_2_rel_y", "enemy_2_health"],
        "feature_indices": [20, 21, 22]
      },
      "sender_feasibility": "Overseer can observe enemy reapers across the pit.",
      "receiver_necessity": "Roaches need enemy locations to navigate and attack.",
      "expected_rollout_behavior": "Roaches receive coordinates of enemy 2 and can move to engage.",
      "uncertainties": [
        "Some reapers may be out of sight range",
        "Positions may become outdated",
        "Roaches must integrate coordinates with local pathfinding"
      ]
    },
    {
      "rule_id": "R4",
      "requirement_ids": ["IR1"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_3_available"],
        "feature_indices": [25],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_3_available is 1 if enemy reaper 3 exists and is visible."
        }
      },
      "what": {
        "feature_names": ["enemy_3_rel_x", "enemy_3_rel_y", "enemy_3_health"],
        "feature_indices": [27, 28, 29]
      },
      "sender_feasibility": "Overseer can observe enemy reapers across the pit.",
      "receiver_necessity": "Roaches need enemy locations to navigate and attack.",
      "expected_rollout_behavior": "Roaches receive coordinates of enemy 3 and can move to engage.",
      "uncertainties": [
        "Some reapers may be out of sight range",
        "Positions may become outdated",
        "Roaches must integrate coordinates with local pathfinding"
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Per-enemy rule granularity ensures only visible enemies are reported; health inclusion supports prioritization; bandwidth impact is low (3 floats per visible enemy)."
}