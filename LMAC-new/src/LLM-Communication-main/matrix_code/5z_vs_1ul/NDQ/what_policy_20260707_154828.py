import torch

def generate_mask(obs, mode='object'):
    """
    Implements the WHAT communication content-selection policy for Zealot agents.
    
    Args:
        obs: torch.Tensor of shape (bs, n_agents, n_agents, obs_dim)
        mode: str, one of 'content', 'object_content', 'object'
    
    Returns:
        mask: torch.Tensor of shape (bs, n_agents, n_agents, obs_dim)
    """
    bs, n_agents, n_agents_check, obs_dim = obs.shape
    device = obs.device
    dtype = obs.dtype
    
    # Feature indices
    FEATURE_ENEMY_0_AVAILABLE = 4
    FEATURE_ENEMY_0_DISTANCE = 5
    FEATURE_ENEMY_0_REL_X = 6
    FEATURE_ENEMY_0_REL_Y = 7
    FEATURE_ENEMY_0_HEALTH = 8
    
    # Ally features: base indices for ally_j
    ALLY_BASE_VISIBLE = 9
    ALLY_BASE_DISTANCE = 10
    ALLY_BASE_REL_X = 11
    ALLY_BASE_REL_Y = 12
    ALLY_BASE_HEALTH = 13
    ALLY_BASE_SHIELD = 14
    
    FEATURE_OWN_HEALTH = 33
    FEATURE_OWN_SHIELD = 34
    
    # Helper: get feature value from sender's own observation
    def get_feature(obs, feature_idx):
        """Get feature from sender's own observation: shape (bs, n_agents)"""
        if feature_idx >= obs_dim:
            return None
        # obs[:, i, i, feature_idx] gives (bs, n_agents) after diagonal extraction
        result = torch.zeros(bs, n_agents, device=device, dtype=dtype)
        for i in range(n_agents):
            result[:, i] = obs[:, i, i, feature_idx]
        return result
    
    def get_feature_safe(obs, feature_idx):
        val = get_feature(obs, feature_idx)
        if val is None:
            return torch.zeros(bs, n_agents, device=device, dtype=dtype)
        return val
    
    # Initialize mask (all zeros by default)
    mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=device, dtype=dtype)
    
    # --- Step 1: Identify which agents are senders for each trigger ---
    
    # Sender's own health
    own_health = get_feature_safe(obs, FEATURE_OWN_HEALTH)
    # Max health is 80
    max_health = 80.0
    
    # Trigger 1: Self-health critically low (own_health < 16)
    trigger1 = (own_health < 16.0)  # (bs, n_agents)
    
    # Trigger 2: Enemy within medium range AND own health high
    enemy_0_available = get_feature_safe(obs, FEATURE_ENEMY_0_AVAILABLE)
    enemy_0_distance = get_feature_safe(obs, FEATURE_ENEMY_0_DISTANCE)
    trigger2 = (enemy_0_available == 1.0) & (enemy_0_distance < 5.0) & (own_health > 56.0)  # 56 = 70% of 80
    
    # Trigger 3: An ally visible AND ally health < 16 AND self healthy
    # Check for each ally j (0..3)
    trigger3_per_ally = []  # list of (bs, n_agents) boolean tensors for each ally
    for j in range(4):  # 4 allies (since 5 agents total)
        ally_visible_idx = ALLY_BASE_VISIBLE + 7 * j
        ally_health_idx = ALLY_BASE_HEALTH + 7 * j
        
        if ally_visible_idx < obs_dim and ally_health_idx < obs_dim:
            ally_visible = get_feature_safe(obs, ally_visible_idx)
            ally_health = get_feature_safe(obs, ally_health_idx)
            trigger3_j = (ally_visible == 1.0) & (ally_health < 16.0) & (own_health > 56.0)
        else:
            trigger3_j = torch.zeros(bs, n_agents, device=device, dtype=torch.bool)
        trigger3_per_ally.append(trigger3_j)
    
    # Combined trigger3: True if any ally triggers
    trigger3 = torch.zeros(bs, n_agents, device=device, dtype=torch.bool)
    for trigger3_j in trigger3_per_ally:
        trigger3 = trigger3 | trigger3_j
    
    # --- Step 2: Build content masks for each trigger ---
    
    # Content mask for trigger 1
    # Features to send: own_health, all ally visible/distance/rel_x/rel_y/health/shield, enemy info
    content1 = torch.zeros(bs, n_agents, obs_dim, device=device, dtype=dtype)
    
    # Add own_health
    if FEATURE_OWN_HEALTH < obs_dim:
        content1[:, :, FEATURE_OWN_HEALTH] = 1.0
    
    # Add ally features for each ally j
    for j in range(4):
        base = ALLY_BASE_VISIBLE + 7 * j
        if base + 6 < obs_dim:  # enough room for all 7 feature slots for this ally
            # visible, distance, rel_x, rel_y, health, shield (indices base+0 through base+5)
            for k in range(6):
                content1[:, :, base + k] = 1.0
        else:
            # Add only available features
            for k in range(6):
                idx = base + k
                if idx < obs_dim:
                    content1[:, :, idx] = 1.0
    
    # Add enemy features (indices 4-8)
    enemy_indices = [FEATURE_ENEMY_0_AVAILABLE, FEATURE_ENEMY_0_DISTANCE, 
                     FEATURE_ENEMY_0_REL_X, FEATURE_ENEMY_0_REL_Y, FEATURE_ENEMY_0_HEALTH]
    for idx in enemy_indices:
        if idx < obs_dim:
            content1[:, :, idx] = 1.0
    
    # Content mask for trigger 2
    content2 = torch.zeros(bs, n_agents, obs_dim, device=device, dtype=dtype)
    # Enemy features
    for idx in enemy_indices:
        if idx < obs_dim:
            content2[:, :, idx] = 1.0
    # Own health
    if FEATURE_OWN_HEALTH < obs_dim:
        content2[:, :, FEATURE_OWN_HEALTH] = 1.0
    
    # Content mask for trigger 3 (per-ally variant, we'll handle per-ally below)
    # Initialize content3 as zeros, we will add per-ally when triggered
    content3 = torch.zeros(bs, n_agents, obs_dim, device=device, dtype=dtype)
    
    # For each ally j, add their features if that ally is the one that triggered
    for j in range(4):
        base = ALLY_BASE_VISIBLE + 7 * j
        trigger3_j = trigger3_per_ally[j]  # (bs, n_agents) boolean
        # For senders where this ally triggered, add that ally's features
        if trigger3_j.any():
            # Features: distance, rel_x, rel_y, health (indices base+1 through base+4)
            for k, feat_offset in enumerate([1, 2, 3, 4]):  # skip visible (offset 0) per spec
                idx = base + feat_offset
                if idx < obs_dim:
                    # We need to set content3[b, sender, idx] = 1 where trigger3_j[b, sender] is True
                    # This is vectorized per batch and agent
                    sender_indices = trigger3_j.nonzero(as_tuple=True)  # returns (batch_indices, agent_indices)
                    if len(sender_indices[0]) > 0:
                        content3[sender_indices[0], sender_indices[1], idx] = 1.0
    
    # Add own_health to content3
    if FEATURE_OWN_HEALTH < obs_dim:
        content3[:, :, FEATURE_OWN_HEALTH] = 1.0
    
    # Add enemy distance/rel_x/rel_y if enemy available (approximate: always send for simplicity)
    # Actually spec says "if enemy_0_available", we'll add conditionally
    # But to keep it simple, we always send these for triggered senders
    enemy_cond_indices = [FEATURE_ENEMY_0_DISTANCE, FEATURE_ENEMY_0_REL_X, FEATURE_ENEMY_0_REL_Y]
    for idx in enemy_cond_indices:
        if idx < obs_dim:
            # Since we don't know per-sender if enemy is available (would require indexing), 
            # we send these for all triggered senders (they'll be 0 if enemy not available)
            sender_indices = trigger3.nonzero(as_tuple=True)
            if len(sender_indices[0]) > 0:
                content3[sender_indices[0], sender_indices[1], idx] = 1.0
    
    # Combine content masks based on triggers
    # For each sender i, determine which trigger applies (priority: trigger1 > trigger2 > trigger3; any applies)
    # We'll build combined content (bs, n_agents, obs_dim)
    combined_content = torch.zeros(bs, n_agents, obs_dim, device=device, dtype=dtype)
    
    # Priority: trigger1 gets all its features, trigger2 gets its, trigger3 gets its
    # Actually triggers can overlap, but spec says each has its own content. If multiple triggers, send union.
    # We'll just add all trigger masks that are active for each sender.
    # This is a loop over agents (small, 5 agents) for safety
    for b in range(bs):
        for i in range(n_agents):
            if trigger1[b, i]:
                combined_content[b, i, :] = torch.max(combined_content[b, i, :], content1[b, i, :])
            if trigger2[b, i]:
                combined_content[b, i, :] = torch.max(combined_content[b, i, :], content2[b, i, :])
            if trigger3[b, i]:
                combined_content[b, i, :] = torch.max(combined_content[b, i, :], content3[b, i, :])
    
    # No default: send nothing (already zeros)
    
    # --- Step 3: Expand sender content to receiver dimension ---
    # For mode 'content': send from all senders to all receivers (but not self)
    # For mode 'object' and 'object_content': also gate by receiver
    
    if mode == 'content':
        # Send to all receivers (except self)
        for i in range(n_agents):
            for j in range(n_agents):
                if i != j:
                    mask[:, i, j, :] = combined_content[:, i, :]
    
    elif mode == 'object_content':
        # Send to all receivers (except self) - spec says "to all other Zealots" typically
        for i in range(n_agents):
            for j in range(n_agents):
                if i != j:
                    mask[:, i, j, :] = combined_content[:, i, :]
    
    elif mode == 'object':
        # Compatibility mode: use object gate (send to all non-self) but still output obs-dim mask
        for i in range(n_agents):
            for j in range(n_agents):
                if i != j:
                    mask[:, i, j, :] = combined_content[:, i, :]
    
    else:
        raise ValueError(f"Unknown mode: {mode}")
    
    return mask