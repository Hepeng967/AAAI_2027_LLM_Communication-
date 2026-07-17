import torch

def message_design_instruction(state=None, env_info=None):
    """
    Returns a string instruction describing the teacher communication policy.
    Required for LMAC validation.
    """
    return (
        "Teacher communication policy for 1o_2r_vs_4r:\n"
        " - Overseer (agent 0) sends enemy information (positions, health, types) to both Roaches.\n"
        " - Each Roach (agents 1,2) sends its previous action to the other Roach.\n"
        " - Communication occurs when Overseer is present (R1) or when a Roach has taken an action (R2).\n"
        " - The content masks select relevant observation features."
    )


def communication_who(o):
    """
    Returns a [batch, receiver, sender] binary matrix indicating allowed communication edges.
    RULE R1: Overseer (agent 0) sends to Roaches (agents 1,2).
    RULE R2: Each Roach sends to the other Roach.
    """
    B, N, _ = o.shape
    who = torch.zeros(B, N, N, dtype=o.dtype, device=o.device)
    # RULE R1: Overseer -> Roaches
    who[:, 1, 0] = 1.0
    who[:, 2, 0] = 1.0
    # RULE R2: Roach i -> Roach j (i != j)
    who[:, 2, 1] = 1.0  # agent 1 -> agent 2
    who[:, 1, 2] = 1.0  # agent 2 -> agent 1
    return who


def communication_when(o):
    """
    Returns a [batch, receiver, sender] binary matrix indicating active communication edges.
    RULE R1: always when Overseer exists (agent_id_0 > -1.0).
    RULE R2: when Roach has taken an action (previous_action_0 > 0.5).
    """
    B, N, D = o.shape
    when = torch.zeros(B, N, N, dtype=o.dtype, device=o.device)

    # RULE R1: agent_id_0 (index 63) > -1.0 for sender 0
    cond_R1 = o[:, 0, 63] > -1.0
    when[:, 1, 0] = cond_R1.to(dtype=o.dtype)
    when[:, 2, 0] = cond_R1.to(dtype=o.dtype)

    # RULE R2: previous_action_0 (index 53) > 0.5 for senders 1 and 2
    cond_s1 = o[:, 1, 53] > 0.5
    cond_s2 = o[:, 2, 53] > 0.5
    when[:, 2, 1] = cond_s1.to(dtype=o.dtype)
    when[:, 1, 2] = cond_s2.to(dtype=o.dtype)

    return when


def communication_what(o):
    """
    Returns an obs-aligned content mask of the same shape as o.
    RULE R1: Overseer's enemy features (indices listed).
    RULE R2: Roaches' previous actions (indices 53..62).
    """
    B, N, D = o.shape
    what = torch.zeros_like(o)

    # Agent identification via one-hot IDs (indices 63, 64, 65)
    is_agent0 = o[:, :, 63] > 0.5  # [B, N]
    is_agent1 = o[:, :, 64] > 0.5
    is_agent2 = o[:, :, 65] > 0.5

    # RULE R1: Enemy information (indices from policy specification)
    r1_indices_tensor = torch.tensor([4, 6, 7, 8, 9, 10, 12, 14, 15, 16, 17, 18,
                                     20, 22, 23, 24, 25, 26, 28, 30, 31, 32, 33, 34],
                                    dtype=torch.long, device=o.device)
    # Keep only indices within D (safety)
    valid_r1 = r1_indices_tensor < D
    r1_indices_tensor = r1_indices_tensor[valid_r1]
    if r1_indices_tensor.numel() > 0:
        mask_r1 = torch.zeros(D, dtype=o.dtype, device=o.device)
        mask_r1.scatter_(0, r1_indices_tensor, 1.0)
        what += is_agent0.unsqueeze(-1) * mask_r1.unsqueeze(0).unsqueeze(0)

    # RULE R2: Previous actions (indices 53 to 62 inclusive)
    r2_start = min(53, D)
    r2_end = min(63, D)
    if r2_start < r2_end:
        mask_r2 = torch.zeros(D, dtype=o.dtype, device=o.device)
        mask_r2[r2_start:r2_end] = 1.0
        what += (is_agent1.unsqueeze(-1) + is_agent2.unsqueeze(-1)) * mask_r2.unsqueeze(0).unsqueeze(0)

    return what


def communication(o):
    """
    Combines who, when, and what to produce the final aggregated communication tensor.
    Returns a tensor of shape [batch, n_agents, obs_dim] where each receiver’s
    channel contains the sum of messages from its allowed senders.
    """
    who = communication_who(o)          # [B, N, N] receiver x sender
    when = communication_when(o)        # [B, N, N]
    what = communication_what(o)        # [B, N, D] per-agent feature mask

    # Edge mask: which (receiver, sender) communications are active
    edge_mask = who * when              # [B, N, N]
    # Content: sender observations masked by what
    content = what * o                  # [B, N, D]

    # Aggregate messages to each receiver: (who*when) x (what * o)
    msg = torch.bmm(edge_mask, content) # [B, N, D]

    return msg
