
Translate this structured LMAC communication policy into a complete Python module:

{
  "policy_hypothesis": "Controlled agents use ball-proximity to dynamically partition into ball carrier (G1) and off-ball receivers (G2). The ball carrier communicates its identity and previous action to receivers; each off-ball receiver communicates its absolute position and opponent relative positions/directions to the ball carrier. Thresholds are LLM hypotheses.",
  "agent_groups": [
    {
      "group_id": "G1",
      "role": "ball carrier",
      "membership_rule": "ball_relative_xy (indices 20-21) L2 norm < 0.15",
      "observable_basis": "indices 20-21: ball_relative_xy"
    },
    {
      "group_id": "G2",
      "role": "off-ball receiver",
      "membership_rule": "ball_relative_xy (indices 20-21) L2 norm >= 0.15",
      "observable_basis": "indices 20-21: ball_relative_xy"
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
        "receiver_selector": "all agents in G2",
        "observable_basis": [
          "agent_id_one_hot (indices 45-47) is locally available to sender"
        ]
      },
      "when": {
        "feature_names": [
          "ball_relative_xy_norm"
        ],
        "feature_indices": [
          20,
          21
        ],
        "operator": "<",
        "threshold": 0.15,
        "threshold_basis": {
          "type": "llm_hypothesis",
          "evidence": "no rollout distribution available; chosen as a reasonable proximity for possession in GRF normalized coordinates"
        }
      },
      "what": {
        "feature_names": [
          "agent_id_one_hot"
        ],
        "feature_indices": [
          45,
          46,
          47
        ]
      },
      "sender_feasibility": "Sender computes ball_distance from indices 20-21; if below threshold, it knows it is G1 and can read its own agent_id one-hot from indices 45-47 appended to the observation.",
      "receiver_necessity": "Off-ball receivers cannot directly observe who possesses the ball; they need the carrier's identity to adjust positioning and make supporting runs (D2).",
      "expected_rollout_behavior": "When an agent becomes the ball carrier, it broadcasts its identity every step until possession is lost. Receivers update a belief of which agent is the carrier.",
      "uncertainties": [
        "Possession threshold is an LLM hypothesis; multiple agents may simultaneously satisfy the condition, causing conflicting broadcasts.",
        "Loose ball scenarios are not addressed; the nearest agent might erroneously claim possession."
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "the current agent in G1 (ball carrier)",
        "observable_basis": [
          "ego_absolute_xy (indices 0-1) is observed by sender"
        ]
      },
      "when": {
        "feature_names": [
          "ball_relative_xy_norm"
        ],
        "feature_indices": [
          20,
          21
        ],
        "operator": ">=",
        "threshold": 0.15,
        "threshold_basis": {
          "type": "llm_hypothesis",
          "evidence": "complement of G1 membership threshold"
        }
      },
      "what": {
        "feature_names": [
          "ego_absolute_xy"
        ],
        "feature_indices": [
          0,
          1
        ]
      },
      "sender_feasibility": "Off-ball agent can read its own absolute position from indices 0-1.",
      "receiver_necessity": "Ball carrier lacks teammates' absolute coordinates (only relative positions are in own observation); absolute positions are needed for long passes, offside avoidance, and strategic decision-making (D1, D3).",
      "expected_rollout_behavior": "Each off-ball agent continuously transmits its absolute position to the ball carrier, enabling the carrier to compute global pitch layout.",
      "uncertainties": [
        "Position data is exact; the main uncertainty is the trigger timing (constant transmission may waste bandwidth but is acceptable)."
      ]
    },
    {
      "rule_id": "R3",
      "requirement_ids": [
        "IR3"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "the current agent in G1 (ball carrier)",
        "observable_basis": [
          "opponent_0_relative_xy (indices 12-13)",
          "opponent_1_relative_xy (indices 14-15)"
        ]
      },
      "when": {
        "feature_names": [
          "ball_relative_xy_norm"
        ],
        "feature_indices": [
          20,
          21
        ],
        "operator": ">=",
        "threshold": 0.15,
        "threshold_basis": {
          "type": "llm_hypothesis",
          "evidence": "complement of G1 membership threshold"
        }
      },
      "what": {
        "feature_names": [
          "opponent_0_relative_xy",
          "opponent_1_relative_xy"
        ],
        "feature_indices": [
          12,
          13,
          14,
          15
        ]
      },
      "sender_feasibility": "Off-ball agent observes opponent positions relative to itself from indices 12-15.",
      "receiver_necessity": "Ball carrier cannot see how opponents are positioned relative to a potential receiver; this view is critical for assessing passing lanes and defensive pressure (D1, D3).",
      "expected_rollout_behavior": "Off-ball agents relay opponent relative positions to the ball carrier, allowing the carrier to evaluate which teammate is under pressure and select a safe pass.",
      "uncertainties": [
        "Opponent slot mapping (which index corresponds to field defender vs goalkeeper) is not explicitly labelled; agents and carrier must infer roles from context.",
        "The mapping is assumed stable within an episode; dynamic reordering would invalidate semantics."
      ]
    },
    {
      "rule_id": "R4",
      "requirement_ids": [
        "IR4"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "the current agent in G1 (ball carrier)",
        "observable_basis": [
          "opponent_0_direction_xy (indices 16-17)",
          "opponent_1_direction_xy (indices 18-19)"
        ]
      },
      "when": {
        "feature_names": [
          "ball_relative_xy_norm"
        ],
        "feature_indices": [
          20,
          21
        ],
        "operator": ">=",
        "threshold": 0.15,
        "threshold_basis": {
          "type": "llm_hypothesis",
          "evidence": "complement of G1 membership threshold"
        }
      },
      "what": {
        "feature_names": [
          "opponent_0_direction_xy",
          "opponent_1_direction_xy"
        ],
        "feature_indices": [
          16,
          17,
          18,
          19
        ]
      },
      "sender_feasibility": "Off-ball agent can observe opponent direction vectors from indices 16-19.",
      "receiver_necessity": "Opponent facing direction indicates interception threat and movement intent; ball carrier needs this from teammates' perspectives (not its own) to gauge pass risk (D1, D3).",
      "expected_rollout_behavior": "Off-ball agents transmit opponent directions, enhancing the carrier's risk assessment for each passing option.",
      "uncertainties": [
        "Same opponent index ambiguity as IR3; role inference required."
      ]
    },
    {
      "rule_id": "R5",
      "requirement_ids": [
        "IR5"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all agents in G2",
        "observable_basis": [
          "previous_action_one_hot (indices 26-44) is available in sender's runtime observation"
        ]
      },
      "when": {
        "feature_names": [
          "ball_relative_xy_norm"
        ],
        "feature_indices": [
          20,
          21
        ],
        "operator": "<",
        "threshold": 0.15,
        "threshold_basis": {
          "type": "llm_hypothesis",
          "evidence": "same possession threshold as R1"
        }
      },
      "what": {
        "feature_names": [
          "previous_action_one_hot"
        ],
        "feature_indices": [
          26,
          27,
          28,
          29,
          30,
          31,
          32,
          33,
          34,
          35,
          36,
          37,
          38,
          39,
          40,
          41,
          42,
          43,
          44
        ]
      },
      "sender_feasibility": "Ball carrier's runtime input includes a 19-action one-hot from the previous step (indices 26-44); the carrier can access and broadcast this.",
      "receiver_necessity": "Off-ball receivers lack direct knowledge of the carrier's most recent discrete action; this information helps infer short-term intent (e.g., recent dribble suggests imminent pass/shoot) and time off-ball movements accordingly (D2). Coordination justification: The previous-action one-hot is not an environment observation but is required to resolve partial observability regarding the ball carrier's action history as stated in IR5.",
      "expected_rollout_behavior": "While in possession, the ball carrier broadcasts its previous action each step; off-ball agents use this to adjust their run timing and anticipation of passes.",
      "uncertainties": [
        "Previous action is a lagged indicator; coordination based on it may be one step behind the carrier's true current intent.",
        "Using non-environment observation may cause the learned policy to overfit to this particular one-hot encoding if not handled carefully."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Sparse communication may be more efficient but the provided thresholds are LLM hypotheses and may need tuning based on actual ball distances during play. Constant broadcasting by off-ball agents (R2-R4) could saturate the communication channel but ensures the ball carrier always has up-to-date information. The opponent index mapping (0 vs 1) is ambiguous; receivers must learn to distinguish field defender from goalkeeper from context, which adds complexity. The previous-action communication (R5) is a non-standard feature selection justified by partial observability of action history; it risks overfitting to the one-hot format but is necessary for the receivers to infer ball carrier intent."
}

Runtime interface:
- n_agents: 3
- obs_dim: 48
- observation feature index map: {'ego_absolute_xy': [0, 2], 'teammate_0_relative_xy': [2, 4], 'teammate_1_relative_xy': [4, 6], 'ego_direction_xy': [6, 8], 'teammate_0_direction_xy': [8, 10], 'teammate_1_direction_xy': [10, 12], 'opponent_0_relative_xy': [12, 14], 'opponent_1_relative_xy': [14, 16], 'opponent_0_direction_xy': [16, 18], 'opponent_1_direction_xy': [18, 20], 'ball_relative_xy': [20, 22], 'ball_z': [22, 23], 'ball_direction_xyz': [23, 26], 'previous_action_0': [26, 27], 'previous_action_1': [27, 28], 'previous_action_2': [28, 29], 'previous_action_3': [29, 30], 'previous_action_4': [30, 31], 'previous_action_5': [31, 32], 'previous_action_6': [32, 33], 'previous_action_7': [33, 34], 'previous_action_8': [34, 35], 'previous_action_9': [35, 36], 'previous_action_10': [36, 37], 'previous_action_11': [37, 38], 'previous_action_12': [38, 39], 'previous_action_13': [39, 40], 'previous_action_14': [40, 41], 'previous_action_15': [41, 42], 'previous_action_16': [42, 43], 'previous_action_17': [43, 44], 'previous_action_18': [44, 45], 'agent_id_0': [45, 46], 'agent_id_1': [46, 47], 'agent_id_2': [47, 48]}

Required functions:
1. message_design_instruction() -> a concise string explaining the policy.
2. communication_who(o) -> [batch, receiver, sender] in [0,1].
3. communication_when(o) -> [batch, receiver, sender] in [0,1].
4. communication_what(o) -> an obs-aligned content mask with exactly the same
   shape as o, in [0,1]. A selected feature remains at its original index;
   unselected features are zero. Never compress or reorder features.

Constraints:
- o has shape [batch, n_agents, obs_dim].
- WHO and WHEN use matrix[:, receiver, sender] convention.
- WHO and WHEN must have zero self-communication diagonal.
- Use runtime o.shape[-1]; safely skip an index that is out of range.
- Use vectorized torch operations. Do not loop over batch elements, agents,
  senders, receivers, or observation dimensions.
- Implement every policy rule exactly once and mark its implementation with a
  comment containing its stable rule_id (for example, `# RULE R1`). Do not add
  tactical rules, thresholds, feature selections, or agent roles absent from the
  policy specification. If a stated rule cannot be implemented from the runtime
  observation, leave it inactive and explain why in its rule comment.
- The runtime derives edge_matrix = clamp(who * when, 0, 1) and
  masked_message = o * what_mask; do not implement extra wrapper functions.
- Output only imports, message_design_instruction, optional vectorized helper
  functions, and the three executable communication functions in one
  ```python block```.

Validation feedback, if any:

