import torch

def message_design_instruction() -> str:
    """
    Concise description of the communication policy:
    All agents (0--3) continuously broadcast their current position (feature index 0)
    to every other agent. This provides each agent with the positions of all others,
    enabling coordinated arrivals at the goal.
    """
    return (
        "Continuous full broadcast: agents 0..3 send their own current_position "
        "(index 0) to all other agents at every timestep."
    )

def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, n_agents, n_agents] binary mask indicating which sender -> receiver
    pairs are allowed to communicate.
    (Implementation of rules R1, R2, R3, R4: every agent sends to all others.)
    """
    batch, n_agents, _ = o.shape
    # Off-diagonal ones: every agent can send to every other agent.
    # RULE R1, R2, R3, R4: sender group G0--G3, receivers = all except sender.
    who = (1 - torch.eye(n_agents, device=o.device, dtype=torch.float32))  # [n_agents, n_agents]
    who = who.unsqueeze(0).expand(batch, -1, -1)  # [batch, n_agents, n_agents]
    return who

def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, n_agents, n_agents] binary mask indicating when a communication
    opportunity is triggered.
    (Always true because positions are always >=0.)
    """
    batch, n_agents, _ = o.shape
    # Always triggered: same off-diagonal matrix as who.
    # RULE R1, R2, R3, R4: condition "current_position >= 0" is always satisfied.
    when = (1 - torch.eye(n_agents, device=o.device, dtype=torch.float32))  # [n_agents, n_agents]
    when = when.unsqueeze(0).expand(batch, -1, -1)  # [batch, n_agents, n_agents]
    return when

def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a content mask of shape [batch, n_agents, obs_dim] indicating which parts
    of the sender's observation are communicated.
    (Messages contain only current_position, index 0.)
    """
    # RULE R1, R2, R3, R4: each agent sends its own current_position (feature index 0).
    what_mask = torch.zeros_like(o)  # [batch, n_agents, obs_dim]
    what_mask[..., 0] = 1.0          # select feature index 0 for all agents
    return what_mask