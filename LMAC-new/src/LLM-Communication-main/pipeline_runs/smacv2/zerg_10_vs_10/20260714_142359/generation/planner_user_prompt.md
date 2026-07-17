
Task and aligned observation description:
SMACv2 cooperative combat task 'zerg_10_vs_10'
- Objective: Ten allied units cooperate under partial observability to defeat ten enemy units.
- Agents/enemies: 10/10.
- Possible allied unit types: ['zergling', 'hydralisk', 'baneling'] with sampling weights [0.45, 0.45, 0.1].
- Unit composition and the agent-to-unit-type assignment can change every episode.
- Agent ID is only a tensor-row identity. Never infer a fixed unit role from agent ID.
- Infer roles from the documented observable unit-type fields.
- The teacher receives the collection of all allied local observations and may compare them.
- Do not use global state, future information, hidden environment state, or invented feature semantics.
- Documented raw observation length: 162.
- Runtime LMAC input length: 188.
- Observation feature index map:
    - 0~0: move_north
    - 1~1: move_south
    - 2~2: move_east
    - 3~3: move_west
    - 4~4: enemy_0_available
    - 5~5: enemy_0_distance
    - 6~6: enemy_0_relative_x
    - 7~7: enemy_0_relative_y
    - 8~8: enemy_0_health
    - 9~9: enemy_0_unit_type_zergling
    - 10~10: enemy_0_unit_type_hydralisk
    - 11~11: enemy_0_unit_type_baneling
    - 12~12: enemy_1_available
    - 13~13: enemy_1_distance
    - 14~14: enemy_1_relative_x
    - 15~15: enemy_1_relative_y
    - 16~16: enemy_1_health
    - 17~17: enemy_1_unit_type_zergling
    - 18~18: enemy_1_unit_type_hydralisk
    - 19~19: enemy_1_unit_type_baneling
    - 20~20: enemy_2_available
    - 21~21: enemy_2_distance
    - 22~22: enemy_2_relative_x
    - 23~23: enemy_2_relative_y
    - 24~24: enemy_2_health
    - 25~25: enemy_2_unit_type_zergling
    - 26~26: enemy_2_unit_type_hydralisk
    - 27~27: enemy_2_unit_type_baneling
    - 28~28: enemy_3_available
    - 29~29: enemy_3_distance
    - 30~30: enemy_3_relative_x
    - 31~31: enemy_3_relative_y
    - 32~32: enemy_3_health
    - 33~33: enemy_3_unit_type_zergling
    - 34~34: enemy_3_unit_type_hydralisk
    - 35~35: enemy_3_unit_type_baneling
    - 36~36: enemy_4_available
    - 37~37: enemy_4_distance
    - 38~38: enemy_4_relative_x
    - 39~39: enemy_4_relative_y
    - 40~40: enemy_4_health
    - 41~41: enemy_4_unit_type_zergling
    - 42~42: enemy_4_unit_type_hydralisk
    - 43~43: enemy_4_unit_type_baneling
    - 44~44: enemy_5_available
    - 45~45: enemy_5_distance
    - 46~46: enemy_5_relative_x
    - 47~47: enemy_5_relative_y
    - 48~48: enemy_5_health
    - 49~49: enemy_5_unit_type_zergling
    - 50~50: enemy_5_unit_type_hydralisk
    - 51~51: enemy_5_unit_type_baneling
    - 52~52: enemy_6_available
    - 53~53: enemy_6_distance
    - 54~54: enemy_6_relative_x
    - 55~55: enemy_6_relative_y
    - 56~56: enemy_6_health
    - 57~57: enemy_6_unit_type_zergling
    - 58~58: enemy_6_unit_type_hydralisk
    - 59~59: enemy_6_unit_type_baneling
    - 60~60: enemy_7_available
    - 61~61: enemy_7_distance
    - 62~62: enemy_7_relative_x
    - 63~63: enemy_7_relative_y
    - 64~64: enemy_7_health
    - 65~65: enemy_7_unit_type_zergling
    - 66~66: enemy_7_unit_type_hydralisk
    - 67~67: enemy_7_unit_type_baneling
    - 68~68: enemy_8_available
    - 69~69: enemy_8_distance
    - 70~70: enemy_8_relative_x
    - 71~71: enemy_8_relative_y
    - 72~72: enemy_8_health
    - 73~73: enemy_8_unit_type_zergling
    - 74~74: enemy_8_unit_type_hydralisk
    - 75~75: enemy_8_unit_type_baneling
    - 76~76: enemy_9_available
    - 77~77: enemy_9_distance
    - 78~78: enemy_9_relative_x
    - 79~79: enemy_9_relative_y
    - 80~80: enemy_9_health
    - 81~81: enemy_9_unit_type_zergling
    - 82~82: enemy_9_unit_type_hydralisk
    - 83~83: enemy_9_unit_type_baneling
    - 84~84: ally_slot_0_visible
    - 85~85: ally_slot_0_distance
    - 86~86: ally_slot_0_relative_x
    - 87~87: ally_slot_0_relative_y
    - 88~88: ally_slot_0_health
    - 89~89: ally_slot_0_unit_type_zergling
    - 90~90: ally_slot_0_unit_type_hydralisk
    - 91~91: ally_slot_0_unit_type_baneling
    - 92~92: ally_slot_1_visible
    - 93~93: ally_slot_1_distance
    - 94~94: ally_slot_1_relative_x
    - 95~95: ally_slot_1_relative_y
    - 96~96: ally_slot_1_health
    - 97~97: ally_slot_1_unit_type_zergling
    - 98~98: ally_slot_1_unit_type_hydralisk
    - 99~99: ally_slot_1_unit_type_baneling
    - 100~100: ally_slot_2_visible
    - 101~101: ally_slot_2_distance
    - 102~102: ally_slot_2_relative_x
    - 103~103: ally_slot_2_relative_y
    - 104~104: ally_slot_2_health
    - 105~105: ally_slot_2_unit_type_zergling
    - 106~106: ally_slot_2_unit_type_hydralisk
    - 107~107: ally_slot_2_unit_type_baneling
    - 108~108: ally_slot_3_visible
    - 109~109: ally_slot_3_distance
    - 110~110: ally_slot_3_relative_x
    - 111~111: ally_slot_3_relative_y
    - 112~112: ally_slot_3_health
    - 113~113: ally_slot_3_unit_type_zergling
    - 114~114: ally_slot_3_unit_type_hydralisk
    - 115~115: ally_slot_3_unit_type_baneling
    - 116~116: ally_slot_4_visible
    - 117~117: ally_slot_4_distance
    - 118~118: ally_slot_4_relative_x
    - 119~119: ally_slot_4_relative_y
    - 120~120: ally_slot_4_health
    - 121~121: ally_slot_4_unit_type_zergling
    - 122~122: ally_slot_4_unit_type_hydralisk
    - 123~123: ally_slot_4_unit_type_baneling
    - 124~124: ally_slot_5_visible
    - 125~125: ally_slot_5_distance
    - 126~126: ally_slot_5_relative_x
    - 127~127: ally_slot_5_relative_y
    - 128~128: ally_slot_5_health
    - 129~129: ally_slot_5_unit_type_zergling
    - 130~130: ally_slot_5_unit_type_hydralisk
    - 131~131: ally_slot_5_unit_type_baneling
    - 132~132: ally_slot_6_visible
    - 133~133: ally_slot_6_distance
    - 134~134: ally_slot_6_relative_x
    - 135~135: ally_slot_6_relative_y
    - 136~136: ally_slot_6_health
    - 137~137: ally_slot_6_unit_type_zergling
    - 138~138: ally_slot_6_unit_type_hydralisk
    - 139~139: ally_slot_6_unit_type_baneling
    - 140~140: ally_slot_7_visible
    - 141~141: ally_slot_7_distance
    - 142~142: ally_slot_7_relative_x
    - 143~143: ally_slot_7_relative_y
    - 144~144: ally_slot_7_health
    - 145~145: ally_slot_7_unit_type_zergling
    - 146~146: ally_slot_7_unit_type_hydralisk
    - 147~147: ally_slot_7_unit_type_baneling
    - 148~148: ally_slot_8_visible
    - 149~149: ally_slot_8_distance
    - 150~150: ally_slot_8_relative_x
    - 151~151: ally_slot_8_relative_y
    - 152~152: ally_slot_8_health
    - 153~153: ally_slot_8_unit_type_zergling
    - 154~154: ally_slot_8_unit_type_hydralisk
    - 155~155: ally_slot_8_unit_type_baneling
    - 156~156: own_health
    - 157~157: own_normalized_x
    - 158~158: own_normalized_y
    - 159~159: own_unit_type_zergling
    - 160~160: own_unit_type_hydralisk
    - 161~161: own_unit_type_baneling
    - 162~162: previous_action_0
    - 163~163: previous_action_1
    - 164~164: previous_action_2
    - 165~165: previous_action_3
    - 166~166: previous_action_4
    - 167~167: previous_action_5
    - 168~168: previous_action_6
    - 169~169: previous_action_7
    - 170~170: previous_action_8
    - 171~171: previous_action_9
    - 172~172: previous_action_10
    - 173~173: previous_action_11
    - 174~174: previous_action_12
    - 175~175: previous_action_13
    - 176~176: previous_action_14
    - 177~177: previous_action_15
    - 178~178: agent_id_0
    - 179~179: agent_id_1
    - 180~180: agent_id_2
    - 181~181: agent_id_3
    - 182~182: agent_id_4
    - 183~183: agent_id_5
    - 184~184: agent_id_6
    - 185~185: agent_id_7
    - 186~186: agent_id_8
    - 187~187: agent_id_9
- Runtime alignment: The LMAC policy consumes raw environment observation followed by previous-action one-hot and agent-id one-hot. For this rollout: environment observation indices are [0,161], previous action indices are [162,177], and agent ID indices are [178,187]. WHAT should prioritize environment observations; previous action or agent ID may only be selected with an explicit coordination justification. Undocumented env_extra dimensions must not be assigned invented semantics.

Information-requirement analysis:
{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Select which enemy to attack from visible enemies, considering enemy health, type, distance, and ally focus fire.",
      "locally_missing_information": [
        "Health of enemies not currently visible to the agent.",
        "Types of enemies not visible.",
        "Positions of enemies not visible.",
        "Which enemies are currently being targeted by other allies."
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Choose movement direction/positioning, such as advancing, retreating, flanking, or grouping with allies.",
      "locally_missing_information": [
        "Positions and health of unseen allies.",
        "Types of unseen allies (to infer formation roles).",
        "Positions of unseen enemies (flanking threats).",
        "Overall team health status and whether allies need assistance."
      ]
    },
    {
      "decision_id": "D3",
      "decision": "For baneling units, decide when to run into enemy group to maximize explosive damage while minimizing ally collateral.",
      "locally_missing_information": [
        "Enemy cluster density and positions beyond vision.",
        "Ally positions relative to potential blast area (including unseen allies).",
        "Health of enemies that might survive the blast."
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "Agents whose own_unit_type_zergling == 1",
      "role_basis": "Unit type dictates melee flanker role; need to coordinate surround and focus low-health enemies."
    },
    {
      "group_id": "G2",
      "members": "Agents whose own_unit_type_hydralisk == 1",
      "role_basis": "Unit type dictates ranged support role; need to maintain distance and focus fire on priority targets."
    },
    {
      "group_id": "G3",
      "members": "Agents whose own_unit_type_baneling == 1",
      "role_basis": "Unit type dictates suicide bomber role; need to coordinate timing with ally safety and enemy grouping."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "My own agent status: agent ID, health, unit type, global position (normalized).",
      "possible_sender_groups": [
        "G1",
        "G2",
        "G3"
      ],
      "possible_receiver_groups": [
        "G1",
        "G2",
        "G3"
      ],
      "sender_observable_features": [
        {
          "name": "own_health",
          "index": 156
        },
        {
          "name": "own_normalized_x",
          "index": 157
        },
        {
          "name": "own_normalized_y",
          "index": 158
        },
        {
          "name": "own_unit_type_zergling",
          "index": 159
        },
        {
          "name": "own_unit_type_hydralisk",
          "index": 160
        },
        {
          "name": "own_unit_type_baneling",
          "index": 161
        },
        {
          "name": "agent_id_0",
          "index": 178
        },
        {
          "name": "agent_id_1",
          "index": 179
        },
        {
          "name": "agent_id_2",
          "index": 180
        },
        {
          "name": "agent_id_3",
          "index": 181
        },
        {
          "name": "agent_id_4",
          "index": 182
        },
        {
          "name": "agent_id_5",
          "index": 183
        },
        {
          "name": "agent_id_6",
          "index": 184
        },
        {
          "name": "agent_id_7",
          "index": 185
        },
        {
          "name": "agent_id_8",
          "index": 186
        },
        {
          "name": "agent_id_9",
          "index": 187
        }
      ],
      "receiver_need_hypothesis": "Receivers need to know ally identities, positions, types, and health to coordinate movement (e.g., forming a line, assisting low-health allies) and to interpret future communications about enemy sightings relative to that ally.",
      "task_decision_ids": [
        "D1",
        "D2",
        "D3"
      ],
      "uncertainties": [
        "Agent ID one-hot indices 178-187; the active ID must be extracted. Global normalized coordinates might not be perfectly aligned across agents, but assumed consistent within the map."
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "Enemy status: global position (computed as own_position + relative_x/y), health, unit type, for a visible enemy (example enemy slot 0; pattern repeats for slots 1–9).",
      "possible_sender_groups": [
        "G1",
        "G2",
        "G3"
      ],
      "possible_receiver_groups": [
        "G1",
        "G2",
        "G3"
      ],
      "sender_observable_features": [
        {
          "name": "own_normalized_x",
          "index": 157
        },
        {
          "name": "own_normalized_y",
          "index": 158
        },
        {
          "name": "enemy_0_available",
          "index": 4
        },
        {
          "name": "enemy_0_distance",
          "index": 5
        },
        {
          "name": "enemy_0_relative_x",
          "index": 6
        },
        {
          "name": "enemy_0_relative_y",
          "index": 7
        },
        {
          "name": "enemy_0_health",
          "index": 8
        },
        {
          "name": "enemy_0_unit_type_zergling",
          "index": 9
        },
        {
          "name": "enemy_0_unit_type_hydralisk",
          "index": 10
        },
        {
          "name": "enemy_0_unit_type_baneling",
          "index": 11
        }
      ],
      "receiver_need_hypothesis": "To build a shared enemy map, receivers need to know the health, type and location of enemies they cannot see, enabling better target selection (focus fire, priority threats) and movement decisions (avoiding flanks). Global position allows disambiguation when enemy slot indices differ across agents.",
      "task_decision_ids": [
        "D1",
        "D2",
        "D3"
      ],
      "uncertainties": [
        "Enemy slot indices i are agent-specific; the communicated enemy must be identified by its global location, not slot index. Enemies with identical positions may cause confusion.",
        "The computation of global position assumes that relative_x/y are in a coordinate system aligned with own_normalized_x/y and that scaling is consistent."
      ]
    },
    {
      "requirement_id": "IR3",
      "fact": "Ally status: health, unit type, global position of a specific ally (matching to an agent ID, e.g., via previously shared own-status). Example: ally seen in sender's slot 0; pattern repeats for slots 0–8.",
      "possible_sender_groups": [
        "G1",
        "G2",
        "G3"
      ],
      "possible_receiver_groups": [
        "G1",
        "G2",
        "G3"
      ],
      "sender_observable_features": [
        {
          "name": "own_normalized_x",
          "index": 157
        },
        {
          "name": "own_normalized_y",
          "index": 158
        },
        {
          "name": "ally_slot_0_visible",
          "index": 84
        },
        {
          "name": "ally_slot_0_distance",
          "index": 85
        },
        {
          "name": "ally_slot_0_relative_x",
          "index": 86
        },
        {
          "name": "ally_slot_0_relative_y",
          "index": 87
        },
        {
          "name": "ally_slot_0_health",
          "index": 88
        },
        {
          "name": "ally_slot_0_unit_type_zergling",
          "index": 89
        },
        {
          "name": "ally_slot_0_unit_type_hydralisk",
          "index": 90
        },
        {
          "name": "ally_slot_0_unit_type_baneling",
          "index": 91
        }
      ],
      "receiver_need_hypothesis": "Agents need to know the health and type of allies that are outside their vision to decide whether to assist a low-health ally or to maintain formation. Global position allows matching to known ally slots when visible, and tracking when not.",
      "task_decision_ids": [
        "D2",
        "D3"
      ],
      "uncertainties": [
        "Ally slot j is specific to the sender; the receiver cannot directly map slot j to its own slot. The identity of the ally must be included (via agent ID) if the sender can infer it. If the sender does not know the agent ID of the ally in slot j, the information is ambiguous.",
        "The sender might deduce agent ID from matching observed ally attributes to previously communicated own-status messages (IR1). This assumes a prior round of communication has linked agent IDs to positions."
      ]
    }
  ],
  "unsupported_assumptions": [
    "Global normalized coordinate system (own_normalized_x/y) is common across agents and can be used to spatially relate communicated positions.",
    "Enemies have distinct positions, allowing disambiguation via global coordinates despite slot alias issues.",
    "Agents can compute enemy global position by adding relative coordinates to own position, and this is accurate.",
    "Agent ID one-hot (indices 178-187) is stable and can be included in messages to identify individuals.",
    "The teacher can compare observations and deduce which ally slot corresponds to which agent ID, enabling communication of ally status with agent ID even if the agent can't directly observe ID (e.g., by matching positions).",
    "Communication latency is negligible relative to decision timescale.",
    "Unit types determine role, and agents can self-identify their group based on own_unit_type features.",
    "Patterns for enemy slots 1–9 and ally slots 1–8 follow the same index offset formulas as the examples given."
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
