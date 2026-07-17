#!/usr/bin/env python3
"""Generate a student-RL launch plan from a frozen DRC teacher manifest."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

IMPORTANT_STATE = {
    "1o_10b_vs_1r": "[62, 63, 67, 68]",
    "5z_vs_1ul": "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]",
    "1o_2r_vs_4r": "[0, 1, 2, 3, 6, 7, 8, 9, 12, 13, 14, 15, 18, 19, 20, 23, 24, 25, 28, 29, 30, 33, 34, 35]",
}


def resolve(path):
    p = Path(path)
    return p if p.is_absolute() else ROOT / p


def main():
    parser = argparse.ArgumentParser(description="Plan teacher-student RL runs from frozen teacher manifest.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--seeds", nargs="+", type=int, default=[2026061700, 2026061701, 2026061702])
    parser.add_argument("--out-md", default=None)
    args = parser.parse_args()

    manifest_path = resolve(args.manifest)
    manifest = json.loads(manifest_path.read_text())
    rows = []
    for map_name, item in sorted(manifest.get("teachers", {}).items()):
        teacher = resolve(item["teacher_path"])
        if not teacher.exists():
            raise SystemExit(f"Teacher path for {map_name} does not exist: {teacher}")
        for seed_idx, seed in enumerate(args.seeds):
            rows.append(
                {
                    "map": map_name,
                    "seed_idx": seed_idx,
                    "seed": seed,
                    "comm_code_paths": json.dumps([str(teacher)]),
                    "important_state": IMPORTANT_STATE.get(map_name, "[]"),
                }
            )

    lines = [
        "# Teacher-Student RL Plan from DRC Manifest",
        "",
        f"- manifest: `{manifest_path}`",
        f"- maps: `{len(manifest.get('teachers', {}))}`",
        f"- runs: `{len(rows)}`",
        "",
        "| map | seed_idx | seed | important_state | comm_code_paths |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['map']} | {row['seed_idx']} | {row['seed']} | "
            f"`{row['important_state']}` | `{row['comm_code_paths']}` |"
        )
    text = "\n".join(lines) + "\n"
    if args.out_md:
        out = Path(args.out_md)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
