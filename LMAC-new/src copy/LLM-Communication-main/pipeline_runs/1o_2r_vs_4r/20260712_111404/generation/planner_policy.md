{
  "policy_hypothesis": "The Overseer communicates full enemy state (availability, relative position, health) whenever any enemy is observed, enabling Roaches to locate, approach, and efficiently attack Reapers despite the vision-blocking pit.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "agent_0 (overseer)",
      "role_basis": "Only agent with vision across the central pit; enemy features are observable."
    },
    {
      "group_id": "G2",
      "members": "agent_1 (roach), agent_2 (roach)",
      "role_basis": "Ground attackers that cannot see enemies across the pit; must rely on communication for enemy information."
    }
  ],
  "rules": [
    {
      "rule_id": "R1",
      "requirement_ids": [
        "IR1",
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "enemy_0_available"
        ],
        "feature_indices": [
          4
        ],
        "operator": ">",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_0_available is 0 if no enemy, 1 if an enemy exists in that slot; >0 triggers even if slot 0 is not the only enumerated enemy, ensuring communication when any enemy is alive."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_available",
          "enemy_0_rel_x",
          "enemy_0_rel_y",
          "enemy_0_health",
          "enemy_1_available",
          "enemy_1_rel_x",
          "enemy_1_rel_y",
          "enemy_1_health",
          "enemy_2_available",
          "enemy_2_rel_x",
          "enemy_2_rel_y",
          "enemy_2_health",
          "enemy_3_available",
          "enemy_3_rel_x",
          "enemy_3_rel_y",
          "enemy_3_health"
        ],
        "feature_indices": [
          4,
          6,
          7,
          8,
          11,
          13,
          14,
          15,
          18,
          20,
          21,
          22,
          25,
          27,
          28,
          29
        ]
      },
      "sender_feasibility": "Overseer directly observes all these features from its own observation vector.",
      "receiver_necessity": "Without this communication, Roaches have no knowledge of any enemy position or health and cannot perform task D1 (move toward enemy) or D2 (select which enemy to attack).",
      "expected_rollout_behavior": "Roaches will receive the Overseer-relative enemy coordinates. If they can also observe the Overseer (ally_*_visible), they can transform coordinates to own-relative frames. They will then move toward the nearest or weakest Reaper and attack, using health for focus-fire decisions.",
      "uncertainties": [
        "Coordinate transformation requires a Roach to see the Overseer; if out of sight, relative positions become unusable.",
        "Enemy slots are not ID‑stable; the same physical enemy may appear in different indices across timesteps, causing targeting errors.",
        "Communication latency may cause stale health values if a Reaper is damaged between message sending and Roach action."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "This policy prioritises full enemy‑state broadcast whenever any enemy exists, sacrificing bandwidth for completeness. Roach‑to‑Roach coordination (IR3) is not included because the Roaches have no observable trigger in their own observation to send a target intention; the policy relies on implicit coordination through movement and health‑based prioritisation."
}
