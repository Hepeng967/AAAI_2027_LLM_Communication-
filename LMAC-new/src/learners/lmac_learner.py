import copy
import os
import torch as th
from torch.optim import Adam, RMSprop

from components.episode_buffer import EpisodeBatch
from components.standarize_stream import RunningMeanStd
from components.certified_task_facts import CERTIFIED_TASK_FACT_EDGES
from modules.mixers.vdn import VDNMixer
from modules.mixers.qmix import QMixer
from controllers import REGISTRY as mac_REGISTRY
import torch.nn.functional as F
import torch.nn as nn


class LMAC_learner:
    def __init__(self, mac ,scheme, important_state,logger, args):
        self.args = args
        self.n_agents = args.n_agents
        self.mac = mac
        self.logger = logger
        
        self.params = list(mac.parameters())
        self.last_target_update_episode = 0

        self.mixer = None
        if args.mixer is not None:
            if args.mixer == "vdn":
                assert args.common_reward, "VDN only supports common reward setting"
                self.mixer = VDNMixer()
            elif args.mixer == "qmix":
                assert args.common_reward, "QMIX only supports common reward setting"
                self.mixer = QMixer(args)
            else:
                raise ValueError("Mixer {} not recognised.".format(args.mixer))
            self.params += list(self.mixer.parameters())
            self.target_mixer = copy.deepcopy(self.mixer) 
            
        self.important_state = important_state
        self.imp_dim = len(important_state)
        
        if self.args.optimiser == "RMSprop":
            self.optimiser = RMSprop(params=self.params, lr=args.lr, alpha=args.optim_alpha, eps=args.optim_eps)
        else:
            self.optimiser = Adam(params=self.params, lr=args.lr)
            
        # a little wasteful to deepcopy (e.g. duplicates action selector), but should work for any MAC
        self.target_mac = copy.deepcopy(mac)
        # LLM policy modules are imported Python modules: they are read-only and
        # deliberately removed by LMAC_MAC.__getstate__ because modules cannot be
        # deep-copied reliably. The target MAC still executes the same fixed WHAT
        # and teacher-matrix functions, so share these immutable module objects.
        self.target_mac.comm_modules = self.mac.comm_modules
        if not self.target_mac.comm_modules:
            raise RuntimeError(
                "Target MAC has no communication modules after deepcopy; "
                "cannot construct target-network messages."
            )

        self.training_steps = 0
        self.last_target_update_step = 0
        self.log_stats_t = -self.args.learner_log_interval - 1
        self.map_name = self._env_map_name()

        device = "cuda" if args.use_cuda and th.cuda.is_available() else "cpu"
        if self.args.standardise_returns:
            self.ret_ms = RunningMeanStd(shape=(self.n_agents,), device=device)
        if self.args.standardise_rewards:
            rew_shape = (1,) if self.args.common_reward else (self.n_agents,)
            self.rew_ms = RunningMeanStd(shape=rew_shape, device=device)    
    

    def train(self, batch: EpisodeBatch, t_env: int, episode_num: int):
        # Get the relevant quantities
        rewards = batch["reward"][:, :-1]
        actions = batch["actions"][:, :-1]
        terminated = batch["terminated"][:, :-1].float()
        mask = batch["filled"][:, :-1].float()
        mask[:, 1:] = mask[:, 1:] * (1 - terminated[:, :-1])
        avail_actions = batch["avail_actions"]

        states = batch['state'][:, :-1]

        if self.args.standardise_rewards:
            self.rew_ms.update(rewards)
            rewards = (rewards - self.rew_ms.mean) / th.sqrt(self.rew_ms.var)

        if self.args.common_reward:
            assert (
                rewards.size(2) == 1
            ), "Expected singular agent dimension for common rewards"
            # reshape rewards to be of shape (batch_size, episode_length, n_agents)
            rewards = rewards.expand(-1, -1, self.n_agents)

        mac_out, pred_states, pred_metas, latent_zs, latent_recons = [], [], [], [], []
        student_logits_seq, teacher_matrix_seq, student_probs_seq = [], [], []
        message_logits_seq, teacher_what_core_seq = [], []
        teacher_what_target_seq, message_probs_seq = [], []
        all_agent_inputs = self.mac.build_all_agent_inputs(batch)
        teacher_matrix_all, teacher_what_core_all, teacher_what_target_all = self.mac.build_teacher_masks(
            batch, teacher_inputs=all_agent_inputs
        )
        online_selector_outputs = self.mac.build_student_selector_outputs(
            batch, agent_inputs=all_agent_inputs
        )
        self.mac.init_hidden(batch.batch_size)
        for t in range(batch.max_seq_length):
            (
                agent_outs,
                pred_state,
                pred_meta,
                latent_z,
                latent_recon,
                student_logits,
                teacher_matrix,
                student_probs,
                message_logits,
                teacher_what_core,
                teacher_what_target,
                message_probs,
            ) = self.mac.forward(batch, t=t, selector_outputs=online_selector_outputs)
            mac_out.append(agent_outs)
            pred_states.append(pred_state)
            pred_metas.append(pred_meta)
            latent_zs.append(latent_z)
            latent_recons.append(latent_recon)
            if student_logits is not None:
                student_logits_seq.append(student_logits)
                student_probs_seq.append(student_probs)
            if message_logits is not None:
                message_logits_seq.append(message_logits)
                message_probs_seq.append(message_probs)

        mac_out = th.stack(mac_out, dim=1)
        pred_states = th.stack(pred_states, dim=1)[:, :-1] 
        pred_metas = th.stack(pred_metas, dim=1)[:, :-1]
        latent_zs = th.stack(latent_zs, dim=1)[:, :-1]
        latent_recons = th.stack(latent_recons, dim=1)[:, :-1]

        chosen_action_qvals = th.gather(mac_out[:, :-1], dim=3, index=actions).squeeze(3)  # Remove the last dim

        target_mac_out = []
        target_selector_outputs = self.target_mac.build_student_selector_outputs(
            batch, agent_inputs=all_agent_inputs
        )
        self.target_mac.init_hidden(batch.batch_size)
        for t in range(batch.max_seq_length):
            target_agent_outs, *_ = self.target_mac.forward(
                batch, t=t, selector_outputs=target_selector_outputs
            )
            target_mac_out.append(target_agent_outs)
        
        target_mac_out = th.stack(target_mac_out[1:], dim=1)

        target_mac_out = target_mac_out.masked_fill(avail_actions[:, 1:] == 0, -9999999)

        # Max over target Q-Values
        if self.args.double_q:
            # Get actions that maximise live Q (for double q-learning)
            mac_out_detach = mac_out.clone().detach()
            mac_out_detach = mac_out_detach.masked_fill(avail_actions == 0, -9999999)
            cur_max_actions = mac_out_detach[:, 1:].max(dim=3, keepdim=True)[1]
            target_max_qvals = th.gather(target_mac_out, 3, cur_max_actions).squeeze(3)
        else:
            target_max_qvals = target_mac_out.max(dim=3)[0]


        # Mix
        if self.mixer is not None:
            chosen_action_qvals = self.mixer(chosen_action_qvals, batch["state"][:, :-1])
            target_max_qvals = self.target_mixer(target_max_qvals, batch["state"][:, 1:])

        if self.args.standardise_returns:
            target_max_qvals = (
                target_max_qvals * th.sqrt(self.ret_ms.var) + self.ret_ms.mean
            )

        targets = (
            rewards + self.args.gamma * (1 - terminated) * target_max_qvals.detach()
        )

        if self.args.standardise_returns:
            self.ret_ms.update(targets)
            targets = (targets - self.ret_ms.mean) / th.sqrt(self.ret_ms.var)


        td_error = chosen_action_qvals - targets.detach()
        mask_td = mask.expand_as(td_error)
        masked_td_error = td_error * mask_td
        loss = (masked_td_error**2).sum() / mask_td.sum()


        state_info = states[:, :, self.important_state]
        state_info_exp = state_info.unsqueeze(2)
        mask_mse = mask.expand_as(state_info) 
        mask_mse_exp = mask_mse.unsqueeze(2)   

        state_pred_loss = (pred_states - state_info_exp) * mask_mse_exp
        state_pred_loss = state_pred_loss ** 2 

        mask_mse_exp = mask_mse_exp.expand_as(state_pred_loss)

        mse_per_agent = (state_pred_loss.sum(dim=(0, 1, 3)) / mask_mse_exp.sum(dim=(0, 1, 3)))
        mse_loss = state_pred_loss.sum() / mask_mse_exp.sum()

        mse_per_state_log = (state_pred_loss.sum(dim=(0, 1, 2)) / mask_mse_exp.sum(dim=(0, 1, 2)))
        
        mse_per_state = (state_pred_loss < self.args.mse_thres).float() 
        bce_elem = -(mse_per_state * pred_metas.clamp(1e-7, 1-1e-7).log() +
                (1 - mse_per_state) * (1 - pred_metas).clamp(1e-7, 1-1e-7).log())
        masked_bce = bce_elem * mask_mse_exp  # (bs, t, n_agents, output_dim)
        meta_loss = masked_bce.sum() / mask_mse_exp.sum() 
        
        consistency_loss = F.mse_loss(latent_zs, latent_recons)
        
        total_mse_loss = self.args.recon_lambda * mse_loss + self.args.meta_lambda * meta_loss + self.args.consistency_lambda * consistency_loss 

        teacher_loss = th.tensor(0.0, device=batch.device)
        sparsity_loss = th.tensor(0.0, device=batch.device)
        teacher_pos_loss = th.tensor(0.0, device=batch.device)
        teacher_neg_loss = th.tensor(0.0, device=batch.device)
        teacher_pos_rate = th.tensor(0.0, device=batch.device)
        teacher_certified_edge_rate = th.tensor(0.0, device=batch.device)
        teacher_weight_mean = th.tensor(1.0, device=batch.device)
        student_forward_rate = th.tensor(0.0, device=batch.device)
        teacher_lambda = 0.0
        what_teacher_loss = th.tensor(0.0, device=batch.device)
        what_coverage_loss = th.tensor(0.0, device=batch.device)
        what_teacher_lambda = 0.0
        student_what_rate = th.tensor(0.0, device=batch.device)
        sparsity_lambda = float(getattr(self.args, "comm_sparsity_lambda", 0.0))
        if student_logits_seq and bool(getattr(self.args, "use_teacher_student_comm", False)):
            student_logits_all = th.stack(student_logits_seq, dim=1)[:, :-1]
            teacher_matrix_all = teacher_matrix_all[:, :-1]
            student_probs_all = th.stack(student_probs_seq, dim=1)[:, :-1]

            offdiag = 1.0 - th.eye(self.n_agents, device=batch.device).view(1, 1, self.n_agents, self.n_agents)
            mask_comm = mask.unsqueeze(2).expand_as(student_logits_all) * offdiag
            bce = F.binary_cross_entropy_with_logits(
                student_logits_all,
                teacher_matrix_all,
                reduction="none",
            )
            teacher_weights = self._teacher_loss_weights(teacher_matrix_all, mask_comm)
            teacher_weight_mean = (teacher_weights * mask_comm).sum() / mask_comm.sum().clamp_min(1.0)
            teacher_loss = (bce * mask_comm * teacher_weights).sum() / (
                mask_comm * teacher_weights
            ).sum().clamp_min(1.0)
            sparsity_loss = (student_probs_all * mask_comm).sum() / mask_comm.sum().clamp_min(1.0)
            teacher_lambda = self._teacher_lambda(t_env)
            pos_mask = mask_comm * (teacher_matrix_all > 0.5).float()
            neg_mask = mask_comm * (teacher_matrix_all <= 0.5).float()
            certified_edge_mask = self._certified_edge_mask_like(teacher_matrix_all)
            certified_pos_mask = pos_mask * certified_edge_mask
            teacher_pos_rate = pos_mask.sum() / mask_comm.sum().clamp_min(1.0)
            teacher_certified_edge_rate = certified_pos_mask.sum() / mask_comm.sum().clamp_min(1.0)
            teacher_pos_loss = (bce * pos_mask).sum() / pos_mask.sum().clamp_min(1.0)
            teacher_neg_loss = (bce * neg_mask).sum() / neg_mask.sum().clamp_min(1.0)
            student_forward_rate = self._student_forward_rate(student_logits_all, student_probs_all, mask_comm)

        if message_logits_seq and bool(getattr(self.args, "use_teacher_student_comm", False)):
            message_logits_all = th.stack(message_logits_seq, dim=1)[:, :-1]
            message_probs_all = th.stack(message_probs_seq, dim=1)[:, :-1]
            teacher_what_core_all = teacher_what_core_all[:, :-1]
            teacher_what_target_all = teacher_what_target_all[:, :-1]

            # WHAT is a per-sender policy. Supervise it at every valid transition,
            # including states where WHO/WHEN currently disable every outgoing
            # edge: otherwise a sender would receive no content supervision until
            # the exact timestep at which it starts communicating.
            mask_what = mask.unsqueeze(2).expand_as(message_logits_all)
            what_bce = F.binary_cross_entropy_with_logits(
                message_logits_all, teacher_what_target_all, reduction="none"
            )
            core = (teacher_what_core_all > 0.5).float()
            supplement = ((teacher_what_target_all > 0.5) & (teacher_what_core_all <= 0.5)).float()
            negative = (teacher_what_target_all <= 0.5).float()
            what_weights = (
                core * float(getattr(self.args, "what_teacher_core_weight", 1.0))
                + supplement * float(getattr(self.args, "what_teacher_supplement_weight", 0.25))
                + negative * float(getattr(self.args, "what_teacher_negative_weight", 0.1))
            )
            what_teacher_loss = (what_bce * what_weights * mask_what).sum() / (
                what_weights * mask_what
            ).sum().clamp_min(1.0)
            what_teacher_lambda = self._what_teacher_lambda(t_env)

            total_dim = message_probs_all.shape[-1]
            eligible_dim = min(self.mac.raw_obs_dim, total_dim)
            eligible = th.arange(total_dim, device=batch.device) < eligible_dim
            excluded = tuple(
                idx for idx in self.mac.non_information_raw_indices if 0 <= idx < total_dim
            )
            if excluded:
                eligible[th.as_tensor(excluded, device=batch.device, dtype=th.long)] = False
            semantic_probs = message_probs_all[..., eligible]
            coverage = semantic_probs.mean(dim=-1)
            min_coverage = float(getattr(self.args, "min_what_coverage", 0.60))
            coverage_penalty = th.relu(min_coverage - coverage).pow(2)
            mask_sender = mask.expand_as(coverage_penalty)
            what_coverage_loss = (coverage_penalty * mask_sender).sum() / mask_sender.sum().clamp_min(1.0)
            student_what_rate = (coverage * mask_sender).sum() / mask_sender.sum().clamp_min(1.0)

        tot_loss = (
            loss + total_mse_loss
            + teacher_lambda * teacher_loss
            + sparsity_lambda * sparsity_loss
            + what_teacher_lambda * what_teacher_loss
            + float(getattr(self.args, "what_coverage_lambda", 0.0)) * what_coverage_loss
        )

        self.optimiser.zero_grad()
        tot_loss.backward()
        message_selector_grad_norm = th.tensor(0.0, device=batch.device)
        if getattr(self.mac, "message_selector", None) is not None:
            grad_sq = [
                parameter.grad.detach().pow(2).sum()
                for parameter in self.mac.message_selector.parameters()
                if parameter.grad is not None
            ]
            if grad_sq:
                message_selector_grad_norm = th.stack(grad_sq).sum().sqrt()
        grad_norm = th.nn.utils.clip_grad_norm_(self.params, self.args.grad_norm_clip)
        self.optimiser.step()
    
                    
        if t_env - self.log_stats_t >= self.args.learner_log_interval:
            self.logger.log_stat("Model_D_loss", total_mse_loss.item(), t_env)
            self.logger.log_stat("Mse_loss", mse_loss.item(), t_env)
            self.logger.log_stat("Meta_loss", meta_loss.item(), t_env)
            self.logger.log_stat("Consistency_loss", consistency_loss.item(), t_env)
            if bool(getattr(self.args, "use_teacher_student_comm", False)):
                self.logger.log_stat("Teacher_comm_loss", teacher_loss.item(), t_env)
                self.logger.log_stat("Teacher_comm_lambda", teacher_lambda, t_env)
                self.logger.log_stat("Teacher_comm_pos_loss", teacher_pos_loss.item(), t_env)
                self.logger.log_stat("Teacher_comm_neg_loss", teacher_neg_loss.item(), t_env)
                self.logger.log_stat("Teacher_comm_pos_rate", teacher_pos_rate.item(), t_env)
                self.logger.log_stat("Teacher_comm_certified_edge_rate", teacher_certified_edge_rate.item(), t_env)
                self.logger.log_stat("Teacher_comm_weight_mean", teacher_weight_mean.item(), t_env)
                self.logger.log_stat("Student_comm_rate", sparsity_loss.item(), t_env)
                self.logger.log_stat("Student_comm_forward_rate", student_forward_rate.item(), t_env)
                self.logger.log_stat("Comm_sparsity_lambda", sparsity_lambda, t_env)
                self.logger.log_stat("Teacher_what_loss", what_teacher_loss.item(), t_env)
                self.logger.log_stat("Teacher_what_lambda", what_teacher_lambda, t_env)
                self.logger.log_stat("What_coverage_loss", what_coverage_loss.item(), t_env)
                self.logger.log_stat("Student_what_soft_rate", student_what_rate.item(), t_env)
                self.logger.log_stat(
                    "Message_selector_grad_norm",
                    message_selector_grad_norm.item(),
                    t_env,
                )

            for i in range(self.n_agents):
                self.logger.log_stat(f"MSE_per_agent_{i}", mse_per_agent[i].item(), t_env)

            for i in range(self.imp_dim):
                self.logger.log_stat(f"Mse_per_state_{self.important_state[i]}", mse_per_state_log[i].item(), t_env)
                
        # Update target
        if self.args.optimiser == "RMSprop":
            if (episode_num - self.last_target_update_episode) / self.args.target_update_interval >= 1.0:
                self._update_targets()
                self.last_target_update_episode = episode_num
        else:
            self.training_steps += 1
            if self.args.target_update_interval_or_tau > 1 and (self.training_steps - self.last_target_update_step) / self.args.target_update_interval_or_tau >= 1.0:
                self._update_targets_hard()
                self.last_target_update_step = self.training_steps
            elif self.args.target_update_interval_or_tau <= 1.0:
                self._update_targets_soft(self.args.target_update_interval_or_tau)

            
        if t_env - self.log_stats_t >= self.args.learner_log_interval:
            self.logger.log_stat("loss", loss.item(), t_env)
            self.logger.log_stat("grad_norm", grad_norm.item(), t_env)
            mask_elems = mask_td.sum().item()
            self.logger.log_stat(
                "td_error_abs", (masked_td_error.abs().sum().item() / mask_elems), t_env
            )
            self.logger.log_stat(
                "q_taken_mean",
                (chosen_action_qvals * mask_td).sum().item()
                / (mask_elems * self.args.n_agents),
                t_env,
            )
            self.logger.log_stat(
                "target_mean",
                (targets * mask_td).sum().item() / (mask_elems * self.args.n_agents),
                t_env,
            )
            self.log_stats_t = t_env

    def _update_targets(self):
        self.target_mac.load_state(self.mac)
        if self.mixer is not None:
            self.target_mixer.load_state_dict(self.mixer.state_dict())
        self.logger.console_logger.info("Updated target network")
        
    def _update_targets_hard(self):
        self.target_mac.load_state(self.mac)
        if self.mixer is not None:
            self.target_mixer.load_state_dict(self.mixer.state_dict())

    def _update_targets_soft(self, tau):
        for target_param, param in zip(self.target_mac.parameters(), self.mac.parameters()):
            target_param.data.copy_(target_param.data * (1.0 - tau) + param.data * tau)
        if self.mixer is not None:
            for target_param, param in zip(self.target_mixer.parameters(), self.mixer.parameters()):
                target_param.data.copy_(target_param.data * (1.0 - tau) + param.data * tau)

    def _teacher_lambda(self, t_env):
        start = float(getattr(self.args, "teacher_lambda", 1.0))
        finish = float(getattr(self.args, "teacher_lambda_finish", start))
        if not bool(getattr(self.args, "teacher_lambda_anneal", True)):
            return start
        anneal_time = float(getattr(self.args, "teacher_lambda_anneal_time", 500000))
        if anneal_time <= 0:
            return finish
        progress = min(max(float(t_env) / anneal_time, 0.0), 1.0)
        return start + progress * (finish - start)

    def _teacher_loss_weights(self, teacher_matrix, mask_comm):
        if not bool(getattr(self.args, "use_certified_teacher_weights", True)):
            return th.ones_like(teacher_matrix)
        mask_comm = mask_comm.expand_as(teacher_matrix)

        mode = str(getattr(self.args, "certified_teacher_weight_mode", "task_facts")).lower()
        pos_weight = float(getattr(self.args, "certified_teacher_positive_weight", 1.0))
        certified_weight = float(getattr(self.args, "certified_teacher_certified_edge_weight", 2.0))
        neg_weight = float(getattr(self.args, "certified_teacher_negative_weight", 1.0))
        weights = th.where(
            teacher_matrix > 0.5,
            th.full_like(teacher_matrix, pos_weight),
            th.full_like(teacher_matrix, neg_weight),
        )
        if mode == "task_facts":
            certified_edges = self._certified_edge_mask_like(teacher_matrix)
            certified_positive = (teacher_matrix > 0.5).float() * certified_edges
            weights = th.where(
                certified_positive > 0.5,
                th.full_like(teacher_matrix, certified_weight),
                weights,
            )
        elif mode != "positive":
            raise ValueError(f"Unknown certified_teacher_weight_mode: {mode}")

        if bool(getattr(self.args, "normalize_certified_teacher_weights", True)):
            mean_weight = (weights * mask_comm).sum() / mask_comm.sum().clamp_min(1.0)
            weights = weights / mean_weight.clamp_min(1e-6)
        return weights

    def _certified_edge_mask_like(self, tensor):
        mask = th.zeros(self.n_agents, self.n_agents, device=tensor.device, dtype=tensor.dtype)
        for receiver, sender in CERTIFIED_TASK_FACT_EDGES.get(self.map_name, []):
            if receiver < self.n_agents and sender < self.n_agents:
                mask[receiver, sender] = 1.0
        shape = [1] * tensor.dim()
        shape[-2:] = [self.n_agents, self.n_agents]
        return mask.view(*shape).expand_as(tensor)

    def _student_forward_rate(self, student_logits, student_probs, mask_comm):
        topk = int(getattr(self.args, "student_comm_topk", 0))
        use_topk = topk > 0 and bool(getattr(self.args, "student_comm_topk_train", False))
        if not use_topk:
            hard_train = bool(getattr(self.args, "student_comm_hard", False))
            if not hard_train:
                return (student_probs * mask_comm).sum() / mask_comm.sum().clamp_min(1.0)
            threshold = float(getattr(self.args, "student_comm_threshold", 0.5))
            hard = (student_probs >= threshold).float()
            return (hard * mask_comm).sum() / mask_comm.sum().clamp_min(1.0)

        topk = max(1, min(topk, self.n_agents - 1))
        eye = th.eye(self.n_agents, device=student_logits.device, dtype=th.bool)
        shape = [1] * student_logits.dim()
        shape[-2:] = [self.n_agents, self.n_agents]
        scores = student_logits.masked_fill(eye.view(*shape), -float("inf"))
        _, indices = scores.topk(topk, dim=-1)
        hard = th.zeros_like(student_probs)
        hard.scatter_(-1, indices, 1.0)
        return (hard * mask_comm).sum() / mask_comm.sum().clamp_min(1.0)

    def _what_teacher_lambda(self, t_env):
        start = float(getattr(self.args, "what_teacher_lambda", 1.0))
        finish = float(getattr(self.args, "what_teacher_lambda_finish", start))
        if not bool(getattr(self.args, "what_teacher_lambda_anneal", True)):
            return start
        anneal_time = max(float(getattr(self.args, "what_teacher_lambda_anneal_time", 500000)), 1.0)
        fraction = min(max(float(t_env) / anneal_time, 0.0), 1.0)
        return start + fraction * (finish - start)

    def _env_map_name(self):
        env_args = getattr(self.args, "env_args", {}) or {}
        if isinstance(env_args, dict):
            return env_args.get("map_name") or env_args.get("key") or "unknown_map"
        return getattr(env_args, "map_name", None) or getattr(env_args, "key", None) or "unknown_map"

    def cuda(self):
        self.mac.cuda()
        self.target_mac.cuda()

        if self.mixer is not None:
            self.mixer.cuda()
            self.target_mixer.cuda()


    def save_models(self, path):
        self.mac.save_models(path)
        if self.mixer is not None:
            th.save(self.mixer.state_dict(), "{}/mixer.th".format(path))
        th.save(self.optimiser.state_dict(), "{}/opt.th".format(path))
        
    def load_models(self, path):
        self.mac.load_models(path)
        # Not quite right but I don't want to save target networks
        self.target_mac.load_models(path)
        if self.mixer is not None:
            self.mixer.load_state_dict(
                th.load(
                    "{}/mixer.th".format(path),
                    map_location=lambda storage, loc: storage,
                )
            )
        self.optimiser.load_state_dict(
            th.load("{}/opt.th".format(path), map_location=lambda storage, loc: storage)
        )
