import torch

def message_design_instruction() -> str:
    """
    Accelerate consensus via two complementary communication rules:
    (1) A sender broadcasts the opinion of any agent it can see and with which it
        disagrees (R1 rules). This shares information about agents invisible to
        receivers, reducing uncertainty about the global majority.
    (2) A sender broadcasts its outgoing influence weight to any agent when that
        weight exceeds 0.5 (R2 rules). This allows receivers to identify
        influential peers, though point‑to‑point delivery is approximated by
        broadcasting due to the single‑message interface.
    The combined mask includes feature indices 0–9 for R1 and 20–29 for R2.
    If no rule fires, no communication occurs.
    """
    return (
        "Broadcast opinions of visible agent that disagree with the sender; "
        "broadcast high (>0.5) outgoing influence weights. "
        "Aims at faster majority alignment."
    )

def _compute_activation_and_mask(o: torch.Tensor):
    """
    Returns:
        active_s : [B, N] float, 1 if sender s triggers any rule
        what_mask: [B, N, D] float, ones at feature indices selected for s
    """
    B, N, D = o.shape
    # relevant slices
    opinions = o[:, :, 0:10]          # opinions all agents (0..9)
    visibility = o[:, :, 10:20]       # visibility mask (0..9)
    influence = o[:, :, 20:30]        # outgoing influence row (0..9)
    id_onehot = o[:, :, 32:42]        # one-hot agent id (indices 32..41)

    # sender's own id (0..9)
    s_id = torch.argmax(id_onehot, dim=-1)               # [B,N]
    # sender's own opinion (gather along opinion dimension)
    own_opinion = torch.gather(opinions, 2,
                               s_id.unsqueeze(-1))       # [B,N,1]

    # i indices [0..9] for broadcasting
    i_range = torch.arange(10, device=o.device).view(1, 1, 10)
    # s_id != i
    s_id_ne_i = s_id.unsqueeze(-1) != i_range            # [B,N,10]

    # ----- RULE R1_0 .. R1_9: broadcast opinion of visible disagreeing agent -----
    vis_ok = (visibility == 1)                           # [B,N,10]
    opinion_diff = (opinions != own_opinion)             # [B,N,10]
    R1_cond = vis_ok & s_id_ne_i & opinion_diff          # [B,N,10]

    # ----- RULE R2_0 .. R2_9: broadcast outgoing influence weight > 0.5 -----
    influence_high = (influence > 0.5)                   # [B,N,10]
    R2_cond = influence_high & s_id_ne_i                 # [B,N,10]

    # sender is active if any rule condition is true
    active_s = (R1_cond.any(dim=-1) | R2_cond.any(dim=-1)).float()   # [B,N]

    # build content mask (same shape as o)
    what_mask = torch.zeros(B, N, D, device=o.device)
    # R1 features: opinions at indices 0..9
    what_mask[:, :, :10]  = R1_cond.float()
    # R2 features: influence weights at indices 20..29
    what_mask[:, :, 20:30] = R2_cond.float()

    return active_s, what_mask


def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns [B, N, N] with 1 for all k != self, 0 on diagonal.
    (All rules use broadcast to all other agents.)
    """
    B, N, _ = o.shape
    off_diag = 1.0 - torch.eye(N, device=o.device)       # [N,N]
    return off_diag.unsqueeze(0).expand(B, -1, -1)       # [B,N,N]


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns [B, N, N] with 1 for (receiver, sender) if sender triggers any rule
    and receiver != sender.
    """
    active_s, _ = _compute_activation_and_mask(o)        # [B,N]
    B, N, _ = o.shape
    off_diag = 1.0 - torch.eye(N, device=o.device)       # [N,N]
    # active_s[b, s] replicated for all receivers r != s
    when = active_s.unsqueeze(-1) * off_diag.unsqueeze(0) # [B,N] * [1,N,N] -> [B,N,N]
    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns [B, N, D] mask with ones at opinion indices (0..9) for R1 triggers
    and influence indices (20..29) for R2 triggers; zero elsewhere.
    """
    _, what_mask = _compute_activation_and_mask(o)
    return what_mask