## system

You are a MARL communication-policy coding agent. Return only one complete Python file in a single ```python code block```.

## user

Revise this LMAC teacher communication policy for `1o_2r_vs_4r` using the LLM judge feedback.

Map spec:
{
  "n_agents": 3,
  "obs_dim": 66,
  "time_seq": 10
}

Rollout-backed LMAC observation alignment:
{
  "map_name": "1o_2r_vs_4r",
  "rollout_root": "/data/hp/LLM_Communication/LMAC-new/data",
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
  "available": true,
  "n_agents": 3,
  "raw_obs_dim": 53,
  "rollout_obs_dim": 66,
  "documented_obs_dim": 49,
  "extra_obs_dim": 4,
  "episodes": 61,
  "transitions": 2975,
  "seq_lengths": [
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    30,
    50,
    50,
    50,
    50,
    50,
    35,
    50,
    50,
    50,
    50,
    50,
    37,
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
    23,
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
  "action_dim": 10,
  "agent_types": [
    "overseer",
    "roach",
    "roach"
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
    "enemy_1_available": [
      11,
      12
    ],
    "enemy_1_distance": [
      12,
      13
    ],
    "enemy_1_rel_x": [
      13,
      14
    ],
    "enemy_1_rel_y": [
      14,
      15
    ],
    "enemy_1_health": [
      15,
      16
    ],
    "enemy_1_type_0": [
      16,
      17
    ],
    "enemy_1_type_1": [
      17,
      18
    ],
    "enemy_2_available": [
      18,
      19
    ],
    "enemy_2_distance": [
      19,
      20
    ],
    "enemy_2_rel_x": [
      20,
      21
    ],
    "enemy_2_rel_y": [
      21,
      22
    ],
    "enemy_2_health": [
      22,
      23
    ],
    "enemy_2_type_0": [
      23,
      24
    ],
    "enemy_2_type_1": [
      24,
      25
    ],
    "enemy_3_available": [
      25,
      26
    ],
    "enemy_3_distance": [
      26,
      27
    ],
    "enemy_3_rel_x": [
      27,
      28
    ],
    "enemy_3_rel_y": [
      28,
      29
    ],
    "enemy_3_health": [
      29,
      30
    ],
    "enemy_3_type_0": [
      30,
      31
    ],
    "enemy_3_type_1": [
      31,
      32
    ],
    "ally_0_visible": [
      32,
      33
    ],
    "ally_0_distance": [
      33,
      34
    ],
    "ally_0_rel_x": [
      34,
      35
    ],
    "ally_0_rel_y": [
      35,
      36
    ],
    "ally_0_health": [
      36,
      37
    ],
    "ally_0_type_0": [
      37,
      38
    ],
    "ally_0_type_1": [
      38,
      39
    ],
    "ally_1_visible": [
      39,
      40
    ],
    "ally_1_distance": [
      40,
      41
    ],
    "ally_1_rel_x": [
      41,
      42
    ],
    "ally_1_rel_y": [
      42,
      43
    ],
    "ally_1_health": [
      43,
      44
    ],
    "ally_1_type_0": [
      44,
      45
    ],
    "ally_1_type_1": [
      45,
      46
    ],
    "own_health": [
      46,
      47
    ],
    "own_type_0": [
      47,
      48
    ],
    "own_type_1": [
      48,
      49
    ],
    "lmac_extra_49": [
      49,
      50
    ],
    "lmac_extra_50": [
      50,
      51
    ],
    "lmac_extra_51": [
      51,
      52
    ],
    "lmac_extra_52": [
      52,
      53
    ],
    "previous_action_0": [
      53,
      54
    ],
    "previous_action_1": [
      54,
      55
    ],
    "previous_action_2": [
      55,
      56
    ],
    "previous_action_3": [
      56,
      57
    ],
    "previous_action_4": [
      57,
      58
    ],
    "previous_action_5": [
      58,
      59
    ],
    "previous_action_6": [
      59,
      60
    ],
    "previous_action_7": [
      60,
      61
    ],
    "previous_action_8": [
      61,
      62
    ],
    "previous_action_9": [
      62,
      63
    ],
    "agent_id_0": [
      63,
      64
    ],
    "agent_id_1": [
      64,
      65
    ],
    "agent_id_2": [
      65,
      66
    ]
  },
  "feature_statistics": {
    "move_north": {
      "index": 0,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.82306,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.82306
    },
    "move_south": {
      "index": 1,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.82306,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.82306
    },
    "move_east": {
      "index": 2,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.80765,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.80765
    },
    "move_west": {
      "index": 3,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.841093,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.841093
    },
    "enemy_0_available": {
      "index": 4,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.362951,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.362951
    },
    "enemy_0_distance": {
      "index": 5,
      "min": 0.0,
      "max": 0.999785,
      "mean": 0.080679,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.393517,
      "nonzero_rate": 0.382623
    },
    "enemy_0_rel_x": {
      "index": 6,
      "min": -0.996392,
      "max": 0.979682,
      "mean": 0.005072,
      "p05": -0.130181,
      "p50": 0.0,
      "p95": 0.171771,
      "nonzero_rate": 0.368634
    },
    "enemy_0_rel_y": {
      "index": 7,
      "min": -0.995931,
      "max": 0.975613,
      "mean": -0.000888,
      "p05": -0.142959,
      "p50": 0.0,
      "p95": 0.152138,
      "nonzero_rate": 0.376721
    },
    "enemy_0_health": {
      "index": 8,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.361968,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.38459
    },
    "enemy_0_type_0": {
      "index": 9,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.38459,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.38459
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
    "enemy_1_available": {
      "index": 11,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_1_distance": {
      "index": 12,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.361967,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.361967
    },
    "enemy_1_rel_x": {
      "index": 13,
      "min": 0.0,
      "max": 0.996976,
      "mean": 0.08283,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.372232,
      "nonzero_rate": 0.382842
    },
    "enemy_1_rel_y": {
      "index": 14,
      "min": -0.966119,
      "max": 0.996202,
      "mean": 0.004267,
      "p05": -0.163344,
      "p50": 0.0,
      "p95": 0.179281,
      "nonzero_rate": 0.373661
    },
    "enemy_1_health": {
      "index": 15,
      "min": -0.9949,
      "max": 0.937174,
      "mean": -0.00084,
      "p05": -0.146946,
      "p50": 0.0,
      "p95": 0.143148,
      "nonzero_rate": 0.37847
    },
    "enemy_1_type_0": {
      "index": 16,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.351994,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.382842
    },
    "enemy_1_type_1": {
      "index": 17,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.382842,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.382842
    },
    "enemy_2_available": {
      "index": 18,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_2_distance": {
      "index": 19,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_2_rel_x": {
      "index": 20,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.339454,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.339454
    },
    "enemy_2_rel_y": {
      "index": 21,
      "min": 0.0,
      "max": 0.99819,
      "mean": 0.07343,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.350125,
      "nonzero_rate": 0.359454
    },
    "enemy_2_health": {
      "index": 22,
      "min": -0.924425,
      "max": 0.980686,
      "mean": -0.002516,
      "p05": -0.143285,
      "p50": 0.0,
      "p95": 0.137448,
      "nonzero_rate": 0.341093
    },
    "enemy_2_type_0": {
      "index": 23,
      "min": -0.995931,
      "max": 0.92711,
      "mean": 0.00033,
      "p05": -0.133287,
      "p50": 0.0,
      "p95": 0.128423,
      "nonzero_rate": 0.357705
    },
    "enemy_2_type_1": {
      "index": 24,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.342349,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.359454
    },
    "enemy_3_available": {
      "index": 25,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.359454,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.359454
    },
    "enemy_3_distance": {
      "index": 26,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_3_rel_x": {
      "index": 27,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_3_rel_y": {
      "index": 28,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.36459,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.36459
    },
    "enemy_3_health": {
      "index": 29,
      "min": 0.0,
      "max": 0.995106,
      "mean": 0.079082,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.382978,
      "nonzero_rate": 0.379235
    },
    "enemy_3_type_0": {
      "index": 30,
      "min": -0.988064,
      "max": 0.995009,
      "mean": -9.4e-05,
      "p05": -0.149109,
      "p50": 0.0,
      "p95": 0.154211,
      "nonzero_rate": 0.367213
    },
    "enemy_3_type_1": {
      "index": 31,
      "min": -0.967122,
      "max": 0.936469,
      "mean": -0.001243,
      "p05": -0.134298,
      "p50": 0.0,
      "p95": 0.1317,
      "nonzero_rate": 0.372787
    },
    "ally_0_visible": {
      "index": 32,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.3563,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.385464
    },
    "ally_0_distance": {
      "index": 33,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.385464,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.385464
    },
    "ally_0_rel_x": {
      "index": 34,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_0_rel_y": {
      "index": 35,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_0_health": {
      "index": 36,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.108415,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.108415
    },
    "ally_0_type_0": {
      "index": 37,
      "min": 0.0,
      "max": 0.998038,
      "mean": 0.063572,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.591519,
      "nonzero_rate": 0.108415
    },
    "ally_0_type_1": {
      "index": 38,
      "min": -0.98782,
      "max": 0.993056,
      "mean": -0.005933,
      "p05": -0.118056,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.108415
    },
    "ally_1_visible": {
      "index": 39,
      "min": -0.997179,
      "max": 0.997179,
      "mean": 0.000786,
      "p05": -0.042687,
      "p50": 0.0,
      "p95": 0.019763,
      "nonzero_rate": 0.108415
    },
    "ally_1_distance": {
      "index": 40,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.100057,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.108415
    },
    "ally_1_rel_x": {
      "index": 41,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.038251,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.038251
    },
    "ally_1_rel_y": {
      "index": 42,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.070164,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.070164
    },
    "ally_1_health": {
      "index": 43,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.603279,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.603279
    },
    "ally_1_type_0": {
      "index": 44,
      "min": 0.0,
      "max": 0.998416,
      "mean": 0.25389,
      "p05": 0.0,
      "p50": 0.172185,
      "p95": 0.805742,
      "nonzero_rate": 0.603279
    },
    "ally_1_type_1": {
      "index": 45,
      "min": -0.993056,
      "max": 0.988173,
      "mean": 0.005933,
      "p05": -0.391602,
      "p50": 0.0,
      "p95": 0.432281,
      "nonzero_rate": 0.562623
    },
    "own_health": {
      "index": 46,
      "min": -0.991699,
      "max": 0.991699,
      "mean": -0.000786,
      "p05": -0.526556,
      "p50": 0.0,
      "p95": 0.520957,
      "nonzero_rate": 0.593443
    },
    "own_type_0": {
      "index": 47,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.583295,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.603279
    },
    "own_type_1": {
      "index": 48,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.603279,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.603279
    },
    "lmac_extra_49": {
      "index": 49,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "lmac_extra_50": {
      "index": 50,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.934026,
      "p05": 0.028683,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.95082
    },
    "lmac_extra_51": {
      "index": 51,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.625246,
      "p05": 0.0,
      "p50": 1.0,
      "p95": 1.0,
      "nonzero_rate": 0.625246
    },
    "lmac_extra_52": {
      "index": 52,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.325574,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.325574
    },
    "previous_action_0": {
      "index": 53,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025027,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025027
    },
    "previous_action_1": {
      "index": 54,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.173333,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.173333
    },
    "previous_action_2": {
      "index": 55,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.154645,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.154645
    },
    "previous_action_3": {
      "index": 56,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.148306,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.148306
    },
    "previous_action_4": {
      "index": 57,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.137923,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.137923
    },
    "previous_action_5": {
      "index": 58,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.144153,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.144153
    },
    "previous_action_6": {
      "index": 59,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.038689,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.038689
    },
    "previous_action_7": {
      "index": 60,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.044044,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044044
    },
    "previous_action_8": {
      "index": 61,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.052678,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.052678
    },
    "previous_action_9": {
      "index": 62,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.039235,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.039235
    },
    "agent_id_0": {
      "index": 63,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.333333,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.333333
    },
    "agent_id_1": {
      "index": 64,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.333333,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.333333
    },
    "agent_id_2": {
      "index": 65,
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

Structured judge summary:
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

LLM failure analysis:
{
  "Evaluation": "The current code misaligns enemy availability indices and what feature blocks for enemies 1–3. The when condition uses indices 12, 20, 28 (should be 11, 18, 25) and the what blocks use 13–18, 21–26, 29–34 (should be 12–17, 19–24, 26–31). This prevents the policy from correctly extracting and sending enemy features, leading to unreliable communication.",
  "Missing_Information_Hypothesis": "Correct observation‑index mapping from the rollout data: enemy_1_available at index 11, enemy_2_available at index 18, enemy_3_available at index 25; and corresponding feature ranges enemy_1 (12–17), enemy_2 (19–24), enemy_3 (26–31).",
  "Improvement_Suggestions": "1. In communication_when, change availability checks to index 11 for enemy_1, index 18 for enemy_2, index 25 for enemy_3.\n2. In communication_what, update the what blocks: assign_block for enemy_1 to range 12–18 (exclusive end), enemy_2 to 19–25, enemy_3 to 26–32.",
  "Target_Functions": ["communication_when", "communication_what"],
  "Target_Rule_IDs": ["R2", "R3", "R4"]
}

Current source:
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

Revision target:
- Preserve stable `# RULE <rule_id>` comments and edit only rule IDs identified
  by the judge unless a documented cross-rule conflict requires another edit.
- who failures: edit communication_who(o).
- when failures: edit communication_when(o).
- what/content failures: edit communication_what(o).
- communication_what(o) must remain an obs-aligned [batch, n_agents, obs_dim]
  mask in [0,1]; selected features keep their original indices.
- Keep the strategy pure: local observation only, deterministic, no trainable parameters.

Return only a complete Python file with all required who/when/what functions.
