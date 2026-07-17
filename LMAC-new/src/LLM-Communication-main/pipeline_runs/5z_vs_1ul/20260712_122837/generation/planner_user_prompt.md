
Task and aligned observation description:
The map is 5z_vs_1ul. You can control 5 Zealot units against 1 powerful Ultralisk unit. The Ultralisk has extremely high health and devastating area damage, making it crucial to coordinate your Zealots carefully. When any Zealot's health drops below 20%, it must immediately retreat and kite away from the Ultralisk. Other healthy Zealots should actively engage the Ultralisk to draw its attention and protect the wounded unit. Use focus fire tactics and avoid clustering to minimize area damage. This scenario tests advanced multi-agent coordination, health management, and tactical positioning against a superior enemy.Observation information for map '5z_vs_1ul':
- Each agent observes a vector of length 48.
- There are 5 agents. Their types are: zealot, zealot, zealot, zealot, zealot.
- Each row of the observation corresponds to agent_id: [0, 1, 2, 3, 4], and their types: ['zealot', 'zealot', 'zealot', 'zealot', 'zealot'].
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
    - 9: ally_0_visible
    - 10: ally_0_distance
    - 11: ally_0_rel_x
    - 12: ally_0_rel_y
    - 13: ally_0_health
    - 14: ally_0_shield
    - 15: ally_1_visible
    - 16: ally_1_distance
    - 17: ally_1_rel_x
    - 18: ally_1_rel_y
    - 19: ally_1_health
    - 20: ally_1_shield
    - 21: ally_2_visible
    - 22: ally_2_distance
    - 23: ally_2_rel_x
    - 24: ally_2_rel_y
    - 25: ally_2_health
    - 26: ally_2_shield
    - 27: ally_3_visible
    - 28: ally_3_distance
    - 29: ally_3_rel_x
    - 30: ally_3_rel_y
    - 31: ally_3_health
    - 32: ally_3_shield
    - 33: own_health
    - 34: own_shield
    - ?: lmac_extra_35
    - ?: lmac_extra_36
    - ?: lmac_extra_37
    - ?: lmac_extra_38
    - ?: lmac_extra_39
    - ?: lmac_extra_40
    - ?: lmac_extra_41
    - ?: lmac_extra_42
    - ?: lmac_extra_43
    - ?: lmac_extra_44
    - ?: lmac_extra_45
    - ?: lmac_extra_46
    - ?: lmac_extra_47

LMAC rollout observation alignment:
- Runtime LMAC observation vector length: 48.
- Documented SMAC observation vector length: 35.
- Rollout available: True from /data/hp/LLM_Communication/LMAC-new/data.
- Use runtime obs_shape for generated code and tests.
- Dimensions named lmac_extra_* are wrapper/config-added features; do not treat them as hidden global state.
- Additional runtime dimensions:
    - 35~35: env_extra_35
    - 36~36: previous_action_0
    - 37~37: previous_action_1
    - 38~38: previous_action_2
    - 39~39: previous_action_3
    - 40~40: previous_action_4
    - 41~41: previous_action_5
    - 42~42: previous_action_6
    - 43~43: agent_id_0
    - 44~44: agent_id_1
    - 45~45: agent_id_2
    - 46~46: agent_id_3
    - 47~47: agent_id_4


Information-requirement analysis:
{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Retreat/kite when own health < 20%",
      "locally_missing_information": []
    },
    {
      "decision_id": "D2",
      "decision": "Protect a wounded ally by engaging the Ultralisk to draw its attention",
      "locally_missing_information": [
        "Ally health status when ally is not visible",
        "Ally location when ally is not visible"
      ]
    },
    {
      "decision_id": "D3",
      "decision": "Avoid clustering with allies to minimize area damage",
      "locally_missing_information": [
        "Positions of allies that are not currently visible"
      ]
    },
    {
      "decision_id": "D4",
      "decision": "Focus fire on the Ultralisk when engaging",
      "locally_missing_information": []
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "0,1,2,3,4",
      "role_basis": "All agents are homogeneous Zealots that must coordinate health management and tactical positioning. Roles dynamically split into 'healthy' (health >= 20%) and 'wounded' (health < 20%) based on the task description."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Agent i has health below 20%",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G1"
      ],
      "sender_observable_features": [
        {
          "name": "own_health",
          "index": 33
        }
      ],
      "receiver_need_hypothesis": "Agents need to know which ally is wounded to trigger protective engagement and to avoid retreating into that ally's path.",
      "task_decision_ids": [
        "D2",
        "D1"
      ],
      "uncertainties": [
        "Communication delay may cause stale health status",
        "Visibility of the wounded agent may be restored before the message is fully propagated",
        "Threshold is predefined (20%) but dynamic changes in health may lead to rapid toggling"
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "Agent i position relative to the Ultralisk",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G1"
      ],
      "sender_observable_features": [
        {
          "name": "enemy_0_rel_x",
          "index": 6
        },
        {
          "name": "enemy_0_rel_y",
          "index": 7
        }
      ],
      "receiver_need_hypothesis": "To move toward the wounded ally to draw aggro or to avoid clustering, agents need the wounded ally's location. The sender can report the enemy's relative position, from which the ally's location can be derived (negative of the vector).",
      "task_decision_ids": [
        "D2",
        "D3"
      ],
      "uncertainties": [
        "Coordinate frame misalignment: the sender's enemy_0_rel_x/y is in the sender's local coordinate frame. A receiver cannot directly map this to its own frame without knowing the sender's position relative to the receiver or having a shared absolute coordinate system. This may render positional information unusable.",
        "The Ultralisk moves, so the reported relative position becomes stale quickly."
      ]
    }
  ],
  "unsupported_assumptions": [
    "Agents can interpret the communicated relative position of a teammate to their own coordinate frame without additional absolute position information. The observation space does not provide absolute coordinates, and the only common reference (the Ultralisk) is given in each agent's own local frame."
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
