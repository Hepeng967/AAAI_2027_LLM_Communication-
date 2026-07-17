# LLM Communication Policy Run

- run directory: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338`

## Initial generation

- policy: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/generation/comm_init.py`

## Iterations

### Iteration 0

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_000/comm_init.py`
- verdict: `rejected`
- score: `0.3`
- who/when/what: `0.7` / `0.5` / `0.1`
- analysis: The communication function's message packing truncation (M=10) renders the what mask nearly useless. The mask correctly selects own health/position/type for medivacs and injured DPS, previous actions for all, and visible enemy/ally data. However, the fixed‑size packing sorts all selected indices and keeps the first 10, which in practice are always the lowest feature indices (enemy slots first, then ally slots). Consequently, the critical own‑state and action features are never transmitted. This degrades the teacher signal to a stream of partial ally‑slot information, failing to satisfy the stated protocol.
- next modification: Either increase the message dimension to accommodate all selected features (e.g., dynamic size equal to count of True entries in the what mask) or deterministically prioritise the most coordination‑relevant features (own health/position/type and actions) before adding environment observations. A possible implementation: build the message by first appending own‑state, then previous actions, then enemy/ally data until a fixed budget is reached, rather than sorting purely by feature index.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_000/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_000/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_000/summarizer_raw_response.md`

### Iteration 1

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_001/comm_init.py`
- verdict: `rejected`
- score: `0.3`
- who/when/what: `0.6` / `0.5` / `0.2`
- analysis: The communication policy's what logic includes all ally/enemy visible features for every agent, resulting in a what mask that can contain up to 79 indices. The subsequent message packing with M=10 selects features by a fixed priority: own state first, then previous actions, then enemy distance, then ally distance. Since previous actions have high priority and are always in the mask, they occupy most of the budget, leaving no room for enemy/ally data except occasionally the closest enemy feature. Consequently, the rich ally/enemy information is almost never transmitted, defeating the purpose of sharing battlefield awareness. Additionally, the full‑connectivity who/when matrices and the unconditional sending of previous actions may be unnecessary and increase communication overhead, but the primary failure is the mismatch between the what mask and the packing budget.
- next modification: 1. Prune the what mask to include only a small set of critical ally/enemy features (e.g., only the closest enemy, or only injured allies) so that the M=10 budget is used effectively. 2. Alternatively, remove the previous actions from the message when other data is more important, or limit action history to a shorter window. 3. Reduce the who/when connectivity: e.g., medivac only sends to injured DPS, DPS only to medivac and nearby allies, to cut unnecessary traffic.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_001/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_001/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_001/summarizer_raw_response.md`

### Iteration 2

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_002/comm_init.py`
- verdict: `accepted`
- score: `0.85`
- who/when/what: `0.9` / `0.8` / `0.9`
- analysis: The policy is compact and plausible. Medivac broadcasts only own state; this is sufficient for healing coordination. Injured DPS reports own state and closest enemy to medivac. The who/when connectivity is sparse and role-based, avoiding all-to-all flooding. Message what selection packs only essential features, fitting within the 10‑slot budget. No thresholds are out of scale, and the observed rollout edge rate (~0.87%) confirms that the policy activates only when the specified unit types and health conditions are met. One minor drawback is the absence of inter‑DPS communication, but this is not a blocking issue for the intended teacher role.
- next modification: Freeze LLM teacher.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_002/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_002/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/candidates/iter_002/summarizer_raw_response.md`

## Final teacher

- manifest: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/smacv2/terran_10_vs_10/20260714_142338/iteration/terran_10_vs_10/20260714_142338/results/frozen_teacher_manifest.json`
