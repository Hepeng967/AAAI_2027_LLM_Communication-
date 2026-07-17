# LLM Communication Policy Run

- run directory: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013`

## Initial generation

- policy: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/generation/comm_init.py`

## Iterations

### Iteration 0

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_000/comm_init.py`
- verdict: `rejected`
- score: `0.4`
- who/when/what: `0.8` / `0.3` / `0.3`
- analysis: The overseer when condition tests only enemy_0_available, missing cases where other enemies are the only visible ones. Roach-to-roach edges are set but the what mask is all‑zero, so those messages carry no information. This violates the intended roach communication rule and wastes bandwidth. The overseer what mask is well-chosen and aligns with rollout evidence, but the other flaws make the policy incomplete.
- next modification: 1. Replace overseer when condition with a check that any enemy is available (e.g., max of enemy_*_available > 0.5, or sum > 0). 2. For roaches, either include features like own_health, previous action, or a learned embedding of the action that can be back‑propagated through, instead of leaving the what mask empty. Alternatively, reconsider whether roach communication should be included at all if the intended target cannot be expressed in the current observation space.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_000/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_000/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_000/summarizer_raw_response.md`

### Iteration 1

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_001/comm_init.py`
- verdict: `rejected`
- score: `0.35`
- who/when/what: `0.9` / `0.8` / `0.4`
- analysis: The overseer part (R1, R2) is correctly implemented and well-grounded in rollout data: enemy positions and health are transmitted when any enemy is visible. The roach-to-roach rule (R3) fails because the what mask only exposes own_health, which cannot convey an intended target. The code comment acknowledges this gap but uses own_health as a placeholder, violating the explicit rule. Rollout evidence confirms that roach messages contain nothing beyond health, so no target coordination is enabled. This makes the policy incomplete as a pure communication strategy.
- next modification: Replace the roach what mask with indices that encode the intended target. The observation includes the previous_action one‑hot at indices 53–62; action 4–9 correspond to attacks on specific enemies. Including these previous_action features would provide a direct proxy for which enemy the roach is attacking at each step. Alternatively, combine own_health with previous_action to convey both status and target. The when condition can remain as-is (alive).
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_001/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_001/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_001/summarizer_raw_response.md`

### Iteration 2

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_002/comm_init.py`
- verdict: `accepted`
- score: `0.92`
- who/when/what: `0.9` / `0.9` / `0.9`
- analysis: No blocking failures. The who, when, and what masks are all task-plausible and well-grounded in rollout data. The overseer broadcasts enemy positions/health when any enemy is visible; roaches exchange attack targets (via last action) and own health while alive. This provides essential coordination information without redundancy.
- next modification: Freeze LLM teacher.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_002/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_002/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/candidates/iter_002/summarizer_raw_response.md`

## Final teacher

- manifest: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_2r_vs_4r/20260712_123013/iteration/1o_2r_vs_4r/20260712_123013/results/frozen_teacher_manifest.json`
