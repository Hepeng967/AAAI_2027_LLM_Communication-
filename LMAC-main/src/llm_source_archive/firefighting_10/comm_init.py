import torch as th

def communication(o: th.Tensor) -> th.Tensor:
    if o.ndim != 3 or o.shape[1:] != (10, 13):
        raise ValueError(f"firefighting_10 expects (batch,10,13), got {tuple(o.shape)}")
    # Share flame detection and previous action; sender identity is already appended.
    msg = o[:, :, :3]
    received = [th.cat([msg[:, j] for j in range(10) if j != i], -1) for i in range(10)]
    return th.cat((o, th.stack(received, 1)), -1)
