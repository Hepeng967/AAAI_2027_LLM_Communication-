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
