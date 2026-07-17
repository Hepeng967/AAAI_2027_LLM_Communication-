```python
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
    enemy_available_indices = torch.tensor([4, 13, 22, 31, 40, 49, 58, 67, 76, 85], device=device)
    ally_visible_indices   = torch.tensor([94, 103, 112, 121, 130, 139, 148, 157, 166], device=device)

    enemy_any = torch.any(o[..., enemy_available_indices] > 0.5, dim=-1)  # (B, N)
    ally_any  = torch.any(o[..., ally_visible_indices] > 0.5, dim=-1)      # (B, N)

    # Precompute feature block indices for each enemy/ally slot (excluding distance)
    # Enemy block: size 9, indices: available(0), distance(1 skipped), rel_x(2), rel_y(3),
    # health(4), shield(5), type_stalker(6), type_zealot(7), type_colossus(8)
    offs = torch.tensor([0, 2, 3, 4, 5, 6, 7, 8], dtype=torch.long, device=device)
    n_enemy_slots = 10
    n_ally_slots = 9
    enemy_start = 4
    ally_start = 94

    enemy_slot_indices = []   # list of tensors, each shape (8,)
    for i in range(n_enemy_slots):
        base = enemy_start + i * 9
        inds = base + offs
        enemy_slot_indices.append(inds)

    ally_slot_indices = []
    for i in range(n_ally_slots):
        base = ally_start + i * 9
        inds = base + offs
        ally_slot_indices.append(inds)

    # Own position features (normalized x and y)
    own_pos = torch.tensor([177, 178], device=device)

    what_mask = torch.zeros(B, N, D, device=device)

    # Helper to apply per-slot features for a given trigger condition
    def add_slot_features(trigger_condition, slot_indices_list, slot_available_flags, is_enemy=True):
        """
        trigger_condition: (B, N) bool, agents that should share these entities.
        slot_indices_list: list of tensors (8,) for each slot.
        slot_available_flags: (B, N, num_slots) raw values (continuous) to threshold.
        """
        # Set own position once per triggered agent
        _apply_what_mask(what_mask, trigger_condition, own_pos)

        num_slots = len(slot_indices_list)
        for s in range(num_slots):
            if is_enemy:
                slot_visible = o[..., enemy_available_indices[s]] > 0.5
            else:
                slot_visible = o[..., ally_visible_indices[s]] > 0.5
            cond_slot = trigger_condition & slot_visible
            _apply_what_mask(what_mask, cond_slot, slot_indices_list[s])

    # Apply rules
    # RULE R1: zealot sees enemy -> share enemy inventory (only visible slots)
    add_slot_features(is_zealot & enemy_any, enemy_slot_indices, enemy_available_indices, is_enemy=True)
    # RULE R2: stalker sees enemy -> share enemy inventory
    add_slot_features(is_stalker & enemy_any, enemy_slot_indices, enemy_available_indices, is_enemy=True)
    # RULE R3: colossus sees enemy -> share enemy inventory
    add_slot_features(is_colossus & enemy_any, enemy_slot_indices, enemy_available_indices, is_enemy=True)
    # RULE R4: zealot sees ally -> share ally inventory (only visible slots)
    add_slot_features(is_zealot & ally_any, ally_slot_indices, ally_visible_indices, is_enemy=False)
    # RULE R5: stalker sees ally -> share ally inventory
    add_slot_features(is_stalker & ally_any, ally_slot_indices, ally_visible_indices, is_enemy=False)
    # RULE R6: colossus sees ally -> share ally inventory
    add_slot_features(is_colossus & ally_any, ally_slot_indices, ally_visible_indices, is_enemy=False)

    return what_mask


# The main communication function expected by the framework
def communication(o):
    who = communication_who(o)
    when = communication_when(o)
    what = communication_what(o)
    return who, when, what
```