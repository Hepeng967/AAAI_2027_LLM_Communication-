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
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_000/comm_init.py",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/5z_vs_1ul/train_traj_0000.pkl"
  ],
  "transitions": 151,
  "n_agents": 5,
  "rollout_obs_dim": 36,
  "message_dim": 36,
  "matrix_edge_rate": 1.0,
  "who_edge_rate": 1.0,
  "when_edge_rate": 1.0,
  "message_nonzero_rate": 0.19444444444444445,
  "message_abs_mean": 0.19444444444444445,
  "matrix_min": 0.0,
  "matrix_max": 1.0,
  "risk_flags": [
    "nearly_all_to_all_edges_on_rollout"
  ]
}

Structured judge summary:
{
  "accepted": false,
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_000/comm_init.py",
  "dry_run": false,
  "expected_effect": "Concentrating communication on the single designated sender reduces noise and bandwidth waste, letting the other Zealots focus on coordinated surround and retreats based solely on the essential target location and team health status, which directly supports the required coordination for this map.",
  "failure_analysis": "Who matrix is all‑to‑all (off‑diagonal) for all agents, ignoring the task spec where only agent 0 needs to broadcast to others. When triggers for any agent that sees the enemy or has low health, causing excessive and redundant communication from all Zealots. What sends a superset of enemy features (availability, distance, relative coordinates, health) and own health/shield, but the spec requires a precise separation: only fields [4,5,6] for the Ultralisk position and [34,42] for health and attack intent; field 42 is not present in rollout observations and own_shield (34) is not sent in the ‘healthy’ trigger case, reducing consistency.",
  "improvement_suggestions": "Narrow who to sender 0 only. For when, restrict the position broadcast to enemy visibility, and the health/intent broadcast to a meaningful event (e.g. health change or threshold). For what, split strictly: position broadcast sends only indices [4,5,6]; health/intent broadcast sends indices [33,34] (own_health, own_shield). Handle the missing field 42 by noting that attack intent may not be directly observable in this rollout; a separate binary feature or proxy could be introduced if required, but the current design should at least align with available features.",
  "replacement_readiness": "not_ready",
  "rollout_grounding_score": 0.9,
  "score": 0.4,
  "usage": {
    "completion_tokens": 2653,
    "prompt_tokens": 4344,
    "total_tokens": 6997
  },
  "what_score": 0.4,
  "when_score": 0.5,
  "who_score": 0.1
}

LLM failure analysis:
{
  "Evaluation": "Current communication policy uses all-to-all who (edge rate 1.0) and triggers when any agent sees enemy or has low health, causing excessive redundant communication. The what sends superset of observations (indices 4,5,6,7,8,33,34) instead of strictly [4,5,6] for enemy position and [33,34] for own health/shield; field 42 (attack intent) is absent. Rollout shows nearly all-to-all edges, consistent with the who and when design.",
  "Missing_Information_Hypothesis": "The code lacks precise alignment with the task spec, which requires only agent 0 to broadcast position (enemy relative coordinates) when enemy is visible, and own health/shield when own health is low. The missing information is the exact observation index semantics: indices [4,5,6] map to enemy availability, distance, and relative x (position subset), while [33,34] are own health and shield. Additionally, the absent attack intent field (index 42) cannot be directly observed and should be omitted or proxied by low-health threshold.",
  "Improvement_Suggestions": [
    "Restrict who to sender 0 only: who_matrix[b,r,s] = 1.0 iff s==0 and r!=s, else 0.0.",
    "When triggers only for sender 0: set when_matrix[b,r,0] = 1.0 if (o[b,0,4] > 0.5) or (o[b,0,33] < 20.0), else 0.0 for all r!=0. Other senders (1..4) never trigger.",
    "What mask strictly separates position and health/intent: if enemy visible (o[b,0,4]>0.5) and health >= 20, enable indices [4,5,6] (position); if health < 20, enable indices [33,34] (own health, shield); if both, enable both sets. Remove indices 7,8 and any other features.",
    "Handle field 42 absence: ignore attack intent; low-health broadcast suffices as a proxy."
  ],
  "Target_Functions": [
    "communication_who",
    "communication_when",
    "communication_what"
  ]
}

Current source:
```python
import torch

def message_design_instruction():
    return (
        "WHO: Each Zealot broadcasts to all other Zealots (no self-communication). "
        "WHEN: A sender sends a message if (a) own_health < 20 (low health distress) "
        "OR (b) enemy_0_available == 1 (enemy visible, combat information). "
        "WHAT: If low health (trigger a): send [own_health, own_shield, enemy_0_available, "
        "enemy_0_distance, enemy_0_rel_x, enemy_0_rel_y, enemy_0_health]. "
        "If healthy and enemy visible (trigger b): send [enemy_0_available, enemy_0_distance, "
        "enemy_0_rel_x, enemy_0_rel_y, enemy_0_health, own_health]. "
        "Otherwise send nothing (zero mask)."
    )

def communication_who(o):
    # o: (batch, n_agents, obs_dim)
    batch_size, n_agents, obs_dim = o.shape
    # All-to-all except self: matrix of ones minus identity
    who_matrix = torch.ones(batch_size, n_agents, n_agents, device=o.device)
    # Zero out self-communication on diagonal
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    who_matrix = who_matrix - mask_self
    # Clamp to [0,1] (should already be, but safety)
    who_matrix = torch.clamp(who_matrix, 0.0, 1.0)
    return who_matrix

def communication_when(o):
    batch_size, n_agents, obs_dim = o.shape
    # Extract features from observation: indices [33]=own_health, [4]=enemy_0_available
    # Handle case where obs_dim < 34 safely; use obs_dim check
    # own_health index 33, enemy_0_available index 4
    # We'll fill tensors with zeros if out-of-range
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)

    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    # Trigger conditions for each sender: 
    # (own_health < 20) OR (enemy_0_available > 0.5)
    # Both return shape (batch, n_agents, 1)
    condition_low_health = (own_health < 20.0).float()
    condition_enemy_visible = (enemy_available > 0.5).float()

    # Combined: trigger if either condition is 1
    sender_trigger = torch.max(condition_low_health, condition_enemy_visible)  # (batch, n_agents, 1)
    sender_trigger = sender_trigger.squeeze(-1)  # (batch, n_agents)

    # Build when matrix: for each (receiver, sender) pair, use sender's trigger
    # Expand sender_trigger to (batch, n_agents, 1) and broadcast multiply with who's pattern
    # Actually: when_matrix[b,r,s] = sender_trigger[b,s] (receiver-agnostic)
    when_matrix = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1)  # (batch, n_agents, n_agents)

    # Zero out self-communication (diagonal)
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    when_matrix = when_matrix * (1.0 - mask_self)

    # Ensure [0,1]
    when_matrix = torch.clamp(when_matrix, 0.0, 1.0)
    return when_matrix

def communication_what(o):
    batch_size, n_agents, obs_dim = o.shape
    # Initialize mask with zeros
    what = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)

    # Indices for trigger a (low health): [4,5,6,7,8,33,34]
    indices_a = [4, 5, 6, 7, 8, 33, 34]
    # Indices for trigger b (healthy + enemy visible): [4,5,6,7,8,33]
    indices_b = [4, 5, 6, 7, 8, 33]

    # Determine per-agent which trigger is active
    # Use same conditions as when: own_health < 20 (trigger a), else if enemy visible (trigger b)
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    condition_low = (own_health < 20.0).float()  # (batch, n_agents, 1)
    condition_enemy = (enemy_available > 0.5).float()

    # Trigger a active: low health (regardless of enemy visible)
    trigger_a = condition_low  # (batch, n_agents, 1)
    # Trigger b active: not low health AND enemy visible
    trigger_b = (1.0 - condition_low) * condition_enemy  # (batch, n_agents, 1)

    # Apply masks for agents where triggers are active
    # Expand to full obs_dim for scatter-like assignment
    for agent_idx in range(n_agents):
        # Get per-agent trigger status (batch, 1)
        ta = trigger_a[:, agent_idx, :]  # (batch, 1)
        tb = trigger_b[:, agent_idx, :]  # (batch, 1)

        # For each batch, if ta=1 use indices_a, else if tb=1 use indices_b, else zeros
        # Vectorized: combine both with appropriate scaling
        # We'll do element-wise assignment per agent
        for b in range(batch_size):
            if ta[b, 0] > 0.5:
                # Use indices_a (filter out-of-range)
                valid_indices = [idx for idx in indices_a if idx < obs_dim]
                what[b, agent_idx, valid_indices] = 1.0
            elif tb[b, 0] > 0.5:
                valid_indices = [idx for idx in indices_b if idx < obs_dim]
                what[b, agent_idx, valid_indices] = 1.0
            # else: what stays zeros

    # Clamp to [0,1] safety
    what = torch.clamp(what, 0.0, 1.0)
    return what
```

Revision target:
- who failures: edit communication_who(o).
- when failures: edit communication_when(o).
- what/content failures: edit communication_what(o).
- communication_what(o) must remain an obs-aligned [batch, n_agents, obs_dim]
  mask in [0,1]; selected features keep their original indices.
- Keep the strategy pure: local observation only, deterministic, no trainable parameters.

Return only a complete Python file with all required who/when/what functions.
