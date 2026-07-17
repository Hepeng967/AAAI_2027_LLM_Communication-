import torch

def generate_mask(obs, mode='object'):
    device = obs.device
    assert mode in ['object', 'content', 'object_content']
    bs, n_agents, _, obs_dim = obs.shape
    
    # Print actual observation shape for debugging
    # print(f"DEBUG: obs shape = {obs.shape}, obs_dim = {obs_dim}")
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), dtype=torch.float32, device=device)
    else:
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=device)
    
    # Get relevant observation indices - check bounds first
    enemy_avail_indices = [4, 11, 18, 25]
    enemy_dist_indices = [5, 12, 19, 26]
    enemy_rel_x_indices = [6, 13, 20, 27]
    enemy_rel_y_indices = [7, 14, 21, 28]
    ally_health_indices = [36, 43]
    own_health_index = 45
    rel_pos_indices = [34, 35, 41, 42]  # ally_0_rel_x, ally_0_rel_y, ally_1_rel_x, ally_1_rel_y
    
    # Validate indices are within bounds
    max_index = max(enemy_avail_indices + enemy_dist_indices + enemy_rel_x_indices + 
                   enemy_rel_y_indices + ally_health_indices + [own_health_index] + rel_pos_indices)
    
    if max_index >= obs_dim:
        print(f"WARNING: Index {max_index} exceeds obs_dim {obs_dim}. Using safe fallback.")
        # Use safe fallback - create a simple mask
        if mode == 'object':
            mask = torch.ones((bs, n_agents, n_agents, 1), dtype=torch.float32, device=device)
        else:
            mask = torch.ones((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=device)
        return mask
    
    # Overseer (Agent 0) communication logic
    # Condition 1: Any enemy detected
    try:
        any_enemy_detected = torch.any(obs[:, 0, :, enemy_avail_indices] > 0, dim=-1)  # (bs, n_agents)
        any_enemy_detected = any_enemy_detected.unsqueeze(-1).unsqueeze(-1)  # (bs, n_agents, 1, 1)
    except Exception as e:
        print(f"ERROR in enemy detection: {e}")
        any_enemy_detected = torch.zeros((bs, n_agents, 1, 1), dtype=torch.float32, device=device)
    
    # Condition 2: Ally health below 50%
    try:
        ally0_low_health = (obs[:, 0, :, 36] < 0.5).unsqueeze(-1).unsqueeze(-1)  # (bs, n_agents, 1, 1)
        ally1_low_health = (obs[:, 0, :, 43] < 0.5).unsqueeze(-1).unsqueeze(-1)  # (bs, n_agents, 1, 1)
    except Exception as e:
        print(f"ERROR in ally health check: {e}")
        ally0_low_health = torch.zeros((bs, n_agents, 1, 1), dtype=torch.float32, device=device)
        ally1_low_health = torch.zeros((bs, n_agents, 1, 1), dtype=torch.float32, device=device)
    
    # Roach communication logic (Agents 1 and 2)
    # Health drop condition (more than 20% in one step)
    try:
        health_drop = (obs[:, 1:, :, own_health_index] < 0.8).unsqueeze(-1).unsqueeze(-1)  # (bs, 2, n_agents, 1, 1)
    except Exception as e:
        print(f"ERROR in health drop check: {e}")
        health_drop = torch.zeros((bs, 2, n_agents, 1, 1), dtype=torch.float32, device=device)
    
    # Overseer to Roaches communication (Condition 1)
    if mode == 'object':
        # Agent 0 communicates with Agents 1 and 2 when any enemy detected
        mask[:, 0, 1:, 0] = any_enemy_detected[:, 0, :2, 0].float()
        
        # Agent 0 communicates with injured Roach (Condition 2)
        mask[:, 0, 1, 0] = torch.logical_or(mask[:, 0, 1, 0], ally0_low_health[:, 0, 0, 0]).float()
        mask[:, 0, 2, 0] = torch.logical_or(mask[:, 0, 2, 0], ally1_low_health[:, 0, 0, 0]).float()
        
        # Roaches communicate with each other when health drops
        mask[:, 1, 2, 0] = health_drop[:, 0, 1, 0, 0].float()
        mask[:, 2, 1, 0] = health_drop[:, 1, 2, 0, 0].float()
    
    elif mode == 'content':
        # All agents can potentially communicate, but we control the content
        # Agent 0 to Agents 1 and 2: enemy info when detected
        enemy_content = torch.zeros((bs, n_agents, obs_dim), dtype=torch.float32, device=device)
        for i, enemy_idx in enumerate(enemy_avail_indices):
            enemy_mask = obs[:, 0, :, enemy_idx] > 0
            enemy_content[:, :, enemy_dist_indices[i]] = enemy_mask.float()
            enemy_content[:, :, enemy_rel_x_indices[i]] = enemy_mask.float()
            enemy_content[:, :, enemy_rel_y_indices[i]] = enemy_mask.float()
        
        # Expand to agent pairs
        enemy_content = enemy_content.unsqueeze(1).expand(-1, n_agents, -1, -1)  # (bs, n_agents, n_agents, obs_dim)
        mask[:, 0, :, :] = enemy_content[:, 0, :, :]
        
        # Agent 0 to injured Roach: retreat signal (use ally_health as placeholder)
        mask[:, 0, 1, ally_health_indices[0]] = ally0_low_health[:, 0, 0, 0].float()
        mask[:, 0, 2, ally_health_indices[1]] = ally1_low_health[:, 0, 0, 0].float()
        
        # Roaches to each other: help request + position
        for i in [1, 2]:
            other = 2 if i == 1 else 1
            mask[:, i, other, own_health_index] = health_drop[:, i-1, other, 0, 0].float()
            mask[:, i, other, rel_pos_indices[2*(i-1)]] = health_drop[:, i-1, other, 0, 0].float()  # rel_x
            mask[:, i, other, rel_pos_indices[2*(i-1)+1]] = health_drop[:, i-1, other, 0, 0].float()  # rel_y
    
    elif mode == 'object_content':
        # Agent 0 to Agents 1 and 2: enemy info when detected
        enemy_content = torch.zeros((bs, 2, obs_dim), dtype=torch.float32, device=device)
        for i, enemy_idx in enumerate(enemy_avail_indices):
            enemy_mask = obs[:, 0, :, enemy_idx] > 0
            enemy_content[:, :, enemy_dist_indices[i]] = enemy_mask[:, :2].float()
            enemy_content[:, :, enemy_rel_x_indices[i]] = enemy_mask[:, :2].float()
            enemy_content[:, :, enemy_rel_y_indices[i]] = enemy_mask[:, :2].float()
        
        # Apply only when any enemy detected
        enemy_content = enemy_content * any_enemy_detected[:, 0, :2, 0].float().unsqueeze(-1)
        mask[:, 0, 1:3, :] = enemy_content
        
        # Agent 0 to injured Roach: retreat signal
        mask[:, 0, 1, ally_health_indices[0]] = ally0_low_health[:, 0, 0, 0].float()
        mask[:, 0, 2, ally_health_indices[1]] = ally1_low_health[:, 0, 0, 0].float()
        
        # Roaches to each other: help request + position
        for i in [1, 2]:
            other = 2 if i == 1 else 1
            mask[:, i, other, own_health_index] = health_drop[:, i-1, other, 0, 0].float()
            mask[:, i, other, rel_pos_indices[2*(i-1)]] = health_drop[:, i-1, other, 0, 0].float()  # rel_x
            mask[:, i, other, rel_pos_indices[2*(i-1)+1]] = health_drop[:, i-1, other, 0, 0].float()  # rel_y
    
    return mask

# # Test code
# if __name__ == "__main__":
#     obs = torch.randn(2, 3, 3, 49)
#     mask = generate_mask(obs, mode='object_content')
#     print(mask)  # Should be (2, 3, 3, 49)