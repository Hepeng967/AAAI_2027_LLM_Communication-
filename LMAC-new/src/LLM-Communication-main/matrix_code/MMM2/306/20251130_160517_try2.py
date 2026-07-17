```python
import torch

def generate_mask(obs, mode='object'):
    """
    Generate communication mask based on MMM2 scenario policy.
    
    Args:
        obs: Tensor of shape (bs, n_agents, n_agents, obs_dim)
        mode: 'object', 'content', or 'object_content'
    
    Returns:
        mask: Tensor of appropriate shape based on mode
    """
    bs, n_agents, _, obs_dim = obs.shape
    device = obs.device
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), device=device)
    elif mode == 'content':
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device)
    elif mode == 'object_content':
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device)
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    # Extract observation features
    own_health_idx = 18
    agent_id_idx = 21
    enemy_medivac_type_idx = 10  # enemy_0_type_1
    enemy_distance_idx = 5  # enemy_0_distance
    enemy_available_idx = 4  # enemy_0_available
    
    # Helper function to get ally health features for a specific agent
    def get_ally_health_indices(agent_idx):
        """Get health indices for all allies from agent_idx's perspective"""
        # Ally features: each ally has 7 features starting at index 11
        # Format: [ally_0_visible, ally_0_distance, ally_0_rel_x, ally_0_rel_y, ally_0_health, ally_0_type_0, ally_0_type_1]
        ally_health_indices = []
        for i in range(n_agents - 1):
            ally_health_idx = 11 + i * 7 + 4  # +4 for health in ally feature block
            ally_health_indices.append(ally_health_idx)
        return ally_health_indices
    
    # Process each agent's communication policies
    
    # Agent 0 (Medivac) - Index 0
    # Condition 1: Any ally health below 50%
    ally_health_indices_0 = get_ally_health_indices(0)
    ally_healths_0 = obs[:, 0, 0, ally_health_indices_0]  # (bs, n_agents-1)
    condition_0_1 = (ally_healths_0 < 0.5).any(dim=-1)  # (bs,)
    condition_0_1 = condition_0_1.view(bs, 1, 1, 1).expand(bs, 1, n_agents, 1)  # (bs, 1, n_agents, 1)
    
    # Condition 2: Enemy Medivac within attack range
    condition_0_2 = (obs[:, 0, 0, enemy_medivac_type_idx] > 0.5) & (obs[:, 0, 0, enemy_distance_idx] < 10.0)
    condition_0_2 = condition_0_2.view(bs, 1, 1, 1).expand(bs, 1, n_agents, 1)  # (bs, 1, n_agents, 1)
    
    # Condition 3: Received "Need healing" request (simplified - check marine health < 40%)
    marine_healths_0 = obs[:, 0, 0, ally_health_indices_0]  # (bs, 7)
    need_healing_0 = marine_healths_0 < 0.4  # (bs, 7)
    
    # Apply Agent 0 policies
    if mode == 'object':
        # Condition 1 & 2: Send to all marines (1-7)
        marine_targets_0 = torch.zeros((bs, 1, n_agents, 1), device=device)
        marine_targets_0[:, 0, 1:8, :] = 1
        mask_0_1_2 = (condition_0_1 | condition_0_2) & marine_targets_0
        
        # Condition 3: Send to requesting agents
        condition_0_3 = torch.zeros((bs, 1, n_agents, 1), device=device)
        condition_0_3[:, 0, 1:8, :] = need_healing_0.unsqueeze(1).unsqueeze(3)
        
        mask[:, 0:1, :, :] = mask_0_1_2 | condition_0_3
        
    elif mode == 'content':
        # All agent pairs can communicate, select content based on conditions
        content_mask_0 = torch.zeros((bs, 1, n_agents, obs_dim), device=device)
        
        # For conditions 1 & 2: Send position-related info to marines
        position_indices = [6, 7, 13, 14]  # enemy and ally relative positions
        marine_targets_0 = torch.zeros((bs, 1, n_agents, 1), device=device)
        marine_targets_0[:, 0, 1:8, :] = 1
        marine_comm_0 = (condition_0_1 | condition_0_2) & marine_targets_0
        marine_comm_expanded_0 = marine_comm_0.expand(bs, 1, n_agents, obs_dim)
        for idx in position_indices:
            content_mask_0[:, :, :, idx] = content_mask_0[:, :, :, idx] | marine_comm_expanded_0[:, :, :, 0]
        
        # For condition 3: Send position info to requesting agents
        condition_0_3 = torch.zeros((bs, 1, n_agents, 1), device=device)
        condition_0_3[:, 0, 1:8, :] = need_healing_0.unsqueeze(1).unsqueeze(3)
        healing_comm_0 = condition_0_3.expand(bs, 1, n_agents, obs_dim)
        for idx in position_indices:
            content_mask_0[:, :, :, idx] = content_mask_0[:, :, :, idx] | healing_comm_0[:, :, :, 0]
        
        mask[:, 0:1, :, :] = content_mask_0
        
    elif mode == 'object_content':
        # Condition 1 & 2: Send to all marines with position info
        marine_targets_0 = torch.zeros((bs, 1, n_agents, obs_dim), device=device)
        marine_targets_0[:, 0, 1:8, :] = 1
        position_indices = [6, 7, 13, 14]
        marine_comm_0 = (condition_0_1 | condition_0_2).expand(bs, 1, n_agents, obs_dim) & marine_targets_0
        position_mask_0 = torch.zeros((bs, 1, n_agents, obs_dim), device=device)
        for idx in position_indices:
            position_mask_0[:, :, :, idx] = 1
        mask_0_1_2 = marine_comm_0 & position_mask_0
        
        # Condition 3: Send to requesting agents with position info
        condition_0_3 = torch.zeros((bs, 1, n_agents, obs_dim), device=device)
        condition_0_3[:, 0, 1:8, :] = need_healing_0.unsqueeze(1).unsqueeze(3).expand(bs, 1, 7, obs_dim)
        healing_mask_0 = torch.zeros((bs, 1, n_agents, obs_dim), device=device)
        for idx in position_indices:
            healing_mask_0[:, :, :, idx] = 1
        mask_0_3 = condition_0_3 & healing_mask_0
        
        mask[:, 0:1, :, :] = mask_0_1_2 | mask_0_3
    
    # Process Marine agents (1-7)
    for marine_idx in range(1, 8):
        # Common conditions for all marines
        # Condition 1: Health below 40% - send to Medivac
        condition_health = obs[:, marine_idx, marine_idx, own_health_idx] < 0.4
        condition_health = condition_health.view(bs, 1, 1, 1).expand(bs, 1, n_agents, 1)  # (bs, 1, n_agents, 1)
        
        # Condition 2: Spot enemy Medivac - send to all agents
        condition_medivac = obs[:, marine_idx, marine_idx, enemy_medivac_type_idx] > 0.5
        condition_medivac = condition_medivac.view(bs, 1, 1, 1).expand(bs, 1, n_agents, 1)  # (bs, 1, n_agents, 1)
        
        # Apply marine policies
        if mode == 'object':
            # Initialize marine mask
            marine_mask = torch.zeros((bs, 1, n_agents, 1), device=device)
            
            # Condition 1: Send to Medivac (agent 0)
            medivac_target = torch.zeros((bs, 1, n_agents, 1), device=device)
            medivac_target[:, 0, 0:1, :] = 1
            marine_mask = marine_mask | (condition_health & medivac_target)
            
            # Condition 2: Send to all agents
            all_targets = torch.ones((bs, 1, n_agents, 1), device=device)
            marine_mask = marine_mask | (condition_medivac & all_targets)
            
            # Condition 3: Marine-specific policies
            if marine_idx == 1:  # Agent 1: Multiple enemies approaching
                multiple_enemies = obs[:, 1, 1, enemy_available_idx] > 0.7  # Simplified
                multiple_enemies = multiple_enemies.view(bs, 1, 1, 1).expand(bs, 1, n_agents, 1)
                marine_targets_1 = torch.zeros((bs, 1, n_agents, 1), device=device)
                marine_targets_1[:, 0, 2:8, :] = 1  # Send to agents 2-7
                marine_mask = marine_mask | (multiple_enemies & marine_targets_1)
                
            elif marine_idx == 2:  # Agent 2: Flanking enemy movement
                enemy_x, enemy_y = obs[:, 2, 2, 6], obs[:, 2, 2, 7]  # enemy relative positions
                flanking = (torch.abs(enemy_x) > 5.0) | (torch.abs(enemy_y) > 5.0)
                flanking = flanking.view(bs, 1, 1, 1).expand(bs, 1, n_agents, 1)
                marine_targets_2 = torch.zeros((bs, 1, n_agents, 1), device=device)
                marine_targets_2[:, 0, [0, 2, 3, 4, 5, 6, 7], :] = 1  # All except self
                marine_mask = marine_mask | (flanking & marine_targets_2)
                
            elif marine_idx == 3:  # Agent 3: Ally formation breaking
                # Simplified: check ally distance variance
                ally_distances = []
                for i in range(n_agents - 1):
                    ally_dist_idx = 11 + i * 7 + 1  # ally distance
                    ally_distances.append(obs[:, 3, 3, ally_dist_idx])
                ally_dists = torch.stack(ally_distances, dim=-1)  # (bs, 7)
                formation_break = ally_dists.std(dim=-1) > 3.0  # High variance
                formation_break = formation_break.view(bs, 1, 1, 1).expand(bs, 1, n_agents, 1)
                marine_targets_3 = torch.zeros((bs, 1, n_agents, 1), device=device)
                marine_targets_3[:, 0, [1, 2, 4], :] = 1  # Nearest 3 marines (simplified)
                marine_mask = marine_mask | (formation_break & marine_targets_3)
                
            elif marine_idx == 4:  # Agent 4: Optimal firing position
                optimal_pos = obs[:, 4, 4, enemy_distance_idx] < 5.0  # Close to enemy
                optimal_pos = optimal_pos.view(bs, 1, 1, 1).expand(bs, 1, n_agents, 1)
                marine_targets_4 = torch.zeros((bs, 1, n_agents, 1), device=device)
                marine_targets_4[:, 0, [0, 1, 2, 4, 5, 6], :] = 1  # All marines except self
                marine_mask = marine_mask | (optimal_pos & marine_targets_4)
                
            elif marine_idx == 5:  # Agent 5: Enemy focus fire
                # Simplified: check if any ally health dropping rapidly
                ally_healths_5 = obs[:, 5, 5, get_ally_health_indices(5)]  # (bs, 7)
                focus_fire = (ally_healths_5 < 0.3).any(dim=-1)  # Very low health
                focus_fire = focus_fire.view(bs, 1, 1, 1).expand(bs, 1, n_agents, 1)
                all_targets_5 = torch.ones((bs, 1, n_agents, 1), device=device)
                marine_mask = marine_mask | (focus_fire & all_targets_5)
                
            elif marine_idx == 6:  # Agent 6: Enemy formation weakness
                enemy_weakness = obs[:, 6, 6, enemy_health_idx] < 0.3  # Low enemy health
                enemy_weakness = enemy_weakness.view(bs, 1, 1, 1).expand(bs, 1, n_agents, 1)
                marine_targets_6 = torch.zeros((bs, 1, n_agents, 1), device=device)
                marine_targets_6[:, 0, [0, 1, 2, 3, 4, 6], :] = 1  # All marines except self
                marine_mask = marine_mask | (enemy_weakness & marine_targets_6)
                
            elif marine_idx == 7:  # Agent 7: Retreating enemies
                retreating = obs[:, 7, 7, enemy_distance_idx] > 15.0  # Far enemy
                retreating = retreating.view(bs, 1, 1, 1).expand(bs, 1, n_agents, 1)
                marine_targets_7 = torch.zeros((bs, 1, n_agents, 1), device=device)
                marine_targets_7[:, 0, 1:7, :] = 1  # Marines 1-6
                marine_mask = marine_mask | (retreating & marine_targets_7)
            
            mask[:, marine_idx:marine_idx+1, :, :] = marine_mask
            
        elif mode == 'content':
            # Initialize content mask for marine
            content_mask_marine = torch.zeros((bs, 1, n_agents, obs_dim), device=device)
            
            # Condition 1: Health and position to Medivac
            medivac_target = torch.zeros((bs, 1, n_agents, 1), device=device)
            medivac_target[:, 0, 0:1, :] = 1
            health_comm = condition_health & medivac_target
            health_comm_expanded = health_comm.expand(bs, 1, n_agents, obs_dim)
            health_indices = [18, 13, 14]  # own_health, position
            for idx in health_indices:
                content_mask_marine[:, :, :, idx] = content_mask_marine[:, :, :, idx] | health_comm_expanded[:, :, :, 0]
            
            # Condition 2: Enemy info to all
            all_targets = torch.ones((bs, 1, n_agents, 1), device=device)
            medivac_comm = condition_medivac & all_targets
            medivac_comm_expanded = medivac_comm.expand(bs, 1, n_agents, obs_dim)
            enemy_indices = [4, 5, 6, 7, 9, 10]  # enemy info
            for idx in enemy_indices:
                content_mask_marine[:, :, :, idx] = content_mask_marine[:, :, :, idx] | medivac_comm_expanded[:, :, :, 0]
            
            mask[:, marine_idx:marine_idx+1, :, :] = content_mask_marine
            
        elif mode == 'object_content':
            # Initialize object_content mask for marine
            obj_content_mask_marine = torch.zeros((bs, 1, n_agents, obs_dim), device=device)
            
            # Condition 1: Health and position to Medivac
            medivac_target = torch.zeros((bs, 1, n_agents, obs_dim), device=device)
            medivac_target[:, 0, 0:1, :] = 1
            health_comm = condition_health.expand(bs, 1, n_agents, obs_dim) & medivac_target
            health_indices_mask = torch.zeros((bs, 1, n_agents, obs_dim), device=device)
            health_indices = [18, 13, 14]  # own_health, position
            for