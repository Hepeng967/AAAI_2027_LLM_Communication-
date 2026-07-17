"""Original-LMAC communication policy for the grouped Hallway task."""

import torch as th


def message_design_instruction():
    return (
        "Each agent broadcasts its two local group-aware observations, previous "
        "action, and sender identity.  Receivers concatenate messages from the "
        "other six agents so both groups can coordinate their arrival times."
    )


def communication(o: th.Tensor) -> th.Tensor:
    """Append messages from the other six agents to the LMAC input.

    ``o`` contains two local observation values, three previous-action features,
    and seven agent-ID features.
    """
    if o.ndim != 3 or o.shape[1:] != (7, 12):
        raise ValueError(f"hallway_group expects (batch, 7, 12), got {tuple(o.shape)}")

    batch_size, n_agents, _ = o.shape
    sender_messages = o
    received = []
    for receiver in range(n_agents):
        received.append(
            th.cat(
                [sender_messages[:, sender] for sender in range(n_agents) if sender != receiver],
                dim=-1,
            )
        )
    received_messages = th.stack(received, dim=1)
    return th.cat((o, received_messages), dim=-1)
