import torch as th


def message_design_instruction():
    return (
        "Tactical-basis teacher for 5z_vs_1ul. Each Zealot broadcasts only "
        "sender-observable decision features derived from its own local "
        "observation: Ultralisk visibility/relative geometry, distance basis, "
        "health, attack intent, and simple engage/retreat/surround indicators. "
        "The message is a compact nonlinear basis over local observations, so it "
        "does not use privileged global state but should be easier for the "
        "student selector and DRC decision probe to use than raw local context."
    )


def _agent_message(o):
    enemy_visible = o[:, :, 4:5]
    rel_x = o[:, :, 5:6]
    rel_y = o[:, :, 6:7]
    own_health = o[:, :, 34:35].clamp(0.0, 1.0)
    attack_intent = o[:, :, 42:43]

    dist = th.sqrt(rel_x.pow(2) + rel_y.pow(2) + 1e-6)
    inv_dist = enemy_visible / (1.0 + dist)
    close_enemy = (enemy_visible > 0.5).to(o.dtype) * (dist < 0.35).to(o.dtype)
    mid_enemy = (enemy_visible > 0.5).to(o.dtype) * ((dist >= 0.35) & (dist < 0.75)).to(o.dtype)
    far_enemy = (enemy_visible > 0.5).to(o.dtype) * (dist >= 0.75).to(o.dtype)

    low_health = ((own_health > 0.0) & (own_health < 0.35)).to(o.dtype)
    medium_health = ((own_health >= 0.35) & (own_health < 0.7)).to(o.dtype)
    high_health = (own_health >= 0.7).to(o.dtype)

    engage_score = enemy_visible * high_health * (close_enemy + 0.5 * mid_enemy)
    kite_score = enemy_visible * low_health * (close_enemy + mid_enemy)
    chase_score = enemy_visible * high_health * far_enemy

    signed_dir_x = enemy_visible * rel_x / dist.clamp_min(1e-3)
    signed_dir_y = enemy_visible * rel_y / dist.clamp_min(1e-3)
    abs_dir_x = signed_dir_x.abs()
    abs_dir_y = signed_dir_y.abs()

    return th.cat(
        [
            enemy_visible,
            rel_x * enemy_visible,
            rel_y * enemy_visible,
            dist * enemy_visible,
            inv_dist,
            signed_dir_x,
            signed_dir_y,
            abs_dir_x,
            abs_dir_y,
            own_health,
            low_health,
            medium_health,
            high_health,
            attack_intent,
            close_enemy,
            mid_enemy,
            far_enemy,
            engage_score,
            kite_score,
            chase_score,
            enemy_visible * own_health,
            enemy_visible * attack_intent,
            low_health * attack_intent,
            high_health * attack_intent,
        ],
        dim=-1,
    )


def communication_matrix(o):
    batch_size, n_agents, _ = o.shape
    msg = _agent_message(o)
    enemy_visible = msg[:, :, 0] > 0.5
    low_health = msg[:, :, 10] > 0.5
    attack_intent = msg[:, :, 13] > 0.5
    tactically_active = enemy_visible | low_health | attack_intent

    # Keep agent 0 as a permanent anchor for the preregistered 5z task facts,
    # and let other Zealots speak only when their local observation is relevant.
    tactically_active[:, 0] = True
    matrix = tactically_active.to(o.dtype).unsqueeze(1).expand(batch_size, n_agents, n_agents).clone()
    eye = th.eye(n_agents, device=o.device, dtype=o.dtype).unsqueeze(0)
    return matrix * (1.0 - eye)


def communication(o):
    batch_size, n_agents, obs_dim = o.shape
    assert n_agents == 5 and obs_dim == 48, "Expected 5 agents and 48-dim observations"

    msg = _agent_message(o)
    matrix = communication_matrix(o)
    chunks = []
    for receiver in range(n_agents):
        sender_chunks = []
        for sender in range(n_agents):
            if sender == receiver:
                continue
            edge = matrix[:, receiver, sender].unsqueeze(-1)
            sender_chunks.append(edge * msg[:, sender, :])
        chunks.append(th.cat(sender_chunks, dim=-1).unsqueeze(1))
    appended = th.cat(chunks, dim=1)
    return th.cat([o, appended], dim=-1)
