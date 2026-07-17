import torch
import numpy as np

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
    # 修复1: 处理numpy数组输入
    if isinstance(obs, np.ndarray):
        obs = torch.from_numpy(obs).float()
    
    # 修复2: 安全获取device
    device = obs.device if hasattr(obs, 'device') else torch.device('cpu')
    
    bs, n_agents, _, obs_dim = obs.shape
    
    # 修复3: 正确的对角线提取方式
    # 原代码: self_obs = torch.diagonal(obs, dim1=1, dim2=2).transpose(1, 2)
    # 应该改为更简单的方式
    self_obs = obs.diagonal(dim1=1, dim2=2).transpose(1, 2)  # (bs, n_agents, obs_dim)
    
    # Current state and active status for each agent
    current_state = self_obs[:, :, 0]  # (bs, n_agents)
    active_status = self_obs[:, :, 1]  # (bs, n_agents)
    
    # Initialize masks based on mode
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), device=device, dtype=torch.float32)
    else:  # 'content' or 'object_content'
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device, dtype=torch.float32)
    
    # 修复4: 使用正确的布尔条件
    at_border = (current_state == 1)  # 布尔张量，不是浮点数
    active = (active_status == 1.0)    # 布尔张量
    
    # 只有活跃的智能体在边界才能触发
    trigger1 = at_border & active
    
    # 对于2个智能体的特殊情况
    if n_agents == 2:
        # 修复5: 确保形状正确
        if mode == 'object':
            # Agent 0 to Agent 1
            mask[:, 0:1, 1:2, 0:1] = trigger1[:, 0:1].view(bs, 1, 1, 1).float()
            # Agent 1 to Agent 0
            mask[:, 1:2, 0:1, 0:1] = trigger1[:, 1:2].view(bs, 1, 1, 1).float()
        else:
            # Agent 0 to Agent 1
            mask[:, 0:1, 1:2, :] = trigger1[:, 0:1].view(bs, 1, 1, 1).float().expand(-1, -1, -1, obs_dim)
            # Agent 1 to Agent 0
            mask[:, 1:2, 0:1, :] = trigger1[:, 1:2].view(bs, 1, 1, 1).float().expand(-1, -1, -1, obs_dim)
    else:
        # 通用情况 (n_agents > 2)
        not_self = 1 - torch.eye(n_agents, device=device).unsqueeze(0)  # (1, n_agents, n_agents)
        
        if mode == 'object':
            # 修复6: 正确扩展trigger1的形状
            trigger1_expanded = trigger1.unsqueeze(2).unsqueeze(3).float()  # (bs, n_agents, 1, 1)
            not_self_expanded = not_self.unsqueeze(3)  # (1, n_agents, n_agents, 1)
            # 修复7: 使用赋值而不是累加，避免重复计数
            mask = trigger1_expanded * not_self_expanded
        else:
            trigger1_expanded = trigger1.unsqueeze(2).unsqueeze(3).float()  # (bs, n_agents, 1, 1)
            not_self_expanded = not_self.unsqueeze(3).expand(-1, -1, -1, obs_dim)  # (1, n_agents, n_agents, obs_dim)
            mask = trigger1_expanded * not_self_expanded
    
    # 修复8: 简化策略，只保留核心的触发条件
    # 对于hallway，通信应该是最简化的
    
    # 确保二值化 (0 或 1)
    mask = (mask > 0).float()
    
    # 根据模式处理
    if mode == 'object':
        # Object模式: 已经是正确形状 (bs, n_agents, n_agents, 1)
        return mask
    
    elif mode == 'content':
        # Content模式: 所有智能体都可以通信，但选择内容
        # 创建全连接mask
        full_connectivity = 1 - torch.eye(n_agents, device=device).unsqueeze(0).unsqueeze(-1)  # (1, n_agents, n_agents, 1)
        full_connectivity = full_connectivity.expand(bs, -1, -1, obs_dim)
        
        # 应用内容选择
        content_mask = full_connectivity * mask
        return content_mask
    
    else:  # 'object_content'
        # Object_content模式: 联合选择对象和内容
        return mask