
Task and aligned observation description:
The map is 1o_2r_vs_4r. There is a large pit in the center of the map, dividing the battlefield into two sides. At the beginning of each episode, the Overseer and 2 Roaches spawn on one side, while 4 Reapers spawn on the other. The pit blocks direct movement and vision, so Roaches must rely on communication from the Overseer to locate and attack the Reapers. This scenario tests communication and coordination under significant terrain constraints.Observation information for map '1o_2r_vs_4r':
- Each agent observes a vector of length 66.
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
    - 12: enemy_1_available
    - 13: enemy_1_distance
    - 14: enemy_1_rel_x
    - 15: enemy_1_rel_y
    - 16: enemy_1_health
    - 17: enemy_1_type_0
    - 18: enemy_1_type_1
    - 20: enemy_2_available
    - 21: enemy_2_distance
    - 22: enemy_2_rel_x
    - 23: enemy_2_rel_y
    - 24: enemy_2_health
    - 25: enemy_2_type_0
    - 26: enemy_2_type_1
    - 28: enemy_3_available
    - 29: enemy_3_distance
    - 30: enemy_3_rel_x
    - 31: enemy_3_rel_y
    - 32: enemy_3_health
    - 33: enemy_3_type_0
    - 34: enemy_3_type_1
    - 36: ally_0_visible
    - 37: ally_0_distance
    - 38: ally_0_rel_x
    - 39: ally_0_rel_y
    - 40: ally_0_health
    - 41: ally_0_type_0
    - 42: ally_0_type_1
    - 43: ally_1_visible
    - 44: ally_1_distance
    - 45: ally_1_rel_x
    - 46: ally_1_rel_y
    - 47: ally_1_health
    - 48: ally_1_type_0
    - 49: ally_1_type_1
    - 50: own_health
    - 51: own_type_0
    - 52: own_type_1
    - ?: lmac_extra_49
    - ?: lmac_extra_50
    - ?: lmac_extra_51
    - ?: lmac_extra_52
    - ?: lmac_extra_53
    - ?: lmac_extra_54
    - ?: lmac_extra_55
    - ?: lmac_extra_56
    - ?: lmac_extra_57
    - ?: lmac_extra_58
    - ?: lmac_extra_59
    - ?: lmac_extra_60
    - ?: lmac_extra_61
    - ?: lmac_extra_62
    - ?: lmac_extra_63
    - ?: lmac_extra_64
    - ?: lmac_extra_65

LMAC rollout observation alignment:
- Runtime LMAC observation vector length: 66.
- Documented SMAC observation vector length: 49.
- Rollout available: True from /data/hp/LLM_Communication/LMAC-new/data.
- Use runtime obs_shape for generated code and tests.
- Dimensions named lmac_extra_* are wrapper/config-added features; do not treat them as hidden global state.
- Additional runtime dimensions:
    - 49~49: ally_1_type_1
    - 50~50: own_health
    - 51~51: own_type_0
    - 52~52: own_type_1
    - 53~53: previous_action_0
    - 54~54: previous_action_1
    - 55~55: previous_action_2
    - 56~56: previous_action_3
    - 57~57: previous_action_4
    - 58~58: previous_action_5
    - 59~59: previous_action_6
    - 60~60: previous_action_7
    - 61~61: previous_action_8
    - 62~62: previous_action_9
    - 63~63: agent_id_0
    - 64~64: agent_id_1
    - 65~65: agent_id_2


Information-requirement analysis:
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
          "name": "enemy_0_type_0",
          "index": 9
        },
        {
          "name": "enemy_0_type_1",
          "index": 10
        },
        {
          "name": "enemy_1_available",
          "index": 12
        },
        {
          "name": "enemy_1_rel_x",
          "index": 14
        },
        {
          "name": "enemy_1_rel_y",
          "index": 15
        },
        {
          "name": "enemy_1_health",
          "index": 16
        },
        {
          "name": "enemy_1_type_0",
          "index": 17
        },
        {
          "name": "enemy_1_type_1",
          "index": 18
        },
        {
          "name": "enemy_2_available",
          "index": 20
        },
        {
          "name": "enemy_2_rel_x",
          "index": 22
        },
        {
          "name": "enemy_2_rel_y",
          "index": 23
        },
        {
          "name": "enemy_2_health",
          "index": 24
        },
        {
          "name": "enemy_2_type_0",
          "index": 25
        },
        {
          "name": "enemy_2_type_1",
          "index": 26
        },
        {
          "name": "enemy_3_available",
          "index": 28
        },
        {
          "name": "enemy_3_rel_x",
          "index": 30
        },
        {
          "name": "enemy_3_rel_y",
          "index": 31
        },
        {
          "name": "enemy_3_health",
          "index": 32
        },
        {
          "name": "enemy_3_type_0",
          "index": 33
        },
        {
          "name": "enemy_3_type_1",
          "index": 34
        }
      ],
      "receiver_need_hypothesis": "Roaches must know which enemies exist and where to compute attack and movement actions. Without enemy locations and health/type, they cannot select a target or navigate around the pit to engage.",
      "task_decision_ids": [
        "D1",
        "D2"
      ],
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
