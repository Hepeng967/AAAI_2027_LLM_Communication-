## system

You are a MARL communication-policy coding agent. Return only one complete Python file in a single ```python code block```.

## user

Repair this LMAC teacher communication policy for `5z_vs_1ul`.

Validation error:
Traceback (most recent call last):
  File "/data/hp/LLM_Communication/LMAC-new/src/hl_comm/candidate_io.py", line 66, in validate_candidate
    return _validate_candidate(path, map_name, rollout_summary=rollout_summary)
  File "/data/hp/LLM_Communication/LMAC-new/src/hl_comm/candidate_io.py", line 93, in _validate_candidate
    raise RuntimeError(f"Candidate is missing required functions: {missing}")
RuntimeError: Candidate is missing required functions: ['message_design_instruction']


Map spec:
{
  "n_agents": 5,
  "obs_dim": 48,
  "time_seq": 10,
  "task_probes": [
    {
      "name": "ultralisk_position_broadcast",
      "sender": 0,
      "fields": [
        4,
        5,
        6
      ],
      "receivers": [
        1,
        2,
        3,
        4
      ],
      "fact": "ultralisk_visibility_position"
    },
    {
      "name": "health_and_attack_intent_broadcast",
      "sender": 0,
      "fields": [
        34,
        42
      ],
      "receivers": [
        1,
        2,
        3,
        4
      ],
      "fact": "health_and_attack_intent"
    }
  ],
  "required_task_facts": [
    {
      "fact": "ultralisk_visibility_position",
      "sender": 0,
      "fields": [
        4,
        5,
        6
      ],
      "receivers": [
        1,
        2,
        3,
        4
      ],
      "feasibility": "The sender observes Ultralisk visibility and relative position.",
      "necessity": "Other Zealots need shared target localization to maintain surround and avoid isolated attacks.",
      "decision_relevance": "Ultralisk position changes chase, surround, and retreat choices."
    },
    {
      "fact": "health_and_attack_intent",
      "sender": 0,
      "fields": [
        34,
        42
      ],
      "receivers": [
        1,
        2,
        3,
        4
      ],
      "feasibility": "The sender observes the relevant health and attack-intent fields.",
      "necessity": "Receivers need team and intent context to coordinate focus and disengagement.",
      "decision_relevance": "Health and attack intent alter whether agents trade damage or reposition."
    }
  ]
}

Rollout-backed LMAC observation alignment:
{
  "map_name": "5z_vs_1ul",
  "rollout_root": "/data/hp/LLM_Communication/LMAC-new/data",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/5z_vs_1ul/train_traj_0000.pkl"
  ],
  "available": true,
  "n_agents": 5,
  "rollout_obs_dim": 36,
  "documented_obs_dim": 35,
  "extra_obs_dim": 1,
  "episodes": 1,
  "transitions": 151,
  "seq_lengths": [
    151
  ],
  "action_dim": 7,
  "agent_types": [
    "zealot",
    "zealot",
    "zealot",
    "zealot",
    "zealot"
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
    "ally_0_visible": [
      9,
      10
    ],
    "ally_0_distance": [
      10,
      11
    ],
    "ally_0_rel_x": [
      11,
      12
    ],
    "ally_0_rel_y": [
      12,
      13
    ],
    "ally_0_health": [
      13,
      14
    ],
    "ally_0_shield": [
      14,
      15
    ],
    "ally_1_visible": [
      15,
      16
    ],
    "ally_1_distance": [
      16,
      17
    ],
    "ally_1_rel_x": [
      17,
      18
    ],
    "ally_1_rel_y": [
      18,
      19
    ],
    "ally_1_health": [
      19,
      20
    ],
    "ally_1_shield": [
      20,
      21
    ],
    "ally_2_visible": [
      21,
      22
    ],
    "ally_2_distance": [
      22,
      23
    ],
    "ally_2_rel_x": [
      23,
      24
    ],
    "ally_2_rel_y": [
      24,
      25
    ],
    "ally_2_health": [
      25,
      26
    ],
    "ally_2_shield": [
      26,
      27
    ],
    "ally_3_visible": [
      27,
      28
    ],
    "ally_3_distance": [
      28,
      29
    ],
    "ally_3_rel_x": [
      29,
      30
    ],
    "ally_3_rel_y": [
      30,
      31
    ],
    "ally_3_health": [
      31,
      32
    ],
    "ally_3_shield": [
      32,
      33
    ],
    "own_health": [
      33,
      34
    ],
    "own_shield": [
      34,
      35
    ],
    "lmac_extra_35": [
      35,
      36
    ]
  },
  "alignment_note": "Use rollout_obs_dim as the true LMAC input dimension. Documented SMAC features keep their original indices. Any lmac_extra_* dimensions are wrapper/config-added features and must not be treated as hidden global state."
}

Current code:
```python
import torch

def communication_who(o):
    """
    Determines which agents are allowed to communicate to which others.
    Only agent 0 may send, and only to agents 1..n_agents-1.
    """
    batch_size, n_agents, obs_dim = o.shape
    who_matrix = torch.zeros(batch_size, n_agents, n_agents, device=o.device)
    if n_agents >= 2:
        who_matrix[:, 1:, 0] = 1.0
    return torch.clamp(who_matrix, 0.0, 1.0)

def communication_when(o):
    """
    Agent 0 sends only when own_health < 40 AND enemy_0 is visible AND (distance < 5 OR enemy_0_health < 300).
    This strict AND condition reduces message rate compared to the previous OR‑based trigger.
    """
    batch_size, n_agents, obs_dim = o.shape
    # Extract relevant features safely
    own_health      = o[..., 33:34] if obs_dim > 33 else torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = o[...,  4:5]  if obs_dim >  4 else torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_distance  = o[...,  5:6]  if obs_dim >  5 else torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_health    = o[...,  8:9]  if obs_dim >  8 else torch.zeros(batch_size, n_agents, 1, device=o.device)

    low_health      = (own_health      < 40.0).float()
    enemy_visible   = (enemy_available >  0.5).float()
    close_enemy     = (enemy_distance  <  5.0).float()
    damaged_enemy   = (enemy_health    < 300.0).float()

    # Stricter AND combination: low_health AND visible AND (close OR damaged)
    trigger = low_health * enemy_visible * torch.max(close_enemy, damaged_enemy)  # (batch, n_agents, 1)
    trigger = trigger.squeeze(-1)  # (batch, n_agents)

    # Build when matrix: sender's trigger broadcast to all receivers
    when_matrix = trigger.unsqueeze(1).expand(-1, n_agents, -1)

    # Block self-communication (diagonal)
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0)
    when_matrix = when_matrix * (1.0 - mask_self)

    return torch.clamp(when_matrix, 0.0, 1.0)

def communication_what(o):
    """
    When the same trigger is active, transmit enemy position and health fields
    needed for ultralisk localisation and team coordination.
    Indices: 4 (enemy_0_available), 5 (enemy_0_distance), 6 (enemy_0_rel_x),
             8 (enemy_0_health), 33 (own_health).
    """
    batch_size, n_agents, obs_dim = o.shape
    # Extract features (same as in communication_when)
    own_health      = o[..., 33:34] if obs_dim > 33 else torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = o[...,  4:5]  if obs_dim >  4 else torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_distance  = o[...,  5:6]  if obs_dim >  5 else torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_health    = o[...,  8:9]  if obs_dim >  8 else torch.zeros(batch_size, n_agents, 1, device=o.device)

    low_health      = (own_health      < 40.0).float()
    enemy_visible   = (enemy_available >  0.5).float()
    close_enemy     = (enemy_distance  <  5.0).float()
    damaged_enemy   = (enemy_health    < 300.0).float()

    # Same strict AND trigger as when
    trigger = low_health * enemy_visible * torch.max(close_enemy, damaged_enemy).squeeze(-1)  # (batch, n_agents)

    # Build the message mask: only the required indices are set to the trigger value
    what = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)
    # ultralisk_position_broadcast: 4,5,6; health_and_attack_intent: 8,33 (own_health)
    indices = [4, 5, 6, 8, 33]
    for idx in indices:
        if idx < obs_dim:
            what[:, :, idx] = trigger

    return torch.clamp(what, 0.0, 1.0)

```

Return a complete corrected Python file. Preserve message_design_instruction, communication,
communication_who, communication_when, and communication_what.
