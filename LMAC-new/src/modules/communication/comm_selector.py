import torch as th
import torch.nn as nn


class CommSelectorNet(nn.Module):
    """Predicts a receiver-by-sender communication matrix from per-agent inputs."""

    def __init__(self, input_dim, args):
        super().__init__()
        self.n_agents = args.n_agents
        hidden_dim = getattr(args, "comm_selector_hidden_dim", args.hidden_dim)

        self.agent_encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )
        self.receiver_proj = nn.Linear(hidden_dim, hidden_dim)
        self.sender_proj = nn.Linear(hidden_dim, hidden_dim)
        self.pair_scorer = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, agent_inputs):
        # agent_inputs: [batch, n_agents, input_dim]
        encoded = self.agent_encoder(agent_inputs)
        receiver = self.receiver_proj(encoded).unsqueeze(2).expand(-1, -1, self.n_agents, -1)
        sender = self.sender_proj(encoded).unsqueeze(1).expand(-1, self.n_agents, -1, -1)
        pair = th.cat([receiver, sender, receiver * sender], dim=-1)
        logits = self.pair_scorer(pair).squeeze(-1)

        eye = th.eye(self.n_agents, device=agent_inputs.device).unsqueeze(0)
        logits = logits.masked_fill(eye.bool(), -20.0)
        return logits
