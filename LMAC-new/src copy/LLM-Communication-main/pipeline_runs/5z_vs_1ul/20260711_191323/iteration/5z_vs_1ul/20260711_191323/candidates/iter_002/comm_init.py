import torch


def message_design_instruction():
    return (
        "WHO: Each Zealot broadcasts to all other Zealots (no self-communication). "
        "WHEN: A sender sends a message if (a) alive (own_health > 0) AND own_health < 0.1 (low health distress) "
        "OR (b) enemy_0_available > 0.5 (enemy visible, combat information). "
        "Dead agents (own_health == 0) never send messages, preventing noise. "
        "WHAT: If low health and alive (trigger a): send [own_health, own_shield, enemy_0_available, "
        "enemy_0_distance, enemy_0_rel_x, enemy_0_rel_y, enemy_0_health]. "
        "If alive, not low health, and enemy visible (trigger b): send [enemy_0_available, enemy_0_distance, "
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
    who_matrix = torch.clamp(who_matrix, 0.0, 1.0)
    return who_matrix


def communication_when(o):
    batch_size, n_agents, obs_dim = o.shape

    # Safely extract own_health (index 33) and enemy_available (index 4)
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    # Alive indicator: non-zero health is a reliable proxy for being alive.
    alive = (own_health > 0.0).float()  # (batch, n_agents, 1)

    # Revised triggers exclude dead agents:
    # (alive AND own_health < 0.1) OR (enemy_0_available > 0.5)
    condition_low_health = alive * (own_health < 0.1).float()
    condition_enemy_visible = (enemy_available > 0.5).float()

    sender_trigger = torch.max(condition_low_health, condition_enemy_visible)  # (batch, n_agents, 1)
    sender_trigger = sender_trigger.squeeze(-1)  # (batch, n_agents)

    # Broadcast sender trigger to all receivers
    when_matrix = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1)  # (batch, n_agents, n_agents)

    # Zero out self-communication diagonal
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    when_matrix = when_matrix * (1.0 - mask_self)

    when_matrix = torch.clamp(when_matrix, 0.0, 1.0)
    return when_matrix


def communication_what(o):
    batch_size, n_agents, obs_dim = o.shape

    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    alive = (own_health > 0.0).float()                   # (batch, n_agents, 1)
    condition_low = alive * (own_health < 0.1).float()   # dead agents excluded
    condition_enemy = (enemy_available > 0.5).float()

    # trigger_a: alive and low health
    trigger_a = condition_low
    # trigger_b: alive, not low health, and enemy visible
    trigger_b = (1.0 - condition_low) * condition_enemy   # 1-condition_low already zero for dead agents

    # Observation feature groups (keeping original indices aligned with rollout dataset)
    indices_a = [4, 5, 6, 7, 8, 33, 34]  # enemy info + own health/shield
    indices_b = [4, 5, 6, 7, 8, 33]       # enemy info + own health

    indices_a_t = torch.tensor(indices_a, dtype=torch.long, device=o.device)
    indices_b_t = torch.tensor(indices_b, dtype=torch.long, device=o.device)

    # Build binary masks for selected features
    valid_a = indices_a_t < obs_dim
    mask_a = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)
    if valid_a.any():
        mask_a[:, :, indices_a_t[valid_a]] = 1.0

    valid_b = indices_b_t < obs_dim
    mask_b = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)
    if valid_b.any():
        mask_b[:, :, indices_b_t[valid_b]] = 1.0

    # Combine masks per sender based on active trigger (dead senders get zero because trigger_a=0 and trigger_b=0)
    what = trigger_a * mask_a + trigger_b * mask_b
    what = torch.clamp(what, 0.0, 1.0)

    return what
