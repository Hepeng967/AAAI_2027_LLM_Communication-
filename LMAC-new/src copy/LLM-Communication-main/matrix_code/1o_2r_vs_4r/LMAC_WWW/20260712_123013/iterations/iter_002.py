import torch

# ------------------------------------------------------------------------------
# Teacher communication policy for 1o_2r_vs_4r
# Agents: agent 0 = Overseer (G1), agent 1 = Roach (G2), agent 2 = Roach (G3)
# The observation is 66-dimensional, aligned to the feature_index provided in
# the rollout summary.
# ------------------------------------------------------------------------------

def message_design_instruction() -> str:
    """
    Returns a string describing the communication design for logging / inspection.
    """
    return (
        "R1 Overseer sends enemy relative positions to all roaches when any enemy is visible. "
        "R2 Overseer sends enemy health values to all roaches when any enemy is visible. "
        "R3 Roaches send their intended target (last attack action) and health status to the other roach while they are alive."
    )


def communication(o: torch.Tensor):
    """
    Convenience wrapper that returns all three masks at once.
    The evaluation framework expects this function to exist.
    """
    return communication_who(o), communication_when(o), communication_what(o)


def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a binary who mask of shape [batch, n_agents, n_agents] where
    mask[b, r, s] = 1 if agent s sends to agent r. Diagonal is always zero.
    """
    batch, n_agents, _ = o.shape
    who = o.new_zeros((batch, n_agents, n_agents))

    # R1 & R2: Overseer (0) broadcasts to both roaches (1, 2)
    who[:, 1, 0] = 1.0
    who[:, 2, 0] = 1.0

    # R3: Roaches send to the other roach
    who[:, 2, 1] = 1.0   # roach 1 -> roach 2
    who[:, 1, 2] = 1.0   # roach 2 -> roach 1

    return who


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a when mask of shape [batch, n_agents, n_agents] where
    mask[b, r, s] = 1 if the sender's trigger condition is met.
    """
    batch, n_agents, _ = o.shape
    when = o.new_zeros((batch, n_agents, n_agents))

    # ---------- R1 & R2 ----------
    # Overseer sends if any enemy is visible (enemy_*_available features)
    overseer_cond = (
        (o[:, 0, 4] > 0.5) |   # enemy_0_available
        (o[:, 0, 11] > 0.5) |  # enemy_1_available
        (o[:, 0, 18] > 0.5) |  # enemy_2_available
        (o[:, 0, 25] > 0.5)    # enemy_3_available
    ).float()
    when[:, 1, 0] = overseer_cond
    when[:, 2, 0] = overseer_cond

    # ---------- R3 ----------
    # A roach sends while it is alive (own_health > 0)
    roach1_alive = (o[:, 1, 46] > 0.0).float()
    roach2_alive = (o[:, 2, 46] > 0.0).float()

    when[:, 2, 1] = roach1_alive   # roach 1 -> roach 2
    when[:, 1, 2] = roach2_alive   # roach 2 -> roach 1

    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a what mask of shape [batch, n_agents, obs_dim] where
    mask[b, a, f] = 1 if agent a includes feature f in its message.
    """
    what_mask = torch.zeros_like(o)

    # ---------- R1 & R2 (Overseer, agent 0) ----------
    # Positions of all four enemies (rel_x, rel_y)
    pos_indices = [
        6, 7,    # enemy_0
        13, 14,  # enemy_1
        20, 21,  # enemy_2
        27, 28,  # enemy_3
    ]
    # Health of all four enemies
    health_indices = [
        8,       # enemy_0
        15,      # enemy_1
        22,      # enemy_2
        29,      # enemy_3
    ]
    what_mask[:, 0, pos_indices] = 1.0
    what_mask[:, 0, health_indices] = 1.0

    # ---------- R3 (Roaches, agents 1 and 2) ----------
    # Send own health (survivability) and the last action (intended target)
    # previous_action features: indices 53–62 encode the one‑hot of the last
    # action, where actions 4–9 correspond to attacks on specific enemies.
    what_mask[:, [1, 2], 46] = 1.0                # own_health
    what_mask[:, [1, 2], 53:63] = 1.0             # previous_action_0 … previous_action_9

    return what_mask
