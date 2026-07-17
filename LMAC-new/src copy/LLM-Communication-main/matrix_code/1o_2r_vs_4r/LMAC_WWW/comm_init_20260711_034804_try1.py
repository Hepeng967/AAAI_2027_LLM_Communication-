import torch

def message_design_instruction():
    return (
        "WHO: Overseer (agent 0) sends to Roach1 (agent 1) and Roach2 (agent 2). "
        "Roach1 and Roach2 each optionally send to Overseer. No other edges are active.\n"
        "WHEN: Overseer->Roach edges are active when Overseer sees any enemy "
        "(any enemy_available flag in obs[sender, indices 4,11,18,25] is 1). "
        "Roach->Overseer edges are active when the roach is alive (own_health > 0, index 46).\n"
        "WHAT: Overseer sends all enemy features (indices 4-31, 28 floats). "
        "Each Roach sends own_health, own_type_0, own_type_1, and ally_0_visible (4 floats)."
    )

def communication_who(o):
    """WHO matrix: (batch, n_agents, n_agents) with [receiver, sender] convention."""
    bs, n_agents, obs_dim = o.shape
    
    # Initialize zeros
    who = torch.zeros(bs, n_agents, n_agents, device=o.device, dtype=o.dtype)
    
    if n_agents >= 3:
        # Overseer (0) -> Roach1 (1): receiver=1, sender=0
        who[:, 1, 0] = 1.0
        # Overseer (0) -> Roach2 (2): receiver=2, sender=0
        who[:, 2, 0] = 1.0
        # Roach1 (1) -> Overseer (0): receiver=0, sender=1
        who[:, 0, 1] = 1.0
        # Roach2 (2) -> Overseer (0): receiver=0, sender=2
        who[:, 0, 2] = 1.0
    
    return who

def communication_when(o):
    """WHEN matrix: (batch, n_agents, n_agents) with [receiver, sender] convention."""
    bs, n_agents, obs_dim = o.shape
    
    # Initialize all to 1 (active by default; we'll zero out what we don't want)
    when = torch.ones(bs, n_agents, n_agents, device=o.device, dtype=o.dtype)
    
    # Zero out diagonal (no self-communication)
    if n_agents > 0:
        idx = torch.arange(n_agents, device=o.device)
        when[:, idx, idx] = 0.0
    
    if n_agents >= 3:
        # --- Edge overseer (sender 0) -> roach1 (receiver 1) ---
        # Trigger: any enemy available in sender 0's obs
        # Check indices 4, 11, 18, 25
        enemy_flags_0 = []
        if 4 < obs_dim:
            enemy_flags_0.append(o[:, 0, 4:5])  # Keep dims
        if 11 < obs_dim:
            enemy_flags_0.append(o[:, 0, 11:12])
        if 18 < obs_dim:
            enemy_flags_0.append(o[:, 0, 18:19])
        if 25 < obs_dim:
            enemy_flags_0.append(o[:, 0, 25:26])
        
        if enemy_flags_0:
            any_enemy_0 = torch.cat(enemy_flags_0, dim=-1).any(dim=-1, keepdim=True).float()  # (bs, 1)
            # Condition: any_enemy_0 == 1
            overseer_active = (any_enemy_0 >= 0.5).float().squeeze(-1)  # (bs,)
            # Apply to edges (receiver=1, sender=0) and (receiver=2, sender=0)
            when[:, 1, 0] = when[:, 1, 0] * overseer_active
            when[:, 2, 0] = when[:, 2, 0] * overseer_active
        else:
            # No enemy features available, zero out overseer->roach edges
            when[:, 1, 0] = 0.0
            when[:, 2, 0] = 0.0
        
        # --- Edge roach1 (sender 1) -> overseer (receiver 0) ---
        # Trigger: own_health > 0 for sender 1
        if 46 < obs_dim:
            health_1 = o[:, 1, 46]  # (bs,)
            roach1_alive = (health_1 > 0).float()
            when[:, 0, 1] = when[:, 0, 1] * roach1_alive
        else:
            when[:, 0, 1] = 0.0
        
        # --- Edge roach2 (sender 2) -> overseer (receiver 0) ---
        if 46 < obs_dim:
            health_2 = o[:, 2, 46]  # (bs,)
            roach2_alive = (health_2 > 0).float()
            when[:, 0, 2] = when[:, 0, 2] * roach2_alive
        else:
            when[:, 0, 2] = 0.0
    
    # Zero out edges not in WHO (though WHO will later multiply, zero when for non-WHO edges)
    who = communication_who(o)
    when = when * who
    
    return when

def communication_what(o):
    """WHAT: per-sender message content. Output shape (bs, n_agents, message_dim)."""
    bs, n_agents, obs_dim = o.shape
    
    # For agent 0 (overseer): message dim 28 (enemy features indices 4-31)
    # For agents 1,2 (roaches): message dim 4
    #
    # We'll build messages as list and then pad to same dim.
    
    # Define max message dim
    msg_dim = 28  # Maximum across agents
    
    # Initialize output tensor
    messages = torch.zeros(bs, n_agents, msg_dim, device=o.device, dtype=o.dtype)
    
    if n_agents >= 1:
        # Agent 0 (overseer): indices 4..31 (28 values)
        # Check bounds
        start_0 = 4
        end_0 = min(32, obs_dim)  # Exclusive end
        if start_0 < obs_dim:
            enemy_data = o[:, 0, start_0:end_0]  # (bs, end_0-start_0)
            msg_dim_0 = end_0 - start_0
            messages[:, 0, :msg_dim_0] = enemy_data
    
    if n_agents >= 2:
        # Agent 1 (roach 1): [own_health(46), own_type_0(47), own_type_1(48), ally_0_visible(32)]
        features_1 = []
        # own_health index 46
        if 46 < obs_dim:
            features_1.append(o[:, 1, 46:47])
        else:
            features_1.append(torch.zeros(bs, 1, device=o.device, dtype=o.dtype))
        # own_type_0 index 47
        if 47 < obs_dim:
            features_1.append(o[:, 1, 47:48])
        else:
            features_1.append(torch.zeros(bs, 1, device=o.device, dtype=o.dtype))
        # own_type_1 index 48
        if 48 < obs_dim:
            features_1.append(o[:, 1, 48:49])
        else:
            features_1.append(torch.zeros(bs, 1, device=o.device, dtype=o.dtype))
        # ally_0_visible index 32
        if 32 < obs_dim:
            features_1.append(o[:, 1, 32:33])
        else:
            features_1.append(torch.zeros(bs, 1, device=o.device, dtype=o.dtype))
        
        msg_1 = torch.cat(features_1, dim=-1)  # (bs, 4)
        messages[:, 1, :4] = msg_1
    
    if n_agents >= 3:
        # Agent 2 (roach 2): same as agent 1
        features_2 = []
        if 46 < obs_dim:
            features_2.append(o[:, 2, 46:47])
        else:
            features_2.append(torch.zeros(bs, 1, device=o.device, dtype=o.dtype))
        if 47 < obs_dim:
            features_2.append(o[:, 2, 47:48])
        else:
            features_2.append(torch.zeros(bs, 1, device=o.device, dtype=o.dtype))
        if 48 < obs_dim:
            features_2.append(o[:, 2, 48:49])
        else:
            features_2.append(torch.zeros(bs, 1, device=o.device, dtype=o.dtype))
        if 32 < obs_dim:
            features_2.append(o[:, 2, 32:33])
        else:
            features_2.append(torch.zeros(bs, 1, device=o.device, dtype=o.dtype))
        
        msg_2 = torch.cat(features_2, dim=-1)  # (bs, 4)
        messages[:, 2, :4] = msg_2
    
    return messages

def communication_matrix(o):
    """Return (batch, n_agents, n_agents) matrix = who * when, with diagonal zero."""
    who = communication_who(o)
    when = communication_when(o)
    mat = torch.clamp(who * when, 0.0, 1.0)
    
    # Ensure diagonal zero
    bs, n_agents, _ = mat.shape
    if n_agents > 0:
        idx = torch.arange(n_agents, device=o.device)
        mat[:, idx, idx] = 0.0
    
    return mat

def communication(o):
    """Concatenate original obs with per-sender messages."""
    msg = communication_what(o)
    return torch.cat([o, msg], dim=-1)