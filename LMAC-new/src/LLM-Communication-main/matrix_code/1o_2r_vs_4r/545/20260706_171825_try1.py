import torch

def generate_mask(obs, mode='object'):
    """
    Implements communication policy for Overseer (agent 0) and Roaches (agents 1 and 2).
    
    Args:
        obs: torch tensor of shape (bs, n_agents, n_agents, obs_dim) 
             Note: n_agents=3, obs_dim=49 (but we'll use last dimension from obs)
        mode: 'object', 'content', or 'object_content'
    
    Returns:
        mask tensor of appropriate shape based on mode
    """
    bs, n_agents, _, obs_dim = obs.shape
    
    # Extract feature indices for readability
    # Enemy features for up to 4 enemies
    enemy_available_indices = [4, 11, 18, 25]  # enemy_0_available, enemy_1_available, etc.
    enemy_rel_x_indices = [6, 13, 20, 27]
    enemy_rel_y_indices = [7, 14, 21, 28]
    enemy_health_indices = [8, 15, 22, 29]
    enemy_type_0_indices = [9, 16, 23, 30]
    enemy_type_1_indices = [10, 17, 24, 31]
    
    # Ally visibility features (ally_0_visible at index 32, ally_1_visible at index 39)
    ally_visible_indices = [32, 39]
    
    # Own health at index 46
    own_health_idx = 46
    
    # ===================== OBJECT MODE =====================
    if mode == 'object':
        # Initialize mask: (bs, n_agents, n_agents, 1)
        mask = torch.zeros((bs, n_agents, n_agents, 1), device=obs.device, dtype=torch.float32)
        
        # ---- Agent 0 (Overseer) communication ----
        # Trigger 1: any enemy available
        # For each agent, check if they have any enemy available
        agent_obs = obs[:, 0, :, :]  # (bs, n_agents, obs_dim) - but we want agent's own obs
        # Actually, in this setup, each agent's observation is at obs[:, agent_idx, agent_idx, :]
        # But the policy describes what the agent observes from its own perspective.
        # The obs tensor is (bs, n_agents, n_agents, obs_dim) which is unusual.
        # Let's interpret: for agent i, its observation is at obs[b, i, i, :] (diagonal elements)
        
        # Get each agent's own observation: (bs, n_agents, obs_dim)
        own_obs = torch.zeros((bs, n_agents, obs_dim), device=obs.device, dtype=obs.dtype)
        for i in range(n_agents):
            own_obs[:, i, :] = obs[:, i, i, :]
        
        # Agent 0: check if any enemy is available
        agent0_obs = own_obs[:, 0, :]  # (bs, obs_dim)
        any_enemy_available = torch.zeros(bs, device=obs.device, dtype=torch.bool)
        for idx in enemy_available_indices:
            any_enemy_available = any_enemy_available | (agent0_obs[:, idx] > 0.5)
        
        # Agent 0 sends to agents 1 and 2 when any enemy available
        # Object mask shape: (bs, n_agents, n_agents, 1)
        # Set mask[b, 0, 1, 0] = 1 and mask[b, 0, 2, 0] = 1 where condition is true
        agent0_mask = torch.zeros((bs, 2), device=obs.device, dtype=torch.float32)  # (bs, 2) for target agents 1 and 2
        # Expand any_enemy_available to (bs, 2)
        any_enemy_available_expanded = any_enemy_available.unsqueeze(1).expand(bs, 2).float()
        agent0_mask = any_enemy_available_expanded  # (bs, 2)
        
        # Assign to mask: mask[:, 0, 1:3, 0] = agent0_mask (shape (bs, 2))
        # First ensure agent0_mask has shape (bs, 2)
        mask[:, 0, 1:3, 0] = agent0_mask
        
        # Trigger 2: Overseer under attack (own_health < 100)
        # In this scenario, initial health is 100, so health < 100 means under attack
        health_under_attack = agent0_obs[:, own_health_idx] < 100.0  # (bs,)
        
        # Combine with previous condition (OR): already sent if enemy available, but also send when under attack
        # Actually we should OR them
        combined_agent0 = (any_enemy_available | health_under_attack).float().unsqueeze(1).expand(bs, 2)  # (bs, 2)
        mask[:, 0, 1:3, 0] = torch.maximum(mask[:, 0, 1:3, 0], combined_agent0)
        
        # ---- Agent 1 (Roach 1) communication ----
        # Trigger: directly observes any enemy
        agent1_obs = own_obs[:, 1, :]  # (bs, obs_dim)
        agent1_enemy_available = torch.zeros(bs, device=obs.device, dtype=torch.bool)
        for idx in enemy_available_indices:
            agent1_enemy_available = agent1_enemy_available | (agent1_obs[:, idx] > 0.5)
        
        # Also trigger when own health critically low (< 50) and ally 2 visible
        health_low_agent1 = (agent1_obs[:, own_health_idx] < 50.0)  # (bs,)
        ally2_visible_agent1 = agent1_obs[:, ally_visible_indices[1]] > 0.5  # ally_1_visible (ally index 1 = agent 2)
        
        # Send to agent 0 and agent 2 when enemy observed
        agent1_to_0_and_2 = agent1_enemy_available.float().unsqueeze(1).expand(bs, 2)  # (bs, 2) for targets 0 and 2
        mask[:, 1, 0, 0] = torch.maximum(mask[:, 1, 0, 0], agent1_to_0_and_2[:, 0])
        mask[:, 1, 2, 0] = torch.maximum(mask[:, 1, 2, 0], agent1_to_0_and_2[:, 1])
        
        # Send to agent 2 only when health low and ally visible
        health_low_and_ally_visible_agent1 = (health_low_agent1 & ally2_visible_agent1).float()  # (bs,)
        mask[:, 1, 2, 0] = torch.maximum(mask[:, 1, 2, 0], health_low_and_ally_visible_agent1)
        
        # ---- Agent 2 (Roach 2) communication ----
        # Trigger: directly observes any enemy
        agent2_obs = own_obs[:, 2, :]  # (bs, obs_dim)
        agent2_enemy_available = torch.zeros(bs, device=obs.device, dtype=torch.bool)
        for idx in enemy_available_indices:
            agent2_enemy_available = agent2_enemy_available | (agent2_obs[:, idx] > 0.5)
        
        # Also trigger when own health critically low (< 50) and ally 1 visible
        health_low_agent2 = (agent2_obs[:, own_health_idx] < 50.0)  # (bs,)
        ally1_visible_agent2 = agent2_obs[:, ally_visible_indices[0]] > 0.5  # ally_0_visible (ally index 0 = agent 1)
        
        # Send to agent 0 and agent 1 when enemy observed
        agent2_to_0_and_1 = agent2_enemy_available.float().unsqueeze(1).expand(bs, 2)  # (bs, 2) for targets 0 and 1
        mask[:, 2, 0, 0] = torch.maximum(mask[:, 2, 0, 0], agent2_to_0_and_1[:, 0])
        mask[:, 2, 1, 0] = torch.maximum(mask[:, 2, 1, 0], agent2_to_0_and_1[:, 1])
        
        # Send to agent 1 only when health low and ally visible
        health_low_and_ally_visible_agent2 = (health_low_agent2 & ally1_visible_agent2).float()  # (bs,)
        mask[:, 2, 1, 0] = torch.maximum(mask[:, 2, 1, 0], health_low_and_ally_visible_agent2)
        
        return mask
    
    # ===================== CONTENT MODE =====================
    elif mode == 'content':
        # In content mode, all agents may communicate, but we select which content to send
        # Initialize mask: (bs, n_agents, n_agents, obs_dim)
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=obs.device, dtype=torch.float32)
        
        # Own observations for each agent: (bs, n_agents, obs_dim)
        own_obs = torch.zeros((bs, n_agents, obs_dim), device=obs.device, dtype=obs.dtype)
        for i in range(n_agents):
            own_obs[:, i, :] = obs[:, i, i, :]
        
        # For content mode, we need to decide what each agent sends.
        # Since all agent pairs may communicate, we'll set content for all possible pairs
        # based on what the sending agent would want to communicate.
        
        # For each agent pair (i, j), agent i sends content to agent j.
        # We'll precompute what each agent would send in general.
        
        # Prepare indices for enemy features (for all 4 enemies, all relevant features)
        enemy_rel_x_indices_all = torch.tensor(enemy_rel_x_indices, device=obs.device, dtype=torch.long)
        enemy_rel_y_indices_all = torch.tensor(enemy_rel_y_indices, device=obs.device, dtype=torch.long)
        enemy_health_indices_all = torch.tensor(enemy_health_indices, device=obs.device, dtype=torch.long)
        enemy_type_0_indices_all = torch.tensor(enemy_type_0_indices, device=obs.device, dtype=torch.long)
        enemy_type_1_indices_all = torch.tensor(enemy_type_1_indices, device=obs.device, dtype=torch.long)
        
        # For each agent i, determine which enemy features to communicate based on which enemies are available
        for i in range(n_agents):
            agent_obs = own_obs[:, i, :]  # (bs, obs_dim)
            
            # Determine which enemies are available for this agent
            enemy_available = torch.zeros((bs, len(enemy_available_indices)), device=obs.device, dtype=torch.float32)
            for e_idx, avail_idx in enumerate(enemy_available_indices):
                enemy_available[:, e_idx] = agent_obs[:, avail_idx]
            
            # For each enemy that is available, we want to send: rel_x, rel_y, health, type_0, type_1
            # We'll compute a content mask for sending agent i
            # Shape: (bs, obs_dim) - which features agent i would send to anyone
            
            content_mask_i = torch.zeros((bs, obs_dim), device=obs.device, dtype=torch.float32)
            
            # For each enemy
            for e_idx in range(4):
                # Check if enemy is available
                e_avail = enemy_available[:, e_idx] > 0.5  # (bs,)
                e_avail_float = e_avail.float().unsqueeze(1)  # (bs, 1)
                
                # Set enemy rel_x, rel_y, health, type_0, type_1 for this enemy
                # Using advanced indexing
                # rel_x
                mask_slice = e_avail_float  # (bs, 1)
                content_mask_i[:, enemy_rel_x_indices[e_idx]] = torch.maximum(
                    content_mask_i[:, enemy_rel_x_indices[e_idx]].unsqueeze(1), 
                    mask_slice
                ).squeeze(1)
                # rel_y
                content_mask_i[:, enemy_rel_y_indices[e_idx]] = torch.maximum(
                    content_mask_i[:, enemy_rel_y_indices[e_idx]].unsqueeze(1),
                    mask_slice
                ).squeeze(1)
                # health
                content_mask_i[:, enemy_health_indices[e_idx]] = torch.maximum(
                    content_mask_i[:, enemy_health_indices[e_idx]].unsqueeze(1),
                    mask_slice
                ).squeeze(1)
                # type_0
                content_mask_i[:, enemy_type_0_indices[e_idx]] = torch.maximum(
                    content_mask_i[:, enemy_type_0_indices[e_idx]].unsqueeze(1),
                    mask_slice
                ).squeeze(1)
                # type_1
                content_mask_i[:, enemy_type_1_indices[e_idx]] = torch.maximum(
                    content_mask_i[:, enemy_type_1_indices[e_idx]].unsqueeze(1),
                    mask_slice
                ).squeeze(1)
            
            # Also add own_health for distress signal (agent 0 sends when under attack, agents 1 and 2 when health low)
            if i == 0:  # Overseer
                # Send own_health when under attack (health < 100)
                under_attack = (agent_obs[:, own_health_idx] < 100.0).float()  # (bs,)
                content_mask_i[:, own_health_idx] = torch.maximum(
                    content_mask_i[:, own_health_idx].unsqueeze(1),
                    under_attack.unsqueeze(1)
                ).squeeze(1)
            else:  # Roaches
                # Send own_health when health < 50
                health_low = (agent_obs[:, own_health_idx] < 50.0).float()  # (bs,)
                content_mask_i[:, own_health_idx] = torch.maximum(
                    content_mask_i[:, own_health_idx].unsqueeze(1),
                    health_low.unsqueeze(1)
                ).squeeze(1)
            
            # Now assign content_mask_i to all pairs (i, j) for all j
            # mask[:, i, :, :] should have shape (bs, n_agents, obs_dim)
            # We need to expand content_mask_i from (bs, obs_dim) to (bs, n_agents, obs_dim)
            content_mask_expanded = content_mask_i.unsqueeze(1).expand(bs, n_agents, obs_dim)  # (bs, n_agents, obs_dim)
            mask[:, i, :, :] = content_mask_expanded
        
        return mask
    
    # ===================== OBJECT_CONTENT MODE =====================
    elif mode == 'object_content':
        # Jointly select both communication object and content
        # Initialize mask: (bs, n_agents, n_agents, obs_dim)
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=obs.device, dtype=torch.float32)
        
        # Own observations for each agent: (bs, n_agents, obs_dim)
        own_obs = torch.zeros((bs, n_agents, obs_dim), device=obs.device, dtype=obs.dtype)
        for i in range(n_agents):
            own_obs[:, i, :] = obs[:, i, i, :]
        
        # Get enemy available and health conditions for each agent
        
        # For agent 0 (Overseer)
        agent0_obs = own_obs[:, 0, :]  # (bs, obs_dim)
        any_enemy_available_0 = torch.zeros(bs, device=obs.device, dtype=torch.bool)
        for idx in enemy_available_indices:
            any_enemy_available_0 = any_enemy_available_0 | (agent0_obs[:, idx] > 0.5)
        health_under_attack_0 = agent0_obs[:, own_health_idx] < 100.0  # (bs,)
        
        # Agent 0 sends to agents 1 and 2 when any enemy available OR under attack
        agent0_sends_to_1 = (any_enemy_available_0 | health_under_attack_0).float()  # (bs,)
        agent0_sends_to_2 = agent0_sends_to_1.clone()  # same condition for both targets
        
        # For agent 1 (Roach 1)
        agent1_obs = own_obs[:, 1, :]  # (bs, obs_dim)
        any_enemy_available_1 = torch.zeros(bs, device=obs.device, dtype=torch.bool)
        for idx in enemy_available_indices:
            any_enemy_available_1 = any_enemy_available_1 | (agent1_obs[:, idx] > 0.5)
        health_low_1 = agent1_obs[:, own_health_idx] < 50.0  # (bs,)
        ally2_visible_1 = agent1_obs[:, ally_visible_indices[1]] > 0.5  # (bs,)
        
        # Agent 1 sends to agent 0 when enemy observed
        agent1_sends_to_0 = any_enemy_available_1.float()  # (bs,)
        # Agent 1 sends to agent 2 when enemy observed OR (health low AND ally visible)
        agent1_sends_to_2 = (any_enemy_available_1 | (health_low_1 & ally2_visible_1)).float()  # (bs,)
        
        # For agent 2 (Roach 2)
        agent2_obs = own_obs[:, 2, :]  # (bs, obs_dim)
        any_enemy_available_2 = torch.zeros(bs, device=obs.device, dtype=torch.bool)
        for idx in enemy_available_indices:
            any_enemy_available_2 = any_enemy_available_2 | (agent2_obs[:, idx] > 0.5)
        health_low_2 = agent2_obs[:, own_health_idx] < 50.0  # (bs,)
        ally1_visible_2 = agent2_obs[:, ally_visible_indices[0]] > 0.5  # (bs,)
        
        # Agent 2 sends to agent 0 when enemy observed
        agent2_sends_to_0 = any_enemy_available_2.float()  # (bs,)
        # Agent 2 sends to agent 1 when enemy observed OR (health low AND ally visible)
        agent2_sends_to_1 = (any_enemy_available_2 | (health_low_2 & ally1_visible_2)).float()  # (bs,)
        
        # Now determine content for each sending agent based on why they're sending
        
        # -- Agent 0 content --
        # When sending due to enemy available: send enemy features (rel_x, rel_y, health, type_0, type_1) for available enemies
        # When sending due to under attack: send own_health
        
        # Initialize content for agent0 (what it sends when it communicates)
        content_0 = torch.zeros((bs, obs_dim), device=obs.device, dtype=torch.float32)
        
        # Enemy features: only send for enemies that are available
        for e_idx in range(4):
            e_avail = (agent0_obs[:, enemy_available_indices[e_idx]] > 0.5).float()  # (bs,)
            # If agent 0 sends to anyone and this enemy is available, include its features
            # But content is based on sending agent's observation, not dependent on receiver
            send_to_any = (agent0_sends_to_1 > 0.5) | (agent0_sends_to_2 > 0.5)  # (bs,)
            send_enemy_features = (send_to_any & (e_avail > 0.5)).float()  # (bs,)
            
            # Set features
            content_0[:, enemy_rel_x_indices[e_idx]] = send_enemy_features
            content_0[:, enemy_rel_y_indices[e_idx]] = send_enemy_features
            content_0[:, enemy_health_indices[e_idx]] = send_enemy_features
            content_0[:, enemy_type_0_indices[e_idx]] = send_enemy_features
            content_0[:, enemy_type_1_indices[e_idx]] = send_enemy_features
        
        # own_health when under attack
        under_attack_0 = (health_under_attack_0.float())  # (bs,)
        content_0[:, own_health_idx] = torch.maximum(content_0[:, own_health_idx], under_attack_0)
        
        # Assign agent 0 content to mask for targets 1 and 2
        # mask[:, 0, 1, :] = content_0 (bs, obs_dim) * agent0_sends_to_1 (bs, 1)
        # First unsqueeze to (bs, 1, obs_dim) then assign to specific target indices
        content_0_unsqueezed = content_0.unsqueeze(1)  # (bs, 1, obs_dim)
        
        # For target 1
        agent0_to_1 = agent0_sends_to_1.unsqueeze(1).expand(bs, obs_dim)  # (bs, obs_dim)
        mask[:, 0, 1, :] = content_0 * agent0_to_1
        
        # For target 2
        agent0_to_2 = agent0_sends_to_2.unsqueeze(1).expand(bs, obs_dim)  # (bs, obs_dim)
        mask[:, 0, 2, :] = content_0 * agent0_to_2
        
        # -- Agent 1 content --
        content_1 = torch.zeros((bs, obs_dim), device=obs.device, dtype=torch.float32)
        
        # Enemy features when enemy observed
        for e_idx in range(4):
            e_avail = (agent1_obs[:, enemy_available_indices[e_idx]] > 0.5).float()  # (bs,)
            send_to_any = (agent1_sends_to_0 > 0.5) | (agent1_sends_to_2 > 0.5)  # (bs,)
            send_enemy_features = (send_to_any & (e_avail > 0.5)).float()
            
            content_1[:, enemy_rel_x_indices[e_idx]] = send_enemy_features
            content_1[:, enemy_rel_y_indices[e_idx]] = send_enemy_features
            content_1[:, enemy_health_indices[e_idx]] = send_enemy_features
        
        # own_health when health low and sending to agent 2 (the condition for sending health)
        # But content is about what's in the message, not who receives it. 
        # According to policy: when health low and ally visible, send own_health.
        # So if sending due to that condition, include own_health in the content.
        # We'll include own_health whenever sending to agent 2 (since that's when the condition matters)
        # Actually for simplicity, include own_health whenever health low
        health_low_1_float = health_low_1.float()  # (bs,)
        content_1[:, own_health_idx] = health_low_1_float  # Always include when health low
        
        # Assign agent 1 content to mask for targets 0 and 2
        content_1_unsqueezed = content_1.unsqueeze(1)  # (bs, 1, obs_dim)
        
        # For target 0
        agent1_to_0 = agent1_sends_to_0.unsqueeze(1).expand(bs, obs_dim)  # (bs, obs_dim)
        mask[:, 1, 0, :] = content_1 * agent1_to_0
        
        # For target 2
        agent1_to_2 = agent1_sends_to_2.unsqueeze(1).expand(bs, obs_dim)  # (bs, obs_dim)
        mask[:, 1, 2, :] = content_1 * agent1_to_2
        
        # -- Agent 2 content --
        content_2 = torch.zeros((bs, obs_dim), device=obs.device, dtype=torch.float32)
        
        # Enemy features when enemy observed
        for e_idx in range(4):
            e_avail = (agent2_obs[:, enemy_available_indices[e_idx]] > 0.5).float()  # (bs,)
            send_to_any = (agent2_sends_to_0 > 0.5) | (agent2_sends_to_1 > 0.5)  # (bs,)
            send_enemy_features = (send_to_any & (e_avail > 0.5)).float()
            
            content_2[:, enemy_rel_x_indices[e_idx]] = send_enemy_features
            content_2[:, enemy_rel_y_indices[e_idx]] = send_enemy_features
            content_2[:, enemy_health_indices[e_idx]] = send_enemy_features
        
        # own_health when health low
        health_low_2_float = health_low_2.float()  # (bs,)
        content_2[:, own_health_idx] = health_low_2_float
        
        # Assign agent 2 content to mask for targets 0 and 1
        content_2_unsqueezed = content_2.unsqueeze(1)  # (bs, 1, obs_dim)
        
        # For target 0
        agent2_to_0 = agent2_sends_to_0.unsqueeze(1).expand(bs, obs_dim)  # (bs, obs_dim)
        mask[:, 2, 0, :] = content_2 * agent2_to_0
        
        # For target 1
        agent2_to_1 = agent2_sends_to_1.unsqueeze(1).expand(bs, obs_dim)  # (bs, obs_dim)
        mask[:, 2, 1, :] = content_2 * agent2_to_1
        
        return mask
    
    else:
        raise ValueError(f"Invalid mode: {mode}. Must be 'object', 'content', or 'object_content'.")