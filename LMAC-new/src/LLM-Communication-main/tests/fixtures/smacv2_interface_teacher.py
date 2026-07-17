"""Shape-only fixture used to smoke-test SMACv2 pipeline integration."""

import torch


def message_design_instruction():
    return "Shape-only integration fixture."


def communication_who(o):
    n = o.shape[1]
    return (1.0 - torch.eye(n, device=o.device, dtype=o.dtype)).unsqueeze(0).expand(o.shape[0], -1, -1)


def communication_when(o):
    return communication_who(o)


def communication_what(o):
    return torch.ones_like(o)
