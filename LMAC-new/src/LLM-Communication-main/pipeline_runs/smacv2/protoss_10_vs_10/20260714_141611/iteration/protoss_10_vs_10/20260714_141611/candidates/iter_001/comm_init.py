import torch


def message_design_instruction():
    """
    Communication design for protoss_10_vs_10 (SMACv2).
    Unit types are dynamic: stalker, zealot, colossus.
    No self-communication; agents talk across unit types (R1-R3).
    The who graph connects each unit type to the other two types.
    The when mask triggers on ANY enemy or ally visibility (using all slots).
    The what mask shares own (x,y) coordinates plus only the slots that are
    currently observed (per-slot availability > 0.5), reducing message noise.

    Revision based on judge feedback:
    - when now uses torch.any over all enemy_available and all ally_visible slots.
    - what dynamically includes only visible slots, not all slots.
    """
    return (
        "Cross-type communication policy: "
        "who: edges from each unit type to the other two types; "
        "when: triggered when sender sees ANY enemy or ANY ally; "
        "what: own position + inventory of only the currently observed entities."
    )


def _add_group_links(who, sender_mask, receiver_mask):
    """
    Add directed edges from any agent with sender_mask True to any agent with receiver_mask True.
    who: (B, N, N) modified in-place.
    """
    who.add_(receiver_mask.unsqueeze(2).float() * sender_mask.unsqueeze(1).float())


def _apply_what_mask(what_mask, condition, feature_indices):
    """
    Set given feature indices to 1 for all senders where condition is True.
    what_mask: (B, N, D) modified in-place.
    condition: (B, N) bool
    feature_indices: (F,) long tensor
    """
    B, N, D = what_mask.shape
    valid_flat = condition.reshape(-1).nonzero(as_tuple=False).squeeze(1)  # (num_true,)
    if valid_flat.size(0) == 0:
        return
    batch_idx = valid_flat // N
    agent_idx = valid_flat % N
    F = feature_indices.size(0)
    num_true = valid_flat.size(0)
    rep_batch = batch_idx.repeat_interleave(F)
    rep_agent = agent_idx.repeat_interleave(F)
    rep_feat = feature_indices.repeat(num_true)
    what_mask[rep_batch, rep_agent, rep_feat] = 1.0


def apply_slot_mask(what_mask, trigger, slot_visibility, slot_feat_idx):
    """
    what_mask: (B, N, D) tensor to modify in-place.
    trigger: (B, N) bool tensor.
    slot_visibility: (B, N, S) bool tensor.
    slot_feat_idx: (S, F) long tensor of feature indices for each slot.
    For each (b,n,s) where trigger[b,n] and slot_visibility[b,n,s] are True,
    set what_mask[b, n, slot_feat_idx[s, :]] = 1.0.
    """
    B, N, D = what_mask.shape
    S, F = slot_feat_idx.shape
    # Create 3D condition (B, N, S)
    condition_3d = trigger.unsqueeze(-1) & slot_visibility  # (B, N, S)
    valid = torch.nonzero(condition_3d)  # (K, 3) with columns [b, n, s]
    if valid.size(0) == 0:
        return
    b_idx = valid[:, 0]
    n_idx = valid[:, 1]
    s_idx = valid[:, 2]
    # Repeat for each feature
    b_rep = b_idx.repeat_interleave(F)
    n_rep = n_idx.repeat_interleave(F)
    # Feature indices for each (b,n,s) pair, then flatten
    feat_idx = slot_feat_idx[s_idx, :].reshape(-1)  # (K*F,)
    what_mask[b_rep, n_rep, feat_idx] = 1.0


def communication_who(o):
    B, N, D = o.shape
    is_stalker = o[..., 179] > 0.5   # own_unit_type_stalker
    is_zealot  = o[..., 180] > 0.5   # own_unit_type_zealot
    is_colossus = o[..., 181] > 0.5  # own_unit_type_colossus

    who = torch.zeros(B, N, N, device=o.device)

    # RULE R1: G1 (zealots) -> G2 or G3
    _add_group_links(who, is_zealot, is_stalker | is_colossus)
    # RULE R2: G2 (stalkers) -> G1 or G3
    _add_group_links(who, is_stalker, is_zealot | is_colossus)
    # RULE R3: G3 (colossi) -> G1 or G2
    _add_group_links(who, is_colossus, is_zealot | is_stalker)

    # Zero diagonal (no self-communication)
    diag = torch.diag_embed(who.diagonal(dim1=1, dim2=2))
    who = who - diag
    who.clamp_(0.0, 1.0)
    return who


def communication_when(o):
    B, N, D = o.shape
    is_stalker = o[..., 179] > 0.5
    is_zealot  = o[..., 180] > 0.5
    is_colossus = o[..., 181] > 0.5

    # Revised trigger: any enemy or any ally visible, not just slot 0.
    enemy_available_indices = [4, 13, 22, 31, 40, 49, 58, 67, 76, 85]
    ally_visible_indices   = [94, 103, 112, 121, 130, 139, 148, 157, 166]

    enemy_visible = torch.any(o[..., enemy_available_indices] > 0.5, dim=-1)  # (B, N)
    ally_visible  = torch.any(o[..., ally_visible_indices] > 0.5, dim=-1)    # (B, N)

    def sender_condition(cond):
        return cond.unsqueeze(1).expand(-1, N, -1)  # (B, N, N)

    when = torch.zeros(B, N, N, device=o.device)

    # RULE R1 (zealot, enemy)
    when = when + sender_condition(is_zealot & enemy_visible)
    # RULE R2 (stalker, enemy)
    when = when + sender_condition(is_stalker & enemy_visible)
    # RULE R3 (colossus, enemy)
    when = when + sender_condition(is_colossus & enemy_visible)
    # RULE R4 (zealot, ally)
    when = when + sender_condition(is_zealot & ally_visible)
    # RULE R5 (stalker, ally)
    when = when + sender_condition(is_stalker & ally_visible)
    # RULE R6 (colossus, ally)
    when = when + sender_condition(is_colossus & ally_visible)

    diag = torch.diag_embed(when.diagonal(dim1=1, dim2=2))
    when = when - diag
    when.clamp_(0.0, 1.0)
    return when


def communication_what(o):
    B, N, D = o.shape
    device = o.device

    # unit-type conditions
    is_stalker = o[..., 179] > 0.5
    is_zealot  = o[..., 180] > 0.5
    is_colossus = o[..., 181] > 0.5

    # Revised: any enemy/ally visible for the overall trigger
    enemy_avail_idx = torch.tensor([4, 13, 22, 31, 40, 49, 58, 67, 76, 85], device=device)
    ally_vis_idx    = torch.tensor([94, 103, 112, 121, 130, 139, 148, 157, 166], device=device)

    enemy_any = torch.any(o[..., enemy_avail_idx] > 0.5, dim=-1)  # (B, N)
    ally_any  = torch.any(o[..., ally_vis_idx] > 0.5, dim=-1)      # (B, N)

    # Feature block indices (skipping distance)
    offs = torch.tensor([0, 2, 3, 4, 5, 6, 7, 8], dtype=torch.long, device=device)
    n_enemy_slots = 10
    n_ally_slots = 9
    enemy_start = 4
    ally_start = 94

    # Vectorized construction of per-slot feature indices (no loops)
    enemy_base = enemy_start + torch.arange(n_enemy_slots, device=device) * 9
    enemy_slot_feat_idx = enemy_base[:, None] + offs[None, :]  # (10, 8)

    ally_base = ally_start + torch.arange(n_ally_slots, device=device) * 9
    ally_slot_feat_idx = ally_base[:, None] + offs[None, :]    # (9, 8)

    # Own position features
    own_pos = torch.tensor([177, 178], device=device)

    what_mask = torch.zeros(B, N, D, device=device)

    # Trigger conditions per rule
    c_zealot_enemy = is_zealot & enemy_any
    c_stalker_enemy = is_stalker & enemy_any
    c_colossus_enemy = is_colossus & enemy_any
    c_zealot_ally = is_zealot & ally_any
    c_stalker_ally = is_stalker & ally_any
    c_colossus_ally = is_colossus & ally_any

    # Own position for any triggered agent (union of all rules)
    any_trigger = c_zealot_enemy | c_stalker_enemy | c_colossus_enemy | \
                  c_zealot_ally | c_stalker_ally | c_colossus_ally
    _apply_what_mask(what_mask, any_trigger, own_pos)

    # Slot visibility tensors
    vis_enemy = o[..., enemy_avail_idx] > 0.5   # (B, N, 10)
    vis_ally  = o[..., ally_vis_idx] > 0.5       # (B, N, 9)

    # Enemy inventory for enemy rules
    apply_slot_mask(what_mask, c_zealot_enemy, vis_enemy, enemy_slot_feat_idx)
    apply_slot_mask(what_mask, c_stalker_enemy, vis_enemy, enemy_slot_feat_idx)
    apply_slot_mask(what_mask, c_colossus_enemy, vis_enemy, enemy_slot_feat_idx)

    # Ally inventory for ally rules
    apply_slot_mask(what_mask, c_zealot_ally, vis_ally, ally_slot_feat_idx)
    apply_slot_mask(what_mask, c_stalker_ally, vis_ally, ally_slot_feat_idx)
    apply_slot_mask(what_mask, c_colossus_ally, vis_ally, ally_slot_feat_idx)

    return what_mask


# The main communication function expected by the framework
def communication(o):
    who = communication_who(o)
    when = communication_when(o)
    what = communication_what(o)
    return who, when, what
