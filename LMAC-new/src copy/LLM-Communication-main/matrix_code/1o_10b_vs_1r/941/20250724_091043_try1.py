import torch

def generate_mask(obs, mode='object'):
    assert mode in ['object', 'content', 'object_content'], "Invalid mode"
    bs, n_agents, _, obs_dim = obs.shape
    device = obs.device
    
    # Create empty masks based on mode
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), device=device)
    else:
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device)
    
    # Get indices from feature names
    enemy_0_available_idx = 4
    enemy_0_distance_idx = 5
    enemy_0_rel_x_idx = 6
    enemy_0_rel_y_idx = 7
    own_health_idx = 80
    
    # Overseer is agent 10 (index 10)
    overseer_idx = 10
    
    # Extract relevant features
    enemy_detected = obs[:, :, :, enemy_0_available_idx] > 0.5  # (bs, n_agents, n_agents)
    enemy_distance = obs[:, :, :, enemy_0_distance_idx]  # (bs, n_agents, n_agents)
    enemy_rel_x = obs[:, :, :, enemy_0_rel_x_idx]  # (bs, n_agents, n_agents)
    enemy_rel_y = obs[:, :, :, enemy_0_rel_y_idx]  # (bs, n_agents, n_agents)
    health = obs[:, :, :, own_health_idx]  # (bs, n_agents, n_agents)
    
    # Create agent type masks
    is_overseer = torch.zeros((bs, n_agents), device=device)
    is_overseer[:, overseer_idx] = 1
    is_baneling = 1 - is_overseer
    
    # Reshape for broadcasting
    is_overseer = is_overseer.unsqueeze(2)  # (bs, n_agents, 1)
    is_baneling = is_baneling.unsqueeze(2)  # (bs, n_agents, 1)
    
    ### Overseer communication rules ###
    # Condition 1: Overseer detects Roach and communicates to all Banelings
    overseer_detects = enemy_detected[:, overseer_idx, :]  # (bs, n_agents)
    overseer_to_banelings = (is_overseer.unsqueeze(2) * is_baneling.unsqueeze(1))  # (bs, n_agents, n_agents, 1)
    overseer_cond1 = overseer_detects.unsqueeze(1).unsqueeze(-1) * overseer_to_banelings  # (bs, n_agents, n_agents, 1)
    
    # Condition 2: Overseer observes damaged Baneling (health < 50%)
    health_percentage = health[:, overseer_idx, :]  # (bs, n_agents)
    damaged_banelings = (health_percentage < 0.5) * is_baneling.squeeze(2)  # (bs, n_agents)
    overseer_cond2 = damaged_banelings.unsqueeze(1).unsqueeze(-1) * overseer_to_banelings  # (bs, n_agents, n_agents, 1)
    
    # Combine overseer conditions (prioritize condition 1)
    overseer_mask = (overseer_cond1 > 0) | (overseer_cond2 > 0)
    
    ### Baneling communication rules ###
    # Condition 1: Baneling detects Roach and communicates to other Banelings
    baneling_detects = enemy_detected * is_baneling.unsqueeze(2)  # (bs, n_agents, n_agents)
    baneling_to_baneling = is_baneling.unsqueeze(2) * is_baneling.unsqueeze(1)  # (bs, n_agents, n_agents, 1)
    no_self_comm = 1 - torch.eye(n_agents, device=device).unsqueeze(0).unsqueeze(-1)  # (1, n_agents, n_agents, 1)
    baneling_cond1 = baneling_detects.unsqueeze(-1) * baneling_to_baneling * no_self_comm  # (bs, n_agents, n_agents, 1)
    
    # Condition 2: Baneling low health (health < 30%) communicates to nearest ally
    low_health = (health < 0.3) * is_baneling.unsqueeze(2)  # (bs, n_agents, n_agents)
    # Find nearest ally (excluding self)
    ally_distances = obs[:, :, :, [12 + 8*i for i in range(10)]]  # (bs, n_agents, n_agents, 10)
    min_distances, _ = torch.min(ally_distances + 1e6 * torch.eye(n_agents, device=device).unsqueeze(0).unsqueeze(-1), dim=3)
    is_nearest = (ally_distances == min_distances.unsqueeze(-1)) * is_baneling.unsqueeze(2)  # (bs, n_agents, n_agents, 10)
    baneling_cond2 = low_health.unsqueeze(-1) * is_nearest.any(dim=3, keepdim=True)  # (bs, n_agents, n_agents, 1)
    
    # Condition 3: Baneling blocked communicates to Overseer
    # Assuming blocked if movement commands are all zero
    move_commands = obs[:, :, :, :4]  # (bs, n_agents, n_agents, 4)
    is_blocked = (move_commands.sum(dim=3) == 0) * is_baneling.unsqueeze(2)  # (bs, n_agents, n_agents)
    baneling_to_overseer = is_baneling.unsqueeze(2) * is_overseer.unsqueeze(1)  # (bs, n_agents, n_agents, 1)
    baneling_cond3 = is_blocked.unsqueeze(-1) * baneling_to_overseer  # (bs, n_agents, n_agents, 1)
    
    # Combine baneling conditions
    baneling_mask = (baneling_cond1 > 0) | (baneling_cond2 > 0) | (baneling_cond3 > 0)
    
    # Combine all communication
    object_mask = (overseer_mask | baneling_mask).float()
    
    if mode == 'object':
        return object_mask
    
    # For content modes, create content masks
    content_mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device)
    
    # Overseer content
    # Condition 1: Send enemy position and distance
    overseer_content1 = torch.zeros_like(content_mask)
    overseer_content1[:, :, :, [enemy_0_rel_x_idx, enemy_0_rel_y_idx, enemy_0_distance_idx]] = 1
    overseer_content1 = overseer_content1 * overseer_cond1.unsqueeze(-1)
    
    # Condition 2: Send retreat signal (use move_south as signal)
    overseer_content2 = torch.zeros_like(content_mask)
    overseer_content2[:, :, :, 1] = 1  # move_south as retreat signal
    overseer_content2 = overseer_content2 * overseer_cond2.unsqueeze(-1)
    
    # Baneling content
    # Condition 1: Send enemy position and distance
    baneling_content1 = torch.zeros_like(content_mask)
    baneling_content1[:, :, :, [enemy_0_rel_x_idx, enemy_0_rel_y_idx, enemy_0_distance_idx]] = 1
    baneling_content1 = baneling_content1 * baneling_cond1.unsqueeze(-1)
    
    # Condition 2: Send own position and health
    baneling_content2 = torch.zeros_like(content_mask)
    for i in range(n_agents):
        ally_x_idx = 14 + 8*i
        ally_y_idx = 15 + 8*i
        baneling_content2[:, i, :, [ally_x_idx, ally_y_idx, own_health_idx]] = 1
    baneling_content2 = baneling_content2 * baneling_cond2.unsqueeze(-1)
    
    # Condition 3: Send own position
    baneling_content3 = torch.zeros_like(content_mask)
    for i in range(n_agents):
        ally_x_idx = 14 + 8*i
        ally_y_idx = 15 + 8*i
        baneling_content3[:, i, :, [ally_x_idx, ally_y_idx]] = 1
    baneling_content3 = baneling_content3 * baneling_cond3.unsqueeze(-1)
    
    # Combine all content
    content_mask = overseer_content1 + overseer_content2 + baneling_content1 + baneling_content2 + baneling_content3
    
    if mode == 'content':
        return content_mask
    else:  # object_content
        return object_mask.unsqueeze(-1) * content_mask