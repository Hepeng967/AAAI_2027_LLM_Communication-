## system

You analyze LLM-judged failures for LMAC communication policies. Return one compact JSON object only.

## user

Analyze the LLM judge result for map `5z_vs_1ul` and propose the next communication-code revision.

Judge summary:
{
  "accepted": false,
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_000/comm_init.py",
  "dry_run": false,
  "expected_effect": "Reducing who to single sender will cut communication to 1/4 of the current rate, making it easier for receivers to learn from a consistent source. Throttling when will reduce message frequency and noise, forcing agents to rely on their own observations when possible. Trimming what avoids sending redundant information that doesn't change decision outcomes.",
  "failure_analysis": "The who matrix erroneously enables all agents to broadcast to all others, while the task spec designates agent 0 as the sole sender. This introduces excessive communication overhead and dilutes the role-specific information. The when condition triggers on almost any enemy visibility and low health, leading to near-constant sending which can overwhelm learning and lacks adaptive throttling. The what content is largely appropriate but could be trimmed to the required fields.",
  "improvement_suggestions": "Restrict the who matrix so that only agent 0 sends to agents 1–4; set all other edges to zero. In the when logic, consider limiting communication to when own_health drops by a significant threshold or when enemy_0 is first spotted or its position changes notably. For what, match the exact required indices [4,5,6] for position and [34,42]? (though 42 absent) – but as a baseline, send only own_health and enemy_0_health maybe.",
  "replacement_readiness": "not_ready",
  "rollout_grounding_score": 0.9,
  "score": 0.5,
  "usage": {
    "completion_tokens": 2461,
    "prompt_tokens": 4344,
    "total_tokens": 6805
  },
  "what_score": 0.7,
  "when_score": 0.6,
  "who_score": 0.3
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "5z_vs_1ul",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_000/comm_init.py",
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

Recent trials:
[
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:46:01+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_000/comm_init.py",
      "documented_obs_dim": 35,
      "map_name": "5z_vs_1ul",
      "matrix_edge_rate": 1.0,
      "matrix_max": 1.0,
      "matrix_min": 0.0,
      "message_dim": 36,
      "valid": true,
      "validation_obs_dim": 36,
      "validation_obs_source": "rollout",
      "what_dim": 36,
      "when_edge_rate": 1.0,
      "who_edge_rate": 1.0
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 36,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:46:01+00:00",
    "valid": true,
    "when_edge_rate": 1.0,
    "who_edge_rate": 1.0
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_000/comm_init.py",
    "failure_analysis": "The who matrix erroneously enables all agents to broadcast to all others, while the task spec designates agent 0 as the sole sender. This introduces excessive communication overhead and dilutes the role-specific information. The when condition triggers on almost any enemy visibility and low health, leading to near-constant sending which can overwhelm learning and lacks adaptive throttling. The what content is largely appropriate but could be trimmed to the required fields.",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 36,
    "next_hypothesis": "Restrict the who matrix so that only agent 0 sends to agents 1–4; set all other edges to zero. In the when logic, consider limiting communication to when own_health drops by a significant threshold or when enemy_0 is first spotted or its position changes notably. For what, match the exact required indices [4,5,6] for position and [34,42]? (though 42 absent) – but as a baseline, send only own_health and enemy_0_health maybe.",
    "rollout_grounding_score": 0.9,
    "score": 0.5,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-11T18:46:48+00:00",
    "valid": true,
    "what_score": 0.7,
    "when_score": 0.6,
    "who_score": 0.3
  }
]

Current code:
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

Return JSON with keys:
- Evaluation
- Missing_Information_Hypothesis
- Improvement_Suggestions
- Target_Functions
Do not use downstream RL win-rate as feedback. Focus on rollout-grounded who/when/what critique only.
