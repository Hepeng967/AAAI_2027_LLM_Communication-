import torch

def generate_mask(obs, mode='object'):
    """
    Generate communication mask based on the specified policy.
    
    Args:
        obs: Tensor of shape (bs, n_agents, n_agents, obs_dim)
        mode: One of 'object', 'content', or 'object_content'
    
    Returns:
        Mask tensor of appropriate shape based on mode
    """
    bs, n_agents, _, obs_dim = obs.shape
    assert n_agents == 8, f"Expected 8 agents, got {n_agents}"
    assert obs_dim == 127, f"Expected 127 observation dimensions, got {obs_dim}"
    
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
    # Count allies with health < 30% (simplified: check if any ally health < 30%)
    low_health_allies = (ally_health_self_exp < critical_health_threshold).float()
    cond3_agent0 = (low_health_allies > 0).float() * is_agent_0
    
    # Marine agents conditions (agents 1-7)
    is_marine = ((agent_id_self_exp >= 1) & (agent_id_self_exp <= 7)).float()  # (bs, n_agents, 1, 1)
    
    # Condition 1: Enemy Medivac detected
    cond1_marine = (enemy_0_available_self_exp > 0).float() * is_marine
    
    # Condition 2: Own health below 25%
    cond2_marine = (own_health_self_exp < health_threshold_marine).float() * is_marine
    
    # Condition 3: Various marine-specific conditions (simplified as always true for demonstration)
    cond3_marine = is_marine  # Simplified: all marines have condition 3 active
    
    # Create target masks for each condition
    
    # Agent 0 conditions
    # Condition 1 & 2: Send to all marines (agents 1-7)
    marine_targets = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device)
    marine_indices = torch.tensor([1, 2, 3, 4, 5, 6, 7], device=obs.device)
    marine_targets[:, :, marine_indices, :] = 1.0
    
    # Condition 3: Send to all agents
    all_targets = torch.ones(bs, n_agents, n_agents, 1, device=obs.device)
    
    # Marine conditions
    # Condition 1 & 3: Send to all agents
    # Condition 2: Send to agent 0 only
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
        
        # Clip to 0-1 range
        mask = torch.clamp(mask, 0, 1)
        
    elif mode == 'content':
        # In content mode, all agents can communicate but we select content
        # Set all communication channels to open
        object_mask = torch.ones(bs, n_agents, n_agents, 1, device=obs.device)
        
        # Define content masks for different message types
        # For simplicity, we'll use different observation dimensions for different messages
        content_dim = obs_dim
        
        # Create content selection based on conditions
        content_mask = torch.zeros(bs, n_agents, n_agents, content_dim, device=obs.device)
        
        # Agent 0 content selection
        agent0_cond = (cond1_agent0 + cond2_agent0 + cond3_agent0).expand(bs, n_agents, n_agents, content_dim)
        # Use first 10 dimensions for agent 0 messages
        content_mask[:, :, :, 0:10] = agent0_cond[:, :, :, 0:10]
        
        # Marine content selection  
        marine_cond = (cond1_marine + cond2_marine + cond3_marine).expand(bs, n_agents, n_agents, content_dim)
        # Use dimensions 10-20 for marine messages
        content_mask[:, :, :, 10:20] = marine_cond[:, :, :, 10:20]
        
        # Combine object and content masks
        mask = object_mask.expand(bs, n_agents, n_agents, content_dim) * content_mask
        
    elif mode == 'object_content':
        # Combine object selection with content selection
        
        # First create object mask (same as object mode)
        object_mask = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device)
        
        # Agent 0 communications
        object_mask = object_mask + cond1_agent0.expand(bs, n_agents, n_agents, 1) * marine_targets
        object_mask = object_mask + cond2_agent0.expand(bs, n_agents, n_agents, 1) * marine_targets
        object_mask = object_mask + cond3_agent0.expand(bs, n_agents, n_agents, 1) * all_targets
        
        # Marine communications
        object_mask = object_mask + cond1_marine.expand(bs, n_agents, n_agents, 1) * all_targets
        object_mask = object_mask + cond2_marine.expand(bs, n_agents, n_agents, 1) * medivac_target
        object_mask = object_mask + cond3_marine.expand(bs, n_agents, n_agents, 1) * all_targets
        
        object_mask = torch.clamp(object_mask, 0, 1)
        
        # Create content selection
        content_mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device)
        
        # Agent 0 content (use first 10 dimensions)
        agent0_active = (cond1_agent0 + cond2_agent0 + cond3_agent0).expand(bs, n_agents, n_agents, obs_dim)
        content_mask[:, :, :, 0:10] = agent0_active[:, :, :, 0:10]
        
        # Marine content (use dimensions 10-20)
        marine_active = (cond1_marine + cond2_marine + cond3_marine).expand(bs, n_agents, n_agents, obs_dim)
        content_mask[:, :, :, 10:20] = marine_active[:, :, :, 10:20]
        
        # Combine object and content selection
        mask = object_mask.expand(bs, n_agents, n_agents, obs_dim) * content_mask
    
    # Ensure binary mask
    mask = (mask > 0).float()
    
    return mask

# Test the function
if __name__ == "__main__":
    # Test with correct dimensions
    obs = torch.randn(2, 8, 8, 127)
    mask_object = generate_mask(obs, mode='object')
    mask_content = generate_mask(obs, mode='content')  
    mask_object_content = generate_mask(obs, mode='object_content')
    
    print(f"Object mask shape: {mask_object.shape}")  # Should be (2, 8, 8, 1)
    print(f"Content mask shape: {mask_content.shape}")  # Should be (2, 8, 8, 127)
    print(f"Object-Content mask shape: {mask_object_content.shape}")  # Should be (2, 8, 8, 127)