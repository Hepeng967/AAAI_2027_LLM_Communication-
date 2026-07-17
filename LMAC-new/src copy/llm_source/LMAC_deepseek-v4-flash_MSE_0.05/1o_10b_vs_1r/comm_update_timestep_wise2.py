import torch as th

def message_design_instruction():
    """
    This protocol provides historical per‑Baneling relative positions and a temporal
    displacement of the Overseer.  The per‑Baneling information is extracted from the
    Overseer's entire 10‑step history: for each Baneling, the most recent timestep
    where it was visible is used, together with a validity flag.  This eliminates the
    information asymmetry that previously caused high variance in X‑coordinate
    reconstruction.  The cumulative displacement of the Overseer over the past 10 steps
    gives every Baneling a consistent reference to align coordinate frames.
    """
    return (
        "New message (32 dims): per‑Baneling historical (dx,dy,valid) and Overseer "
        "cumulative displacement.  These fields complement the previous message (current "
        "enemy position, movement possibilities, last action, current per‑Baneling position) "
        "by providing robust temporal context when a Baneling is not currently visible."
    )

def communication(o):
    """
    Input: o tensor of shape (batch_size, T, 11, 103)
    Output: enhanced observation tensor of shape (batch_size, 11, 103 + 15 + 32)
            = (batch_size, 11, 150)
    """
    batch_size, T, n_agents, obs_dim = o.shape
    device = o.device
    overseer_idx = 10

    # -------- Extract current timestep (last in the history) --------
    o_cur = o[:, -1, :, :]                       # (batch, 11, 103)

    # -------- Build previous message (15 dims) --------
    # Overseer's enemy relative position (2)
    enemy_rel = o_cur[:, overseer_idx, 6:8]       # (batch, 2)
    # Overseer's movement possibilities (4)
    move_poss = o_cur[:, overseer_idx, 0:4]       # (batch, 4)
    # Overseer's last action one-hot (7)
    last_action = o_cur[:, overseer_idx, 85:92]   # (batch, 7)
    base_msg = th.cat([enemy_rel, move_poss, last_action], dim=1)  # (batch, 13)

    # Per‑Baneling current relative positions from Overseer (2 dims each)
    # Ally slots: indices 14+8*k, 15+8*k for k=0..9
    idx_rel = th.cat([th.arange(14 + 8*k, 16 + 8*k, device=device) for k in range(10)])  # (20,)
    per_baneling_cur = o_cur[:, overseer_idx, idx_rel].reshape(batch_size, 10, 2)  # (batch,10,2)

    # Assemble previous message: (batch, 11, 15)
    prev_msg = th.zeros(batch_size, 11, 15, device=device)
    prev_msg[:, :10, :13] = base_msg.unsqueeze(1).expand(-1, 10, -1)   # broadcast base
    prev_msg[:, :10, 13:15] = per_baneling_cur                         # current per-baneling
    # Overseer gets zeros (already)

    # -------- Build new message (32 dims) --------
    # --- 1. Per‑Baneling historical most recent valid (dx, dy) and validity flag ---
    # Overseer's view over all T steps: (batch, T, 103)
    o_ov = o[:, :, overseer_idx, :]               # (batch, T, 103)

    # Indices for each Baneling's visibility flag (12+8*k) and relative position (14+8*k,15+8*k)
    vis_idx = th.tensor([12 + 8*k for k in range(10)], device=device)         # (10,)
    relx_idx = th.tensor([14 + 8*k for k in range(10)], device=device)        # (10,)
    rely_idx = th.tensor([15 + 8*k for k in range(10)], device=device)        # (10,)

    # Extract tensors: shape (batch, T, 10)
    vis = o_ov[:, :, vis_idx]                     # (batch, T, 10)
    relx = o_ov[:, :, relx_idx]                   # (batch, T, 10)
    rely = o_ov[:, :, rely_idx]                   # (batch, T, 10)

    # Find the last timestep (0-indexed) where visibility is 1
    # Use cumulative sum to get the index of the last occurrence
    cum_vis = vis.cumsum(dim=1) > 0               # bool, (batch, T, 10)
    last_visible_t = (cum_vis.sum(dim=1).float() - 1).clamp(min=0)  # (batch, 10)
    # Has any visible timestep?
    has_any = (vis.sum(dim=1) > 0.5).float()      # (batch, 10)

    # Gather relative positions at last_visible_t
    idx_gather = last_visible_t.long().unsqueeze(1)  # (batch, 1, 10)
    relx_hist = th.gather(relx, dim=1, index=idx_gather).squeeze(1)  # (batch, 10)
    rely_hist = th.gather(rely, dim=1, index=idx_gather).squeeze(1)  # (batch, 10)
    # Zero out for banelings that were never visible
    relx_hist = relx_hist * has_any
    rely_hist = rely_hist * has_any

    # Assemble per-baneling new fields (3 dims each): (batch, 10, 3)
    per_baneling_new = th.stack([relx_hist, rely_hist, has_any], dim=2)  # (batch, 10, 3)

    # --- 2. Overseer cumulative displacement over T steps ---
    # Overseer's last_action one-hots over all T timesteps: (batch, T, 7)
    ov_actions = o[:, :, overseer_idx, 85:92]      # (batch, T, 7)
    # Movement vectors: [No-op,Stop,North,South,East,West,Attack]
    movements = th.tensor([[0,0],[0,0],[0,1],[0,-1],[1,0],[-1,0],[0,0]], device=device, dtype=o.dtype)
    disp = ov_actions @ movements                  # (batch, T, 2)
    cum_disp = disp.sum(dim=1) / T                 # (batch, 2)

    # Build new message (batch, 11, 32)
    new_msg = th.zeros(batch_size, 11, 32, device=device)
    # For Banelings (0..9): per-baneling (3 dims) + overseer displacement (2 dims)
    new_msg[:, :10, :3] = per_baneling_new         # historical (dx,dy,flag)
    new_msg[:, :10, 3:5] = cum_disp.unsqueeze(1).expand(-1, 10, -1)  # broadcast displacement
    # Overseer gets zeros (already)

    # -------- Combine previous and new messages into one (47 dims) --------
    combined_msg = th.cat([prev_msg, new_msg], dim=2)   # (batch, 11, 47)

    # -------- Append to current observation --------
    enhanced_o = th.cat([o_cur, combined_msg], dim=2)   # (batch, 11, 103+47=150)

    return enhanced_o
