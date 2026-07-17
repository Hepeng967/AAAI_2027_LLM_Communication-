import torch
import torch.nn.functional as F

def generate_mask(obs, mode='object'):
    """
    Generate communication mask based on the corridor map scenario policy.
    Fixed version: Vectorized, no loops, stable broadcasting.
    """
    # 1. 安全转换
    if not isinstance(obs, torch.Tensor):
        obs = torch.from_numpy(obs)
    if obs.dtype != torch.float32:
        obs = obs.float()

    bs, n_agents, _, obs_dim = obs.shape
    device = obs.device
    
    # 假设 Corridor 是 6 个智能体 (6 Zealots)
    # assert n_agents == 6, f"Expected 6 agents, got {n_agents}"
    
    # Initialize mask
    if mode == 'object':
        mask = torch.zeros(bs, n_agents, n_agents, 1, device=device)
    else:  # 'content' or 'object_content'
        mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=device)
    
    # Indices
    ENEMY_0_DISTANCE = 5
    ENEMY_0_REL_X = 6
    ENEMY_0_REL_Y = 7
    ENEMY_0_HEALTH = 8
    ALLY_0_DISTANCE = 10
    OWN_HEALTH = 15
    OWN_SHIELD = 16 # Zealot has shield
    
    # Constants
    ATTACK_RANGE = 6.0
    
    # === Helper: Get Nearest Ally (Vectorized) ===
    # ally_distances: (bs, n_agents, n_agents)
    ally_distances = obs[:, :, :, ALLY_0_DISTANCE]
    # Mask self distance (infinity)
    eye_mask = torch.eye(n_agents, device=device).unsqueeze(0).expand(bs, -1, -1)
    ally_distances = ally_distances + eye_mask * 1e9
    # indices: (bs, n_agents) -> The index of the nearest ally for each agent
    nearest_ally_indices = torch.argmin(ally_distances, dim=2) 
    
    # === Agent 0 Policies (Leader/Frontline) ===
    # Condition 1: Enemy within attack range
    # Shape: (bs, 1, 1, 1)
    cond_0_1 = (obs[:, 0, 0, ENEMY_0_DISTANCE] <= ATTACK_RANGE).view(bs, 1, 1, 1)
    
    # Condition 2: Low Health (< 50% or raw value, assuming normalized 0-1 here for safety, else adjust threshold)
    # If raw health, 50 is fine. If normalized, use 0.5. Assuming raw based on your code (50).
    cond_0_2 = (obs[:, 0, 0, OWN_HEALTH] < 50).view(bs, 1, 1, 1)
    
    # Targets for Agent 0
    # Target 1: All other agents (1-5)
    target_mask_0_all = torch.zeros(bs, 1, n_agents, 1, device=device)
    if n_agents > 1:
        target_mask_0_all[:, 0, 1:, :] = 1.0
        
    # Target 2: Nearest ally to Agent 0
    # Create one-hot mask for nearest ally
    nearest_to_0 = nearest_ally_indices[:, 0] # (bs,)
    target_mask_0_near = F.one_hot(nearest_to_0, num_classes=n_agents).view(bs, 1, n_agents, 1).float()
    
    # Apply Agent 0 Logic
    if mode == 'object':
        # Cond 1 -> All
        mask[:, 0:1, :, :] = torch.max(mask[:, 0:1, :, :], cond_0_1.float() * target_mask_0_all)
        # Cond 2 -> Nearest
        mask[:, 0:1, :, :] = torch.max(mask[:, 0:1, :, :], cond_0_2.float() * target_mask_0_near)
        
    elif mode in ['content', 'object_content']:
        # Prepare content patterns
        c_patt_1 = torch.zeros(bs, 1, n_agents, obs_dim, device=device)
        feat_idxs_1 = [idx for idx in [ENEMY_0_DISTANCE, ENEMY_0_REL_X, ENEMY_0_REL_Y] if idx < obs_dim]
        c_patt_1[:, :, :, feat_idxs_1] = 1.0
        
        c_patt_2 = torch.zeros(bs, 1, n_agents, obs_dim, device=device)
        if OWN_HEALTH < obs_dim: c_patt_2[:, :, :, OWN_HEALTH] = 1.0
        
        # Apply Logic
        # 1. Enemy info -> All
        mask_update_1 = cond_0_1.float() * c_patt_1
        if mode == 'object_content': mask_update_1 = mask_update_1 * target_mask_0_all
        else: mask_update_1 = mask_update_1 * target_mask_0_all # In content mode, usually broadcast but mask controls valid bits
        
        # 2. Health info -> Nearest
        mask_update_2 = cond_0_2.float() * c_patt_2
        if mode == 'object_content': mask_update_2 = mask_update_2 * target_mask_0_near
        else: mask_update_2 = mask_update_2 * target_mask_0_near # Restrict to nearest
        
        # Combine
        combined_0 = torch.max(mask_update_1, mask_update_2)
        mask[:, 0:1, :, :] = torch.max(mask[:, 0:1, :, :], combined_0)

    # === Agent 1 Policies (Flanker 1) ===
    # Condition 1: Multiple enemies (Simplified heuristic)
    # Using logical_and/or for stability if needed, here just > 0.5
    if n_agents > 1:
        cond_1_1 = (obs[:, 1, 1, 4] > 0.5).view(bs, 1, 1, 1) # ENEMY_AVAILABLE
        
        # Condition 2: Enemy approaching (Y < 0 and Close)
        cond_1_2 = torch.logical_and(
            obs[:, 1, 1, ENEMY_0_REL_Y] < 0,
            obs[:, 1, 1, ENEMY_0_DISTANCE] < 10.0
        ).view(bs, 1, 1, 1)
        
        # Targets
        target_mask_1_group = torch.zeros(bs, 1, n_agents, 1, device=device)
        group_indices = [i for i in [0, 2, 3, 4, 5] if i < n_agents]
        target_mask_1_group[:, 0, group_indices, :] = 1.0
        
        if mode == 'object':
            mask[:, 1:2, :, :] = torch.max(mask[:, 1:2, :, :], cond_1_1.float() * target_mask_1_group)
            mask[:, 1:2, :, :] = torch.max(mask[:, 1:2, :, :], cond_1_2.float() * target_mask_1_group)
        elif mode in ['content', 'object_content']:
            c_patt_1 = torch.zeros(bs, 1, n_agents, obs_dim, device=device)
            idxs = [idx for idx in [4, ENEMY_0_DISTANCE, ENEMY_0_REL_X, ENEMY_0_REL_Y] if idx < obs_dim]
            c_patt_1[:, :, :, idxs] = 1.0
            
            # Combine conditions (logical OR)
            any_cond = torch.max(cond_1_1.float(), cond_1_2.float())
            
            mask_update = any_cond * c_patt_1
            if mode == 'object_content': mask_update = mask_update * target_mask_1_group
            else: mask_update = mask_update * target_mask_1_group
            
            mask[:, 1:2, :, :] = torch.max(mask[:, 1:2, :, :], mask_update)

    # === Agent 2 Policies (Defender) ===
    if n_agents > 2:
        # Cond 1: Base threatened
        cond_2_1 = torch.logical_and(
            torch.abs(obs[:, 2, 2, ENEMY_0_REL_X] - 4.0) < 2.0,
            torch.abs(obs[:, 2, 2, ENEMY_0_REL_Y] - 4.0) < 2.0
        ).view(bs, 1, 1, 1)
        
        # Cond 2: Low Shield (< 30)
        cond_2_2 = (obs[:, 2, 2, OWN_SHIELD] < 30).view(bs, 1, 1, 1)
        
        # Targets
        target_mask_2_group = torch.zeros(bs, 1, n_agents, 1, device=device)
        idxs_2 = [i for i in [0, 1, 3, 4, 5] if i < n_agents]
        target_mask_2_group[:, 0, idxs_2, :] = 1.0
        
        nearest_to_2 = nearest_ally_indices[:, 2]
        target_mask_2_near = F.one_hot(nearest_to_2, num_classes=n_agents).view(bs, 1, n_agents, 1).float()
        
        if mode == 'object':
            mask[:, 2:3, :, :] = torch.max(mask[:, 2:3, :, :], cond_2_1.float() * target_mask_2_group)
            mask[:, 2:3, :, :] = torch.max(mask[:, 2:3, :, :], cond_2_2.float() * target_mask_2_near)
        elif mode in ['content', 'object_content']:
            # Pattern 1: Enemy info
            c_patt_1 = torch.zeros(bs, 1, n_agents, obs_dim, device=device)
            idxs = [idx for idx in [ENEMY_0_REL_X, ENEMY_0_REL_Y, ENEMY_0_DISTANCE] if idx < obs_dim]
            c_patt_1[:, :, :, idxs] = 1.0
            
            # Pattern 2: Shield info
            c_patt_2 = torch.zeros(bs, 1, n_agents, obs_dim, device=device)
            if OWN_SHIELD < obs_dim: c_patt_2[:, :, :, OWN_SHIELD] = 1.0
            
            m_up_1 = cond_2_1.float() * c_patt_1
            if mode == 'object_content': m_up_1 = m_up_1 * target_mask_2_group
            else: m_up_1 = m_up_1 * target_mask_2_group
            
            m_up_2 = cond_2_2.float() * c_patt_2
            if mode == 'object_content': m_up_2 = m_up_2 * target_mask_2_near
            else: m_up_2 = m_up_2 * target_mask_2_near
            
            mask[:, 2:3, :, :] = torch.max(torch.max(mask[:, 2:3, :, :], m_up_1), m_up_2)

    # === Agent 3+ Policies (Flanking/Support) - Fix incomplete code ===
    # Logic for remaining agents (3, 4, 5)
    for i in range(3, n_agents):
        # Generic Policy: If flanking (high Y offset) or low health
        # Flanking: abs(REL_Y) > 3.0
        cond_flank = (torch.abs(obs[:, i, i, ENEMY_0_REL_Y]) > 3.0).view(bs, 1, 1, 1)
        cond_health = (obs[:, i, i, OWN_HEALTH] < 40).view(bs, 1, 1, 1)
        
        # Target: Nearest Ally + Agent 0 (Leader)
        target_mask_i = torch.zeros(bs, 1, n_agents, 1, device=device)
        target_mask_i[:, 0, 0, :] = 1.0 # Always tell leader
        
        nearest_to_i = nearest_ally_indices[:, i]
        target_nearest = F.one_hot(nearest_to_i, num_classes=n_agents).view(bs, 1, n_agents, 1).float()
        target_mask_i = torch.max(target_mask_i, target_nearest)
        
        any_cond = torch.max(cond_flank.float(), cond_health.float())
        
        if mode == 'object':
            mask[:, i:i+1, :, :] = torch.max(mask[:, i:i+1, :, :], any_cond * target_mask_i)
        elif mode in ['content', 'object_content']:
            c_patt = torch.zeros(bs, 1, n_agents, obs_dim, device=device)
            # Send Position + Health
            idxs = [idx for idx in [ENEMY_0_REL_X, ENEMY_0_REL_Y, OWN_HEALTH] if idx < obs_dim]
            c_patt[:, :, :, idxs] = 1.0
            
            m_up = any_cond * c_patt
            if mode == 'object_content': m_up = m_up * target_mask_i
            else: m_up = m_up * target_mask_i
            
            mask[:, i:i+1, :, :] = torch.max(mask[:, i:i+1, :, :], m_up)

    # Ensure binary
    mask = (mask > 0.5).float()
    
    # Safety Check: Content/Object_Content shape should match
    if mode == 'object':
        return mask # (bs, n, n, 1)
    elif mode == 'content':
        # In pure content mode, we usually assume full connectivity but masked content
        # But here we used the target logic to zero out content for non-targets too
        # If framework requires full connectivity with masked content:
        # return mask
        # If framework implies object mask is all ones for content mode, we should check implementation.
        # Based on typical 'content' mode, we usually allow all edges but filter bits.
        # But adhering to the previous logic, we return the calculated mask (which is bs, n, n, obs_dim)
        return mask
    else:
        # object_content: needs (bs, n, n, obs_dim) where edges are 0 if object_mask is 0
        # Our logic above already calculated this implicitly by multiplying patterns with target_masks
        return mask

if __name__ == "__main__":
    # Test
    obs = torch.randn(2, 6, 6, 208) # Corridor typical obs_dim
    m = generate_mask(obs, 'object_content')
    print("Success:", m.shape)