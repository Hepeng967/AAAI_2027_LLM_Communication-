import torch as th

def message_design_instruction():
    """
    This protocol extends the previous message (enemy relative position + Overseer movement hints)
    by providing each Baneling with its own relative position (dx, dy) as observed by the Overseer.
    This direct spatial reference allows a Baneling to accurately convert the enemy's relative
    coordinates from the Overseer's frame to its own frame, eliminating the need to estimate the
    Overseer's location from its movement and last action. The new fields are crucial for
    precise X-coordinate reconstruction, which previously lagged behind Y-coordinate accuracy.
    """
    return ("The message now includes, for each Baneling, its own relative position to the Overseer "
            "(from the Overseer's observation). Together with the earlier enemy relative position, "
            "movement possibilities, and last action, this gives every Baneling a direct transformation "
            "between its own frame and the Overseer's frame, enabling exact enemy localization.")

def communication(o):
    """
    Input: o tensor of shape (32, 11, 103)
    Output: enhanced observation tensor of shape (32, 11, 103 + 15) = (32, 11, 118)

    The appended 15-dimensional message per agent is:
    [enemy_rel_x, enemy_rel_y, move_poss(4), last_action(7), baneling_rel_x, baneling_rel_y]
    Only the Overseer sends messages; Banelings receive them. The Overseer's own message is all zeros.
    """
    batch_size = o.shape[0]
    device = o.device
    overseer_idx = 10

    # ---- Part 1: Previously shared information (13 dimensions) ----
    enemy_rel = o[:, overseer_idx, 6:8]             # (32, 2)
    move_poss = o[:, overseer_idx, 0:4]             # (32, 4)
    last_action = o[:, overseer_idx, 85:92]         # (32, 7)
    base_msg = th.cat([enemy_rel, move_poss, last_action], dim=1)  # (32, 13)

    # ---- Part 2: New per‑Baneling relative positions from Overseer (2 dimensions each) ----
    # Each Baneling (agents 0-9) corresponds to an ally slot in the Overseer's observation.
    # Ally slot k (0..9) occupies indices [12+8*k, 19+8*k].
    # Relative X = index 14+8*k, Relative Y = index 15+8*k.
    # Build a flattened index list for all 10 Banelings: [(14,15), (22,23), ..., (86,87)]
    indices = th.cat([th.arange(14+8*k, 16+8*k, device=device) for k in range(10)])  # (20,)
    # Extract and reshape: (32, 20) -> (32, 10, 2)
    per_baneling = o[:, overseer_idx, indices].reshape(batch_size, 10, 2)

    # ---- Construct final message tensor (32, 11, 15) ----
    msg = th.zeros(batch_size, 11, 15, device=device)
    # For all Banelings (agents 0..9)
    msg[:, :10, :13] = base_msg.unsqueeze(1).expand(-1, 10, -1)   # broadcast base_msg
    msg[:, :10, 13:15] = per_baneling                              # per‑Baneling offset

    # ---- Append to observations ----
    enhanced_o = th.cat([o, msg], dim=2)   # (32, 11, 118)
    return enhanced_o
