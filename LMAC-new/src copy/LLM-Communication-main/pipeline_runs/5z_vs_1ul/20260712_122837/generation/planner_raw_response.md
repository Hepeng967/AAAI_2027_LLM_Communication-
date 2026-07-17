{
  "policy_hypothesis": "Communication of wounded status and relative enemy position by agents whose health falls below 20% enables healthy allies to infer which ally needs protection and roughly its location to draw the Ultralisk's attention, while periodic position sharing can help avoid clustering and coordinate focus fire. Default silence avoids unnecessary overhead.",
  "agent_groups": [
    {
      "group_id": "G1",
      "members": "0,1,2,3,4",
      "role_basis": "All agents are homogeneous Zealots that must coordinate health management and tactical positioning. Roles dynamically split into 'healthy' (health >= 20%) and 'wounded' (health < 20%)."
    }
  ],
  "rules": [
    {
      "rule_id": "R1",
      "requirement_ids": ["IR1", "IR2"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all_other_agents",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["own_health"],
        "feature_indices": [33],
        "operator": "<",
        "threshold": 20.0,
        "threshold_basis": {
          "type": "documented_semantics",
          "evidence": "Task description explicitly states Zealot must retreat when health < 20%"
        }
      },
      "what": {
        "feature_names": ["own_health", "enemy_0_rel_x", "enemy_0_rel_y"],
        "feature_indices": [33, 6, 7]
      },
      "sender_feasibility": "Agent can directly observe own_health and enemy_0_rel_x/y from its local observation vector. Feasible.",
      "receiver_necessity": "Healthy agents need to know wounded ally's health to decide protective engagement, and its enemy-relative position to approximate its location and direct their actions. However, coordinate transformation may be problematic; still useful as a directional cue.",
      "expected_rollout_behavior": "When an agent's health falls below 20, it broadcasts its health and the relative position of the Ultralisk. Other agents, upon receiving the message, interpret the sender as wounded and may use the enemy position to orient themselves to draw attention, or to avoid clustering with the retreating ally. The communication enables dynamic role assignment (wounded vs healthy).",
      "uncertainties": [
        "Communication delay may cause stale health status",
        "Visibility of the wounded agent may be restored before the message is fully propagated",
        "Threshold is fixed but rapid health changes may cause toggling",
        "Coordinate frame misalignment: receiver cannot directly map sender's enemy_0_rel_x/y to its own frame without absolute positions, making positional information ambiguous and potentially unusable",
        "Ultralisk movement makes reported relative position quickly outdated"
      ]
    },
    {
      "rule_id": "R2",
      "requirement_ids": ["IR2"],
      "who": {
        "sender_group": "G1",
        "receiver_selector": "all_other_agents",
        "observable_basis": []
      },
      "when": {
        "feature_names": ["enemy_0_available"],
        "feature_indices": [4],
        "operator": "==",
        "threshold": 1.0,
        "threshold_basis": {
          "type": "binary_semantics",
          "evidence": "Enemy availability is a binary flag (1 = visible, 0 = not visible)."
        }
      },
      "what": {
        "feature_names": ["enemy_0_rel_x", "enemy_0_rel_y"],
        "feature_indices": [6, 7]
      },
      "sender_feasibility": "All agents observe enemy_0_available and enemy_0_rel_x/y when available. Sending is feasible.",
      "receiver_necessity": "Knowing the enemy-relative positions of allies (via their transmitted enemy_0_rel_x/y) may help infer ally locations to avoid clustering and to focus fire on the Ultralisk, though coordinate frame misalignment limits direct utility.",
      "expected_rollout_behavior": "Every agent with a visible Ultralisk periodically broadcasts its relative position to all others. While this may not provide exact ally coordinates, it offers directional cues that can be used heuristically to spread out and orient attacks.",
      "uncertainties": [
        "Coordinate frame misalignment renders the received relative positions not directly usable for exact positioning",
        "High communication frequency may add overhead without proportional coordination gain",
        "Ultralisk movement quickly makes posted positions stale"
      ]
    }
  ],
  "default_behavior": "no communication",
  "design_tradeoffs": "R2's frequent position broadcasting could aid clustering avoidance and focus fire coordination but adds communication overhead and may be ineffective due to coordinate frame misalignment. R1's health alert is critical for health management and is triggered sparingly. Sparse communication reduces message frequency but may miss multi-agent wounding events. Overall, the policy prioritizes health-based coordination while attempting to mitigate positional uncertainty."
}