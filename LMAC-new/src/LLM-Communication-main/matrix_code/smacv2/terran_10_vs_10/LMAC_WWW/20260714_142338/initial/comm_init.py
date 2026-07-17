import torch

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