## system

You are an expert MARL communication-policy judge. Evaluate the generated policy only from the task spec, code, and interface validation. Return one JSON object only.

## user

Evaluate this pure LLM-generated LMAC communication strategy for task `academy_3_vs_1_with_keeper`
in environment `grf`.

Research goal:
- We are testing the capability boundary of LLM-designed communication.
- Do NOT use DRC, decision_sufficient, causally_useful, downstream RL win-rate, or hidden/global state.
- Judge whether the policy gives a plausible pure communication strategy for who, when, and what.

Map spec:
{
  "environment": "grf",
  "n_agents": 3,
  "n_enemies": 2,
  "n_actions": 19,
  "obs_dim": 48,
  "documented_raw_obs_dim": 26,
  "time_seq": 10,
  "objective": "Three attackers coordinate positioning and passes to score against one field defender and a goalkeeper.",
  "raw_feature_semantics": "ego position/direction, teammate relative positions/directions, opponent relative positions/directions, and ball relative position/direction"
}

Rollout-backed LMAC observation alignment:
{
  "map_name": "academy_3_vs_1_with_keeper",
  "rollout_root": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf",
  "files": [
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0000.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0001.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0002.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0003.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0004.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0005.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0006.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0007.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0008.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0009.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0010.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0011.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0012.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0013.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0014.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0015.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0016.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0017.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0018.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0019.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0020.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0021.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0022.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0023.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0024.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0025.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0026.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0027.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0028.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0029.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0030.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0031.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0032.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0033.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0034.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0035.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0036.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0037.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0038.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0039.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0040.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0041.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0042.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0043.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0044.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0045.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0046.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0047.pkl"
  ],
  "available": true,
  "n_agents": 3,
  "raw_obs_dim": 26,
  "rollout_obs_dim": 48,
  "documented_obs_dim": 26,
  "extra_obs_dim": 0,
  "episodes": 48,
  "transitions": 3181,
  "seq_lengths": [
    150,
    42,
    94,
    29,
    41,
    64,
    24,
    52,
    103,
    55,
    55,
    34,
    138,
    42,
    32,
    33,
    68,
    51,
    46,
    24,
    21,
    48,
    48,
    137,
    132,
    50,
    150,
    17,
    116,
    41,
    68,
    122,
    44,
    36,
    84,
    150,
    33,
    113,
    86,
    43,
    26,
    32,
    61,
    72,
    132,
    40,
    35,
    67
  ],
  "action_dim": 19,
  "agent_types": [
    "football_player",
    "football_player",
    "football_player"
  ],
  "feature_index": {
    "ego_absolute_xy": [
      0,
      2
    ],
    "teammate_0_relative_xy": [
      2,
      4
    ],
    "teammate_1_relative_xy": [
      4,
      6
    ],
    "ego_direction_xy": [
      6,
      8
    ],
    "teammate_0_direction_xy": [
      8,
      10
    ],
    "teammate_1_direction_xy": [
      10,
      12
    ],
    "opponent_0_relative_xy": [
      12,
      14
    ],
    "opponent_1_relative_xy": [
      14,
      16
    ],
    "opponent_0_direction_xy": [
      16,
      18
    ],
    "opponent_1_direction_xy": [
      18,
      20
    ],
    "ball_relative_xy": [
      20,
      22
    ],
    "ball_z": [
      22,
      23
    ],
    "ball_direction_xyz": [
      23,
      26
    ],
    "previous_action_0": [
      26,
      27
    ],
    "previous_action_1": [
      27,
      28
    ],
    "previous_action_2": [
      28,
      29
    ],
    "previous_action_3": [
      29,
      30
    ],
    "previous_action_4": [
      30,
      31
    ],
    "previous_action_5": [
      31,
      32
    ],
    "previous_action_6": [
      32,
      33
    ],
    "previous_action_7": [
      33,
      34
    ],
    "previous_action_8": [
      34,
      35
    ],
    "previous_action_9": [
      35,
      36
    ],
    "previous_action_10": [
      36,
      37
    ],
    "previous_action_11": [
      37,
      38
    ],
    "previous_action_12": [
      38,
      39
    ],
    "previous_action_13": [
      39,
      40
    ],
    "previous_action_14": [
      40,
      41
    ],
    "previous_action_15": [
      41,
      42
    ],
    "previous_action_16": [
      42,
      43
    ],
    "previous_action_17": [
      43,
      44
    ],
    "previous_action_18": [
      44,
      45
    ],
    "agent_id_0": [
      45,
      46
    ],
    "agent_id_1": [
      46,
      47
    ],
    "agent_id_2": [
      47,
      48
    ]
  },
  "feature_statistics": {
    "ball_z": {
      "index": 22,
      "min": 0.0,
      "max": 5.226794,
      "mean": 0.286133,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.579566,
      "nonzero_rate": 0.440918
    },
    "previous_action_0": {
      "index": 26,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.023519,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.023519
    },
    "previous_action_1": {
      "index": 27,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.020996,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.020996
    },
    "previous_action_2": {
      "index": 28,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025635,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025635
    },
    "previous_action_3": {
      "index": 29,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.023438,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.023438
    },
    "previous_action_4": {
      "index": 30,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.020752,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.020752
    },
    "previous_action_5": {
      "index": 31,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.02238,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02238
    },
    "previous_action_6": {
      "index": 32,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021891,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021891
    },
    "previous_action_7": {
      "index": 33,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021159,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021159
    },
    "previous_action_8": {
      "index": 34,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.024251,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.024251
    },
    "previous_action_9": {
      "index": 35,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.0236,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0236
    },
    "previous_action_10": {
      "index": 36,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021484,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021484
    },
    "previous_action_11": {
      "index": 37,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.024495,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.024495
    },
    "previous_action_12": {
      "index": 38,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021403,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021403
    },
    "previous_action_13": {
      "index": 39,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.022217,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.022217
    },
    "previous_action_14": {
      "index": 40,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021403,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021403
    },
    "previous_action_15": {
      "index": 41,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021403,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021403
    },
    "previous_action_16": {
      "index": 42,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.018962,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.018962
    },
    "previous_action_17": {
      "index": 43,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.02417,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02417
    },
    "previous_action_18": {
      "index": 44,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.037272,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.037272
    },
    "agent_id_0": {
      "index": 45,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.333333,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.333333
    },
    "agent_id_1": {
      "index": 46,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.333333,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.333333
    },
    "agent_id_2": {
      "index": 47,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.333333,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.333333
    }
  },
  "alignment_note": "rollout_obs_dim is exactly the RL communication input: raw observation + previous-action one-hot + agent-id one-hot. Feature positions are identical in offline evaluation and RL training."
}

Interface validation:
{
  "valid": true,
  "map_name": "academy_3_vs_1_with_keeper",
  "comm_code": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_3_vs_1_with_keeper/20260716_190252/iteration/academy_3_vs_1_with_keeper/20260716_190252/candidates/iter_000/comm_init.py",
  "validation_obs_source": "rollout",
  "validation_obs_dim": 48,
  "documented_obs_dim": 26,
  "message_dim": 48,
  "matrix_edge_rate": 0.0,
  "who_edge_rate": 0.0,
  "when_edge_rate": 1.0,
  "what_dim": 48,
  "matrix_min": 0.0,
  "matrix_max": 0.0
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "academy_3_vs_1_with_keeper",
  "comm_code": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_3_vs_1_with_keeper/20260716_190252/iteration/academy_3_vs_1_with_keeper/20260716_190252/candidates/iter_000/comm_init.py",
  "files": [
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0000.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0001.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0002.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0003.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0004.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0005.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0006.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0007.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0008.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0009.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0010.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0011.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0012.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0013.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0014.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0015.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0016.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0017.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0018.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0019.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0020.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0021.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0022.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0023.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0024.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0025.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0026.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_3_vs_1_with_keeper/train_traj_0027.pkl"
  ],
  "transitions": 4096,
  "n_agents": 3,
  "rollout_obs_dim": 48,
  "message_dim": 48,
  "matrix_edge_rate": 0.2265625,
  "who_edge_rate": 0.2265625,
  "when_edge_rate": 1.0,
  "message_nonzero_rate": 0.3971354166666667,
  "message_abs_mean": 0.3971354166666667,
  "active_sender_what_coverage_mean": 0.3222581413057115,
  "active_sender_what_coverage_min": 0.2083333283662796,
  "active_sender_count": 4176,
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
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
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
          44,
          45,
          46,
          47
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      ],
      "what_coverage_by_sender": [
        0.458333,
        0.208333,
        0.208333
      ],
      "selected_values_by_sender": [
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 1.0,
          "46": 0.0,
          "47": 0.0
        },
        {
          "0": 0.707721,
          "1": 0.203254,
          "12": 0.303309,
          "13": -0.203254,
          "14": 0.050551,
          "15": -0.203254,
          "16": -0.0,
          "17": 0.0,
          "18": -0.0,
          "19": 0.0
        },
        {
          "0": 0.707721,
          "1": -0.203254,
          "12": 0.303309,
          "13": 0.203254,
          "14": 0.050551,
          "15": 0.203254,
          "16": -0.0,
          "17": 0.0,
          "18": -0.0,
          "19": 0.0
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
          44,
          45,
          46,
          47
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      ],
      "what_coverage_by_sender": [
        0.458333,
        0.208333,
        0.208333
      ],
      "selected_values_by_sender": [
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 1.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 1.0,
          "46": 0.0,
          "47": 0.0
        },
        {
          "0": 0.674405,
          "1": 0.143717,
          "12": 0.313823,
          "13": -0.151121,
          "14": 0.019985,
          "15": -0.149711,
          "16": 0.000348,
          "17": -0.004053,
          "18": -0.00243,
          "19": -0.003425
        },
        {
          "0": 0.714262,
          "1": -0.209805,
          "12": 0.273967,
          "13": 0.202401,
          "14": -0.019871,
          "15": 0.203811,
          "16": 0.000348,
          "17": -0.004053,
          "18": -0.00243,
          "19": -0.003425
        }
      ]
    },
    {
      "case_id": "train_traj_0000:27",
      "active_edges_receiver_sender": [
        [
          0,
          2
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
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ],
        [
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
          44,
          45,
          46,
          47
        ]
      ],
      "what_coverage_by_sender": [
        0.208333,
        0.208333,
        0.458333
      ],
      "selected_values_by_sender": [
        {
          "0": 0.552233,
          "1": -0.042706,
          "12": 0.43786,
          "13": 0.010864,
          "14": 0.229831,
          "15": -0.037058,
          "16": -0.00033,
          "17": 0.003916,
          "18": 0.00294,
          "19": -0.002098
        },
        {
          "0": 0.725934,
          "1": 0.060464,
          "12": 0.264159,
          "13": -0.092307,
          "14": 0.05613,
          "15": -0.140229,
          "16": -0.00033,
          "17": 0.003916,
          "18": 0.00294,
          "19": -0.002098
        },
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 1.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 0.0,
          "46": 0.0,
          "47": 1.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:40",
      "active_edges_receiver_sender": [
        [
          0,
          2
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
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ],
        [
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
          44,
          45,
          46,
          47
        ]
      ],
      "what_coverage_by_sender": [
        0.208333,
        0.208333,
        0.458333
      ],
      "selected_values_by_sender": [
        {
          "0": 0.563143,
          "1": -0.091614,
          "12": 0.426178,
          "13": 0.067827,
          "14": 0.280591,
          "15": -0.022816,
          "16": -0.0,
          "17": 0.0,
          "18": 0.006343,
          "19": -0.0007
        },
        {
          "0": 0.693895,
          "1": -0.013286,
          "12": 0.295426,
          "13": -0.010501,
          "14": 0.149839,
          "15": -0.101144,
          "16": -0.0,
          "17": 0.0,
          "18": 0.006343,
          "19": -0.0007
        },
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 1.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 0.0,
          "46": 0.0,
          "47": 1.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:54",
      "active_edges_receiver_sender": [
        [
          0,
          2
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
        ]
      ],
      "selected_what_indices_by_sender": [
        [
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
          44,
          45,
          46,
          47
        ],
        [
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
          44,
          45,
          46,
          47
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      ],
      "what_coverage_by_sender": [
        0.458333,
        0.458333,
        0.208333
      ],
      "selected_values_by_sender": [
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 1.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 1.0,
          "46": 0.0,
          "47": 0.0
        },
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 1.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 0.0,
          "46": 1.0,
          "47": 0.0
        },
        {
          "0": 0.841205,
          "1": -0.137874,
          "12": 0.140156,
          "13": 0.133021,
          "14": -0.032938,
          "15": -0.007796,
          "16": 0.001341,
          "17": 0.002099,
          "18": -0.007073,
          "19": -0.004468
        }
      ]
    },
    {
      "case_id": "train_traj_0000:67",
      "active_edges_receiver_sender": [
        [
          0,
          2
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
        ]
      ],
      "selected_what_indices_by_sender": [
        [
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
          44,
          45,
          46,
          47
        ],
        [
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
          44,
          45,
          46,
          47
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      ],
      "what_coverage_by_sender": [
        0.458333,
        0.458333,
        0.208333
      ],
      "selected_values_by_sender": [
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 1.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 1.0,
          "46": 0.0,
          "47": 0.0
        },
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 1.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 0.0,
          "46": 1.0,
          "47": 0.0
        },
        {
          "0": 0.790009,
          "1": -0.135044,
          "12": 0.164449,
          "13": 0.135963,
          "14": -0.104043,
          "15": -0.006256,
          "16": 0.004827,
          "17": 0.000353,
          "18": -0.001219,
          "19": 0.005894
        }
      ]
    },
    {
      "case_id": "train_traj_0000:81",
      "active_edges_receiver_sender": [
        [
          0,
          2
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
        ]
      ],
      "selected_what_indices_by_sender": [
        [
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
          44,
          45,
          46,
          47
        ],
        [
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
          44,
          45,
          46,
          47
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      ],
      "what_coverage_by_sender": [
        0.458333,
        0.458333,
        0.208333
      ],
      "selected_values_by_sender": [
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 1.0,
          "41": 0.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 1.0,
          "46": 0.0,
          "47": 0.0
        },
        {
          "26": 0.0,
          "27": 0.0,
          "28": 1.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 0.0,
          "46": 1.0,
          "47": 0.0
        },
        {
          "0": 0.841686,
          "1": -0.17251,
          "12": 0.141756,
          "13": 0.177416,
          "14": -0.185774,
          "15": 0.144083,
          "16": -0.0,
          "17": 0.0,
          "18": -0.003733,
          "19": 0.007096
        }
      ]
    },
    {
      "case_id": "train_traj_0000:94",
      "active_edges_receiver_sender": [
        [
          0,
          2
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
        ]
      ],
      "selected_what_indices_by_sender": [
        [
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
          44,
          45,
          46,
          47
        ],
        [
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
          44,
          45,
          46,
          47
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      ],
      "what_coverage_by_sender": [
        0.458333,
        0.458333,
        0.208333
      ],
      "selected_values_by_sender": [
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 1.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 1.0,
          "46": 0.0,
          "47": 0.0
        },
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 1.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 0.0,
          "46": 1.0,
          "47": 0.0
        },
        {
          "0": 0.810289,
          "1": -0.179207,
          "12": 0.175951,
          "13": 0.191281,
          "14": -0.169353,
          "15": 0.180005,
          "16": -0.0,
          "17": 0.0,
          "18": -0.003078,
          "19": 0.006393
        }
      ]
    },
    {
      "case_id": "train_traj_0000:108",
      "active_edges_receiver_sender": [
        [
          0,
          2
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
        ]
      ],
      "selected_what_indices_by_sender": [
        [
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
          44,
          45,
          46,
          47
        ],
        [
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
          44,
          45,
          46,
          47
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      ],
      "what_coverage_by_sender": [
        0.458333,
        0.458333,
        0.208333
      ],
      "selected_values_by_sender": [
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 1.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 1.0,
          "46": 0.0,
          "47": 0.0
        },
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 1.0,
          "44": 0.0,
          "45": 0.0,
          "46": 1.0,
          "47": 0.0
        },
        {
          "0": 0.826075,
          "1": -0.186745,
          "12": 0.161114,
          "13": 0.205673,
          "14": -0.196187,
          "15": 0.303769,
          "16": -0.0,
          "17": 0.0,
          "18": 0.002964,
          "19": 0.009081
        }
      ]
    },
    {
      "case_id": "train_traj_0000:121",
      "active_edges_receiver_sender": [
        [
          0,
          2
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
        ]
      ],
      "selected_what_indices_by_sender": [
        [
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
          44,
          45,
          46,
          47
        ],
        [
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
          44,
          45,
          46,
          47
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      ],
      "what_coverage_by_sender": [
        0.458333,
        0.458333,
        0.208333
      ],
      "selected_values_by_sender": [
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 1.0,
          "39": 0.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 1.0,
          "46": 0.0,
          "47": 0.0
        },
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 1.0,
          "44": 0.0,
          "45": 0.0,
          "46": 1.0,
          "47": 0.0
        },
        {
          "0": 0.79167,
          "1": -0.15641,
          "12": 0.195519,
          "13": 0.175337,
          "14": -0.100018,
          "15": 0.387606,
          "16": -0.0,
          "17": 0.0,
          "18": 0.005113,
          "19": 0.008751
        }
      ]
    },
    {
      "case_id": "train_traj_0000:135",
      "active_edges_receiver_sender": [
        [
          0,
          1
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
          1
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ],
        [
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
          44,
          45,
          46,
          47
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      ],
      "what_coverage_by_sender": [
        0.208333,
        0.458333,
        0.208333
      ],
      "selected_values_by_sender": [
        {
          "0": 0.727478,
          "1": 0.319457,
          "12": 0.183265,
          "13": -0.284053,
          "14": -0.001694,
          "15": -0.038156,
          "16": -0.011735,
          "17": 0.001484,
          "18": -0.000551,
          "19": -0.005422
        },
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 1.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 0.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 0.0,
          "46": 1.0,
          "47": 0.0
        },
        {
          "0": 0.801957,
          "1": -0.15605,
          "12": 0.108786,
          "13": 0.191454,
          "14": -0.076173,
          "15": 0.43735,
          "16": -0.011735,
          "17": 0.001484,
          "18": -0.000551,
          "19": -0.005422
        }
      ]
    },
    {
      "case_id": "train_traj_0000:149",
      "active_edges_receiver_sender": [
        [
          0,
          1
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
          1
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ],
        [
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
          44,
          45,
          46,
          47
        ],
        [
          0,
          1,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19
        ]
      ],
      "what_coverage_by_sender": [
        0.208333,
        0.458333,
        0.208333
      ],
      "selected_values_by_sender": [
        {
          "0": 0.727015,
          "1": 0.292128,
          "12": 0.176453,
          "13": -0.276194,
          "14": -0.016051,
          "15": -0.121625,
          "16": 0.008915,
          "17": -0.001665,
          "18": -0.001833,
          "19": -0.009135
        },
        {
          "26": 0.0,
          "27": 0.0,
          "28": 0.0,
          "29": 0.0,
          "30": 0.0,
          "31": 0.0,
          "32": 0.0,
          "33": 0.0,
          "34": 0.0,
          "35": 0.0,
          "36": 0.0,
          "37": 0.0,
          "38": 0.0,
          "39": 0.0,
          "40": 0.0,
          "41": 1.0,
          "42": 0.0,
          "43": 0.0,
          "44": 0.0,
          "45": 0.0,
          "46": 1.0,
          "47": 0.0
        },
        {
          "0": 0.747157,
          "1": -0.162525,
          "12": 0.156311,
          "13": 0.178459,
          "14": -0.036193,
          "15": 0.333029,
          "16": 0.008915,
          "17": -0.001665,
          "18": -0.001833,
          "19": -0.009135
        }
      ]
    }
  ]
}

Recent trials:
[
  {
    "candidate": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_3_vs_1_with_keeper/20260716_190252/iteration/academy_3_vs_1_with_keeper/20260716_190252/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "academy_3_vs_1_with_keeper",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-16T19:10:29+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_3_vs_1_with_keeper/20260716_190252/iteration/academy_3_vs_1_with_keeper/20260716_190252/candidates/iter_000/comm_init.py",
      "documented_obs_dim": 26,
      "map_name": "academy_3_vs_1_with_keeper",
      "matrix_edge_rate": 0.0,
      "matrix_max": 0.0,
      "matrix_min": 0.0,
      "message_dim": 48,
      "valid": true,
      "validation_obs_dim": 48,
      "validation_obs_source": "rollout",
      "what_dim": 48,
      "when_edge_rate": 1.0,
      "who_edge_rate": 0.0
    }
  },
  {
    "candidate": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_3_vs_1_with_keeper/20260716_190252/iteration/academy_3_vs_1_with_keeper/20260716_190252/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "academy_3_vs_1_with_keeper",
    "matrix_edge_rate": 0.2265625,
    "message_dim": 48,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-16T19:10:29+00:00",
    "valid": true,
    "when_edge_rate": 1.0,
    "who_edge_rate": 0.2265625
  }
]

Candidate code:
```python
import torch

def message_design_instruction() -> str:
    return (
        "Agents dynamically partition into ball carrier (ball distance < 0.15) and off-ball receivers (>= 0.15). "
        "Ball carrier broadcasts its agent_id and previous action to all off-ball receivers. "
        "Off-ball receivers broadcast their absolute position and opponent relative positions/directions to the ball carrier."
    )

def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a binary matrix of shape [batch, receiver, sender] indicating which
    sender-receiver pairs are eligible for communication.
    """
    B, N, _ = o.shape
    device = o.device

    # Compute ball distance for each agent
    ball_dist = torch.norm(o[..., 20:22], dim=-1)  # [B, N]

    # Group membership (mutually exclusive except possible boundary)
    is_G1 = ball_dist < 0.15   # ball carrier
    is_G2 = ball_dist >= 0.15  # off-ball receiver

    # RULE R1, R5: ball carrier (G1) -> off-ball receivers (G2)
    # RULE R2, R3, R4: off-ball (G2) -> ball carrier (G1)
    # Edges: G1->G2 and G2->G1, zero self-communication
    G1_to_G2 = is_G2.unsqueeze(1) * is_G1.unsqueeze(2)  # [B, N, N]
    G2_to_G1 = is_G1.unsqueeze(1) * is_G2.unsqueeze(2)  # [B, N, N]
    who = torch.logical_or(G1_to_G2, G2_to_G1).to(dtype=torch.float32)

    # Zero out diagonal (no self-communication)
    diag = torch.eye(N, device=device, dtype=who.dtype).unsqueeze(0)
    who = who * (1.0 - diag)
    return who


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a binary matrix of shape [batch, receiver, sender] indicating whether
    the sender currently wishes to communicate.
    """
    B, N, _ = o.shape
    device = o.device

    ball_dist = torch.norm(o[..., 20:22], dim=-1)  # [B, N]
    is_G1 = ball_dist < 0.15
    is_G2 = ball_dist >= 0.15

    # RULE R1, R5: sender condition is ball_distance < 0.15 (i.e., sender is G1)
    # RULE R2, R3, R4: sender condition is ball_distance >= 0.15 (i.e., sender is G2)
    # Combine: any sender that belongs to a group communicates when it satisfies its group membership.
    when = is_G1.unsqueeze(1).expand(B, N, N).float() + is_G2.unsqueeze(1).expand(B, N, N).float()
    when = when.clamp(0.0, 1.0)

    # No self-communication
    diag = torch.eye(N, device=device, dtype=when.dtype).unsqueeze(0)
    when = when * (1.0 - diag)
    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns an obs-aligned content mask of shape [batch, n_agents, obs_dim].
    Features to be transmitted are set to 1; all others are 0.
    """
    B, N, D = o.shape
    device = o.device

    ball_dist = torch.norm(o[..., 20:22], dim=-1)  # [B, N]
    is_G1 = ball_dist < 0.15   # ball carrier group
    is_G2 = ball_dist >= 0.15  # off-ball receiver group

    mask = torch.zeros(B, N, D, device=device, dtype=torch.float32)

    # RULE R1: ball carrier sends agent_id_one_hot (indices 45,46,47)
    mask[:, :, [45, 46, 47]] = is_G1.unsqueeze(-1).float().expand(-1, -1, 3)

    # RULE R5: ball carrier sends previous_action_one_hot (indices 26..44)
    mask[:, :, 26:45] = is_G1.unsqueeze(-1).float().expand(-1, -1, 19)

    # RULE R2: off-ball receiver sends ego_absolute_xy (indices 0,1)
    mask[:, :, [0, 1]] = is_G2.unsqueeze(-1).float().expand(-1, -1, 2)

    # RULE R3: off-ball receiver sends opponent_0_relative_xy (12,13) and opponent_1_relative_xy (14,15)
    mask[:, :, 12:14] = is_G2.unsqueeze(-1).float().expand(-1, -1, 2)
    mask[:, :, 14:16] = is_G2.unsqueeze(-1).float().expand(-1, -1, 2)

    # RULE R4: off-ball receiver sends opponent_0_direction_xy (16,17) and opponent_1_direction_xy (18,19)
    mask[:, :, 16:18] = is_G2.unsqueeze(-1).float().expand(-1, -1, 2)
    mask[:, :, 18:20] = is_G2.unsqueeze(-1).float().expand(-1, -1, 2)

    return mask
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
