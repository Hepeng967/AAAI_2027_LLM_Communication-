import torch as th


def message_design_instruction():
    return (
        "Receiver-necessity-pruned teacher for 1o_2r_vs_4r. Offline DRC evidence "
        "showed ally_health was receiver-redundant, so this candidate transmits "
        "only the receiver-necessary enemy relative position and health observed "
        "by agent 0 to agents 1 and 2."
    )


def _sender_message(o):
    sender = 0
    return o[:, sender, 6:9]


def communication_matrix(o):
    batch_size, n_agents, _ = o.shape
    matrix = th.zeros(batch_size, n_agents, n_agents, device=o.device, dtype=o.dtype)
    matrix[:, 1:, 0] = 1.0
    return matrix


def communication(o):
    batch_size, n_agents, obs_dim = o.shape
    assert n_agents == 3 and obs_dim == 66, "Expected 3 agents and 66-dim observations"
    sender = 0
    msg = _sender_message(o)
    matrix = communication_matrix(o)
    appended = matrix[:, :, sender].unsqueeze(-1) * msg.unsqueeze(1)
    return th.cat([o, appended], dim=-1)
