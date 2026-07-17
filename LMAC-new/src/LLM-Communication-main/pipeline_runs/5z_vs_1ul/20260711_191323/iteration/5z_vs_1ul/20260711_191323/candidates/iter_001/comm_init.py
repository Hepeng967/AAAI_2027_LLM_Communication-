import torch

def message_design_instruction():
    return (
        "WHO: Each Zealot broadcasts to all other Zealots (no self-communication). "
        "WHEN: A sender sends a message if (a) own_health < 0.1 (low health distress) "
        "OR (b) enemy_0_available > 0.5 (enemy visible, combat information). "
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
    # Clamp to [0,1] (safety)
    who_matrix = torch.clamp(who_matrix, 0.0, 1.0)
    return who_matrix

def communication_when(o):
    batch_size, n_agents, obs_dim = o.shape
    # Extract features from observation: indices [33]=own_health, [4]=enemy_0_available
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)

    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    # Trigger conditions for each sender (normalised threshold)
    # (own_health < 0.1) OR (enemy_0_available > 0.5)
    condition_low_health = (own_health < 0.1).float()
    condition_enemy_visible = (enemy_available > 0.5).float()

    # Combined: trigger if either condition is 1
    sender_trigger = torch.max(condition_low_health, condition_enemy_visible)  # (batch, n_agents, 1)
    sender_trigger = sender_trigger.squeeze(-1)  # (batch, n_agents)

    # Build when matrix: for each (receiver, sender) pair, use sender's trigger
    when_matrix = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1)  # (batch, n_agents, n_agents)

    # Zero out self-communication (diagonal)
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    when_matrix = when_matrix * (1.0 - mask_self)

    # Ensure [0,1]
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

    # Use the same normalised threshold as when
    condition_low = (own_health < 0.1).float()          # (batch, n_agents, 1)
    condition_enemy = (enemy_available > 0.5).float()

    # Trigger a: low health
    trigger_a = condition_low
    # Trigger b: healthy AND enemy visible
    trigger_b = (1.0 - condition_low) * condition_enemy

    # Define indices sets (indices from the observation mapping)
    indices_a = [4, 5, 6, 7, 8, 33, 34]   # enemy info + own health/shield
    indices_b = [4, 5, 6, 7, 8, 33]        # enemy info + own health

    indices_a_t = torch.tensor(indices_a, dtype=torch.long, device=o.device)
    indices_b_t = torch.tensor(indices_b, dtype=torch.long, device=o.device)

    valid_a = indices_a_t < obs_dim
    valid_b = indices_b_t < obs_dim

    mask_a = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)
    if valid_a.any():
        mask_a[:, :, indices_a_t[valid_a]] = 1.0

    mask_b = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)
    if valid_b.any():
        mask_b[:, :, indices_b_t[valid_b]] = 1.0

    # Combine based on triggers
    what = trigger_a * mask_a + trigger_b * mask_b
    what = torch.clamp(what, 0.0, 1.0)
    return what
