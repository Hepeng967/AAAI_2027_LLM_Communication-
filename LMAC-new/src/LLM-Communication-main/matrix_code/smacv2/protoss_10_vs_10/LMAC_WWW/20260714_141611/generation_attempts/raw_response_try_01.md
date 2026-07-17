```python
import torch

def _add_group_links(who, sender_mask, receiver_mask):
    """
    Add directed edges from any agent with sender_mask True to any agent with receiver_mask True.
    sender_mask:  (B, N) bool
    receiver_mask: (B, N) bool
    who:           (B, N, N) float tensor, modified in-place.
    """
    # (B, N, 1) * (B, 1, N) -> (B, N, N)
    who.add_(receiver_mask.unsqueeze(2) * sender_mask.unsqueeze(1))


def _apply_what_mask(what_mask, condition, feature_indices):
    """
    Set the given feature_indices to 1 for all senders where condition is True.
    what_mask:        (B, N, D) float tensor, modified in-place.
    condition:        (B, N) bool
    feature_indices:  (F,) long tensor
    """
    # Flatten condition to (B*N,)
    valid_flat = condition.reshape(-1).nonzero(as_tuple=False)  # (num_true, 1)
    if valid_flat.size(0) == 0:
        return
    # Convert flat indices back to batch and agent indices
    B, N = condition.shape
    batch_idx = valid_flat // N          # (num_true,)
    agent_idx = valid_flat % N           # (num_true,)
    # Expand to assign each feature index to each valid sender
    F = feature_indices.size(0)
    num_true = valid_flat.size(0)
    batch_expanded = batch_idx.unsqueeze(1).expand(-1, F).reshape(-1)
    agent_expanded = agent_idx.unsqueeze(1).expand(-1, F).reshape(-1)
    feat_expanded = feature_indices.unsqueeze(0).expand(num_true, F).reshape(-1)
    what_mask[batch_expanded, agent_expanded, feat_expanded] = 1.0


def communication_who(o):
    """
    Returns communication who matrix [B, N, N] with 1 for allowed sender-receiver links,
    0 for disallowed (including diagonal).
    """
    B, N, D = o.shape

    # unit type indicators
    is_stalker = o[..., 179] > 0.5
    is_zealot  = o[..., 180] > 0.5
    is_colossus = o[..., 181] > 0.5

    who = torch.zeros(B, N, N, device=o.device)

    # RULE R1: G1 (zealots) -> G2 or G3
    _add_group_links(who, is_zealot, is_stalker | is_colossus)
    # RULE R2: G2 (stalkers) -> G1 or G3
    _add_group_links(who, is_stalker, is_zealot | is_colossus)
    # RULE R3: G3 (colossi) -> G1 or G2
    _add_group_links(who, is_colossus, is_zealot | is_stalker)
    # R4, R5, R6 use the same group links (already added), so no further additions.

    # No self-communication
    who = who - who.diagonal(dim1=1, dim2=2).diag_embed()   # set diagonal to 0
    who.clamp_(0.0, 1.0)
    return who


def communication_when(o):
    """
    Returns communication when matrix [B, N, N] with 1 when the sender meets the
    triggering condition for its rule, 0 otherwise.
    """
    B, N, D = o.shape

    is_stalker = o[..., 179] > 0.5
    is_zealot  = o[..., 180] > 0.5
    is_colossus = o[..., 181] > 0.5

    enemy_visible = o[..., 4] > 0.5     # enemy_0_available
    ally_visible = o[..., 94] > 0.5     # ally_slot_0_visible

    # Helper to build per-sender condition and broadcast to [B, N, N]
    def sender_cond(cond):
        return cond.unsqueeze(1).expand(-1, N, -1)

    when = torch.zeros(B, N, N, device=o.device)

    # RULE R1: zealot sees enemy
    when = when + sender_cond(is_zealot & enemy_visible)
    # RULE R2: stalker sees enemy
    when = when + sender_cond(is_stalker & enemy_visible)
    # RULE R3: colossus sees enemy
    when = when + sender_cond(is_colossus & enemy_visible)
    # RULE R4: zealot sees ally
    when = when + sender_cond(is_zealot & ally_visible)
    # RULE R5: stalker sees ally
    when = when + sender_cond(is_stalker & ally_visible)
    # RULE R6: colossus sees ally
    when = when + sender_cond(is_colossus & ally_visible)

    # diagonal always 0
    when = when - when.diagonal(dim1=1, dim2=2).diag_embed()
    when.clamp_(0.0, 1.0)
    return when


def communication_what(o):
    """
    Returns content mask [B, N, D] with 1 at feature indices the sender should broadcast,
    based on matching rules. If a sender triggers multiple rules, the union of features
    is selected. No features are reordered or compressed.
    """
    B, N, D = o.shape
    device = o.device

    # unit types
    is_stalker = o[..., 179] > 0.5
    is_zealot  = o[..., 180] > 0.5
    is_colossus = o[..., 181] > 0.5

    # rule trigger conditions
    enemy_cond = o[..., 4] > 0.5     # enemy_0_available
    ally_cond  = o[..., 94] > 0.5    # ally_slot_0_visible

    # build per-rule feature indices (only once, as tensors)
    # enemy observation: for slot i = 0..9, indices = base, base+2, base+3, base+4, base+5, base+6, base+7, base+8
    enemy_feats = []
    for i in range(10):
        b = 4 + 9 * i
        enemy_feats.extend([b, b+2, b+3, b+4, b+5, b+6, b+7, b+8])
    what_enemy = torch.tensor([177, 178] + enemy_feats, dtype=torch.long, device=device)

    # ally observation: for slot i = 0..8, indices = base, base+2, base+3, base+4, base+5, base+6, base+7, base+8
    ally_feats = []
    for i in range(9):
        b = 94 + 9 * i
        ally_feats.extend([b, b+2, b+3, b+4, b+5, b+6, b+7, b+8])
    what_ally = torch.tensor([177, 178] + ally_feats, dtype=torch.long, device=device)

    what_mask = torch.zeros(B, N, D, device=device)

    # Apply each rule's what mask to the appropriate senders
    # RULE R1: zealot sees enemy
    _apply_what_mask(what_mask, is_zealot & enemy_cond, what_enemy)
    # RULE R2: stalker sees enemy
    _apply_what_mask(what_mask, is_stalker & enemy_cond, what_enemy)
    # RULE R3: colossus sees enemy
    _apply_what_mask(what_mask, is_colossus & enemy_cond, what_enemy)
    # RULE R4: zealot sees ally
    _apply_what_mask(what_mask, is_zealot & ally_cond, what_ally)
    # RULE R5: stalker sees ally
    _apply_what_mask(what_mask, is_stalker & ally_cond, what_ally)
    # RULE R6: colossus sees ally
    _apply_what_mask(what_mask, is_colossus & ally_cond, what_ally)

    return what_mask
```