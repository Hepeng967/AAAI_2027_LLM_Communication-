import torch

def generate_mask(obs, mode='object'):
    """
    Generate communication mask based on the given policy.
    obs: tensor of shape (bs, n_agents, n_agents, obs_dim)
    mode: 'object', 'content', or 'object_content'
    """
    bs, n_agents, _, obs_dim = obs.shape
    assert n_agents == 3, "Expected 3 agents"
    assert obs_dim == 49, "Expected 49 observation dimensions"
    
    # Initialize mask based on mode
    if mode == 'object':
        mask = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device, dtype=obs.dtype)
    else:
        mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device, dtype=obs.dtype)
    
    # Get indices for observation features
    feature_names = ['move_north', 'move_south', 'move_east', 'move_west', 'enemy_0_available', 'enemy_0_distance', 'enemy_0_rel_x', 'enemy_0_rel_y', 'enemy_0_health', 'enemy_0_type_0', 'enemy_0_type_1', 'enemy_1_available', 'enemy_1_distance', 'enemy_1_rel_x', 'enemy_1_rel_y', 'enemy_1_health', 'enemy_1_type_0', 'enemy_1_type_1', 'enemy_2_available', 'enemy_2_distance', 'enemy_2_rel_x', 'enemy_2_rel_y', 'enemy_2_health', 'enemy_2_type_0', 'enemy_2_type_1', 'enemy_3_available', 'enemy_3_distance', 'enemy_3_rel_x', 'enemy_3_rel_y', 'enemy_3_health', 'enemy_3_type_0', 'enemy_3_type_1', 'ally_0_visible', 'ally_0_distance', 'ally_0_rel_x', 'ally_0_rel_y', 'ally_0_health', 'ally_0_type_0', 'ally_0_type_1', 'ally_1_visible', 'ally_1_distance', 'ally_1_rel_x', 'ally_1_rel_y', 'ally_1_health', 'ally_1_type_0', 'ally_1_type_1', 'own_health', 'own_type_0', 'own_type_1']
    feature_indices = {name: idx for idx, name in enumerate(feature_names)}
    
    # Extract each agent's own observation (diagonal elements)
    own_obs = torch.diagonal(obs, dim1=1, dim2=2).permute(0, 2, 1)  # (bs, n_agents, obs_dim)
    
    # Extract relevant features
    enemy_avail_indices = [feature_indices[f'enemy_{i}_available'] for i in range(4)]
    enemy_avail = own_obs[:, :, enemy_avail_indices]  # (bs, n_agents, 4)
    
    enemy_rel_x_indices = [feature_indices[f'enemy_{i}_rel_x'] for i in range(4)]
    enemy_rel_y_indices = [feature_indices[f'enemy_{i}_rel_y'] for i in range(4)]
    enemy_health_indices = [feature_indices[f'enemy_{i}_health'] for i in range(4)]
    
    own_health_idx = feature_indices['own_health']
    own_health = own_obs[:, :, own_health_idx]  # (bs, n_agents)
    
    ally_rel_x_indices = [feature_indices[f'ally_{i}_rel_x'] for i in range(2)]
    ally_rel_y_indices = [feature_indices[f'ally_{i}_rel_y'] for i in range(2)]
    
    # Create boolean conditions
    enemy_detected = enemy_avail > 0.5  # (bs, n_agents, 4)
    low_health_threshold = 0.4
    critical_health_threshold = 0.25
    low_health = own_health < low_health_threshold  # (bs, n_agents)
    
    # For simplicity, assume enemy health is normalized [0,1]
    enemy_health = own_obs[:, :, enemy_health_indices]  # (bs, n_agents, 4)
    enemy_critical_health = enemy_health < critical_health_threshold  # (bs, n_agents, 4)
    
    if mode == 'object':
        # Agent 0 (Overseer) to both Roaches
        overseer_conditions = (enemy_detected[:, 0, :].any(dim=1) |  # Trigger 1
                             enemy_critical_health[:, 0, :].any(dim=1))  # Trigger 3
        overseer_conditions = overseer_conditions.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        overseer_conditions = overseer_conditions.expand(bs, 1, 2, 1)  # (bs, 1, 2, 1)
        mask[:, 0, 1:3, :] = overseer_conditions.float()
        
        # Agent 1 to Overseer (Trigger 1)
        roach1_to_overseer = enemy_detected[:, 1, :].any(dim=1).unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach1_to_overseer = roach1_to_overseer.expand(bs, 1, 1, 1)  # (bs, 1, 1, 1)
        mask[:, 1, 0:1, :] = roach1_to_overseer.float()
        
        # Agent 1 to Roach 2 and Overseer (Trigger 2)
        roach1_help = low_health[:, 1].unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach1_help = roach1_help.expand(bs, 1, 2, 1)  # (bs, 1, 2, 1)
        mask[:, 1, [0, 2], :] = roach1_help.float()
        
        # Agent 2 to Overseer (Trigger 1)
        roach2_to_overseer = enemy_detected[:, 2, :].any(dim=1).unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach2_to_overseer = roach2_to_overseer.expand(bs, 1, 1, 1)  # (bs, 1, 1, 1)
        mask[:, 2, 0:1, :] = roach2_to_overseer.float()
        
        # Agent 2 to Roach 1 and Overseer (Trigger 2)
        roach2_help = low_health[:, 2].unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach2_help = roach2_help.expand(bs, 1, 2, 1)  # (bs, 1, 2, 1)
        mask[:, 2, [0, 1], :] = roach2_help.float()
        
        # Agent coordination (Trigger 3) - simplified
        roach_coordination = (enemy_detected[:, 1, :].any(dim=1) | enemy_detected[:, 2, :].any(dim=1))  # (bs)
        roach_coordination = roach_coordination.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach_coordination = roach_coordination.expand(bs, 2, 1, 1)  # (bs, 2, 1, 1)
        mask[:, 1, 2:3, :] = roach_coordination[:, 0:1, :, :].float()
        mask[:, 2, 1:2, :] = roach_coordination[:, 1:2, :, :].float()
        
    else:  # content or object_content
        # Create content masks
        enemy_content_indices = []
        for i in range(4):
            enemy_content_indices.extend([
                feature_indices[f'enemy_{i}_rel_x'],
                feature_indices[f'enemy_{i}_rel_y'],
                feature_indices[f'enemy_{i}_health']
            ])
        enemy_content_mask = torch.zeros(obs_dim, device=obs.device, dtype=obs.dtype)
        enemy_content_mask[enemy_content_indices] = 1
        
        help_content_indices = [feature_indices['own_health']] + ally_rel_x_indices + ally_rel_y_indices
        help_content_mask = torch.zeros(obs_dim, device=obs.device, dtype=obs.dtype)
        help_content_mask[help_content_indices] = 1
        
        # Expand content masks
        enemy_content_mask_exp = enemy_content_mask.unsqueeze(0).unsqueeze(0).unsqueeze(0).expand(bs, 1, 1, obs_dim)
        help_content_mask_exp = help_content_mask.unsqueeze(0).unsqueeze(0).unsqueeze(0).expand(bs, 1, 1, obs_dim)
        
        # Agent 0 (Overseer) to both Roaches
        overseer_conditions = (enemy_detected[:, 0, :].any(dim=1) | enemy_critical_health[:, 0, :].any(dim=1))  # (bs)
        overseer_conditions = overseer_conditions.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        overseer_mask = overseer_conditions.expand(bs, 1, 2, obs_dim) * enemy_content_mask_exp.expand(bs, 1, 2, obs_dim)
        if mode == 'object_content':
            overseer_mask = overseer_mask * overseer_conditions.expand(bs, 1, 2, obs_dim).float()
        mask[:, 0, 1:3, :] = overseer_mask
        
        # Agent 1 to Overseer
        roach1_condition = enemy_detected[:, 1, :].any(dim=1).unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach1_mask = roach1_condition.expand(bs, 1, 1, obs_dim) * enemy_content_mask_exp.expand(bs, 1, 1, obs_dim)
        if mode == 'object_content':
            roach1_mask = roach1_mask * roach1_condition.expand(bs, 1, 1, obs_dim).float()
        mask[:, 1, 0:1, :] = roach1_mask
        
        # Agent 1 help request
        roach1_help_condition = low_health[:, 1].unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach1_help_mask = roach1_help_condition.expand(bs, 1, 2, obs_dim) * help_content_mask_exp.expand(bs, 1, 2, obs_dim)
        if mode == 'object_content':
            roach1_help_mask = roach1_help_mask * roach1_help_condition.expand(bs, 1, 2, obs_dim).float()
        mask[:, 1, [0, 2], :] += roach1_help_mask
        
        # Agent 2 to Overseer
        roach2_condition = enemy_detected[:, 2, :].any(dim=1).unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach2_mask = roach2_condition.expand(bs, 1, 1, obs_dim) * enemy_content_mask_exp.expand(bs, 1, 1, obs_dim)
        if mode == 'object_content':
            roach2_mask = roach2_mask * roach2_condition.expand(bs, 1, 1, obs_dim).float()
        mask[:, 2, 0:1, :] = roach2_mask
        
        # Agent 2 help request
        roach2_help_condition = low_health[:, 2].unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach2_help_mask = roach2_help_condition.expand(bs, 1, 2, obs_dim) * help_content_mask_exp.expand(bs, 1, 2, obs_dim)
        if mode == 'object_content':
            roach2_help_mask = roach2_help_mask * roach2_help_condition.expand(bs, 1, 2, obs_dim).float()
        mask[:, 2, [0, 1], :] += roach2_help_mask
        
        # Agent coordination (simplified)
        roach_coord_condition = (enemy_detected[:, 1, :].any(dim=1) | enemy_detected[:, 2, :].any(dim=1))  # (bs)
        roach_coord_condition = roach_coord_condition.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        
        roach1_coord_mask = roach_coord_condition.expand(bs, 1, 1, obs_dim) * enemy_content_mask_exp.expand(bs, 1, 1, obs_dim)
        roach2_coord_mask = roach_coord_condition.expand(bs, 1, 1, obs_dim) * enemy_content_mask_exp.expand(bs, 1, 1, obs_dim)
        if mode == 'object_content':
            roach1_coord_mask = roach1_coord_mask * roach_coord_condition.expand(bs, 1, 1, obs_dim).float()
            roach2_coord_mask = roach2_coord_mask * roach_coord_condition.expand(bs, 1, 1, obs_dim).float()
        mask[:, 1, 2:3, :] += roach1_coord_mask
        mask[:, 2, 1:2, :] += roach2_coord_mask
    
    return mask