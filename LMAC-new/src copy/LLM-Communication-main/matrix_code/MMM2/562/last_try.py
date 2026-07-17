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
    # Ensure obs is float32 to prevent type errors
    if obs.dtype != torch.float32:
        obs = obs.float()
        
    bs, n_agents, _, obs_dim = obs.shape
    device = obs.device
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros(bs, n_agents, n_agents, 1, device=device, dtype=torch.float32)
    elif mode in ['content', 'object_content']:
        mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=device, dtype=torch.float32)
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    # Extract observation features
    # Agent types: 0=Medivac, 1=Marine
    agent_types = torch.zeros(bs, n_agents, device=device, dtype=torch.long)
    for i in range(n_agents):
        type_1_idx = 20  # own_type_1
        # Use logical comparison
        agent_types[:, i] = (obs[:, i, 0, type_1_idx] > 0.5).long()
    
    # Health related indices
    own_health_idx = 18  # own_health
    ally_health_idx = 15  # ally_0_health
    
    # Enemy detection indices
    enemy_available_idx = 4   # enemy_0_available
    enemy_distance_idx = 5    # enemy_0_distance
    enemy_type_0_idx = 9      # enemy_0_type_0 (Medivac)
    enemy_type_1_idx = 10     # enemy_0_type_1 (Marauder)
    
    # ===== AGENT 0 (MEDIVAC) COMMUNICATION POLICY =====
    medivac_idx = 0
    
    # Trigger Condition 1: Enemy units within attack range (distance < 6)
    # Fix: Use torch.logical_and for boolean logic on tensors
    enemy_close = torch.logical_and(
        obs[:, :, :, enemy_available_idx] > 0.5,
        obs[:, :, :, enemy_distance_idx] < 6.0
    )
    enemy_close_any = torch.any(enemy_close, dim=2)  # Shape: (bs, n_agents)
    medivac_enemy_close = enemy_close_any[:, medivac_idx].unsqueeze(1)  # Shape: (bs, 1)
    
    # Trigger Condition 2: Any ally health below 50%
    ally_health_low = torch.logical_and(
        obs[:, :, :, ally_health_idx] < 0.5,
        obs[:, :, :, ally_health_idx] > 0.0
    )
    ally_health_low_any = torch.any(ally_health_low, dim=2)  # Shape: (bs, n_agents)
    medivac_ally_low_health = ally_health_low_any[:, medivac_idx].unsqueeze(1)  # Shape: (bs, 1)
    
    # Trigger Condition 3: Enemy Medivac detected
    enemy_medivac_detected = torch.logical_and(
        obs[:, :, :, enemy_type_0_idx] > 0.5,
        obs[:, :, :, enemy_available_idx] > 0.5
    )
    enemy_medivac_any = torch.any(enemy_medivac_detected, dim=2)  # Shape: (bs, n_agents)
    medivac_enemy_medivac = enemy_medivac_any[:, medivac_idx].unsqueeze(1)  # Shape: (bs, 1)
    
    # Medivac communicates logic (OR logic using addition and clamp)
    medivac_communicates = (medivac_enemy_close.float() + medivac_ally_low_health.float() + medivac_enemy_medivac.float()).clamp(0, 1)  # Shape: (bs, 1)
    
    # Create target mask for Marines (agents 1-7)
    marine_targets = torch.zeros(bs, n_agents, device=device, dtype=torch.float32)
    if n_agents > 1:
        marine_targets[:, 1:min(8, n_agents)] = 1.0
    
    # Apply Medivac communication
    if mode == 'object':
        # Ensure 4D shapes: (bs, 1, 1, 1) * (bs, 1, n_agents, 1)
        medivac_comm_view = medivac_communicates.view(bs, 1, 1, 1)
        marine_targets_view = marine_targets.view(bs, 1, n_agents, 1)
        
        comm_mask = medivac_comm_view * marine_targets_view # Shape: (bs, 1, n_agents, 1)
        mask[:, medivac_idx:medivac_idx+1, :, :] = comm_mask
        
    elif mode in ['content', 'object_content']:
        # Ensure 4D shapes for broadcasting
        medivac_comm_view = medivac_communicates.view(bs, 1, 1, 1)
        marine_targets_view = marine_targets.view(bs, 1, n_agents, 1)
        
        comm_mask = medivac_comm_view * marine_targets_view # Shape: (bs, 1, n_agents, 1)
        # Explicit expand to avoid dimension ambiguity
        comm_mask_expanded = comm_mask.expand(bs, 1, n_agents, obs_dim)
        
        mask[:, medivac_idx:medivac_idx+1, :, :] = comm_mask_expanded
    
    # ===== AGENTS 1-7 (MARINES) COMMUNICATION POLICY =====
    marine_mask = (agent_types == 1)  # Shape: (bs, n_agents)
    
    for marine_idx in range(1, min(8, n_agents)):
        # Optimization: check if any batch has this marine active, strictly speaking we should iterate per batch
        # but here we use vectorization. If marine_mask is false, outputs will be 0 anyway masked later? 
        # Actually logic below calculates triggers based on obs, which is safe.
        
        # Trigger Condition 1: Enemy units first detected (distance < 10)
        marine_enemy_detected = torch.logical_and(
            obs[:, marine_idx, :, enemy_available_idx] > 0.5,
            obs[:, marine_idx, :, enemy_distance_idx] < 10.0
        )
        marine_enemy_any = torch.any(marine_enemy_detected, dim=1).unsqueeze(1)  # Shape: (bs, 1)
        
        # Trigger Condition 2: Own health drops below 40%
        marine_low_health = (obs[:, marine_idx, 0, own_health_idx] < 0.4).unsqueeze(1)  # Shape: (bs, 1)
        
        # For low health, find nearest 2 Marine allies
        # We need to construct nearest_allies mask regardless of whether low_health is true for all batches
        # to keep tensor shapes consistent.
        
        ally_distances = obs[:, marine_idx, :, 12]  # ally_0_distance index 12
        valid_allies = marine_mask.float().clone()
        valid_allies[:, marine_idx] = 0.0  # Exclude self
        valid_allies[:, 0] = 0.0  # Exclude Medivac
        
        large_dist = 1000.0
        dist_with_invalid = ally_distances + (1.0 - valid_allies) * large_dist
        
        # Find top 2 closest
        k_val = min(2, n_agents - 2)
        if k_val > 0:
            _, top2_indices = torch.topk(dist_with_invalid, k=k_val, dim=1, largest=False)
            
            nearest_allies = torch.zeros(bs, n_agents, device=device, dtype=torch.float32)
            # Scatter ones to the indices
            # top2_indices shape: (bs, k)
            nearest_allies.scatter_(1, top2_indices, 1.0)
        else:
            nearest_allies = torch.zeros(bs, n_agents, device=device, dtype=torch.float32)
        
        low_health_targets = nearest_allies.clone()
        low_health_targets[:, 0] = 1.0  # Include Medivac
        
        # Trigger Condition 3: Enemy Marauder detected
        enemy_marauder_detected = torch.logical_and(
            obs[:, marine_idx, :, enemy_type_1_idx] > 0.5,
            obs[:, marine_idx, :, enemy_available_idx] > 0.5
        )
        marine_enemy_marauder = torch.any(enemy_marauder_detected, dim=1).unsqueeze(1)
        
        # Trigger Condition 4: Marine under fire (simplified)
        marine_under_fire = marine_enemy_any
        
        # Trigger Condition 5: Enemy Medivac detected
        marine_enemy_medivac_detected = torch.logical_and(
            obs[:, marine_idx, :, enemy_type_0_idx] > 0.5,
            obs[:, marine_idx, :, enemy_available_idx] > 0.5
        )
        marine_enemy_medivac = torch.any(marine_enemy_medivac_detected, dim=1).unsqueeze(1)
        
        # Combine triggers
        marine_comm_all = (marine_enemy_any.float() + marine_enemy_marauder.float() + 
                           marine_under_fire.float() + marine_enemy_medivac.float()).clamp(0, 1)
        marine_comm_low_health = marine_low_health.float()
        
        # Create target masks
        all_other_agents = torch.ones(bs, n_agents, device=device, dtype=torch.float32)
        all_other_agents[:, marine_idx] = 0.0
        
        if mode == 'object':
            # Use view to force 4D shapes: (bs, 1, 1, 1) and (bs, 1, n_agents, 1)
            marine_comm_all_view = marine_comm_all.view(bs, 1, 1, 1)
            marine_comm_low_health_view = marine_comm_low_health.view(bs, 1, 1, 1)
            
            all_targets_view = all_other_agents.view(bs, 1, n_agents, 1)
            low_health_targets_view = low_health_targets.view(bs, 1, n_agents, 1)
            
            comm_all_mask = marine_comm_all_view * all_targets_view
            comm_low_health_mask = marine_comm_low_health_view * low_health_targets_view
            
            combined_mask = torch.clamp(comm_all_mask + comm_low_health_mask, 0, 1)
            mask[:, marine_idx:marine_idx+1, :, :] = combined_mask
            
        elif mode in ['content', 'object_content']:
            # Use view to force 4D shapes: (bs, 1, 1, 1) and (bs, 1, n_agents, 1)
            marine_comm_all_view = marine_comm_all.view(bs, 1, 1, 1)
            marine_comm_low_health_view = marine_comm_low_health.view(bs, 1, 1, 1)
            
            all_targets_view = all_other_agents.view(bs, 1, n_agents, 1)
            low_health_targets_view = low_health_targets.view(bs, 1, n_agents, 1)
            
            comm_all_mask = marine_comm_all_view * all_targets_view
            comm_low_health_mask = marine_comm_low_health_view * low_health_targets_view
            
            # Explicit expand to obs_dim
            comm_all_mask_expanded = comm_all_mask.expand(bs, 1, n_agents, obs_dim)
            comm_low_health_mask_expanded = comm_low_health_mask.expand(bs, 1, n_agents, obs_dim)
            
            combined_mask = torch.clamp(comm_all_mask_expanded + comm_low_health_mask_expanded, 0, 1)
            mask[:, marine_idx:marine_idx+1, :, :] = combined_mask
            
    return mask