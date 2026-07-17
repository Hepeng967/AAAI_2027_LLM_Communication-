"""HL-style auto-research loop for LMAC communication teachers.

Run from the LMAC-new root with:

    PYTHONPATH=src python -m hl_comm.auto_research --dry-run
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .api_client import DeepSeekClient, LLMResponse
from .candidate_io import (
    candidate_dir,
    validate_candidate,
    write_candidate_from_response,
    write_prompt,
)
from .ledger import append_trial, read_trials, refresh_outputs
from .prompts import (
    DEFAULT_MAPS,
    build_initial_prompt,
    build_llm_judge_prompt,
    build_repair_prompt,
    build_revision_prompt,
    build_summary_prompt,
)
from .rollout_obs import evaluate_candidate_on_rollouts, load_rollout_obs_summary


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from components.certified_task_facts import map_specs  # noqa: E402


def _progress(message: str) -> None:
    print(f"[HL-COMM] {message}", flush=True)


def _short_float(value: Any) -> str:
    try:
        return f"{float(value):.4f}"
    except (TypeError, ValueError):
        return ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run HL-style LMAC communication auto-research.")
    parser.add_argument("--maps", nargs="+", default=DEFAULT_MAPS)
    parser.add_argument("--model", default="deepseek-v4-pro")
    parser.add_argument("--base-url", default="https://api.deepseek.com")
    parser.add_argument("--api-key", default="")
    parser.add_argument("--api-config", default="/data/hp/Skill_RL/new/code/skill/call_LLM/api.py")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--reasoning-effort", default="")
    parser.add_argument("--deepseek-thinking", action="store_true")
    parser.add_argument("--max-iters", type=int, default=5)
    parser.add_argument("--patience", type=int, default=2)
    parser.add_argument("--repair-attempts", type=int, default=3)
    parser.add_argument("--max-transitions", type=int, default=4096)
    parser.add_argument("--max-files", type=int, default=64)
    parser.add_argument("--buffer-root", default=str(ROOT / "data"))
    parser.add_argument("--rollout-root", default=str(ROOT / "data"))
    parser.add_argument("--gate", choices=["llm", "llm_rl"], default="llm")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--output-root", default=str(SRC / "llm_source" / "hl_auto_research"))
    parser.add_argument(
        "--pre-policy-root",
        default=str(SRC / "LLM-Communication-main" / "matrix_code"),
        help="Root containing pre-generated who/when/what priors from LLM-Communication-main.",
    )
    parser.add_argument(
        "--allow-no-prepolicy",
        action="store_true",
        help="Allow iteration to generate iter_000 itself if no seed/pre-policy exists.",
    )
    parser.add_argument("--seed-candidate", action="append", default=[], help="Path or map=path; may be repeated.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--decision-label", default="raw_action")
    parser.add_argument("--conditional-decision-mode", default="local_loss")
    parser.add_argument("--probe-model", default="mlp")
    parser.add_argument("--no-content-control", action="store_true")
    parser.add_argument("--require-stat-significance", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    specs = map_specs()
    # Main capability-boundary experiments must not leak hand-authored answers
    # (designated senders/receivers or required feature indices) to the LLM.
    for spec in specs.values():
        spec.pop("required_task_facts", None)
        spec.pop("task_probes", None)
    unknown = [name for name in args.maps if name not in specs]
    if unknown:
        raise SystemExit(f"Unknown map(s): {unknown}. Available: {sorted(specs)}")

    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    client = DeepSeekClient(
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key,
        api_config=args.api_config,
        temperature=args.temperature,
        reasoning_effort=args.reasoning_effort,
        deepseek_thinking=args.deepseek_thinking,
        dry_run=args.dry_run,
    )
    seed_candidates = _parse_seed_candidates(args.seed_candidate)

    _progress(
        f"start model={client.model} maps={','.join(args.maps)} "
        f"max_iters={args.max_iters} rollout_root={args.rollout_root}"
    )

    for map_name in args.maps:
        run_one_map(args, client, specs[map_name], map_name, run_id, seed_candidates.get(map_name))


def run_one_map(
    args: argparse.Namespace,
    client: DeepSeekClient,
    map_spec: dict[str, Any],
    map_name: str,
    run_id: str,
    seed_candidate: Path | None,
) -> None:
    run_root = Path(args.output_root) / map_name / run_id
    results_dir = run_root / "results"
    judge_dir = results_dir / "judge_outputs"
    trials_path = results_dir / "trials.jsonl"
    summary_path = results_dir / "summary.csv"
    report_path = results_dir / "final_report.md"
    commands_path = results_dir / "commands.sh"
    commands_path.parent.mkdir(parents=True, exist_ok=True)
    commands_path.write_text(_commands_header(args, map_name, run_root), encoding="utf-8")
    _progress(f"map={map_name} run_id={run_id} output={run_root}")

    best_score = float("-inf")
    stale_iters = 0
    current_code_path: Path | None = None
    last_rollout_eval: dict[str, Any] = {}
    rollout_summary = load_rollout_obs_summary(
        map_name=map_name,
        rollout_root=Path(args.rollout_root),
        max_files=args.max_files,
        max_transitions=args.max_transitions,
    )
    _write_json(results_dir / "rollout_obs_summary.json", rollout_summary)
    if rollout_summary.get("available"):
        _progress(
            f"rollout ready files={len(rollout_summary.get('files', []))} "
            f"transitions={rollout_summary.get('transitions')} "
            f"n_agents={rollout_summary.get('n_agents')} obs_dim={rollout_summary.get('rollout_obs_dim')}"
        )
    else:
        _progress(f"rollout unavailable: {rollout_summary.get('error', 'unknown error')}")

    for iteration in range(args.max_iters):
        _progress(f"iteration {iteration + 1}/{args.max_iters} begin")
        cand_dir = candidate_dir(run_root, iteration)
        cand_path = cand_dir / "comm_init.py"

        if iteration == 0:
            pre_policy = seed_candidate or _find_pre_policy_candidate(args, map_name)
            if pre_policy is not None:
                cand_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(pre_policy, cand_path)
                _write_json(cand_dir / "candidate_metadata.json", {"source": str(pre_policy), "kind": "pre_policy_seed"})
                _progress(f"seed candidate copied from {pre_policy}")
            else:
                if not args.allow_no_prepolicy:
                    raise SystemExit(
                        f"No pre-generated policy found for {map_name}. Run "
                        "src/LLM-Communication-main/main.py first, or pass --seed-candidate, "
                        "or use --allow-no-prepolicy."
                    )
                messages = build_initial_prompt(
                    map_name=map_name,
                    map_spec=map_spec,
                    task_facts=None,
                    rollout_summary=rollout_summary,
                )
                _call_and_write_code(client, messages, cand_dir, cand_path, "init_coder")
        else:
            assert current_code_path is not None
            previous_code = current_code_path.read_text(encoding="utf-8")
            last_judgement = _load_json(judge_dir / f"iter_{iteration - 1:03d}_llm_judge.json")
            judge_summary = last_judgement or {}
            recent = read_trials(trials_path)
            summary_messages = build_summary_prompt(
                map_name=map_name,
                current_code=previous_code,
                judge_summary=judge_summary,
                rollout_evaluation=last_rollout_eval,
                recent_trials=recent,
            )
            _progress("analyzing previous judge result and planning the revision")
            feedback_resp = _call_and_write_text(client, summary_messages, cand_dir, "summarizer")
            revision_messages = build_revision_prompt(
                map_name=map_name,
                map_spec=map_spec,
                rollout_summary=rollout_summary,
                rollout_evaluation=last_rollout_eval,
                current_code=previous_code,
                judge_summary=judge_summary,
                llm_feedback=feedback_resp.content,
            )
            _call_and_write_code(client, revision_messages, cand_dir, cand_path, "revision_coder")
            _progress(f"revised candidate saved to {cand_path}")

        if args.dry_run:
            append_trial(
                trials_path,
                {
                    "map_name": map_name,
                    "iteration": iteration,
                    "candidate": str(cand_path),
                    "stage": "dry_run",
                    "valid": "",
                    "accepted": False,
                    "status": "dry_run_prompt_ready",
                    "failure_analysis": "Validation and LLM judge skipped because --dry-run is set.",
                    "next_hypothesis": "Run without --dry-run in the LMAC environment to execute validation and LLM judging.",
                },
            )
            refresh_outputs(trials_path, summary_path, report_path)
            break

        validation = _validate_and_repair(
            args=args,
            client=client,
            map_name=map_name,
            map_spec=map_spec,
            rollout_summary=rollout_summary,
            cand_path=cand_path,
            cand_dir=cand_dir,
        )
        _progress(
            f"interface validation={'PASS' if validation.get('valid') else 'FAIL'} "
            f"who_rate={validation.get('who_edge_rate', '')} "
            f"when_rate={validation.get('when_edge_rate', '')} what_dim={validation.get('what_dim', '')}"
        )
        append_trial(
            trials_path,
            {
                "map_name": map_name,
                "iteration": iteration,
                "candidate": str(cand_path),
                "stage": "interface_validation",
                "valid": validation.get("valid"),
                "status": "pass" if validation.get("valid") else "fail",
                "validation": validation,
                "failure_analysis": validation.get("error", ""),
                "next_hypothesis": "Ask LLM judge to evaluate who/when/what." if validation.get("valid") else "Repair generated code.",
            },
        )
        refresh_outputs(trials_path, summary_path, report_path)
        if not validation.get("valid"):
            break

        rollout_eval = evaluate_candidate_on_rollouts(
            map_name=map_name,
            comm_code=cand_path,
            rollout_root=Path(args.rollout_root),
            max_files=args.max_files,
            max_transitions=args.max_transitions,
        )
        _progress(
            f"rollout validation={'PASS' if rollout_eval.get('valid') else 'FAIL'} "
            f"transitions={rollout_eval.get('transitions', '')} "
            f"edge_rate={_short_float(rollout_eval.get('matrix_edge_rate'))} "
            f"what_rate={_short_float(rollout_eval.get('message_nonzero_rate'))} "
            f"teacher_active_what_coverage={_short_float(rollout_eval.get('active_sender_what_coverage_min'))} "
            f"flags={rollout_eval.get('risk_flags', [])}"
        )
        last_rollout_eval = rollout_eval
        _write_json(cand_dir / "rollout_evaluation.json", rollout_eval)
        append_trial(
            trials_path,
            {
                "map_name": map_name,
                "iteration": iteration,
                "candidate": str(cand_path),
                "stage": "rollout_validation",
                "valid": rollout_eval.get("valid"),
                "status": "pass" if rollout_eval.get("valid") else "fail",
                "matrix_edge_rate": rollout_eval.get("matrix_edge_rate"),
                "who_edge_rate": rollout_eval.get("who_edge_rate"),
                "when_edge_rate": rollout_eval.get("when_edge_rate"),
                "message_dim": rollout_eval.get("message_dim"),
                "failure_analysis": rollout_eval.get("error", ""),
                "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what."
                if rollout_eval.get("valid")
                else "Repair generated code using rollout traceback.",
            },
        )
        refresh_outputs(trials_path, summary_path, report_path)
        if not rollout_eval.get("valid"):
            break

        _progress("asking LLM judge to evaluate WHO / WHEN / WHAT")
        judge = _llm_judge_candidate(
            client=client,
            map_name=map_name,
            map_spec=map_spec,
            cand_path=cand_path,
            cand_dir=cand_dir,
            validation=validation,
            rollout_summary=rollout_summary,
            rollout_evaluation=rollout_eval,
            recent_trials=read_trials(trials_path),
        )
        judge_path = judge_dir / f"iter_{iteration:03d}_llm_judge.json"
        _write_json(judge_path, judge)
        score = _score_value(judge)
        improved = score > best_score
        _progress(
            f"judge verdict={'ACCEPT' if judge.get('accepted') else 'REVISE'} "
            f"score={judge.get('score')} who={judge.get('who_score')} "
            f"when={judge.get('when_score')} what={judge.get('what_score')}"
        )
        if judge.get("failure_analysis"):
            _progress(f"analysis: {judge.get('failure_analysis')}")
        if not judge.get("accepted") and judge.get("improvement_suggestions"):
            _progress(f"next revision: {judge.get('improvement_suggestions')}")
        if improved:
            best_score = score
            stale_iters = 0
            current_code_path = cand_path
        else:
            stale_iters += 1
            current_code_path = cand_path

        append_trial(
            trials_path,
            {
                "map_name": map_name,
                "iteration": iteration,
                "candidate": str(cand_path),
                "stage": "llm_judge",
                "valid": True,
                "accepted": judge.get("accepted"),
                "score": judge.get("score"),
                "who_score": judge.get("who_score"),
                "when_score": judge.get("when_score"),
                "what_score": judge.get("what_score"),
                "rollout_grounding_score": judge.get("rollout_grounding_score"),
                "matrix_edge_rate": validation.get("matrix_edge_rate"),
                "message_dim": validation.get("message_dim"),
                "status": "accepted" if judge.get("accepted") else "rejected",
                "failure_analysis": judge.get("failure_analysis", json.dumps(judge, ensure_ascii=False)),
                "next_hypothesis": "Freeze LLM teacher." if judge.get("accepted") else judge.get("improvement_suggestions", "Ask LLM to revise who/when/what."),
            },
        )
        refresh_outputs(trials_path, summary_path, report_path)

        if judge.get("accepted") and improved:
            _write_llm_teacher_manifest(
                results_dir=results_dir,
                map_name=map_name,
                candidate=cand_path,
                judgement=judge,
                evidence_json=judge_path,
            )
            _progress(f"teacher accepted and frozen: {results_dir / 'frozen_teacher_manifest.json'}")
            if args.gate == "llm_rl":
                from .eval_runner import launch_teacher_student_rl

                launch_teacher_student_rl(
                    map_name=map_name,
                    manifest=results_dir / "frozen_teacher_manifest.json",
                    run_root=results_dir / "teacher_student_rl",
                )
            break
        if stale_iters >= args.patience:
            _progress(f"stopping after {stale_iters} non-improving iteration(s)")
            break

    refresh_outputs(trials_path, summary_path, report_path)
    _progress(f"map={map_name} finished; report={report_path}")


def _validate_and_repair(
    *,
    args: argparse.Namespace,
    client: DeepSeekClient,
    map_name: str,
    map_spec: dict[str, Any],
    rollout_summary: dict[str, Any],
    cand_path: Path,
    cand_dir: Path,
) -> dict[str, Any]:
    validation = validate_candidate(cand_path, map_name, rollout_summary=rollout_summary)
    attempt = 0
    while not validation.get("valid") and attempt < args.repair_attempts:
        attempt += 1
        source = cand_path.read_text(encoding="utf-8") if cand_path.exists() else ""
        messages = build_repair_prompt(
            source_code=source,
            error=validation.get("traceback") or validation.get("error", "unknown validation error"),
            map_name=map_name,
            map_spec=map_spec,
            rollout_summary=rollout_summary,
        )
        repair_dir = cand_dir / f"repair_{attempt:02d}"
        _call_and_write_code(client, messages, repair_dir, cand_path, "repair_coder")
        validation = validate_candidate(cand_path, map_name, rollout_summary=rollout_summary)
    return validation


def _call_and_write_code(
    client: DeepSeekClient,
    messages: list[dict[str, str]],
    out_dir: Path,
    dest: Path,
    call_type: str,
) -> LLMResponse:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_prompt(out_dir / f"{call_type}_prompt.md", messages)
    _progress(f"LLM call started: {call_type}")
    resp = client.chat(messages, call_type=call_type)
    _progress(f"LLM call completed: {call_type} tokens={resp.usage.get('total_tokens', 'n/a')}")
    (out_dir / f"{call_type}_raw_response.md").write_text(resp.content, encoding="utf-8")
    code = write_candidate_from_response(resp.content, dest)
    _write_json(
        out_dir / f"{call_type}_metadata.json",
        {"usage": resp.usage, "dry_run": resp.dry_run, "destination": str(dest), "bytes": len(code)},
    )
    return resp


def _call_and_write_text(
    client: DeepSeekClient,
    messages: list[dict[str, str]],
    out_dir: Path,
    call_type: str,
) -> LLMResponse:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_prompt(out_dir / f"{call_type}_prompt.md", messages)
    _progress(f"LLM call started: {call_type}")
    resp = client.chat(messages, call_type=call_type)
    _progress(f"LLM call completed: {call_type} tokens={resp.usage.get('total_tokens', 'n/a')}")
    (out_dir / f"{call_type}_raw_response.md").write_text(resp.content, encoding="utf-8")
    _write_json(out_dir / f"{call_type}_metadata.json", {"usage": resp.usage, "dry_run": resp.dry_run})
    return resp


def _llm_judge_candidate(
    *,
    client: DeepSeekClient,
    map_name: str,
    map_spec: dict[str, Any],
    cand_path: Path,
    cand_dir: Path,
    validation: dict[str, Any],
    rollout_summary: dict[str, Any],
    rollout_evaluation: dict[str, Any],
    recent_trials: list[dict[str, Any]],
) -> dict[str, Any]:
    code = cand_path.read_text(encoding="utf-8")
    messages = build_llm_judge_prompt(
        map_name=map_name,
        map_spec=map_spec,
        candidate_code=code,
        validation=validation,
        rollout_summary=rollout_summary,
        rollout_evaluation=rollout_evaluation,
        recent_trials=recent_trials,
    )
    resp = _call_and_write_text(client, messages, cand_dir, "llm_judge")
    judgement = _extract_json_object(resp.content)
    judgement.setdefault("accepted", False)
    judgement.setdefault("blocking_failures", [])
    judgement.setdefault("rule_checks", [])
    judgement.setdefault(
        "cross_rule_check",
        {"who_when_what_consistent": False, "conflicts_or_uncovered_requirements": ["missing judge cross-rule check"]},
    )
    if not judgement["rule_checks"]:
        judgement["blocking_failures"].append(
            {
                "type": "missing_rule_checks",
                "evidence": "Judge did not complete the required per-rule evidence audit.",
                "revision_target": "who|when|what",
            }
        )
    cross_rule = judgement.get("cross_rule_check") or {}
    if not cross_rule.get("who_when_what_consistent", False):
        judgement["blocking_failures"].append(
            {
                "type": "cross_rule_inconsistency",
                "evidence": json.dumps(cross_rule, ensure_ascii=False),
                "revision_target": "who|when|what",
            }
        )
    if judgement["blocking_failures"]:
        judgement["accepted"] = False
        judgement["replacement_readiness"] = "not_ready"
    judgement.setdefault("score", 0.0)
    judgement["usage"] = resp.usage
    judgement["dry_run"] = resp.dry_run
    judgement["comm_code"] = str(cand_path)
    return judgement


def _write_llm_teacher_manifest(
    *,
    results_dir: Path,
    map_name: str,
    candidate: Path,
    judgement: dict[str, Any],
    evidence_json: Path,
) -> None:
    manifest = {
        "method": "LLM-only-frozen-teacher-selection-v1",
        "selection_rule": (
            "interface-valid candidates are judged by the LLM on who/when/what; "
            "the first accepted candidate with the best LLM score is frozen"
        ),
        "teachers": {
            map_name: {
                "teacher_path": str(candidate),
                "evidence_json": str(evidence_json),
                "score": judgement.get("score"),
                "who_score": judgement.get("who_score"),
                "when_score": judgement.get("when_score"),
                "what_score": judgement.get("what_score"),
                "replacement_readiness": judgement.get("replacement_readiness"),
                "failure_analysis": judgement.get("failure_analysis", ""),
            }
        },
    }
    _write_json(results_dir / "frozen_teacher_manifest.json", manifest)
    lines = [
        "# Frozen LLM Teacher Manifest",
        "",
        f"- method: `{manifest['method']}`",
        f"- map: `{map_name}`",
        f"- teacher: `{candidate}`",
        f"- score: `{judgement.get('score')}`",
        f"- readiness: `{judgement.get('replacement_readiness')}`",
        "",
        "This manifest intentionally uses LLM-only who/when/what judgement, not DRC.",
    ]
    (results_dir / "frozen_teacher_manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.startswith("json"):
            stripped = stripped[4:].strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start >= 0 and end > start:
            return json.loads(stripped[start : end + 1])
        raise


def _parse_seed_candidates(items: list[str]) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for item in items:
        if "=" in item:
            map_name, path = item.split("=", 1)
            out[map_name] = Path(path)
        else:
            out["*"] = Path(item)
    if "*" in out:
        default = out["*"]
        for name in DEFAULT_MAPS:
            out.setdefault(name, default)
    return {key: value.resolve() for key, value in out.items() if key != "*"}


def _find_pre_policy_candidate(args: argparse.Namespace, map_name: str) -> Path | None:
    root = Path(args.pre_policy_root) / map_name
    preferred = [
        root / "LMAC_WWW" / "comm_init.py",
        root / "LMAC_WWW" / "last_try.py",
        root / "last_try.py",
    ]
    for path in preferred:
        if path.exists():
            return path.resolve()
    candidates = sorted(root.glob("**/comm_init.py"), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0].resolve() if candidates else None


def _score_value(summary: dict[str, Any]) -> float:
    value = summary.get("score")
    if value is None:
        return float("-inf")
    return float(value)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _commands_header(args: argparse.Namespace, map_name: str, run_root: Path) -> str:
    return f"""#!/usr/bin/env bash
set -euo pipefail
cd "{ROOT}"

# Re-run this workflow:
PYTHONPATH=src "{args.python}" -m hl_comm.auto_research \\
  --maps {map_name} \\
  --model {args.model} \\
  --max-iters {args.max_iters} \\
  --max-transitions {args.max_transitions} \\
  --max-files {args.max_files} \\
  --rollout-root "{args.rollout_root}" \\
  --pre-policy-root "{args.pre_policy_root}" \\
  --gate {args.gate} \\
  --run-id {run_root.name}
"""


if __name__ == "__main__":
    main()
