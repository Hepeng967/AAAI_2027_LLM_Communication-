#!/usr/bin/env python3
import sys
from pathlib import Path
from types import SimpleNamespace

import torch as th

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from controllers.lmac_controller import LMAC_MAC
from learners.lmac_learner import LMAC_learner
from components.certified_task_facts import CERTIFIED_TASK_FACT_EDGES, map_specs
from LLM.prompt_templates import PromptTemplates
from scripts.summarize_progress import matches_run_prefix as progress_prefix_match
from scripts.summarize_comm_ablation import matches_run_prefix as ablation_prefix_match


def check_registry():
    specs = map_specs()
    assert specs["1o_10b_vs_1r"]["required_task_facts"][0]["fact"] == "enemy_position"
    assert CERTIFIED_TASK_FACT_EDGES["1o_10b_vs_1r"] == [(i, 10) for i in range(10)]
    assert CERTIFIED_TASK_FACT_EDGES["1o_2r_vs_4r"] == [(i, 0) for i in range(1, 5)]
    assert CERTIFIED_TASK_FACT_EDGES["5z_vs_1ul"] == [(i, 0) for i in range(1, 5)]


def check_prompt_wording():
    prompt = PromptTemplates._get_instruction_I_P("(2, 5, 48)", "o[0, 0, :]", "")
    required = [
        "Task-Decision Completeness",
        "Do not optimize for full state reconstruction",
        "sender feasibility",
        "receiver necessity",
        "communication_matrix(o)",
    ]
    for needle in required:
        assert needle in prompt, f"missing prompt phrase: {needle}"


def check_teacher_weighting():
    learner = LMAC_learner.__new__(LMAC_learner)
    learner.n_agents = 5
    learner.map_name = "5z_vs_1ul"
    learner.args = SimpleNamespace(
        use_certified_teacher_weights=True,
        certified_teacher_weight_mode="task_facts",
        certified_teacher_positive_weight=1.0,
        certified_teacher_certified_edge_weight=2.0,
        certified_teacher_negative_weight=1.0,
        normalize_certified_teacher_weights=True,
    )
    teacher = th.ones(2, 3, 5, 5)
    offdiag = 1.0 - th.eye(5).view(1, 1, 5, 5)
    weights = learner._teacher_loss_weights(teacher, offdiag)
    mask = offdiag.expand_as(weights)
    assert weights[0, 0, 1, 0] > weights[0, 0, 0, 1]
    assert abs(((weights * mask).sum() / mask.sum()).item() - 1.0) < 1e-6


def check_eval_ablation_masks():
    mac = LMAC_MAC.__new__(LMAC_MAC)
    mac.n_agents = 5
    mac.map_name = "5z_vs_1ul"
    base = th.ones(2, 5, 5)

    mac.args = SimpleNamespace(eval_comm_ablation="drop_certified_edges")
    dropped = mac._apply_eval_comm_ablation(base, test_mode=True)
    assert dropped[:, 1, 0].sum().item() == 0.0
    assert dropped[:, 0, 1].sum().item() == 2.0

    mac.args.eval_comm_ablation = "keep_certified_edges"
    kept = mac._apply_eval_comm_ablation(base, test_mode=True)
    assert kept[:, 1, 0].sum().item() == 2.0
    assert kept[:, 0, 1].sum().item() == 0.0


def check_packed_receiver_gating():
    mac = LMAC_MAC.__new__(LMAC_MAC)
    mac.n_agents = 5
    messages = th.ones(1, 5, 20)
    comm = th.zeros(1, 5, 5)
    comm[:, 0, 1] = 1.0
    comm[:, 0, 3] = 1.0

    gated = mac._gate_packed_receiver_messages(comm, messages)
    assert gated[:, 0, 0:5].sum().item() == 5.0
    assert gated[:, 0, 5:10].sum().item() == 0.0
    assert gated[:, 0, 10:15].sum().item() == 5.0
    assert gated[:, 0, 15:20].sum().item() == 0.0
    assert gated[:, 1:].sum().item() == 0.0


def check_prefix_matching():
    assert progress_prefix_match("ts_receiverfix_10b_seed0", "ts_receiverfix")
    assert not progress_prefix_match("ts_receiverfix2_10b_seed0", "ts_receiverfix")
    assert ablation_prefix_match("comm_ablate_ts_2r_seed0_2r_none", "comm_ablate")
    assert not ablation_prefix_match("comm_ablate2_ts_2r_seed0_2r_none", "comm_ablate")


def main():
    checks = [
        ("registry", check_registry),
        ("prompt_wording", check_prompt_wording),
        ("teacher_weighting", check_teacher_weighting),
        ("eval_ablation_masks", check_eval_ablation_masks),
        ("packed_receiver_gating", check_packed_receiver_gating),
        ("prefix_matching", check_prefix_matching),
    ]
    for name, fn in checks:
        fn()
        print(f"PASS {name}")
    print("certified communication pipeline smoke test passed")


if __name__ == "__main__":
    main()
