#!/usr/bin/env python3
"""Offline decision-relevant certification for frozen LLM communication teachers.

This script extends the existing static task-fact certificate with probe-based
offline evidence. It deliberately does not use downstream RL win-rate to select
the teacher.
"""

import argparse
import importlib.util
import json
import math
import pickle
import sys
from pathlib import Path

import torch as th
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT))

from components.certified_task_facts import map_specs  # noqa: E402
from scripts.certify_llm_comm import (  # noqa: E402
    build_completeness_report,
    build_seq,
    call_comm,
    load_module,
    message_part,
    run_task_probes,
)


def find_buffers(buffer_root, map_name, limit):
    root = Path(buffer_root)
    files = sorted(root.glob(f"**/{map_name}/**/buffer/**/*.pkl"))
    if not files:
        files = sorted((root / map_name).glob("**/*.pkl"))
    if not files:
        files = sorted(root.glob(f"**/{map_name}/**/*.pkl"))
    if not files:
        files = sorted(root.glob("**/*.pkl"))
    return files[:limit]


def to_lmac_agent_inputs(raw_obs, actions_onehot, target_obs_dim):
    """Rebuild the controller input: raw obs + previous action + agent id."""
    batch, timesteps, n_agents, _ = raw_obs.shape
    last_action = th.zeros_like(actions_onehot)
    if timesteps > 1:
        last_action[:, 1:] = actions_onehot[:, :-1]
    agent_ids = th.eye(n_agents, dtype=raw_obs.dtype).view(1, 1, n_agents, n_agents)
    agent_ids = agent_ids.expand(batch, timesteps, -1, -1)
    agent_inputs = th.cat([raw_obs, last_action, agent_ids], dim=-1)
    if agent_inputs.shape[-1] == target_obs_dim:
        return agent_inputs
    return None


def load_buffer_tensors(
    paths,
    max_transitions,
    expected_n_agents=None,
    target_obs_dim=None,
    allow_obs_pad=False,
    gamma=0.99,
):
    obs_items, state_items, action_items = [], [], []
    return_items, avail_items = [], []
    has_return_data = True
    has_avail_data = True
    transition_count = 0
    for path in paths:
        with Path(path).open("rb") as f:
            item = pickle.load(f)
        if not all(k in item for k in ("obs", "state", "actions_onehot")):
            continue
        obs = item["obs"].float()
        state = item["state"].float()
        actions_onehot = item["actions_onehot"].float()
        actions = item.get("actions")
        if actions is None:
            actions = actions_onehot.argmax(dim=-1)
        else:
            actions = actions.squeeze(-1).long()
        if expected_n_agents is not None and obs.shape[2] != expected_n_agents:
            continue
        if target_obs_dim is not None and obs.shape[-1] != target_obs_dim:
            rebuilt = to_lmac_agent_inputs(obs, actions_onehot, target_obs_dim)
            if rebuilt is not None:
                obs = rebuilt
            elif obs.shape[-1] < target_obs_dim and allow_obs_pad:
                pad = target_obs_dim - obs.shape[-1]
                obs = F.pad(obs, (0, pad))
            else:
                continue
        mask = item.get("mask")
        if mask is None:
            mask = th.ones(obs.shape[0], obs.shape[1], 1)
        mask = mask.float()
        valid = mask.bool().squeeze(-1)
        if not valid.any():
            continue
        obs_items.append(obs[valid])
        state_items.append(state[valid])
        action_items.append(actions[valid])
        if "reward" in item and "terminated" in item:
            returns = discounted_returns(
                item["reward"].float(),
                item["terminated"].float(),
                mask,
                gamma=gamma,
            )
            return_items.append(returns[valid])
        else:
            has_return_data = False
        if "avail_actions" in item:
            avail_items.append(item["avail_actions"].float()[valid])
        else:
            has_avail_data = False
        transition_count += int(valid.sum().item())
        if transition_count >= max_transitions:
            break
    if not obs_items:
        raise RuntimeError(
            "No readable buffer files with obs/state/actions_onehot and matching map shape were found"
        )

    obs = th.cat(obs_items, dim=0)
    state = th.cat(state_items, dim=0)
    actions = th.cat(action_items, dim=0)
    returns = th.cat(return_items, dim=0) if has_return_data and return_items else None
    avail_actions = th.cat(avail_items, dim=0) if has_avail_data and avail_items else None
    if obs.shape[0] > max_transitions:
        obs = obs[:max_transitions]
        state = state[:max_transitions]
        actions = actions[:max_transitions]
        if returns is not None:
            returns = returns[:max_transitions]
        if avail_actions is not None:
            avail_actions = avail_actions[:max_transitions]
    return obs, state, actions, {"returns": returns, "avail_actions": avail_actions}


def discounted_returns(rewards, terminated, mask, gamma):
    rewards = rewards.squeeze(-1)
    terminated = terminated.squeeze(-1)
    valid = mask.squeeze(-1).float() if mask.dim() == 3 else mask.float()
    out = th.zeros_like(rewards)
    running = th.zeros(rewards.shape[0], dtype=rewards.dtype)
    for t in reversed(range(rewards.shape[1])):
        running = rewards[:, t] + gamma * running * (1.0 - terminated[:, t])
        out[:, t] = running * valid[:, t]
    return out


def split_indices(n, train_frac=0.7):
    n_train = max(1, int(n * train_frac))
    idx = th.randperm(n)
    return idx[:n_train], idx[n_train:]


def standardize_train_test(x_train, x_test):
    mean = x_train.mean(dim=0, keepdim=True)
    std = x_train.std(dim=0, keepdim=True).clamp_min(1e-6)
    return (x_train - mean) / std, (x_test - mean) / std


def add_bias(x):
    return th.cat([x, th.ones(x.shape[0], 1, dtype=x.dtype)], dim=1)


def ridge_regression_score(x, y, train_idx, test_idx, ridge):
    x_train, x_test = x[train_idx], x[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    x_train, x_test = standardize_train_test(x_train, x_test)
    y_mean = y_train.mean(dim=0, keepdim=True)
    y_std = y_train.std(dim=0, keepdim=True).clamp_min(1e-6)
    y_train_n = (y_train - y_mean) / y_std
    xb = add_bias(x_train)
    reg = ridge * th.eye(xb.shape[1], dtype=xb.dtype)
    reg[-1, -1] = 0.0
    w = th.linalg.solve(xb.T @ xb + reg, xb.T @ y_train_n)
    pred_n = add_bias(x_test) @ w
    pred = pred_n * y_std + y_mean
    mse = F.mse_loss(pred, y_test).item()
    var = y_test.var(dim=0, unbiased=False).mean().item()
    r2 = 1.0 - mse / max(var, 1e-8)
    return {"mse": mse, "var": var, "r2": float(max(min(r2, 1.0), -1.0))}


def train_linear_classifier(x, labels, n_classes, train_idx, test_idx, epochs, lr, seed, sample_weights=None):
    th.manual_seed(seed)
    x_train, x_test = x[train_idx], x[test_idx]
    y_train, y_test = labels[train_idx], labels[test_idx]
    w_train = None
    if sample_weights is not None:
        w_train = sample_weights[train_idx].float()
        w_train = w_train / w_train.mean().clamp_min(1e-6)
    x_train, x_test = standardize_train_test(x_train, x_test)
    w = th.zeros(x_train.shape[1], n_classes, requires_grad=True)
    b = th.zeros(n_classes, requires_grad=True)
    opt = th.optim.Adam([w, b], lr=lr)
    for _ in range(epochs):
        logits = x_train @ w + b
        loss_vec = F.cross_entropy(logits, y_train, reduction="none")
        loss = loss_vec.mean() if w_train is None else (loss_vec * w_train).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    with th.no_grad():
        train_logits = x_train @ w + b
        test_logits = x_test @ w + b
        train_acc = (train_logits.argmax(dim=1) == y_train).float().mean().item()
        test_acc = (test_logits.argmax(dim=1) == y_test).float().mean().item()
        test_ce = F.cross_entropy(test_logits, y_test).item()
    return {
        "weight": w.detach(),
        "bias": b.detach(),
        "train_acc": train_acc,
        "test_acc": test_acc,
        "test_ce": test_ce,
        "x_mean": x[train_idx].mean(dim=0, keepdim=True),
        "x_std": x[train_idx].std(dim=0, keepdim=True).clamp_min(1e-6),
    }


def train_mlp_classifier(
    x,
    labels,
    n_classes,
    train_idx,
    test_idx,
    epochs,
    lr,
    seed,
    hidden_dim,
    weight_decay,
    sample_weights=None,
):
    th.manual_seed(seed)
    x_train, x_test = x[train_idx], x[test_idx]
    y_train, y_test = labels[train_idx], labels[test_idx]
    w_train = None
    if sample_weights is not None:
        w_train = sample_weights[train_idx].float()
        w_train = w_train / w_train.mean().clamp_min(1e-6)
    x_train, x_test = standardize_train_test(x_train, x_test)
    model = th.nn.Sequential(
        th.nn.Linear(x_train.shape[1], hidden_dim),
        th.nn.ReLU(),
        th.nn.Linear(hidden_dim, n_classes),
    )
    opt = th.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    for _ in range(epochs):
        logits = model(x_train)
        loss_vec = F.cross_entropy(logits, y_train, reduction="none")
        loss = loss_vec.mean() if w_train is None else (loss_vec * w_train).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    with th.no_grad():
        train_logits = model(x_train)
        test_logits = model(x_test)
        train_acc = (train_logits.argmax(dim=1) == y_train).float().mean().item()
        test_acc = (test_logits.argmax(dim=1) == y_test).float().mean().item()
        test_ce = F.cross_entropy(test_logits, y_test).item()
    return {
        "model_type": "mlp",
        "module": model.eval(),
        "train_acc": train_acc,
        "test_acc": test_acc,
        "test_ce": test_ce,
        "x_mean": x[train_idx].mean(dim=0, keepdim=True),
        "x_std": x[train_idx].std(dim=0, keepdim=True).clamp_min(1e-6),
        "hidden_dim": hidden_dim,
        "weight_decay": weight_decay,
    }


def train_probe_classifier(x, labels, n_classes, train_idx, test_idx, args, seed, sample_weights=None):
    if args.probe_model == "mlp":
        return train_mlp_classifier(
            x,
            labels,
            n_classes,
            train_idx,
            test_idx,
            args.probe_epochs,
            args.probe_lr,
            seed,
            args.probe_hidden_dim,
            args.probe_weight_decay,
            sample_weights=sample_weights,
        )
    model = train_linear_classifier(
        x,
        labels,
        n_classes,
        train_idx,
        test_idx,
        args.probe_epochs,
        args.probe_lr,
        seed,
        sample_weights=sample_weights,
    )
    model["model_type"] = "linear"
    return model


def classifier_logits(model, x):
    x_norm = (x - model["x_mean"]) / model["x_std"]
    if model.get("model_type") == "mlp":
        with th.no_grad():
            return model["module"](x_norm)
    return x_norm @ model["weight"] + model["bias"]


def paired_resampling_report(deltas, n_bootstrap, n_sign_permutations, alpha, seed):
    deltas = deltas.detach().float().reshape(-1)
    if deltas.numel() == 0:
        return {
            "mean": 0.0,
            "ci_low": 0.0,
            "ci_high": 0.0,
            "p_value_positive": 1.0,
            "passes_positive": False,
            "n": 0,
        }
    mean = deltas.mean().item()
    gen = th.Generator()
    gen.manual_seed(seed)

    if n_bootstrap > 0:
        boot_means = []
        n = deltas.numel()
        for _ in range(n_bootstrap):
            idx = th.randint(0, n, (n,), generator=gen)
            boot_means.append(deltas[idx].mean())
        boot = th.stack(boot_means)
        ci_low = th.quantile(boot, alpha / 2.0).item()
        ci_high = th.quantile(boot, 1.0 - alpha / 2.0).item()
    else:
        ci_low = mean
        ci_high = mean

    if n_sign_permutations > 0:
        perm_means = []
        for _ in range(n_sign_permutations):
            signs = th.randint(0, 2, deltas.shape, generator=gen, dtype=th.int64).float()
            signs = signs * 2.0 - 1.0
            perm_means.append((deltas * signs).mean())
        perm = th.stack(perm_means)
        p_value = ((perm >= mean).float().sum().item() + 1.0) / (n_sign_permutations + 1.0)
    else:
        p_value = 0.0 if mean > 0.0 else 1.0

    return {
        "mean": mean,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "p_value_positive": p_value,
        "passes_positive": ci_low > 0.0 and p_value <= alpha,
        "n": int(deltas.numel()),
    }


def build_agent_features(obs, agent_ids=None):
    n = obs.shape[1]
    if agent_ids is None:
        one_hot = th.eye(n).unsqueeze(0).expand(obs.shape[0], -1, -1)
    else:
        one_hot = F.one_hot(agent_ids, num_classes=n).float()
    return one_hot


def compute_teacher_messages(module, obs, obs_dim, time_seq):
    enhanced = call_comm(module, obs, build_seq(obs, time_seq))
    msg = message_part(enhanced, obs_dim)
    return msg


def compute_teacher_matrix(module, obs, n_agents):
    if not hasattr(module, "communication_matrix"):
        matrix = th.ones(obs.shape[0], n_agents, n_agents, dtype=obs.dtype)
    else:
        matrix = module.communication_matrix(obs)
        if not th.is_tensor(matrix):
            matrix = th.as_tensor(matrix, dtype=obs.dtype)
        matrix = matrix.to(dtype=obs.dtype)
    eye = th.eye(n_agents, dtype=obs.dtype).unsqueeze(0)
    return matrix.clamp(0.0, 1.0) * (1.0 - eye)


def flatten_agent_samples(obs, actions, msg=None):
    b, n, _ = obs.shape
    ids = build_agent_features(obs).reshape(b * n, n)
    x_local = th.cat([obs.reshape(b * n, -1), ids], dim=1)
    y = actions.reshape(b * n).long()
    if msg is None:
        return x_local, y
    x_comm = th.cat([obs.reshape(b * n, -1), msg.reshape(b * n, -1), ids], dim=1)
    return x_comm, y


def build_central_features(state, obs, actions):
    b, n, _ = obs.shape
    state_rep = state.unsqueeze(1).expand(-1, n, -1).reshape(b * n, -1)
    ids = build_agent_features(obs).reshape(b * n, n)
    y = actions.reshape(b * n).long()
    return th.cat([state_rep, ids], dim=1), y


def action_group_labels(actions, n_actions):
    labels = th.zeros_like(actions)
    labels[(actions >= 2) & (actions <= 5)] = 1
    labels[actions >= 6] = 2
    if n_actions <= 6:
        labels = actions.clamp(max=max(n_actions - 1, 1))
    return labels.long(), int(labels.max().item() + 1)


def decision_labels(actions, args):
    n_actions = int(actions.max().item() + 1)
    label_kind = getattr(args, "decision_label", "raw_action")
    if label_kind == "action_group":
        labels, n_classes = action_group_labels(actions, n_actions)
        return labels, n_classes, "action_group"
    if label_kind != "raw_action":
        raise RuntimeError(f"Unknown decision label kind: {label_kind}")
    return actions.long(), n_actions, "raw_action"


def fact_values_from_sender(obs, fact):
    sender = fact["sender"]
    fields = [f for f in fact["fields"] if f < obs.shape[-1]]
    if not fields:
        return None
    return obs[:, sender, fields]


def sender_observability_and_necessity(obs, facts, train_idx, test_idx, ridge):
    reports = []
    for fact in facts:
        z = fact_values_from_sender(obs, fact)
        if z is None:
            reports.append({"fact": fact["fact"], "passes": False, "reason": "fields outside obs"})
            continue
        sender_x = obs[:, fact["sender"], :]
        sender_score = ridge_regression_score(sender_x, z, train_idx, test_idx, ridge)
        receiver_scores = []
        for receiver in fact["receivers"]:
            rx = obs[:, receiver, :]
            receiver_scores.append(ridge_regression_score(rx, z, train_idx, test_idx, ridge))
        receiver_r2 = sum(item["r2"] for item in receiver_scores) / max(len(receiver_scores), 1)
        necessity_gain = sender_score["r2"] - receiver_r2
        reports.append(
            {
                "fact": fact["fact"],
                "sender": fact["sender"],
                "receivers": fact["receivers"],
                "sender_observability_r2": sender_score["r2"],
                "receiver_mean_r2": receiver_r2,
                "necessity_gain_r2": necessity_gain,
                "passes_sender_observable": sender_score["r2"] >= 0.5,
                "passes_receiver_necessary": necessity_gain >= 0.05,
            }
        )
    return reports


def return_weights(returns, n_agents):
    ret = returns.reshape(-1).float().repeat_interleave(n_agents)
    ret = (ret - ret.mean()) / ret.std().clamp_min(1e-6)
    return th.sigmoid(ret)


def message_shuffle_control(obs, actions, msg, test_idx_flat, comm_model, oracle_labels, args):
    b = obs.shape[0]
    test_labels = oracle_labels[test_idx_flat]
    x_true, _ = flatten_agent_samples(obs, actions, msg)
    true_logits = classifier_logits(comm_model, x_true[test_idx_flat])
    true_ce_each = F.cross_entropy(true_logits, test_labels, reduction="none")

    gen = th.Generator()
    gen.manual_seed(args.seed + 303)
    deltas = []
    shuffle_ces = []
    for _ in range(max(args.n_message_shuffles, 1)):
        perm = th.randperm(b, generator=gen)
        shuffled_msg = msg[perm]
        x_shuffle, _ = flatten_agent_samples(obs, actions, shuffled_msg)
        shuffle_logits = classifier_logits(comm_model, x_shuffle[test_idx_flat])
        shuffle_ce_each = F.cross_entropy(shuffle_logits, test_labels, reduction="none")
        deltas.append(shuffle_ce_each - true_ce_each)
        shuffle_ces.append(shuffle_ce_each.mean().item())
    delta = th.cat(deltas, dim=0)
    report = paired_resampling_report(
        delta,
        args.n_bootstrap,
        args.n_sign_permutations,
        args.stat_alpha,
        args.seed + 304,
    )
    return {
        "definition": (
            "Content specificity is a negative-control test: teacher messages are "
            "shuffled across held-out transitions while preserving agent slots. "
            "A valid message should outperform this shuffled-message control."
        ),
        "n_message_shuffles": args.n_message_shuffles,
        "true_message_ce": true_ce_each.mean().item(),
        "shuffled_message_ce_mean": sum(shuffle_ces) / max(len(shuffle_ces), 1),
        "shuffle_minus_true_ce": report["mean"],
        "shuffle_minus_true_resampling": report,
        "passes_content_specificity": report["passes_positive"],
    }


def conditional_decision_report(local_logits, comm_logits, test_labels, local_ce_each, comm_ce_each, args):
    mode = getattr(args, "conditional_decision_mode", "none")
    if mode == "none":
        return {
            "enabled": False,
            "mode": mode,
            "passes_conditional_decision_sufficient": False,
            "passes_statistical_conditional_decision_sufficient": False,
        }

    with th.no_grad():
        if mode == "local_entropy":
            probs = F.softmax(local_logits, dim=-1)
            uncertainty = -(probs * probs.clamp_min(1e-8).log()).sum(dim=-1)
            criterion = "top receiver-local predictive entropy"
        elif mode == "local_loss":
            uncertainty = local_ce_each
            criterion = "top receiver-local oracle cross entropy"
        else:
            raise RuntimeError(f"Unknown conditional decision mode: {mode}")

        q = min(max(float(args.conditional_decision_quantile), 0.0), 1.0)
        threshold = th.quantile(uncertainty, 1.0 - q)
        selected = uncertainty >= threshold
        min_samples = max(int(args.min_conditional_decision_samples), 1)
        if int(selected.sum().item()) < min_samples:
            top_k = min(min_samples, uncertainty.numel())
            top_idx = th.topk(uncertainty, k=top_k).indices
            selected = th.zeros_like(uncertainty, dtype=th.bool)
            selected[top_idx] = True

        local_correct = (local_logits.argmax(dim=1) == test_labels).float()
        comm_correct = (comm_logits.argmax(dim=1) == test_labels).float()
        ce_delta = local_ce_each[selected] - comm_ce_each[selected]
        acc_delta = comm_correct[selected] - local_correct[selected]
        local_ce = local_ce_each[selected].mean().item()
        comm_ce = comm_ce_each[selected].mean().item()
        local_acc = local_correct[selected].mean().item()
        comm_acc = comm_correct[selected].mean().item()

    ce_report = paired_resampling_report(
        ce_delta,
        args.n_bootstrap,
        args.n_sign_permutations,
        args.stat_alpha,
        args.seed + 41,
    )
    acc_report = paired_resampling_report(
        acc_delta,
        args.n_bootstrap,
        args.n_sign_permutations,
        args.stat_alpha,
        args.seed + 42,
    )
    ce_gain = ce_report["mean"]
    accuracy_gain = acc_report["mean"]
    passes_point = (
        accuracy_gain >= args.min_decision_gain
        or ce_gain >= args.min_decision_ce_gain
        or ce_gain >= args.min_conditional_decision_nats
    )
    passes_stat = ce_report["passes_positive"] or acc_report["passes_positive"]
    return {
        "enabled": True,
        "mode": mode,
        "criterion": criterion,
        "definition": (
            "Conditional decision relevance measures message value only on "
            "predefined receiver-uncertain held-out samples. This estimates "
            "I(M; Y_dec | O_receiver, U_receiver=1), where U_receiver is "
            "computed without access to the teacher message."
        ),
        "selection_rule": {
            "quantile": args.conditional_decision_quantile,
            "min_samples": args.min_conditional_decision_samples,
            "selected_samples": int(selected.sum().item()),
            "total_test_samples": int(uncertainty.numel()),
            "threshold": threshold.item(),
        },
        "local_to_central_ce": local_ce,
        "comm_to_central_ce": comm_ce,
        "local_to_central_acc": local_acc,
        "comm_to_central_acc": comm_acc,
        "ce_gain": ce_gain,
        "accuracy_gain": accuracy_gain,
        "conditional_decision_value": {
            "estimand": "I(M; Y_dec | O_receiver, U_receiver=1) approximated by predictive log-loss reduction",
            "nats_per_agent_step": ce_gain,
            "bits_per_agent_step": ce_gain / math.log(2.0),
            "resampling": ce_report,
            "passes_minimum_value": ce_gain >= args.min_conditional_decision_nats,
            "minimum_required_nats": args.min_conditional_decision_nats,
        },
        "ce_gain_resampling": ce_report,
        "accuracy_gain_resampling": acc_report,
        "passes_conditional_decision_sufficient": passes_point,
        "passes_statistical_conditional_decision_sufficient": passes_stat,
    }


def decision_sufficiency(obs, state, actions, msg, train_idx_flat, test_idx_flat, args, returns=None):
    y_decision, n_decision_classes, label_kind = decision_labels(actions, args)
    x_central, y_decision = build_central_features(state, obs, y_decision)
    oracle_kind = args.decision_oracle
    if oracle_kind == "auto":
        oracle_kind = "return" if returns is not None else "behavior"
    weights = return_weights(returns, obs.shape[1]) if oracle_kind == "return" and returns is not None else None
    central = train_probe_classifier(
        x_central,
        y_decision,
        n_decision_classes,
        train_idx_flat,
        test_idx_flat,
        args,
        args.seed,
        sample_weights=weights,
    )
    with th.no_grad():
        oracle_labels = classifier_logits(central, x_central).argmax(dim=1)

    x_local, _ = flatten_agent_samples(obs, actions)
    x_comm, _ = flatten_agent_samples(obs, actions, msg)
    local = train_probe_classifier(
        x_local, oracle_labels, n_decision_classes, train_idx_flat, test_idx_flat, args, args.seed + 1
    )
    comm = train_probe_classifier(
        x_comm, oracle_labels, n_decision_classes, train_idx_flat, test_idx_flat, args, args.seed + 2
    )
    with th.no_grad():
        local_logits = classifier_logits(local, x_local[test_idx_flat])
        comm_logits = classifier_logits(comm, x_comm[test_idx_flat])
        test_labels = oracle_labels[test_idx_flat]
        local_ce_each = F.cross_entropy(local_logits, test_labels, reduction="none")
        comm_ce_each = F.cross_entropy(comm_logits, test_labels, reduction="none")
        local_correct = (local_logits.argmax(dim=1) == test_labels).float()
        comm_correct = (comm_logits.argmax(dim=1) == test_labels).float()
    ce_report = paired_resampling_report(
        local_ce_each - comm_ce_each,
        args.n_bootstrap,
        args.n_sign_permutations,
        args.stat_alpha,
        args.seed + 11,
    )
    acc_report = paired_resampling_report(
        comm_correct - local_correct,
        args.n_bootstrap,
        args.n_sign_permutations,
        args.stat_alpha,
        args.seed + 12,
    )
    accuracy_gain = acc_report["mean"]
    ce_gain = ce_report["mean"]
    conditional_decision_value_nats = ce_gain
    conditional_decision_value_bits = conditional_decision_value_nats / math.log(2.0)
    content = message_shuffle_control(
        obs,
        actions,
        msg,
        test_idx_flat,
        comm,
        oracle_labels,
        args,
    )
    conditional = conditional_decision_report(
        local_logits,
        comm_logits,
        test_labels,
        local_ce_each,
        comm_ce_each,
        args,
    )
    passes_statistical_decision = (
        ce_report["passes_positive"]
        or acc_report["passes_positive"]
        or conditional["passes_statistical_conditional_decision_sufficient"]
    )
    passes_decision = (
        accuracy_gain >= args.min_decision_gain
        or ce_gain >= args.min_decision_ce_gain
        or conditional_decision_value_nats >= args.min_conditional_decision_nats
        or conditional["passes_conditional_decision_sufficient"]
    )
    return {
        "definition": (
            "Decision sufficiency is measured as how much local observation plus "
            "teacher message improves matching a centralized state-conditioned "
            "decision oracle. The primary label can be raw SMAC actions, which "
            "preserve movement direction and attack-target choices, or coarser "
            "action groups for robustness ablations. "
            "DRC-v5 uses an advantage/return-weighted oracle when replay returns are "
            "available, reports held-out resampling evidence, and checks a "
            "shuffled-message negative control. The decision oracle can be either "
            "a linear probe or a held-out MLP probe."
        ),
        "decision_label": label_kind,
        "oracle_kind": oracle_kind,
        "probe_model": args.probe_model,
        "probe_hidden_dim": args.probe_hidden_dim if args.probe_model == "mlp" else None,
        "has_return_weights": weights is not None,
        "central_proxy_test_acc": central["test_acc"],
        "local_to_central_test_acc": local["test_acc"],
        "comm_to_central_test_acc": comm["test_acc"],
        "accuracy_gain": accuracy_gain,
        "local_to_central_ce": local["test_ce"],
        "comm_to_central_ce": comm["test_ce"],
        "ce_gain": ce_gain,
        "conditional_decision_value": {
            "definition": (
                "Held-out CE(local-only decision probe) - CE(local+message decision probe). "
                "Under a calibrated probabilistic probe, this is a variational estimate "
                "of the conditional information contributed by the message about the "
                "decision oracle given the receiver-local observation."
            ),
            "estimand": "I(M; Y_dec | O_receiver) approximated by predictive log-loss reduction",
            "nats_per_agent_step": conditional_decision_value_nats,
            "bits_per_agent_step": conditional_decision_value_bits,
            "resampling": ce_report,
            "passes_minimum_value": conditional_decision_value_nats >= args.min_conditional_decision_nats,
            "minimum_required_nats": args.min_conditional_decision_nats,
        },
        "ce_gain_resampling": ce_report,
        "accuracy_gain_resampling": acc_report,
        "conditional_uncertain_decision_value": conditional,
        "content_specificity": content,
        "passes_statistical_decision_sufficient": passes_statistical_decision,
        "resampling_config": {
            "n_bootstrap": args.n_bootstrap,
            "n_sign_permutations": args.n_sign_permutations,
            "alpha": args.stat_alpha,
        },
        "passes_decision_sufficient": passes_decision,
        "central_model": central,
        "comm_model": comm,
        "oracle_labels": oracle_labels,
        "n_decision_classes": n_decision_classes,
        "n_action_groups": n_decision_classes if label_kind == "action_group" else None,
    }


def causal_usefulness(obs, actions, msg, matrix, facts, decision_report, test_idx_flat, args):
    comm_model = decision_report["comm_model"]
    oracle_labels = decision_report["oracle_labels"]
    b, n, _ = obs.shape
    base_x, _ = flatten_agent_samples(obs, actions, msg)
    base_logits = classifier_logits(comm_model, base_x[test_idx_flat])
    test_labels = oracle_labels[test_idx_flat]
    base_ce_each = F.cross_entropy(base_logits, test_labels, reduction="none")
    base_ce = base_ce_each.mean().item()

    def drop_sender_receiver_edge(message, receiver, sender):
        dropped = message.clone()
        packed_senders = n - 1
        if packed_senders > 0 and message.shape[-1] > 0 and message.shape[-1] % packed_senders == 0:
            block_dim = message.shape[-1] // packed_senders
            offset = 0
            for candidate_sender in range(n):
                if candidate_sender == receiver:
                    continue
                if candidate_sender == sender:
                    start = offset * block_dim
                    end = start + block_dim
                    gate = (1.0 - matrix[:, receiver, sender]).view(b, 1)
                    dropped[:, receiver, start:end] = dropped[:, receiver, start:end] * gate
                    return dropped
                offset += 1
        gate = (1.0 - matrix[:, receiver, sender]).view(b, 1)
        dropped[:, receiver, :] = dropped[:, receiver, :] * gate
        return dropped

    def edge_delta(receiver, sender):
        receiver_mask = (test_idx_flat % n) == receiver
        if int(receiver_mask.sum().item()) == 0:
            return None
        receiver_test_idx = test_idx_flat[receiver_mask]
        receiver_labels = oracle_labels[receiver_test_idx]
        receiver_base_ce_each = base_ce_each[receiver_mask]
        msg_drop = drop_sender_receiver_edge(msg, receiver, sender)
        drop_x, _ = flatten_agent_samples(obs, actions, msg_drop)
        drop_logits = classifier_logits(comm_model, drop_x[receiver_test_idx])
        drop_ce_each = F.cross_entropy(drop_logits, receiver_labels, reduction="none")
        return {
            "receiver": receiver,
            "sender": sender,
            "base_ce": receiver_base_ce_each.mean().item(),
            "edge_dropped_ce": drop_ce_each.mean().item(),
            "causal_ce_increase": (drop_ce_each - receiver_base_ce_each).mean().item(),
            "active_rate": matrix[:, receiver, sender].mean().item(),
            "n_test_agent_steps": int(receiver_test_idx.numel()),
        }

    reports = []
    for fact in facts:
        msg_drop = msg.clone()
        receivers = [r for r in fact["receivers"] if r < n]
        sender = fact["sender"]
        active_rate = None
        if receivers:
            active = matrix[:, receivers, sender].reshape(b, len(receivers), 1)
            active_rate = active.mean().item()
            msg_drop[:, receivers, :] = msg_drop[:, receivers, :] * (1.0 - active)
        drop_x, _ = flatten_agent_samples(obs, actions, msg_drop)
        drop_logits = classifier_logits(comm_model, drop_x[test_idx_flat])
        drop_ce_each = F.cross_entropy(drop_logits, test_labels, reduction="none")
        drop_ce = drop_ce_each.mean().item()
        resampling = paired_resampling_report(
            drop_ce_each - base_ce_each,
            args.n_bootstrap,
            args.n_sign_permutations,
            args.stat_alpha,
            args.seed + 101 + len(reports),
        )
        reports.append(
            {
                "fact": fact["fact"],
                "sender": sender,
                "receivers": receivers,
                "base_ce": base_ce,
                "edge_dropped_ce": drop_ce,
                "causal_ce_increase": drop_ce - base_ce,
                "active_rate": active_rate,
                "causal_ce_resampling": resampling,
                "passes_causally_useful": drop_ce > base_ce,
                "passes_statistical_causally_useful": resampling["passes_positive"],
            }
        )
    edge_reports = []
    for receiver in range(n):
        for sender in range(n):
            if sender == receiver:
                continue
            row = edge_delta(receiver, sender)
            if row is not None:
                row["passes_causally_useful"] = row["causal_ce_increase"] > 0.0
                edge_reports.append(row)
    mean_increase = sum(r["causal_ce_increase"] for r in reports) / max(len(reports), 1)
    fact_deltas = th.tensor([r["causal_ce_increase"] for r in reports], dtype=base_ce_each.dtype)
    mean_report = paired_resampling_report(
        fact_deltas,
        args.n_bootstrap,
        args.n_sign_permutations,
        args.stat_alpha,
        args.seed + 199,
    )
    all_fact_statistical = all(r["passes_statistical_causally_useful"] for r in reports) if reports else False
    return {
        "definition": (
            "Causal usefulness is approximated by an offline intervention: remove "
            "the certified sender-to-receiver message edge and measure whether "
            "matching the centralized decision proxy becomes harder."
        ),
        "mean_causal_ce_increase": mean_increase,
        "mean_causal_ce_resampling": mean_report,
        "fact_reports": reports,
        "edge_reports": edge_reports,
        "passes_causally_useful": mean_increase > 0.0,
        "passes_statistical_causally_useful": mean_report["passes_positive"] or all_fact_statistical,
        "all_fact_level_interventions_significant": all_fact_statistical,
    }


def load_fact_subset(path, map_name, default_facts):
    if not path:
        return default_facts, None
    item = json.loads(Path(path).read_text())
    maps = item.get("maps", {})
    if map_name not in maps:
        raise RuntimeError(f"Fact subset manifest {path} has no entry for map {map_name}")
    allowed = set(maps[map_name].get("certified_fact_names", []))
    facts = [fact for fact in default_facts if fact.get("fact") in allowed]
    if not facts:
        raise RuntimeError(f"Fact subset manifest {path} selected no facts for {map_name}")
    note = (
        "This run uses a preregistered receiver-necessity-pruned fact subset; "
        "facts outside the subset are not counted as required communication facts."
    )
    return facts, {"path": str(path), "certified_fact_names": sorted(allowed), "note": note}


def bounded_positive(value, cap):
    return min(max(float(value), 0.0), float(cap))


def static_certificate(module, map_name, obs, spec, required_facts=None, fact_subset_info=None):
    obs_small = obs[: min(16, obs.shape[0])]
    matrix = compute_teacher_matrix(module, obs_small, spec["n_agents"])
    task_reports = run_task_probes(module, map_name, obs_small.shape[0], matrix)
    definition_note = ""
    if fact_subset_info:
        definition_note = fact_subset_info["note"]
    completeness = build_completeness_report(
        map_name,
        task_reports,
        matrix,
        required_facts=required_facts,
        definition_note=definition_note,
    )
    return task_reports, completeness


def strip_large_tensors(obj):
    if isinstance(obj, dict):
        return {
            k: strip_large_tensors(v)
            for k, v in obj.items()
            if k not in ("weight", "bias", "x_mean", "x_std", "module", "oracle_labels", "comm_model", "central_model")
        }
    if isinstance(obj, list):
        return [strip_large_tensors(v) for v in obj]
    if th.is_tensor(obj):
        return obj.detach().cpu().tolist()
    return obj


def build_formal_certificate(result, args):
    decision = result["decision_sufficiency"]
    causal = result["causal_usefulness"]
    content = decision["content_specificity"]
    return {
        "name": "Decision-Relevant Certification",
        "scope": (
            "Offline certification of a frozen teacher communication policy before "
            "student RL. The certificate tests whether messages transmit task "
            "facts that are observable by senders, needed by receivers, complete "
            "for the declared task facts, sufficient for decentralized decision "
            "prediction, and causally useful under edge interventions."
        ),
        "data_split": {
            "unit": "transition-agent samples for decision probes; transitions for fact probes",
            "train_fraction": 0.7,
            "held_out_fraction": 0.3,
            "note": "Acceptance is computed on held-out probe samples where applicable.",
        },
        "gates": [
            {
                "gate": "sender_observable",
                "estimand": "R2_k = R2(z_k ~ o_sender(k)) for each required task fact z_k",
                "null_hypothesis": "The declared sender observation does not contain the task fact.",
                "estimator": "Held-out ridge regression from sender observation fields to task-fact values.",
                "acceptance_rule": "All required facts must have sender R2 >= 0.5.",
                "observed_value": result["scores"]["sender_observable_rate"],
                "passes": result["scores"]["sender_observable_rate"] >= 1.0,
            },
            {
                "gate": "receiver_necessary",
                "estimand": (
                    "Need_k = R2(z_k ~ o_sender(k)) - mean_j R2(z_k ~ o_receiver(j))"
                ),
                "null_hypothesis": "Receivers already locally observe the fact as well as the sender.",
                "estimator": "Matched held-out ridge probes for the sender and declared receivers.",
                "acceptance_rule": (
                    f"Receiver-necessity pass rate must be >= {args.min_receiver_necessity_rate}; "
                    "each passing fact has Need_k >= 0.05."
                ),
                "observed_value": result["scores"]["receiver_necessary_rate"],
                "passes": result["scores"]["receiver_necessary_rate"] >= args.min_receiver_necessity_rate,
            },
            {
                "gate": "task_fact_complete",
                "estimand": "Coverage = covered_required_task_facts / required_task_facts.",
                "null_hypothesis": "The teacher omits at least one declared decision-relevant task fact.",
                "estimator": "Map-specific perturbation probes and required-edge checks.",
                "acceptance_rule": "Coverage must equal 1.0.",
                "observed_value": result["scores"]["task_fact_completeness"],
                "passes": result["scores"]["task_fact_completeness"] >= 1.0,
            },
            {
                "gate": "decision_sufficient",
                "estimand": (
                    "Delta_dec = CE(local probe, centralized oracle) - "
                    "CE(local+message probe, centralized oracle), interpreted as "
                    "a variational conditional decision-information estimate for "
                    "I(M; Y_dec | O_receiver)"
                ),
                "null_hypothesis": "Teacher messages do not improve decentralized matching to the centralized oracle.",
                "estimator": (
                    "Held-out paired cross-entropy and accuracy differences against a "
                    "state-conditioned decision oracle; return-weighted when rewards "
                    "are available and decision_oracle=auto/return."
                ),
                "acceptance_rule": (
                    f"Point estimate must satisfy accuracy gain >= {args.min_decision_gain} "
                    f"or CE gain >= {args.min_decision_ce_gain} or conditional decision "
                    f"value >= {args.min_conditional_decision_nats} nats; if requested, paired "
                    f"resampling must have lower CI > 0 and sign-randomization p <= {args.stat_alpha}."
                ),
                "observed_value": {
                    "decision_label": decision.get("decision_label"),
                    "ce_gain": decision["ce_gain"],
                    "accuracy_gain": decision["accuracy_gain"],
                    "conditional_decision_value_nats": decision["conditional_decision_value"]["nats_per_agent_step"],
                    "conditional_decision_value_bits": decision["conditional_decision_value"]["bits_per_agent_step"],
                    "conditional_uncertain_decision": decision.get(
                        "conditional_uncertain_decision_value",
                        {"enabled": False},
                    ),
                    "ce_ci": [
                        decision["ce_gain_resampling"]["ci_low"],
                        decision["ce_gain_resampling"]["ci_high"],
                    ],
                    "ce_p_value": decision["ce_gain_resampling"]["p_value_positive"],
                    "passes_point_gate": decision["passes_decision_sufficient"],
                    "passes_statistical_gate": decision["passes_statistical_decision_sufficient"],
                },
                "passes": decision["passes_decision_sufficient"]
                and (
                    not result["requires_statistical_significance"]
                    or decision["passes_statistical_decision_sufficient"]
                ),
            },
            {
                "gate": "causally_useful",
                "estimand": (
                    "Delta_causal = CE(edge-deleted message, oracle) - "
                    "CE(full teacher message, oracle)"
                ),
                "null_hypothesis": "Deleting certified sender-to-receiver edges does not hurt decision matching.",
                "estimator": (
                    "Offline do-intervention on declared communication edges with paired "
                    "held-out cross-entropy differences."
                ),
                "acceptance_rule": (
                    "Mean causal CE increase must be positive; if requested, paired "
                    "resampling must pass the positive-effect gate."
                ),
                "observed_value": {
                    "mean_ce_increase": causal["mean_causal_ce_increase"],
                    "ci": [
                        causal["mean_causal_ce_resampling"]["ci_low"],
                        causal["mean_causal_ce_resampling"]["ci_high"],
                    ],
                    "p_value": causal["mean_causal_ce_resampling"]["p_value_positive"],
                    "passes_point_gate": causal["passes_causally_useful"],
                    "passes_statistical_gate": causal["passes_statistical_causally_useful"],
                },
                "passes": causal["passes_causally_useful"]
                and (
                    not result["requires_statistical_significance"]
                    or causal["passes_statistical_causally_useful"]
                ),
            },
            {
                "gate": "content_specificity_negative_control",
                "estimand": (
                    "Delta_shuffle = CE(shuffled messages, oracle) - CE(true messages, oracle)"
                ),
                "null_hypothesis": "The measured decision gain is not tied to semantically aligned message content.",
                "estimator": (
                    "Message-shuffle negative control that preserves agent slots and "
                    "message dimensionality while breaking transition-level alignment."
                ),
                "acceptance_rule": (
                    "If requested, true messages must beat shuffled messages with positive "
                    "paired resampling evidence."
                ),
                "observed_value": {
                    "shuffle_minus_true_ce": content["shuffle_minus_true_ce"],
                    "ci": [
                        content["shuffle_minus_true_resampling"]["ci_low"],
                        content["shuffle_minus_true_resampling"]["ci_high"],
                    ],
                    "p_value": content["shuffle_minus_true_resampling"]["p_value_positive"],
                    "passes": content["passes_content_specificity"],
                    "gate_required": result["requires_content_control"],
                },
                "passes": (not result["requires_content_control"]) or content["passes_content_specificity"],
            },
        ],
        "overall_acceptance_rule": (
            "Accept only if sender_observable, receiver_necessary, "
            "task_fact_complete, decision_sufficient, and causally_useful pass "
            "at their configured thresholds; optional statistical and "
            "content-specificity gates are enforced when enabled."
        ),
        "accepted": result["accepted"],
    }


def write_markdown(path, result, sources):
    lines = [
        "# Decision-Relevant Communication Certification",
        "",
        f"- map: `{result['map_name']}`",
        f"- teacher: `{result['comm_code']}`",
        f"- buffers: `{result['buffer_root']}`",
        f"- samples: `{result['num_transitions']}` transitions",
        f"- accepted: `{result['accepted']}`",
        "",
        "## Academic Basis",
        "",
    ]
    for item in sources:
        lines.append(f"- {item}")
    lines += [
        "",
        "## Scores",
        "",
        f"- sender observable rate: `{result['scores']['sender_observable_rate']:.4f}`",
        f"- receiver necessary rate: `{result['scores']['receiver_necessary_rate']:.4f}`",
        f"- task-fact completeness: `{result['scores']['task_fact_completeness']:.4f}`",
        f"- decision sufficiency gain: `{result['scores']['decision_sufficiency_gain']:.4f}`",
        f"- conditional decision value: `{result['scores']['conditional_decision_value_nats']:.4f}` nats / `{result['scores']['conditional_decision_value_bits']:.4f}` bits per agent-step",
        f"- conditional uncertain-state decision value: `{result['scores'].get('conditional_uncertain_decision_value_nats', 0.0):.4f}` nats",
        f"- causal CE increase: `{result['scores']['causal_usefulness']:.4f}`",
        f"- decision CE gain 95% CI: `[{result['decision_sufficiency']['ce_gain_resampling']['ci_low']:.4f}, {result['decision_sufficiency']['ce_gain_resampling']['ci_high']:.4f}]`",
        f"- decision CE gain p-value: `{result['decision_sufficiency']['ce_gain_resampling']['p_value_positive']:.4f}`",
        f"- shuffled-minus-true message CE: `{result['decision_sufficiency']['content_specificity']['shuffle_minus_true_ce']:.4f}`",
        f"- shuffled-message control p-value: `{result['decision_sufficiency']['content_specificity']['shuffle_minus_true_resampling']['p_value_positive']:.4f}`",
        f"- causal CE increase 95% CI: `[{result['causal_usefulness']['mean_causal_ce_resampling']['ci_low']:.4f}, {result['causal_usefulness']['mean_causal_ce_resampling']['ci_high']:.4f}]`",
        f"- causal CE increase p-value: `{result['causal_usefulness']['mean_causal_ce_resampling']['p_value_positive']:.4f}`",
        f"- bandwidth penalty: `{result['scores']['bandwidth_penalty']:.4f}`",
        f"- final score: `{result['scores']['final_score']:.4f}`",
        "",
        "## Formal Certificate",
        "",
        result["formal_certificate"]["scope"],
        "",
        "| gate | estimand | null hypothesis | estimator | acceptance | observed | pass |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for gate in result["formal_certificate"]["gates"]:
        observed = gate["observed_value"]
        if isinstance(observed, dict):
            observed_text = json.dumps(observed, sort_keys=True)
        else:
            observed_text = f"{observed:.4f}" if isinstance(observed, float) else str(observed)
        lines.append(
            "| {gate} | {estimand} | {null} | {estimator} | {rule} | `{observed}` | `{passes}` |".format(
                gate=gate["gate"],
                estimand=gate["estimand"],
                null=gate["null_hypothesis"],
                estimator=gate["estimator"],
                rule=gate["acceptance_rule"],
                observed=observed_text.replace("|", "/"),
                passes=gate["passes"],
            )
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "This certificate selects a frozen teacher before downstream RL training. "
        "The teacher should only be used for student supervision if it passes the "
        "offline decision-relevance gates; downstream RL win-rate is reserved for "
        "final validation rather than teacher search.",
        "",
        "## Implementation Result",
        "",
        "The current implementation is DRC-v5. It uses a centralized "
        "state-conditioned decision oracle, weighted by offline returns when "
        "reward fields are available, and evaluates whether teacher messages "
        "improve decentralized matching to that oracle. The decision and causal "
        "effects are reported with paired bootstrap intervals and sign-randomization "
        "p-values on held-out samples. It also tests a shuffled-message negative "
        "control to reject teachers whose gains come only from extra input capacity. "
        "For harder maps, the oracle can be upgraded from a linear probe to a small "
        "held-out MLP probe.",
    ]
    Path(path).write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Offline decision-relevant LLM communication certification.")
    parser.add_argument("--map", required=True, choices=sorted(map_specs()))
    parser.add_argument("--comm-code", required=True)
    parser.add_argument("--buffer-root", default=str(ROOT / "data"))
    parser.add_argument("--max-files", type=int, default=64)
    parser.add_argument("--max-transitions", type=int, default=4096)
    parser.add_argument("--probe-epochs", type=int, default=80)
    parser.add_argument("--probe-lr", type=float, default=0.03)
    parser.add_argument("--probe-model", choices=["linear", "mlp"], default="linear")
    parser.add_argument("--probe-hidden-dim", type=int, default=128)
    parser.add_argument("--probe-weight-decay", type=float, default=1e-4)
    parser.add_argument("--ridge", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--gamma", type=float, default=0.99)
    parser.add_argument(
        "--decision-oracle",
        choices=["auto", "behavior", "return"],
        default="auto",
        help="Use behavior decision oracle, return-weighted oracle, or auto-select return when buffers contain rewards.",
    )
    parser.add_argument(
        "--decision-label",
        choices=["raw_action", "action_group"],
        default="raw_action",
        help=(
            "Decision label used to train the centralized oracle. raw_action preserves "
            "SMAC movement direction and attack-target choices; action_group keeps the "
            "older coarse stop/move/attack abstraction for robustness ablations."
        ),
    )
    parser.add_argument("--min-decision-gain", type=float, default=0.01)
    parser.add_argument("--min-decision-ce-gain", type=float, default=0.01)
    parser.add_argument(
        "--min-conditional-decision-nats",
        type=float,
        default=0.01,
        help=(
            "Minimum held-out log-loss reduction, in nats per agent-step, for treating "
            "messages as conditionally decision-informative given receiver-local observation."
        ),
    )
    parser.add_argument(
        "--conditional-decision-mode",
        choices=["none", "local_entropy", "local_loss"],
        default="none",
        help=(
            "Optional preregistered conditional decision-relevance gate. "
            "local_entropy evaluates message value on held-out receiver-local "
            "high-entropy samples; local_loss uses receiver-local high-loss samples."
        ),
    )
    parser.add_argument(
        "--conditional-decision-quantile",
        type=float,
        default=0.25,
        help="Fraction of held-out samples selected for the conditional decision gate.",
    )
    parser.add_argument(
        "--min-conditional-decision-samples",
        type=int,
        default=256,
        help="Minimum held-out agent-step samples for the conditional decision gate.",
    )
    parser.add_argument(
        "--min-receiver-necessity-rate",
        type=float,
        default=1.0,
        help="Minimum fraction of declared task facts that must pass receiver-necessity.",
    )
    parser.add_argument(
        "--fact-subset-manifest",
        default="",
        help=(
            "Optional preregistered manifest selecting receiver-necessary task facts "
            "for this certification run. Defaults to the full map task-fact spec."
        ),
    )
    parser.add_argument("--n-bootstrap", type=int, default=200)
    parser.add_argument("--n-sign-permutations", type=int, default=200)
    parser.add_argument("--stat-alpha", type=float, default=0.05)
    parser.add_argument(
        "--require-stat-significance",
        action="store_true",
        help="Require positive held-out resampling evidence for decision sufficiency and causal usefulness.",
    )
    parser.add_argument("--n-message-shuffles", type=int, default=8)
    parser.add_argument(
        "--require-content-control",
        action="store_true",
        help="Require true teacher messages to beat shuffled-message negative controls.",
    )
    parser.add_argument("--bandwidth-weight", type=float, default=0.05)
    parser.add_argument(
        "--score-gain-cap",
        type=float,
        default=1.0,
        help=(
            "Upper bound applied only to positive decision/causal gains in the "
            "ranking score. Raw gate evidence remains unchanged."
        ),
    )
    parser.add_argument(
        "--allow-obs-pad",
        action="store_true",
        help=(
            "Right-pad old replay buffers whose obs dimension is smaller than the "
            "current teacher spec after attempting to rebuild LMAC agent inputs. "
            "Use only for smoke tests; formal certificates should use shape-matched "
            "raw buffers that can be converted to obs+last_action+agent_id."
        ),
    )
    parser.add_argument("--out-json", default=None)
    parser.add_argument("--out-md", default=None)
    args = parser.parse_args()

    th.manual_seed(args.seed)
    specs = map_specs()
    spec = specs[args.map]
    module = load_module(args.comm_code)
    files = find_buffers(args.buffer_root, args.map, args.max_files)
    if not files:
        raise RuntimeError(f"No pkl buffers found under {args.buffer_root} for {args.map}")
    obs, state, actions, extras = load_buffer_tensors(
        files,
        args.max_transitions,
        expected_n_agents=spec["n_agents"],
        target_obs_dim=spec["obs_dim"],
        allow_obs_pad=args.allow_obs_pad,
        gamma=args.gamma,
    )
    if obs.shape[1] != spec["n_agents"]:
        raise RuntimeError(f"Buffer n_agents={obs.shape[1]} does not match map spec {spec['n_agents']}")
    obs_dim = spec["obs_dim"]
    if obs.shape[-1] < obs_dim:
        raise RuntimeError(f"Buffer obs_dim={obs.shape[-1]} is smaller than map spec {obs_dim}")
    obs = obs[:, :, :obs_dim].contiguous()

    msg = compute_teacher_messages(module, obs, obs_dim, spec["time_seq"])
    matrix = compute_teacher_matrix(module, obs, spec["n_agents"])
    returns = extras.get("returns")
    train_idx, test_idx = split_indices(obs.shape[0])
    flat_count = obs.shape[0] * obs.shape[1]
    train_idx_flat, test_idx_flat = split_indices(flat_count)

    facts, fact_subset_info = load_fact_subset(
        args.fact_subset_manifest,
        args.map,
        spec.get("required_task_facts", []),
    )
    observability = sender_observability_and_necessity(obs, facts, train_idx, test_idx, args.ridge)
    static_task_reports, completeness = static_certificate(
        module,
        args.map,
        obs,
        spec,
        required_facts=facts,
        fact_subset_info=fact_subset_info,
    )
    decision = decision_sufficiency(obs, state, actions, msg, train_idx_flat, test_idx_flat, args, returns=returns)
    causal = causal_usefulness(obs, actions, msg, matrix, facts, decision, test_idx_flat, args)

    sender_rate = sum(1 for r in observability if r.get("passes_sender_observable")) / max(len(observability), 1)
    necessity_rate = sum(1 for r in observability if r.get("passes_receiver_necessary")) / max(len(observability), 1)
    completeness_rate = completeness["coverage_rate"]
    conditional_decision = decision.get("conditional_uncertain_decision_value", {})
    conditional_decision_gain = 0.0
    if conditional_decision.get("enabled"):
        conditional_decision_gain = max(
            conditional_decision.get("accuracy_gain", 0.0),
            conditional_decision.get("ce_gain", 0.0),
        )
    decision_gain = max(decision["accuracy_gain"], decision["ce_gain"], conditional_decision_gain)
    causal_gain = causal["mean_causal_ce_increase"]
    edge_rate = matrix.sum().item() / max(matrix.shape[0] * spec["n_agents"] * (spec["n_agents"] - 1), 1)
    bandwidth_penalty = edge_rate * max(msg.shape[-1], 1)
    bounded_decision_gain = bounded_positive(decision_gain, args.score_gain_cap)
    bounded_causal_gain = bounded_positive(causal_gain, args.score_gain_cap)
    final_score = (
        sender_rate
        + necessity_rate
        + completeness_rate
        + bounded_decision_gain
        + bounded_causal_gain
        - args.bandwidth_weight * bandwidth_penalty
    )
    statistical_gate = (
        not args.require_stat_significance
        or (
            decision["passes_statistical_decision_sufficient"]
            and causal["passes_statistical_causally_useful"]
        )
    )
    content_gate = (
        not args.require_content_control
        or decision["content_specificity"]["passes_content_specificity"]
    )
    accepted = (
        sender_rate >= 1.0
        and necessity_rate >= args.min_receiver_necessity_rate
        and completeness_rate >= 1.0
        and decision["passes_decision_sufficient"]
        and causal["passes_causally_useful"]
        and statistical_gate
        and content_gate
    )

    sources = [
        "Information Bottleneck: Tishby et al. formulate relevant compression as preserving information about target variable Y while compressing X.",
        "DIAL/RIAL: Foerster et al. motivate communication under centralized training and decentralized execution.",
        "TarMAC and IC3Net: targeted communication and when-to-communicate are established MARL communication objectives.",
        "Social influence / causal influence MARL: counterfactual interventions and mutual information are used to quantify inter-agent influence.",
        "Conditional independence / conditional randomization tests motivate testing whether a candidate variable adds predictive information about an outcome after conditioning on existing covariates.",
        "Bootstrap and permutation/randomization tests provide non-parametric uncertainty estimates for fixed offline test statistics.",
        "Negative-control and shuffled-input tests are falsification checks for whether the measured effect is content-specific.",
        "Nonlinear held-out probes can reduce underfitting of the decision oracle on maps where the state-to-decision relation is not linearly separable.",
    ]
    result = {
        "method": "DRC-v5-mlp-or-linear-negative-control-probe",
        "map_name": args.map,
        "comm_code": str(args.comm_code),
        "buffer_root": str(args.buffer_root),
        "num_buffer_files": len(files),
        "num_transitions": int(obs.shape[0]),
        "message_dim": int(msg.shape[-1]),
        "matrix_edge_rate": edge_rate,
        "has_return_data": returns is not None,
        "decision_label": args.decision_label,
        "fact_subset": fact_subset_info,
        "requires_statistical_significance": args.require_stat_significance,
        "passes_statistical_gate": statistical_gate,
        "requires_content_control": args.require_content_control,
        "passes_content_gate": content_gate,
        "observability_and_necessity": observability,
        "static_task_probe_reports": static_task_reports,
        "task_fact_completeness": completeness,
        "decision_sufficiency": strip_large_tensors(decision),
        "causal_usefulness": causal,
        "scores": {
            "sender_observable_rate": sender_rate,
            "receiver_necessary_rate": necessity_rate,
            "task_fact_completeness": completeness_rate,
            "decision_sufficiency_gain": decision_gain,
            "conditional_decision_value_nats": decision["conditional_decision_value"]["nats_per_agent_step"],
            "conditional_decision_value_bits": decision["conditional_decision_value"]["bits_per_agent_step"],
            "conditional_uncertain_decision_gain": conditional_decision_gain,
            "conditional_uncertain_decision_value_nats": conditional_decision.get(
                "conditional_decision_value", {}
            ).get("nats_per_agent_step", 0.0),
            "causal_usefulness": causal_gain,
            "bounded_decision_gain_for_ranking": bounded_decision_gain,
            "bounded_causal_gain_for_ranking": bounded_causal_gain,
            "score_gain_cap": args.score_gain_cap,
            "bandwidth_penalty": bandwidth_penalty,
            "final_score": final_score,
        },
        "accepted": accepted,
        "academic_basis": sources,
        "note": (
            "Teacher selection should use this offline certificate before RL. "
            "Downstream RL is only for fixed-teacher student validation."
        ),
    }
    result["formal_certificate"] = build_formal_certificate(result, args)

    text = json.dumps(strip_large_tensors(result), indent=2)
    if args.out_json:
        Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out_json).write_text(text + "\n")
    if args.out_md:
        Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
        write_markdown(args.out_md, strip_large_tensors(result), sources)
    print(text)


if __name__ == "__main__":
    main()
