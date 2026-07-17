
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
      "decision": "Roach selects a movement direction (north/south/east/west) to navigate around the pit and reach the Reapers.",
      "locally_missing_information": [
        "Positions (relative coordinates) of all Reaper enemies, because the pit blocks the Roach's vision, making all enemy_*_available flags 0."
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Roach selects an attack target (which Reaper to focus on) once in range.",
      "locally_missing_information": [
        "Health values of the Reapers to prioritise damaged enemies.",
        "Which Reaper the other Roach is currently attacking or intends to attack, to avoid redundant overkill."
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "overseer (agent_id 0)",
      "role_basis": "Overseer is a flying unit not blocked by the pit; its observation vector is expected to have enemy_0_available .. enemy_3_available = 1, giving it full vision of all Reaper positions and health. This unique sensor role makes it the primary source of enemy information."
    },
    {
      "group_id": "G2",
      "members": "roach (agent_id 1), roach (agent_id 2)",
      "role_basis": "Both Roaches are ground units with vision blocked by the central pit. Their observation vectors are expected to show enemy_*_available = 0 initially, making them dependent on external information for movement and target selection. They can observe each other and the Overseer (ally_*_visible = 1)."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Relative (x, y) positions of all 4 Reapers.",
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
          "name": "enemy_1_rel_x",
          "index": 14
        },
        {
          "name": "enemy_1_rel_y",
          "index": 15
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
          "name": "enemy_3_rel_x",
          "index": 30
        },
        {
          "name": "enemy_3_rel_y",
          "index": 31
        }
      ],
      "receiver_need_hypothesis": "Roaches need enemy locations to compute a movement direction that navigates around the pit and closes distance. Without this, they cannot decide which cardinal direction to move.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Enemy positions are relative to the Overseer; each Roach must combine the received message with its own knowledge of the Overseer's relative position (via ally_* features) to obtain egocentric coordinates.",
        "Reapers may move while the information is being transmitted, introducing staleness."
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "Current health of each Reaper.",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "enemy_0_health",
          "index": 8
        },
        {
          "name": "enemy_1_health",
          "index": 16
        },
        {
          "name": "enemy_2_health",
          "index": 24
        },
        {
          "name": "enemy_3_health",
          "index": 32
        }
      ],
      "receiver_need_hypothesis": "Roaches benefit from focusing fire on the weakest Reapers to reduce enemy numbers quickly. Without health information they may waste attacks on full-health targets.",
      "task_decision_ids": [
        "D2"
      ],
      "uncertainties": [
        "Health values can change rapidly once combat begins; communicated values may be outdated by the time the Roach acts."
      ]
    },
    {
      "requirement_id": "IR3",
      "fact": "Intended or current attack target (Reaper ID) of the other Roach.",
      "possible_sender_groups": [
        "G2"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [],
      "receiver_need_hypothesis": "If both Roaches select the same target independently it can lead to overkill and leave other full‑health Reapers unthreatened. Sharing target intention allows the Roaches to distribute attacks efficiently.",
      "task_decision_ids": [
        "D2"
      ],
      "uncertainties": [
        "The sender’s intended target is an internal decision variable not directly available in its own observation vector; it must be communicated from the policy output or an explicit intention channel.",
        "If the communication delay is long the sender may have already changed its target by the time the receiver acts."
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
