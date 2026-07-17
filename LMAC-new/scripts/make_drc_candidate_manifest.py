#!/usr/bin/env python3
"""Create a frozen DRC candidate manifest from LLM communication code files."""

import argparse
import ast
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
DEFAULT_CANDIDATE_ROOT = ROOT / "src" / "llm_source" / "LMAC_deepseek-v4-flash_MSE_0.05"


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inspect_python(path):
    text = Path(path).read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(path))
    functions = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    return {
        "has_communication": "communication" in functions,
        "has_communication_matrix": "communication_matrix" in functions,
        "has_message_design_instruction": "message_design_instruction" in functions,
        "top_level_functions": sorted(functions),
    }


def default_current_path(candidate_root, map_name):
    return candidate_root / map_name / "comm_init.py"


def discover_candidate_paths(candidate_root, map_name):
    current = default_current_path(candidate_root, map_name)
    if current.exists():
        yield "current", current, "default_current"

    candidate_dir = candidate_root / f"{map_name}_candidates"
    if not candidate_dir.exists():
        return
    for path in sorted(candidate_dir.glob("*/comm_init.py")):
        yield path.parent.name, path, "candidate_dir"


def task_fact_count(map_name):
    from components.certified_task_facts import map_specs

    spec = map_specs()[map_name]
    return len(spec.get("required_task_facts", []))


def build_manifest(args):
    from components.certified_task_facts import map_specs

    candidate_root = Path(args.candidate_root).resolve()
    maps = args.maps or sorted(map_specs())
    unknown = sorted(set(maps) - set(map_specs()))
    if unknown:
        raise ValueError(f"Unknown maps: {unknown}")

    rows = []
    seen = set()
    for map_name in maps:
        for label, path, source in discover_candidate_paths(candidate_root, map_name):
            if args.exclude_current and label == "current":
                continue
            rel_path = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
            key = (map_name, label, str(rel_path))
            if key in seen:
                continue
            seen.add(key)
            static = inspect_python(path)
            valid = static["has_communication"] and static["has_communication_matrix"]
            rows.append(
                {
                    "map": map_name,
                    "label": label,
                    "path": str(rel_path),
                    "source": source,
                    "sha256": sha256_file(path),
                    "required_task_fact_count": task_fact_count(map_name),
                    "static_interface_check": static,
                    "valid_for_drc_search": valid,
                }
            )

    if args.require_valid and any(not row["valid_for_drc_search"] for row in rows):
        bad = [row for row in rows if not row["valid_for_drc_search"]]
        raise SystemExit(f"Invalid candidate interfaces: {bad}")

    canonical_candidates = [
        {k: row[k] for k in ("map", "label", "path", "sha256")}
        for row in rows
    ]
    manifest = {
        "method": "DRC-candidate-manifest-v1",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo_root": str(ROOT),
        "candidate_root": str(candidate_root),
        "maps": maps,
        "candidate_count": len(rows),
        "valid_candidate_count": sum(1 for row in rows if row["valid_for_drc_search"]),
        "freeze_policy": (
            "This manifest freezes the LLM/rule-generated teacher candidate set before "
            "DRC scoring. Teacher search should evaluate all listed valid candidates "
            "under one hashed DRC protocol and should not add candidates after viewing "
            "certificate or RL results."
        ),
        "candidates": rows,
    }
    manifest["manifest_sha256"] = hashlib.sha256(
        json.dumps(
            {
                "method": manifest["method"],
                "maps": manifest["maps"],
                "candidates": canonical_candidates,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    return manifest


def write_markdown(path, manifest):
    lines = [
        "# DRC Candidate Manifest",
        "",
        f"- method: `{manifest['method']}`",
        f"- created at UTC: `{manifest['created_at_utc']}`",
        f"- manifest sha256: `{manifest['manifest_sha256']}`",
        f"- candidate root: `{manifest['candidate_root']}`",
        f"- maps: `{', '.join(manifest['maps'])}`",
        f"- candidates: `{manifest['candidate_count']}`",
        f"- valid candidates: `{manifest['valid_candidate_count']}`",
        "",
        "## Freeze Policy",
        "",
        manifest["freeze_policy"],
        "",
        "## Candidates",
        "",
        "| map | label | valid | facts | source | sha256 | path |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for row in manifest["candidates"]:
        lines.append(
            f"| {row['map']} | {row['label']} | {row['valid_for_drc_search']} | "
            f"{row['required_task_fact_count']} | {row['source']} | "
            f"`{row['sha256'][:12]}` | `{row['path']}` |"
        )
    lines += [
        "",
        "## Interface Check",
        "",
        "A candidate is valid for DRC search only if static AST inspection finds both "
        "`communication(o)` and `communication_matrix(o)`. The manifest generator "
        "does not import or execute candidate code.",
    ]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Freeze DRC teacher candidates into a JSON manifest.")
    parser.add_argument("--candidate-root", default=str(DEFAULT_CANDIDATE_ROOT))
    parser.add_argument("--maps", nargs="+", default=None)
    parser.add_argument("--exclude-current", action="store_true")
    parser.add_argument("--require-valid", action="store_true")
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", default=None)
    args = parser.parse_args()

    manifest = build_manifest(args)
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if args.out_md:
        Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
        write_markdown(args.out_md, manifest)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
