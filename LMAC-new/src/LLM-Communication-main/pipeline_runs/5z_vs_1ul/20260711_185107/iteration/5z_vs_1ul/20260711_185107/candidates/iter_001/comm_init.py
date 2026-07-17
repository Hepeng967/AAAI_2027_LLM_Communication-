import torch

def message_design_instruction():
    return (
        "WHO: Only the designated sender (agent 0) communicates; it broadcasts to all "
        "other agents (agents 1–4). No self‑communication and no communication from other agents. "
        "WHEN: Agent 0 sends a message only when (a) the enemy (Ultralisk) is visible (field 4 > 0.5), "
        "or (b) its own health falls below 20 (field 33 < 20). The two conditions are OR‑combined. "
        "WHAT: If the enemy is visible AND own health ≥ 20, send only the enemy position subset: "
        "fields [4,5,6] (enemy_0_available, enemy_0_distance, enemy_0_rel_x). "
        "If own health < 20, send the own health status subset: fields [33,34] (own_health, own_shield). "
        "If both conditions are true (visible enemy while already low health), both subsets are sent. "
        "Otherwise no message is generated (all‑zero mask). "
        "All decisions are deterministic and based solely on agent 0's local observation."
    )

def communication_who(o):
    """
    Returns a who matrix of shape (batch, n_agents, n_agents) where
    who[b, r, s] = 1.0 iff s == 0 and r != 0, else 0.0.
    Only agent 0 is allowed to send, and it broadcasts to all other agents (no self‑loop).
    """
    batch_size, n_agents, _ = o.shape
    who = torch.zeros(batch_size, n_agents, n_agents, device=o.device)
    # sender = 0 broadcasts to all receivers except itself
    who[:, :, 0] = 1.0                          # all receivers get 1 for sender 0
    # zero out the diagonal (r == s)
    diag_mask = torch.eye(n_agents, device=o.device).bool().unsqueeze(0)  # (1, n, n)
    who = who.masked_fill(diag_mask, 0.0)
    return who

def communication_when(o):
    """
    Returns a when matrix of shape (batch, n_agents, n_agents) where
    when[b, r, s] = 1.0 iff s == 0, r != 0, and agent 0’s observation triggers sending.
    Trigger condition: enemy_0_available (index 4) > 0.5 OR own_health (index 33) < 20.0.
    """
    batch_size, n_agents, obs_dim = o.shape
    # Safely extract agent 0's observations
    enemy_available = o[:, 0, 4] if obs_dim > 4 else torch.zeros(batch_size, device=o.device)
    own_health = o[:, 0, 33] if obs_dim > 33 else torch.zeros(batch_size, device=o.device)

    # Trigger flags for agent 0
    trigger = ((enemy_available > 0.5) | (own_health < 20.0)).float()  # (batch,)
    # Expand to (batch, n_agents, 1) so it applies to sender dimension
    when = torch.zeros(batch_size, n_agents, n_agents, device=o.device)
    when[:, :, 0] = trigger.unsqueeze(1)         # all receivers get trigger status for sender 0
    # Remove self‑communication (diagonal)
    diag_mask = torch.eye(n_agents, device=o.device).bool().unsqueeze(0)
    when = when.masked_fill(diag_mask, 0.0)
    return when

def communication_what(o):
    """
    Returns a mask of shape (batch, n_agents, obs_dim) where
    for sender 0:
      - if enemy_0_available > 0.5 AND own_health >= 20: enable indices [4,5,6]
      - if own_health < 20: enable indices [33,34]
      - if both (visible enemy and health < 20): enable both sets
      - otherwise: all zeros.
    All other agents’ masks are left zero.
    """
    batch_size, n_agents, obs_dim = o.shape
    what = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)

    # --- compute conditions for agent 0 per batch item ---
    enemy_avail_0 = o[:, 0, 4] if obs_dim > 4 else torch.zeros(batch_size, device=o.device)
    own_health_0   = o[:, 0, 33] if obs_dim > 33 else torch.zeros(batch_size, device=o.device)

    enemy_visible = enemy_avail_0 > 0.5   # bool
    health_low    = own_health_0 < 20.0    # bool

    # Position subset: [4,5,6] (enemy_0_available, distance, rel_x)
    pos_indices = [4, 5, 6]
    # Health subset: [33,34] (own_health, own_shield)
    health_indices = [33, 34]

    # Filter to valid indices
    valid_pos = [idx for idx in pos_indices if idx < obs_dim]
    valid_health = [idx for idx in health_indices if idx < obs_dim]

    for b in range(batch_size):
        mask = torch.zeros(obs_dim, device=o.device)
        ev, hl = enemy_visible[b], health_low[b]

        if ev and not hl:
            # send only position
            mask[valid_pos] = 1.0
        elif hl:
            # send health (and if also enemy_visible, we add position as well)
            mask[valid_health] = 1.0
            if ev:  # both sets
                mask[valid_pos] = 1.0
        # else: mask stays zero

        what[b, 0, :] = mask   # only agent 0 gets a mask; others remain zero

    return what
