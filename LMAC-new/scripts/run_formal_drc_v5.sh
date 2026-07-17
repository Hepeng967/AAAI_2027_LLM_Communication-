#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"
STAMP="${STAMP:-$(date -u +%Y%m%d_%H%M%S)}"
OUT_ROOT="${OUT_ROOT:-$ROOT/description/certification_gate/formal_drc_v5_$STAMP}"
BUFFER_ROOT="${BUFFER_ROOT:-$ROOT/data}"
RUN_MAPS="${RUN_MAPS:-1o_10b_vs_1r 1o_2r_vs_4r 5z_vs_1ul}"
AUDIT_MAX_FILES="${AUDIT_MAX_FILES:-64}"
PROBE_MODEL="${PROBE_MODEL:-mlp}"
PROBE_HIDDEN_DIM="${PROBE_HIDDEN_DIM:-128}"
PROBE_WEIGHT_DECAY="${PROBE_WEIGHT_DECAY:-0.0001}"
PROBE_EPOCHS="${PROBE_EPOCHS:-120}"
MAX_FILES="${MAX_FILES:-64}"
MAX_TRANSITIONS="${MAX_TRANSITIONS:-4096}"
DECISION_ORACLE="${DECISION_ORACLE:-auto}"
DECISION_LABEL="${DECISION_LABEL:-raw_action}"
N_BOOTSTRAP="${N_BOOTSTRAP:-500}"
N_SIGN_PERMUTATIONS="${N_SIGN_PERMUTATIONS:-500}"
N_MESSAGE_SHUFFLES="${N_MESSAGE_SHUFFLES:-16}"
STAT_ALPHA="${STAT_ALPHA:-0.05}"
REQUIRE_STAT_SIGNIFICANCE="${REQUIRE_STAT_SIGNIFICANCE:-true}"
REQUIRE_CONTENT_CONTROL="${REQUIRE_CONTENT_CONTROL:-true}"
MIN_RECEIVER_NECESSITY_RATE="${MIN_RECEIVER_NECESSITY_RATE:-1.0}"
MIN_CONDITIONAL_DECISION_NATS="${MIN_CONDITIONAL_DECISION_NATS:-0.01}"
CONDITIONAL_DECISION_MODE="${CONDITIONAL_DECISION_MODE:-none}"
CONDITIONAL_DECISION_QUANTILE="${CONDITIONAL_DECISION_QUANTILE:-0.25}"
MIN_CONDITIONAL_DECISION_SAMPLES="${MIN_CONDITIONAL_DECISION_SAMPLES:-256}"
SCORE_GAIN_CAP="${SCORE_GAIN_CAP:-1.0}"
EXTRA_CANDIDATES="${EXTRA_CANDIDATES:-}"
CANDIDATE_MANIFEST="${CANDIDATE_MANIFEST:-}"
FACT_SUBSET_MANIFEST="${FACT_SUBSET_MANIFEST:-}"

PROTOCOL_FACT_SUBSET_ARGS=()
if [[ -n "$FACT_SUBSET_MANIFEST" ]]; then
  PROTOCOL_FACT_SUBSET_ARGS=(--fact-subset-manifest "$FACT_SUBSET_MANIFEST")
fi

mkdir -p "$OUT_ROOT"

"$PY" "$ROOT/scripts/write_drc_protocol.py" \
  --buffer-root "$BUFFER_ROOT" \
  --maps $RUN_MAPS \
  --audit-max-files "$AUDIT_MAX_FILES" \
  --max-files "$MAX_FILES" \
  --max-transitions "$MAX_TRANSITIONS" \
  --probe-model "$PROBE_MODEL" \
  --probe-hidden-dim "$PROBE_HIDDEN_DIM" \
  --probe-weight-decay "$PROBE_WEIGHT_DECAY" \
  --probe-epochs "$PROBE_EPOCHS" \
  --decision-oracle "$DECISION_ORACLE" \
  --decision-label "$DECISION_LABEL" \
  --min-conditional-decision-nats "$MIN_CONDITIONAL_DECISION_NATS" \
  --conditional-decision-mode "$CONDITIONAL_DECISION_MODE" \
  --conditional-decision-quantile "$CONDITIONAL_DECISION_QUANTILE" \
  --min-conditional-decision-samples "$MIN_CONDITIONAL_DECISION_SAMPLES" \
  --min-receiver-necessity-rate "$MIN_RECEIVER_NECESSITY_RATE" \
  --score-gain-cap "$SCORE_GAIN_CAP" \
  --n-bootstrap "$N_BOOTSTRAP" \
  --n-sign-permutations "$N_SIGN_PERMUTATIONS" \
  --n-message-shuffles "$N_MESSAGE_SHUFFLES" \
  --stat-alpha "$STAT_ALPHA" \
  $(if [[ "$REQUIRE_STAT_SIGNIFICANCE" == "true" ]]; then echo "--require-stat-significance"; fi) \
  $(if [[ "$REQUIRE_CONTENT_CONTROL" == "true" ]]; then echo "--require-content-control"; fi) \
  --candidate-manifest "$CANDIDATE_MANIFEST" \
  "${PROTOCOL_FACT_SUBSET_ARGS[@]}" \
  --extra-candidates "$EXTRA_CANDIDATES" \
  --out-json "$OUT_ROOT/drc_protocol.json" \
  --out-md "$OUT_ROOT/drc_protocol.md"

"$PY" "$ROOT/scripts/audit_drc_buffers.py" \
  --buffer-root "$BUFFER_ROOT" \
  --maps $RUN_MAPS \
  --max-files "$AUDIT_MAX_FILES" \
  --out-json "$OUT_ROOT/buffer_audit.json" \
  --out-md "$OUT_ROOT/buffer_audit.md"

"$PY" - "$OUT_ROOT/buffer_audit.json" <<'PY'
import json
import sys
from pathlib import Path

audit = json.loads(Path(sys.argv[1]).read_text())
not_ready = [
    (name, item["summary"])
    for name, item in audit["maps"].items()
    if not item["summary"]["formal_ready"]
]
if not_ready:
    for name, summary in not_ready:
        print(
            f"[DRC-V5-AUDIT-FAIL] {name}: "
            f"base={summary['base_coverage']:.3f}, "
            f"return={summary['return_coverage']:.3f}, "
            f"shape={summary['shape_ok_coverage']:.3f}"
        )
    raise SystemExit(
        "Formal DRC-v5 requires reward/terminated-bearing, shape-compatible buffers. "
        "Recollect buffers with scripts/collect_lmac_buffers.py or tmp2=False after the latest schema update."
    )
PY

PROBE_MODEL="$PROBE_MODEL" \
PROBE_HIDDEN_DIM="$PROBE_HIDDEN_DIM" \
PROBE_WEIGHT_DECAY="$PROBE_WEIGHT_DECAY" \
PROBE_EPOCHS="$PROBE_EPOCHS" \
MAX_FILES="$MAX_FILES" \
MAX_TRANSITIONS="$MAX_TRANSITIONS" \
DECISION_ORACLE="$DECISION_ORACLE" \
DECISION_LABEL="$DECISION_LABEL" \
N_BOOTSTRAP="$N_BOOTSTRAP" \
N_SIGN_PERMUTATIONS="$N_SIGN_PERMUTATIONS" \
N_MESSAGE_SHUFFLES="$N_MESSAGE_SHUFFLES" \
STAT_ALPHA="$STAT_ALPHA" \
REQUIRE_STAT_SIGNIFICANCE="$REQUIRE_STAT_SIGNIFICANCE" \
REQUIRE_CONTENT_CONTROL="$REQUIRE_CONTENT_CONTROL" \
MIN_RECEIVER_NECESSITY_RATE="$MIN_RECEIVER_NECESSITY_RATE" \
MIN_CONDITIONAL_DECISION_NATS="$MIN_CONDITIONAL_DECISION_NATS" \
CONDITIONAL_DECISION_MODE="$CONDITIONAL_DECISION_MODE" \
CONDITIONAL_DECISION_QUANTILE="$CONDITIONAL_DECISION_QUANTILE" \
MIN_CONDITIONAL_DECISION_SAMPLES="$MIN_CONDITIONAL_DECISION_SAMPLES" \
SCORE_GAIN_CAP="$SCORE_GAIN_CAP" \
EXTRA_CANDIDATES="$EXTRA_CANDIDATES" \
CANDIDATE_MANIFEST="$CANDIDATE_MANIFEST" \
FACT_SUBSET_MANIFEST="$FACT_SUBSET_MANIFEST" \
RUN_MAPS="$RUN_MAPS" \
BUFFER_ROOT="$BUFFER_ROOT" \
OUT_ROOT="$OUT_ROOT/teacher_search" \
bash "$ROOT/scripts/run_drc_teacher_search.sh"

"$PY" "$ROOT/scripts/summarize_drc_results.py" \
  --search-root "$OUT_ROOT/teacher_search" \
  --out-csv "$OUT_ROOT/drc_results_summary.csv" \
  --out-md "$OUT_ROOT/drc_results_summary.md"

"$PY" "$ROOT/scripts/select_drc_teacher.py" \
  --search-root "$OUT_ROOT/teacher_search" \
  --require-return-data \
  --require-stat-gate \
  --require-content-gate \
  --out-json "$OUT_ROOT/frozen_teacher_manifest.json" \
  --out-md "$OUT_ROOT/frozen_teacher_manifest.md"

"$PY" "$ROOT/scripts/audit_drc_formal_readiness.py" \
  --candidate-manifest "$CANDIDATE_MANIFEST" \
  --buffer-audit "$OUT_ROOT/buffer_audit.json" \
  --protocol "$OUT_ROOT/drc_protocol.json" \
  --teacher-search "$OUT_ROOT/teacher_search" \
  --frozen-manifest "$OUT_ROOT/frozen_teacher_manifest.json" \
  --out-json "$OUT_ROOT/formal_readiness_audit.json" \
  --out-md "$OUT_ROOT/formal_readiness_audit.md"

"$PY" "$ROOT/scripts/write_drc_paper_dossier.py" \
  --teacher-search "$OUT_ROOT/teacher_search" \
  --candidate-manifest "$CANDIDATE_MANIFEST" \
  --protocol "$OUT_ROOT/drc_protocol.json" \
  --buffer-audit "$OUT_ROOT/buffer_audit.json" \
  --frozen-manifest "$OUT_ROOT/frozen_teacher_manifest.json" \
  --formal-readiness-audit "$OUT_ROOT/formal_readiness_audit.json" \
  --out-json "$OUT_ROOT/drc_paper_dossier.json" \
  --out-md "$OUT_ROOT/drc_paper_dossier.md"

echo "Formal DRC-v5 artifacts written to: $OUT_ROOT"
