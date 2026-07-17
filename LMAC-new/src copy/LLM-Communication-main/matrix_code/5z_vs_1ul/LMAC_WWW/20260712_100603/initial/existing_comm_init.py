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


# RULE R4 (all‑to‑all connectivity): In a small homogeneous team, every agent can
# receive from every other agent. Stable, no change needed.
def communication_who(o):
    # o: (batch, n_agents, obs_dim)
    batch_size, n_agents, obs_dim = o.shape
    who_matrix = torch.ones(batch_size, n_agents, n_agents, device=o.device)
    # Remove self-communication on the diagonal
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    who_matrix = who_matrix - mask_self
    who_matrix = torch.clamp(who_matrix, 0.0, 1.0)
    return who_matrix


# RULE R1 (low‑health distress trigger) & RULE R2 (enemy‑visible trigger):
# Corrected threshold from out‑of‑scale 20.0 → normalized 0.2 (max observed ≈0.625).
# RULE R3 (disjoint priority): low‑health overrides enemy visibility, implemented via max.
def communication_when(o):
    batch_size, n_agents, obs_dim = o.shape
    # Extract relevant features
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)

    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    # Normalized threshold: own_health < 0.2 represents low health
    condition_low_health = (own_health < 0.2).float()
    condition_enemy_visible = (enemy_available > 0.5).float()

    # Combined trigger: low health or enemy visible
    sender_trigger = torch.max(condition_low_health, condition_enemy_visible)  # (B, A, 1)
    sender_trigger = sender_trigger.squeeze(-1)  # (B, A)

    # when_matrix: for each (receiver, sender) use sender's trigger
    when_matrix = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1)  # (B, A, A)

    # Zero out self-communication on the diagonal
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    when_matrix = when_matrix * (1.0 - mask_self)

    when_matrix = torch.clamp(when_matrix, 0.0, 1.0)
    return when_matrix


# RULE R5 (feature‑mask selection): Low‑health distress includes shield (index 34),
# enemy‑only report omits shield. Masks unchanged, only threshold fixed.
def communication_what(o):
    batch_size, n_agents, obs_dim = o.shape

    # Feature indices for the two trigger types
    indices_a = [4, 5, 6, 7, 8, 33, 34]   # low health: includes own_shield
    indices_b = [4, 5, 6, 7, 8, 33]        # enemy visible + healthy: omits shield

    # Build binary masks (no loops)
    idx_a_tensor = torch.tensor(indices_a, device=o.device, dtype=torch.long)
    valid_a = idx_a_tensor[idx_a_tensor < obs_dim]
    mask_a = torch.zeros(obs_dim, device=o.device)
    mask_a[valid_a] = 1.0

    idx_b_tensor = torch.tensor(indices_b, device=o.device, dtype=torch.long)
    valid_b = idx_b_tensor[idx_b_tensor < obs_dim]
    mask_b = torch.zeros(obs_dim, device=o.device)
    mask_b[valid_b] = 1.0

    # Extract conditions (normalized threshold, same as `when`)
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]

    condition_low = (own_health < 0.2).float()          # corrected threshold
    condition_enemy = (enemy_available > 0.5).float()

    # Disjoint triggers: low-health always takes priority (R3)
    trigger_a = condition_low                            # (B, A, 1)
    trigger_b = (1.0 - condition_low) * condition_enemy  # (B, A, 1)

    # Build what tensor via vectorized broadcasting
    what = trigger_a * mask_a.view(1, 1, -1) + trigger_b * mask_b.view(1, 1, -1)
    what = torch.clamp(what, 0.0, 1.0)
    return what
