import torch as th

def message_design_instruction():
    return (
        "Each agent encodes its own health, unit type (3 bits), and absolute x/y coordinates, "
        "as well as for every enemy (0..9) its health, unit type (3 bits), and absolute position "
        "(if the enemy is observed, i.e. health > 0; otherwise zeros). "
        "The messages are aggregated by element-wise max over all other agents, so that each agent "
        "obtains a fused view of all allies' statuses and all enemies that are visible to anyone. "
        "This directly supplies the critical dimensions (ally health, position, type and enemy "
        "health, position, type) needed for focus fire, healing, and movement coordination under "
        "partial observability."
    )


def communication(o):
    """
    Computes a communication message for each agent and appends the
    aggregated messages from other agents to the observation.
    Input:  o  (2, 10, 188)   (batch, agents, features)
    Output:    (2, 10, 254)   (original observation + 66-dimensional aggregated message)
    """
    device = o.device
    b, n, _ = o.shape  # n = 10

    # ----- Own information -------------------------------------------------
    own_health = o[..., 156:157]          # (b, n, 1)
    own_type   = o[..., 157:160]          # (b, n, 3)
    own_x      = o[..., 160:161]          # (b, n, 1)
    own_y      = o[..., 161:162]          # (b, n, 1)
    own_seg    = th.cat([own_health, own_type, own_x, own_y], dim=-1)  # (b, n, 6)

    # ----- Enemy information (vectorised over 10 enemies) ------------------
    e_idx = th.arange(10, device=device, dtype=th.long)

    health_idx  = 8 + 8 * e_idx          # (10,)
    rel_x_idx   = 6 + 8 * e_idx
    rel_y_idx   = 7 + 8 * e_idx
    type0_idx   = 9 + 8 * e_idx
    type1_idx   = 10 + 8 * e_idx
    type2_idx   = 11 + 8 * e_idx

    # Gather enemy features: each (b, n, 10)
    e_health = o[..., health_idx]
    e_rel_x  = o[..., rel_x_idx]
    e_rel_y  = o[..., rel_y_idx]
    e_type0  = o[..., type0_idx]
    e_type1  = o[..., type1_idx]
    e_type2  = o[..., type2_idx]

    # Stack type bits -> (b, n, 10, 3)
    e_type = th.stack([e_type0, e_type1, e_type2], dim=-1)

    # Absolute positions
    abs_x = own_x + e_rel_x                    # (b, n, 10)
    abs_y = own_y + e_rel_y

    # Visibility mask: enemy is observed iff health > 0
    visible = (e_health > 0.0).float()         # (b, n, 10)

    # Mask out unobserved enemies
    e_health = e_health * visible
    e_type   = e_type * visible.unsqueeze(-1)  # (b, n, 10, 3)
    abs_x    = abs_x * visible
    abs_y    = abs_y * visible

    # Enemy segment: (health, type(3), abs_x, abs_y) -> 6 values per enemy
    enemy_seg = th.cat([
        e_health.unsqueeze(-1),
        e_type,
        abs_x.unsqueeze(-1),
        abs_y.unsqueeze(-1)
    ], dim=-1)                                  # (b, n, 10, 6)

    # Flatten enemies -> (b, n, 60)
    enemy_seg_flat = enemy_seg.reshape(b, n, 60)

    # Full message = own + all enemies -> (b, n, 66)
    message = th.cat([own_seg, enemy_seg_flat], dim=-1)

    # ----- Aggregate messages from other agents ----------------------------
    # (b, n_recipients, n_senders, 66)
    m_exp = message.unsqueeze(2).expand(-1, -1, n, -1)

    # Mask to exclude the agent's own message
    eye = th.eye(n, device=device)                      # (n, n)
    mask = (1.0 - eye).unsqueeze(0).unsqueeze(-1)       # (1, n, n, 1)
    # For the self-sender, set all features to a very low value
    m_masked = m_exp * mask + (-1e9) * (1.0 - mask)

    # Element-wise max over the sender dimension
    received = th.max(m_masked, dim=2).values            # (b, n, 66)

    # ----- Append aggregated message to observation ------------------------
    enhanced_o = th.cat([o, received], dim=-1)           # (b, n, 254)
    return enhanced_o
