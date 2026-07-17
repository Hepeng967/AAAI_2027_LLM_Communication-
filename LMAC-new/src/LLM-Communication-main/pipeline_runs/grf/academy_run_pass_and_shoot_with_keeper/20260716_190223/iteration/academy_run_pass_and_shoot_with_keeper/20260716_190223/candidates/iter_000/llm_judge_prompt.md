## system

You are an expert MARL communication-policy judge. Evaluate the generated policy only from the task spec, code, and interface validation. Return one JSON object only.

## user

Evaluate this pure LLM-generated LMAC communication strategy for task `academy_run_pass_and_shoot_with_keeper`
in environment `grf`.

Research goal:
- We are testing the capability boundary of LLM-designed communication.
- Do NOT use DRC, decision_sufficient, causally_useful, downstream RL win-rate, or hidden/global state.
- Judge whether the policy gives a plausible pure communication strategy for who, when, and what.

Map spec:
{
  "environment": "grf",
  "n_agents": 2,
  "n_enemies": 2,
  "n_actions": 19,
  "obs_dim": 43,
  "documented_raw_obs_dim": 22,
  "time_seq": 10,
  "objective": "Two attackers coordinate a run-pass-and-shoot sequence against one field defender and a goalkeeper.",
  "raw_feature_semantics": "ego position/direction, teammate relative position/direction, opponent relative positions/directions, and ball relative position/direction"
}

Rollout-backed LMAC observation alignment:
{
  "map_name": "academy_run_pass_and_shoot_with_keeper",
  "rollout_root": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf",
  "files": [
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0000.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0001.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0002.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0003.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0004.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0005.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0006.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0007.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0008.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0009.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0010.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0011.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0012.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0013.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0014.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0015.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0016.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0017.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0018.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0019.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0020.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0021.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0022.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0023.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0024.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0025.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0026.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0027.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0028.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0029.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0030.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0031.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0032.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0033.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0034.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0035.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0036.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0037.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0038.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0039.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0040.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0041.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0042.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0043.pkl"
  ],
  "available": true,
  "n_agents": 2,
  "raw_obs_dim": 22,
  "rollout_obs_dim": 43,
  "documented_obs_dim": 22,
  "extra_obs_dim": 0,
  "episodes": 44,
  "transitions": 3016,
  "seq_lengths": [
    42,
    97,
    24,
    28,
    55,
    52,
    34,
    131,
    43,
    35,
    28,
    84,
    47,
    107,
    29,
    110,
    81,
    43,
    52,
    137,
    98,
    50,
    59,
    125,
    90,
    63,
    76,
    49,
    119,
    37,
    100,
    39,
    85,
    27,
    104,
    24,
    124,
    120,
    97,
    60,
    50,
    63,
    59,
    39
  ],
  "action_dim": 19,
  "agent_types": [
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
    "ego_direction_xy": [
      4,
      6
    ],
    "teammate_0_direction_xy": [
      6,
      8
    ],
    "opponent_0_relative_xy": [
      8,
      10
    ],
    "opponent_1_relative_xy": [
      10,
      12
    ],
    "opponent_0_direction_xy": [
      12,
      14
    ],
    "opponent_1_direction_xy": [
      14,
      16
    ],
    "ball_relative_xy": [
      16,
      18
    ],
    "ball_z": [
      18,
      19
    ],
    "ball_direction_xyz": [
      19,
      22
    ],
    "previous_action_0": [
      22,
      23
    ],
    "previous_action_1": [
      23,
      24
    ],
    "previous_action_2": [
      24,
      25
    ],
    "previous_action_3": [
      25,
      26
    ],
    "previous_action_4": [
      26,
      27
    ],
    "previous_action_5": [
      27,
      28
    ],
    "previous_action_6": [
      28,
      29
    ],
    "previous_action_7": [
      29,
      30
    ],
    "previous_action_8": [
      30,
      31
    ],
    "previous_action_9": [
      31,
      32
    ],
    "previous_action_10": [
      32,
      33
    ],
    "previous_action_11": [
      33,
      34
    ],
    "previous_action_12": [
      34,
      35
    ],
    "previous_action_13": [
      35,
      36
    ],
    "previous_action_14": [
      36,
      37
    ],
    "previous_action_15": [
      37,
      38
    ],
    "previous_action_16": [
      38,
      39
    ],
    "previous_action_17": [
      39,
      40
    ],
    "previous_action_18": [
      40,
      41
    ],
    "agent_id_0": [
      41,
      42
    ],
    "agent_id_1": [
      42,
      43
    ]
  },
  "feature_statistics": {
    "ball_z": {
      "index": 18,
      "min": -0.104609,
      "max": 7.786302,
      "mean": 0.266794,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.475281,
      "nonzero_rate": 0.462158
    },
    "previous_action_0": {
      "index": 22,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.022461,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.022461
    },
    "previous_action_1": {
      "index": 23,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.022339,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.022339
    },
    "previous_action_2": {
      "index": 24,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021606,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021606
    },
    "previous_action_3": {
      "index": 25,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.022583,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.022583
    },
    "previous_action_4": {
      "index": 26,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.022217,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.022217
    },
    "previous_action_5": {
      "index": 27,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.023804,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.023804
    },
    "previous_action_6": {
      "index": 28,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.02356,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02356
    },
    "previous_action_7": {
      "index": 29,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.022095,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.022095
    },
    "previous_action_8": {
      "index": 30,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.030273,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.030273
    },
    "previous_action_9": {
      "index": 31,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.026733,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.026733
    },
    "previous_action_10": {
      "index": 32,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.022705,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.022705
    },
    "previous_action_11": {
      "index": 33,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.026855,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.026855
    },
    "previous_action_12": {
      "index": 34,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.024536,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.024536
    },
    "previous_action_13": {
      "index": 35,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.024292,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.024292
    },
    "previous_action_14": {
      "index": 36,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.022461,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.022461
    },
    "previous_action_15": {
      "index": 37,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.030762,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.030762
    },
    "previous_action_16": {
      "index": 38,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.02356,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02356
    },
    "previous_action_17": {
      "index": 39,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.024414,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.024414
    },
    "previous_action_18": {
      "index": 40,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.024658,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.024658
    },
    "agent_id_0": {
      "index": 41,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.5,
      "p05": 0.0,
      "p50": 0.5,
      "p95": 1.0,
      "nonzero_rate": 0.5
    },
    "agent_id_1": {
      "index": 42,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.5,
      "p05": 0.0,
      "p50": 0.5,
      "p95": 1.0,
      "nonzero_rate": 0.5
    }
  },
  "alignment_note": "rollout_obs_dim is exactly the RL communication input: raw observation + previous-action one-hot + agent-id one-hot. Feature positions are identical in offline evaluation and RL training."
}

Interface validation:
{
  "valid": true,
  "map_name": "academy_run_pass_and_shoot_with_keeper",
  "comm_code": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223/iteration/academy_run_pass_and_shoot_with_keeper/20260716_190223/candidates/iter_000/comm_init.py",
  "validation_obs_source": "rollout",
  "validation_obs_dim": 43,
  "documented_obs_dim": 22,
  "message_dim": 43,
  "matrix_edge_rate": 1.0,
  "who_edge_rate": 1.0,
  "when_edge_rate": 1.0,
  "what_dim": 43,
  "matrix_min": 0.0,
  "matrix_max": 1.0
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "academy_run_pass_and_shoot_with_keeper",
  "comm_code": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223/iteration/academy_run_pass_and_shoot_with_keeper/20260716_190223/candidates/iter_000/comm_init.py",
  "files": [
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0000.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0001.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0002.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0003.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0004.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0005.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0006.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0007.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0008.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0009.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0010.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0011.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0012.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0013.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0014.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0015.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0016.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0017.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0018.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0019.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0020.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0021.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0022.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0023.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0024.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0025.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0026.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/grf/academy_run_pass_and_shoot_with_keeper/train_traj_0027.pkl"
  ],
  "transitions": 4096,
  "n_agents": 2,
  "rollout_obs_dim": 43,
  "message_dim": 43,
  "matrix_edge_rate": 0.674560546875,
  "who_edge_rate": 1.0,
  "when_edge_rate": 0.674560546875,
  "message_nonzero_rate": 0.16279069767441862,
  "message_abs_mean": 0.16279069767441862,
  "active_sender_what_coverage_mean": 0.16279070773419807,
  "active_sender_what_coverage_min": 0.1627907007932663,
  "active_sender_count": 5526,
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
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.707721,
          "1": -0.0,
          "16": -0.007721,
          "17": -0.28,
          "19": -0.0,
          "20": 0.0,
          "21": 0.006164
        },
        {
          "0": 0.707721,
          "1": -0.30488,
          "16": -0.007721,
          "17": 0.02488,
          "19": -0.0,
          "20": 0.0,
          "21": 0.006164
        }
      ]
    },
    {
      "case_id": "train_traj_0000:13",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.647107,
          "1": -0.037692,
          "16": 0.013529,
          "17": -0.116495,
          "19": -0.006682,
          "20": 0.022743,
          "21": 0.079488
        },
        {
          "0": 0.692508,
          "1": -0.264477,
          "16": -0.031872,
          "17": 0.11029,
          "19": -0.006682,
          "20": 0.022743,
          "21": 0.079488
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
          1,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.610065,
          "1": -0.087286,
          "16": -0.004016,
          "17": -0.096058,
          "19": -0.000284,
          "20": -0.021276,
          "21": 0.137359
        },
        {
          "0": 0.640356,
          "1": -0.276481,
          "16": -0.034308,
          "17": 0.093138,
          "19": -0.000284,
          "20": -0.021276,
          "21": 0.137359
        }
      ]
    },
    {
      "case_id": "train_traj_0000:40",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.63302,
          "1": -0.156613,
          "16": -0.001128,
          "17": -0.255406,
          "19": 0.00306,
          "20": -0.011903,
          "21": 0.097883
        },
        {
          "0": 0.638231,
          "1": -0.371119,
          "16": -0.006338,
          "17": -0.0409,
          "19": 0.00306,
          "20": -0.011903,
          "21": 0.097883
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
          1,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        },
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:67",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          1,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        },
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
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
          1,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        },
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:94",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          1,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        },
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:108",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          1,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        },
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:121",
      "active_edges_receiver_sender": [
        [
          0,
          1
        ],
        [
          1,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        },
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
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
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        },
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
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
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ],
        [
          0,
          1,
          16,
          17,
          19,
          20,
          21
        ]
      ],
      "what_coverage_by_sender": [
        0.162791,
        0.162791
      ],
      "selected_values_by_sender": [
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        },
        {
          "0": 0.0,
          "1": 0.0,
          "16": 0.0,
          "17": 0.0,
          "19": 0.0,
          "20": 0.0,
          "21": 0.0
        }
      ]
    }
  ]
}

Recent trials:
[
  {
    "candidate": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223/iteration/academy_run_pass_and_shoot_with_keeper/20260716_190223/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "academy_run_pass_and_shoot_with_keeper",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-16T19:08:48+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223/iteration/academy_run_pass_and_shoot_with_keeper/20260716_190223/candidates/iter_000/comm_init.py",
      "documented_obs_dim": 22,
      "map_name": "academy_run_pass_and_shoot_with_keeper",
      "matrix_edge_rate": 1.0,
      "matrix_max": 1.0,
      "matrix_min": 0.0,
      "message_dim": 43,
      "valid": true,
      "validation_obs_dim": 43,
      "validation_obs_source": "rollout",
      "what_dim": 43,
      "when_edge_rate": 1.0,
      "who_edge_rate": 1.0
    }
  },
  {
    "candidate": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223/iteration/academy_run_pass_and_shoot_with_keeper/20260716_190223/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "academy_run_pass_and_shoot_with_keeper",
    "matrix_edge_rate": 0.674560546875,
    "message_dim": 43,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-16T19:08:48+00:00",
    "valid": true,
    "when_edge_rate": 0.674560546875,
    "who_edge_rate": 1.0
  }
]

Candidate code:
```python
import torch

def message_design_instruction() -> str:
    """
    Concise description of the communication policy.
    """
    return (
        "Symmetric attacker group G1: when an agent has ball possession "
        "(ball distance < 0.1), it sends its absolute position, ball relative "
        "position, and ball direction to the other attacker to coordinate "
        "run-pass-shoot intentions."
    )

# ----------------------------------------------------------------------
# RULE R1
# Symmetric attackers (agent 0 and agent 1) from group G1.
# Sender: any agent that possesses the ball (ball_relative_xy norm < 0.1).
# Receiver: the other agent (teammate).
# Content: ego_absolute_xy (indices 0,1), ball_relative_xy (16,17),
#          ball_direction_xyz (19,20,21).
# ----------------------------------------------------------------------

def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns sender-receiver connectivity matrix.
    Shape: [batch, n_agents, n_agents] with 1 for teammate edges, 0 otherwise.
    Diagonal is zero (no self-communication).
    """
    # RULE R1
    batch, n_agents, _ = o.shape
    # For two symmetric attackers, teammate of agent 0 is 1 and vice versa.
    # Base matrix: anti-diagonal ones.
    base_who = torch.tensor([[0., 1.],
                             [1., 0.]], device=o.device, dtype=torch.float32)
    # Expand to batch dimension
    who = base_who.unsqueeze(0).expand(batch, -1, -1)
    return who

def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns temporal activation for each sender-receiver pair.
    Shape: [batch, n_agents, n_agents] with 1 if sender has ball close,
    0 otherwise, and zero on the diagonal.
    """
    # RULE R1
    batch, n_agents, _ = o.shape
    # Ball distance: ||ball_relative_xy|| (indices 16,17)
    ball_vec = o[..., 16:18]                     # [batch, n_agents, 2]
    ball_dist = torch.norm(ball_vec, dim=-1)     # [batch, n_agents]
    active_sender = (ball_dist < 0.1).float()    # [batch, n_agents]

    # Create when matrix: for sender s, value active_sender[b,s] for all receivers
    when = active_sender.unsqueeze(1).expand(-1, n_agents, -1)  # [batch, n_agents, n_agents]
    # Remove self-communication by zeroing the diagonal
    eye = torch.eye(n_agents, device=o.device).unsqueeze(0)     # [1, n_agents, n_agents]
    when = when * (1.0 - eye)

    return when

def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a mask that selects which observation features to send.
    Shape matches o: [batch, n_agents, obs_dim], with 1 at selected indices,
    0 elsewhere.
    """
    # RULE R1
    obs_dim = o.shape[-1]
    mask = torch.zeros_like(o)
    # Selected indices from the specification
    feature_indices = torch.tensor([0, 1, 16, 17, 19, 20, 21], device=o.device)
    # Filter out indices that are out of bounds (vectorized)
    valid_mask = feature_indices < obs_dim
    valid_indices = feature_indices[valid_mask]   # tensor of valid ints
    # Set selected feature positions to 1 for all agents and batches
    mask[:, :, valid_indices] = 1.0
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
