```python
import torch

def generate_mask(obs, mode='object'):
    """
    Generate communication mask based on the corridor map scenario policy.
    
    Args:
        obs: torch.Tensor of shape (bs, n_agents, n_agents, obs_dim)
        mode: 'object', 'content', or 'object_content'
    
    Returns:
        mask: torch.Tensor of appropriate shape based on mode
    """
    bs, n_agents, _, obs_dim = obs.shape
    assert n_agents == 6, f"Expected 6 agents, got {n_agents}"
    
    # Create base masks
    if mode == 'object':
        mask = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device)
    else:  # 'content' or 'object_content'
        mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device)
    
    # Define observation indices based on the provided feature names
    MOVE_NORTH = 0
    MOVE_SOUTH = 1
    MOVE_EAST = 2
    MOVE_WEST = 3
    ENEMY_0_AVAILABLE = 4
    ENEMY_0_DISTANCE = 5
    ENEMY_0_REL_X = 6
    ENEMY_0_REL_Y = 7
    ENEMY_0_HEALTH = 8
    ALLY_0_VISIBLE = 9
    ALLY_0_DISTANCE = 10
    ALLY_0_REL_X = 11
    ALLY_0_REL_Y = 12
    ALLY_0_HEALTH = 13
    ALLY_0_SHIELD = 14
    OWN_HEALTH = 15
    OWN_SHIELD = 16
    AGENT_ID = 17
    
    # Attack range constant (assuming 6.0 as typical Zealot attack range)
    ATTACK_RANGE = 6.0
    
    # Helper function to get nearest ally for each agent
    def get_nearest_ally(obs_tensor):
        # obs_tensor shape: (bs, n_agents, n_agents, obs_dim)
        # For each agent, find the nearest ally (excluding self)
        ally_distances = obs_tensor[:, :, :, ALLY_0_DISTANCE]  # (bs, n_agents, n_agents)
        
        # Set self-distance to infinity to exclude self
        self_mask = torch.eye(n_agents, device=obs.device).unsqueeze(0)  # (1, n_agents, n_agents)
        ally_distances = ally_distances + self_mask * float('inf')
        
        # Find nearest ally for each agent
        min_dist, nearest_ally = torch.min(ally_distances, dim=2)  # (bs, n_agents)
        return nearest_ally
    
    # Get nearest ally for all agents
    nearest_ally = get_nearest_ally(obs)  # (bs, n_agents)
    
    # Agent 0 policies
    # Condition 1: Enemy within attack range
    enemy_in_range_0 = obs[:, 0, 0, ENEMY_0_DISTANCE] <= ATTACK_RANGE  # (bs,)
    if mode == 'object':
        # Send to agents 1-5
        target_indices = torch.tensor([1, 2, 3, 4, 5], device=obs.device)
        target_mask = torch.zeros(bs, n_agents, device=obs.device)
        target_mask[:, target_indices] = 1.0
        mask[enemy_in_range_0, 0, :, 0] = target_mask[enemy_in_range_0]
    else:
        # Create content mask for "Enemy engaged at my position"
        content_mask_0_1 = torch.zeros(obs_dim, device=obs.device)
        content_mask_0_1[ENEMY_0_DISTANCE] = 1.0
        content_mask_0_1[ENEMY_0_REL_X] = 1.0
        content_mask_0_1[ENEMY_0_REL_Y] = 1.0
        
        if mode == 'object_content':
            target_indices = torch.tensor([1, 2, 3, 4, 5], device=obs.device)
            for idx in target_indices:
                condition_expanded = enemy_in_range_0.unsqueeze(1).unsqueeze(2).unsqueeze(3).expand(bs, 1, 1, obs_dim)
                content_expanded = content_mask_0_1.unsqueeze(0).unsqueeze(0).unsqueeze(0).expand(bs, 1, 1, obs_dim)
                mask[condition_expanded, 0, idx, :] = content_expanded[condition_expanded, 0, idx, :]
        else:  # content mode
            target_indices = torch.tensor([1, 2, 3, 4, 5], device=obs.device)
            for idx in target_indices:
                mask[:, 0, idx, :] = content_mask_0_1.unsqueeze(0).unsqueeze(0).expand(bs, 1, obs_dim)
    
    # Condition 2: Health below 50%
    low_health_0 = obs[:, 0, 0, OWN_HEALTH] < 50  # (bs,)
    nearest_to_0 = nearest_ally[:, 0]  # (bs,)
    
    if mode == 'object':
        for b in range(bs):
            if low_health_0[b]:
                mask[b, 0, nearest_to_0[b].long(), 0] = 1.0
    else:
        # Create content mask for "Low health, need support"
        content_mask_0_2 = torch.zeros(obs_dim, device=obs.device)
        content_mask_0_2[OWN_HEALTH] = 1.0
        
        if mode == 'object_content':
            for b in range(bs):
                if low_health_0[b]:
                    mask[b, 0, nearest_to_0[b].long(), :] = content_mask_0_2
        else:  # content mode
            for b in range(bs):
                mask[b, 0, nearest_to_0[b].long(), :] = content_mask_0_2
    
    # Agent 1 policies
    # Condition 1: Multiple enemies (enemy count > 3)
    multiple_enemies_1 = obs[:, 1, 1, ENEMY_0_AVAILABLE] > 0.5  # Simplified condition
    
    if mode == 'object':
        target_indices = torch.tensor([0, 2, 3, 4, 5], device=obs.device)
        target_mask = torch.zeros(bs, n_agents, device=obs.device)
        target_mask[:, target_indices] = 1.0
        mask[multiple_enemies_1, 1, :, 0] = target_mask[multiple_enemies_1]
    else:
        # Create content mask for "Multiple enemies detected, group up"
        content_mask_1_1 = torch.zeros(obs_dim, device=obs.device)
        content_mask_1_1[ENEMY_0_AVAILABLE] = 1.0
        content_mask_1_1[ENEMY_0_DISTANCE] = 1.0
        
        if mode == 'object_content':
            target_indices = torch.tensor([0, 2, 3, 4, 5], device=obs.device)
            for idx in target_indices:
                condition_expanded = multiple_enemies_1.unsqueeze(1).unsqueeze(2).unsqueeze(3).expand(bs, 1, 1, obs_dim)
                content_expanded = content_mask_1_1.unsqueeze(0).unsqueeze(0).unsqueeze(0).expand(bs, 1, 1, obs_dim)
                mask[condition_expanded, 1, idx, :] = content_expanded[condition_expanded, 1, idx, :]
        else:  # content mode
            target_indices = torch.tensor([0, 2, 3, 4, 5], device=obs.device)
            for idx in target_indices:
                mask[:, 1, idx, :] = content_mask_1_1.unsqueeze(0).unsqueeze(0).expand(bs, 1, obs_dim)
    
    # Condition 2: Enemies approaching corridor entrance
    enemy_approaching_1 = (obs[:, 1, 1, ENEMY_0_REL_Y] < 0) & (obs[:, 1, 1, ENEMY_0_DISTANCE] < 10.0)
    
    if mode == 'object':
        target_indices = torch.tensor([0, 2, 3, 4, 5], device=obs.device)
        target_mask = torch.zeros(bs, n_agents, device=obs.device)
        target_mask[:, target_indices] = 1.0
        mask[enemy_approaching_1, 1, :, 0] = target_mask[enemy_approaching_1]
    else:
        # Create content mask for "Enemies approaching corridor, defend choke point"
        content_mask_1_2 = torch.zeros(obs_dim, device=obs.device)
        content_mask_1_2[ENEMY_0_REL_X] = 1.0
        content_mask_1_2[ENEMY_0_REL_Y] = 1.0
        content_mask_1_2[ENEMY_0_DISTANCE] = 1.0
        
        if mode == 'object_content':
            target_indices = torch.tensor([0, 2, 3, 4, 5], device=obs.device)
            for idx in target_indices:
                condition_expanded = enemy_approaching_1.unsqueeze(1).unsqueeze(2).unsqueeze(3).expand(bs, 1, 1, obs_dim)
                content_expanded = content_mask_1_2.unsqueeze(0).unsqueeze(0).unsqueeze(0).expand(bs, 1, 1, obs_dim)
                mask[condition_expanded, 1, idx, :] = content_expanded[condition_expanded, 1, idx, :]
        else:  # content mode
            target_indices = torch.tensor([0, 2, 3, 4, 5], device=obs.device)
            for idx in target_indices:
                mask[:, 1, idx, :] = content_mask_1_2.unsqueeze(0).unsqueeze(0).expand(bs, 1, obs_dim)
    
    # Agent 2 policies
    # Condition 1: Attacking point (4,4) being threatened
    base_threatened_2 = (torch.abs(obs[:, 2, 2, ENEMY_0_REL_X] - 4.0) < 2.0) & (torch.abs(obs[:, 2, 2, ENEMY_0_REL_Y] - 4.0) < 2.0)
    
    if mode == 'object':
        target_indices = torch.tensor([0, 1, 3, 4, 5], device=obs.device)
        target_mask = torch.zeros(bs, n_agents, device=obs.device)
        target_mask[:, target_indices] = 1.0
        mask[base_threatened_2, 2, :, 0] = target_mask[base_threatened_2]
    else:
        # Create content mask for "Base under threat, fall back to defend"
        content_mask_2_1 = torch.zeros(obs_dim, device=obs.device)
        content_mask_2_1[ENEMY_0_REL_X] = 1.0
        content_mask_2_1[ENEMY_0_REL_Y] = 1.0
        content_mask_2_1[ENEMY_0_DISTANCE] = 1.0
        
        if mode == 'object_content':
            target_indices = torch.tensor([0, 1, 3, 4, 5], device=obs.device)
            for idx in target_indices:
                condition_expanded = base_threatened_2.unsqueeze(1).unsqueeze(2).unsqueeze(3).expand(bs, 1, 1, obs_dim)
                content_expanded = content_mask_2_1.unsqueeze(0).unsqueeze(0).unsqueeze(0).expand(bs, 1, 1, obs_dim)
                mask[condition_expanded, 2, idx, :] = content_expanded[condition_expanded, 2, idx, :]
        else:  # content mode
            target_indices = torch.tensor([0, 1, 3, 4, 5], device=obs.device)
            for idx in target_indices:
                mask[:, 2, idx, :] = content_mask_2_1.unsqueeze(0).unsqueeze(0).expand(bs, 1, obs_dim)
    
    # Condition 2: Shield below 30%
    low_shield_2 = obs[:, 2, 2, OWN_SHIELD] < 30  # (bs,)
    nearest_to_2 = nearest_ally[:, 2]  # (bs,)
    
    if mode == 'object':
        for b in range(bs):
            if low_shield_2[b]:
                mask[b, 2, nearest_to_2[b].long(), 0] = 1.0
    else:
        # Create content mask for "Shield critical, need cover"
        content_mask_2_2 = torch.zeros(obs_dim, device=obs.device)
        content_mask_2_2[OWN_SHIELD] = 1.0
        
        if mode == 'object_content':
            for b in range(bs):
                if low_shield_2[b]:
                    mask[b, 2, nearest_to_2[b].long(), :] = content_mask_2_2
        else:  # content mode
            for b in range(bs):
                mask[b, 2, nearest_to_2[b].long(), :] = content_mask_2_2
    
    # Agent 3 policies
    # Condition 1: Enemy movement pattern suggesting flanking
    flanking_detected_3 = torch.abs(obs[:, 3, 3, ENEMY_0_REL_X]) > torch.abs(obs[:, 3, 3, ENEMY_0_REL_Y]) + 2.0
    
    if mode == 'object':
        target_indices = torch.tensor([0, 1, 2, 4, 5], device=obs.device)
        target_mask = torch.zeros(bs, n_agents, device=obs.device)
        target_mask[:, target_indices] = 1.0
        mask[flanking_detected_3, 3, :, 0] = target_mask[flanking_detected_3]
    else:
        # Create content mask for "Possible flanking maneuver detected"
        content_mask_3_1 = torch.zeros(obs_dim, device=obs.device)
        content_mask_3_1[ENEMY_0_REL_X] = 1.0
        content_mask_3_1[ENEMY_0_REL_Y] = 1.0
        
        if mode == 'object_content':
            target_indices = torch.tensor([0, 1, 2, 4, 5], device=obs.device)
            for idx in target_indices:
                condition_expanded = flanking_detected_3.unsqueeze(1).unsqueeze(2).unsqueeze(3).expand(bs, 1, 1, obs_dim)
                content_expanded = content_mask_3_1.unsqueeze(0).unsqueeze(0).unsqueeze(0).expand(bs, 1, 1, obs_dim)
                mask[condition_expanded, 3, idx, :] = content_expanded[condition_expanded, 3, idx, :]
        else:  # content mode
            target_indices = torch.tensor([0, 1, 2, 4, 5], device=obs.device)
            for idx in target_indices:
                mask[:, 3, idx, :] = content_mask_3_1.unsqueeze(0).unsqueeze(0).expand(bs, 1, obs_dim)
    
    # Condition 2: Ally health below 25%
    ally_critical_3 = obs[:, 3, 3, ALLY_0_HEALTH] < 25  # (bs,)
    nearest_to_3 = nearest_ally[:, 3]  # (bs,)
    
    if mode == 'object':
        for b in range(bs):
            if ally_critical_3[b]:
                # Send to the specific low-health ally and nearest other agent
                mask[b, 3, 0, 0] = 1.0  # ally_0
                mask[b, 3, nearest_to_3[b].long(), 0] = 1.0
    else:
        # Create content mask for "Ally critically wounded, provide assistance"
        content_mask_3_2 = torch.zeros(obs_dim, device=obs.device)
        content_mask_3_2[ALLY_0_HEALTH] = 1.0
        
        if mode == 'object_content':
            for b in range(bs):
                if ally_critical_3[b]:
                    mask[b, 3, 0, :] = content_mask_3_2
                    mask[b, 3, nearest_to_3[b].long(), :] = content_mask_3_2
        else:  # content mode
            for b in range(bs):
                mask[b, 3, 0, :] = content_mask_3_2
                mask[b, 3, nearest_to_3[b].long(), :