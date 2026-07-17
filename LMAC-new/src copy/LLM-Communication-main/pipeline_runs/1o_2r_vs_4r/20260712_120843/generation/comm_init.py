import torch

def communication_who(o):
    """
    RULES: All rules share the same who: sender group G1 (agent 0, Overseer) transmits to receiver group G2 (agents 1,2, Roaches).
    No self-communication, no other edges.
    """
    batch = o.shape[0]
    n_agents = o.shape[1]               # expected 3
    device = o.device
    who = torch.zeros(batch, n_agents, n_agents, device=device)
    # Overseer -> Roach1 and Roach2
    who[:, 1, 0] = 1.0
    who[:, 2, 0] = 1.0
    return who


def communication_when(o):
    """
    RULES:
    - R1_E0: when enemy_0_available > 0.5
    - R1_E1: when enemy_1_available > 0.5
    - R1_E2: when enemy_2_available > 0.5
    - R1_E3: when enemy_3_available > 0.5

    The Overseer transmits if ANY enemy slot is visible.
    """
    batch = o.shape[0]
    n_agents = o.shape[1]               # expected 3
    device = o.device

    # Extract enemy availability flags from agent 0 (Overseer) observation
    e0_avail = o[:, 0, 4] > 0.5        # R1_E0
    e1_avail = o[:, 0, 12] > 0.5       # R1_E1
    e2_avail = o[:, 0, 20] > 0.5       # R1_E2
    e3_avail = o[:, 0, 28] > 0.5       # R1_E3

    any_avail = e0_avail | e1_avail | e2_avail | e3_avail   # [batch]

    when = torch.zeros(batch, n_agents, n_agents, device=device)
    when[:, 1, 0] = any_avail.float()  # Overseer -> Roach1
    when[:, 2, 0] = any_avail.float()  # Overseer -> Roach2
    # All other edges remain 0 (including self)
    return when


def communication_what(o):
    """
    Builds a content mask of the same shape as o. Only the sender (agent 0) can
    contribute content; for receivers the mask is zero.

    RULES (content for each enemy slot, sent when that slot is available):
    - R1_E0: indices [4,6,7,8,9,10]   (skip distance 5, padding 11)
    - R1_E1: indices [12,14,15,16,17,18] (skip distance 13, padding 19)
    - R1_E2: indices [20,22,23,24,25,26] (skip distance 21, padding 27)
    - R1_E3: indices [28,30,31,32,33,34] (skip distance 29, padding 35)
    """
    batch, n_agents, obs_dim = o.shape
    device = o.device

    mask = torch.zeros(batch, n_agents, obs_dim, device=device)

    # Agent 0 (Overseer) mask: only include features for visible enemies
    mask_agent0 = torch.zeros(batch, obs_dim, device=device)

    # R1_E0: enemy 0
    cond0 = o[:, 0, 4] > 0.5
    mask_agent0[:, [4,6,7,8,9,10]] = cond0.unsqueeze(1).float().expand(-1, 6)

    # R1_E1: enemy 1
    cond1 = o[:, 0, 12] > 0.5
    mask_agent0[:, [12,14,15,16,17,18]] = cond1.unsqueeze(1).float().expand(-1, 6)

    # R1_E2: enemy 2
    cond2 = o[:, 0, 20] > 0.5
    mask_agent0[:, [20,22,23,24,25,26]] = cond2.unsqueeze(1).float().expand(-1, 6)

    # R1_E3: enemy 3
    cond3 = o[:, 0, 28] > 0.5
    mask_agent0[:, [28,30,31,32,33,34]] = cond3.unsqueeze(1).float().expand(-1, 6)

    # Assign to agent 0 slot
    mask[:, 0, :] = mask_agent0
    # Agents 1 and 2 remain zero (they never send)
    return mask