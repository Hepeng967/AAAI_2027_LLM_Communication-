
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
    - 49~49: env_extra_49
    - 50~50: env_extra_50
    - 51~51: env_extra_51
    - 52~52: env_extra_52
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
      "decision": "Roach selects a movement target among enemies",
      "locally_missing_information": [
        "Enemy availability (which enemies exist)",
        "Enemy positions relative to roach"
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Roach selects which enemy to attack to coordinate with ally",
      "locally_missing_information": [
        "Designated target assignment (which enemy each roach should focus)"
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "agent_id 0 (overseer)",
      "role_basis": "Task says Overseer can locate Reapers; observation schema includes enemy features (likely sees across pit)."
    },
    {
      "group_id": "G2",
      "members": "agent_id 1 and 2 (roaches)",
      "role_basis": "Task says Roaches must rely on Overseer communication; pit blocks vision so roaches' enemy_available=0."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Positions and availability of each reaper enemy",
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
          "name": "enemy_1_available",
          "index": 11
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
          "name": "enemy_2_available",
          "index": 18
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
          "name": "enemy_3_available",
          "index": 25
        },
        {
          "name": "enemy_3_rel_x",
          "index": 27
        },
        {
          "name": "enemy_3_rel_y",
          "index": 28
        }
      ],
      "receiver_need_hypothesis": "Roaches need enemy locations relative to themselves to navigate around the pit and engage. Without this, they cannot locate enemies.",
      "task_decision_ids": [
        "D1",
        "D2"
      ],
      "uncertainties": [
        "Assumes overseer can always observe all enemies; vision may degrade with distance or if overseer moves."
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "Which enemy each roach should attack to focus fire",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "ally_0_rel_x",
          "index": 34
        },
        {
          "name": "ally_0_rel_y",
          "index": 35
        },
        {
          "name": "ally_1_rel_x",
          "index": 41
        },
        {
          "name": "ally_1_rel_y",
          "index": 42
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
          "name": "enemy_1_rel_x",
          "index": 13
        },
        {
          "name": "enemy_1_rel_y",
          "index": 14
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
          "name": "enemy_3_rel_x",
          "index": 27
        },
        {
          "name": "enemy_3_rel_y",
          "index": 28
        }
      ],
      "receiver_need_hypothesis": "Coordinated focus fire improves elimination speed; roaches need common assignment to avoid splitting damage or overkill.",
      "task_decision_ids": [
        "D2"
      ],
      "uncertainties": [
        "Roaches may prefer nearest target, conflicting with assignment; assignment may become stale if enemy dies."
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
