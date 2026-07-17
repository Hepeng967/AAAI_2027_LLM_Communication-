import torch

def communication_who(o):
    """
    Determines which senders are allowed to communicate to which receivers.
    Shape: [batch, receiver, sender] with entries in {0, 1}.
    """
    batch_size, n_agents, _ = o.shape
    who = torch.zeros(batch_size, n_agents, n_agents, device=o.device, dtype=o.dtype)

    # RULE R1: Overseer (agent 0) is the only sender; it sends to both roaches (agents 1 and 2)
    if n_agents >= 3:
        who[:, 1, 0] = 1.0  # agent 0 -> agent 1
        who[:, 2, 0] = 1.0  # agent 0 -> agent 2
    # diagonal stays 0 (no self‑communication)

    return who


def communication_when(o):
    """
    Decides when a sender actually transmits. 1.0 if the rule condition is met.
    Shape: [batch, receiver, sender].
    """
    batch_size, n_agents, _ = o.shape
    when = torch.zeros(batch_size, n_agents, n_agents, device=o.device, dtype=o.dtype)

    # RULE R1: condition = enemy_0_available > 0.5 for sender agent 0
    condition = (o[:, 0, 4] > 0.5).to(o.dtype)  # shape [batch]

    if n_agents >= 3:
        when[:, 1, 0] = condition
        when[:, 2, 0] = condition
    # all other entries remain 0

    return when


def communication_what(o):
    """
    Produces an observation‑aligned content mask: 1.0 on features that belong
    in the message, 0.0 elsewhere.
    Shape: [batch, n_agents, obs_dim] – same as o.
    """
    # RULE R1: agent 0 transmits selected enemy features
    # indices taken verbatim from the specification
    R1_feature_indices = [4, 5, 6, 7, 8, 11, 12, 13, 14, 15,
                          18, 19, 20, 21, 22, 25, 26, 27, 28, 29]

    what_mask = torch.zeros_like(o)                     # [batch, agents, obs_dim]
    what_mask[:, 0, R1_feature_indices] = 1.0           # set only for agent 0
    # agents 1 and 2 have no sending rules → their masks remain all zeros.

    return what_mask