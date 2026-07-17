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
    
    # For checking received messages, we need to look at other agents' states
    # from our perspective. We'll extract these as needed.
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device)
    else:  # 'content' or 'object_content'
        mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device)
    
    # For simplicity in this implementation, we'll track communication triggers
    # Since we have 2 agents in this hallway environment
    
    # Agent 0 triggers
    # Trigger 1: When Agent 0 reaches state 1
    agent0_state1 = (current_state[:, 0] == 1).float().unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
    
    # Agent 1 triggers (though not explicitly mentioned in policy, we'll handle similarly)
    # In a 2-agent system, Agent 1 would be the slower agent (like Agent 3 in 4-agent system)
    
    # For this 2-agent hallway:
    # Agent 0 (faster) -> Agent 1 (slower)
    # Agent 1 (slower) -> Agent 0 (faster)
    
    # Let's implement based on the policy patterns:
    # 1. When an agent reaches state 1, it should notify the other agent
    # 2. When the slower agent (Agent 1) reaches state 2, it should notify Agent 0
    # 3. When both are at state 1 and have received acknowledgments, final sync
    
    # Extract states for easier reference
    agent0_state = current_state[:, 0]  # (bs,)
    agent1_state = current_state[:, 1]  # (bs,)
    
    # Reshape for broadcasting
    agent0_state_exp = agent0_state.view(bs, 1, 1, 1)
    agent1_state_exp = agent1_state.view(bs, 1, 1, 1)
    
    # Track received messages (simplified - in reality this would require memory)
    # For this implementation, we'll use current observations as proxy
    
    # Agent 0 to Agent 1 communication
    # When Agent 0 is at state 1
    agent0_to_agent1_trigger1 = (agent0_state == 1).float()
    
    # Agent 1 to Agent 0 communication
    # When Agent 1 is at state 2
    agent1_to_agent0_trigger1 = (agent1_state == 2).float()
    
    # When Agent 1 is at state 1 and Agent 0 is at state 1
    both_at_state1 = ((agent0_state == 1) & (agent1_state == 1)).float()
    
    # Apply triggers based on mode
    if mode == 'object':
        # Agent 0 -> Agent 1 when Agent 0 at state 1
        mask[:, 0, 1, :] += agent0_to_agent1_trigger1.view(bs, 1, 1, 1)
        
        # Agent 1 -> Agent 0 when Agent 1 at state 2
        mask[:, 1, 0, :] += agent1_to_agent0_trigger1.view(bs, 1, 1, 1)
        
        # Both directions when both at state 1 (final sync)
        mask[:, 0, 1, :] += both_at_state1.view(bs, 1, 1, 1)
        mask[:, 1, 0, :] += both_at_state1.view(bs, 1, 1, 1)
        
        # Clip to 0-1 range
        mask = torch.clamp(mask, 0, 1)
        
    elif mode == 'content':
        # All agents can communicate, but we select content
        # For simplicity, we'll enable all communication but choose content based on triggers
        
        # Start with all-to-all communication
        mask = torch.ones(bs, n_agents, n_agents, obs_dim, device=obs.device)
        
        # Modify content based on triggers
        # When Agent 0 at state 1, send full state to Agent 1
        # (already enabled by default)
        
        # When Agent 1 at state 2, send full state to Agent 0
        # (already enabled by default)
        
        # When both at state 1, enhance communication
        both_mask = both_at_state1.view(bs, 1, 1, 1)
        # This doesn't change content selection in this simple implementation
        
    elif mode == 'object_content':
        # Agent 0 -> Agent 1 when Agent 0 at state 1
        agent0_to_agent1_mask = agent0_to_agent1_trigger1.view(bs, 1, 1, 1)
        mask[:, 0, 1, :] = agent0_to_agent1_mask.expand(-1, -1, -1, obs_dim)
        
        # Agent 1 -> Agent 0 when Agent 1 at state 2
        agent1_to_agent0_mask = agent1_to_agent0_trigger1.view(bs, 1, 1, 1)
        mask[:, 1, 0, :] = agent1_to_agent0_mask.expand(-1, -1, -1, obs_dim)
        
        # Both directions when both at state 1
        both_mask = both_at_state1.view(bs, 1, 1, 1)
        mask[:, 0, 1, :] = torch.max(mask[:, 0, 1, :], both_mask.expand(-1, -1, -1, obs_dim))
        mask[:, 1, 0, :] = torch.max(mask[:, 1, 0, :], both_mask.expand(-1, -1, -1, obs_dim))
    
    # Ensure binary mask
    mask = (mask > 0.5).float()
    
    return mask