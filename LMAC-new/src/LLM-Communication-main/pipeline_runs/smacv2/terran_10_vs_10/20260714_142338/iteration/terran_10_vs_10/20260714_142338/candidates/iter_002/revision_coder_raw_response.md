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
        "Who/When: Medivac communicates to all active agents. Injured DPS (health < 0.5) communicates only to medivac. No self-loops.\n"
        "What:\n"
        "  - G1 sends own health, position (normalized x,y), and unit type (medivac).\n"
        "  - G2 (injured) sends own health, position, unit type (marine/marauder), plus distance, direction x, direction y, and health of the closest visible enemy.\n"
        "  - Previous actions and ally features are not transmitted to make room for critical spatial data."
    )


def communication(o: torch.Tensor):
    """
    Return a tuple (message, who, when, what) that defines the teacher
    communication for training. The message is a packed vector of selected features
    with a fixed maximum size M.
    Priority: own features first, then enemy features (distance, rel_x, rel_y, health).
    """
    who = communication_who(o)
    when = communication_when(o)
    what = communication_what(o)

    B, A, D = o.shape
    M = 10  # fixed message budget
    device = o.device
    dtype = o.dtype

    # Priority base for feature ordering
    PRIORITY_BASE = torch.full((D,), 1000.0, device=device, dtype=dtype)
    DIST_LOOKUP = -torch.ones(D, dtype=torch.long, device=device)

    # Own features (156-161)   RULE R1, R2
    PRIORITY_BASE[156] = 0.0   # health
    PRIORITY_BASE[157] = 1.0   # normalized_x
    PRIORITY_BASE[158] = 2.0   # normalized_y
    PRIORITY_BASE[159] = 3.0   # marine type
    PRIORITY_BASE[160] = 4.0   # marauder type
    PRIORITY_BASE[161] = 5.0   # medivac type

    # Closest enemy features (indices 5+8*i to 8+8*i)   RULE R2
    for i in range(10):
        base = 4 + 8 * i
        dist_idx = base + 1
        PRIORITY_BASE[base+1] = 20.0   # distance
        PRIORITY_BASE[base+2] = 21.0   # rel_x
        PRIORITY_BASE[base+3] = 22.0   # rel_y
        PRIORITY_BASE[base+4] = 23.0   # health
        for k in range(1, 5):
            DIST_LOOKUP[base + k] = dist_idx

    msg = torch.zeros(B, A, M, device=device, dtype=dtype)

    for b in range(B):
        for a in range(A):
            mask_t = what[b, a].bool()
            if not mask_t.any():
                continue
            idx = mask_t.nonzero(as_tuple=False).squeeze(-1)
            if idx.numel() == 0:
                continue

            base_prio = PRIORITY_BASE[idx]
            dist_idx = DIST_LOOKUP[idx]
            dist_vals = torch.where(
                dist_idx >= 0,
                o[b, a, dist_idx],
                torch.tensor(0.0, device=device, dtype=dtype)
            )
            priority = base_prio + dist_vals
            _, order = torch.sort(priority)
            taken = idx[order][:M]
            msg[b, a, :len(taken)] = o[b, a, taken]

    return msg, who, when, what


def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    RULE who: Medivac to all active agents; Injured DPS only to medivac. No self-loops.
    """
    B, A, _ = o.shape
    device = o.device

    g1 = o[:, :, 161] > 0.5                         # medivac
    g2 = (o[:, :, 159] > 0.5) | (o[:, :, 160] > 0.5)   # marine or marauder
    is_active = g1 | g2
    g2_injured = g2 & (o[:, :, 156] < 0.5)

    identity = torch.eye(A, dtype=torch.bool, device=device).unsqueeze(0)   # (1, A, A)

    # Who mask: (G1 sender to all active receivers) OR (G2 injured sender to G1 receivers), no self
    who_mask = (
        (g1.unsqueeze(2) & is_active.unsqueeze(1)) |
        (g2_injured.unsqueeze(2) & g1.unsqueeze(1))
    ) & ~identity

    return who_mask.float()


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    RULE when: same as who, communication only when there is an intended receiver.
    """
    return communication_who(o).clone()


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    RULE R1 (Medivac): own health, position, unit type.
    RULE R2 (Injured DPS): own health, position, unit type, plus closest visible enemy
    distance, direction, health.
    Previous actions and ally data are excluded to fit the message budget.
    """
    B, A, D = o.shape
    device = o.device
    dtype = o.dtype

    g1 = o[:, :, 161] > 0.5                          # medivac
    g2 = (o[:, :, 159] > 0.5) | (o[:, :, 160] > 0.5)   # DPS
    g2_injured = g2 & (o[:, :, 156] < 0.5)           # injured DPS

    is_marine = o[:, :, 159] > 0.5
    is_marauder = o[:, :, 160] > 0.5

    mask = torch.zeros(B, A, D, dtype=dtype, device=device)

    # Own features for G1 and G2_injured
    own_active = g1 | g2_injured
    mask[:, :, 156] = own_active.to(dtype)          # health
    mask[:, :, 157] = own_active.to(dtype)          # norm_x
    mask[:, :, 158] = own_active.to(dtype)          # norm_y
    mask[:, :, 159] = (g2_injured & is_marine).to(dtype)     # marine type
    mask[:, :, 160] = (g2_injured & is_marauder).to(dtype)   # marauder type
    mask[:, :, 161] = g1.to(dtype)                           # medivac type

    # Closest visible enemy for G2_injured
    enemy_avail = o[:, :, 4::8] > 0.5               # [B, A, 10]
    enemy_dist = o[:, :, 5::8]                      # [B, A, 10]
    enemy_dist_masked = enemy_dist.masked_fill(~enemy_avail, float('inf'))
    closest_idx = enemy_dist_masked.argmin(dim=-1)   # [B, A]
    has_visible_enemy = enemy_avail.any(dim=-1)      # [B, A]
    g2_cond = g2_injured & has_visible_enemy         # only include enemy data if a visible enemy exists

    i = closest_idx
    idx_dist = 5 + 8 * i
    idx_relx = 6 + 8 * i
    idx_rely = 7 + 8 * i
    idx_health = 8 + 8 * i
    all_indices = torch.stack([idx_dist, idx_relx, idx_rely, idx_health], dim=-1)  # (B, A, 4)

    values = g2_cond.unsqueeze(-1).expand(-1, -1, 4).to(dtype)
    mask_flat = mask.reshape(B * A, D)
    mask_flat.scatter_(1, all_indices.reshape(B * A, 4), values.reshape(B * A, 4))

    return mask
```