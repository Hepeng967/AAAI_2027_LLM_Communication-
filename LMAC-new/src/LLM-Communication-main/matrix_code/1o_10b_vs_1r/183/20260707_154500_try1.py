import torch

def generate_mask(obs, mode='object'):
    """
    Implements WHAT communication policy for 11-agent StarCraft II scenario.
    Agent 10 is Overseer, agents 0-9 are Banelings.
    Returns feature mask of shape (bs, n_agents, n_agents, obs_dim).
    """
    bs, n_agents, n_agents_check, obs_dim = obs.shape
    assert n_agents == n_agents_check == 11, f"Expected 11 agents, got {n_agents}"
    device = obs.device
    dtype = obs.dtype
    
    # Initialize full mask to zeros
    mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=device, dtype=dtype)
    
    # Feature indices (0-indexed)
    FEAT_MOVE_NORTH = 0
    FEAT_MOVE_SOUTH = 1
    FEAT_MOVE_EAST = 2
    FEAT_MOVE_WEST = 3
    FEAT_ENEMY_AVAIL = 4
    FEAT_ENEMY_DIST = 5
    FEAT_ENEMY_REL_X = 6
    FEAT_ENEMY_REL_Y = 7
    FEAT_ENEMY_HEALTH = 8
    # FEAT_ENEMY_TYPE_0 = 9
    # FEAT_ENEMY_TYPE_1 = 10
    
    # Ally features: each ally i (i=0..9) occupies 7 indices from 11+7*i to 11+7*i+6
    ALLY_BASE = 11
    ALLY_STRIDE = 7
    ALLY_OFFSET_VISIBLE = 0
    ALLY_OFFSET_DIST = 1
    ALLY_OFFSET_REL_X = 2
    ALLY_OFFSET_REL_Y = 3
    ALLY_OFFSET_HEALTH = 4
    # ALLY_OFFSET_TYPE_0 = 5
    # ALLY_OFFSET_TYPE_1 = 6
    
    # Own features (indices 81,82,83)
    FEAT_OWN_HEALTH = 81
    # FEAT_OWN_TYPE_0 = 82
    # FEAT_OWN_TYPE_1 = 83
    
    # ---- HELPER: get sender obs for a specific feature index ----
    def _sender_obs(sender_idx, feat_idx):
        """Return tensor (bs,) of feature value for sender idx."""
        return obs[:, sender_idx, sender_idx, feat_idx]
    
    # ===================== OVERSEER POLICY (agent 10) =====================
    # Sender is agent 10 (index 10 in 0-indexed)
    OVERSEER_ID = 10
    
    # Get enemy available for Overseer
    enemy_avail_overseer = obs[:, OVERSEER_ID, OVERSEER_ID, FEAT_ENEMY_AVAIL]  # (bs,)
    
    # Case 1: enemy_0_available == 1 -> send enemy location/health
    case1_cond = (enemy_avail_overseer > 0.5).float()  # (bs,)
    
    # Features to send when enemy available
    enemy_feat_indices = [FEAT_ENEMY_DIST, FEAT_ENEMY_REL_X, FEAT_ENEMY_REL_Y, FEAT_ENEMY_HEALTH]
    
    # Build feature mask for these indices
    # For each feature index, set mask[bs, OVERSEER_ID, all_receivers, feat_idx] = case1_cond
    # case1_cond shape: (bs,) -> need to expand to (bs, n_agents)
    case1_cond_exp = case1_cond.view(bs, 1).expand(bs, n_agents)  # (bs, n_agents)
    
    for feat_idx in enemy_feat_indices:
        if feat_idx < obs_dim:
            # We assign for all receivers j (0..10) except self (handled later)
            mask[:, OVERSEER_ID, :, feat_idx] = case1_cond_exp.clone()
    
    # Case 2: enemy_0_available == 0 -> send enemy_available (0) as signal
    case2_cond = (enemy_avail_overseer < 0.5).float()  # (bs,)
    case2_cond_exp = case2_cond.view(bs, 1).expand(bs, n_agents)  # (bs, n_agents)
    
    if FEAT_ENEMY_AVAIL < obs_dim:
        mask[:, OVERSEER_ID, :, FEAT_ENEMY_AVAIL] = case2_cond_exp.clone()
    
    # ===================== BANELING POLICY (agents 0-9) =====================
    for sender_id in range(10):  # agents 0..9
        # ---- Rule 1: visible nearby ally ----
        # Check each potential ally (0..9) except self
        for ally_idx in range(10):
            if ally_idx == sender_id:
                continue
            
            # Feature indices for this ally
            ally_visible_idx = ALLY_BASE + ally_idx * ALLY_STRIDE + ALLY_OFFSET_VISIBLE
            ally_dist_idx = ALLY_BASE + ally_idx * ALLY_STRIDE + ALLY_OFFSET_DIST
            ally_rel_x_idx = ALLY_BASE + ally_idx * ALLY_STRIDE + ALLY_OFFSET_REL_X
            ally_rel_y_idx = ALLY_BASE + ally_idx * ALLY_STRIDE + ALLY_OFFSET_REL_Y
            ally_health_idx = ALLY_BASE + ally_idx * ALLY_STRIDE + ALLY_OFFSET_HEALTH
            
            # Check if indices are within obs_dim
            if ally_visible_idx >= obs_dim or ally_dist_idx >= obs_dim:
                continue  # skip if feature out of range
            
            # Get sender's observation of this ally
            ally_visible = obs[:, sender_id, sender_id, ally_visible_idx]  # (bs,)
            ally_dist = obs[:, sender_id, sender_id, ally_dist_idx]  # (bs,)
            
            # Condition: visible AND distance < 10.0
            cond = ((ally_visible > 0.5) & (ally_dist < 10.0)).float()  # (bs,)
            cond_exp = cond.view(bs, 1).expand(bs, n_agents)  # (bs, n_agents)
            
            # Send ally distance, rel_x, rel_y, health
            ally_feat_indices = [ally_dist_idx, ally_rel_x_idx, ally_rel_y_idx, ally_health_idx]
            for feat_idx in ally_feat_indices:
                if feat_idx < obs_dim:
                    mask[:, sender_id, :, feat_idx] = cond_exp.clone()
        
        # ---- Rule 2: own health < 30 ----
        if FEAT_OWN_HEALTH < obs_dim:
            own_health = obs[:, sender_id, sender_id, FEAT_OWN_HEALTH]  # (bs,)
            cond_own = (own_health < 30.0).float()  # (bs,)
            cond_own_exp = cond_own.view(bs, 1).expand(bs, n_agents)  # (bs, n_agents)
            
            mask[:, sender_id, :, FEAT_OWN_HEALTH] = cond_own_exp.clone()
    
    # ===================== NO SELF-COMMUNICATION =====================
    # Set all self-communication masks to 0
    for i in range(n_agents):
        mask[:, i, i, :] = torch.zeros(bs, obs_dim, device=device, dtype=dtype)
    
    # ===================== MODE TRANSFORMATIONS =====================
    if mode == 'object_content':
        # Already in correct format: (bs, n_agents, n_agents, obs_dim)
        return mask
    
    elif mode == 'content':
        # In content mode, we ignore any receiver gating and just return the feature mask
        # Actually the mask already handles content selection per sender-receiver pair.
        # But the policy says for Baneling rule 1: "send to nearby banelings"
        # For simplicity, we keep all receivers (including non-relevant ones) as per instructions:
        # "This mode should express the WHAT policy even if all non-self receivers are allowed."
        return mask
    
    elif mode == 'object':
        # Compatibility mode: return object gate expanded over feature dimensions.
        # Compute object gate: any feature sent? i.e., mask.sum(-1) > 0 -> (bs, n_agents, n_agents)
        # Then expand to obs_dim.
        object_gate = (mask.sum(dim=-1) > 0).float()  # (bs, n_agents, n_agents)
        # Expand to obs_dim: (bs, n_agents, n_agents, 1) -> (bs, n_agents, n_agents, obs_dim)
        object_gate_exp = object_gate.unsqueeze(-1).expand(bs, n_agents, n_agents, obs_dim)
        return object_gate_exp.clone()
    
    else:
        raise ValueError(f"Unknown mode: {mode}")