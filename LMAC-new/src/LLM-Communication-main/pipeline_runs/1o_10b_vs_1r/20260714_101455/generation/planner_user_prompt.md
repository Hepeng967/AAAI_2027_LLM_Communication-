
Task and aligned observation description:
The map is 1o_10b_vs_1r. The map contains multiple high grounds and obstacles, with 10 Banelings randomly distributed around the map. The Overseer and the Roach spawn at different locations. Only the Overseer can detect the Roach's position, and Banelings must rely on communication to locate and attack the Roach. Complex terrain increases the difficulty of coordination and path planning, making efficient communication essential for success.Observation information for map '1o_10b_vs_1r':
- Each agent observes a vector of length 103.
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
    - ?: lmac_extra_84
    - ?: lmac_extra_85
    - ?: lmac_extra_86
    - ?: lmac_extra_87
    - ?: lmac_extra_88
    - ?: lmac_extra_89
    - ?: lmac_extra_90
    - ?: lmac_extra_91
    - ?: lmac_extra_92
    - ?: lmac_extra_93
    - ?: lmac_extra_94
    - ?: lmac_extra_95
    - ?: lmac_extra_96
    - ?: lmac_extra_97
    - ?: lmac_extra_98
    - ?: lmac_extra_99
    - ?: lmac_extra_100
    - ?: lmac_extra_101
    - ?: lmac_extra_102

LMAC rollout observation alignment:
- Runtime LMAC observation vector length: 103.
- Documented SMAC observation vector length: 84.
- Rollout available: True from /data/hp/LLM_Communication/LMAC-new/data.
- Use runtime obs_shape for generated code and tests.
- Dimensions named lmac_extra_* are wrapper/config-added features; do not treat them as hidden global state.
- Additional runtime dimensions:
    - 84~84: env_extra_84
    - 85~85: previous_action_0
    - 86~86: previous_action_1
    - 87~87: previous_action_2
    - 88~88: previous_action_3
    - 89~89: previous_action_4
    - 90~90: previous_action_5
    - 91~91: previous_action_6
    - 92~92: agent_id_0
    - 93~93: agent_id_1
    - 94~94: agent_id_2
    - 95~95: agent_id_3
    - 96~96: agent_id_4
    - 97~97: agent_id_5
    - 98~98: agent_id_6
    - 99~99: agent_id_7
    - 100~100: agent_id_8
    - 101~101: agent_id_9
    - 102~102: agent_id_10


Information-requirement analysis:
{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Baneling decides movement direction to approach the Roach for attack.",
      "locally_missing_information": [
        "Roach's relative position (distance, rel_x, rel_y) from the Baneling's perspective."
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Baneling decides movement direction when Roach position is unknown, e.g., to search or approach the Overseer.",
      "locally_missing_information": [
        "Whether Roach position is known and from which reference agent; also Overseer's relative position if not visible."
      ]
    },
    {
      "decision_id": "D3",
      "decision": "Overseer decides movement to maintain visibility of the Roach while staying within communication/visibility range of Banelings to relay Roach position.",
      "locally_missing_information": [
        "Positions of Banelings that are not currently visible, especially clusters that could benefit from the info."
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        10
      ],
      "role_basis": "observation/task evidence: Only agent type 'overseer', which can detect the Roach (enemy_0_available=1) as per task description and observation schema; Banelings have enemy_0_available=0."
    },
    {
      "group_id": "G2",
      "members": [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9
      ],
      "role_basis": "observation/task evidence: Agents of type 'baneling'; they cannot directly observe the Roach (enemy_0_available=0) and must rely on communication to attack."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Roach's position relative to the Overseer (i.e., the vector from Overseer to Roach).",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "enemy_0_rel_x",
          "index": 6
        },
        {
          "name": "enemy_0_rel_y",
          "index": 7
        },
        {
          "name": "enemy_0_distance",
          "index": 5
        }
      ],
      "receiver_need_hypothesis": "A Baneling that can see the Overseer can compute the Roach's relative position to itself by adding the observed Overseer relative position to the received vector. This enables direct movement toward the Roach. Without this, Banelings cannot navigate to the Roach.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Only useful when the Baneling can observe the Overseer (Overseer is within ally visibility range and identifiable via ally_i_type).",
        "The Roach may move, making the communicated vector outdated quickly; requires frequent or continuous updates.",
        "Assumes the Baneling has internal memory or receives the message simultaneously with observation to combine with observed Overseer relative position."
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "Estimated Roach position relative to a Baneling that has previously received or computed it.",
      "possible_sender_groups": [
        "G2"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [],
      "receiver_need_hypothesis": "If a Baneling cannot see the Overseer but can see another Baneling that knows the Roach's position relative to that sender, the receiver can compute Roach position relative to itself by vector addition: sender's relative position plus the received Roach-to-sender vector. This enables propagation of Roach location beyond Overseer's visibility range.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "The sender Baneling's estimate of Roach position is not directly observable in its own observation vector; it must be maintained in memory from prior communications.",
        "Accuracy may degrade through multi-hop relay due to motion and communication delays.",
        "Assumes sender Baneling can identify itself to receiver (via ally visibility) and that the communicated vector is in sender's egocentric frame."
      ]
    },
    {
      "requirement_id": "IR3",
      "fact": "Positions of Banelings that are not visible to the Overseer, relative to a Baneling that is visible to the Overseer.",
      "possible_sender_groups": [
        "G2"
      ],
      "possible_receiver_groups": [
        "G1"
      ],
      "sender_observable_features": [
        {
          "name": "ally_i_rel_x (of relayed Baneling)",
          "index": "variable (e.g., 13, 20, 27, ...)"
        },
        {
          "name": "ally_i_rel_y (of relayed Baneling)",
          "index": "variable"
        }
      ],
      "receiver_need_hypothesis": "The Overseer can use aggregated friendly positions to decide where to move to maximize the number of Banelings that can receive IR1-type information. If the Overseer knows the relative positions of distant Banelings (via relay), it can plan a path to bring them into visibility.",
      "task_decision_ids": [
        "D3"
      ],
      "uncertainties": [
        "Requires a chain of Banelings within sight of each other to relay positions back to the Overseer, assuming coordinate transformations are possible.",
        "The Overseer needs to identify which Baneling each position refers to; without explicit agent id in relayed messages, association may be ambiguous."
      ]
    }
  ],
  "unsupported_assumptions": [
    "Agents maintain an internal memory of the Roach's position for relay (IR2), as the observation vector does not include a dedicated memory slot for communicated information.",
    "Coordinate transformations (vector addition) can be performed by agents using relative positions of allies and communicated vectors.",
    "Agent type identification from ally_i_type_0/1 is reliable to distinguish Overseer from Banelings.",
    "Communication channel allows scalar or vector transmission of relative positions (not explicitly specified in observation)."
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
