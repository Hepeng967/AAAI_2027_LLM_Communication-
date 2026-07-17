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
    device = o.device

    # Feature indices for two trigger conditions
    indices_a_all = torch.tensor([4, 5, 6, 7, 8, 33, 34], device=device, dtype=torch.long)
    indices_b_all = torch.tensor([4, 5, 6, 7, 8, 33], device=device, dtype=torch.long)

    # Filter indices to only those within obs_dim (robustness)
    valid_a = indices_a_all < obs_dim
    indices_a = indices_a_all[valid_a]
    valid_b = indices_b_all < obs_dim
    indices_b = indices_b_all[valid_b]

    # Build one-hot masks: (1, 1, obs_dim)
    mask_a_flat = torch.zeros(obs_dim, device=device)
    mask_a_flat[indices_a] = 1.0
    mask_a = mask_a_flat.view(1, 1, obs_dim)

    mask_b_flat = torch.zeros(obs_dim, device=device)
    mask_b_flat[indices_b] = 1.0
    mask_b = mask_b_flat.view(1, 1, obs_dim)

    # Extract own_health and enemy_available for trigger logic
    # (batch, n_agents, 1)
    own_health = o[..., 33:34] if obs_dim > 33 else torch.zeros(batch_size, n_agents, 1, device=device)
    enemy_available = o[..., 4:5] if obs_dim > 4 else torch.zeros(batch_size, n_agents, 1, device=device)

    condition_low = (own_health < 20.0).float()          # (batch, n_agents, 1)
    condition_enemy = (enemy_available > 0.5).float()

    trigger_a = condition_low                           # low health -> uses indices_a
    trigger_b = (1.0 - condition_low) * condition_enemy  # healthy + enemy visible -> uses indices_b

    # Combine via broadcast: trigger shape (batch, n_agents, 1) * mask (1, 1, obs_dim)
    what = trigger_a * mask_a + trigger_b * mask_b  # (batch, n_agents, obs_dim)

    # Clamp to [0,1] for safety
    what = torch.clamp(what, 0.0, 1.0)
    return what
