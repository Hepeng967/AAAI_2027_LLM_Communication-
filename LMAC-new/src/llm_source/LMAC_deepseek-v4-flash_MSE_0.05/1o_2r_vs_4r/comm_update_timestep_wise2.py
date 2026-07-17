import torch as th

def message_design_instruction():
    """
    Returns a string explaining how the complementary protocol aids
    absolute coordinate recovery for roaches.
    """
    return (
        "This protocol adds temporal features missing from the previous static broadcast. "
        "By sharing cumulative displacement (dx, dy) over the past 10 timesteps, "
        "each agent provides its own motion history, enabling receivers (especially roaches) "
        "to align their own odometry and infer relative offsets. "
        "Edge proximity indicators (north/south/east/west) capture how close the sender is "
        "to map borders, offering a coarse absolute reference that is consistent across agents. "
        "The average relative position of all visible enemies over the same window gives a "
        "stable anchor point: combined with enemy absolute coordinates (already well predicted), "
        "a receiver can compute the sender's absolute location. "
        "These new fields fill the knowledge gap that previously prevented roaches from "
        "recovering their own absolute X/Y coordinates."
    )


def communication(o):
    """
    Input: o (torch.Tensor), shape (B, T, N, 66) where T=10 (past 9 + current).
    Output: enhanced_obs (torch.Tensor), shape (B, N, 66 + 94) = (B, N, 160)
    The new message (8 dims) is concatenated with the old message (39 dims)
    to form a 47-dim per-agent message. Each agent receives concatenated
    messages from the other two agents (94 dims).
    """
    B, T, N, _ = o.shape   # N=3
    device = o.device
    last_obs = o[:, -1, :, :]   # (B, N, 66) for current step

    # ---------------------------
    # 1. OLD MESSAGE (same as before) from current step
    # ---------------------------
    own_health = last_obs[..., 50:51]  # (B, N, 1)

    enemy_feats = []
    for j in range(4):
        start = 6 + j * 8
        health = last_obs[..., start + 2:start + 3]
        relX   = last_obs[..., start:start + 1]
        relY   = last_obs[..., start + 1:start + 2]
        enemy_feats.extend([health, relX, relY])
    old_msg = th.cat([own_health] + enemy_feats, dim=-1)  # (B, N, 13)

    move_flags = last_obs[..., 0:4]          # (B,N,4)
    last_action = last_obs[..., 53:63]       # (B,N,10)
    ally0 = last_obs[..., [38,39,40]]        # (B,N,3)
    ally1 = last_obs[..., [45,46,47]]
    ally_info = th.cat([ally0, ally1], dim=-1)  # (B,N,6)
    enemy_visible = last_obs[..., [4,12,20,28]] # (B,N,4)
    own_unit_type = last_obs[..., 51:53]      # (B,N,2)

    new_msg_static = th.cat(
        [move_flags, last_action, ally_info, enemy_visible, own_unit_type],
        dim=-1
    )  # (B,N,26)

    old_combined = th.cat([old_msg, new_msg_static], dim=-1)  # (B,N,39)

    # ---------------------------
    # 2. NEW TEMPORAL MESSAGE (8 dims)
    # ---------------------------
    # (a) Cumulative displacement over T steps from last action bits
    #     Assume action bits: 0=north, 1=south, 2=east, 3=west
    action_bits = o[..., 53:63]  # (B,T,N,10)
    north = action_bits[..., 0]
    south = action_bits[..., 1]
    east  = action_bits[..., 2]
    west  = action_bits[..., 3]
    dx_step = east.float() - west.float()   # (B,T,N)
    dy_step = north.float() - south.float()
    dx = dx_step.sum(dim=1, keepdim=True)   # (B,1,N) -> squeeze? Keep dim for cat
    dy = dy_step.sum(dim=1, keepdim=True)
    # shape: (B,N,1) after transpose?  dx: (B,1,N) -> permute to (B,N,1)
    dx = dx.permute(0,2,1)
    dy = dy.permute(0,2,1)

    # (b) Edge proximity: 1 - mean(can_move) over T
    move_flags_seq = o[..., 0:4].float()   # (B,T,N,4)
    mean_can_move = move_flags_seq.mean(dim=1)  # (B,N,4)
    edge_prox = 1.0 - mean_can_move           # (B,N,4)

    # (c) Average relative position of all visible enemies over T
    total_weight = th.zeros(B,N,1, device=device)
    total_X = th.zeros(B,N,1, device=device)
    total_Y = th.zeros(B,N,1, device=device)
    for j in range(4):
        vis_idx = 4 + j*8
        relX_idx = 6 + j*8
        relY_idx = 7 + j*8
        vis = o[..., vis_idx:vis_idx+1].float()  # (B,T,N,1)
        relX = o[..., relX_idx:relX_idx+1].float()
        relY = o[..., relY_idx:relY_idx+1].float()
        # weighted sum over T
        w = vis.sum(dim=1)   # (B,N,1)
        total_weight += w
        total_X += (relX * vis).sum(dim=1)
        total_Y += (relY * vis).sum(dim=1)
    avg_relX = total_X / (total_weight + 1e-8)
    avg_relY = total_Y / (total_weight + 1e-8)
    avg_enemy_rel = th.cat([avg_relX, avg_relY], dim=-1)  # (B,N,2)

    new_temporal = th.cat([dx, dy, edge_prox, avg_enemy_rel], dim=-1)  # (B,N,8)

    # ---------------------------
    # 3. Combine old and new per-agent message
    # ---------------------------
    msg_per_agent = th.cat([old_combined, new_temporal], dim=-1)  # (B,N,47)

    # ---------------------------
    # 4. For each agent, append messages from the other two
    # ---------------------------
    enhanced_list = []
    for i in range(N):
        other_msgs = msg_per_agent[:, [j for j in range(N) if j != i], :]  # (B,2,47)
        received = other_msgs.reshape(B, -1)  # (B,94)
        base_obs = last_obs[:, i, :]          # (B,66)
        enhanced_obs_i = th.cat([base_obs, received], dim=-1)  # (B,160)
        enhanced_list.append(enhanced_obs_i)

    enhanced_obs = th.stack(enhanced_list, dim=1)  # (B,N,160)
    return enhanced_obs
