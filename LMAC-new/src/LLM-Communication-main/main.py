"""Unified entry point for LLM communication-teacher generation and iteration.

Examples (run from this directory):

    python main.py --mode generate --map 5z_vs_1ul
    python main.py --mode iterate --map 5z_vs_1ul --policy /path/to/comm_init.py
    python main.py --mode full --map 5z_vs_1ul --rollout-root ../../data

Every invocation creates an immutable run directory containing the seed policy,
iteration candidates, prompts, raw LLM responses, judgements, and a consolidated
modification log.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from configs import pipeline_config as pipeline
from env_adapters import get_adapter, normalize_environment


SCRIPT_DIR = Path(__file__).resolve().parent
LMAC_ROOT = SCRIPT_DIR.parents[1]
LMAC_SRC = LMAC_ROOT / "src"
DEFAULT_ROLLOUT_ROOT = LMAC_ROOT / "data"
DEFAULT_RUN_ROOT = SCRIPT_DIR / "pipeline_runs"


def rollout_base(args: argparse.Namespace) -> Path:
    root = Path(args.rollout_root).expanduser().resolve()
    return root if args.env == "smac" else root / args.env


def rollout_dir(args: argparse.Namespace) -> Path:
    return rollout_base(args) / args.map


def matrix_policy_root(environment: str, task: str) -> Path:
    root = SCRIPT_DIR / "matrix_code"
    return root / task / "LMAC_WWW" if environment == "smac" else root / environment / task / "LMAC_WWW"


def pipeline_task_root(args: argparse.Namespace) -> Path:
    root = Path(args.output_root).expanduser().resolve()
    return root / args.map if args.env == "smac" else root / args.env / args.map


class TeeStream:
    def __init__(self, terminal, log_handle):
        self.terminal = terminal
        self.log_handle = log_handle

    def write(self, data):
        self.terminal.write(data)
        self.log_handle.write(data)
        self.log_handle.flush()
        return len(data)

    def flush(self):
        self.terminal.flush()
        self.log_handle.flush()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate and/or iteratively evaluate an LLM who/when/what communication teacher."
    )
    parser.add_argument(
        "--mode",
        choices=("generate", "iterate", "full"),
        default=pipeline.MODE,
        help="generate: initial prior only; iterate: revise an existing policy; full: generate then revise.",
    )
    parser.add_argument("--env", dest="env", default=os.environ.get("LLM_COMM_ENV", pipeline.ENVIRONMENT),
                        help="Environment family: smac, smacv2, hallway, hallway_group, or grf.")
    parser.add_argument("--task", default="", help="Task/scenario name. Preferred over the legacy --map alias.")
    parser.add_argument("--map", default=os.environ.get("LLM_SMAC_MAP_NAME", pipeline.MAP_NAME),
                        help="Legacy task-name alias retained for existing SMAC commands.")
    parser.add_argument(
        "--policy",
        default=pipeline.POLICY_PATH,
        help="Existing comm_init.py used by iterate mode. If omitted, matrix_code/<map>/LMAC_WWW/comm_init.py is used.",
    )
    parser.add_argument("--rollout-root", default=os.environ.get("LMAC_ROLLOUT_ROOT", pipeline.ROLLOUT_ROOT))
    parser.add_argument("--output-root", default=pipeline.OUTPUT_ROOT)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--max-iters", type=int, default=pipeline.MAX_ITERS)
    parser.add_argument("--patience", type=int, default=pipeline.PATIENCE)
    parser.add_argument("--repair-attempts", type=int, default=pipeline.REPAIR_ATTEMPTS)
    parser.add_argument("--max-files", type=int, default=pipeline.MAX_FILES)
    parser.add_argument("--max-transitions", type=int, default=pipeline.MAX_TRANSITIONS)
    parser.add_argument("--collect-t-max", type=int, default=pipeline.COLLECT_T_MAX)
    parser.add_argument("--collect-seeds", type=int, default=pipeline.COLLECT_SEEDS)
    parser.add_argument("--collect-gpu", default=pipeline.COLLECT_GPU)
    parser.add_argument(
        "--no-auto-collect", action="store_true", default=not pipeline.AUTO_COLLECT_ROLLOUTS,
        help="Disable automatic rollout collection in full mode.",
    )
    parser.add_argument("--model", default=pipeline.MODEL, help="Iteration model; defaults to the configured coder model.")
    parser.add_argument("--base-url", default=pipeline.BASE_URL, help="Defaults to the configured coder base URL.")
    parser.add_argument("--api-key", default=pipeline.API_KEY, help="Defaults to the configured coder API key.")
    parser.add_argument("--api-config", default=pipeline.API_CONFIG, help="Optional Python API configuration for the iteration loop.")
    parser.add_argument("--temperature", type=float, default=pipeline.TEMPERATURE)
    parser.add_argument("--reasoning-effort", default=pipeline.REASONING_EFFORT)
    parser.add_argument("--deepseek-thinking", action="store_true", default=pipeline.DEEPSEEK_THINKING)
    parser.add_argument("--dry-run", action="store_true", default=pipeline.DRY_RUN, help="Build iteration prompts without calling the iteration LLM.")
    parser.add_argument("--gate", choices=("llm", "llm_rl"), default=pipeline.GATE)
    args = parser.parse_args()
    args.env = normalize_environment(args.env)
    if args.task:
        args.map = args.task
    args.task = args.map
    adapter = get_adapter(args.env, SCRIPT_DIR)
    if not adapter.supports(args.map):
        raise SystemExit(f"Unsupported task '{args.map}' for environment '{args.env}'.")
    return args


def generate_initial_policy(map_name: str, environment: str, rollout_root: Path, run_dir: Path) -> Path:
    # config.py reads these values at import time, so imports must remain local.
    os.environ["LLM_SMAC_MAP_NAME"] = map_name
    os.environ["LLM_COMM_ENV"] = environment
    os.environ["LMAC_ROLLOUT_ROOT"] = str(rollout_root)
    os.chdir(SCRIPT_DIR)
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))

    from api.LLMCoder import LLMCoder, LMAC_SYSTEM_PROMPT
    from api.LLMPlanner import ANALYZER_SYSTEM_PROMPT, LLMPlanner

    planner = LLMPlanner()
    coder = LLMCoder(run_id=run_dir.name)
    import config as generation_config
    generation_dir = run_dir / "generation"
    generation_dir.mkdir(parents=True, exist_ok=True)
    adapter = get_adapter(environment, SCRIPT_DIR)
    documented_schema = adapter.documented_obs_info(map_name)
    runtime_schema = generation_config.process_lmac_rollout_obs_info(map_name)
    try:
        runtime_probe = adapter.runtime_probe(map_name)
    except Exception as exc:
        runtime_probe = {"available": False, "error": f"{type(exc).__name__}: {exc}"}
    (generation_dir / "task_description.json").write_text(
        json.dumps(adapter.task_description(map_name), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (generation_dir / "raw_obs_schema.json").write_text(
        json.dumps(documented_schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (generation_dir / "runtime_obs_schema.json").write_text(
        json.dumps(runtime_schema, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8"
    )
    (generation_dir / "runtime_probe.json").write_text(
        json.dumps(runtime_probe, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8"
    )
    print(f"[generate] env={environment}, task={map_name}, n_agents={coder.n_agents}, obs_dim={coder.obs_dim}")
    requirements = planner.analyze()
    policy_spec = planner.plan(requirements)
    (generation_dir / "analyzer_system_prompt.md").write_text(
        ANALYZER_SYSTEM_PROMPT, encoding="utf-8",
    )
    (generation_dir / "analyzer_user_prompt.md").write_text(planner.analysis_prompt, encoding="utf-8")
    (generation_dir / "communication_requirements.json").write_text(
        json.dumps(requirements, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (generation_dir / "analyzer_raw_response.md").write_text(
        planner.last_analysis_response, encoding="utf-8"
    )
    (generation_dir / "planner_system_prompt.md").write_text(planner.system_content, encoding="utf-8")
    (generation_dir / "planner_user_prompt.md").write_text(planner.policy_prompt, encoding="utf-8")
    (generation_dir / "policy_spec.json").write_text(
        json.dumps(policy_spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (generation_dir / "planner_raw_response.md").write_text(
        planner.last_policy_response, encoding="utf-8"
    )
    (generation_dir / "planner_policy.md").write_text(
        json.dumps(policy_spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (generation_dir / "coder_system_prompt.md").write_text(
        LMAC_SYSTEM_PROMPT,
        encoding="utf-8",
    )
    (generation_dir / "coder_user_prompt.md").write_text(
        coder._build_prompt(policy_spec, ""), encoding="utf-8"
    )

    teacher = coder.generate_teacher(policy_spec)
    if not teacher:
        raise RuntimeError("LLM failed to generate a valid who/when/what teacher.")

    generated = matrix_policy_root(environment, map_name) / "comm_init.py"
    if not generated.exists():
        raise FileNotFoundError(f"Generator reported success but policy is missing: {generated}")
    archived = generation_dir / "comm_init.py"
    shutil.copy2(generated, archived)
    for attr, name in (("last_raw_path", "coder_raw_response.md"), ("last_archive_path", "coder_generated_attempt.py")):
        source = getattr(coder, attr, None)
        if source and Path(source).exists():
            shutil.copy2(source, generation_dir / name)
    print(f"[generate] immutable initial policy: {archived}")
    return archived


def resolve_existing_policy(args: argparse.Namespace) -> Path:
    policy = Path(args.policy).expanduser().resolve() if args.policy else (
        matrix_policy_root(args.env, args.map) / "comm_init.py"
    )
    if not policy.is_file():
        raise FileNotFoundError(
            f"Existing policy not found: {policy}. Pass --policy /absolute/path/to/comm_init.py."
        )
    return policy


def ensure_offline_rollouts(args: argparse.Namespace, policy: Path, run_dir: Path) -> list[Path]:
    """Collect and normalize map rollouts required by full mode."""
    task_rollout_dir = rollout_dir(args)
    existing = sorted(task_rollout_dir.glob("train_traj_*.pkl"))
    if existing:
        print(f"[collect] reusing {len(existing)} offline rollout file(s) from {task_rollout_dir}")
        return existing
    if args.no_auto_collect:
        raise FileNotFoundError(
            f"No offline rollout files found under {task_rollout_dir} and automatic collection is disabled."
        )

    task_rollout_dir.mkdir(parents=True, exist_ok=True)
    collect_root = run_dir / "collection"
    collect_root.mkdir(parents=True, exist_ok=True)
    print(
        f"[collect] no offline data for map={args.map}; starting automatic collection "
        f"seeds={args.collect_seeds} t_max={args.collect_t_max}", flush=True
    )
    collection = get_adapter(args.env, SCRIPT_DIR).collection_spec(args.map)
    for idx in range(max(1, args.collect_seeds)):
        seed = int(pipeline.COLLECT_SEED_START) + idx
        seed_dir = collect_root / f"seed_{seed}"
        seed_dir.mkdir(parents=True, exist_ok=True)
        staging_buffer = seed_dir / "episodes"
        staging_buffer.mkdir(parents=True, exist_ok=True)
        command = [
            sys.executable, "-u", str(LMAC_SRC / "main_llm_final.py"),
            f"--config={pipeline.COLLECT_CONFIG}",
            f"--env-config={collection.env_config}", "with",
            f"seed={seed}", f"t_max={args.collect_t_max}",
            "epsilon_anneal_time=50000", f"name=LLM_comm_collect_{args.map}_{seed}",
            f"save_dir={seed_dir}", f"buffer_dir={staging_buffer}",
            f"comm_code_paths={[str(policy)]}", "important_state=[0]",
            "phase=multi_train", "tmp2=False", "meta_lambda=0.0",
            "recon_lambda=0.0", "consistency_lambda=0.0",
            "use_tensorboard=True", "use_wandb=False",
            f"running_algorithm_name=({args.map})LLM_comm_offline_collect",
        ]
        command.extend(collection.overrides)
        (seed_dir / "command.json").write_text(
            json.dumps(command, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        env.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
        env["CUDA_VISIBLE_DEVICES"] = str(args.collect_gpu)
        env["WANDB_MODE"] = "disabled"
        env["WANDB_DISABLED"] = "true"
        print(f"[collect] seed={seed} started", flush=True)
        process = subprocess.Popen(
            command, cwd=LMAC_ROOT, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, bufsize=1,
        )
        assert process.stdout is not None
        with (seed_dir / "collect.log").open("w", encoding="utf-8") as log:
            for line in process.stdout:
                log.write(line)
                log.flush()
                print(f"[collect:{seed}] {line}", end="", flush=True)
        return_code = process.wait()
        (seed_dir / "exit_code.txt").write_text(str(return_code) + "\n", encoding="utf-8")
        if return_code != 0:
            tail = ""
            log_path = seed_dir / "collect.log"
            if log_path.exists():
                tail = "\n".join(log_path.read_text(encoding="utf-8", errors="replace").splitlines()[-20:])
            raise RuntimeError(
                f"Offline rollout collection failed for seed={seed} with exit code {return_code}. "
                f"Inspect {log_path}. Last log lines:\n{tail}"
            )

    collected = sorted(collect_root.glob("seed_*/episodes/episode_*.pkl"))
    if not collected:
        raise RuntimeError(f"Collector finished but produced no episode_*.pkl under {task_rollout_dir}")
    normalized = []
    for idx, source in enumerate(collected):
        destination = task_rollout_dir / f"train_traj_{idx:04d}.pkl"
        shutil.copy2(source, destination)
        normalized.append(destination)
    print(f"[collect] ready files={len(normalized)} directory={task_rollout_dir}", flush=True)
    return normalized


def run_iteration(args: argparse.Namespace, seed_policy: Path, run_dir: Path) -> Path:
    iteration_output = run_dir / "iteration"
    effective_rollout_root = rollout_base(args)
    rollout_files = sorted((effective_rollout_root / args.map).glob("train_traj_*.pkl"))
    if not args.dry_run and not rollout_files:
        raise FileNotFoundError(
            f"No offline rollout files found under {effective_rollout_root / args.map}. "
            "Collect train_traj_*.pkl first or pass the correct --rollout-root."
        )
    effective_key = args.api_key or os.environ.get("DEEPSEEK_API_KEY", "")
    effective_model = args.model
    effective_base_url = args.base_url
    if not effective_key or not effective_model or not effective_base_url:
        # Planner/Coder use this project-local configuration. Reuse it for the
        # judge/reviser unless the user explicitly provided iteration settings.
        from configs.llm_api_config import LLMAPIConfig

        configured = LLMAPIConfig.get_task_model("coder")
        if configured is not None:
            effective_key = effective_key or configured.api_key
            effective_base_url = effective_base_url or configured.base_url
        effective_model = effective_model or LLMAPIConfig.TASK_MODELS["coder"]
    effective_model = effective_model or "deepseek-chat"
    effective_base_url = effective_base_url or "https://api.deepseek.com"
    if not effective_key and not args.dry_run:
        raise RuntimeError(
            "No API key is available for iteration. Configure the coder model in "
            "configs/llm_api_config.py, set DEEPSEEK_API_KEY, or pass --api-key."
        )

    command = [
        sys.executable,
        "-u",
        "-m",
        "hl_comm.auto_research",
        "--maps",
        args.map,
        "--seed-candidate",
        f"{args.map}={seed_policy}",
        "--rollout-root",
        str(effective_rollout_root),
        "--output-root",
        str(iteration_output),
        "--run-id",
        run_dir.name,
        "--model",
        effective_model,
        "--base-url",
        effective_base_url,
        "--api-config",
        str(Path(args.api_config).expanduser().resolve()) if args.api_config else "",
        "--temperature",
        str(args.temperature),
        "--max-iters",
        str(args.max_iters),
        "--patience",
        str(args.patience),
        "--repair-attempts",
        str(args.repair_attempts),
        "--max-files",
        str(args.max_files),
        "--max-transitions",
        str(args.max_transitions),
        "--gate",
        args.gate,
    ]
    if args.reasoning_effort:
        command.extend(["--reasoning-effort", args.reasoning_effort])
    if args.deepseek_thinking:
        command.append("--deepseek-thinking")
    if args.dry_run:
        command.append("--dry-run")

    env = os.environ.copy()
    env["LLM_COMM_ENV"] = args.env
    env["PYTHONUNBUFFERED"] = "1"
    if effective_key:
        env["DEEPSEEK_API_KEY"] = effective_key
    env["PYTHONPATH"] = str(LMAC_SRC) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    printable = ["<redacted>" if effective_key and token == effective_key else token for token in command]
    (run_dir / "iteration_command.json").write_text(
        json.dumps(printable, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("[iterate] launching rollout-grounded LLM evaluation and revision loop", flush=True)
    process = subprocess.Popen(
        command, cwd=LMAC_ROOT, env=env, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, bufsize=1,
    )
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="", flush=True)
    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(
            f"LLM iteration subprocess failed with exit code {return_code}. "
            f"Inspect artifacts under {iteration_output}."
        )
    iteration_root = iteration_output / args.map / run_dir.name
    frozen_manifest = iteration_root / "results" / "frozen_teacher_manifest.json"
    if not args.dry_run and not frozen_manifest.is_file():
        raise RuntimeError(
            "Iteration finished without an accepted frozen teacher. "
            f"Inspect {iteration_root / 'results' / 'final_report.md'}; this run is not complete."
        )
    return iteration_root


def write_run_manifest(args: argparse.Namespace, run_dir: Path, seed_policy: Path | None) -> None:
    manifest = {
        "mode": args.mode,
        "environment": args.env,
        "task": args.map,
        "map": args.map,
        "run_id": run_dir.name,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rollout_root": str(Path(args.rollout_root).expanduser().resolve()),
        "seed_policy": str(seed_policy) if seed_policy else None,
        "max_iters": args.max_iters,
        "model": args.model or "configured coder model",
        "gate": args.gate,
        "dry_run": args.dry_run,
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def write_run_context(args: argparse.Namespace, run_dir: Path) -> None:
    task_rollout_dir = rollout_dir(args)
    rollout_files = sorted(task_rollout_dir.glob("**/*.pkl"))
    context = {
        "argv": [sys.argv[0], *sys.argv[1:]],
        "cwd": str(Path.cwd()),
        "python": sys.version,
        "platform": platform.platform(),
        "executable": sys.executable,
        "environment": {
            "SC2PATH": os.environ.get("SC2PATH", ""),
            "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
            "api_key_available": bool(
                args.api_key or os.environ.get("DEEPSEEK_API_KEY")
            ),
        },
        "config": {
            key: ("<redacted>" if key == "api_key" and value else value)
            for key, value in vars(args).items()
        },
        "rollout_files": [_file_record(path, hash_content=False) for path in rollout_files],
    }
    try:
        import torch
        context["torch"] = {
            "version": torch.__version__, "cuda_available": torch.cuda.is_available(),
            "cuda_version": torch.version.cuda,
        }
    except Exception as exc:
        context["torch"] = {"error": str(exc)}
    (run_dir / "run_context.json").write_text(
        json.dumps(context, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def write_artifact_index(run_dir: Path) -> None:
    records = []
    for path in sorted(run_dir.rglob("*")):
        if path.is_file() and path.name != "artifact_index.json":
            record = _file_record(path, hash_content=True)
            record["relative_path"] = str(path.relative_to(run_dir))
            records.append(record)
    (run_dir / "artifact_index.json").write_text(
        json.dumps({"run_dir": str(run_dir), "artifacts": records}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _file_record(path: Path, *, hash_content: bool) -> dict:
    stat = path.stat()
    record = {
        "path": str(path.resolve()), "bytes": stat.st_size,
        "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
    }
    if hash_content:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        record["sha256"] = digest.hexdigest()
    return record


def write_consolidated_log(run_dir: Path, iteration_root: Path | None) -> None:
    lines = [
        "# LLM Communication Policy Run",
        "",
        f"- run directory: `{run_dir}`",
        "",
    ]
    generation = run_dir / "generation" / "comm_init.py"
    if generation.exists():
        lines.extend(["## Initial generation", "", f"- policy: `{generation}`", ""])

    if iteration_root is not None:
        trials_path = iteration_root / "results" / "trials.jsonl"
        lines.extend(["## Iterations", ""])
        if trials_path.exists():
            trials = [json.loads(line) for line in trials_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            for item in trials:
                if item.get("stage") != "llm_judge":
                    continue
                idx = int(item.get("iteration", 0))
                cand = iteration_root / "candidates" / f"iter_{idx:03d}"
                lines.extend(
                    [
                        f"### Iteration {idx}",
                        "",
                        f"- candidate: `{item.get('candidate', '')}`",
                        f"- verdict: `{item.get('status', '')}`",
                        f"- score: `{item.get('score', '')}`",
                        f"- who/when/what: `{item.get('who_score', '')}` / `{item.get('when_score', '')}` / `{item.get('what_score', '')}`",
                        f"- analysis: {item.get('failure_analysis', '')}",
                        f"- next modification: {item.get('next_hypothesis', '')}",
                        f"- judge prompt: `{cand / 'llm_judge_prompt.md'}`",
                        f"- judge response: `{cand / 'llm_judge_raw_response.md'}`",
                        f"- revision analysis: `{cand / 'summarizer_raw_response.md'}`",
                        "",
                    ]
                )
            frozen = iteration_root / "results" / "frozen_teacher_manifest.json"
            if frozen.exists():
                lines.extend(["## Final teacher", "", f"- manifest: `{frozen}`", ""])
        else:
            lines.append("No completed iteration ledger was produced.\n")
    (run_dir / "modification_log.md").write_text("\n".join(lines), encoding="utf-8")


def archive_matrix_policies(
    *, environment: str, map_name: str, run_dir: Path, seed_policy: Path | None,
    iteration_root: Path | None, promote_iterations: bool = True,
) -> Path | None:
    """Archive one experiment's Python policies and update the stable latest path."""
    policy_root = matrix_policy_root(environment, map_name)
    experiment_dir = policy_root / run_dir.name
    initial_dir = experiment_dir / "initial"
    iterations_dir = experiment_dir / "iterations"
    initial_dir.mkdir(parents=True, exist_ok=True)
    iterations_dir.mkdir(parents=True, exist_ok=True)

    records = []
    selected: Path | None = None
    if seed_policy and seed_policy.is_file():
        initial_name = "comm_init.py" if seed_policy.name == "comm_init.py" else seed_policy.name
        initial_copy = initial_dir / initial_name
        shutil.copy2(seed_policy, initial_copy)
        records.append({"stage": "initial", "source": str(seed_policy), "archive": str(initial_copy)})
        selected = initial_copy

    if iteration_root and iteration_root.exists():
        for candidate in sorted((iteration_root / "candidates").glob("iter_*/comm_init.py")):
            iteration_name = candidate.parent.name
            archived = iterations_dir / f"{iteration_name}.py"
            shutil.copy2(candidate, archived)
            records.append({"stage": iteration_name, "source": str(candidate), "archive": str(archived)})

        frozen_manifest = iteration_root / "results" / "frozen_teacher_manifest.json"
        if promote_iterations and frozen_manifest.exists():
            frozen = json.loads(frozen_manifest.read_text(encoding="utf-8"))
            teacher = frozen.get("teachers", {}).get(map_name, {}).get("teacher_path")
            if teacher and Path(teacher).is_file():
                source = Path(teacher)
                selected = iterations_dir / f"{source.parent.name}.py"
        elif promote_iterations and records:
            iteration_records = [item for item in records if item["stage"].startswith("iter_")]
            if iteration_records:
                selected = Path(iteration_records[-1]["archive"])

    latest_path = policy_root / "comm_init.py"
    if selected and selected.is_file():
        shutil.copy2(selected, latest_path)
        print(f"[archive] experiment policies: {experiment_dir}", flush=True)
        print(f"[archive] latest policy updated: {latest_path}", flush=True)

    manifest = {
        "map": map_name,
        "environment": environment,
        "run_id": run_dir.name,
        "pipeline_run": str(run_dir),
        "selected_policy": str(selected) if selected else None,
        "latest_policy": str(latest_path) if selected else None,
        "policies": records,
    }
    (experiment_dir / "policy_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return selected


def write_pipeline_status(
    *, args: argparse.Namespace, run_dir: Path, seed_policy: Path | None,
    iteration_root: Path | None, failure: dict | None, selected_policy: Path | None,
) -> None:
    task_rollout_dir = rollout_dir(args)
    rollout_files = sorted(task_rollout_dir.glob("train_traj_*.pkl"))
    frozen = (
        iteration_root / "results" / "frozen_teacher_manifest.json"
        if iteration_root else None
    )
    status = {
        "run_id": run_dir.name,
        "environment": args.env,
        "task": args.map,
        "map": args.map,
        "mode": args.mode,
        "overall": "failed" if failure else "complete",
        "generation": {
            "status": "complete" if seed_policy and seed_policy.is_file() else "not_completed",
            "policy": str(seed_policy) if seed_policy else None,
        },
        "collection": {
            "status": "complete" if rollout_files else "not_completed",
            "rollout_dir": str(task_rollout_dir),
            "train_files": len(rollout_files),
        },
        "iteration": {
            "status": "accepted" if frozen and frozen.is_file() else (
                "not_requested" if args.mode == "generate" else "not_accepted"
            ),
            "root": str(iteration_root) if iteration_root else None,
            "frozen_manifest": str(frozen) if frozen and frozen.is_file() else None,
        },
        "selected_policy": str(selected_policy) if selected_policy else None,
        "failure": failure,
    }
    (run_dir / "pipeline_status.json").write_text(
        json.dumps(status, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> None:
    args = parse_args()
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = pipeline_task_root(args) / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    log_handle = (run_dir / "pipeline.log").open("a", encoding="utf-8")
    original_stdout, original_stderr = sys.stdout, sys.stderr
    sys.stdout = TeeStream(original_stdout, log_handle)
    sys.stderr = TeeStream(original_stderr, log_handle)
    write_run_context(args, run_dir)

    seed_policy: Path | None = None
    iteration_root: Path | None = None
    failure = None
    try:
        if args.mode in {"generate", "full"}:
            seed_policy = generate_initial_policy(
                args.map, args.env, Path(args.rollout_root).expanduser().resolve(), run_dir
            )
        else:
            existing = resolve_existing_policy(args)
            seed_dir = run_dir / "generation"
            seed_dir.mkdir(parents=True, exist_ok=True)
            seed_policy = seed_dir / "existing_comm_init.py"
            shutil.copy2(existing, seed_policy)
            (seed_dir / "source_path.txt").write_text(str(existing) + "\n", encoding="utf-8")

        write_run_manifest(args, run_dir, seed_policy)
        if args.mode in {"iterate", "full"}:
            ensure_offline_rollouts(args, seed_policy, run_dir)
        if args.mode in {"iterate", "full"}:
            iteration_root = run_iteration(args, seed_policy, run_dir)
    except Exception as exc:
        failure = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "type": type(exc).__name__, "message": str(exc),
            "traceback": traceback.format_exc(),
        }
        (run_dir / "failure.json").write_text(
            json.dumps(failure, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"[failed] {type(exc).__name__}: {exc}", flush=True)
        raise
    except KeyboardInterrupt:
        failure = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "type": "KeyboardInterrupt", "message": "Run interrupted by user.",
        }
        (run_dir / "failure.json").write_text(
            json.dumps(failure, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print("[interrupted] run stopped by user; unaccepted candidates will not replace comm_init.py", flush=True)
        raise
    finally:
        if iteration_root is None:
            expected_iteration_root = run_dir / "iteration" / args.map / run_dir.name
            if expected_iteration_root.exists():
                iteration_root = expected_iteration_root
        write_consolidated_log(run_dir, iteration_root)
        selected_policy = archive_matrix_policies(
            environment=args.env, map_name=args.map, run_dir=run_dir, seed_policy=seed_policy,
            iteration_root=iteration_root, promote_iterations=failure is None,
        )
        write_pipeline_status(
            args=args, run_dir=run_dir, seed_policy=seed_policy,
            iteration_root=iteration_root, failure=failure,
            selected_policy=selected_policy,
        )
        if failure is None:
            print(f"[done] complete record: {run_dir}", flush=True)
            print(f"[done] consolidated modification log: {run_dir / 'modification_log.md'}", flush=True)
        write_artifact_index(run_dir)
        sys.stdout, sys.stderr = original_stdout, original_stderr
        log_handle.close()


if __name__ == "__main__":
    main()
