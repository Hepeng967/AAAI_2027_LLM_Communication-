## system

You are a MARL communication-policy coding agent. Return only one complete Python file in a single ```python code block```.

## user

Repair this LMAC teacher communication policy for `1o_2r_vs_4r`.

Validation error:
Traceback (most recent call last):
  File "/data/hp/LLM_Communication/LMAC-new/src/hl_comm/candidate_io.py", line 66, in validate_candidate
    return _validate_candidate(path, map_name, rollout_summary=rollout_summary)
  File "/data/hp/LLM_Communication/LMAC-new/src/hl_comm/candidate_io.py", line 94, in _validate_candidate
    raise RuntimeError(f"Candidate is missing required functions: {missing}")
RuntimeError: Candidate is missing required functions: ['message_design_instruction']


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

Current code:
```python
import torch

# ------------------------------------------------------------------------------
# Helper: we rely on fixed agent indices per the scenario description.
# Agent 0 = Overseer (G1), Agent 1 = Roach, Agent 2 = Roach (G2)
# ------------------------------------------------------------------------------

def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a binary who mask of shape [batch, n_agents, n_agents] where
    mask[b, r, s] = 1 if agent s sends to agent r. Diagonal is always zero.
    """
    batch, n_agents, _ = o.shape
    # We only support the 3-agent setup described in the policy.
    # Edges are static, determined by roles.
    who = o.new_zeros((batch, n_agents, n_agents))

    # RULE R1 & R2: Overseer (0) broadcasts to both Roaches (1,2).
    # Both rules share the same sender -> receiver pattern.
    who[:, 1, 0] = 1.0   # overseer -> roach1
    who[:, 2, 0] = 1.0   # overseer -> roach2

    # RULE R3: Roaches (1 and 2) send to the peer Roach (the other one).
    who[:, 2, 1] = 1.0   # roach1 -> roach2
    who[:, 1, 2] = 1.0   # roach2 -> roach1

    # Diagonal (self-communication) stays zero as per constraint.
    return who


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a when mask of shape [batch, n_agents, n_agents] where
    mask[b, r, s] = 1 if the sender's trigger condition is met.
    """
    batch, n_agents, _ = o.shape
    when = o.new_zeros((batch, n_agents, n_agents))

    # ---------- RULE R1 & R2 ----------
    # Condition: Overseer (agent 0) sees at least one enemy,
    # indicated by feature "enemy_0_available" (index 4) > 0.5.
    overseer_cond = (o[:, 0, 4] > 0.5).float()   # [batch]
    # Apply to edges from overseer to both roaches.
    when[:, 1, 0] = overseer_cond   # overseer -> roach1
    when[:, 2, 0] = overseer_cond   # overseer -> roach2

    # ---------- RULE R3 ----------
    # Condition: Sender Roach is alive, i.e. "own_health" (index 50) > 0.0.
    # This ensures the Roach sends its intention only while still active.
    roach1_cond = (o[:, 1, 50] > 0.0).float()   # roach1 alive
    roach2_cond = (o[:, 2, 50] > 0.0).float()   # roach2 alive

    when[:, 2, 1] = roach1_cond   # roach1 -> roach2
    when[:, 1, 2] = roach2_cond   # roach2 -> roach1

    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a what mask of shape [batch, n_agents, obs_dim] where
    mask[b, a, f] = 1 if agent a includes feature f in its message.
    """
    what_mask = torch.zeros_like(o)

    # ------------------------------------------------------------------
    # RULE R1 & R2 (Overseer, agent 0)
    #   R1: send enemy relative positions   -> indices [6,7,14,15,22,23,30,31]
    #   R2: send enemy health values       -> indices [8,16,24,32]
    # We combine both sets into the Overseer's mask.
    # (See feature index map for exact offsets.)
    pos_indices = [6, 7, 14, 15, 22, 23, 30, 31]   # R1
    hlth_indices = [8, 16, 24, 32]                 # R2

    what_mask[:, 0, pos_indices] = 1.0
    what_mask[:, 0, hlth_indices] = 1.0

    # ------------------------------------------------------------------
    # RULE R3 (Roaches, agents 1 and 2)
    #   The intended target index is not an observation feature;
    #   the policy expects the learning process to encode it in the
    #   dedicated communication channel. Therefore the what mask for
    #   Roaches is left empty (all zeros). The edge itself is still
    #   provided by who/when to allow the architecture to learn a
    #   suitable encoding if supported by the overall framework.
    #   No observation features are set for agents 1 or 2.

    return what_mask
```

Return a complete corrected Python file. Preserve message_design_instruction, communication,
communication_who, communication_when, and communication_what.
