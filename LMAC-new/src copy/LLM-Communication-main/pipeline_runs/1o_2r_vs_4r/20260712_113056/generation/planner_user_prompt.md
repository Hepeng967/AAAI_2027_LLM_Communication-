
Task and aligned observation description:
The map is 1o_2r_vs_4r. There is a large pit in the center of the map, dividing the battlefield into two sides. At the beginning of each episode, the Overseer and 2 Roaches spawn on one side, while 4 Reapers spawn on the other. The pit blocks direct movement and vision, so Roaches must rely on communication from the Overseer to locate and attack the Reapers. This scenario tests communication and coordination under significant terrain constraints.Observation information for map '1o_2r_vs_4r':
- Each agent observes a vector of length 49.
- There are 3 agents. Their types are: overseer, roach, roach.
- Each row of the observation corresponds to agent_id: [0, 1, 2], and their types: ['overseer', 'roach', 'roach'].
- The observation vector is composed as follows (index: feature):
    - 0: move_north
    - 1: move_south
    - 2: move_east
    - 3: move_west
    - 4: enemy_0_available
    - 5: enemy_0_distance
    - 6: enemy_0_rel_x
    - 7: enemy_0_rel_y
    - 8: enemy_0_health
    - 9: enemy_0_type_0
    - 10: enemy_0_type_1
    - 11: enemy_1_available
    - 12: enemy_1_distance
    - 13: enemy_1_rel_x
    - 14: enemy_1_rel_y
    - 15: enemy_1_health
    - 16: enemy_1_type_0
    - 17: enemy_1_type_1
    - 18: enemy_2_available
    - 19: enemy_2_distance
    - 20: enemy_2_rel_x
    - 21: enemy_2_rel_y
    - 22: enemy_2_health
    - 23: enemy_2_type_0
    - 24: enemy_2_type_1
    - 25: enemy_3_available
    - 26: enemy_3_distance
    - 27: enemy_3_rel_x
    - 28: enemy_3_rel_y
    - 29: enemy_3_health
    - 30: enemy_3_type_0
    - 31: enemy_3_type_1
    - 32: ally_0_visible
    - 33: ally_0_distance
    - 34: ally_0_rel_x
    - 35: ally_0_rel_y
    - 36: ally_0_health
    - 37: ally_0_type_0
    - 38: ally_0_type_1
    - 39: ally_1_visible
    - 40: ally_1_distance
    - 41: ally_1_rel_x
    - 42: ally_1_rel_y
    - 43: ally_1_health
    - 44: ally_1_type_0
    - 45: ally_1_type_1
    - 46: own_health
    - 47: own_type_0
    - 48: own_type_1

LMAC rollout observation alignment:
- Runtime LMAC observation vector length: 49.
- Documented SMAC observation vector length: 49.
- Rollout available: False from /data/hp/LLM_Communication/LMAC-new/data.
- Use runtime obs_shape for generated code and tests.
- Dimensions named lmac_extra_* are wrapper/config-added features; do not treat them as hidden global state.


Information-requirement analysis:
{
  "task_decisions": [
    {
      "decision_id": "D1",
      "decision": "Roach selects a target enemy and decides movement direction (and attack) to engage.",
      "locally_missing_information": [
        "Enemy relative position (rel_x, rel_y) and distance for each active reaper.",
        "Enemy health for each active reaper.",
        "Enemy availability status per slot."
      ]
    },
    {
      "decision_id": "D2",
      "decision": "Roach decides whether to focus attacks with the other roach or split targets to optimize damage.",
      "locally_missing_information": [
        "The other roach's currently targeted enemy index or intended target.",
        "The other roach's distance to its target (requires enemy position to compute locally if enemy info is available)."
      ]
    },
    {
      "decision_id": "D3",
      "decision": "Overseer decides which subset of enemy information to transmit to roaches and at which frequency.",
      "locally_missing_information": [
        "Roaches' current knowledge or belief about enemy states (e.g., what they already know).",
        "Roaches' intended actions or movement targets."
      ]
    }
  ],
  "agent_groups": [
    {
      "group_id": "G1",
      "members": [
        0
      ],
      "role_basis": "Overseer (agent 0) is a flying unit; on map 1o_2r_vs_4r it can see across the central pit and observe all four reapers. Its observation vector likely contains valid enemy features."
    },
    {
      "group_id": "G2",
      "members": [
        1,
        2
      ],
      "role_basis": "Roaches (agents 1,2) are ground units; the pit blocks both movement and vision, so they cannot directly observe enemies across the pit. Their enemy feature slots are expected to be zeroed out (available=0). They can observe each other and the overseer because they spawn on the same side."
    }
  ],
  "information_requirements": [
    {
      "requirement_id": "IR1",
      "fact": "Real-time position and health of each reaper (enemy units) that roaches need to navigate to and attack.",
      "possible_sender_groups": [
        "G1"
      ],
      "possible_receiver_groups": [
        "G2"
      ],
      "sender_observable_features": [
        {
          "name": "enemy_0_available",
          "index": 4
        },
        {
          "name": "enemy_0_distance",
          "index": 5
        },
        {
          "name": "enemy_0_rel_x",
          "index": 6
        },
        {
          "name": "enemy_0_rel_y",
          "index": 7
        },
        {
          "name": "enemy_0_health",
          "index": 8
        },
        {
          "name": "enemy_1_available",
          "index": 11
        },
        {
          "name": "enemy_1_distance",
          "index": 12
        },
        {
          "name": "enemy_1_rel_x",
          "index": 13
        },
        {
          "name": "enemy_1_rel_y",
          "index": 14
        },
        {
          "name": "enemy_1_health",
          "index": 15
        },
        {
          "name": "enemy_2_available",
          "index": 18
        },
        {
          "name": "enemy_2_distance",
          "index": 19
        },
        {
          "name": "enemy_2_rel_x",
          "index": 20
        },
        {
          "name": "enemy_2_rel_y",
          "index": 21
        },
        {
          "name": "enemy_2_health",
          "index": 22
        },
        {
          "name": "enemy_3_available",
          "index": 25
        },
        {
          "name": "enemy_3_distance",
          "index": 26
        },
        {
          "name": "enemy_3_rel_x",
          "index": 27
        },
        {
          "name": "enemy_3_rel_y",
          "index": 28
        },
        {
          "name": "enemy_3_health",
          "index": 29
        }
      ],
      "receiver_need_hypothesis": "Roaches must decide movement and attack actions (D1). Without enemy positions and health, they cannot locate or prioritise targets. The overseer is the only agent with sight across the pit, so roaches need this information via communication.",
      "task_decision_ids": [
        "D1"
      ],
      "uncertainties": [
        "Assumes enemy slot ordering is consistent across agents (based on unit IDs) so that roaches can reference communicated enemies by index.",
        "Assumes overseer vision covers all four reapers at all times (no occlusion or range limitation)."
      ]
    }
  ],
  "unsupported_assumptions": [
    "Coordination of target selection among roaches (D2) may require sharing intended target indices or intended actions. However, no observation feature captures an agent's own intended action, last action, or current target. Such information is not directly observable by any agent and cannot be derived from the given observation vector. Communication of these intentions would require additional internal-state features (e.g., one-hot of own action or target) that are not present.",
    "The overseer's decision about what to communicate (D3) depends on roaches' knowledge state, which cannot be observed. This is a classic epistemic gap; the observation vector provides no feature indicating another agent's observation content or beliefs."
  ]
}

Return this policy schema:
{
  "policy_hypothesis":"...",
  "agent_groups":[...],
  "rules":[
    {"rule_id":"R1","requirement_ids":["IR1"],
      "who":{"sender_group":"G1","receiver_selector":"...","observable_basis":[]},
      "when":{"feature_names":["..."],"feature_indices":[0],"operator":"...",
        "threshold":0.0,"threshold_basis":{"type":"binary_semantics|documented_semantics|rollout_distribution|relative_comparison|llm_hypothesis","evidence":"..."}},
      "what":{"feature_names":["..."],"feature_indices":[0]},
      "sender_feasibility":"...","receiver_necessity":"...",
      "expected_rollout_behavior":"...","uncertainties":[]}
  ],
  "default_behavior":"no communication",
  "design_tradeoffs":"..."
}
Feature indices must match the supplied aligned schema. Do not invent runtime
fields. A threshold without a documented or observed basis must be explicitly
labelled llm_hypothesis. Prefer no communication only as a default, not as a
hard-coded claim that sparse communication is always superior.
