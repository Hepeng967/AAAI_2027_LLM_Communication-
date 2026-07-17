import torch as th


def message_design_instruction():
    return (
        "Masked task-fact anchor teacher for 5z_vs_1ul. Agent 0 is the certified "
        "anchor sender and sends only Ultralisk visibility/relative position plus "
        "own health and attack intent to agents 1..4. The communication content "
        "is sparse and matrix-consistent: receivers with no active edge receive "
        "zero message content."
    )


def _sender_message(o):
    sender = 0
    target_context = o[:, sender, 4:7]
    health_intent = th.cat([o[:, sender, 34:35], o[:, sender, 42:43]], dim=-1)
    return th.cat([target_context, health_intent], dim=-1)


def communication_matrix(o):
    batch_size, n_agents, _ = o.shape
    device = o.device
    dtype = o.dtype
    matrix = th.zeros(batch_size, n_agents, n_agents, device=device, dtype=dtype)
    matrix[:, 1:, 0] = 1.0
    return matrix


def communication(o):
    batch_size, n_agents, obs_dim = o.shape
    assert n_agents == 5 and obs_dim == 48, "Expected 5 agents and 48-dim observations"

    sender = 0
    msg_dim = 5
    matrix = communication_matrix(o)
    sender_msg = _sender_message(o)
    appended = th.zeros(batch_size, n_agents, msg_dim, device=o.device, dtype=o.dtype)
    active = matrix[:, :, sender].unsqueeze(-1)
    appended = appended + active * sender_msg.unsqueeze(1)
    return th.cat([o, appended], dim=-1)
