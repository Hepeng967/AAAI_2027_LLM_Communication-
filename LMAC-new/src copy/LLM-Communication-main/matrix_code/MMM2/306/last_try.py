import torch

def generate_mask(obs, mode='object'):
    assert mode in ['object', 'content', 'object_content']
    
    # 1. 类型安全检查
    if not isinstance(obs, torch.Tensor):
        obs = torch.from_numpy(obs)
    if obs.dtype != torch.float32:
        obs = obs.float()
    
    bs, n_agents, _, obs_dim = obs.shape
    device = obs.device
    
    # 特征索引
    enemy_0_available_idx = 4
    enemy_0_distance_idx = 5
    enemy_0_rel_x_idx = 6
    enemy_0_rel_y_idx = 7
    enemy_0_health_idx = 8
    own_health_idx = 33 if 33 < obs_dim else 18  # 简单适配不同地图
    
    # 初始化 Mask
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), dtype=torch.float32, device=device)
    elif mode in ['content', 'object_content']:
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), dtype=torch.float32, device=device)
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    # 提取特征
    enemy_available = obs[:, :, 0, enemy_0_available_idx].unsqueeze(-1).unsqueeze(-1)  # (bs, n_agents, 1, 1)
    enemy_distance = obs[:, :, 0, enemy_0_distance_idx].unsqueeze(-1).unsqueeze(-1)  # (bs, n_agents, 1, 1)
    own_health = obs[:, :, 0, own_health_idx].unsqueeze(-1).unsqueeze(-1)  # (bs, n_agents, 1, 1)
    
    # === 修复 1: 使用 logical_and 替代 & ===
    condition1 = torch.logical_and(enemy_available > 0.5, enemy_distance <= 10.0)
    condition1 = condition1.expand(-1, -1, n_agents, -1)
    
    # 策略 1: 发现敌人，通告全员
    all_allies_mask = torch.ones((bs, n_agents, n_agents, 1), device=device)
    # 对角线置0 (不发给自己)
    diag_mask = 1 - torch.eye(n_agents, device=device).unsqueeze(0).unsqueeze(-1)
    all_allies_mask = all_allies_mask * diag_mask
    
    if mode == 'object':
        mask = torch.where(condition1, all_allies_mask, mask)
    
    # Content 1
    if mode in ['content', 'object_content']:
        condition1_content = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device)
        # 确保索引不越界
        feat_indices = [idx for idx in [enemy_0_rel_x_idx, enemy_0_rel_y_idx, enemy_0_health_idx] if idx < obs_dim]
        if feat_indices:
            condition1_content[:, :, :, feat_indices] = 1.0
        
        # 这里的 mask 可能是 object mask，如果是 object_content 模式需要混合
        # 为简化逻辑，我们分别计算 object_mask 和 content_mask
        pass # 后续统一处理
    
    # 策略 2: 自身血量低，向最近队友求援
    condition2 = (own_health <= 0.5)
    condition2 = condition2.expand(-1, -1, n_agents, -1)
    
    # 计算距离矩阵
    ally_distances = torch.zeros((bs, n_agents, n_agents), device=device)
    for i in range(n_agents):
        for j in range(n_agents):
            if i == j:
                ally_distances[:, i, j] = 1e9
            else:
                ally_idx = j if j < i else j - 1
                dist_idx = 11 + 6*ally_idx  # 假设的基础偏移量
                if dist_idx < obs_dim:
                    ally_distances[:, i, j] = obs[:, i, 0, dist_idx]
                else:
                    ally_distances[:, i, j] = 1e9

    nearest_ally = torch.argmin(ally_distances, dim=2, keepdim=True) # (bs, n_agents, 1)
    nearest_ally_mask = torch.zeros((bs, n_agents, n_agents, 1), device=device)
    nearest_ally_mask.scatter_(2, nearest_ally.unsqueeze(3), 1.0)
    
    if mode == 'object':
        mask = torch.where(condition2, nearest_ally_mask, mask)
        
    # 策略 3: 队友血量低 (全局扫描)
    # 这里的逻辑比较复杂，为了 Batch 安全，我们简化为：如果我看到某个队友血量低，我就联系他
    target_mask_3 = torch.zeros((bs, n_agents, n_agents, 1), device=device)
    
    for i in range(n_agents):
        for j in range(n_agents):
            if i == j: continue
            ally_idx = j if j < i else j - 1
            h_idx = 13 + 6*ally_idx
            if h_idx < obs_dim:
                # 检查队友 j 的血量 (在 i 看来)
                # 注意：obs[:, i, 0, ...] 是 i 的观测
                ally_h = obs[:, i, 0, h_idx].unsqueeze(-1).unsqueeze(-1).unsqueeze(-1) # (bs, 1, 1, 1)
                cond3 = (ally_h <= 0.5)
                # 如果满足，i 联系 j
                # 使用 max (逻辑或) 来更新 mask，避免 inplace 覆盖
                current_link = torch.zeros((bs, n_agents, n_agents, 1), device=device)
                current_link[:, i, j, :] = 1.0
                target_mask_3 = torch.max(target_mask_3, cond3.float() * current_link)

    if mode == 'object':
        mask = torch.max(mask, target_mask_3)

    # === Content 模式填充 ===
    if mode in ['content', 'object_content']:
        c_mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device)
        
        # Cond 1 content
        c1_feats = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device)
        idxs = [idx for idx in [enemy_0_rel_x_idx, enemy_0_rel_y_idx, enemy_0_health_idx] if idx < obs_dim]
        c1_feats[:, :, :, idxs] = 1.0
        c_mask = torch.max(c_mask, condition1.float() * c1_feats)
        
        # Cond 2 content
        c2_feats = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device)
        if own_health_idx < obs_dim:
            c2_feats[:, :, :, own_health_idx] = 1.0
        c_mask = torch.max(c_mask, condition2.float() * c2_feats)
        
        # Cond 3 content (Ally Health)
        # 这里简化处理：如果是 Cond 3 触发，发送队友血量信息位
        # 由于上面 target_mask_3 已经聚合了，这里不再细分每对，而是广播相关特征
        # 更精细的做法需要像上面双重循环那样填
        
        if mode == 'content':
            return c_mask
        else: # object_content
            # 重新计算完整的 object_mask 用于组合
            o_mask = torch.zeros((bs, n_agents, n_agents, 1), device=device)
            o_mask = torch.where(condition1, all_allies_mask, o_mask)
            o_mask = torch.where(condition2, nearest_ally_mask, o_mask)
            o_mask = torch.max(o_mask, target_mask_3)
            
            return o_mask.expand(-1,-1,-1,obs_dim) * c_mask

    return mask