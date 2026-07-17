## system

You are an expert MARL communication-policy judge. Evaluate the generated policy only from the task spec, code, and interface validation. Return one JSON object only.

## user

Evaluate this pure LLM-generated LMAC communication strategy for SMAC map `5z_vs_1ul`.

Research goal:
- We are testing the capability boundary of LLM-designed communication.
- Do NOT use DRC, decision_sufficient, causally_useful, downstream RL win-rate, or hidden/global state.
- Judge whether the policy gives a plausible pure communication strategy for who, when, and what.

Map spec:
{
  "n_agents": 5,
  "obs_dim": 48,
  "time_seq": 10,
  "task_probes": [
    {
      "name": "ultralisk_position_broadcast",
      "sender": 0,
      "fields": [
        4,
        5,
        6
      ],
      "receivers": [
        1,
        2,
        3,
        4
      ],
      "fact": "ultralisk_visibility_position"
    },
    {
      "name": "health_and_attack_intent_broadcast",
      "sender": 0,
      "fields": [
        34,
        42
      ],
      "receivers": [
        1,
        2,
        3,
        4
      ],
      "fact": "health_and_attack_intent"
    }
  ],
  "required_task_facts": [
    {
      "fact": "ultralisk_visibility_position",
      "sender": 0,
      "fields": [
        4,
        5,
        6
      ],
      "receivers": [
        1,
        2,
        3,
        4
      ],
      "feasibility": "The sender observes Ultralisk visibility and relative position.",
      "necessity": "Other Zealots need shared target localization to maintain surround and avoid isolated attacks.",
      "decision_relevance": "Ultralisk position changes chase, surround, and retreat choices."
    },
    {
      "fact": "health_and_attack_intent",
      "sender": 0,
      "fields": [
        34,
        42
      ],
      "receivers": [
        1,
        2,
        3,
        4
      ],
      "feasibility": "The sender observes the relevant health and attack-intent fields.",
      "necessity": "Receivers need team and intent context to coordinate focus and disengagement.",
      "decision_relevance": "Health and attack intent alter whether agents trade damage or reposition."
    }
  ]
}

Rollout-backed LMAC observation alignment:
{
  "map_name": "5z_vs_1ul",
  "rollout_root": "/data/hp/LLM_Communication/LMAC-new/data",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/5z_vs_1ul/train_traj_0000.pkl"
  ],
  "available": true,
  "n_agents": 5,
  "rollout_obs_dim": 36,
  "documented_obs_dim": 35,
  "extra_obs_dim": 1,
  "episodes": 1,
  "transitions": 151,
  "seq_lengths": [
    151
  ],
  "action_dim": 7,
  "agent_types": [
    "zealot",
    "zealot",
    "zealot",
    "zealot",
    "zealot"
  ],
  "feature_index": {
    "move_north": [
      0,
      1
    ],
    "move_south": [
      1,
      2
    ],
    "move_east": [
      2,
      3
    ],
    "move_west": [
      3,
      4
    ],
    "enemy_0_available": [
      4,
      5
    ],
    "enemy_0_distance": [
      5,
      6
    ],
    "enemy_0_rel_x": [
      6,
      7
    ],
    "enemy_0_rel_y": [
      7,
      8
    ],
    "enemy_0_health": [
      8,
      9
    ],
    "ally_0_visible": [
      9,
      10
    ],
    "ally_0_distance": [
      10,
      11
    ],
    "ally_0_rel_x": [
      11,
      12
    ],
    "ally_0_rel_y": [
      12,
      13
    ],
    "ally_0_health": [
      13,
      14
    ],
    "ally_0_shield": [
      14,
      15
    ],
    "ally_1_visible": [
      15,
      16
    ],
    "ally_1_distance": [
      16,
      17
    ],
    "ally_1_rel_x": [
      17,
      18
    ],
    "ally_1_rel_y": [
      18,
      19
    ],
    "ally_1_health": [
      19,
      20
    ],
    "ally_1_shield": [
      20,
      21
    ],
    "ally_2_visible": [
      21,
      22
    ],
    "ally_2_distance": [
      22,
      23
    ],
    "ally_2_rel_x": [
      23,
      24
    ],
    "ally_2_rel_y": [
      24,
      25
    ],
    "ally_2_health": [
      25,
      26
    ],
    "ally_2_shield": [
      26,
      27
    ],
    "ally_3_visible": [
      27,
      28
    ],
    "ally_3_distance": [
      28,
      29
    ],
    "ally_3_rel_x": [
      29,
      30
    ],
    "ally_3_rel_y": [
      30,
      31
    ],
    "ally_3_health": [
      31,
      32
    ],
    "ally_3_shield": [
      32,
      33
    ],
    "own_health": [
      33,
      34
    ],
    "own_shield": [
      34,
      35
    ],
    "lmac_extra_35": [
      35,
      36
    ]
  },
  "alignment_note": "Use rollout_obs_dim as the true LMAC input dimension. Documented SMAC features keep their original indices. Any lmac_extra_* dimensions are wrapper/config-added features and must not be treated as hidden global state."
}

Interface validation:
{
  "valid": true,
  "map_name": "5z_vs_1ul",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_001/comm_init.py",
  "validation_obs_source": "rollout",
  "validation_obs_dim": 36,
  "documented_obs_dim": 35,
  "message_dim": 36,
  "matrix_edge_rate": 0.2,
  "who_edge_rate": 0.2,
  "when_edge_rate": 1.0,
  "what_dim": 36,
  "matrix_min": 0.0,
  "matrix_max": 1.0
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "5z_vs_1ul",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_001/comm_init.py",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/5z_vs_1ul/train_traj_0000.pkl"
  ],
  "transitions": 151,
  "n_agents": 5,
  "rollout_obs_dim": 36,
  "message_dim": 36,
  "matrix_edge_rate": 0.2,
  "who_edge_rate": 0.2,
  "when_edge_rate": 1.0,
  "message_nonzero_rate": 0.05555555555555555,
  "message_abs_mean": 0.05555555555555555,
  "matrix_min": 0.0,
  "matrix_max": 1.0,
  "risk_flags": []
}

Recent trials:
[
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:46:01+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_000/comm_init.py",
      "documented_obs_dim": 35,
      "map_name": "5z_vs_1ul",
      "matrix_edge_rate": 1.0,
      "matrix_max": 1.0,
      "matrix_min": 0.0,
      "message_dim": 36,
      "valid": true,
      "validation_obs_dim": 36,
      "validation_obs_source": "rollout",
      "what_dim": 36,
      "when_edge_rate": 1.0,
      "who_edge_rate": 1.0
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 36,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:46:01+00:00",
    "valid": true,
    "when_edge_rate": 1.0,
    "who_edge_rate": 1.0
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_000/comm_init.py",
    "failure_analysis": "The who matrix erroneously enables all agents to broadcast to all others, while the task spec designates agent 0 as the sole sender. This introduces excessive communication overhead and dilutes the role-specific information. The when condition triggers on almost any enemy visibility and low health, leading to near-constant sending which can overwhelm learning and lacks adaptive throttling. The what content is largely appropriate but could be trimmed to the required fields.",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 36,
    "next_hypothesis": "Restrict the who matrix so that only agent 0 sends to agents 1–4; set all other edges to zero. In the when logic, consider limiting communication to when own_health drops by a significant threshold or when enemy_0 is first spotted or its position changes notably. For what, match the exact required indices [4,5,6] for position and [34,42]? (though 42 absent) – but as a baseline, send only own_health and enemy_0_health maybe.",
    "rollout_grounding_score": 0.9,
    "score": 0.5,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-11T18:46:48+00:00",
    "valid": true,
    "what_score": 0.7,
    "when_score": 0.6,
    "who_score": 0.3
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:49:01+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_001/comm_init.py",
      "documented_obs_dim": 35,
      "map_name": "5z_vs_1ul",
      "matrix_edge_rate": 0.2,
      "matrix_max": 1.0,
      "matrix_min": 0.0,
      "message_dim": 36,
      "valid": true,
      "validation_obs_dim": 36,
      "validation_obs_source": "rollout",
      "what_dim": 36,
      "when_edge_rate": 1.0,
      "who_edge_rate": 0.2
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_184600/iteration/5z_vs_1ul/20260711_184600/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 0.2,
    "message_dim": 36,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:49:01+00:00",
    "valid": true,
    "when_edge_rate": 1.0,
    "who_edge_rate": 0.2
  }
]

Candidate code:
```python
import torch

def message_design_instruction():
    return (
        "WHO: Only agent 0 sends messages, and only to agents 1-4 (no self-communication). "
        "WHEN: Agent 0 sends when (own_health < 40) OR (enemy_0 is visible AND (dist < 5 OR enemy_0_health < 300)). "
        "WHAT: When triggered, the message carries own_health (index 33) and enemy_0_health (index 8); "
        "all other observation fields are masked to zero."
    )

def communication_who(o):
    """
    Determines which agents are allowed to communicate to which others.
    Input: o – observation tensor, shape (batch_size, n_agents, obs_dim)
    Returns: who_matrix – shape (batch_size, n_agents, n_agents) with values in {0,1}.
             1 indicates that the sender (last dim) is allowed to send to the receiver (middle dim).
    Only agent 0 may send, and only to agents 1..n_agents-1.
    """
    batch_size, n_agents, obs_dim = o.shape
    who_matrix = torch.zeros(batch_size, n_agents, n_agents, device=o.device)
    if n_agents >= 2:
        # receivers indexed 1..n_agents-1, sender index 0
        who_matrix[:, 1:, 0] = 1.0
    return torch.clamp(who_matrix, 0.0, 1.0)

def communication_when(o):
    """
    Determines when each sender is allowed to broadcast.
    Input: o – observation tensor, shape (batch_size, n_agents, obs_dim)
    Returns: when_matrix – shape (batch_size, n_agents, n_agents) with values in {0,1}.
             The condition only depends on the sender's local observation.
             The matrix is used to gate messages: a sender s may send to receiver r
             only if both who_matrix[b, r, s] == 1 and when_matrix[b, r, s] == 1.
    Agent 0 (the only sender) is allowed to send when:
      - own_health < 40, OR
      - enemy_0 is visible AND (distance to enemy_0 < 5 OR enemy_0_health < 300).
    """
    batch_size, n_agents, obs_dim = o.shape
    # Extract relevant features safely
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_distance = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_health = torch.zeros(batch_size, n_agents, 1, device=o.device)

    if obs_dim > 33:
        own_health = o[..., 33:34]        # own_health
    if obs_dim > 4:
        enemy_available = o[..., 4:5]     # enemy_0_available
    if obs_dim > 5:
        enemy_distance = o[..., 5:6]      # enemy_0_distance   (index 5)
    if obs_dim > 8:
        enemy_health = o[..., 8:9]        # enemy_0_health     (index 8)

    # Trigger conditions
    low_health = (own_health < 40.0).float()
    enemy_visible = (enemy_available > 0.5).float()
    close_enemy = (enemy_distance < 5.0).float()
    damaged_enemy = (enemy_health < 300.0).float()

    # Combined trigger: low health OR (enemy visible AND (close or damaged))
    condition_enemy_info = enemy_visible * torch.max(close_enemy, damaged_enemy)
    sender_trigger = torch.max(low_health, condition_enemy_info)   # shape (batch, n_agents, 1)
    sender_trigger = sender_trigger.squeeze(-1)                    # shape (batch, n_agents)

    # Build when matrix: for each (receiver, sender) pair, use the sender's trigger
    when_matrix = sender_trigger.unsqueeze(1).expand(-1, n_agents, -1)  # (batch, n_agents, n_agents)

    # Prevent self‑communication (diagonal zeros)
    mask_self = torch.eye(n_agents, device=o.device).unsqueeze(0).expand(batch_size, -1, -1)
    when_matrix = when_matrix * (1.0 - mask_self)

    return torch.clamp(when_matrix, 0.0, 1.0)

def communication_what(o):
    """
    Determines which observation fields to include in the message.
    Input: o – observation tensor, shape (batch_size, n_agents, obs_dim)
    Returns: what – shape (batch_size, n_agents, obs_dim) with values in {0,1}.
             1 indicates that the corresponding observation value is allowed to be transmitted,
             masked to zero otherwise.
    The same trigger used for *when* is applied: for the sending agent, the allowed fields are
    own_health (index 33) and enemy_0_health (index 8). All other fields are zero.
    """
    batch_size, n_agents, obs_dim = o.shape
    # Extract features (same as communication_when)
    own_health = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_available = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_distance = torch.zeros(batch_size, n_agents, 1, device=o.device)
    enemy_health = torch.zeros(batch_size, n_agents, 1, device=o.device)

    if obs_dim > 33:
        own_health = o[..., 33:34]
    if obs_dim > 4:
        enemy_available = o[..., 4:5]
    if obs_dim > 5:
        enemy_distance = o[..., 5:6]    # correct index for distance
    if obs_dim > 8:
        enemy_health = o[..., 8:9]

    # Same trigger as when
    low_health = (own_health < 40.0).float()
    enemy_visible = (enemy_available > 0.5).float()
    close_enemy = (enemy_distance < 5.0).float()
    damaged_enemy = (enemy_health < 300.0).float()
    condition_enemy_info = enemy_visible * torch.max(close_enemy, damaged_enemy)
    sender_trigger = torch.max(low_health, condition_enemy_info).squeeze(-1)  # (batch, n_agents)

    # Build mask: only indices [33, 8] are set to the sender_trigger value (0 or 1)
    what = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)
    indices = [33, 8]   # own_health, enemy_0_health
    for idx in indices:
        if idx < obs_dim:
            what[:, :, idx] = sender_trigger

    return torch.clamp(what, 0.0, 1.0)

```

Return strict JSON with keys:
{
  "accepted": bool,
  "score": float between 0 and 1,
  "who_score": float between 0 and 1,
  "when_score": float between 0 and 1,
  "what_score": float between 0 and 1,
  "rollout_grounding_score": float between 0 and 1,
  "replacement_readiness": "direct_teacher"|"student_supervision_ready"|"not_ready",
  "failure_analysis": "specific critique of missing or redundant who/when/what logic",
  "improvement_suggestions": "concrete code-level changes for the next revision",
  "expected_effect": "why these changes should improve coordination"
}

Acceptance guideline:
- accepted=true only if who, when, and what are all task-plausible and compact.
- The policy must be grounded in the offline rollout statistics, not only generic SMAC knowledge.
- Favor strategies that could directly replace a fixed communication module and also supervise a learnable selector.
- Penalize all-to-all always-on matrices unless the task truly requires them.
- Penalize messages that merely copy all observations without compact task logic.
