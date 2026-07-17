import torch


def message_design_instruction() -> str:
    """
    Return a string describing the communication protocol design.
    This function is required by the LMAC teacher policy validation.
    """
    return (
        "Teacher communication for Terran 10vs10 with three unit types.\n"
        "Groups: G1 (medivac), G2 (marine/marauder).\n"
        "Who/When: All active agents communicate to every other active agent all the time.\n"
        "What:\n"
        "  - G1 always sends own health, position, unit type, and previous actions.\n"
        "  - G2 only sends if injured (health < 0.5). Sends own health, position, unit type, and previous actions.\n"
        "  - All agents always send previous actions.\n"
        "  - Enemy and ally slot data: only include features for slots where the unit is visible (available)."
    )


def communication(o: torch.Tensor):
    """
    Return a tuple (message, who, when, what) that defines the teacher
    communication for training. The message is a packed vector of selected features
    with a fixed maximum size M.
    Features are prioritized: own health/position/type first, then previous actions,
    then visible enemy data (closest first), then visible ally data (closest first).
    """
    who = communication_who(o)
    when = communication_when(o)
    what = communication_what(o)

    B, A, D = o.shape
    M = 10  # fixed message budget
    device = o.device
    dtype = o.dtype

    # Pre‑compute a global priority base and distance‑index lookup for every feature index.
    # This allows vectorised priority computation for each selected feature.
    PRIORITY_BASE = torch.full((D,), 1000.0, device=device, dtype=dtype)
    DIST_LOOKUP = -torch.ones(D, dtype=torch.long, device=device)

    # Own features (156‑161) – highest priority
    PRIORITY_BASE[156] = 0.0
    PRIORITY_BASE[157] = 1.0
    PRIORITY_BASE[158] = 2.0
    PRIORITY_BASE[159] = 3.0
    PRIORITY_BASE[160] = 4.0
    PRIORITY_BASE[161] = 5.0

    # Previous actions (162‑177) – second priority
    PRIORITY_BASE[162:178] = torch.arange(6.0, 22.0, device=device, dtype=dtype)

    # Enemy features (10 enemies, 7 visible features each) – third priority, ordered by distance
    for i in range(10):                     # 10 enemy slots
        base = 4 + i * 8
        dist_idx = base + 1                # distance is the second element of the group
        for k in range(1, 8):             # indices base+1 .. base+7
            feat_idx = base + k
            PRIORITY_BASE[feat_idx] = 22.0
            DIST_LOOKUP[feat_idx] = dist_idx

    # Ally features (9 allies, 7 visible features each) – fourth priority, ordered by distance
    for j in range(9):                      # 9 ally slots
        base = 84 + j * 8
        dist_idx = base + 1
        for k in range(1, 8):
            feat_idx = base + k
            PRIORITY_BASE[feat_idx] = 32.0
            DIST_LOOKUP[feat_idx] = dist_idx

    msg = torch.zeros(B, A, M, device=device, dtype=dtype)

    # Pack each agent's message by selecting priority‑sorted features up to M.
    for b in range(B):
        for a in range(A):
            mask_t = what[b, a].bool()
            if not mask_t.any():
                continue
            idx = mask_t.nonzero(as_tuple=False).squeeze(-1)  # shape (N,)
            if idx.numel() == 0:
                continue

            # Priority = base priority + distance-based tie‑breaker
            base_prio = PRIORITY_BASE[idx]                     # (N,)
            dist_idx = DIST_LOOKUP[idx]                        # (N,)
            dist_vals = torch.where(
                dist_idx >= 0,
                o[b, a, dist_idx],
                torch.tensor(0.0, device=device, dtype=dtype)
            )
            priority = base_prio + dist_vals

            _, order = torch.sort(priority)
            taken = idx[order][:M]                             # at most M
            msg[b, a, :len(taken)] = o[b, a, taken]

    return msg, who, when, what


def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Return binary matrix [batch, receiver, sender].
    All active agents (G1: medivac, G2: marine/marauder) may send to everyone else.
    """
    B, A, _ = o.shape
    g1 = o[:, :, 161] > 0.5
    g2 = (o[:, :, 159] > 0.5) | (o[:, :, 160] > 0.5)
    is_agent = g1 | g2

    who = is_agent.unsqueeze(1).expand(-1, A, -1).clone()
    diag = torch.eye(A, dtype=torch.bool, device=o.device).unsqueeze(0).expand(B, -1, -1)
    who[diag] = False
    return who.float()


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Return binary matrix [batch, receiver, sender].
    G1 and G2 agents always trigger because of the continuous own-health/action rules.
    """
    B, A, _ = o.shape
    g1 = o[:, :, 161] > 0.5
    g2 = (o[:, :, 159] > 0.5) | (o[:, :, 160] > 0.5)
    is_agent = g1 | g2

    when = is_agent.unsqueeze(1).expand(-1, A, -1).clone()
    diag = torch.eye(A, dtype=torch.bool, device=o.device).unsqueeze(0).expand(B, -1, -1)
    when[diag] = False
    return when.float()


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Return a binary mask of shape [batch, n_agents, obs_dim].
    Selects features according to the policy rules, vectorised over all agents and slots.
    """
    B, A, D = o.shape
    device = o.device
    dtype = o.dtype

    g1 = o[:, :, 161] > 0.5                     # RULE R3_medivac_always, R4_G1_actions
    g2 = (o[:, :, 159] > 0.5) | (o[:, :, 160] > 0.5)  # RULE R3_dps_injured, R4_G2_actions
    g2_injured = g2 & (o[:, :, 156] < 0.5)     # RULE R3_dps_injured

    mask = torch.zeros(B, A, D, dtype=dtype, device=device)

    # ----- own constant features (health & position) ----------
    mask[:, :, 156] = (g1 | g2_injured).to(dtype)
    mask[:, :, 157] = (g1 | g2_injured).to(dtype)
    mask[:, :, 158] = (g1 | g2_injured).to(dtype)

    mask[:, :, 161] = g1.to(dtype)
    mask[:, :, 159] = g2_injured.to(dtype)
    mask[:, :, 160] = g2_injured.to(dtype)

    # ----- previous actions (both groups always) ----------
    mask[:, :, 162:178] = (g1 | g2).unsqueeze(-1).to(dtype)

    # ----- enemy data (10 slots) ----------
    enemy_avail_idx = torch.arange(4, 84, 8, device=device)   # length 10
    enemy_vis = o[:, :, enemy_avail_idx] > 0.5                # [B, A, 10]

    enemy_feat_idx_base = enemy_avail_idx.unsqueeze(1) + torch.arange(1, 8, device=device)  # [10, 7]
    enemy_feat_idx_flat = enemy_feat_idx_base.reshape(-1)     # [70]

    vis_expand = enemy_vis.unsqueeze(-1).expand(-1, -1, -1, 7).reshape(B, A, -1).to(dtype)
    idx_tensor = enemy_feat_idx_flat.view(1, 1, -1).expand(B, A, -1)

    mask_flat = mask.reshape(B * A, D)
    mask_flat.scatter_(1, idx_tensor.reshape(B * A, -1), vis_expand.reshape(B * A, -1))

    # ----- ally data (9 slots) ----------
    ally_avail_idx = torch.arange(84, 156, 8, device=device)   # length 9
    ally_vis = o[:, :, ally_avail_idx] > 0.5                  # [B, A, 9]

    ally_feat_idx_base = ally_avail_idx.unsqueeze(1) + torch.arange(1, 8, device=device)  # [9, 7]
    ally_feat_idx_flat = ally_feat_idx_base.reshape(-1)       # [63]

    vis_expand_ally = ally_vis.unsqueeze(-1).expand(-1, -1, -1, 7).reshape(B, A, -1).to(dtype)
    idx_tensor_ally = ally_feat_idx_flat.view(1, 1, -1).expand(B, A, -1)

    mask_flat = mask.reshape(B * A, D)
    mask_flat.scatter_(1, idx_tensor_ally.reshape(B * A, -1), vis_expand_ally.reshape(B * A, -1))

    return mask
