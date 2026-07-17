{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Roach movement: choose direction to approach a Reaper.",
      "locally_missing_information": [
        "Positions of Reapers relative to self (requires transformation from Overseer's relative coordinates)."
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Roach attack: select a Reaper to attack when in range.",
      "locally_missing_information": [
        "Health of Reapers to determine threat and target priority.",
        "Distance to Reapers to know if attack is possible.",
        "Confirmation that the entity is a Reaper (type)."
      ]
    },
    {
      "decision_id": "D3",
      "decision": "Roach coordination: decide which Reaper to focus on to avoid duplicate effort and maximize damage distribution.",
      "locally_missing_information": [
        "Which Reaper the other Roach is currently targeting or moving towards."
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [0],
      "role_basis": "Overseer (flying) can see over the pit; observation of enemy features is available (enemy_*_available=1). Task evidence: 'Roaches must rely on communication from the Overseer to locate and attack the Reapers.'"
    },
    {
      "group_id": "G2",
      "members": [1, 2],
      "role_basis": "Roaches (ground) cannot see across the pit; enemy_*_available is expected to be 0. Task evidence: 'The pit blocks direct movement and vision, so Roaches must rely on communication from the Overseer.'"
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "State of each Reaper: alive/available, relative position (rel_x, rel_y), health, and type.",
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
      "receiver_need_hypothesis": "Roaches cannot see Reapers because of the pit; they need enemy positions to move towards them and health/type to prioritize attacks.",
      "task_decision_ids": ["D1", "D2"],
      "uncertainties": [
        "Overseer may lose vision of some Reapers if they move out of its sight, causing incomplete information.",
        "Relative coordinates from Overseer require transformation using Overseer's own position (observable via ally_0 features) – if a Roach loses sight of the Overseer, transformation fails.",
        "Communication delay may cause outdated position information (Reapers move)."
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "Currently targeted Reaper of each Roach (e.g., enemy index or identifier).",
      "possible_sender_groups": ["G2"],
      "possible_receiver_groups": ["G2"],
      "sender_observable_features": [],
      "receiver_need_hypothesis": "Roaches need to divide Reapers among themselves efficiently; without knowing the other's target, they risk attacking the same Reaper or ignoring threats.",
      "task_decision_ids": ["D3"],
      "uncertainties": [
        "Target may change rapidly; need frequent updates to avoid coordination lag.",
        "No direct observation of other agent's intention; must be explicitly communicated."
      ]
    }
  ],
  "unsupported_assumptions": []
}