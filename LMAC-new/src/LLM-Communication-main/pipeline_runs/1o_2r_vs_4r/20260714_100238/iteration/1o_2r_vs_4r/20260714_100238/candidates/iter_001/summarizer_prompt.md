## system

You analyze LLM-judged failures for LMAC communication policies. Return one compact JSON object only.

## user

Analyze the LLM judge result for map `1o_2r_vs_4r` and propose the next communication-code revision.

Judge summary:
{
  "accepted": false,
  "blocking_failures": [
    {
      "evidence": "Code uses indices 12, 20, 28 for enemy availability checks and blocks 13-19, 21-27, 29-35 for what content. According to the official feature_index from the rollout data, enemy_1_available is at index 11, enemy_2_available at index 18, enemy_3_available at index 25. The what mask consequently misses distance features for enemies 1-3 (e.g., enemy_1_distance at index 12 is omitted, index 18 is wrongly included as enemy_2_available). This misalignment prevents the policy from reliably extracting the intended enemy features.",
      "revision_target": "what",
      "type": "feature_misalignment"
    },
    {
      "evidence": "{\"who_when_what_consistent\": false, \"conflicts_or_uncovered_requirements\": [\"All enemy-feature rules share the same misalignment, so the communicated content is not the actual enemy data. The who (static overser→roaches) is consistent but the when/what coordinates are broken.\"]}",
      "revision_target": "who|when|what",
      "type": "cross_rule_inconsistency"
    }
  ],
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260714_100238/iteration/1o_2r_vs_4r/20260714_100238/candidates/iter_000/comm_init.py",
  "cross_rule_check": {
    "conflicts_or_uncovered_requirements": [
      "All enemy-feature rules share the same misalignment, so the communicated content is not the actual enemy data. The who (static overser→roaches) is consistent but the when/what coordinates are broken."
    ],
    "who_when_what_consistent": false
  },
  "dry_run": false,
  "evidence_case_ids": [
    "train_traj_0000:0",
    "train_traj_0000:4",
    "train_traj_0000:8",
    "train_traj_0000:13",
    "train_traj_0000:17",
    "train_traj_0000:22",
    "train_traj_0000:26",
    "train_traj_0000:31",
    "train_traj_0000:35",
    "train_traj_0000:40",
    "train_traj_0000:44",
    "train_traj_0000:49"
  ],
  "expected_effect": "Fixing the indices will ensure that only genuinely visible enemy data is sent, and the message content faithfully represents the enemy positions, health, and types. This will allow the roaches to make informed decisions based on true enemy state, improving coordination.",
  "failure_analysis": "The policy’s intent (overseer reports visible enemy attributes to roaches) is plausible, but the implementation misaligns observation indices for enemy availability and feature blocks for enemies 1–3. As a result, the when condition uses incorrect proxy features (e.g., distance instead of availability) and the what mask includes wrong or missing elements. Even though the rollout evaluation shows non‑zero communication, the conveyed information does not match the intended enemy data, making the policy unreliable for coordinating with actual enemy observations.",
  "improvement_suggestions": "Correct the availability checks to indices 11, 18, 25 (enemy_1_available, enemy_2_available, enemy_3_available). Adjust the what blocks to the exact feature ranges: enemy_1 (12–17), enemy_2 (19–24), enemy_3 (26–31). Use the feature_index mapping provided in the rollout alignment to guarantee correctness.",
  "replacement_readiness": "not_ready",
  "rollout_grounding_score": 0.1,
  "rule_checks": [
    {
      "counterexample_case_ids": [],
      "observed_trigger_or_edge_rate": 0.362951,
      "requirement_hypothesis": "Overseer communicates enemy_0 features (distance, relative position, health, type) when enemy_0 is visible.",
      "rule_id": "R1",
      "supporting_case_ids": [
        "train_traj_0000:0"
      ],
      "threshold_in_observed_range": true,
      "unresolved_questions": [
        "Availability check at index 4 is correct for enemy_0, but the what block (5-10) is correct. Therefore R1 works, but the reliance on wrong indices for other enemies makes the overall strategy unreliable."
      ],
      "what_supported": false,
      "when_supported": false,
      "who_supported": true
    },
    {
      "counterexample_case_ids": [
        "train_traj_0000:0"
      ],
      "observed_trigger_or_edge_rate": 0.0,
      "requirement_hypothesis": "Overseer communicates enemy_1 features when enemy_1 is visible.",
      "rule_id": "R2",
      "supporting_case_ids": [],
      "threshold_in_observed_range": false,
      "unresolved_questions": [
        "Availability check uses index 12 (enemy_1_distance) instead of index 11 (enemy_1_available). What block (13-18) misses distance and includes index 18 (enemy_2_available). This rule is non-functional."
      ],
      "what_supported": false,
      "when_supported": false,
      "who_supported": true
    },
    {
      "counterexample_case_ids": [
        "train_traj_0000:0"
      ],
      "observed_trigger_or_edge_rate": 0.0,
      "requirement_hypothesis": "Overseer communicates enemy_2 features when enemy_2 is visible.",
      "rule_id": "R3",
      "supporting_case_ids": [],
      "threshold_in_observed_range": false,
      "unresolved_questions": [
        "Availability check at index 20 (should be 18), what block 21-27 misses distance and rel_x, includes wrong indices. Rule is non-functional."
      ],
      "what_supported": false,
      "when_supported": false,
      "who_supported": true
    },
    {
      "counterexample_case_ids": [
        "train_traj_0000:0"
      ],
      "observed_trigger_or_edge_rate": 0.0,
      "requirement_hypothesis": "Overseer communicates enemy_3 features when enemy_3 is visible.",
      "rule_id": "R4",
      "supporting_case_ids": [],
      "threshold_in_observed_range": false,
      "unresolved_questions": [
        "Availability check at index 28 (should be 25), what block 29-35 misses distance, rel_x, rel_y. Rule is non-functional."
      ],
      "what_supported": false,
      "when_supported": false,
      "who_supported": true
    }
  ],
  "score": 0.25,
  "usage": {
    "completion_tokens": 5316,
    "prompt_tokens": 19872,
    "total_tokens": 25188
  },
  "what_score": 0.1,
  "when_score": 0.5,
  "who_score": 0.9
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "1o_2r_vs_4r",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260714_100238/iteration/1o_2r_vs_4r/20260714_100238/candidates/iter_000/comm_init.py",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0000.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0001.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0002.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0003.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0004.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0005.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0006.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0007.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0008.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0009.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0010.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0011.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0012.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0013.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0014.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0015.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0016.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0017.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0018.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0019.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0020.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0021.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0022.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0023.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0024.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0025.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0026.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0027.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0028.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0029.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0030.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0031.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0032.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0033.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0034.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0035.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0036.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0037.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0038.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0039.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0040.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0041.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0042.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0043.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0044.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0045.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0046.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0047.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0048.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0049.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0050.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0051.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0052.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0053.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0054.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0055.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0056.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0057.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0058.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0059.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_2r_vs_4r/train_traj_0060.pkl"
  ],
  "transitions": 3050,
  "n_agents": 3,
  "rollout_obs_dim": 66,
  "message_dim": 66,
  "matrix_edge_rate": 0.3251366120218579,
  "who_edge_rate": 0.3333333333333333,
  "when_edge_rate": 0.3251366120218579,
  "message_nonzero_rate": 0.1160059612518629,
  "message_abs_mean": 0.1160059612518629,
  "active_sender_what_coverage_mean": 0.3567914392166779,
  "active_sender_what_coverage_min": 0.09090909361839294,
  "active_sender_count": 2975,
  "matrix_min": 0.0,
  "matrix_max": 1.0,
  "risk_flags": [],
  "evidence_cases": [
    {
      "case_id": "train_traj_0000:0",
      "active_edges_receiver_sender": [
        [
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.076497,
          "6": 0.0,
          "7": -0.076497,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.076497,
          "14": 0.0,
          "15": 0.076497,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.076497,
          "22": 0.076497,
          "23": 0.0,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:4",
      "active_edges_receiver_sender": [
        [
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.08737,
          "6": 0.042209,
          "7": -0.076497,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.08737,
          "14": 0.042209,
          "15": 0.076497,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.118707,
          "22": 0.118707,
          "23": 0.0,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.042209,
          "30": 0.042209,
          "31": 0.0,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:8",
      "active_edges_receiver_sender": [
        [
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.125532,
          "6": 0.071913,
          "7": -0.102892,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.087646,
          "14": 0.071913,
          "15": 0.050103,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.150739,
          "22": 0.14841,
          "23": -0.026394,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.076604,
          "30": 0.071913,
          "31": -0.026394,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:13",
      "active_edges_receiver_sender": [
        [
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.118734,
          "6": -0.057916,
          "7": -0.103651,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.076085,
          "14": -0.057916,
          "15": 0.049344,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.032903,
          "22": 0.018582,
          "23": -0.027154,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.063965,
          "30": -0.057916,
          "31": -0.027154,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:17",
      "active_edges_receiver_sender": [
        [
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.078336,
          "6": -0.058295,
          "7": -0.052327,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.116328,
          "14": -0.058295,
          "15": 0.100667,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.030257,
          "22": 0.018202,
          "23": 0.02417,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.063107,
          "30": -0.058295,
          "31": 0.02417,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:22",
      "active_edges_receiver_sender": [
        [
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.191563,
          "6": -0.058621,
          "7": -0.182373,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.06557,
          "14": -0.058621,
          "15": -0.029378,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.107374,
          "22": 0.017877,
          "23": -0.105876,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.121021,
          "30": -0.058621,
          "31": -0.105876,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:26",
      "active_edges_receiver_sender": [
        [
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.191563,
          "6": -0.058621,
          "7": -0.182373,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.06557,
          "14": -0.058621,
          "15": -0.029378,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.107374,
          "22": 0.017877,
          "23": -0.105876,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.121021,
          "30": -0.058621,
          "31": -0.105876,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:31",
      "active_edges_receiver_sender": [
        [
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.192488,
          "6": 0.00963,
          "7": -0.192247,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.040416,
          "14": 0.00963,
          "15": -0.039252,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.144277,
          "22": 0.086127,
          "23": -0.11575,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.11615,
          "30": 0.00963,
          "31": -0.11575,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:35",
      "active_edges_receiver_sender": [
        [
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.197569,
          "6": 0.045546,
          "7": -0.192247,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.060126,
          "14": 0.045546,
          "15": -0.039252,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.168204,
          "22": 0.122043,
          "23": -0.11575,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.124388,
          "30": 0.045546,
          "31": -0.11575,
          "32": 1.0,
          "33": 1.0,
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
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.132097,
          "6": 0.045546,
          "7": -0.123996,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.053994,
          "14": 0.045546,
          "15": 0.028998,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.130961,
          "22": 0.122043,
          "23": -0.047499,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.065807,
          "30": 0.045546,
          "31": -0.047499,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:44",
      "active_edges_receiver_sender": [
        [
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.049675,
          "6": 0.045546,
          "7": -0.01983,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.140739,
          "14": 0.045546,
          "15": 0.133165,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.134558,
          "22": 0.122043,
          "23": 0.056668,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.072702,
          "30": 0.045546,
          "31": 0.056668,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:49",
      "active_edges_receiver_sender": [
        [
          1,
          0
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          5,
          6,
          7,
          8,
          9,
          10,
          13,
          14,
          15,
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          29,
          30,
          31,
          32,
          33,
          34
        ],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {
          "5": 0.069128,
          "6": 0.045546,
          "7": 0.052002,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "13": 0.209995,
          "14": 0.045546,
          "15": 0.204997,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "21": 0.177219,
          "22": 0.122043,
          "23": 0.128499,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "29": 0.136332,
          "30": 0.045546,
          "31": 0.128499,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {},
        {}
      ]
    }
  ]
}

Recent trials:
[
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260714_100238/iteration/1o_2r_vs_4r/20260714_100238/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "1o_2r_vs_4r",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-14T10:06:55+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260714_100238/iteration/1o_2r_vs_4r/20260714_100238/candidates/iter_000/comm_init.py",
      "documented_obs_dim": 49,
      "map_name": "1o_2r_vs_4r",
      "matrix_edge_rate": 0.08333333333333333,
      "matrix_max": 1.0,
      "matrix_min": 0.0,
      "message_dim": 66,
      "valid": true,
      "validation_obs_dim": 66,
      "validation_obs_source": "rollout",
      "what_dim": 66,
      "when_edge_rate": 0.08333333333333333,
      "who_edge_rate": 0.3333333333333333
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260714_100238/iteration/1o_2r_vs_4r/20260714_100238/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "1o_2r_vs_4r",
    "matrix_edge_rate": 0.3251366120218579,
    "message_dim": 66,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-14T10:06:55+00:00",
    "valid": true,
    "when_edge_rate": 0.3251366120218579,
    "who_edge_rate": 0.3333333333333333
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260714_100238/iteration/1o_2r_vs_4r/20260714_100238/candidates/iter_000/comm_init.py",
    "failure_analysis": "The policy’s intent (overseer reports visible enemy attributes to roaches) is plausible, but the implementation misaligns observation indices for enemy availability and feature blocks for enemies 1–3. As a result, the when condition uses incorrect proxy features (e.g., distance instead of availability) and the what mask includes wrong or missing elements. Even though the rollout evaluation shows non‑zero communication, the conveyed information does not match the intended enemy data, making the policy unreliable for coordinating with actual enemy observations.",
    "iteration": 0,
    "map_name": "1o_2r_vs_4r",
    "matrix_edge_rate": 0.08333333333333333,
    "message_dim": 66,
    "next_hypothesis": "Correct the availability checks to indices 11, 18, 25 (enemy_1_available, enemy_2_available, enemy_3_available). Adjust the what blocks to the exact feature ranges: enemy_1 (12–17), enemy_2 (19–24), enemy_3 (26–31). Use the feature_index mapping provided in the rollout alignment to guarantee correctness.",
    "rollout_grounding_score": 0.1,
    "score": 0.25,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-14T10:08:13+00:00",
    "valid": true,
    "what_score": 0.1,
    "when_score": 0.5,
    "who_score": 0.9
  }
]

Current code:
```python
import torch


def message_design_instruction():
    """
    Returns a textual instruction describing the communication policy.
    Required by LMAC validation.
    """
    return (
        "Overseer-to-roach communication policy for 1o_2r_vs_4r.\n"
        "The overseer (agent 0) sends information about all currently visible enemies "
        "(enemy presence, distance, relative position, health, type) to both roaches "
        "(agents 1 and 2) whenever at least one enemy is detected. "
        "Communication is static (always allowed from overseer to roaches)."
    )


def communication_who(o):
    """
    Returns a [batch, n_agents, n_agents] binary mask indicating allowed sender→receiver edges.
    Overseer (agent 0) is the permanent sender; roaches (agent 1 and agent 2) are the receivers.
    """
    batch, n_agents, obs_dim = o.shape
    who = torch.zeros(batch, n_agents, n_agents, device=o.device, dtype=torch.float32)
    # Static sender: agent 0 -> receivers: agent 1, agent 2
    if n_agents > 1:
        who[:, 1, 0] = 1.0  # RULE R1, R2, R3, R4: agent 0 to agent 1
    if n_agents > 2:
        who[:, 2, 0] = 1.0  # RULE R1, R2, R3, R4: agent 0 to agent 2
    return who


def communication_when(o):
    """
    Returns a [batch, n_agents, n_agents] binary mask; 1 if a message should be sent.
    Sending edge (0→1) and (0→2) is activated when at least one enemy is visible to the Overseer.
    """
    batch, n_agents, obs_dim = o.shape
    # Per-enemy availability checks (feature indices 4, 12, 20, 28)
    e0_avail = o[:, 0, 4] > 0.5   # R1: enemy_0_available
    e1_avail = o[:, 0, 12] > 0.5  # R2: enemy_1_available
    e2_avail = o[:, 0, 20] > 0.5  # R3: enemy_2_available
    e3_avail = o[:, 0, 28] > 0.5  # R4: enemy_3_available

    any_avail = e0_avail | e1_avail | e2_avail | e3_avail  # [batch] boolean

    when = torch.zeros(batch, n_agents, n_agents, device=o.device, dtype=torch.float32)
    if n_agents > 1:
        when[:, 1, 0] = any_avail.float()  # R1-R4 sender to agent 1
    if n_agents > 2:
        when[:, 2, 0] = any_avail.float()  # R1-R4 sender to agent 2
    return when


def communication_what(o):
    """
    Returns an observation-aligned content mask [batch, n_agents, obs_dim].
    For agent 0 (Overseer) it selects the features of each visible enemy.
    """
    batch, n_agents, obs_dim = o.shape
    what = torch.zeros(batch, n_agents, obs_dim, device=o.device, dtype=torch.float32)

    # Helper: safely assign a contiguous block of indices, respecting obs_dim
    def assign_block(agent_idx, start, end, flag):
        if start >= obs_dim:
            return
        end_clipped = min(end, obs_dim)
        if end_clipped <= start:
            return
        what[:, agent_idx, start:end_clipped] = flag.unsqueeze(1).expand(batch, end_clipped - start).float()

    # RULE R1: enemy_0 features (indices 5..10) when enemy_0_available (index 4) > 0.5
    e0_avail = o[:, 0, 4] > 0.5
    assign_block(0, 5, 11, e0_avail)

    # RULE R2: enemy_1 features (indices 13..18) when enemy_1_available (index 12) > 0.5
    e1_avail = o[:, 0, 12] > 0.5
    assign_block(0, 13, 19, e1_avail)

    # RULE R3: enemy_2 features (indices 21..26) when enemy_2_available (index 20) > 0.5
    e2_avail = o[:, 0, 20] > 0.5
    assign_block(0, 21, 27, e2_avail)

    # RULE R4: enemy_3 features (indices 29..34) when enemy_3_available (index 28) > 0.5
    e3_avail = o[:, 0, 28] > 0.5
    assign_block(0, 29, 35, e3_avail)

    return what

```

Return JSON with keys:
- Evaluation
- Missing_Information_Hypothesis
- Improvement_Suggestions
- Target_Functions
- Target_Rule_IDs
Do not use downstream RL win-rate as feedback. Focus on rollout-grounded who/when/what critique only.
