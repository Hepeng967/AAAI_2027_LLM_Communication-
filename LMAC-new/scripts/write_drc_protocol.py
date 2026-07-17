#!/usr/bin/env python3
"""Write a hashed DRC protocol snapshot before formal teacher selection."""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def normalize_path(path):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    try:
        return str(p.resolve())
    except FileNotFoundError:
        return str(p.absolute())


def default_candidate(map_name):
    base = ROOT / "src" / "llm_source" / "LMAC_deepseek-v4-flash_MSE_0.05" / map_name
    return str(base / "comm_init.py")


def parse_extra_candidates(text):
    rows = []
    if not text:
        return rows
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            raise ValueError("EXTRA_CANDIDATES rows must be map<TAB>label<TAB>path")
        rows.append({"map": parts[0], "label": parts[1], "path": parts[2]})
    return rows


def load_candidate_manifest(path):
    if not path:
        return []
    manifest = json.loads(Path(path).read_text())
    rows = manifest.get("candidates", manifest if isinstance(manifest, list) else [])
    out = []
    for row in rows:
        if not all(k in row for k in ("map", "label", "path")):
            raise ValueError(f"Candidate rows require map, label, path: {row}")
        out.append({"map": row["map"], "label": row["label"], "path": row["path"]})
    return out


def canonical_hash(protocol):
    payload = json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def dedupe_candidates(candidates):
    out = []
    seen = set()
    for row in candidates:
        key = (row["map"], row["label"], normalize_path(row["path"]))
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def main():
    parser = argparse.ArgumentParser(description="Write DRC formal protocol snapshot.")
    parser.add_argument("--buffer-root", required=True)
    parser.add_argument("--maps", nargs="+", required=True)
    parser.add_argument("--audit-max-files", type=int, required=True)
    parser.add_argument("--max-files", type=int, required=True)
    parser.add_argument("--max-transitions", type=int, required=True)
    parser.add_argument("--probe-model", required=True)
    parser.add_argument("--probe-hidden-dim", type=int, required=True)
    parser.add_argument("--probe-weight-decay", type=float, required=True)
    parser.add_argument("--probe-epochs", type=int, required=True)
    parser.add_argument("--decision-oracle", required=True)
    parser.add_argument("--decision-label", choices=["raw_action", "action_group"], default="raw_action")
    parser.add_argument("--min-conditional-decision-nats", type=float, required=True)
    parser.add_argument(
        "--conditional-decision-mode",
        choices=["none", "local_entropy", "local_loss"],
        default="none",
    )
    parser.add_argument("--conditional-decision-quantile", type=float, default=0.25)
    parser.add_argument("--min-conditional-decision-samples", type=int, default=256)
    parser.add_argument("--min-receiver-necessity-rate", type=float, required=True)
    parser.add_argument("--score-gain-cap", type=float, default=1.0)
    parser.add_argument("--n-bootstrap", type=int, required=True)
    parser.add_argument("--n-sign-permutations", type=int, required=True)
    parser.add_argument("--n-message-shuffles", type=int, required=True)
    parser.add_argument("--stat-alpha", type=float, required=True)
    parser.add_argument("--require-stat-significance", action="store_true")
    parser.add_argument("--require-content-control", action="store_true")
    parser.add_argument("--candidate-manifest", default="")
    parser.add_argument("--fact-subset-manifest", default="")
    parser.add_argument("--extra-candidates", default="")
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", default=None)
    args = parser.parse_args()

    default_candidates = [
        {"map": map_name, "label": "current", "path": default_candidate(map_name)}
        for map_name in args.maps
    ]
    candidates = default_candidates + load_candidate_manifest(args.candidate_manifest) + parse_extra_candidates(args.extra_candidates)
    requested = set(args.maps)
    candidates = dedupe_candidates([row for row in candidates if row["map"] in requested])
    protocol = {
        "method": "DRC-v5-formal-protocol",
        "repo_root": str(ROOT),
        "buffer_root": str(args.buffer_root),
        "maps": args.maps,
        "audit": {"max_files": args.audit_max_files},
        "certification": {
            "max_files": args.max_files,
            "max_transitions": args.max_transitions,
            "probe_model": args.probe_model,
            "probe_hidden_dim": args.probe_hidden_dim,
            "probe_weight_decay": args.probe_weight_decay,
            "probe_epochs": args.probe_epochs,
            "decision_oracle": args.decision_oracle,
            "decision_label": args.decision_label,
            "min_conditional_decision_nats": args.min_conditional_decision_nats,
            "conditional_decision_mode": args.conditional_decision_mode,
            "conditional_decision_quantile": args.conditional_decision_quantile,
            "min_conditional_decision_samples": args.min_conditional_decision_samples,
            "min_receiver_necessity_rate": args.min_receiver_necessity_rate,
            "score_gain_cap": args.score_gain_cap,
            "n_bootstrap": args.n_bootstrap,
            "n_sign_permutations": args.n_sign_permutations,
            "n_message_shuffles": args.n_message_shuffles,
            "stat_alpha": args.stat_alpha,
            "require_stat_significance": args.require_stat_significance,
            "require_content_control": args.require_content_control,
        },
        "selection": {
            "require_return_data": True,
            "require_stat_gate": True,
            "require_content_gate": True,
            "rank_by": "scores.final_score",
            "tie_break": "lower matrix_edge_rate",
        },
        "candidate_manifest": args.candidate_manifest,
        "fact_subset_manifest": args.fact_subset_manifest,
        "candidates": candidates,
    }
    protocol["protocol_sha256"] = canonical_hash(protocol)

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(protocol, indent=2) + "\n")

    if args.out_md:
        lines = [
            "# DRC Formal Protocol Snapshot",
            "",
            f"- protocol sha256: `{protocol['protocol_sha256']}`",
            f"- buffer root: `{protocol['buffer_root']}`",
            f"- maps: `{', '.join(protocol['maps'])}`",
            f"- fact subset manifest: `{protocol['fact_subset_manifest'] or 'none'}`",
            "",
            "## Certification Settings",
            "",
        ]
        for key, value in protocol["certification"].items():
            lines.append(f"- `{key}`: `{value}`")
        lines += [
            "",
            "## Candidates",
            "",
            "| map | label | path |",
            "| --- | --- | --- |",
        ]
        for item in protocol["candidates"]:
            lines.append(f"| {item['map']} | {item['label']} | `{item['path']}` |")
        Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out_md).write_text("\n".join(lines) + "\n")

    print(json.dumps(protocol, indent=2))


if __name__ == "__main__":
    main()
