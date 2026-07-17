## system

You are a MARL communication-policy coding agent. Return only one complete Python file in a single ```python code block```.

## user

Repair this LMAC teacher communication policy for `protoss_10_vs_10`.

Validation error:
Traceback (most recent call last):
  File "/data/hp/LLM_Communication/LMAC-new/src/hl_comm/candidate_io.py", line 66, in validate_candidate
    return _validate_candidate(path, map_name, rollout_summary=rollout_summary)
  File "/data/hp/LLM_Communication/LMAC-new/src/hl_comm/candidate_io.py", line 78, in _validate_candidate
    _reject_python_loops(path)
  File "/data/hp/LLM_Communication/LMAC-new/src/hl_comm/candidate_io.py", line 144, in _reject_python_loops
    raise RuntimeError(
RuntimeError: Python loops/comprehensions are forbidden inside communication functions; use vectorized torch operations. Violations: communication_what:140:For, communication_what:146:For, communication_what:167:For


Map spec:
{
  "environment": "smacv2",
  "n_agents": 10,
  "n_enemies": 10,
  "obs_dim": 208,
  "documented_raw_obs_dim": 182,
  "time_seq": 10,
  "dynamic_agent_roles": true,
  "possible_unit_types": [
    "stalker",
    "zealot",
    "colossus"
  ],
  "agent_id_role_warning": "Agent ID does not identify a fixed unit type across episodes."
}

Rollout-backed LMAC observation alignment:
{
  "map_name": "protoss_10_vs_10",
  "rollout_root": "/data/hp/LLM_Communication/LMAC-new/data/smacv2",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0000.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0001.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0002.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0003.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0004.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0005.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0006.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0007.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0008.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0009.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0010.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0011.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0012.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0013.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0014.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0015.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0016.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0017.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0018.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0019.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0020.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0021.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0022.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0023.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0024.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0025.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0026.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0027.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0028.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0029.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0030.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0031.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0032.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0033.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0034.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0035.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0036.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0037.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0038.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0039.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0040.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0041.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0042.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0043.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0044.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0045.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0046.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0047.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0048.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/protoss_10_vs_10/train_traj_0049.pkl"
  ],
  "available": true,
  "n_agents": 10,
  "raw_obs_dim": 182,
  "rollout_obs_dim": 208,
  "documented_obs_dim": 182,
  "extra_obs_dim": 0,
  "episodes": 50,
  "transitions": 2992,
  "seq_lengths": [
    69,
    49,
    64,
    57,
    63,
    52,
    57,
    54,
    63,
    53,
    67,
    60,
    65,
    66,
    55,
    60,
    57,
    56,
    53,
    53,
    55,
    58,
    74,
    73,
    58,
    60,
    53,
    64,
    50,
    65,
    48,
    52,
    56,
    61,
    55,
    71,
    51,
    67,
    72,
    63,
    57,
    64,
    72,
    52,
    85,
    62,
    49,
    68,
    51,
    53
  ],
  "action_dim": 16,
  "agent_types": [
    "dynamic_from_own_unit_type_bits",
    "dynamic_from_own_unit_type_bits",
    "dynamic_from_own_unit_type_bits",
    "dynamic_from_own_unit_type_bits",
    "dynamic_from_own_unit_type_bits",
    "dynamic_from_own_unit_type_bits",
    "dynamic_from_own_unit_type_bits",
    "dynamic_from_own_unit_type_bits",
    "dynamic_from_own_unit_type_bits",
    "dynamic_from_own_unit_type_bits"
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
    "enemy_0_relative_x": [
      6,
      7
    ],
    "enemy_0_relative_y": [
      7,
      8
    ],
    "enemy_0_health": [
      8,
      9
    ],
    "enemy_0_shield": [
      9,
      10
    ],
    "enemy_0_unit_type_stalker": [
      10,
      11
    ],
    "enemy_0_unit_type_zealot": [
      11,
      12
    ],
    "enemy_0_unit_type_colossus": [
      12,
      13
    ],
    "enemy_1_available": [
      13,
      14
    ],
    "enemy_1_distance": [
      14,
      15
    ],
    "enemy_1_relative_x": [
      15,
      16
    ],
    "enemy_1_relative_y": [
      16,
      17
    ],
    "enemy_1_health": [
      17,
      18
    ],
    "enemy_1_shield": [
      18,
      19
    ],
    "enemy_1_unit_type_stalker": [
      19,
      20
    ],
    "enemy_1_unit_type_zealot": [
      20,
      21
    ],
    "enemy_1_unit_type_colossus": [
      21,
      22
    ],
    "enemy_2_available": [
      22,
      23
    ],
    "enemy_2_distance": [
      23,
      24
    ],
    "enemy_2_relative_x": [
      24,
      25
    ],
    "enemy_2_relative_y": [
      25,
      26
    ],
    "enemy_2_health": [
      26,
      27
    ],
    "enemy_2_shield": [
      27,
      28
    ],
    "enemy_2_unit_type_stalker": [
      28,
      29
    ],
    "enemy_2_unit_type_zealot": [
      29,
      30
    ],
    "enemy_2_unit_type_colossus": [
      30,
      31
    ],
    "enemy_3_available": [
      31,
      32
    ],
    "enemy_3_distance": [
      32,
      33
    ],
    "enemy_3_relative_x": [
      33,
      34
    ],
    "enemy_3_relative_y": [
      34,
      35
    ],
    "enemy_3_health": [
      35,
      36
    ],
    "enemy_3_shield": [
      36,
      37
    ],
    "enemy_3_unit_type_stalker": [
      37,
      38
    ],
    "enemy_3_unit_type_zealot": [
      38,
      39
    ],
    "enemy_3_unit_type_colossus": [
      39,
      40
    ],
    "enemy_4_available": [
      40,
      41
    ],
    "enemy_4_distance": [
      41,
      42
    ],
    "enemy_4_relative_x": [
      42,
      43
    ],
    "enemy_4_relative_y": [
      43,
      44
    ],
    "enemy_4_health": [
      44,
      45
    ],
    "enemy_4_shield": [
      45,
      46
    ],
    "enemy_4_unit_type_stalker": [
      46,
      47
    ],
    "enemy_4_unit_type_zealot": [
      47,
      48
    ],
    "enemy_4_unit_type_colossus": [
      48,
      49
    ],
    "enemy_5_available": [
      49,
      50
    ],
    "enemy_5_distance": [
      50,
      51
    ],
    "enemy_5_relative_x": [
      51,
      52
    ],
    "enemy_5_relative_y": [
      52,
      53
    ],
    "enemy_5_health": [
      53,
      54
    ],
    "enemy_5_shield": [
      54,
      55
    ],
    "enemy_5_unit_type_stalker": [
      55,
      56
    ],
    "enemy_5_unit_type_zealot": [
      56,
      57
    ],
    "enemy_5_unit_type_colossus": [
      57,
      58
    ],
    "enemy_6_available": [
      58,
      59
    ],
    "enemy_6_distance": [
      59,
      60
    ],
    "enemy_6_relative_x": [
      60,
      61
    ],
    "enemy_6_relative_y": [
      61,
      62
    ],
    "enemy_6_health": [
      62,
      63
    ],
    "enemy_6_shield": [
      63,
      64
    ],
    "enemy_6_unit_type_stalker": [
      64,
      65
    ],
    "enemy_6_unit_type_zealot": [
      65,
      66
    ],
    "enemy_6_unit_type_colossus": [
      66,
      67
    ],
    "enemy_7_available": [
      67,
      68
    ],
    "enemy_7_distance": [
      68,
      69
    ],
    "enemy_7_relative_x": [
      69,
      70
    ],
    "enemy_7_relative_y": [
      70,
      71
    ],
    "enemy_7_health": [
      71,
      72
    ],
    "enemy_7_shield": [
      72,
      73
    ],
    "enemy_7_unit_type_stalker": [
      73,
      74
    ],
    "enemy_7_unit_type_zealot": [
      74,
      75
    ],
    "enemy_7_unit_type_colossus": [
      75,
      76
    ],
    "enemy_8_available": [
      76,
      77
    ],
    "enemy_8_distance": [
      77,
      78
    ],
    "enemy_8_relative_x": [
      78,
      79
    ],
    "enemy_8_relative_y": [
      79,
      80
    ],
    "enemy_8_health": [
      80,
      81
    ],
    "enemy_8_shield": [
      81,
      82
    ],
    "enemy_8_unit_type_stalker": [
      82,
      83
    ],
    "enemy_8_unit_type_zealot": [
      83,
      84
    ],
    "enemy_8_unit_type_colossus": [
      84,
      85
    ],
    "enemy_9_available": [
      85,
      86
    ],
    "enemy_9_distance": [
      86,
      87
    ],
    "enemy_9_relative_x": [
      87,
      88
    ],
    "enemy_9_relative_y": [
      88,
      89
    ],
    "enemy_9_health": [
      89,
      90
    ],
    "enemy_9_shield": [
      90,
      91
    ],
    "enemy_9_unit_type_stalker": [
      91,
      92
    ],
    "enemy_9_unit_type_zealot": [
      92,
      93
    ],
    "enemy_9_unit_type_colossus": [
      93,
      94
    ],
    "ally_slot_0_visible": [
      94,
      95
    ],
    "ally_slot_0_distance": [
      95,
      96
    ],
    "ally_slot_0_relative_x": [
      96,
      97
    ],
    "ally_slot_0_relative_y": [
      97,
      98
    ],
    "ally_slot_0_health": [
      98,
      99
    ],
    "ally_slot_0_shield": [
      99,
      100
    ],
    "ally_slot_0_unit_type_stalker": [
      100,
      101
    ],
    "ally_slot_0_unit_type_zealot": [
      101,
      102
    ],
    "ally_slot_0_unit_type_colossus": [
      102,
      103
    ],
    "ally_slot_1_visible": [
      103,
      104
    ],
    "ally_slot_1_distance": [
      104,
      105
    ],
    "ally_slot_1_relative_x": [
      105,
      106
    ],
    "ally_slot_1_relative_y": [
      106,
      107
    ],
    "ally_slot_1_health": [
      107,
      108
    ],
    "ally_slot_1_shield": [
      108,
      109
    ],
    "ally_slot_1_unit_type_stalker": [
      109,
      110
    ],
    "ally_slot_1_unit_type_zealot": [
      110,
      111
    ],
    "ally_slot_1_unit_type_colossus": [
      111,
      112
    ],
    "ally_slot_2_visible": [
      112,
      113
    ],
    "ally_slot_2_distance": [
      113,
      114
    ],
    "ally_slot_2_relative_x": [
      114,
      115
    ],
    "ally_slot_2_relative_y": [
      115,
      116
    ],
    "ally_slot_2_health": [
      116,
      117
    ],
    "ally_slot_2_shield": [
      117,
      118
    ],
    "ally_slot_2_unit_type_stalker": [
      118,
      119
    ],
    "ally_slot_2_unit_type_zealot": [
      119,
      120
    ],
    "ally_slot_2_unit_type_colossus": [
      120,
      121
    ],
    "ally_slot_3_visible": [
      121,
      122
    ],
    "ally_slot_3_distance": [
      122,
      123
    ],
    "ally_slot_3_relative_x": [
      123,
      124
    ],
    "ally_slot_3_relative_y": [
      124,
      125
    ],
    "ally_slot_3_health": [
      125,
      126
    ],
    "ally_slot_3_shield": [
      126,
      127
    ],
    "ally_slot_3_unit_type_stalker": [
      127,
      128
    ],
    "ally_slot_3_unit_type_zealot": [
      128,
      129
    ],
    "ally_slot_3_unit_type_colossus": [
      129,
      130
    ],
    "ally_slot_4_visible": [
      130,
      131
    ],
    "ally_slot_4_distance": [
      131,
      132
    ],
    "ally_slot_4_relative_x": [
      132,
      133
    ],
    "ally_slot_4_relative_y": [
      133,
      134
    ],
    "ally_slot_4_health": [
      134,
      135
    ],
    "ally_slot_4_shield": [
      135,
      136
    ],
    "ally_slot_4_unit_type_stalker": [
      136,
      137
    ],
    "ally_slot_4_unit_type_zealot": [
      137,
      138
    ],
    "ally_slot_4_unit_type_colossus": [
      138,
      139
    ],
    "ally_slot_5_visible": [
      139,
      140
    ],
    "ally_slot_5_distance": [
      140,
      141
    ],
    "ally_slot_5_relative_x": [
      141,
      142
    ],
    "ally_slot_5_relative_y": [
      142,
      143
    ],
    "ally_slot_5_health": [
      143,
      144
    ],
    "ally_slot_5_shield": [
      144,
      145
    ],
    "ally_slot_5_unit_type_stalker": [
      145,
      146
    ],
    "ally_slot_5_unit_type_zealot": [
      146,
      147
    ],
    "ally_slot_5_unit_type_colossus": [
      147,
      148
    ],
    "ally_slot_6_visible": [
      148,
      149
    ],
    "ally_slot_6_distance": [
      149,
      150
    ],
    "ally_slot_6_relative_x": [
      150,
      151
    ],
    "ally_slot_6_relative_y": [
      151,
      152
    ],
    "ally_slot_6_health": [
      152,
      153
    ],
    "ally_slot_6_shield": [
      153,
      154
    ],
    "ally_slot_6_unit_type_stalker": [
      154,
      155
    ],
    "ally_slot_6_unit_type_zealot": [
      155,
      156
    ],
    "ally_slot_6_unit_type_colossus": [
      156,
      157
    ],
    "ally_slot_7_visible": [
      157,
      158
    ],
    "ally_slot_7_distance": [
      158,
      159
    ],
    "ally_slot_7_relative_x": [
      159,
      160
    ],
    "ally_slot_7_relative_y": [
      160,
      161
    ],
    "ally_slot_7_health": [
      161,
      162
    ],
    "ally_slot_7_shield": [
      162,
      163
    ],
    "ally_slot_7_unit_type_stalker": [
      163,
      164
    ],
    "ally_slot_7_unit_type_zealot": [
      164,
      165
    ],
    "ally_slot_7_unit_type_colossus": [
      165,
      166
    ],
    "ally_slot_8_visible": [
      166,
      167
    ],
    "ally_slot_8_distance": [
      167,
      168
    ],
    "ally_slot_8_relative_x": [
      168,
      169
    ],
    "ally_slot_8_relative_y": [
      169,
      170
    ],
    "ally_slot_8_health": [
      170,
      171
    ],
    "ally_slot_8_shield": [
      171,
      172
    ],
    "ally_slot_8_unit_type_stalker": [
      172,
      173
    ],
    "ally_slot_8_unit_type_zealot": [
      173,
      174
    ],
    "ally_slot_8_unit_type_colossus": [
      174,
      175
    ],
    "own_health": [
      175,
      176
    ],
    "own_shield": [
      176,
      177
    ],
    "own_normalized_x": [
      177,
      178
    ],
    "own_normalized_y": [
      178,
      179
    ],
    "own_unit_type_stalker": [
      179,
      180
    ],
    "own_unit_type_zealot": [
      180,
      181
    ],
    "own_unit_type_colossus": [
      181,
      182
    ],
    "previous_action_0": [
      182,
      183
    ],
    "previous_action_1": [
      183,
      184
    ],
    "previous_action_2": [
      184,
      185
    ],
    "previous_action_3": [
      185,
      186
    ],
    "previous_action_4": [
      186,
      187
    ],
    "previous_action_5": [
      187,
      188
    ],
    "previous_action_6": [
      188,
      189
    ],
    "previous_action_7": [
      189,
      190
    ],
    "previous_action_8": [
      190,
      191
    ],
    "previous_action_9": [
      191,
      192
    ],
    "previous_action_10": [
      192,
      193
    ],
    "previous_action_11": [
      193,
      194
    ],
    "previous_action_12": [
      194,
      195
    ],
    "previous_action_13": [
      195,
      196
    ],
    "previous_action_14": [
      196,
      197
    ],
    "previous_action_15": [
      197,
      198
    ],
    "agent_id_0": [
      198,
      199
    ],
    "agent_id_1": [
      199,
      200
    ],
    "agent_id_2": [
      200,
      201
    ],
    "agent_id_3": [
      201,
      202
    ],
    "agent_id_4": [
      202,
      203
    ],
    "agent_id_5": [
      203,
      204
    ],
    "agent_id_6": [
      204,
      205
    ],
    "agent_id_7": [
      205,
      206
    ],
    "agent_id_8": [
      206,
      207
    ],
    "agent_id_9": [
      207,
      208
    ]
  },
  "feature_statistics": {
    "move_north": {
      "index": 0,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.093115,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.093115
    },
    "move_south": {
      "index": 1,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.092456,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.092456
    },
    "move_east": {
      "index": 2,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.09436,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.09436
    },
    "move_west": {
      "index": 3,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.090723,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.090723
    },
    "enemy_0_available": {
      "index": 4,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.026172,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.026172
    },
    "enemy_0_distance": {
      "index": 5,
      "min": 0.0,
      "max": 0.999955,
      "mean": 0.025034,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043945
    },
    "enemy_0_relative_x": {
      "index": 6,
      "min": -0.986111,
      "max": 0.9815,
      "mean": -0.005627,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043945
    },
    "enemy_0_relative_y": {
      "index": 7,
      "min": -0.990885,
      "max": 0.979167,
      "mean": 0.001094,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043945
    },
    "enemy_0_health": {
      "index": 8,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.040956,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043945
    },
    "enemy_0_shield": {
      "index": 9,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.0252,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.034058
    },
    "enemy_0_unit_type_stalker": {
      "index": 10,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.018286,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.018286
    },
    "enemy_0_unit_type_zealot": {
      "index": 11,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.023535,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.023535
    },
    "enemy_0_unit_type_colossus": {
      "index": 12,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.002124,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.002124
    },
    "enemy_1_available": {
      "index": 13,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025977,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025977
    },
    "enemy_1_distance": {
      "index": 14,
      "min": 0.0,
      "max": 0.999898,
      "mean": 0.02206,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.040918
    },
    "enemy_1_relative_x": {
      "index": 15,
      "min": -0.987223,
      "max": 0.994819,
      "mean": 0.000598,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.040918
    },
    "enemy_1_relative_y": {
      "index": 16,
      "min": -0.986545,
      "max": 0.988797,
      "mean": 4.5e-05,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.040747
    },
    "enemy_1_health": {
      "index": 17,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.03813,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.040918
    },
    "enemy_1_shield": {
      "index": 18,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.023456,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.031592
    },
    "enemy_1_unit_type_stalker": {
      "index": 19,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.011987,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.011987
    },
    "enemy_1_unit_type_zealot": {
      "index": 20,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025293,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025293
    },
    "enemy_1_unit_type_colossus": {
      "index": 21,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.003638,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.003638
    },
    "enemy_2_available": {
      "index": 22,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.029614,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029614
    },
    "enemy_2_distance": {
      "index": 23,
      "min": 0.0,
      "max": 0.999585,
      "mean": 0.025961,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046973
    },
    "enemy_2_relative_x": {
      "index": 24,
      "min": -0.988281,
      "max": 0.985243,
      "mean": -4.6e-05,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046973
    },
    "enemy_2_relative_y": {
      "index": 25,
      "min": -0.966363,
      "max": 0.949192,
      "mean": -0.008117,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046973
    },
    "enemy_2_health": {
      "index": 26,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.042939,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046973
    },
    "enemy_2_shield": {
      "index": 27,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.028073,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.034692
    },
    "enemy_2_unit_type_stalker": {
      "index": 28,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.016675,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.016675
    },
    "enemy_2_unit_type_zealot": {
      "index": 29,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.030298,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.030298
    },
    "enemy_2_unit_type_colossus": {
      "index": 30,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_3_available": {
      "index": 31,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.02605,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02605
    },
    "enemy_3_distance": {
      "index": 32,
      "min": 0.0,
      "max": 0.998501,
      "mean": 0.02433,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043481
    },
    "enemy_3_relative_x": {
      "index": 33,
      "min": -0.975098,
      "max": 0.989719,
      "mean": -0.002499,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043481
    },
    "enemy_3_relative_y": {
      "index": 34,
      "min": -0.946479,
      "max": 0.982693,
      "mean": -0.005565,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043408
    },
    "enemy_3_health": {
      "index": 35,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.039795,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043481
    },
    "enemy_3_shield": {
      "index": 36,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.026553,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.034961
    },
    "enemy_3_unit_type_stalker": {
      "index": 37,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.019824,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.019824
    },
    "enemy_3_unit_type_zealot": {
      "index": 38,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.023657,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.023657
    },
    "enemy_3_unit_type_colossus": {
      "index": 39,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_4_available": {
      "index": 40,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021802,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021802
    },
    "enemy_4_distance": {
      "index": 41,
      "min": 0.0,
      "max": 0.999956,
      "mean": 0.0222,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.038599
    },
    "enemy_4_relative_x": {
      "index": 42,
      "min": -0.974691,
      "max": 0.992486,
      "mean": -0.004495,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.038599
    },
    "enemy_4_relative_y": {
      "index": 43,
      "min": -0.98055,
      "max": 0.86716,
      "mean": -0.00626,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.038452
    },
    "enemy_4_health": {
      "index": 44,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.036426,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.038599
    },
    "enemy_4_shield": {
      "index": 45,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.023851,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.031567
    },
    "enemy_4_unit_type_stalker": {
      "index": 46,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.006274,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.006274
    },
    "enemy_4_unit_type_zealot": {
      "index": 47,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.026465,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.026465
    },
    "enemy_4_unit_type_colossus": {
      "index": 48,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.005859,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.005859
    },
    "enemy_5_available": {
      "index": 49,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.020117,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.020117
    },
    "enemy_5_distance": {
      "index": 50,
      "min": 0.0,
      "max": 0.999021,
      "mean": 0.020827,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0354
    },
    "enemy_5_relative_x": {
      "index": 51,
      "min": -0.95006,
      "max": 0.997531,
      "mean": -0.003592,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0354
    },
    "enemy_5_relative_y": {
      "index": 52,
      "min": -0.985189,
      "max": 0.955105,
      "mean": -0.007829,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.035376
    },
    "enemy_5_health": {
      "index": 53,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.033157,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0354
    },
    "enemy_5_shield": {
      "index": 54,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025906,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029126
    },
    "enemy_5_unit_type_stalker": {
      "index": 55,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.01333,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.01333
    },
    "enemy_5_unit_type_zealot": {
      "index": 56,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.018042,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.018042
    },
    "enemy_5_unit_type_colossus": {
      "index": 57,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.004028,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.004028
    },
    "enemy_6_available": {
      "index": 58,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.030859,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.030859
    },
    "enemy_6_distance": {
      "index": 59,
      "min": 0.0,
      "max": 0.999818,
      "mean": 0.022111,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043945
    },
    "enemy_6_relative_x": {
      "index": 60,
      "min": -0.94892,
      "max": 0.990397,
      "mean": -0.003139,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043945
    },
    "enemy_6_relative_y": {
      "index": 61,
      "min": -0.994982,
      "max": 0.971191,
      "mean": -0.005008,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043579
    },
    "enemy_6_health": {
      "index": 62,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.039731,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043945
    },
    "enemy_6_shield": {
      "index": 63,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.017403,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.030396
    },
    "enemy_6_unit_type_stalker": {
      "index": 64,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.010303,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.010303
    },
    "enemy_6_unit_type_zealot": {
      "index": 65,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.031177,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.031177
    },
    "enemy_6_unit_type_colossus": {
      "index": 66,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.002466,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.002466
    },
    "enemy_7_available": {
      "index": 67,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.026636,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.026636
    },
    "enemy_7_distance": {
      "index": 68,
      "min": 0.0,
      "max": 0.999863,
      "mean": 0.0229,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.041919
    },
    "enemy_7_relative_x": {
      "index": 69,
      "min": -0.917019,
      "max": 0.999023,
      "mean": 0.001092,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.041919
    },
    "enemy_7_relative_y": {
      "index": 70,
      "min": -0.980849,
      "max": 0.987305,
      "mean": -0.003758,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.04187
    },
    "enemy_7_health": {
      "index": 71,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.037481,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.041919
    },
    "enemy_7_shield": {
      "index": 72,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021422,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.032495
    },
    "enemy_7_unit_type_stalker": {
      "index": 73,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.019653,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.019653
    },
    "enemy_7_unit_type_zealot": {
      "index": 74,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.020312,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.020312
    },
    "enemy_7_unit_type_colossus": {
      "index": 75,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001953,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001953
    },
    "enemy_8_available": {
      "index": 76,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.016992,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.016992
    },
    "enemy_8_distance": {
      "index": 77,
      "min": 0.0,
      "max": 0.999803,
      "mean": 0.02123,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.033472
    },
    "enemy_8_relative_x": {
      "index": 78,
      "min": -0.955024,
      "max": 0.984022,
      "mean": 0.003324,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.033472
    },
    "enemy_8_relative_y": {
      "index": 79,
      "min": -0.907552,
      "max": 0.986762,
      "mean": 0.000658,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.033423
    },
    "enemy_8_health": {
      "index": 80,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.031962,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.033472
    },
    "enemy_8_shield": {
      "index": 81,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021965,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.030811
    },
    "enemy_8_unit_type_stalker": {
      "index": 82,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.024902,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.024902
    },
    "enemy_8_unit_type_zealot": {
      "index": 83,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.008569,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.008569
    },
    "enemy_8_unit_type_colossus": {
      "index": 84,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_9_available": {
      "index": 85,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021216,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021216
    },
    "enemy_9_distance": {
      "index": 86,
      "min": 0.0,
      "max": 0.99991,
      "mean": 0.025701,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.041699
    },
    "enemy_9_relative_x": {
      "index": 87,
      "min": -0.980577,
      "max": 0.990316,
      "mean": 0.004289,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.041699
    },
    "enemy_9_relative_y": {
      "index": 88,
      "min": -0.96639,
      "max": 0.964979,
      "mean": -0.007357,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.041577
    },
    "enemy_9_health": {
      "index": 89,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.040383,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.041699
    },
    "enemy_9_shield": {
      "index": 90,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.028264,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.036328
    },
    "enemy_9_unit_type_stalker": {
      "index": 91,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.027295,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027295
    },
    "enemy_9_unit_type_zealot": {
      "index": 92,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013354,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013354
    },
    "enemy_9_unit_type_colossus": {
      "index": 93,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00105,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00105
    },
    "ally_slot_0_visible": {
      "index": 94,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.042407,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042407
    },
    "ally_slot_0_distance": {
      "index": 95,
      "min": 0.0,
      "max": 0.999411,
      "mean": 0.019826,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042334
    },
    "ally_slot_0_relative_x": {
      "index": 96,
      "min": -0.992405,
      "max": 0.94477,
      "mean": -0.002041,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.041968
    },
    "ally_slot_0_relative_y": {
      "index": 97,
      "min": -0.98112,
      "max": 0.985433,
      "mean": -0.001219,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042017
    },
    "ally_slot_0_health": {
      "index": 98,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.03823,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042407
    },
    "ally_slot_0_shield": {
      "index": 99,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.027389,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.033008
    },
    "ally_slot_0_unit_type_stalker": {
      "index": 100,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.017212,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017212
    },
    "ally_slot_0_unit_type_zealot": {
      "index": 101,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_0_unit_type_colossus": {
      "index": 102,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025195,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025195
    },
    "ally_slot_1_visible": {
      "index": 103,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.046948,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046948
    },
    "ally_slot_1_distance": {
      "index": 104,
      "min": 0.0,
      "max": 0.998395,
      "mean": 0.022991,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046899
    },
    "ally_slot_1_relative_x": {
      "index": 105,
      "min": -0.965115,
      "max": 0.98782,
      "mean": -0.002238,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046655
    },
    "ally_slot_1_relative_y": {
      "index": 106,
      "min": -0.992486,
      "max": 0.941759,
      "mean": 0.001618,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046729
    },
    "ally_slot_1_health": {
      "index": 107,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.045558,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046948
    },
    "ally_slot_1_shield": {
      "index": 108,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.040775,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043555
    },
    "ally_slot_1_unit_type_stalker": {
      "index": 109,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.037891,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.037891
    },
    "ally_slot_1_unit_type_zealot": {
      "index": 110,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_1_unit_type_colossus": {
      "index": 111,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.009058,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.009058
    },
    "ally_slot_2_visible": {
      "index": 112,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.050269,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.050269
    },
    "ally_slot_2_distance": {
      "index": 113,
      "min": 0.0,
      "max": 0.999821,
      "mean": 0.025426,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.118145,
      "nonzero_rate": 0.050269
    },
    "ally_slot_2_relative_x": {
      "index": 114,
      "min": -0.94477,
      "max": 0.969889,
      "mean": 0.002182,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.049902
    },
    "ally_slot_2_relative_y": {
      "index": 115,
      "min": -0.97385,
      "max": 0.97385,
      "mean": -0.000319,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.050146
    },
    "ally_slot_2_health": {
      "index": 116,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.048344,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.076904,
      "nonzero_rate": 0.050269
    },
    "ally_slot_2_shield": {
      "index": 117,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.040773,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044995
    },
    "ally_slot_2_unit_type_stalker": {
      "index": 118,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.04895,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.04895
    },
    "ally_slot_2_unit_type_zealot": {
      "index": 119,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.000977,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.000977
    },
    "ally_slot_2_unit_type_colossus": {
      "index": 120,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.000342,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.000342
    },
    "ally_slot_3_visible": {
      "index": 121,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.043677,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043677
    },
    "ally_slot_3_distance": {
      "index": 122,
      "min": 0.0,
      "max": 0.997931,
      "mean": 0.023051,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043652
    },
    "ally_slot_3_relative_x": {
      "index": 123,
      "min": -0.991916,
      "max": 0.994032,
      "mean": 0.003239,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043286
    },
    "ally_slot_3_relative_y": {
      "index": 124,
      "min": -0.953776,
      "max": 0.992486,
      "mean": 0.000102,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043481
    },
    "ally_slot_3_health": {
      "index": 125,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.042178,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043677
    },
    "ally_slot_3_shield": {
      "index": 126,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.035176,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.039648
    },
    "ally_slot_3_unit_type_stalker": {
      "index": 127,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.038208,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.038208
    },
    "ally_slot_3_unit_type_zealot": {
      "index": 128,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.005469,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.005469
    },
    "ally_slot_3_unit_type_colossus": {
      "index": 129,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_4_visible": {
      "index": 130,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.042871,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042871
    },
    "ally_slot_4_distance": {
      "index": 131,
      "min": 0.0,
      "max": 0.999821,
      "mean": 0.02348,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042871
    },
    "ally_slot_4_relative_x": {
      "index": 132,
      "min": -0.969889,
      "max": 0.856391,
      "mean": -0.00125,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042847
    },
    "ally_slot_4_relative_y": {
      "index": 133,
      "min": -0.989204,
      "max": 0.994005,
      "mean": 0.001272,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042725
    },
    "ally_slot_4_health": {
      "index": 134,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.039951,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042871
    },
    "ally_slot_4_shield": {
      "index": 135,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.030827,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.036011
    },
    "ally_slot_4_unit_type_stalker": {
      "index": 136,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.028491,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028491
    },
    "ally_slot_4_unit_type_zealot": {
      "index": 137,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.01438,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.01438
    },
    "ally_slot_4_unit_type_colossus": {
      "index": 138,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_5_visible": {
      "index": 139,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.050879,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.050879
    },
    "ally_slot_5_distance": {
      "index": 140,
      "min": 0.0,
      "max": 0.998395,
      "mean": 0.028227,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.118148,
      "nonzero_rate": 0.050879
    },
    "ally_slot_5_relative_x": {
      "index": 141,
      "min": -0.994927,
      "max": 0.958333,
      "mean": -9.8e-05,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.050757
    },
    "ally_slot_5_relative_y": {
      "index": 142,
      "min": -0.985433,
      "max": 0.955024,
      "mean": -0.001266,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.05083
    },
    "ally_slot_5_health": {
      "index": 143,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.047241,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.16,
      "nonzero_rate": 0.050879
    },
    "ally_slot_5_shield": {
      "index": 144,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.038125,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042822
    },
    "ally_slot_5_unit_type_stalker": {
      "index": 145,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.015967,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.015967
    },
    "ally_slot_5_unit_type_zealot": {
      "index": 146,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.034912,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.034912
    },
    "ally_slot_5_unit_type_colossus": {
      "index": 147,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_6_visible": {
      "index": 148,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.046655,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046655
    },
    "ally_slot_6_distance": {
      "index": 149,
      "min": 0.0,
      "max": 0.997062,
      "mean": 0.02268,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046631
    },
    "ally_slot_6_relative_x": {
      "index": 150,
      "min": -0.966634,
      "max": 0.965115,
      "mean": -0.00085,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046387
    },
    "ally_slot_6_relative_y": {
      "index": 151,
      "min": -0.994005,
      "max": 0.964111,
      "mean": 0.002978,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.04646
    },
    "ally_slot_6_health": {
      "index": 152,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.043733,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046655
    },
    "ally_slot_6_shield": {
      "index": 153,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.035684,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.039941
    },
    "ally_slot_6_unit_type_stalker": {
      "index": 154,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.004443,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.004443
    },
    "ally_slot_6_unit_type_zealot": {
      "index": 155,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.042212,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042212
    },
    "ally_slot_6_unit_type_colossus": {
      "index": 156,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_7_visible": {
      "index": 157,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.046606,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046606
    },
    "ally_slot_7_distance": {
      "index": 158,
      "min": 0.0,
      "max": 0.999073,
      "mean": 0.022159,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046606
    },
    "ally_slot_7_relative_x": {
      "index": 159,
      "min": -0.998644,
      "max": 0.991916,
      "mean": -0.0011,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046509
    },
    "ally_slot_7_relative_y": {
      "index": 160,
      "min": -0.962484,
      "max": 0.954915,
      "mean": 0.000864,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046558
    },
    "ally_slot_7_health": {
      "index": 161,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.043534,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046606
    },
    "ally_slot_7_shield": {
      "index": 162,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.032219,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.038452
    },
    "ally_slot_7_unit_type_stalker": {
      "index": 163,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.000513,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.000513
    },
    "ally_slot_7_unit_type_zealot": {
      "index": 164,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.046094,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046094
    },
    "ally_slot_7_unit_type_colossus": {
      "index": 165,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_8_visible": {
      "index": 166,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.044922,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044922
    },
    "ally_slot_8_distance": {
      "index": 167,
      "min": 0.0,
      "max": 0.999411,
      "mean": 0.021421,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044897
    },
    "ally_slot_8_relative_x": {
      "index": 168,
      "min": -0.98782,
      "max": 0.998644,
      "mean": 0.002155,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044775
    },
    "ally_slot_8_relative_y": {
      "index": 169,
      "min": -0.94732,
      "max": 0.962484,
      "mean": -0.004031,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.04458
    },
    "ally_slot_8_health": {
      "index": 170,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.040069,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044922
    },
    "ally_slot_8_shield": {
      "index": 171,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.028295,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.034985
    },
    "ally_slot_8_unit_type_stalker": {
      "index": 172,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_8_unit_type_zealot": {
      "index": 173,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.044922,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044922
    },
    "ally_slot_8_unit_type_colossus": {
      "index": 174,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "own_health": {
      "index": 175,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.085444,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.094434
    },
    "own_shield": {
      "index": 176,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.064896,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.075195
    },
    "own_normalized_x": {
      "index": 177,
      "min": 0.0,
      "max": 0.923828,
      "mean": 0.037688,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.411942,
      "nonzero_rate": 0.094434
    },
    "own_normalized_y": {
      "index": 178,
      "min": 0.0,
      "max": 0.927277,
      "mean": 0.046065,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.480354,
      "nonzero_rate": 0.094434
    },
    "own_unit_type_stalker": {
      "index": 179,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.044238,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044238
    },
    "own_unit_type_zealot": {
      "index": 180,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.041406,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.041406
    },
    "own_unit_type_colossus": {
      "index": 181,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.008789,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.008789
    },
    "previous_action_0": {
      "index": 182,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.066455,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.066455
    },
    "previous_action_1": {
      "index": 183,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.016016,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.016016
    },
    "previous_action_2": {
      "index": 184,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013647,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013647
    },
    "previous_action_3": {
      "index": 185,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.014429,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.014429
    },
    "previous_action_4": {
      "index": 186,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.01438,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.01438
    },
    "previous_action_5": {
      "index": 187,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.012695,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.012695
    },
    "previous_action_6": {
      "index": 188,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.002515,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.002515
    },
    "previous_action_7": {
      "index": 189,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.002783,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.002783
    },
    "previous_action_8": {
      "index": 190,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.002808,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.002808
    },
    "previous_action_9": {
      "index": 191,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.002344,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.002344
    },
    "previous_action_10": {
      "index": 192,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001953,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001953
    },
    "previous_action_11": {
      "index": 193,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001831,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001831
    },
    "previous_action_12": {
      "index": 194,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.003076,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.003076
    },
    "previous_action_13": {
      "index": 195,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.002539,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.002539
    },
    "previous_action_14": {
      "index": 196,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001636,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001636
    },
    "previous_action_15": {
      "index": 197,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001782,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001782
    },
    "agent_id_0": {
      "index": 198,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_1": {
      "index": 199,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_2": {
      "index": 200,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_3": {
      "index": 201,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_4": {
      "index": 202,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_5": {
      "index": 203,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_6": {
      "index": 204,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_7": {
      "index": 205,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_8": {
      "index": 206,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_9": {
      "index": 207,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    }
  },
  "alignment_note": "rollout_obs_dim is exactly the RL communication input: raw observation + previous-action one-hot + agent-id one-hot. Feature positions are identical in offline evaluation and RL training."
}

Current code:
```python
import torch


def message_design_instruction():
    """
    Communication design for protoss_10_vs_10 (SMACv2).
    Unit types are dynamic: stalker, zealot, colossus.
    No self-communication; agents talk across unit types (R1-R3).
    The who graph connects each unit type to the other two types.
    The when mask triggers on ANY enemy or ally visibility (using all slots).
    The what mask shares own (x,y) coordinates plus only the slots that are
    currently observed (per-slot availability > 0.5), reducing message noise.

    Revision based on judge feedback:
    - when now uses torch.any over all enemy_available and all ally_visible slots.
    - what dynamically includes only visible slots, not all slots.
    """
    return (
        "Cross-type communication policy: "
        "who: edges from each unit type to the other two types; "
        "when: triggered when sender sees ANY enemy or ANY ally; "
        "what: own position + inventory of only the currently observed entities."
    )


def _add_group_links(who, sender_mask, receiver_mask):
    """
    Add directed edges from any agent with sender_mask True to any agent with receiver_mask True.
    who: (B, N, N) modified in-place.
    """
    who.add_(receiver_mask.unsqueeze(2).float() * sender_mask.unsqueeze(1).float())


def _apply_what_mask(what_mask, condition, feature_indices):
    """
    Set given feature indices to 1 for all senders where condition is True.
    what_mask: (B, N, D) modified in-place.
    condition: (B, N) bool
    feature_indices: (F,) long tensor
    """
    B, N, D = what_mask.shape
    valid_flat = condition.reshape(-1).nonzero(as_tuple=False).squeeze(1)  # (num_true,)
    if valid_flat.size(0) == 0:
        return
    batch_idx = valid_flat // N
    agent_idx = valid_flat % N
    F = feature_indices.size(0)
    num_true = valid_flat.size(0)
    rep_batch = batch_idx.repeat_interleave(F)
    rep_agent = agent_idx.repeat_interleave(F)
    rep_feat = feature_indices.repeat(num_true)
    what_mask[rep_batch, rep_agent, rep_feat] = 1.0


def communication_who(o):
    B, N, D = o.shape
    is_stalker = o[..., 179] > 0.5   # own_unit_type_stalker
    is_zealot  = o[..., 180] > 0.5   # own_unit_type_zealot
    is_colossus = o[..., 181] > 0.5  # own_unit_type_colossus

    who = torch.zeros(B, N, N, device=o.device)

    # RULE R1: G1 (zealots) -> G2 or G3
    _add_group_links(who, is_zealot, is_stalker | is_colossus)
    # RULE R2: G2 (stalkers) -> G1 or G3
    _add_group_links(who, is_stalker, is_zealot | is_colossus)
    # RULE R3: G3 (colossi) -> G1 or G2
    _add_group_links(who, is_colossus, is_zealot | is_stalker)

    # Zero diagonal (no self-communication)
    diag = torch.diag_embed(who.diagonal(dim1=1, dim2=2))
    who = who - diag
    who.clamp_(0.0, 1.0)
    return who


def communication_when(o):
    B, N, D = o.shape
    is_stalker = o[..., 179] > 0.5
    is_zealot  = o[..., 180] > 0.5
    is_colossus = o[..., 181] > 0.5

    # Revised trigger: any enemy or any ally visible, not just slot 0.
    enemy_available_indices = [4, 13, 22, 31, 40, 49, 58, 67, 76, 85]
    ally_visible_indices   = [94, 103, 112, 121, 130, 139, 148, 157, 166]

    enemy_visible = torch.any(o[..., enemy_available_indices] > 0.5, dim=-1)  # (B, N)
    ally_visible  = torch.any(o[..., ally_visible_indices] > 0.5, dim=-1)    # (B, N)

    def sender_condition(cond):
        return cond.unsqueeze(1).expand(-1, N, -1)  # (B, N, N)

    when = torch.zeros(B, N, N, device=o.device)

    # RULE R1 (zealot, enemy)
    when = when + sender_condition(is_zealot & enemy_visible)
    # RULE R2 (stalker, enemy)
    when = when + sender_condition(is_stalker & enemy_visible)
    # RULE R3 (colossus, enemy)
    when = when + sender_condition(is_colossus & enemy_visible)
    # RULE R4 (zealot, ally)
    when = when + sender_condition(is_zealot & ally_visible)
    # RULE R5 (stalker, ally)
    when = when + sender_condition(is_stalker & ally_visible)
    # RULE R6 (colossus, ally)
    when = when + sender_condition(is_colossus & ally_visible)

    diag = torch.diag_embed(when.diagonal(dim1=1, dim2=2))
    when = when - diag
    when.clamp_(0.0, 1.0)
    return when


def communication_what(o):
    B, N, D = o.shape
    device = o.device

    # unit-type conditions
    is_stalker = o[..., 179] > 0.5
    is_zealot  = o[..., 180] > 0.5
    is_colossus = o[..., 181] > 0.5

    # Revised: any enemy/ally visible for the overall trigger
    enemy_available_indices = torch.tensor([4, 13, 22, 31, 40, 49, 58, 67, 76, 85], device=device)
    ally_visible_indices   = torch.tensor([94, 103, 112, 121, 130, 139, 148, 157, 166], device=device)

    enemy_any = torch.any(o[..., enemy_available_indices] > 0.5, dim=-1)  # (B, N)
    ally_any  = torch.any(o[..., ally_visible_indices] > 0.5, dim=-1)      # (B, N)

    # Precompute feature block indices for each enemy/ally slot (excluding distance)
    # Enemy block: size 9, indices: available(0), distance(1 skipped), rel_x(2), rel_y(3),
    # health(4), shield(5), type_stalker(6), type_zealot(7), type_colossus(8)
    offs = torch.tensor([0, 2, 3, 4, 5, 6, 7, 8], dtype=torch.long, device=device)
    n_enemy_slots = 10
    n_ally_slots = 9
    enemy_start = 4
    ally_start = 94

    enemy_slot_indices = []   # list of tensors, each shape (8,)
    for i in range(n_enemy_slots):
        base = enemy_start + i * 9
        inds = base + offs
        enemy_slot_indices.append(inds)

    ally_slot_indices = []
    for i in range(n_ally_slots):
        base = ally_start + i * 9
        inds = base + offs
        ally_slot_indices.append(inds)

    # Own position features (normalized x and y)
    own_pos = torch.tensor([177, 178], device=device)

    what_mask = torch.zeros(B, N, D, device=device)

    # Helper to apply per-slot features for a given trigger condition
    def add_slot_features(trigger_condition, slot_indices_list, slot_available_flags, is_enemy=True):
        """
        trigger_condition: (B, N) bool, agents that should share these entities.
        slot_indices_list: list of tensors (8,) for each slot.
        slot_available_flags: (B, N, num_slots) raw values (continuous) to threshold.
        """
        # Set own position once per triggered agent
        _apply_what_mask(what_mask, trigger_condition, own_pos)

        num_slots = len(slot_indices_list)
        for s in range(num_slots):
            if is_enemy:
                slot_visible = o[..., enemy_available_indices[s]] > 0.5
            else:
                slot_visible = o[..., ally_visible_indices[s]] > 0.5
            cond_slot = trigger_condition & slot_visible
            _apply_what_mask(what_mask, cond_slot, slot_indices_list[s])

    # Apply rules
    # RULE R1: zealot sees enemy -> share enemy inventory (only visible slots)
    add_slot_features(is_zealot & enemy_any, enemy_slot_indices, enemy_available_indices, is_enemy=True)
    # RULE R2: stalker sees enemy -> share enemy inventory
    add_slot_features(is_stalker & enemy_any, enemy_slot_indices, enemy_available_indices, is_enemy=True)
    # RULE R3: colossus sees enemy -> share enemy inventory
    add_slot_features(is_colossus & enemy_any, enemy_slot_indices, enemy_available_indices, is_enemy=True)
    # RULE R4: zealot sees ally -> share ally inventory (only visible slots)
    add_slot_features(is_zealot & ally_any, ally_slot_indices, ally_visible_indices, is_enemy=False)
    # RULE R5: stalker sees ally -> share ally inventory
    add_slot_features(is_stalker & ally_any, ally_slot_indices, ally_visible_indices, is_enemy=False)
    # RULE R6: colossus sees ally -> share ally inventory
    add_slot_features(is_colossus & ally_any, ally_slot_indices, ally_visible_indices, is_enemy=False)

    return what_mask


# The main communication function expected by the framework
def communication(o):
    who = communication_who(o)
    when = communication_when(o)
    what = communication_what(o)
    return who, when, what

```

Return a complete corrected Python file. Preserve message_design_instruction, communication,
communication_who, communication_when, and communication_what.
