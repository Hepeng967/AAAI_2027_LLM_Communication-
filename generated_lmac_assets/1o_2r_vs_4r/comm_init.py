import torch as th

def message_design_instruction():
    return (
        "Each agent sends a compact message containing: (1) for each of the 4 enemies: "
        "visibility flag, relative X/Y coordinates, and health ratio; (2) own health ratio; "
        "(3) own unit type (Roach or Overseer); (4) movement capabilities in the four "
        "cardinal directions. The recipient receives the messages from its two teammates "
        "(appended without identity reordering). This allows an allied Roach with limited "
        "sight to reconstruct enemy positions and health seen by the Overseer or the other "
        "Roach, infer teammate health and type, and understand their movement constraints, "
        "thereby improving focus fire and positioning coordination."
    )

def communication(o):
    """
    Builds enhanced observations with teammate messages.

    Input:
        o: torch.tensor of shape (2, 3, 66)
            2 scenes, 3 agents, 66 observation features.
    Output:
        torch.tensor of shape (2, 3, 66 + 46)
            Concatenation of original observation and the two other agents' messages.
    """
    device = o.device
    batch_size, n_agents, _ = o.shape

    # Indices for the compact per‑agent message (sender's view)
    # Enemies: 4 enemies * {visible, relX, relY, health}
    enemy_idx = []
    for e in range(4):
        base = 4 + e * 8  # visible flag
        enemy_idx.extend([base, base + 2, base + 3, base + 4])
    # Own status
    own_health = [50]
    own_type   = [51, 52]
    move_caps  = [0, 1, 2, 3]

    msg_indices = enemy_idx + own_health + own_type + move_caps
    msg_indices = th.tensor(msg_indices, device=device, dtype=th.long)

    # Extract message from every agent: (2, 3, 23)
    all_msgs = o[:, :, msg_indices]

    # For agent i, combine messages from the two other agents.
    # Fixed order of teammates for each agent:
    other_map = th.tensor([[1, 2],
                           [0, 2],
                           [0, 1]], device=device)  # (3, 2)

    # Gather: (2, 3, 2, 23)
    gathered = all_msgs[:, other_map]
    # Flatten to (2, 3, 46)
    others_msg = gathered.reshape(batch_size, n_agents, -1)

    # Append to original observation → (2, 3, 66 + 46 = 112)
    enhanced_o = th.cat([o, others_msg], dim=-1)
    return enhanced_o
