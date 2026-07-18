import torch as th

def communication(o: th.Tensor) -> th.Tensor:
    if o.ndim != 3 or o.shape[1:] != (10, 42):
        raise ValueError(f"binary_consensus_10 expects (batch,10,42), got {tuple(o.shape)}")
    msg = o[:, :, :30]
    received = [th.cat([msg[:, j] for j in range(10) if j != i], -1) for i in range(10)]
    return th.cat((o, th.stack(received, 1)), -1)
