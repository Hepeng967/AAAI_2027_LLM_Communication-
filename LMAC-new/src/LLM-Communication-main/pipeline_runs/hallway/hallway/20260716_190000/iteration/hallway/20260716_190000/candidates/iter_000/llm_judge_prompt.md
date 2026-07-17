## system

You are an expert MARL communication-policy judge. Evaluate the generated policy only from the task spec, code, and interface validation. Return one JSON object only.

## user

Evaluate this pure LLM-generated LMAC communication strategy for task `hallway`
in environment `hallway`.

Research goal:
- We are testing the capability boundary of LLM-designed communication.
- Do NOT use DRC, decision_sufficient, causally_useful, downstream RL win-rate, or hidden/global state.
- Judge whether the policy gives a plausible pure communication strategy for who, when, and what.

Map spec:
{
  "environment": "hallway",
  "n_agents": 4,
  "n_actions": 3,
  "obs_dim": 8,
  "documented_raw_obs_dim": 1,
  "time_seq": 10,
  "state_numbers": [
    4,
    6,
    8,
    10
  ],
  "objective": "All four agents must reach position 0 on the same timestep.",
  "failure_condition": "The episode fails if only a subset reaches position 0.",
  "actions": {
    "0": "stay",
    "1": "toward_zero",
    "2": "away_from_zero"
  },
  "raw_features": {
    "current_position": [
      0,
      1
    ]
  }
}

Rollout-backed LMAC observation alignment:
{
  "map_name": "hallway",
  "rollout_root": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway",
  "files": [
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0000.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0001.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0002.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0003.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0004.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0005.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0006.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0007.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0008.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0009.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0010.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0011.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0012.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0013.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0014.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0015.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0016.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0017.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0018.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0019.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0020.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0021.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0022.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0023.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0024.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0025.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0026.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0027.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0028.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0029.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0030.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0031.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0032.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0033.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0034.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0035.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0036.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0037.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0038.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0039.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0040.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0041.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0042.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0043.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0044.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0045.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0046.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0047.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0048.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0049.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0050.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0051.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0052.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0053.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0054.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0055.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0056.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0057.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0058.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0059.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0060.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0061.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0062.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0063.pkl"
  ],
  "available": true,
  "n_agents": 4,
  "raw_obs_dim": 1,
  "rollout_obs_dim": 8,
  "documented_obs_dim": 1,
  "extra_obs_dim": 0,
  "episodes": 64,
  "transitions": 469,
  "seq_lengths": [
    20,
    20,
    15,
    8,
    1,
    7,
    1,
    1,
    16,
    20,
    8,
    3,
    1,
    5,
    16,
    6,
    20,
    5,
    1,
    9,
    2,
    11,
    1,
    1,
    5,
    11,
    3,
    1,
    6,
    1,
    20,
    1,
    5,
    2,
    6,
    17,
    3,
    13,
    1,
    1,
    5,
    8,
    1,
    15,
    3,
    9,
    1,
    2,
    3,
    20,
    20,
    10,
    2,
    2,
    15,
    1,
    2,
    7,
    20,
    20,
    3,
    3,
    2,
    1
  ],
  "action_dim": 3,
  "agent_types": [
    "hallway_agent",
    "hallway_agent",
    "hallway_agent",
    "hallway_agent"
  ],
  "feature_index": {
    "current_position": [
      0,
      1
    ],
    "previous_action_0": [
      1,
      2
    ],
    "previous_action_1": [
      2,
      3
    ],
    "previous_action_2": [
      3,
      4
    ],
    "agent_id_0": [
      4,
      5
    ],
    "agent_id_1": [
      5,
      6
    ],
    "agent_id_2": [
      6,
      7
    ],
    "agent_id_3": [
      7,
      8
    ]
  },
  "feature_statistics": {
    "current_position": {
      "index": 0,
      "min": 0.0,
      "max": 10.0,
      "mean": 1.808008,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 8.0,
      "nonzero_rate": 0.398242
    },
    "previous_action_0": {
      "index": 1,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.130078,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.130078
    },
    "previous_action_1": {
      "index": 2,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.134961,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.134961
    },
    "previous_action_2": {
      "index": 3,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.137305,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.137305
    },
    "agent_id_0": {
      "index": 4,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.25,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.25
    },
    "agent_id_1": {
      "index": 5,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.25,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.25
    },
    "agent_id_2": {
      "index": 6,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.25,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.25
    },
    "agent_id_3": {
      "index": 7,
      "min": 0.0,
      "max": 1.0,
      "mean": 0.25,
      "p05": 0.0,
      "p50": 0.0,
      "p95": 1.0,
      "nonzero_rate": 0.25
    }
  },
  "alignment_note": "rollout_obs_dim is exactly the RL communication input: raw observation + previous-action one-hot + agent-id one-hot. Feature positions are identical in offline evaluation and RL training."
}

Interface validation:
{
  "valid": true,
  "map_name": "hallway",
  "comm_code": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/hallway/hallway/20260716_190000/iteration/hallway/20260716_190000/candidates/iter_000/comm_init.py",
  "validation_obs_source": "rollout",
  "validation_obs_dim": 8,
  "documented_obs_dim": 1,
  "message_dim": 8,
  "matrix_edge_rate": 1.0,
  "who_edge_rate": 1.0,
  "when_edge_rate": 1.0,
  "what_dim": 8,
  "matrix_min": 0.0,
  "matrix_max": 1.0
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "hallway",
  "comm_code": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/hallway/hallway/20260716_190000/iteration/hallway/20260716_190000/candidates/iter_000/comm_init.py",
  "files": [
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0000.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0001.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0002.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0003.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0004.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0005.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0006.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0007.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0008.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0009.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0010.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0011.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0012.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0013.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0014.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0015.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0016.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0017.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0018.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0019.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0020.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0021.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0022.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0023.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0024.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0025.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0026.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0027.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0028.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0029.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0030.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0031.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0032.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0033.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0034.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0035.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0036.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0037.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0038.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0039.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0040.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0041.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0042.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0043.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0044.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0045.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0046.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0047.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0048.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0049.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0050.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0051.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0052.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0053.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0054.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0055.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0056.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0057.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0058.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0059.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0060.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0061.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0062.pkl",
    "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/data/hallway/hallway/train_traj_0063.pkl"
  ],
  "transitions": 1280,
  "n_agents": 4,
  "rollout_obs_dim": 8,
  "message_dim": 8,
  "matrix_edge_rate": 1.0,
  "who_edge_rate": 1.0,
  "when_edge_rate": 1.0,
  "message_nonzero_rate": 0.125,
  "message_abs_mean": 0.125,
  "active_sender_what_coverage_mean": 0.125,
  "active_sender_what_coverage_min": 0.125,
  "active_sender_count": 5120,
  "matrix_min": 0.0,
  "matrix_max": 1.0,
  "risk_flags": [
    "nearly_all_to_all_edges_on_rollout"
  ],
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 3.0
        },
        {
          "0": 6.0
        },
        {
          "0": 1.0
        },
        {
          "0": 2.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:1",
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 2.0
        },
        {
          "0": 5.0
        },
        {
          "0": 2.0
        },
        {
          "0": 3.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:3",
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 1.0
        },
        {
          "0": 4.0
        },
        {
          "0": 2.0
        },
        {
          "0": 3.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:5",
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 2.0
        },
        {
          "0": 4.0
        },
        {
          "0": 1.0
        },
        {
          "0": 3.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:6",
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 2.0
        },
        {
          "0": 4.0
        },
        {
          "0": 2.0
        },
        {
          "0": 4.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:8",
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 2.0
        },
        {
          "0": 4.0
        },
        {
          "0": 4.0
        },
        {
          "0": 3.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:10",
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 2.0
        },
        {
          "0": 6.0
        },
        {
          "0": 4.0
        },
        {
          "0": 3.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:12",
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 3.0
        },
        {
          "0": 6.0
        },
        {
          "0": 5.0
        },
        {
          "0": 3.0
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 4.0
        },
        {
          "0": 5.0
        },
        {
          "0": 5.0
        },
        {
          "0": 3.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:15",
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 4.0
        },
        {
          "0": 4.0
        },
        {
          "0": 7.0
        },
        {
          "0": 5.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:17",
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 3.0
        },
        {
          "0": 4.0
        },
        {
          "0": 8.0
        },
        {
          "0": 3.0
        }
      ]
    },
    {
      "case_id": "train_traj_0000:19",
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
          0,
          3
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
          1,
          3
        ],
        [
          2,
          0
        ],
        [
          2,
          1
        ],
        [
          2,
          3
        ],
        [
          3,
          0
        ],
        [
          3,
          1
        ],
        [
          3,
          2
        ]
      ],
      "selected_what_indices_by_sender": [
        [
          0
        ],
        [
          0
        ],
        [
          0
        ],
        [
          0
        ]
      ],
      "what_coverage_by_sender": [
        0.125,
        0.125,
        0.125,
        0.125
      ],
      "selected_values_by_sender": [
        {
          "0": 2.0
        },
        {
          "0": 5.0
        },
        {
          "0": 8.0
        },
        {
          "0": 3.0
        }
      ]
    }
  ]
}

Recent trials:
[
  {
    "candidate": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/hallway/hallway/20260716_190000/iteration/hallway/20260716_190000/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "hallway",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-16T19:05:46+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/hallway/hallway/20260716_190000/iteration/hallway/20260716_190000/candidates/iter_000/comm_init.py",
      "documented_obs_dim": 1,
      "map_name": "hallway",
      "matrix_edge_rate": 1.0,
      "matrix_max": 1.0,
      "matrix_min": 0.0,
      "message_dim": 8,
      "valid": true,
      "validation_obs_dim": 8,
      "validation_obs_source": "rollout",
      "what_dim": 8,
      "when_edge_rate": 1.0,
      "who_edge_rate": 1.0
    }
  },
  {
    "candidate": "/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/hallway/hallway/20260716_190000/iteration/hallway/20260716_190000/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "hallway",
    "matrix_edge_rate": 1.0,
    "message_dim": 8,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-16T19:05:46+00:00",
    "valid": true,
    "when_edge_rate": 1.0,
    "who_edge_rate": 1.0
  }
]

Candidate code:
```python
import torch

def message_design_instruction() -> str:
    """
    Concise description of the communication policy:
    All agents (0--3) continuously broadcast their current position (feature index 0)
    to every other agent. This provides each agent with the positions of all others,
    enabling coordinated arrivals at the goal.
    """
    return (
        "Continuous full broadcast: agents 0..3 send their own current_position "
        "(index 0) to all other agents at every timestep."
    )

def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, n_agents, n_agents] binary mask indicating which sender -> receiver
    pairs are allowed to communicate.
    (Implementation of rules R1, R2, R3, R4: every agent sends to all others.)
    """
    batch, n_agents, _ = o.shape
    # Off-diagonal ones: every agent can send to every other agent.
    # RULE R1, R2, R3, R4: sender group G0--G3, receivers = all except sender.
    who = (1 - torch.eye(n_agents, device=o.device, dtype=torch.float32))  # [n_agents, n_agents]
    who = who.unsqueeze(0).expand(batch, -1, -1)  # [batch, n_agents, n_agents]
    return who

def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, n_agents, n_agents] binary mask indicating when a communication
    opportunity is triggered.
    (Always true because positions are always >=0.)
    """
    batch, n_agents, _ = o.shape
    # Always triggered: same off-diagonal matrix as who.
    # RULE R1, R2, R3, R4: condition "current_position >= 0" is always satisfied.
    when = (1 - torch.eye(n_agents, device=o.device, dtype=torch.float32))  # [n_agents, n_agents]
    when = when.unsqueeze(0).expand(batch, -1, -1)  # [batch, n_agents, n_agents]
    return when

def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a content mask of shape [batch, n_agents, obs_dim] indicating which parts
    of the sender's observation are communicated.
    (Messages contain only current_position, index 0.)
    """
    # RULE R1, R2, R3, R4: each agent sends its own current_position (feature index 0).
    what_mask = torch.zeros_like(o)  # [batch, n_agents, obs_dim]
    what_mask[..., 0] = 1.0          # select feature index 0 for all agents
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
