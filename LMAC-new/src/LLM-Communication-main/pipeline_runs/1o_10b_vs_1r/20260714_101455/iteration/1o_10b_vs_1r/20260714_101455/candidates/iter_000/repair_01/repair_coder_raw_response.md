```python
import torch

def message_design_instruction():
    """
    Returns a human-readable instruction describing the communication policy design.
    """
    return (
        "This communication policy coordinates an overseer (agent 10) and 10 banelings (agents 0-9) "
        "on the 1o_10b_vs_1r map. The overseer broadcasts enemy location (distance, relative x, y) "
        "to all banelings only when an enemy (roach) is detected (enemy_0_available == 1). "
        "Each baneling relays its own relative position (ally_0_rel_x, ally_0_rel_y) to the overseer "
        "only when it sees at least one other ally (max(ally_i_visible) > 0.5), providing the overseer "
        "with positional awareness of the swarm."
    )


def communication_who(o):
    """
    Returns who can communicate: static edges based on agent roles.
    Shape: [batch, n_agents, n_agents] in [0,1].
    """
    batch, n_agents, obs_dim = o.shape
    # Build static connectivity matrix (receivers x senders)
    who = torch.zeros((n_agents, n_agents), device=o.device, dtype=torch.float32)

    # RULE R1: Overseer (agent 10) broadcasts to Banelings (0-9)
    who[0:10, 10] = 1.0

    # RULE R2: Banelings (0-9) relay to Overseer (10)
    who[10, 0:10] = 1.0

    # Expand to match batch dimension
    who = who.unsqueeze(0).expand(batch, -1, -1)
    # Self-communication is already zero by construction
    return who


def communication_when(o):
    """
    Returns when each link is active, based on sender observation.
    Shape: [batch, n_agents, n_agents] in [0,1].
    """
    batch, n_agents, obs_dim = o.shape
    when = torch.zeros(batch, n_agents, n_agents, device=o.device)

    # RULE R1: Overseer sends when it sees the Roach (enemy_0_available == 1)
    overseer_idx = 10
    enemy_avail = o[:, overseer_idx, 4]  # index 4 = enemy_0_available
    r1_condition = (enemy_avail == 1.0).float()
    when[:, 0:10, overseer_idx] = r1_condition.unsqueeze(1).expand(-1, 10)

    # RULE R2: Baneling sends when it sees at least one ally (max ally_i_visible > 0.5)
    # ally_0..ally_9 visible indices: 11,18,25,32,39,46,53,60,67,74
    ally_visible_indices = [11, 18, 25, 32, 39, 46, 53, 60, 67, 74]
    baneling_visible = o[:, 0:10, ally_visible_indices]  # [batch, 10, 10]
    max_visible, _ = baneling_visible.max(dim=-1)        # [batch, 10]
    r2_condition = (max_visible > 0.5).float()
    when[:, overseer_idx, 0:10] = r2_condition

    # Ensure no self-communication
    diag = torch.arange(n_agents, device=o.device)
    when[:, diag, diag] = 0.0

    return when


def communication_what(o):
    """
    Returns a mask selecting which features each sender would transmit.
    Shape: same as o, [batch, n_agents, obs_dim] in [0,1].
    """
    batch, n_agents, obs_dim = o.shape
    mask = torch.zeros_like(o)

    # RULE R1: Overseer sends enemy_0_distance, enemy_0_rel_x, enemy_0_rel_y
    overseer_idx = 10
    mask[:, overseer_idx, [5, 6, 7]] = 1.0  # indices 5,6,7

    # RULE R2: Banelings send ally_0_rel_x, ally_0_rel_y
    mask[:, 0:10, [13, 14]] = 1.0            # indices 13,14

    return mask
```