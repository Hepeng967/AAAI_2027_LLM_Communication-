import torch as th

def message_design_instruction():
    """
    This protocol bridges the knowledge gap for Banelings by having the Overseer (Agent 10)
    share its observed enemy relative position, its own movement possibilities, and its last action.
    Since Banelings do not know the enemy location and lack a common reference frame,
    the Overseer's message provides the necessary information for each Baneling to reconstruct
    the enemy's absolute position relative to itself (using the Overseer's position as a reference).
    The movement possibilities and last action help infer the Overseer's current location
    and movement intent, further improving localization and coordination.
    """
    return ("The Overseer shares enemy relative position, its movement capabilities, and last action. "
            "Baneling recipients use this to infer the enemy's absolute location relative to themselves, "
            "enabling rapid convergence on the target.")

def communication(o):
    """
    Input: o tensor of shape (32, 11, 103)
    Output: enhanced observation tensor of shape (32, 11, 103 + message_dim)
    """
    batch_size = o.shape[0]
    device = o.device
    overseer_idx = 10  # agent index of the Overseer

    # ----- Extract Overseer's critical features -----
    # Enemy relative position (continuous): indices 6,7
    enemy_rel = o[:, overseer_idx, 6:8]                     # (32, 2)

    # Movement possibilities (binary): indices 0..3
    move_poss = o[:, overseer_idx, 0:4]                     # (32, 4)

    # Last action one‑hot (binary): indices 85..91 (7 values)
    last_action = o[:, overseer_idx, 85:92]                 # (32, 7)

    # Concatenate into a 13‑dimensional message
    overseer_msg = th.cat([enemy_rel, move_poss, last_action], dim=1)  # (32, 13)

    # ----- Build message tensor for all agents -----
    msg_dim = overseer_msg.shape[1]                         # 13
    msg = th.zeros(batch_size, 11, msg_dim, device=device)

    # Assign the Overseer's message to all Banelings (agents 0..9)
    baneling_indices = [i for i in range(11) if i != overseer_idx]  # 10 agents
    # Expand overseer_msg to match the number of Banelings
    msg[:, baneling_indices, :] = overseer_msg.unsqueeze(1).expand(-1, len(baneling_indices), -1)

    # ----- Append message to observations -----
    enhanced_o = th.cat([o, msg], dim=2)                    # (32, 11, 116)

    return enhanced_o

def communication_matrix(o):
    """
    matrix[:, receiver, sender] = 1.
    Banelings receive the Overseer's message; the Overseer does not receive from itself.
    """
    batch_size, n_agents, _ = o.shape
    device = o.device
    matrix = th.zeros(batch_size, n_agents, n_agents, device=device, dtype=o.dtype)
    overseer_idx = n_agents - 1
    baneling_indices = [i for i in range(n_agents) if i != overseer_idx]
    matrix[:, baneling_indices, overseer_idx] = 1.0
    return matrix
