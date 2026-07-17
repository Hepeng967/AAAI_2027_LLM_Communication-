# LLM Communication Policy Run

- run directory: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436`

## Iterations

### Iteration 0

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_000/comm_init.py`
- verdict: `rejected`
- score: `0.25`
- who/when/what: `0.6` / `0.1` / `0.7`
- analysis: The when‑component is designed to trigger only for low‑health or enemy‑visible conditions, but the health threshold `20.0` is incompatible with the actual observation scale (normalized health ≤ 0.625). Consequently, every agent triggers communication at every timestep, yielding a fully‑connected, always‑active communication graph. This contradicts the stated intention of sparse, event‑driven messaging and fails to provide selective supervision. The what‑component selects a reasonable set of features (enemy info + own health/shield), but because the broken trigger forces the mask to be constant, it cannot demonstrate the intended dynamic switch between message sets. The who‑matrix, while simple, is acceptable in itself, but its interaction with the faulty when‑logic makes the overall strategy an inappropriate teacher for a learnable selector.
- next modification: 1. Replace the health threshold with a value consistent with the rollout feature statistics—e.g., `own_health < 0.2`—so that only genuinely damaged agents send messages.  2. Optionally, tighten the who‑matrix by limiting communication to allies that are visible (using the ally visibility features) to further reduce useless traffic.  3. Keep the enemy‑visible trigger (`enemy_0_available > 0.5`) as is, but ensure it does not get overridden by an always‑true health condition.  4. After fixing the threshold, verify that the dynamic what‑mask correctly toggles between set A and set B according to the new trigger logic.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_000/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_000/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_000/summarizer_raw_response.md`

### Iteration 1

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_001/comm_init.py`
- verdict: `rejected`
- score: `0.45`
- who/when/what: `0.6` / `0.2` / `0.65`
- analysis: The when-condition uses own_health < 0.2 as a trigger. In the rollout observations, own_health is zero for the majority of timesteps (nonzero_rate only 0.103, mean 0.065, max 0.625). Because health values are often exactly zero, the condition is true almost continuously for all agents, resulting in an always-on communication pattern. This contradicts the stated goal of sending messages only in distress or when the enemy is visible. The what-component correctly switches between two compact message sets, but the near-universal activation of trigger_a makes the switching logic ineffective and degenerates the strategy into a static mask. The who-matrix is acceptable but reinforces the excessive traffic.
- next modification: 1. Replace the health threshold condition with something that reflects actual hull damage, e.g., `own_health > 0.0` (meaning the agent has taken hull damage, not full health). Optionally combine with shield status: `own_health > 0.0 and own_shield < 0.5` to indicate real distress. 2. Consider using `enemy_0_available > 0.5` as the primary trigger, and only add health-based distress when the enemy is not visible or when the agent is exposed. 3. Introduce a time-decay or event-based hysteresis to avoid rapid toggling if needed. 4. After fixing the trigger, verify that the dynamic what-mask correctly toggles between set A (with shield) and set B (enemy info only) as intended, and that the resulting when_edge_rate drops significantly.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_001/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_001/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_001/summarizer_raw_response.md`

### Iteration 2

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_002/comm_init.py`
- verdict: `accepted`
- score: `0.9`
- who/when/what: `0.8` / `0.9` / `0.9`
- analysis: No blocking failures. The strategy is compact, correctly thresholds own health damage (own_health > 0) and enemy visibility (enemy_0_available > 0.5) to trigger sparse communication. Messages are sparse (2.5% non‑zeros) and use only task‑relevant features (enemy info, own health/shield). Rollout evidence shows expected behaviour: mix of triggers, agents can be silent, and the who‑matrix (all‑to‑all except self) is effectively gated by the when conditions, making overall edge rate low (18.5%).
- next modification: Freeze LLM teacher.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_002/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_002/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/candidates/iter_002/summarizer_raw_response.md`

## Final teacher

- manifest: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_192436/iteration/5z_vs_1ul/20260711_192436/results/frozen_teacher_manifest.json`
