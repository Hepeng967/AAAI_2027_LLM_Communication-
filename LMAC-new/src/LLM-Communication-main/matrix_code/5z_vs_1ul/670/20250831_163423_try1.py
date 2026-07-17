import torch
import numpy as np

def generate_mask(obs, mode='object'):
    """
    Generate communication mask based on the specified policy.
    
    Args:
        obs: torch.Tensor of shape (bs, n_agents, n_agents, obs_dim)
        mode: one of 'object', 'content', or 'object_content'
    
    Returns:
        mask: torch.Tensor with shape depending on mode
    """
    bs, n_agents, _, obs_dim = obs.shape
    assert n_agents == 5, "Expected 5 agents"
    assert obs_dim == 35, "Expected 35 observation dimensions"
    
    # Constants
    attack_range_threshold = 6.0  # Example value, adjust based on unit stats
    safe_distance_threshold = 3.0  # Example value, adjust based on splash radius
    health_threshold = 0.5  # 50% health
    
    # Get observation indices
    obs_feature_names = [
        'move_north', 'move_south', 'move_east', 'move_west', 'enemy_0_available',
        'enemy_0_distance', 'enemy_0_rel_x', 'enemy_0_rel_y', 'enemy_0_health',
        'ally_0_visible', 'ally_0_distance', 'ally_0_rel_x', 'ally_0_rel_y', 'ally_0_health', 'ally_0_shield',
        'ally_1_visible', 'ally_1_distance', 'ally_1_rel_x', 'ally_1_rel_y', 'ally_1_health', 'ally_1_shield',
        'ally_2_visible', 'ally_2_distance', 'ally_2_rel_x', 'ally_2_rel_y', 'ally_2_health', 'ally_2_shield',
        'ally_3_visible', 'ally_3_distance', 'ally_3_rel_x', 'ally_3_rel_y', 'ally_3_health', 'ally_3_shield',
        'own_health', 'own_shield'
    ]
    
    # Create index mapping
    idx_map = {name: i for i, name in enumerate(obs_feature_names)}
    
    # Initialize masks
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), dtype=torch.float32, device=obs.device)
    else:
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=obs.device)
    
    # Extract relevant features for all agents
    enemy_distance = obs[:, :, :, idx_map['enemy_0_distance']]
    own_health = obs[:, :, :, idx_map['own_health']]
    
    # For each agent, get its own observation (diagonal elements)
    own_obs = torch.diagonal(obs, dim1=1, dim2=2).permute(0, 2, 1)  # (bs, n_agents, obs_dim)
    
    # Extract self features
    self_enemy_distance = own_obs[:, :, idx_map['enemy_0_distance']]  # (bs, n_agents)
    self_own_health = own_obs[:, :, idx_map['own_health']]  # (bs, n_agents)
    
    # Extract ally distances for each agent
    ally_distances = []
    for i in range(n_agents):
        if i == 0:
            ally_distances.append(own_obs[:, :, idx_map['ally_0_distance']].unsqueeze(2))  # (bs, n_agents, 1)
        elif i == 1:
            ally_distances.append(own_obs[:, :, idx_map['ally_1_distance']].unsqueeze(2))  # (bs, n_agents, 1)
        elif i == 2:
            ally_distances.append(own_obs[:, :, idx_map['ally_2_distance']].unsqueeze(2))  # (bs, n_agents, 1)
        elif i == 3:
            ally_distances.append(own_obs[:, :, idx_map['ally_3_distance']].unsqueeze(2))  # (bs, n_agents, 1)
    
    ally_distances = torch.cat(ally_distances, dim=2)  # (bs, n_agents, 4)
    
    # Condition 1: Enemy in attack range and no recent communication
    condition1 = (self_enemy_distance < attack_range_threshold).unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
    
    # Condition 2: Low health and enemy targeting (simplified: enemy is close)
    condition2 = ((self_own_health < health_threshold) & 
                 (self_enemy_distance < attack_range_threshold * 1.5)).unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
    
    # Condition 3: Allies too close and enemy near
    too_close = (ally_distances < safe_distance_threshold)  # (bs, n_agents, 4)
    two_or_more_too_close = (too_close.sum(dim=2) >= 2).unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
    enemy_near = (self_enemy_distance < attack_range_threshold * 2).unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
    condition3 = two_or_more_too_close & enemy_near
    
    # For condition 2: Find nearest ally for each agent
    # Replace infinite distances with large values
    ally_distances_masked = ally_distances.clone()
    ally_distances_masked[ally_distances_masked == 0] = float('inf')  # Ignore self (distance 0)
    
    nearest_ally_idx = torch.argmin(ally_distances_masked, dim=2)  # (bs, n_agents)
    
    # Create one-hot encoding for nearest allies
    nearest_ally_mask = torch.zeros((bs, n_agents, n_agents), dtype=torch.float32, device=obs.device)
    for b in range(bs):
        for i in range(n_agents):
            if nearest_ally_idx[b, i] < n_agents - 1:  # Valid nearest ally
                target_idx = nearest_ally_idx[b, i] + (1 if nearest_ally_idx[b, i] >= i else 0)
                if target_idx < n_agents:
                    nearest_ally_mask[b, i, target_idx] = 1.0
    
    nearest_ally_mask = nearest_ally_mask.unsqueeze(3)  # (bs, n_agents, n_agents, 1)
    
    # For condition 3: Create mask for allies that are too close
    too_close_mask = torch.zeros((bs, n_agents, n_agents), dtype=torch.float32, device=obs.device)
    for i in range(n_agents):
        for j in range(4):  # 4 allies
            if j < i:  # Ally index mapping
                target_idx = j
            else:
                target_idx = j + 1
            
            if target_idx < n_agents:
                too_close_mask[:, i, target_idx] = too_close[:, i, j]
    
    too_close_mask = too_close_mask.unsqueeze(3)  # (bs, n_agents, n_agents, 1)
    
    # Apply conditions to object mask
    object_mask = torch.zeros((bs, n_agents, n_agents, 1), dtype=torch.float32, device=obs.device)
    
    # Condition 1: Communicate with all allies
    all_allies_mask = torch.ones((bs, n_agents, n_agents, 1), dtype=torch.float32, device=obs.device)
    for i in range(n_agents):
        all_allies_mask[:, i, i, 0] = 0  # Don't communicate with self
    
    object_mask = object_mask + (condition1 * all_allies_mask)
    
    # Condition 2: Communicate with nearest ally
    object_mask = object_mask + (condition2 * nearest_ally_mask)
    
    # Condition 3: Communicate with allies that are too close
    object_mask = object_mask + (condition3 * too_close_mask)
    
    # Clip to 0-1 range (in case multiple conditions trigger)
    object_mask = torch.clamp(object_mask, 0, 1)
    
    if mode == 'object':
        return object_mask
    
    # For content modes, create content masks
    if mode in ['content', 'object_content']:
        # Create content selection based on conditions
        content_mask = torch.zeros((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=obs.device)
        
        # Condition 1 content: enemy position
        enemy_x_idx = idx_map['enemy_0_rel_x']
        enemy_y_idx = idx_map['enemy_0_rel_y']
        condition1_content = torch.zeros((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=obs.device)
        condition1_content[:, :, :, enemy_x_idx] = 1.0
        condition1_content[:, :, :, enemy_y_idx] = 1.0
        
        # Condition 2 content: self position (approximated from relative observations)
        # Use relative positions to allies to estimate absolute position
        condition2_content = torch.zeros((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=obs.device)
        # For simplicity, we'll use relative positions to the nearest ally
        condition2_content[:, :, :, enemy_x_idx] = 1.0  # Use enemy position as proxy
        condition2_content[:, :, :, enemy_y_idx] = 1.0
        
        # Condition 3 content: simple warning message (no specific content)
        condition3_content = torch.ones((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=obs.device)
        
        # Apply content based on conditions
        condition1_expanded = condition1.expand(-1, -1, n_agents, obs_dim)
        condition2_expanded = condition2.expand(-1, -1, n_agents, obs_dim)
        condition3_expanded = condition3.expand(-1, -1, n_agents, obs_dim)
        
        content_mask = content_mask + (condition1_expanded * condition1_content)
        content_mask = content_mask + (condition2_expanded * condition2_content)
        content_mask = content_mask + (condition3_expanded * condition3_content)
        
        if mode == 'content':
            # In content mode, all agents can communicate but content is selected
            communication_possible = torch.ones((bs, n_agents, n_agents, 1), dtype=torch.float32, device=obs.device)
            for i in range(n_agents):
                communication_possible[:, i, i, 0] = 0  # Don't communicate with self
            
            communication_possible = communication_possible.expand(-1, -1, -1, obs_dim)
            return content_mask * communication_possible
        
        elif mode == 'object_content':
            # In object_content mode, combine object and content selection
            object_mask_expanded = object_mask.expand(-1, -1, -1, obs_dim)
            return content_mask * object_mask_expanded
    
    return mask