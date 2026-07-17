import numpy as np

def select_important_state():
    """
    Selects the indices of the global state dimensions that are most critical
    for multi-agent coordination in the SMACv2 protoss 10v10 scenario.

    Reasoning:
    - The task description states that agents must communicate **role**, **health**,
      **position**, and **locally observed enemy information** to coordinate focus fire,
      support, and movement.
    - These correspond exactly to the following raw state dimensions:
        * Ally dimensions (indices 0-79): health, cooldown (attack readiness),
          absolute x/y position, shield, and unit type bits for all 10 allies.
        * Enemy dimensions (indices 80-149): health, absolute x/y position, shield,
          and unit type bits for all 10 enemies.
    - Cooldown is included because it directly affects attack timing and is an essential
      part of an ally's combat status.
    - Last-action information (indices 150-309) is not explicitly mentioned as a
      communication requirement and would dramatically increase dimensionality. While
      it can be useful for intent prediction, the base coordination primitives rely on
      the current state of allies and enemies. Therefore only the 150 dimensions
      containing ally and enemy attributes are selected.

    Returns:
        important_dims (list of int): Indices of the selected state dimensions.
    """
    # All ally attributes: 10 allies * 8 dims = indices 0..79
    ally_dims = list(range(0, 80))

    # All enemy attributes: 10 enemies * 7 dims = indices 80..149
    enemy_dims = list(range(80, 150))

    important_dims = ally_dims + enemy_dims
    return important_dims
