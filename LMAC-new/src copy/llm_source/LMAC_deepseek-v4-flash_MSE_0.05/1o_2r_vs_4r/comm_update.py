import torch as th

def message_design_instruction():
    """
    Returns a string explaining how the complementary protocol aids
    global state reconstruction using the newly added critical dimensions.
    """
    return (
        "This complementary protocol adds essential behavioral and contextual information "
        "missing from the previous broadcast. By sharing movement possibilities (can-move flags) "
        "and the last one‑hot action, each agent provides cues about its current intent and possible "
        "future displacement, which helps others infer changes in absolute position over time. "
        "Including relative positions and health of other allies (two per sender) enables receivers "
        "to triangulate the sender's absolute location when combined with their own knowledge of "
        "that ally's position. Adding the enemy visibility (attackability) flags prevents the receiver "
        "from interpreting zero‑filled enemy slots (unseen) as valid positional data, thereby avoiding "
        "misleading updates that degraded Overseer coordinate prediction. Finally, broadcasting the "
        "sender’s own unit type (Roach or Overseer) allows receivers to adapt their interpretation of "
        "the message – for instance, trusting the Overseer’s enemy coordinates more heavily while "
        "treating Roach reports with caution. Together, these new fields fill the identified knowledge "
        "gaps and should improve absolute coordinate recovery for all agents."
    )


def communication(o):
    """
    Input: o (torch.Tensor), shape (batch, agents, 66)
    Output: enhanced_obs (torch.Tensor), shape (batch, agents, 66 + 78)
            where 78 = (old_msg_len + new_msg_len) * (N-1) = (13+26)*2 = 78.
    """
    B, N, _ = o.shape  # N = 3 agents
    device = o.device

    # ------------------------------------------------------------------
    # 1. Compute OLD message (same as previous protocol)
    #    Own health (1) + for each enemy: health, relX, relY (4*3=12) => total 13
    # ------------------------------------------------------------------
    own_health = o[..., 50:51]  # (B, N, 1)

    enemy_feats_old = []
    for j in range(4):
        start = 6 + j * 8
        health = o[..., start + 2:start + 3]  # health index = start+2
        relX   = o[..., start:start + 1]      # relX index = start
        relY   = o[..., start + 1:start + 2]  # relY index = start+1
        enemy_feats_old.extend([health, relX, relY])
    old_msg = th.cat([own_health] + enemy_feats_old, dim=-1)  # (B, N, 13)

    # ------------------------------------------------------------------
    # 2. Compute NEW message (complementary fields)
    #    - movement flags (4): indices 0..3
    #    - last action one-hot (10): indices 53..62
    #    - other ally 0: relX (38), relY (39), health (40)
    #    - other ally 1: relX (45), relY (46), health (47)
    #    - enemy visibility flags (4): indices 4,12,20,28
    #    - own unit type (2): indices 51,52
    #    Total: 4+10+6+4+2 = 26
    # ------------------------------------------------------------------
    move_flags = o[..., 0:4]          # (B, N, 4)
    last_action = o[..., 53:63]       # (B, N, 10)

    ally0 = o[..., [38, 39, 40]]      # (B, N, 3)  # relX, relY, health
    ally1 = o[..., [45, 46, 47]]      # (B, N, 3)
    ally_info = th.cat([ally0, ally1], dim=-1)  # (B, N, 6)

    enemy_visible = o[..., [4, 12, 20, 28]]   # (B, N, 4)

    own_unit_type = o[..., 51:53]     # (B, N, 2)   # bit0=Roach, bit1=Overseer

    new_msg = th.cat([move_flags, last_action, ally_info, enemy_visible, own_unit_type],
                     dim=-1)  # (B, N, 26)

    # Combine old and new messages into a single per-agent message
    msg_per_agent = th.cat([old_msg, new_msg], dim=-1)  # (B, N, 39)

    # ------------------------------------------------------------------
    # 3. For each agent, append messages from the other two agents
    # ------------------------------------------------------------------
    enhanced_list = []
    for i in range(N):
        # Messages from agents j != i: shape (B, 2, 39) -> flatten to (B, 78)
        other_msgs = msg_per_agent[:, [j for j in range(N) if j != i], :]  # (B, 2, 39)
        received = other_msgs.view(B, -1)  # (B, 78)
        enhanced_obs_i = th.cat([o[:, i, :], received], dim=-1)  # (B, 66+78)
        enhanced_list.append(enhanced_obs_i)

    enhanced_obs = th.stack(enhanced_list, dim=1)  # (B, N, 144)
    return enhanced_obs
