
Task and aligned observation description:
The map is 1o_10b_vs_1r. The map contains multiple high grounds and obstacles, with 10 Banelings randomly distributed around the map. The Overseer and the Roach spawn at different locations. Only the Overseer can detect the Roach's position, and Banelings must rely on communication to locate and attack the Roach. Complex terrain increases the difficulty of coordination and path planning, making efficient communication essential for success.Observation information for map '1o_10b_vs_1r':
- Each agent observes a vector of length 84.
- There are 11 agents. Their types are: baneling, baneling, baneling, baneling, baneling, baneling, baneling, baneling, baneling, baneling, overseer.
- Each row of the observation corresponds to agent_id: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], and their types: ['baneling', 'baneling', 'baneling', 'baneling', 'baneling', 'baneling', 'baneling', 'baneling', 'baneling', 'baneling', 'overseer'].
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
    - 11: ally_0_visible
    - 12: ally_0_distance
    - 13: ally_0_rel_x
    - 14: ally_0_rel_y
    - 15: ally_0_health
    - 16: ally_0_type_0
    - 17: ally_0_type_1
    - 18: ally_1_visible
    - 19: ally_1_distance
    - 20: ally_1_rel_x
    - 21: ally_1_rel_y
    - 22: ally_1_health
    - 23: ally_1_type_0
    - 24: ally_1_type_1
    - 25: ally_2_visible
    - 26: ally_2_distance
    - 27: ally_2_rel_x
    - 28: ally_2_rel_y
    - 29: ally_2_health
    - 30: ally_2_type_0
    - 31: ally_2_type_1
    - 32: ally_3_visible
    - 33: ally_3_distance
    - 34: ally_3_rel_x
    - 35: ally_3_rel_y
    - 36: ally_3_health
    - 37: ally_3_type_0
    - 38: ally_3_type_1
    - 39: ally_4_visible
    - 40: ally_4_distance
    - 41: ally_4_rel_x
    - 42: ally_4_rel_y
    - 43: ally_4_health
    - 44: ally_4_type_0
    - 45: ally_4_type_1
    - 46: ally_5_visible
    - 47: ally_5_distance
    - 48: ally_5_rel_x
    - 49: ally_5_rel_y
    - 50: ally_5_health
    - 51: ally_5_type_0
    - 52: ally_5_type_1
    - 53: ally_6_visible
    - 54: ally_6_distance
    - 55: ally_6_rel_x
    - 56: ally_6_rel_y
    - 57: ally_6_health
    - 58: ally_6_type_0
    - 59: ally_6_type_1
    - 60: ally_7_visible
    - 61: ally_7_distance
    - 62: ally_7_rel_x
    - 63: ally_7_rel_y
    - 64: ally_7_health
    - 65: ally_7_type_0
    - 66: ally_7_type_1
    - 67: ally_8_visible
    - 68: ally_8_distance
    - 69: ally_8_rel_x
    - 70: ally_8_rel_y
    - 71: ally_8_health
    - 72: ally_8_type_0
    - 73: ally_8_type_1
    - 74: ally_9_visible
    - 75: ally_9_distance
    - 76: ally_9_rel_x
    - 77: ally_9_rel_y
    - 78: ally_9_health
    - 79: ally_9_type_0
    - 80: ally_9_type_1
    - 81: own_health
    - 82: own_type_0
    - 83: own_type_1

LMAC rollout observation alignment:
- Runtime LMAC observation vector length: 84.
- Documented SMAC observation vector length: 84.
- Rollout available: False from /data/hp/LLM_Communication/LMAC-new/data.
- Use runtime obs_shape for generated code and tests.
- Dimensions named lmac_extra_* are wrapper/config-added features; do not treat them as hidden global state.


Information-requirement analysis:
{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Choose movement direction to approach and attack the Roach.",
      "locally_missing_information": [
        "Roach presence (enemy_0_available), distance, relative coordinates, health, and type."
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Coordinate movement with other Banelings to avoid collisions and optimize paths through complex terrain.",
      "locally_missing_information": [
        "Positions of Banelings (and Overseer) that are not currently visible due to limited sight range or terrain occlusion."
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "Agent 10 (Overseer)",
      "role_basis": "Only agent type that can observe the Roach (enemy_0_available=1) according to task description and observation feature 4."
    },
    {
      "group_id": "G2",
      "members": "Agents 0-9 (Banelings)",
      "role_basis": "Cannot observe Roach (enemy_0_available=0 in observation feature 4); must rely on communication to locate Roach."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Presence, distance, relative X and Y coordinates, health, and type of the Roach (enemy_0).",
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
          "name": "enemy_0_type_0",
          "index": 9
        },
        {
          "name": "enemy_0_type_1",
          "index": 10
        }
      ],
      "receiver_need_hypothesis": "Banelings require the Roach's location to navigate towards it. Without this information, movement decisions (D1) cannot be goal-directed, leading to random exploration.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "The coordinates (rel_x, rel_y) are relative to the Overseer. A receiving Baneling may not know the Overseer's own position if the Overseer is not currently visible (ally_*_visible may be 0 for the Overseer's ally slot). This prevents direct conversion of coordinates to the Baneling's local frame, potentially rendering the message unusable without additional frame-of-reference information (e.g., Overseer's position relative to the Baneling or a common landmark). This uncertainty is not resolvable from the given observation schema alone."
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "Positions (relative coordinates or distance and direction) of other Banelings and, optionally, the Overseer that are not visible to a Baneling.",
      "possible_sender_groups": [
        "G2",
        "G1"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "ally_*_visible (for each ally slot)",
          "index": "11,18,25,32,39,46,53,60,67,74"
        },
        {
          "name": "ally_*_distance",
          "index": "12,19,26,33,40,47,54,61,68,75"
        },
        {
          "name": "ally_*_rel_x",
          "index": "13,20,27,34,41,48,55,62,69,76"
        },
        {
          "name": "ally_*_rel_y",
          "index": "14,21,28,35,42,49,56,63,70,77"
        },
        {
          "name": "ally_*_health",
          "index": "15,22,29,36,43,50,57,64,71,78"
        },
        {
          "name": "ally_*_type_0",
          "index": "16,23,30,37,44,51,58,65,72,79"
        },
        {
          "name": "ally_*_type_1",
          "index": "17,24,31,38,45,52,59,66,73,80"
        }
      ],
      "receiver_need_hypothesis": "For coordinated movement and path planning (D2), agents need awareness of nearby allies, especially those outside their sight range, to avoid collisions, form effective formations, and navigate obstacles without redundancy or blocking.",
      "task_decision_ids": [
        "D2"
      ],
      "uncertainties": [
        "The observation provides up to 10 ally slots covering all allies. The 'visible' flag indicates whether the ally is within sensor range. Positioning of non-visible allies is unknown; this may cause repeated path conflicts around corners of obstacles. This need is inferred from the task statement: 'Complex terrain increases the difficulty of coordination and path planning, making efficient communication essential for success.'"
      ]
    }
  ],
  "unsupported_assumptions": [
    "It is assumed that communicated relative coordinates from the Overseer can be transformed by a Baneling into its own coordinate frame using locally observed ally positions. If the Overseer is not visible, this transformation fails; no global coordinate system or map landmarks are present in observations to serve as a common reference.",
    "We assume the communication channel allows all agents to receive any sent message irrespective of distance or terrain, as no communication constraints are specified.",
    "The identification of ally types (e.g., distinguishing Overseer from Banelings) relies on the observation features ally_type_0 and ally_type_1; we assume these encode type information unambiguously."
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
