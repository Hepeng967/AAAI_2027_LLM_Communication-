# LLM Communication Policy Run

- run directory: `/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223`

## Initial generation

- policy: `/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223/generation/comm_init.py`

## Iterations

### Iteration 0

- candidate: `/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223/iteration/academy_run_pass_and_shoot_with_keeper/20260716_190223/candidates/iter_000/comm_init.py`
- verdict: `accepted`
- score: `0.85`
- who/when/what: `1.0` / `0.8` / `0.9`
- analysis: The when threshold (ball distance < 0.1) may be too restrictive for early intention signalling, but it fires in 67% of timesteps, which is acceptable for a bare‑possession strategy. The what mask includes ego absolute position that could be redundant because the teammate already observes relative position, but it adds global context without harm.
- next modification: Freeze LLM teacher.
- judge prompt: `/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223/iteration/academy_run_pass_and_shoot_with_keeper/20260716_190223/candidates/iter_000/llm_judge_prompt.md`
- judge response: `/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223/iteration/academy_run_pass_and_shoot_with_keeper/20260716_190223/candidates/iter_000/llm_judge_raw_response.md`
- revision analysis: `/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223/iteration/academy_run_pass_and_shoot_with_keeper/20260716_190223/candidates/iter_000/summarizer_raw_response.md`

## Final teacher

- manifest: `/root/autodl-tmp/AAAI/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/grf/academy_run_pass_and_shoot_with_keeper/20260716_190223/iteration/academy_run_pass_and_shoot_with_keeper/20260716_190223/results/frozen_teacher_manifest.json`
