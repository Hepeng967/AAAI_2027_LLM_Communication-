{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Roach selects which enemy Reaper to attack.",
      "locally_missing_information": [
        "Enemy availability (whether each enemy slot is occupied/visible).",
        "Enemy relative position (rel_x, rel_y) and distance.",
        "Enemy health and type to prioritize targets."
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Roach chooses movement direction to approach the target enemy.",
      "locally_missing_information": [
        "Relative position (rel_x, rel_y) of the selected enemy to compute heading.",
        "Enemy availability to confirm the target is still valid."
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "[0]",
      "role_basis": "Agent 0 is an Overseer (type 'overseer'), a flying unit capable of moving over terrain; task description states Overseer provides vision of Reapers to Roaches. Overseer can access enemy observation features that Roaches cannot because it flies over the central pit."
    },
    {
      "group_id": "G2",
      "members": "[1, 2]",
      "role_basis": "Agents 1 and 2 are Roaches (type 'roach'), ground units whose vision and movement are blocked by the central pit. They cannot observe enemy slots directly; all enemy_available fields are expected to be 0 locally. They must rely on communication to acquire enemy information."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Which Reapers are alive, their positions, health, and type.",
      "possible_sender_groups": ["G1"],
      "possible_receiver_groups": ["G2"],
      "sender_observable_features": [
        {"name": "enemy_0_available", "index": 4},
        {"name": "enemy_0_rel_x", "index": 6},
        {"name": "enemy_0_rel_y", "index": 7},
        {"name": "enemy_0_health", "index": 8},
        {"name": "enemy_0_type_0", "index": 9},
        {"name": "enemy_0_type_1", "index": 10},
        {"name": "enemy_1_available", "index": 12},
        {"name": "enemy_1_rel_x", "index": 14},
        {"name": "enemy_1_rel_y", "index": 15},
        {"name": "enemy_1_health", "index": 16},
        {"name": "enemy_1_type_0", "index": 17},
        {"name": "enemy_1_type_1", "index": 18},
        {"name": "enemy_2_available", "index": 20},
        {"name": "enemy_2_rel_x", "index": 22},
        {"name": "enemy_2_rel_y", "index": 23},
        {"name": "enemy_2_health", "index": 24},
        {"name": "enemy_2_type_0", "index": 25},
        {"name": "enemy_2_type_1", "index": 26},
        {"name": "enemy_3_available", "index": 28},
        {"name": "enemy_3_rel_x", "index": 30},
        {"name": "enemy_3_rel_y", "index": 31},
        {"name": "enemy_3_health", "index": 32},
        {"name": "enemy_3_type_0", "index": 33},
        {"name": "enemy_3_type_1", "index": 34}
      ],
      "receiver_need_hypothesis": "Roaches must know which enemies exist and where to compute attack and movement actions. Without enemy locations and health/type, they cannot select a target or navigate around the pit to engage.",
      "task_decision_ids": ["D1", "D2"],
      "uncertainties": [
        "Whether the Overseer's vision always covers all four Reapers (they may move out of vision range or be temporarily hidden).",
        "Whether the Roaches can process full enemy state or only need a subset (e.g., closest enemy)."
      ]
    }
  ],
  "unsupported_assumptions": [
    "The Overseer can observe all four Reapers reliably because it can fly over the pit and its vision is unobstructed.",
    "The central pit completely blocks vision for ground units; Roaches cannot obtain any direct enemy observation.",
    "Communication from Overseer to Roaches is lossless and instantaneous.",
    "The Overseer does not require any information from Roaches; its own local observations are sufficient for its decisions (e.g., movement).",
    "The agent types (overseer, roach) correspond exactly to the observation capabilities assumed (flying vs ground vision).",
    "All Reapers remain on the opposite side of the pit throughout the episode, so only the Overseer has vision."
  ]
}