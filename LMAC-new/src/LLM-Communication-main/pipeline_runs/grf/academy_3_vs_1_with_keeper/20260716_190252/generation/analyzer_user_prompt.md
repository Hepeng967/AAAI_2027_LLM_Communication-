
Task and aligned observation description:
Google Research Football task 'academy_3_vs_1_with_keeper'
- Objective: Three controlled attackers cooperate against one field defender and a goalkeeper, using positioning and passes to score.
- Controlled agents/opponents including goalkeeper: 3/2.
- Episode limit: 150 steps.
- Reward: 100 for scoring; a failed terminal episode returns -1; otherwise 0.
- Information boundary: A teacher may compare controlled players' local observations, but may not use unexposed raw football state, future events, or global state.
- Coordinates are in the GRF normalized pitch coordinate system.
- Teammate slots exclude the observing player; opponent slots include the configured field defender and goalkeeper.
- Relative positions are centered on the observing controlled player; direction vectors are not relative positions.
- Raw local observation length: 26.
- Runtime LMAC communication input length: 48.
- Runtime input appends the previous 19-action one-hot and controlled-player ID one-hot.
- Observation feature index map:
    - 0~1: ego_absolute_xy
    - 2~3: teammate_0_relative_xy
    - 4~5: teammate_1_relative_xy
    - 6~7: ego_direction_xy
    - 8~9: teammate_0_direction_xy
    - 10~11: teammate_1_direction_xy
    - 12~13: opponent_0_relative_xy
    - 14~15: opponent_1_relative_xy
    - 16~17: opponent_0_direction_xy
    - 18~19: opponent_1_direction_xy
    - 20~21: ball_relative_xy
    - 22~22: ball_z
    - 23~25: ball_direction_xyz
    - 26~26: previous_action_0
    - 27~27: previous_action_1
    - 28~28: previous_action_2
    - 29~29: previous_action_3
    - 30~30: previous_action_4
    - 31~31: previous_action_5
    - 32~32: previous_action_6
    - 33~33: previous_action_7
    - 34~34: previous_action_8
    - 35~35: previous_action_9
    - 36~36: previous_action_10
    - 37~37: previous_action_11
    - 38~38: previous_action_12
    - 39~39: previous_action_13
    - 40~40: previous_action_14
    - 41~41: previous_action_15
    - 42~42: previous_action_16
    - 43~43: previous_action_17
    - 44~44: previous_action_18
    - 45~45: agent_id_0
    - 46~46: agent_id_1
    - 47~47: agent_id_2
- Runtime alignment: The LMAC policy consumes raw environment observation followed by previous-action one-hot and agent-id one-hot. For this rollout: environment observation indices are [0,25], previous action indices are [26,44], and agent ID indices are [45,47]. WHAT should prioritize environment observations; previous action or agent ID may only be selected with an explicit coordination justification. Undocumented env_extra dimensions must not be assigned invented semantics.

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
