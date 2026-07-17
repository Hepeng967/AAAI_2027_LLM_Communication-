# LLM Communication Policy Run

- run directory: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455`

## Initial generation

- policy: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455/generation/comm_init.py`

## Iterations

### Iteration 0

- candidate: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455/iteration/1o_10b_vs_1r/20260714_101455/candidates/iter_000/comm_init.py`
- verdict: `accepted`
- score: `0.75`
- who/when/what: `1.0` / `0.9` / `0.6`
- analysis: No critical blocking failures. The who and when rules are well defined, sparse, and use observed features. The what for banelings (ally_0_rel_x, ally_0_rel_y) is a plausible spatial signal but is not the most direct coordinate for the overseer. It does not break the policy, but it reduces the information quality.
- next modification: Freeze LLM teacher.
- judge prompt: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455/iteration/1o_10b_vs_1r/20260714_101455/candidates/iter_000/llm_judge_prompt.md`
- judge response: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455/iteration/1o_10b_vs_1r/20260714_101455/candidates/iter_000/llm_judge_raw_response.md`
- revision analysis: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455/iteration/1o_10b_vs_1r/20260714_101455/candidates/iter_000/summarizer_raw_response.md`

## Final teacher

- manifest: `/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/1o_10b_vs_1r/20260714_101455/iteration/1o_10b_vs_1r/20260714_101455/results/frozen_teacher_manifest.json`
