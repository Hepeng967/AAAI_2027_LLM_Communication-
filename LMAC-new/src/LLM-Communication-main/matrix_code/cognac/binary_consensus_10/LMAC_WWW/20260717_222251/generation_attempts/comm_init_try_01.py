import torch


def message_design_instruction() -> str:
    """
    Concise summary of the communication policy.
    """
    return (
        "Every agent unconditionally broadcasts its observed node opinions (indices 0-9, "
        "selected by the corresponding portion of its own visibility mask) and its full "
        "outgoing influence row (indices 20-29) to all other agents."
    )


def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, receiver, sender] binary mask indicating which sender-receiver
    pairs are allowed to communicate. All off-diagonal pairs are allowed.
    """
    batch, n_agents, _ = o.shape
    # RULE R2 (and implicitly R1_*): all agents can send to all except self
    who = torch.ones((batch, n_agents, n_agents), dtype=o.dtype, device=o.device)
    # zero out the diagonal
    who.diagonal(dim1=-2, dim2=-1).zero_()
    return who


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a [batch, receiver, sender] binary mask indicating when a message may
    actually be sent. Always true (except for self-loops, which are forced to zero).
    """
    batch, n_agents, _ = o.shape
    # RULE R2 when: unconditional (>=0 is always true) – covers all senders
    # RULE R1_* when: also visibility_mask[10+i]==1, but this is a subset already
    when = torch.ones((batch, n_agents, n_agents), dtype=o.dtype, device=o.device)
    # enforce zero self-communication as required
    when.diagonal(dim1=-2, dim2=-1).zero_()
    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns an obs-aligned content mask with the same shape as o. For each agent:
      - opinion indices 0..9 are selected iff the corresponding visibility mask
        entry (indices 10..19) is 1  (rules R1_0 .. R1_9)
      - influence row indices 20..29 are always selected  (rule R2)
    """
    what = torch.zeros_like(o)

    # RULE R1_0 .. R1_9: broadcast opinions of visible nodes
    # visibility mask for nodes 0..9 is stored in o[..., 10:20]
    what[..., :10] = o[..., 10:20]

    # RULE R2: broadcast the full outgoing influence row (indices 20..29)
    what[..., 20:30] = 1.0

    return what