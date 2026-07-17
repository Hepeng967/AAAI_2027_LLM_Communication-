```python
import torch


def message_design_instruction():
    """
    Returns a textual instruction describing the communication policy.
    Required by LMAC validation.
    """
    return (
        "Overseer-to-roach communication policy for 1o_2r_vs_4r.\n"
        "The overseer (agent 0) sends information about all currently visible enemies "
        "(enemy presence, distance, relative position, health, type) to both roaches "
        "(agents 1 and 2) whenever at least one enemy is detected. "
        "Communication is static (always allowed from overseer to roaches)."
    )


def communication_who(o):
    """
    Returns a [batch, n_agents, n_agents] binary mask indicating allowed sender→receiver edges.
    Overseer (agent 0) is the permanent sender; roaches (agent 1 and agent 2) are the receivers.
    """
    batch, n_agents, obs_dim = o.shape
    who = torch.zeros(batch, n_agents, n_agents, device=o.device, dtype=torch.float32)
    # Static sender: agent 0 -> receivers: agent 1, agent 2
    if n_agents > 1:
        who[:, 1, 0] = 1.0  # RULE R1, R2, R3, R4: agent 0 to agent 1
    if n_agents > 2:
        who[:, 2, 0] = 1.0  # RULE R1, R2, R3, R4: agent 0 to agent 2
    return who


def communication_when(o):
    """
    Returns a [batch, n_agents, n_agents] binary mask; 1 if a message should be sent.
    Sending edge (0→1) and (0→2) is activated when at least one enemy is visible to the Overseer.
    """
    batch, n_agents, obs_dim = o.shape
    # Per-enemy availability checks (feature indices 4, 12, 20, 28)
    e0_avail = o[:, 0, 4] > 0.5   # R1: enemy_0_available
    e1_avail = o[:, 0, 12] > 0.5  # R2: enemy_1_available
    e2_avail = o[:, 0, 20] > 0.5  # R3: enemy_2_available
    e3_avail = o[:, 0, 28] > 0.5  # R4: enemy_3_available

    any_avail = e0_avail | e1_avail | e2_avail | e3_avail  # [batch] boolean

    when = torch.zeros(batch, n_agents, n_agents, device=o.device, dtype=torch.float32)
    if n_agents > 1:
        when[:, 1, 0] = any_avail.float()  # R1-R4 sender to agent 1
    if n_agents > 2:
        when[:, 2, 0] = any_avail.float()  # R1-R4 sender to agent 2
    return when


def communication_what(o):
    """
    Returns an observation-aligned content mask [batch, n_agents, obs_dim].
    For agent 0 (Overseer) it selects the features of each visible enemy.
    """
    batch, n_agents, obs_dim = o.shape
    what = torch.zeros(batch, n_agents, obs_dim, device=o.device, dtype=torch.float32)

    # Helper: safely assign a contiguous block of indices, respecting obs_dim
    def assign_block(agent_idx, start, end, flag):
        if start >= obs_dim:
            return
        end_clipped = min(end, obs_dim)
        if end_clipped <= start:
            return
        what[:, agent_idx, start:end_clipped] = flag.unsqueeze(1).expand(batch, end_clipped - start).float()

    # RULE R1: enemy_0 features (indices 5..10) when enemy_0_available (index 4) > 0.5
    e0_avail = o[:, 0, 4] > 0.5
    assign_block(0, 5, 11, e0_avail)

    # RULE R2: enemy_1 features (indices 13..18) when enemy_1_available (index 12) > 0.5
    e1_avail = o[:, 0, 12] > 0.5
    assign_block(0, 13, 19, e1_avail)

    # RULE R3: enemy_2 features (indices 21..26) when enemy_2_available (index 20) > 0.5
    e2_avail = o[:, 0, 20] > 0.5
    assign_block(0, 21, 27, e2_avail)

    # RULE R4: enemy_3 features (indices 29..34) when enemy_3_available (index 28) > 0.5
    e3_avail = o[:, 0, 28] > 0.5
    assign_block(0, 29, 35, e3_avail)

    return what
```