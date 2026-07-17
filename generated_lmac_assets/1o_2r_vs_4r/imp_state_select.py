import numpy

def select_important_state():
    """
    Importance extractor for the 1 Overseer + 2 Roaches vs 4 enemy Roaches task.

    Reasoning:
    - The Overseer provides vision but cannot attack; allied Roaches must coordinate
      movement and focus fire under partial observability.
    - Dimensions critical for coordination and focus firing are:
      1) Allied health (to know when to retreat/help).
      2) Allied weapon cooldown (Roaches' attack readiness; Overseer's is constant but included for completeness).
      3) Allied absolute positions (for movement coordination and staying in Overseer vision).
      4) Allied unit type bits (to distinguish Overseer from Roaches).
      5) Enemy health (to select lowest-health targets for focus fire).
      6) Enemy absolute positions (to move into range and focus specific enemies).
    - Enemy unit type bits are constant (always Roach) and the unused placeholder bit
      is always 0, so they are uninformative and excluded.
    - All allied features (indices 0-17) are kept because they vary/identify roles.
    - Enemy health and positions only (indices 18,19,20, 23,24,25, 28,29,30, 33,34,35).
    """
    # Allied features (0-17)
    allied = list(range(18))  # 0 through 17

    # Enemy health and positions for each of the 4 enemies
    enemy_important = []
    for e in range(4):
        base = 18 + e * 5  # each enemy block: health, X, Y, type0, type1
        enemy_important.extend([base, base+1, base+2])  # health, X, Y

    important_dims = allied + enemy_important
    return important_dims
