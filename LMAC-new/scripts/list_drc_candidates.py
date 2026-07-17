#!/usr/bin/env python3
"""List DRC teacher candidates from defaults, JSON manifest, and extra TSV."""

import argparse
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
    path = base / "comm_init.py"
    return {"map": map_name, "label": "current", "path": str(path)}


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


def load_manifest(path):
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


def main():
    parser = argparse.ArgumentParser(description="List DRC candidates as TSV.")
    parser.add_argument("--maps", nargs="+", required=True)
    parser.add_argument("--candidate-manifest", default="")
    parser.add_argument("--extra-candidates", default="")
    parser.add_argument("--include-defaults", action="store_true")
    args = parser.parse_args()

    requested = set(args.maps)
    rows = []
    if args.include_defaults:
        rows.extend(default_candidate(map_name) for map_name in args.maps)
    rows.extend(load_manifest(args.candidate_manifest))
    rows.extend(parse_extra_candidates(args.extra_candidates))

    seen = set()
    for row in rows:
        if row["map"] not in requested:
            continue
        key = (row["map"], row["label"], normalize_path(row["path"]))
        if key in seen:
            continue
        seen.add(key)
        print(f"{row['map']}\t{row['label']}\t{row['path']}")


if __name__ == "__main__":
    main()
