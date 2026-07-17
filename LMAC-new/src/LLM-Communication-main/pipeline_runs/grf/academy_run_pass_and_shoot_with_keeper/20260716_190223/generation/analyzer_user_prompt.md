
Task and aligned observation description:
Google Research Football task 'academy_run_pass_and_shoot_with_keeper'
- Objective: Two controlled attackers execute a run-pass-and-shoot sequence against one field defender and a goalkeeper.
- Controlled agents/opponents including goalkeeper: 2/2.
- Episode limit: 150 steps.
- Reward: 100 for scoring; a failed terminal episode returns -1; otherwise 0.
- Information boundary: A teacher may compare controlled players' local observations, but may not use unexposed raw football state, future events, or global state.
- Coordinates are in the GRF normalized pitch coordinate system.
- Teammate slots exclude the observing player; opponent slots include the configured field defender and goalkeeper.
- Relative positions are centered on the observing controlled player; direction vectors are not relative positions.
- Raw local observation length: 22.
- Runtime LMAC communication input length: 43.
- Runtime input appends the previous 19-action one-hot and controlled-player ID one-hot.
- Observation feature index map:
    - 0~1: ego_absolute_xy
    - 2~3: teammate_0_relative_xy
    - 4~5: ego_direction_xy
    - 6~7: teammate_0_direction_xy
    - 8~9: opponent_0_relative_xy
    - 10~11: opponent_1_relative_xy
    - 12~13: opponent_0_direction_xy
    - 14~15: opponent_1_direction_xy
    - 16~17: ball_relative_xy
    - 18~18: ball_z
    - 19~21: ball_direction_xyz
    - 22~22: previous_action_0
    - 23~23: previous_action_1
    - 24~24: previous_action_2
    - 25~25: previous_action_3
    - 26~26: previous_action_4
    - 27~27: previous_action_5
    - 28~28: previous_action_6
    - 29~29: previous_action_7
    - 30~30: previous_action_8
    - 31~31: previous_action_9
    - 32~32: previous_action_10
    - 33~33: previous_action_11
    - 34~34: previous_action_12
    - 35~35: previous_action_13
    - 36~36: previous_action_14
    - 37~37: previous_action_15
    - 38~38: previous_action_16
    - 39~39: previous_action_17
    - 40~40: previous_action_18
    - 41~41: agent_id_0
    - 42~42: agent_id_1
- Runtime alignment: The LMAC policy consumes raw environment observation followed by previous-action one-hot and agent-id one-hot. For this rollout: environment observation indices are [0,21], previous action indices are [22,40], and agent ID indices are [41,42]. WHAT should prioritize environment observations; previous action or agent ID may only be selected with an explicit coordination justification. Undocumented env_extra dimensions must not be assigned invented semantics.

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
