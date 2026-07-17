from modules.agents import REGISTRY as agent_REGISTRY
from components.action_selectors import REGISTRY as action_REGISTRY
from components.certified_task_facts import CERTIFIED_TASK_FACT_EDGES
from modules.meta import REGISTRY as meta_REGISTRY
from modules.communication import REGISTRY as comm_REGISTRY
import torch as th
import os

import time

class LMAC_MAC:
    def __init__(self, scheme, groups, comm_modules, message_dims, important_state, args):
        self.n_agents = args.n_agents
        self.args = args
        self.map_name = self._env_map_name()
        self.raw_obs_dim = int(scheme["obs"]["vshape"])
        self.non_information_raw_indices = self._non_information_raw_indices()
        input_shape = self._get_input_shape(scheme)

        self.comm_modules = comm_modules
        self.message_dims = message_dims
        self.use_teacher_student_comm = bool(getattr(args, "use_teacher_student_comm", False))

        self.important_state_dim = len(important_state)

        self._build_agents(input_shape + self.args.latent_dim, self.important_state_dim)
        
        self.agent_output_type = args.agent_output_type

        self.action_selector = action_REGISTRY[args.action_selector](args)

        self.hidden_states = None

        self.msg_hidden_states = None
        self.without_msg_hidden_states = None

        self.imp_state = important_state
        self.meta = meta_REGISTRY[args.meta](input_shape + sum(self.message_dims), self.important_state_dim, args)
        if self.use_teacher_student_comm:
            self.comm_selector = comm_REGISTRY["comm_selector"](input_shape, args)
            self.message_selector = comm_REGISTRY["message_selector"](input_shape, args)
        else:
            self.comm_selector = None
            self.message_selector = None

    def __getstate__(self):
        state = self.__dict__.copy()
        # Imported Python modules are not deepcopy/pickle friendly. The target MAC only
        # Teacher labels are produced by the live MAC during learner training.
        state["comm_modules"] = []
        return state
    
    def select_actions(self, ep_batch, t_ep, t_env, bs=slice(None), test_mode=False):
        # Only select actions for the selected batch elements in bs
        avail_actions = ep_batch["avail_actions"][:, t_ep]

        agent_outputs, *_ = self.forward(ep_batch, t_ep, test_mode=test_mode)
        chosen_actions = self.action_selector.select_action(agent_outputs[bs], avail_actions[bs], t_env, test_mode=test_mode)

        return chosen_actions

    def forward(self, ep_batch, t, test_mode=False):
        agent_inputs = self._build_inputs(ep_batch, t)
        agent_inputs_to_No_msg = self._build_inputs(ep_batch, t)
        m_inputs = self._build_time_inputs(ep_batch, t)
        if agent_inputs.shape[0]/ep_batch.batch_size >=1:
            agent_inputs = agent_inputs.reshape(ep_batch.batch_size, self.n_agents, -1)
        else: 
            agent_inputs = agent_inputs.unsqueeze(0)

        if m_inputs.shape[0]/ep_batch.batch_size >=1:
            m_inputs = m_inputs.reshape(ep_batch.batch_size,self.args.time_seq ,self.n_agents, -1)
        else:
            m_inputs = m_inputs.unsqueeze(0)

        student_logits = None
        student_probs = None
        teacher_matrix = None
        message_logits = None
        message_probs = None
        teacher_what_core = None
        teacher_what_target = None

        if self.use_teacher_student_comm:
            teacher_matrix = self._teacher_comm_matrix(agent_inputs)
            student_logits = self.comm_selector(agent_inputs)
            student_probs = th.sigmoid(student_logits)
            comm_matrix = self._student_comm_matrix(student_probs, student_logits, test_mode)
            comm_matrix = self._apply_eval_comm_ablation(comm_matrix, test_mode)
            teacher_what_core = self._teacher_what_mask(agent_inputs)
            teacher_what_target = self._supplement_what_mask(teacher_what_core, agent_inputs)
            message_logits = self.message_selector(agent_inputs)
            message_probs = th.sigmoid(message_logits)
            content_mask = self._student_what_mask(message_probs, message_logits, test_mode)
            phase_messages = self._build_student_gated_messages(
                agent_inputs, m_inputs, comm_matrix, ep_batch.batch_size, content_mask
            )
        else:
            full_matrix = 1.0 - th.eye(self.n_agents, device=agent_inputs.device).unsqueeze(0)
            phase_messages = self._build_student_gated_messages(
                agent_inputs, m_inputs, full_matrix, ep_batch.batch_size, None
            )

        messages = th.cat(phase_messages, dim=-1)

        pred_state_meta_combined, latent_z, self.msg_hidden_states, latent_recon = self.meta(messages, self.msg_hidden_states)
        pred_state, pred_meta = pred_state_meta_combined.split(self.important_state_dim, dim=-1)
        
        pred_state_to_agent = pred_state.detach()
        detach_latent_to_agent = bool(getattr(self.args, "detach_latent_to_agent", True))
        latent_to_agent = latent_z.detach() if detach_latent_to_agent else latent_z
        agent_inputs = th.cat([agent_inputs_to_No_msg, latent_to_agent], dim=-1)
        
        agent_outs, self.hidden_states = self.agent(agent_inputs,self.hidden_states)
        avail_actions = ep_batch["avail_actions"][:, t]

        # Softmax the agent outputs if they're policy logits
        if self.agent_output_type == "pi_logits":

            if getattr(self.args, "mask_before_softmax", True):
                # Make the logits for unavailable actions very negative to minimise their affect on the softmax
                reshaped_avail_actions = avail_actions.reshape(ep_batch.batch_size * self.n_agents, -1)
                agent_outs[reshaped_avail_actions == 0] = -1e10
            agent_outs = th.nn.functional.softmax(agent_outs, dim=-1)
        
        return (
            agent_outs.view(ep_batch.batch_size, self.n_agents, -1),
            pred_state.view(ep_batch.batch_size, self.n_agents, -1),
            pred_meta.view(ep_batch.batch_size, self.n_agents, -1),
            latent_z.view(ep_batch.batch_size, self.n_agents, -1),
            latent_recon.view(ep_batch.batch_size, self.n_agents, -1),
            student_logits,
            teacher_matrix,
            student_probs,
            message_logits,
            teacher_what_core,
            teacher_what_target,
            message_probs,
        )
    
    def init_hidden(self, batch_size):
        self.hidden_states = self.agent.init_hidden().unsqueeze(0).expand(batch_size, self.n_agents, -1)  # bav
        self.msg_hidden_states = self.meta.init_hidden().unsqueeze(0).expand(batch_size, self.n_agents, -1)
    
    def parameters(self):
        params = list(self.agent.parameters()) + list(self.meta.parameters())
        if self.comm_selector is not None:
            params += list(self.comm_selector.parameters())
        if self.message_selector is not None:
            params += list(self.message_selector.parameters())
        return params

    def load_state(self, other_mac):
        self.agent.load_state_dict(other_mac.agent.state_dict())
        self.meta.load_state_dict(other_mac.meta.state_dict())
        other_comm_selector = getattr(other_mac, "comm_selector", None)
        if self.comm_selector is not None and other_comm_selector is not None:
            self.comm_selector.load_state_dict(other_mac.comm_selector.state_dict())
        other_message_selector = getattr(other_mac, "message_selector", None)
        if self.message_selector is not None and other_message_selector is not None:
            self.message_selector.load_state_dict(other_message_selector.state_dict())

    def cuda(self):
        self.agent.cuda()
        self.meta.cuda()
        if self.comm_selector is not None:
            self.comm_selector.cuda()
        if self.message_selector is not None:
            self.message_selector.cuda()

    def save_models(self, path):
        th.save(self.agent.state_dict(), "{}/agent.th".format(path))
        th.save(self.meta.state_dict(), "{}/meta.th".format(path))
        if self.comm_selector is not None:
            th.save(self.comm_selector.state_dict(), "{}/comm_selector.th".format(path))
        if self.message_selector is not None:
            th.save(self.message_selector.state_dict(), "{}/message_selector.th".format(path))

    def load_models(self, path):
        self.agent.load_state_dict(th.load("{}/agent.th".format(path), map_location=lambda storage, loc: storage))
        self.meta.load_state_dict(th.load("{}/meta.th".format(path), map_location=lambda storage, loc: storage))
        selector_path = "{}/comm_selector.th".format(path)
        if self.comm_selector is not None and os.path.exists(selector_path):
            self.comm_selector.load_state_dict(th.load(selector_path, map_location=lambda storage, loc: storage))
        message_selector_path = "{}/message_selector.th".format(path)
        if self.message_selector is not None and os.path.exists(message_selector_path):
            self.message_selector.load_state_dict(
                th.load(message_selector_path, map_location=lambda storage, loc: storage)
            )
        
    def _build_agents(self, input_shape, important_state_dim):
        self.agent = agent_REGISTRY[self.args.agent](input_shape, important_state_dim ,self.args)

    def _teacher_comm_matrix(self, agent_inputs):
        if not self.comm_modules:
            matrix = th.ones(
                agent_inputs.shape[0], self.n_agents, self.n_agents,
                device=agent_inputs.device,
            )
        else:
            module = self.comm_modules[0]
            who = module.communication_who(agent_inputs)
            when = module.communication_when(agent_inputs)
            matrix = who * when
            if not th.is_tensor(matrix):
                matrix = th.as_tensor(matrix, dtype=agent_inputs.dtype, device=agent_inputs.device)
            else:
                matrix = matrix.to(device=agent_inputs.device, dtype=agent_inputs.dtype)
            if matrix.dim() == 4:
                matrix = matrix.mean(dim=-1)
            if matrix.dim() == 2:
                matrix = matrix.unsqueeze(0).expand(agent_inputs.shape[0], -1, -1)

        matrix = matrix.clamp(0.0, 1.0)
        eye = th.eye(self.n_agents, device=agent_inputs.device).unsqueeze(0)
        return matrix * (1.0 - eye)

    def _teacher_what_mask(self, agent_inputs):
        if not self.comm_modules:
            raise RuntimeError("Cannot construct WHAT teacher without a frozen communication module")
        mask = self.comm_modules[0].communication_what(agent_inputs)
        if not th.is_tensor(mask):
            mask = th.as_tensor(mask, device=agent_inputs.device, dtype=agent_inputs.dtype)
        mask = mask.to(device=agent_inputs.device, dtype=agent_inputs.dtype)
        if mask.shape != agent_inputs.shape:
            raise ValueError(f"communication_what mask {mask.shape} != input {agent_inputs.shape}")
        return mask.clamp(0.0, 1.0)

    def _student_comm_matrix(self, student_probs, student_logits, test_mode):
        hard_train = bool(getattr(self.args, "student_comm_hard", False))
        hard_eval = bool(getattr(self.args, "student_comm_hard_eval", False))
        threshold = float(getattr(self.args, "student_comm_threshold", 0.5))
        use_hard = hard_eval if test_mode else hard_train
        topk = int(getattr(self.args, "student_comm_topk", 0))
        topk_train = bool(getattr(self.args, "student_comm_topk_train", False))
        topk_eval = bool(getattr(self.args, "student_comm_topk_eval", False))
        use_topk = topk > 0 and (topk_eval if test_mode else topk_train)
        if use_topk:
            return self._topk_student_comm_matrix(student_probs, student_logits, topk)
        if not use_hard:
            return student_probs

        hard = (student_probs >= threshold).float()
        return hard.detach() - student_probs.detach() + student_probs

    def _topk_student_comm_matrix(self, student_probs, student_logits, topk):
        topk = max(1, min(int(topk), self.n_agents - 1))
        scores = student_logits
        eye = th.eye(self.n_agents, device=student_probs.device, dtype=th.bool).unsqueeze(0)
        scores = scores.masked_fill(eye, -float("inf"))
        _, indices = scores.topk(topk, dim=-1)
        hard = th.zeros_like(student_probs)
        hard.scatter_(-1, indices, 1.0)
        hard = hard * (1.0 - eye.to(student_probs.dtype))
        return hard.detach() - student_probs.detach() + student_probs

    def _apply_eval_comm_ablation(self, comm_matrix, test_mode):
        if not test_mode:
            return comm_matrix
        mode = getattr(self.args, "eval_comm_ablation", "none").lower()
        if mode in ("none", "", "normal"):
            return comm_matrix
        if mode == "zero":
            return th.zeros_like(comm_matrix)
        if mode == "random_same_rate":
            offdiag = 1.0 - th.eye(self.n_agents, device=comm_matrix.device).unsqueeze(0)
            edge_count = offdiag.sum(dim=(1, 2), keepdim=True).clamp_min(1.0)
            rate = (comm_matrix.detach() * offdiag).sum(dim=(1, 2), keepdim=True) / edge_count
            random_edges = (th.rand_like(comm_matrix) < rate).to(comm_matrix.dtype)
            return random_edges * offdiag
        if mode == "drop_certified_edges":
            certified = self._certified_edge_mask(comm_matrix)
            return comm_matrix * (1.0 - certified)
        if mode == "keep_certified_edges":
            certified = self._certified_edge_mask(comm_matrix)
            return comm_matrix * certified
        raise ValueError(f"Unknown eval_comm_ablation mode: {mode}")

    def _certified_edge_mask(self, tensor):
        mask = th.zeros(self.n_agents, self.n_agents, device=tensor.device, dtype=tensor.dtype)
        for receiver, sender in CERTIFIED_TASK_FACT_EDGES.get(self.map_name, []):
            if receiver < self.n_agents and sender < self.n_agents:
                mask[receiver, sender] = 1.0
        return mask.unsqueeze(0).expand_as(tensor)

    def _build_student_gated_messages(
        self, agent_inputs, m_inputs, comm_matrix, batch_size, student_content_mask
    ):
        if not self.comm_modules:
            raise RuntimeError(
                "LMAC_MAC has no communication modules; expected at least one "
                "LLM WHO/WHEN/WHAT teacher module."
            )
        phase_messages = []
        input_dim = agent_inputs.shape[-1]
        for i, module in enumerate(self.comm_modules):
            if i < 2:
                source = agent_inputs
            else:
                source = m_inputs[:, -1]
            if i == 0 and student_content_mask is not None:
                what_mask = student_content_mask
            else:
                what_mask = module.communication_what(source).to(agent_inputs.device)
                if what_mask.shape != source.shape:
                    raise ValueError(f"communication_what mask {what_mask.shape} != input {source.shape}")
                what_mask = self._supplement_what_mask(what_mask, source)
            sender_messages = source * what_mask
            gated_msg = self._aggregate_sender_messages(comm_matrix, sender_messages)
            if i == 0:
                phase_messages.append(th.cat([agent_inputs, gated_msg], dim=-1))
            else:
                phase_messages.append(gated_msg)

        return [msg.reshape(batch_size * self.n_agents, -1) for msg in phase_messages]

    def _student_what_mask(self, probs, logits, test_mode):
        """Hard forward mask with straight-through gradients to MessageSelectNet."""
        total_dim = probs.shape[-1]
        eligible_dim = min(self.raw_obs_dim, total_dim)
        eligible = th.arange(total_dim, device=probs.device) < eligible_dim
        excluded = tuple(idx for idx in self.non_information_raw_indices if 0 <= idx < total_dim)
        if excluded:
            eligible[th.as_tensor(excluded, device=probs.device, dtype=th.long)] = False
        semantic_dim = int(eligible.sum().item())
        coverage = float(getattr(self.args, "min_what_coverage", 0.60))
        k = max(1, min(semantic_dim, int(coverage * semantic_dim + 0.999999)))

        eligible_view = eligible.view(*([1] * (probs.dim() - 1)), total_dim)
        scores = logits.masked_fill(~eligible_view, -float("inf"))
        topk_indices = scores.topk(k, dim=-1).indices
        hard_env = th.zeros_like(probs)
        hard_env.scatter_(-1, topk_indices, 1.0)

        appended = th.arange(total_dim, device=probs.device) >= eligible_dim
        appended = appended.view(*([1] * (probs.dim() - 1)), total_dim)
        hard_appended = (probs >= float(getattr(self.args, "message_selector_threshold", 0.5))).to(probs.dtype)
        hard = hard_env + hard_appended * appended.to(probs.dtype)
        hard = hard.clamp(0.0, 1.0)

        allowed = eligible_view | appended
        soft = probs * allowed.to(probs.dtype)
        if test_mode or bool(getattr(self.args, "message_selector_hard_train", True)):
            return hard.detach() - soft.detach() + soft
        return soft

    def _supplement_what_mask(self, teacher_mask, source):
        """Preserve teacher-important fields and fill RL messages to a minimum width.

        The LLM WHAT policy remains untouched and supplies the semantic core.
        Additional fields are chosen independently for every batch item/sender by
        descending absolute observed value. This is fully tensorized and does not
        alter WHO/WHEN or create a message when no communication edge is active.
        """
        if not bool(getattr(self.args, "enforce_min_what_coverage", False)):
            return teacher_mask
        coverage = float(getattr(self.args, "min_what_coverage", 0.60))
        if not 0.0 <= coverage <= 1.0:
            raise ValueError(f"min_what_coverage must be in [0,1], got {coverage}")

        # Coverage is defined over environment observation features only. Last
        # action and agent-id one-hots appended by _build_inputs are neither
        # counted nor used as filler merely to satisfy the bandwidth floor.
        total_dim = source.shape[-1]
        eligible_dim = min(self.raw_obs_dim, total_dim)
        eligible = th.arange(total_dim, device=source.device) < eligible_dim
        excluded = tuple(idx for idx in self.non_information_raw_indices if 0 <= idx < total_dim)
        if excluded:
            eligible[th.as_tensor(excluded, device=source.device, dtype=th.long)] = False
        eligible = eligible.view(*([1] * (source.dim() - 1)), -1)
        semantic_dim = eligible_dim - len(excluded)
        target_dims = min(semantic_dim, int(coverage * semantic_dim + 0.999999))
        core = teacher_mask > 1e-8
        eligible_core = core & eligible
        core_count = eligible_core.sum(dim=-1, keepdim=True)
        required = (target_dims - core_count).clamp_min(0)

        scores = source.detach().abs().masked_fill(core | (~eligible), float("-inf"))
        order = scores.argsort(dim=-1, descending=True)
        ranks = th.empty_like(order)
        rank_values = th.arange(total_dim, device=source.device, dtype=order.dtype)
        rank_values = rank_values.view(*([1] * (order.dim() - 1)), total_dim).expand_as(order)
        ranks.scatter_(-1, order, rank_values)
        supplement = (ranks < required) & (~core) & eligible
        return th.maximum(teacher_mask.clamp(0.0, 1.0), supplement.to(teacher_mask.dtype))

    def _non_information_raw_indices(self):
        """Known environment-implementation padding, never message content."""
        if self.map_name == "1o_2r_vs_4r" and self.raw_obs_dim == 53:
            return (11, 19, 27, 35)
        return ()

    def _gate_llm_messages(self, comm_matrix, msg_only, message_semantics):
        if message_semantics == "sender":
            return self._aggregate_sender_messages(comm_matrix, msg_only)
        if message_semantics in ("receiver_packed", "packed_receiver", "auto"):
            return self._aggregate_sender_messages(comm_matrix, msg_only)
        if message_semantics != "receiver":
            raise ValueError(
                "llm_message_semantics must be 'receiver', 'receiver_packed', 'auto', or 'sender', "
                f"got {message_semantics}"
            )
        return self._gate_receiver_messages(comm_matrix, msg_only)

    def _gate_receiver_messages(self, comm_matrix, receiver_messages):
        if receiver_messages.shape[-1] == 0:
            return receiver_messages
        # Existing LLM communication functions return enhanced observations where
        # receiver_messages[:, i] is already the message intended for receiver i.
        # The student matrix therefore gates whether receiver i should use that
        # teacher-designed message, instead of treating row i as a sender message.
        receiver_gate = comm_matrix.sum(dim=-1, keepdim=True).clamp(0.0, 1.0)
        return receiver_messages * receiver_gate

    def _aggregate_sender_messages(self, comm_matrix, sender_messages):
        if sender_messages.shape[-1] == 0:
            return sender_messages
        weighted = th.bmm(comm_matrix, sender_messages)
        if bool(getattr(self.args, "normalize_student_messages", True)):
            denom = comm_matrix.sum(dim=-1, keepdim=True).clamp_min(1.0)
            weighted = weighted / denom
        return weighted

    def _build_inputs(self, batch, t):
        # Assumes homogenous agents with flat observations.
        # Other MACs might want to e.g. delegate building inputs to each agent
        bs = batch.batch_size
        inputs = []
        inputs.append(batch["obs"][:, t])  # b1av
        if self.args.obs_last_action:
            if t == 0:
                inputs.append(th.zeros_like(batch["actions_onehot"][:, t]))
            else:
                inputs.append(batch["actions_onehot"][:, t-1])
        if self.args.obs_agent_id:
            inputs.append(th.eye(self.n_agents, device=batch.device).unsqueeze(0).expand(bs, -1, -1))

        inputs = th.cat([x.reshape(bs*self.n_agents, -1) for x in inputs], dim=1)
        return inputs

    def _build_state_inputs(self, batch, t):
        # Assumes homogenous agents with flat observations.
        # Other MACs might want to e.g. delegate building inputs to each agent
        bs = batch.batch_size
        inputs = []
        inputs.append(batch["state"][:, t].unsqueeze(1).repeat(1, self.n_agents, 1))  # b1av
        inputs = th.cat([x.reshape(bs*self.n_agents, -1) for x in inputs], dim=1)
        return inputs

    def _get_input_shape(self, scheme):
        input_shape = scheme["obs"]["vshape"]
        if self.args.obs_last_action:
            input_shape += scheme["actions_onehot"]["vshape"][0]
        if self.args.obs_agent_id:
            input_shape += self.n_agents

        return input_shape

    def _env_map_name(self):
        env_args = getattr(self.args, "env_args", {}) or {}
        if isinstance(env_args, dict):
            return env_args.get("map_name") or env_args.get("key") or "unknown_map"
        return getattr(env_args, "map_name", None) or getattr(env_args, "key", None) or "unknown_map"
    
    def _build_time_inputs(self, batch, t):
        bs = batch.batch_size
        time_seq = self.args.time_seq 
        input_seq = []
        for i in range(t - time_seq + 1, t + 1):
            # observation
            if i < 0:
                obs = th.full_like(batch["obs"][:, 0], fill_value=-1.0)  
            else:
                obs = batch["obs"][:, i] 
            input_seq.append(obs)

            # last action
            if self.args.obs_last_action:
                if i <= 0:
                    last_action = th.full_like(batch["actions_onehot"][:, 0], fill_value=-1.0)
                else:
                    last_action = batch["actions_onehot"][:, i-1]
                input_seq.append(last_action)

            if self.args.obs_agent_id:
                agent_id = th.eye(self.n_agents, device=batch.device).unsqueeze(0).expand(bs, -1, -1)
                input_seq.append(agent_id)

        input_seq = [x.reshape(bs * self.n_agents, -1) for x in input_seq]
        inputs = th.cat(input_seq, dim=1)  
        return inputs
