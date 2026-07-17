import torch as th


def message_design_instruction():
    return (
        "All-local-context teacher for 5z_vs_1ul. Each Zealot broadcasts its "
        "own sender-observable local context, excluding agent-id fields, to the "
        "other Zealots. This is a stronger DRC diagnostic candidate: it tests "
        "whether 5z decision sufficiency requires teammate-local context rather "
        "than a single anchor sender, while still avoiding privileged global "
        "state."
    )


def _agent_message(o):
    return o[:, :, :43]


def communication_matrix(o):
    batch_size, n_agents, _ = o.shape
    eye = th.eye(n_agents, device=o.device, dtype=o.dtype).unsqueeze(0)
    return (1.0 - eye).expand(batch_size, n_agents, n_agents).clone()


def communication(o):
    batch_size, n_agents, obs_dim = o.shape
    assert n_agents == 5 and obs_dim == 48, "Expected 5 agents and 48-dim observations"

    msg = _agent_message(o)
    chunks = []
    for receiver in range(n_agents):
        sender_chunks = []
        for sender in range(n_agents):
            if sender == receiver:
                continue
            sender_chunks.append(msg[:, sender, :])
        chunks.append(th.cat(sender_chunks, dim=-1).unsqueeze(1))
    appended = th.cat(chunks, dim=1)
    return th.cat([o, appended], dim=-1)

