import torch

def generate_mask(obs, mode='object'):
    """
    Generate communication mask based on MMM2 scenario policy.
    
    Args:
        obs: Tensor of shape (bs, n_agents, n_agents, obs_dim)
        mode: One of 'object', 'content', or 'object_content'
    
    Returns:
        mask: Tensor of shape:
            - (bs, n_agents, n_agents, 1) for 'object' mode
            - (bs, n_agents, n_agents, obs_dim) for 'content' and 'object_content' modes
    """
    bs, n_agents, _, obs_dim = obs.shape
    
    # Initialize masks based on mode
    if mode == 'object':
        object_mask = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device, dtype=torch.float32)
        content_mask = None
    elif mode == 'content':
        object_mask = torch.ones(bs, n_agents, n_agents, 1, device=obs.device, dtype=torch.float32)
        content_mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device, dtype=torch.float32)
    elif mode == 'object_content':
        object_mask = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device, dtype=torch.float32)
        content_mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device, dtype=torch.float32)
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    # Extract observation features - using indices from provided feature names
    # Agent types: 0=Medivac, 1=Marine
    agent_types = torch.zeros(bs, n_agents, device=obs.device, dtype=torch.long)
    for i in range(n_agents):
        type_0_idx = 19  # own_type_0
        type_1_idx = 20  # own_type_1
        agent_types[:, i] = (obs[:, i, 0, type_1_idx] > 0.5).long()  # Marine if type_1 > 0.5
    
    # Health related indices
    own_health_idx = 18  # own_health
    ally_health_idx = 15  # ally_0_health
    
    # Enemy detection indices
    enemy_available_idx = 4   # enemy_0_available
    enemy_distance_idx = 5    # enemy_0_distance
    enemy_rel_x_idx = 6       # enemy_0_rel_x
    enemy_rel_y_idx = 7       # enemy_0_rel_y
    enemy_health_idx = 8      # enemy_0_health
    enemy_type_0_idx = 9      # enemy_0_type_0 (Medivac)
    enemy_type_1_idx = 10     # enemy_0_type_1 (Marauder)
    
    # Ally position indices
    ally_rel_x_idx = 13       # ally_0_rel_x
    ally_rel_y_idx = 14       # ally_0_rel_y
    
    # ===== AGENT 0 (MEDIVAC) COMMUNICATION POLICY =====
    medivac_idx = 0
    
    # Trigger Condition 1: Enemy units within attack range (distance < 6)
    enemy_close = (obs[:, :, :, enemy_available_idx] > 0.5) & (obs[:, :, :, enemy_distance_idx] < 6.0)
    enemy_close_any = torch.any(enemy_close, dim=2)  # Shape: (bs, n_agents)
    medivac_enemy_close = enemy_close_any[:, medivac_idx].unsqueeze(1)  # Shape: (bs, 1)
    
    # Trigger Condition 2: Any ally health below 50%
    ally_health_low = (obs[:, :, :, ally_health_idx] < 0.5) & (obs[:, :, :, ally_health_idx] > 0.0)
    ally_health_low_any = torch.any(ally_health_low, dim=2)  # Shape: (bs, n_agents)
    medivac_ally_low_health = ally_health_low_any[:, medivac_idx].unsqueeze(1)  # Shape: (bs, 1)
    
    # Trigger Condition 3: Enemy Medivac detected
    enemy_medivac_detected = (obs[:, :, :, enemy_type_0_idx] > 0.5) & (obs[:, :, :, enemy_available_idx] > 0.5)
    enemy_medivac_any = torch.any(enemy_medivac_detected, dim=2)  # Shape: (bs, n_agents)
    medivac_enemy_medivac = enemy_medivac_any[:, medivac_idx].unsqueeze(1)  # Shape: (bs, 1)
    
    # Medivac communicates to all Marines (agents 1-7) when any trigger condition is met
    medivac_communicates = (medivac_enemy_close | medivac_ally_low_health | medivac_enemy_medivac)  # Shape: (bs, 1)
    
    # Create target mask for Marines (agents 1-7)
    marine_targets = torch.zeros(bs, n_agents, device=obs.device, dtype=torch.bool)
    if n_agents > 1:
        marine_targets[:, 1:min(8, n_agents)] = True
    
    # Expand shapes for assignment - using proper type conversion
    medivac_comm_expanded = medivac_communicates.float().unsqueeze(2).unsqueeze(3)  # Shape: (bs, 1, 1, 1)
    marine_targets_expanded = marine_targets.unsqueeze(1).unsqueeze(3).float()  # Shape: (bs, 1, n_agents, 1)
    
    # Apply Medivac communication - use addition instead of bitwise OR for float tensors
    if mode in ['object', 'object_content']:
        medivac_comm_mask = (medivac_comm_expanded * marine_targets_expanded).clamp(0, 1)
        object_mask[:, medivac_idx:medivac_idx+1, :, :] += medivac_comm_mask
        object_mask[:, medivac_idx:medivac_idx+1, :, :] = object_mask[:, medivac_idx:medivac_idx+1, :, :].clamp(0, 1)
    
    if mode in ['content', 'object_content']:
        # For content modes, set specific message content
        content_trigger = medivac_communicates.float().unsqueeze(2).unsqueeze(3).unsqueeze(4)  # Shape: (bs, 1, 1, 1, 1)
        marine_targets_content = marine_targets.unsqueeze(1).unsqueeze(3).unsqueeze(4).float()  # Shape: (bs, 1, n_agents, 1, 1)
        
        # Set content based on triggers - using first few dimensions as message indicators
        content_comm_mask = (content_trigger * marine_targets_content).expand(bs, 1, n_agents, obs_dim)
        
        if mode == 'content':
            content_mask[:, medivac_idx:medivac_idx+1, :, :] = content_comm_mask
        else:  # object_content mode
            content_mask[:, medivac_idx:medivac_idx+1, :, :] = content_comm_mask
    
    # ===== AGENTS 1-7 (MARINES) COMMUNICATION POLICY =====
    marine_mask = (agent_types == 1)  # Shape: (bs, n_agents)
    
    for marine_idx in range(1, min(8, n_agents)):
        if not torch.any(marine_mask[:, marine_idx]):
            continue
            
        # Trigger Condition 1: Enemy units first detected (distance < 10)
        marine_enemy_detected = (obs[:, marine_idx, :, enemy_available_idx] > 0.5) & (obs[:, marine_idx, :, enemy_distance_idx] < 10.0)
        marine_enemy_any = torch.any(marine_enemy_detected, dim=1).unsqueeze(1)  # Shape: (bs, 1)
        
        # Trigger Condition 2: Own health drops below 40%
        marine_low_health = (obs[:, marine_idx, 0, own_health_idx] < 0.4).unsqueeze(1)  # Shape: (bs, 1)
        
        # For low health, find nearest 2 Marine allies (excluding self and Medivac)
        if torch.any(marine_low_health):
            # Calculate distances to other agents
            ally_distances = obs[:, marine_idx, :, 12]  # ally_0_distance index 12
            # Create mask for valid Marine allies (not self, not Medivac)
            valid_allies = marine_mask.clone()
            valid_allies[:, marine_idx] = False  # Exclude self
            valid_allies[:, 0] = False  # Exclude Medivac
            
            # Get indices of nearest 2 Marine allies
            large_dist = 1000.0
            dist_with_invalid = ally_distances.clone()
            dist_with_invalid[~valid_allies] = large_dist
            
            # Find top 2 closest allies
            _, top2_indices = torch.topk(dist_with_invalid, k=min(2, n_agents-2), dim=1, largest=False)
            
            # Create target mask for nearest allies
            nearest_allies = torch.zeros(bs, n_agents, device=obs.device, dtype=torch.bool)
            for b in range(bs):
                for k in range(min(2, n_agents-2)):
                    if top2_indices[b, k] < n_agents:
                        nearest_allies[b, top2_indices[b, k]] = True
        else:
            nearest_allies = torch.zeros(bs, n_agents, device=obs.device, dtype=torch.bool)
        
        # Always include Medivac for low health condition
        low_health_targets = nearest_allies.clone()
        low_health_targets[:, 0] = True  # Include Medivac
        
        # Trigger Condition 3: Enemy Marauder detected
        enemy_marauder_detected = (obs[:, marine_idx, :, enemy_type_1_idx] > 0.5) & (obs[:, marine_idx, :, enemy_available_idx] > 0.5)
        marine_enemy_marauder = torch.any(enemy_marauder_detected, dim=1).unsqueeze(1)  # Shape: (bs, 1)
        
        # Trigger Condition 4: Multiple enemies focusing fire (simplified: any enemy attacking)
        marine_under_fire = marine_enemy_any  # Simplified condition
        
        # Trigger Condition 5: Enemy Medivac detected  
        marine_enemy_medivac_detected = (obs[:, marine_idx, :, enemy_type_0_idx] > 0.5) & (obs[:, marine_idx, :, enemy_available_idx] > 0.5)
        marine_enemy_medivac = torch.any(marine_enemy_medivac_detected, dim=1).unsqueeze(1)  # Shape: (bs, 1)
        
        # Marine communication triggers
        marine_comm_all = (marine_enemy_any | marine_enemy_marauder | marine_under_fire | marine_enemy_medivac)  # Shape: (bs, 1)
        marine_comm_low_health = marine_low_health  # Shape: (bs, 1)
        
        # Create target masks
        all_other_agents = torch.ones(bs, n_agents, device=obs.device, dtype=torch.bool)
        all_other_agents[:, marine_idx] = False  # Exclude self
        
        # Expand shapes for assignment - convert to float for operations
        marine_comm_all_expanded = marine_comm_all.float().unsqueeze(2).unsqueeze(3)  # Shape: (bs, 1, 1, 1)
        marine_comm_low_health_expanded = marine_comm_low_health.float().unsqueeze(2).unsqueeze(3)  # Shape: (bs, 1, 1, 1)
        
        all_targets_expanded = all_other_agents.unsqueeze(1).unsqueeze(3).float()  # Shape: (bs, 1, n_agents, 1)
        low_health_targets_expanded = low_health_targets.unsqueeze(1).unsqueeze(3).float()  # Shape: (bs, 1, n_agents, 1)
        
        # Apply Marine communication for object modes - use multiplication instead of bitwise operations
        if mode in ['object', 'object_content']:
            # Communications to all other agents
            comm_all_mask = (marine_comm_all_expanded * all_targets_expanded).clamp(0, 1)
            object_mask[:, marine_idx:marine_idx+1, :, :] += comm_all_mask
            
            # Low health communication to specific targets
            comm_low_health_mask = (marine_comm_low_health_expanded * low_health_targets_expanded).clamp(0, 1)
            object_mask[:, marine_idx:marine_idx+1, :, :] += comm_low_health_mask
            
            # Clamp to ensure values are 0 or 1
            object_mask[:, marine_idx:marine_idx+1, :, :] = object_mask[:, marine_idx:marine_idx+1, :, :].clamp(0, 1)
        
        # Apply Marine communication for content modes
        if mode in ['content', 'object_content']:
            # Expand for content dimensions
            marine_comm_all_content = marine_comm_all.float().unsqueeze(2).unsqueeze(3).unsqueeze(4)  # Shape: (bs, 1, 1, 1, 1)
            marine_comm_low_health_content = marine_comm_low_health.float().unsqueeze(2).unsqueeze(3).unsqueeze(4)  # Shape: (bs, 1, 1, 1, 1)
            
            all_targets_content = all_other_agents.unsqueeze(1).unsqueeze(3).unsqueeze(4).float()  # Shape: (bs, 1, n_agents, 1, 1)
            low_health_targets_content = low_health_targets.unsqueeze(1).unsqueeze(3).unsqueeze(4).float()  # Shape: (bs, 1, n_agents, 1, 1)
            
            if mode == 'content':
                # In content mode, set content for all communications
                content_all_mask = (marine_comm_all_content * all_targets_content).expand(bs, 1, n_agents, obs_dim)
                content_low_health_mask = (marine_comm_low_health_content * low_health_targets_content).expand(bs, 1, n_agents, obs_dim)
                content_mask[:, marine_idx:marine_idx+1, :, :] = (content_all_mask + content_low_health_mask).clamp(0, 1)
            else:  # object_content mode
                content_all_mask = (marine_comm_all_content * all_targets_content).expand(bs, 1, n_agents, obs_dim)
                content_low_health_mask = (marine_comm_low_health_content * low_health_targets_content).expand(bs, 1, n_agents, obs_dim)
                content_mask[:, marine_idx:marine_idx+1, :, :] = (content_all_mask + content_low_health_mask).clamp(0, 1)
    
    # Final mask construction based on mode
    if mode == 'object':
        return object_mask
    elif mode == 'content':
        return content_mask
    else:  # object_content
        # In object_content mode, content_mask should be zero where object_mask is zero
        object_mask_expanded = object_mask.expand(bs, n_agents, n_agents, obs_dim)
        final_mask = content_mask * object_mask_expanded
        return final_mask

# Test the function
if __name__ == "__main__":
    # Test with the required shape
    obs = torch.randn(2, 8, 8, 127)  # bs=2, n_agents=8, obs_dim=127
    mask = generate_mask(obs, mode='object_content')
    print(f"Mask shape: {mask.shape}")  # Should be (2, 8, 8, 127)
    
    # Test with smaller shape as in the requirement
    obs_small = torch.randn(2, 3, 3, 50)
    mask_small = generate_mask(obs_small, mode='object_content')
    print(f"Small mask shape: {mask_small.shape}")  # Should be (2, 3, 3, 50)
    
    # Test all modes
    for test_mode in ['object', 'content', 'object_content']:
        test_mask = generate_mask(obs_small, mode=test_mode)
        print(f"Mode {test_mode}: shape {test_mask.shape}")