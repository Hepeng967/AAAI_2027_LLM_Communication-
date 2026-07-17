import torch

def communication_who(o):
    """
    Returns a [batch, n_agents, n_agents] binary mask indicating allowed
    sender-receiver pairs. Only the single rule R1 is implemented.
    """
    batch, n_agents, _ = o.shape
    who = torch.zeros(batch, n_agents, n_agents, dtype=torch.float32, device=o.device)

    # RULE R1: sender group G1 (agent 0) to receivers group G2 (agents 1, 2)
    if n_agents > 2:
        who[:, 1, 0] = 1.0
        who[:, 2, 0] = 1.0
    elif n_agents > 1:
        who[:, 1, 0] = 1.0
    # If n_agents == 1, no communication possible (diagonal remains zero)
    return who


def communication_when(o):
    """
    Returns a [batch, n_agents, n_agents] binary mask indicating whether a
    designated sender may communicate at this step. Only rule R1.
    """
    batch, n_agents, obs_dim = o.shape
    when = torch.zeros(batch, n_agents, n_agents, dtype=torch.float32, device=o.device)

    # RULE R1: trigger when enemy_0_available (index 4) > 0
    if obs_dim > 4:
        condition = (o[:, 0, 4] > 0).float()  # shape [batch]
        if n_agents > 2:
            when[:, 1, 0] = condition
            when[:, 2, 0] = condition
        elif n_agents > 1:
            when[:, 1, 0] = condition
    return when


def communication_what(o):
    """
    Returns an obs-aligned mask of shape [batch, n_agents, obs_dim] with 1.0 at
    feature indices the sender is allowed to transmit. Only rule R1.
    """
    batch, n_agents, obs_dim = o.shape
    what = torch.zeros(batch, n_agents, obs_dim, dtype=torch.float32, device=o.device)

    # RULE R1: overseer (agent 0) sends enemy observation block (indices 4..31)
    feature_indices = list(range(4, min(32, obs_dim)))
    if feature_indices and n_agents > 0:
        what[:, 0, feature_indices] = 1.0
    return what