## system

You are a MARL communication-policy coding agent. Return only one complete Python file in a single ```python code block```.

## user

Revise this LMAC teacher communication policy for `5z_vs_1ul` using the LLM judge feedback.

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

Rollout evaluation:
{
  "valid": true,
  "map_name": "5z_vs_1ul",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_001/comm_init.py",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/5z_vs_1ul/train_traj_0000.pkl"
  ],
  "transitions": 151,
  "n_agents": 5,
  "rollout_obs_dim": 36,
  "message_dim": 36,
  "matrix_edge_rate": 0.2,
  "who_edge_rate": 0.2,
  "when_edge_rate": 1.0,
  "message_nonzero_rate": 0.05555555555555555,
  "message_abs_mean": 0.05555555555555555,
  "matrix_min": 0.0,
  "matrix_max": 1.0,
  "risk_flags": []
}

Structured judge summary:
{
  "accepted": false,
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_001/comm_init.py",
  "dry_run": false,
  "expected_effect": "Adding position fields gives all Zealots a shared view of the Ultralisk's location, enabling coordinated surrounds and retreats. Throttling when reduces communication overhead and forces the downstream learner to focus on truly informative moments, improving training stability and policy quality.",
  "failure_analysis": "The who matrix correctly restricts sending to agent 0 broadcasting to agents 1-4, matching the task spec. The when logic uses relevant local features (own_health, enemy visibility/distance/health) but triggers too pervasively: rollout when_edge_rate=1.0 suggests it is always on during engagement, which removes sparse gating and can lead to redundant messages. The critical flaw is in what: the policy omits the required enemy position fields (indices 4,5,6 for availability, distance, rel_x), making it impossible for receivers to localise the Ultralisk. Only own_health (33) and enemy_health (8) are transmitted, leaving the team blind to target location. This fails the primary communication fact 'ultralisk_position_broadcast'.",
  "improvement_suggestions": "Modify communication_what to also set indices 4, 6, and optionally 5 according to the trigger, ensuring enemy_0_available, enemy_0_rel_x, and enemy_0_distance are included. For instance, add lines in the what function: for idx in [4,6,8,33]: what[:,:,idx] = sender_trigger. To reduce when spamming, refine the when condition to fire only on significant changes, e.g., when own_health drops below a threshold for the first time, or when enemy position changes by more than a set delta from the last message.",
  "replacement_readiness": "not_ready",
  "rollout_grounding_score": 0.9,
  "score": 0.45,
  "usage": {
    "completion_tokens": 2016,
    "prompt_tokens": 5375,
    "total_tokens": 7391
  },
  "what_score": 0.2,
  "when_score": 0.7,
  "who_score": 0.95
}

LLM failure analysis:
{
  "Evaluation": "The current who matrix is correct (agent 0 broadcasts to 1-4). The when logic triggers too pervasively (when_edge_rate=1.0 in rollout), sending on almost every step where conditions are met, causing redundant messages. The what policy omits crucial enemy position fields (indices 4,5,6) needed for localization; only own_health and enemy_health (33,8) are transmitted, which fails the primary communication fact 'ultralisk_position_broadcast'. This makes coordinated surrounds impossible. The rollout grounding is high (0.9), confirming the critique.",
  "Missing_Information_Hypothesis": "The policy fails to include the ultralisk's availability, relative x coordinate, and distance, which are essential for receivers to localize the target. Without this spatial information, the team cannot coordinate effectively, even if they know the ultralisk's health. The constant triggering reduces sparsity, making it harder for the downstream learner to attend to critical messages.",
  "Improvement_Suggestions": [
    "Add transmission of enemy position fields: indices 4 (enemy_0_available), 6 (enemy_0_rel_x), and optionally 5 (enemy_0_distance) in communication_what, alongside health (8, 33).",
    "Refine communication_when to reduce spamming: combine conditions with AND to trigger only when own_health is low AND enemy is visible AND (close or damaged). This stricter condition should lower the when_edge_rate.",
    "Use the same refined trigger for both when and what to ensure consistent gating."
  ],
  "Target_Functions": {
    "communication_who": "def communication_who(o):\n    \"\"\"\n    Only agent 0 may send to agents 1..n_agents-1.\n    \"\"\"\n    import torch\n    batch_size, n_agents, obs_dim = o.shape\n    who_matrix = torch.zeros(batch_size, n_agents, n_agents, device=o.device)\n    if n_agents >= 2:\n        who_matrix[:, 1:, 0] = 1.0\n    return torch.clamp(who_matrix, 0.0, 1.0)",
    "communication_when": "def communication_when(o):\n    \"\"\"\n    Agent 0 sends only when own_health < 40 AND enemy_0 is visible AND (distance < 5 OR enemy_0_health < 300).\n    This reduces message rate by requiring multiple conditions to be met simultaneously.\n    \"\"\"\n    import torch\n    batch_size, n_agents, obs_dim = o.shape\n    own_health = o[..., 33:34] if obs_dim > 33 else torch.zeros(batch_size, n_agents, 1)\n    enemy_available = o[..., 4:5] if obs_dim > 4 else torch.zeros(batch_size, n_agents, 1)\n    enemy_distance = o[..., 5:6] if obs_dim > 5 else torch.zeros(batch_size, n_agents, 1)\n    enemy_health = o[..., 8:9] if obs_dim > 8 else torch.zeros(batch_size, n_agents, 1)\n    low_health = (own_health < 40.0).float()\n    enemy_visible = (enemy_available > 0.5).float()\n    close_enemy = (enemy_distance < 5.0).float()\n    damaged_enemy = (enemy_health < 300.0).float()\n    trigger = low_health * enemy_visible * torch.max(close_enemy, damaged_enemy)  # (batch, n_agents, 1)\n    trigger = trigger.squeeze(-1)  # (batch, n_agents)\n    when_matrix = trigger.unsqueeze(1).expand(-1, n_agents, -1)\n    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0)\n    when_matrix = when_matrix * (1.0 - mask_self)\n    return torch.clamp(when_matrix, 0.0, 1.0)",
    "communication_what": "def communication_what(o):\n    \"\"\"\n    When the same trigger is true, include enemy position and health fields for full localization.\n    Indices: 4 (enemy_0_available), 5 (enemy_0_distance), 6 (enemy_0_rel_x), 8 (enemy_0_health), 33 (own_health).\n    \"\"\"\n    import torch\n    batch_size, n_agents, obs_dim = o.shape\n    own_health = o[..., 33:34] if obs_dim > 33 else torch.zeros(batch_size, n_agents, 1)\n    enemy_available = o[..., 4:5] if obs_dim > 4 else torch.zeros(batch_size, n_agents, 1)\n    enemy_distance = o[..., 5:6] if obs_dim > 5 else torch.zeros(batch_size, n_agents, 1)\n    enemy_health = o[..., 8:9] if obs_dim > 8 else torch.zeros(batch_size, n_agents, 1)\n    low_health = (own_health < 40.0).float()\n    enemy_visible = (enemy_available > 0.5).float()\n    close_enemy = (enemy_distance < 5.0).float()\n    damaged_enemy = (enemy_health < 300.0).float()\n    trigger = low_health * enemy_visible * torch.max(close_enemy, damaged_enemy)  # (batch, n_agents, 1)\n    trigger = trigger.squeeze(-1)  # (batch, n_agents)\n    what = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)\n    indices = [4, 5, 6, 8, 33]\n    for idx in indices:\n        if idx < obs_dim:\n            what[:, :, idx] = trigger\n    return torch.clamp(what, 0.0, 1.0)"
  }
}

Current source:
```python
import torch

def message_design_instruction():
    return (
        "WHO: Only agent 0 sends messages, and only to agents 1-4 (no self-communication). "
        "WHEN: Agent 0 sends when (own_health < 40) OR (enemy_0 is visible AND (dist < 5 OR enemy_0_health < 300)). "
        "WHAT: When triggered, the message carries own_health (index 33) and enemy_0_health (index 8); "
        "all other observation fields are masked to zero."
    )

def communication_who(o):
    """
    Determines which agents are allowed to communicate to which others.
    Input: o – observation tensor, shape (batch_size, n_agents, obs_dim)
    Returns: who_matrix – shape (batch_size, n_agents, n_agents) with values in {0,1}.
             1 indicates that the sender (last dim) is allowed to send to the receiver (middle dim).
    Only agent 0 may send, and only to agents 1..n_agents-1.
    """
    batch_size, n_agents, obs_dim = o.shape
    who_matrix = torch.zeros(batch_size, n_agents, n_agents, device=o.device)
    if n_agents >= 2:
        # receivers indexed 1..n_agents-1, sender index 0
        who_matrix[:, 1:, 0] = 1.0
    return torch.clamp(who_matrix, 0.0, 1.0)

def communication_when(o):
    """
    Determines when each sender is allowed to broadcast.
    Input: o – observation tensor, shape (batch_size, n_agents, obs_dim)
    Returns: when_matrix – shape (batch_size, n_agents, n_agents) with values in {0,1}.
             The condition only depends on the sender's local observation.
             The matrix is used to gate messages: a sender s may send to receiver r
             only if both who_matrix[b, r, s] == 1 and when_matrix[b, r, s] == 1.
    Agent 0 (the only sender) is allowed to send when:
      - own_health < 40, OR
      - enemy_0 is visible AND (distance to enemy_0 < 5 OR enemy_0_health < 300).
    """
    batch_size, n_agents, obs_dim = o.shape
    # Extract relevant features safely
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_distance = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_health = torch.zeros(batch_size, n_agents, 1, device=o.device)

    if obs_dim > 33:
        own_health = o[..., 33:34]        # own_health
    if obs_dim > 4:
        enemy_available = o[..., 4:5]     # enemy_0_available
    if obs_dim > 5:
        enemy_distance = o[..., 5:6]      # enemy_0_distance   (index 5)
    if obs_dim > 8:
        enemy_health = o[..., 8:9]        # enemy_0_health     (index 8)

    # Trigger conditions
    low_health = (own_health < 40.0).float()
    enemy_visible = (enemy_available > 0.5).float()
    close_enemy = (enemy_distance < 5.0).float()
    damaged_enemy = (enemy_health < 300.0).float()

    # Combined trigger: low health OR (enemy visible AND (close or damaged))
    condition_enemy_info = enemy_visible * torch.max(close_enemy, damaged_enemy)
    sender_trigger = torch.max(low_health, condition_enemy_info)   # shape (batch, n_agents, 1)
    sender_trigger = sender_trigger.squeeze(-1)                    # shape (batch, n_agents)

    # Build when matrix: for each (receiver, sender) pair, use the sender's trigger
    when_matrix = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1)  # (batch, n_agents, n_agents)

    # Prevent self‑communication (diagonal zeros)
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    when_matrix = when_matrix * (1.0 - mask_self)

    return torch.clamp(when_matrix, 0.0, 1.0)

def communication_what(o):
    """
    Determines which observation fields to include in the message.
    Input: o – observation tensor, shape (batch_size, n_agents, obs_dim)
    Returns: what – shape (batch_size, n_agents, obs_dim) with values in {0,1}.
             1 indicates that the corresponding observation value is allowed to be transmitted,
             masked to zero otherwise.
    The same trigger used for *when* is applied: for the sending agent, the allowed fields are
    own_health (index 33) and enemy_0_health (index 8). All other fields are zero.
    """
    batch_size, n_agents, obs_dim = o.shape
    # Extract features (same as communication_when)
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_distance = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_health = torch.zeros(batch_size, n_agents, 1, device=o.device)

    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]
    if obs_dim > 5:
        enemy_distance = o[..., 5:6]    # correct index for distance
    if obs_dim > 8:
        enemy_health = o[..., 8:9]

    # Same trigger as when
    low_health = (own_health < 40.0).float()
    enemy_visible = (enemy_available > 0.5).float()
    close_enemy = (enemy_distance < 5.0).float()
    damaged_enemy = (enemy_health < 300.0).float()
    condition_enemy_info = enemy_visible * torch.max(close_enemy, damaged_enemy)
    sender_trigger = torch.max(low_health, condition_enemy_info).squeeze(-1)  # (batch, n_agents)

    # Build mask: only indices [33, 8] are set to the sender_trigger value (0 or 1)
    what = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)
    indices = [33, 8]   # own_health, enemy_0_health
    for idx in indices:
        if idx < obs_dim:
            what[:, :, idx] = sender_trigger

    return torch.clamp(what, 0.0, 1.0)

```

Revision target:
- who failures: edit communication_who(o).
- when failures: edit communication_when(o).
- what/content failures: edit communication_what(o).
- communication_what(o) must remain an obs-aligned [batch, n_agents, obs_dim]
  mask in [0,1]; selected features keep their original indices.
- Keep the strategy pure: local observation only, deterministic, no trainable parameters.

Return only a complete Python file with all required who/when/what functions.
