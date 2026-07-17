import torch as th


def message_design_instruction():
    return (
        "Masked task-fact anchor teacher for 1o_2r_vs_4r. Agent 0 is the only "
        "certified sender. It sends own health and the first observed enemy's "
        "relative position/health to agents 1 and 2. Unlike the dense baseline, "
        "there is no all-to-all broadcast and the appended message is exactly "
        "masked by communication_matrix."
    )


def _sender_message(o):
    sender = 0
    own_health = o[:, sender, 50:51]
    enemy_rel_health = o[:, sender, 6:9]
    return th.cat([own_health, enemy_rel_health], dim=-1)


def communication_matrix(o):
    batch_size, n_agents, _ = o.shape
    device = o.device
    dtype = o.dtype
    matrix = th.zeros(batch_size, n_agents, n_agents, device=device, dtype=dtype)
    matrix[:, 1:, 0] = 1.0
    return matrix


def communication(o):
    batch_size, n_agents, obs_dim = o.shape
    assert n_agents == 3 and obs_dim == 66, "Expected 3 agents and 66-dim observations"

    sender = 0
    msg_dim = 4
    matrix = communication_matrix(o)
    sender_msg = _sender_message(o)
    appended = th.zeros(batch_size, n_agents, msg_dim, device=o.device, dtype=o.dtype)
    active = matrix[:, :, sender].unsqueeze(-1)
    appended = appended + active * sender_msg.unsqueeze(1)
    return th.cat([o, appended], dim=-1)
