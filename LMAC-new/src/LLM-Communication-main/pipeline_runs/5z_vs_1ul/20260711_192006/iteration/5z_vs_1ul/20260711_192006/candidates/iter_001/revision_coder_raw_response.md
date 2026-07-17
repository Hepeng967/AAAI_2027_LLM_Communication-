```python
import torch

def message_design_instruction():
    return (
        "WHO: Each Zealot broadcasts to all other Zealots (no self-communication). "
        "WHEN: A sender sends a message if (a) own_health > 0.01 (damage taken, low health distress) "
        "OR (b) enemy_0_available == 1 (enemy visible, combat information). "
        "WHAT: If damaged (trigger a): send [own_health, own_shield, enemy_0_available, "
        "enemy_0_distance, enemy_0_rel_x, enemy_0_rel_y, enemy_0_health]. "
        "If healthy and enemy visible (trigger b): send [enemy_0_available, enemy_0_distance, "
        "enemy_0_rel_x, enemy_0_rel_y, enemy_0_health, own_health]. "
        "Otherwise send nothing (zero mask)."
    )

def communication_who(o):
    """
    o: (batch, n_agents, obs_dim)
    Returns who_matrix: (batch, n_agents, n_agents) in [0,1].
    All-to-all except self.
    """
    batch_size, n_agents, obs_dim = o.shape
    # All ones, then zero out diagonal
    who_matrix = torch.ones(batch_size, n_agents, n_agents, device=o.device)
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    who_matrix = who_matrix - mask_self
    return torch.clamp(who_matrix, 0.0, 1.0)

def communication_when(o):
    """
    Determines when a sender should transmit.
    A sender activates if:
      - own_health > 0.01 (damage) OR
      - enemy_0_available > 0.5 (enemy visible)
    Creates a receiver-independent when_matrix: when_matrix[b,r,s] = sender_trigger[b,s].
    Self-communication is disabled.
    Returns when_matrix: (batch, n_agents, n_agents) in [0,1].
    """
    batch_size, n_agents, obs_dim = o.shape
    device = o.device

    # Extract features safely
    own_health = torch.zeros(batch_size, n_agents, 1, device=device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=device)

    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    # Trigger conditions (damage or enemy visible)
    condition_damaged = (own_health > 0.01).float()       # (batch, n_agents, 1)
    condition_enemy = (enemy_available > 0.5).float()     # (batch, n_agents, 1)

    sender_trigger = torch.max(condition_damaged, condition_enemy).squeeze(-1)  # (batch, n_agents)

    # Expand to (batch, n_agents, n_agents) where each column (sender) is the same trigger
    when_matrix = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1)

    # Remove self-communication
    mask_self = torch.eye(n_agents, device=device).unsqueeze(0).expand(batch_size, -1, -1)
    when_matrix = when_matrix * (1.0 - mask_self)

    return torch.clamp(when_matrix, 0.0, 1.0)

def communication_what(o):
    """
    Returns a binary mask (batch, n_agents, obs_dim) indicating which observation features
    each agent will send.
    If sender is damaged (own_health > 0.01): send features [4,5,6,7,8,33,34].
    If sender is healthy + enemy visible: send [4,5,6,7,8,33].
    Otherwise send nothing (all zeros).
    The returned mask is in [0,1].
    """
    batch_size, n_agents, obs_dim = o.shape
    device = o.device

    # Feature sets for the two cases (used with valid filtering)
    indices_a_all = torch.tensor([4, 5, 6, 7, 8, 33, 34], device=device, dtype=torch.long)
    indices_b_all = torch.tensor([4, 5, 6, 7, 8, 33], device=device, dtype=torch.long)

    # Filter indices to those within obs_dim
    valid_a = indices_a_all < obs_dim
    indices_a = indices_a_all[valid_a]
    valid_b = indices_b_all < obs_dim
    indices_b = indices_b_all[valid_b]

    # Create one-hot masks: (1, 1, obs_dim)
    mask_a = torch.zeros(1, 1, obs_dim, device=device)
    if len(indices_a) > 0:
        mask_a[0, 0, indices_a] = 1.0

    mask_b = torch.zeros(1, 1, obs_dim, device=device)
    if len(indices_b) > 0:
        mask_b[0, 0, indices_b] = 1.0

    # Extract decision features
    own_health = torch.zeros(batch_size, n_agents, 1, device=device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=device)

    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    # Trigger definitions (damaged vs enemy visible)
    condition_damaged = (own_health > 0.01).float()        # (batch, n_agents, 1)
    condition_enemy = (enemy_available > 0.5).float()

    # For damaged agents: use mask_a
    trigger_a = condition_damaged
    # For healthy agents with enemy: use mask_b
    trigger_b = (1.0 - condition_damaged) * condition_enemy

    # Combine masks weighted by triggers
    what = trigger_a * mask_a + trigger_b * mask_b   # (batch, n_agents, obs_dim)

    return torch.clamp(what, 0.0, 1.0)

```