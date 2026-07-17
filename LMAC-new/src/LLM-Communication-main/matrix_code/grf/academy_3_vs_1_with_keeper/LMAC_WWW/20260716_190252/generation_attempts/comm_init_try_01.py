import torch

def message_design_instruction() -> str:
    return (
        "Agents dynamically partition into ball carrier (ball distance < 0.15) and off-ball receivers (>= 0.15). "
        "Ball carrier broadcasts its agent_id and previous action to all off-ball receivers. "
        "Off-ball receivers broadcast their absolute position and opponent relative positions/directions to the ball carrier."
    )

def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a binary matrix of shape [batch, receiver, sender] indicating which
    sender-receiver pairs are eligible for communication.
    """
    B, N, _ = o.shape
    device = o.device

    # Compute ball distance for each agent
    ball_dist = torch.norm(o[..., 20:22], dim=-1)  # [B, N]

    # Group membership (mutually exclusive except possible boundary)
    is_G1 = ball_dist < 0.15   # ball carrier
    is_G2 = ball_dist >= 0.15  # off-ball receiver

    # RULE R1, R5: ball carrier (G1) -> off-ball receivers (G2)
    # RULE R2, R3, R4: off-ball (G2) -> ball carrier (G1)
    # Edges: G1->G2 and G2->G1, zero self-communication
    G1_to_G2 = is_G2.unsqueeze(1) * is_G1.unsqueeze(2)  # [B, N, N]
    G2_to_G1 = is_G1.unsqueeze(1) * is_G2.unsqueeze(2)  # [B, N, N]
    who = torch.logical_or(G1_to_G2, G2_to_G1).to(dtype=torch.float32)

    # Zero out diagonal (no self-communication)
    diag = torch.eye(N, device=device, dtype=who.dtype).unsqueeze(0)
    who = who * (1.0 - diag)
    return who


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a binary matrix of shape [batch, receiver, sender] indicating whether
    the sender currently wishes to communicate.
    """
    B, N, _ = o.shape
    device = o.device

    ball_dist = torch.norm(o[..., 20:22], dim=-1)  # [B, N]
    is_G1 = ball_dist < 0.15
    is_G2 = ball_dist >= 0.15

    # RULE R1, R5: sender condition is ball_distance < 0.15 (i.e., sender is G1)
    # RULE R2, R3, R4: sender condition is ball_distance >= 0.15 (i.e., sender is G2)
    # Combine: any sender that belongs to a group communicates when it satisfies its group membership.
    when = is_G1.unsqueeze(1).expand(B, N, N).float() + is_G2.unsqueeze(1).expand(B, N, N).float()
    when = when.clamp(0.0, 1.0)

    # No self-communication
    diag = torch.eye(N, device=device, dtype=when.dtype).unsqueeze(0)
    when = when * (1.0 - diag)
    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns an obs-aligned content mask of shape [batch, n_agents, obs_dim].
    Features to be transmitted are set to 1; all others are 0.
    """
    B, N, D = o.shape
    device = o.device

    ball_dist = torch.norm(o[..., 20:22], dim=-1)  # [B, N]
    is_G1 = ball_dist < 0.15   # ball carrier group
    is_G2 = ball_dist >= 0.15  # off-ball receiver group

    mask = torch.zeros(B, N, D, device=device, dtype=torch.float32)

    # RULE R1: ball carrier sends agent_id_one_hot (indices 45,46,47)
    mask[:, :, [45, 46, 47]] = is_G1.unsqueeze(-1).float().expand(-1, -1, 3)

    # RULE R5: ball carrier sends previous_action_one_hot (indices 26..44)
    mask[:, :, 26:45] = is_G1.unsqueeze(-1).float().expand(-1, -1, 19)

    # RULE R2: off-ball receiver sends ego_absolute_xy (indices 0,1)
    mask[:, :, [0, 1]] = is_G2.unsqueeze(-1).float().expand(-1, -1, 2)

    # RULE R3: off-ball receiver sends opponent_0_relative_xy (12,13) and opponent_1_relative_xy (14,15)
    mask[:, :, 12:14] = is_G2.unsqueeze(-1).float().expand(-1, -1, 2)
    mask[:, :, 14:16] = is_G2.unsqueeze(-1).float().expand(-1, -1, 2)

    # RULE R4: off-ball receiver sends opponent_0_direction_xy (16,17) and opponent_1_direction_xy (18,19)
    mask[:, :, 16:18] = is_G2.unsqueeze(-1).float().expand(-1, -1, 2)
    mask[:, :, 18:20] = is_G2.unsqueeze(-1).float().expand(-1, -1, 2)

    return mask