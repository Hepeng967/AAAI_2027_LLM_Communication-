import torch as th

def message_design_instruction():
    """
    Returns a string explaining how the designed communication protocol aids
    global state reconstruction and coordination.
    """
    explanation = (
        "Each agent broadcasts a compact 5-dimensional message containing:\n"
        " - enemy_visible (categorical): whether the agent sees the Ultralisk.\n"
        " - relative_enemy_x, relative_enemy_y (continuous): the agent's relative "
        "position to the enemy (if visible, else 0).\n"
        " - own_health_ratio (continuous): the agent's remaining health.\n"
        " - attack_flag (categorical): whether the agent's last action was Attack.\n\n"
        "These local features are directly observable by each agent and are key "
        "for reconstructing the global state. When received by teammates, they allow:\n"
        " - Inference of each agent's absolute position relative to the enemy and to each other.\n"
        " - Awareness of teammate health and engagement status (attack vs. movement).\n"
        " - Coordinated focus fire, kiting, and positioning despite partial visibility.\n\n"
        "The message is compact (5 floats per agent), ensuring low overhead while "
        "providing sufficient information for state uncertainty reduction."
    )
    return explanation

def communication(o):
    """
    Input: o – torch.Tensor of shape (batch_size, n_agents, 48)
    Output: enhanced observation of shape (batch_size, n_agents, 48 + appended_message_dim)
    where appended_message_dim = (n_agents - 1) * 5 = 20.
    
    The protocol broadcasts each agent's own features (enemy visibility, relative enemy
    position, health, attack flag) to all other agents. No message is appended to the sender.
    """
    batch_size, n_agents, obs_dim = o.shape
    assert n_agents == 5 and obs_dim == 48, "Expected 5 agents and 48-dim observations"
    
    # Extract components for the message (shape: (batch, n_agents, 1) each)
    enemy_vis = o[:, :, 4:5]          # can enemy be seen?
    rel_enemy_x = o[:, :, 5:6]        # relative X to enemy
    rel_enemy_y = o[:, :, 6:7]        # relative Y to enemy
    own_health = o[:, :, 34:35]       # own health ratio
    attack_flag = o[:, :, 42:43]      # last action was Attack
    
    # Build message: (batch, n_agents, 5)
    msg = th.cat([enemy_vis, rel_enemy_x, rel_enemy_y, own_health, attack_flag], dim=2)
    
    # Prepare output: original observation + zeros for received messages
    msg_append_dim = (n_agents - 1) * 5  # 20
    output = th.cat([o, th.zeros(batch_size, n_agents, msg_append_dim,
                                 device=o.device, dtype=o.dtype)], dim=2)
    
    # For each agent, gather messages from all other agents
    for i in range(n_agents):
        other_indices = [j for j in range(n_agents) if j != i]
        # messages from others: list of (batch, 1, 5) tensors
        others_msg_list = [msg[:, j:j+1, :] for j in other_indices]
        # concatenate over the feature dimension to get (batch, 1, 20)
        others_msg = th.cat(others_msg_list, dim=2)  # (batch, 1, 20)
        # remove the singleton agent dimension and assign into output
        output[:, i, 48:] = others_msg.squeeze(1)
    
    return output

def communication_matrix(o):
    """
    matrix[:, receiver, sender] = 1.
    Dynamic task-decision teacher:
    - Zealots that see the Ultralisk broadcast target position.
    - Zealots that are attacking broadcast engagement intent.
    - Low-health Zealots broadcast survivability context.
    - Agent 0 remains the certified anchor sender, which keeps the required
      task-fact edge available while other Zealots communicate only when useful.
    """
    batch_size, n_agents, _ = o.shape
    device = o.device
    dtype = o.dtype

    enemy_visible = o[:, :, 4] > 0.5
    attack_intent = o[:, :, 42] > 0.5
    own_health = o[:, :, 34]
    low_health = (own_health > 0.0) & (own_health < 0.45)
    active_sender = enemy_visible | attack_intent | low_health

    active_sender[:, 0] = True

    matrix = active_sender.to(dtype).unsqueeze(1).expand(batch_size, n_agents, n_agents).clone()
    eye = th.eye(n_agents, device=device, dtype=dtype).unsqueeze(0)
    return matrix * (1.0 - eye)
