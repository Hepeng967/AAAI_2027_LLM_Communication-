import torch

def communication_who(o):
    """
    Determines which sender-receiver pairs may communicate.
    Returns a binary mask of shape [batch, receiver, sender].
    Based on the policy, only the overseer (agent 0) sends to the two roaches (agents 1 and 2).
    The who mask is static and does not depend on the observation.
    """
    batch, n_agents, _ = o.shape
    who = torch.zeros(batch, n_agents, n_agents, dtype=torch.float32, device=o.device)
    # Overseer (sender index 0) communicates to roaches (receiver indices 1 and 2)
    who[:, 1, 0] = 1.0
    who[:, 2, 0] = 1.0
    return who


def communication_when(o):
    """
    Determines when a communication edge is active.
    Returns a binary mask of shape [batch, receiver, sender].
    Communication is triggered if at least one enemy reaper is visible to the overseer.
    """
    # Check visibility of each enemy for the overseer (agent 0)
    # RULE R1: enemy_0_available
    av0 = o[:, 0, 4] == 1.0
    # RULE R2: enemy_1_available
    av1 = o[:, 0, 11] == 1.0
    # RULE R3: enemy_2_available
    av2 = o[:, 0, 18] == 1.0
    # RULE R4: enemy_3_available
    av3 = o[:, 0, 25] == 1.0

    any_visible = av0 | av1 | av2 | av3

    batch, n_agents, _ = o.shape
    when = torch.zeros(batch, n_agents, n_agents, dtype=torch.float32, device=o.device)
    # Overseer sends to roaches when any enemy is visible
    when[:, 1, 0] = any_visible.float()
    when[:, 2, 0] = any_visible.float()
    return when


def communication_what(o):
    """
    Produces a mask of the same shape as the observation tensor,
    indicating which features the sender should transmit.
    Only the overseer (agent 0) transmits features of visible enemies.
    Features from multiple enemies are simply OR-ed together.
    """
    mask = torch.zeros_like(o)

    # Overseer is agent 0.
    # For each rule, if the corresponding enemy is visible, set the mask
    # for that enemy's relative position and health features.

    # RULE R1: enemy_0_available -> transmit enemy_0_rel_x, enemy_0_rel_y, enemy_0_health
    av0 = o[:, 0, 4] == 1.0
    mask[:, 0, 6] = av0.float()   # enemy_0_rel_x
    mask[:, 0, 7] = av0.float()   # enemy_0_rel_y
    mask[:, 0, 8] = av0.float()   # enemy_0_health

    # RULE R2: enemy_1_available -> transmit enemy_1_rel_x, enemy_1_rel_y, enemy_1_health
    av1 = o[:, 0, 11] == 1.0
    mask[:, 0, 13] = av1.float()  # enemy_1_rel_x
    mask[:, 0, 14] = av1.float()  # enemy_1_rel_y
    mask[:, 0, 15] = av1.float()  # enemy_1_health

    # RULE R3: enemy_2_available -> transmit enemy_2_rel_x, enemy_2_rel_y, enemy_2_health
    av2 = o[:, 0, 18] == 1.0
    mask[:, 0, 20] = av2.float()  # enemy_2_rel_x
    mask[:, 0, 21] = av2.float()  # enemy_2_rel_y
    mask[:, 0, 22] = av2.float()  # enemy_2_health

    # RULE R4: enemy_3_available -> transmit enemy_3_rel_x, enemy_3_rel_y, enemy_3_health
    av3 = o[:, 0, 25] == 1.0
    mask[:, 0, 27] = av3.float()  # enemy_3_rel_x
    mask[:, 0, 28] = av3.float()  # enemy_3_rel_y
    mask[:, 0, 29] = av3.float()  # enemy_3_health

    return mask