import torch

def communication_who(o):
    """
    Returns a binary mask of shape [batch, n_agents, n_agents] indicating sender-
    receiver pairs that are allowed to communicate.  The matrix uses the
    convention mask[b, receiver, sender].

    RULE R1: sender = agent_0 (overseer), receivers = agents 1 and 2 (roaches).
    """
    batch, n_agents, _ = o.shape
    mask = torch.zeros(batch, n_agents, n_agents, device=o.device, dtype=torch.float32)
    # sender is agent 0; receivers are all agents with index >= 1
    if n_agents > 1:
        mask[:, 1:n_agents, 0] = 1.0
    return mask


def communication_when(o):
    """
    Returns a binary mask of shape [batch, n_agents, n_agents] indicating the
    timesteps (and sender–receiver pairs) when communication actually occurs.

    RULE R1: agent_0 sends when enemy_0_available > 0.0 (index 4).
    The condition is broadcast to all eligible receivers (agents >=1).
    """
    batch, n_agents, _ = o.shape
    # sender 0 trigger: enemy_0_available (index 4) > 0
    trigger = (o[:, 0, 4] > 0.0).float()           # [batch]

    mask = torch.zeros(batch, n_agents, n_agents, device=o.device, dtype=torch.float32)
    if n_agents > 1:
        # expand trigger to all receivers with index >= 1
        mask[:, 1:n_agents, 0] = trigger.unsqueeze(1).expand(batch, n_agents - 1)
    return mask


def communication_what(o):
    """
    Returns a mask of the same shape as `o` that selects which features from
    the sender's local observation are included in the message.

    RULE R1: agent_0 broadcasts all enemy features (availability, rel_x, rel_y,
    health) for enemy slots 0–3.  Other agents send nothing.
    """
    # Feature indices for enemy 0..3 (availability, rel_x, rel_y, health)
    indices = [4, 6, 7, 8,          # enemy_0
               11, 13, 14, 15,      # enemy_1
               18, 20, 21, 22,      # enemy_2
               25, 27, 28, 29]      # enemy_3

    mask = torch.zeros_like(o, dtype=torch.float32)
    # Only agent_0 (index 0) sends; set selected features to 1
    mask[:, 0, indices] = 1.0
    return mask