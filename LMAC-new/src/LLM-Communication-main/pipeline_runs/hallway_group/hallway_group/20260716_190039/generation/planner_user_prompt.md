
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

Information-requirement analysis:
{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Determine movement actions (stay, move toward 0, move away) to synchronize position with other members of the same group so that all reach position 0 simultaneously.",
      "locally_missing_information": [
        "Positions of other agents in the same group"
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Determine when the entire group should attempt to finish (all members move to 0) to avoid finishing in the same round as the other group.",
      "locally_missing_information": [
        "Active status of the other group",
        "Positions of agents in the other group (to anticipate their finish readiness)"
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        0,
        1,
        2
      ],
      "role_basis": "Fixed group assignment from task configuration; agents in G1 must finish together in the same round, distinct from G2."
    },
    {
      "group_id": "G2",
      "members": [
        3,
        4,
        5,
        6
      ],
      "role_basis": "Fixed group assignment from task configuration; agents in G2 must finish together in the same round, distinct from G1."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "current_position of each agent in group G1",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G1"
      ],
      "sender_observable_features": [
        {
          "name": "current_position",
          "index": 0
        }
      ],
      "receiver_need_hypothesis": "To know the distances of all G1 members from the target, enabling coordinated movement to reach 0 simultaneously.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Positions may become stale before the receiver acts due to communication delay and asynchronous action execution."
      ]
    },
    {
      "requirement_id": "IR2",
      "fact": "current_position of each agent in group G2",
      "possible_sender_groups": [
        "G2"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "current_position",
          "index": 0
        }
      ],
      "receiver_need_hypothesis": "To know the distances of all G2 members from the target, enabling coordinated movement to reach 0 simultaneously.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Positions may become stale before the receiver acts due to communication delay and asynchronous action execution."
      ]
    },
    {
      "requirement_id": "IR3",
      "fact": "active_status of group G1",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "active_status",
          "index": 1
        }
      ],
      "receiver_need_hypothesis": "To know when G1 has finished (active_status becomes 0), so that G2 can safely complete its own finish without causing a same-round conflict.",
      "task_decision_ids": [
        "D2"
      ],
      "uncertainties": [
        "Active_status=1 indicates G1 is still active, but G1 could decide to finish at the same moment G2 does, leading to a simultaneous finish and penalty; simple status observation does not guarantee mutual exclusion."
      ]
    },
    {
      "requirement_id": "IR4",
      "fact": "active_status of group G2",
      "possible_sender_groups": [
        "G2"
      ],
      "possible_receiver_groups": [
        "G1"
      ],
      "sender_observable_features": [
        {
          "name": "active_status",
          "index": 1
        }
      ],
      "receiver_need_hypothesis": "To know when G2 has finished (active_status becomes 0), so that G1 can safely complete its own finish without causing a same-round conflict.",
      "task_decision_ids": [
        "D2"
      ],
      "uncertainties": [
        "Active_status=1 indicates G2 is still active, but G2 could decide to finish at the same moment G1 does, leading to a simultaneous finish and penalty; simple status observation does not guarantee mutual exclusion."
      ]
    },
    {
      "requirement_id": "IR5",
      "fact": "current_position of each agent in group G1",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "current_position",
          "index": 0
        }
      ],
      "receiver_need_hypothesis": "To estimate the collective distance of the other group from the target and better anticipate when they might attempt to finish, reducing risk of simultaneous finishes.",
      "task_decision_ids": [
        "D2"
      ],
      "uncertainties": [
        "Exact finish timing depends on future actions; positional proximity does not guarantee immediate finish, especially if agents deliberately delay."
      ]
    },
    {
      "requirement_id": "IR6",
      "fact": "current_position of each agent in group G2",
      "possible_sender_groups": [
        "G2"
      ],
      "possible_receiver_groups": [
        "G1"
      ],
      "sender_observable_features": [
        {
          "name": "current_position",
          "index": 0
        }
      ],
      "receiver_need_hypothesis": "To estimate the collective distance of the other group from the target and better anticipate when they might attempt to finish, reducing risk of simultaneous finishes.",
      "task_decision_ids": [
        "D2"
      ],
      "uncertainties": [
        "Exact finish timing depends on future actions; positional proximity does not guarantee immediate finish, especially if agents deliberately delay."
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
