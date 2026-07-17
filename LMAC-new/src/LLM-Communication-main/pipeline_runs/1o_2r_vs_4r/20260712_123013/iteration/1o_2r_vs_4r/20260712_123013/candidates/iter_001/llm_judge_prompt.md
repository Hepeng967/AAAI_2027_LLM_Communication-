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
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_001/comm_init.py",
  "validation_obs_source": "rollout",
  "validation_obs_dim": 66,
  "documented_obs_dim": 49,
  "message_dim": 66,
  "matrix_edge_rate": 0.16666666666666666,
  "who_edge_rate": 0.6666666666666666,
  "when_edge_rate": 0.16666666666666666,
  "what_dim": 66,
  "matrix_min": 0.0,
  "matrix_max": 1.0
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "1o_2r_vs_4r",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_001/comm_init.py",
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
  "matrix_edge_rate": 0.46344262295081967,
  "who_edge_rate": 0.6666666666666666,
  "when_edge_rate": 0.46344262295081967,
  "message_nonzero_rate": 0.0707070707070707,
  "message_abs_mean": 0.0707070707070707,
  "active_sender_what_coverage_mean": 0.10432194912595447,
  "active_sender_what_coverage_min": 0.01515151560306549,
  "active_sender_count": 5525,
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
        ],
        [
          2,
          1
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": 0.0,
          "7": -0.076497,
          "8": 1.0,
          "13": 0.076497,
          "14": 0.0,
          "15": 0.076497,
          "20": 1.0,
          "21": 0.076497,
          "22": 0.076497,
          "27": 0.0,
          "28": 1.0,
          "29": 0.0
        },
        {
          "46": 0.104275
        },
        {
          "46": -0.104275
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
          1,
          2
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": 0.042209,
          "7": -0.076497,
          "8": 1.0,
          "13": 0.08737,
          "14": 0.042209,
          "15": 0.076497,
          "20": 1.0,
          "21": 0.118707,
          "22": 0.118707,
          "27": 0.0,
          "28": 1.0,
          "29": 0.042209
        },
        {
          "46": -0.117242
        },
        {
          "46": 0.117242
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
          1,
          2
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": 0.071913,
          "7": -0.102892,
          "8": 1.0,
          "13": 0.087646,
          "14": 0.071913,
          "15": 0.050103,
          "20": 1.0,
          "21": 0.150739,
          "22": 0.14841,
          "27": 0.0,
          "28": 1.0,
          "29": 0.076604
        },
        {
          "46": -0.242242
        },
        {
          "46": 0.242242
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
          1,
          2
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": -0.057916,
          "7": -0.103651,
          "8": 1.0,
          "13": 0.076085,
          "14": -0.057916,
          "15": 0.049344,
          "20": 1.0,
          "21": 0.032903,
          "22": 0.018582,
          "27": 0.0,
          "28": 1.0,
          "29": 0.063965
        },
        {
          "46": -0.617242
        },
        {
          "46": 0.617242
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
        ],
        [
          2,
          1
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": -0.058295,
          "7": -0.052327,
          "8": 1.0,
          "13": 0.116328,
          "14": -0.058295,
          "15": 0.100667,
          "20": 1.0,
          "21": 0.030257,
          "22": 0.018202,
          "27": 0.0,
          "28": 1.0,
          "29": 0.063107
        },
        {
          "46": 0.007758
        },
        {
          "46": -0.007758
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
          1,
          2
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": -0.058621,
          "7": -0.182373,
          "8": 1.0,
          "13": 0.06557,
          "14": -0.058621,
          "15": -0.029378,
          "20": 1.0,
          "21": 0.107374,
          "22": 0.017877,
          "27": 0.0,
          "28": 1.0,
          "29": 0.121021
        },
        {
          "46": -0.117242
        },
        {
          "46": 0.117242
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
          1,
          2
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": -0.058621,
          "7": -0.182373,
          "8": 1.0,
          "13": 0.06557,
          "14": -0.058621,
          "15": -0.029378,
          "20": 1.0,
          "21": 0.107374,
          "22": 0.017877,
          "27": 0.0,
          "28": 1.0,
          "29": 0.121021
        },
        {
          "46": -0.242242
        },
        {
          "46": 0.242242
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
          1,
          2
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": 0.00963,
          "7": -0.192247,
          "8": 1.0,
          "13": 0.040416,
          "14": 0.00963,
          "15": -0.039252,
          "20": 1.0,
          "21": 0.144277,
          "22": 0.086127,
          "27": 0.0,
          "28": 1.0,
          "29": 0.11615
        },
        {
          "46": -0.867242
        },
        {
          "46": 0.867242
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
          1,
          2
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": 0.045546,
          "7": -0.192247,
          "8": 1.0,
          "13": 0.060126,
          "14": 0.045546,
          "15": -0.039252,
          "20": 1.0,
          "21": 0.168204,
          "22": 0.122043,
          "27": 0.0,
          "28": 1.0,
          "29": 0.124388
        },
        {
          "46": -0.867242
        },
        {
          "46": 0.867242
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
          1,
          2
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": 0.045546,
          "7": -0.123996,
          "8": 1.0,
          "13": 0.053994,
          "14": 0.045546,
          "15": 0.028998,
          "20": 1.0,
          "21": 0.130961,
          "22": 0.122043,
          "27": 0.0,
          "28": 1.0,
          "29": 0.065807
        },
        {
          "46": -0.742242
        },
        {
          "46": 0.742242
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
          1,
          2
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": 0.045546,
          "7": -0.01983,
          "8": 1.0,
          "13": 0.140739,
          "14": 0.045546,
          "15": 0.133165,
          "20": 1.0,
          "21": 0.134558,
          "22": 0.122043,
          "27": 0.0,
          "28": 1.0,
          "29": 0.072702
        },
        {
          "46": -0.742242
        },
        {
          "46": 0.742242
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
          1,
          2
        ],
        [
          2,
          0
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          6,
          7,
          8,
          13,
          14,
          15,
          20,
          21,
          22,
          27,
          28,
          29
        ],
        [
          46
        ],
        [
          46
        ]
      ],
      "what_coverage_by_sender": [
        0.181818,
        0.015152,
        0.015152
      ],
      "selected_values_by_sender": [
        {
          "6": 0.045546,
          "7": 0.052002,
          "8": 1.0,
          "13": 0.209995,
          "14": 0.045546,
          "15": 0.204997,
          "20": 1.0,
          "21": 0.177219,
          "22": 0.122043,
          "27": 0.0,
          "28": 1.0,
          "29": 0.136332
        },
        {
          "46": -0.617242
        },
        {
          "46": 0.617242
        }
      ]
    }
  ]
}

Recent trials:
[
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "1o_2r_vs_4r",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-12T12:34:39+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_000/comm_init.py",
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
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "1o_2r_vs_4r",
    "matrix_edge_rate": 0.46256830601092896,
    "message_dim": 66,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-12T12:34:39+00:00",
    "valid": true,
    "when_edge_rate": 0.46256830601092896,
    "who_edge_rate": 0.6666666666666666
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_000/comm_init.py",
    "failure_analysis": "The overseer when condition tests only enemy_0_available, missing cases where other enemies are the only visible ones. Roach-to-roach edges are set but the what mask is all‑zero, so those messages carry no information. This violates the intended roach communication rule and wastes bandwidth. The overseer what mask is well-chosen and aligns with rollout evidence, but the other flaws make the policy incomplete.",
    "iteration": 0,
    "map_name": "1o_2r_vs_4r",
    "matrix_edge_rate": 0.3333333333333333,
    "message_dim": 66,
    "next_hypothesis": "1. Replace overseer when condition with a check that any enemy is available (e.g., max of enemy_*_available > 0.5, or sum > 0). 2. For roaches, either include features like own_health, previous action, or a learned embedding of the action that can be back‑propagated through, instead of leaving the what mask empty. Alternatively, reconsider whether roach communication should be included at all if the intended target cannot be expressed in the current observation space.",
    "rollout_grounding_score": 0.5,
    "score": 0.4,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-12T12:35:40+00:00",
    "valid": true,
    "what_score": 0.3,
    "when_score": 0.3,
    "who_score": 0.8
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "1o_2r_vs_4r",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-12T12:37:16+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_001/comm_init.py",
      "documented_obs_dim": 49,
      "map_name": "1o_2r_vs_4r",
      "matrix_edge_rate": 0.16666666666666666,
      "matrix_max": 1.0,
      "matrix_min": 0.0,
      "message_dim": 66,
      "valid": true,
      "validation_obs_dim": 66,
      "validation_obs_source": "rollout",
      "what_dim": 66,
      "when_edge_rate": 0.16666666666666666,
      "who_edge_rate": 0.6666666666666666
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "1o_2r_vs_4r",
    "matrix_edge_rate": 0.46344262295081967,
    "message_dim": 66,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-12T12:37:16+00:00",
    "valid": true,
    "when_edge_rate": 0.46344262295081967,
    "who_edge_rate": 0.6666666666666666
  }
]

Candidate code:
```python
import torch

# ------------------------------------------------------------------------------
# Teacher communication policy for 1o_2r_vs_4r
# Agents: agent 0 = Overseer (G1), agent 1 = Roach (G2), agent 2 = Roach (G3)
# The observation is 66-dimensional, aligned to the feature_index provided in
# the rollout summary.
# ------------------------------------------------------------------------------

def message_design_instruction() -> str:
    """
    Returns a string describing the communication design for logging / inspection.
    """
    return (
        "R1 Overseer sends enemy relative positions to all roaches when any enemy is visible. "
        "R2 Overseer sends enemy health values to all roaches when any enemy is visible. "
        "R3 Roaches send their intended target to the other roach while they are alive."
    )


def communication(o: torch.Tensor):
    """
    Convenience wrapper that returns all three masks at once.
    The evaluation framework expects this function to exist.
    """
    return communication_who(o), communication_when(o), communication_what(o)


def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a binary who mask of shape [batch, n_agents, n_agents] where
    mask[b, r, s] = 1 if agent s sends to agent r. Diagonal is always zero.
    """
    batch, n_agents, _ = o.shape
    who = o.new_zeros((batch, n_agents, n_agents))

    # R1 & R2: Overseer (0) broadcasts to both roaches (1, 2)
    who[:, 1, 0] = 1.0
    who[:, 2, 0] = 1.0

    # R3: Roaches send to the other roach
    who[:, 2, 1] = 1.0   # roach 1 -> roach 2
    who[:, 1, 2] = 1.0   # roach 2 -> roach 1

    return who


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a when mask of shape [batch, n_agents, n_agents] where
    mask[b, r, s] = 1 if the sender's trigger condition is met.
    """
    batch, n_agents, _ = o.shape
    when = o.new_zeros((batch, n_agents, n_agents))

    # ---------- R1 & R2 ----------
    # Overseer sends if any enemy is visible (enemy_*_available features)
    overseer_cond = (
        (o[:, 0, 4] > 0.5) |   # enemy_0_available
        (o[:, 0, 11] > 0.5) |  # enemy_1_available
        (o[:, 0, 18] > 0.5) |  # enemy_2_available
        (o[:, 0, 25] > 0.5)    # enemy_3_available
    ).float()
    when[:, 1, 0] = overseer_cond
    when[:, 2, 0] = overseer_cond

    # ---------- R3 ----------
    # A roach sends while it is alive (own_health > 0)
    roach1_alive = (o[:, 1, 46] > 0.0).float()
    roach2_alive = (o[:, 2, 46] > 0.0).float()

    when[:, 2, 1] = roach1_alive   # roach 1 -> roach 2
    when[:, 1, 2] = roach2_alive   # roach 2 -> roach 1

    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a what mask of shape [batch, n_agents, obs_dim] where
    mask[b, a, f] = 1 if agent a includes feature f in its message.
    """
    what_mask = torch.zeros_like(o)

    # ---------- R1 & R2 (Overseer, agent 0) ----------
    # Positions of all four enemies (rel_x, rel_y)
    pos_indices = [
        6, 7,    # enemy_0
        13, 14,  # enemy_1
        20, 21,  # enemy_2
        27, 28,  # enemy_3
    ]
    # Health of all four enemies
    health_indices = [
        8,       # enemy_0
        15,      # enemy_1
        22,      # enemy_2
        29,      # enemy_3
    ]
    what_mask[:, 0, pos_indices] = 1.0
    what_mask[:, 0, health_indices] = 1.0

    # ---------- R3 (Roaches, agents 1 and 2) ----------
    # The intended target is not a direct observation feature, so we include
    # the agent's own health (index 46) as a proxy for survivability / state.
    what_mask[:, [1, 2], 46] = 1.0

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
