{
  "policy_hypothesis": "Symmetric attacker group G1 communicates ball-carrier intentions to improve run-pass-shoot coordination. When an agent has possession (ball close), it sends its absolute position, ball relative location, and ball trajectory direction to its teammate. The off-ball agent uses this to anticipate the intended pass or shot, timing its runs and positioning for receiving the ball or covering the goal.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        "controlled_agent_0",
        "controlled_agent_1"
      ],
      "role_basis": "Both agents are attackers with symmetric observation indices [0,21] and identical action spaces. They are expected to coordinate the run-pass-and-shoot sequence."
    }
  ],
  "rules": [
    {
      "rule_id": "R1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "teammate_0",
        "observable_basis": [
          "Each agent's local observation includes teammate_0_relative_xy (indices 2-3) and teammate_0_direction_xy (indices 6-7). With exactly two controlled agents, teammate_0 always references the other attacker."
        ]
      },
      "when": {
        "feature_names": [
          "ball_relative_xy"
        ],
        "feature_indices": [
          16,
          17
        ],
        "operator": "norm_less_than",
        "threshold": 0.1,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "Normalized pitch coordinates; ball_relative_xy magnitude <0.1 implies the ball is very close (approximately 10% of pitch length), indicating clear possession by the observing player."
        }
      },
      "what": {
        "feature_names": [
          "ego_absolute_xy",
          "ball_relative_xy",
          "ball_direction_xyz"
        ],
        "feature_indices": [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      },
      "sender_feasibility": "All features are directly observable by the sender from its local observation at indices [0,1], [16,17], and [19-21] respectively. No additional computation required.",
      "receiver_necessity": "The receiver cannot infer the sender's absolute position from its own relative observation without communication. Knowing the ball's relative position and trajectory allows the off-ball agent to anticipate whether the ball carrier will shoot (ball directed toward goal) or pass (ball directed toward teammate), and to time its run accordingly.",
      "expected_rollout_behavior": "Upon gaining possession (ball within threshold), the ball carrier transmits its absolute location, ball relative location, and ball movement direction. The off-ball agent uses the absolute position to estimate the passer's location on the pitch, combined with ball direction to infer pass target or shooting intent, and adjusts its movement to create a passing lane or prepare for a shot opportunity.",
      "uncertainties": [
        "Opponent indexing: opponent_0 assumed to be field defender, opponent_1 assumed to be goalkeeper; not verified in schema.",
        "Ball direction may be zero or noisy before the actual kick, reducing timely intention communication.",
        "Teammate intention can change rapidly after communication due to opponent movement.",
        "Goalkeeper behavior only partially observed, adding uncertainty to shooting decisions."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Communicating 7 environment features (ego_absolute_xy, ball_relative_xy, ball_direction_xyz) provides rich spatial context but consumes communication bandwidth. An alternative would be to send the sender's previous action one-hot (indices 22-40) as a proxy for intention, but that does not guarantee future intent and violates the priority on environment observations. The chosen trigger (ball-close) minimizes unnecessary communication when no agent has possession, but may miss early coordination opportunities if the ball carrier wants to signal a pass before receiving the ball."
}