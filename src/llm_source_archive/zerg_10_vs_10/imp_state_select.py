import numpy

def select_important_state():
    """
    Selects state dimensions that are crucial for coordinated multi-agent decision-making
    in a 10v10 Zergling/Hydralisk/Baneling battle under partial observability.

    The hypothesis is:
    - Each agent can only partially observe the environment, so communication must carry
      the information that is hardest to perceive individually but most critical for
      coordination: allied unit roles (type), health, cooldown, positions, as well as
      observed enemy health, positions, and types.
    - Additionally, to support coordinated focus fire and avoid overkill, each ally's
      current attack target (which enemy it is attacking) should be shared.
    
    Hence, we select:
    1. All ally state dimensions (health, cooldown, x, y, unit type bits): indices 0–69
    2. All enemy state dimensions (health, x, y, unit type bits): indices 70–129
    3. For each ally (0–9), the "attack enemy k" one-hot indices from the last-action block,
       capturing which enemy the ally is currently focusing. Indices:
       ally_0: 136–145, ally_1: 152–161, ally_2: 168–177, ally_3: 184–193,
       ally_4: 200–209, ally_5: 216–225, ally_6: 232–241, ally_7: 248–257,
       ally_8: 264–273, ally_9: 280–289.
    """
    # Basic ally and enemy info (continuous + categorical types)
    important_dims = list(range(130))  # 0 to 129 inclusive

    # Append attack target indicators for each ally
    for ally_idx in range(10):
        base = 130 + ally_idx * 16  # start of this ally's action block
        attack_start = base + 6      # first attack action (attack_enemy_0)
        attack_end = base + 16       # exclusive (attack_enemy_9 is index base+15)
        important_dims.extend(range(attack_start, attack_end))

    return important_dims
