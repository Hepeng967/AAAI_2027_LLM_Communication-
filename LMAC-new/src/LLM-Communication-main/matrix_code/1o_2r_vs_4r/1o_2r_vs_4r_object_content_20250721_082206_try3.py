import torch

def generate_mask(obs, mode='object'):
    assert mode in ['object', 'content', 'object_content']
    bs, n_agents, _, obs_dim = obs.shape
    assert n_agents == 3  # Only supports 3 agents (Overseer + 2 Roaches)
    
    # Create base masks with proper shapes
    object_mask = torch.zeros((bs, n_agents, n_agents, 1), device=obs.device)
    content_mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=obs.device)
    
    # Get indices for relevant observation features
    enemy_available_indices = [4, 11, 18, 25]
    enemy_distance_indices = [5, 12, 19, 26]
    enemy_rel_x_indices = [6, 13, 20, 27]
    enemy_rel_y_indices = [7, 14, 21, 28]
    ally_health_indices = [36, 44]
    ally_visible_indices = [32, 39]
    own_health_index = 45
    ally_rel_x_indices = [34, 41]
    ally_rel_y_indices = [35, 42]
    
    # ---------------------------
    # Overseer (Agent 0) Policies
    # ---------------------------
    
    # Trigger Condition 1: Any enemy detected
    any_enemy_detected = (obs[:, 0, 0, enemy_available_indices].sum(dim=-1) > 0).float()  # (bs,)
    any_enemy_detected = any_enemy_detected.view(bs, 1, 1, 1).expand(-1, 1, n_agents, 1)  # (bs, 1, 3, 1)
    
    # Targets: Agent 1 and 2
    overseer_targets = torch.zeros((bs, n_agents, 1), device=obs.device)
    overseer_targets[:, 1, 0] = 1  # Agent 1
    overseer_targets[:, 2, 0] = 1  # Agent 2
    overseer_targets = overseer_targets.unsqueeze(1)  # (bs, 1, 3, 1)
    
    # Add to object mask
    object_mask[:, 0:1, :, :] += any_enemy_detected * overseer_targets
    
    # Content for enemy detection (rel_x, rel_y, distance for all available enemies)
    enemy_content_mask = torch.zeros((bs, 1, 1, obs_dim), device=obs.device)
    for idx in enemy_rel_x_indices + enemy_rel_y_indices + enemy_distance_indices:
        enemy_content_mask[:, :, :, idx] = 1
    enemy_content_mask = enemy_content_mask.expand(-1, 1, n_agents, -1)  # (bs, 1, 3, obs_dim)
    content_mask[:, 0:1, :, :] += any_enemy_detected * overseer_targets * enemy_content_mask
    
    # Trigger Condition 2: Ally health below threshold (50%)
    ally_health = obs[:, 0, 0, ally_health_indices]  # (bs, 2)
    ally_health_low = (ally_health < 0.5).float()  # (bs, 2)
    
    # For each low-health ally, communicate to both that ally and the other roach
    # Ally 0 (Agent 1) health low
    ally0_low = ally_health_low[:, 0].view(bs, 1, 1, 1).expand(-1, 1, n_agents, 1)  # (bs, 1, 3, 1)
    targets_ally0_low = torch.zeros((bs, n_agents, 1), device=obs.device)
    targets_ally0_low[:, 1, 0] = 1  # Agent 1 (the injured)
    targets_ally0_low[:, 2, 0] = 1  # Agent 2 (the other roach)
    targets_ally0_low = targets_ally0_low.unsqueeze(1)  # (bs, 1, 3, 1)
    
    # Ally 1 (Agent 2) health low
    ally1_low = ally_health_low[:, 1].view(bs, 1, 1, 1).expand(-1, 1, n_agents, 1)  # (bs, 1, 3, 1)
    targets_ally1_low = torch.zeros((bs, n_agents, 1), device=obs.device)
    targets_ally1_low[:, 0, 0] = 1  # Agent 0 (Overseer)
    targets_ally1_low[:, 1, 0] = 1  # Agent 1 (the other roach)
    targets_ally1_low = targets_ally1_low.unsqueeze(1)  # (bs, 1, 3, 1)
    
    # Add to object mask
    object_mask[:, 0:1, :, :] += ally0_low * targets_ally0_low
    object_mask[:, 0:1, :, :] += ally1_low * targets_ally1_low
    
    # Content for low health (ally position and health)
    low_health_content = torch.zeros((bs, 1, 1, obs_dim), device=obs.device)
    for idx in ally_rel_x_indices + ally_rel_y_indices + ally_health_indices:
        low_health_content[:, :, :, idx] = 1
    low_health_content = low_health_content.expand(-1, 1, n_agents, -1)  # (bs, 1, 3, obs_dim)
    content_mask[:, 0:1, :, :] += (ally0_low * targets_ally0_low + ally1_low * targets_ally1_low) * low_health_content
    
    # Trigger Condition 3: Multiple enemies detected (>=2)
    num_enemies_detected = (obs[:, 0, 0, enemy_available_indices].sum(dim=-1) >= 2).float().view(bs, 1, 1, 1).expand(-1, 1, n_agents, 1)  # (bs, 1, 3, 1)
    object_mask[:, 0:1, :, :] += num_enemies_detected * overseer_targets
    content_mask[:, 0:1, :, :] += num_enemies_detected * overseer_targets * enemy_content_mask
    
    # ---------------------------
    # Roach 1 (Agent 1) Policies
    # ---------------------------
    
    # Trigger Condition 1: Own health drops significantly
    health_drop = (obs[:, 1, 1, own_health_index] < 0.5).float().view(bs, 1, 1, 1).expand(-1, 1, n_agents, 1)  # (bs, 1, 3, 1)
    roach1_targets = torch.zeros((bs, n_agents, 1), device=obs.device)
    roach1_targets[:, 0, 0] = 1  # Overseer
    roach1_targets[:, 2, 0] = 1  # Other roach
    roach1_targets = roach1_targets.unsqueeze(1)  # (bs, 1, 3, 1)
    
    object_mask[:, 1:2, :, :] += health_drop * roach1_targets
    
    # Content for health drop (own position and health)
    health_drop_content = torch.zeros((bs, 1, 1, obs_dim), device=obs.device)
    health_drop_content[:, :, :, own_health_index] = 1
    health_drop_content[:, :, :, ally_rel_x_indices[0]] = 1  # Agent 1's own rel_x
    health_drop_content[:, :, :, ally_rel_y_indices[0]] = 1  # Agent 1's own rel_y
    health_drop_content = health_drop_content.expand(-1, 1, n_agents, -1)  # (bs, 1, 3, obs_dim)
    content_mask[:, 1:2, :, :] += health_drop * roach1_targets * health_drop_content
    
    # Trigger Condition 2: Lose sight of other roach
    ally1_visible = obs[:, 1, 1, ally_visible_indices[1]].view(bs, 1, 1, 1).expand(-1, 1, n_agents, 1)  # (bs, 1, 3, 1)
    lose_sight = (ally1_visible < 1).float()
    roach1_target_single = torch.zeros((bs, n_agents, 1), device=obs.device)
    roach1_target_single[:, 2, 0] = 1  # Other roach
    roach1_target_single = roach1_target_single.unsqueeze(1)  # (bs, 1, 3, 1)
    
    object_mask[:, 1:2, :, :] += lose_sight * roach1_target_single
    
    # Content for position request (empty message)
    content_mask[:, 1:2, :, :] += lose_sight * roach1_target_single * torch.zeros((bs, 1, 3, obs_dim), device=obs.device)
    
    # Trigger Condition 3: Detect enemy without Overseer guidance
    any_enemy_detected_roach1 = (obs[:, 1, 1, enemy_available_indices].sum(dim=-1) > 0).float().view(bs, 1, 1, 1).expand(-1, 1, n_agents, 1)  # (bs, 1, 3, 1)
    object_mask[:, 1:2, :, :] += any_enemy_detected_roach1 * roach1_targets
    content_mask[:, 1:2, :, :] += any_enemy_detected_roach1 * roach1_targets * enemy_content_mask.expand(-1, 1, n_agents, -1)
    
    # ---------------------------
    # Roach 2 (Agent 2) Policies
    # ---------------------------
    
    # Mirror of Roach 1's policies
    
    # Trigger Condition 1: Own health drops significantly
    health_drop = (obs[:, 2, 2, own_health_index] < 0.5).float().view(bs, 1, 1, 1).expand(-1, 1, n_agents, 1)  # (bs, 1, 3, 1)
    roach2_targets = torch.zeros((bs, n_agents, 1), device=obs.device)
    roach2_targets[:, 0, 0] = 1  # Overseer
    roach2_targets[:, 1, 0] = 1  # Other roach
    roach2_targets = roach2_targets.unsqueeze(1)  # (bs, 1, 3, 1)
    
    object_mask[:, 2:3, :, :] += health_drop * roach2_targets
    
    # Content for health drop (own position and health)
    health_drop_content = torch.zeros((bs, 1, 1, obs_dim), device=obs.device)
    health_drop_content[:, :, :, own_health_index] = 1
    health_drop_content[:, :, :, ally_rel_x_indices[1]] = 1  # Agent 2's own rel_x
    health_drop_content[:, :, :, ally_rel_y_indices[1]] = 1  # Agent 2's own rel_y
    health_drop_content = health_drop_content.expand(-1, 1, n_agents, -1)  # (bs, 1, 3, obs_dim)
    content_mask[:, 2:3, :, :] += health_drop * roach2_targets * health_drop_content
    
    # Trigger Condition 2: Lose sight of other roach
    ally0_visible = obs[:, 2, 2, ally_visible_indices[0]].view(bs, 1, 1, 1).expand(-1, 1, n_agents, 1)  # (bs, 1, 3, 1)
    lose_sight = (ally0_visible < 1).float()
    roach2_target_single = torch.zeros((bs, n_agents, 1), device=obs.device)
    roach2_target_single[:, 1, 0] = 1  # Other roach
    roach2_target_single = roach2_target_single.unsqueeze(1)  # (bs, 1, 3, 1)
    
    object_mask[:, 2:3, :, :] += lose_sight * roach2_target_single
    
    # Content for position request (empty message)
    content_mask[:, 2:3, :, :] += lose_sight * roach2_target_single * torch.zeros((bs, 1, 3, obs_dim), device=obs.device)
    
    # Trigger Condition 3: Detect enemy without Overseer guidance
    any_enemy_detected_roach2 = (obs[:, 2, 2, enemy_available_indices].sum(dim=-1) > 0).float().view(bs, 1, 1, 1).expand(-1, 1, n_agents, 1)  # (bs, 1, 3, 1)
    object_mask[:, 2:3, :, :] += any_enemy_detected_roach2 * roach2_targets
    content_mask[:, 2:3, :, :] += any_enemy_detected_roach2 * roach2_targets * enemy_content_mask.expand(-1, 1, n_agents, -1)
    
    # ---------------------------
    # Final mask construction
    # ---------------------------
    
    if mode == 'object':
        return object_mask
    elif mode == 'content':
        # In content mode, all agents can communicate but content is selected
        comm_allowed = torch.ones((bs, n_agents, n_agents, 1), device=obs.device)
        return comm_allowed * content_mask
    elif mode == 'object_content':
        # In object_content mode, only selected agents can communicate with selected content
        return object_mask * content_mask
    
    return torch.zeros_like(obs)  # fallback



