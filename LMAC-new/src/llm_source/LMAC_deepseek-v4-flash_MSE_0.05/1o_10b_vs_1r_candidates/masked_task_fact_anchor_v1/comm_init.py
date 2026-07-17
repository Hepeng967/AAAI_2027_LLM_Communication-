import torch as th


def message_design_instruction():
    return (
        "Masked task-fact anchor teacher for 1o_10b_vs_1r. The Overseer is the "
        "only sender. It sends enemy position and enemy/intent action context to "
        "Baneling receivers. The appended message is masked by the same "
        "communication_matrix used by certification, so inactive or self edges "
        "carry zero content."
    )


def _sender_message(o):
    overseer_idx = o.shape[1] - 1
    enemy_rel = o[:, overseer_idx, 6:8]
    last_action = o[:, overseer_idx, 85:92]
    return th.cat([enemy_rel, last_action], dim=-1)


def communication_matrix(o):
    batch_size, n_agents, _ = o.shape
    device = o.device
    dtype = o.dtype
    matrix = th.zeros(batch_size, n_agents, n_agents, device=device, dtype=dtype)
    overseer_idx = n_agents - 1
    receivers = [idx for idx in range(n_agents) if idx != overseer_idx]
    matrix[:, receivers, overseer_idx] = 1.0
    return matrix


def communication(o):
    batch_size, n_agents, obs_dim = o.shape
    assert n_agents == 11 and obs_dim == 103, "Expected 11 agents and 103-dim observations"

    sender_idx = n_agents - 1
    msg_dim = 9
    matrix = communication_matrix(o)
    sender_msg = _sender_message(o)
    appended = th.zeros(batch_size, n_agents, msg_dim, device=o.device, dtype=o.dtype)
    active = matrix[:, :, sender_idx].unsqueeze(-1)
    appended = appended + active * sender_msg.unsqueeze(1)
    return th.cat([o, appended], dim=-1)
