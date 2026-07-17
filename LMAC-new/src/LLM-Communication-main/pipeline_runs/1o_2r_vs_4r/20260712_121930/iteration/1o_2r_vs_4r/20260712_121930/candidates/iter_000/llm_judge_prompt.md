## system

You are an expert MARL communication-policy judge. Evaluate the generated policy only from the task spec, code, and interface validation. Return one JSON object only.

## user

Evaluate this pure LLM-generated LMAC communication strategy for SMAC map `1o_2r_vs_4r`.

Research goal:
- We are testing the capability boundary of LLM-designed communication.
- Do NOT use DRC, decision_sufficient, causally_useful, downstream RL win-rate, or hidden/global state.
- Judge whether the policy gives a plausible pure communication strategy for who, when, and what.

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

Interface validation:
{
  "valid": true,
  "map_name": "1o_2r_vs_4r",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_121930/iteration/1o_2r_vs_4r/20260712_121930/candidates/iter_000/comm_init.py",
  "validation_obs_source": "rollout",
  "validation_obs_dim": 66,
  "documented_obs_dim": 49,
  "message_dim": 66,
  "matrix_edge_rate": 0.3333333333333333,
  "who_edge_rate": 0.6666666666666666,
  "when_edge_rate": 0.3333333333333333,
  "what_dim": 66,
  "matrix_min": 0.0,
  "matrix_max": 1.0
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
  }
]

Candidate code:
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
