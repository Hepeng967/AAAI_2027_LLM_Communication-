import torch as th

def message_design_instruction():
    """
    Returns a string explaining how the updated communication protocol aids
    global state reconstruction and coordination, complementing the existing message.
    """
    explanation = (
        "The updated protocol builds upon the existing 5-dimensional message (enemy_visibility, "
        "relative enemy position, own health, attack flag) by adding 6 new dimensions:\n"
        " - can_move_N (idx0): whether the agent can move North.\n"
        " - can_move_S (idx1): whether the agent can move South.\n"
        " - can_move_E (idx2): whether the agent can move East.\n"
        " - can_move_W (idx3): whether the agent can move West.\n"
        " - own_shield_ratio (idx35): the agent's remaining shield ratio.\n"
        " - normalized_distance_to_enemy (idx7): normalized Euclidean distance to the enemy.\n\n"
        "These additional features are directly observable by each agent and provide critical "
        "spatial and resource constraints. Movement possibilities encode map boundaries and allow "
        "receiving agents to better infer absolute positions (e.g., when an agent cannot move north, "
        "it is near the top edge). The shield ratio together with health gives a complete survivability "
        "picture, essential for coordinated focus fire and retreat decisions. The normalized distance "
        "to enemy enhances relative positioning awareness, especially when agents lose line-of-sight. "
        "Combined, the 11-dimensional message per agent (5+6) reduces state uncertainty across all "
        "agents, enabling more accurate reconstruction of the global state and improving coordination."
    )
    return explanation

def communication(o):
    """
    Input: o – torch.Tensor of shape (batch_size, n_agents, 48)
    Output: enhanced observation of shape (batch_size, n_agents, 48 + appended_message_dim)
    where appended_message_dim = (n_agents - 1) * 11 = 44.
    
    Each agent broadcasts an 11-dimensional message combining the previous 5 fields
    (enemy_visible, rel_enemy_x, rel_enemy_y, own_health, attack_flag) and the new 6 fields
    (can_move_N, can_move_S, can_move_E, can_move_W, own_shield_ratio, normalized_distance_to_enemy).
    The message from all other agents is appended to each agent's observation.
    """
    batch_size, n_agents, obs_dim = o.shape
    assert n_agents == 5 and obs_dim == 48, "Expected 5 agents and 48-dim observations"

    # ---- Extract all 11 message components (batch, n_agents, 1) each ----
    # Existing fields (keep unchanged)
    enemy_vis     = o[:, :, 4:5]     # enemy visible
    rel_enemy_x   = o[:, :, 5:6]     # relative enemy x
    rel_enemy_y   = o[:, :, 6:7]     # relative enemy y
    own_health    = o[:, :, 34:35]   # own health ratio
    attack_flag   = o[:, :, 42:43]   # last action was Attack

    # New fields (complementary, not overlapping)
    can_move_north = o[:, :, 0:1]    # can move north
    can_move_south = o[:, :, 1:2]    # can move south
    can_move_east  = o[:, :, 2:3]    # can move east
    can_move_west  = o[:, :, 3:4]    # can move west
    own_shield     = o[:, :, 35:36]  # own shield ratio
    dist_to_enemy  = o[:, :, 7:8]    # normalized distance to enemy

    # Concatenate along feature dimension -> (batch, n_agents, 11)
    msg = th.cat([
        enemy_vis, rel_enemy_x, rel_enemy_y, own_health, attack_flag,
        can_move_north, can_move_south, can_move_east, can_move_west,
        own_shield, dist_to_enemy
    ], dim=2)

    # ---- Build output: original obs + zeros for appended messages ----
    msg_append_dim = (n_agents - 1) * 11  # 44
    output = th.cat([
        o,
        th.zeros(batch_size, n_agents, msg_append_dim,
                 device=o.device, dtype=o.dtype)
    ], dim=2)

    # ---- For each agent, gather the 11-dim messages from all others ----
    for i in range(n_agents):
        other_indices = [j for j in range(n_agents) if j != i]
        # Stack messages from others: each shape (batch, 1, 11)
        others_msg_list = [msg[:, j:j+1, :] for j in other_indices]
        # Concatenate over feature dim -> (batch, 1, 44)
        others_msg = th.cat(others_msg_list, dim=2)
        # Write into output at the appended portion
        output[:, i, 48:] = others_msg.squeeze(1)

    return output
