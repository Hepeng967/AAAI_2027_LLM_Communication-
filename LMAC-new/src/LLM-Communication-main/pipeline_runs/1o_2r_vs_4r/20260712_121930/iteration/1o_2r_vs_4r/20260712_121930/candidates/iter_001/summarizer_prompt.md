## system

You analyze LLM-judged failures for LMAC communication policies. Return one compact JSON object only.

## user

Analyze the LLM judge result for map `1o_2r_vs_4r` and propose the next communication-code revision.

Judge summary:
{
  "accepted": false,
  "blocking_failures": [
    {
      "evidence": "Roach-to-roach communication (R2) triggers only on `previous_action_0 > 0.5`, but that feature has a nonzero rate of 0.025 (see feature statistics). The rollout evidence shows roaches taking non‑zero actions (e.g. case train_traj_0000:4 agent 1 has previous_action_2 = 1) yet no roach‑to‑roach edge activates. The intended rule 'when a Roach has taken an action' should use any non‑noop action, not exclusively action 0.",
      "revision_target": "when",
      "type": "when_condition_too_restrictive"
    },
    {
      "evidence": "For R1 (overseer→roaches) the what mask includes ally features (indices 32,33,34) but the rule declares it sends 'enemy information'. It also omits many relevant enemy fields such as enemy_1_rel_x, enemy_2_distance, enemy_3_health etc. (compare code indices with feature_index). The mask is not grounded in comprehensive situational awareness. For R2 (roach→roach) the what mask covers all previous actions (indices 53‑62), but the restrictive when condition means the message is only sent when `previous_action_0` is 1, rendering the mask effectively useless. The policy description claims roaches communicate after any action, not just action 0.",
      "revision_target": "what",
      "type": "what_mask_incomplete_and_misaligned"
    },
    {
      "evidence": "{\"who_when_what_consistent\": false, \"conflicts_or_uncovered_requirements\": [\"R2 when condition contradicts the rule's intent; R1 what mask includes ally features not listed in the instructions.\"]}",
      "revision_target": "who|when|what",
      "type": "cross_rule_inconsistency"
    }
  ],
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_121930/iteration/1o_2r_vs_4r/20260712_121930/candidates/iter_000/comm_init.py",
  "cross_rule_check": {
    "conflicts_or_uncovered_requirements": [
      "R2 when condition contradicts the rule's intent; R1 what mask includes ally features not listed in the instructions."
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
  "expected_effect": "With these changes, roaches will exchange action information whenever they act, enabling better coordination, and the overseer’s message will provide a complete snapshot of the enemy team, giving roaches the global view needed for effective decision‑making.",
  "failure_analysis": "The who matrix is structurally sound (overseer→roaches, roach↔roach), but the when and what implementations are inconsistent with the described rules and do not exploit the available information. The R2 when condition is so narrow that roach communication almost never happens, and the R1 what mask is a haphazard selection of features that misses critical enemy fields while including ally fields. These defects prevent the policy from being a plausible pure communication strategy.",
  "improvement_suggestions": "1. R2 when: replace `o[:, :, 53] > 0.5` with `(o[:, :, 53:63] > 0.5).any(dim=-1)` so that any non‑noop action triggers communication. 2. R1 what: reconstruct the mask to include all enemy features (available, distance, rel_x, rel_y, health, type_0, type_1 for each of the four enemies, i.e. indices 4‑31 plus possibly ally info if needed). Remove unintended ally features unless they are explicitly justified. 3. Ensure the policy description matches the implementation: if ally information is included, update the instruction text.",
  "replacement_readiness": "not_ready",
  "rollout_grounding_score": 0.2,
  "rule_checks": [
    {
      "counterexample_case_ids": [],
      "observed_trigger_or_edge_rate": 1.0,
      "requirement_hypothesis": "Overseer provides global enemy (and possibly ally) information to roaches for target selection and positioning.",
      "rule_id": "R1",
      "supporting_case_ids": [
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
      "threshold_in_observed_range": true,
      "unresolved_questions": [
        "Should the overseer include ally information? If yes, the rule description must be updated."
      ],
      "what_supported": false,
      "when_supported": true,
      "who_supported": true
    },
    {
      "counterexample_case_ids": [
        "train_traj_0000:4"
      ],
      "observed_trigger_or_edge_rate": 0.025,
      "requirement_hypothesis": "Roaches share their previous actions to coordinate focus fire or avoid redundant actions.",
      "rule_id": "R2",
      "supporting_case_ids": [],
      "threshold_in_observed_range": true,
      "unresolved_questions": [
        "Should roach communication occur every step? Using any previous_action>0.5 would raise the edge rate to ~0.55 (sum of nonzero rates of action channels), better matching the original intent."
      ],
      "what_supported": false,
      "when_supported": false,
      "who_supported": true
    }
  ],
  "score": 0.35,
  "usage": {
    "completion_tokens": 7306,
    "prompt_tokens": 23059,
    "total_tokens": 30365
  },
  "what_score": 0.2,
  "when_score": 0.2,
  "who_score": 0.8
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "1o_2r_vs_4r",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_121930/iteration/1o_2r_vs_4r/20260712_121930/candidates/iter_000/comm_init.py",
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
  "matrix_edge_rate": 0.34584699453551915,
  "who_edge_rate": 0.6666666666666666,
  "when_edge_rate": 0.34584699453551915,
  "message_nonzero_rate": 0.2222222222222222,
  "message_abs_mean": 0.2222222222222222,
  "active_sender_what_coverage_mean": 0.3488221617870558,
  "active_sender_what_coverage_min": 0.1515151560306549,
  "active_sender_count": 3279,
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": 0.0,
          "7": -0.076497,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": 0.0,
          "15": 0.076497,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.076497,
          "23": 0.0,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": 0.0,
          "31": 0.0,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": 0.042209,
          "7": -0.076497,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": 0.042209,
          "15": 0.076497,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.118707,
          "23": 0.0,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": 0.042209,
          "31": 0.0,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 1.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 1.0,
          "55": 0.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": 0.071913,
          "7": -0.102892,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": 0.071913,
          "15": 0.050103,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.14841,
          "23": -0.026394,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": 0.071913,
          "31": -0.026394,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 0.0,
          "57": 1.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 0.0,
          "57": 1.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": -0.057916,
          "7": -0.103651,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": -0.057916,
          "15": 0.049344,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.018582,
          "23": -0.027154,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": -0.057916,
          "31": -0.027154,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 1.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 1.0,
          "55": 0.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": -0.058295,
          "7": -0.052327,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": -0.058295,
          "15": 0.100667,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.018202,
          "23": 0.02417,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": -0.058295,
          "31": 0.02417,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 1.0,
          "55": 0.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 1.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": -0.058621,
          "7": -0.182373,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": -0.058621,
          "15": -0.029378,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.017877,
          "23": -0.105876,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": -0.058621,
          "31": -0.105876,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 0.0,
          "57": 0.0,
          "58": 1.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 1.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": -0.058621,
          "7": -0.182373,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": -0.058621,
          "15": -0.029378,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.017877,
          "23": -0.105876,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": -0.058621,
          "31": -0.105876,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 1.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 1.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": 0.00963,
          "7": -0.192247,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": 0.00963,
          "15": -0.039252,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.086127,
          "23": -0.11575,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": 0.00963,
          "31": -0.11575,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 1.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 1.0,
          "55": 0.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": 0.045546,
          "7": -0.192247,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": 0.045546,
          "15": -0.039252,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.122043,
          "23": -0.11575,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": 0.045546,
          "31": -0.11575,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 1.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 1.0,
          "55": 0.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": 0.045546,
          "7": -0.123996,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": 0.045546,
          "15": 0.028998,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.122043,
          "23": -0.047499,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": 0.045546,
          "31": -0.047499,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 1.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 0.0,
          "57": 1.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": 0.045546,
          "7": -0.01983,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": 0.045546,
          "15": 0.133165,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.122043,
          "23": 0.056668,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": 0.045546,
          "31": 0.056668,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 1.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 1.0,
          "55": 0.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
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
          4,
          6,
          7,
          8,
          9,
          10,
          12,
          14,
          15,
          16,
          17,
          18,
          20,
          22,
          23,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          34
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ],
        [
          53,
          54,
          55,
          56,
          57,
          58,
          59,
          60,
          61,
          62
        ]
      ],
      "what_coverage_by_sender": [
        0.363636,
        0.151515,
        0.151515
      ],
      "selected_values_by_sender": [
        {
          "4": 1.0,
          "6": 0.045546,
          "7": 0.052002,
          "8": 1.0,
          "9": 1.0,
          "10": 0.0,
          "12": 1.0,
          "14": 0.045546,
          "15": 0.204997,
          "16": 1.0,
          "17": 1.0,
          "18": 0.0,
          "20": 1.0,
          "22": 0.122043,
          "23": 0.128499,
          "24": 1.0,
          "25": 1.0,
          "26": 0.0,
          "28": 1.0,
          "30": 0.045546,
          "31": 0.128499,
          "32": 1.0,
          "33": 1.0,
          "34": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 0.0,
          "56": 1.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        },
        {
          "53": 0.0,
          "54": 0.0,
          "55": 1.0,
          "56": 0.0,
          "57": 0.0,
          "58": 0.0,
          "59": 0.0,
          "60": 0.0,
          "61": 0.0,
          "62": 0.0
        }
      ]
    }
  ]
}

Recent trials:
[
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_121930/iteration/1o_2r_vs_4r/20260712_121930/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "1o_2r_vs_4r",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-12T12:24:22+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_121930/iteration/1o_2r_vs_4r/20260712_121930/candidates/iter_000/comm_init.py",
      "documented_obs_dim": 49,
      "map_name": "1o_2r_vs_4r",
      "matrix_edge_rate": 0.3333333333333333,
      "matrix_max": 1.0,
      "matrix_min": 0.0,
      "message_dim": 66,
      "valid": true,
      "validation_obs_dim": 66,
      "validation_obs_source": "rollout",
      "what_dim": 66,
      "when_edge_rate": 0.3333333333333333,
      "who_edge_rate": 0.6666666666666666
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_121930/iteration/1o_2r_vs_4r/20260712_121930/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "1o_2r_vs_4r",
    "matrix_edge_rate": 0.34584699453551915,
    "message_dim": 66,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-12T12:24:22+00:00",
    "valid": true,
    "when_edge_rate": 0.34584699453551915,
    "who_edge_rate": 0.6666666666666666
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_121930/iteration/1o_2r_vs_4r/20260712_121930/candidates/iter_000/comm_init.py",
    "failure_analysis": "The who matrix is structurally sound (overseer→roaches, roach↔roach), but the when and what implementations are inconsistent with the described rules and do not exploit the available information. The R2 when condition is so narrow that roach communication almost never happens, and the R1 what mask is a haphazard selection of features that misses critical enemy fields while including ally fields. These defects prevent the policy from being a plausible pure communication strategy.",
    "iteration": 0,
    "map_name": "1o_2r_vs_4r",
    "matrix_edge_rate": 0.3333333333333333,
    "message_dim": 66,
    "next_hypothesis": "1. R2 when: replace `o[:, :, 53] > 0.5` with `(o[:, :, 53:63] > 0.5).any(dim=-1)` so that any non‑noop action triggers communication. 2. R1 what: reconstruct the mask to include all enemy features (available, distance, rel_x, rel_y, health, type_0, type_1 for each of the four enemies, i.e. indices 4‑31 plus possibly ally info if needed). Remove unintended ally features unless they are explicitly justified. 3. Ensure the policy description matches the implementation: if ally information is included, update the instruction text.",
    "rollout_grounding_score": 0.2,
    "score": 0.35,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-12T12:25:58+00:00",
    "valid": true,
    "what_score": 0.2,
    "when_score": 0.2,
    "who_score": 0.8
  }
]

Current code:
```python
import torch

def message_design_instruction(state=None, env_info=None):
    """
    Returns a string instruction describing the teacher communication policy.
    Required for LMAC validation.
    """
    return (
        "Teacher communication policy for 1o_2r_vs_4r:\n"
        " - Overseer (agent 0) sends enemy information (positions, health, types) to both Roaches.\n"
        " - Each Roach (agents 1,2) sends its previous action to the other Roach.\n"
        " - Communication occurs when Overseer is present (R1) or when a Roach has taken an action (R2).\n"
        " - The content masks select relevant observation features."
    )


def communication_who(o):
    """
    Returns a [batch, receiver, sender] binary matrix indicating allowed communication edges.
    RULE R1: Overseer (agent 0) sends to Roaches (agents 1,2).
    RULE R2: Each Roach sends to the other Roach.
    """
    B, N, _ = o.shape
    who = torch.zeros(B, N, N, dtype=o.dtype, device=o.device)
    # RULE R1: Overseer -> Roaches
    who[:, 1, 0] = 1.0
    who[:, 2, 0] = 1.0
    # RULE R2: Roach i -> Roach j (i != j)
    who[:, 2, 1] = 1.0  # agent 1 -> agent 2
    who[:, 1, 2] = 1.0  # agent 2 -> agent 1
    return who


def communication_when(o):
    """
    Returns a [batch, receiver, sender] binary matrix indicating active communication edges.
    RULE R1: always when Overseer exists (agent_id_0 > -1.0).
    RULE R2: when Roach has taken an action (previous_action_0 > 0.5).
    """
    B, N, D = o.shape
    when = torch.zeros(B, N, N, dtype=o.dtype, device=o.device)

    # RULE R1: agent_id_0 (index 63) > -1.0 for sender 0
    cond_R1 = o[:, 0, 63] > -1.0
    when[:, 1, 0] = cond_R1.to(dtype=o.dtype)
    when[:, 2, 0] = cond_R1.to(dtype=o.dtype)

    # RULE R2: previous_action_0 (index 53) > 0.5 for senders 1 and 2
    cond_s1 = o[:, 1, 53] > 0.5
    cond_s2 = o[:, 2, 53] > 0.5
    when[:, 2, 1] = cond_s1.to(dtype=o.dtype)
    when[:, 1, 2] = cond_s2.to(dtype=o.dtype)

    return when


def communication_what(o):
    """
    Returns an obs-aligned content mask of the same shape as o.
    RULE R1: Overseer's enemy features (indices listed).
    RULE R2: Roaches' previous actions (indices 53..62).
    """
    B, N, D = o.shape
    what = torch.zeros_like(o)

    # Agent identification via one-hot IDs (indices 63, 64, 65)
    is_agent0 = o[:, :, 63] > 0.5  # [B, N]
    is_agent1 = o[:, :, 64] > 0.5
    is_agent2 = o[:, :, 65] > 0.5

    # RULE R1: Enemy information (indices from policy specification)
    r1_indices_tensor = torch.tensor([4, 6, 7, 8, 9, 10, 12, 14, 15, 16, 17, 18,
                                     20, 22, 23, 24, 25, 26, 28, 30, 31, 32, 33, 34],
                                    dtype=torch.long, device=o.device)
    # Keep only indices within D (safety)
    valid_r1 = r1_indices_tensor < D
    r1_indices_tensor = r1_indices_tensor[valid_r1]
    if r1_indices_tensor.numel() > 0:
        mask_r1 = torch.zeros(D, dtype=o.dtype, device=o.device)
        mask_r1.scatter_(0, r1_indices_tensor, 1.0)
        what += is_agent0.unsqueeze(-1) * mask_r1.unsqueeze(0).unsqueeze(0)

    # RULE R2: Previous actions (indices 53 to 62 inclusive)
    r2_start = min(53, D)
    r2_end = min(63, D)
    if r2_start < r2_end:
        mask_r2 = torch.zeros(D, dtype=o.dtype, device=o.device)
        mask_r2[r2_start:r2_end] = 1.0
        what += (is_agent1.unsqueeze(-1) + is_agent2.unsqueeze(-1)) * mask_r2.unsqueeze(0).unsqueeze(0)

    return what


def communication(o):
    """
    Combines who, when, and what to produce the final aggregated communication tensor.
    Returns a tensor of shape [batch, n_agents, obs_dim] where each receiver’s
    channel contains the sum of messages from its allowed senders.
    """
    who = communication_who(o)          # [B, N, N] receiver x sender
    when = communication_when(o)        # [B, N, N]
    what = communication_what(o)        # [B, N, D] per-agent feature mask

    # Edge mask: which (receiver, sender) communications are active
    edge_mask = who * when              # [B, N, N]
    # Content: sender observations masked by what
    content = what * o                  # [B, N, D]

    # Aggregate messages to each receiver: (who*when) x (what * o)
    msg = torch.bmm(edge_mask, content) # [B, N, D]

    return msg

```

Return JSON with keys:
- Evaluation
- Missing_Information_Hypothesis
- Improvement_Suggestions
- Target_Functions
- Target_Rule_IDs
Do not use downstream RL win-rate as feedback. Focus on rollout-grounded who/when/what critique only.
