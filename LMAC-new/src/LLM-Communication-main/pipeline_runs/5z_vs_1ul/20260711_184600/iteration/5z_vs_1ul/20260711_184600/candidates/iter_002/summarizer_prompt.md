## system

You analyze LLM-judged failures for LMAC communication policies. Return one compact JSON object only.

## user

Analyze the LLM judge result for map `5z_vs_1ul` and propose the next communication-code revision.

Judge summary:
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

Recent trials:
[
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
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:49:01+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_001/comm_init.py",
      "documented_obs_dim": 35,
      "map_name": "5z_vs_1ul",
      "matrix_edge_rate": 0.2,
      "matrix_max": 1.0,
      "matrix_min": 0.0,
      "message_dim": 36,
      "valid": true,
      "validation_obs_dim": 36,
      "validation_obs_source": "rollout",
      "what_dim": 36,
      "when_edge_rate": 1.0,
      "who_edge_rate": 0.2
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 0.2,
    "message_dim": 36,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:49:01+00:00",
    "valid": true,
    "when_edge_rate": 1.0,
    "who_edge_rate": 0.2
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_001/comm_init.py",
    "failure_analysis": "The who matrix correctly restricts sending to agent 0 broadcasting to agents 1-4, matching the task spec. The when logic uses relevant local features (own_health, enemy visibility/distance/health) but triggers too pervasively: rollout when_edge_rate=1.0 suggests it is always on during engagement, which removes sparse gating and can lead to redundant messages. The critical flaw is in what: the policy omits the required enemy position fields (indices 4,5,6 for availability, distance, rel_x), making it impossible for receivers to localise the Ultralisk. Only own_health (33) and enemy_health (8) are transmitted, leaving the team blind to target location. This fails the primary communication fact 'ultralisk_position_broadcast'.",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 0.2,
    "message_dim": 36,
    "next_hypothesis": "Modify communication_what to also set indices 4, 6, and optionally 5 according to the trigger, ensuring enemy_0_available, enemy_0_rel_x, and enemy_0_distance are included. For instance, add lines in the what function: for idx in [4,6,8,33]: what[:,:,idx] = sender_trigger. To reduce when spamming, refine the when condition to fire only on significant changes, e.g., when own_health drops below a threshold for the first time, or when enemy position changes by more than a set delta from the last message.",
    "rollout_grounding_score": 0.9,
    "score": 0.45,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-11T18:49:36+00:00",
    "valid": true,
    "what_score": 0.2,
    "when_score": 0.7,
    "who_score": 0.95
  }
]

Current code:
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

Return JSON with keys:
- Evaluation
- Missing_Information_Hypothesis
- Improvement_Suggestions
- Target_Functions
Do not use downstream RL win-rate as feedback. Focus on rollout-grounded who/when/what critique only.
