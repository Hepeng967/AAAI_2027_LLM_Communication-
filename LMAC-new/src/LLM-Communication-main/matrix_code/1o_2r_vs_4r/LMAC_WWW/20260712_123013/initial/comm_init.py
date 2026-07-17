import torch

# ------------------------------------------------------------------------------
# Helper: we rely on fixed agent indices per the scenario description.
# Agent 0 = Overseer (G1), Agent 1 = Roach, Agent 2 = Roach (G2)
# ------------------------------------------------------------------------------

def communication_who(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a binary who mask of shape [batch, n_agents, n_agents] where
    mask[b, r, s] = 1 if agent s sends to agent r. Diagonal is always zero.
    """
    batch, n_agents, _ = o.shape
    # We only support the 3-agent setup described in the policy.
    # Edges are static, determined by roles.
    who = o.new_zeros((batch, n_agents, n_agents))

    # RULE R1 & R2: Overseer (0) broadcasts to both Roaches (1,2).
    # Both rules share the same sender -> receiver pattern.
    who[:, 1, 0] = 1.0   # overseer -> roach1
    who[:, 2, 0] = 1.0   # overseer -> roach2

    # RULE R3: Roaches (1 and 2) send to the peer Roach (the other one).
    who[:, 2, 1] = 1.0   # roach1 -> roach2
    who[:, 1, 2] = 1.0   # roach2 -> roach1

    # Diagonal (self-communication) stays zero as per constraint.
    return who


def communication_when(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a when mask of shape [batch, n_agents, n_agents] where
    mask[b, r, s] = 1 if the sender's trigger condition is met.
    """
    batch, n_agents, _ = o.shape
    when = o.new_zeros((batch, n_agents, n_agents))

    # ---------- RULE R1 & R2 ----------
    # Condition: Overseer (agent 0) sees at least one enemy,
    # indicated by feature "enemy_0_available" (index 4) > 0.5.
    overseer_cond = (o[:, 0, 4] > 0.5).float()   # [batch]
    # Apply to edges from overseer to both roaches.
    when[:, 1, 0] = overseer_cond   # overseer -> roach1
    when[:, 2, 0] = overseer_cond   # overseer -> roach2

    # ---------- RULE R3 ----------
    # Condition: Sender Roach is alive, i.e. "own_health" (index 50) > 0.0.
    # This ensures the Roach sends its intention only while still active.
    roach1_cond = (o[:, 1, 50] > 0.0).float()   # roach1 alive
    roach2_cond = (o[:, 2, 50] > 0.0).float()   # roach2 alive

    when[:, 2, 1] = roach1_cond   # roach1 -> roach2
    when[:, 1, 2] = roach2_cond   # roach2 -> roach1

    return when


def communication_what(o: torch.Tensor) -> torch.Tensor:
    """
    Returns a what mask of shape [batch, n_agents, obs_dim] where
    mask[b, a, f] = 1 if agent a includes feature f in its message.
    """
    what_mask = torch.zeros_like(o)

    # ------------------------------------------------------------------
    # RULE R1 & R2 (Overseer, agent 0)
    #   R1: send enemy relative positions   -> indices [6,7,14,15,22,23,30,31]
    #   R2: send enemy health values       -> indices [8,16,24,32]
    # We combine both sets into the Overseer's mask.
    # (See feature index map for exact offsets.)
    pos_indices = [6, 7, 14, 15, 22, 23, 30, 31]   # R1
    hlth_indices = [8, 16, 24, 32]                 # R2

    what_mask[:, 0, pos_indices] = 1.0
    what_mask[:, 0, hlth_indices] = 1.0

    # ------------------------------------------------------------------
    # RULE R3 (Roaches, agents 1 and 2)
    #   The intended target index is not an observation feature;
    #   the policy expects the learning process to encode it in the
    #   dedicated communication channel. Therefore the what mask for
    #   Roaches is left empty (all zeros). The edge itself is still
    #   provided by who/when to allow the architecture to learn a
    #   suitable encoding if supported by the overall framework.
    #   No observation features are set for agents 1 or 2.

    return what_mask