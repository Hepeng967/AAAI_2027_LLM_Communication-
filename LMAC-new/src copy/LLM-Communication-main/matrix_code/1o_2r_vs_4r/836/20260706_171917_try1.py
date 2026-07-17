import torch

def generate_mask(obs, mode='object'):
    """
    Implements the communication policy for 3 agents (Overseer + 2 Roaches).
    
    obs: torch.Tensor of shape (bs, n_agents, n_agents, obs_dim)
         obs_dim = 49 (but we handle arbitrary obs_dim, e.g., 50 for safety)
    mode: 'object', 'content', or 'object_content'
    
    Returns mask of shape (bs, n_agents, n_agents, 1) for 'object' mode
           or (bs, n_agents, n_agents, obs_dim) for 'content'/'object_content' modes
    """
    bs, n_agents, _, obs_dim = obs.shape
    device = obs.device
    
    # Feature indices (using 0-based indexing)
    # Enemy features: 4 enemies, each with available(1), distance(1), rel_x(1), rel_y(1), health(1), type_0(1), type_1(1) = 7 dims each
    # Enemy i starts at index 4 + i*7
    enemy_available_indices = [4 + i*7 for i in range(4)]
    enemy_rel_x_indices = [4 + i*7 + 2 for i in range(4)]
    enemy_rel_y_indices = [4 + i*7 + 3 for i in range(4)]
    enemy_health_indices = [4 + i*7 + 4 for i in range(4)]
    enemy_type_0_indices = [4 + i*7 + 5 for i in range(4)]
    enemy_type_1_indices = [4 + i*7 + 6 for i in range(4)]
    
    # Ally features: 2 allies, each with visible(1), distance(1), rel_x(1), rel_y(1), health(1), type_0(1), type_1(1) = 7 dims each
    # Ally i starts at index 32 + i*7 (enemies occupy 4*7=28 dims starting at 4, so enemy ends at 4+28=32)
    ally_visible_indices = [32 + i*7 for i in range(2)]
    ally_health_indices = [32 + i*7 + 4 for i in range(2)]
    
    # Own health is at index 46 (since 32 + 2*7 = 46)
    own_health_idx = 46
    
    # Create mask tensor with zeros
    mask = torch.zeros(bs, n_agents, n_agents, obs_dim, device=device)
    
    # ---- Helper to check dims ----
    def assert_shape(t, expected_shape, name=""):
        assert t.shape == expected_shape, f"{name} expected {expected_shape}, got {t.shape}"
    
    # ---- Extract agent-specific observations ----
    # Agent 0 uses obs[:, 0, 0, :] (self observation), Agent 1 uses obs[:, 1, 1, :], etc.
    # But the policy defines communication FROM agent i TO agent j based on agent i's observation.
    # We'll process each sender agent's observation individually.
    
    for sender_id in range(n_agents):
        # Sender's own observation: (bs, obs_dim)
        sender_obs = obs[:, sender_id, sender_id, :]  # (bs, obs_dim)
        
        # Check if sender is Overseer (agent 0) or Roach (agent 1 or 2)
        if sender_id == 0:
            # ---- Agent 0 (Overseer) Policy ----
            
            # Condition 1: Any enemy available
            enemy_avail = torch.stack([sender_obs[:, idx] for idx in enemy_available_indices], dim=1)  # (bs, 4)
            any_enemy_avail = (enemy_avail > 0.5).any(dim=1, keepdim=True)  # (bs, 1)
            
            # Target agents for condition 1: agents 1 and 2
            targets_c1 = torch.tensor([1, 2], device=device)  # sorted indices
            
            # Content for condition 1: for each available enemy, send rel_x, rel_y, health, type_0, type_1
            # We'll build a mask for obs dimensions: for each enemy i, if available, send indices:
            # rel_x, rel_y, health, type_0, type_1
            c1_content_indices = []
            for i in range(4):
                # If enemy i available, add its relevant indices
                c1_content_indices.extend([
                    enemy_rel_x_indices[i],
                    enemy_rel_y_indices[i],
                    enemy_health_indices[i],
                    enemy_type_0_indices[i],
                    enemy_type_1_indices[i],
                ])
            c1_content_indices = list(set(c1_content_indices))  # unique indices
            c1_content_mask = torch.zeros(obs_dim, device=device)
            c1_content_mask[c1_content_indices] = 1.0
            
            # Expand to batch and targets
            for t_idx in targets_c1:
                # t_idx is an integer (0 or 1 or 2)
                # mask[:, sender_id, t_idx, :] should be set to (any_enemy_avail * c1_content_mask) per batch
                # any_enemy_avail: (bs, 1)
                # c1_content_mask: (obs_dim,)
                # Result: (bs, obs_dim)
                cond_batch = any_enemy_avail.expand(-1, obs_dim)  # (bs, obs_dim)
                content_val = c1_content_mask.unsqueeze(0).expand(bs, -1)  # (bs, obs_dim)
                mask[:, sender_id, t_idx, :] = cond_batch * content_val
            
            # Condition 2: own_health < 50% of max health (assume max health is 1.0 if normalized, but we use threshold)
            # Since we don't have max health, let's assume health is in [0,1] and threshold is 0.5
            own_health = sender_obs[:, own_health_idx:own_health_idx+1]  # (bs, 1)
            low_health = (own_health < 0.5)  # (bs, 1)
            
            # Content: own_health and a flag (we can add a dummy dimension for flag? But we have limited obs_dim.
            # We'll send own_health dimension and also "send" a flag by sending own_health and type_0/type_1 dimensions
            # to represent the "call for protection" flag. For simplicity, we send own_health and own_type_0 (as flag).
            c2_content_indices = [own_health_idx, 47, 48]  # own_health, own_type_0, own_type_1 (use type as flag)
            c2_content_mask = torch.zeros(obs_dim, device=device)
            c2_content_mask[c2_content_indices] = 1.0
            
            for t_idx in targets_c1:
                cond_batch = low_health.expand(-1, obs_dim)  # (bs, obs_dim)
                content_val = c2_content_mask.unsqueeze(0).expand(bs, -1)  # (bs, obs_dim)
                # We want to OR with condition 1, so we take max (since mask is 0/1)
                mask[:, sender_id, t_idx, :] = torch.max(mask[:, sender_id, t_idx, :], cond_batch * content_val)
            
            # Condition 3: No enemies available AND position changed (simplified: just no enemies)
            # We'll compute "no enemies" and send to same targets
            no_enemies = (enemy_avail.max(dim=1, keepdim=True)[0] < 0.5)  # (bs, 1)
            
            # Content: "no enemies" flag - we can send own_type_0 and own_type_1 with specific pattern
            c3_content_indices = [47, 48]  # use type dims to represent flag
            c3_content_mask = torch.zeros(obs_dim, device=device)
            c3_content_mask[c3_content_indices] = 1.0
            
            for t_idx in targets_c1:
                cond_batch = no_enemies.expand(-1, obs_dim)  # (bs, obs_dim)
                content_val = c3_content_mask.unsqueeze(0).expand(bs, -1)  # (bs, obs_dim)
                mask[:, sender_id, t_idx, :] = torch.max(mask[:, sender_id, t_idx, :], cond_batch * content_val)
        
        else:
            # ---- Agent 1 or 2 (Roach) Policy ----
            # sender_id is 1 or 2
            
            # Enemy available for this roach
            enemy_avail = torch.stack([sender_obs[:, idx] for idx in enemy_available_indices], dim=1)  # (bs, 4)
            any_enemy_avail = (enemy_avail > 0.5).any(dim=1, keepdim=True)  # (bs, 1)
            no_enemy = (enemy_avail.max(dim=1, keepdim=True)[0] < 0.5)  # (bs, 1)
            
            # Ally visible: check if both allies visible? For Roach, allies are agent 0 (Overseer) and other Roach
            # But Roach's observation has ally_0 and ally_1. Who is ally_0 and ally_1? 
            # Let's assume ally_0 = agent 0 (Overseer) and ally_1 = the other Roach.
            # For sender_id=1, ally_0 is Overseer (0), ally_1 is agent 2.
            # For sender_id=2, ally_0 is Overseer (0), ally_1 is agent 1.
            # We need to map ally indices to agent IDs.
            # Since agents are 0,1,2, we can set:
            if sender_id == 1:
                ally_map = {0: 0, 1: 2}  # ally_0 -> agent 0, ally_1 -> agent 2
            else:  # sender_id == 2
                ally_map = {0: 0, 1: 1}  # ally_0 -> agent 0, ally_1 -> agent 1
            
            # Own health
            own_health = sender_obs[:, own_health_idx:own_health_idx+1]  # (bs, 1)
            low_health = (own_health < 0.3)  # (bs, 1)  # threshold 30%
            
            # Condition 1: Enemy directly observed -> send to agent 0 and other roach
            targets_c1 = [0, 3 - sender_id]  # agent 0 and the other roach (since 1+2=3)
            
            # Content: same as Overseer condition 1
            c1_content_indices = []
            for i in range(4):
                c1_content_indices.extend([
                    enemy_rel_x_indices[i],
                    enemy_rel_y_indices[i],
                    enemy_health_indices[i],
                    enemy_type_0_indices[i],
                    enemy_type_1_indices[i],
                ])
            c1_content_indices = list(set(c1_content_indices))
            c1_content_mask = torch.zeros(obs_dim, device=device)
            c1_content_mask[c1_content_indices] = 1.0
            
            for t_idx in targets_c1:
                cond_batch = any_enemy_avail.expand(-1, obs_dim)  # (bs, obs_dim)
                content_val = c1_content_mask.unsqueeze(0).expand(bs, -1)  # (bs, obs_dim)
                mask[:, sender_id, t_idx, :] = cond_batch * content_val
            
            # Condition 2: No enemy visible -> send "request enemy location" to agent 0
            c2_content_indices = [47, 48]  # use type dims as flag
            c2_content_mask = torch.zeros(obs_dim, device=device)
            c2_content_mask[c2_content_indices] = 1.0
            
            cond_c2 = no_enemy.expand(-1, obs_dim)  # (bs, obs_dim)
            content_c2 = c2_content_mask.unsqueeze(0).expand(bs, -1)  # (bs, obs_dim)
            mask[:, sender_id, 0, :] = torch.max(mask[:, sender_id, 0, :], cond_c2 * content_c2)
            
            # Condition 3: Low health -> send to agent 0 and other roach
            c3_content_indices = [own_health_idx, 47, 48]  # own_health and flags
            c3_content_mask = torch.zeros(obs_dim, device=device)
            c3_content_mask[c3_content_indices] = 1.0
            
            for t_idx in targets_c1:
                cond_batch = low_health.expand(-1, obs_dim)  # (bs, obs_dim)
                content_val = c3_content_mask.unsqueeze(0).expand(bs, -1)  # (bs, obs_dim)
                mask[:, sender_id, t_idx, :] = torch.max(mask[:, sender_id, t_idx, :], cond_batch * content_val)
            
            # Condition 4: Ally visible and ally health low -> send help to that ally
            # Check ally_0 and ally_1
            for ally_idx in range(2):
                ally_visible = sender_obs[:, ally_visible_indices[ally_idx]:ally_visible_indices[ally_idx]+1]  # (bs, 1)
                ally_health = sender_obs[:, ally_health_indices[ally_idx]:ally_health_indices[ally_idx]+1]  # (bs, 1)
                ally_low_health = (ally_health < 0.3) & (ally_visible > 0.5)  # (bs, 1)
                
                target_agent = ally_map[ally_idx]  # agent ID
                
                # Content: help/retreat flag (send own_type_0 and own_type_1 as flag)
                c4_content_indices = [47, 48]  # flag dimensions
                c4_content_mask = torch.zeros(obs_dim, device=device)
                c4_content_mask[c4_content_indices] = 1.0
                
                cond_batch = ally_low_health.expand(-1, obs_dim)  # (bs, obs_dim)
                content_val = c4_content_mask.unsqueeze(0).expand(bs, -1)  # (bs, obs_dim)
                mask[:, sender_id, target_agent, :] = torch.max(mask[:, sender_id, target_agent, :], cond_batch * content_val)
    
    # ---- Now produce output based on mode ----
    if mode == 'object':
        # For object mode, we need to decide if any communication occurs per pair.
        # If any content is sent from i to j, then object mask should be 1.
        object_mask = (mask.sum(dim=3, keepdim=True) > 0).float()  # (bs, n_agents, n_agents, 1)
        return object_mask
    
    elif mode == 'content':
        # For content mode, all pairs communicate, but content is selected.
        # We'll return the mask as is, but we need to ensure all entries are 0/1.
        # The current mask already has 0/1 values based on policy.
        # But content mode says "All agent pairs may communicate", so we need to allow
        # that every pair sends some content. However, the policy only defines specific pairs.
        # To adhere to the policy, we'll return the mask as computed.
        # But to satisfy "all pairs may communicate", we could set unspecific pairs to 0.
        return mask
    
    elif mode == 'object_content':
        # Joint mask: if no communication from i to j, all content dims are zero.
        # Our current mask already enforces this because unspecific pairs are zero.
        return mask
    
    else:
        raise ValueError(f"Unknown mode: {mode}")