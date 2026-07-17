{
  "policy_hypothesis": "In the 1o_2r_vs_4r map, the Overseer has full vision of all Reapers and serves as an information hub, broadcasting enemy positions and health to the blind Roaches. Roaches additionally coordinate their attack targets by sharing intended target indices, mitigating overkill. The communication policy is deterministic, with rules triggering on relevant observations.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        "overseer"
      ],
      "role_basis": "Flying unit not blocked by the pit, can see all enemies."
    },
    {
      "group_id": "G2",
      "members": [
        "roach",
        "roach"
      ],
      "role_basis": "Ground units blocked by the pit, cannot see enemies initially, rely on Overseer intel."
    }
  ],
  "rules": [
    {
      "rule_id": "R1",
      "requirement_ids": [
        "IR1"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "group:G2",
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
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_*_available is a binary flag (0 or 1); 1 indicates the Overseer currently sees the Reaper."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_rel_x",
          "enemy_0_rel_y",
          "enemy_1_rel_x",
          "enemy_1_rel_y",
          "enemy_2_rel_x",
          "enemy_2_rel_y",
          "enemy_3_rel_x",
          "enemy_3_rel_y"
        ],
        "feature_indices": [
          6,
          7,
          14,
          15,
          22,
          23,
          30,
          31
        ]
      },
      "sender_feasibility": "Overseer's observation includes enemy relative coordinates for all four Reapers because enemy_*_available flags are 1.",
      "receiver_necessity": "Roaches need Reaper positions to compute movement directions around the pit; without this they cannot navigate towards the enemy side.",
      "expected_rollout_behavior": "Overseer continuously broadcasts all enemy positions every step. Roaches receive and use them to move towards the nearest Reaper.",
      "uncertainties": [
        "Coordinates are relative to the Overseer; Roaches must transform them using their own observation of the Overseer's relative position (ally_* features) to get egocentric coordinates.",
        "Reaper movement can make position data stale between updates."
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": [
        "IR2"
      ],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "group:G2",
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
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "Same as R1; Overseer's enemy_*_available=1 triggers health sharing."
        }
      },
      "what": {
        "feature_names": [
          "enemy_0_health",
          "enemy_1_health",
          "enemy_2_health",
          "enemy_3_health"
        ],
        "feature_indices": [
          8,
          16,
          24,
          32
        ]
      },
      "sender_feasibility": "Overseer observes health of each Reaper.",
      "receiver_necessity": "Roaches need health to focus fire on the weakest Reapers, improving elimination speed and reducing incoming damage.",
      "expected_rollout_behavior": "Overseer broadcasts health values. Roaches use them to select the Reaper with lowest health as primary target.",
      "uncertainties": [
        "Health changes dynamically during combat; communicated values may be outdated before the Roach acts."
      ]
    },
    {
      "rule_id": "R3",
      "requirement_ids": [
        "IR3"
      ],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "peer_agents",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "own_health"
        ],
        "feature_indices": [
          50
        ],
        "operator": ">",
        "threshold": 0.0,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "The agent's own health remains positive while alive; this trigger ensures the Roach sends its intention every step it is active."
        }
      },
      "what": {
        "feature_names": [],
        "feature_indices": []
      },
      "sender_feasibility": "The sender Roach can derive an intended target index (0‑3) from its policy (e.g., selecting the Reaper with the lowest received health) and encode it in the communication vector. This index is not a raw observation feature but a computed decision variable.",
      "receiver_necessity": "Receiving Roach uses the target intention to avoid attacking the same Reaper, reducing overkill and improving team damage distribution.",
      "expected_rollout_behavior": "Each Roach sends its currently intended target index at every step. The peer Roach uses this to pick a different target if possible.",
      "uncertainties": [
        "Intended target is not directly observable in the sender's own observation; it relies on a learned encoding from the sender's policy network.",
        "If transmission/decision delay occurs, the sender's actual target may have changed by the time the receiver acts."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Centralized observation via the Overseer creates a single point of information which simplifies Roach decision‑making but may become a bottleneck. Broadcasting all enemy data every step provides robustness against outdated information but increases communication load. Roach intention sharing improves coordination but adds extra communication overhead; the empty 'what' relies on the learning process to encode the target index efficiently."
}
