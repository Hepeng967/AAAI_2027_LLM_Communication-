import torch

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
    # Expand to (num_true * F,) indices
    rep_batch = batch_idx.repeat_interleave(F)
    rep_agent = agent_idx.repeat_interleave(F)
    rep_feat = feature_indices.repeat(num_true)
    what_mask[rep_batch, rep_agent, rep_feat] = 1.0

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
    # R4,R5,R6 use the same group links, already covered

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

    enemy_visible = o[..., 4] > 0.5     # enemy_0_available
    ally_visible = o[..., 94] > 0.5     # ally_slot_0_visible

    def sender_condition(cond):
        return cond.unsqueeze(1).expand(-1, N, -1)  # (B, N, N)

    when = torch.zeros(B, N, N, device=o.device)
    # RULE R1
    when = when + sender_condition(is_zealot & enemy_visible)
    # RULE R2
    when = when + sender_condition(is_stalker & enemy_visible)
    # RULE R3
    when = when + sender_condition(is_colossus & enemy_visible)
    # RULE R4
    when = when + sender_condition(is_zealot & ally_visible)
    # RULE R5
    when = when + sender_condition(is_stalker & ally_visible)
    # RULE R6
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

    enemy_cond = o[..., 4] > 0.5     # enemy visible
    ally_cond  = o[..., 94] > 0.5    # ally visible

    # Vectorized construction of enemy feature indices
    # 10 enemy slots, each block: [available, rel_x, rel_y, health, shield, type_stalker, type_zealot, type_colossus]
    # Offsets relative to block start: 0,2,3,4,5,6,7,8
    offs = torch.tensor([0, 2, 3, 4, 5, 6, 7, 8], dtype=torch.long, device=device)
    # Enemy blocks start at index 4, stride 9
    base_enemy = 4 + 9 * torch.arange(10, device=device)   # (10,)
    enemy_indices = (base_enemy.unsqueeze(1) + offs.unsqueeze(0)).reshape(-1)  # (80,)
    what_enemy = torch.cat([torch.tensor([177, 178], device=device), enemy_indices])  # (82,)

    # Ally slots: 9 slots, same offsets, start at 94
    base_ally = 94 + 9 * torch.arange(9, device=device)    # (9,)
    ally_indices = (base_ally.unsqueeze(1) + offs.unsqueeze(0)).reshape(-1)    # (72,)
    what_ally = torch.cat([torch.tensor([177, 178], device=device), ally_indices])    # (74,)

    what_mask = torch.zeros(B, N, D, device=device)

    # Apply each rule
    # RULE R1: zealot sees enemy -> share enemy inventory
    _apply_what_mask(what_mask, is_zealot & enemy_cond, what_enemy)
    # RULE R2: stalker sees enemy -> share enemy inventory
    _apply_what_mask(what_mask, is_stalker & enemy_cond, what_enemy)
    # RULE R3: colossus sees enemy -> share enemy inventory
    _apply_what_mask(what_mask, is_colossus & enemy_cond, what_enemy)
    # RULE R4: zealot sees ally -> share ally inventory
    _apply_what_mask(what_mask, is_zealot & ally_cond, what_ally)
    # RULE R5: stalker sees ally -> share ally inventory
    _apply_what_mask(what_mask, is_stalker & ally_cond, what_ally)
    # RULE R6: colossus sees ally -> share ally inventory
    _apply_what_mask(what_mask, is_colossus & ally_cond, what_ally)

    return what_mask