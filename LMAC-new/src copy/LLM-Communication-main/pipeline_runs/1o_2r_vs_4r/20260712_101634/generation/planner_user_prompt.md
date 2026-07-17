
Task and aligned observation description:
The map is 1o_2r_vs_4r. There is a large pit in the center of the map, dividing the battlefield into two sides. At the beginning of each episode, the Overseer and 2 Roaches spawn on one side, while 4 Reapers spawn on the other. The pit blocks direct movement and vision, so Roaches must rely on communication from the Overseer to locate and attack the Reapers. This scenario tests communication and coordination under significant terrain constraints.Observation information for map '1o_2r_vs_4r':
- Each agent observes a vector of length 49.
- There are 3 agents. Their types are: overseer, roach, roach.
- Each row of the observation corresponds to agent_id: [0, 1, 2], and their types: ['overseer', 'roach', 'roach'].
- The observation vector is composed as follows (index: feature):
    - 0: move_north
    - 1: move_south
    - 2: move_east
    - 3: move_west
    - 4: enemy_0_available
    - 5: enemy_0_distance
    - 6: enemy_0_rel_x
    - 7: enemy_0_rel_y
    - 8: enemy_0_health
    - 9: enemy_0_type_0
    - 10: enemy_0_type_1
    - 11: enemy_1_available
    - 12: enemy_1_distance
    - 13: enemy_1_rel_x
    - 14: enemy_1_rel_y
    - 15: enemy_1_health
    - 16: enemy_1_type_0
    - 17: enemy_1_type_1
    - 18: enemy_2_available
    - 19: enemy_2_distance
    - 20: enemy_2_rel_x
    - 21: enemy_2_rel_y
    - 22: enemy_2_health
    - 23: enemy_2_type_0
    - 24: enemy_2_type_1
    - 25: enemy_3_available
    - 26: enemy_3_distance
    - 27: enemy_3_rel_x
    - 28: enemy_3_rel_y
    - 29: enemy_3_health
    - 30: enemy_3_type_0
    - 31: enemy_3_type_1
    - 32: ally_0_visible
    - 33: ally_0_distance
    - 34: ally_0_rel_x
    - 35: ally_0_rel_y
    - 36: ally_0_health
    - 37: ally_0_type_0
    - 38: ally_0_type_1
    - 39: ally_1_visible
    - 40: ally_1_distance
    - 41: ally_1_rel_x
    - 42: ally_1_rel_y
    - 43: ally_1_health
    - 44: ally_1_type_0
    - 45: ally_1_type_1
    - 46: own_health
    - 47: own_type_0
    - 48: own_type_1

LMAC rollout observation alignment:
- Runtime LMAC observation vector length: 49.
- Documented SMAC observation vector length: 49.
- Rollout available: False from /data/hp/LLM_Communication/LMAC-new/data.
- Use runtime obs_shape for generated code and tests.
- Dimensions named lmac_extra_* are wrapper/config-added features; do not treat them as hidden global state.


Information-requirement analysis:
{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Move to a position that enables attacking enemies across the pit while remaining safe.",
      "locally_missing_information": [
        "Positions of enemy Reapers relative to self (to know direction and distance to approach)."
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Select which enemy Reaper to attack and execute the attack command.",
      "locally_missing_information": [
        "Which enemies are alive and available to target.",
        "Relative positions and health of enemy Reapers to choose optimal target."
      ]
    },
    {
      "decision_id": "D3",
      "decision": "Move the Overseer to maintain vision of enemies or avoid danger.",
      "locally_missing_information": []
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "0",
      "role_basis": "Agent type 'overseer' (own_type) has global vision across the pit as suggested by scenario; observation includes full enemy availability and positions; likely lacks attack capability."
    },
    {
      "group_id": "G2",
      "members": "1,2",
      "role_basis": "Agent type 'roach' has ground unit limitation; pit blocks direct enemy vision, so their local enemy availability flags are likely 0; need external enemy info to engage."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Positions, health, and availability of all 4 enemy Reapers relative to the Overseer.",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "enemy_0_available",
          "index": 4
        },
        {
          "name": "enemy_0_distance",
          "index": 5
        },
        {
          "name": "enemy_0_rel_x",
          "index": 6
        },
        {
          "name": "enemy_0_rel_y",
          "index": 7
        },
        {
          "name": "enemy_0_health",
          "index": 8
        },
        {
          "name": "enemy_1_available",
          "index": 11
        },
        {
          "name": "enemy_1_distance",
          "index": 12
        },
        {
          "name": "enemy_1_rel_x",
          "index": 13
        },
        {
          "name": "enemy_1_rel_y",
          "index": 14
        },
        {
          "name": "enemy_1_health",
          "index": 15
        },
        {
          "name": "enemy_2_available",
          "index": 18
        },
        {
          "name": "enemy_2_distance",
          "index": 19
        },
        {
          "name": "enemy_2_rel_x",
          "index": 20
        },
        {
          "name": "enemy_2_rel_y",
          "index": 21
        },
        {
          "name": "enemy_2_health",
          "index": 22
        },
        {
          "name": "enemy_3_available",
          "index": 25
        },
        {
          "name": "enemy_3_distance",
          "index": 26
        },
        {
          "name": "enemy_3_rel_x",
          "index": 27
        },
        {
          "name": "enemy_3_rel_y",
          "index": 28
        },
        {
          "name": "enemy_3_health",
          "index": 29
        }
      ],
      "receiver_need_hypothesis": "Roaches (G2) cannot directly observe the Reapers across the pit. To decide where to move (D1) and which enemy to attack (D2), they need enemy presence and spatial data. The Overseer can provide these observations from its side. Roaches can transform the coordinates to their own frame using the Overseer's known relative position (from ally observation).",
      "task_decision_ids": [
        "D1",
        "D2"
      ],
      "uncertainties": [
        "Whether Overseer always sees all four Reapers or some may be outside its vision range (assumed full vision per scenario description).",
        "Whether Reapers move frequently, making communicated positions stale before Roaches can act (timing uncertainty).",
        "Exact transformation arithmetic required by Roaches to convert Overseer-relative coordinates to self-relative may introduce error if not precise."
      ]
    }
  ],
  "unsupported_assumptions": [
    "Roaches can always observe the Overseer (ally_visible for one of the ally slots corresponds to the Overseer).",
    "Overseer has no attack capability and its movement decisions do not rely on communication from Roaches.",
    "The pit completely blocks vision and movement for ground units, but not for Overseer.",
    "Enemy Reapers do not have stealth or ability to hide."
  ]
}

Return this policy schema:
{
  "policy_hypothesis":"...",
  "agent_groups":[...],
  "rules":[
    {"rule_id":"R1","requirement_ids":["IR1"],
      "who":{"sender_group":"G1","receiver_selector":"...","observable_basis":[]},
      "when":{"feature_names":["..."],"feature_indices":[0],"operator":"...",
        "threshold":0.0,"threshold_basis":{"type":"binary_semantics|documented_semantics|rollout_distribution|relative_comparison|llm_hypothesis","evidence":"..."}},
      "what":{"feature_names":["..."],"feature_indices":[0]},
      "sender_feasibility":"...","receiver_necessity":"...",
      "expected_rollout_behavior":"...","uncertainties":[]}
  ],
  "default_behavior":"no communication",
  "design_tradeoffs":"..."
}
Feature indices must match the supplied aligned schema. Do not invent runtime
fields. A threshold without a documented or observed basis must be explicitly
labelled llm_hypothesis. Prefer no communication only as a default, not as a
hard-coded claim that sparse communication is always superior.
