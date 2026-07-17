Here's the implementation of the generate_mask function that follows the communication policy:

```python
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
    
    # Get indices for observation features
    feature_names = ['move_north', 'move_south', 'move_east', 'move_west', 'enemy_0_available', 'enemy_0_distance', 'enemy_0_rel_x', 'enemy_0_rel_y', 'enemy_0_health', 'enemy_0_type_0', 'enemy_0_type_1', 'enemy_1_available', 'enemy_1_distance', 'enemy_1_rel_x', 'enemy_1_rel_y', 'enemy_1_health', 'enemy_1_type_0', 'enemy_1_type_1', 'enemy_2_available', 'enemy_2_distance', 'enemy_2_rel_x', 'enemy_2_rel_y', 'enemy_2_health', 'enemy_2_type_0', 'enemy_2_type_1', 'enemy_3_available', 'enemy_3_distance', 'enemy_3_rel_x', 'enemy_3_rel_y', 'enemy_3_health', 'enemy_3_type_0', 'enemy_3_type_1', 'ally_0_visible', 'ally_0_distance', 'ally_0_rel_x', 'ally_0_rel_y', 'ally_0_health', 'ally_0_type_0', 'ally_0_type_1', 'ally_1_visible', 'ally_1_distance', 'ally_1_rel_x', 'ally_1_rel_y', 'ally_1_health', 'ally_1_type_0', 'ally_1_type_1', 'own_health', 'own_type_0', 'own_type_1']
    
    # Create index mapping
    feature_indices = {name: idx for idx, name in enumerate(feature_names)}
    
    # Initialize mask based on mode
    if mode == 'object':
        mask = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device, dtype=obs.dtype)
    else:  # content or object_content
        mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device, dtype=obs.dtype)
    
    # Extract relevant features from obs
    # For each agent, we need their own observation (diagonal elements)
    own_obs = torch.diagonal(obs, dim1=1, dim2=2).permute(0, 2, 1)  # (bs, n_agents, obs_dim)
    
    # Enemy availability flags for each agent
    enemy_avail_indices = [feature_indices[f'enemy_{i}_available'] for i in range(4)]
    enemy_avail = own_obs[:, :, enemy_avail_indices]  # (bs, n_agents, 4)
    
    # Enemy relative positions and health
    enemy_pos_health_indices = []
    for i in range(4):
        enemy_pos_health_indices.extend([
            feature_indices[f'enemy_{i}_rel_x'],
            feature_indices[f'enemy_{i}_rel_y'],
            feature_indices[f'enemy_{i}_health']
        ])
    enemy_pos_health = own_obs[:, :, enemy_pos_health_indices]  # (bs, n_agents, 12)
    
    # Own health for each agent
    own_health_idx = feature_indices['own_health']
    own_health = own_obs[:, :, own_health_idx]  # (bs, n_agents)
    
    # Ally relative positions (for approximate position when health is low)
    ally_pos_indices = []
    for i in range(2):
        ally_pos_indices.extend([
            feature_indices[f'ally_{i}_rel_x'],
            feature_indices[f'ally_{i}_rel_y']
        ])
    ally_pos = own_obs[:, :, ally_pos_indices]  # (bs, n_agents, 4)
    
    # Create boolean masks for conditions
    # Enemy detection (availability > 0)
    enemy_detected = enemy_avail > 0.5  # (bs, n_agents, 4)
    
    # Low health conditions
    low_health_threshold = 0.4
    critical_health_threshold = 0.25
    low_health = own_health < low_health_threshold  # (bs, n_agents)
    critical_health = own_health < critical_health_threshold  # (bs, n_agents)
    
    # For simplicity, we'll assume enemy health is normalized [0,1]
    enemy_low_health = enemy_pos_health[:, :, 2::3] < critical_health_threshold  # (bs, n_agents, 4)
    
    # Agent 0 (Overseer) communication
    # Trigger 1: Enemy detected
    overseer_enemy_detected = enemy_detected[:, 0, :]  # (bs, 4)
    
    # Trigger 2: Enemy lost (simplified - track previous state would be needed for exact implementation)
    # For now, we'll use a simple heuristic: enemy was available but now not
    enemy_lost = torch.zeros_like(overseer_enemy_detected, dtype=torch.bool)
    
    # Trigger 3: Enemy health critical
    overseer_enemy_critical = enemy_low_health[:, 0, :]  # (bs, 4)
    
    # Agent 1 & 2 (Roaches) communication
    roach1_enemy_detected = enemy_detected[:, 1, :]  # (bs, 4)
    roach2_enemy_detected = enemy_detected[:, 2, :]  # (bs, 4)
    
    roach1_low_health = low_health[:, 1]  # (bs)
    roach2_low_health = low_health[:, 2]  # (bs)
    
    # For mode-specific implementations
    if mode == 'object':
        # Agent 0 to both Roaches (conditions 1, 2, 3)
        overseer_to_roaches = (overseer_enemy_detected.any(dim=1, keepdim=True) | 
                              enemy_lost.any(dim=1, keepdim=True) | 
                              overseer_enemy_critical.any(dim=1, keepdim=True))  # (bs, 1)
        overseer_to_roaches = overseer_to_roaches.unsqueeze(2).expand(bs, 1, 2, 1)  # (bs, 1, 2, 1)
        mask[:, 0, 1:3, :] = overseer_to_roaches.float()
        
        # Agent 1 to Overseer (condition 1)
        roach1_to_overseer = roach1_enemy_detected.any(dim=1, keepdim=True).unsqueeze(2)  # (bs, 1, 1)
        roach1_to_overseer = roach1_to_overseer.expand(bs, 1, 1, 1)  # (bs, 1, 1, 1)
        mask[:, 1, 0:1, :] = roach1_to_overseer.float()
        
        # Agent 1 to Roach 2 and Overseer (condition 2)
        roach1_help = roach1_low_health.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach1_help = roach1_help.expand(bs, 1, 2, 1)  # (bs, 1, 2, 1)
        mask[:, 1, [0, 2], :] = roach1_help.float()
        
        # Agent 2 to Overseer (condition 1)
        roach2_to_overseer = roach2_enemy_detected.any(dim=1, keepdim=True).unsqueeze(2)  # (bs, 1, 1)
        roach2_to_overseer = roach2_to_overseer.expand(bs, 1, 1, 1)  # (bs, 1, 1, 1)
        mask[:, 2, 0:1, :] = roach2_to_overseer.float()
        
        # Agent 2 to Roach 1 and Overseer (condition 2)
        roach2_help = roach2_low_health.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach2_help = roach2_help.expand(bs, 1, 2, 1)  # (bs, 1, 2, 1)
        mask[:, 2, [0, 1], :] = roach2_help.float()
        
        # Agent 1 to Roach 2 and Agent 2 to Roach 1 (condition 3 - simplified)
        # This would normally require tracking received messages, but for simplicity:
        roach_coordination = (roach1_enemy_detected.any(dim=1) | roach2_enemy_detected.any(dim=1))  # (bs)
        roach_coordination = roach_coordination.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach_coordination = roach_coordination.expand(bs, 2, 1, 1)  # (bs, 2, 1, 1)
        mask[:, 1, 2:3, :] = roach_coordination[:, 0:1, :, :].float()
        mask[:, 2, 1:2, :] = roach_coordination[:, 1:2, :, :].float()
        
    else:  # content or object_content
        # Create content masks for each communication type
        # Enemy position and health content (for Overseer triggers 1 and 3)
        enemy_content_mask = torch.zeros(obs_dim, device=obs.device, dtype=obs.dtype)
        for i in range(4):
            enemy_content_mask[feature_indices[f'enemy_{i}_rel_x']] = 1
            enemy_content_mask[feature_indices[f'enemy_{i}_rel_y']] = 1
            enemy_content_mask[feature_indices[f'enemy_{i}_health']] = 1
        
        # Enemy lost notification (simplified - use enemy availability flags)
        enemy_lost_mask = torch.zeros(obs_dim, device=obs.device, dtype=obs.dtype)
        for i in range(4):
            enemy_lost_mask[feature_indices[f'enemy_{i}_available']] = 1
        
        # Need help content (own health and approximate position)
        help_content_mask = torch.zeros(obs_dim, device=obs.device, dtype=obs.dtype)
        help_content_mask[feature_indices['own_health']] = 1
        # Add approximate position from ally data
        help_content_mask[feature_indices['ally_0_rel_x']] = 1
        help_content_mask[feature_indices['ally_0_rel_y']] = 1
        help_content_mask[feature_indices['ally_1_rel_x']] = 1
        help_content_mask[feature_indices['ally_1_rel_y']] = 1
        
        # Attack coordination content (enemy position)
        attack_content_mask = torch.zeros(obs_dim, device=obs.device, dtype=obs.dtype)
        for i in range(4):
            attack_content_mask[feature_indices[f'enemy_{i}_rel_x']] = 1
            attack_content_mask[feature_indices[f'enemy_{i}_rel_y']] = 1
        
        # Expand content masks to batch size
        enemy_content_mask = enemy_content_mask.unsqueeze(0).unsqueeze(0).unsqueeze(0).expand(bs, 1, 1, obs_dim)
        enemy_lost_mask = enemy_lost_mask.unsqueeze(0).unsqueeze(0).unsqueeze(0).expand(bs, 1, 1, obs_dim)
        help_content_mask = help_content_mask.unsqueeze(0).unsqueeze(0).unsqueeze(0).expand(bs, 1, 1, obs_dim)
        attack_content_mask = attack_content_mask.unsqueeze(0).unsqueeze(0).unsqueeze(0).expand(bs, 1, 1, obs_dim)
        
        # Agent 0 to both Roaches
        # Trigger 1: Enemy detected
        overseer_detect_cond = overseer_enemy_detected.any(dim=1, keepdim=True)  # (bs, 1)
        overseer_detect_mask = overseer_detect_cond.unsqueeze(2).unsqueeze(3).expand(bs, 1, 2, obs_dim) * enemy_content_mask
        
        # Trigger 3: Enemy critical health
        overseer_critical_cond = overseer_enemy_critical.any(dim=1, keepdim=True)  # (bs, 1)
        overseer_critical_mask = overseer_critical_cond.unsqueeze(2).unsqueeze(3).expand(bs, 1, 2, obs_dim) * enemy_content_mask
        
        # Combine Overseer communications
        overseer_mask = overseer_detect_mask + overseer_critical_mask
        if mode == 'object_content':
            # Only add if communication is happening
            overseer_comm_cond = (overseer_detect_cond | overseer_critical_cond).unsqueeze(2).unsqueeze(3).expand(bs, 1, 2, obs_dim)
            overseer_mask = overseer_mask * overseer_comm_cond.float()
        mask[:, 0, 1:3, :] = overseer_mask
        
        # Agent 1 to Overseer (enemy detection)
        roach1_detect_cond = roach1_enemy_detected.any(dim=1, keepdim=True)  # (bs, 1)
        roach1_detect_mask = roach1_detect_cond.unsqueeze(2).unsqueeze(3).expand(bs, 1, 1, obs_dim) * enemy_content_mask
        if mode == 'object_content':
            roach1_detect_mask = roach1_detect_mask * roach1_detect_cond.unsqueeze(2).unsqueeze(3).expand(bs, 1, 1, obs_dim).float()
        mask[:, 1, 0:1, :] = roach1_detect_mask
        
        # Agent 1 help request
        roach1_help_cond = roach1_low_health.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach1_help_mask = roach1_help_cond.expand(bs, 1, 2, obs_dim) * help_content_mask
        if mode == 'object_content':
            roach1_help_mask = roach1_help_mask * roach1_help_cond.expand(bs, 1, 2, obs_dim).float()
        mask[:, 1, [0, 2], :] += roach1_help_mask
        
        # Agent 2 to Overseer (enemy detection)
        roach2_detect_cond = roach2_enemy_detected.any(dim=1, keepdim=True)  # (bs, 1)
        roach2_detect_mask = roach2_detect_cond.unsqueeze(2).unsqueeze(3).expand(bs, 1, 1, obs_dim) * enemy_content_mask
        if mode == 'object_content':
            roach2_detect_mask = roach2_detect_mask * roach2_detect_cond.unsqueeze(2).unsqueeze(3).expand(bs, 1, 1, obs_dim).float()
        mask[:, 2, 0:1, :] = roach2_detect_mask
        
        # Agent 2 help request
        roach2_help_cond = roach2_low_health.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        roach2_help_mask = roach2_help_cond.expand(bs, 1, 2, obs_dim) * help_content_mask
        if mode == 'object_content':
            roach2_help_mask = roach2_help_mask * roach2_help_cond.expand(bs, 1, 2, obs_dim).float()
        mask[:, 2, [0, 1], :] += roach2_help_mask
        
        # Agent coordination (simplified)
        roach_coord_cond = (roach1_enemy_detected.any(dim=1) | roach2_enemy_detected.any(dim=1))  # (bs)
        roach_coord_cond = roach_coord_cond.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
        
        roach1_coord_mask = roach_coord_cond.expand(bs, 1, 1, obs_dim) * attack_content_mask
        roach2_coord_mask = roach_coord_cond