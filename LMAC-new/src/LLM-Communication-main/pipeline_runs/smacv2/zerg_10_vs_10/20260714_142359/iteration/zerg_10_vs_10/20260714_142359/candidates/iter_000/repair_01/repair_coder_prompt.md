## system

You are a MARL communication-policy coding agent. Return only one complete Python file in a single ```python code block```.

## user

Repair this LMAC teacher communication policy for `zerg_10_vs_10`.

Validation error:
Traceback (most recent call last):
  File "/data/hp/LLM_Communication/LMAC-new/src/hl_comm/candidate_io.py", line 66, in validate_candidate
    return _validate_candidate(path, map_name, rollout_summary=rollout_summary)
  File "/data/hp/LLM_Communication/LMAC-new/src/hl_comm/candidate_io.py", line 94, in _validate_candidate
    raise RuntimeError(f"Candidate is missing required functions: {missing}")
RuntimeError: Candidate is missing required functions: ['message_design_instruction']


Map spec:
{
  "environment": "smacv2",
  "n_agents": 10,
  "n_enemies": 10,
  "obs_dim": 188,
  "documented_raw_obs_dim": 162,
  "time_seq": 10,
  "dynamic_agent_roles": true,
  "possible_unit_types": [
    "zergling",
    "hydralisk",
    "baneling"
  ],
  "agent_id_role_warning": "Agent ID does not identify a fixed unit type across episodes."
}

Rollout-backed LMAC observation alignment:
{
  "map_name": "zerg_10_vs_10",
  "rollout_root": "/data/hp/LLM_Communication/LMAC-new/data/smacv2",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0000.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0001.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0002.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0003.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0004.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0005.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0006.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0007.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0008.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0009.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0010.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0011.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0012.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0013.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0014.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0015.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0016.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0017.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0018.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0019.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0020.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0021.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0022.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0023.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0024.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0025.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0026.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0027.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0028.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0029.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0030.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0031.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0032.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0033.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0034.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0035.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0036.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0037.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0038.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0039.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0040.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0041.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0042.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0043.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0044.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0045.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0046.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0047.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0048.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0049.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0050.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0051.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0052.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0053.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0054.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0055.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0056.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0057.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0058.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0059.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0060.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0061.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0062.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/zerg_10_vs_10/train_traj_0063.pkl"
  ],
  "available": true,
  "n_agents": 10,
  "raw_obs_dim": 162,
  "rollout_obs_dim": 188,
  "documented_obs_dim": 162,
  "extra_obs_dim": 0,
  "episodes": 64,
  "transitions": 2226,
  "seq_lengths": [
    38,
    52,
    30,
    28,
    33,
    37,
    42,
    28,
    35,
    30,
    26,
    33,
    35,
    33,
    38,
    45,
    45,
    30,
    40,
    33,
    36,
    36,
    33,
    41,
    27,
    32,
    39,
    41,
    41,
    40,
    39,
    53,
    28,
    41,
    30,
    39,
    35,
    30,
    31,
    40,
    34,
    34,
    32,
    22,
    39,
    37,
    42,
    30,
    31,
    33,
    23,
    28,
    30,
    32,
    24,
    32,
    44,
    36,
    31,
    27,
    39,
    41,
    33,
    29
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
    "enemy_0_unit_type_zergling": [
      9,
      10
    ],
    "enemy_0_unit_type_hydralisk": [
      10,
      11
    ],
    "enemy_0_unit_type_baneling": [
      11,
      12
    ],
    "enemy_1_available": [
      12,
      13
    ],
    "enemy_1_distance": [
      13,
      14
    ],
    "enemy_1_relative_x": [
      14,
      15
    ],
    "enemy_1_relative_y": [
      15,
      16
    ],
    "enemy_1_health": [
      16,
      17
    ],
    "enemy_1_unit_type_zergling": [
      17,
      18
    ],
    "enemy_1_unit_type_hydralisk": [
      18,
      19
    ],
    "enemy_1_unit_type_baneling": [
      19,
      20
    ],
    "enemy_2_available": [
      20,
      21
    ],
    "enemy_2_distance": [
      21,
      22
    ],
    "enemy_2_relative_x": [
      22,
      23
    ],
    "enemy_2_relative_y": [
      23,
      24
    ],
    "enemy_2_health": [
      24,
      25
    ],
    "enemy_2_unit_type_zergling": [
      25,
      26
    ],
    "enemy_2_unit_type_hydralisk": [
      26,
      27
    ],
    "enemy_2_unit_type_baneling": [
      27,
      28
    ],
    "enemy_3_available": [
      28,
      29
    ],
    "enemy_3_distance": [
      29,
      30
    ],
    "enemy_3_relative_x": [
      30,
      31
    ],
    "enemy_3_relative_y": [
      31,
      32
    ],
    "enemy_3_health": [
      32,
      33
    ],
    "enemy_3_unit_type_zergling": [
      33,
      34
    ],
    "enemy_3_unit_type_hydralisk": [
      34,
      35
    ],
    "enemy_3_unit_type_baneling": [
      35,
      36
    ],
    "enemy_4_available": [
      36,
      37
    ],
    "enemy_4_distance": [
      37,
      38
    ],
    "enemy_4_relative_x": [
      38,
      39
    ],
    "enemy_4_relative_y": [
      39,
      40
    ],
    "enemy_4_health": [
      40,
      41
    ],
    "enemy_4_unit_type_zergling": [
      41,
      42
    ],
    "enemy_4_unit_type_hydralisk": [
      42,
      43
    ],
    "enemy_4_unit_type_baneling": [
      43,
      44
    ],
    "enemy_5_available": [
      44,
      45
    ],
    "enemy_5_distance": [
      45,
      46
    ],
    "enemy_5_relative_x": [
      46,
      47
    ],
    "enemy_5_relative_y": [
      47,
      48
    ],
    "enemy_5_health": [
      48,
      49
    ],
    "enemy_5_unit_type_zergling": [
      49,
      50
    ],
    "enemy_5_unit_type_hydralisk": [
      50,
      51
    ],
    "enemy_5_unit_type_baneling": [
      51,
      52
    ],
    "enemy_6_available": [
      52,
      53
    ],
    "enemy_6_distance": [
      53,
      54
    ],
    "enemy_6_relative_x": [
      54,
      55
    ],
    "enemy_6_relative_y": [
      55,
      56
    ],
    "enemy_6_health": [
      56,
      57
    ],
    "enemy_6_unit_type_zergling": [
      57,
      58
    ],
    "enemy_6_unit_type_hydralisk": [
      58,
      59
    ],
    "enemy_6_unit_type_baneling": [
      59,
      60
    ],
    "enemy_7_available": [
      60,
      61
    ],
    "enemy_7_distance": [
      61,
      62
    ],
    "enemy_7_relative_x": [
      62,
      63
    ],
    "enemy_7_relative_y": [
      63,
      64
    ],
    "enemy_7_health": [
      64,
      65
    ],
    "enemy_7_unit_type_zergling": [
      65,
      66
    ],
    "enemy_7_unit_type_hydralisk": [
      66,
      67
    ],
    "enemy_7_unit_type_baneling": [
      67,
      68
    ],
    "enemy_8_available": [
      68,
      69
    ],
    "enemy_8_distance": [
      69,
      70
    ],
    "enemy_8_relative_x": [
      70,
      71
    ],
    "enemy_8_relative_y": [
      71,
      72
    ],
    "enemy_8_health": [
      72,
      73
    ],
    "enemy_8_unit_type_zergling": [
      73,
      74
    ],
    "enemy_8_unit_type_hydralisk": [
      74,
      75
    ],
    "enemy_8_unit_type_baneling": [
      75,
      76
    ],
    "enemy_9_available": [
      76,
      77
    ],
    "enemy_9_distance": [
      77,
      78
    ],
    "enemy_9_relative_x": [
      78,
      79
    ],
    "enemy_9_relative_y": [
      79,
      80
    ],
    "enemy_9_health": [
      80,
      81
    ],
    "enemy_9_unit_type_zergling": [
      81,
      82
    ],
    "enemy_9_unit_type_hydralisk": [
      82,
      83
    ],
    "enemy_9_unit_type_baneling": [
      83,
      84
    ],
    "ally_slot_0_visible": [
      84,
      85
    ],
    "ally_slot_0_distance": [
      85,
      86
    ],
    "ally_slot_0_relative_x": [
      86,
      87
    ],
    "ally_slot_0_relative_y": [
      87,
      88
    ],
    "ally_slot_0_health": [
      88,
      89
    ],
    "ally_slot_0_unit_type_zergling": [
      89,
      90
    ],
    "ally_slot_0_unit_type_hydralisk": [
      90,
      91
    ],
    "ally_slot_0_unit_type_baneling": [
      91,
      92
    ],
    "ally_slot_1_visible": [
      92,
      93
    ],
    "ally_slot_1_distance": [
      93,
      94
    ],
    "ally_slot_1_relative_x": [
      94,
      95
    ],
    "ally_slot_1_relative_y": [
      95,
      96
    ],
    "ally_slot_1_health": [
      96,
      97
    ],
    "ally_slot_1_unit_type_zergling": [
      97,
      98
    ],
    "ally_slot_1_unit_type_hydralisk": [
      98,
      99
    ],
    "ally_slot_1_unit_type_baneling": [
      99,
      100
    ],
    "ally_slot_2_visible": [
      100,
      101
    ],
    "ally_slot_2_distance": [
      101,
      102
    ],
    "ally_slot_2_relative_x": [
      102,
      103
    ],
    "ally_slot_2_relative_y": [
      103,
      104
    ],
    "ally_slot_2_health": [
      104,
      105
    ],
    "ally_slot_2_unit_type_zergling": [
      105,
      106
    ],
    "ally_slot_2_unit_type_hydralisk": [
      106,
      107
    ],
    "ally_slot_2_unit_type_baneling": [
      107,
      108
    ],
    "ally_slot_3_visible": [
      108,
      109
    ],
    "ally_slot_3_distance": [
      109,
      110
    ],
    "ally_slot_3_relative_x": [
      110,
      111
    ],
    "ally_slot_3_relative_y": [
      111,
      112
    ],
    "ally_slot_3_health": [
      112,
      113
    ],
    "ally_slot_3_unit_type_zergling": [
      113,
      114
    ],
    "ally_slot_3_unit_type_hydralisk": [
      114,
      115
    ],
    "ally_slot_3_unit_type_baneling": [
      115,
      116
    ],
    "ally_slot_4_visible": [
      116,
      117
    ],
    "ally_slot_4_distance": [
      117,
      118
    ],
    "ally_slot_4_relative_x": [
      118,
      119
    ],
    "ally_slot_4_relative_y": [
      119,
      120
    ],
    "ally_slot_4_health": [
      120,
      121
    ],
    "ally_slot_4_unit_type_zergling": [
      121,
      122
    ],
    "ally_slot_4_unit_type_hydralisk": [
      122,
      123
    ],
    "ally_slot_4_unit_type_baneling": [
      123,
      124
    ],
    "ally_slot_5_visible": [
      124,
      125
    ],
    "ally_slot_5_distance": [
      125,
      126
    ],
    "ally_slot_5_relative_x": [
      126,
      127
    ],
    "ally_slot_5_relative_y": [
      127,
      128
    ],
    "ally_slot_5_health": [
      128,
      129
    ],
    "ally_slot_5_unit_type_zergling": [
      129,
      130
    ],
    "ally_slot_5_unit_type_hydralisk": [
      130,
      131
    ],
    "ally_slot_5_unit_type_baneling": [
      131,
      132
    ],
    "ally_slot_6_visible": [
      132,
      133
    ],
    "ally_slot_6_distance": [
      133,
      134
    ],
    "ally_slot_6_relative_x": [
      134,
      135
    ],
    "ally_slot_6_relative_y": [
      135,
      136
    ],
    "ally_slot_6_health": [
      136,
      137
    ],
    "ally_slot_6_unit_type_zergling": [
      137,
      138
    ],
    "ally_slot_6_unit_type_hydralisk": [
      138,
      139
    ],
    "ally_slot_6_unit_type_baneling": [
      139,
      140
    ],
    "ally_slot_7_visible": [
      140,
      141
    ],
    "ally_slot_7_distance": [
      141,
      142
    ],
    "ally_slot_7_relative_x": [
      142,
      143
    ],
    "ally_slot_7_relative_y": [
      143,
      144
    ],
    "ally_slot_7_health": [
      144,
      145
    ],
    "ally_slot_7_unit_type_zergling": [
      145,
      146
    ],
    "ally_slot_7_unit_type_hydralisk": [
      146,
      147
    ],
    "ally_slot_7_unit_type_baneling": [
      147,
      148
    ],
    "ally_slot_8_visible": [
      148,
      149
    ],
    "ally_slot_8_distance": [
      149,
      150
    ],
    "ally_slot_8_relative_x": [
      150,
      151
    ],
    "ally_slot_8_relative_y": [
      151,
      152
    ],
    "ally_slot_8_health": [
      152,
      153
    ],
    "ally_slot_8_unit_type_zergling": [
      153,
      154
    ],
    "ally_slot_8_unit_type_hydralisk": [
      154,
      155
    ],
    "ally_slot_8_unit_type_baneling": [
      155,
      156
    ],
    "own_health": [
      156,
      157
    ],
    "own_normalized_x": [
      157,
      158
    ],
    "own_normalized_y": [
      158,
      159
    ],
    "own_unit_type_zergling": [
      159,
      160
    ],
    "own_unit_type_hydralisk": [
      160,
      161
    ],
    "own_unit_type_baneling": [
      161,
      162
    ],
    "previous_action_0": [
      162,
      163
    ],
    "previous_action_1": [
      163,
      164
    ],
    "previous_action_2": [
      164,
      165
    ],
    "previous_action_3": [
      165,
      166
    ],
    "previous_action_4": [
      166,
      167
    ],
    "previous_action_5": [
      167,
      168
    ],
    "previous_action_6": [
      168,
      169
    ],
    "previous_action_7": [
      169,
      170
    ],
    "previous_action_8": [
      170,
      171
    ],
    "previous_action_9": [
      171,
      172
    ],
    "previous_action_10": [
      172,
      173
    ],
    "previous_action_11": [
      173,
      174
    ],
    "previous_action_12": [
      174,
      175
    ],
    "previous_action_13": [
      175,
      176
    ],
    "previous_action_14": [
      176,
      177
    ],
    "previous_action_15": [
      177,
      178
    ],
    "agent_id_0": [
      178,
      179
    ],
    "agent_id_1": [
      179,
      180
    ],
    "agent_id_2": [
      180,
      181
    ],
    "agent_id_3": [
      181,
      182
    ],
    "agent_id_4": [
      182,
      183
    ],
    "agent_id_5": [
      183,
      184
    ],
    "agent_id_6": [
      184,
      185
    ],
    "agent_id_7": [
      185,
      186
    ],
    "agent_id_8": [
      186,
      187
    ],
    "agent_id_9": [
      187,
      188
    ]
  },
  "feature_statistics": {
    "move_north": {
      "index": 0,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.051611,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.051611
    },
    "move_south": {
      "index": 1,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.049414,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.049414
    },
    "move_east": {
      "index": 2,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.05188,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.05188
    },
    "move_west": {
      "index": 3,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.048291,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.048291
    },
    "enemy_0_available": {
      "index": 4,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.010864,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.010864
    },
    "enemy_0_distance": {
      "index": 5,
      "min": 0.0,
      "max": 0.998774,
      "mean": 0.009691,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017188
    },
    "enemy_0_relative_x": {
      "index": 6,
      "min": -0.890733,
      "max": 0.961751,
      "mean": 0.001189,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017188
    },
    "enemy_0_relative_y": {
      "index": 7,
      "min": -0.986925,
      "max": 0.982558,
      "mean": -0.001008,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017041
    },
    "enemy_0_health": {
      "index": 8,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.014252,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017188
    },
    "enemy_0_unit_type_zergling": {
      "index": 9,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.007031,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.007031
    },
    "enemy_0_unit_type_hydralisk": {
      "index": 10,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.006836,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.006836
    },
    "enemy_0_unit_type_baneling": {
      "index": 11,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00332,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00332
    },
    "enemy_1_available": {
      "index": 12,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.009302,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.009302
    },
    "enemy_1_distance": {
      "index": 13,
      "min": 0.0,
      "max": 0.998553,
      "mean": 0.010475,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017212
    },
    "enemy_1_relative_x": {
      "index": 14,
      "min": -0.978407,
      "max": 0.9933,
      "mean": 0.000761,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017212
    },
    "enemy_1_relative_y": {
      "index": 15,
      "min": -0.995877,
      "max": 0.970757,
      "mean": -0.004174,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017139
    },
    "enemy_1_health": {
      "index": 16,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.016111,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017212
    },
    "enemy_1_unit_type_zergling": {
      "index": 17,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00918,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00918
    },
    "enemy_1_unit_type_hydralisk": {
      "index": 18,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.008032,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.008032
    },
    "enemy_1_unit_type_baneling": {
      "index": 19,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_2_available": {
      "index": 20,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.005981,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.005981
    },
    "enemy_2_distance": {
      "index": 21,
      "min": 0.0,
      "max": 0.998161,
      "mean": 0.011995,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017212
    },
    "enemy_2_relative_x": {
      "index": 22,
      "min": -0.92589,
      "max": 0.988335,
      "mean": 0.001657,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017212
    },
    "enemy_2_relative_y": {
      "index": 23,
      "min": -0.978217,
      "max": 0.950548,
      "mean": -0.003279,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017114
    },
    "enemy_2_health": {
      "index": 24,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.015595,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017212
    },
    "enemy_2_unit_type_zergling": {
      "index": 25,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.003442,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.003442
    },
    "enemy_2_unit_type_hydralisk": {
      "index": 26,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.012646,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.012646
    },
    "enemy_2_unit_type_baneling": {
      "index": 27,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001123,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001123
    },
    "enemy_3_available": {
      "index": 28,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00835,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00835
    },
    "enemy_3_distance": {
      "index": 29,
      "min": 0.0,
      "max": 0.999423,
      "mean": 0.012427,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.019019
    },
    "enemy_3_relative_x": {
      "index": 30,
      "min": -0.947808,
      "max": 0.997667,
      "mean": 0.00448,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.019019
    },
    "enemy_3_relative_y": {
      "index": 31,
      "min": -0.969455,
      "max": 0.96129,
      "mean": -0.003827,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.01875
    },
    "enemy_3_health": {
      "index": 32,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.016812,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.019019
    },
    "enemy_3_unit_type_zergling": {
      "index": 33,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.007886,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.007886
    },
    "enemy_3_unit_type_hydralisk": {
      "index": 34,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.011133,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.011133
    },
    "enemy_3_unit_type_baneling": {
      "index": 35,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_4_available": {
      "index": 36,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.006958,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.006958
    },
    "enemy_4_distance": {
      "index": 37,
      "min": 0.0,
      "max": 0.999613,
      "mean": 0.011947,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017725
    },
    "enemy_4_relative_x": {
      "index": 38,
      "min": -0.915365,
      "max": 0.96799,
      "mean": 0.001206,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017725
    },
    "enemy_4_relative_y": {
      "index": 39,
      "min": -0.992215,
      "max": 0.952745,
      "mean": -0.003268,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017529
    },
    "enemy_4_health": {
      "index": 40,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.016279,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017725
    },
    "enemy_4_unit_type_zergling": {
      "index": 41,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.006299,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.006299
    },
    "enemy_4_unit_type_hydralisk": {
      "index": 42,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.010107,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.010107
    },
    "enemy_4_unit_type_baneling": {
      "index": 43,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001318,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001318
    },
    "enemy_5_available": {
      "index": 44,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.007104,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.007104
    },
    "enemy_5_distance": {
      "index": 45,
      "min": 0.0,
      "max": 0.99866,
      "mean": 0.010988,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.016699
    },
    "enemy_5_relative_x": {
      "index": 46,
      "min": -0.939101,
      "max": 0.986735,
      "mean": 0.001795,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.016699
    },
    "enemy_5_relative_y": {
      "index": 47,
      "min": -0.981689,
      "max": 0.929796,
      "mean": -0.005256,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.016675
    },
    "enemy_5_health": {
      "index": 48,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.01534,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.016699
    },
    "enemy_5_unit_type_zergling": {
      "index": 49,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.007422,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.007422
    },
    "enemy_5_unit_type_hydralisk": {
      "index": 50,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.008789,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.008789
    },
    "enemy_5_unit_type_baneling": {
      "index": 51,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.000488,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.000488
    },
    "enemy_6_available": {
      "index": 52,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.010815,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.010815
    },
    "enemy_6_distance": {
      "index": 53,
      "min": 0.0,
      "max": 0.999012,
      "mean": 0.010754,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.019214
    },
    "enemy_6_relative_x": {
      "index": 54,
      "min": -0.948758,
      "max": 0.982042,
      "mean": 0.002105,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.019214
    },
    "enemy_6_relative_y": {
      "index": 55,
      "min": -0.928114,
      "max": 0.981988,
      "mean": -0.003876,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.019189
    },
    "enemy_6_health": {
      "index": 56,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.01499,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.019214
    },
    "enemy_6_unit_type_zergling": {
      "index": 57,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.008447,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.008447
    },
    "enemy_6_unit_type_hydralisk": {
      "index": 58,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.010767,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.010767
    },
    "enemy_6_unit_type_baneling": {
      "index": 59,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_7_available": {
      "index": 60,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.010742,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.010742
    },
    "enemy_7_distance": {
      "index": 61,
      "min": 0.0,
      "max": 0.999427,
      "mean": 0.009291,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017017
    },
    "enemy_7_relative_x": {
      "index": 62,
      "min": -0.890272,
      "max": 0.974691,
      "mean": 0.002294,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017017
    },
    "enemy_7_relative_y": {
      "index": 63,
      "min": -0.956028,
      "max": 0.924778,
      "mean": -0.002236,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017017
    },
    "enemy_7_health": {
      "index": 64,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.014966,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017017
    },
    "enemy_7_unit_type_zergling": {
      "index": 65,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013696,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013696
    },
    "enemy_7_unit_type_hydralisk": {
      "index": 66,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00332,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00332
    },
    "enemy_7_unit_type_baneling": {
      "index": 67,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_8_available": {
      "index": 68,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013159,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013159
    },
    "enemy_8_distance": {
      "index": 69,
      "min": 0.0,
      "max": 0.998984,
      "mean": 0.01193,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021265
    },
    "enemy_8_relative_x": {
      "index": 70,
      "min": -0.906358,
      "max": 0.981228,
      "mean": 0.00352,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021265
    },
    "enemy_8_relative_y": {
      "index": 71,
      "min": -0.996826,
      "max": 0.950602,
      "mean": -0.001535,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021265
    },
    "enemy_8_health": {
      "index": 72,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.018382,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021265
    },
    "enemy_8_unit_type_zergling": {
      "index": 73,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.007764,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.007764
    },
    "enemy_8_unit_type_hydralisk": {
      "index": 74,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.011646,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.011646
    },
    "enemy_8_unit_type_baneling": {
      "index": 75,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001855,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001855
    },
    "enemy_9_available": {
      "index": 76,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.014673,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.014673
    },
    "enemy_9_distance": {
      "index": 77,
      "min": 0.0,
      "max": 0.99853,
      "mean": 0.011117,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021387
    },
    "enemy_9_relative_x": {
      "index": 78,
      "min": -0.861871,
      "max": 0.988824,
      "mean": 0.002744,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021387
    },
    "enemy_9_relative_y": {
      "index": 79,
      "min": -0.958957,
      "max": 0.950901,
      "mean": -0.001211,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02124
    },
    "enemy_9_health": {
      "index": 80,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.014549,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021387
    },
    "enemy_9_unit_type_zergling": {
      "index": 81,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.014404,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.014404
    },
    "enemy_9_unit_type_hydralisk": {
      "index": 82,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.006982,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.006982
    },
    "enemy_9_unit_type_baneling": {
      "index": 83,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_0_visible": {
      "index": 84,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.028638,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028638
    },
    "ally_slot_0_distance": {
      "index": 85,
      "min": 0.0,
      "max": 0.997668,
      "mean": 0.01361,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028638
    },
    "ally_slot_0_relative_x": {
      "index": 86,
      "min": -0.966064,
      "max": 0.932671,
      "mean": -0.001931,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028369
    },
    "ally_slot_0_relative_y": {
      "index": 87,
      "min": -0.994466,
      "max": 0.994466,
      "mean": -0.001608,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028394
    },
    "ally_slot_0_health": {
      "index": 88,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.026246,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028638
    },
    "ally_slot_0_unit_type_zergling": {
      "index": 89,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_0_unit_type_hydralisk": {
      "index": 90,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.015405,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.015405
    },
    "ally_slot_0_unit_type_baneling": {
      "index": 91,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013232,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013232
    },
    "ally_slot_1_visible": {
      "index": 92,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.034277,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.034277
    },
    "ally_slot_1_distance": {
      "index": 93,
      "min": 0.0,
      "max": 0.993814,
      "mean": 0.014811,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.034277
    },
    "ally_slot_1_relative_x": {
      "index": 94,
      "min": -0.976915,
      "max": 0.891981,
      "mean": -0.002249,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.033887
    },
    "ally_slot_1_relative_y": {
      "index": 95,
      "min": -0.978407,
      "max": 0.953206,
      "mean": 1.9e-05,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.034082
    },
    "ally_slot_1_health": {
      "index": 96,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.031438,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.034277
    },
    "ally_slot_1_unit_type_zergling": {
      "index": 97,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_1_unit_type_hydralisk": {
      "index": 98,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.031348,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.031348
    },
    "ally_slot_1_unit_type_baneling": {
      "index": 99,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00293,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00293
    },
    "ally_slot_2_visible": {
      "index": 100,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.033203,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.033203
    },
    "ally_slot_2_distance": {
      "index": 101,
      "min": 0.0,
      "max": 0.998176,
      "mean": 0.013871,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.033203
    },
    "ally_slot_2_relative_x": {
      "index": 102,
      "min": -0.940104,
      "max": 0.906006,
      "mean": 0.000394,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.03313
    },
    "ally_slot_2_relative_y": {
      "index": 103,
      "min": -0.869358,
      "max": 0.972249,
      "mean": 0.000973,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.032935
    },
    "ally_slot_2_health": {
      "index": 104,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.031135,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.033203
    },
    "ally_slot_2_unit_type_zergling": {
      "index": 105,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001416,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001416
    },
    "ally_slot_2_unit_type_hydralisk": {
      "index": 106,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.029907,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029907
    },
    "ally_slot_2_unit_type_baneling": {
      "index": 107,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00188,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00188
    },
    "ally_slot_3_visible": {
      "index": 108,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.028638,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028638
    },
    "ally_slot_3_distance": {
      "index": 109,
      "min": 0.0,
      "max": 0.998972,
      "mean": 0.012425,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028638
    },
    "ally_slot_3_relative_x": {
      "index": 110,
      "min": -0.932671,
      "max": 0.957818,
      "mean": 0.000656,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02854
    },
    "ally_slot_3_relative_y": {
      "index": 111,
      "min": -0.93259,
      "max": 0.945123,
      "mean": 0.000806,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02854
    },
    "ally_slot_3_health": {
      "index": 112,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025872,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028638
    },
    "ally_slot_3_unit_type_zergling": {
      "index": 113,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.006299,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.006299
    },
    "ally_slot_3_unit_type_hydralisk": {
      "index": 114,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.022339,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.022339
    },
    "ally_slot_3_unit_type_baneling": {
      "index": 115,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_4_visible": {
      "index": 116,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.029761,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029761
    },
    "ally_slot_4_distance": {
      "index": 117,
      "min": 0.0,
      "max": 0.98939,
      "mean": 0.012552,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029761
    },
    "ally_slot_4_relative_x": {
      "index": 118,
      "min": -0.902344,
      "max": 0.904541,
      "mean": 0.000134,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02959
    },
    "ally_slot_4_relative_y": {
      "index": 119,
      "min": -0.907633,
      "max": 0.93259,
      "mean": 0.000774,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029517
    },
    "ally_slot_4_health": {
      "index": 120,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.026626,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029761
    },
    "ally_slot_4_unit_type_zergling": {
      "index": 121,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.012939,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.012939
    },
    "ally_slot_4_unit_type_hydralisk": {
      "index": 122,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.016821,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.016821
    },
    "ally_slot_4_unit_type_baneling": {
      "index": 123,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_5_visible": {
      "index": 124,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.023291,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.023291
    },
    "ally_slot_5_distance": {
      "index": 125,
      "min": 0.0,
      "max": 0.997187,
      "mean": 0.010835,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.023291
    },
    "ally_slot_5_relative_x": {
      "index": 126,
      "min": -0.97781,
      "max": 0.959473,
      "mean": 0.001584,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.023193
    },
    "ally_slot_5_relative_y": {
      "index": 127,
      "min": -0.969998,
      "max": 0.984321,
      "mean": 0.001082,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02312
    },
    "ally_slot_5_health": {
      "index": 128,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021538,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.023291
    },
    "ally_slot_5_unit_type_zergling": {
      "index": 129,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013696,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013696
    },
    "ally_slot_5_unit_type_hydralisk": {
      "index": 130,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.009595,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.009595
    },
    "ally_slot_5_unit_type_baneling": {
      "index": 131,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_6_visible": {
      "index": 132,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025513,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025513
    },
    "ally_slot_6_distance": {
      "index": 133,
      "min": 0.0,
      "max": 0.998972,
      "mean": 0.010723,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025513
    },
    "ally_slot_6_relative_x": {
      "index": 134,
      "min": -0.93693,
      "max": 0.902344,
      "mean": -0.000563,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025049
    },
    "ally_slot_6_relative_y": {
      "index": 135,
      "min": -0.972249,
      "max": 0.94222,
      "mean": -0.001406,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025391
    },
    "ally_slot_6_health": {
      "index": 136,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.023579,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025513
    },
    "ally_slot_6_unit_type_zergling": {
      "index": 137,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.02085,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02085
    },
    "ally_slot_6_unit_type_hydralisk": {
      "index": 138,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.004663,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.004663
    },
    "ally_slot_6_unit_type_baneling": {
      "index": 139,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_7_visible": {
      "index": 140,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.026563,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.026563
    },
    "ally_slot_7_distance": {
      "index": 141,
      "min": 0.0,
      "max": 0.998176,
      "mean": 0.010994,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.026563
    },
    "ally_slot_7_relative_x": {
      "index": 142,
      "min": -0.747748,
      "max": 0.976915,
      "mean": -0.000507,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.026099
    },
    "ally_slot_7_relative_y": {
      "index": 143,
      "min": -0.97168,
      "max": 0.963786,
      "mean": -9.2e-05,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02644
    },
    "ally_slot_7_health": {
      "index": 144,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.024979,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.026563
    },
    "ally_slot_7_unit_type_zergling": {
      "index": 145,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025903,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025903
    },
    "ally_slot_7_unit_type_hydralisk": {
      "index": 146,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.000659,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.000659
    },
    "ally_slot_7_unit_type_baneling": {
      "index": 147,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_8_visible": {
      "index": 148,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.020068,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.020068
    },
    "ally_slot_8_distance": {
      "index": 149,
      "min": 0.0,
      "max": 0.997361,
      "mean": 0.008586,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.020068
    },
    "ally_slot_8_relative_x": {
      "index": 150,
      "min": -0.731852,
      "max": 0.97781,
      "mean": 0.002482,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.019897
    },
    "ally_slot_8_relative_y": {
      "index": 151,
      "min": -0.953206,
      "max": 0.978407,
      "mean": -0.000548,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02002
    },
    "ally_slot_8_health": {
      "index": 152,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.017113,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.020068
    },
    "ally_slot_8_unit_type_zergling": {
      "index": 153,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.020068,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.020068
    },
    "ally_slot_8_unit_type_hydralisk": {
      "index": 154,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_8_unit_type_baneling": {
      "index": 155,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "own_health": {
      "index": 156,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.045988,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.239851,
      "nonzero_rate": 0.05188
    },
    "own_normalized_x": {
      "index": 157,
      "min": 0.0,
      "max": 0.674194,
      "mean": 0.019321,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.072266,
      "nonzero_rate": 0.05188
    },
    "own_normalized_y": {
      "index": 158,
      "min": 0.0,
      "max": 0.927734,
      "mean": 0.024567,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.089157,
      "nonzero_rate": 0.05188
    },
    "own_unit_type_zergling": {
      "index": 159,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021558,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.021558
    },
    "own_unit_type_hydralisk": {
      "index": 160,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.026611,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.026611
    },
    "own_unit_type_baneling": {
      "index": 161,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.003711,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.003711
    },
    "previous_action_0": {
      "index": 162,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.043335,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043335
    },
    "previous_action_1": {
      "index": 163,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.008618,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.008618
    },
    "previous_action_2": {
      "index": 164,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.008887,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.008887
    },
    "previous_action_3": {
      "index": 165,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.008154,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.008154
    },
    "previous_action_4": {
      "index": 166,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.008569,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.008569
    },
    "previous_action_5": {
      "index": 167,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.007617,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.007617
    },
    "previous_action_6": {
      "index": 168,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.000903,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.000903
    },
    "previous_action_7": {
      "index": 169,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00083,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00083
    },
    "previous_action_8": {
      "index": 170,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.000708,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.000708
    },
    "previous_action_9": {
      "index": 171,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001074,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001074
    },
    "previous_action_10": {
      "index": 172,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00083,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00083
    },
    "previous_action_11": {
      "index": 173,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.000757,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.000757
    },
    "previous_action_12": {
      "index": 174,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001001,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001001
    },
    "previous_action_13": {
      "index": 175,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.000952,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.000952
    },
    "previous_action_14": {
      "index": 176,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00127,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00127
    },
    "previous_action_15": {
      "index": 177,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001709,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001709
    },
    "agent_id_0": {
      "index": 178,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_1": {
      "index": 179,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_2": {
      "index": 180,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_3": {
      "index": 181,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_4": {
      "index": 182,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_5": {
      "index": 183,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_6": {
      "index": 184,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_7": {
      "index": 185,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_8": {
      "index": 186,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.1,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.1
    },
    "agent_id_9": {
      "index": 187,
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
from typing import List, Tuple

def _compute_rules(o: torch.Tensor) -> Tuple[List[torch.Tensor], List[torch.Tensor]]:
    """
    Helper that computes for each rule:
      - a boolean trigger tensor of shape [batch, n_agents]
      - a 1-D float mask of length obs_dim indicating which features to send
    Both lists are ordered: R1, R2, ..., R20.
    """
    batch, n_agents, obs_dim = o.shape
    triggers: List[torch.Tensor] = []
    masks: List[torch.Tensor] = []

    # Helper to create a feature mask, skipping indices >= obs_dim
    def _make_mask(indices):
        m = torch.zeros(obs_dim, device=o.device)
        for i in indices:
            if i < obs_dim:
                m[i] = 1.0
        return m

    # --- R1: own_health > 0.0 ---------------------------------------------------
    idx_cond = 156
    trig = (o[..., idx_cond] > 0.0) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([156, 157, 158, 159, 160, 161, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187]))

    # --- R2: enemy_0_available > 0.5 -------------------------------------------
    idx_cond = 4
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 4, 5, 6, 7, 8, 9, 10, 11]))

    # --- R3: enemy_1_available > 0.5 -------------------------------------------
    idx_cond = 12
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 12, 13, 14, 15, 16, 17, 18, 19]))

    # --- R4: enemy_2_available > 0.5 -------------------------------------------
    idx_cond = 20
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 20, 21, 22, 23, 24, 25, 26, 27]))

    # --- R5: enemy_3_available > 0.5 -------------------------------------------
    idx_cond = 28
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 28, 29, 30, 31, 32, 33, 34, 35]))

    # --- R6: enemy_4_available > 0.5 -------------------------------------------
    idx_cond = 36
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 36, 37, 38, 39, 40, 41, 42, 43]))

    # --- R7: enemy_5_available > 0.5 -------------------------------------------
    idx_cond = 44
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 44, 45, 46, 47, 48, 49, 50, 51]))

    # --- R8: enemy_6_available > 0.5 -------------------------------------------
    idx_cond = 52
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 52, 53, 54, 55, 56, 57, 58, 59]))

    # --- R9: enemy_7_available > 0.5 -------------------------------------------
    idx_cond = 60
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 60, 61, 62, 63, 64, 65, 66, 67]))

    # --- R10: enemy_8_available > 0.5 ------------------------------------------
    idx_cond = 68
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 68, 69, 70, 71, 72, 73, 74, 75]))

    # --- R11: enemy_9_available > 0.5 ------------------------------------------
    idx_cond = 76
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 76, 77, 78, 79, 80, 81, 82, 83]))

    # --- R12: ally_slot_0_visible > 0.5 ----------------------------------------
    idx_cond = 84
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 84, 85, 86, 87, 88, 89, 90, 91]))

    # --- R13: ally_slot_1_visible > 0.5 ----------------------------------------
    idx_cond = 92
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 92, 93, 94, 95, 96, 97, 98, 99]))

    # --- R14: ally_slot_2_visible > 0.5 ----------------------------------------
    idx_cond = 100
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 100, 101, 102, 103, 104, 105, 106, 107]))

    # --- R15: ally_slot_3_visible > 0.5 ----------------------------------------
    idx_cond = 108
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 108, 109, 110, 111, 112, 113, 114, 115]))

    # --- R16: ally_slot_4_visible > 0.5 ----------------------------------------
    idx_cond = 116
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 116, 117, 118, 119, 120, 121, 122, 123]))

    # --- R17: ally_slot_5_visible > 0.5 ----------------------------------------
    idx_cond = 124
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 124, 125, 126, 127, 128, 129, 130, 131]))

    # --- R18: ally_slot_6_visible > 0.5 ----------------------------------------
    idx_cond = 132
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 132, 133, 134, 135, 136, 137, 138, 139]))

    # --- R19: ally_slot_7_visible > 0.5 ----------------------------------------
    idx_cond = 140
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 140, 141, 142, 143, 144, 145, 146, 147]))

    # --- R20: ally_slot_8_visible > 0.5 ----------------------------------------
    idx_cond = 148
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 148, 149, 150, 151, 152, 153, 154, 155]))

    return triggers, masks


def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    All-to-all communication (every sender can reach every receiver) except self.
    Returns tensor of shape [batch, n_agents, n_agents] with off-diagonal 1s.
    """
    batch, n_agents, _ = o.shape
    who = torch.ones(batch, n_agents, n_agents, device=o.device)
    # Zero out self-communication diagonal
    diag = torch.arange(n_agents, device=o.device)
    who[:, diag, diag] = 0.0
    return who


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns [batch, n_agents, n_agents] with 1 when any rule triggers for the sender.
    Self-communication is explicitly set to 0 on the diagonal.
    """
    batch, n_agents, _ = o.shape
    triggers, _ = _compute_rules(o)  # list of [batch, n_agents] bool tensors

    # Stack to [num_rules, batch, n_agents] and take OR across rules
    all_trig = torch.stack(triggers, dim=0)  # shape [20, batch, n_agents]
    sender_trigger = all_trig.any(dim=0)      # [batch, n_agents] bool

    # A triggered sender sends to all receivers: broadcast across receiver dim
    when = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1).float()

    # Ensure zero self-communication diagonal
    diag_idx = torch.arange(n_agents, device=o.device)
    when[:, diag_idx, diag_idx] = 0.0

    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns an obs-aligned content mask of shape [batch, n_agents, obs_dim].
    For each sender, the mask is the union of feature indices from all triggered rules.
    """
    triggers, masks = _compute_rules(o)  # list of length 20

    # Stack triggers: [num_rules, batch, n_agents]       float
    triggers_stack = torch.stack(triggers, dim=0).float()   # shape [20, B, N]
    # Stack masks:    [num_rules, obs_dim]                float
    masks_stack = torch.stack(masks, dim=0)                # shape [20, obs_dim]

    # For each rule, a sender contributes its mask where triggered:
    #   contribution = triggers_stack[:,:,:,None] * masks_stack[:,None,None,:]
    #   shape: [20, B, N, obs_dim]
    contribution = (triggers_stack.unsqueeze(-1) * masks_stack.unsqueeze(1).unsqueeze(1))
    # Union: any rule triggers that feature -> max across rules, clip to [0,1]
    what = contribution.sum(dim=0).clamp(max=1.0)
    return what
```

Return a complete corrected Python file. Preserve message_design_instruction, communication,
communication_who, communication_when, and communication_what.
