import torch

def generate_mask(obs, mode='object'):
    """
    Generate communication mask for complex hallway coordination.
    
    Args:
        obs: torch.Tensor of shape (bs, n_agents, n_agents, 2)
            obs[:, i, j, 0] = current_state of agent i from perspective of agent j
            obs[:, i, j, 1] = active_status of agent i from perspective of agent j
        mode: str, one of ['object', 'content', 'object_content']
    
    Returns:
        mask: torch.Tensor of appropriate shape based on mode
    """
    bs, n_agents, _, obs_dim = obs.shape
    device = obs.device
    
    # Each agent's maximum state (based on agent index)
    max_states = torch.tensor([4, 6, 8, 10], device=device).view(1, n_agents, 1, 1)
    
    # Extract current states and active status
    # obs[:, i, i, :] gives agent i's own observation
    current_states = obs[:, :, :, 0]  # (bs, n_agents, n_agents)
    active_status = obs[:, :, :, 1]  # (bs, n_agents, n_agents)
    
    # Get each agent's own state (diagonal elements)
    # current_states_self[b, i] = state of agent i
    current_states_self = torch.diagonal(current_states, dim1=1, dim2=2)  # (bs, n_agents)
    current_states_self = current_states_self.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
    
    # Get each agent's own active status
    active_self = torch.diagonal(active_status, dim1=1, dim2=2)  # (bs, n_agents)
    active_self = active_self.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
    
    # Initialize masks
    if mode == 'object':
        mask = torch.zeros(bs, n_agents, n_agents, 1, device=device)
    else:  # 'content' or 'object_content'
        mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=device)
    
    # ========== AGENT 0-2 POLICIES (Agents 0, 1, 2) ==========
    # These agents have identical policies
    for agent_idx in [0, 1, 2]:
        # Trigger 1: When agent reaches state 1
        trigger1 = (current_states_self[:, agent_idx, 0, 0] == 1).float()
        trigger1 = trigger1.view(bs, 1, 1, 1)
        
        # For object mode
        if mode == 'object':
            mask[:, agent_idx, 3, :] += trigger1  # Send to Agent 3
        else:
            # Send "At border, waiting" - encode as sending current_state dimension
            mask[:, agent_idx, 3, 0:1] += trigger1  # Send current_state feature
        
        # Trigger 2: When agent receives "Ready to sync" from Agent 3 and is at state 1
        # Check if Agent 3 sent "Ready to sync" (state 2)
        agent3_state = current_states_self[:, 3, 0, 0]  # (bs,)
        agent3_ready = (agent3_state == 2).float().view(bs, 1, 1, 1)
        
        trigger2 = (current_states_self[:, agent_idx, 0, 0] == 1).float() * agent3_ready
        trigger2 = trigger2.view(bs, 1, 1, 1)
        
        if mode == 'object':
            mask[:, agent_idx, 3, :] += trigger2  # Send to Agent 3
        else:
            # Send "Acknowledged, ready" - encode as sending active_status dimension
            mask[:, agent_idx, 3, 1:2] += trigger2  # Send active_status feature
        
        # Trigger 3: When agent receives "Final move" from Agent 3
        # Check if Agent 3 sent "Final move" (state 1 after receiving acknowledgments)
        # This requires tracking acknowledgments - simplified implementation
        # We'll assume Agent 3 sends "Final move" when at state 1
        agent3_final = (agent3_state == 1).float().view(bs, 1, 1, 1)
        
        trigger3 = agent3_final  # Receive final move from Agent 3
        
        if mode == 'object':
            mask[:, agent_idx, 3, :] += trigger3  # Send to Agent 3
        else:
            # Send "Moving now" - encode as sending both features
            mask[:, agent_idx, 3, :] += trigger3  # Send all features
    
    # ========== AGENT 3 POLICY ==========
    # Trigger 1: When Agent 3 reaches state 2
    trigger3_1 = (current_states_self[:, 3, 0, 0] == 2).float()
    trigger3_1 = trigger3_1.view(bs, 1, 1, 1)
    
    if mode == 'object':
        # Send to Agents 0, 1, 2
        mask[:, 3, 0, :] += trigger3_1
        mask[:, 3, 1, :] += trigger3_1
        mask[:, 3, 2, :] += trigger3_1
    else:
        # Send "Ready to sync" - encode as sending current_state dimension
        mask[:, 3, 0, 0:1] += trigger3_1
        mask[:, 3, 1, 0:1] += trigger3_1
        mask[:, 3, 2, 0:1] += trigger3_1
    
    # Trigger 2: When Agent 3 has received "Acknowledged, ready" from all agents 0-2 and is at state 1
    # Check if agents 0-2 are at state 1 (waiting position)
    agents_0_2_at_state1 = (
        (current_states_self[:, 0, 0, 0] == 1).float() *
        (current_states_self[:, 1, 0, 0] == 1).float() *
        (current_states_self[:, 2, 0, 0] == 1).float()
    )
    
    # Check if Agent 3 is at state 1
    agent3_at_state1 = (current_states_self[:, 3, 0, 0] == 1).float()
    
    trigger3_2 = agents_0_2_at_state1 * agent3_at_state1
    trigger3_2 = trigger3_2.view(bs, 1, 1, 1)
    
    if mode == 'object':
        # Send to Agents 0, 1, 2
        mask[:, 3, 0, :] += trigger3_2
        mask[:, 3, 1, :] += trigger3_2
        mask[:, 3, 2, :] += trigger3_2
    else:
        # Send "Final move" - encode as sending active_status dimension
        mask[:, 3, 0, 1:2] += trigger3_2
        mask[:, 3, 1, 1:2] += trigger3_2
        mask[:, 3, 2, 1:2] += trigger3_2
    
    # ========== POST-PROCESSING ==========
    # Clip mask values to 0 or 1
    mask = torch.clamp(mask, 0, 1)
    
    # For object_content mode, ensure if object not selected, all content is 0
    if mode == 'object_content':
        # Create object mask by checking if any content dimension is 1
        object_mask = torch.any(mask > 0.5, dim=-1, keepdim=True).float()  # (bs, n_agents, n_agents, 1)
        # Expand object mask to content dimensions
        object_mask_expanded = object_mask.expand(-1, -1, -1, obs_dim)
        # Apply object mask to content mask
        mask = mask * object_mask_expanded
    
    # Ensure self-communication is always 0 (agents don't send to themselves)
    for i in range(n_agents):
        mask[:, i, i, :] = 0
    
    return mask

# Test the function
if __name__ == "__main__":
    # Test with random data
    obs = torch.randn(2, 4, 4, 2)
    
    # Test all modes
    mask_object = generate_mask(obs, mode='object')
    mask_content = generate_mask(obs, mode='content')
    mask_object_content = generate_mask(obs, mode='object_content')
    
    print(f"Object mask shape: {mask_object.shape}")
    print(f"Content mask shape: {mask_content.shape}")
    print(f"Object-content mask shape: {mask_object_content.shape}")
    
    # Test with specific states to verify triggers
    test_obs = torch.zeros(1, 4, 4, 2)
    # Set Agent 0 at state 1
    test_obs[0, 0, 0, 0] = 1
    # Set Agent 3 at state 2
    test_obs[0, 3, 3, 0] = 2
    
    test_mask = generate_mask(test_obs, mode='object_content')
    print(f"\nTest mask shape: {test_mask.shape}")
    print(f"Agent 0 to Agent 3 communication: {test_mask[0, 0, 3, :]}")
    print(f"Agent 3 to Agent 0 communication: {test_mask[0, 3, 0, :]}")