import numpy as np

def select_important_state():
    """
    Selects the state dimensions important for the 10v10 multi-agent battle task.
    
    Hypothesis:
    In this partially observable scenario, agents must communicate role, health,
    position, and locally observed enemy information to coordinate effectively.
    Therefore, the critical state features are:
      - All ally health, unit type, and position (excluding cooldown).
      - All enemy health, unit type, and position (enemies have no cooldown).
    Last-action indicators (indices 130-289) are high-dimensional, historical
    action data and are less directly relevant than the current entity states.
    Ally cooldown (omitted) is not mentioned in the required communication.
    
    Returns:
        list of ints: indices of the important state dimensions.
    """
    important = []
    # Ally features: 10 allies, each with 7 dims: health, cooldown, x, y, type0, type1, type2
    for i in range(10):
        base = i * 7
        # health, x, y, unit_type_bits (0,2,3,4,5,6) – skip cooldown (base+1)
        important += [base, base+2, base+3, base+4, base+5, base+6]
    
    # Enemy features: indices 70..129 include health, x, y, unit_type_bits – all included
    important += list(range(70, 130))
    
    return important
