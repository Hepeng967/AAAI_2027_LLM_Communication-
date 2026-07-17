import torch as th

def message_design_instruction():
    return (
        "The message contains the sender's self status (type, health, absolute position), "
        "last action one-hot, and the two highest-priority enemy targets (type, health, absolute position). "
        "For each recipient, the received message is the mean of all other agents' messages, providing "
        "a summary of teammates' states and intentions, aiding in focus firing and coordination."
    )

def communication(o):
    """
    Constructs enhanced observations with messages from other agents.

    Args:
        o: observation tensor, shape (2, 10, 188)

    Returns:
        enhanced_o: tensor of shape (2, 10, 188 + 34) where the extra 34 dimensions
                    contain the aggregated message from all other agents.
    """
    batch_size, n_agents, _ = o.shape

    # 1. Self info: own_health (156), unit_type bits (157-159), own_pos (160-161)
    self_info = o[..., 156:162]  # (2,10,6)

    # 2. Last action one-hot (162:178)
    last_action = o[..., 162:178]  # (2,10,16)

    # 3. Enemy info: dims 4..83 (80), reshape to (2,10,10,8)
    enemy_block = o[..., 4:84].reshape(batch_size, n_agents, 10, 8)
    rel_x = enemy_block[..., 2]      # (2,10,10)
    rel_y = enemy_block[..., 3]
    health = enemy_block[..., 4]
    type_bits = enemy_block[..., 5:8]  # (2,10,10,3)

    # Compute absolute positions using own absolute pos
    own_pos_x = o[..., 160:161]   # (2,10,1)
    own_pos_y = o[..., 161:162]
    abs_x = own_pos_x + rel_x
    abs_y = own_pos_y + rel_y

    # Select 2 enemies with smallest positive health (alive)
    valid_mask = health > 0
    health_for_sort = health.clone()
    health_for_sort[~valid_mask] = float('inf')
    topk_health, topk_indices = th.topk(health_for_sort, k=2, dim=2, largest=False)

    # Gather features for top enemies
    # type_bits: (2,10,10,3) -> gather along dim=2
    indices_3d = topk_indices.unsqueeze(-1).expand(-1, -1, -1, 3)
    sel_type_bits = th.gather(type_bits, dim=2, index=indices_3d)  # (2,10,2,3)

    # health, abs_x, abs_y
    indices_2d = topk_indices
    sel_health = th.gather(health, dim=2, index=indices_2d).unsqueeze(-1)  # (2,10,2,1)
    sel_abs_x = th.gather(abs_x, dim=2, index=indices_2d).unsqueeze(-1)
    sel_abs_y = th.gather(abs_y, dim=2, index=indices_2d).unsqueeze(-1)

    enemy_feat = th.cat([sel_type_bits, sel_health, sel_abs_x, sel_abs_y], dim=-1)  # (2,10,2,6)

    # Zero out invalid entries (where topk_health is inf)
    valid_selected = (topk_health < float('inf')).unsqueeze(-1).float()  # (2,10,2,1)
    enemy_feat = enemy_feat * valid_selected

    enemy_info = enemy_feat.reshape(batch_size, n_agents, 12)

    # 4. per-agent message (34 dims)
    message = th.cat([self_info, last_action, enemy_info], dim=-1)  # (2,10,34)

    # 5. Aggregate messages from other agents (exclude self)
    sum_all = message.sum(dim=1, keepdim=True)  # (2,1,34)
    others_mean = (sum_all - message) / (n_agents - 1)  # (2,10,34)

    # 6. Append to original observation
    enhanced_o = th.cat([o, others_mean], dim=-1)  # (2,10,188+34)

    return enhanced_o
