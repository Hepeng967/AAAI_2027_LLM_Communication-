import torch

def generate_mask(obs, mode='object'):
    """
    Implements the WHAT communication policy for a StarCraft II micro scenario.
    For details on the policy see the docstring.
    
    Args:
        obs: torch.Tensor of shape (bs, n_agents, n_agents, obs_dim)
        mode: str, one of 'content', 'object_content', 'object'
    
    Returns:
        mask: torch.Tensor of shape (bs, n_agents, n_agents, obs_dim)
    """
    bs, n_agents, n_agents_check, obs_dim = obs.shape
    assert n_agents_check == n_agents, "Expected square agent dimension"
    device = obs.device
    dtype = obs.dtype
    
    # Initialize output mask with zeros
    mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=device, dtype=dtype)
    
    # Feature indices (0-indexed)
    # enemy_0: 4-10 (available at 4, distance 5, rel_x 6, rel_y 7, health 8, type_0 9, type_1 10)
    # enemy_1: 11-17 (available at 11, distance 12, rel_x 13, rel_y 14, health 15, type_0 16, type_1 17)
    # enemy_2: 18-24 (available at 18, distance 19, rel_x 20, rel_y 21, health 22, type_0 23, type_1 24)
    # enemy_3: 25-31 (available at 25, distance 26, rel_x 27, rel_y 28, health 29, type_0 30, type_1 31)
    # ally_0: 32-38 (visible 32, distance 33, rel_x 34, rel_y 35, health 36, type_0 37, type_1 38)
    # ally_1: 39-45 (visible 39, distance 40, rel_x 41, rel_y 42, health 43, type_0 44, type_1 45)
    # own_health: 46
    # own_type: 47-48
    
    enemy_features = [
        (4, 5, 6, 7, 8, 9, 10),   # enemy_0: available, distance, rel_x, rel_y, health, type_0, type_1
        (11, 12, 13, 14, 15, 16, 17), # enemy_1
        (18, 19, 20, 21, 22, 23, 24), # enemy_2
        (25, 26, 27, 28, 29, 30, 31)  # enemy_3
    ]
    # Indices for each enemy: [avail, dist, rel_x, rel_y, health, type_0, type_1]
    
    # Helper to check if an index is within obs_dim
    def valid(idx):
        return idx < obs_dim
    
    # Filter feature lists to only valid indices
    enemy_feature_indices = []
    for en_feats in enemy_features:
        valid_feats = [f for f in en_feats if valid(f)]
        enemy_feature_indices.append(valid_feats)
    
    # Sender's own obs is at obs[:, i, i, :]
    own_obs = torch.stack([obs[:, i, i, :] for i in range(n_agents)], dim=1)  # (bs, n_agents, obs_dim)
    
    # ---- Helper to create a mask for specific feature indices ----
    def feature_mask_from_indices(indices_list):
        """
        Create a mask of shape (bs, n_agents, n_agents, obs_dim) where for each agent i,
        if indices_list[i] is non-empty, mask[:, i, :, indices] = 1.
        Otherwise, all zeros for that sender.
        """
        fmask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=device, dtype=dtype)
        for i in range(n_agents):
            if not indices_list[i]:
                continue
            # Set all receivers for sender i to have these feature indices active
            # Shape: (bs, 1, obs_dim) for sender i -> expand to (bs, n_agents, obs_dim)
            sender_mask = torch.zeros(bs, 1, obs_dim, device=device, dtype=dtype)
            for idx in indices_list[i]:
                sender_mask[:, 0, idx] = 1.0
            # Expand to (bs, n_agents, obs_dim) for receiver dimension
            sender_mask_exp = sender_mask.expand(bs, n_agents, obs_dim)
            # Assign to all receivers: fmask[:, i, :, :] = sender_mask_exp
            fmask[:, i, :, :] = sender_mask_exp
        return fmask
    
    # ---- Compute per-sender content selection ----
    # We'll compute for each sender i a list of feature indices to send (or None)
    sender_features = [[] for _ in range(n_agents)]  # list of list of indices
    
    # Agent 0: Overseer
    if n_agents >= 1:
        i = 0  # sender index for Overseer
        own = own_obs[:, i, :]  # (bs, obs_dim)
        
        # Rule 1: any enemy available
        for en_idx, en_feats in enumerate(enemy_feature_indices):
            # en_feats[0] is available index if within obs_dim
            if not en_feats:
                continue
            avail_idx = en_feats[0]  # available feature
            # Check if available == 1
            avail = own[:, avail_idx]  # (bs,)
            # Condition: avail >= 0.5 (binary)
            cond = (avail >= 0.5).float()  # (bs,)
            # If trigger, add the remaining features (distance, rel_x, rel_y, health, type_0, type_1)
            if len(en_feats) > 1:
                # Add all features except available (index 0) for this enemy
                for f_idx in en_feats[1:]:
                    # We'll add conditionally later; but for simplicity, expand over batch
                    pass
        
        # Simpler approach: for each sender, compute a mask based on triggers and add to mask
        # We'll construct a per-sender feature list using triggers
        for en_idx, en_feats in enumerate(enemy_feature_indices):
            if not en_feats:
                continue
            avail_idx = en_feats[0]
            avail = own[:, avail_idx]  # (bs,)
            # For which batch elements is trigger active?
            trigger_active = (avail >= 0.5).nonzero(as_tuple=True)[0]  # indices where trigger true
            # For those batch elements, we want to send the enemy features (if any)
            if len(en_feats) > 1:
                for f_idx in en_feats[1:]:
                    # Add f_idx to sender_features[i] for the specific batch indices
                    # But sender_features is per-agent, not per-batch. We'll handle batch in mask construction.
                    pass
        
        # Given complexity, let's directly fill mask using torch operations
        # We'll create a (bs, 1, obs_dim) mask for this sender and expand
    
    # Better approach: construct mask iterating over agents and using broadcasting for batch.
    # We'll create a mask of shape (bs, n_agents, obs_dim) for per-sender features, then expand to receivers.
    
    per_sender_mask = torch.zeros(bs, n_agents, obs_dim, device=device, dtype=dtype)
    
    # Agent 0: Overseer
    if n_agents >= 1:
        i = 0
        own = own_obs[:, i, :]  # (bs, obs_dim)
        
        # Rule 1: any enemy available -> send that enemy's features
        for en_idx, en_feats in enumerate(enemy_feature_indices):
            if not en_feats:
                continue
            avail_idx = en_feats[0]
            if not valid(avail_idx):
                continue
            avail = own[:, avail_idx]  # (bs,)
            trigger = (avail >= 0.5).float()  # (bs,)
            # Broadcast trigger to feature dimensions
            if len(en_feats) > 1:
                # For each feature index in en_feats[1:], add trigger * 1.0 to per_sender_mask[:, i, idx]
                for f_idx in en_feats[1:]:
                    if valid(f_idx):
                        per_sender_mask[:, i, f_idx] += trigger
        
        # Rule 2: own_health < 0.3 * max_health
        # max_health is not directly in obs, but we can infer from own_type? 
        # For simplicity, assume max_health is known constant: e.g., 150 for Overseer? 
        # But we'll use a typical value: assume health is normalized [0,1]? 
        # The policy says "own_health < 0.3 * max_health". We'll approximate: use 0.3 as threshold if health is normalized.
        # Actually, health could be raw value. We'll use a reasonable heuristic: if health < 0.3, or if max_health not known, use own_health < 0.3.
        own_health_idx = 46
        if valid(own_health_idx):
            own_health = own[:, own_health_idx]  # (bs,)
            # Assume max_health = 1.0 if normalized, or use a fixed value.
            # We'll assume health is scaled to [0,1] or use a threshold of 0.3 
            trigger2 = (own_health < 0.3).float()  # (bs,)
            per_sender_mask[:, i, own_health_idx] += trigger2
    
    # Agent 1 and 2: Roaches
    for i in [1, 2]:
        if i >= n_agents:
            break
        own = own_obs[:, i, :]  # (bs, obs_dim)
        
        # Rule 1: ally_0_visible == 1 AND ally_0_distance > 0.8 * max_visibility_range
        # ally_0 is the other Roach: for i=1, ally_0 is agent 0? Wait: ally_0 is the first ally in observation.
        # In a 3-agent scenario, agent 0 is Overseer, agents 1,2 are Roaches.
        # For a Roach (i=1 or 2), its ally_0 could be the other Roach? Actually, ally_0 is the first ally.
        # Since there are 3 agents, each has two allies: for agent 1, ally_0 is agent 0 (Overseer), ally_1 is agent 2.
        # For agent 2, ally_0 is agent 0, ally_1 is agent 1.
        # So ally_0 is always the Overseer? That's not correct; the policy mentions "the other Roach".
        # We need to find which ally index corresponds to the other Roach.
        # Since Roach IDs are 1 and 2, for agent 1, the other Roach is ally_1 (index 1 in ally list).
        # For agent 2, the other Roach is ally_0 (index 0 in ally list).
        # We'll handle this by checking both allies.
        
        # For simplicity, we'll check ally_0 and ally_1 for visible and distance > threshold.
        visible_indices = [32, 39]  # ally_0_visible, ally_1_visible
        distance_indices = [33, 40] # ally_0_distance, ally_1_distance
        rel_indices = [(34,35), (41,42)]  # rel_x, rel_y pairs
        
        # We need to decide which ally is the other Roach. We'll check based on own_type? Not available.
        # Alternative: Use the fact that for Roach i, ally_0 is always the Overseer (agent 0) because agent order is 0,1,2.
        # So for Roach 1 (i=1), its own_obs has ally_0 = agent 0, ally_1 = agent 2.
        # For Roach 2 (i=2), ally_0 = agent 0, ally_1 = agent 1.
        # So the other Roach is ally_1 for agent 1, and ally_0 for agent 2? Wait:
        # Observation: for agent i, allies are in order of agent index: first ally is agent 0 if i!=0, then agent 1 if i!=1, etc.
        # For 3 agents, for agent 1: allies are [agent0, agent2]; for agent2: allies are [agent0, agent1].
        # So other Roach is ally_1 for agent1, and ally_1 for agent2? Let's check:
        # agent1 (Roach) observes: ally_0 = agent0 (Overseer), ally_1 = agent2 (Roach). So other Roach is ally_1.
        # agent2 (Roach) observes: ally_0 = agent0 (Overseer), ally_1 = agent1 (Roach). So other Roach is ally_1 as well.
        # Wait: For agent2, ally_0 = agent0, ally_1 = agent1. So ally_1 is the other Roach.
        # Thus for both Roaches, the other Roach is ally_1 (index 1 in ally list). 
        # So we use ally_1 visible (index 39) and distance (40), rel_x (41), rel_y (42).
        
        other_roach_visible_idx = 39
        other_roach_dist_idx = 40
        other_roach_rel_x_idx = 41
        other_roach_rel_y_idx = 42
        
        if valid(other_roach_visible_idx) and valid(other_roach_dist_idx):
            visible = own[:, other_roach_visible_idx]  # (bs,)
            distance = own[:, other_roach_dist_idx]     # (bs,)
            # Assume max_visibility_range might be known constant, e.g., 10.0.
            # Or we can use a fixed threshold like 0.8 * 10 = 8.0.
            # Since we don't know, we'll use distance > 8.0 as heuristic for "far away".
            # Better: use a general threshold that makes sense: distance > 5.0 maybe.
            # We'll define threshold = 5.0 (since map units are unknown).
            threshold = 5.0
            trigger = ((visible >= 0.5) & (distance > threshold)).float()  # (bs,)
            
            # If trigger, send own_health (46) and ally_1 distance, rel_x, rel_y
            if valid(46):
                per_sender_mask[:, i, 46] += trigger
            if valid(other_roach_dist_idx):
                per_sender_mask[:, i, other_roach_dist_idx] += trigger
            if valid(other_roach_rel_x_idx):
                per_sender_mask[:, i, other_roach_rel_x_idx] += trigger
            if valid(other_roach_rel_y_idx):
                per_sender_mask[:, i, other_roach_rel_y_idx] += trigger
        
        # Rule 2: enemy_0_available == 1 AND enemy_0_distance < 2.0
        enemy_avail_idx = 4
        enemy_dist_idx = 5
        if valid(enemy_avail_idx) and valid(enemy_dist_idx):
            enemy_avail = own[:, enemy_avail_idx]  # (bs,)
            enemy_dist = own[:, enemy_dist_idx]    # (bs,)
            trigger2 = ((enemy_avail >= 0.5) & (enemy_dist < 2.0)).float()  # (bs,)
            # Send enemy_0 features: distance, rel_x, rel_y, health, type_0, type_1
            enemy_feats_0 = [5, 6, 7, 8, 9, 10]  # indices for enemy_0
            for f_idx in enemy_feats_0:
                if valid(f_idx):
                    per_sender_mask[:, i, f_idx] += trigger2
    
    # Now per_sender_mask has shape (bs, n_agents, obs_dim) with binary values (0/1)
    # Clip to 0/1 to avoid double counting
    per_sender_mask = torch.clamp(per_sender_mask, 0, 1)
    
    # For content mode: expand over receivers
    if mode == 'content':
        # Expand per_sender_mask from (bs, n_agents, obs_dim) to (bs, n_agents, n_agents, obs_dim)
        # by adding receiver dimension
        mask = per_sender_mask.unsqueeze(2).expand(bs, n_agents, n_agents, obs_dim)
        # Remove self-communication
        for i in range(n_agents):
            mask[:, i, i, :] = 0
        return mask
    
    # For object and object_content modes: we need receiver gating.
    # If mode is 'object' or 'object_content', we apply WHO gating on top of content.
    # Since policy specifies optional receiver contexts, we implement simple WHO mask based on content:
    # For Overseer, send only to Roaches (1,2). For Roaches, send to other Roach only (agent1->2, agent2->1).
    # We'll create a WHO mask of shape (bs, n_agents, n_agents, 1) and multiply with content.
    
    who_mask = torch.zeros(bs, n_agents, n_agents, 1, device=device, dtype=dtype)
    
    # Agent 0 -> agents 1,2
    if n_agents >= 3:
        who_mask[:, 0, 1, :] = 1.0
        who_mask[:, 0, 2, :] = 1.0
    
    # Agent 1 -> agent 2 only
    if n_agents >= 2:
        who_mask[:, 1, 0, :] = 0.0  # Roach1 does not send to Overseer? Policy says Roaches send to other Roach.
        who_mask[:, 1, 2, :] = 1.0  # Actually policy says "the other Roach", so Roach1 sends to Roach2.
    
    # Agent 2 -> agent 1 only
    if n_agents >= 3:
        who_mask[:, 2, 1, :] = 1.0
        who_mask[:, 2, 0, :] = 0.0
    
    # Self communication is already zero from who_mask (since we didn't set diagonal)
    # But ensure self is 0
    for i in range(n_agents):
        who_mask[:, i, i, :] = 0.0
    
    # Now combine: content mask * who_mask expanded over obs_dim
    # per_sender_mask has (bs, n_agents, obs_dim)
    # who_mask has (bs, n_agents, n_agents, 1)
    # We need to expand per_sender_mask to (bs, n_agents, n_agents, obs_dim) and multiply
    content_expanded = per_sender_mask.unsqueeze(2).expand(bs, n_agents, n_agents, obs_dim)  # (bs, n, n, obs_dim)
    who_expanded = who_mask.expand(bs, n_agents, n_agents, obs_dim)  # (bs, n, n, obs_dim)
    
    mask = content_expanded * who_expanded
    
    # If mode is 'object', we pretend we only have object (who) gating and expand content? 
    # Actually mode='object' is compatibility: we return the same as object_content but may be used as gating.
    # Our implementation already resembles object_content.
    
    return mask