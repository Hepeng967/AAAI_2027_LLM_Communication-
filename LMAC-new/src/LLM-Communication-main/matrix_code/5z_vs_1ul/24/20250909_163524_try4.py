Here's the complete and fixed implementation of the generate_mask function:

```python
import torch

def generate_mask(obs, mode='object'):
    bs, n_agents, _, obs_dim = obs.shape
    assert n_agents == 5, "Expected 5 agents"
    assert obs_dim == 35, "Expected 35 observation dimensions"
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros(bs, n_agents, n_agents, 1, device=obs.device, dtype=obs.dtype)
    elif mode in ['content', 'object_content']:
        mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=obs.device, dtype=obs.dtype)
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    # Observation feature indices
    enemy_0_available_idx = 4
    enemy_0_rel_x_idx = 6
    enemy_0_rel_y_idx = 7
    enemy_0_health_idx = 8
    own_health_idx = 33
    
    # For each agent, implement their specific communication policy
    for agent_id in range(n_agents):
        # Get this agent's observation
        agent_obs = obs[:, agent_id, agent_id, :]  # shape: (bs, obs_dim)
        
        # Trigger 1: First to spot enemy
        enemy_spotted = (agent_obs[:, enemy_0_available_idx] == 1).float()  # shape: (bs,)
        
        if mode == 'object':
            # Send to all other agents
            targets = torch.ones(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
            targets[:, agent_id] = 0  # Don't send to self
            mask[:, agent_id, :, 0] += enemy_spotted.unsqueeze(1) * targets  # (bs, 1) * (bs, n_agents)
        else:
            # Create content mask for enemy spotted message
            content_mask = torch.zeros(bs, obs_dim, device=obs.device)  # shape: (bs, obs_dim)
            content_mask[:, enemy_0_rel_x_idx] = 1
            content_mask[:, enemy_0_rel_y_idx] = 1
            
            if mode == 'content':
                # Send to all other agents
                targets = torch.ones(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                targets[:, agent_id] = 0
                # Expand dimensions for broadcasting
                expanded_enemy_spotted = enemy_spotted.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
                expanded_targets = targets.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
                expanded_content = content_mask.unsqueeze(1).unsqueeze(1)  # (bs, 1, 1, obs_dim)
                mask[:, agent_id, :, :] += expanded_enemy_spotted * expanded_targets * expanded_content
            else:  # object_content
                # Send to all other agents
                targets = torch.ones(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                targets[:, agent_id] = 0
                # Expand dimensions for broadcasting
                expanded_enemy_spotted = enemy_spotted.unsqueeze(1).unsqueeze(2)  # (bs, 1, 1)
                expanded_targets = targets.unsqueeze(2)  # (bs, n_agents, 1)
                expanded_content = content_mask.unsqueeze(1)  # (bs, 1, obs_dim)
                mask[:, agent_id, :, :] += expanded_enemy_spotted * expanded_targets * expanded_content
        
        # Trigger 2: Low health request help
        low_health = (agent_obs[:, own_health_idx] < 50).float()  # shape: (bs,)
        
        # Find nearest visible ally
        ally_distances = []
        for ally_id in range(n_agents):
            if ally_id != agent_id:
                # Get distance to this ally (indices: 10, 16, 22, 28 for allies 0,1,2,3,4 respectively)
                dist_idx = 10 + 6 * (ally_id if ally_id < agent_id else ally_id - 1)
                visible_idx = 9 + 6 * (ally_id if ally_id < agent_id else ally_id - 1)
                
                distance = agent_obs[:, dist_idx]  # shape: (bs,)
                visible = agent_obs[:, visible_idx] == 1  # shape: (bs,)
                
                # Set distance to infinity if not visible
                distance = torch.where(visible, distance, torch.full_like(distance, float('inf')))
                ally_distances.append(distance.unsqueeze(1))  # shape: (bs, 1)
            else:
                # Self distance is infinity
                ally_distances.append(torch.full((bs, 1), float('inf'), device=obs.device))
        
        ally_distances = torch.cat(ally_distances, dim=1)  # shape: (bs, n_agents)
        nearest_ally = torch.argmin(ally_distances, dim=1)  # shape: (bs,)
        
        if mode == 'object':
            # One-hot encoding of nearest ally
            nearest_ally_onehot = torch.zeros(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
            nearest_ally_onehot.scatter_(1, nearest_ally.unsqueeze(1), 1)
            mask[:, agent_id, :, 0] += low_health.unsqueeze(1) * nearest_ally_onehot  # (bs, 1) * (bs, n_agents)
        else:
            # Create content mask for help request
            content_mask = torch.zeros(bs, obs_dim, device=obs.device)  # shape: (bs, obs_dim)
            
            if mode == 'content':
                # Send to nearest ally
                nearest_ally_onehot = torch.zeros(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                nearest_ally_onehot.scatter_(1, nearest_ally.unsqueeze(1), 1)
                # Expand dimensions for broadcasting
                expanded_low_health = low_health.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
                expanded_targets = nearest_ally_onehot.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
                expanded_content = content_mask.unsqueeze(1).unsqueeze(1)  # (bs, 1, 1, obs_dim)
                mask[:, agent_id, :, :] += expanded_low_health * expanded_targets * expanded_content
            else:  # object_content
                nearest_ally_onehot = torch.zeros(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                nearest_ally_onehot.scatter_(1, nearest_ally.unsqueeze(1), 1)
                # Expand dimensions for broadcasting
                expanded_low_health = low_health.unsqueeze(1).unsqueeze(2)  # (bs, 1, 1)
                expanded_targets = nearest_ally_onehot.unsqueeze(2)  # (bs, n_agents, 1)
                expanded_content = content_mask.unsqueeze(1)  # (bs, 1, obs_dim)
                mask[:, agent_id, :, :] += expanded_low_health * expanded_targets * expanded_content
        
        # Trigger 3: Agent-specific conditions
        if agent_id == 0:
            # Check if any ally health < 30%
            for ally_id in range(n_agents):
                if ally_id != agent_id:
                    health_idx = 13 + 6 * (ally_id if ally_id < agent_id else ally_id - 1)
                    ally_low_health = (agent_obs[:, health_idx] < 30).float()  # shape: (bs,)
                    
                    if mode == 'object':
                        # Send to all other agents
                        targets = torch.ones(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                        targets[:, agent_id] = 0
                        mask[:, agent_id, :, 0] += ally_low_health.unsqueeze(1) * targets  # (bs, 1) * (bs, n_agents)
                    else:
                        # Create content mask for ally critical message
                        content_mask = torch.zeros(bs, obs_dim, device=obs.device)  # shape: (bs, obs_dim)
                        rel_x_idx = 11 + 6 * (ally_id if ally_id < agent_id else ally_id - 1)
                        rel_y_idx = 12 + 6 * (ally_id if ally_id < agent_id else ally_id - 1)
                        content_mask[:, rel_x_idx] = 1
                        content_mask[:, rel_y_idx] = 1
                        
                        if mode == 'content':
                            targets = torch.ones(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                            targets[:, agent_id] = 0
                            # Expand dimensions for broadcasting
                            expanded_ally_health = ally_low_health.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
                            expanded_targets = targets.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
                            expanded_content = content_mask.unsqueeze(1).unsqueeze(1)  # (bs, 1, 1, obs_dim)
                            mask[:, agent_id, :, :] += expanded_ally_health * expanded_targets * expanded_content
                        else:
                            targets = torch.ones(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                            targets[:, agent_id] = 0
                            # Expand dimensions for broadcasting
                            expanded_ally_health = ally_low_health.unsqueeze(1).unsqueeze(2)  # (bs, 1, 1)
                            expanded_targets = targets.unsqueeze(2)  # (bs, n_agents, 1)
                            expanded_content = content_mask.unsqueeze(1)  # (bs, 1, obs_dim)
                            mask[:, agent_id, :, :] += expanded_ally_health * expanded_targets * expanded_content
        
        elif agent_id == 1:
            # Check if Ultralisk is focusing on a single ally
            # Simplified: if any ally health is decreasing rapidly
            for ally_id in range(n_agents):
                if ally_id != agent_id:
                    health_idx = 13 + 6 * (ally_id if ally_id < agent_id else ally_id - 1)
                    ally_focused = (agent_obs[:, health_idx] < 70).float()  # shape: (bs,)
                    
                    if mode == 'object':
                        # Send to the focused ally
                        target_mask = torch.zeros(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                        target_mask[:, ally_id] = 1
                        mask[:, agent_id, :, 0] += ally_focused.unsqueeze(1) * target_mask  # (bs, 1) * (bs, n_agents)
                    else:
                        # Create content mask for fall back message
                        content_mask = torch.zeros(bs, obs_dim, device=obs.device)  # shape: (bs, obs_dim)
                        
                        if mode == 'content':
                            target_mask = torch.zeros(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                            target_mask[:, ally_id] = 1
                            # Expand dimensions for broadcasting
                            expanded_ally_focused = ally_focused.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
                            expanded_targets = target_mask.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
                            expanded_content = content_mask.unsqueeze(1).unsqueeze(1)  # (bs, 1, 1, obs_dim)
                            mask[:, agent_id, :, :] += expanded_ally_focused * expanded_targets * expanded_content
                        else:
                            target_mask = torch.zeros(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                            target_mask[:, ally_id] = 1
                            # Expand dimensions for broadcasting
                            expanded_ally_focused = ally_focused.unsqueeze(1).unsqueeze(2)  # (bs, 1, 1)
                            expanded_targets = target_mask.unsqueeze(2)  # (bs, n_agents, 1)
                            expanded_content = content_mask.unsqueeze(1)  # (bs, 1, obs_dim)
                            mask[:, agent_id, :, :] += expanded_ally_focused * expanded_targets * expanded_content
        
        elif agent_id == 2:
            # Check if allies are too clustered
            # Count number of allies with distance < threshold
            close_allies = torch.zeros(bs, device=obs.device)  # shape: (bs,)
            for ally_id in range(n_agents):
                if ally_id != agent_id:
                    dist_idx = 10 + 6 * (ally_id if ally_id < agent_id else ally_id - 1)
                    close_allies += (agent_obs[:, dist_idx] < 5).float()  # shape: (bs,)
            
            clustered = (close_allies >= 2).float()  # shape: (bs,)
            
            if mode == 'object':
                # Find closest ally
                closest_ally = torch.argmin(ally_distances, dim=1)  # shape: (bs,)
                target_mask = torch.zeros(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                target_mask.scatter_(1, closest_ally.unsqueeze(1), 1)
                mask[:, agent_id, :, 0] += clustered.unsqueeze(1) * target_mask  # (bs, 1) * (bs, n_agents)
            else:
                # Create content mask for spread out message
                content_mask = torch.zeros(bs, obs_dim, device=obs.device)  # shape: (bs, obs_dim)
                
                if mode == 'content':
                    closest_ally = torch.argmin(ally_distances, dim=1)  # shape: (bs,)
                    target_mask = torch.zeros(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                    target_mask.scatter_(1, closest_ally.unsqueeze(1), 1)
                    # Expand dimensions for broadcasting
                    expanded_clustered = clustered.unsqueeze(1).unsqueeze(2).unsqueeze(3)  # (bs, 1, 1, 1)
                    expanded_targets = target_mask.unsqueeze(2).unsqueeze(3)  # (bs, n_agents, 1, 1)
                    expanded_content = content_mask.unsqueeze(1).unsqueeze(1)  # (bs, 1, 1, obs_dim)
                    mask[:, agent_id, :, :] += expanded_clustered * expanded_targets * expanded_content
                else:
                    closest_ally = torch.argmin(ally_distances, dim=1)  # shape: (bs,)
                    target_mask = torch.zeros(bs, n_agents, device=obs.device)  # shape: (bs, n_agents)
                    target_mask.scatter_(1, closest_ally.unsqueeze(1), 1)
                    # Expand dimensions for broadcasting
                    expanded_clustered = clustered.unsqueeze(1).unsqueeze(2)  # (bs, 1, 1)
                    expanded_targets = target_mask.unsqueeze(2)  # (bs, n_agents, 1)
                    expanded_content = content_mask.unsqueeze(1)  # (bs, 1, obs