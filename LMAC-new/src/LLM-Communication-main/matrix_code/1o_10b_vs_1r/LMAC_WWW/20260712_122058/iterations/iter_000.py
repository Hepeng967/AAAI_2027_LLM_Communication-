import torch


def message_design_instruction():
    """
    Returns a human-readable string describing the communication design for the scenario.
    This is required by the validation framework.
    """
    return (
        "LMAC Communication Policy for 1o_10b_vs_1r. "
        "Static rules: Overseer (agent 10) can send to all Banelings (0-9); "
        "Banelings can send to each other (no self-communication). "
        "Dynamic when: Overseer sends when it sees the enemy (enemy_0_available) "
        "or when a Baneling is visible (ally_0_visible). "
        "Banelings send when they see the Overseer (ally_9_visible). "
        "What: Overseer transmits enemy features and all Baneling ally features (except visibility). "
        "Banelings transmit the Overseer's ally features (distance, relative position, health, type)."
    )


def communication_who(o):
    """
    Returns static mask defining which sender-receiver pairs can communicate.
    shape: [batch, n_agents, n_agents] with 1 where communication is allowed,
    zero self-communication diagonal.
    """
    batch, n_agents, _ = o.shape
    who = torch.zeros(batch, n_agents, n_agents, device=o.device, dtype=torch.float32)

    # RULE R1 & R3: Overseer (agent 10) sends to all Banelings (0..9)
    who[:, 0:10, 10] = 1.0

    # RULE R2: any Baneling (0..9) can send to any other Baneling (0..9), except itself
    # G2 member-to-member communication
    baneling_mask = torch.ones(n_agents, n_agents, device=o.device) - torch.eye(n_agents, device=o.device)
    # restrict to first 10 agents (Banelings) as both sender and receiver
    who[:, :10, :10] = baneling_mask[:10, :10]

    return who


def communication_when(o):
    """
    Returns dynamic mask indicating when a sender is allowed to communicate,
    based on its local observation features.
    shape: [batch, receiver, sender], zero self-communication diagonal.
    """
    batch, n_agents, obs_dim = o.shape
    sender_active = torch.zeros(batch, n_agents, device=o.device)

    # RULE R1: Overseer (agent 10) sends when enemy_0_available == 1 (index 4)
    cond_r1 = (o[:, 10, 4] == 1.0)
    # RULE R3: Overseer sends when ally_0_visible == 1 (index 11)
    cond_r3 = (o[:, 10, 11] == 1.0)
    sender_active[:, 10] = (cond_r1 | cond_r3).float()

    # RULE R2: Banelings (0..9) send when ally_9_visible == 1 (index 74)
    # (ally_9 = overseer for Banelings)
    cond_r2 = (o[:, 0:10, 74] == 1.0)  # shape [batch, 10]
    sender_active[:, 0:10] = cond_r2.float()

    # Expand to [batch, receiver, sender]
    when = sender_active.unsqueeze(1).expand(-1, n_agents, -1)

    # Enforce zero self-communication diagonal
    diag_mask = 1.0 - torch.eye(n_agents, device=o.device)
    when = when * diag_mask

    return when


def communication_what(o):
    """
    Returns a content mask of the same shape as the observation,
    with 1's at feature indices that a sender should transmit.
    """
    batch, n_agents, obs_dim = o.shape
    what = torch.zeros(batch, n_agents, obs_dim, device=o.device, dtype=torch.float32)

    # RULE R1 + R3 combined what for Overseer (agent 10):
    # All enemy_0 features (5..10) and all Baneling ally features (non-visibility):
    # ally_0: 12-17, ally_1: 19-24, ally_2: 26-31, ally_3: 33-38,
    # ally_4: 40-45, ally_5: 47-52, ally_6: 54-59, ally_7: 61-66,
    # ally_8: 68-73, ally_9: 75-80
    idx_overseer = torch.tensor([
        5, 6, 7, 8, 9, 10,               # R1
        12, 13, 14, 15, 16, 17,           # ally_0
        19, 20, 21, 22, 23, 24,           # ally_1
        26, 27, 28, 29, 30, 31,           # ally_2
        33, 34, 35, 36, 37, 38,           # ally_3
        40, 41, 42, 43, 44, 45,           # ally_4
        47, 48, 49, 50, 51, 52,           # ally_5
        54, 55, 56, 57, 58, 59,           # ally_6
        61, 62, 63, 64, 65, 66,           # ally_7
        68, 69, 70, 71, 72, 73,           # ally_8
        75, 76, 77, 78, 79, 80            # ally_9 (skip index 74, the visibility flag)
    ], device=o.device)
    # Filter indices that are within the actual observation dimension
    valid_overseer = idx_overseer < obs_dim
    if valid_overseer.any():
        what[:, 10, idx_overseer[valid_overseer]] = 1.0

    # RULE R2 what: Banelings (0..9) send ally_9 (Overseer) features (75..80)
    idx_baneling = torch.arange(75, 81, device=o.device)
    valid_baneling = idx_baneling < obs_dim
    if valid_baneling.any():
        what[:, 0:10, idx_baneling[valid_baneling]] = 1.0

    return what
