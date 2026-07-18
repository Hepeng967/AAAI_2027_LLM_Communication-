```python
import torch

def message_design_instruction():
    """
    Adjacent agents (pairs 0-1,1-2,...,8-9) share a fire alert (raw flame observation)
    and their previous action when they detect a fire. This allows the receiver to
    decide whether to join the sender at the shared burning house. Communication is
    sparse because it is triggered only on fire detection.
    """
    return "Fire-alert policy: adjacent firefighters share flame indicator and previous action on fire detection."

# ---------------------------------------------------------------------------
# Helper: build adjacency matrix for all adjacent pairs (bidirectional).
# This captures all groups G1–G9.
# ---------------------------------------------------------------------------
def _adjacency_matrix(num_agents, device):
    adj = torch.zeros(num_agents, num_agents, device=device)
    # set upper and lower off-diagonals
    idx = torch.arange(num_agents - 1, device=device)
    adj[idx, idx + 1] = 1.0
    adj[idx + 1, idx] = 1.0
    return adj

# ===========================================================================
# RULES R1-R9: Each rule defines a pair of adjacent agents (G1:0-1, G2:1-2, ...,
# G9:8-9). The who mask allows bidirectional communication for all these groups.
# ===========================================================================
def communication_who(o):
    B, N, _ = o.shape
    adj = _adjacency_matrix(N, o.device)            # [N, N]
    who = adj.unsqueeze(0).expand(B, -1, -1)        # [B, receiver, sender]
    return who

# ===========================================================================
# RULES R1-R9: A message is triggered when the sender observes a fire at its
# last visited house, i.e., raw_flame_observation (index 0) > 0.5.
# ===========================================================================
def communication_when(o):
    B, N, _ = o.shape
    fire = (o[:, :, 0] > 0.5).float()               # [B, N] -- sender flag
    adj = _adjacency_matrix(N, o.device)            # [N, N]
    who = adj.unsqueeze(0).expand(B, -1, -1)        # [B, receiver, sender]

    # when[b, j, i] = 1 if i and j are adjacent AND sender i has fire.
    when = who * fire.unsqueeze(1)                  # fire broadcast over receiver dim
    return when

# ===========================================================================
# RULES R1-R9: The message content is the sender's raw flame observation
# (index 0) and its previous action one-hot encoding (indices 1 and 2).
# ===========================================================================
def communication_what(o):
    mask = torch.zeros_like(o)                      # same shape as o
    mask[..., [0, 1, 2]] = 1.0                      # select features 0,1,2
    return mask
```