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