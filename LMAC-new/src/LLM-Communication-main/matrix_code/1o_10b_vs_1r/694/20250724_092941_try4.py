import torch

def generate_mask(obs, mode='object'):
    assert mode in ['object', 'content', 'object_content'], "Invalid mode"
    bs, n_agents, _, obs_dim = obs.shape
    device = obs.device if hasattr(obs, 'device') else 'cpu'
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), device=device)
    else:
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device)
    
    # Get indices for important observation features
    move_indices = list(range(4))  # First 4 features are movement directions
    enemy_0_available_idx = 4
    enemy_0_distance_idx = 5
    enemy_0_rel_x_idx = 6
    enemy_0_rel_y_idx = 7
    own_health_idx = 80
    
    # Health threshold for low health condition
    health_threshold = 20
    
    # Overseer is agent 10 (index 10)
    overseer_idx = 10
    baneling_indices = list(range(10))  # Agents 0-9 are Banelings
    
    # Extract relevant features from obs
    enemy_available = obs[:, :, :, enemy_0_available_idx]  # (bs, n_agents, n_agents)
    enemy_distance = obs[:, :, :, enemy_0_distance_idx]    # (bs, n_agents, n_agents)
    own_health = obs[:, :, :, own_health_idx]             # (bs, n_agents, n_agents)
    
    # Overseer communication logic
    # Trigger Condition 1: Overseer detects Roach
    overseer_detects = (enemy_available[:, overseer_idx, overseer_idx] == 1).float()
    overseer_detects = overseer_detects.view(bs, 1, 1, 1)  # (bs, 1, 1, 1)
    
    if mode == 'object':
        # Overseer communicates with all Banelings
        mask[:, overseer_idx, :10, :] = overseer_detects.expand(-1, 1, 10, 1)
        
        # Trigger Condition 2: Overseer observes low health Baneling
        for baneling_idx in baneling_indices:
            ally_health_idx = 15 + 8 * baneling_idx  # ally_X_health indices
            if ally_health_idx >= obs_dim:  # Ensure index is within bounds
                continue
            ally_health = obs[:, overseer_idx, overseer_idx, ally_health_idx]  # (bs,)
            low_health = (ally_health < health_threshold).float().view(bs, 1, 1, 1)
            mask[:, overseer_idx, baneling_idx:baneling_idx+1, :] = low_health
    else:
        # Content selection for Overseer
        overseer_content = torch.zeros((bs, 1, 1, obs_dim), device=device)
        overseer_content[:, :, :, [enemy_0_rel_x_idx, enemy_0_rel_y_idx, enemy_0_distance_idx]] = 1
        
        # Apply trigger condition
        mask[:, overseer_idx, :10, :] = overseer_detects.expand(-1, 1, 10, obs_dim) * overseer_content.expand(-1, 1, 10, -1)
        
        # Trigger Condition 2: Overseer observes low health Baneling
        for baneling_idx in baneling_indices:
            ally_health_idx = 15 + 8 * baneling_idx  # ally_X_health indices
            if ally_health_idx >= obs_dim:  # Ensure index is within bounds
                continue
            ally_health = obs[:, overseer_idx, overseer_idx, ally_health_idx]  # (bs,)
            low_health = (ally_health < health_threshold).float().view(bs, 1, 1, 1)
            
            # Create retreat message (using move directions)
            retreat_content = torch.zeros((bs, 1, 1, obs_dim), device=device)
            retreat_content[:, :, :, move_indices] = 1  # Using move directions as retreat signal
            
            if mode == 'content':
                mask[:, overseer_idx, baneling_idx:baneling_idx+1, :] = retreat_content.squeeze(2)
            else:
                mask[:, overseer_idx, baneling_idx:baneling_idx+1, :] = low_health.expand(-1, 1, 1, obs_dim) * retreat_content
    
    # Baneling communication logic
    for baneling_idx in baneling_indices:
        # Trigger Condition 1: Baneling receives Roach position from Overseer
        if mode == 'object':
            received_info = (mask[:, overseer_idx, baneling_idx, 0] > 0).float().view(bs, 1, 1, 1)
        else:
            received_info = (mask[:, overseer_idx, baneling_idx, enemy_0_rel_x_idx] > 0).float().view(bs, 1, 1, 1)
        
        if mode == 'object':
            # Communicate with nearest 3 Banelings (simplified - just pick next 3)
            targets = [(baneling_idx + i + 1) % 10 for i in range(3)]
            for target in targets:
                mask[:, baneling_idx, target:target+1, :] = received_info
        else:
            # Forward Roach position + movement info
            forward_content = torch.zeros((bs, 1, 1, obs_dim), device=device)
            forward_content[:, :, :, [enemy_0_rel_x_idx, enemy_0_rel_y_idx, enemy_0_distance_idx]] = 1  # Roach info
            forward_content[:, :, :, move_indices] = 1  # Movement info
            
            if mode == 'content':
                mask[:, baneling_idx, :, :] = forward_content.expand(-1, n_agents, n_agents, -1)[:, 0, :, :]
            else:
                mask[:, baneling_idx, :, :] = received_info.expand(-1, 1, n_agents, obs_dim).squeeze(1) * forward_content.expand(-1, n_agents, n_agents, -1)[:, 0, :, :]
        
        # Trigger Condition 3: Baneling close to Roach
        close_to_roach = (enemy_distance[:, baneling_idx, baneling_idx] < 5).float().view(bs, 1, 1, 1)
        
        if mode == 'object':
            # Communicate with all Banelings in range (simplified - all Banelings)
            mask[:, baneling_idx, :10, :] = torch.maximum(mask[:, baneling_idx, :10, :], close_to_roach.expand(-1, 1, 10, 1))
        else:
            attack_content = torch.zeros((bs, 1, 1, obs_dim), device=device)
            attack_content[:, :, :, [enemy_0_rel_x_idx, enemy_0_rel_y_idx]] = 1  # Attack position
            
            if mode == 'content':
                mask[:, baneling_idx, :, :] = torch.maximum(mask[:, baneling_idx, :, :], attack_content.expand(-1, n_agents, n_agents, -1)[:, 0, :, :])
            else:
                mask[:, baneling_idx, :, :] = torch.maximum(
                    mask[:, baneling_idx, :, :], 
                    close_to_roach.expand(-1, 1, n_agents, obs_dim).squeeze(1) * attack_content.expand(-1, n_agents, n_agents, -1)[:, 0, :, :]
                )
        
        # Trigger Condition 4: Baneling low health and can't reach Roach
        low_health = (own_health[:, baneling_idx, baneling_idx] < health_threshold).float().view(bs, 1, 1, 1)
        cant_reach = (enemy_distance[:, baneling_idx, baneling_idx] > 10).float().view(bs, 1, 1, 1)
        
        if mode == 'object':
            mask[:, baneling_idx, overseer_idx:overseer_idx+1, :] = (low_health * cant_reach).expand(-1, 1, 1, 1)
        else:
            cant_engage_content = torch.zeros((bs, 1, 1, obs_dim), device=device)
            cant_engage_content[:, :, :, own_health_idx] = 1  # Health status
            
            if mode == 'content':
                mask[:, baneling_idx, overseer_idx:overseer_idx+1, :] = cant_engage_content.squeeze(2)
            else:
                mask[:, baneling_idx, overseer_idx:overseer_idx+1, :] = (low_health * cant_reach).expand(-1, 1, 1, obs_dim) * cant_engage_content

    return mask