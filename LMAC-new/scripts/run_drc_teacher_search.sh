#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/hp/anaconda3/envs/LMAC/bin/python}"
STAMP="${STAMP:-$(date -u +%Y%m%d_%H%M%S)}"
OUT_ROOT="${OUT_ROOT:-$ROOT/description/certification_gate/drc_teacher_search_$STAMP}"
BUFFER_ROOT="${BUFFER_ROOT:-$ROOT/data}"
MAX_FILES="${MAX_FILES:-128}"
MAX_TRANSITIONS="${MAX_TRANSITIONS:-4096}"
PROBE_EPOCHS="${PROBE_EPOCHS:-80}"
PROBE_MODEL="${PROBE_MODEL:-linear}"
PROBE_HIDDEN_DIM="${PROBE_HIDDEN_DIM:-128}"
PROBE_WEIGHT_DECAY="${PROBE_WEIGHT_DECAY:-0.0001}"
RUN_MAPS="${RUN_MAPS:-1o_10b_vs_1r 1o_2r_vs_4r 5z_vs_1ul}"
DECISION_ORACLE="${DECISION_ORACLE:-auto}"
DECISION_LABEL="${DECISION_LABEL:-raw_action}"
N_BOOTSTRAP="${N_BOOTSTRAP:-200}"
N_SIGN_PERMUTATIONS="${N_SIGN_PERMUTATIONS:-200}"
STAT_ALPHA="${STAT_ALPHA:-0.05}"
REQUIRE_STAT_SIGNIFICANCE="${REQUIRE_STAT_SIGNIFICANCE:-false}"
N_MESSAGE_SHUFFLES="${N_MESSAGE_SHUFFLES:-8}"
REQUIRE_CONTENT_CONTROL="${REQUIRE_CONTENT_CONTROL:-false}"
MIN_RECEIVER_NECESSITY_RATE="${MIN_RECEIVER_NECESSITY_RATE:-1.0}"
MIN_CONDITIONAL_DECISION_NATS="${MIN_CONDITIONAL_DECISION_NATS:-0.01}"
CONDITIONAL_DECISION_MODE="${CONDITIONAL_DECISION_MODE:-none}"
CONDITIONAL_DECISION_QUANTILE="${CONDITIONAL_DECISION_QUANTILE:-0.25}"
MIN_CONDITIONAL_DECISION_SAMPLES="${MIN_CONDITIONAL_DECISION_SAMPLES:-256}"
SCORE_GAIN_CAP="${SCORE_GAIN_CAP:-1.0}"
CANDIDATE_MANIFEST="${CANDIDATE_MANIFEST:-}"
FACT_SUBSET_MANIFEST="${FACT_SUBSET_MANIFEST:-}"

FACT_SUBSET_ARGS=()
if [[ -n "$FACT_SUBSET_MANIFEST" ]]; then
  FACT_SUBSET_ARGS=(--fact-subset-manifest "$FACT_SUBSET_MANIFEST")
fi

mkdir -p "$OUT_ROOT"

run_one() {
  local map="$1"
  local label="$2"
  local comm_code="$3"
  local safe_label
  safe_label="$(echo "$label" | tr '/: ' '___')"
  "$PY" "$ROOT/scripts/certify_decision_relevant_comm.py" \
    --map "$map" \
    --comm-code "$comm_code" \
    --buffer-root "$BUFFER_ROOT" \
    --max-files "$MAX_FILES" \
    --max-transitions "$MAX_TRANSITIONS" \
    --probe-epochs "$PROBE_EPOCHS" \
    --probe-model "$PROBE_MODEL" \
    --probe-hidden-dim "$PROBE_HIDDEN_DIM" \
    --probe-weight-decay "$PROBE_WEIGHT_DECAY" \
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
    --stat-alpha "$STAT_ALPHA" \
    --n-message-shuffles "$N_MESSAGE_SHUFFLES" \
    "${FACT_SUBSET_ARGS[@]}" \
    $(if [[ "$REQUIRE_STAT_SIGNIFICANCE" == "true" ]]; then echo "--require-stat-significance"; fi) \
    $(if [[ "$REQUIRE_CONTENT_CONTROL" == "true" ]]; then echo "--require-content-control"; fi) \
    --out-json "$OUT_ROOT/${map}_${safe_label}.json" \
    --out-md "$OUT_ROOT/${map}_${safe_label}.md"
}

"$PY" "$ROOT/scripts/list_drc_candidates.py" \
  --maps $RUN_MAPS \
  --candidate-manifest "$CANDIDATE_MANIFEST" \
  --extra-candidates "${EXTRA_CANDIDATES:-}" \
  --include-defaults \
  > "$OUT_ROOT/candidates.tsv"

while IFS=$'\t' read -r map label path; do
  [[ -z "${map:-}" ]] && continue
  run_one "$map" "$label" "$path"
done < "$OUT_ROOT/candidates.tsv"

"$PY" - "$OUT_ROOT" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
rows = []
for path in sorted(root.glob("*.json")):
    with path.open() as f:
        item = json.load(f)
    rows.append({
        "file": path.name,
        "map": item["map_name"],
        "accepted": item["accepted"],
        "stat_gate": item.get("passes_statistical_gate"),
        "content_gate": item.get("passes_content_gate"),
        "oracle": item.get("decision_sufficiency", {}).get("oracle_kind"),
        "decision_label": item.get("decision_sufficiency", {}).get("decision_label"),
        "probe_model": item.get("decision_sufficiency", {}).get("probe_model"),
        "return_data": item.get("has_return_data"),
        "score": item["scores"]["final_score"],
        "decision_gain": item["scores"]["decision_sufficiency_gain"],
        "decision_p": item.get("decision_sufficiency", {}).get("ce_gain_resampling", {}).get("p_value_positive"),
        "shuffle_delta": item.get("decision_sufficiency", {}).get("content_specificity", {}).get("shuffle_minus_true_ce"),
        "shuffle_p": item.get("decision_sufficiency", {}).get("content_specificity", {}).get("shuffle_minus_true_resampling", {}).get("p_value_positive"),
        "causal": item["scores"]["causal_usefulness"],
        "causal_p": item.get("causal_usefulness", {}).get("mean_causal_ce_resampling", {}).get("p_value_positive"),
        "edge_rate": item["matrix_edge_rate"],
        "teacher": item["comm_code"],
    })
rows.sort(key=lambda r: (r["map"], not r["accepted"], -r["score"]))
summary = root / "summary.md"

def fmt(value):
    return "n/a" if value is None else f"{value:.4f}"

with summary.open("w") as f:
    f.write("# DRC Teacher Search Summary\n\n")
    f.write("| map | accepted | stat_gate | content_gate | oracle | decision_label | probe | return_data | score | decision_gain | decision_p | shuffle_delta | shuffle_p | causal | causal_p | edge_rate | file |\n")
    f.write("| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |\n")
    for r in rows:
        f.write(
            f"| {r['map']} | {r['accepted']} | {r['stat_gate']} | {r['content_gate']} | {r['oracle']} | {r['decision_label']} | {r['probe_model']} | {r['return_data']} | "
            f"{r['score']:.4f} | {r['decision_gain']:.4f} | "
            f"{fmt(r['decision_p'])} | {fmt(r['shuffle_delta'])} | {fmt(r['shuffle_p'])} | "
            f"{r['causal']:.4f} | {fmt(r['causal_p'])} | "
            f"{r['edge_rate']:.4f} | {r['file']} |\n"
        )
print(summary)
PY

echo "DRC teacher search written to: $OUT_ROOT"
