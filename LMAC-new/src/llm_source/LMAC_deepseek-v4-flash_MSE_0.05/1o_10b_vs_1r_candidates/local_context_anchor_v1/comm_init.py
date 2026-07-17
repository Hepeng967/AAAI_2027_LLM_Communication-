import torch as th


def message_design_instruction():
    return (
        "Local-context anchor teacher for 1o_10b_vs_1r. The Overseer remains "
        "the only sender and broadcasts its sender-observable local context, "
        "excluding agent-id fields. This keeps the certified Overseer-to-"
        "Baneling task-fact edge fixed while testing whether the earlier sparse "
        "teacher failed decision sufficiency because it omitted useful "
        "sender-local decision context."
    )


def _sender_message(o):
    overseer = o.shape[1] - 1
    return o[:, overseer, :92]


def communication_matrix(o):
    batch_size, n_agents, _ = o.shape
    overseer = n_agents - 1
    matrix = th.zeros(batch_size, n_agents, n_agents, device=o.device, dtype=o.dtype)
    receivers = [idx for idx in range(n_agents) if idx != overseer]
    matrix[:, receivers, overseer] = 1.0
    return matrix


def communication(o):
    batch_size, n_agents, obs_dim = o.shape
    assert n_agents == 11 and obs_dim == 103, "Expected 11 agents and 103-dim observations"

    overseer = n_agents - 1
    msg = _sender_message(o)
    active = communication_matrix(o)[:, :, overseer].unsqueeze(-1)
    appended = active * msg.unsqueeze(1)
    return th.cat([o, appended], dim=-1)

