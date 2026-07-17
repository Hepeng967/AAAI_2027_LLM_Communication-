```python
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
    communication for training. The message is a packed vector of selected features.
    Here we pack up to 10 features per agent (deterministic order 0..D-1)
    for compatibility with a fixed message size.
    """
    who = communication_who(o)
    when = communication_when(o)
    what = communication_what(o)
    B, A, D = o.shape
    M = 10  # typical message size for SMACv2
    msg = torch.zeros(B, A, M, device=o.device, dtype=o.dtype)
    # For each agent, take the first M features marked True in the what mask.
    # This is vectorised for efficiency.
    flat_mask = what.reshape(B * A, D) > 0.5  # (B*A, D)
    # Find indices of selected features per agent (flat)
    selected_indices = flat_mask.nonzero(as_tuple=False)  # (N_selected, 2) [flat_idx, feat_idx]
    # Sort by flat_idx then feat_idx to ensure first-M per agent
    selected_indices = selected_indices[selected_indices[:, 1].argsort()]
    selected_indices = selected_indices[selected_indices[:, 0].argsort(kind='stable')]
    # Count selections per flat index
    if selected_indices.numel() > 0:
        flat_idx = selected_indices[:, 0]
        feat_idx = selected_indices[:, 1]
        # Use scatter to fill message
        # truncation: for each agent, take first M
        counts = torch.zeros(B * A, dtype=torch.long, device=o.device)
        for i in range(selected_indices.size(0)):
            ag = flat_idx[i].item()
            if counts[ag] < M:
                msg.view(B * A, M)[ag, counts[ag]] = o.view(B * A, D)[ag, feat_idx[i]]
                counts[ag] += 1
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
```