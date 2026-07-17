import torch

def generate_mask(obs, mode='object'):
    assert mode in ['object', 'content', 'object_content']
    bs, n_agents, _, obs_dim = obs.shape
    
    # Convert obs to torch tensor if it's numpy
    if not isinstance(obs, torch.Tensor):
        obs = torch.from_numpy(obs)
    
    # Get device from obs tensor
    device = obs.device
    
    # Get indices for important features
    enemy_0_available_idx = 4
    enemy_0_distance_idx = 5
    enemy_0_rel_x_idx = 6
    enemy_0_rel_y_idx = 7
    enemy_0_health_idx = 8
    own_health_idx = 33
    
    # Create base masks
    object_mask = torch.zeros((bs, n_agents, n_agents, 1), dtype=torch.float32, device=device)
    content_mask = torch.zeros((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=device)
    
    # Extract relevant features
    enemy_available = obs[:, :, 0, enemy_0_available_idx].unsqueeze(-1).unsqueeze(-1)  # (bs, n_agents, 1, 1)
    enemy_distance = obs[:, :, 0, enemy_0_distance_idx].unsqueeze(-1).unsqueeze(-1)  # (bs, n_agents, 1, 1)
    own_health = obs[:, :, 0, own_health_idx].unsqueeze(-1).unsqueeze(-1)  # (bs, n_agents, 1, 1)
    
    # Condition 1: Ultralisk spotted and close
    condition1 = (enemy_available > 0.5) & (enemy_distance <= 10)
    condition1 = condition1.expand(-1, -1, n_agents, -1)  # (bs, n_agents, n_agents, 1)
    
    # For condition1, communicate to all allies (all other agents)
    all_allies_mask = torch.ones_like(object_mask, device=device)
    diag_mask = 1 - torch.eye(n_agents, device=device).unsqueeze(0).unsqueeze(-1)  # (1, n_agents, n_agents, 1)
    all_allies_mask = all_allies_mask * diag_mask
    object_mask = torch.where(condition1, all_allies_mask, object_mask)
    
    # Content for condition1: enemy position and health info
    condition1_content = torch.zeros_like(content_mask, device=device)
    condition1_content[:, :, :, [enemy_0_rel_x_idx, enemy_0_rel_y_idx, enemy_0_health_idx]] = 1
    content_mask = torch.where(condition1.expand(-1, -1, -1, obs_dim), condition1_content, content_mask)
    
    # Condition 2: Own health low
    condition2 = (own_health <= 0.5)
    condition2 = condition2.expand(-1, -1, n_agents, -1)  # (bs, n_agents, n_agents, 1)
    
    # Find nearest ally for each agent
    # Create a matrix of distances from each agent to each other agent
    ally_distances = torch.zeros((bs, n_agents, n_agents), device=device)
    for i in range(n_agents):
        for j in range(n_agents):
            if i == j:
                ally_distances[:, i, j] = float('inf')
            else:
                # Get the distance to ally j from agent i's perspective
                if j < i:
                    ally_idx = j
                else:
                    ally_idx = j - 1
                ally_distances[:, i, j] = obs[:, i, 0, 11 + 6*ally_idx]  # 11 is ally_0_distance_idx
    
    nearest_ally = torch.argmin(ally_distances, dim=2)  # (bs, n_agents)
    nearest_ally_mask = torch.zeros((bs, n_agents, n_agents, 1), device=device)
    nearest_ally_mask.scatter_(2, nearest_ally.unsqueeze(-1).unsqueeze(-1), 1)
    
    object_mask = torch.where(condition2, nearest_ally_mask, object_mask)
    
    # Content for condition2: own health
    condition2_content = torch.zeros_like(content_mask, device=device)
    condition2_content[:, :, :, [own_health_idx]] = 1
    content_mask = torch.where(condition2.expand(-1, -1, -1, obs_dim), condition2_content, content_mask)
    
    # Condition 3: Ally health low
    # Check each ally's health from each agent's perspective
    for i in range(n_agents):
        for j in range(n_agents):
            if i != j:
                # Determine the ally index (0-3) for agent j from agent i's perspective
                if j < i:
                    ally_idx = j
                else:
                    ally_idx = j - 1
                
                # Get the health of this ally
                ally_health_idx = 13 + 6*ally_idx  # 13 is ally_0_health_idx
                ally_health = obs[:, i, 0, ally_health_idx].unsqueeze(-1).unsqueeze(-1).unsqueeze(-1)  # (bs, 1, 1, 1)
                
                # Check if this ally has low health
                condition3 = (ally_health <= 0.5)
                
                if condition3.any():
                    # Create mask for communicating to this ally and nearest other ally
                    target_mask = torch.zeros((bs, n_agents, n_agents, 1), device=device)
                    
                    # Communicate to the low-health ally (agent j)
                    target_mask[:, i, j, :] = 1
                    
                    # Also communicate to nearest other ally (excluding self and the low-health ally)
                    temp_distances = ally_distances.clone()
                    temp_distances[:, i, i] = float('inf')  # exclude self
                    temp_distances[:, i, j] = float('inf')  # exclude the low-health ally
                    
                    second_nearest = torch.argmin(temp_distances[:, i, :], dim=1)  # (bs,)
                    target_mask.scatter_(2, second_nearest.unsqueeze(1).unsqueeze(-1).unsqueeze(-1), 1)
                    
                    object_mask = torch.where(condition3.expand(-1, n_agents, n_agents, 1), target_mask, object_mask)
                    
                                        # Content for condition3: the low ally's health
                    condition3_content = torch.zeros_like(content_mask, device=device)
                    condition3_content[:, :, :, [ally_health_idx]] = 1
                    content_mask = torch.where(condition3.expand(-1, n_agents, n_agents, obs_dim), condition3_content, content_mask)
    
    # Return based on mode
    if mode == 'object':
        return object_mask
    elif mode == 'content':
        return content_mask
    else:  # object_content
        return object_mask.expand(-1, -1, -1, obs_dim) * content_mask