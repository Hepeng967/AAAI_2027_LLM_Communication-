{
  "policy_hypothesis": "Overseer broadcasts Roach position to all Banelings when it sees the Roach, enabling direct approach. Banelings relay positions of visible allies back to Overseer to help Overseer move closer to distant Baneling clusters.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [10],
      "role_basis": "Overseer, can detect Roach and observe all agents."
    },
    {
      "group_id": "G2",
      "members": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
      "role_basis": "Banelings, cannot directly see Roach, rely on communication."
    }
  ],
  "rules": [
    {
      "rule_id": "R1",
      "requirement_ids": ["IR1"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all members of G2",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_0_available"],
        "feature_indices": [4],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "enemy_0_available is a binary flag indicating Roach is visible in observation range."
        }
      },
      "what": {
        "feature_names": ["enemy_0_rel_x", "enemy_0_rel_y", "enemy_0_distance"],
        "feature_indices": [6, 7, 5]
      },
      "sender_feasibility": "Overseer always observes enemy_0_available and its components when available.",
      "receiver_necessity": "Banelings need Roach position to navigate and attack; without this they cannot complete task.",
      "expected_rollout_behavior": "When Overseer sees Roach, it continuously broadcasts Roach position; Banelings receiving this (if they also see Overseer) compute attack path.",
      "uncertainties": [
        "Only useful if Baneling can observe Overseer to perform coordinate transformation; otherwise message discarded.",
        "Communication delay and Roach movement may make info stale quickly."
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": ["IR3"],
      "who": {
        "sender_group": "G2",
        "receiver_selector": "all members of G1",
        "observable_basis": []
      },
      "when": {
        "feature_names": [
          "ally_0_visible",
          "ally_1_visible",
          "ally_2_visible",
          "ally_3_visible",
          "ally_4_visible",
          "ally_5_visible",
          "ally_6_visible",
          "ally_7_visible",
          "ally_8_visible",
          "ally_9_visible"
        ],
        "feature_indices": [11, 18, 25, 32, 39, 46, 53, 60, 67, 74],
        "operator": "max",
        "threshold": 0.5,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "Each ally_i_visible is 1 if that ally is currently observable by sender. max > 0.5 triggers when at least one ally is visible."
        }
      },
      "what": {
        "feature_names": ["ally_0_rel_x", "ally_0_rel_y"],
        "feature_indices": [13, 14]
      },
      "sender_feasibility": "Baneling can always observe its own ally visibility and corresponding relative coordinates.",
      "receiver_necessity": "Overseer needs to know positions of Banelings not directly visible to itself, to navigate towards them and extend communication coverage.",
      "expected_rollout_behavior": "Banelings broadcast position of first visible ally; Overseer aggregates to estimate unseen Baneling positions and moves to connect them.",
      "uncertainties": [
        "The relayed position is relative to sender; Overseer must know sender's own relative position to compute absolute location, possible if sender is visible.",
        "Only first ally slot transmitted; may miss other visible allies, but serves as sample.",
        "No explicit agent identity in relay; Overseer must associate sender identity with its own ally tracking to infer which Baneling is reported."
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "Overseer broadcasts continuously which may lead to high bandwidth, but necessary for real-time Roach tracking. Baneling ally relay attempts to improve Overseer's movement planning, but relayed position may be outdated or ambiguous. IR2 (Baneling-to-Baneling relay of Roach position) is unsupported due to lack of memory for estimated Roach position."
}