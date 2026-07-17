import torch as th

def message_design_instruction():
    """
    Returns a string explaining how the new temporal message aids global state reconstruction.
    """
    explanation = (
        "The new protocol complements the existing 11-dimensional current-step message by broadcasting "
        "a 67-dimensional temporal history of each agent's own movement actions (last action move directions "
        "for all 10 past steps) and its past health, shield, and attack flag (for the 9 steps before the current step). "
        "This sequence provides other agents with a trajectory of displacement and damage events. "
        "By integrating these actions over time, agents can estimate relative position changes from a common reference, "
        "reducing the systematic failure in absolute coordinate prediction identified in the evaluation. "
        "The explicit sharing of past health/shield dynamics also helps propagate sudden damage events, "
        "lowering residual variance in health prediction. This temporal context is strictly complementary "
        "to the static single-timestep features already shared, and it addresses the missing information "
        "of action history and health/shield changes over time."
    )
    return explanation

def communication(o):
    """
    Input: o – torch.Tensor of shape (batch_size, T, n_agents, 48) where T=10 (window of past 10 steps)
    Output: enhanced observation of shape (batch_size, n_agents, 48 + appended_msg_dim)
    where appended_msg_dim = (n_agents - 1) * (11 + 67) = 4 * 78 = 312.
    
    Each agent broadcasts:
      - 11-dimensional message from the previous protocol (current-step features)
      - 67-dimensional temporal message (history of actions and past health/shield/attack)
    These are concatenated per other agent and appended to each agent's observation.
    """
    batch_size, T, n_agents, obs_dim = o.shape
    assert T == 10, "Expected T=10 (past 10 steps)"
    assert n_agents == 5 and obs_dim == 48, "Expected 5 agents and 48-dim observations"

    device = o.device
    dtype = o.dtype

    # ----- Current observation (last timestep) -----
    o_cur = o[:, 9, :, :]  # (batch, agents, 48)

    # ----- Previous 11-dim message (from current timestep) -----
    enemy_vis     = o_cur[:, :, 4:5]   # (batch, agents, 1)
    rel_enemy_x   = o_cur[:, :, 5:6]
    rel_enemy_y   = o_cur[:, :, 6:7]
    own_health    = o_cur[:, :, 34:35]
    attack_flag   = o_cur[:, :, 42:43]
    can_move_north = o_cur[:, :, 0:1]
    can_move_south = o_cur[:, :, 1:2]
    can_move_east  = o_cur[:, :, 2:3]
    can_move_west  = o_cur[:, :, 3:4]
    own_shield     = o_cur[:, :, 35:36]
    dist_to_enemy  = o_cur[:, :, 7:8]

    msg_11 = th.cat([
        enemy_vis, rel_enemy_x, rel_enemy_y, own_health, attack_flag,
        can_move_north, can_move_south, can_move_east, can_move_west,
        own_shield, dist_to_enemy
    ], dim=2)  # (batch, agents, 11)

    # ----- New 67-dim temporal message (from history) -----
    # For each agent, extract a sequence of:
    # - last action move directions (indices 38-41) for all 10 timesteps -> 40 dims
    # - past 9 timesteps (t=0..8) of attack flag (42), own health (34), own shield (35) -> 27 dims
    # Total 67 dims.

    # Move directions: (batch, 10, agents, 4) -> reshape to (batch, agents, 40)
    move_dirs = o[:, :, :, 38:42]  # (batch, 10, agents, 4)
    move_dirs_flat = move_dirs.permute(0, 2, 1, 3).contiguous().view(batch_size, n_agents, 40)  # (batch, agents, 40)

    # Past health, shield, attack: timesteps 0..8 (9 timesteps)
    past_health = o[:, 0:9, :, 34:35]   # (batch, 9, agents, 1)
    past_shield = o[:, 0:9, :, 35:36]   # (batch, 9, agents, 1)
    past_attack = o[:, 0:9, :, 42:43]   # (batch, 9, agents, 1)
    past_combined = th.cat([past_attack, past_health, past_shield], dim=3)  # (batch, 9, agents, 3)
    past_flat = past_combined.permute(0, 2, 1, 3).contiguous().view(batch_size, n_agents, 27)  # (batch, agents, 27)

    msg_67 = th.cat([move_dirs_flat, past_flat], dim=2)  # (batch, agents, 67)

    # ----- Combined message per agent (11+67=78) -----
    msg_combined = th.cat([msg_11, msg_67], dim=2)  # (batch, agents, 78)

    # ----- Build output tensor -----
    msg_append_dim = (n_agents - 1) * 78  # 4*78=312
    output = th.cat([
        o_cur,
        th.zeros(batch_size, n_agents, msg_append_dim, device=device, dtype=dtype)
    ], dim=2)

    # ----- For each agent, gather messages from all other agents -----
    for i in range(n_agents):
        # Indices of other agents
        other_indices = [j for j in range(n_agents) if j != i]
        # Stack their combined messages
        others_msg = th.cat([msg_combined[:, j:j+1, :] for j in other_indices], dim=2)  # (batch, 1, 312)
        output[:, i, 48:] = others_msg.squeeze(1)

    return output
