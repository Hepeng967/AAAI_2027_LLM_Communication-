```python
import torch

def message_design_instruction():
    return (
        "WHO: Each Zealot broadcasts to all other Zealots (no self-communication). "
        "WHEN: A sender sends a message if (a) own_health < 0.2 (low health distress) "
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
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    who_matrix = who_matrix - mask_self
    # Optional: further gating by ally visibility can be added here,
    # but current simple all-to-all is kept for high coordination.
    return torch.clamp(who_matrix, 0.0, 1.0)


def communication_when(o):
    batch_size, n_agents, obs_dim = o.shape
    # own_health at index 33, enemy_0_available at index 4
    own_health = o[..., 33:34] if obs_dim > 33 else torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = o[..., 4:5] if obs_dim > 4 else torch.zeros(batch_size, n_agents, 1, device=o.device)

    # Normalized threshold: max health is 0.625, so 0.2 means ~32% health.
    condition_low = (own_health < 0.2).float()
    condition_enemy = (enemy_available > 0.5).float()
    sender_trigger = torch.max(condition_low, condition_enemy).squeeze(-1)  # (batch, n_agents)

    when_matrix = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1)  # (batch, n_agents, n_agents)
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    when_matrix = when_matrix * (1.0 - mask_self)
    return torch.clamp(when_matrix, 0.0, 1.0)


def communication_what(o):
    batch_size, n_agents, obs_dim = o.shape

    # Extract relevant features with fallback
    own_health = o[..., 33:34] if obs_dim > 33 else torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = o[..., 4:5] if obs_dim > 4 else torch.zeros(batch_size, n_agents, 1, device=o.device)

    # Corrected threshold
    condition_low = (own_health < 0.2).float()
    condition_enemy = (enemy_available > 0.5).float()

    # trigger_a: low health (always sends set a)
    # trigger_b: healthy AND enemy visible (sends set b)
    trigger_a = condition_low
    trigger_b = (1.0 - condition_low) * condition_enemy

    # Define desired feature index sets (as in message_design_instruction)
    indices_a = torch.tensor([4, 5, 6, 7, 8, 33, 34], dtype=torch.long, device=o.device)
    indices_b = torch.tensor([4, 5, 6, 7, 8, 33], dtype=torch.long, device=o.device)

    # Filter out-of-range indices (safety)
    valid_a = indices_a[indices_a < obs_dim]
    valid_b = indices_b[indices_b < obs_dim]

    # Build binary masks for the two sets
    mask_a = torch.zeros(1, 1, obs_dim, device=o.device)
    mask_b = torch.zeros(1, 1, obs_dim, device=o.device)
    if valid_a.numel() > 0:
        mask_a[..., valid_a] = 1.0
    if valid_b.numel() > 0:
        mask_b[..., valid_b] = 1.0

    # Combine: if trigger_a active -> mask_a; if trigger_b active -> mask_b; else zeros
    what = trigger_a * mask_a + trigger_b * mask_b
    return torch.clamp(what, 0.0, 1.0)
```