"""Original-LMAC communication policy for the single-group Hallway task."""

import torch as th


def message_design_instruction():
    return (
        "Each agent broadcasts its local hallway observation, previous-action "
        "one-hot vector, and sender identity.  A receiver gets the concatenated "
        "messages of every other agent; self messages are excluded."
    )


def communication(o: th.Tensor) -> th.Tensor:
    """Append messages from the other three agents to the LMAC input.

    ``o`` is the original LMAC controller input: one local observation value,
    three previous-action features, and four agent-ID features.
    """
    if o.ndim != 3 or o.shape[1:] != (4, 8):
        raise ValueError(f"hallway expects (batch, 4, 8), got {tuple(o.shape)}")

    batch_size, n_agents, _ = o.shape
    sender_messages = o  # all eight dimensions are coordination-relevant
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
