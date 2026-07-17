{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Roach selects a movement target among enemies",
      "locally_missing_information": [
        "Enemy availability (which enemies exist)",
        "Enemy positions relative to roach"
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Roach selects which enemy to attack to coordinate with ally",
      "locally_missing_information": [
        "Designated target assignment (which enemy each roach should focus)"
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "agent_id 0 (overseer)",
      "role_basis": "Task says Overseer can locate Reapers; observation schema includes enemy features (likely sees across pit)."
    },
    {
      "group_id": "G2",
      "members": "agent_id 1 and 2 (roaches)",
      "role_basis": "Task says Roaches must rely on Overseer communication; pit blocks vision so roaches' enemy_available=0."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Positions and availability of each reaper enemy",
      "possible_sender_groups": ["G1"],
      "possible_receiver_groups": ["G2"],
      "sender_observable_features": [
        {"name": "enemy_0_available", "index": 4},
        {"name": "enemy_0_rel_x", "index": 6},
        {"name": "enemy_0_rel_y", "index": 7},
        {"name": "enemy_1_available", "index": 11},
        {"name": "enemy_1_rel_x", "index": 13},
        {"name": "enemy_1_rel_y", "index": 14},
        {"name": "enemy_2_available", "index": 18},
        {"name": "enemy_2_rel_x", "index": 20},
        {"name": "enemy_2_rel_y", "index": 21},
        {"name": "enemy_3_available", "index": 25},
        {"name": "enemy_3_rel_x", "index": 27},
        {"name": "enemy_3_rel_y", "index": 28}
      ],
      "receiver_need_hypothesis": "Roaches need enemy locations relative to themselves to navigate around the pit and engage. Without this, they cannot locate enemies.",
      "task_decision_ids": ["D1", "D2"],
      "uncertainties": [
        "Assumes overseer can always observe all enemies; vision may degrade with distance or if overseer moves."
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "Which enemy each roach should attack to focus fire",
      "possible_sender_groups": ["G1"],
      "possible_receiver_groups": ["G2"],
      "sender_observable_features": [
        {"name": "ally_0_rel_x", "index": 34},
        {"name": "ally_0_rel_y", "index": 35},
        {"name": "ally_1_rel_x", "index": 41},
        {"name": "ally_1_rel_y", "index": 42},
        {"name": "enemy_0_rel_x", "index": 6},
        {"name": "enemy_0_rel_y", "index": 7},
        {"name": "enemy_1_rel_x", "index": 13},
        {"name": "enemy_1_rel_y", "index": 14},
        {"name": "enemy_2_rel_x", "index": 20},
        {"name": "enemy_2_rel_y", "index": 21},
        {"name": "enemy_3_rel_x", "index": 27},
        {"name": "enemy_3_rel_y", "index": 28}
      ],
      "receiver_need_hypothesis": "Coordinated focus fire improves elimination speed; roaches need common assignment to avoid splitting damage or overkill.",
      "task_decision_ids": ["D2"],
      "uncertainties": [
        "Roaches may prefer nearest target, conflicting with assignment; assignment may become stale if enemy dies."
      ]
    }
  ],
  "unsupported_assumptions": []
}