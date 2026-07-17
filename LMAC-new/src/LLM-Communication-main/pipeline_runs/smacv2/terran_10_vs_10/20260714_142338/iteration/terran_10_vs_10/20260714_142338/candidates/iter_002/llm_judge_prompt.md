## system

You are an expert MARL communication-policy judge. Evaluate the generated policy only from the task spec, code, and interface validation. Return one JSON object only.

## user

Evaluate this pure LLM-generated LMAC communication strategy for task `terran_10_vs_10`
in environment `smacv2`.

Research goal:
- We are testing the capability boundary of LLM-designed communication.
- Do NOT use DRC, decision_sufficient, causally_useful, downstream RL win-rate, or hidden/global state.
- Judge whether the policy gives a plausible pure communication strategy for who, when, and what.

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
    "marine",
    "marauder",
    "medivac"
  ],
  "agent_id_role_warning": "Agent ID does not identify a fixed unit type across episodes."
}

Rollout-backed LMAC observation alignment:
{
  "map_name": "terran_10_vs_10",
  "rollout_root": "/data/hp/LLM_Communication/LMAC-new/data/smacv2",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0000.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0001.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0002.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0003.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0004.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0005.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0006.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0007.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0008.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0009.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0010.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0011.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0012.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0013.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0014.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0015.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0016.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0017.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0018.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0019.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0020.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0021.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0022.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0023.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0024.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0025.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0026.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0027.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0028.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0029.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0030.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0031.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0032.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0033.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0034.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0035.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0036.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0037.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0038.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0039.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0040.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0041.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0042.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0043.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0044.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0045.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0046.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0047.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0048.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0049.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0050.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0051.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0052.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0053.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0054.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0055.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0056.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0057.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0058.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0059.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0060.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0061.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0062.pkl"
  ],
  "available": true,
  "n_agents": 10,
  "raw_obs_dim": 162,
  "rollout_obs_dim": 188,
  "documented_obs_dim": 162,
  "extra_obs_dim": 0,
  "episodes": 63,
  "transitions": 3053,
  "seq_lengths": [
    39,
    62,
    43,
    50,
    58,
    52,
    34,
    47,
    41,
    50,
    36,
    63,
    55,
    65,
    40,
    52,
    44,
    43,
    86,
    36,
    69,
    44,
    62,
    57,
    43,
    38,
    41,
    64,
    46,
    37,
    38,
    37,
    42,
    49,
    48,
    73,
    45,
    67,
    41,
    51,
    40,
    49,
    55,
    38,
    46,
    39,
    50,
    41,
    56,
    67,
    37,
    45,
    55,
    48,
    37,
    34,
    49,
    26,
    42,
    84,
    43,
    34,
    50
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
    "enemy_0_unit_type_marine": [
      9,
      10
    ],
    "enemy_0_unit_type_marauder": [
      10,
      11
    ],
    "enemy_0_unit_type_medivac": [
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
    "enemy_1_unit_type_marine": [
      17,
      18
    ],
    "enemy_1_unit_type_marauder": [
      18,
      19
    ],
    "enemy_1_unit_type_medivac": [
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
    "enemy_2_unit_type_marine": [
      25,
      26
    ],
    "enemy_2_unit_type_marauder": [
      26,
      27
    ],
    "enemy_2_unit_type_medivac": [
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
    "enemy_3_unit_type_marine": [
      33,
      34
    ],
    "enemy_3_unit_type_marauder": [
      34,
      35
    ],
    "enemy_3_unit_type_medivac": [
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
    "enemy_4_unit_type_marine": [
      41,
      42
    ],
    "enemy_4_unit_type_marauder": [
      42,
      43
    ],
    "enemy_4_unit_type_medivac": [
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
    "enemy_5_unit_type_marine": [
      49,
      50
    ],
    "enemy_5_unit_type_marauder": [
      50,
      51
    ],
    "enemy_5_unit_type_medivac": [
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
    "enemy_6_unit_type_marine": [
      57,
      58
    ],
    "enemy_6_unit_type_marauder": [
      58,
      59
    ],
    "enemy_6_unit_type_medivac": [
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
    "enemy_7_unit_type_marine": [
      65,
      66
    ],
    "enemy_7_unit_type_marauder": [
      66,
      67
    ],
    "enemy_7_unit_type_medivac": [
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
    "enemy_8_unit_type_marine": [
      73,
      74
    ],
    "enemy_8_unit_type_marauder": [
      74,
      75
    ],
    "enemy_8_unit_type_medivac": [
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
    "enemy_9_unit_type_marine": [
      81,
      82
    ],
    "enemy_9_unit_type_marauder": [
      82,
      83
    ],
    "enemy_9_unit_type_medivac": [
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
    "ally_slot_0_unit_type_marine": [
      89,
      90
    ],
    "ally_slot_0_unit_type_marauder": [
      90,
      91
    ],
    "ally_slot_0_unit_type_medivac": [
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
    "ally_slot_1_unit_type_marine": [
      97,
      98
    ],
    "ally_slot_1_unit_type_marauder": [
      98,
      99
    ],
    "ally_slot_1_unit_type_medivac": [
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
    "ally_slot_2_unit_type_marine": [
      105,
      106
    ],
    "ally_slot_2_unit_type_marauder": [
      106,
      107
    ],
    "ally_slot_2_unit_type_medivac": [
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
    "ally_slot_3_unit_type_marine": [
      113,
      114
    ],
    "ally_slot_3_unit_type_marauder": [
      114,
      115
    ],
    "ally_slot_3_unit_type_medivac": [
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
    "ally_slot_4_unit_type_marine": [
      121,
      122
    ],
    "ally_slot_4_unit_type_marauder": [
      122,
      123
    ],
    "ally_slot_4_unit_type_medivac": [
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
    "ally_slot_5_unit_type_marine": [
      129,
      130
    ],
    "ally_slot_5_unit_type_marauder": [
      130,
      131
    ],
    "ally_slot_5_unit_type_medivac": [
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
    "ally_slot_6_unit_type_marine": [
      137,
      138
    ],
    "ally_slot_6_unit_type_marauder": [
      138,
      139
    ],
    "ally_slot_6_unit_type_medivac": [
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
    "ally_slot_7_unit_type_marine": [
      145,
      146
    ],
    "ally_slot_7_unit_type_marauder": [
      146,
      147
    ],
    "ally_slot_7_unit_type_medivac": [
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
    "ally_slot_8_unit_type_marine": [
      153,
      154
    ],
    "ally_slot_8_unit_type_marauder": [
      154,
      155
    ],
    "ally_slot_8_unit_type_medivac": [
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
    "own_unit_type_marine": [
      159,
      160
    ],
    "own_unit_type_marauder": [
      160,
      161
    ],
    "own_unit_type_medivac": [
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
      "mean": 0.072974,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.072974
    },
    "move_south": {
      "index": 1,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.074048,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.074048
    },
    "move_east": {
      "index": 2,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.075098,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.075098
    },
    "move_west": {
      "index": 3,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.069409,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.069409
    },
    "enemy_0_available": {
      "index": 4,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013623,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013623
    },
    "enemy_0_distance": {
      "index": 5,
      "min": 0.0,
      "max": 0.997999,
      "mean": 0.02075,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.031641
    },
    "enemy_0_relative_x": {
      "index": 6,
      "min": -0.955268,
      "max": 0.99547,
      "mean": 0.008363,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.031641
    },
    "enemy_0_relative_y": {
      "index": 7,
      "min": -0.979004,
      "max": 0.972466,
      "mean": 0.00767,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.031543
    },
    "enemy_0_health": {
      "index": 8,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.02736,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.031641
    },
    "enemy_0_unit_type_marine": {
      "index": 9,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013574,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013574
    },
    "enemy_0_unit_type_marauder": {
      "index": 10,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.011133,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.011133
    },
    "enemy_0_unit_type_medivac": {
      "index": 11,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.006934,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.006934
    },
    "enemy_1_available": {
      "index": 12,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013843,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013843
    },
    "enemy_1_distance": {
      "index": 13,
      "min": 0.0,
      "max": 0.998718,
      "mean": 0.019918,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029932
    },
    "enemy_1_relative_x": {
      "index": 14,
      "min": -0.782796,
      "max": 0.988715,
      "mean": 0.009311,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029932
    },
    "enemy_1_relative_y": {
      "index": 15,
      "min": -0.964328,
      "max": 0.986762,
      "mean": 0.006264,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029785
    },
    "enemy_1_health": {
      "index": 16,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025393,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029932
    },
    "enemy_1_unit_type_marine": {
      "index": 17,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.01377,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.01377
    },
    "enemy_1_unit_type_marauder": {
      "index": 18,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.012012,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.012012
    },
    "enemy_1_unit_type_medivac": {
      "index": 19,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00415,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00415
    },
    "enemy_2_available": {
      "index": 20,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.012622,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.012622
    },
    "enemy_2_distance": {
      "index": 21,
      "min": 0.0,
      "max": 0.99807,
      "mean": 0.018564,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028223
    },
    "enemy_2_relative_x": {
      "index": 22,
      "min": -0.904704,
      "max": 0.983371,
      "mean": 0.006715,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028223
    },
    "enemy_2_relative_y": {
      "index": 23,
      "min": -0.96129,
      "max": 0.984728,
      "mean": 0.005781,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028223
    },
    "enemy_2_health": {
      "index": 24,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025474,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.028223
    },
    "enemy_2_unit_type_marine": {
      "index": 25,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013232,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013232
    },
    "enemy_2_unit_type_marauder": {
      "index": 26,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.005933,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.005933
    },
    "enemy_2_unit_type_medivac": {
      "index": 27,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.009058,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.009058
    },
    "enemy_3_available": {
      "index": 28,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.009741,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.009741
    },
    "enemy_3_distance": {
      "index": 29,
      "min": 0.0,
      "max": 0.999979,
      "mean": 0.017397,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025293
    },
    "enemy_3_relative_x": {
      "index": 30,
      "min": -0.951145,
      "max": 0.991347,
      "mean": -0.00141,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025293
    },
    "enemy_3_relative_y": {
      "index": 31,
      "min": -0.95147,
      "max": 0.959663,
      "mean": -0.000777,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025073
    },
    "enemy_3_health": {
      "index": 32,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.021447,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025293
    },
    "enemy_3_unit_type_marine": {
      "index": 33,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.012988,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.012988
    },
    "enemy_3_unit_type_marauder": {
      "index": 34,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.012305,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.012305
    },
    "enemy_3_unit_type_medivac": {
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
      "mean": 0.00979,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00979
    },
    "enemy_4_distance": {
      "index": 37,
      "min": 0.0,
      "max": 0.998464,
      "mean": 0.018794,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027295
    },
    "enemy_4_relative_x": {
      "index": 38,
      "min": -0.970269,
      "max": 0.983724,
      "mean": -0.002081,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027295
    },
    "enemy_4_relative_y": {
      "index": 39,
      "min": -0.948866,
      "max": 0.978,
      "mean": -0.004528,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027295
    },
    "enemy_4_health": {
      "index": 40,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025901,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027295
    },
    "enemy_4_unit_type_marine": {
      "index": 41,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.010181,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.010181
    },
    "enemy_4_unit_type_marauder": {
      "index": 42,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.017114,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.017114
    },
    "enemy_4_unit_type_medivac": {
      "index": 43,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "enemy_5_available": {
      "index": 44,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.006689,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.006689
    },
    "enemy_5_distance": {
      "index": 45,
      "min": 0.0,
      "max": 0.999922,
      "mean": 0.019634,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027051
    },
    "enemy_5_relative_x": {
      "index": 46,
      "min": -0.97092,
      "max": 0.995171,
      "mean": -0.000507,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027051
    },
    "enemy_5_relative_y": {
      "index": 47,
      "min": -0.999892,
      "max": 0.979601,
      "mean": -0.005339,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027051
    },
    "enemy_5_health": {
      "index": 48,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.023489,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027051
    },
    "enemy_5_unit_type_marine": {
      "index": 49,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.010205,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.010205
    },
    "enemy_5_unit_type_marauder": {
      "index": 50,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013403,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013403
    },
    "enemy_5_unit_type_medivac": {
      "index": 51,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.003442,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.003442
    },
    "enemy_6_available": {
      "index": 52,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.007935,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.007935
    },
    "enemy_6_distance": {
      "index": 53,
      "min": 0.0,
      "max": 0.999894,
      "mean": 0.018567,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025732
    },
    "enemy_6_relative_x": {
      "index": 54,
      "min": -0.975179,
      "max": 0.975315,
      "mean": -0.000409,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025732
    },
    "enemy_6_relative_y": {
      "index": 55,
      "min": -0.974284,
      "max": 0.982449,
      "mean": -0.006645,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025635
    },
    "enemy_6_health": {
      "index": 56,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.024052,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025732
    },
    "enemy_6_unit_type_marine": {
      "index": 57,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.016431,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.016431
    },
    "enemy_6_unit_type_marauder": {
      "index": 58,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.009302,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.009302
    },
    "enemy_6_unit_type_medivac": {
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
      "mean": 0.008472,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.008472
    },
    "enemy_7_distance": {
      "index": 61,
      "min": 0.0,
      "max": 0.999873,
      "mean": 0.017461,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025049
    },
    "enemy_7_relative_x": {
      "index": 62,
      "min": -0.994249,
      "max": 0.992811,
      "mean": 0.003149,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025049
    },
    "enemy_7_relative_y": {
      "index": 63,
      "min": -0.989041,
      "max": 0.969672,
      "mean": -0.00258,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.024927
    },
    "enemy_7_health": {
      "index": 64,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.022934,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025049
    },
    "enemy_7_unit_type_marine": {
      "index": 65,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.02041,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.02041
    },
    "enemy_7_unit_type_marauder": {
      "index": 66,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.004639,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.004639
    },
    "enemy_7_unit_type_medivac": {
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
      "mean": 0.010278,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.010278
    },
    "enemy_8_distance": {
      "index": 69,
      "min": 0.0,
      "max": 0.99943,
      "mean": 0.019446,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029736
    },
    "enemy_8_relative_x": {
      "index": 70,
      "min": -0.953423,
      "max": 0.994385,
      "mean": 0.007665,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029736
    },
    "enemy_8_relative_y": {
      "index": 71,
      "min": -0.976237,
      "max": 0.927979,
      "mean": 0.003127,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029736
    },
    "enemy_8_health": {
      "index": 72,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.02566,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.029736
    },
    "enemy_8_unit_type_marine": {
      "index": 73,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.0073,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0073
    },
    "enemy_8_unit_type_marauder": {
      "index": 74,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.01687,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.01687
    },
    "enemy_8_unit_type_medivac": {
      "index": 75,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.005566,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.005566
    },
    "enemy_9_available": {
      "index": 76,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.012549,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.012549
    },
    "enemy_9_distance": {
      "index": 77,
      "min": 0.0,
      "max": 0.999703,
      "mean": 0.022099,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.032959
    },
    "enemy_9_relative_x": {
      "index": 78,
      "min": -0.888129,
      "max": 0.999023,
      "mean": 0.009366,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.032959
    },
    "enemy_9_relative_y": {
      "index": 79,
      "min": -0.963515,
      "max": 0.982829,
      "mean": 0.006059,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.032959
    },
    "enemy_9_health": {
      "index": 80,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.028131,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.032959
    },
    "enemy_9_unit_type_marine": {
      "index": 81,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.0104,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0104
    },
    "enemy_9_unit_type_marauder": {
      "index": 82,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.018848,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.018848
    },
    "enemy_9_unit_type_medivac": {
      "index": 83,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.003711,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.003711
    },
    "ally_slot_0_visible": {
      "index": 84,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.044824,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044824
    },
    "ally_slot_0_distance": {
      "index": 85,
      "min": 0.0,
      "max": 0.998963,
      "mean": 0.020925,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044824
    },
    "ally_slot_0_relative_x": {
      "index": 86,
      "min": -0.960422,
      "max": 0.997043,
      "mean": -0.007751,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.04458
    },
    "ally_slot_0_relative_y": {
      "index": 87,
      "min": -0.98093,
      "max": 0.981879,
      "mean": -0.001541,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044653
    },
    "ally_slot_0_health": {
      "index": 88,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.040606,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044824
    },
    "ally_slot_0_unit_type_marine": {
      "index": 89,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_0_unit_type_marauder": {
      "index": 90,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.044824,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044824
    },
    "ally_slot_0_unit_type_medivac": {
      "index": 91,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_1_visible": {
      "index": 92,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.046338,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046338
    },
    "ally_slot_1_distance": {
      "index": 93,
      "min": 0.0,
      "max": 0.999457,
      "mean": 0.021784,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046313
    },
    "ally_slot_1_relative_x": {
      "index": 94,
      "min": -0.974365,
      "max": 0.941976,
      "mean": -0.00428,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.045703
    },
    "ally_slot_1_relative_y": {
      "index": 95,
      "min": -0.996853,
      "max": 0.98093,
      "mean": -0.002187,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.045874
    },
    "ally_slot_1_health": {
      "index": 96,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.043842,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046338
    },
    "ally_slot_1_unit_type_marine": {
      "index": 97,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001392,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001392
    },
    "ally_slot_1_unit_type_marauder": {
      "index": 98,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.044946,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044946
    },
    "ally_slot_1_unit_type_medivac": {
      "index": 99,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_2_visible": {
      "index": 100,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.047363,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.047363
    },
    "ally_slot_2_distance": {
      "index": 101,
      "min": 0.0,
      "max": 0.999533,
      "mean": 0.022936,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.047339
    },
    "ally_slot_2_relative_x": {
      "index": 102,
      "min": -0.963135,
      "max": 0.996121,
      "mean": 0.001561,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.046484
    },
    "ally_slot_2_relative_y": {
      "index": 103,
      "min": -0.971191,
      "max": 0.957275,
      "mean": -0.000877,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.047217
    },
    "ally_slot_2_health": {
      "index": 104,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.043847,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.047363
    },
    "ally_slot_2_unit_type_marine": {
      "index": 105,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.004907,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.004907
    },
    "ally_slot_2_unit_type_marauder": {
      "index": 106,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.042456,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042456
    },
    "ally_slot_2_unit_type_medivac": {
      "index": 107,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_3_visible": {
      "index": 108,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.040137,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.040137
    },
    "ally_slot_3_distance": {
      "index": 109,
      "min": 0.0,
      "max": 0.999258,
      "mean": 0.019426,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.040112
    },
    "ally_slot_3_relative_x": {
      "index": 110,
      "min": -0.986437,
      "max": 0.955159,
      "mean": 0.000951,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.039917
    },
    "ally_slot_3_relative_y": {
      "index": 111,
      "min": -0.992025,
      "max": 0.998834,
      "mean": 0.001533,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.03999
    },
    "ally_slot_3_health": {
      "index": 112,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.035301,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.040137
    },
    "ally_slot_3_unit_type_marine": {
      "index": 113,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.0125,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0125
    },
    "ally_slot_3_unit_type_marauder": {
      "index": 114,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.027637,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027637
    },
    "ally_slot_3_unit_type_medivac": {
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
      "mean": 0.035693,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.035693
    },
    "ally_slot_4_distance": {
      "index": 117,
      "min": 0.0,
      "max": 0.99544,
      "mean": 0.015208,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.035693
    },
    "ally_slot_4_relative_x": {
      "index": 118,
      "min": -0.923286,
      "max": 0.963135,
      "mean": 0.001019,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.035596
    },
    "ally_slot_4_relative_y": {
      "index": 119,
      "min": -0.938043,
      "max": 0.965413,
      "mean": 0.001723,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.035522
    },
    "ally_slot_4_health": {
      "index": 120,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.030666,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.035693
    },
    "ally_slot_4_unit_type_marine": {
      "index": 121,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.019995,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.019995
    },
    "ally_slot_4_unit_type_marauder": {
      "index": 122,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.015698,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.015698
    },
    "ally_slot_4_unit_type_medivac": {
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
      "mean": 0.036987,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.036987
    },
    "ally_slot_5_distance": {
      "index": 125,
      "min": 0.0,
      "max": 0.998353,
      "mean": 0.016561,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.036987
    },
    "ally_slot_5_relative_x": {
      "index": 126,
      "min": -0.958984,
      "max": 0.958984,
      "mean": 0.001666,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.036646
    },
    "ally_slot_5_relative_y": {
      "index": 127,
      "min": -0.925673,
      "max": 0.992025,
      "mean": 0.000235,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.036816
    },
    "ally_slot_5_health": {
      "index": 128,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.032304,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.036987
    },
    "ally_slot_5_unit_type_marine": {
      "index": 129,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.032349,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.032349
    },
    "ally_slot_5_unit_type_marauder": {
      "index": 130,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.002881,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.002881
    },
    "ally_slot_5_unit_type_medivac": {
      "index": 131,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001758,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001758
    },
    "ally_slot_6_visible": {
      "index": 132,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.044385,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044385
    },
    "ally_slot_6_distance": {
      "index": 133,
      "min": 0.0,
      "max": 0.998741,
      "mean": 0.019622,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044385
    },
    "ally_slot_6_relative_x": {
      "index": 134,
      "min": -0.913656,
      "max": 0.984972,
      "mean": 0.004125,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044019
    },
    "ally_slot_6_relative_y": {
      "index": 135,
      "min": -0.950005,
      "max": 0.996853,
      "mean": 0.001216,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044263
    },
    "ally_slot_6_health": {
      "index": 136,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.03998,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.044385
    },
    "ally_slot_6_unit_type_marine": {
      "index": 137,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.041113,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.041113
    },
    "ally_slot_6_unit_type_marauder": {
      "index": 138,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_6_unit_type_medivac": {
      "index": 139,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.003271,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.003271
    },
    "ally_slot_7_visible": {
      "index": 140,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.038184,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.038184
    },
    "ally_slot_7_distance": {
      "index": 141,
      "min": 0.0,
      "max": 0.999533,
      "mean": 0.017656,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.038135
    },
    "ally_slot_7_relative_x": {
      "index": 142,
      "min": -0.997043,
      "max": 0.960422,
      "mean": 0.000546,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.037427
    },
    "ally_slot_7_relative_y": {
      "index": 143,
      "min": -0.998834,
      "max": 0.960666,
      "mean": -0.000298,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.037866
    },
    "ally_slot_7_health": {
      "index": 144,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.033778,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.038184
    },
    "ally_slot_7_unit_type_marine": {
      "index": 145,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.027588,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.027588
    },
    "ally_slot_7_unit_type_marauder": {
      "index": 146,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_7_unit_type_medivac": {
      "index": 147,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.010596,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.010596
    },
    "ally_slot_8_visible": {
      "index": 148,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.043579,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043579
    },
    "ally_slot_8_distance": {
      "index": 149,
      "min": 0.0,
      "max": 0.996441,
      "mean": 0.019229,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043457
    },
    "ally_slot_8_relative_x": {
      "index": 150,
      "min": -0.996121,
      "max": 0.961344,
      "mean": 0.002164,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.042383
    },
    "ally_slot_8_relative_y": {
      "index": 151,
      "min": -0.955865,
      "max": 0.947781,
      "mean": 0.000195,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043042
    },
    "ally_slot_8_health": {
      "index": 152,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.038915,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.043579
    },
    "ally_slot_8_unit_type_marine": {
      "index": 153,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013306,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013306
    },
    "ally_slot_8_unit_type_marauder": {
      "index": 154,
      "min": 0.0,
      "max": 0.0,
      "mean": 0.0,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.0
    },
    "ally_slot_8_unit_type_medivac": {
      "index": 155,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.030273,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.030273
    },
    "own_health": {
      "index": 156,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.063941,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.96,
      "nonzero_rate": 0.075098
    },
    "own_normalized_x": {
      "index": 157,
      "min": 0.0,
      "max": 0.890686,
      "mean": 0.029362,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.325096,
      "nonzero_rate": 0.075098
    },
    "own_normalized_y": {
      "index": 158,
      "min": 0.0,
      "max": 0.937492,
      "mean": 0.039365,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.464844,
      "nonzero_rate": 0.075098
    },
    "own_unit_type_marine": {
      "index": 159,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.025781,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.025781
    },
    "own_unit_type_marauder": {
      "index": 160,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.03689,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.03689
    },
    "own_unit_type_medivac": {
      "index": 161,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.012427,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.012427
    },
    "previous_action_0": {
      "index": 162,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.052588,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.052588
    },
    "previous_action_1": {
      "index": 163,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013525,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013525
    },
    "previous_action_2": {
      "index": 164,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.012842,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.012842
    },
    "previous_action_3": {
      "index": 165,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013013,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013013
    },
    "previous_action_4": {
      "index": 166,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.013379,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.013379
    },
    "previous_action_5": {
      "index": 167,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.010742,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.010742
    },
    "previous_action_6": {
      "index": 168,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001733,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001733
    },
    "previous_action_7": {
      "index": 169,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001636,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001636
    },
    "previous_action_8": {
      "index": 170,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001367,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001367
    },
    "previous_action_9": {
      "index": 171,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001147,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001147
    },
    "previous_action_10": {
      "index": 172,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001074,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001074
    },
    "previous_action_11": {
      "index": 173,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.000684,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.000684
    },
    "previous_action_12": {
      "index": 174,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.00083,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.00083
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
      "mean": 0.000952,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.000952
    },
    "previous_action_15": {
      "index": 177,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.001221,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 0.0,
      "nonzero_rate": 0.001221
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

Interface validation:
{
  "valid": true,
  "map_name": "terran_10_vs_10",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_002/comm_init.py",
  "validation_obs_source": "rollout",
  "validation_obs_dim": 188,
  "documented_obs_dim": 162,
  "message_dim": 188,
  "matrix_edge_rate": 0.0,
  "who_edge_rate": 0.0,
  "when_edge_rate": 0.0,
  "what_dim": 188,
  "matrix_min": 0.0,
  "matrix_max": 0.0
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "terran_10_vs_10",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_002/comm_init.py",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0000.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0001.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0002.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0003.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0004.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0005.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0006.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0007.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0008.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0009.pkl",
    "/data/hp/LLM_Communication/LMAC-new/data/smacv2/terran_10_vs_10/train_traj_0010.pkl"
  ],
  "transitions": 4096,
  "n_agents": 10,
  "rollout_obs_dim": 188,
  "message_dim": 188,
  "matrix_edge_rate": 0.008732096354166666,
  "who_edge_rate": 0.008732096354166666,
  "when_edge_rate": 0.008732096354166666,
  "message_nonzero_rate": 0.0005316551695478723,
  "message_abs_mean": 0.0005316551695478723,
  "active_sender_what_coverage_mean": 0.007228092508943263,
  "active_sender_what_coverage_min": 0.0,
  "active_sender_count": 1931,
  "matrix_min": 0.0,
  "matrix_max": 1.0,
  "risk_flags": [],
  "evidence_cases": [
    {
      "case_id": "train_traj_0000:0",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:36",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [
          69,
          70,
          71,
          72,
          156,
          157,
          158,
          159
        ]
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.042553
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {
          "69": 0.202357,
          "70": 0.023546,
          "71": 0.200982,
          "72": 0.88,
          "156": 0.333333,
          "157": 0.61573,
          "158": 0.590927,
          "159": 1.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:72",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:108",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:145",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:181",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:217",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:253",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:290",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:326",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:362",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    },
    {
      "case_id": "train_traj_0000:399",
      "active_edges_receiver_sender": [],
      "selected_what_indices_by_sender": [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
      ],
      "what_coverage_by_sender": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "selected_values_by_sender": [
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    }
  ]
}

Recent trials:
[
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "terran_10_vs_10",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-14T14:47:47+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_001/comm_init.py",
      "documented_obs_dim": 162,
      "map_name": "terran_10_vs_10",
      "matrix_edge_rate": 0.0,
      "matrix_max": 0.0,
      "matrix_min": 0.0,
      "message_dim": 188,
      "valid": true,
      "validation_obs_dim": 188,
      "validation_obs_source": "rollout",
      "what_dim": 188,
      "when_edge_rate": 0.0,
      "who_edge_rate": 0.0
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "terran_10_vs_10",
    "matrix_edge_rate": 0.07509765625,
    "message_dim": 188,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-14T14:47:47+00:00",
    "valid": true,
    "when_edge_rate": 0.07509765625,
    "who_edge_rate": 0.07509765625
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_001/comm_init.py",
    "failure_analysis": "The communication policy's what logic includes all ally/enemy visible features for every agent, resulting in a what mask that can contain up to 79 indices. The subsequent message packing with M=10 selects features by a fixed priority: own state first, then previous actions, then enemy distance, then ally distance. Since previous actions have high priority and are always in the mask, they occupy most of the budget, leaving no room for enemy/ally data except occasionally the closest enemy feature. Consequently, the rich ally/enemy information is almost never transmitted, defeating the purpose of sharing battlefield awareness. Additionally, the full‑connectivity who/when matrices and the unconditional sending of previous actions may be unnecessary and increase communication overhead, but the primary failure is the mismatch between the what mask and the packing budget.",
    "iteration": 1,
    "map_name": "terran_10_vs_10",
    "matrix_edge_rate": 0.0,
    "message_dim": 188,
    "next_hypothesis": "1. Prune the what mask to include only a small set of critical ally/enemy features (e.g., only the closest enemy, or only injured allies) so that the M=10 budget is used effectively. 2. Alternatively, remove the previous actions from the message when other data is more important, or limit action history to a shorter window. 3. Reduce the who/when connectivity: e.g., medivac only sends to injured DPS, DPS only to medivac and nearby allies, to cut unnecessary traffic.",
    "rollout_grounding_score": 0.4,
    "score": 0.3,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-14T14:49:43+00:00",
    "valid": true,
    "what_score": 0.2,
    "when_score": 0.5,
    "who_score": 0.6
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_002/comm_init.py",
    "failure_analysis": "",
    "iteration": 2,
    "map_name": "terran_10_vs_10",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-14T14:54:32+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_002/comm_init.py",
      "documented_obs_dim": 162,
      "map_name": "terran_10_vs_10",
      "matrix_edge_rate": 0.0,
      "matrix_max": 0.0,
      "matrix_min": 0.0,
      "message_dim": 188,
      "valid": true,
      "validation_obs_dim": 188,
      "validation_obs_source": "rollout",
      "what_dim": 188,
      "when_edge_rate": 0.0,
      "who_edge_rate": 0.0
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_002/comm_init.py",
    "failure_analysis": "",
    "iteration": 2,
    "map_name": "terran_10_vs_10",
    "matrix_edge_rate": 0.008732096354166666,
    "message_dim": 188,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-14T14:54:32+00:00",
    "valid": true,
    "when_edge_rate": 0.008732096354166666,
    "who_edge_rate": 0.008732096354166666
  }
]

Candidate code:
```python
import torch

def message_design_instruction() -> str:
    """
    Return a string describing the communication protocol design.
    This function is required by the LMAC teacher policy validation.
    """
    return (
        "Teacher communication for Terran 10vs10 with three unit types.\n"
        "Groups: G1 (medivac), G2 (marine/marauder).\n"
        "Who/When: Medivac communicates to all active agents. Injured DPS (health < 0.5) communicates only to medivac. No self-loops.\n"
        "What:\n"
        "  - G1 sends own health, position (normalized x,y), and unit type (medivac).\n"
        "  - G2 (injured) sends own health, position, unit type (marine/marauder), plus distance, direction x, direction y, and health of the closest visible enemy.\n"
        "  - Previous actions and ally features are not transmitted to make room for critical spatial data."
    )


def communication(o: torch.Tensor):
    """
    Return a tuple (message, who, when, what) that defines the teacher
    communication for training. The message is a packed vector of selected features
    with a fixed maximum size M.
    Priority: own features first, then enemy features (distance, rel_x, rel_y, health).
    """
    who = communication_who(o)
    when = communication_when(o)
    what = communication_what(o)

    B, A, D = o.shape
    M = 10  # fixed message budget
    device = o.device
    dtype = o.dtype

    # Priority base for feature ordering
    PRIORITY_BASE = torch.full((D,), 1000.0, device=device, dtype=dtype)
    DIST_LOOKUP = -torch.ones(D, dtype=torch.long, device=device)

    # Own features (156-161)   RULE R1, R2
    PRIORITY_BASE[156] = 0.0   # health
    PRIORITY_BASE[157] = 1.0   # normalized_x
    PRIORITY_BASE[158] = 2.0   # normalized_y
    PRIORITY_BASE[159] = 3.0   # marine type
    PRIORITY_BASE[160] = 4.0   # marauder type
    PRIORITY_BASE[161] = 5.0   # medivac type

    # Closest enemy features (indices 5+8*i to 8+8*i)   RULE R2
    for i in range(10):
        base = 4 + 8 * i
        dist_idx = base + 1
        PRIORITY_BASE[base+1] = 20.0   # distance
        PRIORITY_BASE[base+2] = 21.0   # rel_x
        PRIORITY_BASE[base+3] = 22.0   # rel_y
        PRIORITY_BASE[base+4] = 23.0   # health
        for k in range(1, 5):
            DIST_LOOKUP[base + k] = dist_idx

    msg = torch.zeros(B, A, M, device=device, dtype=dtype)

    for b in range(B):
        for a in range(A):
            mask_t = what[b, a].bool()
            if not mask_t.any():
                continue
            idx = mask_t.nonzero(as_tuple=False).squeeze(-1)
            if idx.numel() == 0:
                continue

            base_prio = PRIORITY_BASE[idx]
            dist_idx = DIST_LOOKUP[idx]
            dist_vals = torch.where(
                dist_idx >= 0,
                o[b, a, dist_idx],
                torch.tensor(0.0, device=device, dtype=dtype)
            )
            priority = base_prio + dist_vals
            _, order = torch.sort(priority)
            taken = idx[order][:M]
            msg[b, a, :len(taken)] = o[b, a, taken]

    return msg, who, when, what


def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    RULE who: Medivac to all active agents; Injured DPS only to medivac. No self-loops.
    """
    B, A, _ = o.shape
    device = o.device

    g1 = o[:, :, 161] > 0.5                         # medivac
    g2 = (o[:, :, 159] > 0.5) | (o[:, :, 160] > 0.5)   # marine or marauder
    is_active = g1 | g2
    g2_injured = g2 & (o[:, :, 156] < 0.5)

    identity = torch.eye(A, dtype=torch.bool, device=device).unsqueeze(0)   # (1, A, A)

    # Who mask: (G1 sender to all active receivers) OR (G2 injured sender to G1 receivers), no self
    who_mask = (
        (g1.unsqueeze(2) & is_active.unsqueeze(1)) |
        (g2_injured.unsqueeze(2) & g1.unsqueeze(1))
    ) & ~identity

    return who_mask.float()


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    RULE when: same as who, communication only when there is an intended receiver.
    """
    return communication_who(o).clone()


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    RULE R1 (Medivac): own health, position, unit type.
    RULE R2 (Injured DPS): own health, position, unit type, plus closest visible enemy
    distance, direction, health.
    Previous actions and ally data are excluded to fit the message budget.
    """
    B, A, D = o.shape
    device = o.device
    dtype = o.dtype

    g1 = o[:, :, 161] > 0.5                          # medivac
    g2 = (o[:, :, 159] > 0.5) | (o[:, :, 160] > 0.5)   # DPS
    g2_injured = g2 & (o[:, :, 156] < 0.5)           # injured DPS

    is_marine = o[:, :, 159] > 0.5
    is_marauder = o[:, :, 160] > 0.5

    mask = torch.zeros(B, A, D, dtype=dtype, device=device)

    # Own features for G1 and G2_injured
    own_active = g1 | g2_injured
    mask[:, :, 156] = own_active.to(dtype)          # health
    mask[:, :, 157] = own_active.to(dtype)          # norm_x
    mask[:, :, 158] = own_active.to(dtype)          # norm_y
    mask[:, :, 159] = (g2_injured & is_marine).to(dtype)     # marine type
    mask[:, :, 160] = (g2_injured & is_marauder).to(dtype)   # marauder type
    mask[:, :, 161] = g1.to(dtype)                           # medivac type

    # Closest visible enemy for G2_injured
    enemy_avail = o[:, :, 4::8] > 0.5               # [B, A, 10]
    enemy_dist = o[:, :, 5::8]                      # [B, A, 10]
    enemy_dist_masked = enemy_dist.masked_fill(~enemy_avail, float('inf'))
    closest_idx = enemy_dist_masked.argmin(dim=-1)   # [B, A]
    has_visible_enemy = enemy_avail.any(dim=-1)      # [B, A]
    g2_cond = g2_injured & has_visible_enemy         # only include enemy data if a visible enemy exists

    i = closest_idx
    idx_dist = 5 + 8 * i
    idx_relx = 6 + 8 * i
    idx_rely = 7 + 8 * i
    idx_health = 8 + 8 * i
    all_indices = torch.stack([idx_dist, idx_relx, idx_rely, idx_health], dim=-1)  # (B, A, 4)

    values = g2_cond.unsqueeze(-1).expand(-1, -1, 4).to(dtype)
    mask_flat = mask.reshape(B * A, D)
    mask_flat.scatter_(1, all_indices.reshape(B * A, 4), values.reshape(B * A, 4))

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
