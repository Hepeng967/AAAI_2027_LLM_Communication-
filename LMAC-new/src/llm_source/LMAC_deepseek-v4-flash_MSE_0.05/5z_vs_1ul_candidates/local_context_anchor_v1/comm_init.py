import torch as th


def message_design_instruction():
    return (
        "Local-context anchor teacher for 5z_vs_1ul. Agent 0 remains the "
        "certified sender and broadcasts its sender-observable local context, "
        "excluding agent-id fields. The message includes the required "
        "Ultralisk position and health/intent facts plus nearby local decision "
        "context, without using privileged global state."
    )


def _sender_message(o):
    sender = 0
    return o[:, sender, :43]


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
    active = communication_matrix(o)[:, :, sender].unsqueeze(-1)
    appended = active * msg.unsqueeze(1)
    return th.cat([o, appended], dim=-1)

