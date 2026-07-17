import torch

def generate_mask(obs, mode='object'):
    # obs shape: (bs, n_agents, n_agents, obs_dim)
    bs, n_agents, _, obs_dim = obs.shape
    assert n_agents == 5, "Expected 5 agents"
    assert obs_dim == 35, "Expected 35 observation dimensions"
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), dtype=torch.float32, device=obs.device)
    elif mode == 'content':
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=obs.device)
    elif mode == 'object_content':
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=obs.device)
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    # Extract health information
    # own_health is at index 33
    own_health = obs[..., 33]  # shape: (bs, n_agents, n_agents)
    
    # Ally health indices: 13, 19, 25, 31 for allies 0, 1, 2, 3 respectively
    ally_health_indices = [13, 19, 25, 31]
    
    # Create a tensor for ally health (bs, n_agents, n_agents, 4)
    ally_health = torch.stack([obs[..., idx] for idx in ally_health_indices], dim=-1)
    
    # Create identity matrix to exclude self from "all other agents"
    identity = torch.eye(n_agents, device=obs.device).unsqueeze(0).unsqueeze(-1)  # (1, n_agents, n_agents, 1)
    identity = identity.expand(bs, n_agents, n_agents, 1)
    
    # Condition 1: Own health < 20%
    low_health_mask = (own_health < 0.2).float()  # (bs, n_agents, n_agents)
    
    # For all other agents (exclude self)
    all_other_agents = (1.0 - identity.squeeze(-1))  # (bs, n_agents, n_agents)
    
    # Condition 1: Send to all other agents when own health < 20%
    cond1_mask = low_health_mask.unsqueeze(-1) * all_other_agents.unsqueeze(-1)  # (bs, n_agents, n_agents, 1)
    
    # Condition 2: Ally health < 20% and Ultralisk targeting (simplified: assume always true for now)
    # Check if any ally has health < 20%
    ally_low_health = (ally_health < 0.2).any(dim=-1).float()  # (bs, n_agents, n_agents)
    cond2_mask = ally_low_health.unsqueeze(-1) * all_other_agents.unsqueeze(-1)  # (bs, n_agents, n_agents, 1)
    
    # Condition 3: Ultralisk not engaged (simplified: always true for now)
    # Find nearest healthy ally (health > 80%)
    healthy_allies = (ally_health > 0.8).float()  # (bs, n_agents, n_agents, 4)
    
    # Get distances to allies (indices: 10, 16, 22, 28)
    ally_dist_indices = [10, 16, 22, 28]
    ally_distances = torch.stack([obs[..., idx] for idx in ally_dist_indices], dim=-1)  # (bs, n_agents, n_agents, 4)
    
    # Mask out unhealthy allies and self (set distance to very high)
    masked_distances = ally_distances + (1.0 - healthy_allies) * 1000.0
    
    # Find nearest healthy ally for each agent
    min_dist, nearest_ally_idx = masked_distances.min(dim=-1)  # (bs, n_agents, n_agents)
    
    # Create one-hot encoding for nearest healthy ally
    nearest_ally_mask = torch.zeros_like(healthy_allies[..., 0])  # (bs, n_agents, n_agents)
    for i in range(4):  # For each ally index
        ally_mask = (nearest_ally_idx == i).float()
        nearest_ally_mask = nearest_ally_mask + ally_mask
    
    cond3_mask = nearest_ally_mask.unsqueeze(-1)  # (bs, n_agents, n_agents, 1)
    
    # Combine all conditions
    if mode == 'object':
        # Any condition triggers communication to target
        object_mask = ((cond1_mask + cond2_mask + cond3_mask) > 0).float()
        mask = object_mask
    elif mode == 'content':
        # All agents can communicate, but we need to select content
        # For simplicity, we'll set all content to 1 when any condition is met
        content_mask = ((cond1_mask + cond2_mask + cond3_mask) > 0).float()
        content_mask = content_mask.expand(bs, n_agents, n_agents, obs_dim)
        mask = content_mask
    elif mode == 'object_content':
        # Combine object and content selection
        object_mask = ((cond1_mask + cond2_mask + cond3_mask) > 0).float()
        object_mask = object_mask.expand(bs, n_agents, n_agents, obs_dim)
        mask = object_mask
    
    return mask

# Test the function
if __name__ == "__main__":
    # Test with the required shape
    obs = torch.randn(2, 5, 5, 35)
    mask = generate_mask(obs, mode='object_content')
    print(mask.shape)  # Should be (2, 5, 5, 35)
    
    # Test other modes
    mask_obj = generate_mask(obs, mode='object')
    print(mask_obj.shape)  # Should be (2, 5, 5, 1)
    
    mask_content = generate_mask(obs, mode='content')
    print(mask_content.shape)  # Should be (2, 5, 5, 35)