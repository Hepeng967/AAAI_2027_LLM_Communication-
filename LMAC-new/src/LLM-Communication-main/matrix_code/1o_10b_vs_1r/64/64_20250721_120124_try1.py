import torch
import numpy as np

def generate_mask(obs, mode='object'):
    """
    Generate communication mask based on the 1o_10b_vs_1r scenario policy.
    
    Args:
        obs: Tensor of shape (bs, n_agents, n_agents, obs_dim)
        mode: One of 'object', 'content', or 'object_content'
    
    Returns:
        mask: Tensor of shape:
            - (bs, n_agents, n_agents, 1) for 'object' mode
            - (bs, n_agents, n_agents, obs_dim) for 'content' or 'object_content' mode
    """
    bs, n_agents, _, obs_dim = obs.shape
    device = obs.device
    
    # Get indices of important observation features
    enemy_0_available_idx = 4
    enemy_0_distance_idx = 5
    enemy_0_rel_x_idx = 6
    enemy_0_rel_y_idx = 7
    own_health_idx = 80
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), device=device)
    else:
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device)
    
    # Get health thresholds (50% for Roach, 20% for Banelings)
    max_health = 100  # Assuming max health is 100
    roach_health_threshold = 0.5 * max_health
    baneling_health_threshold = 0.2 * max_health
    
    # Get agent types (Roach is agent 10, Banelings are 0-9)
    is_roach = torch.zeros(n_agents, device=device)
    is_roach[10] = 1  # Agent 10 is the Roach
    is_baneling = 1 - is_roach
    
    # Expand agent type masks for batch operations
    is_roach_exp = is_roach.view(1, 1, n_agents, 1).expand(bs, n_agents, n_agents, 1)
    is_baneling_exp = is_baneling.view(1, 1, n_agents, 1).expand(bs, n_agents, n_agents, 1)
    
    # --- Roach (agent 10) communication policies ---
    # Get Roach's observations (agent 10 is sender)
    roach_obs = obs[:, 10:11, :, :]  # shape (bs, 1, n_agents, obs_dim)
    
    # Condition 1: Roach detects enemy Baneling
    enemy_detected = (roach_obs[:, :, :, enemy_0_available_idx] > 0).float()  # shape (bs, 1, n_agents)
    enemy_detected = enemy_detected.unsqueeze(-1)  # shape (bs, 1, n_agents, 1)
    
    # Condition 2: Roach health low
    roach_health = roach_obs[:, :, :, own_health_idx]  # shape (bs, 1, n_agents)
    health_low = (roach_health < roach_health_threshold).float().unsqueeze(-1)  # shape (bs, 1, n_agents, 1)
    
    # Roach communicates to all Banelings when either condition is met
    roach_comm = ((enemy_detected + health_low) > 0).float() * is_baneling_exp
    
    # Set content for Roach communication
    if mode in ['content', 'object_content']:
        # Get position features to send
        pos_features = torch.zeros_like(mask[0, 0, 0, :])  # shape (obs_dim,)
        pos_features[enemy_0_rel_x_idx] = 1
        pos_features[enemy_0_rel_y_idx] = 1
        pos_features = pos_features.view(1, 1, 1, obs_dim).expand(bs, 1, n_agents, obs_dim)
        
        # Get health alert features to send
        health_features = torch.zeros_like(mask[0, 0, 0, :])  # shape (obs_dim,)
        health_features[own_health_idx] = 1
        health_features[enemy_0_rel_x_idx] = 1  # current position x
        health_features[enemy_0_rel_y_idx] = 1  # current position y
        health_features = health_features.view(1, 1, 1, obs_dim).expand(bs, 1, n_agents, obs_dim)
        
        # Combine content based on conditions
        roach_content = (enemy_detected * pos_features + health_low * health_features)
        roach_content = (roach_content > 0).float()
        
        if mode == 'object_content':
            roach_comm = roach_comm * roach_content
    
    # Apply Roach communication to mask
    if mode == 'object':
        mask[:, 10:11, :, :] = roach_comm
    else:
        if mode == 'content':
            # In content mode, all agents can communicate but we select content
            mask[:, 10:11, :, :] = roach_content
        else:
            mask[:, 10:11, :, :] = roach_comm
    
    # --- Baneling (agents 0-9) communication policies ---
    baneling_obs = obs[:, :10, :, :]  # shape (bs, 10, n_agents, obs_dim)
    
    # Condition 1: Baneling observes Roach
    baneling_enemy_detected = (baneling_obs[:, :, :, enemy_0_available_idx] > 0).float()  # shape (bs, 10, n_agents)
    baneling_enemy_detected = baneling_enemy_detected.unsqueeze(-1)  # shape (bs, 10, n_agents, 1)
    
    # Condition 2: Baneling within attack range (simplified to distance < threshold)
    attack_threshold = 5.0  # arbitrary distance threshold
    baneling_distance = baneling_obs[:, :, :, enemy_0_distance_idx]  # shape (bs, 10, n_agents)
    in_attack_range = (baneling_distance < attack_threshold).float().unsqueeze(-1)  # shape (bs, 10, n_agents, 1)
    
    # Condition 3: Baneling health critically low
    baneling_health = baneling_obs[:, :, :, own_health_idx]  # shape (bs, 10, n_agents)
    baneling_health_low = (baneling_health < baneling_health_threshold).float().unsqueeze(-1)  # shape (bs, 10, n_agents, 1)
    
    # Baneling communication targets (simplified to all other Banelings for broadcast)
    # For simplicity, we'll make all Banelings communicate to all other Banelings when conditions are met
    baneling_comm = ((baneling_enemy_detected + in_attack_range + baneling_health_low) > 0).float()
    
    # Set content for Baneling communication
    if mode in ['content', 'object_content']:
        # Position features
        baneling_pos_features = torch.zeros_like(mask[0, 0, 0, :])  # shape (obs_dim,)
        baneling_pos_features[enemy_0_rel_x_idx] = 1
        baneling_pos_features[enemy_0_rel_y_idx] = 1
        baneling_pos_features[enemy_0_distance_idx] = 1
        baneling_pos_features = baneling_pos_features.view(1, 1, 1, obs_dim).expand(bs, 10, n_agents, obs_dim)
        
        # Health alert features
        baneling_health_features = torch.zeros_like(mask[0, 0, 0, :])  # shape (obs_dim,)
        baneling_health_features[own_health_idx] = 1
        baneling_health_features[enemy_0_rel_x_idx] = 1  # current position x
        baneling_health_features[enemy_0_rel_y_idx] = 1  # current position y
        baneling_health_features = baneling_health_features.view(1, 1, 1, obs_dim).expand(bs, 10, n_agents, obs_dim)
        
        # Combine content based on conditions
        baneling_content = (baneling_enemy_detected * baneling_pos_features + 
                           in_attack_range * baneling_pos_features + 
                           baneling_health_low * baneling_health_features)
        baneling_content = (baneling_content > 0).float()
        
        if mode == 'object_content':
            baneling_comm = baneling_comm * baneling_content
    
    # Apply Baneling communication to mask
    if mode == 'object':
        mask[:, :10, :, :] = baneling_comm
    else:
        if mode == 'content':
            # In content mode, all agents can communicate but we select content
            mask[:, :10, :, :] = baneling_content
        else:
            mask[:, :10, :, :] = baneling_comm
    
    # Ensure no self-communication
    self_mask = 1 - torch.eye(n_agents, device=device).view(1, n_agents, n_agents, 1)
    if mode == 'object':
        mask = mask * self_mask
    else:
        mask = mask * self_mask.expand_as(mask)
    
    return mask