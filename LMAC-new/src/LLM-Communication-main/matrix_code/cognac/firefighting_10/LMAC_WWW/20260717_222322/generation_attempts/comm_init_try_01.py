import torch

def message_design_instruction():
    return (
        "Adjacent firefighters (each pair from agents 0-1 to 8-9) share their noisy flame observation "
        "and previous action one-hot vectors (indices 0,1,2) only when they detect a flame (>0.5). "
        "This reduces communication overhead and focuses coordination on active fires."
    )


def communication_who(o):
    """who matrix: for each adjacent pair (i,i+1) both directions are active."""
    batch_size, n_agents, _ = o.shape
    # RULE R1 - R9: each adjacent pair forms a bidirectional communication group
    # off-diagonal ones on the first off-diagonals give exactly these pairs
    who = torch.diag_embed(torch.ones(n_agents - 1, device=o.device), offset=1) \
          + torch.diag_embed(torch.ones(n_agents - 1, device=o.device), offset=-1)
    return who.unsqueeze(0).expand(batch_size, -1, -1)


def communication_when(o):
    """when matrix: sender condition = flame observation > 0.5, zero on the diagonal."""
    batch_size, n_agents, _ = o.shape
    flame_obs = o[:, :, 0]                     # (batch, n_agents)
    cond = (flame_obs > 0.5).float()
    when = cond.unsqueeze(1).expand(-1, n_agents, -1)  # (batch, n_agents, n_agents)
    # enforce zero self-communication
    diag = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    when = when * (1.0 - diag)
    return when


def communication_what(o):
    """what mask: if flame detected, select indices 0,1,2; otherwise all zeros."""
    batch_size, n_agents, obs_dim = o.shape
    flame_obs = o[:, :, 0]                     # (batch, n_agents)
    cond = (flame_obs > 0.5).float()           # (batch, n_agents)

    # fixed selection pattern for the three features
    pattern = torch.zeros(n_agents, obs_dim, device=o.device)
    pattern[:, 0] = 1.0
    pattern[:, 1] = 1.0
    pattern[:, 2] = 1.0

    # conditionally mask: 1 where condition true and feature selected, else 0
    what_mask = cond.unsqueeze(-1) * pattern.unsqueeze(0)   # (batch, n_agents, obs_dim)
    return what_mask