import numpy

def select_important_state():
    """
    Returns a list of state dimensions that are crucial for the team's success.
    
    Reasoning:
    - Allied health, cooldown, and absolute positions (indices 0-3, 6-9, 12-15) are needed for each Roach to assess its own combat readiness, coordinate movement, and decide when to engage.
    - Enemy health and absolute positions (indices 18-20, 23-25, 28-30, 33-35) enable the team to focus fire on low-health targets and track enemy locations, which are not directly visible to all agents.
    - Type bits are omitted because the role of each agent is fixed and can be deduced from the index order; they do not provide continuous value for decision-making.
    """
    important_dims = [
        0, 1, 2, 3,       # Agent 0: health, cooldown, x, y
        6, 7, 8, 9,       # Agent 1: health, cooldown, x, y
        12, 13, 14, 15,   # Agent 2: health, cooldown, x, y
        18, 19, 20,       # Enemy 0: health, x, y
        23, 24, 25,       # Enemy 1: health, x, y
        28, 29, 30,       # Enemy 2: health, x, y
        33, 34, 35        # Enemy 3: health, x, y
    ]
    return important_dims
