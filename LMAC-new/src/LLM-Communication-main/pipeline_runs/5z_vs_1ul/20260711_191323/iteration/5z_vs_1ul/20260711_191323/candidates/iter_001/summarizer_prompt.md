## system

You analyze LLM-judged failures for LMAC communication policies. Return one compact JSON object only.

## user

Analyze the LLM judge result for map `5z_vs_1ul` and propose the next communication-code revision.

Judge summary:
{
  "accepted": false,
  "blocking_failures": [
    {
      "evidence": "The health threshold `own_health < 20.0` uses an absolute value 20, but `own_health` is normalised to [0, 0.625] in the rollout (max=0.625, p95=0.625). This makes the condition always true for all agents, turning `when` into an always‑on matrix (except self). The rollout evaluation shows `when_edge_rate=1.0` and risk flag `nearly_all_to_all_edges_on_rollout`, confirming the behaviour.",
      "revision_target": "when",
      "type": "when"
    }
  ],
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_000/comm_init.py",
  "dry_run": false,
  "evidence_case_ids": [
    "train_traj_0000:0",
    "train_traj_0000:13",
    "train_traj_0000:27"
  ],
  "expected_effect": "Correcting the threshold will restore the intended conditional communication: messages will be sent only when an agent is critically hurt or sees the enemy. This reduces unnecessary channel usage, focuses communication on critical events, and provides a meaningful test of LLM‑designed sparsity and content selection.",
  "failure_analysis": "The intended strategy introduces a low‑health distress condition, but the implementation uses a hard‑coded threshold of 20. Because all observed `own_health` values are ≤ 0.625, the comparison `own_health < 20.0` always yields `True`. Consequently `sender_trigger` is 1 for every agent at every timestep, producing an unconditional all‑to‑all broadcast. This contradicts the design instruction ('send … if low health or enemy visible') and eliminates any sparsity benefit. The `what` function consequently always selects the ‘trigger a’ feature set, never using ‘trigger b’. The constant broadcast may be acceptable for such a small map, but it fails the conditional‑communication capability test and is flagged as a blocking bug.",
  "improvement_suggestions": "Replace the health threshold with a normalised value grounded in the rollout statistics, e.g., `condition_low_health = (own_health < 0.1).float()` (≤10 % of observed maximum health). Optionally include shield in the distress trigger or in the message. If ally partial visibility is important, consider adding the nearest ally’s state to `what`. Ensure that future iterations maintain the intended conditional logic: the `when` matrix must reflect the OR of a correctly scaled low‑health signal and the enemy‑visible signal.",
  "replacement_readiness": "not_ready",
  "rollout_grounding_score": 0.3,
  "score": 0.3,
  "usage": {
    "completion_tokens": 4197,
    "prompt_tokens": 16746,
    "total_tokens": 20943
  },
  "what_score": 0.6,
  "when_score": 0.1,
  "who_score": 1.0
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "5z_vs_1ul",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_000/comm_init.py",
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
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-11T19:14:13+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_000/comm_init.py",
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
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 48,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-11T19:14:13+00:00",
    "valid": true,
    "when_edge_rate": 1.0,
    "who_edge_rate": 1.0
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_000/comm_init.py",
    "failure_analysis": "The intended strategy introduces a low‑health distress condition, but the implementation uses a hard‑coded threshold of 20. Because all observed `own_health` values are ≤ 0.625, the comparison `own_health < 20.0` always yields `True`. Consequently `sender_trigger` is 1 for every agent at every timestep, producing an unconditional all‑to‑all broadcast. This contradicts the design instruction ('send … if low health or enemy visible') and eliminates any sparsity benefit. The `what` function consequently always selects the ‘trigger a’ feature set, never using ‘trigger b’. The constant broadcast may be acceptable for such a small map, but it fails the conditional‑communication capability test and is flagged as a blocking bug.",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 48,
    "next_hypothesis": "Replace the health threshold with a normalised value grounded in the rollout statistics, e.g., `condition_low_health = (own_health < 0.1).float()` (≤10 % of observed maximum health). Optionally include shield in the distress trigger or in the message. If ally partial visibility is important, consider adding the nearest ally’s state to `what`. Ensure that future iterations maintain the intended conditional logic: the `when` matrix must reflect the OR of a correctly scaled low‑health signal and the enemy‑visible signal.",
    "rollout_grounding_score": 0.3,
    "score": 0.3,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-11T19:15:25+00:00",
    "valid": true,
    "what_score": 0.6,
    "when_score": 0.1,
    "who_score": 1.0
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

    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    condition_low = (own_health < 20.0).float()          # (batch, n_agents, 1)
    condition_enemy = (enemy_available > 0.5).float()

    # Trigger a: low health
    trigger_a = condition_low
    # Trigger b: healthy AND enemy visible
    trigger_b = (1.0 - condition_low) * condition_enemy

    # Define indices sets
    indices_a = [4, 5, 6, 7, 8, 33, 34]
    indices_b = [4, 5, 6, 7, 8, 33]

    indices_a_t = torch.tensor(indices_a, dtype=torch.long, device=o.device)
    indices_b_t = torch.tensor(indices_b, dtype=torch.long, device=o.device)

    valid_a = indices_a_t < obs_dim
    valid_b = indices_b_t < obs_dim

    mask_a = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)
    if valid_a.any():
        mask_a[:, :, indices_a_t[valid_a]] = 1.0

    mask_b = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)
    if valid_b.any():
        mask_b[:, :, indices_b_t[valid_b]] = 1.0

    # Combine based on triggers
    what = trigger_a * mask_a + trigger_b * mask_b
    what = torch.clamp(what, 0.0, 1.0)
    return what

```

Return JSON with keys:
- Evaluation
- Missing_Information_Hypothesis
- Improvement_Suggestions
- Target_Functions
Do not use downstream RL win-rate as feedback. Focus on rollout-grounded who/when/what critique only.
