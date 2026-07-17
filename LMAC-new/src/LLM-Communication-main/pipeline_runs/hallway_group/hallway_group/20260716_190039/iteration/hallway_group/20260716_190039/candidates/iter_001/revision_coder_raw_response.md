```python
import torch


def message_design_instruction() -> str:
    """
    Return a concise description of the communication policy.
    """
    return (
        "G1 (agents 0-2) and G2 (agents 3-6) continuously share current_position (obs index 0) "
        "within their own group. Across groups, communication is sparse: only activated when the "
        "sender is near the goal (position ≤ 2.0) or has already finished (active_status == 0). "
        "Content: always position, active_status only when finished (R3,R4). All edges are directional "
        "and self-loops are excluded."
    )


def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, receiver, sender] binary mask.
    Fully connected minus self-loops – the who-mask is all-to-all.
    The actual edging is further gated by communication_when.
    """
    batch, n, _ = o.shape
    who = torch.ones((n, n), device=o.device) - torch.eye(n, device=o.device)
    return who.unsqueeze(0).expand(batch, -1, -1)


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, receiver, sender] binary mask.
    - Intra-group edges (within {0,1,2} or within {3,4,5,6}) are always on (R1,R2).
    - Inter-group edges are on only when the sender is near completion (pos ≤ 2.0) or has
      already finished (active_status == 0.0). This satisfies R3,R4 efficiently.
    Self-loops are removed.
    """
    batch, n, _ = o.shape
    device = o.device

    # Agent indices: 0..6
    idx = torch.arange(n, device=device)
    group0_mask = idx < 3                  # agents 0,1,2
    # group1_mask = ~group0_mask            # agents 3,4,5,6

    # Same-group boolean matrix [n, n]
    same_group = (group0_mask.unsqueeze(0) == group0_mask.unsqueeze(1))   # [n, n], True if both in G0 or both in G1
    intra_mask = same_group
    inter_mask = ~intra_mask

    # Sender conditions for inter-group activation
    pos = o[..., 0]                         # [batch, n]
    active = o[..., 1]                      # [batch, n]
    near_goal = pos <= 2.0
    finished = active == 0.0
    inter_cond = (near_goal | finished)     # [batch, n]

    # Expand to [batch, n, n] where condition depends on sender j
    inter_cond_edge = inter_cond.unsqueeze(1).expand(batch, n, n)  # [batch, n, n]

    # Final when mask: intra always True, inter only if condition holds
    when_bool = intra_mask.unsqueeze(0) | (inter_mask.unsqueeze(0) & inter_cond_edge)
    # Remove self-loops
    self_mask = ~torch.eye(n, dtype=torch.bool, device=device)
    when = (when_bool & self_mask).float()   # [batch, n, n]

    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, agent, obs_dim] content mask.
    Selected features:
      - index 0 (current_position): always included  (R1,R2,R5,R6)
      - index 1 (active_status):   included only when the sender's active_status == 0 (R3,R4)
    All other features remain 0.
    """
    batch, n_agents, obs_dim = o.shape
    mask = torch.zeros_like(o)
    # Always send position
    mask[..., 0] = 1.0
    # Send active_status only when finished (value exactly 0)
    active = o[..., 1]                     # [batch, n_agents]
    finished = (active == 0.0).float()     # [batch, n_agents]
    mask[..., 1] = finished
    return mask
```