# COGNAC baseline runs

The following baselines include the same COGNAC task settings used by
`LMAC-main` and `LMAC-new`:

- `sysadmin_10`: 10 agents, observation 40, state 20, 2 actions, 100 steps
- `binary_consensus_10`: 10 agents, observation 30, state 10, 2 actions, 100 steps
- `firefighting_10`: 10 agents, observation 1, state 11, 2 actions, 100 steps

Each baseline provides `cognac_run.sh`. Run all three tasks with:

```bash
cd Baseline/<algorithm>
bash cognac_run.sh
```

Select tasks or GPUs with, for example:

```bash
GPU_IDS=0,1 RUNS_PER_TASK=5 bash cognac_run.sh sysadmin_10 firefighting_10
```

The default Python executable is
`/root/miniconda3/envs/gfootball/bin/python`; override it with `PYTHON_BIN`.
Install the shared environment dependencies from `requirements_cognac.txt`.

GACG additionally imports `torch_scatter`; install a wheel matching the
selected PyTorch and CUDA versions. The TarMAC source tree names its original
algorithm config `vffac`, and the MASIA source directory retains its existing
name `maisa`.

Generated `results/`, `log/`, caches, and experiment output are excluded from
version control.
