import torch

def message_design_instruction() -> str:
    """
    Return a concise description of the communication policy.
    """
    return (
        "G1 (agents 0-2) and G2 (agents 3-6) continuously share their current_position (obs index 0) "
        "both within and across groups. Additionally, each agent broadcasts its active_status (obs index 1) "
        "only when it becomes 0 (finished), so that the other group can learn about completion. "
        "All links are active; the content mask includes position always and active_status conditionally."
    )


def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, receiver, sender] binary mask.
    All agents communicate with every other agent (no self-loops).
    Implements the sender/receiver pairs of rules R1, R2, R3, R4, R5, R6.
    """
    batch, n, _ = o.shape
    # Fully-connected minus self
    who = torch.ones((n, n), device=o.device) - torch.eye(n, device=o.device)
    return who.unsqueeze(0).expand(batch, -1, -1)


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, receiver, sender] binary mask.
    Condition for every link is sender's current_position >= 0.0, which is always true.
    This satisfies the "when" conditions of all rules:
      R1,R2,R5,R6: current_position >= 0.0 (always true)
      R3,R4: active_status == 0.0 is handled in the what-mask, not needed as edge gate.
    """
    batch, n, _ = o.shape
    # Sender's current_position (index 0)
    pos = o[..., 0]                     # [batch, n]
    # Always true (>= 0)
    cond = (pos >= 0.0).float()         # [batch, n]
    # Expand to [batch, n, n] where entry (i,j) depends on sender j
    when = cond.unsqueeze(2).expand(-1, -1, n)   # [batch, n, n]
    # Set diagonal to zero (no self-communication)
    mask = ~torch.eye(n, dtype=torch.bool, device=o.device).unsqueeze(0)
    when = when * mask
    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, agent, obs_dim] content mask.
    Features selected:
      - index 0 (current_position): always included  (R1, R2, R5, R6)
      - index 1 (active_status):   included only when the sender's active_status == 0 (R3, R4)
    All other features remain 0.
    """
    batch, n_agents, obs_dim = o.shape
    mask = torch.zeros_like(o)
    # R1,R2,R5,R6: always send position
    mask[..., 0] = 1.0
    # R3,R4: send active_status only when finished (value exactly 0)
    active = o[..., 1]                 # [batch, n_agents]
    finished = (active == 0.0).float() # [batch, n_agents]
    mask[..., 1] = finished
    return mask