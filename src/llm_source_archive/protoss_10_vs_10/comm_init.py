import torch as th

def message_design_instruction():
    """
    This protocol enables global state reconstruction and coordination by having each agent
    explicitly share its own status (health, shield, unit type, position) and its current
    attack intent, including the target's identity, health, shield, absolute position, and
    unit type. Recipients aggregate these messages (mean over all other agents) to obtain a
    team-wide summary: which enemies are being focused, average health of allies, spatial
    distribution, and the presence of low-health targets. This directly addresses the
    critical dimensions (ally/enemy health, shield, absolute positions, unit types) and
    compensates for partial observability, enabling coordinated focus fire, support, and
    movement.
    """
    return __doc__  # using the string above

def communication(o):
    """
    Args:
        o: observation tensor of shape (2, 10, 208)
    Returns:
        Enhanced observation with message_dim=25 appended (shape (2, 10, 233)).
        The appended 25 dimensions are the mean of the messages from all *other* agents.
    """
    # Extract own state
    own_health = o[..., 175]          # (2, 10)
    own_shield = o[..., 176]          # (2, 10)
    unit_type = o[..., 177:180]       # (2, 10, 3)
    own_pos_x = o[..., 180]           # (2, 10)
    own_pos_y = o[..., 181]           # (2, 10)

    # Attack action: indices 188..197 (attack enemy 0..9) as one-hot, shape (2, 10, 10)
    att_onehot = o[..., 188:198]
    is_attacking = att_onehot.sum(dim=-1)  # 1 if attacking any enemy, else 0

    # Gather enemy features for all 10 enemies (each enemy block has 9 dims starting at index 4)
    # Indices for health, shield, rel_x, rel_y, and the three unit-type bits
    enemy_health_all = th.stack([o[..., 8 + i*9] for i in range(10)], dim=-1)   # (2, 10, 10)
    enemy_shield_all = th.stack([o[..., 9 + i*9] for i in range(10)], dim=-1)   # (2, 10, 10)
    enemy_relx_all   = th.stack([o[..., 6 + i*9] for i in range(10)], dim=-1)   # (2, 10, 10)
    enemy_rely_all   = th.stack([o[..., 7 + i*9] for i in range(10)], dim=-1)   # (2, 10, 10)
    enemy_type0_all  = th.stack([o[..., 10 + i*9] for i in range(10)], dim=-1)  # (2, 10, 10)
    enemy_type1_all  = th.stack([o[..., 11 + i*9] for i in range(10)], dim=-1)
    enemy_type2_all  = th.stack([o[..., 12 + i*9] for i in range(10)], dim=-1)

    # Use the one-hot attack vector to select the target's features
    # (2, 10, 10) -> weighted sum over the last dim -> (2, 10)
    target_health   = (att_onehot * enemy_health_all).sum(dim=-1)
    target_shield   = (att_onehot * enemy_shield_all).sum(dim=-1)
    target_relx     = (att_onehot * enemy_relx_all).sum(dim=-1)
    target_rely     = (att_onehot * enemy_rely_all).sum(dim=-1)
    target_type0    = (att_onehot * enemy_type0_all).sum(dim=-1)
    target_type1    = (att_onehot * enemy_type1_all).sum(dim=-1)
    target_type2    = (att_onehot * enemy_type2_all).sum(dim=-1)

    # Compute absolute position of the target
    target_abs_x = own_pos_x + target_relx
    target_abs_y = own_pos_y + target_rely

    # Assemble per-agent message of size 25
    # Stack along last dimension
    message = th.stack([
        own_health,
        own_shield,
        unit_type[..., 0],
        unit_type[..., 1],
        unit_type[..., 2],
        own_pos_x,
        own_pos_y,
        is_attacking,
        att_onehot[..., 0],  # one-hot of target index (10 values)
        att_onehot[..., 1],
        att_onehot[..., 2],
        att_onehot[..., 3],
        att_onehot[..., 4],
        att_onehot[..., 5],
        att_onehot[..., 6],
        att_onehot[..., 7],
        att_onehot[..., 8],
        att_onehot[..., 9],
        target_health,
        target_shield,
        target_abs_x,
        target_abs_y,
        target_type0,
        target_type1,
        target_type2,
    ], dim=-1)  # shape (2, 10, 25)

    # Aggregate: for each agent, take the mean of all *other* agents' messages
    sum_all = message.sum(dim=1, keepdim=True)      # (2, 1, 25)
    sum_others = sum_all - message                  # (2, 10, 25)
    agg_message = sum_others / (message.shape[1] - 1)  # divide by 9

    # Append aggregated message to the original observation
    enhanced_o = th.cat([o, agg_message], dim=-1)   # (2, 10, 208+25)
    return enhanced_o
