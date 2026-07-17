#!/usr/bin/env python3
"""Call DeepSeek/OpenAI-compatible LLM to revise DRC teacher communication code."""

import argparse
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

import torch as th


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from components.certified_task_facts import map_specs  # noqa: E402


def resolve(path):
    p = Path(path)
    return p if p.is_absolute() else ROOT / p


def extract_code_block(text):
    matches = re.findall(r"```(?:python)?\n([\s\S]*?)```", text)
    if matches:
        return matches[0].strip() + "\n"
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("def "):
            start = idx
            break
    if start is None:
        raise RuntimeError("LLM response did not contain executable Python code.")
    return "\n".join(lines[start:]).strip() + "\n"


def load_module(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_candidate(path, map_name):
    spec = map_specs()[map_name]
    module = load_module(path)
    missing = [name for name in ("message_design_instruction", "communication", "communication_matrix") if not hasattr(module, name)]
    if missing:
        raise RuntimeError(f"Candidate is missing required functions: {missing}")

    b = 4
    n = spec["n_agents"]
    d = spec["obs_dim"]
    obs = th.zeros(b, n, d)
    obs[:, :, : min(d, 8)] = th.rand(b, n, min(d, 8))
    enhanced = module.communication(obs)
    if not th.is_tensor(enhanced):
        enhanced = th.as_tensor(enhanced)
    if enhanced.dim() != 3 or tuple(enhanced.shape[:2]) != (b, n) or enhanced.shape[-1] < d:
        raise RuntimeError(f"communication(o) returned invalid shape {tuple(enhanced.shape)} for obs {(b, n, d)}")

    matrix = module.communication_matrix(obs)
    if not th.is_tensor(matrix):
        matrix = th.as_tensor(matrix)
    if matrix.dim() == 4:
        matrix = matrix.mean(dim=-1)
    if tuple(matrix.shape) != (b, n, n):
        raise RuntimeError(f"communication_matrix(o) returned invalid shape {tuple(matrix.shape)}; expected {(b, n, n)}")
    diag = matrix[:, th.arange(n), th.arange(n)].abs().max().item()
    if diag > 1e-6:
        raise RuntimeError("communication_matrix(o) must have zero self-communication diagonal.")
    return {
        "message_dim": int(enhanced.shape[-1] - d),
        "matrix_edge_rate": float(matrix.sum().item() / max(b * n * (n - 1), 1)),
    }


def build_prompt(feedback, source_code):
    return f"""You are revising a teacher communication policy for a MARL DRC pipeline.

Use only the structured DRC feedback below. Do not use downstream RL win-rate,
training curves, reward logs, global state, file I/O, randomness, or trainable
parameters.

Revision target:
- `decision_sufficient_feedback` edits `communication(o)` for what/content.
- `causally_useful_feedback` edits `communication_matrix(o)` for who/when.
- Keep sender-observable and receiver-necessary checks as internal constraints.

Return only executable Python code defining:

```python
import torch as th

def message_design_instruction():
    ...

def communication(o):
    ...

def communication_matrix(o):
    ...
```

Structured DRC feedback:
```json
{json.dumps(feedback, indent=2, ensure_ascii=False)}
```

Current source teacher code:
```python
{source_code}
```
"""


def call_openai_compatible(prompt, args):
    try:
        from openai import OpenAI
    except Exception as exc:
        raise RuntimeError("The openai package is required for DeepSeek/OpenAI-compatible calls.") from exc

    api_key = args.api_key or os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("No API key found. Set DEEPSEEK_API_KEY or pass --api-key.")
    client = OpenAI(api_key=api_key, base_url=args.base_url)
    kwargs = {
        "model": args.model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "temperature": args.temperature,
    }
    if args.reasoning_effort:
        kwargs["reasoning_effort"] = args.reasoning_effort
    if args.deepseek_thinking:
        kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
    resp = client.chat.completions.create(**kwargs)
    usage = {}
    if getattr(resp, "usage", None) is not None:
        usage = {
            "prompt_tokens": getattr(resp.usage, "prompt_tokens", None),
            "completion_tokens": getattr(resp.usage, "completion_tokens", None),
            "total_tokens": getattr(resp.usage, "total_tokens", None),
        }
    return resp.choices[0].message.content, usage


def main():
    parser = argparse.ArgumentParser(description="Call an LLM to revise a DRC communication teacher.")
    parser.add_argument("--feedback-json", required=True)
    parser.add_argument("--source-code", default="", help="Current comm_init.py. Defaults to feedback source_teacher.")
    parser.add_argument("--destination-file", default="", help="Output comm_init.py. Defaults to feedback destination_file.")
    parser.add_argument("--prompt-out", required=True)
    parser.add_argument("--raw-response-out", default="")
    parser.add_argument("--metadata-out", required=True)
    parser.add_argument("--model", default="deepseek-v4-flash")
    parser.add_argument("--base-url", default=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"))
    parser.add_argument("--api-key", default="")
    parser.add_argument("--reasoning-effort", default=os.environ.get("DEEPSEEK_REASONING_EFFORT", ""))
    parser.add_argument("--deepseek-thinking", action="store_true")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--dry-run", action="store_true", help="Only write prompt and metadata; do not call LLM.")
    parser.add_argument("--validate-only", action="store_true", help="Validate an existing destination file.")
    args = parser.parse_args()

    feedback = json.loads(resolve(args.feedback_json).read_text(encoding="utf-8"))
    map_name = feedback["map_name"]
    source_path = resolve(args.source_code or feedback["source_teacher"])
    destination = resolve(args.destination_file or feedback["destination_file"])
    source_code = source_path.read_text(encoding="utf-8")
    prompt = build_prompt(feedback, source_code)

    prompt_out = resolve(args.prompt_out)
    prompt_out.parent.mkdir(parents=True, exist_ok=True)
    prompt_out.write_text(prompt, encoding="utf-8")

    metadata = {
        "method": "DRC-LLM-revision-call-v1",
        "feedback_json": str(resolve(args.feedback_json)),
        "source_code": str(source_path),
        "destination_file": str(destination),
        "map_name": map_name,
        "model": args.model,
        "base_url": args.base_url,
        "dry_run": args.dry_run,
        "prompt_out": str(prompt_out),
    }

    if args.validate_only:
        metadata["validation"] = validate_candidate(destination, map_name)
    elif args.dry_run:
        metadata["status"] = "dry_run_prompt_written"
    else:
        raw_text, usage = call_openai_compatible(prompt, args)
        raw_out = resolve(args.raw_response_out) if args.raw_response_out else destination.with_suffix(".raw_response.md")
        raw_out.parent.mkdir(parents=True, exist_ok=True)
        raw_out.write_text(raw_text, encoding="utf-8")
        code = extract_code_block(raw_text)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(code, encoding="utf-8")
        metadata["raw_response_out"] = str(raw_out)
        metadata["usage"] = usage
        metadata["validation"] = validate_candidate(destination, map_name)
        metadata["status"] = "candidate_written_and_validated"

    metadata_out = resolve(args.metadata_out)
    metadata_out.parent.mkdir(parents=True, exist_ok=True)
    metadata_out.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
