```python
import torch

def communication_who(o):
    """
    Determine which sender-receiver pairs are allowed to communicate.
    o shape: [batch, n_agents, obs_dim]
    Returns: [batch, n_agents (receivers), n_agents (senders)] in {0,1}.
    """
    batch, n_agents, obs_dim = o.shape
    # RULE R1: Overseer (agent 0, sender) communicates with roaches (agents 1,2, receivers)
    # conditioned on visibility of those allies from the overseer's perspective.
    who = torch.zeros(batch, n_agents, n_agents, device=o.device, dtype=o.dtype)

    # ally_0_visible at index 32 (receiver 1), ally_1_visible at index 39 (receiver 2)
    who[:, 1, 0] = o[:, 0, 32]   # visibility of ally 0 (agent 1)
    who[:, 2, 0] = o[:, 0, 39]   # visibility of ally 1 (agent 2)

    # Ensure outputs are strictly in [0,1] (clamp to handle any potential out-of-range inputs)
    who = who.clamp(min=0.0, max=1.0)

    # Zero the diagonal (no self-communication)
    diag = torch.arange(n_agents, device=o.device)
    who[:, diag, diag] = 0.0
    return who


def communication_when(o):
    """
    Determine when a sender should transmit.
    o shape: [batch, n_agents, obs_dim]
    Returns: [batch, n_agents, n_agents] in {0,1}.
    """
    batch, n_agents, obs_dim = o.shape

    # RULE R1: sender transmits when its own health > 0
    own_health = o[:, :, 46]                # [batch, n_agents]
    alive = (own_health > 0.0).float()      # 1 if alive

    # Broadcast sender condition across all receivers
    when = alive.unsqueeze(1).expand(-1, n_agents, -1).clone()

    # Zero the diagonal (no self-communication)
    diag_mask = torch.eye(n_agents, device=o.device, dtype=torch.bool).unsqueeze(0)
    when = when.masked_fill(diag_mask, 0.0)
    return when


def communication_what(o):
    """
    Build the content mask: which observation features are transmitted.
    o shape: [batch, n_agents, obs_dim]
    Returns: [batch, n_agents, obs_dim] mask in {0,1}.
    """
    batch, n_agents, obs_dim = o.shape

    # RULE R1: only the Overseer (agent 0) transmits, and it sends enemy position / health info
    what = torch.zeros(batch, n_agents, obs_dim, device=o.device, dtype=o.dtype)

    # feature indices for enemies 0–3 (availability, distance, rel x, rel y, health)
    idx = torch.tensor(
        [4, 5, 6, 7, 8, 11, 12, 13, 14, 15,
         18, 19, 20, 21, 22, 25, 26, 27, 28, 29],
        device=o.device, dtype=torch.long
    )
    what[:, 0, idx] = 1.0   # only sender 0 has these features set to 1
    return what
```