{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "On-ball action selection: choose to shoot, pass, or dribble.",
      "locally_missing_information": [
        "teammate's intended action and availability to receive a pass",
        "teammate's movement plan relative to defenders and goal"
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Off-ball movement: choose position and timing to receive a pass or create space for a shot.",
      "locally_missing_information": [
        "ball carrier's intended action (pass, dribble, shoot) and timing",
        "intended pass direction and recipient"
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": ["controlled_agent_0", "controlled_agent_1"],
      "role_basis": "Both agents are attackers with symmetric observation indices [0-21] and identical action spaces. No task evidence differentiates static roles (e.g., striker vs. winger). They are expected to coordinate the run-pass-and-shoot sequence."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Teammate's current intended discrete action (pass/shoot/dribble/move-to-receive) and intended movement target zone.",
      "possible_sender_groups": ["G1"],
      "possible_receiver_groups": ["G1"],
      "sender_observable_features": [
        {"name": "ego_absolute_xy", "index": [0, 1]},
        {"name": "teammate_0_relative_xy", "index": [2, 3]},
        {"name": "teammate_0_direction_xy", "index": [6, 7]},
        {"name": "opponent_0_relative_xy", "index": [8, 9]},
        {"name": "opponent_1_relative_xy", "index": [10, 11]},
        {"name": "ball_relative_xy", "index": [16, 17]},
        {"name": "ball_z", "index": 18},
        {"name": "ball_direction_xyz", "index": [19, 20, 21]},
        {"name": "previous_19_actions_onehot", "index": [22, 40], "note": "Agent's own previous action one-hot, may provide context for intention but does not guarantee future intent."}
      ],
      "receiver_need_hypothesis": "Without explicit communication, the receiver must infer the teammate's intention from delayed kinematic cues (ball movement, teammate acceleration). This can cause mis-coordination, wasted steps, and reduced shooting opportunity quality. Communicating the intention early enables the off-ball agent to time runs and select passing lanes, and the on-ball agent to choose an optimal pass target.",
      "task_decision_ids": ["D1", "D2"],
      "uncertainties": [
        "Opponent field defender may intercept passes based on ball trajectory, making coordination timing critical.",
        "Teammate's intention may change rapidly after communication due to dynamic opponent positioning.",
        "Goalkeeper behavior (diving, rushing out) is partially observed and adds uncertainty to shooting decisions.",
        "Assumption: opponent_0 is the field defender and opponent_1 the goalkeeper (not confirmed by schema)."
      ]
    }
  ],
  "unsupported_assumptions": [
    "Opponent indexing: opponent_0 assumed to be field defender, opponent_1 assumed to be goalkeeper based on typical GRF academy scenario setup, but not verified in given schema.",
    "Previous action one-hot (indices 22-40) is assumed to encode the observing agent's own previous action, not the teammate's; this interpretation follows the LMAC pattern of appending own history, but absolute confirmation is missing.",
    "Ball_z and ball_direction_xyz are assumed to provide sufficient height and trajectory information for shooting assessment.",
    "No other hidden information (e.g., stamina, fatigue) is present beyond the listed observation features."
  ]
}