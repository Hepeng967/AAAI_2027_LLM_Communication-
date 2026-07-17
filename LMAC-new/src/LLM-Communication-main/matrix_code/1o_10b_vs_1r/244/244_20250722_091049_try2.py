import torch

def generate_mask(obs, mode='object'):
    assert mode in ['object', 'content', 'object_content'], "Invalid mode"
    bs, n_agents, _, obs_dim = obs.shape
    device = obs.device
    
    # Define observation feature names
    obs_feature_names = ['move_north', 'move_south', 'move_east', 'move_west', 'enemy_0_available', 
                        'enemy_0_distance', 'enemy_0_rel_x', 'enemy_0_rel_y', 'enemy_0_health', 
                        'enemy_0_type_0', 'enemy_0_type_1', 'ally_0_visible', 'ally_0_distance', 
                        'ally_0_rel_x', 'ally_0_rel_y', 'ally_0_health', 'ally_0_type_0', 
                        'ally_0_type_1', 'ally_1_visible', 'ally_1_distance', 'ally_1_rel_x', 
                        'ally_1_rel_y', 'ally_1_health', 'ally_1_type_0', 'ally_1_type_1', 
                        'ally_2_visible', 'ally_2_distance', 'ally_2_rel_x', 'ally_2_rel_y', 
                        'ally_2_health', 'ally_2_type_0', 'ally_2_type_1', 'ally_3_visible', 
                        'ally_3_distance', 'ally_3_rel_x', 'ally_3_rel_y', 'ally_3_health', 
                        'ally_3_type_0', 'ally_3_type_1', 'ally_4_visible', 'ally_4_distance', 
                        'ally_4_rel_x', 'ally_4_rel_y', 'ally_4_health', 'ally_4_type_0', 
                        'ally_4_type_1', 'ally_5_visible', 'ally_5_distance', 'ally_5_rel_x', 
                        'ally_5_rel_y', 'ally_5_health', 'ally_5_type_0', 'ally_5_type_1', 
                        'ally_6_visible', 'ally_6_distance', 'ally_6_rel_x', 'ally_6_rel_y', 
                        'ally_6_health', 'ally_6_type_0', 'ally_6_type_1', 'ally_7_visible', 
                        'ally_7_distance', 'ally_7_rel_x', 'ally_7_rel_y', 'ally_7_health', 
                        'ally_7_type_0', 'ally_7_type_1', 'ally_8_visible', 'ally_8_distance', 
                        'ally_8_rel_x', 'ally_8_rel_y', 'ally_8_health', 'ally_8_type_0', 
                        'ally_8_type_1', 'ally_9_visible', 'ally_9_distance', 'ally_9_rel_x', 
                        'ally_9_rel_y', 'ally_9_health', 'ally_9_type_0', 'ally_9_type_1', 
                        'own_health', 'own_type_0', 'own_type_1']
    
    # Create base masks with proper shapes
    object_mask = torch.zeros((bs, n_agents, n_agents, 1), device=device)
    content_mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device)
    
    # Get indices for important observation features
    enemy_0_available_idx = obs_feature_names.index('enemy_0_available')
    enemy_0_distance_idx = obs_feature_names.index('enemy_0_distance')
    enemy_0_rel_x_idx = obs_feature_names.index('enemy_0_rel_x')
    enemy_0_rel_y_idx = obs_feature_names.index('enemy_0_rel_y')
    own_health_idx = obs_feature_names.index('own_health')
    
    # Extract relevant features from observations
    enemy_0_available = obs[..., enemy_0_available_idx].unsqueeze(-1)  # (bs, n_agents, n_agents, 1)
    enemy_0_distance = obs[..., enemy_0_distance_idx].unsqueeze(-1)    # (bs, n_agents, n_agents, 1)
    enemy_0_rel_x = obs[..., enemy_0_rel_x_idx].unsqueeze(-1)          # (bs, n_agents, n_agents, 1)
    enemy_0_rel_y = obs[..., enemy_0_rel_y_idx].unsqueeze(-1)          # (bs, n_agents, n_agents, 1)
    own_health = obs[..., own_health_idx].unsqueeze(-1)                # (bs, n_agents, n_agents, 1)
    
    # Overseer is agent 10 (index 10)
    overseer_idx = 10
    baneling_indices = torch.tensor([i for i in range(n_agents) if i != overseer_idx], device=device)
    
    # Thresholds
    health_threshold = 0.2  # 20% health threshold
    distance_threshold = 5.0  # arbitrary distance threshold for nearby agents
    
    # --------------------------
    # Overseer communication logic
    # --------------------------
    # Overseer detects Roach (Condition 1)
    overseer_roach_detected = (enemy_0_available[:, overseer_idx:overseer_idx+1, :, :] > 0.5).float()  # (bs, 1, n_agents, 1)
    
    # Overseer detects injured Baneling (Condition 2)
    ally_healths = torch.stack([obs[:, overseer_idx, :, obs_feature_names.index(f'ally_{i}_health')] 
                              for i in range(n_agents-1)], dim=-1)  # (bs, n_agents, n_agents-1)
    injured_banelings = (ally_healths[:, overseer_idx, :] < health_threshold).float()  # (bs, n_agents-1)
    injured_banelings = injured_banelings.unsqueeze(1).unsqueeze(-1)  # (bs, 1, n_agents-1, 1)
    
    # --------------------------
    # Baneling communication logic
    # --------------------------
    # Baneling detects Roach (Condition 1)
    baneling_roach_detected = (enemy_0_available[:, baneling_indices, :, :] > 0.5).float()  # (bs, n_agents-1, n_agents, 1)
    
    # Baneling low health (Condition 2)
    baneling_low_health = (own_health[:, baneling_indices, :, :] < health_threshold).float()  # (bs, n_agents-1, n_agents, 1)
    
    # --------------------------
    # Build communication masks
    # --------------------------
    
    # Overseer to Banelings (Roach detected)
    object_mask[:, overseer_idx:overseer_idx+1, baneling_indices, :] = overseer_roach_detected[:, :, baneling_indices, :]
    
    # Content for Overseer to Banelings (Roach position)
    roach_content_indices = [enemy_0_rel_x_idx, enemy_0_rel_y_idx, enemy_0_distance_idx]
    content_mask[:, overseer_idx:overseer_idx+1, baneling_indices, roach_content_indices] = \
        overseer_roach_detected[:, :, baneling_indices, :].expand(-1, -1, -1, len(roach_content_indices))
    
    # Banelings to other Banelings (Roach detected)
    broadcast_mask = torch.ones((bs, n_agents-1, n_agents, 1), device=device)
    object_mask[:, baneling_indices, :, :] = baneling_roach_detected * broadcast_mask
    
    # Content for Banelings to Banelings (Roach position)
    content_mask[:, baneling_indices, :, roach_content_indices] = \
        baneling_roach_detected.expand(-1, -1, -1, len(roach_content_indices)) * \
        broadcast_mask.expand(-1, -1, -1, len(roach_content_indices))
    
    # Banelings to Overseer (Path blocked - simplified as health check)
    object_mask[:, baneling_indices, overseer_idx:overseer_idx+1, :] = baneling_low_health[:, :, overseer_idx:overseer_idx+1, :]
    
    # --------------------------
    # Return mask based on mode
    # --------------------------
    if mode == 'object':
        return object_mask
    elif mode == 'content':
        return content_mask
    elif mode == 'object_content':
        # Combine object and content masks
        combined_mask = content_mask * object_mask.expand(-1, -1, -1, obs_dim)
        return combined_mask

# Test case
if __name__ == "__main__":
    obs = torch.randn(2, 11, 11, 84)  # bs=2, n_agents=11, obs_dim=84
    mask = generate_mask(obs, mode='object_content')
    print(mask.shape)  # Should be (2, 11, 11, 84)