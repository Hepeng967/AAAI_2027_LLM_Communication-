# LLM Communication Policy Run

- run directory: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107`

## Iterations

### Iteration 0

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_000/comm_init.py`
- verdict: `rejected`
- score: `0.4`
- who/when/what: `0.1` / `0.5` / `0.4`
- analysis: Who matrix is all‑to‑all (off‑diagonal) for all agents, ignoring the task spec where only agent 0 needs to broadcast to others. When triggers for any agent that sees the enemy or has low health, causing excessive and redundant communication from all Zealots. What sends a superset of enemy features (availability, distance, relative coordinates, health) and own health/shield, but the spec requires a precise separation: only fields [4,5,6] for the Ultralisk position and [34,42] for health and attack intent; field 42 is not present in rollout observations and own_shield (34) is not sent in the ‘healthy’ trigger case, reducing consistency.
- next modification: Narrow who to sender 0 only. For when, restrict the position broadcast to enemy visibility, and the health/intent broadcast to a meaningful event (e.g. health change or threshold). For what, split strictly: position broadcast sends only indices [4,5,6]; health/intent broadcast sends indices [33,34] (own_health, own_shield). Handle the missing field 42 by noting that attack intent may not be directly observable in this rollout; a separate binary feature or proxy could be introduced if required, but the current design should at least align with available features.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_000/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_000/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_000/summarizer_raw_response.md`

### Iteration 1

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_001/comm_init.py`
- verdict: `accepted`
- score: `0.85`
- who/when/what: `1.0` / `0.8` / `0.8`
- analysis: The what logic is missing field 42 (attack intent) from the task spec, as it is not present in the rollout observations. The substitute own_health/shield combination provides partial health status but omits the explicit attack‑intent component. The when threshold of 20 for own health is somewhat arbitrary and not derived from any specification.
- next modification: Freeze LLM teacher.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_001/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_001/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_001/summarizer_raw_response.md`

## Final teacher

- manifest: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/results/frozen_teacher_manifest.json`
