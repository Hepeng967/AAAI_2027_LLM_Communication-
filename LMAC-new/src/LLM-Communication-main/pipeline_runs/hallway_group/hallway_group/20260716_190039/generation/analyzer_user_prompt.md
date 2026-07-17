
Task and aligned observation description:
hallway_group coordination task 'hallway_group'
- Objective: Members of each group must reach position 0 simultaneously; groups should finish in separate rounds.
- Number of agents: 7.
- Per-agent maximum positions: [3, 5, 7, 4, 6, 8, 10].
- Actions: {0: 'stay', 1: 'move one step toward 0', 2: 'move one step away from 0'}.
- Information boundary: Each agent observes only its own position and whether its group remains active.
- Raw local observation length: 2.
- Runtime LMAC communication input length: 12.
- Runtime input appends previous-action one-hot and agent-ID one-hot to the raw observation.
- Agent ID may be used to recover the fixed maximum-position assignment from the task configuration.
- Fixed group assignment by agent row: [0, 0, 0, 1, 1, 1, 1].
- Number of groups: 2.
- Failure condition: A group fails when only a subset of its active members reaches position 0.
- Failure condition: If multiple groups finish in the same round, that round is rolled back and penalized.
- Observation feature index map:
    - 0~0: current_position
    - 1~1: active_status
    - 2~2: previous_action_0
    - 3~3: previous_action_1
    - 4~4: previous_action_2
    - 5~5: agent_id_0
    - 6~6: agent_id_1
    - 7~7: agent_id_2
    - 8~8: agent_id_3
    - 9~9: agent_id_4
    - 10~10: agent_id_5
    - 11~11: agent_id_6
- Runtime alignment: The LMAC policy consumes raw environment observation followed by previous-action one-hot and agent-id one-hot. For this rollout: environment observation indices are [0,1], previous action indices are [2,4], and agent ID indices are [5,11]. WHAT should prioritize environment observations; previous action or agent ID may only be selected with an explicit coordination justification. Undocumented env_extra dimensions must not be assigned invented semantics.

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
