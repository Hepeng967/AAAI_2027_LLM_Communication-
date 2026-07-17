import torch

def generate_mask(obs, mode='object'):
    """
    Generate communication masks based on the given policy.
    
    Args:
        obs: torch.Tensor of shape (bs, n_agents, n_agents, obs_dim)
        mode: str in {'object', 'content', 'object_content'}
        
    Returns:
        mask: torch.Tensor based on mode
    """
    bs, n_agents, _, obs_dim = obs.shape
    assert n_agents == 5, f"Expected 5 agents, got {n_agents}"
    assert obs_dim == 35, f"Expected 35 obs dims, got {obs_dim}"
    
    # Extract feature indices
    # own_health is at index 33
    own_health_idx = 33
    
    # enemy_0 features start at index 4
    enemy_0_available_idx = 4
    enemy_0_rel_x_idx = 6
    enemy_0_rel_y_idx = 7
    
    # ally features: each ally has 7 features starting at index 9
    # Ally 0: indices 9-15, Ally 1: 16-22, Ally 2: 23-29, Ally 3: 30-36
    ally_start_indices = [9, 16, 23, 30]
    ally_visible_offset = 0
    ally_rel_x_offset = 2
    ally_rel_y_offset = 3
    ally_health_offset = 4
    
    # Agent indices (0-4)
    agent_indices = torch.arange(n_agents, device=obs.device)
    
    # For each agent, we need its own observation from the perspective of itself
    # obs[b, i, j, k] means agent i sees agent j's observation... but actually in this setup
    # obs[b, i, j, :] is the observation of agent j from agent i's perspective
    # So for agent i's own observation, it's obs[b, i, i, :]
    
    # Extract own observations for each agent
    own_obs = obs[:, agent_indices, agent_indices, :]  # (bs, n_agents, obs_dim)
    
    # Extract own_health
    own_health = own_obs[:, :, own_health_idx]  # (bs, n_agents)
    
    # Extract enemy_0_available for each agent
    enemy_0_available = own_obs[:, :, enemy_0_available_idx]  # (bs, n_agents)
    
    # Extract enemy_0_rel_x, enemy_0_rel_y
    enemy_0_rel_x = own_obs[:, :, enemy_0_rel_x_idx]  # (bs, n_agents)
    enemy_0_rel_y = own_obs[:, :, enemy_0_rel_y_idx]  # (bs, n_agents)
    
    # Extract ally visible, health, rel_x, rel_y for each agent
    # We'll create tensors of shape (bs, n_agents, n_allies) where n_allies = 4
    n_allies = n_agents - 1
    
    # For each ally (0-3), get features
    ally_visible_list = []
    ally_health_list = []
    ally_rel_x_list = []
    ally_rel_y_list = []
    
    for ally_idx in range(n_allies):
        start = ally_start_indices[ally_idx]
        ally_visible_list.append(own_obs[:, :, start + ally_visible_offset])  # (bs, n_agents)
        ally_rel_x_list.append(own_obs[:, :, start + ally_rel_x_offset])  # (bs, n_agents)
        ally_rel_y_list.append(own_obs[:, :, start + ally_rel_y_offset])  # (bs, n_agents)
        ally_health_list.append(own_obs[:, :, start + ally_health_offset])  # (bs, n_agents)
    
    ally_visible = torch.stack(ally_visible_list, dim=-1)  # (bs, n_agents, 4)
    ally_health = torch.stack(ally_health_list, dim=-1)  # (bs, n_agents, 4)
    ally_rel_x = torch.stack(ally_rel_x_list, dim=-1)  # (bs, n_agents, 4)
    ally_rel_y = torch.stack(ally_rel_y_list, dim=-1)  # (bs, n_agents, 4)
    
    # Determine which agents are wounded (own_health < 16)
    own_wounded = (own_health < 16).float()  # (bs, n_agents)
    
    # Determine which agents have enemy available and are not wounded
    enemy_available_and_healthy = (enemy_0_available == 1).float() * (own_health > 16).float()  # (bs, n_agents)
    
    # Determine for each agent which allies are visible and wounded
    # ally_visible[b, i, a] = 1 if agent i sees ally a (where a maps to actual agent index)
    # We need to map ally index to actual agent index
    # ally a (0-3) corresponds to agent index (0,1,2,3,4) excluding the current agent i
    # For simplicity, we'll compute per target agent
    
    # Initialize object masks
    # object_mask[b, i, j] = 1 if agent i should send to agent j
    object_mask = torch.zeros(bs, n_agents, n_agents, device=obs.device)
    
    # Compute content mask for all possible content indices
    # We'll pre-compute the features we want to send
    content_features = torch.zeros(obs_dim, device=obs.device)
    
    # Index of features we might want to send
    send_own_health_idx = own_health_idx  # 33
    send_enemy_0_available_idx = enemy_0_available_idx  # 4
    send_enemy_0_rel_x_idx = enemy_0_rel_x_idx  # 6
    send_enemy_0_rel_y_idx = enemy_0_rel_y_idx  # 7
    
    # Ally feature indices: for each ally a (0-3), the corresponding indices in obs
    # ally_a_visible: ally_start_indices[a] + 0
    # ally_a_rel_x: ally_start_indices[a] + 2
    # ally_a_rel_y: ally_start_indices[a] + 3
    # ally_a_health: ally_start_indices[a] + 4
    
    # For each agent i, we need to determine:
    # 1. Is own_health < 16? -> send own_health to all others
    # 2. Is enemy available and healthy? -> send enemy info to all others
    # 3. Is any ally visible and wounded? -> send ally info to all others (and to wounded ally)
    
    # We'll iterate over source agents using broadcasting
    
    # For each source agent i, decide which target agents to send to
    for i in range(n_agents):
        # Shape (bs, 1) for source agent i
        source_wounded = own_wounded[:, i:i+1]  # (bs, 1)
        source_enemy_avail_healthy = enemy_available_and_healthy[:, i:i+1]  # (bs, 1)
        
        # Set object mask for source i to all other agents based on conditions
        # Condition 1: if wounded, send to all others
        # Condition 2: if enemy available and healthy, send to all others
        # Condition 3: if any ally visible and wounded, send to all others and to that ally
        
        # Targets for condition 1 and 2: all other agents
        other_agents_mask = torch.ones(1, n_agents, device=obs.device)
        other_agents_mask[0, i] = 0  # Don't send to self
        
        # Add condition 1: wounded -> send to all others
        cond1_mask = source_wounded * other_agents_mask  # (bs, n_agents)
        
        # Add condition 2: enemy available and healthy -> send to all others
        cond2_mask = source_enemy_avail_healthy * other_agents_mask  # (bs, n_agents)
        
        # Condition 3: for each ally a (0-3), check if visible and wounded
        # ally_visible[b, i, a] and ally_health[b, i, a] < 16
        ally_visible_i = ally_visible[:, i, :]  # (bs, 4)
        ally_health_i = ally_health[:, i, :]  # (bs, 4)
        
        ally_wounded_visible = (ally_visible_i == 1).float() * (ally_health_i < 16).float()  # (bs, 4)
        
        # For each ally a, we need to send to:
        # - The wounded ally (agent index corresponding to a)
        # - All other agents
        
        # Map ally index to actual agent index
        # ally_idx 0 -> agent 0 if i!=0, else skip? Actually ally 0 is always agent 0
        # But agent i's perspective: ally indices are 0,1,2,3 corresponding to agents excluding i
        # We'll use a mapping: for agent i, ally a maps to agent (a if a < i else a+1)
        
        # For efficiency, we'll loop over allies (only 4, which is small)
        for a in range(n_allies):
            ally_wounded = ally_wounded_visible[:, a:a+1]  # (bs, 1)
            if ally_wounded.sum() > 0:
                # Determine actual agent index for this ally
                actual_ally_idx = a if a < i else a + 1
                
                # Send to this wounded ally
                target_wounded = torch.zeros(1, n_agents, device=obs.device)
                target_wounded[0, actual_ally_idx] = 1
                cond3_to_wounded = ally_wounded * target_wounded  # (bs, n_agents)
                
                # Send to all other agents (including the wounded one, but we already added that)
                cond3_to_all = ally_wounded * other_agents_mask  # (bs, n_agents)
                
                # Combine: send to wounded ally AND all others
                cond3_mask = cond3_to_wounded + cond3_to_all  # (bs, n_agents)
                cond3_mask = torch.clamp(cond3_mask, 0, 1)
                
                # Add to object mask for source i
                object_mask[:, i:i+1, :] += cond3_mask.unsqueeze(1)  # (bs, 1, n_agents)
        
        # Add cond1 and cond2 to object mask
        object_mask[:, i:i+1, :] += cond1_mask.unsqueeze(1)  # (bs, 1, n_agents)
        object_mask[:, i:i+1, :] += cond2_mask.unsqueeze(1)  # (bs, 1, n_agents)
    
    # Clamp object mask to binary
    object_mask = torch.clamp(object_mask, 0, 1)
    
    if mode == 'object':
        # Return (bs, n_agents, n_agents, 1)
        return object_mask.unsqueeze(-1)
    
    # For content and object_content modes, build the content mask
    # Initialize content mask with zeros
    content_mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device)
    
    # For each source agent i, set the appropriate content features
    for i in range(n_agents):
        source_wounded = own_wounded[:, i:i+1]  # (bs, 1)
        source_enemy_avail_healthy = enemy_available_and_healthy[:, i:i+1]  # (bs, 1)
        
        # Get the target agents for source i
        targets_i = object_mask[:, i, :]  # (bs, n_agents)
        
        # For each target j that receives communication
        for j in range(n_agents):
            if j == i:
                continue  # Skip self-communication
            
            # Get how many agents are targeted
            target_active = targets_i[:, j:j+1]  # (bs, 1)
            
            if target_active.sum() == 0:
                continue
            
            # Determine what content to send based on policy
            # Check conditions for source i sending to target j
            
            # Condition 1: source wounded -> send own_health
            if source_wounded.sum() > 0:
                # Send own_health (index 33)
                content_mask[:, i:i+1, j:j+1, own_health_idx] = target_active * source_wounded
            
            # Condition 2: source enemy available and healthy -> send enemy info
            if source_enemy_avail_healthy.sum() > 0:
                content_mask[:, i:i+1, j:j+1, enemy_0_available_idx] = target_active * source_enemy_avail_healthy
                content_mask[:, i:i+1, j:j+1, enemy_0_rel_x_idx] = target_active * source_enemy_avail_healthy
                content_mask[:, i:i+1, j:j+1, enemy_0_rel_y_idx] = target_active * source_enemy_avail_healthy
            
            # Condition 3: ally visible and wounded
            ally_visible_i = ally_visible[:, i, :]  # (bs, 4)
            ally_health_i = ally_health[:, i, :]  # (bs, 4)
            ally_wounded_visible = (ally_visible_i == 1).float() * (ally_health_i < 16).float()  # (bs, 4)
            
            for a in range(n_allies):
                ally_wounded = ally_wounded_visible[:, a:a+1]  # (bs, 1)
                if ally_wounded.sum() > 0:
                    actual_ally_idx = a if a < i else a + 1
                    
                    # Check if target is the wounded ally or other
                    if j == actual_ally_idx:
                        # To wounded ally: send own_health reminder
                        content_mask[:, i:i+1, j:j+1, own_health_idx] += target_active * ally_wounded
                    else:
                        # To others: send ally_X_health, ally_X_rel_x, ally_X_rel_y
                        ally_start = ally_start_indices[a]
                        content_mask[:, i:i+1, j:j+1, ally_start + ally_health_offset] += target_active * ally_wounded
                        content_mask[:, i:i+1, j:j+1, ally_start + ally_rel_x_offset] += target_active * ally_wounded
                        content_mask[:, i:i+1, j:j+1, ally_start + ally_rel_y_offset] += target_active * ally_wounded
    
    # Clamp content mask to binary
    content_mask = torch.clamp(content_mask, 0, 1)
    
    if mode == 'content':
        return content_mask
    
    if mode == 'object_content':
        # Apply object mask to content: if no communication, zero out all content
        object_mask_expanded = object_mask.unsqueeze(-1).expand(-1, -1, -1, obs_dim)  # (bs, n_agents, n_agents, obs_dim)
        return content_mask * object_mask_expanded
    
    raise ValueError(f"Unknown mode: {mode}")