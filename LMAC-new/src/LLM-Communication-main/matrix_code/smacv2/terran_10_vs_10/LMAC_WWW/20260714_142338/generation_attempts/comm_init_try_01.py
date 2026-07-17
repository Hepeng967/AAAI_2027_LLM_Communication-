import torch

def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Return a binary matrix [batch, n_agents, n_agents] where entry [:, r, s] == 1 means
    sender s is allowed to communicate to receiver r (r != s).  In this policy all agents
    (G1: medivac, G2: marine/marauder) are eligible.
    """
    batch, n_agents, obs_dim = o.shape
    # G1: own_unit_type_medivac (index 161) > 0.5
    G1 = (o[:, :, 161] > 0.5)
    # G2: own_unit_type_marine (159) or marauder (160) > 0.5
    G2 = (o[:, :, 159] > 0.5) | (o[:, :, 160] > 0.5)
    group = G1 | G2   # all alive agents belong to at least one group

    who = group.unsqueeze(1).expand(-1, n_agents, -1).clone()  # [batch, recv, send]
    who.fill_diagonal_(False)                                   # no self‑communication
    return who.float()


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Return a binary matrix [batch, n_agents, n_agents] where entry [:, r, s] == 1 means
    sender s triggers a message to receiver r at this time step.
    """
    batch, n_agents, obs_dim = o.shape
    G1 = (o[:, :, 161] > 0.5)
    G2 = (o[:, :, 159] > 0.5) | (o[:, :, 160] > 0.5)

    when = torch.zeros(batch, n_agents, n_agents, dtype=torch.bool, device=o.device)

    # --- R1_enemy0_G1 … R1_enemy9_G2: visible enemy broadcast ------------------
    for i in range(10):
        avail_idx = 4 + i * 8          # enemy_i_available
        # G1 rule
        cond = G1 & (o[:, :, avail_idx] > 0.5)
        when |= cond.unsqueeze(1).expand(-1, n_agents, -1)
        # G2 rule
        cond = G2 & (o[:, :, avail_idx] > 0.5)
        when |= cond.unsqueeze(1).expand(-1, n_agents, -1)

    # --- R2_ally0_G1 … R2_ally8_G2: visible ally broadcast ---------------------
    for j in range(9):
        avail_idx = 84 + j * 8         # ally_slot_j_visible
        cond = G1 & (o[:, :, avail_idx] > 0.5)
        when |= cond.unsqueeze(1).expand(-1, n_agents, -1)
        cond = G2 & (o[:, :, avail_idx] > 0.5)
        when |= cond.unsqueeze(1).expand(-1, n_agents, -1)

    # --- R3_medivac_always ----------------------------------------------------
    cond = G1   # own_health >= 0.0 always true alive
    when |= cond.unsqueeze(1).expand(-1, n_agents, -1)

    # --- R3_dps_injured -------------------------------------------------------
    cond = G2 & (o[:, :, 156] < 0.5)   # own_health < 0.5
    when |= cond.unsqueeze(1).expand(-1, n_agents, -1)

    # --- R4_G1_actions --------------------------------------------------------
    cond = G1   # own_health >= 0.0 always true
    when |= cond.unsqueeze(1).expand(-1, n_agents, -1)

    # --- R4_G2_actions --------------------------------------------------------
    cond = G2   # own_health >= 0.0 always true
    when |= cond.unsqueeze(1).expand(-1, n_agents, -1)

    when.fill_diagonal_(False)          # no self‑communication
    return when.float()


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Return a binary mask of shape [batch, n_agents, obs_dim] where a 1 means the
    feature is included in the message sent by the corresponding agent.
    """
    batch, n_agents, obs_dim = o.shape
    G1 = (o[:, :, 161] > 0.5)
    G2 = (o[:, :, 159] > 0.5) | (o[:, :, 160] > 0.5)

    what = torch.zeros_like(o, dtype=torch.bool)

    # --- R1_enemy*_G1 / R1_enemy*_G2: visible enemy data -----------------------
    for i in range(10):
        base = 4 + i * 8
        avail_idx = base
        # distance, rel_x, rel_y, health, marine, marauder, medivac
        share_idxs = [base+1, base+2, base+3, base+4, base+5, base+6, base+7]
        cond_g1 = G1 & (o[:, :, avail_idx] > 0.5)
        cond_g2 = G2 & (o[:, :, avail_idx] > 0.5)
        for idx in share_idxs:
            what[:, :, idx] |= cond_g1
            what[:, :, idx] |= cond_g2

    # --- R2_ally*_G1 / R2_ally*_G2: visible ally data -------------------------
    for j in range(9):
        base = 84 + j * 8
        avail_idx = base
        share_idxs = [base+1, base+2, base+3, base+4, base+5, base+6, base+7]
        cond_g1 = G1 & (o[:, :, avail_idx] > 0.5)
        cond_g2 = G2 & (o[:, :, avail_idx] > 0.5)
        for idx in share_idxs:
            what[:, :, idx] |= cond_g1
            what[:, :, idx] |= cond_g2

    # --- R3_medivac_always ----------------------------------------------------
    cond = G1
    what[:, :, 156] |= cond   # own_health
    what[:, :, 157] |= cond   # own_normalized_x
    what[:, :, 158] |= cond   # own_normalized_y
    what[:, :, 161] |= cond   # own_unit_type_medivac

    # --- R3_dps_injured -------------------------------------------------------
    cond = G2 & (o[:, :, 156] < 0.5)
    what[:, :, 156] |= cond   # own_health
    what[:, :, 157] |= cond   # own_normalized_x
    what[:, :, 158] |= cond   # own_normalized_y
    what[:, :, 159] |= cond   # own_unit_type_marine
    what[:, :, 160] |= cond   # own_unit_type_marauder

    # --- R4_G1_actions --------------------------------------------------------
    cond = G1
    # previous_action_0 … previous_action_15  (indices 162–177)
    what[:, :, 162:178] |= cond.unsqueeze(-1)

    # --- R4_G2_actions --------------------------------------------------------
    cond = G2
    what[:, :, 162:178] |= cond.unsqueeze(-1)

    return what.float()