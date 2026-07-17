#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"
WORK="${WORK:-/tmp/lmac_drc_pipeline_smoke}"
TEACHER="$ROOT/src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05/5z_vs_1ul/comm_init.py"

rm -rf "$WORK"
mkdir -p "$WORK/buffer/5z_vs_1ul/test" "$WORK/search"

"$PY" - "$WORK/fact_subset_fixture.json" <<'PY'
import json
import sys
from pathlib import Path

fixture = {
    "method": "DRC-receiver-necessity-fact-subset-v1",
    "maps": {
        "5z_vs_1ul": {
            "certified_fact_names": ["ultralisk_visibility_position"],
            "rejected_fact_names": ["health_and_attack_intent"],
        }
    },
}
Path(sys.argv[1]).write_text(json.dumps(fixture, indent=2) + "\n")
PY

"$PY" -m py_compile \
  "$ROOT/scripts/audit_drc_buffers.py" \
  "$ROOT/scripts/audit_drc_formal_readiness.py" \
  "$ROOT/scripts/build_drc_llm_feedback.py" \
  "$ROOT/scripts/call_drc_llm_candidate.py" \
  "$ROOT/scripts/call_drc_llm_revision.py" \
  "$ROOT/scripts/certify_decision_relevant_comm.py" \
  "$ROOT/scripts/generate_drc_candidate_prompt.py" \
  "$ROOT/scripts/generate_drc_feedback_prompt.py" \
  "$ROOT/scripts/generate_drc_revision_round.py" \
  "$ROOT/scripts/make_drc_fact_subset_manifest.py" \
  "$ROOT/scripts/make_drc_candidate_manifest.py" \
  "$ROOT/scripts/preflight_drc_formal_run.py" \
  "$ROOT/scripts/list_drc_candidates.py" \
  "$ROOT/scripts/write_drc_protocol.py" \
  "$ROOT/scripts/select_drc_teacher.py" \
  "$ROOT/scripts/select_drc_robust_teacher.py" \
  "$ROOT/scripts/manifest_comm_paths.py" \
  "$ROOT/scripts/plan_teacher_student_from_manifest.py" \
  "$ROOT/scripts/write_drc_paper_dossier.py" \
  "$ROOT/scripts/split_drc_buffer_root.py" \
  "$ROOT/scripts/validate_drc_comm_code.py"

bash -n \
  "$ROOT/scripts/collect_formal_drc_buffers.sh" \
  "$ROOT/scripts/run_drc_two_stage_evidence_pipeline.sh" \
  "$ROOT/scripts/run_drc_teacher_construction.sh" \
  "$ROOT/scripts/run_drc_formal_evidence_pipeline.sh" \
  "$ROOT/scripts/run_drc_sensitivity_suite.sh" \
  "$ROOT/scripts/run_formal_drc_v5.sh" \
  "$ROOT/scripts/run_drc_teacher_search.sh" \
  "$ROOT/scripts/run_drc_llm_iteration.sh" \
  "$ROOT/scripts/validate_generated_teacher_pipeline.sh" \
  "$ROOT/scripts/launch_teacher_student_eval.sh"

"$PY" - \
  "$ROOT/scripts/collect_formal_drc_buffers.sh" \
  "$ROOT/scripts/collect_lmac_buffers.py" \
  "$ROOT/scripts/run_drc_teacher_search.sh" \
  "$ROOT/scripts/run_drc_sensitivity_suite.sh" \
  "$ROOT/scripts/run_drc_teacher_construction.sh" \
  "$ROOT/scripts/run_formal_drc_v5.sh" \
  "$ROOT/scripts/run_drc_formal_evidence_pipeline.sh" \
  "$ROOT/scripts/launch_teacher_student_eval.sh" <<'PY'
import sys
from pathlib import Path

formal = Path(sys.argv[1]).read_text()
collector = Path(sys.argv[2]).read_text()
wrappers = [Path(path).read_text() for path in sys.argv[3:]]
three_maps = "1o_10b_vs_1r 1o_2r_vs_4r 5z_vs_1ul"
assert 'MAPS="${MAPS:-10b 2r 5z}"' in formal, formal
assert three_maps in formal, formal
assert '"2r": "1o_2r_vs_4r"' in collector, collector
for text in wrappers:
    assert three_maps in text, text[:500]
PY

RUN_MODE=dry_run \
OUT_ROOT="$WORK/evidence_pipeline_dry_run" \
FACT_SUBSET_MANIFEST="$WORK/fact_subset_fixture.json" \
bash "$ROOT/scripts/run_drc_formal_evidence_pipeline.sh" \
  > "$WORK/evidence_pipeline_dry_run.stdout"

"$PY" - "$WORK/evidence_pipeline_dry_run/README.md" "$WORK/evidence_pipeline_dry_run/commands.sh" <<'PY'
import sys
from pathlib import Path

readme = Path(sys.argv[1]).read_text()
commands = Path(sys.argv[2]).read_text()
assert "1o_10b_vs_1r 1o_2r_vs_4r 5z_vs_1ul" in readme, readme
assert "10b 2r 5z" in readme, readme
assert "collect_formal_drc_buffers.sh" in commands, commands
assert "preflight_drc_formal_run.py" in commands, commands
assert "run_formal_drc_v5.sh" in commands, commands
assert "FACT_SUBSET_MANIFEST=" in commands, commands
assert "--fact-subset-manifest" in commands, commands
PY

RUN_MODE=dry_run \
OUT_ROOT="$WORK/two_stage_dry_run" \
BUFFER_ROOT="$WORK/buffer" \
bash "$ROOT/scripts/run_drc_two_stage_evidence_pipeline.sh" \
  > "$WORK/two_stage_dry_run.stdout"

"$PY" - "$WORK/two_stage_dry_run/README.md" "$WORK/two_stage_dry_run/commands.sh" <<'PY'
import sys
from pathlib import Path

readme = Path(sys.argv[1]).read_text()
commands = Path(sys.argv[2]).read_text()
for needle in (
    "DRC Two-Stage Evidence Pipeline",
    "calibration root",
    "certification root",
):
    assert needle in readme, needle
for needle in (
    "split_drc_buffer_root.py",
    "make_drc_fact_subset_manifest.py",
    "calibration_drc",
    "certification_drc",
    "run_formal_drc_v5.sh",
):
    assert needle in commands, needle
PY
bash -n "$WORK/two_stage_dry_run/commands.sh"

"$PY" "$ROOT/scripts/generate_drc_candidate_prompt.py" \
  --maps 5z_vs_1ul \
  --out-dir "$WORK/prompts" \
  > "$WORK/prompt.stdout"

"$PY" - "$WORK/prompts/5z_vs_1ul_drc_candidate_prompt.md" <<'PY'
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text()
for needle in (
    "sender_observable",
    "receiver_necessary",
    "task_fact_complete",
    "decision_sufficient",
    "causally_useful",
    "ultralisk_visibility_position",
    "communication_matrix(o)",
):
    assert needle in text, needle
PY

"$PY" "$ROOT/scripts/call_drc_llm_candidate.py" \
  --prompt "$WORK/prompts/5z_vs_1ul_drc_candidate_prompt.md" \
  --map 5z_vs_1ul \
  --candidate-root "$WORK/generated_candidates" \
  --candidate-label smoke_init_candidate \
  --metadata-out "$WORK/init_candidate_metadata.json" \
  --dry-run \
  > "$WORK/init_candidate_dry_run.stdout"

"$PY" - "$WORK/init_candidate_metadata.json" <<'PY'
import json
import sys
from pathlib import Path

meta = json.loads(Path(sys.argv[1]).read_text())
assert meta["method"] == "DRC-LLM-initial-candidate-call-v1", meta
assert meta["dry_run"], meta
assert meta["candidate_path"].endswith("comm_init.py"), meta
PY

"$PY" "$ROOT/scripts/validate_drc_comm_code.py" \
  --map 5z_vs_1ul \
  --comm-code "$TEACHER" \
  --out-json "$WORK/teacher_interface_validation.json" \
  > "$WORK/teacher_interface_validation.stdout"

MAP_NAME=5z_vs_1ul \
COMM_CODE="$TEACHER" \
OUT_ROOT="$WORK/generated_teacher_validation" \
RUN_DRC=false \
RUN_RL=false \
bash "$ROOT/scripts/validate_generated_teacher_pipeline.sh" \
  > "$WORK/generated_teacher_validation.stdout"

"$PY" - "$WORK/teacher_interface_validation.json" "$WORK/generated_teacher_validation/README.md" "$WORK/generated_teacher_validation/commands.sh" <<'PY'
import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text())
readme = Path(sys.argv[2]).read_text()
commands = Path(sys.argv[3]).read_text()
assert report["valid"], report
assert report["message_dim"] >= 0, report
assert "Generated Teacher Validation Pipeline" in readme, readme
assert "certify_decision_relevant_comm.py" in commands, commands
assert "launch_teacher_student_eval.sh" in commands, commands
PY

RUN_MAPS=5z_vs_1ul \
OUT_ROOT="$WORK/construction" \
RUN_FORMAL=false \
bash "$ROOT/scripts/run_drc_teacher_construction.sh" \
  > "$WORK/construction.stdout"

"$PY" - "$WORK/construction/drc_candidates.json" "$WORK/construction/candidate_prompts/5z_vs_1ul_drc_candidate_prompt.md" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text())
prompt = Path(sys.argv[2]).read_text()
assert manifest["candidate_count"] >= 1, manifest
assert manifest["valid_candidate_count"] == manifest["candidate_count"], manifest
assert "sender_observable" in prompt and "causally_useful" in prompt
PY

RUN_MAPS=5z_vs_1ul \
OUT_ROOT="$WORK/sensitivity" \
CANDIDATE_MANIFEST="$WORK/construction/drc_candidates.json" \
RUN_SUITE=false \
SENSITIVITY_CONFIGS="linear_return mlp_return" \
bash "$ROOT/scripts/run_drc_sensitivity_suite.sh" \
  > "$WORK/sensitivity.stdout"

"$PY" - "$WORK/sensitivity/sensitivity_plan.tsv" <<'PY'
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text()
assert "linear_return" in text, text
assert "mlp_return" in text, text
assert "teacher_search" not in text or "linear_return" in text
PY

"$PY" - "$WORK/buffer" <<'PY'
import pickle
import sys
from pathlib import Path

import torch as th

root = Path(sys.argv[1]) / "5z_vs_1ul"
paths = [root / "train_traj_0000.pkl", root / "test" / "test_traj_0000.pkl"]
for path in paths:
    path.parent.mkdir(parents=True, exist_ok=True)
    split = "test" if path.parent.name == "test" else "train"
    sample = {
        "obs": th.zeros(1, 4, 5, 36),
        "state": th.zeros(1, 4, 28),
        "mask": th.ones(1, 4, 1),
        "actions": th.zeros(1, 4, 5, 1, dtype=th.long),
        "actions_onehot": th.zeros(1, 4, 5, 7),
        "avail_actions": th.ones(1, 4, 5, 7),
        "reward": th.zeros(1, 4, 1),
        "terminated": th.zeros(1, 4, 1),
        "metadata": {
            "collector": "smoke_drc_pipeline.sh",
            "schema": "formal_drc_buffer_v2",
            "map_name": "5z_vs_1ul",
            "split": split,
            "seed": 0,
            "episode_index": 0,
            "test_mode": split == "test",
            "contains_return_fields": True,
        },
    }
    sample["actions_onehot"][..., 0] = 1.0
    with path.open("wb") as f:
        pickle.dump(sample, f)
PY

"$PY" "$ROOT/scripts/audit_drc_buffers.py" \
  --buffer-root "$WORK/buffer" \
  --maps 5z_vs_1ul \
  --max-files 4 \
  --out-json "$WORK/audit.json" \
  --out-md "$WORK/audit.md" \
  > "$WORK/audit.stdout"

"$PY" - "$WORK/audit.json" <<'PY'
import json
import sys
from pathlib import Path

audit = json.loads(Path(sys.argv[1]).read_text())
summary = audit["maps"]["5z_vs_1ul"]["summary"]
assert summary["formal_ready"], summary
assert summary["return_coverage"] == 1.0, summary
assert summary["metadata_coverage"] == 1.0, summary
assert summary["metadata_ok_coverage"] == 1.0, summary
PY

"$PY" "$ROOT/scripts/split_drc_buffer_root.py" \
  --buffer-root "$WORK/buffer" \
  --maps 5z_vs_1ul \
  --out-root "$WORK/buffer_split" \
  --out-json "$WORK/buffer_split/split_manifest.json" \
  --out-md "$WORK/buffer_split/split_manifest.md" \
  > "$WORK/buffer_split.stdout"

"$PY" - "$WORK/buffer_split/split_manifest.json" "$WORK/buffer_split/calibration" "$WORK/buffer_split/certification" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text())
calibration = Path(sys.argv[2])
certification = Path(sys.argv[3])
assert manifest["ready"], manifest
assert manifest["maps"]["5z_vs_1ul"]["counts"]["calibration"] == 1, manifest
assert manifest["maps"]["5z_vs_1ul"]["counts"]["certification"] == 1, manifest
assert list(calibration.glob("5z_vs_1ul/**/*.pkl")), calibration
assert list(certification.glob("5z_vs_1ul/**/*.pkl")), certification
PY

"$PY" "$ROOT/scripts/audit_drc_buffers.py" \
  --buffer-root "$WORK/buffer_split/calibration" \
  --maps 5z_vs_1ul \
  --max-files 4 \
  --out-json "$WORK/buffer_split/calibration_audit.json" \
  --out-md "$WORK/buffer_split/calibration_audit.md" \
  > "$WORK/buffer_split/calibration_audit.stdout"

"$PY" "$ROOT/scripts/audit_drc_buffers.py" \
  --buffer-root "$WORK/buffer_split/certification" \
  --maps 5z_vs_1ul \
  --max-files 4 \
  --out-json "$WORK/buffer_split/certification_audit.json" \
  --out-md "$WORK/buffer_split/certification_audit.md" \
  > "$WORK/buffer_split/certification_audit.stdout"

"$PY" - "$WORK/buffer_split/calibration_audit.json" "$WORK/buffer_split/certification_audit.json" <<'PY'
import json
import sys
from pathlib import Path

for path in sys.argv[1:]:
    audit = json.loads(Path(path).read_text())
    summary = audit["maps"]["5z_vs_1ul"]["summary"]
    assert summary["formal_ready"], (path, summary)
    assert summary["metadata_ok_coverage"] == 1.0, (path, summary)
PY

"$PY" "$ROOT/scripts/write_drc_protocol.py" \
  --buffer-root "$WORK/buffer" \
  --maps 5z_vs_1ul \
  --audit-max-files 4 \
  --max-files 4 \
  --max-transitions 128 \
  --probe-model mlp \
  --probe-hidden-dim 32 \
  --probe-weight-decay 0.0001 \
  --probe-epochs 2 \
  --decision-oracle auto \
  --min-conditional-decision-nats 0.01 \
  --min-receiver-necessity-rate 1.0 \
  --score-gain-cap 1.0 \
  --n-bootstrap 10 \
  --n-sign-permutations 10 \
  --n-message-shuffles 2 \
  --stat-alpha 0.05 \
  --require-stat-significance \
  --require-content-control \
  --fact-subset-manifest "$WORK/fact_subset_fixture.json" \
  --out-json "$WORK/drc_protocol.json" \
  --out-md "$WORK/drc_protocol.md" \
  > "$WORK/protocol.stdout"

"$PY" - "$WORK/drc_protocol.json" <<'PY'
import json
import sys
from pathlib import Path

protocol = json.loads(Path(sys.argv[1]).read_text())
assert protocol["protocol_sha256"], protocol
assert protocol["certification"]["probe_model"] == "mlp", protocol
assert protocol["fact_subset_manifest"].endswith("fact_subset_fixture.json"), protocol
assert protocol["certification"]["score_gain_cap"] == 1.0, protocol
PY

"$PY" "$ROOT/scripts/preflight_drc_formal_run.py" \
  --buffer-root "$WORK/buffer" \
  --candidate-manifest "$WORK/construction/drc_candidates.json" \
  --fact-subset-manifest "$WORK/fact_subset_fixture.json" \
  --maps 5z_vs_1ul \
  --out-dir "$WORK/preflight_ready" \
  --audit-max-files 4 \
  --max-files 4 \
  --max-transitions 128 \
  --probe-model mlp \
  --probe-hidden-dim 32 \
  --probe-weight-decay 0.0001 \
  --probe-epochs 2 \
  --decision-oracle auto \
  --min-conditional-decision-nats 0.01 \
  --min-receiver-necessity-rate 1.0 \
  --score-gain-cap 1.0 \
  --n-bootstrap 10 \
  --n-sign-permutations 10 \
  --n-message-shuffles 2 \
  --stat-alpha 0.05 \
  > "$WORK/preflight_ready.stdout"

"$PY" - "$WORK/preflight_ready/preflight_report.json" <<'PY'
import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text())
assert report["ready"], report
assert report["checks"][0]["passes"], report
assert report["checks"][1]["passes"], report
assert report["checks"][2]["passes"], report
assert "run_formal_drc_v5.sh" in report["commands"]["formal_drc_command"], report
assert "FACT_SUBSET_MANIFEST" in report["commands"]["formal_drc_command"], report
assert "SCORE_GAIN_CAP" in report["commands"]["formal_drc_command"], report
PY

mkdir -p "$WORK/buffer_missing_returns/5z_vs_1ul/test"
"$PY" - "$WORK/buffer/5z_vs_1ul/test/test_traj_0000.pkl" "$WORK/buffer_missing_returns/5z_vs_1ul/test/test_traj_0000.pkl" <<'PY'
import pickle
import sys
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
with src.open("rb") as f:
    item = pickle.load(f)
item.pop("reward", None)
item.pop("terminated", None)
with dst.open("wb") as f:
    pickle.dump(item, f)
PY

set +e
"$PY" "$ROOT/scripts/preflight_drc_formal_run.py" \
  --buffer-root "$WORK/buffer_missing_returns" \
  --candidate-manifest "$WORK/construction/drc_candidates.json" \
  --maps 5z_vs_1ul \
  --out-dir "$WORK/preflight_fail" \
  --audit-max-files 4 \
  --max-files 4 \
  --max-transitions 128 \
  --probe-epochs 2 \
  > "$WORK/preflight_fail.stdout"
preflight_fail_status=$?
set -e
test "$preflight_fail_status" -eq 2
"$PY" - "$WORK/preflight_fail/preflight_report.json" <<'PY'
import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text())
assert not report["ready"], report
assert not report["checks"][1]["passes"], report
assert report["checks"][1]["failed_maps"]["5z_vs_1ul"]["return_coverage"] == 0.0, report
PY

"$PY" - "$WORK/search" "$TEACHER" <<'PY'
import json
import sys
from pathlib import Path

search = Path(sys.argv[1])
teacher = sys.argv[2]
base = {
    "method": "synthetic-drc-smoke",
    "map_name": "5z_vs_1ul",
    "comm_code": teacher,
    "has_return_data": True,
    "passes_statistical_gate": True,
    "passes_content_gate": True,
    "observability_and_necessity": [
        {
            "fact": "ultralisk_visibility_position",
            "passes_sender_observable": True,
            "passes_receiver_necessary": True,
            "necessity_gain_r2": 0.5,
        }
    ],
    "task_fact_completeness": {"coverage_rate": 1.0},
    "decision_sufficiency": {
        "passes_decision_sufficient": True,
        "probe_model": "mlp",
        "oracle_kind": "return",
        "ce_gain_resampling": {"p_value_positive": 0.01},
        "content_specificity": {"shuffle_minus_true_ce": 0.5},
    },
    "causal_usefulness": {
        "passes_causally_useful": True,
        "mean_causal_ce_resampling": {"p_value_positive": 0.01},
    },
    "matrix_edge_rate": 0.2,
    "formal_certificate": {
        "accepted": True,
        "gates": [
            {"gate": "sender_observable", "passes": True},
            {"gate": "receiver_necessary", "passes": True},
            {"gate": "task_fact_complete", "passes": True},
            {"gate": "decision_sufficient", "passes": True},
            {"gate": "causally_useful", "passes": True},
        ],
    },
    "scores": {
        "sender_observable_rate": 1.0,
        "receiver_necessary_rate": 1.0,
        "task_fact_completeness": 1.0,
        "final_score": 3.0,
        "decision_sufficiency_gain": 0.2,
        "conditional_decision_value_nats": 0.2,
        "conditional_decision_value_bits": 0.2885,
        "causal_usefulness": 0.3,
    },
}
accepted = dict(base, accepted=True)
rejected = dict(base, accepted=False)
rejected["passes_statistical_gate"] = False
rejected["passes_content_gate"] = False
rejected["decision_sufficiency"] = dict(
    base["decision_sufficiency"],
    passes_decision_sufficient=False,
    accuracy_gain=0.0,
    ce_gain=-0.1,
)
rejected["scores"] = dict(
    base["scores"],
    receiver_necessary_rate=0.5,
    final_score=0.1,
    decision_sufficiency_gain=-0.1,
)
rejected["formal_certificate"] = dict(
    base["formal_certificate"],
    accepted=False,
    gates=[
        {"gate": "sender_observable", "passes": True},
        {"gate": "receiver_necessary", "passes": False},
        {"gate": "task_fact_complete", "passes": True},
        {"gate": "decision_sufficient", "passes": False},
        {"gate": "causally_useful", "passes": True},
    ],
)
better = dict(base, accepted=True)
better["scores"] = dict(base["scores"], final_score=3.5)
better["matrix_edge_rate"] = 0.25
(search / "5z_rejected.json").write_text(json.dumps(rejected, indent=2) + "\n")
(search / "5z_accepted.json").write_text(json.dumps(accepted, indent=2) + "\n")
(search / "5z_better.json").write_text(json.dumps(better, indent=2) + "\n")
PY

"$PY" "$ROOT/scripts/generate_drc_feedback_prompt.py" \
  --result "$WORK/search/5z_rejected.json" \
  --out-dir "$WORK/feedback_failed" \
  > "$WORK/feedback_failed.stdout"

"$PY" "$ROOT/scripts/generate_drc_feedback_prompt.py" \
  --result "$WORK/search/5z_better.json" \
  --out-dir "$WORK/feedback_accepted" \
  > "$WORK/feedback_accepted.stdout"

"$PY" - "$WORK/feedback_failed/5z_vs_1ul_5z_rejected_revision_prompt.md" "$WORK/feedback_accepted/5z_vs_1ul_5z_better_freeze_prompt.md" <<'PY'
import sys
from pathlib import Path

failed = Path(sys.argv[1]).read_text()
accepted = Path(sys.argv[2]).read_text()
assert "Revision Instructions" in failed, failed
assert "Freeze Instructions" in accepted, accepted
assert "Do not generate a new candidate" in accepted, accepted
assert "TensorBoard" in failed and "TensorBoard" in accepted
PY

"$PY" "$ROOT/scripts/generate_drc_revision_round.py" \
  --result "$WORK/search" \
  --candidate-root "$ROOT/src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05" \
  --round-label smoke_round \
  --out-dir "$WORK/revision_round" \
  --include-accepted \
  > "$WORK/revision_round.stdout"

"$PY" - "$WORK/revision_round/revision_round_manifest.json" "$WORK/revision_round/revision_round_manifest.md" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text())
md = Path(sys.argv[2]).read_text()
assert manifest["method"] == "DRC-guided-revision-round-v1", manifest
assert manifest["offline_only"], manifest
assert manifest["num_revision_prompts"] == 1, manifest
assert manifest["num_accepted_prompts"] == 2, manifest
row = manifest["revision_prompts"][0]
assert row["primary_failure"] == "receiver_necessary", row
assert "decision_sufficient" in row["failed_gates"], row
assert Path(row["prompt_path"]).exists(), row
prompt = Path(row["prompt_path"]).read_text()
assert "Offline Selection Principle" in prompt, prompt
assert "downstream RL results" in prompt, prompt
assert "Revision Prompts" in md, md
PY

"$PY" "$ROOT/scripts/build_drc_llm_feedback.py" \
  --result "$WORK/search/5z_rejected.json" \
  --candidate-root "$WORK/generated_candidates" \
  --candidate-label smoke_llm_candidate \
  --round-label smoke_llm_round \
  --out-json "$WORK/drc_llm_feedback.json" \
  --out-md "$WORK/drc_llm_feedback.md" \
  > "$WORK/drc_llm_feedback.stdout"

"$PY" "$ROOT/scripts/call_drc_llm_revision.py" \
  --feedback-json "$WORK/drc_llm_feedback.json" \
  --prompt-out "$WORK/deepseek_prompt.md" \
  --metadata-out "$WORK/deepseek_metadata.json" \
  --dry-run \
  > "$WORK/deepseek_dry_run.stdout"

"$PY" - "$WORK/drc_llm_feedback.json" "$WORK/drc_llm_feedback.md" "$WORK/deepseek_prompt.md" "$WORK/deepseek_metadata.json" <<'PY'
import json
import sys
from pathlib import Path

feedback = json.loads(Path(sys.argv[1]).read_text())
md = Path(sys.argv[2]).read_text()
prompt = Path(sys.argv[3]).read_text()
meta = json.loads(Path(sys.argv[4]).read_text())
assert feedback["decision_sufficient_feedback"]["target_function"] == "communication(o)", feedback
assert feedback["causally_useful_feedback"]["target_function"] == "communication_matrix(o)", feedback
assert "Rollout Data Conclusion" in md, md
assert "Structured DRC feedback" in prompt, prompt
assert meta["dry_run"], meta
PY

RESULT_JSON="$WORK/search/5z_rejected.json" \
OUT_ROOT="$WORK/drc_llm_iteration" \
CANDIDATE_ROOT="$WORK/generated_candidates" \
CANDIDATE_LABEL=smoke_llm_candidate \
RUN_LLM=false \
bash "$ROOT/scripts/run_drc_llm_iteration.sh" \
  > "$WORK/drc_llm_iteration.stdout"

"$PY" - "$WORK/drc_llm_iteration/README.md" "$WORK/drc_llm_iteration/commands.sh" "$WORK/drc_llm_iteration/drc_llm_feedback.json" <<'PY'
import json
import sys
from pathlib import Path

readme = Path(sys.argv[1]).read_text()
commands = Path(sys.argv[2]).read_text()
feedback = json.loads(Path(sys.argv[3]).read_text())
assert "DRC-LLM Iteration Run" in readme, readme
assert "launch_teacher_student_eval.sh" in commands, commands
assert "certify_decision_relevant_comm.py" in commands, commands
assert feedback["destination_file"].endswith("comm_init.py"), feedback
PY

"$PY" "$ROOT/scripts/make_drc_fact_subset_manifest.py" \
  --result "$WORK/search" \
  --out-json "$WORK/fact_subset.json" \
  --out-md "$WORK/fact_subset.md" \
  > "$WORK/fact_subset.stdout"

"$PY" - "$WORK/fact_subset.json" "$WORK/fact_subset.md" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text())
md = Path(sys.argv[2]).read_text()
assert manifest["method"] == "DRC-receiver-necessity-fact-subset-v1", manifest
assert manifest["maps"]["5z_vs_1ul"]["certified_fact_names"], manifest
assert "receiver-necessity" in md, md
PY

"$PY" "$ROOT/scripts/select_drc_teacher.py" \
  --search-root "$WORK/search" \
  --require-return-data \
  --require-stat-gate \
  --require-content-gate \
  --out-json "$WORK/frozen_teacher_manifest.json" \
  --out-md "$WORK/frozen_teacher_manifest.md" \
  > "$WORK/select.stdout"

"$PY" - "$WORK/frozen_teacher_manifest.json" "$TEACHER" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text())
teacher = sys.argv[2]
item = manifest["teachers"]["5z_vs_1ul"]
assert item["teacher_path"] == teacher, item
assert item["score"] == 3.5, item
assert manifest["num_selected_maps"] == 1, manifest
PY

mkdir -p "$WORK/search_copy"
cp "$WORK/search/"*.json "$WORK/search_copy/"

"$PY" "$ROOT/scripts/select_drc_robust_teacher.py" \
  --search-roots "$WORK/search" "$WORK/search_copy" \
  --require-return-data \
  --require-stat-gate \
  --require-content-gate \
  --out-json "$WORK/robust_frozen_teacher_manifest.json" \
  --out-md "$WORK/robust_frozen_teacher_manifest.md" \
  > "$WORK/robust_select.stdout"

"$PY" - "$WORK/robust_frozen_teacher_manifest.json" "$TEACHER" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text())
teacher = sys.argv[2]
item = manifest["teachers"]["5z_vs_1ul"]
assert item["teacher_path"] == teacher, item
assert item["mean_score"] == 3.5, item
assert len(item["robust_evidence"]) == 2, item
PY

"$PY" "$ROOT/scripts/audit_drc_formal_readiness.py" \
  --candidate-manifest "$WORK/construction/drc_candidates.json" \
  --buffer-audit "$WORK/audit.json" \
  --protocol "$WORK/drc_protocol.json" \
  --teacher-search "$WORK/search" \
  --frozen-manifest "$WORK/robust_frozen_teacher_manifest.json" \
  --require-robust-manifest \
  --out-json "$WORK/readiness_audit.json" \
  --out-md "$WORK/readiness_audit.md" \
  > "$WORK/readiness.stdout"

"$PY" - "$WORK/readiness_audit.json" <<'PY'
import json
import sys
from pathlib import Path

audit = json.loads(Path(sys.argv[1]).read_text())
assert audit["formal_ready"], audit
PY

"$PY" "$ROOT/scripts/write_drc_paper_dossier.py" \
  --teacher-search "$WORK/search" \
  --candidate-manifest "$WORK/construction/drc_candidates.json" \
  --protocol "$WORK/drc_protocol.json" \
  --buffer-audit "$WORK/audit.json" \
  --frozen-manifest "$WORK/frozen_teacher_manifest.json" \
  --formal-readiness-audit "$WORK/readiness_audit.json" \
  --out-json "$WORK/drc_paper_dossier.json" \
  --out-md "$WORK/drc_paper_dossier.md" \
  > "$WORK/dossier.stdout"

"$PY" - "$WORK/drc_paper_dossier.json" <<'PY'
import json
import sys
from pathlib import Path

dossier = json.loads(Path(sys.argv[1]).read_text())
assert dossier["method"] == "DRC-paper-dossier-v1", dossier
assert dossier["formal_ready"], dossier
assert dossier["map_summary"]["5z_vs_1ul"]["num_candidates"] == 3, dossier
assert dossier["frozen_teachers"]["5z_vs_1ul"]["teacher_path"], dossier
assert dossier["frozen_teachers"]["5z_vs_1ul"]["conditional_decision_value_nats"] == 0.2, dossier
PY

"$PY" "$ROOT/scripts/manifest_comm_paths.py" \
  --manifest "$WORK/frozen_teacher_manifest.json" \
  --map 5z_vs_1ul \
  --format json-list \
  > "$WORK/comm_paths.txt"

"$PY" "$ROOT/scripts/plan_teacher_student_from_manifest.py" \
  --manifest "$WORK/frozen_teacher_manifest.json" \
  --out-md "$WORK/student_plan.md" \
  > "$WORK/student_plan.stdout"

grep -q "5z_vs_1ul" "$WORK/student_plan.md"
grep -q "$TEACHER" "$WORK/comm_paths.txt"

echo "DRC pipeline smoke passed. Artifacts: $WORK"
