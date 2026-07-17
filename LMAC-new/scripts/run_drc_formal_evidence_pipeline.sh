#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"
STAMP="${STAMP:-$(date -u +%Y%m%d_%H%M%S)}"
OUT_ROOT="${OUT_ROOT:-$ROOT/description/certification_gate/drc_formal_evidence_$STAMP}"

RUN_MODE="${RUN_MODE:-dry_run}"  # dry_run | preflight | execute
RUN_MAPS="${RUN_MAPS:-1o_10b_vs_1r 1o_2r_vs_4r 5z_vs_1ul}"
COLLECT_MAPS="${COLLECT_MAPS:-10b 2r 5z}"
CANDIDATE_ROOT="${CANDIDATE_ROOT:-$ROOT/src/llm_source/LMAC_deepseek-v4-flash_MSE_0.05}"
CANDIDATE_MANIFEST="${CANDIDATE_MANIFEST:-$OUT_ROOT/drc_candidates.json}"
CANDIDATE_MANIFEST_MD="${CANDIDATE_MANIFEST_MD:-$OUT_ROOT/drc_candidates.md}"
FACT_SUBSET_MANIFEST="${FACT_SUBSET_MANIFEST:-}"
PROMPT_DIR="${PROMPT_DIR:-$OUT_ROOT/candidate_prompts}"
BUFFER_ROOT="${BUFFER_ROOT:-$OUT_ROOT/formal_buffers}"
FORMAL_OUT="${FORMAL_OUT:-$OUT_ROOT/formal_drc_v5}"
PREFLIGHT_OUT="${PREFLIGHT_OUT:-$OUT_ROOT/preflight}"

TRAIN_COUNT="${TRAIN_COUNT:-64}"
TEST_COUNT="${TEST_COUNT:-64}"
SEED="${SEED:-1234}"

AUDIT_MAX_FILES="${AUDIT_MAX_FILES:-64}"
MAX_FILES="${MAX_FILES:-64}"
MAX_TRANSITIONS="${MAX_TRANSITIONS:-4096}"
PROBE_MODEL="${PROBE_MODEL:-mlp}"
PROBE_HIDDEN_DIM="${PROBE_HIDDEN_DIM:-128}"
PROBE_WEIGHT_DECAY="${PROBE_WEIGHT_DECAY:-0.0001}"
PROBE_EPOCHS="${PROBE_EPOCHS:-120}"
DECISION_ORACLE="${DECISION_ORACLE:-auto}"
DECISION_LABEL="${DECISION_LABEL:-raw_action}"
MIN_CONDITIONAL_DECISION_NATS="${MIN_CONDITIONAL_DECISION_NATS:-0.01}"
CONDITIONAL_DECISION_MODE="${CONDITIONAL_DECISION_MODE:-none}"
CONDITIONAL_DECISION_QUANTILE="${CONDITIONAL_DECISION_QUANTILE:-0.25}"
MIN_CONDITIONAL_DECISION_SAMPLES="${MIN_CONDITIONAL_DECISION_SAMPLES:-256}"
MIN_RECEIVER_NECESSITY_RATE="${MIN_RECEIVER_NECESSITY_RATE:-1.0}"
SCORE_GAIN_CAP="${SCORE_GAIN_CAP:-1.0}"
N_BOOTSTRAP="${N_BOOTSTRAP:-500}"
N_SIGN_PERMUTATIONS="${N_SIGN_PERMUTATIONS:-500}"
N_MESSAGE_SHUFFLES="${N_MESSAGE_SHUFFLES:-16}"
STAT_ALPHA="${STAT_ALPHA:-0.05}"
REQUIRE_STAT_SIGNIFICANCE="${REQUIRE_STAT_SIGNIFICANCE:-true}"
REQUIRE_CONTENT_CONTROL="${REQUIRE_CONTENT_CONTROL:-true}"
REQUIRE_METADATA="${REQUIRE_METADATA:-true}"

mkdir -p "$OUT_ROOT"

if [[ "$REQUIRE_STAT_SIGNIFICANCE" == "true" ]]; then
  PREFLIGHT_STAT_ARGS="--require-stat-significance"
else
  PREFLIGHT_STAT_ARGS="--no-require-stat-significance"
fi
if [[ "$REQUIRE_CONTENT_CONTROL" == "true" ]]; then
  PREFLIGHT_CONTENT_ARGS="--require-content-control"
else
  PREFLIGHT_CONTENT_ARGS="--no-require-content-control"
fi
if [[ "$REQUIRE_METADATA" == "true" ]]; then
  PREFLIGHT_METADATA_ARGS="--require-metadata"
else
  PREFLIGHT_METADATA_ARGS="--no-require-metadata"
fi

cat > "$OUT_ROOT/README.md" <<EOF
# DRC Formal Evidence Pipeline

- stamp: \`$STAMP\`
- run mode: \`$RUN_MODE\`
- maps: \`$RUN_MAPS\`
- collect aliases: \`$COLLECT_MAPS\`
- candidate root: \`$CANDIDATE_ROOT\`
- candidate manifest: \`$CANDIDATE_MANIFEST\`
- fact subset manifest: \`${FACT_SUBSET_MANIFEST:-none}\`
- buffer root: \`$BUFFER_ROOT\`
- preflight out: \`$PREFLIGHT_OUT\`
- formal out: \`$FORMAL_OUT\`
- decision label: \`$DECISION_LABEL\`
- conditional decision mode: \`$CONDITIONAL_DECISION_MODE\`
- conditional decision quantile: \`$CONDITIONAL_DECISION_QUANTILE\`
- min conditional decision samples: \`$MIN_CONDITIONAL_DECISION_SAMPLES\`

## Modes

- \`dry_run\`: write this plan only.
- \`preflight\`: generate prompts/manifest and run preflight on an existing buffer root.
- \`execute\`: generate prompts/manifest, collect buffers, run preflight, then run formal DRC.

EOF

cat > "$OUT_ROOT/commands.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail

cd "$ROOT"

# 1. Generate prompts and freeze candidate manifest
RUN_MAPS="$RUN_MAPS" \\
OUT_ROOT="$OUT_ROOT/construction" \\
PROMPT_DIR="$PROMPT_DIR" \\
CANDIDATE_ROOT="$CANDIDATE_ROOT" \\
CANDIDATE_MANIFEST="$CANDIDATE_MANIFEST" \\
CANDIDATE_MANIFEST_MD="$CANDIDATE_MANIFEST_MD" \\
RUN_FORMAL=false \\
bash "$ROOT/scripts/run_drc_teacher_construction.sh"

# 2. Collect formal reward-bearing buffers
MAPS="$COLLECT_MAPS" \\
RUN_MAPS="$RUN_MAPS" \\
TRAIN_COUNT="$TRAIN_COUNT" \\
TEST_COUNT="$TEST_COUNT" \\
SEED="$SEED" \\
OUTPUT_ROOT="$BUFFER_ROOT" \\
AUDIT_OUT="$OUT_ROOT/buffer_collection_audit" \\
bash "$ROOT/scripts/collect_formal_drc_buffers.sh"

# 3. Preflight formal DRC
"$PY" "$ROOT/scripts/preflight_drc_formal_run.py" \\
  --buffer-root "$BUFFER_ROOT" \\
  --candidate-manifest "$CANDIDATE_MANIFEST" \\
  --fact-subset-manifest "$FACT_SUBSET_MANIFEST" \\
  --maps $RUN_MAPS \\
  --out-dir "$PREFLIGHT_OUT" \\
  --formal-out-root "$FORMAL_OUT" \\
  --audit-max-files "$AUDIT_MAX_FILES" \\
  --max-files "$MAX_FILES" \\
  --max-transitions "$MAX_TRANSITIONS" \\
  --probe-model "$PROBE_MODEL" \\
  --probe-hidden-dim "$PROBE_HIDDEN_DIM" \\
  --probe-weight-decay "$PROBE_WEIGHT_DECAY" \\
  --probe-epochs "$PROBE_EPOCHS" \\
  --decision-oracle "$DECISION_ORACLE" \\
  --decision-label "$DECISION_LABEL" \\
  --min-conditional-decision-nats "$MIN_CONDITIONAL_DECISION_NATS" \\
  --conditional-decision-mode "$CONDITIONAL_DECISION_MODE" \\
  --conditional-decision-quantile "$CONDITIONAL_DECISION_QUANTILE" \\
  --min-conditional-decision-samples "$MIN_CONDITIONAL_DECISION_SAMPLES" \\
  --min-receiver-necessity-rate "$MIN_RECEIVER_NECESSITY_RATE" \\
  --score-gain-cap "$SCORE_GAIN_CAP" \\
  --n-bootstrap "$N_BOOTSTRAP" \\
  --n-sign-permutations "$N_SIGN_PERMUTATIONS" \\
  --n-message-shuffles "$N_MESSAGE_SHUFFLES" \\
  --stat-alpha "$STAT_ALPHA" \\
  $PREFLIGHT_STAT_ARGS \\
  $PREFLIGHT_CONTENT_ARGS \\
  $PREFLIGHT_METADATA_ARGS

# 4. Run formal DRC and write dossier
RUN_MAPS="$RUN_MAPS" \\
BUFFER_ROOT="$BUFFER_ROOT" \\
CANDIDATE_MANIFEST="$CANDIDATE_MANIFEST" \\
FACT_SUBSET_MANIFEST="$FACT_SUBSET_MANIFEST" \\
OUT_ROOT="$FORMAL_OUT" \\
AUDIT_MAX_FILES="$AUDIT_MAX_FILES" \\
MAX_FILES="$MAX_FILES" \\
MAX_TRANSITIONS="$MAX_TRANSITIONS" \\
PROBE_MODEL="$PROBE_MODEL" \\
PROBE_HIDDEN_DIM="$PROBE_HIDDEN_DIM" \\
PROBE_WEIGHT_DECAY="$PROBE_WEIGHT_DECAY" \\
PROBE_EPOCHS="$PROBE_EPOCHS" \\
DECISION_ORACLE="$DECISION_ORACLE" \\
DECISION_LABEL="$DECISION_LABEL" \\
MIN_CONDITIONAL_DECISION_NATS="$MIN_CONDITIONAL_DECISION_NATS" \\
CONDITIONAL_DECISION_MODE="$CONDITIONAL_DECISION_MODE" \\
CONDITIONAL_DECISION_QUANTILE="$CONDITIONAL_DECISION_QUANTILE" \\
MIN_CONDITIONAL_DECISION_SAMPLES="$MIN_CONDITIONAL_DECISION_SAMPLES" \\
MIN_RECEIVER_NECESSITY_RATE="$MIN_RECEIVER_NECESSITY_RATE" \\
SCORE_GAIN_CAP="$SCORE_GAIN_CAP" \\
N_BOOTSTRAP="$N_BOOTSTRAP" \\
N_SIGN_PERMUTATIONS="$N_SIGN_PERMUTATIONS" \\
N_MESSAGE_SHUFFLES="$N_MESSAGE_SHUFFLES" \\
STAT_ALPHA="$STAT_ALPHA" \\
REQUIRE_STAT_SIGNIFICANCE="$REQUIRE_STAT_SIGNIFICANCE" \\
REQUIRE_CONTENT_CONTROL="$REQUIRE_CONTENT_CONTROL" \\
bash "$ROOT/scripts/run_formal_drc_v5.sh"
EOF
chmod +x "$OUT_ROOT/commands.sh"

if [[ "$RUN_MODE" == "dry_run" ]]; then
  cat <<EOF
[DRC-EVIDENCE] dry run complete.

Plan:
  $OUT_ROOT/README.md
Commands:
  $OUT_ROOT/commands.sh

To run preflight on an existing buffer root:
  RUN_MODE=preflight BUFFER_ROOT=<formal_buffer_root> OUT_ROOT="$OUT_ROOT" bash "$ROOT/scripts/run_drc_formal_evidence_pipeline.sh"

To execute collection + formal DRC:
  RUN_MODE=execute OUT_ROOT="$OUT_ROOT" bash "$ROOT/scripts/run_drc_formal_evidence_pipeline.sh"
EOF
  exit 0
fi

echo "[DRC-EVIDENCE] generating prompts and freezing candidate manifest"
RUN_MAPS="$RUN_MAPS" \
OUT_ROOT="$OUT_ROOT/construction" \
PROMPT_DIR="$PROMPT_DIR" \
CANDIDATE_ROOT="$CANDIDATE_ROOT" \
CANDIDATE_MANIFEST="$CANDIDATE_MANIFEST" \
CANDIDATE_MANIFEST_MD="$CANDIDATE_MANIFEST_MD" \
RUN_FORMAL=false \
bash "$ROOT/scripts/run_drc_teacher_construction.sh"

if [[ "$RUN_MODE" == "execute" ]]; then
  echo "[DRC-EVIDENCE] collecting formal buffers"
  MAPS="$COLLECT_MAPS" \
  RUN_MAPS="$RUN_MAPS" \
  TRAIN_COUNT="$TRAIN_COUNT" \
  TEST_COUNT="$TEST_COUNT" \
  SEED="$SEED" \
  OUTPUT_ROOT="$BUFFER_ROOT" \
  AUDIT_OUT="$OUT_ROOT/buffer_collection_audit" \
  bash "$ROOT/scripts/collect_formal_drc_buffers.sh"
fi

echo "[DRC-EVIDENCE] running formal preflight"
"$PY" "$ROOT/scripts/preflight_drc_formal_run.py" \
  --buffer-root "$BUFFER_ROOT" \
  --candidate-manifest "$CANDIDATE_MANIFEST" \
  --fact-subset-manifest "$FACT_SUBSET_MANIFEST" \
  --maps $RUN_MAPS \
  --out-dir "$PREFLIGHT_OUT" \
  --formal-out-root "$FORMAL_OUT" \
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
  $PREFLIGHT_STAT_ARGS \
  $PREFLIGHT_CONTENT_ARGS \
  $PREFLIGHT_METADATA_ARGS

if [[ "$RUN_MODE" == "preflight" ]]; then
  echo "[DRC-EVIDENCE] preflight complete: $PREFLIGHT_OUT"
  exit 0
fi

if [[ "$RUN_MODE" != "execute" ]]; then
  echo "Unknown RUN_MODE=$RUN_MODE; expected dry_run, preflight, or execute" >&2
  exit 2
fi

echo "[DRC-EVIDENCE] running formal DRC"
RUN_MAPS="$RUN_MAPS" \
BUFFER_ROOT="$BUFFER_ROOT" \
CANDIDATE_MANIFEST="$CANDIDATE_MANIFEST" \
FACT_SUBSET_MANIFEST="$FACT_SUBSET_MANIFEST" \
OUT_ROOT="$FORMAL_OUT" \
AUDIT_MAX_FILES="$AUDIT_MAX_FILES" \
MAX_FILES="$MAX_FILES" \
MAX_TRANSITIONS="$MAX_TRANSITIONS" \
PROBE_MODEL="$PROBE_MODEL" \
PROBE_HIDDEN_DIM="$PROBE_HIDDEN_DIM" \
PROBE_WEIGHT_DECAY="$PROBE_WEIGHT_DECAY" \
PROBE_EPOCHS="$PROBE_EPOCHS" \
DECISION_ORACLE="$DECISION_ORACLE" \
DECISION_LABEL="$DECISION_LABEL" \
MIN_CONDITIONAL_DECISION_NATS="$MIN_CONDITIONAL_DECISION_NATS" \
CONDITIONAL_DECISION_MODE="$CONDITIONAL_DECISION_MODE" \
CONDITIONAL_DECISION_QUANTILE="$CONDITIONAL_DECISION_QUANTILE" \
MIN_CONDITIONAL_DECISION_SAMPLES="$MIN_CONDITIONAL_DECISION_SAMPLES" \
MIN_RECEIVER_NECESSITY_RATE="$MIN_RECEIVER_NECESSITY_RATE" \
SCORE_GAIN_CAP="$SCORE_GAIN_CAP" \
N_BOOTSTRAP="$N_BOOTSTRAP" \
N_SIGN_PERMUTATIONS="$N_SIGN_PERMUTATIONS" \
N_MESSAGE_SHUFFLES="$N_MESSAGE_SHUFFLES" \
STAT_ALPHA="$STAT_ALPHA" \
REQUIRE_STAT_SIGNIFICANCE="$REQUIRE_STAT_SIGNIFICANCE" \
REQUIRE_CONTENT_CONTROL="$REQUIRE_CONTENT_CONTROL" \
bash "$ROOT/scripts/run_formal_drc_v5.sh"

echo "[DRC-EVIDENCE] complete: $FORMAL_OUT"
