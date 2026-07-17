import numpy

def select_important_state():
    # All 28 state dimensions are critical for coordinated micro-management:
    # - Agent healths (0,5,10,15,20) determine survivability and retreat decisions.
    # - Weapon cooldowns (1,6,11,16,21) are essential for timing focus fire.
    # - Absolute positions (2,3,7,8,12,13,17,18,22,23) enable kiting and spacing.
    # - Shields (4,9,14,19,24) affect durability and engagement order.
    # - Enemy health (25) indicates progress and when to commit.
    # - Enemy position (26,27) is crucial for positioning and kiting.
    # In the partially observable setting, many of these are not directly
    # perceivable by all agents, making inter-agent communication vital.
    important_dims = list(range(28))
    return important_dims
