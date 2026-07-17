# LLM Communication Policy Run

- run directory: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/protoss_10_vs_10/20260714_141611`

## Initial generation

- policy: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/protoss_10_vs_10/20260714_141611/generation/comm_init.py`

## Iterations

### Iteration 0

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/protoss_10_vs_10/20260714_141611/iteration/protoss_10_vs_10/20260714_141611/candidates/iter_000/comm_init.py`
- verdict: `rejected`
- score: `0.3`
- who/when/what: `0.8` / `0.2` / `0.5`
- analysis: The who matrix uses a plausible cross‑type design, but the when condition is brittle: it uses only enemy_0_available and ally_slot_0_visible. In a 10v10 setting with dynamic roles, many agents may see enemies/ allies in other slots while slot 0 stays empty. The rollout evidence shows communication dropping to zero early in episodes, which risks missing critical coordination. The what masks are logically consistent with the triggers, but they include all enemy/ally slot indices even for slots that may never be visible, causing message bloat. The policy needs a more robust trigger using any enemy/ally visibility and potentially filtered what based on actual visibility.
- next modification: 1) Replace the when trigger to use OR over all enemy_available (indices 4, 13, 22, 31, 40, 49, 58, 67, 76, 85) and all ally_visible (indices 94, 103, 112, 121, 130, 139, 148, 157, 166) using torch.any over the last dimension. 2) Optionally, restrict the what mask to only include enemy/ally slots whose availability flag is currently true, reducing noise and message dimension when many slots are empty.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/protoss_10_vs_10/20260714_141611/iteration/protoss_10_vs_10/20260714_141611/candidates/iter_000/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/protoss_10_vs_10/20260714_141611/iteration/protoss_10_vs_10/20260714_141611/candidates/iter_000/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/protoss_10_vs_10/20260714_141611/iteration/protoss_10_vs_10/20260714_141611/candidates/iter_000/summarizer_raw_response.md`

### Iteration 1

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/protoss_10_vs_10/20260714_141611/iteration/protoss_10_vs_10/20260714_141611/candidates/iter_001/comm_init.py`
- verdict: `accepted`
- score: `0.85`
- who/when/what: `0.8` / `0.9` / `0.9`
- analysis: The policy largely addresses the previous rejection: the when trigger now uses any enemy/ally visibility, and the what mask dynamically includes only visible slots, reducing noise. The cross‑type who graph and the sparse what are both compact and grounded in the observed features. The most notable weakness is the exclusion of same‑type edges, which may limit coordination among identical unit types (e.g., multiple stalkers). However, this is not a blocking issue for basic communication. All thresholds are within observed ranges, and the rollout evidence confirms that communication silences when no entities are visible.
- next modification: Freeze LLM teacher.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/protoss_10_vs_10/20260714_141611/iteration/protoss_10_vs_10/20260714_141611/candidates/iter_001/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/protoss_10_vs_10/20260714_141611/iteration/protoss_10_vs_10/20260714_141611/candidates/iter_001/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/protoss_10_vs_10/20260714_141611/iteration/protoss_10_vs_10/20260714_141611/candidates/iter_001/summarizer_raw_response.md`

## Final teacher

- manifest: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/protoss_10_vs_10/20260714_141611/iteration/protoss_10_vs_10/20260714_141611/results/frozen_teacher_manifest.json`
