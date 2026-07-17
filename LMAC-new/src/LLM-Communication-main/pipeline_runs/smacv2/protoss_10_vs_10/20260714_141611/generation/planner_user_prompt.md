
Task and aligned observation description:
SMACv2 cooperative combat task 'protoss_10_vs_10'
- Objective: Ten allied units cooperate under partial observability to defeat ten enemy units.
- Agents/enemies: 10/10.
- Possible allied unit types: ['stalker', 'zealot', 'colossus'] with sampling weights [0.45, 0.45, 0.1].
- Unit composition and the agent-to-unit-type assignment can change every episode.
- Agent ID is only a tensor-row identity. Never infer a fixed unit role from agent ID.
- Infer roles from the documented observable unit-type fields.
- The teacher receives the collection of all allied local observations and may compare them.
- Do not use global state, future information, hidden environment state, or invented feature semantics.
- Documented raw observation length: 182.
- Runtime LMAC input length: 208.
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
    - 9~9: enemy_0_shield
    - 10~10: enemy_0_unit_type_stalker
    - 11~11: enemy_0_unit_type_zealot
    - 12~12: enemy_0_unit_type_colossus
    - 13~13: enemy_1_available
    - 14~14: enemy_1_distance
    - 15~15: enemy_1_relative_x
    - 16~16: enemy_1_relative_y
    - 17~17: enemy_1_health
    - 18~18: enemy_1_shield
    - 19~19: enemy_1_unit_type_stalker
    - 20~20: enemy_1_unit_type_zealot
    - 21~21: enemy_1_unit_type_colossus
    - 22~22: enemy_2_available
    - 23~23: enemy_2_distance
    - 24~24: enemy_2_relative_x
    - 25~25: enemy_2_relative_y
    - 26~26: enemy_2_health
    - 27~27: enemy_2_shield
    - 28~28: enemy_2_unit_type_stalker
    - 29~29: enemy_2_unit_type_zealot
    - 30~30: enemy_2_unit_type_colossus
    - 31~31: enemy_3_available
    - 32~32: enemy_3_distance
    - 33~33: enemy_3_relative_x
    - 34~34: enemy_3_relative_y
    - 35~35: enemy_3_health
    - 36~36: enemy_3_shield
    - 37~37: enemy_3_unit_type_stalker
    - 38~38: enemy_3_unit_type_zealot
    - 39~39: enemy_3_unit_type_colossus
    - 40~40: enemy_4_available
    - 41~41: enemy_4_distance
    - 42~42: enemy_4_relative_x
    - 43~43: enemy_4_relative_y
    - 44~44: enemy_4_health
    - 45~45: enemy_4_shield
    - 46~46: enemy_4_unit_type_stalker
    - 47~47: enemy_4_unit_type_zealot
    - 48~48: enemy_4_unit_type_colossus
    - 49~49: enemy_5_available
    - 50~50: enemy_5_distance
    - 51~51: enemy_5_relative_x
    - 52~52: enemy_5_relative_y
    - 53~53: enemy_5_health
    - 54~54: enemy_5_shield
    - 55~55: enemy_5_unit_type_stalker
    - 56~56: enemy_5_unit_type_zealot
    - 57~57: enemy_5_unit_type_colossus
    - 58~58: enemy_6_available
    - 59~59: enemy_6_distance
    - 60~60: enemy_6_relative_x
    - 61~61: enemy_6_relative_y
    - 62~62: enemy_6_health
    - 63~63: enemy_6_shield
    - 64~64: enemy_6_unit_type_stalker
    - 65~65: enemy_6_unit_type_zealot
    - 66~66: enemy_6_unit_type_colossus
    - 67~67: enemy_7_available
    - 68~68: enemy_7_distance
    - 69~69: enemy_7_relative_x
    - 70~70: enemy_7_relative_y
    - 71~71: enemy_7_health
    - 72~72: enemy_7_shield
    - 73~73: enemy_7_unit_type_stalker
    - 74~74: enemy_7_unit_type_zealot
    - 75~75: enemy_7_unit_type_colossus
    - 76~76: enemy_8_available
    - 77~77: enemy_8_distance
    - 78~78: enemy_8_relative_x
    - 79~79: enemy_8_relative_y
    - 80~80: enemy_8_health
    - 81~81: enemy_8_shield
    - 82~82: enemy_8_unit_type_stalker
    - 83~83: enemy_8_unit_type_zealot
    - 84~84: enemy_8_unit_type_colossus
    - 85~85: enemy_9_available
    - 86~86: enemy_9_distance
    - 87~87: enemy_9_relative_x
    - 88~88: enemy_9_relative_y
    - 89~89: enemy_9_health
    - 90~90: enemy_9_shield
    - 91~91: enemy_9_unit_type_stalker
    - 92~92: enemy_9_unit_type_zealot
    - 93~93: enemy_9_unit_type_colossus
    - 94~94: ally_slot_0_visible
    - 95~95: ally_slot_0_distance
    - 96~96: ally_slot_0_relative_x
    - 97~97: ally_slot_0_relative_y
    - 98~98: ally_slot_0_health
    - 99~99: ally_slot_0_shield
    - 100~100: ally_slot_0_unit_type_stalker
    - 101~101: ally_slot_0_unit_type_zealot
    - 102~102: ally_slot_0_unit_type_colossus
    - 103~103: ally_slot_1_visible
    - 104~104: ally_slot_1_distance
    - 105~105: ally_slot_1_relative_x
    - 106~106: ally_slot_1_relative_y
    - 107~107: ally_slot_1_health
    - 108~108: ally_slot_1_shield
    - 109~109: ally_slot_1_unit_type_stalker
    - 110~110: ally_slot_1_unit_type_zealot
    - 111~111: ally_slot_1_unit_type_colossus
    - 112~112: ally_slot_2_visible
    - 113~113: ally_slot_2_distance
    - 114~114: ally_slot_2_relative_x
    - 115~115: ally_slot_2_relative_y
    - 116~116: ally_slot_2_health
    - 117~117: ally_slot_2_shield
    - 118~118: ally_slot_2_unit_type_stalker
    - 119~119: ally_slot_2_unit_type_zealot
    - 120~120: ally_slot_2_unit_type_colossus
    - 121~121: ally_slot_3_visible
    - 122~122: ally_slot_3_distance
    - 123~123: ally_slot_3_relative_x
    - 124~124: ally_slot_3_relative_y
    - 125~125: ally_slot_3_health
    - 126~126: ally_slot_3_shield
    - 127~127: ally_slot_3_unit_type_stalker
    - 128~128: ally_slot_3_unit_type_zealot
    - 129~129: ally_slot_3_unit_type_colossus
    - 130~130: ally_slot_4_visible
    - 131~131: ally_slot_4_distance
    - 132~132: ally_slot_4_relative_x
    - 133~133: ally_slot_4_relative_y
    - 134~134: ally_slot_4_health
    - 135~135: ally_slot_4_shield
    - 136~136: ally_slot_4_unit_type_stalker
    - 137~137: ally_slot_4_unit_type_zealot
    - 138~138: ally_slot_4_unit_type_colossus
    - 139~139: ally_slot_5_visible
    - 140~140: ally_slot_5_distance
    - 141~141: ally_slot_5_relative_x
    - 142~142: ally_slot_5_relative_y
    - 143~143: ally_slot_5_health
    - 144~144: ally_slot_5_shield
    - 145~145: ally_slot_5_unit_type_stalker
    - 146~146: ally_slot_5_unit_type_zealot
    - 147~147: ally_slot_5_unit_type_colossus
    - 148~148: ally_slot_6_visible
    - 149~149: ally_slot_6_distance
    - 150~150: ally_slot_6_relative_x
    - 151~151: ally_slot_6_relative_y
    - 152~152: ally_slot_6_health
    - 153~153: ally_slot_6_shield
    - 154~154: ally_slot_6_unit_type_stalker
    - 155~155: ally_slot_6_unit_type_zealot
    - 156~156: ally_slot_6_unit_type_colossus
    - 157~157: ally_slot_7_visible
    - 158~158: ally_slot_7_distance
    - 159~159: ally_slot_7_relative_x
    - 160~160: ally_slot_7_relative_y
    - 161~161: ally_slot_7_health
    - 162~162: ally_slot_7_shield
    - 163~163: ally_slot_7_unit_type_stalker
    - 164~164: ally_slot_7_unit_type_zealot
    - 165~165: ally_slot_7_unit_type_colossus
    - 166~166: ally_slot_8_visible
    - 167~167: ally_slot_8_distance
    - 168~168: ally_slot_8_relative_x
    - 169~169: ally_slot_8_relative_y
    - 170~170: ally_slot_8_health
    - 171~171: ally_slot_8_shield
    - 172~172: ally_slot_8_unit_type_stalker
    - 173~173: ally_slot_8_unit_type_zealot
    - 174~174: ally_slot_8_unit_type_colossus
    - 175~175: own_health
    - 176~176: own_shield
    - 177~177: own_normalized_x
    - 178~178: own_normalized_y
    - 179~179: own_unit_type_stalker
    - 180~180: own_unit_type_zealot
    - 181~181: own_unit_type_colossus
    - 182~182: previous_action_0
    - 183~183: previous_action_1
    - 184~184: previous_action_2
    - 185~185: previous_action_3
    - 186~186: previous_action_4
    - 187~187: previous_action_5
    - 188~188: previous_action_6
    - 189~189: previous_action_7
    - 190~190: previous_action_8
    - 191~191: previous_action_9
    - 192~192: previous_action_10
    - 193~193: previous_action_11
    - 194~194: previous_action_12
    - 195~195: previous_action_13
    - 196~196: previous_action_14
    - 197~197: previous_action_15
    - 198~198: agent_id_0
    - 199~199: agent_id_1
    - 200~200: agent_id_2
    - 201~201: agent_id_3
    - 202~202: agent_id_4
    - 203~203: agent_id_5
    - 204~204: agent_id_6
    - 205~205: agent_id_7
    - 206~206: agent_id_8
    - 207~207: agent_id_9
- Runtime alignment: The LMAC policy consumes raw environment observation followed by previous-action one-hot and agent-id one-hot. For this rollout: environment observation indices are [0,181], previous action indices are [182,197], and agent ID indices are [198,207]. WHAT should prioritize environment observations; previous action or agent ID may only be selected with an explicit coordination justification. Undocumented env_extra dimensions must not be assigned invented semantics.

Information-requirement analysis:
{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Select an enemy unit to engage (move towards and attack). This requires knowing the full set of enemy units, their types, health, shield, and positions to prioritize high-value targets, avoid overkill, and coordinate focus fire.",
      "locally_missing_information": [
        "Existence, type, health, shield, and position of enemy units not currently visible to the agent."
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Choose movement direction for formation coordination, positioning, retreat, or support. This requires knowing the positions, types, and health of all allied units to maintain appropriate front/backline, avoid collisions, and react to ally status.",
      "locally_missing_information": [
        "Type, health, shield, and position of allied units not currently visible to the agent."
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "all agents whose own_unit_type_zealot == 1 (zealot)",
      "role_basis": "observation/task evidence: zealots are melee units, typical frontline tanks; decision priorities focus on engaging and absorbing damage."
    },
    {
      "group_id": "G2",
      "members": "all agents whose own_unit_type_stalker == 1 (stalker)",
      "role_basis": "observation/task evidence: stalkers are ranged, high-damage units; they should stay behind zealots and focus fire on priority targets."
    },
    {
      "group_id": "G3",
      "members": "all agents whose own_unit_type_colossus == 1 (colossus)",
      "role_basis": "observation/task evidence: colossi are heavy ranged units with strong area damage; they should position safely behind the frontline and target clusters."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Complete inventory of all 10 enemy units: existence flag, unit type, current health, current shield, and global (absolute) coordinates (x, y).",
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
          "index": 177
        },
        {
          "name": "own_normalized_y",
          "index": 178
        },
        {
          "name": "enemy_k_available",
          "index": "4+9*k for k=0..9"
        },
        {
          "name": "enemy_k_relative_x",
          "index": "6+9*k"
        },
        {
          "name": "enemy_k_relative_y",
          "index": "7+9*k"
        },
        {
          "name": "enemy_k_health",
          "index": "8+9*k"
        },
        {
          "name": "enemy_k_shield",
          "index": "9+9*k"
        },
        {
          "name": "enemy_k_unit_type_stalker",
          "index": "10+9*k"
        },
        {
          "name": "enemy_k_unit_type_zealot",
          "index": "11+9*k"
        },
        {
          "name": "enemy_k_unit_type_colossus",
          "index": "12+9*k"
        }
      ],
      "receiver_need_hypothesis": "An agent that cannot see a particular enemy lacks its position, type, and status, leading to suboptimal engagement decisions (e.g., attacking a low-value target, ignoring a high-threat enemy, or moving into an ambush). Providing the full enemy set enables coordinated target selection and efficient movement.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Enemy positions are relative to the sender; the teacher must transform them to a common global frame using sender's own coordinates — precision may degrade with movement delays.",
        "Agents may receive information they already possess, causing redundancy; filtering requires teacher-level knowledge of each agent's current observation.",
        "Receivers' policies may not be trained to incorporate externally communicated enemy data effectively."
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "Complete inventory of all 9 other allied units: type, current health, current shield, and global (absolute) coordinates (x, y).",
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
          "index": 177
        },
        {
          "name": "own_normalized_y",
          "index": 178
        },
        {
          "name": "ally_slot_m_visible",
          "index": "94+9*m for m=0..8"
        },
        {
          "name": "ally_slot_m_relative_x",
          "index": "96+9*m"
        },
        {
          "name": "ally_slot_m_relative_y",
          "index": "97+9*m"
        },
        {
          "name": "ally_slot_m_health",
          "index": "98+9*m"
        },
        {
          "name": "ally_slot_m_shield",
          "index": "99+9*m"
        },
        {
          "name": "ally_slot_m_unit_type_stalker",
          "index": "100+9*m"
        },
        {
          "name": "ally_slot_m_unit_type_zealot",
          "index": "101+9*m"
        },
        {
          "name": "ally_slot_m_unit_type_colossus",
          "index": "102+9*m"
        }
      ],
      "receiver_need_hypothesis": "Without knowledge of hidden allies, an agent may choose a movement direction that collides with friendlies, breaks formation (e.g., a stalker moving in front of zealots), or fails to support a low-health ally. Full allied status information allows formation-aware movement and improved team coherence.",
      "task_decision_ids": [
        "D2"
      ],
      "uncertainties": [
        "Ally slot indices do not consistently correspond to the same physical unit across agents; teacher must disambiguate using transformed global positions.",
        "Motion and latency can make communicated ally positions stale; time-critical decisions may be affected.",
        "Receiving agents may not have learned to use ally spatial information for movement planning."
      ]
    }
  ],
  "unsupported_assumptions": []
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
