## system

You analyze LLM-judged failures for LMAC communication policies. Return one compact JSON object only.

## user

Analyze the LLM judge result for map `5z_vs_1ul` and propose the next communication-code revision.

Judge summary:
{
  "accepted": false,
  "blocking_failures": [
    {
      "evidence": "In communication_when(), condition own_health < 20.0 is always true because own_health is a normalized scalar between 0.0 and 0.625 (rollout feature statistics: min 0.0, max 0.625, mean 0.06457). Consequently, sender_trigger is always 1, when_matrix is fully on (off-diagonal ones), and trigger_a in communication_what() always selects mask_a. This collapses the intended conditional strategy into a constant all-to-all broadcast of 7 features.",
      "revision_target": "when",
      "type": "out_of_scale_threshold"
    },
    {
      "evidence": "{\"who_when_what_consistent\": false, \"conflicts_or_uncovered_requirements\": [\"The out‑of‑scale threshold creates a contradiction between the intended conditional logic and the actual constant broadcast. R2 and R5 are effectively dead code, while R1 and R4 dominate, producing an always‑on homogeneous message.\"]}",
      "revision_target": "who|when|what",
      "type": "cross_rule_inconsistency"
    }
  ],
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_095059/iteration/5z_vs_1ul/20260712_095059/candidates/iter_000/comm_init.py",
  "cross_rule_check": {
    "conflicts_or_uncovered_requirements": [
      "The out‑of‑scale threshold creates a contradiction between the intended conditional logic and the actual constant broadcast. R2 and R5 are effectively dead code, while R1 and R4 dominate, producing an always‑on homogeneous message."
    ],
    "who_when_what_consistent": false
  },
  "dry_run": false,
  "evidence_case_ids": [
    "train_traj_0000:0",
    "train_traj_0000:13",
    "train_traj_0000:27",
    "train_traj_0000:54",
    "train_traj_0000:150"
  ],
  "expected_effect": "Fixing the out‑of‑scale threshold will restore the intended two‑mode communication: a distress signal when an agent is actually low on health, and a regular enemy report otherwise. This can reduce unnecessary messaging (message_nonzero_rate would drop when no enemy is present) and provide teammates with context‑sensitive information, potentially improving coordinated response to threats.",
  "failure_analysis": "The policy attempts to combine two triggers (low health, enemy visible) with different message content, but the low‑health threshold (20.0) is wildly out of range for the normalized observation space (max own_health ≈ 0.625). This makes the low‑health condition permanently true, turning the when matrix into an always‑on all‑to‑all broadcast and forcing the what mask to the constant 7‑feature set. The enemy‑visible trigger never activates, and the intended sparse, condition‑dependent communication degenerates into a trivial full‑broadcast scheme that sends identical information in every step. The strategy is therefore not a plausible conditional policy and cannot serve as a pure communication module.",
  "improvement_suggestions": "1. Scale the low‑health threshold to a normalized value (suggest own_health < 0.2 based on rollout statistics, or a value derived from max observed health). 2. Verify that after the fix, trigger_a and trigger_b alternate as intended; add a test for the disjointness condition. 3. Consider making the when condition more refined (e.g., only send if enemy distance is below a threshold, or if own health is below a fraction of max). 4. Ensure the what masks still select the intended features after the threshold correction.",
  "replacement_readiness": "not_ready",
  "rollout_grounding_score": 0.3,
  "rule_checks": [
    {
      "counterexample_case_ids": [
        "train_traj_0000:0",
        "train_traj_0000:13",
        "train_traj_0000:54"
      ],
      "observed_trigger_or_edge_rate": 1.0,
      "requirement_hypothesis": "Agents with critically low health should alert teammates (e.g., to request assistance or signal retreat).",
      "rule_id": "R1 (inferred: low‑health distress trigger)",
      "supporting_case_ids": [],
      "threshold_in_observed_range": false,
      "unresolved_questions": [
        "Threshold 20.0 is far outside observed range; it must be rescaled to a normalized value (e.g., <0.2) to represent actual low health."
      ],
      "what_supported": true,
      "when_supported": false,
      "who_supported": true
    },
    {
      "counterexample_case_ids": [
        "train_traj_0000:0",
        "train_traj_0000:13",
        "train_traj_0000:54"
      ],
      "observed_trigger_or_edge_rate": 0.0,
      "requirement_hypothesis": "When an enemy appears, agents should share its position and health for coordinated engagement.",
      "rule_id": "R2 (inferred: enemy‑visible trigger)",
      "supporting_case_ids": [],
      "threshold_in_observed_range": true,
      "unresolved_questions": [
        "This trigger is never reached because R1 always activates (trigger_a = 1), making trigger_b = (1−trigger_a)*condition_enemy_visible = 0. The intended what mask_b is never applied."
      ],
      "what_supported": false,
      "when_supported": false,
      "who_supported": true
    },
    {
      "counterexample_case_ids": [
        "train_traj_0000:0"
      ],
      "observed_trigger_or_edge_rate": 1.0,
      "requirement_hypothesis": "Low‑health distress takes priority over regular enemy reporting.",
      "rule_id": "R3 (inferred: disjoint priority)",
      "supporting_case_ids": [],
      "threshold_in_observed_range": true,
      "unresolved_questions": [
        "The priority rule is logical, but the constant activation of R1 renders it trivial and eliminates any adaptation."
      ],
      "what_supported": false,
      "when_supported": false,
      "who_supported": true
    },
    {
      "counterexample_case_ids": [],
      "observed_trigger_or_edge_rate": 1.0,
      "requirement_hypothesis": "In a small homogeneous team, every agent should be able to receive messages from every other agent.",
      "rule_id": "R4 (inferred: all‑to‑all connectivity)",
      "supporting_case_ids": [
        "train_traj_0000:0",
        "train_traj_0000:13",
        "train_traj_0000:150"
      ],
      "threshold_in_observed_range": true,
      "unresolved_questions": [],
      "what_supported": true,
      "when_supported": true,
      "who_supported": true
    },
    {
      "counterexample_case_ids": [
        "train_traj_0000:0"
      ],
      "observed_trigger_or_edge_rate": 0.0,
      "requirement_hypothesis": "The message content should be tailored: low‑health includes shield, enemy report omits shield.",
      "rule_id": "R5 (inferred: feature‑mask selection)",
      "supporting_case_ids": [],
      "threshold_in_observed_range": true,
      "unresolved_questions": [
        "Because of the broken threshold, the policy always uses mask_a (indices 4,5,6,7,8,33,34); the distinguishing behaviour of mask_b is never exercised."
      ],
      "what_supported": false,
      "when_supported": false,
      "who_supported": true
    }
  ],
  "score": 0.25,
  "usage": {
    "completion_tokens": 5665,
    "prompt_tokens": 17082,
    "total_tokens": 22747
  },
  "what_score": 0.65,
  "when_score": 0.0,
  "who_score": 0.8
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "5z_vs_1ul",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_095059/iteration/5z_vs_1ul/20260712_095059/candidates/iter_000/comm_init.py",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/5z_vs_1ul/train_traj_0000.pkl"
  ],
  "transitions": 151,
  "n_agents": 5,
  "rollout_obs_dim": 48,
  "message_dim": 48,
  "matrix_edge_rate": 1.0,
  "who_edge_rate": 1.0,
  "when_edge_rate": 1.0,
  "message_nonzero_rate": 0.14583333333333334,
  "message_abs_mean": 0.14583333333333334,
  "matrix_min": 0.0,
  "matrix_max": 1.0,
  "risk_flags": [
    "nearly_all_to_all_edges_on_rollout"
  ],
  "evidence_cases": [
    {
      "case_id": "train_traj_0000:0",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "5": 0.264106,
          "6": 0.0,
          "7": 0.264106,
          "8": 1.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 1.0,
          "5": 0.159831,
          "6": 0.0,
          "7": 0.159831,
          "8": 1.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 1.0,
          "5": 0.190838,
          "6": -0.104275,
          "7": 0.159831,
          "8": 1.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.625,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.625,
          "34": 1.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:13",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "5": 0.374281,
          "6": 0.230659,
          "7": 0.294759,
          "8": 0.965572,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 1.0,
          "5": 0.22961,
          "6": 0.163656,
          "7": 0.161051,
          "8": 0.965572,
          "33": 0.0,
          "34": 0.483418
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.625,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.625,
          "34": 1.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:27",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.625,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.625,
          "34": 1.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:40",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:54",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:68",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:81",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 1.0,
          "5": 0.240333,
          "6": -0.097059,
          "7": -0.219862,
          "8": 0.948166,
          "33": 0.0,
          "34": 0.81
        }
      ]
    },
    {
      "case_id": "train_traj_0000:95",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:109",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:122",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:136",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:150",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          0,
          2
        ],
        [
          0,
          3
        ],
        [
          0,
          4
        ],
        [
          1,
          0
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ],
        [
          3,
          4
        ],
        [
          4,
          0
        ],
        [
          4,
          1
        ],
        [
          4,
          2
        ],
        [
          4,
          3
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ],
        [
          4,
          5,
          6,
          7,
          8,
          33,
          34
        ]
      ],
      "selected_values_by_sender": [
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 1.0
        },
        {
          "4": 0.0,
          "5": 0.0,
          "6": 0.0,
          "7": 0.0,
          "8": 0.0,
          "33": 0.0,
          "34": 0.0
        }
      ]
    }
  ]
}

Recent trials:
[
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_095059/iteration/5z_vs_1ul/20260712_095059/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-12T09:51:36+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_095059/iteration/5z_vs_1ul/20260712_095059/candidates/iter_000/comm_init.py",
      "documented_obs_dim": 35,
      "map_name": "5z_vs_1ul",
      "matrix_edge_rate": 1.0,
      "matrix_max": 1.0,
      "matrix_min": 0.0,
      "message_dim": 48,
      "valid": true,
      "validation_obs_dim": 48,
      "validation_obs_source": "rollout",
      "what_dim": 48,
      "when_edge_rate": 1.0,
      "who_edge_rate": 1.0
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_095059/iteration/5z_vs_1ul/20260712_095059/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 48,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-12T09:51:36+00:00",
    "valid": true,
    "when_edge_rate": 1.0,
    "who_edge_rate": 1.0
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_095059/iteration/5z_vs_1ul/20260712_095059/candidates/iter_000/comm_init.py",
    "failure_analysis": "The policy attempts to combine two triggers (low health, enemy visible) with different message content, but the low‑health threshold (20.0) is wildly out of range for the normalized observation space (max own_health ≈ 0.625). This makes the low‑health condition permanently true, turning the when matrix into an always‑on all‑to‑all broadcast and forcing the what mask to the constant 7‑feature set. The enemy‑visible trigger never activates, and the intended sparse, condition‑dependent communication degenerates into a trivial full‑broadcast scheme that sends identical information in every step. The strategy is therefore not a plausible conditional policy and cannot serve as a pure communication module.",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 48,
    "next_hypothesis": "1. Scale the low‑health threshold to a normalized value (suggest own_health < 0.2 based on rollout statistics, or a value derived from max observed health). 2. Verify that after the fix, trigger_a and trigger_b alternate as intended; add a test for the disjointness condition. 3. Consider making the when condition more refined (e.g., only send if enemy distance is below a threshold, or if own health is below a fraction of max). 4. Ensure the what masks still select the intended features after the threshold correction.",
    "rollout_grounding_score": 0.3,
    "score": 0.25,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-12T09:53:26+00:00",
    "valid": true,
    "what_score": 0.65,
    "when_score": 0.0,
    "who_score": 0.8
  }
]

Current code:
```python
import torch

def message_design_instruction():
    return (
        "WHO: Each Zealot broadcasts to all other Zealots (no self-communication). "
        "WHEN: A sender sends a message if (a) own_health < 20 (low health distress) "
        "OR (b) enemy_0_available == 1 (enemy visible, combat information). "
        "WHAT: If low health (trigger a): send [own_health, own_shield, enemy_0_available, "
        "enemy_0_distance, enemy_0_rel_x, enemy_0_rel_y, enemy_0_health]. "
        "If healthy and enemy visible (trigger b): send [enemy_0_available, enemy_0_distance, "
        "enemy_0_rel_x, enemy_0_rel_y, enemy_0_health, own_health]. "
        "Otherwise send nothing (zero mask)."
    )


def communication_who(o):
    # o: (batch, n_agents, obs_dim)
    batch_size, n_agents, obs_dim = o.shape
    # All-to-all except self: matrix of ones minus identity
    who_matrix = torch.ones(batch_size, n_agents, n_agents, device=o.device)
    # Zero out self-communication on diagonal
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    who_matrix = who_matrix - mask_self
    # Clamp to [0,1] (should already be, but safety)
    who_matrix = torch.clamp(who_matrix, 0.0, 1.0)
    return who_matrix


def communication_when(o):
    batch_size, n_agents, obs_dim = o.shape
    # Extract features from observation: indices [33]=own_health, [4]=enemy_0_available
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)

    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    # Trigger conditions for each sender: 
    # (own_health < 20) OR (enemy_0_available > 0.5)
    condition_low_health = (own_health < 20.0).float()
    condition_enemy_visible = (enemy_available > 0.5).float()

    # Combined: trigger if either condition is 1
    sender_trigger = torch.max(condition_low_health, condition_enemy_visible)  # (batch, n_agents, 1)
    sender_trigger = sender_trigger.squeeze(-1)  # (batch, n_agents)

    # Build when matrix: for each (receiver, sender) pair, use sender's trigger
    when_matrix = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1)  # (batch, n_agents, n_agents)

    # Zero out self-communication (diagonal)
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    when_matrix = when_matrix * (1.0 - mask_self)

    # Ensure [0,1]
    when_matrix = torch.clamp(when_matrix, 0.0, 1.0)
    return when_matrix


def communication_what(o):
    batch_size, n_agents, obs_dim = o.shape

    # Feature indices for the two trigger types
    indices_a = [4, 5, 6, 7, 8, 33, 34]   # low health
    indices_b = [4, 5, 6, 7, 8, 33]        # enemy visible + healthy

    # Build masks without loops/list comprehensions
    idx_a_tensor = torch.tensor(indices_a, device=o.device, dtype=torch.long)
    valid_a = idx_a_tensor[idx_a_tensor < obs_dim]
    mask_a = torch.zeros(obs_dim, device=o.device)
    mask_a[valid_a] = 1.0

    idx_b_tensor = torch.tensor(indices_b, device=o.device, dtype=torch.long)
    valid_b = idx_b_tensor[idx_b_tensor < obs_dim]
    mask_b = torch.zeros(obs_dim, device=o.device)
    mask_b[valid_b] = 1.0

    # Extract conditions (same logic as `when`)
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    condition_low = (own_health < 20.0).float()          # (B, A, 1)
    condition_enemy = (enemy_available > 0.5).float()    # (B, A, 1)

    # Disjoint triggers: low-health first, enemy visibility only if not low
    trigger_a = condition_low                            # (B, A, 1)
    trigger_b = (1.0 - condition_low) * condition_enemy  # (B, A, 1)

    # Build what tensor via broadcasting (purely vectorized)
    what = trigger_a * mask_a.view(1, 1, -1) + trigger_b * mask_b.view(1, 1, -1)
    # Clamp to [0,1]
    what = torch.clamp(what, 0.0, 1.0)
    return what

```

Return JSON with keys:
- Evaluation
- Missing_Information_Hypothesis
- Improvement_Suggestions
- Target_Functions
- Target_Rule_IDs
Do not use downstream RL win-rate as feedback. Focus on rollout-grounded who/when/what critique only.
