import torch


def message_design_instruction():
    """
    Returns a natural language description of the designed communication protocol.
    This function is required by the candidate validation process.
    """
    return (
        "Communication rules:\n"
        "R1 (health alert): when an agent's own_health < 0.2 (normalized units), "
        "it sends its own_health (33), enemy_0_rel_x (6), and enemy_0_rel_y (7) to all other agents.\n"
        "R2 (enemy position broadcast): when an agent detects an enemy (enemy_0_available == 1), "
        "it sends enemy_0_rel_x (6) and enemy_0_rel_y (7) to all other agents."
    )


def communication_who(o):
    # RULE R1, R2: all agents can send to all other agents (off-diagonal only)
    # sender_group: G1 (all agents), receiver_selector: all_other_agents
    batch_size, n_agents, obs_dim = o.shape
    who = (1 - torch.eye(n_agents, device=o.device, dtype=o.dtype)).unsqueeze(0).expand(batch_size, -1, -1)
    return who


def communication_when(o):
    # RULE R1 (health alert): triggered when own_health < 0.2
    # RULE R2 (enemy position broadcast): triggered when enemy_0_available == 1.0
    health_cond = (o[:, :, 33] < 0.2)      # [batch, n_agents]
    enemy_cond = (o[:, :, 4] == 1.0)        # [batch, n_agents]
    when = (health_cond | enemy_cond).float()  # sender‑side condition mask
    batch_size, n_agents, _ = o.shape
    when = when.unsqueeze(1).expand(-1, n_agents, -1)   # [batch, n_receivers, n_senders]
    # zero out self-communication diagonal
    when = when * (1 - torch.eye(n_agents, device=o.device, dtype=when.dtype).unsqueeze(0))
    return when


def communication_what(o):
    # RULE R1: wounded agent sends own_health (33), enemy_0_rel_x (6), enemy_0_rel_y (7)
    # RULE R2: agent seeing enemy sends enemy_0_rel_x (6), enemy_0_rel_y (7)
    health_cond = (o[:, :, 33] < 0.2)      # [batch, n_agents]
    enemy_cond = (o[:, :, 4] == 1.0)        # [batch, n_agents]

    send_health = health_cond                # health only sent when wounded
    send_enemy_pos = health_cond | enemy_cond # enemy position sent by either rule

    what_mask = torch.zeros_like(o)
    what_mask[:, :, 33] = send_health.float()
    what_mask[:, :, 6]  = send_enemy_pos.float()
    what_mask[:, :, 7]  = send_enemy_pos.float()
    return what_mask
