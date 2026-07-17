import torch as th


def message_design_instruction():
    """
    Decision-relevant sparse teacher for 5z_vs_1ul.

    The message content stays identical to the accepted dense/dynamic teacher:
    each sender exposes Ultralisk visibility, relative target position, own
    health, and attack intent. The communication matrix is made sparser by
    keeping agent 0 as the certified anchor and only allowing non-anchor senders
    to transmit when they provide novel target visibility or urgent health /
    engagement context.
    """
    return (
        "Use agent 0 as a certified target/health anchor. Other Zealots only "
        "communicate when their local observation is decision-relevant to a "
        "receiver: they see the Ultralisk while the receiver does not, they are "
        "low-health, or they are actively attacking. This preserves task facts "
        "while reducing redundant all-to-all communication."
    )


def communication(o):
    batch_size, n_agents, obs_dim = o.shape
    assert n_agents == 5 and obs_dim == 48, "Expected 5 agents and 48-dim observations"

    enemy_vis = o[:, :, 4:5]
    rel_enemy_x = o[:, :, 5:6]
    rel_enemy_y = o[:, :, 6:7]
    own_health = o[:, :, 34:35]
    attack_flag = o[:, :, 42:43]
    msg = th.cat([enemy_vis, rel_enemy_x, rel_enemy_y, own_health, attack_flag], dim=2)

    msg_append_dim = (n_agents - 1) * 5
    output = th.cat(
        [
            o,
            th.zeros(batch_size, n_agents, msg_append_dim, device=o.device, dtype=o.dtype),
        ],
        dim=2,
    )

    for receiver in range(n_agents):
        other_indices = [sender for sender in range(n_agents) if sender != receiver]
        output[:, receiver, 48:] = th.cat(
            [msg[:, sender : sender + 1, :] for sender in other_indices],
            dim=2,
        ).squeeze(1)

    return output


def communication_matrix(o):
    """
    matrix[:, receiver, sender] = 1.

    Sparse decision-relevant schedule:
    - agent 0 -> agents 1..4 is always kept as the certified anchor edge;
    - non-anchor sender j -> receiver i if j sees the Ultralisk and i does not;
    - non-anchor sender j -> receiver i if j is low health or attacking, so the
      receiver gets urgent coordination context;
    - no self edges.
    """
    batch_size, n_agents, _ = o.shape
    device = o.device
    dtype = o.dtype

    enemy_visible = o[:, :, 4] > 0.5
    own_health = o[:, :, 34]
    attack_intent = o[:, :, 42] > 0.5
    low_health = (own_health > 0.0) & (own_health < 0.35)

    matrix = th.zeros(batch_size, n_agents, n_agents, device=device, dtype=dtype)

    receivers = [i for i in range(n_agents) if i != 0]
    matrix[:, receivers, 0] = 1.0

    for sender in range(1, n_agents):
        sender_novel_target = enemy_visible[:, sender].view(batch_size, 1)
        sender_urgent = (low_health[:, sender] | attack_intent[:, sender]).view(batch_size, 1)
        for receiver in range(n_agents):
            if receiver == sender:
                continue
            receiver_missing_target = (~enemy_visible[:, receiver]).view(batch_size, 1)
            should_send = (sender_novel_target & receiver_missing_target) | sender_urgent
            matrix[:, receiver, sender] = should_send.squeeze(1).to(dtype)

    eye = th.eye(n_agents, device=device, dtype=dtype).unsqueeze(0)
    return matrix * (1.0 - eye)
