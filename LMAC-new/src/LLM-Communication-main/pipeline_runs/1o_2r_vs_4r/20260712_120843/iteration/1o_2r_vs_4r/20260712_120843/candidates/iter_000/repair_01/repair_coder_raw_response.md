```python
import torch


def message_design_instruction():
    """
    Teacher communication policy for map 1o_2r_vs_4r.

    Agent roles:
    - Agent 0: Overseer (central decision-maker)
    - Agents 1, 2: Roaches (executors)

    Communication topology:
    - Who: Overseer transmits to both Roaches. No other communication edges.

    Transmission trigger:
    - When: the Overseer sends a message whenever any enemy is observed.
      Observed is defined as the enemy's "available" flag being > 0.5.

    Message content (What):
    - For each enemy that is observed, the following features are transmitted,
      in this order per enemy slot:
        * availability flag (1 scalar)
        * relative x position
        * relative y position
        * health
        * type one-hot (2 scalars)
      The distance feature is NOT transmitted.
    - The feature mask selects the following raw-observation indices:
        Enemy 0: indices [4, 6, 7, 8, 9, 10]
        Enemy 1: indices [11,13,14,15,16,17]
        Enemy 2: indices [18,20,21,22,23,24]
        Enemy 3: indices [25,27,28,29,30,31]
      Unavailable enemy slots have all features set to zero.
    """
    return """
    Teacher communication policy for map 1o_2r_vs_4r.
    Agent roles: Agent 0 Overseer, Agents 1,2 Roaches.
    Who: Overseer -> Roach1, Roach2.
    When: any enemy available flag > 0.5.
    What: for each available enemy slot, send [availability, rel_x, rel_y, health, type_0, type_1] (distance omitted).
    Feature indices: Enemy0:[4,6,7,8,9,10]; Enemy1:[11,13,14,15,16,17]; Enemy2:[18,20,21,22,23,24]; Enemy3:[25,27,28,29,30,31].
    """.strip()


def communication_who(o):
    """
    Overseer (agent 0) sends to Roaches (agents 1 and 2).
    """
    batch, n_agents = o.shape[0], o.shape[1]
    device = o.device
    who = torch.zeros(batch, n_agents, n_agents, device=device)
    who[:, 1, 0] = 1.0   # Overseer -> Roach1
    who[:, 2, 0] = 1.0   # Overseer -> Roach2
    return who


def communication_when(o):
    """
    Send when any enemy is available.
    """
    batch, n_agents = o.shape[0], o.shape[1]
    device = o.device

    # Enemy availability flags (corrected indices)
    e0_avail = o[:, 0, 4] > 0.5   # Enemy 0
    e1_avail = o[:, 0, 11] > 0.5  # Enemy 1
    e2_avail = o[:, 0, 18] > 0.5  # Enemy 2
    e3_avail = o[:, 0, 25] > 0.5  # Enemy 3

    any_avail = e0_avail | e1_avail | e2_avail | e3_avail

    when = torch.zeros(batch, n_agents, n_agents, device=device)
    when[:, 1, 0] = any_avail.float()
    when[:, 2, 0] = any_avail.float()
    return when


def communication_what(o):
    """
    Mask out all features except the selected ones for visible enemies.
    """
    batch, n_agents, obs_dim = o.shape
    device = o.device
    mask = torch.zeros(batch, n_agents, obs_dim, device=device)

    mask_agent0 = torch.zeros(batch, obs_dim, device=device)

    # Enemy 0: indices [4,6,7,8,9,10]
    cond0 = o[:, 0, 4] > 0.5
    mask_agent0[:, [4,6,7,8,9,10]] = cond0.unsqueeze(1).float().expand(-1, 6)

    # Enemy 1: indices [11,13,14,15,16,17]
    cond1 = o[:, 0, 11] > 0.5
    mask_agent0[:, [11,13,14,15,16,17]] = cond1.unsqueeze(1).float().expand(-1, 6)

    # Enemy 2: indices [18,20,21,22,23,24]
    cond2 = o[:, 0, 18] > 0.5
    mask_agent0[:, [18,20,21,22,23,24]] = cond2.unsqueeze(1).float().expand(-1, 6)

    # Enemy 3: indices [25,27,28,29,30,31]
    cond3 = o[:, 0, 25] > 0.5
    mask_agent0[:, [25,27,28,29,30,31]] = cond3.unsqueeze(1).float().expand(-1, 6)

    mask[:, 0, :] = mask_agent0
    return mask
```