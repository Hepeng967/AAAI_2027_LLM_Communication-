## system

You are an expert MARL communication-policy judge. Evaluate the generated policy only from the task spec, code, and interface validation. Return one JSON object only.

## user

Evaluate this pure LLM-generated LMAC communication strategy for SMAC map `1o_10b_vs_1r`.

Research goal:
- We are testing the capability boundary of LLM-designed communication.
- Do NOT use DRC, decision_sufficient, causally_useful, downstream RL win-rate, or hidden/global state.
- Judge whether the policy gives a plausible pure communication strategy for who, when, and what.

Map spec:
{
  "n_agents": 11,
  "obs_dim": 103,
  "time_seq": 10,
  "expected_sender_rate": 0.09090909090909091,
  "critical_receivers": [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9
  ],
  "critical_senders": [
    10
  ]
}

Rollout-backed LMAC observation alignment:
{
  "map_name": "1o_10b_vs_1r",
  "rollout_root": "/data/hp/LLM_Communication/LMAC-new/data",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0000.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0001.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0002.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0003.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0004.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0005.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0006.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0007.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0008.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0009.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0010.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0011.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0012.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0013.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0014.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0015.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0016.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0017.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0018.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0019.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0020.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0021.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0022.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0023.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0024.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0025.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0026.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0027.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0028.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0029.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0030.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0031.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0032.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0033.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0034.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0035.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0036.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0037.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0038.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0039.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0040.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0041.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0042.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0043.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0044.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0045.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0046.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0047.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0048.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0049.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0050.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0051.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0052.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0053.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0054.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0055.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0056.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0057.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0058.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0059.pkl"
  ],
  "available": true,
  "n_agents": 11,
  "raw_obs_dim": 85,
  "rollout_obs_dim": 103,
  "documented_obs_dim": 84,
  "extra_obs_dim": 1,
  "episodes": 60,
  "transitions": 3000,
  "seq_lengths": [
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50
  ],
  "action_dim": 7,
  "agent_types": [
    "baneling",
    "baneling",
    "baneling",
    "baneling",
    "baneling",
    "baneling",
    "baneling",
    "baneling",
    "baneling",
    "baneling",
    "overseer"
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
    "enemy_0_type_0": [
      9,
      10
    ],
    "enemy_0_type_1": [
      10,
      11
    ],
    "ally_0_visible": [
      11,
      12
    ],
    "ally_0_distance": [
      12,
      13
    ],
    "ally_0_rel_x": [
      13,
      14
    ],
    "ally_0_rel_y": [
      14,
      15
    ],
    "ally_0_health": [
      15,
      16
    ],
    "ally_0_type_0": [
      16,
      17
    ],
    "ally_0_type_1": [
      17,
      18
    ],
    "ally_1_visible": [
      18,
      19
    ],
    "ally_1_distance": [
      19,
      20
    ],
    "ally_1_rel_x": [
      20,
      21
    ],
    "ally_1_rel_y": [
      21,
      22
    ],
    "ally_1_health": [
      22,
      23
    ],
    "ally_1_type_0": [
      23,
      24
    ],
    "ally_1_type_1": [
      24,
      25
    ],
    "ally_2_visible": [
      25,
      26
    ],
    "ally_2_distance": [
      26,
      27
    ],
    "ally_2_rel_x": [
      27,
      28
    ],
    "ally_2_rel_y": [
      28,
      29
    ],
    "ally_2_health": [
      29,
      30
    ],
    "ally_2_type_0": [
      30,
      31
    ],
    "ally_2_type_1": [
      31,
      32
    ],
    "ally_3_visible": [
      32,
      33
    ],
    "ally_3_distance": [
      33,
      34
    ],
    "ally_3_rel_x": [
      34,
      35
    ],
    "ally_3_rel_y": [
      35,
      36
    ],
    "ally_3_health": [
      36,
      37
    ],
    "ally_3_type_0": [
      37,
      38
    ],
    "ally_3_type_1": [
      38,
      39
    ],
    "ally_4_visible": [
      39,
      40
    ],
    "ally_4_distance": [
      40,
      41
    ],
    "ally_4_rel_x": [
      41,
      42
    ],
    "ally_4_rel_y": [
      42,
      43
    ],
    "ally_4_health": [
      43,
      44
    ],
    "ally_4_type_0": [
      44,
      45
    ],
    "ally_4_type_1": [
      45,
      46
    ],
    "ally_5_visible": [
      46,
      47
    ],
    "ally_5_distance": [
      47,
      48
    ],
    "ally_5_rel_x": [
      48,
      49
    ],
    "ally_5_rel_y": [
      49,
      50
    ],
    "ally_5_health": [
      50,
      51
    ],
    "ally_5_type_0": [
      51,
      52
    ],
    "ally_5_type_1": [
      52,
      53
    ],
    "ally_6_visible": [
      53,
      54
    ],
    "ally_6_distance": [
      54,
      55
    ],
    "ally_6_rel_x": [
      55,
      56
    ],
    "ally_6_rel_y": [
      56,
      57
    ],
    "ally_6_health": [
      57,
      58
    ],
    "ally_6_type_0": [
      58,
      59
    ],
    "ally_6_type_1": [
      59,
      60
    ],
    "ally_7_visible": [
      60,
      61
    ],
    "ally_7_distance": [
      61,
      62
    ],
    "ally_7_rel_x": [
      62,
      63
    ],
    "ally_7_rel_y": [
      63,
      64
    ],
    "ally_7_health": [
      64,
      65
    ],
    "ally_7_type_0": [
      65,
      66
    ],
    "ally_7_type_1": [
      66,
      67
    ],
    "ally_8_visible": [
      67,
      68
    ],
    "ally_8_distance": [
      68,
      69
    ],
    "ally_8_rel_x": [
      69,
      70
    ],
    "ally_8_rel_y": [
      70,
      71
    ],
    "ally_8_health": [
      71,
      72
    ],
    "ally_8_type_0": [
      72,
      73
    ],
    "ally_8_type_1": [
      73,
      74
    ],
    "ally_9_visible": [
      74,
      75
    ],
    "ally_9_distance": [
      75,
      76
    ],
    "ally_9_rel_x": [
      76,
      77
    ],
    "ally_9_rel_y": [
      77,
      78
    ],
    "ally_9_health": [
      78,
      79
    ],
    "ally_9_type_0": [
      79,
      80
    ],
    "ally_9_type_1": [
      80,
      81
    ],
    "own_health": [
      81,
      82
    ],
    "own_type_0": [
      82,
      83
    ],
    "own_type_1": [
      83,
      84
    ],
    "lmac_extra_84": [
      84,
      85
    ],
    "previous_action_0": [
      85,
      86
    ],
    "previous_action_1": [
      86,
      87
    ],
    "previous_action_2": [
      87,
      88
    ],
    "previous_action_3": [
      88,
      89
    ],
    "previous_action_4": [
      89,
      90
    ],
    "previous_action_5": [
      90,
      91
    ],
    "previous_action_6": [
      91,
      92
    ],
    "agent_id_0": [
      92,
      93
    ],
    "agent_id_1": [
      93,
      94
    ],
    "agent_id_2": [
      94,
      95
    ],
    "agent_id_3": [
      95,
      96
    ],
    "agent_id_4": [
      96,
      97
    ],
    "agent_id_5": [
      97,
      98
    ],
    "agent_id_6": [
      98,
      99
    ],
    "agent_id_7": [
      99,
      100
    ],
    "agent_id_8": [
      100,
      101
    ],
    "agent_id_9": [
      101,
      102
    ],
    "agent_id_10": [
      102,
      103
    ]
  },
  "feature_statistics": {
    "move_north": {
      "index": 0,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.81097,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.81097
    },
    "move_south": {
      "index": 1,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.790576,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.790576
    },
    "move_east": {
      "index": 2,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.794333,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.794333
    },
    "move_west": {
      "index": 3,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.788545,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.788545
    },
    "enemy_0_available": {
      "index": 4,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.104394,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.104394
    },
    "enemy_0_distance": {
      "index": 5,
      "min": 0.0,
      "max": 0.99977,
      "mean": 0.031446,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.167086,
      "nonzero_rate": 0.120364
    },
    "enemy_0_rel_x": {
      "index": 6,
      "min": -0.949653,
      "max": 0.990479,
      "mean": 0.001648,
      "p05": -0.002253,
      "p50": 0.0,
      "p95": 0.035211,
      "nonzero_rate": 0.117061
    },
    "enemy_0_rel_y": {
      "index": 7,
      "min": -0.997504,
      "max": 0.996691,
      "mean": -0.007201,
      "p05": -0.059794,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.119576
    },
    "enemy_0_health": {
      "index": 8,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.112831,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.121182
    },
    "enemy_0_type_0": {
      "index": 9,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.121182,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.121182
    },
    "enemy_0_type_1": {
      "index": 10,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_0_visible": {
      "index": 11,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_0_distance": {
      "index": 12,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.142909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.142909
    },
    "ally_0_rel_x": {
      "index": 13,
      "min": 0.0,
      "max": 0.999709,
      "mean": 0.0833,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.724975,
      "nonzero_rate": 0.142909
    },
    "ally_0_rel_y": {
      "index": 14,
      "min": -0.996528,
      "max": 0.929362,
      "mean": -0.01652,
      "p05": -0.212077,
      "p50": 0.0,
      "p95": 0.038194,
      "nonzero_rate": 0.141364
    },
    "ally_0_health": {
      "index": 15,
      "min": -0.995904,
      "max": 0.990207,
      "mean": -0.005485,
      "p05": -0.285158,
      "p50": 0.0,
      "p95": 0.1536,
      "nonzero_rate": 0.142545
    },
    "ally_0_type_0": {
      "index": 16,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.142334,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.142909
    },
    "ally_0_type_1": {
      "index": 17,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_1_visible": {
      "index": 18,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.142909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.142909
    },
    "ally_1_distance": {
      "index": 19,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.137909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.137909
    },
    "ally_1_rel_x": {
      "index": 20,
      "min": 0.0,
      "max": 0.999973,
      "mean": 0.084409,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.755679,
      "nonzero_rate": 0.137909
    },
    "ally_1_rel_y": {
      "index": 21,
      "min": -0.996636,
      "max": 0.982286,
      "mean": -0.019992,
      "p05": -0.28785,
      "p50": 0.0,
      "p95": 0.004391,
      "nonzero_rate": 0.136788
    },
    "ally_1_health": {
      "index": 22,
      "min": -0.994466,
      "max": 0.99688,
      "mean": -0.000269,
      "p05": -0.193273,
      "p50": 0.0,
      "p95": 0.153347,
      "nonzero_rate": 0.137455
    },
    "ally_1_type_0": {
      "index": 23,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.137351,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.137909
    },
    "ally_1_type_1": {
      "index": 24,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_2_visible": {
      "index": 25,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.137909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.137909
    },
    "ally_2_distance": {
      "index": 26,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.149273,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.149273
    },
    "ally_2_rel_x": {
      "index": 27,
      "min": 0.0,
      "max": 0.999973,
      "mean": 0.087134,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.763428,
      "nonzero_rate": 0.149273
    },
    "ally_2_rel_y": {
      "index": 28,
      "min": -0.994954,
      "max": 0.990858,
      "mean": -0.007783,
      "p05": -0.21494,
      "p50": 0.0,
      "p95": 0.138889,
      "nonzero_rate": 0.14803
    },
    "ally_2_health": {
      "index": 29,
      "min": -0.998074,
      "max": 0.998291,
      "mean": -0.002232,
      "p05": -0.199002,
      "p50": 0.0,
      "p95": 0.175491,
      "nonzero_rate": 0.148636
    },
    "ally_2_type_0": {
      "index": 30,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.148476,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.149273
    },
    "ally_2_type_1": {
      "index": 31,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_3_visible": {
      "index": 32,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.149273,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.149273
    },
    "ally_3_distance": {
      "index": 33,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.173121,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.173121
    },
    "ally_3_rel_x": {
      "index": 34,
      "min": 0.0,
      "max": 0.999868,
      "mean": 0.099368,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.772044,
      "nonzero_rate": 0.173121
    },
    "ally_3_rel_y": {
      "index": 35,
      "min": -0.99585,
      "max": 0.987657,
      "mean": -0.004504,
      "p05": -0.27888,
      "p50": 0.0,
      "p95": 0.233615,
      "nonzero_rate": 0.173061
    },
    "ally_3_health": {
      "index": 36,
      "min": -0.993924,
      "max": 0.993924,
      "mean": 0.004739,
      "p05": -0.212918,
      "p50": 0.0,
      "p95": 0.277941,
      "nonzero_rate": 0.172182
    },
    "ally_3_type_0": {
      "index": 37,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.172753,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.173121
    },
    "ally_3_type_1": {
      "index": 38,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_4_visible": {
      "index": 39,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.173121,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.173121
    },
    "ally_4_distance": {
      "index": 40,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.183,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.183
    },
    "ally_4_rel_x": {
      "index": 41,
      "min": 0.0,
      "max": 0.999865,
      "mean": 0.110984,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.805981,
      "nonzero_rate": 0.183
    },
    "ally_4_rel_y": {
      "index": 42,
      "min": -0.998888,
      "max": 0.996528,
      "mean": -0.002875,
      "p05": -0.327542,
      "p50": 0.0,
      "p95": 0.294271,
      "nonzero_rate": 0.182515
    },
    "ally_4_health": {
      "index": 43,
      "min": -0.990072,
      "max": 0.984239,
      "mean": 0.002161,
      "p05": -0.256411,
      "p50": 0.0,
      "p95": 0.276367,
      "nonzero_rate": 0.182242
    },
    "ally_4_type_0": {
      "index": 44,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.182775,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.183
    },
    "ally_4_type_1": {
      "index": 45,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_5_visible": {
      "index": 46,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.183,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.183
    },
    "ally_5_distance": {
      "index": 47,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.158576,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.158576
    },
    "ally_5_rel_x": {
      "index": 48,
      "min": 0.0,
      "max": 0.99971,
      "mean": 0.097103,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.785076,
      "nonzero_rate": 0.158576
    },
    "ally_5_rel_y": {
      "index": 49,
      "min": -0.995877,
      "max": 0.996636,
      "mean": 0.003851,
      "p05": -0.208198,
      "p50": 0.0,
      "p95": 0.229069,
      "nonzero_rate": 0.158394
    },
    "ally_5_health": {
      "index": 50,
      "min": -0.99094,
      "max": 0.995497,
      "mean": 0.008205,
      "p05": -0.147553,
      "p50": 0.0,
      "p95": 0.283556,
      "nonzero_rate": 0.157485
    },
    "ally_5_type_0": {
      "index": 51,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.158065,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.158576
    },
    "ally_5_type_1": {
      "index": 52,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_6_visible": {
      "index": 53,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.158576,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.158576
    },
    "ally_6_distance": {
      "index": 54,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.171091,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.171091
    },
    "ally_6_rel_x": {
      "index": 55,
      "min": 0.0,
      "max": 0.999559,
      "mean": 0.10097,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.770996,
      "nonzero_rate": 0.171091
    },
    "ally_6_rel_y": {
      "index": 56,
      "min": -0.997179,
      "max": 0.998888,
      "mean": 0.016243,
      "p05": -0.154744,
      "p50": 0.0,
      "p95": 0.346734,
      "nonzero_rate": 0.170788
    },
    "ally_6_health": {
      "index": 57,
      "min": -0.988742,
      "max": 0.986979,
      "mean": 0.001231,
      "p05": -0.235971,
      "p50": 0.0,
      "p95": 0.276008,
      "nonzero_rate": 0.17097
    },
    "ally_6_type_0": {
      "index": 58,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.170404,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.171091
    },
    "ally_6_type_1": {
      "index": 59,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_7_visible": {
      "index": 60,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.171091,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.171091
    },
    "ally_7_distance": {
      "index": 61,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.150879,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.150879
    },
    "ally_7_rel_x": {
      "index": 62,
      "min": 0.0,
      "max": 0.999731,
      "mean": 0.086683,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.738455,
      "nonzero_rate": 0.150879
    },
    "ally_7_rel_y": {
      "index": 63,
      "min": -0.979167,
      "max": 0.997179,
      "mean": 0.012042,
      "p05": -0.099013,
      "p50": 0.0,
      "p95": 0.23586,
      "nonzero_rate": 0.149758
    },
    "ally_7_health": {
      "index": 64,
      "min": -0.996663,
      "max": 0.988742,
      "mean": -0.005672,
      "p05": -0.236057,
      "p50": 0.0,
      "p95": 0.177083,
      "nonzero_rate": 0.150758
    },
    "ally_7_type_0": {
      "index": 65,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.150129,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.150879
    },
    "ally_7_type_1": {
      "index": 66,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_8_visible": {
      "index": 67,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.150879,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.150879
    },
    "ally_8_distance": {
      "index": 68,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.151121,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.151121
    },
    "ally_8_rel_x": {
      "index": 69,
      "min": 0.0,
      "max": 0.999865,
      "mean": 0.086213,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.720522,
      "nonzero_rate": 0.151121
    },
    "ally_8_rel_y": {
      "index": 70,
      "min": -0.917508,
      "max": 0.988661,
      "mean": 0.018923,
      "p05": -0.020648,
      "p50": 0.0,
      "p95": 0.242215,
      "nonzero_rate": 0.149121
    },
    "ally_8_health": {
      "index": 71,
      "min": -0.983615,
      "max": 0.996663,
      "mean": 0.001347,
      "p05": -0.23291,
      "p50": 0.0,
      "p95": 0.238135,
      "nonzero_rate": 0.151061
    },
    "ally_8_type_0": {
      "index": 72,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.150192,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.151121
    },
    "ally_8_type_1": {
      "index": 73,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_9_visible": {
      "index": 74,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.151121,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.151121
    },
    "ally_9_distance": {
      "index": 75,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.035515,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.035515
    },
    "ally_9_rel_x": {
      "index": 76,
      "min": 0.0,
      "max": 0.998753,
      "mean": 0.024321,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.035515
    },
    "ally_9_rel_y": {
      "index": 77,
      "min": -0.99452,
      "max": 0.995877,
      "mean": 0.000615,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.035515
    },
    "ally_9_health": {
      "index": 78,
      "min": -0.998291,
      "max": 0.998074,
      "mean": -0.004024,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.035515
    },
    "ally_9_type_0": {
      "index": 79,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.035147,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.035515
    },
    "ally_9_type_1": {
      "index": 80,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.032576,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.032576
    },
    "own_health": {
      "index": 81,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.002939,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.002939
    },
    "own_type_0": {
      "index": 82,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.902779,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.905606
    },
    "own_type_1": {
      "index": 83,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    },
    "lmac_extra_84": {
      "index": 84,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.814697,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.814697
    },
    "previous_action_0": {
      "index": 85,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.091848,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.091848
    },
    "previous_action_1": {
      "index": 86,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.191939,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.191939
    },
    "previous_action_2": {
      "index": 87,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.175424,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.175424
    },
    "previous_action_3": {
      "index": 88,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.164879,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.164879
    },
    "previous_action_4": {
      "index": 89,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.168576,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.168576
    },
    "previous_action_5": {
      "index": 90,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.166515,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.166515
    },
    "previous_action_6": {
      "index": 91,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.020818,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.020818
    },
    "agent_id_0": {
      "index": 92,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    },
    "agent_id_1": {
      "index": 93,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    },
    "agent_id_2": {
      "index": 94,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    },
    "agent_id_3": {
      "index": 95,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    },
    "agent_id_4": {
      "index": 96,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    },
    "agent_id_5": {
      "index": 97,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    },
    "agent_id_6": {
      "index": 98,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    },
    "agent_id_7": {
      "index": 99,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    },
    "agent_id_8": {
      "index": 100,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    },
    "agent_id_9": {
      "index": 101,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    },
    "agent_id_10": {
      "index": 102,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090909,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090909
    }
  },
  "alignment_note": "rollout_obs_dim is exactly the RL communication input: raw observation + previous-action one-hot + agent-id one-hot. Feature positions are identical in offline evaluation and RL training."
}

Interface validation:
{
  "valid": true,
  "map_name": "1o_10b_vs_1r",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455/iteration/1o_10b_vs_1r/20260714_101455/candidates/iter_000/comm_init.py",
  "validation_obs_source": "rollout",
  "validation_obs_dim": 103,
  "documented_obs_dim": 84,
  "message_dim": 103,
  "matrix_edge_rate": 0.0,
  "who_edge_rate": 0.18181818181818182,
  "when_edge_rate": 0.0,
  "what_dim": 103,
  "matrix_min": 0.0,
  "matrix_max": 0.0
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "1o_10b_vs_1r",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455/iteration/1o_10b_vs_1r/20260714_101455/candidates/iter_000/comm_init.py",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0000.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0001.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0002.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0003.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0004.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0005.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0006.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0007.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0008.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0009.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0010.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0011.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0012.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0013.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0014.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0015.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0016.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0017.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0018.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0019.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0020.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0021.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0022.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0023.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0024.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0025.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0026.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0027.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0028.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0029.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0030.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0031.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0032.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0033.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0034.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0035.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0036.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0037.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0038.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0039.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0040.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0041.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0042.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0043.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0044.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0045.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0046.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0047.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0048.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0049.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0050.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0051.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0052.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0053.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0054.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0055.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0056.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0057.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0058.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/1o_10b_vs_1r/train_traj_0059.pkl"
  ],
  "transitions": 3000,
  "n_agents": 11,
  "rollout_obs_dim": 103,
  "message_dim": 103,
  "matrix_edge_rate": 0.15845151515151515,
  "who_edge_rate": 0.18181818181818182,
  "when_edge_rate": 0.15845151515151515,
  "message_nonzero_rate": 0.02030008826125331,
  "message_abs_mean": 0.02030008826125331,
  "active_sender_what_coverage_mean": 0.020569211473441963,
  "active_sender_what_coverage_min": 0.019417475908994675,
  "active_sender_count": 25289,
  "matrix_min": 0.0,
  "matrix_max": 1.0,
  "risk_flags": [],
  "evidence_cases": [
    {
      "case_id": "train_traj_0000:0",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          3
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ],
        [
          10,
          8
        ],
        [
          10,
          9
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.07382,
          "6": 0.055556,
          "7": 0.048611
        }
      ]
    },
    {
      "case_id": "train_traj_0000:4",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          3
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ],
        [
          10,
          8
        ],
        [
          10,
          9
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.081196,
          "6": 0.076118,
          "7": -0.028266
        }
      ]
    },
    {
      "case_id": "train_traj_0000:8",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          3
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ],
        [
          10,
          8
        ],
        [
          10,
          9
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.061824,
          "6": 0.013509,
          "7": -0.06033
        }
      ]
    },
    {
      "case_id": "train_traj_0000:13",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          3
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ],
        [
          10,
          8
        ],
        [
          10,
          9
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.163071,
          "6": -0.005534,
          "7": -0.162977
        }
      ]
    },
    {
      "case_id": "train_traj_0000:17",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          3
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ],
        [
          10,
          8
        ],
        [
          10,
          9
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.153162,
          "6": -0.004232,
          "7": -0.153103
        }
      ]
    },
    {
      "case_id": "train_traj_0000:22",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          0
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          3
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ],
        [
          10,
          8
        ],
        [
          10,
          9
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.928932,
          "14": 0.461507
        },
        {
          "13": 0.928932,
          "14": -0.461507
        },
        {
          "13": 0.958887,
          "14": -0.843858
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.122875,
          "6": -0.023085,
          "7": -0.120687
        }
      ]
    },
    {
      "case_id": "train_traj_0000:26",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ],
        [
          10,
          8
        ],
        [
          10,
          9
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.141629,
          "6": 0.01614,
          "7": -0.140706
        }
      ]
    },
    {
      "case_id": "train_traj_0000:31",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ],
        [
          10,
          8
        ],
        [
          10,
          9
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.194283,
          "6": 0.15842,
          "7": -0.112467
        }
      ]
    },
    {
      "case_id": "train_traj_0000:35",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ],
        [
          10,
          8
        ],
        [
          10,
          9
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.162568,
          "6": 0.121419,
          "7": -0.1081
        }
      ]
    },
    {
      "case_id": "train_traj_0000:40",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ],
        [
          10,
          8
        ],
        [
          10,
          9
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.135798,
          "6": 0.102186,
          "7": -0.089437
        }
      ]
    },
    {
      "case_id": "train_traj_0000:44",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ],
        [
          10,
          8
        ],
        [
          10,
          9
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.097317,
          "6": 0.077393,
          "7": -0.059001
        }
      ]
    },
    {
      "case_id": "train_traj_0000:49",
      "active_edges_receiver_sender": [
        [
          0,
          10
        ],
        [
          1,
          10
        ],
        [
          2,
          10
        ],
        [
          3,
          10
        ],
        [
          4,
          10
        ],
        [
          5,
          10
        ],
        [
          6,
          10
        ],
        [
          7,
          10
        ],
        [
          8,
          10
        ],
        [
          9,
          10
        ],
        [
          10,
          1
        ],
        [
          10,
          2
        ],
        [
          10,
          4
        ],
        [
          10,
          5
        ],
        [
          10,
          6
        ],
        [
          10,
          7
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          13,
          14
        ],
        [
          5,
          6,
          7
        ]
      ],
      "what_coverage_by_sender": [
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.019417,
        0.029126
      ],
      "selected_values_by_sender": [
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "13": 0.0,
          "14": 0.0
        },
        {
          "5": 0.140498,
          "6": 0.073812,
          "7": -0.119548
        }
      ]
    }
  ]
}

Recent trials:
[
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455/iteration/1o_10b_vs_1r/20260714_101455/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "1o_10b_vs_1r",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-14T10:21:52+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455/iteration/1o_10b_vs_1r/20260714_101455/candidates/iter_000/comm_init.py",
      "documented_obs_dim": 84,
      "map_name": "1o_10b_vs_1r",
      "matrix_edge_rate": 0.0,
      "matrix_max": 0.0,
      "matrix_min": 0.0,
      "message_dim": 103,
      "valid": true,
      "validation_obs_dim": 103,
      "validation_obs_source": "rollout",
      "what_dim": 103,
      "when_edge_rate": 0.0,
      "who_edge_rate": 0.18181818181818182
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455/iteration/1o_10b_vs_1r/20260714_101455/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "1o_10b_vs_1r",
    "matrix_edge_rate": 0.15845151515151515,
    "message_dim": 103,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-14T10:21:52+00:00",
    "valid": true,
    "when_edge_rate": 0.15845151515151515,
    "who_edge_rate": 0.18181818181818182
  }
]

Candidate code:
```python
import torch

def message_design_instruction():
    """
    Returns a human-readable instruction describing the communication policy design.
    """
    return (
        "This communication policy coordinates an overseer (agent 10) and 10 banelings (agents 0-9) "
        "on the 1o_10b_vs_1r map. The overseer broadcasts enemy location (distance, relative x, y) "
        "to all banelings only when an enemy (roach) is detected (enemy_0_available == 1). "
        "Each baneling relays its own relative position (ally_0_rel_x, ally_0_rel_y) to the overseer "
        "only when it sees at least one other ally (max(ally_i_visible) > 0.5), providing the overseer "
        "with positional awareness of the swarm."
    )


def communication_who(o):
    """
    Returns who can communicate: static edges based on agent roles.
    Shape: [batch, n_agents, n_agents] in [0,1].
    """
    batch, n_agents, obs_dim = o.shape
    # Build static connectivity matrix (receivers x senders)
    who = torch.zeros((n_agents, n_agents), device=o.device, dtype=torch.float32)

    # RULE R1: Overseer (agent 10) broadcasts to Banelings (0-9)
    who[0:10, 10] = 1.0

    # RULE R2: Banelings (0-9) relay to Overseer (10)
    who[10, 0:10] = 1.0

    # Expand to match batch dimension
    who = who.unsqueeze(0).expand(batch, -1, -1)
    # Self-communication is already zero by construction
    return who


def communication_when(o):
    """
    Returns when each link is active, based on sender observation.
    Shape: [batch, n_agents, n_agents] in [0,1].
    """
    batch, n_agents, obs_dim = o.shape
    when = torch.zeros(batch, n_agents, n_agents, device=o.device)

    # RULE R1: Overseer sends when it sees the Roach (enemy_0_available == 1)
    overseer_idx = 10
    enemy_avail = o[:, overseer_idx, 4]  # index 4 = enemy_0_available
    r1_condition = (enemy_avail == 1.0).float()
    when[:, 0:10, overseer_idx] = r1_condition.unsqueeze(1).expand(-1, 10)

    # RULE R2: Baneling sends when it sees at least one ally (max ally_i_visible > 0.5)
    # ally_0..ally_9 visible indices: 11,18,25,32,39,46,53,60,67,74
    ally_visible_indices = [11, 18, 25, 32, 39, 46, 53, 60, 67, 74]
    baneling_visible = o[:, 0:10, ally_visible_indices]  # [batch, 10, 10]
    max_visible, _ = baneling_visible.max(dim=-1)        # [batch, 10]
    r2_condition = (max_visible > 0.5).float()
    when[:, overseer_idx, 0:10] = r2_condition

    # Ensure no self-communication
    diag = torch.arange(n_agents, device=o.device)
    when[:, diag, diag] = 0.0

    return when


def communication_what(o):
    """
    Returns a mask selecting which features each sender would transmit.
    Shape: same as o, [batch, n_agents, obs_dim] in [0,1].
    """
    batch, n_agents, obs_dim = o.shape
    mask = torch.zeros_like(o)

    # RULE R1: Overseer sends enemy_0_distance, enemy_0_rel_x, enemy_0_rel_y
    overseer_idx = 10
    mask[:, overseer_idx, [5, 6, 7]] = 1.0  # indices 5,6,7

    # RULE R2: Banelings send ally_0_rel_x, ally_0_rel_y
    mask[:, 0:10, [13, 14]] = 1.0            # indices 13,14

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
