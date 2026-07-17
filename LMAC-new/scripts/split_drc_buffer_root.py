#!/usr/bin/env python3
"""Split formal DRC buffers into calibration and certification roots.

Calibration buffers can be used to derive a receiver-necessity fact subset or
LLM revision prompts. Certification buffers are then held out for final teacher
certification, avoiding double dipping.
"""

import argparse
import hashlib
import json
import os
import pickle
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from components.certified_task_facts import map_specs  # noqa: E402


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_files(root, map_name):
    base = Path(root)
    files = sorted((base / map_name).glob("**/*.pkl"))
    if not files:
        files = sorted(base.glob(f"**/{map_name}/**/*.pkl"))
    return files


def load_metadata(path):
    try:
        with Path(path).open("rb") as f:
            item = pickle.load(f)
    except Exception as exc:
        return {}, f"pickle_load_failed:{exc}"
    metadata = item.get("metadata")
    if not isinstance(metadata, dict):
        return {}, "metadata_missing"
    return metadata, ""


def place_file(src, dst, mode):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    if mode == "copy":
        shutil.copy2(src, dst)
        return "copy"
    if mode == "symlink":
        os.symlink(src.resolve(), dst)
        return "symlink"
    try:
        os.link(src, dst)
        return "hardlink"
    except OSError:
        shutil.copy2(src, dst)
        return "copy_fallback"


def relative_destination(root, map_name, split_name, source):
    if split_name == "test":
        return Path(root) / map_name / "test" / source.name
    return Path(root) / map_name / source.name


def split_buffers(args):
    specs = map_specs()
    calibration_splits = set(args.calibration_splits)
    certification_splits = set(args.certification_splits)
    result = {
        "method": "DRC-buffer-calibration-certification-split-v1",
        "source_root": str(args.buffer_root),
        "out_root": str(args.out_root),
        "calibration_root": str(Path(args.out_root) / "calibration"),
        "certification_root": str(Path(args.out_root) / "certification"),
        "calibration_splits": sorted(calibration_splits),
        "certification_splits": sorted(certification_splits),
        "link_mode_requested": args.link_mode,
        "maps": {},
    }

    for map_name in args.maps:
        if map_name not in specs:
            raise ValueError(f"Unknown map {map_name}; expected one of {sorted(specs)}")
        rows = []
        counts = {
            "calibration": 0,
            "certification": 0,
            "ignored": 0,
            "metadata_failed": 0,
        }
        for src in find_files(args.buffer_root, map_name):
            metadata, issue = load_metadata(src)
            if issue:
                counts["metadata_failed"] += 1
                rows.append({"source": str(src), "issue": issue, "target": "metadata_failed"})
                continue
            split_name = metadata.get("split")
            if split_name in calibration_splits:
                target = "calibration"
                dst = relative_destination(result["calibration_root"], map_name, split_name, src)
            elif split_name in certification_splits:
                target = "certification"
                dst = relative_destination(result["certification_root"], map_name, split_name, src)
            else:
                counts["ignored"] += 1
                rows.append(
                    {
                        "source": str(src),
                        "metadata_split": split_name,
                        "target": "ignored",
                        "sha256": sha256_file(src),
                    }
                )
                continue

            actual_mode = place_file(src, dst, args.link_mode)
            counts[target] += 1
            rows.append(
                {
                    "source": str(src),
                    "destination": str(dst),
                    "target": target,
                    "metadata_split": split_name,
                    "metadata_seed": metadata.get("seed"),
                    "metadata_episode_index": metadata.get("episode_index"),
                    "sha256": sha256_file(src),
                    "link_mode": actual_mode,
                }
            )

        result["maps"][map_name] = {
            "counts": counts,
            "files": rows,
            "ready": counts["calibration"] > 0 and counts["certification"] > 0,
        }
    result["ready"] = all(row["ready"] for row in result["maps"].values())
    return result


def write_md(path, result):
    lines = [
        "# DRC Buffer Calibration/Certification Split",
        "",
        f"- source root: `{result['source_root']}`",
        f"- calibration root: `{result['calibration_root']}`",
        f"- certification root: `{result['certification_root']}`",
        f"- ready: `{result['ready']}`",
        "",
        "| map | calibration | certification | ignored | metadata_failed | ready |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for map_name, item in result["maps"].items():
        c = item["counts"]
        lines.append(
            f"| {map_name} | {c['calibration']} | {c['certification']} | "
            f"{c['ignored']} | {c['metadata_failed']} | {item['ready']} |"
        )
    lines.extend(
        [
            "",
            "## Protocol Note",
            "",
            "Use the calibration root for fact-subset derivation and LLM revision diagnostics. "
            "Use the certification root for the final formal DRC teacher selection run.",
        ]
    )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Split DRC buffers into calibration and certification roots.")
    parser.add_argument("--buffer-root", required=True)
    parser.add_argument("--maps", nargs="+", default=["1o_10b_vs_1r", "1o_2r_vs_4r", "5z_vs_1ul"])
    parser.add_argument("--out-root", required=True)
    parser.add_argument("--calibration-splits", nargs="+", default=["train"])
    parser.add_argument("--certification-splits", nargs="+", default=["test"])
    parser.add_argument("--link-mode", choices=["hardlink", "copy", "symlink"], default="hardlink")
    parser.add_argument("--out-json", default="")
    parser.add_argument("--out-md", default="")
    args = parser.parse_args()

    result = split_buffers(args)
    out_json = Path(args.out_json) if args.out_json else Path(args.out_root) / "split_manifest.json"
    out_md = Path(args.out_md) if args.out_md else Path(args.out_root) / "split_manifest.md"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_md(out_md, result)
    print(json.dumps({"ready": result["ready"], "out_json": str(out_json), "out_md": str(out_md)}, indent=2))
    if not result["ready"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
