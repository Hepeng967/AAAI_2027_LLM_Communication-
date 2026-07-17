"""Lightweight self-tests for the HL communication workflow.

These tests avoid StarCraft, buffers, network calls, and torch-dependent
validation so they can run in a minimal Python environment.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from .api_client import DeepSeekClient
from .candidate_io import extract_code_block
from .ledger import append_trial, read_trials, refresh_outputs


def main() -> None:
    test_extract_code_block()
    test_dry_run_client()
    test_ledger_outputs()
    print("hl_comm self-test passed")


def test_extract_code_block() -> None:
    md = "before\n```python\nimport torch as th\n\ndef f():\n    return 1\n```\nafter"
    assert "def f" in extract_code_block(md)
    raw = "import torch as th\n\ndef g():\n    return 2\n"
    assert "def g" in extract_code_block(raw)


def test_dry_run_client() -> None:
    client = DeepSeekClient(dry_run=True, api_config="")
    resp = client.chat([{"role": "user", "content": "make code"}], call_type="init_coder")
    assert resp.dry_run
    assert "def communication" in resp.content


def test_ledger_outputs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        trials = root / "trials.jsonl"
        summary = root / "summary.csv"
        report = root / "final_report.md"
        append_trial(
            trials,
            {
                "map_name": "1o_2r_vs_4r",
                "iteration": 0,
                "candidate": "comm_init.py",
                "stage": "dry_run",
                "valid": "",
                "accepted": False,
                "status": "dry_run_prompt_ready",
            },
        )
        refresh_outputs(trials, summary, report)
        assert len(read_trials(trials)) == 1
        assert "1o_2r_vs_4r" in summary.read_text(encoding="utf-8")
        assert "HL Communication" in report.read_text(encoding="utf-8")


if __name__ == "__main__":
    main()

