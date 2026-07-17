{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Roach selects a target enemy and decides movement direction (and attack) to engage.",
      "locally_missing_information": [
        "Enemy relative position (rel_x, rel_y) and distance for each active reaper.",
        "Enemy health for each active reaper.",
        "Enemy availability status per slot."
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Roach decides whether to focus attacks with the other roach or split targets to optimize damage.",
      "locally_missing_information": [
        "The other roach's currently targeted enemy index or intended target.",
        "The other roach's distance to its target (requires enemy position to compute locally if enemy info is available)."
      ]
    },
    {
      "decision_id": "D3",
      "decision": "Overseer decides which subset of enemy information to transmit to roaches and at which frequency.",
      "locally_missing_information": [
        "Roaches' current knowledge or belief about enemy states (e.g., what they already know).",
        "Roaches' intended actions or movement targets."
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [0],
      "role_basis": "Overseer (agent 0) is a flying unit; on map 1o_2r_vs_4r it can see across the central pit and observe all four reapers. Its observation vector likely contains valid enemy features."
    },
    {
      "group_id": "G2",
      "members": [1, 2],
      "role_basis": "Roaches (agents 1,2) are ground units; the pit blocks both movement and vision, so they cannot directly observe enemies across the pit. Their enemy feature slots are expected to be zeroed out (available=0). They can observe each other and the overseer because they spawn on the same side."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Real-time position and health of each reaper (enemy units) that roaches need to navigate to and attack.",
      "possible_sender_groups": ["G1"],
      "possible_receiver_groups": ["G2"],
      "sender_observable_features": [
        {"name": "enemy_0_available", "index": 4},
        {"name": "enemy_0_distance", "index": 5},
        {"name": "enemy_0_rel_x", "index": 6},
        {"name": "enemy_0_rel_y", "index": 7},
        {"name": "enemy_0_health", "index": 8},
        {"name": "enemy_1_available", "index": 11},
        {"name": "enemy_1_distance", "index": 12},
        {"name": "enemy_1_rel_x", "index": 13},
        {"name": "enemy_1_rel_y", "index": 14},
        {"name": "enemy_1_health", "index": 15},
        {"name": "enemy_2_available", "index": 18},
        {"name": "enemy_2_distance", "index": 19},
        {"name": "enemy_2_rel_x", "index": 20},
        {"name": "enemy_2_rel_y", "index": 21},
        {"name": "enemy_2_health", "index": 22},
        {"name": "enemy_3_available", "index": 25},
        {"name": "enemy_3_distance", "index": 26},
        {"name": "enemy_3_rel_x", "index": 27},
        {"name": "enemy_3_rel_y", "index": 28},
        {"name": "enemy_3_health", "index": 29}
      ],
      "receiver_need_hypothesis": "Roaches must decide movement and attack actions (D1). Without enemy positions and health, they cannot locate or prioritise targets. The overseer is the only agent with sight across the pit, so roaches need this information via communication.",
      "task_decision_ids": ["D1"],
      "uncertainties": [
        "Assumes enemy slot ordering is consistent across agents (based on unit IDs) so that roaches can reference communicated enemies by index.",
        "Assumes overseer vision covers all four reapers at all times (no occlusion or range limitation)."
      ]
    }
  ],
  "unsupported_assumptions": [
    "Coordination of target selection among roaches (D2) may require sharing intended target indices or intended actions. However, no observation feature captures an agent's own intended action, last action, or current target. Such information is not directly observable by any agent and cannot be derived from the given observation vector. Communication of these intentions would require additional internal-state features (e.g., one-hot of own action or target) that are not present.",
    "The overseer's decision about what to communicate (D3) depends on roaches' knowledge state, which cannot be observed. This is a classic epistemic gap; the observation vector provides no feature indicating another agent's observation content or beliefs."
  ]
}