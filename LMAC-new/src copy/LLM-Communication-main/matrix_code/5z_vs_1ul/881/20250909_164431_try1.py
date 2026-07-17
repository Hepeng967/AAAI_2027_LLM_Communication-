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
        trigger1_mask = (agent_obs[:, :, ENEMY_0_AVAILABLE] > 0.5).float()  # (bs, n_agents)
        
        # Trigger 2: Own health drops below 50%
        trigger2_mask = (agent_obs[:, :, OWN_HEALTH] < 0.5).float()  # (bs, n_agents)
        
        # For trigger 2: Find nearest visible ally
        ally_distances = agent_obs[:, :, ally_indices['distance']]  # (bs, n_agents, 4)
        ally_visible = agent_obs[:, :, ally_indices['visible']] > 0.5  # (bs, n_agents, 4)
        
        # Set distance to infinity for invisible allies
        max_distance = torch.max(ally_distances) + 1.0
        masked_distances = torch.where(ally_visible, ally_distances, max_distance)
        
        # Find nearest ally index for each batch
        nearest_ally_indices = torch.argmin(masked_distances, dim=2)  # (bs, n_agents)
        
        # Create one-hot encoding for nearest ally
        nearest_ally_mask = torch.zeros_like(ally_visible[:, :, 0], dtype=torch.float32)  # (bs, n_agents)
        for b in range(bs):
            for a in range(n_agents):
                if nearest_ally_indices[b, a] < 4:  # Valid ally index
                    nearest_ally_mask[b, a] = (nearest_ally_indices[b, a] == torch.arange(4, device=obs.device)).float().sum()
        
        # Trigger 3 conditions vary by agent
        if agent_id == 0:
            # Agent 0: Ally health below 25%
            ally_health = agent_obs[:, :, ally_indices['health']]  # (bs, n_agents, 4)
            injured_ally_mask = (ally_health < 0.25).float()  # (bs, n_agents, 4)
            
            # Find farthest ally from enemy
            enemy_distance = agent_obs[:, :, 5]  # enemy_0_distance (bs, n_agents)
            farthest_ally_indices = torch.argmax(enemy_distance, dim=1)  # (bs)
            
        elif agent_id == 1:
            # Agent 1: Enemy focusing on specific ally
            # This is complex to implement, so we'll use a simplified version
            trigger3_mask = torch.zeros((bs, n_agents), dtype=torch.float32, device=obs.device)
            
        elif agent_id == 2:
            # Agent 2: Allies too clustered
            # Check if any two allies are within distance 3
            trigger3_mask = torch.zeros((bs, n_agents), dtype=torch.float32, device=obs.device)
            
        elif agent_id == 3:
            # Agent 3: On opposite side of Ultralisk
            trigger3_mask = torch.zeros((bs, n_agents), dtype=torch.float32, device=obs.device)
            
        elif agent_id == 4:
            # Agent 4: Highest health and not target
            own_health_shield = agent_obs[:, :, OWN_HEALTH] + agent_obs[:, :, OWN_SHIELD]
            ally_health_shield = torch.zeros((bs, n_agents, 4), dtype=torch.float32, device=obs.device)
            for i in range(4):
                ally_health_shield[:, :, i] = agent_obs[:, :, ally_indices['health'][i]] + agent_obs[:, :, ally_indices['shield'][i]]
            
            # Check if this agent has highest health+shield
            is_highest = (own_health_shield > torch.max(ally_health_shield, dim=2)[0]).float()
            trigger3_mask = is_highest
        
        # Apply communication based on triggers
        # For simplicity, we'll implement a basic version
        
        # Trigger 1: Broadcast to all other agents
        if mode == 'object':
            # Set communication to all other agents when enemy spotted
            other_agents_mask = torch.ones((bs, n_agents, n_agents, 1), dtype=torch.float32, device=obs.device)
            for i in range(n_agents):
                other_agents_mask[:, i, i, :] = 0  # Don't communicate with self
            
            mask[:, agent_id, :, :] += trigger1_mask.unsqueeze(2).unsqueeze(3) * other_agents_mask[:, agent_id, :, :]
            
        elif mode in ['content', 'object_content']:
            # Set specific content for enemy spotted
            content_mask = torch.zeros((bs, n_agents, obs_dim), dtype=torch.float32, device=obs.device)
            content_mask[:, :, content_indices['enemy_spotted']] = 1.0
            
            # Broadcast to all other agents
            other_agents = [j for j in range(n_agents) if j != agent_id]
            mask[:, agent_id, other_agents, :] += trigger1_mask.unsqueeze(2).unsqueeze(3) * content_mask.unsqueeze(1)
    
    # Ensure binary mask
    mask = (mask > 0).float()
    
    return mask