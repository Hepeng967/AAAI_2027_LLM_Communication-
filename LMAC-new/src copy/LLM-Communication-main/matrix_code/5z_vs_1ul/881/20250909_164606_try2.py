import torch

def generate_mask(obs, mode='object'):
    bs, n_agents, _, obs_dim = obs.shape
    assert n_agents == 5, "Expected 5 agents"
    assert obs_dim == 35, "Expected 35 observation dimensions"
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), dtype=torch.float32, device=obs.device)
    elif mode in ['content', 'object_content']:
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=obs.device)
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    # Define observation indices
    ENEMY_0_AVAILABLE = 4
    OWN_HEALTH = 33
    OWN_SHIELD = 34
    
    # Ally observation indices (for each ally 0-4)
    ally_indices = {
        'visible': [9, 15, 21, 27],
        'distance': [10, 16, 22, 28],
        'health': [13, 19, 25, 31],
        'shield': [14, 20, 26, 32]
    }
    
    # Content indices for different message types
    content_indices = {
        'enemy_spotted': [5, 6, 7],  # enemy_0_distance, enemy_0_rel_x, enemy_0_rel_y
        'low_health_kite': [33, 34, 6, 7],  # own_health, own_shield, own_rel_x, own_rel_y
        'fall_back': [],
        'cover_ally': [],
        'focus_fire': [5, 6, 7],  # enemy info
        'spread_out': [],
        'flanking': [],
        'engage_kite': []
    }
    
    # Process each agent's communication triggers
    for agent_id in range(n_agents):
        # Get this agent's observation
        agent_obs = obs[:, agent_id, :, :]  # (bs, n_agents, obs_dim)
        
        # Trigger 1: First observe Ultralisk (enemy_0_available becomes 1)
        trigger1 = (agent_obs[:, :, ENEMY_0_AVAILABLE] > 0.5).float()  # (bs, n_agents)
        
        # Trigger 2: Own health drops below 50%
        trigger2 = (agent_obs[:, :, OWN_HEALTH] < 0.5).float()  # (bs, n_agents)
        
        # For trigger 2: Find nearest visible ally
        ally_distances = agent_obs[:, :, ally_indices['distance']]  # (bs, n_agents, 4)
        ally_visible = (agent_obs[:, :, ally_indices['visible']] > 0.5).float()  # (bs, n_agents, 4)
        
        # Set distance to a large value for invisible allies
        max_distance = torch.max(ally_distances) + 100.0
        masked_distances = ally_distances + (1 - ally_visible) * max_distance
        
        # Find nearest ally index for each batch and agent
        nearest_ally_indices = torch.argmin(masked_distances, dim=2)  # (bs, n_agents)
        
        # Create one-hot encoding for nearest ally (shape: bs, n_agents, 4)
        nearest_ally_mask = torch.zeros((bs, n_agents, 4), dtype=torch.float32, device=obs.device)
        batch_indices = torch.arange(bs).unsqueeze(1).unsqueeze(2).expand(bs, n_agents, 1)
        agent_indices = torch.arange(n_agents).unsqueeze(0).unsqueeze(2).expand(bs, n_agents, 1)
        nearest_ally_mask.scatter_(2, nearest_ally_indices.unsqueeze(2), 1.0)
        
        # Convert to target agent indices (0-4)
        nearest_ally_targets = torch.zeros((bs, n_agents, n_agents), dtype=torch.float32, device=obs.device)
        for ally_idx in range(4):
            target_mask = nearest_ally_mask[:, :, ally_idx].unsqueeze(2)  # (bs, n_agents, 1)
            nearest_ally_targets[:, :, ally_idx + (1 if ally_idx >= agent_id else 0)] = target_mask.squeeze(2)
        
        # Apply communication based on triggers
        # Trigger 1: Broadcast to all other agents when enemy spotted
        if mode == 'object':
            # Create mask for all other agents
            other_agents = torch.ones((bs, n_agents, n_agents, 1), dtype=torch.float32, device=obs.device)
            for i in range(n_agents):
                other_agents[:, i, i, :] = 0  # Don't communicate with self
            
            # Apply trigger 1
            trigger1_expanded = trigger1.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
            mask[:, agent_id, :, :] += trigger1_expanded * other_agents[:, agent_id, :, :]
            
            # Apply trigger 2 (nearest ally)
            trigger2_expanded = trigger2.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
            nearest_targets_expanded = nearest_ally_targets.unsqueeze(3)  # (bs, n_agents, n_agents, 1)
            mask[:, agent_id, :, :] += trigger2_expanded * nearest_targets_expanded[:, agent_id, :, :]
            
        elif mode in ['content', 'object_content']:
            # Create content mask for enemy spotted
            enemy_content = torch.zeros((bs, n_agents, obs_dim), dtype=torch.float32, device=obs.device)
            enemy_content[:, :, content_indices['enemy_spotted']] = 1.0
            
            # Create content mask for low health kite
            low_health_content = torch.zeros((bs, n_agents, obs_dim), dtype=torch.float32, device=obs.device)
            low_health_content[:, :, content_indices['low_health_kite']] = 1.0
            
            # Apply trigger 1: Broadcast to all other agents
            other_agents = [j for j in range(n_agents) if j != agent_id]
            trigger1_broadcast = trigger1.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
            enemy_content_broadcast = enemy_content.unsqueeze(1)  # (bs, 1, n_agents, obs_dim)
            
            mask[:, agent_id, other_agents, :] += (trigger1_broadcast * enemy_content_broadcast)[:, agent_id, other_agents, :]
            
            # Apply trigger 2: Send to nearest ally
            trigger2_expanded = trigger2.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
            low_health_expanded = low_health_content.unsqueeze(1)  # (bs, 1, n_agents, obs_dim)
            nearest_targets_expanded = nearest_ally_targets.unsqueeze(3)  # (bs, n_agents, n_agents, 1)
            
            # Combine all factors
            trigger2_comm = trigger2_expanded * low_health_expanded * nearest_targets_expanded
            mask[:, agent_id, :, :] += trigger2_comm[:, agent_id, :, :]
    
    # Ensure binary mask
    mask = (mask > 0).float()
    
    return mask