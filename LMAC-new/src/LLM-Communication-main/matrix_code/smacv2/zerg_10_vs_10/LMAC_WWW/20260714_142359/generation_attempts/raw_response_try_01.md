```python
import torch
from typing import List, Tuple

def _compute_rules(o: torch.Tensor) -> Tuple[List[torch.Tensor], List[torch.Tensor]]:
    """
    Helper that computes for each rule:
      - a boolean trigger tensor of shape [batch, n_agents]
      - a 1-D float mask of length obs_dim indicating which features to send
    Both lists are ordered: R1, R2, ..., R20.
    """
    batch, n_agents, obs_dim = o.shape
    triggers: List[torch.Tensor] = []
    masks: List[torch.Tensor] = []

    # Helper to create a feature mask, skipping indices >= obs_dim
    def _make_mask(indices):
        m = torch.zeros(obs_dim, device=o.device)
        for i in indices:
            if i < obs_dim:
                m[i] = 1.0
        return m

    # --- R1: own_health > 0.0 ---------------------------------------------------
    # Trigger: always true when alive (own_health > 0)
    idx_cond = 156
    trig = (o[..., idx_cond] > 0.0) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([156, 157, 158, 159, 160, 161, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187]))

    # --- R2: enemy_0_available > 0.5 -------------------------------------------
    idx_cond = 4
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 4, 5, 6, 7, 8, 9, 10, 11]))

    # --- R3: enemy_1_available > 0.5 -------------------------------------------
    idx_cond = 12
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 12, 13, 14, 15, 16, 17, 18, 19]))

    # --- R4: enemy_2_available > 0.5 -------------------------------------------
    idx_cond = 20
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 20, 21, 22, 23, 24, 25, 26, 27]))

    # --- R5: enemy_3_available > 0.5 -------------------------------------------
    idx_cond = 28
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 28, 29, 30, 31, 32, 33, 34, 35]))

    # --- R6: enemy_4_available > 0.5 -------------------------------------------
    idx_cond = 36
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 36, 37, 38, 39, 40, 41, 42, 43]))

    # --- R7: enemy_5_available > 0.5 -------------------------------------------
    idx_cond = 44
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 44, 45, 46, 47, 48, 49, 50, 51]))

    # --- R8: enemy_6_available > 0.5 -------------------------------------------
    idx_cond = 52
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 52, 53, 54, 55, 56, 57, 58, 59]))

    # --- R9: enemy_7_available > 0.5 -------------------------------------------
    idx_cond = 60
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 60, 61, 62, 63, 64, 65, 66, 67]))

    # --- R10: enemy_8_available > 0.5 ------------------------------------------
    idx_cond = 68
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 68, 69, 70, 71, 72, 73, 74, 75]))

    # --- R11: enemy_9_available > 0.5 ------------------------------------------
    idx_cond = 76
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 76, 77, 78, 79, 80, 81, 82, 83]))

    # --- R12: ally_slot_0_visible > 0.5 ----------------------------------------
    idx_cond = 84
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 84, 85, 86, 87, 88, 89, 90, 91]))

    # --- R13: ally_slot_1_visible > 0.5 ----------------------------------------
    idx_cond = 92
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 92, 93, 94, 95, 96, 97, 98, 99]))

    # --- R14: ally_slot_2_visible > 0.5 ----------------------------------------
    idx_cond = 100
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 100, 101, 102, 103, 104, 105, 106, 107]))

    # --- R15: ally_slot_3_visible > 0.5 ----------------------------------------
    idx_cond = 108
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 108, 109, 110, 111, 112, 113, 114, 115]))

    # --- R16: ally_slot_4_visible > 0.5 ----------------------------------------
    idx_cond = 116
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 116, 117, 118, 119, 120, 121, 122, 123]))

    # --- R17: ally_slot_5_visible > 0.5 ----------------------------------------
    idx_cond = 124
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 124, 125, 126, 127, 128, 129, 130, 131]))

    # --- R18: ally_slot_6_visible > 0.5 ----------------------------------------
    idx_cond = 132
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 132, 133, 134, 135, 136, 137, 138, 139]))

    # --- R19: ally_slot_7_visible > 0.5 ----------------------------------------
    idx_cond = 140
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 140, 141, 142, 143, 144, 145, 146, 147]))

    # --- R20: ally_slot_8_visible > 0.5 ----------------------------------------
    idx_cond = 148
    trig = (o[..., idx_cond] > 0.5) if idx_cond < obs_dim else torch.zeros(batch, n_agents, dtype=torch.bool, device=o.device)
    triggers.append(trig)
    masks.append(_make_mask([157, 158, 148, 149, 150, 151, 152, 153, 154, 155]))

    return triggers, masks


def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    All-to-all communication (every sender can reach every receiver) except self.
    Returns tensor of shape [batch, n_agents, n_agents] with off-diagonal 1s.
    """
    batch, n_agents, _ = o.shape
    who = torch.ones(batch, n_agents, n_agents, device=o.device)
    # Zero out self-communication diagonal
    diag = torch.arange(n_agents, device=o.device)
    who[:, diag, diag] = 0.0
    return who


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns [batch, n_agents, n_agents] with 1 when any rule triggers for the sender.
    A triggered sender broadcasts to all receivers (all columns for that sender are 1).
    Self-communication is handled later by the runtime via who * when.
    """
    batch, n_agents, _ = o.shape
    triggers, _ = _compute_rules(o)  # list of [batch, n_agents] bool tensors

    # Stack to [num_rules, batch, n_agents] and take OR across rules
    all_trig = torch.stack(triggers, dim=0)  # shape [20, batch, n_agents]
    sender_trigger = all_trig.any(dim=0)      # [batch, n_agents] bool

    # A triggered sender sends to all receivers: broadcast across receiver dim
    when = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1).float()
    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns an obs-aligned content mask of shape [batch, n_agents, obs_dim].
    For each sender, the mask is the union of feature indices from all triggered rules.
    """
    triggers, masks = _compute_rules(o)  # list of length 20

    # Stack triggers: [num_rules, batch, n_agents]       float
    triggers_stack = torch.stack(triggers, dim=0).float()   # shape [20, B, N]
    # Stack masks:    [num_rules, obs_dim]                float
    masks_stack = torch.stack(masks, dim=0)                # shape [20, obs_dim]

    # For each rule, a sender contributes its mask where triggered:
    #   contribution = triggers_stack[:,:,:,None] * masks_stack[:,None,None,:]
    #   shape: [20, B, N, obs_dim]
    contribution = (triggers_stack.unsqueeze(-1) * masks_stack.unsqueeze(1).unsqueeze(1))
    # Union: any rule triggers that feature -> max across rules, clip to [0,1]
    what = contribution.sum(dim=0).clamp(max=1.0)
    return what
```