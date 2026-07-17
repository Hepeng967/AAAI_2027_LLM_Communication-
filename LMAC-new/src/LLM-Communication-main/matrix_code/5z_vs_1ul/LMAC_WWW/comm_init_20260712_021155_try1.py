import torch

def message_design_instruction():
    return """
    WHO: All-to-all broadcast (every agent sends to every other agent).
    WHEN: A sender triggers communication if its own health < 0.20 OR it sees any visible ally with health < 0.20.
    WHAT: 
      - If sender is wounded (own_health < 0.20): broadcast own_health (index 33) and own_shield (index 34) as 1s.
      - Else if sender sees a wounded ally (first visible ally with health < 0.20): broadcast that ally's rel_x, rel_y, and health as 1s.
      - Else: send all zeros.
    """

def communication_who(o):
    batch, n_agents, obs_dim = o.shape
    # All-to-all, but diagonal is zero (self-communication disabled)
    who = torch.ones(batch, n_agents, n_agents, device=o.device)
    who[:, range(n_agents), range(n_agents)] = 0
    return who

def communication_when(o):
    batch, n_agents, obs_dim = o.shape
    device = o.device
    
    # Initialize all edges as inactive
    when = torch.zeros(batch, n_agents, n_agents, device=device)
    
    # For each sender, determine if trigger condition is met
    # Trigger condition: own_health < 0.20 (index 33) OR any visible ally with health < 0.20
    own_health_idx = 33
    ally_visible_indices = [9, 15, 21, 27]  # indices for ally_i_visible (each is a single feature)
    ally_health_indices = [13, 19, 25, 31]  # indices for ally_i_health
    
    for sender in range(n_agents):
        sender_own_health = o[:, sender, own_health_idx] if own_health_idx < obs_dim else torch.tensor(1.0, device=device)
        
        # Check sender's own health
        sender_wounded = sender_own_health < 0.20 if own_health_idx < obs_dim else False
        
        # Check if sender sees any wounded ally
        sees_wounded_ally = torch.zeros(batch, device=device, dtype=torch.bool)
        if own_health_idx < obs_dim:
            for vis_idx, heal_idx in zip(ally_visible_indices, ally_health_indices):
                if vis_idx < obs_dim and heal_idx < obs_dim:
                    visible = o[:, sender, vis_idx] == 1
                    ally_wounded = o[:, sender, heal_idx] < 0.20
                    sees_wounded_ally = sees_wounded_ally | (visible & ally_wounded)
        
        trigger = sender_wounded | sees_wounded_ally
        
        # Set all edges from this sender to be active if trigger is true
        when[:, :, sender] = trigger.float().unsqueeze(1).expand(-1, n_agents)
    
    # Remove self-communication (diagonal must be zero)
    when[:, range(n_agents), range(n_agents)] = 0
    
    return when

def communication_what(o):
    batch, n_agents, obs_dim = o.shape
    device = o.device
    
    # Initialize output as all zeros
    what = torch.zeros(batch, n_agents, obs_dim, device=device)
    
    own_health_idx = 33
    own_shield_idx = 34
    
    ally_visible_indices = [9, 15, 21, 27]
    ally_rel_x_indices = [11, 17, 23, 29]
    ally_rel_y_indices = [12, 18, 24, 30]
    ally_health_indices = [13, 19, 25, 31]
    
    for sender in range(n_agents):
        # Case 1: Sender is wounded
        if own_health_idx < obs_dim:
            sender_wounded = o[:, sender, own_health_idx] < 0.20
            for b in range(batch):
                if sender_wounded[b]:
                    if own_health_idx < obs_dim:
                        what[b, sender, own_health_idx] = 1.0
                    if own_shield_idx < obs_dim:
                        what[b, sender, own_shield_idx] = 1.0
                    continue  # Skip to next sender, wounded takes priority
        
        # Case 2: Check for visible wounded ally
        found_wounded = torch.zeros(batch, device=device, dtype=torch.bool)
        for vis_idx, rx_idx, ry_idx, heal_idx in zip(ally_visible_indices, ally_rel_x_indices, ally_rel_y_indices, ally_health_indices):
            if max(vis_idx, rx_idx, ry_idx, heal_idx) >= obs_dim:
                continue
            visible = o[:, sender, vis_idx] == 1
            ally_wounded = o[:, sender, heal_idx] < 0.20
            candidate = visible & ally_wounded & ~found_wounded
            
            for b in range(batch):
                if candidate[b]:
                    what[b, sender, rx_idx] = 1.0
                    what[b, sender, ry_idx] = 1.0
                    what[b, sender, heal_idx] = 1.0
                    found_wounded[b] = True
        
        # Case 3: No trigger - already all zeros, nothing to do
    
    return what