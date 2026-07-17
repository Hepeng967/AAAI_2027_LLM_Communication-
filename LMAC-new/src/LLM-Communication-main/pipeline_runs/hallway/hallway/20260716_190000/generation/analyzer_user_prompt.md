
Task and aligned observation description:
hallway coordination task 'hallway'
- Objective: All agents must reach position 0 on the same timestep.
- Number of agents: 4.
- Per-agent maximum positions: [4, 6, 8, 10].
- Actions: {0: 'stay', 1: 'move one step toward 0', 2: 'move one step away from 0'}.
- Information boundary: Each agent locally observes only its own current position.
- Raw local observation length: 1.
- Runtime LMAC communication input length: 8.
- Runtime input appends previous-action one-hot and agent-ID one-hot to the raw observation.
- Agent ID may be used to recover the fixed maximum-position assignment from the task configuration.
- Failure condition: The episode terminates unsuccessfully if only a subset reaches position 0.
- Observation feature index map:
    - 0~0: current_position
    - 1~1: previous_action_0
    - 2~2: previous_action_1
    - 3~3: previous_action_2
    - 4~4: agent_id_0
    - 5~5: agent_id_1
    - 6~6: agent_id_2
    - 7~7: agent_id_3
- Runtime alignment: The LMAC policy consumes raw environment observation followed by previous-action one-hot and agent-id one-hot. For this rollout: environment observation indices are [0,0], previous action indices are [1,3], and agent ID indices are [4,7]. WHAT should prioritize environment observations; previous action or agent ID may only be selected with an explicit coordination justification. Undocumented env_extra dimensions must not be assigned invented semantics.

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
