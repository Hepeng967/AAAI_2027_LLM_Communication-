## system

You are an expert MARL communication-policy judge. Evaluate the generated policy only from the task spec, code, and interface validation. Return one JSON object only.

## user

Evaluate this pure LLM-generated LMAC communication strategy for SMAC map `5z_vs_1ul`.

Research goal:
- We are testing the capability boundary of LLM-designed communication.
- Do NOT use DRC, decision_sufficient, causally_useful, downstream RL win-rate, or hidden/global state.
- Judge whether the policy gives a plausible pure communication strategy for who, when, and what.

Map spec:
{
  "n_agents": 5,
  "obs_dim": 48,
  "time_seq": 10
}

Rollout-backed LMAC observation alignment:
{
  "map_name": "5z_vs_1ul",
  "rollout_root": "/data/hp/LLM_Communication/LMAC-new/data",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/5z_vs_1ul/train_traj_0000.pkl"
  ],
  "available": true,
  "n_agents": 5,
  "raw_obs_dim": 36,
  "rollout_obs_dim": 48,
  "documented_obs_dim": 35,
  "extra_obs_dim": 1,
  "episodes": 1,
  "transitions": 151,
  "seq_lengths": [
    151
  ],
  "action_dim": 7,
  "agent_types": [
    "zealot",
    "zealot",
    "zealot",
    "zealot",
    "zealot"
  ],
  "feature_index": {
    "move_north": [
      0,
      1
    ],
    "move_south": [
      1,
      2
    ],
    "move_east": [
      2,
      3
    ],
    "move_west": [
      3,
      4
    ],
    "enemy_0_available": [
      4,
      5
    ],
    "enemy_0_distance": [
      5,
      6
    ],
    "enemy_0_rel_x": [
      6,
      7
    ],
    "enemy_0_rel_y": [
      7,
      8
    ],
    "enemy_0_health": [
      8,
      9
    ],
    "ally_0_visible": [
      9,
      10
    ],
    "ally_0_distance": [
      10,
      11
    ],
    "ally_0_rel_x": [
      11,
      12
    ],
    "ally_0_rel_y": [
      12,
      13
    ],
    "ally_0_health": [
      13,
      14
    ],
    "ally_0_shield": [
      14,
      15
    ],
    "ally_1_visible": [
      15,
      16
    ],
    "ally_1_distance": [
      16,
      17
    ],
    "ally_1_rel_x": [
      17,
      18
    ],
    "ally_1_rel_y": [
      18,
      19
    ],
    "ally_1_health": [
      19,
      20
    ],
    "ally_1_shield": [
      20,
      21
    ],
    "ally_2_visible": [
      21,
      22
    ],
    "ally_2_distance": [
      22,
      23
    ],
    "ally_2_rel_x": [
      23,
      24
    ],
    "ally_2_rel_y": [
      24,
      25
    ],
    "ally_2_health": [
      25,
      26
    ],
    "ally_2_shield": [
      26,
      27
    ],
    "ally_3_visible": [
      27,
      28
    ],
    "ally_3_distance": [
      28,
      29
    ],
    "ally_3_rel_x": [
      29,
      30
    ],
    "ally_3_rel_y": [
      30,
      31
    ],
    "ally_3_health": [
      31,
      32
    ],
    "ally_3_shield": [
      32,
      33
    ],
    "own_health": [
      33,
      34
    ],
    "own_shield": [
      34,
      35
    ],
    "lmac_extra_35": [
      35,
      36
    ],
    "previous_action_0": [
      36,
      37
    ],
    "previous_action_1": [
      37,
      38
    ],
    "previous_action_2": [
      38,
      39
    ],
    "previous_action_3": [
      39,
      40
    ],
    "previous_action_4": [
      40,
      41
    ],
    "previous_action_5": [
      41,
      42
    ],
    "previous_action_6": [
      42,
      43
    ],
    "agent_id_0": [
      43,
      44
    ],
    "agent_id_1": [
      44,
      45
    ],
    "agent_id_2": [
      45,
      46
    ],
    "agent_id_3": [
      46,
      47
    ],
    "agent_id_4": [
      47,
      48
    ]
  },
  "feature_statistics": {
    "move_north": {
      "index": 0,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.32053,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.32053
    },
    "move_south": {
      "index": 1,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.377483,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.377483
    },
    "move_east": {
      "index": 2,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.337748,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.337748
    },
    "move_west": {
      "index": 3,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.381457,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.381457
    },
    "enemy_0_available": {
      "index": 4,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.082119,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.082119
    },
    "enemy_0_distance": {
      "index": 5,
      "min": 0.0,
      "max": 0.954298,
      "mean": 0.029114,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.236573,
      "nonzero_rate": 0.088742
    },
    "enemy_0_rel_x": {
      "index": 6,
      "min": -0.540012,
      "max": 0.251112,
      "mean": 0.000636,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.030897,
      "nonzero_rate": 0.084768
    },
    "enemy_0_rel_y": {
      "index": 7,
      "min": -0.786811,
      "max": 0.536947,
      "mean": 0.007022,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.159831,
      "nonzero_rate": 0.088742
    },
    "enemy_0_health": {
      "index": 8,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.086093,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.964834,
      "nonzero_rate": 0.088742
    },
    "ally_0_visible": {
      "index": 9,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_0_distance": {
      "index": 10,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.050331,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.299988,
      "nonzero_rate": 0.050331
    },
    "ally_0_rel_x": {
      "index": 11,
      "min": 0.0,
      "max": 0.501021,
      "mean": 0.014716,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.031281,
      "nonzero_rate": 0.050331
    },
    "ally_0_rel_y": {
      "index": 12,
      "min": -0.354275,
      "max": 0.138129,
      "mean": -0.004254,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.047682
    },
    "ally_0_health": {
      "index": 13,
      "min": -0.428521,
      "max": 0.428521,
      "mean": -0.004761,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.050331
    },
    "ally_0_shield": {
      "index": 14,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.043535,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.007341,
      "nonzero_rate": 0.050331
    },
    "ally_1_visible": {
      "index": 15,
      "min": 0.0,
      "max": 0.625,
      "mean": 0.014686,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.039735
    },
    "ally_1_distance": {
      "index": 16,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.050331,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.299988,
      "nonzero_rate": 0.050331
    },
    "ally_1_rel_x": {
      "index": 17,
      "min": 0.0,
      "max": 0.501021,
      "mean": 0.014017,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.031281,
      "nonzero_rate": 0.050331
    },
    "ally_1_rel_y": {
      "index": 18,
      "min": -0.479275,
      "max": 0.479275,
      "mean": 0.004254,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.050331
    },
    "ally_1_health": {
      "index": 19,
      "min": -0.186659,
      "max": 0.383952,
      "mean": 0.004761,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.037086
    },
    "ally_1_shield": {
      "index": 20,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.040188,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.007341,
      "nonzero_rate": 0.050331
    },
    "ally_2_visible": {
      "index": 21,
      "min": 0.0,
      "max": 0.625,
      "mean": 0.01393,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027815
    },
    "ally_2_distance": {
      "index": 22,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_2_rel_x": {
      "index": 23,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_2_rel_y": {
      "index": 24,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_2_health": {
      "index": 25,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_2_shield": {
      "index": 26,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_3_visible": {
      "index": 27,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_3_distance": {
      "index": 28,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.103311,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.103311
    },
    "ally_3_rel_x": {
      "index": 29,
      "min": 0.0,
      "max": 0.890059,
      "mean": 0.05074,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.479275,
      "nonzero_rate": 0.103311
    },
    "ally_3_rel_y": {
      "index": 30,
      "min": -0.75,
      "max": 0.75,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.07947
    },
    "ally_3_health": {
      "index": 31,
      "min": -0.604275,
      "max": 0.604275,
      "mean": 0.0,
      "p05": -0.141775,
      "p50": 0.0,
      "p95": 0.141774,
      "nonzero_rate": 0.103311
    },
    "ally_3_shield": {
      "index": 32,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.103311,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.103311
    },
    "own_health": {
      "index": 33,
      "min": 0.0,
      "max": 0.625,
      "mean": 0.06457,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.625,
      "nonzero_rate": 0.103311
    },
    "own_shield": {
      "index": 34,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.362889,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.381457
    },
    "lmac_extra_35": {
      "index": 35,
      "min": 0.0,
      "max": 0.625,
      "mean": 0.205765,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.625,
      "nonzero_rate": 0.34702
    },
    "previous_action_0": {
      "index": 36,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.613245,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.613245
    },
    "previous_action_1": {
      "index": 37,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.075497,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.075497
    },
    "previous_action_2": {
      "index": 38,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.06755,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.06755
    },
    "previous_action_3": {
      "index": 39,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.070199,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.070199
    },
    "previous_action_4": {
      "index": 40,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.066225,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.066225
    },
    "previous_action_5": {
      "index": 41,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.083444,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.083444
    },
    "previous_action_6": {
      "index": 42,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.017219,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017219
    },
    "agent_id_0": {
      "index": 43,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.2,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.2
    },
    "agent_id_1": {
      "index": 44,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.2,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.2
    },
    "agent_id_2": {
      "index": 45,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.2,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.2
    },
    "agent_id_3": {
      "index": 46,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.2,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.2
    },
    "agent_id_4": {
      "index": 47,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.2,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.2
    }
  },
  "alignment_note": "rollout_obs_dim is exactly the RL communication input: raw observation + previous-action one-hot + agent-id one-hot. Feature positions are identical in offline evaluation and RL training."
}

Interface validation:
{
  "valid": true,
  "map_name": "5z_vs_1ul",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_122837/iteration/5z_vs_1ul/20260712_122837/candidates/iter_001/comm_init.py",
  "validation_obs_source": "rollout",
  "validation_obs_dim": 48,
  "documented_obs_dim": 35,
  "message_dim": 48,
  "matrix_edge_rate": 1.0,
  "who_edge_rate": 1.0,
  "when_edge_rate": 1.0,
  "what_dim": 48,
  "matrix_min": 0.0,
  "matrix_max": 1.0
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "5z_vs_1ul",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_122837/iteration/5z_vs_1ul/20260712_122837/candidates/iter_001/comm_init.py",
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
  "message_nonzero_rate": 0.056043046357615894,
  "message_abs_mean": 0.056043046357615894,
  "active_sender_what_coverage_mean": 0.0625,
  "active_sender_what_coverage_min": 0.0625,
  "active_sender_count": 677,
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
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0,
        0.0
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
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0,
        0.0
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
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0625,
        0.0625,
        0.0625,
        0.0,
        0.0
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
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_122837/iteration/5z_vs_1ul/20260712_122837/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-12T12:34:00+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_122837/iteration/5z_vs_1ul/20260712_122837/candidates/iter_001/comm_init.py",
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
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260712_122837/iteration/5z_vs_1ul/20260712_122837/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 0.8966887417218543,
    "message_dim": 48,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-12T12:34:00+00:00",
    "valid": true,
    "when_edge_rate": 0.8966887417218543,
    "who_edge_rate": 1.0
  }
]

Candidate code:
```python
import torch


def message_design_instruction():
    """
    Returns a natural language description of the designed communication protocol.
    This function is required by the candidate validation process.
    """
    return (
        "Communication rules:\n"
        "R1 (health alert): when an agent's own_health < 0.2 (normalized units), "
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
    # RULE R1 (health alert): triggered when own_health < 0.2
    # RULE R2 (enemy position broadcast): triggered when enemy_0_available == 1.0
    health_cond = (o[:, :, 33] < 0.2)      # [batch, n_agents]
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
    health_cond = (o[:, :, 33] < 0.2)      # [batch, n_agents]
    enemy_cond = (o[:, :, 4] == 1.0)        # [batch, n_agents]

    send_health = health_cond                # health only sent when wounded
    send_enemy_pos = health_cond | enemy_cond # enemy position sent by either rule

    what_mask = torch.zeros_like(o)
    what_mask[:, :, 33] = send_health.float()
    what_mask[:, :, 6]  = send_enemy_pos.float()
    what_mask[:, :, 7]  = send_enemy_pos.float()
    return what_mask

```

Return strict JSON with keys:
{
  "accepted": bool,
  "score": float between 0 and 1,
  "who_score": float between 0 and 1,
  "when_score": float between 0 and 1,
  "what_score": float between 0 and 1,
  "rollout_grounding_score": float between 0 and 1,
  "replacement_readiness": "direct_teacher"|"student_supervision_ready"|"not_ready",
  "blocking_failures": [{"type": "short_name", "evidence": "specific rollout/code evidence", "revision_target": "who|when|what"}],
  "rule_checks": [{
    "rule_id": "R1 or a deterministic inferred ID if legacy code has no marker",
    "requirement_hypothesis": "information need served by this rule",
    "who_supported": true,
    "when_supported": true,
    "what_supported": true,
    "threshold_in_observed_range": true,
    "observed_trigger_or_edge_rate": 0.0,
    "supporting_case_ids": [],
    "counterexample_case_ids": [],
    "unresolved_questions": []
  }],
  "cross_rule_check": {
    "who_when_what_consistent": true,
    "conflicts_or_uncovered_requirements": []
  },
  "evidence_case_ids": ["case ids used to support the verdict"],
  "failure_analysis": "specific critique of missing or redundant who/when/what logic",
  "improvement_suggestions": "concrete code-level changes for the next revision",
  "expected_effect": "why these changes should improve coordination"
}

Acceptance guideline:
- accepted=true only if who, when, and what are all task-plausible and compact.
- accepted=true requires blocking_failures=[]; any always-on condition caused by
  an out-of-scale threshold, missing runtime field, interface inefficiency, or
  contradiction between analysis and code is blocking and requires revision.
- Derive conclusions from rollout feature statistics and evidence cases. Do not
  treat an agent id or feature index as required unless the task description and
  actual runtime observations support it.
- The policy must be grounded in the offline rollout statistics, not only generic SMAC knowledge.
- Favor strategies that could directly replace a fixed communication module and also supervise a learnable selector.
- Penalize all-to-all always-on matrices unless the task truly requires them.
- Penalize messages that merely copy all observations without compact task logic.
- First inventory every `# RULE <rule_id>` represented in the code. For legacy
  code without markers, infer stable IDs R1, R2, ... and state that they were inferred.
- Complete one rule_checks entry per inventoried rule. Explicitly look for
  counterexamples before accepting; a prose claim contradicted by a cited case or
  by the code is a blocking failure.
- Sparse or dense communication is not independently correct or incorrect. Treat
  communication rates as evidence and justify the verdict from task needs.
