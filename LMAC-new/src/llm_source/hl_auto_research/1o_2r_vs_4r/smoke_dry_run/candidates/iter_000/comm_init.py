import torch as th

def message_design_instruction():
    return "Dry-run teacher: appends one zero message dimension and disables communication edges."

def communication(o):
    msg = th.zeros(*o.shape[:-1], 1, device=o.device, dtype=o.dtype)
    return th.cat([o, msg], dim=-1)

def communication_matrix(o):
    b, n = o.shape[0], o.shape[-2]
    return th.zeros(b, n, n, device=o.device, dtype=o.dtype)
