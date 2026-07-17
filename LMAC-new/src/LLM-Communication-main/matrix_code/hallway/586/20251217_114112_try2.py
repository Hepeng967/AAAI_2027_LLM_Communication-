import torch

def generate_mask(obs, mode='object'):
    """
    Generate communication mask based on hallway coordination policy.
    
    Args:
        obs: torch.Tensor of shape (bs, n_agents, n_agents, 2)
            obs[:, i, j, 0] = current_state of agent i from perspective of agent j
            obs[:, i, j, 1] = active_status of agent i from perspective of agent j
        mode: str, one of ['object', 'content', 'object_content']
    
    Returns:
        mask: torch.Tensor of appropriate shape based on mode
    """
    bs, n_agents, _, obs_dim = obs.shape
    
    # Extract state and status information
    # We need each agent's own state from its own perspective
    # obs[:, i, i, :] gives agent i's own state from its own perspective
    agent_self_states = torch.diagonal(obs, dim1=1, dim2=2)  # (bs, n_agents, obs_dim)
    
    # Current state for each agent (from its own perspective)
    current_state = agent_self_states[:, :, 0]  # (bs, n_agents)
    active_status = agent_self_states[:, :, 1]  # (bs, n_agents)
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device)
    else:  # 'content' or 'object_content'
        mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device)
    
    # Extract states for easier reference
    agent0_state = current_state[:, 0]  # (bs,)
    agent1_state = current_state[:, 1]  # (bs,)
    
    # Reshape for broadcasting - FIXED: Proper shape expansion
    agent0_state_exp = agent0_state.view(bs, 1, 1, 1)
    agent1_state_exp = agent1_state.view(bs, 1, 1, 1)
    
    # Agent 0 to Agent 1 communication triggers
    # Trigger 1: When Agent 0 reaches state 1
    agent0_to_agent1_trigger1 = (agent0_state == 1).float()
    agent0_to_agent1_trigger1_exp = agent0_to_agent1_trigger1.view(bs, 1, 1, 1)
    
    # Agent 1 to Agent 0 communication triggers
    # Trigger 1: When Agent 1 reaches state 2
    agent1_to_agent0_trigger1 = (agent1_state == 2).float()
    agent1_to_agent0_trigger1_exp = agent1_to_agent0_trigger1.view(bs, 1, 1, 1)
    
    # When both agents are at state 1
    both_at_state1 = ((agent0_state == 1) & (agent1_state == 1)).float()
    both_at_state1_exp = both_at_state1.view(bs, 1, 1, 1)
    
    # Apply triggers based on mode
    if mode == 'object':
        # Agent 0 -> Agent 1 when Agent 0 at state 1
        mask[:, 0, 1, :] = agent0_to_agent1_trigger1_exp
        
        # Agent 1 -> Agent 0 when Agent 1 at state 2
        mask[:, 1, 0, :] = agent1_to_agent0_trigger1_exp
        
        # Both directions when both at state 1 (final sync)
        # Use logical OR to combine triggers
        mask[:, 0, 1, :] = torch.max(mask[:, 0, 1, :], both_at_state1_exp)
        mask[:, 1, 0, :] = torch.max(mask[:, 1, 0, :], both_at_state1_exp)
        
    elif mode == 'content':
        # All agents can communicate, but we select content
        # For simplicity in this 2-agent system:
        # - When Agent 0 at state 1: send both features to Agent 1
        # - When Agent 1 at state 2: send both features to Agent 0
        # - When both at state 1: send both features both ways
        
        # Start with no communication
        mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device)
        
        # Agent 0 -> Agent 1 when Agent 0 at state 1
        mask[:, 0, 1, :] = agent0_to_agent1_trigger1_exp.expand(-1, -1, -1, obs_dim)
        
        # Agent 1 -> Agent 0 when Agent 1 at state 2
        mask[:, 1, 0, :] = agent1_to_agent0_trigger1_exp.expand(-1, -1, -1, obs_dim)
        
        # Both directions when both at state 1
        both_mask = both_at_state1_exp.expand(-1, -1, -1, obs_dim)
        mask[:, 0, 1, :] = torch.max(mask[:, 0, 1, :], both_mask)
        mask[:, 1, 0, :] = torch.max(mask[:, 1, 0, :], both_mask)
        
    elif mode == 'object_content':
        # Agent 0 -> Agent 1 when Agent 0 at state 1
        agent0_to_agent1_mask = agent0_to_agent1_trigger1_exp.expand(-1, -1, -1, obs_dim)
        mask[:, 0, 1, :] = agent0_to_agent1_mask
        
        # Agent 1 -> Agent 0 when Agent 1 at state 2
        agent1_to_agent0_mask = agent1_to_agent0_trigger1_exp.expand(-1, -1, -1, obs_dim)
        mask[:, 1, 0, :] = agent1_to_agent0_mask
        
        # Both directions when both at state 1
        both_mask = both_at_state1_exp.expand(-1, -1, -1, obs_dim)
        mask[:, 0, 1, :] = torch.max(mask[:, 0, 1, :], both_mask)
        mask[:, 1, 0, :] = torch.max(mask[:, 1, 0, :], both_mask)
    
    # Ensure binary mask (0 or 1)
    mask = (mask > 0.5).float()
    
    return mask