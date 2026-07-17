#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"
STAMP="${STAMP:-$(date -u +%Y%m%d_%H%M%S)}"
OUT_ROOT="${OUT_ROOT:-$ROOT/description/certification_gate/drc_sensitivity_$STAMP}"
RUN_MAPS="${RUN_MAPS:-1o_10b_vs_1r 1o_2r_vs_4r 5z_vs_1ul}"
BUFFER_ROOT="${BUFFER_ROOT:-$ROOT/data}"
CANDIDATE_MANIFEST="${CANDIDATE_MANIFEST:?CANDIDATE_MANIFEST is required}"
RUN_SUITE="${RUN_SUITE:-false}"

SENSITIVITY_CONFIGS="${SENSITIVITY_CONFIGS:-linear_return mlp_return}"
MIN_RECEIVER_NECESSITY_RATE="${MIN_RECEIVER_NECESSITY_RATE:-1.0}"
MIN_CONDITIONAL_DECISION_NATS="${MIN_CONDITIONAL_DECISION_NATS:-0.01}"
REQUIRE_STAT_SIGNIFICANCE="${REQUIRE_STAT_SIGNIFICANCE:-true}"
REQUIRE_CONTENT_CONTROL="${REQUIRE_CONTENT_CONTROL:-true}"
DECISION_ORACLE="${DECISION_ORACLE:-auto}"
DECISION_LABEL="${DECISION_LABEL:-raw_action}"
N_BOOTSTRAP="${N_BOOTSTRAP:-500}"
N_SIGN_PERMUTATIONS="${N_SIGN_PERMUTATIONS:-500}"
N_MESSAGE_SHUFFLES="${N_MESSAGE_SHUFFLES:-16}"
STAT_ALPHA="${STAT_ALPHA:-0.05}"
MAX_FILES="${MAX_FILES:-64}"
MAX_TRANSITIONS="${MAX_TRANSITIONS:-4096}"
AUDIT_MAX_FILES="${AUDIT_MAX_FILES:-64}"

mkdir -p "$OUT_ROOT"

config_probe_model() {
  case "$1" in
    linear_return|linear_behavior) echo "linear" ;;
    mlp_return|mlp_behavior) echo "mlp" ;;
    *) echo "Unknown sensitivity config: $1" >&2; return 1 ;;
  esac
}

config_oracle() {
  case "$1" in
    linear_return|mlp_return) echo "auto" ;;
    linear_behavior|mlp_behavior) echo "behavior" ;;
    *) echo "Unknown sensitivity config: $1" >&2; return 1 ;;
  esac
}

config_epochs() {
  case "$1" in
    linear_*) echo "${LINEAR_PROBE_EPOCHS:-120}" ;;
    mlp_*) echo "${MLP_PROBE_EPOCHS:-160}" ;;
    *) echo "Unknown sensitivity config: $1" >&2; return 1 ;;
  esac
}

config_hidden() {
  case "$1" in
    linear_*) echo "${LINEAR_PROBE_HIDDEN_DIM:-128}" ;;
    mlp_*) echo "${MLP_PROBE_HIDDEN_DIM:-128}" ;;
    *) echo "Unknown sensitivity config: $1" >&2; return 1 ;;
  esac
}

roots=()
plan="$OUT_ROOT/sensitivity_plan.tsv"
echo -e "config\tprobe_model\tdecision_oracle\tout_root" > "$plan"

for config in $SENSITIVITY_CONFIGS; do
  probe_model="$(config_probe_model "$config")"
  oracle="$(config_oracle "$config")"
  epochs="$(config_epochs "$config")"
  hidden="$(config_hidden "$config")"
  config_out="$OUT_ROOT/$config"
  roots+=("$config_out/teacher_search")
  echo -e "$config\t$probe_model\t$oracle\t$config_out" >> "$plan"

  echo "[DRC-SENSITIVITY] config=$config probe=$probe_model oracle=$oracle out=$config_out"
  if [[ "$RUN_SUITE" == "true" ]]; then
    OUT_ROOT="$config_out" \
    RUN_MAPS="$RUN_MAPS" \
    BUFFER_ROOT="$BUFFER_ROOT" \
    CANDIDATE_MANIFEST="$CANDIDATE_MANIFEST" \
    PROBE_MODEL="$probe_model" \
    PROBE_HIDDEN_DIM="$hidden" \
    PROBE_EPOCHS="$epochs" \
    DECISION_ORACLE="$oracle" \
    DECISION_LABEL="$DECISION_LABEL" \
    MIN_RECEIVER_NECESSITY_RATE="$MIN_RECEIVER_NECESSITY_RATE" \
    MIN_CONDITIONAL_DECISION_NATS="$MIN_CONDITIONAL_DECISION_NATS" \
    REQUIRE_STAT_SIGNIFICANCE="$REQUIRE_STAT_SIGNIFICANCE" \
    REQUIRE_CONTENT_CONTROL="$REQUIRE_CONTENT_CONTROL" \
    N_BOOTSTRAP="$N_BOOTSTRAP" \
    N_SIGN_PERMUTATIONS="$N_SIGN_PERMUTATIONS" \
    N_MESSAGE_SHUFFLES="$N_MESSAGE_SHUFFLES" \
    STAT_ALPHA="$STAT_ALPHA" \
    MAX_FILES="$MAX_FILES" \
    MAX_TRANSITIONS="$MAX_TRANSITIONS" \
    AUDIT_MAX_FILES="$AUDIT_MAX_FILES" \
    bash "$ROOT/scripts/run_formal_drc_v5.sh"
  fi
done

cat > "$OUT_ROOT/README.md" <<EOF
# DRC Sensitivity Suite

- stamp: \`$STAMP\`
- maps: \`$RUN_MAPS\`
- candidate manifest: \`$CANDIDATE_MANIFEST\`
- buffer root: \`$BUFFER_ROOT\`
- configs: \`$SENSITIVITY_CONFIGS\`
- decision label: \`$DECISION_LABEL\`
- run suite: \`$RUN_SUITE\`

The suite is intended to run multiple pre-specified DRC settings on the same
frozen candidate manifest. Robust teacher selection should then require the same
teacher path to pass every selected setting.

Plan file:

\`\`\`text
$plan
\`\`\`
EOF

if [[ "$RUN_SUITE" == "true" ]]; then
  echo "[DRC-SENSITIVITY] selecting robust teachers"
  "$PY" "$ROOT/scripts/select_drc_robust_teacher.py" \
    --search-roots "${roots[@]}" \
    --require-return-data \
    --require-stat-gate \
    --require-content-gate \
    --out-json "$OUT_ROOT/robust_frozen_teacher_manifest.json" \
    --out-md "$OUT_ROOT/robust_frozen_teacher_manifest.md"
else
  cat <<EOF
[DRC-SENSITIVITY] dry run complete.

Plan:
  $plan

To execute the suite:

  RUN_SUITE=true \\
  RUN_MAPS="$RUN_MAPS" \\
  CANDIDATE_MANIFEST="$CANDIDATE_MANIFEST" \\
  BUFFER_ROOT=<formal_buffer_root> \\
  bash "$ROOT/scripts/run_drc_sensitivity_suite.sh"
EOF
fi
