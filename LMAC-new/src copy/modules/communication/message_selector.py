import torch.nn as nn


class MessageSelectNet(nn.Module):
    """Predict an observation-aligned content mask for every sender."""

    def __init__(self, input_dim, args):
        super().__init__()
        hidden_dim = int(getattr(args, "message_selector_hidden_dim", args.hidden_dim))
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
        )

    def forward(self, agent_inputs):
        # [batch, sender, input_dim] -> [batch, sender, input_dim]
        return self.net(agent_inputs)
