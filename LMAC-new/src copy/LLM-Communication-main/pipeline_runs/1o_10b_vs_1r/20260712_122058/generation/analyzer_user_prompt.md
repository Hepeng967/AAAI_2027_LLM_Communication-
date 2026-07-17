
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
