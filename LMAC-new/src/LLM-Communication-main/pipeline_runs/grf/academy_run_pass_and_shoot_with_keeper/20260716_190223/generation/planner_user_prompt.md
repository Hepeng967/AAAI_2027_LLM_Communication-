
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

Information-requirement analysis:
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
      "members": [
        "controlled_agent_0",
        "controlled_agent_1"
      ],
      "role_basis": "Both agents are attackers with symmetric observation indices [0-21] and identical action spaces. No task evidence differentiates static roles (e.g., striker vs. winger). They are expected to coordinate the run-pass-and-shoot sequence."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Teammate's current intended discrete action (pass/shoot/dribble/move-to-receive) and intended movement target zone.",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G1"
      ],
      "sender_observable_features": [
        {
          "name": "ego_absolute_xy",
          "index": [
            0,
            1
          ]
        },
        {
          "name": "teammate_0_relative_xy",
          "index": [
            2,
            3
          ]
        },
        {
          "name": "teammate_0_direction_xy",
          "index": [
            6,
            7
          ]
        },
        {
          "name": "opponent_0_relative_xy",
          "index": [
            8,
            9
          ]
        },
        {
          "name": "opponent_1_relative_xy",
          "index": [
            10,
            11
          ]
        },
        {
          "name": "ball_relative_xy",
          "index": [
            16,
            17
          ]
        },
        {
          "name": "ball_z",
          "index": 18
        },
        {
          "name": "ball_direction_xyz",
          "index": [
            19,
            20,
            21
          ]
        },
        {
          "name": "previous_19_actions_onehot",
          "index": [
            22,
            40
          ],
          "note": "Agent's own previous action one-hot, may provide context for intention but does not guarantee future intent."
        }
      ],
      "receiver_need_hypothesis": "Without explicit communication, the receiver must infer the teammate's intention from delayed kinematic cues (ball movement, teammate acceleration). This can cause mis-coordination, wasted steps, and reduced shooting opportunity quality. Communicating the intention early enables the off-ball agent to time runs and select passing lanes, and the on-ball agent to choose an optimal pass target.",
      "task_decision_ids": [
        "D1",
        "D2"
      ],
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
