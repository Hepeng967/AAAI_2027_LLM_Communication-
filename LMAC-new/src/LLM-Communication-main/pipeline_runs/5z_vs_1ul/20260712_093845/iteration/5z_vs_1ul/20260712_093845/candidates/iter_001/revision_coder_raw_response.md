```python
import torch

def message_design_instruction():
    return (
        "WHO: Each Zealot broadcasts to all other Zealots (no self-communication). "
        "WHEN: A sender sends a message if (a) own_health < 0.25 (low health distress) "
        "OR (b) enemy_0_available > 0.5 (enemy visible). "
        "WHAT: If low health (trigger a): send [own_health, own_shield]. "
        "If enemy visible (trigger b): send [enemy_0_available, enemy_0_distance, "
        "enemy_0_rel_x, enemy_0_rel_y, enemy_0_health, own_health]. "
        "If both triggers are active, send union of both sets. "
        "Otherwise send nothing (zero mask)."
    )


def communication_who(o):
    """
    All-to-all except self.
    o: (batch_size, n_agents, obs_dim)
    Returns: (batch_size, n_agents, n_agents) in [0,1].
    """
    batch_size, n_agents, obs_dim = o.shape
    who_matrix = torch.ones(batch_size, n_agents, n_agents, device=o.device)
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    who_matrix = who_matrix - mask_self
    return torch.clamp(who_matrix, 0.0, 1.0)


def communication_when(o):
    """
    Sparse triggering based on own health and enemy visibility.
    o: (batch_size, n_agents, obs_dim)
    Returns: (batch_size, n_agents, n_agents) in [0,1].
    """
    batch_size, n_agents, obs_dim = o.shape

    # Extract relevant observation slices (safe indexing)
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    # R1: Threshold within observed range [0, 0.625]; 0.25 ≈ 40 % health.
    condition_low_health = (own_health < 0.25).float()
    condition_enemy_visible = (enemy_available > 0.5).float()

    # Sender triggers if either condition holds
    sender_trigger = torch.max(condition_low_health, condition_enemy_visible).squeeze(-1)  # (batch, n_agents)

    # When matrix: sender_trigger broadcast over receivers
    when_matrix = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1)  # (batch, n_agents, n_agents)

    # No self-communication
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    when_matrix = when_matrix * (1.0 - mask_self)

    return torch.clamp(when_matrix, 0.0, 1.0)


def communication_what(o):
    """
    Build observation‑aligned masks for two independent triggers.
    o: (batch_size, n_agents, obs_dim)
    Returns: (batch_size, n_agents, obs_dim) in [0,1].
    """
    batch_size, n_agents, obs_dim = o.shape

    # Safe extraction
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    # Separate triggers (both can be active)
    trigger_a = (own_health < 0.25).float()          # low health
    trigger_b = (enemy_available > 0.5).float()      # enemy visible

    # Feature index sets (R2: what to send per condition)
    indices_a = [33, 34]            # own_health, own_shield
    indices_b = [4, 5, 6, 7, 8, 33] # enemy info + own_health

    # One‑hot masks over the observation dimension
    mask_a = torch.zeros(obs_dim, device=o.device)
    mask_b = torch.zeros(obs_dim, device=o.device)
    mask_a[torch.tensor(indices_a, device=o.device, dtype=torch.long)] = 1.0
    mask_b[torch.tensor(indices_b, device=o.device, dtype=torch.long)] = 1.0

    # Broadcast triggers to obs dimension
    what_a = trigger_a * mask_a.unsqueeze(0).unsqueeze(0)  # (batch, n_agents, obs_dim)
    what_b = trigger_b * mask_b.unsqueeze(0).unsqueeze(0)

    what = what_a + what_b
    return torch.clamp(what, 0.0, 1.0)
```