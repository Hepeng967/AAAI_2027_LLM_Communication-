## system

You analyze LLM-judged failures for LMAC communication policies. Return one compact JSON object only.

## user

Analyze the LLM judge result for map `5z_vs_1ul` and propose the next communication-code revision.

Judge summary:
{
  "accepted": false,
  "blocking_failures": [
    {
      "evidence": "own_health (index 33) observed max=0.625, threshold 20.0 always true; resulting when_edge_rate=1.0",
      "revision_target": "when",
      "type": "out_of_scale_threshold"
    },
    {
      "evidence": "{\"who_when_what_consistent\": false, \"conflicts_or_uncovered_requirements\": [\"R1 threshold bug makes the communication always‑on, overriding the intended selective R2; the observed behavior is a dense broadcast of three features, not the intended event‑driven strategy\"]}",
      "revision_target": "who|when|what",
      "type": "cross_rule_inconsistency"
    }
  ],
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_122837/iteration/5z_vs_1ul/20260712_122837/candidates/iter_000/comm_init.py",
  "cross_rule_check": {
    "conflicts_or_uncovered_requirements": [
      "R1 threshold bug makes the communication always‑on, overriding the intended selective R2; the observed behavior is a dense broadcast of three features, not the intended event‑driven strategy"
    ],
    "who_when_what_consistent": false
  },
  "dry_run": false,
  "evidence_case_ids": [
    "train_traj_0000:0",
    "train_traj_0000:13",
    "train_traj_0000:27",
    "train_traj_0000:40"
  ],
  "expected_effect": "Fixing the threshold will restore the intended event‑triggered communication: agents will only broadcast when wounded or upon seeing the enemy, reducing message density and making the protocol task‑plausible.",
  "failure_analysis": "The when function incorrectly uses an absolute health threshold of 20.0 while the observed own_health is normalised to max 0.625. This makes health_cond always True, turning the intended sparse communication into a dense all‑to‑all transmission of enemy position and own health on every step. The bug completely invalidates the selective intent of both R1 and R2.",
  "improvement_suggestions": "Replace the health threshold with a normalised value (e.g. o[:,:,33] < 0.2 for 20% of max health) or use max_health from the environment. Also consider making the communicate‑what masking depend on the actual trigger (e.g., health_cond selects health, enemy_cond selects position) rather than sending everything when either condition fires.",
  "replacement_readiness": "not_ready",
  "rollout_grounding_score": 0.5,
  "rule_checks": [
    {
      "counterexample_case_ids": [],
      "observed_trigger_or_edge_rate": 1.0,
      "requirement_hypothesis": "share own_health and enemy relative position when agent is wounded",
      "rule_id": "R1",
      "supporting_case_ids": [
        "train_traj_0000:0",
        "train_traj_0000:13"
      ],
      "threshold_in_observed_range": false,
      "unresolved_questions": [
        "health threshold 20.0 is out of the observed range (0-0.625), making R1 always active"
      ],
      "what_supported": true,
      "when_supported": false,
      "who_supported": true
    },
    {
      "counterexample_case_ids": [],
      "observed_trigger_or_edge_rate": 0.082119,
      "requirement_hypothesis": "share enemy relative position when enemy is visible",
      "rule_id": "R2",
      "supporting_case_ids": [
        "train_traj_0000:0",
        "train_traj_0000:13"
      ],
      "threshold_in_observed_range": true,
      "unresolved_questions": [
        "R2 condition (enemy_0_available==1) is correct but overshadowed by always‑true R1"
      ],
      "what_supported": true,
      "when_supported": true,
      "who_supported": true
    }
  ],
  "score": 0.3,
  "usage": {
    "completion_tokens": 3770,
    "prompt_tokens": 14108,
    "total_tokens": 17878
  },
  "what_score": 0.5,
  "when_score": 0.0,
  "who_score": 1.0
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "5z_vs_1ul",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_122837/iteration/5z_vs_1ul/20260712_122837/candidates/iter_000/comm_init.py",
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
  "message_nonzero_rate": 0.0625,
  "message_abs_mean": 0.0625,
  "active_sender_what_coverage_mean": 0.0625,
  "active_sender_what_coverage_min": 0.0625,
  "active_sender_count": 755,
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": 0.264106,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.159831,
          "33": 0.0
        },
        {
          "6": -0.104275,
          "7": 0.159831,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.625
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.625
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.230659,
          "7": 0.294759,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.163656,
          "7": 0.161051,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.625
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.625
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.625
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.625
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": -0.097059,
          "7": -0.219862,
          "33": 0.0
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
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
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ],
        [
          6,
          7,
          33
        ]
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0625,
        0.0625
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        },
        {
          "6": 0.0,
          "7": 0.0,
          "33": 0.0
        }
      ]
    }
  ]
}

Recent trials:
[
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_122837/iteration/5z_vs_1ul/20260712_122837/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-12T12:32:12+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_122837/iteration/5z_vs_1ul/20260712_122837/candidates/iter_000/comm_init.py",
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
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_122837/iteration/5z_vs_1ul/20260712_122837/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 48,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-12T12:32:12+00:00",
    "valid": true,
    "when_edge_rate": 1.0,
    "who_edge_rate": 1.0
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_122837/iteration/5z_vs_1ul/20260712_122837/candidates/iter_000/comm_init.py",
    "failure_analysis": "The when function incorrectly uses an absolute health threshold of 20.0 while the observed own_health is normalised to max 0.625. This makes health_cond always True, turning the intended sparse communication into a dense all‑to‑all transmission of enemy position and own health on every step. The bug completely invalidates the selective intent of both R1 and R2.",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 48,
    "next_hypothesis": "Replace the health threshold with a normalised value (e.g. o[:,:,33] < 0.2 for 20% of max health) or use max_health from the environment. Also consider making the communicate‑what masking depend on the actual trigger (e.g., health_cond selects health, enemy_cond selects position) rather than sending everything when either condition fires.",
    "rollout_grounding_score": 0.5,
    "score": 0.3,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-12T12:33:03+00:00",
    "valid": true,
    "what_score": 0.5,
    "when_score": 0.0,
    "who_score": 1.0
  }
]

Current code:
```python
import torch


def message_design_instruction():
    """
    Returns a natural language description of the designed communication protocol.
    This function is required by the candidate validation process.
    """
    return (
        "Communication rules:\n"
        "R1 (health alert): when an agent's own_health < 20 (normalized units), "
        "it sends its own_health (33), enemy_0_rel_x (6), and enemy_0_rel_y (7) to all other agents.\n"
        "R2 (enemy position broadcast): when an agent detects an enemy (enemy_0_available == 1), "
        "it sends enemy_0_rel_x (6) and enemy_0_rel_y (7) to all other agents."
    )


def communication_who(o):
    # RULE R1, R2: all agents can send to all other agents (off-diagonal only)
    # sender_group: G1 (all agents), receiver_selector: all_other_agents
    batch_size, n_agents, obs_dim = o.shape
    who = (1 - torch.eye(n_agents, device=o.device, dtype=o.dtype)).unsqueeze(0).expand(batch_size, -1, -1)
    return who


def communication_when(o):
    # RULE R1 (health alert): triggered when own_health < 20.0
    # RULE R2 (enemy position broadcast): triggered when enemy_0_available == 1.0
    health_cond = (o[:, :, 33] < 20.0)      # [batch, n_agents]
    enemy_cond = (o[:, :, 4] == 1.0)        # [batch, n_agents]
    when = (health_cond | enemy_cond).float()  # sender‑side condition mask
    batch_size, n_agents, _ = o.shape
    when = when.unsqueeze(1).expand(-1, n_agents, -1)   # [batch, n_receivers, n_senders]
    # zero out self-communication diagonal
    when = when * (1 - torch.eye(n_agents, device=o.device, dtype=when.dtype).unsqueeze(0))
    return when


def communication_what(o):
    # RULE R1: wounded agent sends own_health (33), enemy_0_rel_x (6), enemy_0_rel_y (7)
    # RULE R2: agent seeing enemy sends enemy_0_rel_x (6), enemy_0_rel_y (7)
    health_cond = (o[:, :, 33] < 20.0)      # [batch, n_agents]
    enemy_cond = (o[:, :, 4] == 1.0)        # [batch, n_agents]

    send_health = health_cond                # health only sent when wounded
    send_enemy_pos = health_cond | enemy_cond # enemy position sent by either rule

    what_mask = torch.zeros_like(o)
    what_mask[:, :, 33] = send_health.float()
    what_mask[:, :, 6]  = send_enemy_pos.float()
    what_mask[:, :, 7]  = send_enemy_pos.float()
    return what_mask

```

Return JSON with keys:
- Evaluation
- Missing_Information_Hypothesis
- Improvement_Suggestions
- Target_Functions
- Target_Rule_IDs
Do not use downstream RL win-rate as feedback. Focus on rollout-grounded who/when/what critique only.
