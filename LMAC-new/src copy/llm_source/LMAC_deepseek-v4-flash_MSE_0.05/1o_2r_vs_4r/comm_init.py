import torch as th

def message_design_instruction():
    """
    Returns a string explaining how the designed protocol aids
    global state reconstruction using critical dimensions.
    """
    return (
        "This protocol compensates for partial observability by having each agent broadcast "
        "its own health and the health and relative positions of all four enemies it perceives. "
        "The Overseer (agent with large sight range) can share accurate enemy positions and "
        "healths; other agents can infer the global enemy state by combining these broadcasts "
        "with their own knowledge of the sender's location (via ally visibility slots). "
        "The shared enemy healths enable coordinated focus fire on the weakest target, "
        "while shared relative positions allow approximate triangulation of enemy locations. "
        "Additionally, broadcasting own health helps allies assess team survivability and "
        "decide when to engage or retreat. Together, these messages bridge the knowledge gap "
        "caused by limited sight ranges and enhance coordination efficiency."
    )

def communication(o):
    """
    Input: o (torch.Tensor), shape (batch, agents, 66)
    Output: enhanced_obs (torch.Tensor), shape (batch, agents, 66 + 2*M)
            where M = 13 (health + 4 enemies * 3 features = 1+12=13).
    """
    B, N, _ = o.shape  # N = 3 agents
    M = 13  # message length per agent

    # 1. Own health: index 50
    own_health = o[..., 50:51]  # shape (B, N, 1)

    # 2. Enemy features: indices for each enemy j
    #    health: 8 + j*8, relX: 6 + j*8, relY: 7 + j*8
    enemy_feats = []
    for j in range(4):
        start = 6 + j * 8
        health = o[..., start+2:start+3]   # health index = start+2
        relX   = o[..., start:start+1]     # relX index = start
        relY   = o[..., start+1:start+2]   # relY index = start+1
        enemy_feats.extend([health, relX, relY])

    # Concatenate to form per-agent message (B, N, M)
    msg_per_agent = th.cat([own_health] + enemy_feats, dim=-1)  # (B, N, 13)

    # 3. Build enhanced observations: for each agent, append messages from the other two agents
    enhanced_list = []
    for i in range(N):
        # Gather messages from agents j != i
        other_msgs = [msg_per_agent[:, j, :] for j in range(N) if j != i]  # list of 2 tensors (B, 13)
        received = th.cat(other_msgs, dim=-1)  # (B, 26)
        # Append to agent i's own observation
        enhanced_obs_i = th.cat([o[:, i, :], received], dim=-1)  # (B, 66+26)
        enhanced_list.append(enhanced_obs_i)

    # Stack across agents -> (B, N, 66+26)
    enhanced_obs = th.stack(enhanced_list, dim=1)
    return enhanced_obs

def communication_matrix(o):
    """
    matrix[:, receiver, sender] = 1.
    Each agent receives messages from the other two agents.
    """
    batch_size, n_agents, _ = o.shape
    device = o.device
    matrix = th.ones(batch_size, n_agents, n_agents, device=device, dtype=o.dtype)
    eye = th.eye(n_agents, device=device, dtype=o.dtype).unsqueeze(0)
    return matrix * (1.0 - eye)
