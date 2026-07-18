```python
import torch

def message_design_instruction():
    """
    Concise natural-language description of the communication policy.
    """
    return (
        "Unhealthy agents (machine_status == 0) broadcast their machine "
        "and job status to all other agents. Receivers use this information "
        "to assess failure propagation risk and make informed reboot decisions."
    )

def communication_who(o):
    """
    Returns a mask of shape [batch, receiver, sender] indicating allowed
    communication edges. 1 for allowed, 0 otherwise.
    All agents broadcast to all other agents (no self-communication).
    """
    n_agents = o.shape[1]
    # Off-diagonal matrix: [n_agents, n_agents]
    off_diag = 1.0 - torch.eye(n_agents, device=o.device, dtype=o.dtype)
    who = off_diag.unsqueeze(0).expand(o.shape[0], -1, -1)  # [batch, receiver, sender]
    return who

def communication_when(o):
    """
    Returns a mask of shape [batch, receiver, sender] indicating when an edge
    is active. An edge from sender j to receiver i is active if sender j's
    own machine status (index 2*j) equals 0 (unhealthy) and i != j.
    This implements rules R1_0 through R1_9.
    """
    batch, n_agents, _obs_dim = o.shape
    agent_ids = torch.arange(n_agents, device=o.device)

    # Gather each agent's own machine status from its observation.
    # Feature index = 2 * agent_id
    machine_indices = 2 * agent_ids  # [n_agents]
    # Build batch and agent indices for advanced indexing.
    batch_idx = torch.arange(batch, device=o.device).view(-1, 1).expand(-1, n_agents).reshape(-1)
    agent_idx = agent_ids.view(1, -1).expand(batch, -1).reshape(-1)
    feat_idx = machine_indices.view(1, -1).expand(batch, -1).reshape(-1)
    machine_self = o[batch_idx, agent_idx, feat_idx].view(batch, n_agents)  # [batch, n_agents]

    # Condition: machine_status == 0 (unhealthy)
    condition = (machine_self == 0.0).to(o.dtype)  # [batch, n_agents] (sender dimension)

    # Off-diagonal mask (no self-communication)
    off_diag = 1.0 - torch.eye(n_agents, device=o.device, dtype=o.dtype)  # [n_agents, n_agents]

    # Broadcast condition over receivers: when[b,i,j] = off_diag[i,j] * condition[b,j]
    when = off_diag.unsqueeze(0) * condition.unsqueeze(1)  # [batch, receiver, sender]
    return when

def communication_what(o):
    """
    Returns a content mask of the same shape as o ([batch, agent, obs_dim]).
    For each agent j, the mask selects its own machine status (index 2*j) and
    job status (index 2*j+1), leaving all other features zero.
    """
    batch, n_agents, obs_dim = o.shape
    mask = torch.zeros(n_agents, obs_dim, device=o.device, dtype=o.dtype)
    agent_ids = torch.arange(n_agents, device=o.device)
    # Machine status at 2*j, job status at 2*j+1
    mask[agent_ids, 2 * agent_ids] = 1.0
    mask[agent_ids, 2 * agent_ids + 1] = 1.0
    what = mask.unsqueeze(0).expand(batch, -1, -1)  # [batch, n_agents, obs_dim]
    return what
```