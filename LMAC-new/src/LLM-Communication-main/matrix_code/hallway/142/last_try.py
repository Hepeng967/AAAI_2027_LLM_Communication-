import torch
import numpy as np

def generate_mask(obs, mode='object'):
    """
    Generate communication mask for complex hallway coordination.
    
    Args:
        obs: torch.Tensor OR numpy.ndarray of shape (bs, n_agents, n_agents, 2)
            obs[:, i, j, 0] = current_state of agent i from perspective of agent j
            obs[:, i, j, 1] = active_status of agent i from perspective of agent j
        mode: str, one of ['object', 'content', 'object_content']
    
    Returns:
        mask: torch.Tensor of appropriate shape based on mode
    """
    # 处理numpy数组输入
    if isinstance(obs, np.ndarray):
        obs = torch.from_numpy(obs).float()
    
    # 安全获取device
    if hasattr(obs, 'device'):
        device = obs.device
    else:
        device = torch.device('cpu')
        if not isinstance(obs, torch.Tensor):
            obs = torch.tensor(obs, device=device, dtype=torch.float32)
    
    bs, n_agents, _, obs_dim = obs.shape
    
    # 初始化mask，确保形状完全正确
    if mode == 'object':
        mask = torch.zeros((bs, n_agents, n_agents, 1), device=device, dtype=torch.float32)
    else:  # 'content' or 'object_content'
        mask = torch.zeros((bs, n_agents, n_agents, obs_dim), device=device, dtype=torch.float32)
    
    # 只有4个智能体时才执行策略
    if n_agents < 4:
        return mask
    
    # 提取当前状态（从每个智能体自身的视角）
    # obs的形状是(bs, n_agents, n_agents, 2)，对角线元素是智能体自身的状态
    current_states = torch.zeros((bs, n_agents), device=device, dtype=torch.float32)
    for i in range(n_agents):
        current_states[:, i] = obs[:, i, i, 0]
    
    # 创建广播形状
    # 对于每个触发条件，我们创建形状为(bs, 1, 1, 1)的张量，然后正确扩展
    
    # ========== AGENT 0, 1, 2 的策略 ==========
    for agent_idx in [0, 1, 2]:
        # Trigger 1: 当智能体到达状态1
        # 创建形状为(bs,)的布尔张量，然后转换为(bs, 1, 1, 1)
        trigger1_bool = current_states[:, agent_idx] == 1
        trigger1 = trigger1_bool.float().view(bs, 1, 1, 1)  # (bs, 1, 1, 1)
        
        # 根据模式正确赋值
        if mode == 'object':
            # object模式：mask形状为(bs, n_agents, n_agents, 1)
            # 我们需要将trigger1赋值给mask[:, agent_idx, 3, :]
            # 确保形状匹配：trigger1是(bs, 1, 1, 1)，目标形状是(bs, 1, 1, 1)
            mask[:, agent_idx:agent_idx+1, 3:4, :] = mask[:, agent_idx:agent_idx+1, 3:4, :] + trigger1
        else:
            # content或object_content模式：mask形状为(bs, n_agents, n_agents, obs_dim)
            # 发送到第0个特征维度（current_state）
            mask[:, agent_idx:agent_idx+1, 3:4, 0:1] = mask[:, agent_idx:agent_idx+1, 3:4, 0:1] + trigger1
        
        # Trigger 2: 当智能体在状态1且收到来自Agent 3的"准备同步"信号
        # Agent 3在状态2时发送"准备同步"
        agent3_at_state2 = (current_states[:, 3] == 2).float().view(bs, 1, 1, 1)
        agent_at_state1 = (current_states[:, agent_idx] == 1).float().view(bs, 1, 1, 1)
        
        trigger2 = agent_at_state1 * agent3_at_state2  # (bs, 1, 1, 1)
        
        if mode == 'object':
            mask[:, agent_idx:agent_idx+1, 3:4, :] = mask[:, agent_idx:agent_idx+1, 3:4, :] + trigger2
        else:
            # 发送到第1个特征维度（active_status）
            mask[:, agent_idx:agent_idx+1, 3:4, 1:2] = mask[:, agent_idx:agent_idx+1, 3:4, 1:2] + trigger2
        
        # Trigger 3: 当收到来自Agent 3的"最终移动"信号
        agent3_at_state1 = (current_states[:, 3] == 1).float().view(bs, 1, 1, 1)
        trigger3 = agent3_at_state1  # (bs, 1, 1, 1)
        
        if mode == 'object':
            mask[:, agent_idx:agent_idx+1, 3:4, :] = mask[:, agent_idx:agent_idx+1, 3:4, :] + trigger3
        else:
            # 发送所有特征维度
            # 需要扩展trigger3到(bs, 1, 1, obs_dim)
            trigger3_expanded = trigger3.expand(-1, -1, -1, obs_dim)
            mask[:, agent_idx:agent_idx+1, 3:4, :] = mask[:, agent_idx:agent_idx+1, 3:4, :] + trigger3_expanded
    
    # ========== AGENT 3 的策略 ==========
    # Trigger 1: 当Agent 3到达状态2
    agent3_at_state2 = (current_states[:, 3] == 2).float().view(bs, 1, 1, 1)  # (bs, 1, 1, 1)
    
    if mode == 'object':
        # 发送给Agent 0, 1, 2
        mask[:, 3:4, 0:1, :] = mask[:, 3:4, 0:1, :] + agent3_at_state2
        mask[:, 3:4, 1:2, :] = mask[:, 3:4, 1:2, :] + agent3_at_state2
        mask[:, 3:4, 2:3, :] = mask[:, 3:4, 2:3, :] + agent3_at_state2
    else:
        # 发送到第0个特征维度
        mask[:, 3:4, 0:1, 0:1] = mask[:, 3:4, 0:1, 0:1] + agent3_at_state2
        mask[:, 3:4, 1:2, 0:1] = mask[:, 3:4, 1:2, 0:1] + agent3_at_state2
        mask[:, 3:4, 2:3, 0:1] = mask[:, 3:4, 2:3, 0:1] + agent3_at_state2
    
    # Trigger 2: 当Agent 3在状态1且所有Agent 0-2都在状态1
    agent0_at_state1 = (current_states[:, 0] == 1).float().view(bs, 1, 1, 1)
    agent1_at_state1 = (current_states[:, 1] == 1).float().view(bs, 1, 1, 1)
    agent2_at_state1 = (current_states[:, 2] == 1).float().view(bs, 1, 1, 1)
    agent3_at_state1 = (current_states[:, 3] == 1).float().view(bs, 1, 1, 1)
    
    all_ready = agent0_at_state1 * agent1_at_state1 * agent2_at_state1 * agent3_at_state1  # (bs, 1, 1, 1)
    
    if mode == 'object':
        # 发送给Agent 0, 1, 2
        mask[:, 3:4, 0:1, :] = mask[:, 3:4, 0:1, :] + all_ready
        mask[:, 3:4, 1:2, :] = mask[:, 3:4, 1:2, :] + all_ready
        mask[:, 3:4, 2:3, :] = mask[:, 3:4, 2:3, :] + all_ready
    else:
        # 发送到第1个特征维度
        mask[:, 3:4, 0:1, 1:2] = mask[:, 3:4, 0:1, 1:2] + all_ready
        mask[:, 3:4, 1:2, 1:2] = mask[:, 3:4, 1:2, 1:2] + all_ready
        mask[:, 3:4, 2:3, 1:2] = mask[:, 3:4, 2:3, 1:2] + all_ready
    
    # ========== 后处理 ==========
    # 确保mask值为0或1
    mask = (mask > 0).float()
    
    # 对于object_content模式，确保如果对象未选择，所有内容都为0
    if mode == 'object_content':
        # 创建对象mask：检查是否有任何内容维度为1
        object_mask = torch.any(mask > 0.5, dim=-1, keepdim=True).float()  # (bs, n_agents, n_agents, 1)
        # 扩展到内容维度
        object_mask_expanded = object_mask.expand(-1, -1, -1, obs_dim)
        # 应用对象mask到内容mask
        mask = mask * object_mask_expanded
    
    # 确保自我通信始终为0（智能体不向自己发送消息）
    # 创建单位矩阵用于自索引
    eye = torch.eye(n_agents, device=device).view(1, n_agents, n_agents, 1)
    if mode != 'object':
        eye = eye.expand(-1, -1, -1, obs_dim)
    
    # 设置自我通信为0
    mask = mask * (1 - eye)
    
    return mask

