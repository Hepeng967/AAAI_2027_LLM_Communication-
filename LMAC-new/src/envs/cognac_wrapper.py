"""PyMARL adapter for the pinned COGNAC graph environments."""

from pathlib import Path

import numpy as np

from .multiagentenv import MultiAgentEnv
from .cognac_vendor.env import (
    BinaryConsensusNetworkEnvironment,
    RowFireFightingGraphEnvironment,
    SysAdminNetworkEnvironment,
)


class COGNACWrapper(MultiAgentEnv):
    def __init__(self, task, max_steps=100, graph_path=None, seed=0, **kwargs):
        self.task = task
        self.episode_limit = int(max_steps)
        self._seed = seed
        self._seed_pending = True

        if task in ("sysadmin_10", "binary_consensus_10"):
            if graph_path is None:
                graph_path = Path(__file__).with_name("cognac_assets") / "basic_directed_network_10.npy"
            graph_path = Path(graph_path)
            if not graph_path.is_absolute():
                graph_path = Path(__file__).resolve().parents[2] / graph_path
            adjacency = np.load(str(graph_path))
            if adjacency.shape != (10, 10):
                raise ValueError(f"Expected a 10x10 COGNAC graph, got {adjacency.shape}")
            cls = SysAdminNetworkEnvironment if task == "sysadmin_10" else BinaryConsensusNetworkEnvironment
            self.env = cls(
                adjacency_matrix=adjacency,
                max_steps=self.episode_limit,
                show_neighborhood_state=True,
                is_shared_reward=True,
            )
        elif task == "firefighting_10":
            self.env = RowFireFightingGraphEnvironment(
                n=10, max_steps=self.episode_limit, is_shared_reward=True
            )
        else:
            raise ValueError(f"Unknown COGNAC task: {task}")

        self.n_agents = self.env.n_agents
        self.n_actions = int(self.env.action_space(self.env.possible_agents[0]).n)
        self._obs_dict = None
        self._infos = None

    def reset(self, seed=None, options=None):
        reset_seed = seed
        if reset_seed is None and self._seed_pending:
            reset_seed = self._seed
        self._seed_pending = False
        self._obs_dict, self._infos = self.env.reset(seed=reset_seed, options=options)
        return self.get_obs(), self.get_state()

    def step(self, actions):
        action_dict = {agent: int(actions[i]) for i, agent in enumerate(self.env.possible_agents)}
        obs, rewards, terms, truncs, infos = self.env.step(action_dict)
        self._obs_dict, self._infos = obs, infos
        terminated = all(bool(terms[a]) for a in self.env.possible_agents)
        truncated = all(bool(truncs[a]) for a in self.env.possible_agents)
        # BinaryConsensus/SysAdmin replicate their summed global reward for every
        # agent. DefaultFFGReward keeps local rewards even when as_global=True,
        # and the official QMIX benchmark sums those per-agent values.
        if self.task == "firefighting_10":
            reward = float(sum(rewards.values()))
        else:
            reward = float(rewards[self.env.possible_agents[0]])
        info = self._episode_info(terminated, truncated)
        return self.get_obs(), reward, terminated, truncated, info

    def _episode_info(self, terminated, truncated):
        info = {"episode_limit": bool(truncated)}
        if self.task == "binary_consensus_10":
            state = np.asarray(self.env.state())
            info["success"] = float(terminated and not truncated and (np.all(state == 0) or np.all(state == 1)))
            info["consensus_fraction"] = float(max(np.mean(state == 0), np.mean(state == 1)))
        elif self.task == "sysadmin_10":
            state = np.asarray(self.env.state())
            info["healthy_machine_fraction"] = float(np.mean(state[:, 0] == 0))
        else:
            info["mean_fire_level"] = float(np.mean(self.env.state))
            info["all_fires_out"] = float(np.all(np.asarray(self.env.state) == 0))
        return info

    def _fixed_graph_obs(self, agent_id):
        mask = np.asarray(self.env.neighboring_masks[agent_id], dtype=np.float32)
        adjacency_row = np.asarray(self.env.adjacency_matrix[agent_id], dtype=np.float32)
        visible_ids = np.flatnonzero(mask)
        local = np.asarray(self._obs_dict[agent_id], dtype=np.float32)
        if self.task == "binary_consensus_10":
            values = np.zeros(self.n_agents, dtype=np.float32)
            values[visible_ids] = local.reshape(-1)
            return np.concatenate((values, mask, adjacency_row))
        values = np.zeros((self.n_agents, 2), dtype=np.float32)
        values[visible_ids] = local.reshape(-1, 2)
        return np.concatenate((values.reshape(-1) / 2.0, mask, adjacency_row))

    def get_obs_agent(self, agent_id):
        if self.task == "firefighting_10":
            return np.asarray(self._obs_dict[agent_id], dtype=np.float32).reshape(-1)
        return self._fixed_graph_obs(agent_id)

    def get_obs(self):
        return [self.get_obs_agent(i) for i in range(self.n_agents)]

    def get_obs_size(self):
        return {"binary_consensus_10": 30, "sysadmin_10": 40, "firefighting_10": 1}[self.task]

    def get_state(self):
        if self.task == "firefighting_10":
            return np.asarray(self.env.state, dtype=np.float32).reshape(-1) / float(self.env.max_fire_level)
        state = np.asarray(self.env.state(), dtype=np.float32).reshape(-1)
        return state / 2.0 if self.task == "sysadmin_10" else state

    def get_state_size(self):
        return {"binary_consensus_10": 10, "sysadmin_10": 20, "firefighting_10": 11}[self.task]

    def get_avail_agent_actions(self, agent_id):
        return [1] * self.n_actions

    def get_avail_actions(self):
        return [self.get_avail_agent_actions(i) for i in range(self.n_agents)]

    def get_total_actions(self):
        return self.n_actions

    def seed(self, seed=None):
        self._seed = seed
        self._seed_pending = True

    def close(self):
        close = getattr(self.env, "close", None)
        if close:
            close()

    def render(self):
        return self.env.render()

    def save_replay(self):
        pass
