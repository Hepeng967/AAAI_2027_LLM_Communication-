import torch

def generate_mask(obs, mode='object'):
    """
    Generate communication mask based on hallway coordination policy.
    
    Args:
        obs: torch.Tensor of shape (bs, n_agents, n_agents, 2)
            obs[b, i, j, 0] = current_state of agent i from perspective of agent j
            obs[b, i, j, 1] = active_status of agent i from perspective of agent j
        mode: str, one of ['object', 'content', 'object_content']
    
    Returns:
        mask: torch.Tensor of appropriate shape based on mode
    """
    bs, n_agents, _, obs_dim = obs.shape
    device = obs.device
    
    # Extract self-observations (agent i's own state from its own perspective)
    # obs[:, i, i, :] gives agent i's own state
    self_obs = torch.diagonal(obs, dim1=1, dim2=2).transpose(1, 2)  # (bs, n_agents, obs_dim)
    
    # Current state and active status for each agent
    current_state = self_obs[:, :, 0]  # (bs, n_agents)
    active_status = self_obs[:, :, 1]  # (bs, n_agents)
    
    # Create base tensors for broadcasting
    bs_idx = torch.arange(bs, device=device).view(bs, 1, 1, 1)
    agent_i_idx = torch.arange(n_agents, device=device).view(1, n_agents, 1, 1)
    agent_j_idx = torch.arange(n_agents, device=device).view(1, 1, n_agents, 1)
    
    # Initialize masks
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), device=device, dtype=torch.float32)
    else:  # 'content' or 'object_content'
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device, dtype=torch.float32)
    
    # Policy implementation for 2-agent case
    # For n_agents > 2, we would implement the general extension
    
    # TRIGGER 1: Agent reaches state 1 (border position)
    # When agent i reaches state 1, it sends "Ready to move to goal" to all other agents
    at_border = (current_state == 1).float()  # (bs, n_agents)
    active = (active_status == 1.0).float()   # (bs, n_agents)
    
    # Only active agents at border can trigger
    trigger1 = at_border * active  # (bs, n_agents)
    
    # Create communication for trigger1
    # Agent i communicates with all j != i
    if n_agents == 2:
        # For 2 agents, each agent communicates with the other
        # Agent 0 to Agent 1
        mask[:, 0, 1, :] += trigger1[:, 0:1].unsqueeze(-1).expand(-1, -1, obs_dim)
        # Agent 1 to Agent 0
        mask[:, 1, 0, :] += trigger1[:, 1:2].unsqueeze(-1).expand(-1, -1, obs_dim)
    else:
        # For general case (n_agents > 2)
        # Create identity matrix to exclude self-communication
        not_self = 1 - torch.eye(n_agents, device=device).unsqueeze(0)  # (1, n_agents, n_agents)
        trigger1_expanded = trigger1.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
        not_self_expanded = not_self.unsqueeze(3)  # (1, n_agents, n_agents, 1)
        
        if mode == 'object':
            mask += (trigger1_expanded * not_self_expanded)
        else:
            mask += (trigger1_expanded * not_self_expanded.expand(-1, -1, -1, obs_dim))
    
    # TRIGGER 2: Agent receives "Ready to move to goal" and responds with "Proceed to goal"
    # This requires tracking message history, which we simulate using current state
    # Simplified: If agent is at border and other agent is also at border, send "Proceed"
    
    # Check if both agents are at border
    if n_agents == 2:
        both_at_border = (at_border[:, 0] * at_border[:, 1]).unsqueeze(1)  # (bs, 1)
        
        # Agent 0 sends to Agent 1 when both at border
        mask[:, 0, 1, :] += both_at_border.unsqueeze(-1).expand(-1, -1, obs_dim)
        # Agent 1 sends to Agent 0 when both at border
        mask[:, 1, 0, :] += both_at_border.unsqueeze(-1).expand(-1, -1, obs_dim)
    
    # TRIGGER 3: Agent receives "Proceed to goal" and responds with "Acknowledged"
    # Simplified: If agent is at state 0 (goal) and other is at border, acknowledge
    
    at_goal = (current_state == 0).float()  # (bs, n_agents)
    
    if n_agents == 2:
        # Agent 0 acknowledges Agent 1 if Agent 0 at goal and Agent 1 at border
        ack_0_to_1 = (at_goal[:, 0:1] * at_border[:, 1:2]).unsqueeze(-1)  # (bs, 1, 1)
        mask[:, 0, 1, :] += ack_0_to_1.expand(-1, -1, obs_dim)
        
        # Agent 1 acknowledges Agent 0 if Agent 1 at goal and Agent 0 at border
        ack_1_to_0 = (at_goal[:, 1:2] * at_border[:, 0:1]).unsqueeze(-1)  # (bs, 1, 1)
        mask[:, 1, 0, :] += ack_1_to_0.expand(-1, -1, obs_dim)
    
    # Ensure binary mask (0 or 1)
    mask = (mask > 0).float()
    
    # Handle different modes
    if mode == 'object':
        # Object mode: only indicate which agents communicate
        # Any content dimension > 0 means communication
        object_mask = (mask.sum(dim=-1, keepdim=True) > 0).float()
        return object_mask
    
    elif mode == 'content':
        # Content mode: all agents can communicate, but select content
        # Create full connectivity mask
        full_connectivity = 1 - torch.eye(n_agents, device=device).unsqueeze(0).unsqueeze(-1)  # (1, n_agents, n_agents, 1)
        full_connectivity = full_connectivity.expand(bs, -1, -1, obs_dim)
        
        # Apply content selection from our policy mask
        content_mask = full_connectivity * mask
        return content_mask
    
    else:  # 'object_content'
        # Object_content mode: jointly select both
        return mask