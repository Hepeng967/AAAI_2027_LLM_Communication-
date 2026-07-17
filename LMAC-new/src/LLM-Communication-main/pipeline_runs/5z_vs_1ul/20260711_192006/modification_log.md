# LLM Communication Policy Run

- run directory: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192006`

## Iterations

### Iteration 0

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192006/iteration/5z_vs_1ul/20260711_192006/candidates/iter_000/comm_init.py`
- verdict: `rejected`
- score: `0.3`
- who/when/what: `0.9` / `0.1` / `0.7`
- analysis: The when logic uses an out-of-scale threshold (20) on a feature that appears to represent damage taken (0 = full health, >0 = damage). Because own_health never exceeds 0.625, the low-health condition is always true, causing permanent all-to-all communication. The intended selectivity is broken, and the what mask is always the same set of features.
- next modification: Change the low-health trigger from `own_health < 20.0` to `own_health > 0.01` (any damage). This correctly interprets the feature as damage taken, as supported by rollout values (0.0 for uninjured agents, >0 for those who have taken hits). The exact threshold may be tuned (e.g., >0.05) if noise is an issue, but >0 is already a sparse selector given the feature’s low nonzero rate.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192006/iteration/5z_vs_1ul/20260711_192006/candidates/iter_000/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192006/iteration/5z_vs_1ul/20260711_192006/candidates/iter_000/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192006/iteration/5z_vs_1ul/20260711_192006/candidates/iter_000/summarizer_raw_response.md`

### Iteration 1

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192006/iteration/5z_vs_1ul/20260711_192006/candidates/iter_001/comm_init.py`
- verdict: `accepted`
- score: `0.88`
- who/when/what: `0.85` / `0.95` / `0.85`
- analysis: Minor inefficiency: damaged agents always include enemy-related observation fields in the message mask, even when the enemy is not visible; this results in zero values being transmitted for those fields, which is not harmful but slightly wasteful. No blocking failures.
- next modification: Freeze LLM teacher.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192006/iteration/5z_vs_1ul/20260711_192006/candidates/iter_001/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192006/iteration/5z_vs_1ul/20260711_192006/candidates/iter_001/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192006/iteration/5z_vs_1ul/20260711_192006/candidates/iter_001/summarizer_raw_response.md`

## Final teacher

- manifest: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192006/iteration/5z_vs_1ul/20260711_192006/results/frozen_teacher_manifest.json`
