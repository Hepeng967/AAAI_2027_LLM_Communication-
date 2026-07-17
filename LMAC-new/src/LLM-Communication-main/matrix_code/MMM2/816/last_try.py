import torch

def generate_mask(obs, mode='object'):
    """
    Generate communication mask based on the specified policy.
    """
    # 1. 确保输入是 Tensor 且为 float32
    if not isinstance(obs, torch.Tensor):
        obs = torch.from_numpy(obs)
    if obs.dtype != torch.float32:
        obs = obs.float()

    bs, n_agents, _, obs_dim = obs.shape
    # assert n_agents == 8, f"Expected 8 agents, got {n_agents}"
    # assert obs_dim == 127, f"Expected 127 observation dimensions, got {obs_dim}"
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device)
    elif mode in ['content', 'object_content']:
        mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device)
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    # Extract observation features
    enemy_0_distance = obs[:, :, :, 5]  # Index 5: enemy_0_distance
    own_health = obs[:, :, :, 18]       # Index 18: own_health
    ally_health = obs[:, :, :, 15]      # Index 15: ally_0_health
    enemy_0_available = obs[:, :, :, 4] # Index 4: enemy_0_available
    agent_id = obs[:, :, :, 21]         # Index 21: agent_id
    
    # Get diagonal elements for self-observations
    enemy_0_distance_self = torch.diagonal(enemy_0_distance, dim1=1, dim2=2)  # (bs, n_agents)
    own_health_self = torch.diagonal(own_health, dim1=1, dim2=2)              # (bs, n_agents)
    ally_health_self = torch.diagonal(ally_health, dim1=1, dim2=2)            # (bs, n_agents)
    enemy_0_available_self = torch.diagonal(enemy_0_available, dim1=1, dim2=2) # (bs, n_agents)
    agent_id_self = torch.diagonal(agent_id, dim1=1, dim2=2)                  # (bs, n_agents)
    
    # Reshape for broadcasting
    enemy_0_distance_self_exp = enemy_0_distance_self.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
    own_health_self_exp = own_health_self.unsqueeze(2).unsqueeze(3)              # (bs, n_agents, 1, 1)
    ally_health_self_exp = ally_health_self.unsqueeze(2).unsqueeze(3)            # (bs, n_agents, 1, 1)
    enemy_0_available_self_exp = enemy_0_available_self.unsqueeze(2).unsqueeze(3) # (bs, n_agents, 1, 1)
    agent_id_self_exp = agent_id_self.unsqueeze(2).unsqueeze(3)                  # (bs, n_agents, 1, 1)
    
    # Define constants
    attack_range = 10.0
    health_threshold_medivac = 0.5
    health_threshold_marine = 0.25
    critical_health_threshold = 0.3
    
    # Agent 0 (Medivac) conditions
    is_agent_0 = (agent_id_self_exp == 0).float()  # (bs, n_agents, 1, 1)
    
    # Condition 1: Enemy within attack range
    cond1_agent0 = (enemy_0_distance_self_exp < attack_range).float() * is_agent_0
    
    # Condition 2: Own health below 50%
    cond2_agent0 = (own_health_self_exp < health_threshold_medivac).float() * is_agent_0
    
    # Condition 3: Multiple allies with health below 30%
    low_health_allies = (ally_health_self_exp < critical_health_threshold).float()
    cond3_agent0 = (low_health_allies > 0).float() * is_agent_0
    
    # Marine agents conditions (agents 1-7)
    # === Fix 1: 使用 logical_and 修复 bitwise & 报错 ===
    is_marine = torch.logical_and(agent_id_self_exp >= 1, agent_id_self_exp <= 7).float()
    
    # Condition 1: Enemy Medivac detected
    cond1_marine = (enemy_0_available_self_exp > 0).float() * is_marine
    
    # Condition 2: Own health below 25%
    cond2_marine = (own_health_self_exp < health_threshold_marine).float() * is_marine
    
    # Condition 3: Various marine-specific conditions
    cond3_marine = is_marine 
    
    # Create target masks for each condition
    marine_targets = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device)
    marine_indices = torch.tensor([1, 2, 3, 4, 5, 6, 7], device=obs.device)
    # Ensure indices are within range to prevent error on other maps
    marine_indices = marine_indices[marine_indices < n_agents]
    if len(marine_indices) > 0:
        marine_targets[:, :, marine_indices, :] = 1.0
    
    all_targets = torch.ones(bs, n_agents, n_agents, 1, device=obs.device)
    
    medivac_target = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device)
    medivac_target[:, :, 0:1, :] = 1.0
    
    # Combine conditions and targets
    if mode == 'object':
        # Agent 0 communications
        mask = mask + cond1_agent0.expand(bs, n_agents, n_agents, 1) * marine_targets
        mask = mask + cond2_agent0.expand(bs, n_agents, n_agents, 1) * marine_targets
        mask = mask + cond3_agent0.expand(bs, n_agents, n_agents, 1) * all_targets
        
        # Marine communications
        mask = mask + cond1_marine.expand(bs, n_agents, n_agents, 1) * all_targets
        mask = mask + cond2_marine.expand(bs, n_agents, n_agents, 1) * medivac_target
        mask = mask + cond3_marine.expand(bs, n_agents, n_agents, 1) * all_targets
        
        mask = torch.clamp(mask, 0, 1)
        
    elif mode == 'content':
        object_mask = torch.ones(bs, n_agents, n_agents, 1, device=obs.device)
        content_dim = obs_dim
        content_mask = torch.zeros(bs, n_agents, n_agents, content_dim, device=obs.device)
        
        agent0_cond = (cond1_agent0 + cond2_agent0 + cond3_agent0).expand(bs, n_agents, n_agents, content_dim)
        # Use first 10 dims
        max_idx = min(10, content_dim)
        content_mask[:, :, :, 0:max_idx] = agent0_cond[:, :, :, 0:max_idx]
        
        marine_cond = (cond1_marine + cond2_marine + cond3_marine).expand(bs, n_agents, n_agents, content_dim)
        # Use dims 10-20
        start_idx = min(10, content_dim)
        end_idx = min(20, content_dim)
        content_mask[:, :, :, start_idx:end_idx] = marine_cond[:, :, :, start_idx:end_idx]
        
        mask = object_mask.expand(bs, n_agents, n_agents, content_dim) * content_mask
        
    elif mode == 'object_content':
        object_mask = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device)
        
        object_mask = object_mask + cond1_agent0.expand(bs, n_agents, n_agents, 1) * marine_targets
        object_mask = object_mask + cond2_agent0.expand(bs, n_agents, n_agents, 1) * marine_targets
        object_mask = object_mask + cond3_agent0.expand(bs, n_agents, n_agents, 1) * all_targets
        
        object_mask = object_mask + cond1_marine.expand(bs, n_agents, n_agents, 1) * all_targets
        object_mask = object_mask + cond2_marine.expand(bs, n_agents, n_agents, 1) * medivac_target
        object_mask = object_mask + cond3_marine.expand(bs, n_agents, n_agents, 1) * all_targets
        
        object_mask = torch.clamp(object_mask, 0, 1)
        
        content_mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device)
        
        agent0_active = (cond1_agent0 + cond2_agent0 + cond3_agent0).expand(bs, n_agents, n_agents, obs_dim)
        max_idx = min(10, obs_dim)
        content_mask[:, :, :, 0:max_idx] = agent0_active[:, :, :, 0:max_idx]
        
        marine_active = (cond1_marine + cond2_marine + cond3_marine).expand(bs, n_agents, n_agents, obs_dim)
        start_idx = min(10, obs_dim)
        end_idx = min(20, obs_dim)
        content_mask[:, :, :, start_idx:end_idx] = marine_active[:, :, :, start_idx:end_idx]
        
        mask = object_mask.expand(bs, n_agents, n_agents, obs_dim) * content_mask
    
    mask = (mask > 0).float()
    return mask

if __name__ == "__main__":
    # Test
    obs = torch.randn(2, 8, 8, 127)
    m = generate_mask(obs, 'object_content')
    print("Success:", m.shape)