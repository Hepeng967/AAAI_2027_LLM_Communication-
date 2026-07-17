#!/usr/bin/env python3
import argparse
import os
import pickle
import sys
from copy import deepcopy
from types import SimpleNamespace as SN

import torch as th
import yaml


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

for proxy_var in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"):
    os.environ.pop(proxy_var, None)

from components.transforms import OneHot
from controllers import REGISTRY as mac_REGISTRY
from runners import REGISTRY as runner_REGISTRY


MAP_ALIASES = {
    "10b": "1o_10b_vs_1r",
    "2r": "1o_2r_vs_4r",
    "5z": "5z_vs_1ul",
}


class NullLogger:
    def log_stat(self, *args, **kwargs):
        return None


def load_yaml(*parts):
    with open(os.path.join(PROJECT_ROOT, "src", "config", *parts), "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def recursive_update(dst, src):
    for key, value in src.items():
        if isinstance(value, dict):
            dst[key] = recursive_update(dst.get(key, {}), value)
        else:
            dst[key] = value
    return dst


def build_args(map_name, seed):
    config = load_yaml("default.yaml")
    recursive_update(config, load_yaml("envs", "sc2.yaml"))
    recursive_update(config, load_yaml("algs", "qmix.yaml"))

    config["env"] = "sc2"
    config["env_args"]["map_name"] = map_name
    config["env_args"]["seed"] = seed
    config["seed"] = seed
    config["use_cuda"] = False
    config["device"] = "cpu"
    config["use_wandb"] = False
    config["use_tensorboard"] = False
    config["save_model"] = False
    config["batch_size_run"] = 1
    config["test_nepisode"] = 1
    config["runner_log_interval"] = 10**9
    config["mac"] = "basic_mac"
    config["agent"] = "rnn"
    config["add_state"] = False

    args = SN(**config)
    args.env_args = deepcopy(config["env_args"])
    return args


def build_runner_and_mac(args):
    runner = runner_REGISTRY[args.runner](args=args, logger=NullLogger())
    env_info = runner.get_env_info()
    args.n_agents = env_info["n_agents"]
    args.n_actions = env_info["n_actions"]
    args.state_shape = env_info["state_shape"]

    scheme = {
        "state": {"vshape": env_info["state_shape"]},
        "obs": {"vshape": env_info["obs_shape"], "group": "agents"},
        "actions": {"vshape": (1,), "group": "agents", "dtype": th.long},
        "avail_actions": {
            "vshape": (env_info["n_actions"],),
            "group": "agents",
            "dtype": th.int,
        },
        "terminated": {"vshape": (1,), "dtype": th.uint8},
        "reward": {"vshape": (1,)},
        "actions_onehot": {
            "vshape": (env_info["n_actions"],),
            "group": "agents",
            "dtype": th.float32,
        },
    }
    groups = {"agents": args.n_agents}
    preprocess = {"actions": ("actions_onehot", [OneHot(out_dim=args.n_actions)])}
    mac = mac_REGISTRY[args.mac](scheme, groups, args)
    runner.setup(scheme=scheme, groups=groups, preprocess=preprocess, mac=mac)
    return runner


def save_episode(path, episode_batch, metadata=None):
    max_t = int(episode_batch.max_t_filled().item())
    end_t = max_t + 1
    sample = {
        "obs": episode_batch["obs"][:, :end_t].cpu(),
        "state": episode_batch["state"][:, :end_t].cpu(),
        "mask": episode_batch["filled"][:, :end_t].float().cpu(),
        "actions": episode_batch["actions"][:, :end_t].long().cpu(),
        "actions_onehot": episode_batch["actions_onehot"][:, :end_t].float().cpu(),
        "avail_actions": episode_batch["avail_actions"][:, :end_t].int().cpu(),
        "reward": episode_batch["reward"][:, :end_t].float().cpu(),
        "terminated": episode_batch["terminated"][:, :end_t].float().cpu(),
    }
    if metadata is not None:
        sample["metadata"] = dict(metadata)
    with open(path, "wb") as f:
        pickle.dump(sample, f)


def collect_split(output_root, map_name, split, count, seed, overwrite):
    out_dir = os.path.join(output_root, map_name)
    if split == "test":
        out_dir = os.path.join(out_dir, "test")
    os.makedirs(out_dir, exist_ok=True)

    existing = [name for name in os.listdir(out_dir) if name.endswith(".pkl")]
    if not overwrite and len(existing) >= count:
        print(f"[SKIP] {map_name}/{split}: already has {len(existing)} pkl files")
        return

    args = build_args(map_name, seed)
    runner = build_runner_and_mac(args)
    try:
        start_idx = 0 if overwrite else len(existing)
        test_mode = split == "test"
        for idx in range(start_idx, count):
            episode = runner.run(test_mode=test_mode)
            file_path = os.path.join(out_dir, f"{split}_traj_{idx:04d}.pkl")
            save_episode(
                file_path,
                episode,
                metadata={
                    "collector": "collect_lmac_buffers.py",
                    "schema": "formal_drc_buffer_v2",
                    "map_name": map_name,
                    "split": split,
                    "seed": seed,
                    "episode_index": idx,
                    "test_mode": test_mode,
                    "contains_return_fields": True,
                },
            )
            print(f"[SAVE] {file_path}")
    finally:
        runner.close_env()


def main():
    parser = argparse.ArgumentParser(description="Collect LMAC discriminator buffer trajectories.")
    parser.add_argument(
        "--maps",
        nargs="+",
        default=["1o_10b_vs_1r", "1o_2r_vs_4r", "5z_vs_1ul"],
        help="Map names or aliases: 10b, 2r, 5z",
    )
    parser.add_argument("--train-count", type=int, default=32)
    parser.add_argument("--test-count", type=int, default=32)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--output-root", default=os.path.join(PROJECT_ROOT, "data"))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    output_root = os.path.abspath(args.output_root)
    os.makedirs(output_root, exist_ok=True)
    maps = [MAP_ALIASES.get(name, name) for name in args.maps]
    for map_index, map_name in enumerate(maps):
        split_seed = args.seed + map_index * 1000
        collect_split(output_root, map_name, "train", args.train_count, split_seed, args.overwrite)
        collect_split(output_root, map_name, "test", args.test_count, split_seed + 500, args.overwrite)


if __name__ == "__main__":
    main()
