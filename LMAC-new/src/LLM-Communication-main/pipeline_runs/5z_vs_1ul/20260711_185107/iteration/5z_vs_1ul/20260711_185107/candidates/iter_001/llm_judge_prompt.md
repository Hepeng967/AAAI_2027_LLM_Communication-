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
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_001/comm_init.py",
  "validation_obs_source": "rollout",
  "validation_obs_dim": 36,
  "documented_obs_dim": 35,
  "message_dim": 36,
  "matrix_edge_rate": 0.2,
  "who_edge_rate": 0.2,
  "when_edge_rate": 0.2,
  "what_dim": 36,
  "matrix_min": 0.0,
  "matrix_max": 1.0
}

Rollout evaluation:
{
  "valid": true,
  "map_name": "5z_vs_1ul",
  "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_001/comm_init.py",
  "files": [
    "/data/hp/LLM_Communication/LMAC-new/data/5z_vs_1ul/train_traj_0000.pkl"
  ],
  "transitions": 151,
  "n_agents": 5,
  "rollout_obs_dim": 36,
  "message_dim": 36,
  "matrix_edge_rate": 0.2,
  "who_edge_rate": 0.2,
  "when_edge_rate": 0.2,
  "message_nonzero_rate": 0.013760117733627668,
  "message_abs_mean": 0.013760117733627668,
  "matrix_min": 0.0,
  "matrix_max": 1.0,
  "risk_flags": []
}

Recent trials:
[
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:51:08+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_000/comm_init.py",
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
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_000/comm_init.py",
    "failure_analysis": "",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 36,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:51:08+00:00",
    "valid": true,
    "when_edge_rate": 1.0,
    "who_edge_rate": 1.0
  },
  {
    "accepted": false,
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_000/comm_init.py",
    "failure_analysis": "Who matrix is all‑to‑all (off‑diagonal) for all agents, ignoring the task spec where only agent 0 needs to broadcast to others. When triggers for any agent that sees the enemy or has low health, causing excessive and redundant communication from all Zealots. What sends a superset of enemy features (availability, distance, relative coordinates, health) and own health/shield, but the spec requires a precise separation: only fields [4,5,6] for the Ultralisk position and [34,42] for health and attack intent; field 42 is not present in rollout observations and own_shield (34) is not sent in the ‘healthy’ trigger case, reducing consistency.",
    "iteration": 0,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 1.0,
    "message_dim": 36,
    "next_hypothesis": "Narrow who to sender 0 only. For when, restrict the position broadcast to enemy visibility, and the health/intent broadcast to a meaningful event (e.g. health change or threshold). For what, split strictly: position broadcast sends only indices [4,5,6]; health/intent broadcast sends indices [33,34] (own_health, own_shield). Handle the missing field 42 by noting that attack intent may not be directly observable in this rollout; a separate binary feature or proxy could be introduced if required, but the current design should at least align with available features.",
    "rollout_grounding_score": 0.9,
    "score": 0.4,
    "stage": "llm_judge",
    "status": "rejected",
    "timestamp": "2026-07-11T18:51:57+00:00",
    "valid": true,
    "what_score": 0.4,
    "when_score": 0.5,
    "who_score": 0.1
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "next_hypothesis": "Ask LLM judge to evaluate who/when/what.",
    "stage": "interface_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:53:24+00:00",
    "valid": true,
    "validation": {
      "comm_code": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_001/comm_init.py",
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
      "when_edge_rate": 0.2,
      "who_edge_rate": 0.2
    }
  },
  {
    "candidate": "/data/hp/LLM_Communication/LMAC-new/src/LLM-Communication-main/pipeline_runs/5z_vs_1ul/20260711_185107/iteration/5z_vs_1ul/20260711_185107/candidates/iter_001/comm_init.py",
    "failure_analysis": "",
    "iteration": 1,
    "map_name": "5z_vs_1ul",
    "matrix_edge_rate": 0.2,
    "message_dim": 36,
    "next_hypothesis": "Ask LLM judge to evaluate rollout-grounded who/when/what.",
    "stage": "rollout_validation",
    "status": "pass",
    "timestamp": "2026-07-11T18:53:24+00:00",
    "valid": true,
    "when_edge_rate": 0.2,
    "who_edge_rate": 0.2
  }
]

Candidate code:
```python
import torch

def message_design_instruction():
    return (
        "WHO: Only the designated sender (agent 0) communicates; it broadcasts to all "
        "other agents (agents 1–4). No self‑communication and no communication from other agents. "
        "WHEN: Agent 0 sends a message only when (a) the enemy (Ultralisk) is visible (field 4 > 0.5), "
        "or (b) its own health falls below 20 (field 33 < 20). The two conditions are OR‑combined. "
        "WHAT: If the enemy is visible AND own health ≥ 20, send only the enemy position subset: "
        "fields [4,5,6] (enemy_0_available, enemy_0_distance, enemy_0_rel_x). "
        "If own health < 20, send the own health status subset: fields [33,34] (own_health, own_shield). "
        "If both conditions are true (visible enemy while already low health), both subsets are sent. "
        "Otherwise no message is generated (all‑zero mask). "
        "All decisions are deterministic and based solely on agent 0's local observation."
    )

def communication_who(o):
    """
    Returns a who matrix of shape (batch, n_agents, n_agents) where
    who[b, r, s] = 1.0 iff s == 0 and r != 0, else 0.0.
    Only agent 0 is allowed to send, and it broadcasts to all other agents (no self‑loop).
    """
    batch_size, n_agents, _ = o.shape
    who = torch.zeros(batch_size, n_agents, n_agents, device=o.device)
    # sender = 0 broadcasts to all receivers except itself
    who[:, :, 0] = 1.0                          # all receivers get 1 for sender 0
    # zero out the diagonal (r == s)
    diag_mask = torch.eye(n_agents, device=o.device).bool().unsqueeze(0)  # (1, n, n)
    who = who.masked_fill(diag_mask, 0.0)
    return who

def communication_when(o):
    """
    Returns a when matrix of shape (batch, n_agents, n_agents) where
    when[b, r, s] = 1.0 iff s == 0, r != 0, and agent 0’s observation triggers sending.
    Trigger condition: enemy_0_available (index 4) > 0.5 OR own_health (index 33) < 20.0.
    """
    batch_size, n_agents, obs_dim = o.shape
    # Safely extract agent 0's observations
    enemy_available = o[:, 0, 4] if obs_dim > 4 else torch.zeros(batch_size, device=o.device)
    own_health = o[:, 0, 33] if obs_dim > 33 else torch.zeros(batch_size, device=o.device)

    # Trigger flags for agent 0
    trigger = ((enemy_available > 0.5) | (own_health < 20.0)).float()  # (batch,)
    # Expand to (batch, n_agents, 1) so it applies to sender dimension
    when = torch.zeros(batch_size, n_agents, n_agents, device=o.device)
    when[:, :, 0] = trigger.unsqueeze(1)         # all receivers get trigger status for sender 0
    # Remove self‑communication (diagonal)
    diag_mask = torch.eye(n_agents, device=o.device).bool().unsqueeze(0)
    when = when.masked_fill(diag_mask, 0.0)
    return when

def communication_what(o):
    """
    Returns a mask of shape (batch, n_agents, obs_dim) where
    for sender 0:
      - if enemy_0_available > 0.5 AND own_health >= 20: enable indices [4,5,6]
      - if own_health < 20: enable indices [33,34]
      - if both (visible enemy and health < 20): enable both sets
      - otherwise: all zeros.
    All other agents’ masks are left zero.
    """
    batch_size, n_agents, obs_dim = o.shape
    what = torch.zeros(batch_size, n_agents, obs_dim, device=o.device)

    # --- compute conditions for agent 0 per batch item ---
    enemy_avail_0 = o[:, 0, 4] if obs_dim > 4 else torch.zeros(batch_size, device=o.device)
    own_health_0   = o[:, 0, 33] if obs_dim > 33 else torch.zeros(batch_size, device=o.device)

    enemy_visible = enemy_avail_0 > 0.5   # bool
    health_low    = own_health_0 < 20.0    # bool

    # Position subset: [4,5,6] (enemy_0_available, distance, rel_x)
    pos_indices = [4, 5, 6]
    # Health subset: [33,34] (own_health, own_shield)
    health_indices = [33, 34]

    # Filter to valid indices
    valid_pos = [idx for idx in pos_indices if idx < obs_dim]
    valid_health = [idx for idx in health_indices if idx < obs_dim]

    for b in range(batch_size):
        mask = torch.zeros(obs_dim, device=o.device)
        ev, hl = enemy_visible[b], health_low[b]

        if ev and not hl:
            # send only position
            mask[valid_pos] = 1.0
        elif hl:
            # send health (and if also enemy_visible, we add position as well)
            mask[valid_health] = 1.0
            if ev:  # both sets
                mask[valid_pos] = 1.0
        # else: mask stays zero

        what[b, 0, :] = mask   # only agent 0 gets a mask; others remain zero

    return what

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
