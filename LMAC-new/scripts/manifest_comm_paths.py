#!/usr/bin/env python3
"""Read frozen DRC teacher paths from a manifest for RL launch scripts."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def resolve_path(path):
    p = Path(path)
    if p.is_absolute():
        return p
    return ROOT / p


def main():
    parser = argparse.ArgumentParser(description="Extract comm_code_paths from a frozen teacher manifest.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--map", required=True)
    parser.add_argument("--format", choices=["json-list", "path"], default="json-list")
    args = parser.parse_args()

    manifest_path = resolve_path(args.manifest)
    manifest = json.loads(manifest_path.read_text())
    teachers = manifest.get("teachers", {})
    if args.map not in teachers:
        raise SystemExit(f"Map {args.map} is not present in frozen teacher manifest {manifest_path}")

    teacher_path = teachers[args.map].get("teacher_path")
    if not teacher_path:
        raise SystemExit(f"Manifest entry for {args.map} has no teacher_path")
    resolved = resolve_path(teacher_path)
    if not resolved.exists():
        raise SystemExit(f"Teacher path for {args.map} does not exist: {resolved}")

    if args.format == "path":
        print(str(resolved))
    else:
        print(json.dumps([str(resolved)]))


if __name__ == "__main__":
    main()
