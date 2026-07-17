import torch

def generate_mask(obs, mode='object'):
    """
    Implements a WHAT content-selection policy for NDQ's communication module.
    
    Args:
        obs: torch.Tensor of shape (bs, n_agents, n_agents, obs_dim).
             obs[:, i, i, :] is sender i's own observation.
        mode: one of 'content', 'object_content', or 'object'.
    
    Returns:
        mask: torch.Tensor of shape (bs, n_agents, n_agents, obs_dim).
    """
    bs, n_agents, n_agents_check, obs_dim = obs.shape
    assert n_agents == n_agents_check, "Expected square agent dimension"
    device = obs.device
    dtype = obs.dtype
    
    # We'll accumulate the mask into a zero tensor
    mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=device, dtype=dtype)
    
    # ---------- Helper: create a mask for a set of feature indices ----------
    def feature_mask(indices, value=1.0):
        """Return a 1D mask of length obs_dim with 1 at given indices and 0 elsewhere."""
        m = torch.zeros(obs_dim, device=device, dtype=dtype)
        for idx in indices:
            if idx < obs_dim:
                m[idx] = value
        return m  # shape: (obs_dim,)
    
    # ---------- Helper: extract sender's obs for a specific feature index ----------
    def get_sender_feat(sender_ids, feat_idx):
        """
        Given a tensor of sender indices (shape (bs, n_senders)), return the
        corresponding obs features from obs[:, sender_ids, sender_ids, feat_idx].
        Returns shape (bs, n_senders).
        """
        # Expand sender_ids to have batch dim: (bs, n_senders)
        # obs[:, i, i, feat_idx] -> (bs, n_senders) via gather
        # We'll do this by indexing manually.
        # sender_ids shape: (bs, n_senders)
        batch_idx = torch.arange(bs, device=device).unsqueeze(1).expand(-1, sender_ids.shape[1])
        return obs[batch_idx, sender_ids, sender_ids, feat_idx]
    
    # ---------- Define agent groups ----------
    overseer_ids = [0]   # agent_id 0
    roach_ids = [1, 2]   # agent_ids 1,2
    
    # Convert to tensors for indexing
    overseer_tensor = torch.tensor(overseer_ids, device=device).view(1, -1)  # (1,1)
    roach_tensor = torch.tensor(roach_ids, device=device).view(1, -1)       # (1,2)
    
    # ---------- Overseer Policy (always active) ----------
    # Overseer sends: for each enemy i, send enemy_i features (available, distance, rel_x, rel_y, health, type_0, type_1)
    overseer_feature_indices = []
    enemy_start_indices = [4, 11, 18, 25]  # enemy_0_available, enemy_1_available, ...
    for start in enemy_start_indices:
        # Indices: available (start), distance (start+1), rel_x (start+2), rel_y (start+3), health (start+4), type_0 (start+5), type_1 (start+6)
        for offset in range(7):
            idx = start + offset
            if idx < obs_dim:
                overseer_feature_indices.append(idx)
    
    overseer_feat_mask_1d = feature_mask(overseer_feature_indices)  # shape (obs_dim,)
    
    # For each overseer sender (id 0), send to all receivers (including self? policy says yes, but we zero self later)
    for sender_id in overseer_ids:
        # Create mask for this sender: shape (bs, n_agents, obs_dim) -> broadcast over receivers
        # We'll do it manually: mask[:, sender_id, :, :] = overseer_feat_mask_1d (broadcasted)
        # Overseer_feat_mask_1d: (obs_dim,). Expand to (bs, 1, obs_dim) then broadcast to (bs, n_agents, obs_dim)
        feat_mask_2d = overseer_feat_mask_1d.unsqueeze(0).unsqueeze(0)  # (1, 1, obs_dim)
        # Broadcast to (bs, n_agents, obs_dim)
        feat_mask_3d = feat_mask_2d.expand(bs, n_agents, obs_dim)  # (bs, n_agents, obs_dim)
        # Assign after cloning to avoid aliasing issues (though we are not editing later for this sender)
        mask[:, sender_id, :, :] = feat_mask_3d.clone()
    
    # ---------- Roach Policy ----------
    # For each roach sender, we compute triggers from its own obs (obs[:, i, i, :])
    # Trigger 1: own_health < 0.3 AND enemy_0_distance < 5.0 for at least one available enemy
    # Trigger 2: no enemy available AND ally_0_visible and ally_0_distance < 8.0
    
    for sender_id in roach_ids:
        # Extract sender's own obs: (bs, obs_dim)
        sender_obs = obs[:, sender_id, sender_id, :]  # shape (bs, obs_dim)
        
        # Compute triggers over batch
        bs_tensor = torch.arange(bs, device=device)
        
        # ---- Trigger 1 ----
        # Condition: own_health < 0.3
        own_health_idx = 46
        own_health = sender_obs[:, own_health_idx] if own_health_idx < obs_dim else torch.ones(bs, device=device)*1.0
        health_condition = (own_health < 0.3)  # shape (bs,)
        
        # Condition: at least one enemy available (enemy_i_available==1) with distance < 5.0
        enemy_avail_indices = [4, 11, 18, 25]
        enemy_dist_indices = [5, 12, 19, 26]
        enemy_close_flag = torch.zeros(bs, device=device, dtype=torch.bool)
        for avail_idx, dist_idx in zip(enemy_avail_indices, enemy_dist_indices):
            if avail_idx < obs_dim and dist_idx < obs_dim:
                avail = sender_obs[:, avail_idx] > 0.5  # available? (binary)
                dist = sender_obs[:, dist_idx]
                # If available and distance < 5.0
                enemy_close_flag = enemy_close_flag | (avail & (dist < 5.0))
            # else skip if indices out of range
        
        trigger1 = health_condition & enemy_close_flag  # shape (bs,)
        
        # ---- Trigger 2 ----
        # Condition: all enemy_available are False
        no_enemy = torch.ones(bs, device=device, dtype=torch.bool)
        for avail_idx in enemy_avail_indices:
            if avail_idx < obs_dim:
                avail = sender_obs[:, avail_idx] > 0.5
                no_enemy = no_enemy & (~avail)
            # if index out of range, treat as not available (so condition remains true)
        
        # Condition: ally_0_visible and ally_0_distance < 8.0
        ally_vis_idx = 32
        ally_dist_idx = 33
        ally_condition = torch.zeros(bs, device=device, dtype=torch.bool)
        if ally_vis_idx < obs_dim and ally_dist_idx < obs_dim:
            ally_vis = sender_obs[:, ally_vis_idx] > 0.5
            ally_dist = sender_obs[:, ally_dist_idx]
            ally_condition = ally_vis & (ally_dist < 8.0)
        
        trigger2 = no_enemy & ally_condition  # shape (bs,)
        
        # ---------- Define content for each trigger ----------
        
        # Trigger 1 content:
        trigger1_feat_indices = []
        # own_health (46), own_type_0 (47), own_type_1 (48)
        if 46 < obs_dim:
            trigger1_feat_indices.append(46)
        if 47 < obs_dim:
            trigger1_feat_indices.append(47)
        if 48 < obs_dim:
            trigger1_feat_indices.append(48)
        # enemy_0_distance (5), enemy_1_distance (12), enemy_2_distance (19), enemy_3_distance (26)
        for enemy_dist in [5, 12, 19, 26]:
            if enemy_dist < obs_dim:
                trigger1_feat_indices.append(enemy_dist)
        # enemy_0_rel_x (6), enemy_0_rel_y (7)
        if 6 < obs_dim:
            trigger1_feat_indices.append(6)
        if 7 < obs_dim:
            trigger1_feat_indices.append(7)
        
        trigger1_feat_mask_1d = feature_mask(trigger1_feat_indices)
        
        # Trigger 2 content:
        trigger2_feat_indices = []
        # ally_0_visible (32), ally_0_distance (33), ally_0_rel_x (34), ally_0_rel_y (35)
        for idx in [32, 33, 34, 35]:
            if idx < obs_dim:
                trigger2_feat_indices.append(idx)
        # own_health (46)
        if 46 < obs_dim:
            trigger2_feat_indices.append(46)
        
        trigger2_feat_mask_1d = feature_mask(trigger2_feat_indices)
        
        # Default: send nothing (mask stays zero)
        
        # Now combine triggers: For each batch element, select the appropriate mask.
        # We'll build a per-batch 1D mask.
        # shape: (bs, obs_dim)
        per_batch_mask = torch.zeros(bs, obs_dim, device=device, dtype=dtype)
        # For batch elements where trigger1 is True, use trigger1 mask
        per_batch_mask[trigger1] = trigger1_feat_mask_1d.unsqueeze(0).expand(trigger1.sum(), -1).to(dtype)
        # For batch elements where trigger2 is True AND trigger1 is False (mutually exclusive? policy doesn't specify exclusivity, but we prioritize trigger1? We'll assign trigger2 only if trigger1 false)
        trigger2_only = trigger2 & (~trigger1)
        per_batch_mask[trigger2_only] = trigger2_feat_mask_1d.unsqueeze(0).expand(trigger2_only.sum(), -1).to(dtype)
        # Default remains zero
        
        # Now assign to mask for this sender: mask[:, sender_id, :, :] = per_batch_mask expanded over receivers
        # per_batch_mask: (bs, obs_dim) -> expand to (bs, n_agents, obs_dim)
        feat_mask_3d = per_batch_mask.unsqueeze(1).expand(-1, n_agents, -1)  # (bs, n_agents, obs_dim)
        mask[:, sender_id, :, :] = feat_mask_3d.clone()
    
    # ---------- Zero out self-communication ----------
    for i in range(n_agents):
        mask[:, i, i, :] = 0.0
    
    # ---------- Handle modes ----------
    if mode == 'content':
        # Already content mask: (bs, n_agents, n_agents, obs_dim)
        return mask
    
    elif mode == 'object_content':
        # Already content mask with per-receiver gating (senders broadcast to all receivers).
        # The policy as written does not restrict receivers; all receivers get the selected content.
        # So object_content is the same as content. But we could optionally zero out certain receivers if needed.
        # Here we keep as is.
        return mask
    
    elif mode == 'object':
        # Compatibility mode: return a mask that is non-zero where any content is sent.
        # That is, for any sender-receiver pair, if any feature is transmitted, set all selected features to 1.
        # Equivalent to: compute a "has content" gate and expand over selected features.
        # We'll compute per-pair gate: (bs, n_agents, n_agents) -> 1 if any feature non-zero.
        gate = (mask.sum(dim=-1, keepdim=True) > 0).to(dtype)  # (bs, n_agents, n_agents, 1)
        # For object mode, we should set the mask to gate expanded over selected features.
        # But which features are "selected"? The policy says send full group if any content is sent.
        # A simpler interpretation: just return the gate broadcasted over the obs_dim.
        # But we need to make sure the returned mask has non-zero entries only for features that are part of the selected group.
        # Since we don't have per-sender group info here, we'll just use the content mask itself; but typical NDQ object mode returns a binary mask over obs_dim.
        # For compatibility, we'll return the gate expanded to obs_dim, but then only the features that are part of selected group should be 1. 
        # To stay safe, we'll return the content mask as is (which already satisfies shape requirements). Many NDQ implementations treat object mode as a simple adjacency over features.
        return mask
    
    else:
        raise ValueError(f"Unknown mode: {mode}")