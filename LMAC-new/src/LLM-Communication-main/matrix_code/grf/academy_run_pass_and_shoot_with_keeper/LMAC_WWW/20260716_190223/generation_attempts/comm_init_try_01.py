import torch

def message_design_instruction() -> str:
    """
    Concise description of the communication policy.
    """
    return (
        "Symmetric attacker group G1: when an agent has ball possession "
        "(ball distance < 0.1), it sends its absolute position, ball relative "
        "position, and ball direction to the other attacker to coordinate "
        "run-pass-shoot intentions."
    )

# ----------------------------------------------------------------------
# RULE R1
# Symmetric attackers (agent 0 and agent 1) from group G1.
# Sender: any agent that possesses the ball (ball_relative_xy norm < 0.1).
# Receiver: the other agent (teammate).
# Content: ego_absolute_xy (indices 0,1), ball_relative_xy (16,17),
#          ball_direction_xyz (19,20,21).
# ----------------------------------------------------------------------

def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns sender-receiver connectivity matrix.
    Shape: [batch, n_agents, n_agents] with 1 for teammate edges, 0 otherwise.
    Diagonal is zero (no self-communication).
    """
    # RULE R1
    batch, n_agents, _ = o.shape
    # For two symmetric attackers, teammate of agent 0 is 1 and vice versa.
    # Base matrix: anti-diagonal ones.
    base_who = torch.tensor([[0., 1.],
                             [1., 0.]], device=o.device, dtype=torch.float32)
    # Expand to batch dimension
    who = base_who.unsqueeze(0).expand(batch, -1, -1)
    return who

def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns temporal activation for each sender-receiver pair.
    Shape: [batch, n_agents, n_agents] with 1 if sender has ball close,
    0 otherwise, and zero on the diagonal.
    """
    # RULE R1
    batch, n_agents, _ = o.shape
    # Ball distance: ||ball_relative_xy|| (indices 16,17)
    ball_vec = o[..., 16:18]                     # [batch, n_agents, 2]
    ball_dist = torch.norm(ball_vec, dim=-1)     # [batch, n_agents]
    active_sender = (ball_dist < 0.1).float()    # [batch, n_agents]

    # Create when matrix: for sender s, value active_sender[b,s] for all receivers
    when = active_sender.unsqueeze(1).expand(-1, n_agents, -1)  # [batch, n_agents, n_agents]
    # Remove self-communication by zeroing the diagonal
    eye = torch.eye(n_agents, device=o.device).unsqueeze(0)     # [1, n_agents, n_agents]
    when = when * (1.0 - eye)

    return when

def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a mask that selects which observation features to send.
    Shape matches o: [batch, n_agents, obs_dim], with 1 at selected indices,
    0 elsewhere.
    """
    # RULE R1
    # Selected indices: ego_absolute_xy (0,1), ball_relative_xy (16,17),
    #                   ball_direction_xyz (19,20,21)
    mask = torch.zeros_like(o)
    feature_indices = [0, 1, 16, 17, 19, 20, 21]
    # Only use indices that are within the actual observation dimension
    obs_dim = o.shape[-1]
    valid_indices = [idx for idx in feature_indices if idx < obs_dim]
    # Assign 1.0 to the selected features for all agents
    mask[:, :, valid_indices] = 1.0
    return mask