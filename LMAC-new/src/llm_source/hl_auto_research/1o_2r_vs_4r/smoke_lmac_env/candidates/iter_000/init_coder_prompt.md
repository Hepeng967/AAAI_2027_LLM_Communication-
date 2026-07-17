## system

You are a MARL communication-policy coding agent. Return only one complete Python file in a single ```python code block```.

## user

Design an initial LMAC teacher communication policy for SMAC map `1o_2r_vs_4r`.

Map spec:
{
  "n_agents": 3,
  "obs_dim": 66,
  "time_seq": 10,
  "task_probes": [
    {
      "name": "ally_health_broadcast",
      "sender": 0,
      "fields": [
        50
      ],
      "receivers": [
        1,
        2
      ],
      "fact": "ally_health"
    },
    {
      "name": "enemy_position_health_broadcast",
      "sender": 0,
      "fields": [
        6,
        7,
        8
      ],
      "receivers": [
        1,
        2
      ],
      "fact": "enemy_position_health"
    }
  ],
  "required_task_facts": [
    {
      "fact": "ally_health",
      "sender": 0,
      "fields": [
        50
      ],
      "receivers": [
        1,
        2
      ],
      "feasibility": "The reporting unit observes its own health field.",
      "necessity": "Other agents need team health to coordinate focus fire and avoid over-committing wounded allies.",
      "decision_relevance": "Ally health changes retreat, cover, and attack allocation decisions."
    },
    {
      "fact": "enemy_position_health",
      "sender": 0,
      "fields": [
        6,
        7,
        8
      ],
      "receivers": [
        1,
        2
      ],
      "feasibility": "The sender observes enemy relative position and health fields.",
      "necessity": "Receivers may not observe the same enemy state under partial observability.",
      "decision_relevance": "Enemy position and health determine target selection and movement."
    }
  ]
}

Certified task facts, if available:
{
  "required_task_facts": [
    {
      "fact": "ally_health",
      "sender": 0,
      "fields": [
        50
      ],
      "receivers": [
        1,
        2
      ],
      "feasibility": "The reporting unit observes its own health field.",
      "necessity": "Other agents need team health to coordinate focus fire and avoid over-committing wounded allies.",
      "decision_relevance": "Ally health changes retreat, cover, and attack allocation decisions."
    },
    {
      "fact": "enemy_position_health",
      "sender": 0,
      "fields": [
        6,
        7,
        8
      ],
      "receivers": [
        1,
        2
      ],
      "feasibility": "The sender observes enemy relative position and health fields.",
      "necessity": "Receivers may not observe the same enemy state under partial observability.",
      "decision_relevance": "Enemy position and health determine target selection and movement."
    }
  ]
}

Required functions:
- message_design_instruction() -> str
- communication(o) -> tensor [batch, n_agents, obs_dim + message_dim]
- communication_matrix(o) -> tensor [batch, receiver_agent, sender_agent]

Constraints:
- Use only local observation tensor `o`; do not read global state, files, randomness, trainable parameters, or environment internals.
- Use torch operations and keep the code deterministic.
- Self communication diagonal must be zero.
- Matrix convention: matrix[:, receiver, sender] = 1 means receiver uses sender's message.
- Message content should be sender-observable, receiver-necessary, decision-relevant, and compact.
