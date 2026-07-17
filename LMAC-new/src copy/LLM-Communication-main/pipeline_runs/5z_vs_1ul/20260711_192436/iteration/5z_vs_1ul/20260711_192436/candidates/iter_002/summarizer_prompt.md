## system

You analyze LLM-judged failures for LMAC communication policies. Return one compact JSON object only.

## user

Analyze the LLM judge result for map `5z_vs_1ul` and propose the next communication-code revision.

Judge summary:
{
  "accepted": false,
  "blocking_failures": [
    {
      "evidence": "when_edge_rate is 0.897 in rollout. Evidence cases (e.g., train_traj_0000:27, :40, :54) show own_health = 0.0 for multiple agents, which triggers condition_low because 0.0 < 0.2 is always true. This makes the when-matrix nearly always-on, defeating the intended sparse event-driven communication.",
      "revision_target": "when",
      "type": "when"
    }
  ],
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_001/comm_init.py",
  "dry_run": false,
  "evidence_case_ids": [
    "train_traj_0000:0",
    "train_traj_0000:27",
    "train_traj_0000:40",
    "train_traj_0000:54"
  ],
  "expected_effect": "Reducing the trigger to true distress events (when hull damage is non-zero and shield is low) will drastically lower the when_edge_rate, making communication sparse and more informative. This should make the strategy both a better teacher for a learnable selector and a more efficient fixed communication policy.",
  "failure_analysis": "The when-condition uses own_health < 0.2 as a trigger. In the rollout observations, own_health is zero for the majority of timesteps (nonzero_rate only 0.103, mean 0.065, max 0.625). Because health values are often exactly zero, the condition is true almost continuously for all agents, resulting in an always-on communication pattern. This contradicts the stated goal of sending messages only in distress or when the enemy is visible. The what-component correctly switches between two compact message sets, but the near-universal activation of trigger_a makes the switching logic ineffective and degenerates the strategy into a static mask. The who-matrix is acceptable but reinforces the excessive traffic.",
  "improvement_suggestions": "1. Replace the health threshold condition with something that reflects actual hull damage, e.g., `own_health > 0.0` (meaning the agent has taken hull damage, not full health). Optionally combine with shield status: `own_health > 0.0 and own_shield < 0.5` to indicate real distress. 2. Consider using `enemy_0_available > 0.5` as the primary trigger, and only add health-based distress when the enemy is not visible or when the agent is exposed. 3. Introduce a time-decay or event-based hysteresis to avoid rapid toggling if needed. 4. After fixing the trigger, verify that the dynamic what-mask correctly toggles between set A (with shield) and set B (enemy info only) as intended, and that the resulting when_edge_rate drops significantly.",
  "replacement_readiness": "not_ready",
  "rollout_grounding_score": 0.5,
  "score": 0.45,
  "usage": {
    "completion_tokens": 3610,
    "prompt_tokens": 17014,
    "total_tokens": 20624
  },
  "what_score": 0.65,
  "when_score": 0.2,
  "who_score": 0.6
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "5z_vs_1ul",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_001/comm_init.py",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/5z_vs_1ul/train_traj_0000.pkl"
  ],
  "transitions": 151,
  "n_agents": 5,
  "rollout_obs_dim": 48,
  "message_dim": 48,
  "matrix_edge_rate": 0.8966887417218543,
  "who_edge_rate": 1.0,
  "when_edge_rate": 0.8966887417218543,
  "message_nonzero_rate": 0.13076710816777043,
  "message_abs_mean": 0.13076710816777043,
  "matrix_min": 0.0,
  "matrix_max": 1.0,
  "risk_flags": [],
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
          1,
          0
        ],
        [
          1,
          2
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
        [],
        []
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
        {},
        {}
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
          1,
          0
        ],
        [
          1,
          2
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
        [],
        []
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
        {},
        {}
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
          1,
          0
        ],
        [
          1,
          2
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
        [],
        []
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
        {},
        {}
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
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 48,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-11T19:25:25+00:00",
    "valid": true,
    "when_edge_rate": 1.0,
    "who_edge_rate": 1.0
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_000/comm_init.py",
    "failure_analysis": "The when‑component is designed to trigger only for low‑health or enemy‑visible conditions, but the health threshold `20.0` is incompatible with the actual observation scale (normalized health ≤ 0.625). Consequently, every agent triggers communication at every timestep, yielding a fully‑connected, always‑active communication graph. This contradicts the stated intention of sparse, event‑driven messaging and fails to provide selective supervision. The what‑component selects a reasonable set of features (enemy info + own health/shield), but because the broken trigger forces the mask to be constant, it cannot demonstrate the intended dynamic switch between message sets. The who‑matrix, while simple, is acceptable in itself, but its interaction with the faulty when‑logic makes the overall strategy an inappropriate teacher for a learnable selector.",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 48,
    "next_hypothesis": "1. Replace the health threshold with a value consistent with the rollout feature statistics—e.g., `own_health < 0.2`—so that only genuinely damaged agents send messages.  2. Optionally, tighten the who‑matrix by limiting communication to allies that are visible (using the ally visibility features) to further reduce useless traffic.  3. Keep the enemy‑visible trigger (`enemy_0_available > 0.5`) as is, but ensure it does not get overridden by an always‑true health condition.  4. After fixing the threshold, verify that the dynamic what‑mask correctly toggles between set A and set B according to the new trigger logic.",
    "rollout_grounding_score": 0.3,
    "score": 0.25,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-11T19:26:29+00:00",
    "valid": true,
    "what_score": 0.7,
    "when_score": 0.1,
    "who_score": 0.6
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-11T19:27:03+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_001/comm_init.py",
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
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 0.8966887417218543,
    "message_dim": 48,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-11T19:27:03+00:00",
    "valid": true,
    "when_edge_rate": 0.8966887417218543,
    "who_edge_rate": 1.0
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_001/comm_init.py",
    "failure_analysis": "The when-condition uses own_health < 0.2 as a trigger. In the rollout observations, own_health is zero for the majority of timesteps (nonzero_rate only 0.103, mean 0.065, max 0.625). Because health values are often exactly zero, the condition is true almost continuously for all agents, resulting in an always-on communication pattern. This contradicts the stated goal of sending messages only in distress or when the enemy is visible. The what-component correctly switches between two compact message sets, but the near-universal activation of trigger_a makes the switching logic ineffective and degenerates the strategy into a static mask. The who-matrix is acceptable but reinforces the excessive traffic.",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 48,
    "next_hypothesis": "1. Replace the health threshold condition with something that reflects actual hull damage, e.g., `own_health > 0.0` (meaning the agent has taken hull damage, not full health). Optionally combine with shield status: `own_health > 0.0 and own_shield < 0.5` to indicate real distress. 2. Consider using `enemy_0_available > 0.5` as the primary trigger, and only add health-based distress when the enemy is not visible or when the agent is exposed. 3. Introduce a time-decay or event-based hysteresis to avoid rapid toggling if needed. 4. After fixing the trigger, verify that the dynamic what-mask correctly toggles between set A (with shield) and set B (enemy info only) as intended, and that the resulting when_edge_rate drops significantly.",
    "rollout_grounding_score": 0.5,
    "score": 0.45,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-11T19:28:02+00:00",
    "valid": true,
    "what_score": 0.65,
    "when_score": 0.2,
    "who_score": 0.6
  }
]

Current code:
```python
import torch

def message_design_instruction():
    return (
        "WHO: Each Zealot broadcasts to all other Zealots (no self-communication). "
        "WHEN: A sender sends a message if (a) own_health < 0.2 (low health distress) "
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
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    who_matrix = who_matrix - mask_self
    # Optional: further gating by ally visibility can be added here,
    # but current simple all-to-all is kept for high coordination.
    return torch.clamp(who_matrix, 0.0, 1.0)


def communication_when(o):
    batch_size, n_agents, obs_dim = o.shape
    # own_health at index 33, enemy_0_available at index 4
    own_health = o[..., 33:34] if obs_dim > 33 else torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = o[..., 4:5] if obs_dim > 4 else torch.zeros(batch_size, n_agents, 1, device=o.device)

    # Normalized threshold: max health is 0.625, so 0.2 means ~32% health.
    condition_low = (own_health < 0.2).float()
    condition_enemy = (enemy_available > 0.5).float()
    sender_trigger = torch.max(condition_low, condition_enemy).squeeze(-1)  # (batch, n_agents)

    when_matrix = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1)  # (batch, n_agents, n_agents)
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    when_matrix = when_matrix * (1.0 - mask_self)
    return torch.clamp(when_matrix, 0.0, 1.0)


def communication_what(o):
    batch_size, n_agents, obs_dim = o.shape

    # Extract relevant features with fallback
    own_health = o[..., 33:34] if obs_dim > 33 else torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = o[..., 4:5] if obs_dim > 4 else torch.zeros(batch_size, n_agents, 1, device=o.device)

    # Corrected threshold
    condition_low = (own_health < 0.2).float()
    condition_enemy = (enemy_available > 0.5).float()

    # trigger_a: low health (always sends set a)
    # trigger_b: healthy AND enemy visible (sends set b)
    trigger_a = condition_low
    trigger_b = (1.0 - condition_low) * condition_enemy

    # Define desired feature index sets (as in message_design_instruction)
    indices_a = torch.tensor([4, 5, 6, 7, 8, 33, 34], dtype=torch.long, device=o.device)
    indices_b = torch.tensor([4, 5, 6, 7, 8, 33], dtype=torch.long, device=o.device)

    # Filter out-of-range indices (safety)
    valid_a = indices_a[indices_a < obs_dim]
    valid_b = indices_b[indices_b < obs_dim]

    # Build binary masks for the two sets
    mask_a = torch.zeros(1, 1, obs_dim, device=o.device)
    mask_b = torch.zeros(1, 1, obs_dim, device=o.device)
    if valid_a.numel() > 0:
        mask_a[..., valid_a] = 1.0
    if valid_b.numel() > 0:
        mask_b[..., valid_b] = 1.0

    # Combine: if trigger_a active -> mask_a; if trigger_b active -> mask_b; else zeros
    what = trigger_a * mask_a + trigger_b * mask_b
    return torch.clamp(what, 0.0, 1.0)

```

Return JSON with keys:
- Evaluation
- Missing_Information_Hypothesis
- Improvement_Suggestions
- Target_Functions
Do not use downstream RL win-rate as feedback. Focus on rollout-grounded who/when/what critique only.
