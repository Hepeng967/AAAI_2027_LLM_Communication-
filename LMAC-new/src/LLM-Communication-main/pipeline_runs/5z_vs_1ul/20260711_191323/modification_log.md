# LLM Communication Policy Run

- run directory: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323`

## Iterations

### Iteration 0

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_000/comm_init.py`
- verdict: `rejected`
- score: `0.3`
- who/when/what: `1.0` / `0.1` / `0.6`
- analysis: The intended strategy introduces a low‑health distress condition, but the implementation uses a hard‑coded threshold of 20. Because all observed `own_health` values are ≤ 0.625, the comparison `own_health < 20.0` always yields `True`. Consequently `sender_trigger` is 1 for every agent at every timestep, producing an unconditional all‑to‑all broadcast. This contradicts the design instruction ('send … if low health or enemy visible') and eliminates any sparsity benefit. The `what` function consequently always selects the ‘trigger a’ feature set, never using ‘trigger b’. The constant broadcast may be acceptable for such a small map, but it fails the conditional‑communication capability test and is flagged as a blocking bug.
- next modification: Replace the health threshold with a normalised value grounded in the rollout statistics, e.g., `condition_low_health = (own_health < 0.1).float()` (≤10 % of observed maximum health). Optionally include shield in the distress trigger or in the message. If ally partial visibility is important, consider adding the nearest ally’s state to `what`. Ensure that future iterations maintain the intended conditional logic: the `when` matrix must reflect the OR of a correctly scaled low‑health signal and the enemy‑visible signal.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_000/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_000/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_000/summarizer_raw_response.md`

### Iteration 1

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_001/comm_init.py`
- verdict: `rejected`
- score: `0.5`
- who/when/what: `1.0` / `0.5` / `0.7`
- analysis: The when condition `own_health < 0.1` fires for agents with health = 0 (dead), because 0 is the most frequent health value (median 0, nonzero rate 0.103). This turns the intended conditional distress signal into a near‑constant broadcast from dead agents, defeating sparsity goals and injecting noise. The high edge‑rate of 0.8967 is largely driven by this flaw.
- next modification: Add an alive check to the when trigger, e.g., `(own_health + own_shield) > 0` before allowing a sender to transmit. This will silence dead agents entirely. Optionally, raise the distress threshold above 0.1 based on the distribution (p50=0, p95=0.625) to avoid triggering on every tiny health drop. Use `condition_low_health = ((own_health < 0.1) & (alive > 0)).float()`.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_001/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_001/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_001/summarizer_raw_response.md`

### Iteration 2

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_002/comm_init.py`
- verdict: `accepted`
- score: `0.95`
- who/when/what: `0.9` / `1.0` / `1.0`
- analysis: The who matrix is all-to-all minus self, making it dense, but actual communication is sparse (8.2% edge rate) because of the when condition. The when condition reliably silences dead agents via an alive check for low-health distress, and the enemy-visible branch empirically does not fire for dead agents in the rollout. The what features are a compact, task-relevant subset (enemy info, own health/shield) selected per trigger, matching the evidence cases.
- next modification: Freeze LLM teacher.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_002/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_002/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/candidates/iter_002/summarizer_raw_response.md`

## Final teacher

- manifest: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_191323/iteration/5z_vs_1ul/20260711_191323/results/frozen_teacher_manifest.json`
