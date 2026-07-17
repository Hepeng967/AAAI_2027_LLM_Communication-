import torch as th


def message_design_instruction():
    return (
        "Receiver-necessity-pruned teacher for 5z_vs_1ul. Offline DRC evidence "
        "showed health_and_attack_intent was largely receiver-redundant, so this "
        "candidate transmits only agent 0's Ultralisk visibility and relative "
        "position to agents 1..4."
    )


def _sender_message(o):
    sender = 0
    return o[:, sender, 4:7]


def communication_matrix(o):
    batch_size, n_agents, _ = o.shape
    matrix = th.zeros(batch_size, n_agents, n_agents, device=o.device, dtype=o.dtype)
    matrix[:, 1:, 0] = 1.0
    return matrix


def communication(o):
    batch_size, n_agents, obs_dim = o.shape
    assert n_agents == 5 and obs_dim == 48, "Expected 5 agents and 48-dim observations"
    sender = 0
    msg = _sender_message(o)
    matrix = communication_matrix(o)
    appended = matrix[:, :, sender].unsqueeze(-1) * msg.unsqueeze(1)
    return th.cat([o, appended], dim=-1)
