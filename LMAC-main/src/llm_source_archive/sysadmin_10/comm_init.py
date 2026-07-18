import torch as th

def communication(o: th.Tensor) -> th.Tensor:
    if o.ndim != 3 or o.shape[1:] != (10, 52):
        raise ValueError(f"sysadmin_10 expects (batch,10,52), got {tuple(o.shape)}")
    # Broadcast dynamic visible node values and masks; omit the redundant appended IDs.
    msg = o[:, :, :40]
    received = [th.cat([msg[:, j] for j in range(10) if j != i], -1) for i in range(10)]
    return th.cat((o, th.stack(received, 1)), -1)
