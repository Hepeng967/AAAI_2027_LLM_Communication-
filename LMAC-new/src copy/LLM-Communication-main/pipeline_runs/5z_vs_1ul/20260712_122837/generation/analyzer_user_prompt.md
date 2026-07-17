
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


Identify information requirements before designing communication. Return:
{
  "task_decisions": [{"decision_id":"D1","decision":"...","locally_missing_information":["..."]}],
  "agent_groups": [{"group_id":"G1","members":"...","role_basis":"observation/task evidence"}],
  "information_requirements": [
    {"requirement_id":"IR1","fact":"...","possible_sender_groups":["G1"],
      "possible_receiver_groups":["G1"],"sender_observable_features":
      [{"name":"...","index":0}],"receiver_need_hypothesis":"...",
      "task_decision_ids":["D1"],"uncertainties":["..."]}
  ],
  "unsupported_assumptions": []
}
Do not assume a designated agent, threshold, feature, or sparse/dense topology
without explaining its task/observation basis.
